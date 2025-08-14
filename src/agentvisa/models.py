"""Pydantic models for AgentVisa API responses."""

from __future__ import annotations

from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class DelegationResponse(BaseModel):
    """Validated response for a delegation create request.

    Accepts both the canonical API field names and legacy aliases used in
    earlier SDK samples/tests.
    """

    agent_id: str = Field(validation_alias=AliasChoices("agent_id", "id"))
    credential: str = Field(validation_alias=AliasChoices("credential", "token"))

    # Optional/ancillary fields the API may include
    correlation_id: str | None = None
    expires_at: str
    expires_in: int | None = None
    end_user_identifier: str | None = None
    scopes: list[str] | None = None
    created_at: str | None = None
    metadata: dict[str, Any] | None = None

    model_config = ConfigDict(extra="ignore")


class VerifyResponse(BaseModel):
    """Validated response for a credential verification request."""

    valid: bool
    agent_id: str | None = None
    expires_at: str | None = None
    end_user_identifier: str | None = None
    scopes: list[str] | None = None
    metadata: dict[str, Any] | None = None

    model_config = ConfigDict(extra="ignore")
