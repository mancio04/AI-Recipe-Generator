FROM python:3.12-slim

WORKDIR /app

COPY app/backend/requirements.txt .
RUN pip install --no-cache-dir --default-timeout=1000 \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r requirements.txt

COPY config.py .
COPY app/backend/ ./app/backend/

WORKDIR /app/app/backend

CMD ["python", "api.py"]