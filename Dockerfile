FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTHCODE=1 \
    PYTHONUNBUFFERED=1 \
    SQLITE_DIR=/app/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /appa/data

EXPOSE 5000

CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 app:app"]