"""
Agent Graph Builder
===================
Constructs and compiles the LangGraph StateGraph that wires together
all nodes and conditional edges into the complete agent workflow.

Flow:
    START → plan → agent ⇄ tools → (reflection → replan) → agent → … → final_output → END
"""

import logging
from functools import partial
from typing import Any

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agent.state import AgentState
from agent.nodes import (
    plan_node,
    agent_node,
    tool_node,
    reflection_node,
    replan_node,
    final_output_node,
)
from agent.edges import (
    should_continue,
    route_after_tool,
    route_after_reflection,
    route_after_replan,
)

logger = logging.getLogger("browser_agent.graph")


def create_agent_graph(
    tools: list,
    tool_map: dict[str, Any],
    page=None,
) -> Any:
    """
    Build and compile the full agent graph.

    Args:
        tools:    List of LangChain Tool objects to bind to the LLM.
        tool_map: Dict mapping tool name → callable for execution.
        page:     Playwright Page object for browser interaction.

    Returns:
        A compiled LangGraph runnable (with MemorySaver checkpointer).
    """
    logger.info("🏗️  Building agent graph …")

    # ── Create partial node functions with injected dependencies ───────
    _agent_node = partial(agent_node, tools=tools)
    _tool_node = partial(tool_node, tool_map=tool_map, page=page)

    # ── Build the graph ───────────────────────────────────────────────
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("plan", plan_node)
    workflow.add_node("agent", _agent_node)
    workflow.add_node("tools", _tool_node)
    workflow.add_node("reflection", reflection_node)
    workflow.add_node("replan", replan_node)
    workflow.add_node("final_output", final_output_node)

    # ── Wire edges ────────────────────────────────────────────────────

    # Entry point: always start with planning
    workflow.set_entry_point("plan")

    # After planning, go to the agent
    workflow.add_edge("plan", "agent")

    # After agent reasoning, decide: use tool, or finish
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "final_output": "final_output",
        },
    )

    # After tool execution, decide: reflect on error, continue, or finish
    workflow.add_conditional_edges(
        "tools",
        route_after_tool,
        {
            "reflection": "reflection",
            "agent": "agent",
            "final_output": "final_output",
        },
    )

    # After reflection, decide: replan, retry, or give up
    workflow.add_conditional_edges(
        "reflection",
        route_after_reflection,
        {
            "replan": "replan",
            "agent": "agent",
            "final_output": "final_output",
        },
    )

    # After replanning, always go back to agent
    workflow.add_conditional_edges(
        "replan",
        route_after_replan,
        {
            "agent": "agent",
        },
    )

    # Final output ends the graph
    workflow.add_edge("final_output", END)

    # ── Compile with checkpointer ─────────────────────────────────────
    checkpointer = MemorySaver()
    compiled = workflow.compile(checkpointer=checkpointer)

    logger.info("✅ Agent graph compiled successfully")
    return compiled
