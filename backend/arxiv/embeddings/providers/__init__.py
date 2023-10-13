from enum import Enum

from arxiv.embeddings.providers.cohere import CohereProvider
from arxiv.embeddings.providers.huggingface import HuggingFaceProvider


class Provider(Enum):
    huggingface = "huggingface"
    openai = "openai"
    cohere = "cohere"