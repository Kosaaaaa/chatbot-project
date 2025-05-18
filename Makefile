.PHONY: install_poetry install build run test

POETRY_VENV ?= ${HOME}/.chatbot_project_poetry_venv
POETRY_BIN := $(POETRY_VENV)/bin/poetry
CMD:=$(POETRY_BIN) run
PYMODULE:=app
UNIT_TESTS:=tests/unit
FUNCTIONAL_TESTS:=tests/functional
PYTHON := $(VENV)/bin/python

install_poetry:
	test -d $(POETRY_VENV) || python3 -m venv $(POETRY_VENV)
	. $(POETRY_VENV)/bin/pip install --upgrade pip; $(POETRY_VENV)/bin/pip install poetry

install:
	$(POETRY_BIN) config virtualenvs.in-project true
	${POETRY_VIRTUALENVS_IN_PROJECT=true} $(POETRY_BIN) install

build: install_poetry install

run:
	$(CMD) python -m uvicorn app.main:app --reload

test:
	$(CMD) pytest --cov=$(PYMODULE) $(UNIT_TESTS) $(FUNCTIONAL_TESTS)
