"""
Validation Tools
================
Tools for checking page state — waiting for elements and verifying their existence.
"""

import logging
import asyncio
from langchain_core.tools import tool

logger = logging.getLogger("browser_agent.tools.validation")


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
def wait_for_element(selector: str, timeout: int = 10000, page=None) -> str:
    """Wait for a specific element to appear on the page.

    Args:
        selector: CSS selector for the element to wait for.
        timeout: Maximum time to wait in milliseconds (default: 10000).
        page: Playwright page instance (injected automatically).
    """
    async def _wait():
        try:
            await page.wait_for_selector(selector, timeout=timeout, state="visible")
            logger.info("✅ Element appeared: %s", selector)
            return f"Element '{selector}' is now visible on the page."
        except Exception as e:
            logger.warning("⏰ Timeout waiting for element: %s", selector)
            return f"Timeout: element '{selector}' did not appear within {timeout}ms. Error: {str(e)}"

    return _run_async(_wait())


@tool
def check_element_exists(selector: str, page=None) -> str:
    """Check whether a specific element exists on the current page (without waiting).

    Args:
        selector: CSS selector for the element to check.
        page: Playwright page instance (injected automatically).
    """
    async def _check():
        element = await page.query_selector(selector)
        if element:
            # Also check visibility
            is_visible = await element.is_visible()
            status = "visible" if is_visible else "exists but hidden"
            logger.info("🔍 Element '%s': %s", selector, status)
            return f"Element '{selector}' {status} on the page."
        else:
            logger.info("🔍 Element '%s': not found", selector)
            return f"Element '{selector}' does NOT exist on the page."

    return _run_async(_check())
