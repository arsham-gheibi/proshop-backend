FROM python:3.12.3-alpine3.20
LABEL maintainer="Roboland.io"

COPY ./app /app
COPY ./scripts /scripts
COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock
WORKDIR /app
EXPOSE 8000

ARG DEV=false

ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME=/poetry \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/scripts:/poetry/bin:$PATH"

RUN apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-deps \
    build-base linux-headers curl postgresql-dev musl-dev zlib zlib-dev && \
    curl -sSL https://install.python-poetry.org | python - && \
    if [ $DEV = "true" ]; \
    then poetry install --no-root --no-ansi --no-interaction --no-cache ; \
    else poetry install --no-root --no-ansi --no-interaction --no-cache --only main ; \
    fi && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /poetry /vol && \
    chmod -R 755 /poetry /vol && \
    chmod -R +x /scripts


USER django-user

CMD ["run.sh"]
