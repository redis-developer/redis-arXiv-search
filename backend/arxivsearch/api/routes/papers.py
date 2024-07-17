import asyncio
import numpy as np
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi import APIRouter, Query, Depends
from redis.asyncio import Redis

from redisvl.index import AsyncSearchIndex
from redisvl.query import VectorQuery, FilterQuery, CountQuery

from arxivsearch import config
from arxivsearch.db import redis_helpers
from arxivsearch.utils.embeddings import Embeddings
from arxivsearch.schema.similarity import (
    PaperSimilarityRequest,
    UserTextSimilarityRequest,
    SearchResponse,
    VectorSearchResponse,
)


logger = logging.getLogger(__name__)


# class DB:
#     client = None
#     schema = None
#     index = None


# db = DB()

# Initialize embeddings once
embeddings = Embeddings()

# client = Redis.from_url(config.REDIS_URL)
# schema = redis_helpers.get_schema()
# index = AsyncSearchIndex(schema, client)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     db.client = Redis.from_url(config.REDIS_URL)
#     db.schema = redis_helpers.get_schema()
#     db.index = AsyncSearchIndex(db.schema, db.client)
#     yield
#     db.client.aclose()


# Initialize the API router
router = APIRouter()


@router.get("/", response_model=SearchResponse)
async def get_papers(
    index: AsyncSearchIndex = Depends(redis_helpers.get_async_index),
    limit: int = Query(default=20, description="Maximum number of papers to return."),
    skip: int = Query(
        default=0, description="Number of papers to skip for pagination."
    ),
    years: str = Query(
        default="", description="Comma-separated string of years to filter papers."
    ),
    categories: str = Query(
        default="", description="Comma-separated string of categories to filter papers."
    ),
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

    # Build queries
    filter_expression = redis_helpers.build_filter_expression(
        years.split(","), categories.split(",")
    )
    filter_query = FilterQuery(return_fields=[], filter_expression=filter_expression)
    filter_query.set_paging(skip, limit)
    count_query = CountQuery(filter_expression)

    # Execute searches
    total_count, result_papers = await asyncio.gather(
        index.query(count_query), index.query(filter_query)
    )
    # await index.client.aclose()
    return SearchResponse(total=total_count, papers=result_papers)


@router.post("/vector_search/by_paper", response_model=VectorSearchResponse)
async def find_papers_by_paper(
    similarity_request: PaperSimilarityRequest,
    index: AsyncSearchIndex = Depends(redis_helpers.get_async_index),
):
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

    # Fetch paper vector from the HASH, cast to numpy array
    paper = await index.fetch(similarity_request.paper_id)
    paper_vector = np.frombuffer(
        paper[similarity_request.provider.value], dtype=np.float32
    )
    # Build filter expression
    filter_expression = redis_helpers.build_filter_expression(
        similarity_request.years, similarity_request.categories
    )
    # Create queries
    paper_similarity_query = VectorQuery(
        vector=paper_vector,
        vector_field_name=similarity_request.provider.value,
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
    # await index.client.aclose()
    return VectorSearchResponse(total=total_count, papers=result_papers)


@router.post("/vector_search/by_text", response_model=VectorSearchResponse)
async def find_papers_by_text(
    similarity_request: UserTextSimilarityRequest,
    index: AsyncSearchIndex = Depends(redis_helpers.get_async_index),
):
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

    # Build filter expression
    filter_expression = redis_helpers.build_filter_expression(
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

    # await index.client.aclose()
    return VectorSearchResponse(total=total_count, papers=result_papers)
