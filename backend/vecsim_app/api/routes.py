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
    """_summary_

    Args:
        paper (_type_): _description_

    Returns:
        t.Dict[str, t.Any]: _description_
    """
    if not isinstance(paper, dict):
        paper = paper.__dict__
    if 'vector_distance' in paper:
        paper['similarity_score'] = 1 - float(paper['vector_distance'])
    return paper


def build_filter_expression(years: list, categories: list) -> FilterExpression:
    """_summary_

    Args:
        years (list): _description_
        categories (list): _description_

    Returns:
        FilterExpression: _description_
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


def papers_from_results(total: int, results) -> t.Dict[str, t.Any]:
    """_summary_

    Args:
        total (int): _description_
        results (_type_): _description_

    Returns:
        t.Dict[str, t.Any]: _description_
    """
    # extract papers from VSS results
    if not isinstance(results, list):
        results = results.docs
    return {
        'total': total,
        'papers': [process_paper(paper) for paper in results.docs]
    }


@r.get("/", response_model=t.Dict)
async def get_papers(
    limit: int = 20,
    skip: int = 0,
    years: str = "",
    categories: str = ""
):
    """_summary_

    Args:
        limit (int, optional): _description_. Defaults to 20.
        skip (int, optional): _description_. Defaults to 0.
        years (str, optional): _description_. Defaults to "".
        categories (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    query = Query("*")
    # Build query
    years = [year for year in years.split(",") if year]
    categories = [cat for cat in categories.split(",") if cat]
    filter_expression = build_filter_expression(years, categories)
    if filter_expression:
        filter_query = FilterQuery(return_fields=[], filter_expression=filter_expression)
        query = filter_query.query
    # Execute search
    # TODO port the `total` attribute to redisvl as part of (optional) response object?
    # TODO support the * operator on filter queries
    results = await redis_client.ft(config.DEFAULT_PROVIDER).search(
        query.paging(skip, limit)
    )
    return papers_from_results(results.total, results)


@r.post("/vectorsearch/paper", response_model=t.Dict)
async def find_papers_by_text(similarity_request: SimilarityRequest):
    """_summary_

    Args:
        similarity_request (SimilarityRequest): _description_

    Returns:
        _type_: _description_
    """
    # Create index
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
    # TODO need a better way to handle return fields?
    vector_query = VectorQuery(
        vector=paper_vector,
        vector_field_name=paper_vector_field_name,
        num_results=similarity_request.number_of_results,
        return_fields=["paper_id", "authors", "categories", "year", "title", "vector_distance"],
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
    # TODO properly post process these results
    return papers_from_results(count.total, result_papers)


@r.post("/vectorsearch/text", response_model=t.Dict)
async def find_papers_by_user_text(similarity_request: UserTextSimilarityRequest):
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
    # TODO need a better way to handle return fields?
    vector_query = VectorQuery(
        vector=query_vector,
        vector_field_name=paper_vector_field_name,
        num_results=similarity_request.number_of_results,
        return_fields=["paper_id", "authors", "categories", "year", "title", "vector_distance"],
        filter_expression=filter_expression
    )

    # Perform Vector Search
    result_papers = await redis_client.ft(index_name).search(
        vector_query.query, query_params=vector_query.params
    )

    # Get Paper records of those results
    # TODO properly post process these results
    return papers_from_results(count.total, result_papers)
