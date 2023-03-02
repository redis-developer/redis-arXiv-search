import uvicorn

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from vecsim_app import config
from vecsim_app.api import routes
from vecsim_app.spa import SinglePageApplication


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=config.API_DOCS,
    openapi_url=config.OPENAPI_DOCS
)

app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

# Routers
app.include_router(
    routes.paper_router,
    prefix=config.API_V1_STR + "/paper",
    tags=["papers"]
)

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
    import os
    env = os.environ.get("DEPLOYMENT", "prod")

    server_attr = {
        "host": "0.0.0.0",
        "reload": True,
        "port": 8888,
        "workers": 1
    }
    if env == "prod":
        server_attr.update({"reload": False,
                            "workers": 2,
                            "ssl_keyfile": "key.pem",
                            "ssl_certfile": "full.pem"})

    uvicorn.run("main:app", **server_attr)
