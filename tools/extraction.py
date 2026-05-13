"""
Extraction Tools
================
Playwright-based tools for extracting content from web pages —
text, links, tables, titles, and URLs.
"""

import logging
import asyncio
from langchain_core.tools import tool

logger = logging.getLogger("browser_agent.tools.extraction")


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
def extract_text(selector: str, page=None) -> str:
    """Extract text content from a specific element identified by a CSS selector.

    Args:
        selector: CSS selector for the element to extract text from.
        page: Playwright page instance (injected automatically).
    """
    async def _extract():
        element = await page.query_selector(selector)
        if element is None:
            return f"No element found matching selector: '{selector}'"
        text = await element.inner_text()
        text = text.strip()
        logger.info("📝 Extracted %d chars from: %s", len(text), selector)
        return text if text else "Element found but contains no text."

    return _run_async(_extract())


@tool
def extract_all_text(page=None) -> str:
    """Extract all visible text content from the current page.

    Args:
        page: Playwright page instance (injected automatically).
    """
    async def _extract_all():
        text = await page.inner_text("body")
        text = text.strip()
        # Trim to avoid overwhelming the LLM context
        if len(text) > 5000:
            text = text[:5000] + "\n\n… [content trimmed to 5000 characters]"
        logger.info("📝 Extracted all page text: %d chars", len(text))
        return text if text else "No visible text found on the page."

    return _run_async(_extract_all())


@tool
def extract_links(selector: str = "a", page=None) -> str:
    """Extract all hyperlinks (href values and anchor text) from the page or a specific container.

    Args:
        selector: CSS selector for the container or 'a' for all links. Default: 'a'.
        page: Playwright page instance (injected automatically).
    """
    async def _extract_links():
        links = await page.evaluate(f"""
            () => {{
                const elements = document.querySelectorAll('{selector}');
                const results = [];
                elements.forEach(el => {{
                    if (el.tagName === 'A') {{
                        results.push({{
                            text: el.innerText.trim().substring(0, 100),
                            href: el.href
                        }});
                    }} else {{
                        el.querySelectorAll('a').forEach(a => {{
                            results.push({{
                                text: a.innerText.trim().substring(0, 100),
                                href: a.href
                            }});
                        }});
                    }}
                }});
                return results.slice(0, 50);  // Limit to 50 links
            }}
        """)
        if not links:
            return "No links found."

        result_lines = [f"Found {len(links)} links:"]
        for link in links:
            text = link.get("text", "").replace("\n", " ")[:80]
            href = link.get("href", "")
            result_lines.append(f"  - [{text}]({href})")

        logger.info("🔗 Extracted %d links", len(links))
        return "\n".join(result_lines)

    return _run_async(_extract_links())


@tool
def extract_table_data(selector: str = "table", page=None) -> str:
    """Extract data from an HTML table into a structured text format.

    Args:
        selector: CSS selector for the table element. Default: 'table'.
        page: Playwright page instance (injected automatically).
    """
    async def _extract_table():
        table_data = await page.evaluate(f"""
            () => {{
                const table = document.querySelector('{selector}');
                if (!table) return null;
                const rows = [];
                table.querySelectorAll('tr').forEach(tr => {{
                    const cells = [];
                    tr.querySelectorAll('th, td').forEach(cell => {{
                        cells.push(cell.innerText.trim());
                    }});
                    if (cells.length > 0) rows.push(cells);
                }});
                return rows;
            }}
        """)

        if not table_data:
            return f"No table found matching selector: '{selector}'"

        # Format as pipe-separated table
        result_lines = []
        for i, row in enumerate(table_data[:50]):  # Limit rows
            result_lines.append(" | ".join(str(cell)[:50] for cell in row))
            if i == 0:
                result_lines.append(" | ".join("---" for _ in row))

        logger.info("📊 Extracted table with %d rows", len(table_data))
        return "\n".join(result_lines)

    return _run_async(_extract_table())


@tool
def get_page_title(page=None) -> str:
    """Get the title of the current page.

    Args:
        page: Playwright page instance (injected automatically).
    """
    async def _title():
        title = await page.title()
        logger.info("📄 Page title: %s", title)
        return f"Page title: '{title}'"

    return _run_async(_title())


@tool
def get_current_url(page=None) -> str:
    """Get the current URL of the browser.

    Args:
        page: Playwright page instance (injected automatically).
    """
    url = page.url
    logger.info("🔗 Current URL: %s", url)
    return f"Current URL: {url}"
