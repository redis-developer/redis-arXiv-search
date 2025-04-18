import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from arxivsearch import config
from arxivsearch.api.main import api_router
from arxivsearch.db.utils import get_async_index
from arxivsearch.spa import SinglePageApplication

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    index = await get_async_index()
    async with index:
        yield


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=config.API_DOCS,
    openapi_url=config.OPENAPI_DOCS,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    api_router,
    prefix=config.API_V1_STR,
)

# static image files
app.mount("/data", StaticFiles(directory="data"), name="data")

## mount the built GUI react files into the static dir to be served.
current_file = Path(__file__)
project_root = current_file.parent.resolve()
gui_build_dir = project_root / "templates" / "build"
app.mount(path="/", app=SinglePageApplication(directory=gui_build_dir), name="SPA")


def main():
    server_attr = {"host": "0.0.0.0", "reload": True, "port": 8888, "workers": 1}
    if config.DEPLOYMENT_ENV == "prod":
        server_attr.update(
            {
                "reload": False,
                "workers": 2,
                "ssl_keyfile": "app/backend/arxivsearch/key.pem",
                "ssl_certfile": "app/backend/arxivsearch/full.pem",
            }
        )

    uvicorn.run("arxivsearch.main:app", **server_attr)


if __name__ == "__main__":
    main()
