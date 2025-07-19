FROM python:3.8-slim-bullseye

WORKDIR /app

RUN apt-get update --allow-releaseinfo-change \
 && apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      libgomp1 \
 && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

CMD ["python", "app.py"]
