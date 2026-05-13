"""
API Middleware
==============
Authentication and CORS middleware for the FastAPI application.
"""

import logging
from fastapi import Request, HTTPException, Security
from fastapi.security import APIKeyHeader

from config.settings import settings

logger = logging.getLogger("browser_agent.api.middleware")

# API Key security scheme
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Validate the API key from the Authorization header.
    Expects format: 'Bearer <api_key>'

    Args:
        api_key: The Authorization header value.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the key is missing or invalid.
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key. Use the Authorization header with 'Bearer <key>'.",
        )

    # Strip 'Bearer ' prefix
    if api_key.startswith("Bearer "):
        api_key = api_key[7:]

    if api_key != settings.api_key:
        logger.warning("⚠️ Invalid API key attempt")
        raise HTTPException(
            status_code=403,
            detail="Invalid API key.",
        )

    return api_key


# CORS origins — adjust for production
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]
