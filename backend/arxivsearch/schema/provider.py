from enum import Enum

class Provider(str, Enum):
    """Embedding model provider"""
    huggingface = "huggingface"
    openai = "openai"
    cohere = "cohere"