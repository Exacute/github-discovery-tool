# START HERE - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Start the Backend (Terminal 1)

```bash
cd F:/AIApps/AISoftware/github-discovery-tool/backend
source venv/Scripts/activate
python run.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 2: Start the Frontend (Terminal 2)

```bash
cd F:/AIApps/AISoftware/github-discovery-tool/frontend
npm run dev
```

You should see:
```
Local:        http://127.0.0.1:5173
```

### Step 3: Open in Browser

Go to: **http://localhost:5173**

---

## 🔍 Try These Searches

1. **"framework"** - Web frameworks (FastAPI, Django, Express, Gin, etc.)
2. **"api"** - API clients and libraries  
3. **"database"** - Database tools and libraries
4. **"web"** - Web-related projects

### Filter by Language
- Select "Python" from language dropdown
- Select "Go" from language dropdown
- Add topic filters for more specific results

### Download a Repository
Click **"Download as ZIP"** on any repository to get the code locally

---

## 📊 What's in the Database?

✅ **80 Real GitHub Repositories**
- FastAPI (97K stars)
- Gin (88K stars)
- Django (87K stars)
- Flask (71K stars)
- Express (69K stars)
- And 75 more...

✅ **6 Programming Languages**
- Python (16 repos)
- JavaScript (16 repos)
- Go (16 repos)
- Rust (16 repos)
- Java (8 repos)
- C++ (8 repos)

✅ **370 Topics/Categories**
- web-framework
- api
- database
- machine-learning
- cli
- testing
- And 365 more...

---

## 🛠️ If You Get "Failed to Search Repositories"

1. **Check Flask is running:**
   ```bash
   # In Terminal 1, you should see:
   # * Running on http://127.0.0.1:5000
   ```

2. **Check React is running:**
   ```bash
   # In Terminal 2, you should see:
   # Local:        http://127.0.0.1:5173
   ```

3. **Database is populated:**
   ```bash
   # Terminal - check database has data
   cd backend && source venv/Scripts/activate && python crawler.py --limit 5 --pages 1
   ```

---

## 🎯 Common Tasks

### Search for Python Web Frameworks
1. Type "framework" in search box
2. Select "Python" from Language dropdown
3. View results sorted by popularity

### Find Go API Libraries
1. Type "api" in search box
2. Select "Go" from Language dropdown
3. Download any repository as ZIP

### Get Recent JavaScript Projects
1. Type "javascript" in search box
2. Click Search
3. Results show most popular JS projects

---

## 📚 Learn More

- **How to use the crawler:** [GITHUB_CRAWLER_GUIDE.md](GITHUB_CRAWLER_GUIDE.md)
- **Database operations:** [DATABASE_SETUP.md](DATABASE_SETUP.md)
- **Semantic search setup:** [EMBEDDINGS_SETUP.md](EMBEDDINGS_SETUP.md)
- **Full documentation:** [README.md](README.md)
- **Setup complete checklist:** [SETUP_COMPLETE.md](SETUP_COMPLETE.md)

---

## 🔧 Add More Repositories

Want more projects in the database? Run the crawler:

```bash
cd backend
source venv/Scripts/activate

# Fetch more repositories from GitHub
python crawler.py --limit 15 --pages 2
```

For even more repositories (requires GitHub token):

```bash
export GITHUB_TOKEN=ghp_your_token_here
python crawler.py --token $GITHUB_TOKEN --limit 30 --pages 3
```

Get a GitHub token: https://github.com/settings/tokens

---

## ⚡ Next Steps

1. **Use it now** - Search and download projects
2. **Enable semantic search** - Set up embeddings for smarter matching
3. **Fetch more data** - Use the crawler to get more repositories
4. **Deploy** - Move to production with PostgreSQL

---

## 🆘 Stuck?

| Problem | Solution |
|---------|----------|
| "Connection refused" | Make sure both servers are running (Flask + React) |
| "No results found" | Database might be empty, run `python crawler.py` |
| Port 5000 in use | Another app is using Flask port, kill it or restart |
| Port 5173 in use | Another app is using React port, or restart terminal |

---

## 💡 Example Workflow

1. **Search for "React UI components"**
   - Results: React, Vue.js, Yew, etc.
   
2. **Filter by "JavaScript"**
   - Results: React, Vue.js, Phaser, etc.
   
3. **Click most popular**
   - Reads: "Fast, unopinionated, minimalist web framework"
   
4. **Download as ZIP**
   - Gets React source code locally
   
5. **Use as AI coding base**
   - Feed to Claude with AI prompt:
   - "Build a React component library using this structure"

---

## That's It! 🎉

You're ready to discover and download GitHub projects.

**Open http://localhost:5173 in your browser and start searching!**
