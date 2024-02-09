import os

# Project Details
PROJECT_NAME = "arxivsearch"
API_DOCS = "/api/docs"
OPENAPI_DOCS = "/api/openapi.json"
API_V1_STR = "/api/v1"

# Configuration
DEFAULT_DATASET = os.environ.get("DEFAULT_DATASET", "arxiv-papers-1000.json")
DATA_LOCATION = os.environ.get("DATA_LOCATION", "../../data")
DEPLOYMENT_ENV = os.environ.get("DEPLOYMENT", "dev")
WRITE_CONCURRENCY = os.environ.get("WRITE_CONCURRENCY", 150)
RETURN_FIELDS = [
    "paper_id",
    "authors",
    "categories",
    "year",
    "title",
    "vector_distance"
]

# Redis
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# Model Providers
DEFAULT_PROVIDER = "huggingface"
SENTENCE_TRANSFORMER_MODEL = os.environ.get("SENTENCE_TRANSFORMER_MODEL", "sentence-transformers/all-mpnet-base-v2")
OPENAI_EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
COHERE_EMBEDDING_MODEL = os.environ.get("COHERE_EMBEDDING_MODEL", "embed-multilingual-v3.0")
