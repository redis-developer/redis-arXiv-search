from typing import Any
from pydantic import BaseModel, field_validator

from arxivsearch.schema.provider import Provider


class BaseRequest(BaseModel):
    categories: list
    years: list
    provider: Provider
    number_of_results: int = 15
    search_type: str = "KNN"


class PaperSimilarityRequest(BaseRequest):
    paper_id: str


class UserTextSimilarityRequest(BaseRequest):
    user_text: str


class Paper(BaseModel):
    id: str
    paper_id: str
    authors: str
    categories: str
    year: str
    title: str
    abstract: str = ""


class BaseSearchPaper(Paper):
    # vector embeddings
    huggingface: str
    openai: str
    cohere: str


class VectorSearchPaper(Paper):
    vector_distance: float
    similarity_score: float

    def __init__(self, *args, **kwargs):
        kwargs["similarity_score"] = 1 - float(kwargs["vector_distance"])
        super().__init__(*args, **kwargs)


class SearchResponse(BaseModel):
    total: int
    papers: list[BaseSearchPaper]


class VectorSearchResponse(BaseModel):
    total: int
    papers: list[VectorSearchPaper]
