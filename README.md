
<div align="center">
    <a href="https://github.com/redis-developer/redis-arxiv-search"><img src="https://redis.io/wp-content/uploads/2024/04/Logotype.svg?raw=true" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://docsearch.redisvl.com"><b>Hosted Demo</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/redis-developer/redis-arxiv-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/redis-developer/redis-ai-resources"><b>More AI Recipes</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://datasciencedojo.com/blog/ai-powered-document-search/"><b>Blog Post</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://redis.io/docs/interact/search-and-query/advanced-concepts/vectors/"><b>Redis Vector Search Documentation</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>

# 🔎 Redis arXiv Search
*This repository is the official codebase for the arxiv paper search app hosted at: **https://docsearch.redisvl.com***


[Redis](https://redis.com) is a highly performant, production-ready vector database, which can be used for many types of applications. Here we showcase Redis vector search applied to a document retrieval use case. Read more about AI-powered search in [the technical blog post](https://datasciencedojo.com/blog/ai-powered-document-search/) published by our partners, *[Data Science Dojo](https://datasciencedojo.com)*.

### Dataset

The arXiv papers dataset was sourced from the the following [Kaggle link](https://www.kaggle.com/Cornell-University/arxiv). arXiv is commonly used for scientific research in a variety of fields. Exposing a semantic search layer enables natural human language to be used to discover relevant papers.


## Application

This app was built as a Single Page Application (SPA) with the following components:

- **[Redis Stack](https://redis.io/docs/stack/)** for vector database
- **[RedisVL](https://redisvl.com)** for Python vector db client
- **[FastAPI](https://fastapi.tiangolo.com/)** for Python API
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** for schema and validation
- **[React](https://reactjs.org/)** (with Typescript)
- **[Docker Compose](https://docs.docker.com/compose/)** for development
- **[MaterialUI](https://material-ui.com/)** for some UI elements/components
- **[React-Bootstrap](https://react-bootstrap.github.io/)** for some UI elements
- **[Huggingface](https://huggingface.co/sentence-transformers)**, **[OpenAI](https://platform.openai.com)**, and **[Cohere](https://cohere.com)** for vector embedding creation

Some inspiration was taken from this [tiangolo/full-stack-fastapi-template](https://github.com/tiangolo/full-stack-fastapi-template)
and turned into a SPA application instead of a separate front-end server approach.

### General Project Structure

```
/backend
    /arxivsearch
        /api
            /routes
                papers.py # primary paper search logic lives here
        /db
            load.py # seeds Redis DB
            redis_helpers.py # redis util
        /schema
            # pydantic models for serialization/validation from API
        /tests
        /utils
        config.py
        spa.py # logic for serving compiled react project
        main.py # entrypoint
/frontend
    /public
        # index, manifest, logos, etc.
    /src
        /config
        /styles
        /views
            # primary components live here

        api.ts # logic for connecting with BE
        App.tsx # project entry
        Routes.tsk # route definitions
        ...
/data
    # folder mounted as volume in Docker
    # load script auto populates initial data from S3

```

### Embedding Providers
Embeddings represent the semantic properies of the raw text and enable vector similarity search. This applications supports `HuggingFace`, `OpenAI`, and `Cohere` embeddings out of the box.

| Provider        | Embedding Model           | Required?  |
| ------------- |-------------| ----- |
| HuggingFace      | `sentence-transformers/all-mpnet-base-v2` | Yes |
| OpenAI      | `text-embedding-ada-002`      |   Yes |
| Cohere | `embed-multilingual-v3.0`      |    Yes |

**Interested in a different embedding provider?** Feel free to open a PR and make a suggested addition.

**Want to use a different model than the one listed?** Set the following environment variables in your `.env` file (see below) to change:

- `SENTENCE_TRANSFORMER_MODEL`
- `OPENAI_EMBEDDING_MODEL`
- `COHERE_EMBEDDING_MODEL`


## 🚀 Running the App
1. Before running the app, install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Clone (and optionally fork) this Github repo to your machine.
    ```bash
    $ git clone https://github.com/RedisVentures/redis-arXiv-search.git
    ```
3. Make a copy of the `.env.template` file:
    ```bash
    $ cd redis-arXiv-search/
    $ cp .env.template .env
    ```
    - Add your `OPENAI_API_KEY` to the `.env` file. **Need one?** [Get an API key](https://platform.openai.com)
    - Add you `COHERE_API_KEY` to the `.env` file. **Need one?** [Get an API key](https://cohere.ai)

### Redis Stack Docker (Local) with make
```bash
make build
```


## Customizing (optional)

### Run local redis with Docker
```bash
docker run -d --name redis -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

### FastApi with poetry
To run the backend locally

1. `cd backend`
2. `poetry install`
3. `poetry run start-app`

*poetry run start-app runs the initial db load script and launch the API*

### React Dev Environment
It's typically easier to build front end in an interactive environment, testing changes in realtime.

1. Deploy the app using steps above.
2. Install packages
    ```bash
    $ cd frontend/
    $ npm install
    ````
4. Use `npm` to serve the application from your machine
    ```bash
    $ npm run start
    ```
5. Navigate to `http://localhost:3000` in a browser.

All changes to your frontend code will be reflected in your display in semi realtime.


### Troubleshooting
Every once and a while you need to clear out some Docker cached artifacts. Run `docker system prune`, restart Docker Desktop, and try again.

This project is maintained by Redis on a good faith basis. Please, open an issue here on GitHub and we will try to be responsive to these.
