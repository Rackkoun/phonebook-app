# file frontend\Dockerfile
FROM python:3.11.3-slim

WORKDIR  /app

COPY frontend/ .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
CMD [ "python", "app/main.py" ]