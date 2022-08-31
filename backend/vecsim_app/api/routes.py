import typing as t
import redis.asyncio as redis
import vecsim_app.embeddings as embeddings

from fastapi import APIRouter
from vecsim_app import config
from vecsim_app.schema import (
    SimilarityRequest,
    UserTextSimilarityRequest
)
from vecsim_app.models import Paper
from vecsim_app.query import create_query


paper_router = r = APIRouter()
redis_client = redis.from_url(config.REDIS_URL)

async def process_paper(p):
    paper = await Paper.get(p.paper_pk)
    paper = paper.dict()
    print(p.paper_id, p.vector_score)
    paper['similarity_score'] = 1 - float(p.vector_score)
    return paper

async def papers_from_results(results) -> list:
    return [await process_paper(p) for p in results.docs]

@r.get("/", response_model=t.List[Paper],
       name="paper:get_paper_samples",
       operation_id="get_papers_samples")
async def get_papers(limit: int = 20, skip: int = 0):
    pks = await Paper.all_pks()
    if pks:
        # TODO figure out how to slice async_generator
        papers = []
        i = 0
        async for pk in pks:
            if i >= skip and i < skip + limit:
                papers.append(await Paper.get(pk))
            if len(papers) == limit:
                break
            i += 1
        return papers
    return []

@r.post("/vectorsearch/text",
       response_model=t.List[t.Dict],
       name="paper:find_similar_by_text",
       operation_id="compute_text_similarity")
async def find_papers_by_text(similarity_request: SimilarityRequest) -> t.List[t.Dict]:
    q = create_query(
        similarity_request.search_type,
        similarity_request.number_of_results
    )

    # find the vector of the Paper listed in the request
    paper_vector_key = "paper_vector:" + str(similarity_request.paper_id)
    vector = await redis_client.hget(paper_vector_key, "vector")

    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector})

    # Get Paper records of those results
    return await papers_from_results(results)


@r.post("/vectorsearch/text/user",
       response_model=t.List[t.Dict],
       name="paper:find_similar_by_user_text",
       operation_id="compute_user_text_similarity")
async def find_papers_by_user_text(similarity_request: UserTextSimilarityRequest) -> t.List[t.Dict]:
    q = create_query(
        similarity_request.search_type,
        similarity_request.number_of_results
    )

    vector = embeddings.make(similarity_request.user_text)

    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector.numpy().tobytes()})

    # Get Paper records of those results
    return await papers_from_results(results)
