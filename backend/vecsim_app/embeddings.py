import re
import string

from vecsim_app.providers import (
    Provider,
    CohereProvider
)
from redisvl.vectorize.text import OpenAITextVectorizer, HFTextVectorizer


def preprocess_text(text: str) -> str:
    if not text:
        return ""
    # remove unicode characters
    text = text.encode('ascii', 'ignore').decode()

    # remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

    # clean up the spacing
    text = re.sub('\s{2,}', " ", text)

    # remove newlines
    text = text.replace("\n", " ")

    # split on capitalized words
    text = " ".join(re.split('(?=[A-Z])', text))

    # clean up the spacing again
    text = re.sub('\s{2,}', " ", text)

    # make all words lowercase
    text = text.lower()

    return text.strip()


class Embeddings:

    def __init__(self):
        # Initialize embedding providers if relevant
        self.hf_vectorizer = HFTextVectorizer()
        self.oai_vectorizer = OpenAITextVectorizer()
        # TODO add cohere to redisvl
        self.co_vectorizer = CohereProvider()

    async def get(self, provider: str, text: str):
        """
        Create embeddings from input text.

        Args:
            provider (str): Specified provider to use
            text (str): Text to embed.
        """

        if provider == Provider.huggingface.value:
            # Use HuggingFace Sentence Transformer
            return await self.hf_vectorizer.aembed(
                text,
                preprocess=preprocess_text
            )
        elif provider == Provider.openai.value:
            # Use OpenAI Embeddings API
            return await self.oai_vectorizer.aembed(
                text,
                preprocess=preprocess_text
            )
        elif provider == Provider.cohere.value:
            return await self.co_vectorizer.embed_query(
                text,
                preprocess=preprocess_text
            )


