from typing import Generator
import pytest_asyncio
import pytest
from redis.asyncio import Redis as AsyncRedis
from httpx import AsyncClient
from asyncio import get_event_loop
from redis.asyncio import Redis
from arxivsearch.db import redis_helpers
from arxivsearch.tests.utils.seed import seed_test_db
from arxivsearch import config
from redisvl.index import AsyncSearchIndex

from arxivsearch.main import app


@pytest.fixture(scope="module")
def papers():
    papers = seed_test_db()
    return papers


@pytest.fixture
async def client():
    client = await Redis.from_url(config.REDIS_URL)
    yield client
    try:
        await client.aclose()
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise


@pytest_asyncio.fixture(scope="session")
async def async_client():

    async with AsyncClient(app=app, base_url="http://test/api/v1/") as client:

        yield client
