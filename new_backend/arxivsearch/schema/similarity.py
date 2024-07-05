from pydantic import BaseModel

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
