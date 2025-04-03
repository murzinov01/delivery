FROM python:3.11 AS compile-image

ARG POETRY_VERSION=1.8.4
ARG POETRY_INSTALLER_MAX_WORKERS=1
ARG POETRY_VIRTUALENVS_CREATE=false
ARG WORKDIR=/srv/www

RUN groupadd --gid 2000 python
RUN useradd --uid 2000 --gid python --shell /usr/sbin/nologin --create-home python

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y postgresql-client libpq-dev krb5-user krb5-config libkrb5-dev curl --no-install-recommends

COPY pyproject* ./
COPY poetry.lock ./

RUN pip install -U pip "poetry==${POETRY_VERSION}"
RUN poetry install --without dev

RUN apt-get remove -y gcc cmake libkrb5-dev libpq-dev make libc-dev-bin libc6-dev
RUN rm -rf /var/lib/apt/lists/* && apt-get autoremove -y && apt-get clean && rm -rf /etc/apt/auth.conf

FROM scratch AS runtime-image

ARG LOG_LEVEL=INFO
ARG APP_HOST=0.0.0.0
ARG APP_PORT=8080
ARG WORKDIR=/srv/www


ENV PYTHON_VERSION=3.11 \
    PYTHONUNBUFFERED=1 \
    APP_HOST=${APP_HOST} \
    APP_PORT=${APP_PORT} \
    LOG_LEVEL=${LOG_LEVEL}

WORKDIR $WORKDIR
EXPOSE ${APP_PORT}

COPY --from=compile-image / /

COPY . .

RUN chmod +x entrypoint.sh

USER python:python

ENTRYPOINT ["./entrypoint.sh"]