import asyncio
import numpy as np
import logging

from fastapi import APIRouter
from redis.asyncio import Redis

from redisvl.index import AsyncSearchIndex
from redisvl.query import VectorQuery, FilterQuery, CountQuery

from arxivsearch import config
from arxivsearch.redis import helpers
from arxivsearch.utils.embeddings import Embeddings
from arxivsearch.utils.utils import build_filter_expression, prepare_response
from arxivsearch.schema.similarity import (
    PaperSimilarityRequest,
    UserTextSimilarityRequest,
    SearchResponse,
    VectorSearchResponse,
)


logger = logging.getLogger(__name__)

# Initialize the API router
router = APIRouter()

# TODO: these could move to a deps file and be injected potentially
# Initialize embeddings and paper vector field name
embeddings = Embeddings()

# Preload Redis connection details
client = Redis.from_url(config.REDIS_URL)

# Preload schema
schema = helpers.get_index()


@router.get("/", response_model=SearchResponse)
async def get_papers(
    limit: int = 20, skip: int = 0, years: str = "", categories: str = ""
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
    filter_expression = build_filter_expression(years.split(","), categories.split(","))
    filter_query = FilterQuery(return_fields=[], filter_expression=filter_expression)
    filter_query.set_paging(skip, limit)
    count_query = CountQuery(filter_expression)
    # Execute searches
    total_count, result_papers = await asyncio.gather(
        index.query(count_query), index.query(filter_query)
    )
    result_papers = await index.query(filter_query)
    return SearchResponse(total=total_count, papers=result_papers)


@router.post("/vector_search/by_paper", response_model=VectorSearchResponse)
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
    paper_vector = np.frombuffer(paper[similarity_request.provider], dtype=np.float32)
    # Build filter expression
    filter_expression = build_filter_expression(
        similarity_request.years, similarity_request.categories
    )
    # Create queries
    paper_similarity_query = VectorQuery(
        vector=paper_vector,
        vector_field_name=similarity_request.provider,
        num_results=similarity_request.number_of_results,
        return_fields=config.RETURN_FIELDS,
        filter_expression=filter_expression,
    )
    count_query = CountQuery(filter_expression)
    # Execute searches
    total_count, result_papers = await asyncio.gather(
        index.query(count_query), index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return VectorSearchResponse(total=total_count, papers=result_papers)


@router.post("/vector_search/by_text", response_model=VectorSearchResponse)
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
        similarity_request.years, similarity_request.categories
    )
    # Check available paper count and create vector from user text
    count_query = CountQuery(filter_expression)
    query_vector = await embeddings.get(
        provider=similarity_request.provider.value, text=similarity_request.user_text
    )
    # Assemble vector query
    paper_similarity_query = VectorQuery(
        vector=query_vector,
        vector_field_name=similarity_request.provider.value,
        num_results=similarity_request.number_of_results,
        return_fields=config.RETURN_FIELDS,
        filter_expression=filter_expression,
    )
    # Execute searches
    total_count, result_papers = await asyncio.gather(
        index.query(count_query), index.query(paper_similarity_query)
    )  # Get Paper records of those results
    return VectorSearchResponse(total=total_count, papers=result_papers)
