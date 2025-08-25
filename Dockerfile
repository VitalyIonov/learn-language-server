FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS dev

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-root

COPY app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS prod

RUN pip install "poetry==2.1.3" "poetry-plugin-export==1.8.0"

COPY pyproject.toml poetry.lock* /app/

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt \
 && pip install --no-cache-dir -r requirements.txt

COPY app /app/app

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000", "--workers", "4"]
