"""Shared test fixtures and configuration."""

import pytest
import responses

from agentvisa import AgentVisaClient


@pytest.fixture
def api_key():
    """Return a test API key."""
    return "test_api_key_123"


@pytest.fixture
def base_url():
    """Return a test base URL."""
    return "https://api.test.agentvisa.dev/v1"


@pytest.fixture
def client(api_key, base_url):
    """Return a test AgentVisaClient instance."""
    return AgentVisaClient(api_key=api_key, base_url=base_url)


@pytest.fixture
def mock_responses():
    """Provide a responses mock for HTTP requests."""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def sample_delegation_response():
    """Return a sample delegation API response."""
    return {
        "agent_id": "del_123456789",
        "credential": "av_tok_abcdef123456",
        "end_user_identifier": "user123",
        "scopes": ["read", "write"],
        "expires_at": "2025-01-01T12:00:00Z",
        "expires_in": 3600,
        "created_at": "2025-01-01T11:00:00Z",
    }


@pytest.fixture
def sample_verify_response():
    """Return a sample verify API response."""
    return {
        "valid": True,
        "agent_id": "del_123456789",
        "end_user_identifier": "user123",
        "scopes": ["read", "write"],
        "expires_at": "2025-01-01T12:00:00Z",
        "metadata": {"description": "Test agent"},
    }


@pytest.fixture
def sample_invalid_verify_response():
    """Return a sample invalid verify API response."""
    return {
        "valid": False,
    }
