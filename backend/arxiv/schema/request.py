from pydantic import BaseModel

class BaseRequest(BaseModel):
    categories: list
    years: list
    provider: str
    number_of_results: int = 15
    search_type: str = "KNN"

class SimilarityRequest(BaseRequest):
    paper_id: str

class UserTextSimilarityRequest(BaseRequest):
    user_text: str
