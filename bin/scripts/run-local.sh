#!/usr/bin/env bash

alembic upgrade head && uvicorn api.application:APP --reload --host localhost --port 8010
