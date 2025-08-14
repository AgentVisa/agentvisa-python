"""Tests for the convenience functions in agentvisa.__init__."""

import pytest
import responses

import agentvisa
from agentvisa import AgentVisaClient


class TestInitModule:
    """Test cases for agentvisa module convenience functions."""

    def setup_method(self):
        """Reset the global client before each test."""
        agentvisa.default_client = None

    def test_init_function(self, api_key):
        """Test the init function creates a global client."""
        agentvisa.init(api_key=api_key)

        assert agentvisa.default_client is not None
        assert isinstance(agentvisa.default_client, AgentVisaClient)
        assert agentvisa.default_client.api_key == api_key

    def test_init_function_overwrites_existing_client(self, api_key):
        """Test that init overwrites an existing client."""
        # Initialize first client
        agentvisa.init(api_key="first_key")
        first_client = agentvisa.default_client

        # Initialize second client
        agentvisa.init(api_key=api_key)
        second_client = agentvisa.default_client

        assert first_client is not second_client
        assert second_client.api_key == api_key

    @responses.activate
    def test_create_delegation_success(self, api_key, sample_delegation_response):
        """Test successful delegation creation using convenience function."""
        # Initialize the SDK
        agentvisa.init(api_key=api_key)

        # Mock the API response
        responses.add(
            responses.POST,
            f"{agentvisa.default_client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        result = agentvisa.create_delegation(
            end_user_identifier="user123", scopes=["read", "write"], expires_in=3600
        )

        assert result == sample_delegation_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_create_delegation_with_defaults(self, api_key, sample_delegation_response):
        """Test delegation creation with default parameters."""
        agentvisa.init(api_key=api_key)

        responses.add(
            responses.POST,
            f"{agentvisa.default_client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        result = agentvisa.create_delegation(
            end_user_identifier="user123", scopes=["read", "write"]
        )

        assert result == sample_delegation_response

        # Check default expires_in was used
        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["expires_in"] == 3600

    def test_create_delegation_without_init(self):
        """Test delegation creation fails when init hasn't been called."""
        with pytest.raises(Exception, match="Please call agentvisa.init"):
            agentvisa.create_delegation(
                end_user_identifier="user123", scopes=["read", "write"]
            )

    def test_create_delegation_after_reset(self, api_key):
        """Test delegation creation fails after resetting default_client."""
        agentvisa.init(api_key=api_key)
        agentvisa.default_client = None  # Simulate reset

        with pytest.raises(Exception, match="Please call agentvisa.init"):
            agentvisa.create_delegation(
                end_user_identifier="user123", scopes=["read", "write"]
            )

    @responses.activate
    def test_create_delegation_passes_all_parameters(
        self, api_key, sample_delegation_response
    ):
        """Test that create_delegation passes all parameters correctly."""
        agentvisa.init(api_key=api_key)

        responses.add(
            responses.POST,
            f"{agentvisa.default_client.base_url}/agents",
            json=sample_delegation_response,
            status=201,
        )

        end_user_id = "test_user_456"
        scopes = ["admin", "read", "write"]
        expires_in = 7200

        agentvisa.create_delegation(
            end_user_identifier=end_user_id, scopes=scopes, expires_in=expires_in
        )

        # Verify all parameters were passed correctly
        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["type"] == "ephemeral"
        assert payload["end_user_identifier"] == end_user_id
        assert payload["scopes"] == scopes
        assert payload["expires_in"] == expires_in

    @responses.activate
    def test_verify_delegation_success(self, api_key, sample_verify_response):
        """Test successful delegation verification using convenience function."""
        # Initialize the SDK
        agentvisa.init(api_key=api_key)

        # Mock the API response
        responses.add(
            responses.POST,
            f"{agentvisa.default_client.base_url}/agents/verify",
            json=sample_verify_response,
            status=200,
        )

        credential = "av_tok_abcdef123456"
        result = agentvisa.verify_delegation(credential=credential)

        assert result == sample_verify_response
        assert len(responses.calls) == 1

        # Verify request details
        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["credential"] == credential

    @responses.activate
    def test_verify_delegation_with_custom_timeout(
        self, api_key, sample_verify_response
    ):
        """Test delegation verification with custom timeout."""
        agentvisa.init(api_key=api_key)

        responses.add(
            responses.POST,
            f"{agentvisa.default_client.base_url}/agents/verify",
            json=sample_verify_response,
            status=200,
        )

        credential = "av_tok_abcdef123456"
        result = agentvisa.verify_delegation(credential=credential, timeout=5)

        assert result == sample_verify_response

        # Verify request details
        import json

        payload = json.loads(responses.calls[0].request.body)
        assert payload["credential"] == credential

    def test_verify_delegation_without_init(self):
        """Test delegation verification fails when init hasn't been called."""
        with pytest.raises(Exception, match="Please call agentvisa.init"):
            agentvisa.verify_delegation(credential="av_tok_abcdef123456")

    def test_verify_delegation_after_reset(self, api_key):
        """Test delegation verification fails after resetting default_client."""
        agentvisa.init(api_key=api_key)
        agentvisa.default_client = None  # Simulate reset

        with pytest.raises(Exception, match="Please call agentvisa.init"):
            agentvisa.verify_delegation(credential="av_tok_abcdef123456")
