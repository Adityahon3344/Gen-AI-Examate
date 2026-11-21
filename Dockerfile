
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app/ ./app/
COPY ui/ ./ui/
COPY data/ ./data/

# Expose API and Streamlit ports
EXPOSE 8000 8501

# Default command starts the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
