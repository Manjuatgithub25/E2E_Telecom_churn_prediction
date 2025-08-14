# FROM python:3.11-slim-bullseye

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# CMD ["python3", "app.py"]

# Use Python 3.11 slim image
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies for ML packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \                     
    gcc \                           
    g++ \                           
 && rm -rf /var/lib/apt/lists/*     

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . /app

# Default command to run the app
CMD ["python3", "app.py"]
