from enum import Enum

from arxiv.providers.cohere import CohereProvider
from arxiv.providers.huggingface import HuggingFaceProvider


class Provider(Enum):
    huggingface = "huggingface"
    openai = "openai"
    cohere = "cohere"