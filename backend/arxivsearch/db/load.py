import asyncio
import json
import logging
import os
from typing import Any, Dict, List

import numpy as np
import requests
from redisvl.index import AsyncSearchIndex

from arxivsearch import config
from arxivsearch.db.utils import get_schema
from arxivsearch.schema.models import Provider

logger = logging.getLogger(__name__)


def read_from_s3(path):
    res = requests.get(config.S3_DATA_URL)
    data = res.json()

    if os.path.isdir(config.DATA_LOCATION):
        logger.info(f"Writing s3 file to {path}")
        with open(path, "w") as f:
            json.dump(data, f)
    else:
        logger.warning(
            f"Data directory {config.DATA_LOCATION} not found. Skipping write of S3 data"
        )
    return data


def read_paper_json() -> List[Dict[str, Any]]:
    """
    Load JSON array of arXiv papers and embeddings.
    """
    logger.info("Loading papers dataset from disk")
    path = os.path.join(config.DATA_LOCATION, config.DEFAULT_DATASET)
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except:
        logger.info(f"Failed to read {path} => getting from s3")
        data = read_from_s3(path)

    return data


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
        concurrency=int(config.WRITE_CONCURRENCY),
        id_field="id",
    )

    logger.info("All papers loaded")


async def load_data():
    # Load schema specs and create index in Redis
    index = AsyncSearchIndex(schema=get_schema(), redis_url=config.REDIS_URL)

    # Load dataset and create index
    try:
        # Check if index exists
        if await index.exists() and len((await index.search("*")).docs) > 0:
            # if running local and not seeing logger logs make sure index isn't already created
            logger.info("Index and data already exists, skipping load")
        else:
            logger.info("Creating new index")
            await index.create(overwrite=True)
            papers = read_paper_json()
            await write_async(index=index, papers=papers)
    except Exception as e:
        logger.exception(
            "An exception occurred while trying to load the index and dataset"
        )
        raise

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
