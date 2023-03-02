# Data

Document search applications much have embedded documents stored in a low-latency vector database like Redis prior to serving results.

![document embedding](assets/DocVector.png)

Out of the box, the docker containers shipped with this app/repo can run without manually generating any data. However, if you wish to create your own embeddings, use some of the resources below. Generate data before trying to run this application.

## Useful Notebooks

1. `create-arxiv-embeddings.ipynb`
    - Uses local CPU and creates embeddings for ~1k machine learning papers with HuggingFace Sentence Transformers and OpenAI APIs.
    - Outputs: `arxiv_huggingface_embeddings_1000.pkl` AND `arxiv_openai_embeddings_1000.pkl`

2. `saturncloud/single-gpu-arxiv-embddings.ipynb`
    - Uses RAPIDS (CuDF) and GPU on Saturn Cloud to speed up embedding creation with HuggingFace Sentence Transformer models. Much larger subset (100k).
    - Output: `arxiv_embeddings_100000.pkl`

3. `saturncloud/multi-gpu-arxiv-embeddings.ipynb`
    - Uses RAPIDS and Dask (Dask CuDF) on Saturn Cloud to parallelize embedding creation with HuggingFace Sentence Transformer models. Much much larger subset (700k). Only output 300k to file.
    - Output: `arxiv_embeddings_300000pkl`.
