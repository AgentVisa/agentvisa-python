"""Tests for the DelegationsAPI class."""

import pytest
import responses
from requests.exceptions import HTTPError

from agentvisa.delegations import DelegationsAPI


class TestDelegationsAPI:
    """Test cases for DelegationsAPI."""

    def test_init(self, client):
        """Test DelegationsAPI initialization."""
        delegations = DelegationsAPI(client.session, client.base_url)

        assert delegations.session is client.session
        assert delegations.base_url == client.base_url

    @responses.activate
    def test_create_delegation_success(self, client, sample_delegation_response):
        """Test successful delegation creation."""
        # Mock the API response
        responses.add(
            responses.POST,
            f"{client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        result = client.delegations.create(
            end_user_identifier="user123", scopes=["read", "write"], expires_in=3600
        )

        assert result == sample_delegation_response
        assert len(responses.calls) == 1

        # Verify request details
        request = responses.calls[0].request
        assert request.url == f"{client.base_url}/agents"

        # Check request payload
        import json

        payload = json.loads(request.body)
        assert payload["type"] == "ephemeral"
        assert payload["end_user_identifier"] == "user123"
        assert payload["scopes"] == ["read", "write"]
        assert payload["expires_in"] == 3600

    @responses.activate
    def test_create_delegation_with_default_expires_in(
        self, client, sample_delegation_response
    ):
        """Test delegation creation with default expires_in."""
        responses.add(
            responses.POST,
            f"{client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        result = client.delegations.create(
            end_user_identifier="user123", scopes=["read", "write"]
        )

        assert result == sample_delegation_response

        # Check default expires_in was used
        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["type"] == "ephemeral"
        assert payload["expires_in"] == 3600

    def test_create_delegation_without_end_user_identifier(self, client):
        """Test delegation creation fails without end_user_identifier."""
        with pytest.raises(ValueError, match="end_user_identifier is required"):
            client.delegations.create(end_user_identifier="", scopes=["read", "write"])

    def test_create_delegation_with_none_end_user_identifier(self, client):
        """Test delegation creation fails with None end_user_identifier."""
        with pytest.raises(ValueError, match="end_user_identifier is required"):
            client.delegations.create(
                end_user_identifier=None, scopes=["read", "write"]
            )

    @responses.activate
    def test_create_delegation_http_error(self, client):
        """Test delegation creation handles HTTP errors."""
        responses.add(
            responses.POST,
            f"{client.base_url}/agents",
            json={"error": "Unauthorized"},
            status=401,
        )

        with pytest.raises(HTTPError):
            client.delegations.create(
                end_user_identifier="user123", scopes=["read", "write"]
            )

    @responses.activate
    def test_create_delegation_server_error(self, client):
        """Test delegation creation handles server errors."""
        responses.add(
            responses.POST,
            f"{client.base_url}/agents",
            json={"error": "Internal server error"},
            status=500,
        )

        with pytest.raises(HTTPError):
            client.delegations.create(
                end_user_identifier="user123", scopes=["read", "write"]
            )

    @responses.activate
    def test_create_delegation_with_different_scopes(
        self, client, sample_delegation_response
    ):
        """Test delegation creation with different scopes."""
        responses.add(
            responses.POST,
            f"{client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        scopes = ["admin", "read", "write", "delete"]
        client.delegations.create(end_user_identifier="user123", scopes=scopes)

        # Verify scopes in request
        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["scopes"] == scopes

    @responses.activate
    def test_create_delegation_with_custom_expires_in(
        self, client, sample_delegation_response
    ):
        """Test delegation creation with custom expires_in."""
        responses.add(
            responses.POST,
            f"{client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        custom_expires_in = 7200
        client.delegations.create(
            end_user_identifier="user123", scopes=["read"], expires_in=custom_expires_in
        )

        # Verify expires_in in request
        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["expires_in"] == custom_expires_in

    @responses.activate
    def test_create_delegation_with_metadata_and_overrides(
        self, client, sample_delegation_response
    ):
        """Test delegation creation with metadata and type/timeout overrides."""
        responses.add(
            responses.POST,
            f"{client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        metadata = {"description": "desc", "foo": 1}
        _ = client.delegations.create(
            end_user_identifier="user123",
            scopes=["read"],
            metadata=metadata,
            delegation_type="ephemeral",
            timeout=5,
        )

        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["type"] == "ephemeral"
        assert payload["metadata"] == metadata
