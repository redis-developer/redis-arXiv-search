import pytest
from httpx import AsyncClient

from arxivsearch.main import app
from arxivsearch.schema.models import PaperSimilarityRequest, UserTextSimilarityRequest


@pytest.fixture
def years(papers):
    return papers[0]["year"]


@pytest.fixture
def categories(papers):
    return papers[0]["categories"]


@pytest.fixture
def bad_req_json():
    return {"not": "valid"}


@pytest.fixture
def text_req(years, categories):
    return UserTextSimilarityRequest(
        categories=[categories],
        years=[years],
        provider="huggingface",
        user_text="deep learning",
    )


@pytest.fixture
def paper_req(papers):
    return PaperSimilarityRequest(
        categories=[], years=[], provider="huggingface", paper_id=papers[0]["paper_id"]
    )


@pytest.mark.asyncio(scope="session")
async def test_root_w_filters(
    async_client: AsyncClient, years: str, categories: str
) -> None:

    response = await async_client.get(
        f"papers/?limit=1&years={years}&categories={categories}"
    )

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 1
    assert len(content["papers"]) == 1
    assert content["papers"][0]["categories"] == categories
    assert content["papers"][0]["year"] == years


@pytest.mark.asyncio(scope="session")
async def test_root_na_category(async_client: AsyncClient, years: str):

    response = await async_client.get(f"papers/?limit=1&years={years}&categories=NA")

    assert response.status_code == 200
    content = response.json()
    assert content["total"] == 0
    assert len(content["papers"]) == 0


@pytest.mark.asyncio(scope="session")
async def test_vector_by_text(
    async_client: AsyncClient,
    years: str,
    categories: str,
    text_req: UserTextSimilarityRequest,
):
    response = await async_client.post(
        f"papers/vector_search/by_text", json=text_req.model_dump()
    )

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 1
    assert len(content["papers"]) == 1
    assert content["papers"][0]["categories"] == categories
    assert content["papers"][0]["year"] == years


@pytest.mark.asyncio(scope="session")
async def test_vector_by_text_bad_input(async_client: AsyncClient, bad_req_json: dict):

    response = await async_client.post(
        f"papers/vector_search/by_text", json=bad_req_json
    )

    assert response.status_code == 422


@pytest.mark.asyncio(scope="session")
async def test_vector_by_paper(
    async_client: AsyncClient,
    paper_req: PaperSimilarityRequest,
):
    response = await async_client.post(
        f"papers/vector_search/by_paper", json=paper_req.model_dump()
    )

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 2
    assert len(content["papers"]) == 2


@pytest.mark.asyncio(scope="session")
async def test_vector_by_paper_bad_input(async_client: AsyncClient, bad_req_json: dict):

    response = await async_client.post(
        f"papers/vector_search/by_paper", json=bad_req_json
    )

    assert response.status_code == 422
