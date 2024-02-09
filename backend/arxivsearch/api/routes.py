import asyncio
import os
import numpy as np
import logging
from typing import List, Dict, Any

from fastapi import APIRouter
from redis.asyncio import Redis

from redisvl.index import AsyncSearchIndex
from redisvl.schema import IndexSchema
from redisvl.query import VectorQuery, FilterQuery, CountQuery
from redisvl.query.filter import Tag, FilterExpression

from arxivsearch import config
from arxivsearch.embeddings import Embeddings
from arxivsearch.schema import (
    PaperSimilarityRequest,
    UserTextSimilarityRequest
)


logger = logging.getLogger(__name__)

# Initialize the API router
router = APIRouter()

# Initialize embeddings and paper vector field name
embeddings = Embeddings()

# Preload Redis connection details
client = Redis.from_url(config.REDIS_URL)

# Preload index schema
schema = IndexSchema.from_yaml(os.path.join("./schema", "index.yaml"))


def process_paper(paper: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process paper data and calculate similarity score.

    Args:
        paper: Input paper data.

    Returns:
        dict: Processed paper data with similarity score.
    """
    if 'vector_distance' in paper:
        paper['similarity_score'] = 1 - float(paper['vector_distance'])
    return paper


def build_filter_expression(years: List[int], categories: List[str]) -> FilterExpression:
    """
    Construct a filter expression based on the provided years and categories.

    Args:
        years (list): A list of years (integers or strings) to be included in
            the filter expression. An empty list means there's no filter applied
            based on years.
        categories (list): A list of category strings to be included in the
            filter expression. An empty list means there's no filter applied
            based on categories.

    Returns:
        FilterExpression: A FilterExpression object representing the combined
            filter for both years and categories.
    """
    year_filter = Tag("year") == [str(year) for year in years if year]
    category_filter = Tag("categories") == [str(category) for category in categories if category]
    return year_filter & category_filter


def prepare_response(total: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract and process papers from search results.

    This function extracts papers from the provided search results, processes
    each paper, and returns a dictionary containing the total count and a list
    of processed papers.

    Args:
        total (int): The hypothetical count of papers present in the db that
            match the filters.
        results (List[Dict[str, Any]): The iterable containing
            raw paper data.

    Returns:
        dict: A dictionary with 'total' count and a list of 'papers', where
            each paper is a processed dict.
    """
    logger.info("Preparing paper response")
    return {
        'total': total,
        'papers': [process_paper(paper) for paper in results]
    }


@router.get("/", response_model=Dict)
async def get_papers(
    limit: int = 20,
    skip: int = 0,
    years: str = "",
    categories: str = ""
):
    """Fetch and return papers with optional filtering by years and categories.

    Args:
        limit (int, optional): Maximum number of papers to return.
            Defaults to 20.
        skip (int, optional): Number of papers to skip for pagination.
            Defaults to 0.
        years (str, optional): Comma-separated string of years to filter papers.
            Defaults to "".
        categories (str, optional): Comma-separated string of categories to
            filter papers. Defaults to "".

    Returns:
        dict: Dictionary containing total count and list of papers.
    """
    # Attach to index
    index = AsyncSearchIndex(schema, client)

    # Build queries
    filter_expression = build_filter_expression(
        years.split(","),
        categories.split(",")
    )
    filter_query = FilterQuery(
        return_fields=[],
        filter_expression=filter_expression
    )
    filter_query.set_paging(skip, limit)
    count_query = CountQuery(filter_expression)
    # Execute searches
    total_count, result_papers = await asyncio.gather(
        index.query(count_query),
        index.query(filter_query)
    )
    result_papers = await index.query(filter_query)
    return prepare_response(total_count, result_papers)


@router.post("/vectorsearch/paper", response_model=Dict)
async def find_papers_by_paper(similarity_request: PaperSimilarityRequest):
    """
    Find and return papers similar to a given paper based on vector
    similarity.

    Args:
        similarity_request (SimilarityRequest): Similarity request object
            containing paper_id, provider, number_of_results, years, and
            categories for filtering.

    Returns:
        dict: Dictionary containing total count and list of similar papers.
    """
    # Attach to index
    index = AsyncSearchIndex(schema, client)

    # Fetch paper vector from the HASH, cast to numpy array
    paper = await index.fetch(similarity_request.paper_id)
    paper_vector = np.frombuffer(
        paper[similarity_request.provider], dtype=np.float32
    )
    # Build filter expression
    filter_expression = build_filter_expression(
        similarity_request.years,
        similarity_request.categories
    )
    # Create queries
    paper_similarity_query = VectorQuery(
        vector=paper_vector,
        vector_field_name=similarity_request.provider,
        num_results=similarity_request.number_of_results,
        return_fields=config.RETURN_FIELDS,
        filter_expression=filter_expression
    )
    count_query = CountQuery(filter_expression)
    # Execute searches
    total_count, result_papers = await asyncio.gather(
        index.query(count_query),
        index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return prepare_response(total_count, result_papers)


@router.post("/vectorsearch/text", response_model=Dict)
async def find_papers_by_text(similarity_request: UserTextSimilarityRequest):
    """
    Find and return papers similar to user-provided text based on
    vector similarity.

    Args:
        similarity_request (UserTextSimilarityRequest): Similarity request
            object containing user_text, provider, number_of_results, years,
            and categories for filtering.

    Returns:
        dict: Dictionary containing total count and list of similar papers.
    """
    # Attach to index
    index = AsyncSearchIndex(schema, client)

    # Build filter expression
    filter_expression = build_filter_expression(
        similarity_request.years,
        similarity_request.categories
    )
    # Check available paper count and create vector from user text
    count_query = CountQuery(filter_expression)
    query_vector = await embeddings.get(
        provider=similarity_request.provider,
        text=similarity_request.user_text
    )
    # Assemble vector query
    paper_similarity_query = VectorQuery(
        vector=query_vector,
        vector_field_name=similarity_request.provider,
        num_results=similarity_request.number_of_results,
        return_fields=config.RETURN_FIELDS,
        filter_expression=filter_expression
    )
    # Execute searches
    total_count, result_papers = await asyncio.gather(
        index.query(count_query),
        index.query(paper_similarity_query)
    )    # Get Paper records of those results
    return prepare_response(total_count, result_papers)
