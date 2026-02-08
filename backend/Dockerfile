FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including build tools and libraries needed for AI
RUN apt-get update && apt-get install -y \
    build-essential \
    libopencv-dev \
    libgomp1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt .
COPY requirements-production.txt .

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies (base requirements first)
RUN pip install --no-cache-dir -r requirements.txt

# Install production requirements with AI libraries
RUN pip install --no-cache-dir -r requirements-production.txt

# Install TensorFlow CPU (optimized for VPS without GPU)
RUN pip install --no-cache-dir tensorflow-cpu==2.15.0

# Install PyTorch CPU version
RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.16.0 --index-url https://download.pytorch.org/whl/cpu

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p reports uploads logs ai_engine/models

# Set proper permissions
RUN chmod -R 755 /app

# Add health check script
RUN echo '#!/bin/sh\ncurl -f http://localhost:8000/health || exit 1' > /app/healthcheck.sh && \
    chmod +x /app/healthcheck.sh

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TF_CPP_MIN_LOG_LEVEL=2 \
    NUMBA_CACHE_DIR=/tmp

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD /app/healthcheck.sh

# Run the application with optimized settings
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "5"]

