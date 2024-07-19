import logging
import os
from typing import List

from redis.asyncio import Redis
from redisvl.index import AsyncSearchIndex, SearchIndex
from redisvl.query.filter import FilterExpression, Tag
from redisvl.schema import IndexSchema

from arxivsearch import config

logger = logging.getLogger(__name__)


dir_path = os.path.dirname(os.path.realpath(__file__))
schema = IndexSchema.from_yaml(os.path.join(dir_path, "index.yaml"))
client = Redis.from_url(config.REDIS_URL)
global_index = None


def get_schema():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return IndexSchema.from_yaml(os.path.join(dir_path, "index.yaml"))


def get_index():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return SearchIndex.from_yaml(os.path.join(dir_path, "index.yaml"))


async def get_async_index():
    global global_index
    if not global_index:
        global_index = AsyncSearchIndex(schema, client)
    yield global_index


def build_filter_expression(
    years: List[str], categories: List[str]
) -> FilterExpression:
    """
    Construct a filter expression based on the provided years and categories.

    Args:
        years (list): A list of years (integers or strings) to be included in
            the filter expression. An empty list means there's no filter applied
            based on years.
        categories (list): A list of category strings to be included in the
            filter expression. An empty list means there's no filter applied
            based on categories.

    Returns:
        FilterExpression: A FilterExpression object representing the combined
            filter for both years and categories.
    """
    year_filter = Tag("year") == [str(year) for year in years if year]
    category_filter = Tag("categories") == [
        str(category) for category in categories if category
    ]
    return year_filter & category_filter
