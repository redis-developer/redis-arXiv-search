
<div align="center">
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><img src="https://github.com/RedisVentures/redis-arXiv-search/blob/main/backend/vecsim_app/data/redis-logo.png?raw=true" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://docsearch.redisventures.com"><b>Hosted Demo</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://redis.io/docs/stack/search/reference/vectors/"><b>Redis VSS Documentation</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>

# Redis arXiv Search Demo

This repository is the codebase for the arxiv paper search demo hosted at: https://docsearch.redisventures.com

This arXiv demo showcases the vector search similarity (VSS) capability within Redis Stack and Redis Enterprise.
Through the RediSearch module, vector types and indexes can be added to Redis. This turns Redis into
a highly performant vector database which can be used for all types of applications.


![Screen Shot 2022-09-20 at 12 20 16 PM](https://user-images.githubusercontent.com/13009163/191346916-4b8f648f-7552-4910-ad4e-9cc117230f00.png)

## Datasets

The dataset was taken from the the following [Kaggle link](https://www.kaggle.com/Cornell-University/arxiv).

Download and extract the zip file and place the json file (`arxiv-metadata-oai-snapshot.json`) in the `data/` directory.

## Application

This app was built as a Single Page Application (SPA) with the following components:

- **[Redis Stack](https://redis.io/docs/stack/)**: Vector database + JSON storage
- **[FastAPI](https://fastapi.tiangolo.com/)** (Python 3.8)
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** for schema and validation
- **[React](https://reactjs.org/)** (with Typescript)
- **[Redis OM](https://redis.io/docs/stack/get-started/tutorials/stack-python/)** for ORM
- **[Docker Compose](https://docs.docker.com/compose/)** for development
- **[MaterialUI](https://material-ui.com/)** for some UI elements/components
- **[React-Bootstrap](https://react-bootstrap.github.io/)** for some UI elements
- **[Huggingface Tokenizers + Models](https://huggingface.co/sentence-transformers)** for vector embedding creation

Some inspiration was taken from this [Cookiecutter project](https://github.com/Buuntu/fastapi-react)
and turned into a SPA application instead of a separate front-end server approach.

## Running Locally

>Before running locally - you should download the data and run through the `arXivPrepSubset.ipynb` notebook to generate some sample embeddings.

Setup python environment
- If you use conda, take advantage of the Makefile included here: `make env`
- Otherwise, setup your virtual env however and install python deps in `requirements.txt`

To launch app, run the following
- ``docker compose up`` in same directory as ``docker-compose.yml``
- Navigate to ``http://localhost:8888`` in a browser

### Building the containers

The first time you run `docker compose up` it will automatically build your Docker images based on the `Dockerfile`. However, in future passes when you need to rebuild, simply run: `docker compose up --build` to force a new build.

### Using a React development env
It's typically easier to write front end code in an interactive environment (**outside of Docker**)where one can test out code changes in real time. In order to use this approach:

1. Follow steps from previous section with Docker Compose to deploy the backend API.
2. Skip the step about launching a browser at host/port.
3. `cd gui/` directory and use `yarn` to install packages: `yarn install --no-optional` (you may need to use `npm` to install `yarn`).
4. Use `yarn` to serve the application from your machine: `yarn start`.
5. Navigate to `http://localhost:3000` in a browser.

### Troubleshooting

#### Issues building the container
- Sometimes it works if you try again. Or maybe you need to clear out some Docker cache. Run `docker system prune`, restart Docker Desktop, and try again.
- The generated `node_modules` folder (under `gui/` when running the app outside of Docker) can mess things up when building docker images. Delete that folder (if present) and try rebuilding again.
