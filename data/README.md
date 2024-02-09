# Dataset Preparation

Document search applications require a dataset of embedded documents stored in a vector database (Redis).

![document embedding](assets/DocVector.png)

## Generate your own embeddings
Out of the box, the docker container shipped with this project runs without manually generating any data. However, if you wish to create your own document embeddings, use this provided [Jupyter Notebook](./create-arxiv-embeddings.ipynb) as a starting point.

- The notebook will generate a file called `arxiv-papers-1000.json` that contains 1,000 sampled arxiv abstracts & embeddings from a few different embedding providers (OpenAI, Cohere, and HuggingFace).
- The notebook requires a [Kaggle API key](https://kaggle.com) and all python libraries listed in the main repo requirements.txt.
