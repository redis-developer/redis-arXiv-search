from enum import Enum

from vecsim_app.providers.openai import OpenAIProvider
from vecsim_app.providers.huggingface import HuggingFaceProvider


class Provider(Enum):
    huggingface = "huggingface"
    openai = "openai"