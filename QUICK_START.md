# Quick Start Guide

## 1. Terminal 1 - Start the Flask Backend

```bash
cd F:/AIApps/AISoftware/github-discovery-tool/backend

# Activate virtual environment
source venv/Scripts/activate

# Start Flask server
python run.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

## 2. Terminal 2 - Start the React Frontend

```bash
cd F:/AIApps/AISoftware/github-discovery-tool/frontend

# Start development server
npm run dev
```

You should see:
```
  Local:        http://127.0.0.1:5173
```

## 3. Open Your Browser

Go to: **http://localhost:5173**

## Testing the Application

### Search for Projects
1. Type a keyword like "react", "api", "authentication" in the search box
2. Select a programming language from the dropdown (optional)
3. Select a category/topic from the dropdown (optional)
4. Results appear below sorted by star count

### Download a Repository
Click the "Download as ZIP" button on any result to download the repository.

### Available Test Data

The database includes these popular projects:
- Express.js (JavaScript, web-framework)
- Django (Python, web-framework)
- React (JavaScript, ui-library)
- FastAPI (Python, api-framework)
- Vue.js (JavaScript, frontend-framework)
- TensorFlow (Python, machine-learning)
- Go (Go, programming-language)
- Docker (Go, containers, devops)
- Kubernetes (Go, orchestration)
- Next.js (JavaScript, react-framework)
- MongoDB (NoSQL database)
- PostgreSQL (SQL database)
- Flask (Python, web-framework)
- Rust (Rust, programming-language)
- SQLAlchemy (Python, orm)

### Try These Searches

- "web" → web frameworks
- "api" → API-related projects  
- "database" → database projects
- "machine" → ML/AI projects
- "javascript" with JavaScript language filter → JS projects only

## Troubleshooting

### Flask server won't start
- Check Python is installed: `python --version`
- Verify virtual environment is activated
- Make sure port 5000 is not in use

### React dev server won't start
- Check Node.js is installed: `node --version`
- Run `npm install` in frontend directory
- Make sure port 5173 is not in use

### API requests failing
- Ensure Flask server is running on port 5000
- Check browser console for errors (F12)
- Verify CORS is enabled in Flask (`flask-cors` installed)

### Database empty
- Run `python seed_data.py` in backend directory to populate test data
- Check file `github_discovery.db` exists in backend folder

## Next Steps

After testing Phase 1:

1. **Implement Semantic Search** (Phase 2)
   - Replace keyword matching with Claude API embeddings
   - More intelligent project matching

2. **Build GitHub Crawler**
   - Automated indexing of popular repos
   - Periodic updates from GitHub API
   - Auto-categorization by topics

3. **Add More Features**
   - User authentication
   - Save favorite repositories
   - Custom categories
   - Search history
