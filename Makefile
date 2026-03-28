.PHONY: help build deploy fmt lint test

help:
	@echo "Available targets:"
	@echo ""
	@echo "  build    - Build the local environment using uv sync with PyPI"
	@echo "  fmt      - Format all Python files with ruff"
	@echo "  lint     - Run pre-commit checks"
	@echo "  test     - Run pytest"
	@echo "  deploy   - Deploy the local target to Databricks (profile: bojarovski-llmops)"
	@echo ""

build:
	uv sync --extra dev --index https://pypi.org/simple/

fmt:
	uv run --index https://pypi.org/simple/ ruff format .

lint:
	uv run --index https://pypi.org/simple/ pre-commit run --all-files

test:
	uv run --index https://pypi.org/simple/ pytest

deploy:
	databricks --profile bojarovski-llmops bundle validate --target=local
	UV_DEFAULT_INDEX=https://pypi.org/simple databricks --profile bojarovski-llmops bundle deploy --target=local
	databricks --profile bojarovski-llmops bundle summary --target=local

.DEFAULT_GOAL := help
