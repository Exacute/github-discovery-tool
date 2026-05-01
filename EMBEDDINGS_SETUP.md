# Semantic Search & Embeddings Setup Guide

This guide explains how to set up semantic search with your preferred LLM provider.

## Overview

The application supports **3 embedding providers**:
1. **OpenAI** - Cloud-based, high quality (requires API key)
2. **Ollama** - Local, free, runs on your machine
3. **Local (sentence-transformers)** - Local, free, built-in Python library

## Configuration

Set the `EMBEDDINGS_PROVIDER` environment variable to choose which provider to use:

```bash
# In .env file
EMBEDDINGS_PROVIDER=openai    # or: ollama, local
```

Or set via command line:

```bash
export EMBEDDINGS_PROVIDER=openai
python run.py
```

---

## Option 1: OpenAI (Recommended for Production)

### Pros
- ✅ Highest quality embeddings
- ✅ Commercial API with SLA
- ✅ Best semantic search results

### Cons
- ❌ Requires API key
- ❌ Per-request cost (~$0.02 per 1M tokens)
- ❌ Requires internet connection

### Setup

1. **Get an OpenAI API Key**
   - Go to: https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key

2. **Set Environment Variable**
   ```bash
   # In backend/.env
   EMBEDDINGS_PROVIDER=openai
   OPENAI_API_KEY=sk-...your-key-here...
   ```

3. **Install Dependencies** (already included)
   ```bash
   pip install openai
   ```

4. **Test**
   ```bash
   curl "http://localhost:5000/api/search?query=web&semantic=true"
   ```

### Cost Estimation
- Embedding 100 repos: ~$0.001
- 1000 semantic searches/month: ~$0.02

---

## Option 2: Ollama (Best for Development)

### Pros
- ✅ Completely free
- ✅ Runs locally (no internet needed)
- ✅ Good embedding quality
- ✅ Privacy-friendly

### Cons
- ❌ Requires ~2GB RAM
- ❌ Slower than cloud APIs (~1-2 sec per search)
- ❌ Need to run separate Ollama service

### Setup

1. **Download & Install Ollama**
   - Visit: https://ollama.ai
   - Download for your OS (Windows, Mac, Linux)
   - Run the installer

2. **Pull Embedding Model**
   ```bash
   # In a terminal
   ollama pull nomic-embed-text
   ```
   
   Alternative models:
   ```bash
   ollama pull mxbai-embed-large  # Better quality, slower
   ollama pull all-minilm         # Faster, smaller
   ```

3. **Verify Ollama is Running**
   ```bash
   # Should return status
   curl http://localhost:11434/api/tags
   ```

4. **Configure in Flask**
   ```bash
   # In backend/.env
   EMBEDDINGS_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=nomic-embed-text
   ```

5. **Start Flask**
   ```bash
   source venv/Scripts/activate
   python run.py
   ```

6. **Test**
   ```bash
   curl "http://localhost:5000/api/search?query=web&semantic=true"
   ```

### Troubleshooting

**"Cannot connect to Ollama"**
- Make sure Ollama is running: `ollama serve` (if not auto-running)
- Check URL is correct: `http://localhost:11434`

**"Model not found"**
- Pull the model: `ollama pull nomic-embed-text`

**Slow responses**
- Normal (1-2 seconds per search)
- Use a faster model: `ollama pull all-minilm`

---

## Option 3: Local Embeddings (Easiest Setup)

### Pros
- ✅ Pure Python, no external services
- ✅ Free and open source
- ✅ Works offline
- ✅ Automatic model download

### Cons
- ❌ Moderate quality (good enough for most use cases)
- ❌ Slower than Ollama on first run (~5-10 sec to download & load model)
- ❌ Uses ~400MB RAM and disk space

### Setup

1. **Install sentence-transformers**
   ```bash
   source venv/Scripts/activate
   pip install sentence-transformers
   ```

2. **Configure**
   ```bash
   # In backend/.env
   EMBEDDINGS_PROVIDER=local
   LOCAL_EMBEDDINGS_MODEL=all-MiniLM-L6-v2
   ```

3. **Available Models**
   ```
   all-MiniLM-L6-v2           # Fast, small (default)
   all-mpnet-base-v2          # Better quality, slower
   paraphrase-MiniLM-L6-v2    # For semantic similarity
   ```
   
   Full list: https://www.sbert.net/docs/pretrained_models.html

4. **Start Flask**
   ```bash
   python run.py
   ```
   
   First request will download the model (~100MB).

5. **Test**
   ```bash
   curl "http://localhost:5000/api/search?query=web&semantic=true"
   ```

---

## Comparison Table

| Feature | OpenAI | Ollama | Local |
|---------|--------|--------|-------|
| **Cost** | $ | Free | Free |
| **Speed** | Fast | Moderate | Slow first run |
| **Quality** | Best | Good | Good |
| **Setup** | Easy | Medium | Very Easy |
| **Internet** | Required | No | No |
| **Privacy** | Cloud | Local | Local |
| **Best for** | Production | Development | Learning |

---

## Using Semantic Search in API

### Query with Semantic Search
```bash
curl "http://localhost:5000/api/search?query=authentication&semantic=true"
```

### Fallback to Keyword if Semantic Fails
```bash
curl "http://localhost:5000/api/search?query=authentication"
```

### Check Configuration
```bash
curl "http://localhost:5000/api/config" | jq
```

---

## Frontend Integration

The React frontend can enable semantic search by adding `&semantic=true` to API calls:

```typescript
// In frontend/src/api/client.ts
async search(query: string, language?: string, topic?: string, semantic: boolean = false) {
    const params = new URLSearchParams({ query, semantic: semantic ? 'true' : 'false' })
    // ... rest of implementation
}
```

Add a UI toggle:
```tsx
// In SearchBar or FilterPanel
<label>
    <input type="checkbox" onChange={(e) => setSemantic(e.target.checked)} />
    Use Semantic Search
</label>
```

---

## Performance Tips

### OpenAI
- Batch requests to save costs
- Cache embeddings for popular searches
- Consider gpt-3.5-turbo-embed (lower cost)

### Ollama
- Use `all-minilm` model for faster responses
- Add more RAM if available
- Run on GPU if possible

### Local
- Use `all-MiniLM-L6-v2` for faster inference
- First load might be slow, subsequent requests are fast
- Increase batch size for multiple searches

---

## Migration Between Providers

You can change providers anytime:

```bash
# Was using OpenAI, switch to Ollama
EMBEDDINGS_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=nomic-embed-text
```

No database migration needed! Embeddings are computed on-the-fly.

---

## Troubleshooting

### "Embeddings provider not configured"
- Check `EMBEDDINGS_PROVIDER` is set in `.env`
- Make sure required dependencies are installed:
  - OpenAI: `pip install openai`
  - Ollama: Just need service running
  - Local: `pip install sentence-transformers`

### Semantic search returns no results
- Verify provider is working: check `/api/config` endpoint
- Make sure database has repositories
- Try with fewer filters (language/topic)

### Slow embeddings
- OpenAI: Normal, cloud API calls take time
- Ollama: Expected (1-2 sec), use faster model
- Local: First run downloads model, subsequent runs are fast

---

## Recommendation

| Situation | Provider |
|-----------|----------|
| Learning & testing | **Local** |
| Development locally | **Ollama** |
| Production deployment | **OpenAI** |
| Privacy-critical | **Ollama** or **Local** |
| Best quality | **OpenAI** |
