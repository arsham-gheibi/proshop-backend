FROM python:3.12.3-alpine3.20
LABEL maintainer="Roboland.io"

ENV PYTHONUNBUFFERED=1

COPY ./app /app
COPY ./scripts /scripts
COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock
WORKDIR /app
EXPOSE 8000

ARG DEV=false

ENV POETRY_HOME=/poetry
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-deps \
    build-base linux-headers curl postgresql-dev musl-dev zlib zlib-dev && \
    mkdir -p /poetry && \
    curl -sSL https://install.python-poetry.org | python - && \
    if [ $DEV = "true" ]; \
    then /poetry/bin/poetry install --no-root --no-ansi --no-interaction --no-cache ; \
    else /poetry/bin/poetry install --no-root --no-ansi --no-interaction --no-cache --only main ; \
    fi && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app && \
    mkdir /vol/web/media && \
    mkdir /vol/web/static && \
    chown -R django-user:django-user /poetry /vol && \
    chmod -R 755 /poetry /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:$PATH"

USER django-user

CMD ["run.sh"]
