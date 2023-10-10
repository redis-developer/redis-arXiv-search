import asyncio
import typing as t
import numpy as np
import redis.asyncio as redis

from redis.commands.search.query import Query

from redisvl.index import AsyncSearchIndex
from redisvl.query import VectorQuery, FilterQuery
from redisvl.query.filter import FilterExpression
from redisvl.query.filter import Tag

from fastapi import APIRouter
from functools import reduce
from vecsim_app import config
from vecsim_app.embeddings import Embeddings
from vecsim_app.schema import (
    SimilarityRequest,
    UserTextSimilarityRequest
)
from vecsim_app.search_index import SearchIndex


paper_router = r = APIRouter()
redis_client = redis.from_url(config.REDIS_URL)
embeddings = Embeddings()
search_index = SearchIndex()
paper_vector_field_name = "vector"


def process_paper(paper) -> t.Dict[str, t.Any]:
    """
    Process paper data and calculate similarity score.

    Args:
        paper: Input paper data.

    Returns:
        dict: Processed paper data with similarity score.
    """
    if not isinstance(paper, dict):
        paper = paper.__dict__
    if 'vector_distance' in paper:
        paper['similarity_score'] = 1 - float(paper['vector_distance'])
    return paper


# TODO this is only necessary now while I have to manually build the iterable filters from these two inputs
def build_filter_expression(years: list, categories: list) -> FilterExpression:
    """
    Construct a filter expression based on the provided years and categories.

    This function builds a FilterExpression used for querying papers in Redis.
    It takes lists of years and categories as input, constructs filter expressions for
    each set of parameters, and then combines them using the AND operator. The filter
    expressions for years and categories are constructed by OR'ing individual year and
    category conditions. If either years or categories list is empty, the function will
    return a filter expression based solely on the non-empty parameter list.

    Args:
        years (list): A list of years (integers or strings) to be included in the filter
                      expression. An empty list means there's no filter applied based on years.
        categories (list): A list of category strings to be included in the filter
                           expression. An empty list means there's no filter applied based
                           on categories.

    Returns:
        FilterExpression: A FilterExpression object representing the combined filter for both years and
            categories. If both input lists are empty, the function returns None.
    """
    if not years and not categories:
        return None

    def or_expression(accumulator, value):
        return accumulator | (Tag(value[0]) == value[1])

    def or_expression(accumulator, value, field):
        return accumulator | (Tag(field) == value)

    year_filter = None
    category_filter = None

    if years:
        year_filter = Tag("year") == years[0]
        year_filter = reduce(lambda acc, year: or_expression(acc, year, "year"), years[1:], year_filter)

    if categories:
        category_filter = Tag("categories") == categories[0]
        category_filter = reduce(lambda acc, cat: or_expression(acc, cat, "categories"), categories[1:], category_filter)

    if year_filter and category_filter:
        return year_filter & category_filter
    return year_filter or category_filter


def prepare_response(total: int, results) -> t.Dict[str, t.Any]:
    """
    Extract and process papers from search results.

    This function extracts papers from the provided search results, processes each paper,
    and returns a dictionary containing the total count and a list of processed papers.

    Args:
        total (int): The hypothetical count of papers present in the db that match the filters.
        results (list): The iterable containing raw paper data.

    Returns:
        dict: A dictionary with 'total' count and a list of 'papers', where each paper is a processed dict.
    """
    # extract papers from VSS results
    if not isinstance(results, list):
        results = results.docs
    return {
        'total': total,
        'papers': [process_paper(paper) for paper in results]
    }


def create_vector_query(
    vector: np.ndarray,
    num_results: int,
    filter_expression: FilterExpression) -> VectorQuery:
    """
    Create and return a VectorQuery instance.

    Args:
        vector (np.ndarray): The input vector for the query.
        num_results (int): The number of results to return.
        filter_expression (FilterExpression): The filter expression for the query.

    Returns:
        VectorQuery: The constructed VectorQuery instance.
    """
    return VectorQuery(
        vector=vector,
        vector_field_name=paper_vector_field_name,
        num_results=num_results,
        return_fields=["paper_id", "authors", "categories", "year", "title", "vector_distance"],
        filter_expression=filter_expression
    )


