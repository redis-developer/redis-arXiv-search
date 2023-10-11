import numpy as np
from arxiv import config
from typing import (
    List
)


class HuggingFaceProvider:
    def __init__(self):
        """Initialize the Hugging Face sentence_transformer client"""
        try:
            import sentence_transformers

            self.client = sentence_transformers.SentenceTransformer(
                config.SENTENCE_TRANSFORMER_MODEL
            )
        except ImportError:
            raise ValueError(
                "Could not import sentence_transformers python package. "
                "Please install it with `pip install sentence_transformers`."
            )

    def embed_documents(self, texts: List[str], preprocess: callable) -> np.array:
        """
        Compute doc embeddings using a HuggingFace transformer model.

        Args:
            texts: The list of texts to embed.
        Returns:
            Array of embeddings, one for each text.
        """
        texts = list(map(lambda x: preprocess(x), texts))
        return self.client.encode(texts, normalize_embeddings=True)

    def embed_query(self, text: str, preprocess: callable) -> np.array:
        """
        Compute query embeddings using a HuggingFace transformer model.

        Args:
            text: The text to embed.
        Returns:
            Embeddings for the text.
        """
        print(f"-- preprocessing text {text}", flush=True)
        text = preprocess(text)
        print(f"-- preprocessed text -- {text}", flush=True)
        return self.client.encode(text, normalize_embeddings=True)