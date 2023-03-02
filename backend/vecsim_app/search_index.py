import re

from schema import SimilarityRequest
from redis.asyncio import Redis
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)
from typing import (
    Optional,
    Pattern
)


class TokenEscaper:
    """
    Escape punctuation within an input string. Taken from RedisOM Python.
    """
    # Characters that RediSearch requires us to escape during queries.
    # Source: https://redis.io/docs/stack/search/reference/escaping/#the-rules-of-text-field-tokenization
    DEFAULT_ESCAPED_CHARS = r"[,.<>{}\[\]\\\"\':;!@#$%^&*()\-+=~\/ ]"

    def __init__(self, escape_chars_re: Optional[Pattern] = None):
        if escape_chars_re:
            self.escaped_chars_re = escape_chars_re
        else:
            self.escaped_chars_re = re.compile(self.DEFAULT_ESCAPED_CHARS)

    def escape(self, value: str) -> str:
        def escape_symbol(match):
            value = match.group(0)
            return f"\\{value}"

        return self.escaped_chars_re.sub(escape_symbol, value)

class SearchIndex:
    """
    SearchIndex is used to wrap and capture all information
    and actions applied to a RediSearch index including creation,
    manegement, and query construction.
    """
    escaper = TokenEscaper()

    @staticmethod
    def key(provider: str, paper_id: str) -> str:
        return f"{provider}:arXiv:{paper_id}"

    async def create(
        self,
        fields: list,
        index_name: str,
        redis_conn: Redis,
        prefix: str
    ):
        # Create Index
        await redis_conn.ft(index_name).create_index(
            fields = fields,
            definition= IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def process_tags(self, categories: list, years: list) -> str:
        """
        Helper function to process tags data. TODO - factor this
        out so it's agnostic to the name of the field.

        Args:
            categories (list): List of categories.
            years (list): List of years.

        Returns:
            str: RediSearch tag query string.
        """
        tag = "("
        if years:
            years = "|".join([self.escaper.escape(year) for year in years])
            tag += f"(@year:{{{years}}})"
        if categories:
            categories = "|".join([self.escaper.escape(cat) for cat in categories])
            if tag:
                tag += f" (@categories:{{{categories}}})"
            else:
                tag += f"(@categories:{{{categories}}})"
        tag += ")"
        # if no tags are selected
        if len(tag) < 3:
            tag = "*"
        return tag

    def query(self, categories, years, offset: int, limit: int) -> Query:
        """
        Create a RediSearch query to perform standard searches.

        Args:

        Returns:
            Query: RediSearch Query

        """
        # Parse tags to create query
        tag_query = self.process_tags(categories, years)
        return (
            Query(tag_query)
            .paging(offset, limit)
            .dialect(2)
        )

    def vector_query(self, request: SimilarityRequest) -> Query:
        """
        Create a RediSearch query to perform hybrid vector and tag based searches.

        Args:
            request (SimilarityRequest): Request object.

        Returns:
            Query: RediSearch Query

        """
        # Parse tags to create query
        tag_query = self.process_tags(request.categories, request.years)
        base_query = f'{tag_query}=>[{request.search_type} {request.number_of_results} @vector $vector AS similarity_score]'
        return (
            Query(base_query)
            .sort_by("similarity_score")
            .paging(0, request.number_of_results)
            .dialect(2)
        )

    def count_query(self, request: SimilarityRequest) -> Query:
        """
        Create a RediSearch query to count available documents.

        Args:
            request (SimilarityRequest): Request object.

        Returns:
            Query: RediSearch Query
        """
        # Parse tags to create query
        tag_query = self.process_tags(request.categories, request.years)
        return (
            Query(f'{tag_query}')
            .no_content()
            .dialect(2)
        )

