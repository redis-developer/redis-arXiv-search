from enum import Enum

from vecsim_app.providers.cohere import CohereProvider


class Provider(Enum):
    huggingface = "huggingface"
    openai = "openai"
    cohere = "cohere"