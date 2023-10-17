#!/usr/bin/env python3
import asyncio
import numpy as np
import pandas as pd
import pickle
import os

from arxivsearch import config
from arxivsearch.schema import Provider

from redisvl.index import AsyncSearchIndex


def read_paper_df(provider: str) -> pd.DataFrame:
    """
    Load pickled dataframe of arXiv papers and embeddings.

    Args:
        provider (str): Embedding model provider.

    Returns:
        pd.DataFrame: Dataframe of papers and associated embeddings.
    """
    # TODO improve this data loading method
    path = os.path.join(
        config.DATA_LOCATION, f"arxiv_{provider}_embeddings_1000.pkl"
    )
    with open(path, "rb") as f:
        df = pickle.load(f)
    return df

async def write_papers(index: AsyncSearchIndex, papers: list):
    """
    Write paper records to Redis.

    Args:
        index (AsyncSearchIndex): Redis search index.
        papers (list): List of documents to store.
    """

    def preprocess_paper(paper: dict) -> dict:
        paper['vector'] = np.array(paper['vector'], dtype=np.float32).tobytes()
        paper['paper_id'] = paper.pop('id')
        paper['categories'] = paper['categories'].replace(",", "|")
        return paper

    # TODO add an optional preprocessor callable to index.load()
    await index.load(
        data=[preprocess_paper(paper) for paper in papers],
        concurrency=config.WRITE_CONCURRENCY,
        key_field="paper_id"
    )

async def load_data():
    # Iterate through embedding providers and create an index for each
    for provider in Provider:
        provider = provider.value
        index = AsyncSearchIndex.from_yaml(
            os.path.join("./schema", f"{provider}.yaml")
        )
        index.connect(config.REDIS_URL)
        # Check if index exists
        if await index.exists():
            print(f"{provider} index already exists")
        else:
            print(f"Loading arXiv papers -- {provider} index")
            papers = read_paper_df(provider)
            papers = papers.to_dict('records')
            await write_papers(index=index, papers=papers)
            print(f"{provider} vectors loaded")
            await index.create()
            print("Search index created")


if __name__ == "__main__":
    asyncio.run(load_data())
