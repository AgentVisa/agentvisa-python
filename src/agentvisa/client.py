"""AgentVisa API client module."""

import requests

from .delegations import DelegationsAPI


class AgentVisaClient:
    """Main client class for interacting with the AgentVisa API."""

    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        """Initialize the AgentVisa client.

        Args:
            api_key: The API key for authentication. Must be provided.
            base_url: Optional base URL for the API. Defaults to production URL.

        Raises:
            ValueError: If api_key is not provided or is empty.
        """
        if not api_key:
            raise ValueError("API key cannot be empty.")

        self.api_key = api_key
        self.base_url = base_url or "https://api.agentvisa.dev/v1"
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

        # Initialize API resource classes
        self.delegations = DelegationsAPI(self.session, self.base_url)
