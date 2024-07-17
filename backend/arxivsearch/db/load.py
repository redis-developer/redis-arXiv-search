import asyncio
import numpy as np
import json
import os
import logging

from typing import Any, Dict, List

from arxivsearch import config
from arxivsearch.schema.provider import Provider
from arxivsearch.db import redis_helpers

from redisvl.index import AsyncSearchIndex


logger = logging.getLogger(__name__)


def read_paper_json() -> List[Dict[str, Any]]:
    """
    Load JSON array of arXiv papers and embeddings.
    """
    logger.info("Loading papers dataset from disk")
    path = os.path.join(config.DATA_LOCATION, config.DEFAULT_DATASET)
    with open(path, "r") as f:
        df = json.load(f)
    return df


async def write_async(index: AsyncSearchIndex, papers: list):
    """
    Write arXiv paper records to Redis asynchronously.
    """

    async def preprocess_paper(paper: dict) -> dict:
        for provider_vector in Provider:
            paper[provider_vector] = np.array(
                paper[provider_vector], dtype=np.float32
            ).tobytes()
        paper["paper_id"] = paper.pop("id")
        paper["categories"] = paper["categories"].replace(",", "|")
        return paper

    logger.info("Loading papers dataset to Redis")

    _ = await index.load(
        data=papers,
        preprocess=preprocess_paper,
        concurrency=config.WRITE_CONCURRENCY,
        id_field="id",
    )

    logger.info("All papers loaded")


async def load_data():
    # Load schema specs and create index in Redis
    index = await redis_helpers.get_async_index()

    # Load dataset and create index
    try:
        # Check if index exists
        if await index.exists():
            # if running local and not seeing logger logs make sure index isn't already created
            logger.info("Index already exists, skipping data load")
        else:
            logger.info("Creating new index")
            await index.create(overwrite=True)
            papers = read_paper_json()
            await write_async(index=index, papers=papers)
    except Exception as e:
        logger.exception(
            "An exception occurred while trying to load the index and dataset"
        )
    finally:
        await index.client.aclose()

    # Wait for any indexing to finish
    while True:
        info = await index.info()
        if info["percent_indexed"] == "1":
            logger.info("Indexing is complete!")
            break
        logger.info(f"{info['percent_indexed']} indexed...")
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(load_data())
