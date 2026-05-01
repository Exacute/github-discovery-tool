# Database Setup & Management

## Database Overview

The application uses SQLite for development and PostgreSQL for production. The database automatically creates tables on first run.

## Database Schema

### Repos Table

```
repos:
  - id (INTEGER, Primary Key) - Auto-increment ID
  - repo_id (BIGINT, Unique) - GitHub repository ID
  - name (VARCHAR) - Repository name
  - url (VARCHAR) - GitHub URL
  - description (TEXT) - Repository description
  - language (VARCHAR) - Primary programming language
  - topics (JSON/ARRAY) - GitHub topics/categories
  - stars (INTEGER) - GitHub star count
  - forks (INTEGER) - GitHub fork count
  - last_updated (DATETIME) - Last sync time
  - indexed_at (DATETIME) - When repo was indexed
```

## Current Data

Database includes 15 popular repositories:

| Repository | Language | Topics | Stars |
|------------|----------|--------|-------|
| Express.js | JavaScript | web-framework, nodejs | 64K |
| Django | Python | web-framework, orm | 78K |
| React | JavaScript | ui-library, frontend | 218K |
| FastAPI | Python | api-framework, async | 75K |
| Vue.js | JavaScript | frontend-framework | 208K |
| TensorFlow | Python | machine-learning, ai | 185K |
| Go | Go | programming-language | 121K |
| Docker | Go | containers, devops | 68K |
| SQLAlchemy | Python | orm, database | 9K |
| Kubernetes | Go | orchestration | 110K |
| Next.js | JavaScript | react-framework | 126K |
| MongoDB | C++ | nosql, database | 26K |
| PostgreSQL | C | sql, database | 14K |
| Flask | Python | web-framework | 68K |
| Rust | Rust | programming-language | 98K |

## Seeding Data

### Reset Database

Clear all data and start fresh:

```bash
cd backend
source venv/Scripts/activate
rm github_discovery.db
python seed_data.py
```

### Manual Database Operations

```python
from app import create_app, db
from app.models import Repo

app = create_app()
with app.app_context():
    # Add a repository
    repo = Repo(
        repo_id=123456789,
        name="My Awesome Repo",
        url="https://github.com/owner/repo",
        description="Amazing project",
        language="Python",
        topics=["ml", "python", "ai"],
        stars=1000,
        forks=100
    )
    db.session.add(repo)
    db.session.commit()
    
    # Query repositories
    repos = Repo.query.filter_by(language="Python").all()
    
    # Count
    total = Repo.query.count()
```

## Database Operations

### Check Database Status

```bash
cd backend
source venv/Scripts/activate
python -c "
from app import create_app
from app.models import Repo
from app.database import get_languages, get_topics

app = create_app()
with app.app_context():
    print(f'Total repos: {Repo.query.count()}')
    print(f'Languages: {get_languages()}')
    print(f'Topics: {get_topics()[:10]}')
"
```

### Export Data to JSON

```python
from app import create_app
from app.models import Repo
import json

app = create_app()
with app.app_context():
    repos = Repo.query.all()
    data = [repo.to_dict() for repo in repos]
    
    with open('repos_backup.json', 'w') as f:
        json.dump(data, f, indent=2)
```

### Import Data from JSON

```python
from app import create_app, db
from app.models import Repo
import json

app = create_app()
with app.app_context():
    with open('repos_backup.json', 'r') as f:
        data = json.load(f)
    
    for repo_data in data:
        repo = Repo(**repo_data)
        db.session.add(repo)
    
    db.session.commit()
```

## Production Database (PostgreSQL)

### Setup PostgreSQL with Docker

```bash
docker-compose up -d
```

Or install PostgreSQL locally and create database:

```sql
CREATE DATABASE github_discovery;
```

### Configure Connection

Update `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/github_discovery
```

### Migrate from SQLite to PostgreSQL

```bash
# Backup SQLite data
python -c "
from app import create_app
from app.models import Repo
import json

app = create_app()
with app.app_context():
    repos = Repo.query.all()
    data = [repo.to_dict() for repo in repos]
    with open('backup.json', 'w') as f:
        json.dump(data, f)
"

# Update DATABASE_URL in .env to PostgreSQL
# Update config.py to use new database
# Run migrations
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
"

# Restore data
python -c "
from app import create_app, db
from app.models import Repo
import json

app = create_app()
with app.app_context():
    with open('backup.json', 'r') as f:
        data = json.load(f)
    for repo_data in data:
        repo = Repo(**repo_data)
        db.session.add(repo)
    db.session.commit()
"
```

## Troubleshooting

### "No repositories found" on Search

1. Check database has data:
   ```bash
   python seed_data.py
   ```

2. Verify database file exists:
   ```bash
   ls -la backend/github_discovery.db
   ```

3. Check database connection:
   ```bash
   python -c "from app import create_app; app = create_app(); print('Database OK')"
   ```

### Database Locked

If you see "database is locked":
- Close all Python processes accessing the database
- On Windows: `taskkill /F /IM python.exe`
- Delete `.db-journal` files if they exist
- Restart Flask server

### Wrong Data Shows Up

Clear and reseed:
```bash
rm backend/github_discovery.db
python backend/seed_data.py
```

## Backup & Restore

### Backup to JSON

```bash
python -c "
from app import create_app
from app.models import Repo
import json
from datetime import datetime

app = create_app()
with app.app_context():
    repos = Repo.query.all()
    data = [repo.to_dict() for repo in repos]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'backup_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f'Backed up {len(data)} repos to {filename}')
"
```

### Restore from JSON

```bash
python -c "
from app import create_app, db
from app.models import Repo
import json

app = create_app()
with app.app_context():
    with open('backup_20260501_120000.json', 'r') as f:
        data = json.load(f)
    
    # Clear existing
    db.session.query(Repo).delete()
    
    # Add from backup
    for repo_data in data:
        repo = Repo(**repo_data)
        db.session.add(repo)
    
    db.session.commit()
    print(f'Restored {len(data)} repos')
"
```

## Next Steps

1. **Add GitHub Crawler** - Auto-index popular repos
2. **Add Vector Search** - Store embeddings in database
3. **Add Caching** - Cache popular searches
4. **Add Indexing** - Full-text search indexes for PostgreSQL
