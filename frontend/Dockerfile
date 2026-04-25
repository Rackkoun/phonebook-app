# file frontend\Dockerfile
FROM python:3.11.3-slim

WORKDIR  /app

COPY frontend/requirements.txt ./frontend/
RUN pip install --no-cache-dir -r frontend/requirements.txt

COPY frontend/ ./frontend/

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
CMD [ "python", "frontend/app/main.py" ]