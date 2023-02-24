#!/usr/bin/env python3
import asyncio
import numpy as np
import pickle
import typing as t
import redis.asyncio as redis

from redis.commands.search.field import (
    TagField,
    TextField,
    VectorField
)
from vecsim_app import config
from vecsim_app.search_index import SearchIndex
from vecsim_app.providers import Provider


def read_paper_df(provider: str) -> t.List:
    with open(config.DATA_LOCATION + f"/arxiv_{provider}_embeddings_1000.pkl", "rb") as f:
        df = pickle.load(f)
    return df

async def gather_with_concurrency(n: int, prefix: str, redis_conn: redis.Redis, papers: list):
    """
    Write documents to Redis.

    Args:
        n (int): Level of write concurrency enabled by asyncio semaphores.
        prefix (str): RediSearch document prefix to use.
        redis_conn (redis.Redis): Redis client.
        papers (list): List of documents to store.
    """
    semaphore = asyncio.Semaphore(n)
    async def load_paper(paper):
        async with semaphore:
            paper['vector'] = np.array(paper['vector'], dtype=np.float32).tobytes()
            paper['paper_id'] = paper.pop('id')
            paper['categories'] = paper['categories'].replace(",", "|")
            key = SearchIndex.key(prefix, str(paper['paper_id']))
            await redis_conn.hset(key, mapping=paper)
    # gather with concurrency
    await asyncio.gather(*[load_paper(p) for p in papers])

def create_schema(num_docs: int, vector_dimensions: int):
    fields = [
        TagField("categories", separator = "|"),
        TagField("year", separator = "|"),
        TextField("title"),
        TextField("abstract")
    ]
    if config.INDEX_TYPE == "FLAT":
        fields.append(VectorField(
            "vector",
            "FLAT", {
                "TYPE": "FLOAT32",
                "DIM": vector_dimensions,
                "DISTANCE_METRIC": config.DISTANCE_METRIC,
                "INITIAL_CAP": num_docs,
                "BLOCK_SIZE": num_docs
            }
        ))
    elif config.INDEX_TYPE == "HNSW":
        fields.append(VectorField(
            "vector",
            "HNSW", {
                "TYPE": "FLOAT32",
                "DIM": vector_dimensions,
                "DISTANCE_METRIC": config.DISTANCE_METRIC,
                "INITIAL_CAP": num_docs,
            }
        ))
    return fields

async def load_data():
    redis_conn = redis.from_url(config.REDIS_URL)
    search_index = SearchIndex()
    # Iterate through embedding providers
    for provider in Provider:
        provider = provider.value
        try:
            await redis_conn.ft(provider).info()
            print(f"{provider} vector index already created!")
        except:
            print(f"Loading arXiv {provider} vectors.")
            papers = read_paper_df(provider)
            papers = papers.to_dict('records')
            num_docs = len(papers)
            vector_dimensions = len(papers[0]['vector'])
            # Write to Redis
            await gather_with_concurrency(
                n=int(config.WRITE_CONCURRENCY),
                prefix=provider,
                redis_conn=redis_conn,
                papers=papers
            )
            print(f"{provider} vectors loaded")

            print("Creating vector search index")
            fields = create_schema(num_docs, vector_dimensions)
            # Create a search index
            await search_index.create(
                fields=fields,
                index_name=provider,
                redis_conn=redis_conn,
                prefix=provider
            )
            print("Search index created")


if __name__ == "__main__":
    asyncio.run(load_data())
