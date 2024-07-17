from fastapi import APIRouter

from arxivsearch.api.routes import papers

api_router = APIRouter()
api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
