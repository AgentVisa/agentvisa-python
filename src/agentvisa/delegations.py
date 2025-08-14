"""Delegations API resource module."""

from typing import Any

import requests

from .models import DelegationResponse, VerifyResponse


class DelegationsAPI:
    """API resource class for managing agent delegations."""

    def __init__(self, session: requests.Session, base_url: str) -> None:
        """Initialize the DelegationsAPI.

        Args:
            session: The requests session object from the main client.
            base_url: The base URL for API requests.
        """
        self.session = session
        self.base_url = base_url

    def create(
        self,
        end_user_identifier: str,
        scopes: list[str],
        expires_in: int = 3600,
        *,
        delegation_type: str = "ephemeral",
        metadata: dict[str, Any] | None = None,
        timeout: float | None = 30,
    ) -> dict[str, Any]:
        """Create a new delegated credential for an agent.

        Args:
            end_user_identifier: Unique identifier for the end user.
            scopes: List of permission scopes for the delegation.
            expires_in: Expiration time in seconds. Defaults to 3600 (1 hour).
            delegation_type: Delegation type. Defaults to "ephemeral".
            metadata: Optional metadata to attach to the delegation.
            timeout: Optional timeout in seconds for the HTTP request. Defaults to 15s.

        Returns:
            Dict containing the API response with delegation details.

        Raises:
            ValueError: If end_user_identifier is not provided.
            requests.HTTPError: If the API request fails.
        """
        if not end_user_identifier:
            raise ValueError("end_user_identifier is required.")

        url = f"{self.base_url}/agents"
        payload: dict[str, Any] = {
            "type": delegation_type,
            "end_user_identifier": end_user_identifier,
            "scopes": scopes,
            "expires_in": expires_in,
        }
        if metadata is not None:
            payload["metadata"] = metadata

        response = self.session.post(url, json=payload, timeout=timeout)
        response.raise_for_status()  # Raises an exception for bad status codes
        data: dict[str, Any] = response.json()
        # Will raise ValidationError if unexpected structure is returned
        DelegationResponse.model_validate(data)
        return data

    def verify(
        self,
        credential: str,
        *,
        timeout: float | None = 30,
    ) -> dict[str, Any]:
        """Verify a delegated credential.

        Args:
            credential: The credential token to verify.
            timeout: Optional timeout in seconds for the HTTP request. Defaults to 30s.

        Returns:
            Dict containing the API response with verification details.

        Raises:
            ValueError: If credential is not provided.
            requests.HTTPError: If the API request fails.
        """
        if not credential:
            raise ValueError("credential is required.")

        url = f"{self.base_url}/agents/verify"
        payload: dict[str, Any] = {
            "credential": credential,
        }

        response = self.session.post(url, json=payload, timeout=timeout)
        response.raise_for_status()  # Raises an exception for bad status codes
        data: dict[str, Any] = response.json()
        # Will raise ValidationError if unexpected structure is returned
        VerifyResponse.model_validate(data)
        return data
