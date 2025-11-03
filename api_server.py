#!/usr/bin/env python3
"""
RA Longevity MLOps Microservice API
Serves RA Longevity artifacts with secure endpoints.
"""

import os
import json
import zipfile
import uuid
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException, Security, UploadFile, File, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
import pandas as pd

# Configuration
ARTIFACTS_DIR = Path("artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)

# Security: Require API_BEARER_TOKEN to be set, no insecure default
BEARER_TOKEN = os.getenv("API_BEARER_TOKEN")
if not BEARER_TOKEN:
    raise ValueError(
        "API_BEARER_TOKEN environment variable must be set. "
        "Generate a secure random token: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
    )

# Initialize FastAPI
app = FastAPI(
    title="RA Longevity MLOps API",
    description="Microservice for RA Longevity analysis, reporting, and deployment",
    version="1.0.0"
)

# Security
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify bearer token authentication."""
    if credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials


def validate_run_id(run_id: str) -> str:
    """
    Validate and sanitize run_id to prevent path traversal attacks.
    Only allows UUID format (alphanumeric and hyphens).
    
    Security Note: This function acts as a sanitizer for CodeQL path-injection alerts.
    By validating that run_id matches strict UUID format (no slashes, dots, or special chars),
    we prevent directory traversal attacks like '../../../etc/passwd'.
    """
    # UUID format: 8-4-4-4-12 hexadecimal characters
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    if not uuid_pattern.match(run_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid run_id format. Must be a valid UUID."
        )
    
    return run_id


# Pydantic Models
class AnalyzeRequest(BaseModel):
    """Request model for longevity analysis."""
    data: List[Dict[str, Any]] = Field(..., description="Tabular data as list of dictionaries")
    mode: str = Field(default="tabular", description="Analysis mode: 'tabular' or 'time_series'")
    threshold: Optional[float] = Field(default=None, description="DKIL threshold if applicable")


class AnalyzeResponse(BaseModel):
    """Response model for longevity analysis."""
    run_id: str
    predictions: List[float]
    ldrop_metrics: Dict[str, float]
    ra_score_deltas: List[float]
    timestamp: str
    dkil_locked: bool


class DeployRequest(BaseModel):
    """Request model for model deployment."""
    run_id: str
    human_key: str = Field(..., description="Human approval key")
    logic_key: str = Field(..., description="Logic validation key")
    dkil_validation: bool = Field(default=True, description="Require DKIL validation")


class DeployResponse(BaseModel):
    """Response model for deployment."""
    status: str
    model_registry_url: Optional[str]
    message: str


# RA Feature Encoder (Mock implementation)
def ra_feature_encoder(data: pd.DataFrame) -> Dict[str, Any]:
    """
    Mock RA feature encoder that processes data with RA, D, M, S, LR features.
    In production, this would call the actual ML model.
    """
    # Mock feature extraction
    num_rows = len(data)
    
    # Generate mock predictions and metrics
    predictions = [0.85 + (i * 0.01) % 0.15 for i in range(num_rows)]
    
    ldrop_metrics = {
        "mean_ldrop": 0.12,
        "max_ldrop": 0.25,
        "min_ldrop": 0.05,
        "std_ldrop": 0.08
    }
    
    ra_score_deltas = [0.02 + (i * 0.005) % 0.05 for i in range(num_rows)]
    
    return {
        "predictions": predictions,
        "ldrop_metrics": ldrop_metrics,
        "ra_score_deltas": ra_score_deltas,
        "num_samples": num_rows
    }


def check_dkil(artifacts_path: Path) -> bool:
    """Check if DKIL lock file exists and threshold is met."""
    dkil_lock_path = artifacts_path / "dkil.lock"
    if dkil_lock_path.exists():
        with open(dkil_lock_path, "r") as f:
            dkil_data = json.load(f)
            return dkil_data.get("threshold_met", False)
    return False


def create_html_report(run_id: str, results: Dict[str, Any]) -> str:
    """Generate HTML report for analysis results."""
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>RA Longevity Report - {run_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        .metric {{ margin: 10px 0; padding: 10px; background: #ecf0f1; }}
        .metric strong {{ color: #34495e; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #bdc3c7; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
    </style>
</head>
<body>
    <h1>RA Longevity Analysis Report</h1>
    <p><strong>Run ID:</strong> {run_id}</p>
    <p><strong>Timestamp:</strong> {results.get('timestamp', 'N/A')}</p>
    <p><strong>Mode:</strong> {results.get('mode', 'N/A')}</p>
    
    <h2>LDrop Metrics</h2>
    <div class="metric"><strong>Mean LDrop:</strong> {results['ldrop_metrics']['mean_ldrop']:.4f}</div>
    <div class="metric"><strong>Max LDrop:</strong> {results['ldrop_metrics']['max_ldrop']:.4f}</div>
    <div class="metric"><strong>Min LDrop:</strong> {results['ldrop_metrics']['min_ldrop']:.4f}</div>
    <div class="metric"><strong>Std LDrop:</strong> {results['ldrop_metrics']['std_ldrop']:.4f}</div>
    
    <h2>Predictions Summary</h2>
    <p><strong>Number of Samples:</strong> {results.get('num_samples', 0)}</p>
    <p><strong>Mean Prediction:</strong> {sum(results['predictions']) / len(results['predictions']):.4f}</p>
    
    <h2>DKIL Status</h2>
    <p><strong>DKIL Locked:</strong> {'Yes' if results.get('dkil_locked', False) else 'No'}</p>
</body>
</html>
"""
    return html_content


def create_bundle_zip(run_id: str, artifacts_path: Path) -> Path:
    """Create a bundle.zip containing all artifacts for a run."""
    bundle_path = artifacts_path / f"bundle_{run_id}.zip"
    
    with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add report files
        report_json = artifacts_path / f"report_{run_id}.json"
        report_html = artifacts_path / f"report_{run_id}.html"
        dkil_lock = artifacts_path / "dkil.lock"
        
        if report_json.exists():
            zipf.write(report_json, report_json.name)
        if report_html.exists():
            zipf.write(report_html, report_html.name)
        if dkil_lock.exists():
            zipf.write(dkil_lock, dkil_lock.name)
    
    return bundle_path


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "RA Longevity MLOps API",
        "version": "1.0.0",
        "endpoints": [
            "POST /api/longevity/analyze",
            "GET /api/longevity/report/{run_id}",
            "POST /api/longevity/deploy"
        ]
    }


