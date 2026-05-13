"""
Graph Edge Functions
====================
Conditional edge functions that control the routing between nodes
in the LangGraph state graph.
"""

import logging
from langchain_core.messages import AIMessage

from config.settings import settings

logger = logging.getLogger("browser_agent.edges")


def should_continue(state: dict) -> str:
    """
    Main routing function after the agent node.
    Determines whether to:
      - execute a tool  → "tools"
      - finish          → "final_output"
      - stop (max iter) → "final_output"

    Returns:
        The name of the next node to execute.
    """
    # Check iteration limit
    if state.get("iteration_count", 0) >= settings.max_iterations:
        logger.warning(
            "⚠️ Max iterations (%d) reached — terminating",
            settings.max_iterations,
        )
        return "final_output"

    # Check the last message for tool calls
    last_message = state["messages"][-1] if state["messages"] else None

    if last_message is None:
        return "final_output"

    # If the LLM made a tool call, route to the tool node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # If the LLM responded with text (no tool call), it's done
    if isinstance(last_message, AIMessage) and last_message.content:
        content_lower = last_message.content.lower()
        # Check for explicit completion signals
        completion_signals = [
            "task complete",
            "goal achieved",
            "successfully completed",
            "here is the final",
            "final answer",
            "task accomplished",
        ]
        if any(signal in content_lower for signal in completion_signals):
            logger.info("✅ Agent signalled task completion")
            return "final_output"

    # If there's text but no clear completion, let the agent continue
    # (it might need another iteration)
    return "final_output"


def route_after_tool(state: dict) -> str:
    """
    Routing function after tool execution.
    Determines whether to:
      - reflect on errors → "reflection"
      - continue reasoning → "agent"
      - finish             → "final_output"

    Returns:
        The name of the next node to execute.
    """
    # Check iteration limit
    if state.get("iteration_count", 0) >= settings.max_iterations:
        logger.warning("⚠️ Max iterations reached after tool — terminating")
        return "final_output"

    # If there was an error, route to reflection
    if state.get("status") == "reflecting":
        logger.info("🔍 Error detected — routing to reflection")
        return "reflection"

    # Otherwise, continue the reasoning loop
    return "agent"


def route_after_reflection(state: dict) -> str:
    """
    Routing function after the reflection node.
    Determines whether to:
      - replan    → "replan"
      - retry     → "agent"
      - give up   → "final_output"

    Returns:
        The name of the next node to execute.
    """
    status = state.get("status", "running")

    if status == "replanning":
        logger.info("🔄 Routing to replanner")
        return "replan"

    if state.get("retry_count", 0) >= settings.retry_limit:
        logger.warning("❌ Retry limit exceeded — terminating")
        return "final_output"

    # Retry the action
    logger.info("🔁 Retrying with corrected strategy")
    return "agent"


def route_after_replan(state: dict) -> str:
    """
    After replanning, always go back to the agent node.

    Returns:
        Always "agent".
    """
    return "agent"
