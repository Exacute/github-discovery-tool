# GitHub Project Discovery Tool

A website that helps users discover and reuse existing GitHub projects as starting points for their applications, reducing wasteful AI-generated code.

## Project Structure

```
github-discovery-tool/
├── frontend/          # React TypeScript frontend (Vite)
├── backend/           # Flask Python backend with SQLAlchemy ORM
├── docker-compose.yml # PostgreSQL setup (for production)
└── README.md
```

## Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: Python Flask + SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production)
- **Search**: Keyword matching with filters for language and GitHub topics

## Features

✅ **Keyword Search** - Fast search by name and description  
✅ **Semantic Search** - Smart matching using any LLM (OpenAI, Ollama, or local)  
✅ **Filter by Language** - Filter repositories by programming language  
✅ **Filter by Topics** - Filter by GitHub topics/categories  
✅ **Sort by Stars** - Results ranked by popularity  
✅ **Download as ZIP** - Download repositories for offline use  
✅ **Multi-LLM Support** - Choose your preferred LLM provider  
✅ **Responsive Design** - Works on desktop and mobile  

## Two Search Modes

### 1. Keyword Search (Default)
Fast, no setup required. Matches keywords in repo names and descriptions.

```bash
curl "http://localhost:5000/api/search?query=web"
```

### 2. Semantic Search (Optional)
Intelligent matching using embeddings. Requires configuring an LLM provider:
- **OpenAI** (Cloud, $) - Best quality
- **Ollama** (Local, Free) - Good for development
- **Local** (Python, Free) - Easiest setup

```bash
curl "http://localhost:5000/api/search?query=web&semantic=true"
```

See [EMBEDDINGS_SETUP.md](EMBEDDINGS_SETUP.md) for detailed configuration.

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Git
- (Optional) OpenAI API key, Ollama, or sentence-transformers

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database with test data (optional - database auto-initializes)
python seed_data.py

# Start Flask server
python run.py
```

Flask server will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Vite dev server will run on `http://localhost:5173`

## API Endpoints

### Search Repositories
```
GET /api/search?query=string&language=string&topic=string&limit=5
```
Returns top 5 repositories sorted by stars.

**Query Parameters:**
- `query` (required): Keyword search term
- `language` (optional): Filter by programming language
- `topic` (optional): Filter by GitHub topic/category
- `limit` (optional, default: 5): Number of results

**Response:**
```json
{
  "repos": [
    {
      "id": 1,
      "repo_id": 12345,
      "name": "Express.js",
      "url": "https://github.com/expressjs/express",
      "description": "...",
      "language": "JavaScript",
      "topics": ["web-framework", "nodejs"],
      "stars": 64000,
      "forks": 15000
    }
  ]
}
```

### Get Available Languages
```
GET /api/languages
```

**Response:**
```json
{
  "languages": ["JavaScript", "Python", "Go", "Java", ...]
}
```

### Get Available Topics
```
GET /api/topics
```

**Response:**
```json
{
  "topics": ["web-framework", "api", "database", ...]
}
```

### Download Repository
```
POST /api/repos/:repo_id/download
```

Downloads a repository as a ZIP file.

## Database Schema

### Repos Table (SQLite/PostgreSQL)
```sql
repos:
  - id (Integer, Primary Key)
  - repo_id (BigInteger, Unique) - GitHub repo ID
  - name (String)
  - url (String)
  - description (Text)
  - language (String) - Primary programming language
  - topics (JSON/Array) - GitHub topic tags
  - stars (Integer) - GitHub star count
  - forks (Integer) - GitHub fork count
  - last_updated (DateTime)
  - indexed_at (DateTime) - When repo was indexed
```

## Development Workflow

1. **Backend Development**
   - Edit Flask routes in `backend/app/routes.py`
   - Modify database queries in `backend/app/database.py`
   - Update models in `backend/app/models.py`

2. **Frontend Development**
   - React components in `frontend/src/components/`
   - API client in `frontend/src/api/client.ts`
   - Styling with CSS files in each component directory

3. **Database**
   - Automatic schema creation on app startup
   - Seed test data: `python backend/seed_data.py`

## Configuration

**Backend (.env)**
```
DATABASE_URL=sqlite:///github_discovery.db
FLASK_ENV=development
FLASK_PORT=5000
```

Change `DATABASE_URL` to use PostgreSQL:
```
DATABASE_URL=postgresql://user:password@localhost:5432/github_discovery
```

## Phase 2: GitHub Crawler

Coming soon - automated crawler to:
- Fetch repositories from GitHub API
- Index by language and topics
- Categorize and deduplicate
- Update periodically

## Project Goals

- **Phase 1** (Current): Search interface + keyword matching
  - ✅ React frontend with search UI
  - ✅ Flask backend with search API
  - ✅ SQLite database with test data
  - ✅ Language and topic filtering
  - ✅ ZIP download functionality

- **Phase 2**: GitHub crawler
  - Automated repo indexing
  - Semantic search with embeddings
  - Periodic updates from GitHub

- **Phase 3**: Enhanced features
  - Semantic search using LLM embeddings
  - Machine learning for better categorization
  - User preferences and saved searches

## Environment Variables

- `DATABASE_URL`: Database connection string (default: `sqlite:///github_discovery.db`)
- `FLASK_ENV`: Set to `development` or `production` (default: `development`)
- `FLASK_PORT`: Flask server port (default: `5000`)

## Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`

**Backend:**
Use a production WSGI server:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

For PostgreSQL production setup, use Docker Compose:
```bash
docker-compose up -d
```

## Notes

- Development uses SQLite for simplicity
- Production should use PostgreSQL
- CORS is enabled for frontend-backend communication on port 5000
- Tests can be added to `backend/tests/` and `frontend/src/__tests__/`

## Future Enhancements

1. Implement semantic search using Claude API embeddings
2. Build GitHub crawler for auto-indexing
3. Add user authentication and saved searches
4. Analytics dashboard for search trends
5. Integration with AI code generation tools
