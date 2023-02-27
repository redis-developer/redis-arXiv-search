import uvicorn
import logging
from pathlib import Path

from aredis_om import Migrator, get_redis_connection
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from vecsim_app import config
from vecsim_app.api import routes
from vecsim_app.models import Paper
from vecsim_app.spa import SinglePageApplication

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=config.API_DOCS,
    openapi_url=config.OPENAPI_DOCS
)

# Routers
app.include_router(
    routes.paper_router,
    prefix=config.API_V1_STR + "/paper",
    tags=["papers"]
)


@app.on_event("startup")
async def startup():
    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    Paper.Meta.database = get_redis_connection(url=config.REDIS_URL, decode_responses=True)
    await Migrator().run()

# static image files
app.mount("/data", StaticFiles(directory="data"), name="data")

## mount the built GUI react files into the static dir to be served.
current_file = Path(__file__)
project_root = current_file.parent.resolve()
gui_build_dir = project_root / "templates" / "build"
app.mount(
    path="/", app=SinglePageApplication(directory=gui_build_dir), name="SPA"
)
if __name__ == "__main__":
    import logging
    import os

    logging.basicConfig(level=logging.INFO)

    env = os.environ.get("DEPLOYMENT", "prod")
    logging.info(f"Running in {env} mode")

    server_attr = {
        "host": config.SERVER_HOST,
        "reload": True,
        "port": int(config.SERVER_PORT),
        "workers": 1,
        "log_level": "debug",
    }
    if env == "prod":
        server_attr.update(
            {
                "reload": False,
                "workers": 2,
                "ssl_keyfile": "key.pem",
                "ssl_certfile": "full.pem",
            }
        )
        app.add_middleware(
            CORSMiddleware,
            allow_origins="*",
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    uvicorn.run("vecsim_app.main:app", **server_attr)
