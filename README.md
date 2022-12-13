
<div align="center">
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><img src="https://github.com/RedisVentures/redis-arXiv-search/blob/main/backend/vecsim_app/data/redis-logo.png?raw=true" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://docsearch.redisventures.com"><b>Hosted Demo</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://datasciencedojo.com/blog/ai-powered-document-search/"><b>Blog Post</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://redis.io/docs/stack/search/reference/vectors/"><b>Redis VSS Documentation</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>

# Redis arXiv Search
*This repository is the official codebase for the arxiv paper search app hosted at: **https://docsearch.redisventures.com***

Through the [RediSearch](https://redis.io/docs/stack/search/reference/vectors/) module, vector data types and search indexes can be added to Redis. This turns Redis into a highly performant, in-memory, vector database, which can be used for many types of applications.

___

Here we showcase Redis vector similarity search (VSS) applied to a document search/retrieval use case. Read more about AI-powered search in [our blog post](https://datasciencedojo.com/blog/ai-powered-document-search/) (shout out to our friends at Data Science Dojo).


![Screen Shot 2022-09-20 at 12 20 16 PM](https://user-images.githubusercontent.com/13009163/191346916-4b8f648f-7552-4910-ad4e-9cc117230f00.png)

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

### Dataset

The arXiv dataset was sourced from the the following [Kaggle link](https://www.kaggle.com/Cornell-University/arxiv).

If you wish to modify or work with your own data...download and extract the zip and place the resulting json file (`arxiv-metadata-oai-snapshot.json`) in the `data/` directory.

## Running the App
Before running the app, install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### Use pre-built containers
Both **Redis Stack** and the paper search app run with **Docker Compose** using pre-built containers. Choose one of the methods below based on your Redis setup.

#### Redis Cloud (recommended)

1. [Get your Redis Cloud Database](https://app.redislabs.com/) (if needed).

2. Export Redis Endpoint Environment Variables:
    ```bash
    $ export REDIS_HOST=your-redis-host
    $ export REDIS_PORT=your-redis-port
    $ export REDIS_PASSOWRD=your-redis-password
    ```

3. Run the App:
    ```bash
    $ docker compose -f docker-cloud-redis.yml up
    ```
> The benefit of this approach is that the db will persist beyond application runs. So you can make updates and re run the app without having to provision the dataset or create another search index.

#### Redis Docker
```bash
$ docker compose -f docker-local-redis.yml up
```

### Customizing (optional)
You can use the Jupyter Notebooks in the [`data/`](data/README.md) directory to create paper embeddings and metadata. The pickled dataframe will end up stored in the `data/` directory and used when creating your own container.

Use the `build.sh` script to create your own, and then make sure to update the `.yml` file with the right image name.

### Running with Kubernetes
If you want to use K8s instead of Docker Compose, we have some [resources to help you get started](k8s/README.md).

### Using a React development env
It's typically easier to write front end code in an interactive environment, testing changes in realtime.

1. Deploy the app using steps above.
2. Install NPM packages (you may need to use `npm` to install `yarn`)
    ```bash
    $ cd gui/
    $ yarn install --no-optional
    ````
4. Use `yarn` to serve the application from your machine
    ```bash
    $ yarn start
    ```
5. Navigate to `http://localhost:3000` in a browser.

All changes to your local code will be reflected in your display in semi realtime.

### Using a React dev env
It's typically easier to manipulate front end code in an interactive environment (**outside of Docker**) where one can test out code changes in real time. In order to use this approach:

1. Follow steps from previous section with Docker Compose to deploy the backend API.
2. `cd gui/` directory and use `yarn` to install packages: `yarn install --no-optional` (you may need to use `npm` to install `yarn`).
3. Use `yarn` to serve the application from your machine: `yarn start`.
4. Navigate to `http://localhost:3000` in a browser.
5. Make front end changes in realtime.

### Troubleshooting
Sometimes you need to clear out some Docker cached artifacts. Run `docker system prune`, restart Docker Desktop, and try again.

Open an issue here on GitHub and we will try to be responsive to these. Additionally, please consider [contributing](CONTRIBUTING.md).