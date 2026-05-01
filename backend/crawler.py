#!/usr/bin/env python
"""GitHub Repository Crawler - Fetches and indexes repositories from GitHub."""

import os
import requests
import time
from datetime import datetime
from typing import List, Dict, Optional
from app import create_app, db
from app.models import Repo

class GitHubCrawler:
    """Crawls GitHub API to fetch and index repositories."""

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize crawler.

        Args:
            github_token: GitHub API token (optional but recommended for higher rate limits)
        """
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Discovery-Tool"
        }

        if github_token:
            self.headers["Authorization"] = f"token {github_token}"

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def search_repositories(
        self,
        query: str,
        language: Optional[str] = None,
        sort: str = "stars",
        per_page: int = 30,
        max_pages: int = 1
    ) -> List[Dict]:
        """
        Search GitHub for repositories.

        Args:
            query: Search query
            language: Filter by language
            sort: Sort by (stars, forks, updated)
            per_page: Results per page (max 100)
            max_pages: Maximum pages to fetch

        Returns:
            List of repository data
        """
        repos = []
        search_query = query

        if language:
            search_query += f" language:{language}"

        params = {
            "q": search_query,
            "sort": sort,
            "order": "desc",
            "per_page": min(per_page, 100),
        }

        print(f"\nSearching GitHub: {search_query}")
        print(f"Sort by: {sort}, Fetching up to {max_pages} pages")

        for page in range(1, max_pages + 1):
            params["page"] = page

            try:
                response = self.session.get(
                    f"{self.base_url}/search/repositories",
                    params=params,
                    timeout=10
                )

                if response.status_code == 403:
                    print("\n[!] Rate limit exceeded. Try again later or use GitHub token.")
                    print("    Set GITHUB_TOKEN environment variable for higher limits.")
                    break

                if response.status_code != 200:
                    print(f"[!] Error: HTTP {response.status_code}")
                    break

                data = response.json()
                items = data.get("items", [])

                if not items:
                    print(f"[*] No more results (page {page})")
                    break

                repos.extend(items)
                print(f"[+] Fetched page {page}: {len(items)} repos (total: {len(repos)})")

                # Respect rate limits
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"[!] Request error: {e}")
                break

        return repos

    def parse_repository(self, github_repo: Dict) -> Dict:
        """
        Parse GitHub API response to our database format.

        Args:
            github_repo: Repository data from GitHub API

        Returns:
            Parsed repository data
        """
        # Parse ISO 8601 datetime string to Python datetime
        updated_at = None
        if github_repo.get('updated_at'):
            try:
                # Convert ISO 8601 string to datetime
                updated_at_str = github_repo['updated_at']
                # Remove 'Z' and parse
                updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
            except:
                updated_at = None

        return {
            'repo_id': github_repo['id'],
            'name': github_repo['name'],
            'url': github_repo['html_url'],
            'description': github_repo.get('description', ''),
            'language': github_repo.get('language'),
            'topics': github_repo.get('topics', []),
            'stars': github_repo.get('stargazers_count', 0),
            'forks': github_repo.get('forks_count', 0),
            'last_updated': updated_at,
        }

    def add_repository(self, repo_data: Dict) -> bool:
        """
        Add or update repository in database.

        Args:
            repo_data: Parsed repository data

        Returns:
            True if successful
        """
        try:
            # Check if repo already exists
            existing = Repo.query.filter_by(repo_id=repo_data['repo_id']).first()

            if existing:
                # Update existing
                existing.name = repo_data['name']
                existing.url = repo_data['url']
                existing.description = repo_data['description']
                existing.language = repo_data['language']
                existing.topics = repo_data['topics']
                existing.stars = repo_data['stars']
                existing.forks = repo_data['forks']
                existing.last_updated = repo_data['last_updated']
            else:
                # Create new
                repo = Repo(**repo_data)
                db.session.add(repo)

            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"[!] Error adding repo {repo_data['name']}: {e}")
            return False

    def crawl(
        self,
        queries: List[str],
        per_language: int = 10,
        pages_per_query: int = 2
    ) -> int:
        """
        Crawl multiple queries and populate database.

        Args:
            queries: List of search queries
            per_language: Repos to fetch per language per query
            pages_per_query: Number of pages to fetch per query

        Returns:
            Number of repositories added/updated
        """
        print("=" * 60)
        print("GitHub Repository Crawler")
        print("=" * 60)

        total_added = 0
        languages = ["Python", "JavaScript", "Go", "Rust", "Java", "C++"]

        for query in queries:
            for language in languages:
                repos = self.search_repositories(
                    query=query,
                    language=language,
                    sort="stars",
                    per_page=per_language,
                    max_pages=pages_per_query
                )

                for github_repo in repos:
                    parsed = self.parse_repository(github_repo)
                    if self.add_repository(parsed):
                        total_added += 1
                        print(f"    [+] Added: {parsed['name']} ({language})")

        return total_added


def main():
    """Main crawler function."""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub Repository Crawler")
    parser.add_argument(
        "--token",
        default=os.getenv("GITHUB_TOKEN"),
        help="GitHub API token (or set GITHUB_TOKEN env var)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Repositories to fetch per language (default: 10)"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=2,
        help="Pages to fetch per query (default: 2)"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear database before crawling"
    )

    args = parser.parse_args()

    # Create Flask app context
    app = create_app()

    with app.app_context():
        # Clear database if requested
        if args.clear:
            print("Clearing database...")
            db.session.query(Repo).delete()
            db.session.commit()
            print("[+] Database cleared")

        # Initialize crawler
        crawler = GitHubCrawler(github_token=args.token)

        # Define search queries
        queries = [
            "web framework",
            "api client",
            "database",
            "machine learning",
            "cli",
            "testing",
        ]

        # Crawl repositories
        added = crawler.crawl(
            queries=queries,
            per_language=args.limit,
            pages_per_query=args.pages
        )

        # Print summary
        total_repos = Repo.query.count()
        print("\n" + "=" * 60)
        print(f"Crawling Complete!")
        print(f"Added/Updated: {added} repositories")
        print(f"Total in database: {total_repos}")
        print("=" * 60)

        if total_repos > 0:
            # Show statistics
            languages = db.session.query(Repo.language).distinct().all()
            topics_set = set()
            for repo in Repo.query.all():
                topics_set.update(repo.topics or [])

            print(f"\nDatabase Statistics:")
            print(f"  Languages: {len(languages)}")
            print(f"  Topics: {len(topics_set)}")
            print(f"  Repositories: {total_repos}")

            # Show top repos
            print(f"\nTop 5 Most Popular:")
            top_repos = Repo.query.order_by(Repo.stars.desc()).limit(5).all()
            for i, repo in enumerate(top_repos, 1):
                print(f"  {i}. {repo.name} ({repo.language}) - {repo.stars} stars")


if __name__ == "__main__":
    main()
