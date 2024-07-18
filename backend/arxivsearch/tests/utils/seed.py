import json
import os
import numpy as np
from arxivsearch import config
from arxivsearch.db import redis_helpers


def seed_test_db():
    cwd = os.getcwd()
    with open(f"{cwd}/arxivsearch/tests/utils/test_vectors.json", "r") as f:
        papers = json.load(f)

    # convert to bytes
    for paper in papers:
        paper["huggingface"] = np.array(
            paper["huggingface"], dtype=np.float32
        ).tobytes()
        paper["openai"] = np.array(paper["openai"], dtype=np.float32).tobytes()
        paper["cohere"] = np.array(paper["cohere"], dtype=np.float32).tobytes()

    index = redis_helpers.get_index()
    index.connect(redis_url=config.REDIS_URL)
    index.load(data=papers, id_field="paper_id")
    return papers
