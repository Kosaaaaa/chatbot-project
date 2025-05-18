FROM python:3.13 AS ci

WORKDIR /app
RUN pip install --upgrade pip
RUN apt-get update \
  && apt-get install -y --no-install-recommends git curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - \
  && ln -s /etc/poetry/bin/poetry /usr/local/bin/poetry \
  && export PATH="/etc/poetry/bin:$PATH"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./

RUN poetry install

FROM python:3.13 AS builder

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry~=2.0.0 && \
  poetry install --no-root --only main && \
  poetry self add poetry-plugin-export && \
  poetry export -f requirements.txt --with dev --without-hashes --output dev-requirements.txt


FROM python:3.13 AS dev

ENV PYTHONUNBUFFERED=1 \
  PATH="/venv/bin:$PATH"

WORKDIR /app

COPY --chown=appuser:appuser --from=builder /app/.venv /venv
COPY --from=builder /app/dev-requirements.txt /tmp

RUN pip install --no-cache-dir -r /tmp/dev-requirements.txt && \
  rm /tmp/dev-requirements.txt

RUN adduser --disabled-password --uid 1000 --gecos "" --no-create-home appuser

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]

FROM python:3.13 AS runtime

ENV PATH="/venv/bin:$PATH" \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

RUN adduser --disabled-password --uid 1000 --gecos "" --no-create-home appuser

COPY --chown=appuser:appuser --from=builder /app/.venv /venv
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
