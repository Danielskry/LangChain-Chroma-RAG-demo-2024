# Use an official Python runtime as a parent image
FROM python:3.11-bookworm

RUN pip install poetry==1.6.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

ADD pyproject.toml .
ADD poetry.lock .

RUN poetry install

COPY . .

# Run Gunicorn with Poetry
CMD ["poetry", "run", "gunicorn", "-k", "uvicorn.workers.UvicornH11Worker", "-b", "0.0.0.0:5000", "--reload", "server:app"]
