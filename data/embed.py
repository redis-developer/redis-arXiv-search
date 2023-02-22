import json
import pandas as pd
import os
import re
import string
import pickle


DATA_PATH = "arxiv-metadata-oai-snapshot.json"
YEAR_CUTOFF = 2012
YEAR_PATTERN = r"(19|20[0-9]{2})"
ML_CATEGORY = "cs.LG"


def process(paper: dict):
    paper = json.loads(paper)
    if paper['journal-ref']:
        years = [int(year) for year in re.findall(YEAR_PATTERN, paper['journal-ref'])]
        years = [year for year in years if (year <= 2022 and year >= 1991)]
        year = min(years) if years else None
    else:
        year = None
    return {
        'id': paper['id'],
        'title': paper['title'],
        'year': year,
        'authors': paper['authors'],
        'categories': ','.join(paper['categories'].split(' ')),
        'abstract': paper['abstract']
    }

def papers():
    with open(DATA_PATH, 'r') as f:
        for paper in f:
            paper = process(paper)
            if paper['year']:
                if paper['year'] >= YEAR_CUTOFF and ML_CATEGORY in paper['categories']:
                    yield paper

def export(provider: str, df: pd.DataFrame):
    with open(f'arxiv_{provider}_embeddings.pkl', 'wb') as f:
        data = pickle.dumps(df)
        f.write(data)

def clean_description(description: str):
    if not description:
        return ""
    # remove unicode characters
    description = description.encode('ascii', 'ignore').decode()

    # remove punctuation
    description = re.sub('[%s]' % re.escape(string.punctuation), ' ', description)

    # clean up the spacing
    description = re.sub('\s{2,}', " ", description)

    # remove urls
    #description = re.sub("https*\S+", " ", description)

    # remove newlines
    description = description.replace("\n", " ")

    # remove all numbers
    #description = re.sub('\w*\d+\w*', '', description)

    # split on capitalized words
    description = " ".join(re.split('(?=[A-Z])', description))

    # clean up the spacing again
    description = re.sub('\s{2,}', " ", description)

    # make all words lowercase
    description = description.lower()

    return description.strip()


def huggingface(df, texts):
    from sentence_transformers import SentenceTransformer

    provider = "huggingface"
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model = SentenceTransformer(model_name)

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    df = df.reset_index().drop('index', axis=1)
    df['vector'] = embeddings.tolist()
    export(provider, df)


async def openai(df, texts):
    import openai
    import time

    provider = "openai"
    model_name = "text-embedding-ada-002"
    openai.api_key = os.environ["OPENAI_API_KEY"]

    embeddings = []

    def batchify(seq: list, size: int):
        for pos in range(0, len(seq), size):
            yield seq[pos:pos + size]

    for i, batch in enumerate(batchify(texts, size=30)):
        st = time.time()
        response = await openai.Embedding.acreate(
            input=batch,
            engine=model_name
        )
        embeddings += [r["embedding"] for r in response["data"]]
        print(f"Finished batch {i} in {time.time()-st} sec")

        df['vector'] = embeddings.tolist()
        export(provider, df)


if __name__ == "__main__":
    df = pd.DataFrame(papers()).sample(n=100)
    texts = df.apply(lambda r: clean_description(r['title'] + ' ' + r['abstract']), axis=1).tolist()

    huggingface(df, texts)

    openai(df, texts)


