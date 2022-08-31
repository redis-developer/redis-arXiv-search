from aredis_om import (
    Field,
    HashModel
)

# Paper Model
class Paper(HashModel):
    paper_id: str
    title: str
    authors: str
    abstract: str
    categories: str = Field(index=True)
    year: int = Field(index=True)
