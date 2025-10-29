# Quick Start Guide - RA Longevity API

Get the RA Longevity MLOps API running in 5 minutes!

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Clone and Navigate
```bash
git clone https://github.com/Joedaddy66/nt-rule-index.git
cd nt-rule-index
```

### 2. Install Dependencies
```bash
pip install -r requirements-api.txt
```

### 3. Set Your API Token
```bash
# Generate a secure token
export API_BEARER_TOKEN=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')

# Or set a custom token
export API_BEARER_TOKEN="your-secure-token-here"
```

### 4. Start the Server
```bash
python api_server.py
```

The server will start on `http://localhost:8080`

## Quick Test

Open a new terminal and run:

```bash
# Set the same token
export API_BEARER_TOKEN="your-secure-token-here"

# Run tests
python test_api.py
```

You should see: `ALL TESTS PASSED ✓`

## First API Call

### Analyze Some Data

```bash
curl -X POST "http://localhost:8080/api/longevity/analyze" \
  -H "Authorization: Bearer ${API_BEARER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"feature1": 1.0, "feature2": 2.0},
      {"feature1": 1.5, "feature2": 2.5},
      {"feature1": 2.0, "feature2": 3.0}
    ],
    "mode": "tabular",
    "threshold": 0.1
  }'
```

### Get Your Results

The analyze endpoint returns a `run_id`. Use it to get your report:

```bash
# Replace RUN_ID with the actual run_id from above
curl -X GET "http://localhost:8080/api/longevity/report/RUN_ID" \
  -H "Authorization: Bearer ${API_BEARER_TOKEN}"
```

### Browse Your Artifacts

Open your browser and go to:
```
http://localhost:8080/artifacts/
```

(Note: This requires authentication in production. For local dev, you can access artifacts directly in the `artifacts/` folder)

## Using Docker (Alternative)

### Build and Run
```bash
docker-compose up -d
```

### Set Token in docker-compose.yml
Edit `docker-compose.yml` and update:
```yaml
environment:
  - API_BEARER_TOKEN=your-secure-token-here
```

## Interactive Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## Common Issues

### "API_BEARER_TOKEN environment variable must be set"
**Solution**: Set the token before starting:
```bash
export API_BEARER_TOKEN="your-token-here"
python api_server.py
```

### "Port 8080 already in use"
**Solution**: Kill the process or use a different port:
```bash
# Kill existing process
lsof -ti:8080 | xargs kill -9

# Or use different port
export PORT=8081
python api_server.py
```

### "Module not found"
**Solution**: Install dependencies:
```bash
pip install -r requirements-api.txt
```

## Next Steps

1. Read the full [API_README.md](API_README.md) for detailed documentation
2. Check [SECURITY.md](SECURITY.md) for security best practices
3. Review example use cases in the test script: [test_api.py](test_api.py)
4. Deploy to production (see API_README.md for Cloud Run/Firebase instructions)

## Support

- Report issues: https://github.com/Joedaddy66/nt-rule-index/issues
- Read docs: See API_README.md

---

**Ready to analyze some data!** 🚀
