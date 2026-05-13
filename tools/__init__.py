"""
Browser Tools Package
=====================
Exposes all Playwright-based browser automation tools as LangChain-compatible
tool functions that can be bound to the agent's LLM.

Usage:
    from tools import get_all_tools, get_tool_map
    tools = get_all_tools()         # LangChain Tool list for LLM binding
    tool_map = get_tool_map()       # name → callable dict for execution
"""

from langchain_core.tools import tool as langchain_tool
from tools.navigation import navigate_to_url, go_back, go_forward, refresh_page
from tools.interaction import click_element, type_text, select_dropdown, scroll_page, press_key
from tools.extraction import (
    extract_text,
    extract_all_text,
    extract_links,
    extract_table_data,
    get_page_title,
    get_current_url,
)
from tools.screenshot import take_screenshot
from tools.validation import wait_for_element, check_element_exists


# All tool functions in registration order
_ALL_TOOL_FUNCTIONS = [
    # Navigation
    navigate_to_url,
    go_back,
    go_forward,
    refresh_page,
    # Interaction
    click_element,
    type_text,
    select_dropdown,
    scroll_page,
    press_key,
    # Extraction
    extract_text,
    extract_all_text,
    extract_links,
    extract_table_data,
    get_page_title,
    get_current_url,
    # Observation
    take_screenshot,
    wait_for_element,
    check_element_exists,
]


def get_all_tools() -> list:
    """Return list of LangChain Tool objects for LLM binding."""
    return _ALL_TOOL_FUNCTIONS


def get_tool_map() -> dict:
    """Return a dict mapping tool name → callable for tool execution."""
    return {fn.name: fn for fn in _ALL_TOOL_FUNCTIONS}


__all__ = ["get_all_tools", "get_tool_map"]
