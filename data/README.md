# Data!

Generate data before trying to run this application.

### Three Notebooks

1. `arxiv-embeddings.ipynb` (app default)
    - Uses local CPU and creates embeddings for ~10k machine learning papers.
    - Output: `arxiv_embeddings_10000.pkl`

2. `single-gpu-arxiv-embddings.ipynb`
    - Uses RAPIDS (CuDF) and GPU on Saturn Cloud to speed up embedding. Much larger subset (100k).
    - Output: `arxiv_embeddings_100000.pkl`

3. `multi-gpu-arxiv-embeddings.ipynb`
    - Uses RAPIDS and Dask (Dask CuDF) on Saturn Cloud to parallelize embedding creation. Much much larger subset (700k). Only output 300k to file.
    - Output: `arxiv_embeddings_300000pkl`.


