from typing import List, Dict, Any
from pydantic import TypeAdapter
from redisvl.query.filter import Tag, FilterExpression
import logging

logger = logging.getLogger(__name__)


def process_paper(paper: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process paper data and calculate similarity score.

    Args:
        paper: Input paper data.

    Returns:
        dict: Processed paper data with similarity score.
    """
    if "vector_distance" in paper:
        paper["similarity_score"] = 1 - float(paper["vector_distance"])
    return paper


def build_filter_expression(
    years: List[int], categories: List[str]
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


def prepare_response(total: int, results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract and process papers from search results.

    This function extracts papers from the provided search results, processes
    each paper, and returns a dictionary containing the total count and a list
    of processed papers.

    Args:
        total (int): The hypothetical count of papers present in the db that
            match the filters.
        results (List[Dict[str, Any]): The iterable containing
            raw paper data.

    Returns:
        dict: A dictionary with 'total' count and a list of 'papers', where
            each paper is a processed dict.
    """
    logger.info("Preparing paper response")
    return {"total": total, "papers": [process_paper(paper) for paper in results]}
