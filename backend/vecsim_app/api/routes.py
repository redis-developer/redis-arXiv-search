import asyncio
import typing as t
import redis.asyncio as redis

from fastapi import APIRouter
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


def process_paper(paper) -> t.Dict[str, t.Any]:
    paper = paper.__dict__
    if 'similarity_score' in paper:
        paper['similarity_score'] = 1 - float(paper['similarity_score'])
    return paper


def papers_from_results(total: int, results) -> t.Dict[str, t.Any]:
    # extract papers from VSS results
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
    # Create query
    years = [year for year in years.split(",") if year]
    categories = [cat for cat in categories.split(",") if cat]
    query = search_index.query(
        categories=categories,
        years=years,
        offset=skip,
        limit=limit
    )
    # obtain results of the queries
    results = await redis_client.ft(config.DEFAULT_PROVIDER).search(query)

    return papers_from_results(results.total, results)


@r.post("/vectorsearch/text", response_model=t.Dict)
async def find_papers_by_text(similarity_request: SimilarityRequest):
    # Create query
    index_name = similarity_request.provider
    query = search_index.vector_query(similarity_request)
    count_query = search_index.count_query(similarity_request)

    # Fetch the vector of the Paper of interest in the request
    paper_vector_key = search_index.key(index_name, similarity_request.paper_id)
    vector = await redis_client.hget(paper_vector_key, "vector")

    # Check available paper count and perform vector search
    count, results = await asyncio.gather(
        redis_client.ft(index_name).search(count_query),
        redis_client.ft(index_name).search(
            query,
            query_params={"vector": vector}
        )
    )

    # Get Paper records of those results
    return papers_from_results(count.total, results)


@r.post("/vectorsearch/text/user", response_model=t.Dict)
async def find_papers_by_user_text(similarity_request: UserTextSimilarityRequest):
    # Create query
    index_name = similarity_request.provider
    query = search_index.vector_query(similarity_request)
    count_query = search_index.count_query(similarity_request)

    # Check available paper count and create vector
    vector, count = await asyncio.gather(
        embeddings.get(
            provider=similarity_request.provider,
            text=similarity_request.user_text
        ),
        redis_client.ft(index_name).search(count_query)
    )

    # Perform Vector Search
    results = await redis_client.ft(index_name).search(
        query,
        query_params={"vector": vector.tobytes()}
    )

    # Get Paper records of those results
    return papers_from_results(count.total, results)
