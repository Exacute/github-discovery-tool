import os
import json
from typing import List, Dict, Any
from app.models import Repo
from app.embeddings import get_embeddings_provider, EmbeddingsProvider
from app import db


class SemanticSearchEngine:
    """Semantic search engine for finding relevant repositories."""

    def __init__(self, embeddings_provider: EmbeddingsProvider = None):
        self.embeddings = embeddings_provider or get_embeddings_provider()

    def search(
        self,
        query: str,
        language: str = None,
        topic: str = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for repositories.

        Returns top repositories sorted by relevance and stars.
        """
        # Get all repos (apply language/topic filters first for efficiency)
        repos_query = Repo.query

        if language:
            repos_query = repos_query.filter(Repo.language.ilike(language))

        if topic:
            repos_query = repos_query.filter(Repo.topics.contains(f'"{topic}"'))

        repos = repos_query.all()

        if not repos:
            return []

        # Generate embeddings
        query_embedding = self.embeddings.embed(query)

        # Calculate similarity scores
        scored_repos = []
        for repo in repos:
            # Create search text from repo name and description
            search_text = f"{repo.name} {repo.description or ''}"
            repo_embedding = self.embeddings.embed(search_text)

            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_embedding, repo_embedding)

            scored_repos.append({
                'repo': repo,
                'similarity': similarity,
            })

        # Sort by similarity and stars
        scored_repos.sort(
            key=lambda x: (x['similarity'], x['repo'].stars),
            reverse=True
        )

        # Return top N repos
        return [repo['repo'].to_dict() for repo in scored_repos[:limit]]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
        magnitude2 = sum(b ** 2 for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)
