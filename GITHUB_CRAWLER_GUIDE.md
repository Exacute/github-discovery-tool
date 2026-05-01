# GitHub Repository Crawler Guide

## Overview

The crawler fetches real repositories from GitHub and populates the database with actual project data.

## Current Database Status

✅ **80 Real GitHub Repositories Indexed**

### Distribution by Language
- Python: 16 repos
- JavaScript: 16 repos
- Go: 16 repos
- Rust: 16 repos
- Java: 8 repos
- C++: 8 repos

### Categories Covered
- Web frameworks
- API clients
- Databases
- Machine learning
- CLI tools
- Testing frameworks

### Top Repositories by Stars
1. **FastAPI** (Python) - 97,797 stars
2. **Gin** (Go) - 88,416 stars
3. **Django** (Python) - 87,365 stars
4. **Flask** (Python) - 71,484 stars
5. **Express** (JavaScript) - 68,980 stars

## Running the Crawler

### Basic Usage

```bash
cd backend
source venv/Scripts/activate

# Fetch from GitHub (uses unauthenticated API - 60 req/hour limit)
python crawler.py --limit 10 --pages 1

# Clear database and refetch
python crawler.py --clear --limit 10 --pages 1
```

### With GitHub Token (Recommended)

Get more requests per hour (5000 instead of 60):

```bash
# Set token
export GITHUB_TOKEN=ghp_...your_token_here...

# Run crawler
python crawler.py --token $GITHUB_TOKEN --limit 20 --pages 2
```

Get your token: https://github.com/settings/tokens

### Crawler Options

```bash
python crawler.py --help

# Examples:
python crawler.py --limit 5 --pages 1      # 5 repos per language, 1 page each
python crawler.py --limit 20 --pages 2     # 20 repos per language, 2 pages each
python crawler.py --clear                   # Clear and refetch all data
python crawler.py --token TOKEN --limit 15  # Use GitHub token for higher limits
```

### Parameters

- `--limit`: Repos to fetch per language per query (default: 10)
- `--pages`: Number of pages to fetch per query (default: 2)
- `--clear`: Clear database before crawling
- `--token`: GitHub API token

## Search Queries

The crawler searches for these topics across all supported languages:

1. **web framework** - Express, Django, Flask, Gin, etc.
2. **api client** - REST clients, SDKs
3. **database** - Database libraries and tools
4. **machine learning** - ML frameworks
5. **cli** - Command-line tools
6. **testing** - Testing frameworks

Each query is searched across 6 languages:
- Python
- JavaScript  
- Go
- Rust
- Java
- C++

## Database Operations

### Check Database Status

```bash
python -c "
from app import create_app
from app.models import Repo
from sqlalchemy import func

app = create_app()
with app.app_context():
    total = Repo.query.count()
    langs = Repo.query.with_entities(Repo.language, func.count(Repo.id)).group_by(Repo.language).all()
    print(f'Total repos: {total}')
    for lang, count in langs:
        print(f'  {lang}: {count}')
"
```

### Search Database

```bash
python -c "
from app import create_app
from app.database import search_repos

app = create_app()
with app.app_context():
    # Search for web frameworks in Python
    results = search_repos('framework', language='Python', limit=10)
    for r in results:
        print(f'{r[\"name\"]}: {r[\"stars\"]} stars')
"
```

### Export Data

```bash
python -c "
from app import create_app
from app.models import Repo
import json

app = create_app()
with app.app_context():
    repos = Repo.query.all()
    data = [r.to_dict() for r in repos]
    with open('repos_export.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f'Exported {len(data)} repos')
"
```

## API Testing

Once Flask server is running:

```bash
# Search
curl "http://localhost:5000/api/search?query=framework"
curl "http://localhost:5000/api/search?query=api&language=Python"

# Get metadata
curl "http://localhost:5000/api/languages"
curl "http://localhost:5000/api/topics"

# Configuration
curl "http://localhost:5000/api/config"
```

## Rate Limiting

**Without GitHub Token:**
- 60 requests/hour
- ~5-10 queries possible before hitting limit

**With GitHub Token:**
- 5,000 requests/hour
- Fetch much more data

**Solutions:**
1. Get a GitHub token: https://github.com/settings/tokens (create personal access token)
2. Set environment variable: `export GITHUB_TOKEN=ghp_...`
3. Run crawler with token: `python crawler.py --token $GITHUB_TOKEN`

## Troubleshooting

### "Rate limit exceeded"
- You're using unauthenticated API (60 req/hour)
- Get a GitHub token and retry

### No results found in search
1. Verify database has data:
   ```bash
   python -c "from app import create_app; from app.models import Repo; \
       app = create_app(); print(Repo.query.count())"
   ```

2. Reseed if empty:
   ```bash
   python crawler.py --clear --limit 5 --pages 1
   ```

### Flask server won't start
- Check port 5000 is available
- Check database file exists: `ls github_discovery.db`
- Try: `python run.py`

### Topics/Languages not showing
- Run crawler: `python crawler.py`
- Wait for it to complete
- Restart Flask server

## Next Steps

### Automated Crawling

Schedule the crawler to run periodically:

```bash
# Daily at 2 AM
0 2 * * * cd /path/to/backend && python crawler.py --token $GITHUB_TOKEN
```

### Selective Updates

Update only specific categories:

```bash
# Create a custom crawler for specific queries
python -c "
from crawler import GitHubCrawler
from app import create_app

app = create_app()
with app.app_context():
    crawler = GitHubCrawler(github_token='...')
    repos = crawler.search_repositories('machine learning', limit=50, max_pages=2)
    for repo in repos:
        crawler.add_repository(crawler.parse_repository(repo))
"
```

### Incremental Crawling

The crawler updates existing repos with new stars/forks data:

```bash
# Updates stars, forks, and metadata for all existing repos
python crawler.py --limit 5 --pages 1
```

## Performance Tips

1. **Use GitHub Token** - Dramatically increases rate limit
2. **Batch Searches** - Combine with cron jobs
3. **Selective Queries** - Focus on categories you care about
4. **Database Indexing** - For PostgreSQL, add indexes for production

## Future Improvements

1. **Incremental Updates** - Only fetch changed repos
2. **Topic Auto-Detection** - Better categorization
3. **Trending Repos** - Track new/growing projects
4. **Repository Metadata** - Fetch more details (contributors, license, etc.)
5. **Semantic Search** - Enable with embeddings

## Example Scenarios

### Scenario 1: Fresh Start
```bash
# Get 80 Python/JS/Go web frameworks
python crawler.py --clear --limit 15 --pages 1
```

### Scenario 2: Deep Dive
```bash
# Get 200 repos across all languages and topics
export GITHUB_TOKEN=ghp_...
python crawler.py --clear --limit 30 --pages 2 --token $GITHUB_TOKEN
```

### Scenario 3: Nightly Update
```bash
# Keep data fresh without clearing
export GITHUB_TOKEN=ghp_...
python crawler.py --limit 5 --pages 1 --token $GITHUB_TOKEN
```

## Resources

- GitHub API Docs: https://docs.github.com/en/rest
- Search Syntax: https://docs.github.com/en/search-github/searching-on-github/searching-for-repositories
- Create GitHub Token: https://github.com/settings/tokens

## Success Indicators

✅ You're set up correctly if:
- `python crawler.py` completes without errors
- Database has 80+ repositories
- Searching returns results from different languages
- Topics/languages endpoints show 30+ topics and 6 languages
