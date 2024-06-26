# Dockerfile

FROM python:3.12

ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN pip install poetry

COPY . /code/
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

EXPOSE 8000