import json
import logging
import os

import httpx
import numpy as np
import pytest
import pytest_asyncio
from httpx import AsyncClient
from redisvl.index import SearchIndex

from arxivsearch import config
from arxivsearch.db.utils import get_async_index, get_schema
from arxivsearch.main import app


@pytest_asyncio.fixture(scope="session")
def index():
    index = SearchIndex(schema=get_schema(), redis_url=config.REDIS_URL)
    index.create()
    yield index
    index.disconnect()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_index():
    index = await get_async_index()
    async with index:
        yield index


@pytest_asyncio.fixture(scope="session", autouse=True)
def cleanup_logging_handlers():
    """
    Pytest closes logging handlers when running tests, so any atexit handlers or
    weakref finalizers that try to log will generate I/O errors. Clearing the
    handlers with an autouse fixture prevents this.
    """
    try:
        yield
    finally:
        logger = logging.getLogger()
        logger.handlers.clear()


@pytest.fixture(scope="session", autouse=True)
def test_data(index):
    cwd = os.getcwd()
    with open(f"{cwd}/arxivsearch/tests/test_vectors.json", "r") as f:
        papers = json.load(f)

    # convert to bytes
    for paper in papers:
        paper["huggingface"] = np.array(
            paper["huggingface"], dtype=np.float32
        ).tobytes()
        paper["openai"] = np.array(paper["openai"], dtype=np.float32).tobytes()
        paper["cohere"] = np.array(paper["cohere"], dtype=np.float32).tobytes()

    _ = index.load(data=papers, id_field="paper_id")
    return papers


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test/api/v1/"  # type: ignore
    ) as client:
        yield client
