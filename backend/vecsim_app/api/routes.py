import typing as t
import redis.asyncio as redis
import vecsim_app.embeddings as embeddings

from fastapi import APIRouter
from vecsim_app import config
from vecsim_app.models import Paper
from vecsim_app.schema import (
    SimilarityRequest,
    UserTextSimilarityRequest
)
from vecsim_app.query import create_query


paper_router = r = APIRouter()
redis_client = redis.from_url(config.REDIS_URL)

async def process_paper(p):
    paper = await Paper.get(p.paper_pk)
    paper = paper.dict()
    paper['similarity_score'] = 1 - float(p.vector_score)
    return paper

async def papers_from_results(results) -> list:
    return [await process_paper(p) for p in results.docs]


@r.get("/", response_model=t.List[Paper])
async def get_papers(limit: int = 20, skip: int = 0, years: str = "", categories: str = ""):
    papers = []
    expressions = []
    years = [year for year in years.split(",") if year]
    categories = [cat for cat in categories.split(",") if cat]
    if years and categories:
        expressions.append(
            (Paper.year << years) & \
            (Paper.categories << categories)
        )
    elif years and not categories:
        expressions.append(Paper.year << years)
    elif categories and not years:
        expressions.append(Paper.categories << categories)
    # Run query
    print(years, categories)
    print(Paper.find(*expressions).copy(offset=skip, limit=limit).query, flush=True)

    papers = await Paper.find(*expressions)\
        .copy(offset=skip, limit=limit)\
        .execute(exhaust_results=False)
    return papers


@r.post("/vectorsearch/text", response_model=t.List[t.Dict])
async def find_papers_by_text(similarity_request: SimilarityRequest) -> t.List[t.Dict]:
    # Create query
    query = create_query(
        similarity_request.categories,
        similarity_request.years,
        similarity_request.search_type,
        similarity_request.number_of_results
    )

    # find the vector of the Paper listed in the request
    paper_vector_key = "paper_vector:" + str(similarity_request.paper_id)
    vector = await redis_client.hget(paper_vector_key, "vector")

    # Execute query
    results = await redis_client.ft(config.INDEX_NAME).search(
        query,
        query_params={"vec_param": vector}
    )

    # Get Paper records of those results
    return await papers_from_results(results)


@r.post("/vectorsearch/text/user", response_model=t.List[t.Dict])
async def find_papers_by_user_text(similarity_request: UserTextSimilarityRequest) -> t.List[t.Dict]:
    # Create query
    query = create_query(
        similarity_request.categories,
        similarity_request.years,
        similarity_request.search_type,
        similarity_request.number_of_results
    )

    # Execute query
    results = await redis_client.ft(config.INDEX_NAME).search(
        query,
        query_params={
            "vec_param": embeddings.make(similarity_request.user_text).tobytes()
        }
    )
    return await papers_from_results(results)
