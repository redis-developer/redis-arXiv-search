from enum import Enum

from vecsim_app.providers.openai import OpenAIProvider
from vecsim_app.providers.huggingface import HuggingFaceProvider
from vecsim_app.providers.cohere import CohereProvider


class Provider(Enum):
    huggingface = "huggingface"
    openai = "openai"
    cohere = "cohere"