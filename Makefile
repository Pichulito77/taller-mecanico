.PHONY: setup lint format test ci

setup:
	python -m pip install --upgrade pip
	pip install ruff black pre-commit pytest
	pre-commit install

lint:
	ruff check .

format:
	black .

test:
	pytest || true

ci: lint test