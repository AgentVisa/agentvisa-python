"""Delegations API resource module."""

from typing import Any

import requests


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
        self, end_user_identifier: str, scopes: list[str], expires_in: int = 3600
    ) -> dict[str, Any]:
        """Create a new delegated credential for an agent.

        Args:
            end_user_identifier: Unique identifier for the end user.
            scopes: List of permission scopes for the delegation.
            expires_in: Expiration time in seconds. Defaults to 3600 (1 hour).

        Returns:
            Dict containing the API response with delegation details.

        Raises:
            ValueError: If end_user_identifier is not provided.
            requests.HTTPError: If the API request fails.
        """
        if not end_user_identifier:
            raise ValueError("end_user_identifier is required.")

        url = f"{self.base_url}/agents"
        payload = {
            "end_user_identifier": end_user_identifier,
            "scopes": scopes,
            "expires_in": expires_in,
        }

        response = self.session.post(url, json=payload)
        response.raise_for_status()  # Raises an exception for bad status codes
        return response.json()  # type: ignore[no-any-return]
