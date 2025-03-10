#!/usr/bin/env bash

poetry run isort .
poetry run black .
poetry run ruff check .
poetry run mypy .