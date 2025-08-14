"""AgentVisa Python SDK - Simple interface for the AgentVisa API."""

from typing import Any

from .client import AgentVisaClient

# Global default client instance
default_client: AgentVisaClient | None = None


def init(api_key: str) -> None:
    """Initialize the global AgentVisa client.

    Args:
        api_key: The API key for authentication.
    """
    global default_client
    default_client = AgentVisaClient(api_key=api_key)


def create_delegation(
    end_user_identifier: str,
    scopes: list[str],
    expires_in: int = 3600,
    *,
    delegation_type: str = "ephemeral",
    metadata: dict[str, Any] | None = None,
    timeout: float | None = 30,
) -> dict[str, Any]:
    """Create a delegation using the global client.

    Args:
        end_user_identifier: Unique identifier for the end user.
        scopes: List of permission scopes for the delegation.
        expires_in: Expiration time in seconds. Defaults to 3600 (1 hour).
        delegation_type: Delegation type. Defaults to "ephemeral".
        metadata: Optional metadata to attach to the delegation.
        timeout: Optional timeout in seconds for the HTTP request. Defaults to 30s.

    Returns:
        Dict containing the API response with delegation details.

    Raises:
        Exception: If init() has not been called first.
    """
    if not default_client:
        raise Exception("Please call agentvisa.init(api_key='...') first.")
    return default_client.delegations.create(
        end_user_identifier=end_user_identifier,
        scopes=scopes,
        expires_in=expires_in,
        delegation_type=delegation_type,
        metadata=metadata,
        timeout=timeout,
    )


def verify_delegation(
    credential: str,
    *,
    timeout: float | None = 30,
) -> dict[str, Any]:
    """Verify a delegated credential using the global client.

    Args:
        credential: The credential token to verify.
        timeout: Optional timeout in seconds for the HTTP request. Defaults to 30s.

    Returns:
        Dict containing the API response with verification details.

    Raises:
        Exception: If init() has not been called first.
    """
    if not default_client:
        raise Exception("Please call agentvisa.init(api_key='...') first.")
    return default_client.delegations.verify(
        credential=credential,
        timeout=timeout,
    )
