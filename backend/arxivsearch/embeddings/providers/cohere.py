import numpy as np

from typing import List
from arxivsearch import config


class CohereProvider:
    def __init__(self):
        try:
            import cohere

            self.client = cohere.AsyncClient(config.COHERE_API_KEY)
            self.model = config.COHERE_EMBEDDING_MODEL
        except ImportError:
            raise ValueError(
                "Could not import cohere python package. "
                "Please it install it with `pip install cohere`."
            )

    async def embed_documents(
        self,
        texts: List[str],
        preprocess: callable,
        chunk_size: int = 1000
    ) -> np.array:
        """
        Call out to Cohere's embedding endpoint for embedding searchable docs.

        Args:
            texts: The list of texts to embed.
            chunk_size: The maximum number of texts to send to OpenAI at once
                (max 1000).
        Returns:
            Array of embeddings, one for each text.
        """
        def batchify(seq: list, size: int):
            for pos in range(0, len(seq), size):
                yield [preprocess(chunk) for chunk in seq[pos:pos + size]]
        results = []
        for batch in batchify(texts, chunk_size):
            response = await self.client.embed(texts=batch, model=self.model)
            results.extend(response.embeddings)
        return np.array(results, dtype=np.float32)

    async def embed_query(self, text: str, preprocess: callable) -> np.array:
        """
        Call out to OpenAI's embedding endpoint for embedding query text.

        Args:
            text: The text to embed.
        Returns:
            Embeddings for the text.
        """
        text = preprocess(text)
        response = await self.client.embed(texts=[text], model=self.model)
        return np.array(response.embeddings[0], dtype=np.float32)