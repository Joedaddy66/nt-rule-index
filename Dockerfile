FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements-api.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy application code
COPY api_server.py .

# Create artifacts directory
RUN mkdir -p /app/artifacts

# Set environment variables
ENV PORT=8080
ENV API_BEARER_TOKEN=default-secure-token-change-me

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "api_server.py"]
