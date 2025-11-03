# RA Longevity MLOps Microservice API

FastAPI microservice for serving RA Longevity analysis artifacts with secure endpoints.

## Features

- **POST /api/longevity/analyze** - Analyze CSV/JSON data with RA feature encoder
- **GET /api/longevity/report/:run_id** - Retrieve JSON + HTML reports
- **POST /api/longevity/deploy** - Deploy models to registry with DKIL validation
- Bearer token authentication
- Automatic bundle.zip creation
- Static artifact serving at `/artifacts`

## Installation

### Option 1: Using pip

```bash
pip install -r requirements-api.txt
```

### Option 2: Using a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-api.txt
```

## Configuration

Set environment variables:

```bash
export API_BEARER_TOKEN="your-secure-token-here"
export PORT=8080  # Optional, defaults to 8080
```

## Running the Server

### Development mode

```bash
python api_server.py
```

Or using uvicorn directly:

```bash
uvicorn api_server:app --reload --host 0.0.0.0 --port 8080
```

### Production mode

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8080 --workers 4
```

## API Endpoints

### 1. POST /api/longevity/analyze

Analyze tabular or time-series data with RA feature encoder.

**Request Headers:**
```
Authorization: Bearer <your-token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "data": [
    {"feature1": 1.0, "feature2": 2.0},
    {"feature1": 1.5, "feature2": 2.5}
  ],
  "mode": "tabular",
  "threshold": 0.1
}
```

**Response:**
```json
{
  "run_id": "uuid-here",
  "predictions": [0.85, 0.86],
  "ldrop_metrics": {
    "mean_ldrop": 0.12,
    "max_ldrop": 0.25,
    "min_ldrop": 0.05,
    "std_ldrop": 0.08
  },
  "ra_score_deltas": [0.02, 0.025],
  "timestamp": "2025-10-29T07:19:15.484Z",
  "dkil_locked": false
}
```

### 2. POST /api/longevity/analyze/upload

Alternative endpoint for CSV file upload.

**Request:**
```bash
curl -X POST "http://localhost:8080/api/longevity/analyze/upload" \
  -H "Authorization: Bearer your-token" \
  -F "file=@data.csv" \
  -F "mode=tabular" \
  -F "threshold=0.1"
```

### 3. GET /api/longevity/report/:run_id

Retrieve analysis report (JSON + HTML) for a specific run.

**Request:**
```bash
curl -X GET "http://localhost:8080/api/longevity/report/{run_id}" \
  -H "Authorization: Bearer your-token"
```

**Response:**
```json
{
  "run_id": "uuid-here",
  "json_report": {...},
  "html_report": "<html>...</html>",
  "dkil_locked": false
}
```

### 4. GET /api/longevity/report/:run_id/download

Download the complete bundle.zip for a run.

**Request:**
```bash
curl -X GET "http://localhost:8080/api/longevity/report/{run_id}/download" \
  -H "Authorization: Bearer your-token" \
  -o bundle.zip
```

### 5. POST /api/longevity/deploy

Deploy model to registry with DKIL validation.

**Request:**
```json
{
  "run_id": "uuid-here",
  "human_key": "human-approval-key-12345",
  "logic_key": "logic-validation-key-67890",
  "dkil_validation": true
}
```

**Response:**
```json
{
  "status": "success",
  "model_registry_url": "https://model-registry.example.com/models/ra-longevity/uuid-here",
  "message": "Model uuid-here successfully deployed to registry"
}
```

### 6. GET /artifacts

Static file serving for artifacts directory. Browse or download files directly:

```
http://localhost:8080/artifacts/report_uuid.json
http://localhost:8080/artifacts/report_uuid.html
http://localhost:8080/artifacts/bundle_uuid.zip
http://localhost:8080/artifacts/dkil.lock
```

## Security

- All endpoints (except root `/`) require bearer token authentication
- Set `API_BEARER_TOKEN` environment variable to configure the token
- For production, use a strong, randomly generated token
- Consider using Firebase Auth or OAuth2 for enhanced security

## Deployment

### Google Cloud Run

```bash
# Build Docker image
docker build -t gcr.io/YOUR_PROJECT/ra-longevity-api .

# Push to GCR
docker push gcr.io/YOUR_PROJECT/ra-longevity-api

# Deploy
gcloud run deploy ra-longevity-api \
  --image gcr.io/YOUR_PROJECT/ra-longevity-api \
  --platform managed \
  --region us-central1 \
  --set-env-vars API_BEARER_TOKEN=your-secure-token
```

### Firebase / App Engine

Create `app.yaml`:
```yaml
runtime: python312
entrypoint: uvicorn api_server:app --host 0.0.0.0 --port $PORT

env_variables:
  API_BEARER_TOKEN: "your-secure-token"
```

Deploy:
```bash
gcloud app deploy
```

## Directory Structure

```
.
├── api_server.py           # Main FastAPI application
├── requirements-api.txt    # API dependencies
├── artifacts/             # Generated artifacts (auto-created)
│   ├── report_*.json      # JSON reports
│   ├── report_*.html      # HTML reports
│   ├── bundle_*.zip       # Bundled artifacts
│   ├── dkil.lock          # DKIL lock file
│   └── deployment_*.json  # Deployment records
├── README.md              # Main project README
└── API_README.md          # This file
```

## Testing

### Using curl

```bash
# Set token
export TOKEN="your-secure-token"

# Analyze data
curl -X POST "http://localhost:8080/api/longevity/analyze" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{"x": 1}, {"x": 2}],
    "mode": "tabular"
  }'

# Get report
curl -X GET "http://localhost:8080/api/longevity/report/{run_id}" \
  -H "Authorization: Bearer $TOKEN"

# Deploy model
curl -X POST "http://localhost:8080/api/longevity/deploy" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "run_id": "{run_id}",
    "human_key": "human-key-12345678",
    "logic_key": "logic-key-87654321"
  }'
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:8080"
TOKEN = "your-secure-token"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Analyze
response = requests.post(
    f"{BASE_URL}/api/longevity/analyze",
    headers=headers,
    json={
        "data": [{"x": 1}, {"x": 2}],
        "mode": "tabular"
    }
)
result = response.json()
run_id = result["run_id"]

# Get report
report = requests.get(
    f"{BASE_URL}/api/longevity/report/{run_id}",
    headers=headers
).json()

print(report)
```

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## Troubleshooting

### Port already in use

```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Or use a different port
export PORT=8081
python api_server.py
```

### Authentication errors

Ensure the `Authorization` header is properly set:
```
Authorization: Bearer your-token-here
```

### Missing artifacts

The `artifacts/` directory is automatically created on startup. Ensure the application has write permissions.

## License

See LICENSE file in the repository root.
