from pydantic import BaseModel


class CategoriesPredictionRequest(BaseModel):
    articles: list
    proba_threshold: float = 0.35
