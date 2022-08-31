
<div align="center">
    <a href="https://github.com/spartee/redis-vector-search"><img src="https://github.com/RedisVentures/redis-arXiv-search/blob/master/app/vecsim_app/data/redis-logo.png?raw=true" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://redis.io/docs/stack/search/reference/vectors/"><b>Redis VSS Documentation</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>

# Redis arXiv Search Demo

This arXiv demo showcases the vector search similarity (VSS) capability within Redis Stack and Redis Enterprise.
Through the RediSearch module, vector types and indexes can be added to Redis. This turns Redis into
a highly performant vector database which can be used for all types of applications.

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

## Datasets

The dataset was taken from the the following [Kaggle link](https://www.kaggle.com/Cornell-University/arxiv).

Download and extract the zip file and place the json file (`arxiv-metadata-oai-snapshot.json`) in the `data/` directory.

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

### Running outside docker

#### Front End
You can run the 
