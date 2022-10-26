#!/usr/bin/env python3
import typing as t
import asyncio
import numpy as np
import pickle
import redis.asyncio as redis

from redis.commands.search.field import TagField
from vecsim_app import config
from vecsim_app.models import Paper
from vecsim_app.search_index import SearchIndex


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
            # TODO - we need to be able to use other separators
            paper['categories'] = paper['categories'].replace(",", "|")
            p = Paper(**paper)
            # save model TODO -- combine these two objects eventually
            await p.save()
            # save vector data
            key = "paper_vector:" + str(p.paper_id)
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
    search_index = SearchIndex()
    if await redis_conn.dbsize() > 300:
        print("Papers already loaded")
    else:
        print("Loading papers into Vecsim App")
        papers = read_paper_df()
        papers = papers.to_dict('records')
        await gather_with_concurrency(100, redis_conn, *papers)
        print("Papers loaded!")

        print("Creating vector search index")
        categories_field = TagField("categories", separator = "|")
        year_field = TagField("year", separator = "|")
        # create a search index
        if config.INDEX_TYPE == "HNSW":
            await search_index.create_hnsw(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix="paper_vector:",
                distance_metric="IP",
            )
        else:
            await search_index.create_flat(
                categories_field,
                year_field,
                redis_conn=redis_conn,
                number_of_vectors=len(papers),
                prefix="paper_vector:",
                distance_metric="IP",
            )
        print("Search index created")


if __name__ == "__main__":
    asyncio.run(load_all_data())