@app.post("/api/longevity/analyze", response_model=AnalyzeResponse)
async def analyze_longevity(
    request: AnalyzeRequest,
    token: str = Depends(verify_token)
):
    """
    Analyze CSV/JSON data with RA feature encoder.
    Returns model predictions, ldrop metrics, and RA score deltas.
    """
    try:
        # Generate unique run ID
        run_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Convert data to DataFrame
        df = pd.DataFrame(request.data)
        
        # Process with RA feature encoder
        results = ra_feature_encoder(df)
        
        # Check DKIL threshold
        dkil_locked = False
        if request.threshold is not None:
            # Mock DKIL check - in production, this would be more sophisticated
            if results['ldrop_metrics']['mean_ldrop'] >= request.threshold:
                dkil_locked = True
                dkil_data = {
                    "threshold_met": True,
                    "threshold": request.threshold,
                    "mean_ldrop": results['ldrop_metrics']['mean_ldrop'],
                    "timestamp": timestamp
                }
                with open(ARTIFACTS_DIR / "dkil.lock", "w") as f:
                    json.dump(dkil_data, f, indent=2)
        
        # Prepare response data
        response_data = {
            "run_id": run_id,
            "predictions": results["predictions"],
            "ldrop_metrics": results["ldrop_metrics"],
            "ra_score_deltas": results["ra_score_deltas"],
            "timestamp": timestamp,
            "dkil_locked": dkil_locked,
            "mode": request.mode,
            "num_samples": results["num_samples"]
        }
        
        # Save JSON report
        json_path = ARTIFACTS_DIR / f"report_{run_id}.json"
        with open(json_path, "w") as f:
            json.dump(response_data, f, indent=2)
        
        # Generate and save HTML report
        html_content = create_html_report(run_id, response_data)
        html_path = ARTIFACTS_DIR / f"report_{run_id}.html"
        with open(html_path, "w") as f:
            f.write(html_content)
        
        # Create bundle.zip
        create_bundle_zip(run_id, ARTIFACTS_DIR)
        
        return AnalyzeResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/longevity/analyze/upload")
