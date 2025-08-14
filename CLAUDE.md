# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the official Python SDK for the AgentVisa API - a service that creates short-lived, scoped credentials (delegations) for AI agents to perform actions on behalf of end users. The SDK provides both a simple global interface and a more advanced client-based interface.

## Architecture

The SDK has a layered architecture:

- **Global Interface (`src/agentvisa/__init__.py`)**: Simple functions like `init()` and `create_delegation()` that use a default client instance
- **Client Layer (`src/agentvisa/client.py`)**: `AgentVisaClient` class that manages authentication and HTTP sessions
- **API Resources (`src/agentvisa/delegations.py`)**: `DelegationsAPI` class that handles delegation-specific API calls
- **Models (`src/agentvisa/models.py`)**: Pydantic models for request/response validation, including backward compatibility aliases

The main flow: User calls global function → Uses default client → Calls appropriate API resource → Makes HTTP request → Validates response with Pydantic models.

## Development Commands

This project uses `uv` for dependency management and a Makefile for common tasks:

**Setup:**
```bash
make install          # Install production dependencies
make install-dev      # Install with dev dependencies
make dev-setup        # Full development setup
```

**Testing:**
```bash
make test            # Run tests with pytest
make test-cov        # Run tests with coverage report (requires 90% coverage)
make test-watch      # Run tests in watch mode
```

**Code Quality:**
```bash
make lint           # Run ruff linting
make format         # Format code with ruff
make format-check   # Check formatting without modifying
make typecheck      # Run mypy type checking
make check          # Run all checks (format, lint, typecheck, test)
```

**Build/Release:**
```bash
make clean          # Clean build artifacts
make build          # Build package with hatchling
make publish        # Publish to PyPI
```

**Running individual tests:**
```bash
uv run pytest tests/test_client.py::TestAgentVisaClient::test_init_success
uv run pytest tests/test_delegations.py -k "test_create"
```

## Testing Patterns

Tests use pytest with these key patterns:
- **Fixtures in `conftest.py`**: `api_key`, `base_url`, `client`, `mock_responses`, `sample_delegation_response`
- **HTTP mocking**: Uses `responses` library to mock API calls
- **Coverage**: Minimum 90% coverage required, generates HTML reports in `htmlcov/`
- **Test structure**: Tests are in `tests/` directory, following `test_*.py` naming

## Code Standards

**Type Checking:**
- Uses mypy with strict settings (disallow untyped defs, etc.)
- All source code must have type annotations
- Tests are exempt from some type checking requirements

**Linting/Formatting:**
- Uses ruff for both linting and formatting
- Line length: 88 characters
- Target Python version: 3.13
- Imports organized with isort rules

**Dependencies:**
- Production: `requests`, `pydantic` 
- Dev: `pytest`, `pytest-cov`, `pytest-mock`, `responses`, `ruff`, `mypy`
- Python >= 3.13 required

## Key Implementation Details

**Authentication**: API key passed as Bearer token in Authorization header

**Response Handling**: All API responses validated with Pydantic models. The `DelegationResponse` model includes backward compatibility aliases (`id` for `agent_id`, `token` for `credential`).

**Error Handling**: Uses standard Python exceptions - `ValueError` for invalid inputs, `requests.HTTPError` for API errors.

**Global State**: The global interface uses a module-level `default_client` variable that must be initialized with `init()` before use.

**HTTP Timeouts**: Default 30-second timeout for API requests, configurable per request.