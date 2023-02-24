import os

PROJECT_NAME = "vecsim_app"
API_DOCS = "/api/docs"
OPENAPI_DOCS = "/api/openapi.json"
DEFAULT_PROVIDER = "huggingface"
DISTANCE_METRIC = os.environ.get("DISTANCE_METRIC", "COSINE")
WRITE_CONCURRENCY = os.environ.get("WRITE_CONCURRENCY", 150)
INDEX_TYPE = os.environ.get("VECSIM_INDEX_TYPE", "HNSW")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis-vector-db")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "testing123")
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
API_V1_STR = "/api/v1"
DATA_LOCATION = os.environ.get("DATA_LOCATION", "../../data")

# Model Providers
SENTENCE_TRANSFORMER_MODEL = os.environ.get("SENTENCE_TRANSFORMER_MODEL", "sentence-transformers/all-mpnet-base-v2")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")