"""
Application Settings
====================
Centralized configuration loaded from environment variables via Pydantic BaseSettings.
All settings are validated at startup. Missing required fields cause an immediate error.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application-wide settings loaded from .env file."""

    # ── LLM Configuration ──────────────────────────────────────────────
    groq_api_key: str = Field(
        default="",
        description="API key for Groq LLM inference",
    )
    model_name: str = Field(
        default="llama3-70b-8192",
        description="LLM model identifier on Groq",
    )
    temperature: float = Field(
        default=0.1,
        ge=0.0,
        le=2.0,
        description="LLM sampling temperature (lower = more deterministic)",
    )
    max_tokens: int = Field(
        default=4096,
        gt=0,
        description="Maximum tokens per LLM response",
    )

    # ── LangSmith / LangChain (Optional) ───────────────────────────────
    langchain_api_key: Optional[str] = Field(
        default=None,
        description="LangSmith API key for tracing (optional)",
    )
    langchain_tracing_v2: bool = Field(
        default=False,
        description="Enable LangSmith tracing",
    )
    langchain_project: str = Field(
        default="browser-automation-agent",
        description="LangSmith project name",
    )

    # ── Browser Configuration ──────────────────────────────────────────
    browser_headless: bool = Field(
        default=True,
        description="Run Playwright browser in headless mode",
    )
    browser_timeout: int = Field(
        default=30000,
        description="Default page load / action timeout in milliseconds",
    )
    browser_viewport_width: int = Field(
        default=1920,
        description="Browser viewport width in pixels",
    )
    browser_viewport_height: int = Field(
        default=1080,
        description="Browser viewport height in pixels",
    )

    # ── Memory Configuration ───────────────────────────────────────────
    chromadb_persist_dir: str = Field(
        default="./data/chromadb",
        description="Directory for ChromaDB persistent storage",
    )
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence-transformer model for embeddings",
    )

    # ── Agent Configuration ────────────────────────────────────────────
    max_iterations: int = Field(
        default=25,
        gt=0,
        description="Maximum ReAct loop iterations before termination",
    )
    retry_limit: int = Field(
        default=3,
        gt=0,
        description="Maximum retries per failed action",
    )
    screenshot_on_every_step: bool = Field(
        default=True,
        description="Capture a screenshot after every agent action",
    )

    # ── API Configuration ──────────────────────────────────────────────
    api_host: str = Field(
        default="0.0.0.0",
        description="FastAPI server host",
    )
    api_port: int = Field(
        default=8000,
        description="FastAPI server port",
    )
    api_key: str = Field(
        default="changeme",
        description="API key for endpoint authentication",
    )

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }


# Singleton instance — import this everywhere
settings = Settings()
