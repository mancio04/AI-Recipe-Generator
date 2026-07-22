FROM python:3.12-slim

WORKDIR /app

COPY app/frontend/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

COPY app/frontend/ ./app/frontend/

WORKDIR /app/app/frontend

CMD ["python", "app.py"]