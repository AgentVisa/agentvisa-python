"""Tests for the AgentVisaClient class."""

import pytest
import requests

from agentvisa import AgentVisaClient
from agentvisa.delegations import DelegationsAPI


class TestAgentVisaClient:
    """Test cases for AgentVisaClient."""

    def test_init_with_api_key(self, api_key):
        """Test client initialization with API key."""
        client = AgentVisaClient(api_key=api_key)

        assert client.api_key == api_key
        assert client.base_url == "https://api.agentvisa.dev/v1"
        assert isinstance(client.session, requests.Session)
        assert client.session.headers["Authorization"] == f"Bearer {api_key}"
        assert client.session.headers["Content-Type"] == "application/json"
        assert isinstance(client.delegations, DelegationsAPI)

    def test_init_with_custom_base_url(self, api_key, base_url):
        """Test client initialization with custom base URL."""
        client = AgentVisaClient(api_key=api_key, base_url=base_url)

        assert client.base_url == base_url

    def test_init_without_api_key(self):
        """Test client initialization fails without API key."""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            AgentVisaClient(api_key="")

    def test_init_with_none_api_key(self):
        """Test client initialization fails with None API key."""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            AgentVisaClient(api_key=None)

    def test_session_headers_are_set(self, api_key):
        """Test that session headers are properly configured."""
        client = AgentVisaClient(api_key=api_key)

        expected_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        for key, value in expected_headers.items():
            assert client.session.headers[key] == value

    def test_delegations_api_is_configured(self, client):
        """Test that delegations API is properly configured."""
        assert hasattr(client, "delegations")
        assert isinstance(client.delegations, DelegationsAPI)
        assert client.delegations.session is client.session
        assert client.delegations.base_url == client.base_url
