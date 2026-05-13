"""
Navigation Tools
================
Playwright-based tools for URL navigation and page management.
Each tool accepts a `page` kwarg (Playwright Page) injected by the tool_node.
"""

import logging
import asyncio
from langchain_core.tools import tool

logger = logging.getLogger("browser_agent.tools.navigation")


def _run_async(coro):
    """Helper to run an async coroutine from sync context."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # We're inside an async context — create a task
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    else:
        return asyncio.run(coro)


@tool
def navigate_to_url(url: str, page=None) -> str:
    """Navigate the browser to a specific URL. Returns the page title after loading.

    Args:
        url: The full URL to navigate to (e.g., 'https://example.com').
        page: Playwright page instance (injected automatically).
    """
    async def _nav():
        await page.goto(url, wait_until="domcontentloaded")
        title = await page.title()
        logger.info("🌐 Navigated to: %s (title: %s)", url, title)
        return f"Successfully navigated to {url}. Page title: '{title}'"

    return _run_async(_nav())


@tool
def go_back(page=None) -> str:
    """Navigate the browser back to the previous page.

    Args:
        page: Playwright page instance (injected automatically).
    """
    async def _back():
        await page.go_back(wait_until="domcontentloaded")
        url = page.url
        title = await page.title()
        logger.info("⬅️ Navigated back to: %s", url)
        return f"Navigated back to {url}. Page title: '{title}'"

    return _run_async(_back())


@tool
def go_forward(page=None) -> str:
    """Navigate the browser forward to the next page.

    Args:
        page: Playwright page instance (injected automatically).
    """
    async def _forward():
        await page.go_forward(wait_until="domcontentloaded")
        url = page.url
        title = await page.title()
        logger.info("➡️ Navigated forward to: %s", url)
        return f"Navigated forward to {url}. Page title: '{title}'"

    return _run_async(_forward())


@tool
def refresh_page(page=None) -> str:
    """Reload the current page.

    Args:
        page: Playwright page instance (injected automatically).
    """
    async def _refresh():
        await page.reload(wait_until="domcontentloaded")
        url = page.url
        title = await page.title()
        logger.info("🔄 Page refreshed: %s", url)
        return f"Page refreshed. URL: {url}. Title: '{title}'"

    return _run_async(_refresh())
