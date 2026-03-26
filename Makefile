PYTHON := python
VENV_DIR := .venv

.PHONY: venv install train run test lint docker-build docker-run

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install:
	$(VENV_DIR)/Scripts/python -m pip install --upgrade pip
	$(VENV_DIR)/Scripts/pip install -r requirements-dev.txt

train:
	$(VENV_DIR)/Scripts/python scripts/train.py

run:
	$(VENV_DIR)/Scripts/uvicorn mlops_api.main:app --app-dir apps/api --host 0.0.0.0 --port 8000

test:
	$(VENV_DIR)/Scripts/pytest

lint:
	$(VENV_DIR)/Scripts/ruff check .

docker-build:
	docker build -t ml-api .

docker-run:
	docker run --rm -p 8000:8000 ml-api
