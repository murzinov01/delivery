#!/usr/bin/env bash

alembic upgrade head && uvicorn api.application:APP --reload --host "${APP_HOST}" --port "${APP_PORT}" "$@"
