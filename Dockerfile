
# Use Python 3.13 lightweight image
FROM python:3.13-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure Python logs appear immediately
ENV PYTHONUNBUFFERED=1

# Set application working directory
WORKDIR /app

# Copy package metadata and documentation
COPY pyproject.toml README.md ./

# Copy application source code
COPY src/ ./src/

# Install the application and its dependencies
RUN pip install --no-cache-dir .

# FastAPI default port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "receipt_ocr.api:app", "--host", "0.0.0.0", "--port", "8000"]
