PROJECT_ID := airflow-tdd-ci-workflow
SHELL := /bin/bash
VENV_DIR := ${CURDIR}/.venv/bin
VENV_PYTHON := ${VENV_DIR}/python
PYTEST_ARGS := ""
TAG := $(shell git rev-parse --short HEAD)
ENVIRONMENT := dev

.venv:
	@python3 -m venv .venv
	@${VENV_PYTHON} -m pip install -U -q pip pip-tools

.PHONY: install-deps
install-deps: .venv
	@"${VENV_PYTHON}" -m pip install -r requirements.txt

.PHONY: isort-check
isort-check: install-deps
	@${VENV_PYTHON} -m isort -c .

.PHONY: black-check
black-check: install-deps
	@${VENV_PYTHON} -m black . --exclude=.cookiecutters

.PHONY: autoflake-check
autoflake-check: install-deps
	@${VENV_PYTHON} -m autoflake -c --remove-unused-variables --remove-all-unused-imports -r bigquery_utils credentials_utils datastore_utils pubsub_utils main.py functions tests &> /dev/null

.PHONY: mypy
mypy: install-deps
	@${VENV_PYTHON} -m mypy

.PHONY: lint
lint: autoflake-check isort-check black-check mypy

.PHONY: isort
isort: install-deps
	@${VENV_PYTHON} -m isort .

.PHONY: black
black: install-deps
	@${VENV_PYTHON} -m black . --exclude=.cookiecutters

.PHONY: autoflake
autoflake: install-deps
	@${VENV_PYTHON} -m autoflake --remove-unused-variables --remove-all-unused-imports -i -r -r bigquery_utils credentials_utils datastore_utils pubsub_utils main.py functions tests

.PHONY: format
format: autoflake isort black

.PHONY: test
test: lint update-components
	@${VENV_PYTHON} -m pytest ${PYTEST_ARGS}