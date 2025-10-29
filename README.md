# NT Rule Index
Local-first repository linking Drive artifacts to **Number-Theory Rule Packs** and publishing a MkDocs site.

## Quick start

### Documentation Site
- Build index: `python scripts/build_index.py`
- Install docs deps: `pip install -r requirements.txt`
- Serve locally: `mkdocs serve` → http://127.0.0.1:8000

### RA Longevity MLOps API
Fast, secure microservice for RA Longevity analysis and deployment.

- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
- **Full Docs**: See [API_README.md](API_README.md)
- **Security**: See [SECURITY.md](SECURITY.md)

```bash
# Install API dependencies
pip install -r requirements-api.txt

# Set authentication token
export API_BEARER_TOKEN=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# Start the API server
python api_server.py
```

Server runs on http://localhost:8080 with interactive docs at /docs

**Features:**
- POST /api/longevity/analyze - Analyze CSV/JSON data
- GET /api/longevity/report/:run_id - Get analysis reports
- POST /api/longevity/deploy - Deploy models with validation
- Bearer token authentication
- Automatic bundle.zip generation
- DKIL threshold validation
