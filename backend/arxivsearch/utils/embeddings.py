import re
import string

from redisvl.utils.vectorize import (
    CohereTextVectorizer,
    HFTextVectorizer,
    OpenAITextVectorizer,
)

from arxivsearch import config
from arxivsearch.schema.models import Provider


def preprocess_text(text: str) -> str:
    if not text:
        return ""
    # remove unicode characters
    text = text.encode("ascii", "ignore").decode()

    # remove punctuation
    text = re.sub("[%s]" % re.escape(string.punctuation), " ", text)

    # clean up the spacing
    text = re.sub("\s{2,}", " ", text)

    # remove newlines
    text = text.replace("\n", " ")

    # split on capitalized words
    text = " ".join(re.split("(?=[A-Z])", text))

    # clean up the spacing again
    text = re.sub("\s{2,}", " ", text)

    # make all words lowercase
    text = text.lower()

    return text.strip()


class Embeddings:

    def __init__(self):
        self.oai_vectorizer = OpenAITextVectorizer(model=config.OPENAI_EMBEDDING_MODEL)
        self.co_vectorizer = CohereTextVectorizer(model=config.COHERE_EMBEDDING_MODEL)
        self.hf_vectorizer = HFTextVectorizer(model=config.SENTENCE_TRANSFORMER_MODEL)

    async def get(self, provider: str, text: str):
        """
        Create embeddings from input text.

        Args:
            provider (str): Specified provider to use
            text (str): Text to embed.
        """
        if provider == Provider.huggingface.value:
            # Use HuggingFace Sentence Transformer
            return self.hf_vectorizer.embed(text, preprocess=preprocess_text)
        elif provider == Provider.openai.value:
            # Use OpenAI Embeddings API
            return await self.oai_vectorizer.aembed(text, preprocess=preprocess_text)
        elif provider == Provider.cohere.value:
            return self.co_vectorizer.embed(
                text, input_type="search_query", preprocess=preprocess_text
            )
