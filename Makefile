.PHONY: help install install-dev test test-cov lint format typecheck clean build publish

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	uv sync

install-dev: ## Install development dependencies
	uv sync --extra dev

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage report
	uv run pytest --cov=src/agentvisa --cov-report=term-missing --cov-report=html

test-watch: ## Run tests in watch mode
	uv run pytest -f

lint: ## Run linting with ruff
	uv run ruff check src tests

format: ## Format code with ruff
	uv run ruff format src tests

format-check: ## Check code formatting with ruff
	uv run ruff check src tests
	uv run ruff format --check src tests

typecheck: ## Run type checking with mypy
	uv run mypy src

check: format-check lint typecheck test ## Run all checks (format, lint, typecheck, test)

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	uv build

publish: build ## Publish to PyPI
	twine upload dist/*

dev-setup: install-dev ## Full development setup
	@echo "✅ Development environment ready!"
	@echo "Run 'make test' to verify everything works"

ci: format-check lint typecheck test ## Run all CI checks 