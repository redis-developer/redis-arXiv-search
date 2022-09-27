#!/usr/bin/env python3
import typing as t
import json
import asyncio
import numpy as np
import pickle
import redis.asyncio as redis

from vecsim_app import config
from vecsim_app.models import Paper
from vecsim_app.query import (
    create_flat_index,
    create_hnsw_index
)

def read_paper_df() -> t.List:
    with open(config.DATA_LOCATION + "/arxiv_embeddings_10000.pkl", "rb") as f:
        df = pickle.load(f)
    return df

async def gather_with_concurrency(n, redis_conn, *papers):
    semaphore = asyncio.Semaphore(n)
    async def load_paper(paper):
        async with semaphore:
            vector = paper.pop('vector')
            paper['paper_id'] = paper.pop('id')
            p = Paper(**paper)
            key = "paper_vector:" + str(p.paper_id)
            # async write data to redis
            await p.save()
            await redis_conn.hset(
                key,
                mapping={
                    "paper_pk": p.pk,
                    "paper_id": p.paper_id,
                    "categories": p.categories,
                    "year": p.year,
                    "vector": np.array(vector, dtype=np.float32).tobytes(),
            })
    # gather with concurrency
    await asyncio.gather(*[load_paper(p) for p in papers])

async def load_all_data():
    # TODO use redis-om connection
    redis_conn = redis.from_url(config.REDIS_URL)
    if await redis_conn.dbsize() > 300:
        print("papers already loaded")
    else:
        print("Loading papers into Vecsim App")
        papers = read_paper_df()
        papers = papers.to_dict('records')
        await gather_with_concurrency(100, redis_conn, *papers)
        print("papers loaded!")

        print("Creating vector search index")
        # create a search index
        if config.INDEX_TYPE == "HNSW":
            await create_hnsw_index(redis_conn, len(papers), prefix="paper_vector:", distance_metric="IP")
        else:
            await create_flat_index(redis_conn, len(papers), prefix="paper_vector:", distance_metric="L2")
        print("Search index created")


if __name__ == "__main__":
    asyncio.run(load_all_data())
