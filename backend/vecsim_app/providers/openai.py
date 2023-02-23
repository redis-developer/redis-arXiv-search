import numpy as np

from typing import List
from vecsim_app import config


class OpenAIProvider:
    def __init__(self):
        try:
            import openai

            openai.api_key = config.OPENAI_API_KEY
            self.client = openai.Embedding
            self.model = config.OPENAI_EMBEDDING_MODEL
        except ImportError:
            raise ValueError(
                "Could not import openai python package. "
                "Please it install it with `pip install openai`."
            )

    async def embed_documents(
        self,
        texts: List[str],
        preprocess: callable,
        chunk_size: int = 1000
    ) -> np.array:
        """
        Call out to OpenAI's embedding endpoint for embedding searchable docs.

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
            response = await self.client.acreate(
                input=batch,
                engine=self.model
            )
            results += [r["embedding"] for r in response["data"]]
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
        embedding = (await self.client.acreate(
            input=[text],
            engine=self.model
        ))["data"][0]["embedding"]
        return np.array(embedding, dtype=np.float32)