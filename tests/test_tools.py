"""
Tool Unit Tests
===============
Tests for browser automation tools.
Uses pytest-asyncio for async tool testing with a mock Playwright page.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# ═══════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_page():
    """Create a mock Playwright Page object."""
    page = AsyncMock()
    page.url = "https://example.com"
    page.title = AsyncMock(return_value="Example Domain")
    page.goto = AsyncMock()
    page.go_back = AsyncMock()
    page.go_forward = AsyncMock()
    page.reload = AsyncMock()
    page.click = AsyncMock()
    page.fill = AsyncMock()
    page.type = AsyncMock()
    page.select_option = AsyncMock()
    page.evaluate = AsyncMock(return_value=None)
    page.keyboard = AsyncMock()
    page.keyboard.press = AsyncMock()
    page.query_selector = AsyncMock()
    page.wait_for_selector = AsyncMock()
    page.wait_for_timeout = AsyncMock()
    page.inner_text = AsyncMock(return_value="Sample page text content")
    page.screenshot = AsyncMock()
    return page


# ═══════════════════════════════════════════════════════════════════════
# Navigation Tool Tests
# ═══════════════════════════════════════════════════════════════════════

class TestNavigationTools:
    """Tests for navigation tools."""

    def test_navigate_to_url(self, mock_page):
        """Test navigating to a URL."""
        from tools.navigation import navigate_to_url
        result = navigate_to_url.invoke({"url": "https://example.com", "page": mock_page})
        assert "Successfully navigated" in result or "example.com" in result.lower()

    def test_go_back(self, mock_page):
        """Test going back."""
        from tools.navigation import go_back
        result = go_back.invoke({"page": mock_page})
        assert "back" in result.lower() or "navigated" in result.lower()

    def test_go_forward(self, mock_page):
        """Test going forward."""
        from tools.navigation import go_forward
        result = go_forward.invoke({"page": mock_page})
        assert "forward" in result.lower() or "navigated" in result.lower()

    def test_refresh_page(self, mock_page):
        """Test refreshing the page."""
        from tools.navigation import refresh_page
        result = refresh_page.invoke({"page": mock_page})
        assert "refresh" in result.lower()


# ═══════════════════════════════════════════════════════════════════════
# Interaction Tool Tests
# ═══════════════════════════════════════════════════════════════════════

class TestInteractionTools:
    """Tests for interaction tools."""

    def test_click_element(self, mock_page):
        """Test clicking an element."""
        from tools.interaction import click_element
        result = click_element.invoke({"selector": "#submit-btn", "page": mock_page})
        assert "clicked" in result.lower() or "successfully" in result.lower()

    def test_type_text(self, mock_page):
        """Test typing text."""
        from tools.interaction import type_text
        result = type_text.invoke({
            "selector": "#search-input",
            "text": "hello world",
            "page": mock_page,
        })
        assert "typed" in result.lower() or "successfully" in result.lower()

    def test_scroll_page(self, mock_page):
        """Test scrolling."""
        from tools.interaction import scroll_page
        result = scroll_page.invoke({"direction": "down", "amount": 500, "page": mock_page})
        assert "scroll" in result.lower()

    def test_press_key(self, mock_page):
        """Test pressing a key."""
        from tools.interaction import press_key
        result = press_key.invoke({"key": "Enter", "page": mock_page})
        assert "pressed" in result.lower() or "enter" in result.lower()


# ═══════════════════════════════════════════════════════════════════════
# Extraction Tool Tests
# ═══════════════════════════════════════════════════════════════════════

class TestExtractionTools:
    """Tests for extraction tools."""

    def test_extract_text(self, mock_page):
        """Test extracting text from an element."""
        mock_element = AsyncMock()
        mock_element.inner_text = AsyncMock(return_value="Hello World")
        mock_page.query_selector = AsyncMock(return_value=mock_element)

        from tools.extraction import extract_text
        result = extract_text.invoke({"selector": "h1", "page": mock_page})
        assert "Hello World" in result or "hello" in result.lower()

    def test_extract_text_not_found(self, mock_page):
        """Test extracting text when element not found."""
        mock_page.query_selector = AsyncMock(return_value=None)

        from tools.extraction import extract_text
        result = extract_text.invoke({"selector": ".nonexistent", "page": mock_page})
        assert "no element" in result.lower() or "not found" in result.lower()

    def test_get_page_title(self, mock_page):
        """Test getting page title."""
        from tools.extraction import get_page_title
        result = get_page_title.invoke({"page": mock_page})
        assert "Example Domain" in result

    def test_get_current_url(self, mock_page):
        """Test getting current URL."""
        from tools.extraction import get_current_url
        result = get_current_url.invoke({"page": mock_page})
        assert "example.com" in result


# ═══════════════════════════════════════════════════════════════════════
# Validation Tool Tests
# ═══════════════════════════════════════════════════════════════════════

class TestValidationTools:
    """Tests for validation tools."""

    def test_check_element_exists_found(self, mock_page):
        """Test checking an element that exists."""
        mock_element = AsyncMock()
        mock_element.is_visible = AsyncMock(return_value=True)
        mock_page.query_selector = AsyncMock(return_value=mock_element)

        from tools.validation import check_element_exists
        result = check_element_exists.invoke({"selector": "#main", "page": mock_page})
        assert "visible" in result.lower() or "exists" in result.lower()

    def test_check_element_exists_not_found(self, mock_page):
        """Test checking an element that doesn't exist."""
        mock_page.query_selector = AsyncMock(return_value=None)

        from tools.validation import check_element_exists
        result = check_element_exists.invoke({"selector": ".missing", "page": mock_page})
        assert "not" in result.lower()


# ═══════════════════════════════════════════════════════════════════════
# Tool Registry Tests
# ═══════════════════════════════════════════════════════════════════════

class TestToolRegistry:
    """Tests for the tool registry."""

    def test_get_all_tools(self):
        """Test that all tools are registered."""
        from tools import get_all_tools
        tools = get_all_tools()
        assert len(tools) >= 17  # We defined 17+ tools
        # Verify each has a name
        for t in tools:
            assert hasattr(t, "name")
            assert t.name

    def test_get_tool_map(self):
        """Test that the tool map has all entries."""
        from tools import get_tool_map
        tool_map = get_tool_map()
        assert isinstance(tool_map, dict)
        assert len(tool_map) >= 17
        # Check key tools exist
        expected_tools = [
            "navigate_to_url",
            "click_element",
            "type_text",
            "extract_text",
            "take_screenshot",
        ]
        for name in expected_tools:
            assert name in tool_map, f"Tool '{name}' missing from tool map"
