from pydantic import BaseModel


class SimilarityRequest(BaseModel):
    paper_id: str
    number_of_results: int = 15
    search_type: str = "KNN"

class UserTextSimilarityRequest(BaseModel):
    user_text: str
    number_of_results: int = 15
    search_type: str = "KNN"
