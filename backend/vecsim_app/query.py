from redis.asyncio import Redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query


async def create_flat_index(
    redis_conn: Redis,
    number_of_vectors: int,
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
    categories_field = TagField("categories")
    await redis_conn.ft().create_index([text_field, categories_field])


async def create_hnsw_index(
    redis_conn: Redis,
    number_of_vectors: int,
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
    categories_field = TagField("categories")
    await redis_conn.ft().create_index([text_field, categories_field])


def create_query(
    search_type: str="KNN",
    number_of_results: int=20
) -> Query:
    base_query = f'*=>[{search_type} {number_of_results} @vector $vec_param AS vector_score]'
    q = Query(base_query)
    q.sort_by("vector_score")
    q.paging(0, number_of_results)
    q.return_fields("paper_id", "paper_pk", "vector_score")
    q.dialect(2)
    return q
