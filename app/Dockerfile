FROM python:3.10.6-slim

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 8000

USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
