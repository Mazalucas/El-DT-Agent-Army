"""Embedding providers for semantic search."""

from abc import ABC, abstractmethod
from typing import List, Optional

from agents_army.core.agent import LLMProvider


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        pass

    @property
    @abstractmethod
    def dimensions(self) -> int:
        """Get embedding dimensions."""
        pass


class MockEmbeddings(EmbeddingProvider):
    """
    Mock embedding provider for testing and development.
    
    Generates simple hash-based embeddings without external dependencies.
    """

    def __init__(self, dimensions: int = 384):
        """
        Initialize MockEmbeddings.

        Args:
            dimensions: Embedding dimensions (default: 384)
        """
        self._dimensions = dimensions

    async def embed(self, text: str) -> List[float]:
        """
        Generate mock embedding using hash-based approach.

        Args:
            text: Text to embed

        Returns:
            Mock embedding vector
        """
        # Simple hash-based embedding for testing
        import hashlib

        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()

        # Convert hex to floats
        embedding = []
        for i in range(0, len(hash_hex), 2):
            if len(embedding) >= self._dimensions:
                break
            # Convert hex pair to float between -1 and 1
            val = int(hash_hex[i : i + 2], 16) / 255.0 * 2 - 1
            embedding.append(val)

        # Pad or truncate to exact dimensions
        while len(embedding) < self._dimensions:
            embedding.append(0.0)

        return embedding[: self._dimensions]

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts

        Returns:
            List of embedding vectors
        """
        return [await self.embed(text) for text in texts]

    @property
    def dimensions(self) -> int:
        """Get embedding dimensions."""
        return self._dimensions


class OpenAIEmbeddings(EmbeddingProvider):
    """
    OpenAI embedding provider.
    
    Requires openai package and OPENAI_API_KEY environment variable.
    """

    def __init__(self, model: str = "text-embedding-3-small", api_key: Optional[str] = None):
        """
        Initialize OpenAIEmbeddings.

        Args:
            model: OpenAI embedding model
            api_key: Optional API key (uses env var if not provided)
        """
        self.model = model
        self.api_key = api_key
        self._dimensions_map = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }

    async def embed(self, text: str) -> List[float]:
        """
        Generate embedding using OpenAI API.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            ImportError: If openai package not installed
            ValueError: If API key not configured
        """
        try:
            import os

            import openai

            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY not configured. Set environment variable or pass api_key."
                )

            client = openai.OpenAI(api_key=api_key)
            response = client.embeddings.create(model=self.model, input=text)
            return response.data[0].embedding

        except ImportError:
            raise ImportError(
                "openai package required. Install with: pip install openai"
            )

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts

        Returns:
            List of embedding vectors
        """
        try:
            import os

            import openai

            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not configured")

            client = openai.OpenAI(api_key=api_key)
            response = client.embeddings.create(model=self.model, input=texts)
            return [item.embedding for item in response.data]

        except ImportError:
            raise ImportError("openai package required")

    @property
    def dimensions(self) -> int:
        """Get embedding dimensions."""
        return self._dimensions_map.get(self.model, 1536)
