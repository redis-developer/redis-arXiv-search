from aredis_om import (
    Field,
    HashModel
)

# Paper Model
class Paper(HashModel):
    paper_id: str
    title: str = Field(index=True, full_text_search=True)
    authors: str
    abstract: str = Field(index=True, full_text_search=True)
    categories: str = Field(index=True)
    year: int = Field(index=True)
