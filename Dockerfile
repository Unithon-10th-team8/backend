# Run on Python 3.11 Alpine
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.6.1

# Install Poetry
RUN apk add --no-cache curl make build-base libffi-dev openssl-dev python3-dev \
    && curl -sSL https://install.python-poetry.org | python -


# Update PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Copy requirements
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-dev --sync

# Copy the application
COPY . /app

# Run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]