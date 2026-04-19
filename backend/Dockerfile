FROM python:3.11.3-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY app/ ./app/

# create non-route user for sec
RUN useradd -m -u 1000 && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "8000" ]