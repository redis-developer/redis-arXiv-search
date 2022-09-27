from pydantic import BaseModel


class SimilarityRequest(BaseModel):
    paper_id: str
    categories: list
    years: list
    number_of_results: int = 15
    search_type: str = "KNN"

class UserTextSimilarityRequest(BaseModel):
    user_text: str
    categories: list
    years: list
    number_of_results: int = 15
    search_type: str = "KNN"
