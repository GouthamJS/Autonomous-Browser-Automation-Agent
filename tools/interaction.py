"""
Interaction Tools
=================
Playwright-based tools for interacting with web page elements —
clicking, typing, selecting dropdowns, scrolling, and pressing keys.
"""

import logging
import asyncio
from langchain_core.tools import tool

logger = logging.getLogger("browser_agent.tools.interaction")


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
def click_element(selector: str, page=None) -> str:
    """Click on a web element identified by a CSS selector or text.

    Args:
        selector: CSS selector, text selector (e.g., 'text=Submit'), or XPath.
        page: Playwright page instance (injected automatically).
    """
    async def _click():
        await page.click(selector, timeout=10000)
        logger.info("🖱️ Clicked element: %s", selector)
        # Wait a moment for any page transitions
        await page.wait_for_timeout(500)
        return f"Successfully clicked element: '{selector}'"

    return _run_async(_click())


@tool
def type_text(selector: str, text: str, clear_first: bool = True, page=None) -> str:
    """Type text into an input field identified by a CSS selector.

    Args:
        selector: CSS selector for the input field.
        text: The text to type.
        clear_first: Whether to clear the field before typing (default True).
        page: Playwright page instance (injected automatically).
    """
    async def _type():
        if clear_first:
            await page.fill(selector, text, timeout=10000)
        else:
            await page.type(selector, text, timeout=10000)
        logger.info("⌨️ Typed '%s' into: %s", text, selector)
        return f"Successfully typed '{text}' into element: '{selector}'"

    return _run_async(_type())


@tool
def select_dropdown(selector: str, value: str, page=None) -> str:
    """Select an option from a dropdown/select element.

    Args:
        selector: CSS selector for the <select> element.
        value: The value or visible text of the option to select.
        page: Playwright page instance (injected automatically).
    """
    async def _select():
        # Try selecting by value first, then by label
        try:
            await page.select_option(selector, value=value, timeout=10000)
        except Exception:
            await page.select_option(selector, label=value, timeout=10000)
        logger.info("📋 Selected '%s' from dropdown: %s", value, selector)
        return f"Successfully selected '{value}' from dropdown: '{selector}'"

    return _run_async(_select())


@tool
def scroll_page(direction: str = "down", amount: int = 500, page=None) -> str:
    """Scroll the page in a specified direction.

    Args:
        direction: Direction to scroll — 'up', 'down', 'top', or 'bottom'.
        amount: Number of pixels to scroll (used for 'up'/'down'). Default: 500.
        page: Playwright page instance (injected automatically).
    """
    async def _scroll():
        if direction == "top":
            await page.evaluate("window.scrollTo(0, 0)")
        elif direction == "bottom":
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        elif direction == "up":
            await page.evaluate(f"window.scrollBy(0, -{amount})")
        else:  # down
            await page.evaluate(f"window.scrollBy(0, {amount})")

        logger.info("📜 Scrolled %s by %dpx", direction, amount)
        return f"Scrolled {direction} by {amount}px"

    return _run_async(_scroll())


@tool
def press_key(key: str, page=None) -> str:
    """Press a keyboard key (e.g., Enter, Tab, Escape, ArrowDown).

    Args:
        key: The key to press (e.g., 'Enter', 'Tab', 'Escape', 'ArrowDown').
        page: Playwright page instance (injected automatically).
    """
    async def _press():
        await page.keyboard.press(key)
        logger.info("⌨️ Pressed key: %s", key)
        await page.wait_for_timeout(300)
        return f"Pressed key: '{key}'"

    return _run_async(_press())