@r.get("/", response_model=t.Dict)
async def get_papers(
    limit: int = 20,
    skip: int = 0,
    years: str = "",
    categories: str = ""
):
   """Fetch and return papers with optional filtering by years and categories.

    Args:
        limit (int, optional): Maximum number of papers to return. Defaults to 20.
        skip (int, optional): Number of papers to skip for pagination. Defaults to 0.
        years (str, optional): Comma-separated string of years to filter papers. Defaults to "".
        categories (str, optional): Comma-separated string of categories to filter papers. Defaults to "".

    Returns:
        dict: Dictionary containing total count and list of papers.
    """
    query = Query("*")
    # Build query
    year_values = [year for year in years.split(",") if year]
    category_values = [cat for cat in categories.split(",") if cat]
    filter_expression = build_filter_expression(year_values, category_values)
    if filter_expression:
        filter_query = FilterQuery(return_fields=[], filter_expression=filter_expression)
        query = filter_query.query
    # Execute search
    # TODO port the `total` attribute to redisvl as part of (optional) response object?
    # TODO support the * operator on filter queries
    results = await redis_client.ft(config.DEFAULT_PROVIDER).search(
        query.paging(skip, limit)
    )
    return prepare_response(results.total, results)


@r.post("/vectorsearch/paper", response_model=t.Dict)
async def find_papers_by_paper(similarity_request: SimilarityRequest):
    """Find and return papers similar to a given paper based on vector similarity.

    Args:
        similarity_request (SimilarityRequest): Similarity request object containing paper_id, provider,
                                                number_of_results, years, and categories for filtering.

    Returns:
        dict: Dictionary containing total count and list of similar papers.
    """
    # Connect to index
    index_name = similarity_request.provider
    index = await AsyncSearchIndex.from_existing(
        name=index_name,
        url=config.REDIS_URL
    )
    # TODO - need to figure out how to do this better with RedisVL
    paper_key = index._get_key({"paper_id": "arXiv:" + similarity_request.paper_id}, "paper_id")
    paper_vector = np.frombuffer(
        await index._redis_conn.hget(paper_key, paper_vector_field_name),
        dtype=np.float32
    )

    # Build filter expression
    filter_expression = build_filter_expression(
        similarity_request.years,
        similarity_request.categories
    )

    # Assemble vector query
    vector_query = create_vector_query(
        vector=paper_vector,
        num_results=similarity_request.number_of_results,
        filter_expression=filter_expression
    )

    # Async execute count search and vector search
    # TODO add a CountQuery class to redisvl
    count, result_papers = await asyncio.gather(
        redis_client.ft(index_name).search(
            Query(filter_expression or "*").no_content().dialect(2)
        ),
        redis_client.ft(index_name).search(
            vector_query.query, query_params=vector_query.params
        )
    )

    # Get Paper records of those results
    return prepare_response(count.total, result_papers)


@r.post("/vectorsearch/text", response_model=t.Dict)
async def find_papers_by_text(similarity_request: UserTextSimilarityRequest):
    """Find and return papers similar to user-provided text based on vector similarity.

    Args:
        similarity_request (UserTextSimilarityRequest): Similarity request object containing user_text, provider,
                                                        number_of_results, years, and categories for filtering.

    Returns:
        dict: Dictionary containing total count and list of similar papers.
    """
    # Attach to index
    index_name = similarity_request.provider
    index = await AsyncSearchIndex.from_existing(
        name=index_name,
        url=config.REDIS_URL
    )

    # Build filter expression
    filter_expression = build_filter_expression(
        similarity_request.years,
        similarity_request.categories
    )

    # Check available paper count and create vector from user text
    # TODO add the count query class to redisvl
    query_vector, count = await asyncio.gather(
        embeddings.get(
            provider=index_name,
            text=similarity_request.user_text
        ),
        redis_client.ft(index_name).search(
            Query(filter_expression or "*").no_content().dialect(2)
        )
    )

    # construct vector query
    vector_query = create_vector_query(
        vector=query_vector,
        num_results=similarity_request.number_of_results,
        filter_expression=filter_expression
    )

    # Perform Vector Search
    result_papers = await redis_client.ft(index_name).search(
        vector_query.query, query_params=vector_query.params
    )

    # Get Paper records of those results
    return prepare_response(count.total, result_papers)
