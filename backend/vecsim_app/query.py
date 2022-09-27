from config import INDEX_NAME
from redis.asyncio import Redis
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)
from redis.commands.search.field import (
    VectorField,
    TagField
)


async def create_index(redis_conn, prefix: str, v_field: VectorField):
    categories_field = TagField("categories")
    year_field = TagField("year")
    # Create Index
    await redis_conn.ft(INDEX_NAME).create_index(
        fields = [v_field, categories_field, year_field],
        definition= IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
    )

async def create_flat_index(
    redis_conn: Redis,
    number_of_vectors: int,
    prefix: str,
    distance_metric: str='L2'
):
    text_field = VectorField(
        "vector",
        "FLAT", {
            "TYPE": "FLOAT32",
            "DIM": 768,
            "DISTANCE_METRIC": distance_metric,
            "INITIAL_CAP": number_of_vectors,
            "BLOCK_SIZE": number_of_vectors
        }
    )
    await create_index(redis_conn, prefix, text_field)


async def create_hnsw_index(
    redis_conn: Redis,
    number_of_vectors: int,
    prefix: str,
    distance_metric: str='COSINE'
):
    text_field = VectorField(
        "vector",
        "HNSW", {
            "TYPE": "FLOAT32",
            "DIM": 768,
            "DISTANCE_METRIC": distance_metric,
            "INITIAL_CAP": number_of_vectors,
        }
    )
    await create_index(redis_conn, prefix, text_field)


def create_query(
    categories: list,
    years: list,
    search_type: str="KNN",
    number_of_results: int=20
) -> Query:

    tag = "("
    if years:
        years = " | ".join(years)
        tag += f"@year:{{{years}}}"
    if categories:
        categories = " | ".join(categories)
        tag += f"@categories:{{{categories}}}"
    tag += ")"
    # if no tags are selected
    if len(tag) < 3:
        tag = "*"
    print(tag, flush=True)
    base_query = f'{tag}=>[{search_type} {number_of_results} @vector $vec_param AS vector_score]'
    return Query(base_query)\
        .sort_by("vector_score")\
        .paging(0, number_of_results)\
        .return_fields("paper_id", "paper_pk", "vector_score")\
        .dialect(2)
