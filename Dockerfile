FROM python:3.11-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 gcc g++ \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]