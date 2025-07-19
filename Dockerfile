FROM python:3.8-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update --allow-releaseinfo-change \
 && apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies cleanly
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Run the app
CMD ["python", "app.py"]