async def analyze_longevity_csv(
    file: UploadFile = File(...),
    mode: str = "tabular",
    threshold: Optional[float] = None,
    token: str = Depends(verify_token)
):
    """
    Analyze uploaded CSV file with RA feature encoder.
    Alternative endpoint that accepts file upload.
    """
    try:
        # Read CSV file
        content = await file.read()
        df = pd.read_csv(pd.io.common.BytesIO(content))
        
        # Convert to list of dictionaries
        data = df.to_dict(orient='records')
        
        # Create request and call main analyze endpoint
        request = AnalyzeRequest(data=data, mode=mode, threshold=threshold)
        return await analyze_longevity(request, token)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV upload failed: {str(e)}")


@app.get("/api/longevity/report/{run_id}")
async def get_report(
    run_id: str,
    token: str = Depends(verify_token)
):
    """
    Get JSON and HTML report for a specific run.
    Checks DKIL before serving if enabled.
    """
    try:
        # Validate run_id to prevent path traversal
        run_id = validate_run_id(run_id)
        
        json_path = ARTIFACTS_DIR / f"report_{run_id}.json"
        html_path = ARTIFACTS_DIR / f"report_{run_id}.html"
        
        if not json_path.exists():
            raise HTTPException(status_code=404, detail=f"Report for run_id '{run_id}' not found")
        
        # Check DKIL if lock file exists
        dkil_locked = check_dkil(ARTIFACTS_DIR)
        
        # Load JSON report
        with open(json_path, "r") as f:
            json_report = json.load(f)
        
        # Load HTML report if exists
        html_report = None
        if html_path.exists():
            with open(html_path, "r") as f:
                html_report = f.read()
        
        return {
            "run_id": run_id,
            "json_report": json_report,
            "html_report": html_report,
            "dkil_locked": dkil_locked
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve report: {str(e)}")


@app.get("/api/longevity/report/{run_id}/download")
async def download_report_bundle(
    run_id: str,
    token: str = Depends(verify_token)
):
    """Download the bundle.zip for a specific run."""
    # Validate run_id to prevent path traversal
    run_id = validate_run_id(run_id)
    
    bundle_path = ARTIFACTS_DIR / f"bundle_{run_id}.zip"
    
    if not bundle_path.exists():
        raise HTTPException(status_code=404, detail=f"Bundle for run_id '{run_id}' not found")
    
    return FileResponse(
        path=bundle_path,
        media_type="application/zip",
        filename=f"bundle_{run_id}.zip"
    )


@app.post("/api/longevity/deploy", response_model=DeployResponse)
async def deploy_model(
    request: DeployRequest,
    token: str = Depends(verify_token)
):
    """
    Deploy model to model registry.
    Validates DKIL and requires two keys (human + logic).
    """
    try:
        # Validate run_id to prevent path traversal
        run_id = validate_run_id(request.run_id)
        
        # Validate run_id exists
        json_path = ARTIFACTS_DIR / f"report_{run_id}.json"
        if not json_path.exists():
            raise HTTPException(status_code=404, detail=f"Report for run_id '{run_id}' not found")
        
        # Validate DKIL if required
        if request.dkil_validation:
            if not check_dkil(ARTIFACTS_DIR):
                raise HTTPException(
                    status_code=403,
                    detail="DKIL validation failed: threshold not met or lock file missing"
                )
        
        # Validate keys (mock validation - in production, this would be more sophisticated)
        if not request.human_key or len(request.human_key) < 16:
            raise HTTPException(
                status_code=400,
                detail="Invalid human approval key: minimum 16 characters required"
            )
        
        if not request.logic_key or len(request.logic_key) < 16:
            raise HTTPException(
                status_code=400,
                detail="Invalid logic validation key: minimum 16 characters required"
            )
        
        # Mock deployment to model registry
        model_registry_url = f"https://model-registry.example.com/models/ra-longevity/{run_id}"
        
        # Create deployment record (keys are not logged for security)
        deployment_record = {
            "run_id": run_id,
            "deployed_at": datetime.now().isoformat(),
            "dkil_validated": request.dkil_validation,
            "model_registry_url": model_registry_url
        }
        
        deployment_path = ARTIFACTS_DIR / f"deployment_{run_id}.json"
        with open(deployment_path, "w") as f:
            json.dump(deployment_record, f, indent=2)
        
        return DeployResponse(
            status="success",
            model_registry_url=model_registry_url,
            message=f"Model {run_id} successfully deployed to registry"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")


# Mount static files for artifacts
app.mount("/artifacts", StaticFiles(directory=str(ARTIFACTS_DIR)), name="artifacts")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
