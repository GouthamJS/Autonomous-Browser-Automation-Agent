"""
Browser Configuration
=====================
Manages Playwright browser lifecycle — launch, context creation, and cleanup.
Provides an async context manager for convenient usage.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Tuple

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from config.settings import settings

logger = logging.getLogger("browser_agent.browser")


# Default browser launch arguments for stability
BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-extensions",
    "--disable-infobars",
]


@asynccontextmanager
async def get_browser() -> AsyncGenerator[Tuple[Browser, BrowserContext, Page], None]:
    """
    Async context manager that yields (browser, context, page).

    Usage:
        async with get_browser() as (browser, context, page):
            await page.goto("https://example.com")

    Automatically cleans up browser resources on exit.
    """
    playwright = await async_playwright().start()

    logger.info(
        "Launching Chromium (headless=%s, viewport=%dx%d)",
        settings.browser_headless,
        settings.browser_viewport_width,
        settings.browser_viewport_height,
    )

    browser = await playwright.chromium.launch(
        headless=settings.browser_headless,
        args=BROWSER_ARGS,
    )

    context = await browser.new_context(
        viewport={
            "width": settings.browser_viewport_width,
            "height": settings.browser_viewport_height,
        },
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        locale="en-US",
        timezone_id="America/New_York",
    )

    # Set default navigation timeout
    context.set_default_timeout(settings.browser_timeout)

    page = await context.new_page()

    try:
        yield browser, context, page
    finally:
        logger.info("Closing browser resources")
        await context.close()
        await browser.close()
        await playwright.stop()
