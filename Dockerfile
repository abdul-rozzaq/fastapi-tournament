FROM python:3.12-slim

WORKDIR /app

RUN apt-get update

RUN apt-get update && \
    apt-get install -y gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080


CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8080"]