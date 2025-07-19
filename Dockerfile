FROM python:3.8-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgomp1 \
    g++ \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# 👇 This is the fix
RUN pip install --no-cache-dir --force-reinstall --no-binary :all: numpy==1.24.4

# Install other Python dependencies
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
