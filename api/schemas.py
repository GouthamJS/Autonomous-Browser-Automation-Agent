"""
API Schemas
===========
Pydantic models for request validation and response serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    """Possible agent run statuses."""
    QUEUED = "queued"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentRunRequest(BaseModel):
    """Request body for starting a new agent run."""

    goal: str = Field(
        ...,
        description="Natural-language description of the task for the agent.",
        min_length=3,
        max_length=2000,
        examples=["Search for AI news on TechCrunch and extract the top 5 headlines"],
    )
    max_iterations: Optional[int] = Field(
        default=None,
        ge=1,
        le=100,
        description="Override the default max iterations for this run.",
    )
    headless: Optional[bool] = Field(
        default=None,
        description="Override headless browser setting for this run.",
    )
    use_memory: bool = Field(
        default=True,
        description="Whether to use long-term memory for this run.",
    )


class AgentRunResponse(BaseModel):
    """Response returned when an agent run starts."""

    run_id: str = Field(
        ...,
        description="Unique identifier for this agent run.",
    )
    status: AgentStatus = Field(
        ...,
        description="Current status of the run.",
    )
    goal: str = Field(
        ...,
        description="The goal that was submitted.",
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the run was created.",
    )
    message: str = Field(
        default="Agent run started successfully.",
        description="Human-readable status message.",
    )


class AgentRunResult(BaseModel):
    """Full result of a completed agent run."""

    run_id: str
    status: AgentStatus
    goal: str
    final_output: str = Field(default="", description="The agent's final answer/result.")
    iterations: int = Field(default=0, description="Number of iterations executed.")
    screenshots: list[str] = Field(default_factory=list, description="Paths to captured screenshots.")
    errors: list[str] = Field(default_factory=list, description="Errors encountered during execution.")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)
