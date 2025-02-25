import logging
import os
from typing import List

from redisvl.index import AsyncSearchIndex
from redisvl.query.filter import FilterExpression, Tag
from redisvl.schema import IndexSchema

from arxivsearch import config

logger = logging.getLogger(__name__)


# global search index
_global_index = None


def get_schema() -> IndexSchema:
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/schema"
    file_path = os.path.join(dir_path, "index.yaml")
    return IndexSchema.from_yaml(file_path)


async def get_async_index():
    global _global_index
    if not _global_index:
        _global_index = AsyncSearchIndex(get_schema(), redis_url=config.REDIS_URL)
    return _global_index


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
