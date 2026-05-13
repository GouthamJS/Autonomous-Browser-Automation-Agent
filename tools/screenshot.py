"""
Screenshot Tool
===============
Captures browser viewport or full-page screenshots and saves them
to the logs/screenshots/ directory with timestamps.
"""

import logging
import os
import asyncio
from datetime import datetime

from langchain_core.tools import tool

logger = logging.getLogger("browser_agent.tools.screenshot")

# Ensure screenshots directory exists
SCREENSHOT_DIR = os.path.join("logs", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def _run_async(coro):
    """Helper to run an async coroutine from sync context."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)


@tool
def take_screenshot(full_page: bool = False, page=None) -> str:
    """Capture a screenshot of the current browser viewport or the full page.

    Args:
        full_page: If True, captures the entire scrollable page. If False (default),
                   captures only the visible viewport.
        page: Playwright page instance (injected automatically).
    """
    async def _screenshot():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)

        await page.screenshot(
            path=filepath,
            full_page=full_page,
            type="png",
        )

        file_size = os.path.getsize(filepath)
        logger.info(
            "📸 Screenshot saved: %s (%d bytes, full_page=%s)",
            filepath, file_size, full_page,
        )
        return f"Screenshot saved to: {filepath} ({file_size} bytes)"

    return _run_async(_screenshot())
