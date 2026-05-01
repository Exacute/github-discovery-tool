import os
from abc import ABC, abstractmethod
from typing import List, Optional

class EmbeddingsProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass


class OpenAIEmbeddings(EmbeddingsProvider):
    """OpenAI embeddings provider."""

    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        try:
            import openai
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model

    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            input=text,
            model=self.model,
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model,
        )
        return [item.embedding for item in response.data]


class AnthropicEmbeddings(EmbeddingsProvider):
    """Anthropic Claude embeddings provider (requires claude-3-5-sonnet or later with API)."""

    def __init__(self, api_key: Optional[str] = None):
        # Note: As of now, Anthropic doesn't offer embeddings API
        # This is a placeholder for future support
        raise NotImplementedError(
            "Anthropic embeddings API not yet available. "
            "Use OpenAI, Ollama, or local embeddings instead."
        )


class OllamaEmbeddings(EmbeddingsProvider):
    """Local Ollama embeddings provider (requires Ollama running locally)."""

    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        try:
            import requests
        except ImportError:
            raise ImportError("requests package required. Install with: pip install requests")

        self.base_url = base_url
        self.model = model
        self.requests = __import__('requests')

        # Test connection
        try:
            response = self.requests.get(f"{self.base_url}/api/tags")
            if response.status_code != 200:
                raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}")
        except Exception as e:
            raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}: {e}")

    def embed(self, text: str) -> List[float]:
        response = self.requests.post(
            f"{self.base_url}/api/embed",
            json={"model": self.model, "input": text},
        )
        if response.status_code != 200:
            raise RuntimeError(f"Ollama error: {response.text}")
        return response.json()["embeddings"][0]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embeddings.append(self.embed(text))
        return embeddings


class LocalEmbeddings(EmbeddingsProvider):
    """Local embeddings using sentence-transformers (no API key needed)."""

    def __init__(self, model: str = "all-MiniLM-L6-v2"):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers package required. "
                "Install with: pip install sentence-transformers"
            )

        self.model = SentenceTransformer(model)

    def embed(self, text: str) -> List[float]:
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()


def get_embeddings_provider(provider: Optional[str] = None) -> EmbeddingsProvider:
    """Get embeddings provider based on environment or parameter."""
    provider = provider or os.getenv("EMBEDDINGS_PROVIDER", "openai").lower()

    if provider == "openai":
        return OpenAIEmbeddings()
    elif provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "nomic-embed-text")
        return OllamaEmbeddings(model=model, base_url=base_url)
    elif provider == "local":
        model = os.getenv("LOCAL_EMBEDDINGS_MODEL", "all-MiniLM-L6-v2")
        return LocalEmbeddings(model=model)
    else:
        raise ValueError(
            f"Unknown embeddings provider: {provider}. "
            "Choose: openai, ollama, local"
        )
