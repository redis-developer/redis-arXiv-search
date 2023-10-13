from enum import Enum

from arxiv.embeddings.providers.cohere import CohereProvider


class Provider(Enum):
    huggingface = "huggingface"
    openai = "openai"
    cohere = "cohere"