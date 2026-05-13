"""
Agent Graph Nodes
=================
Each function in this module is a *node* in the LangGraph state graph.
Nodes receive the current AgentState and return a partial state update dict.
"""

import json
import logging
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq

from agent.prompts import (
    AGENT_SYSTEM_PROMPT,
    PLANNER_SYSTEM_PROMPT,
    REPLANNER_SYSTEM_PROMPT,
    REFLECTION_SYSTEM_PROMPT,
    FINAL_ANSWER_PROMPT,
)
from config.settings import settings

logger = logging.getLogger("browser_agent.nodes")


def _get_llm(temperature: float | None = None) -> ChatGroq:
    """Return a configured ChatGroq LLM instance."""
    return ChatGroq(
        api_key=settings.groq_api_key,
        model_name=settings.model_name,
        temperature=temperature if temperature is not None else settings.temperature,
        max_tokens=settings.max_tokens,
    )


# ═══════════════════════════════════════════════════════════════════════
# NODE: Plan — Initial task decomposition
# ═══════════════════════════════════════════════════════════════════════

def plan_node(state: dict) -> dict:
    """
    Decompose the user goal into an ordered list of sub-tasks.
    Called once at the start of every agent run.
    """
    logger.info("📋 Planning: decomposing goal into sub-tasks …")

    llm = _get_llm(temperature=0.2)

    prompt = PLANNER_SYSTEM_PROMPT.format(
        goal=state["goal"],
        memory_context="\n".join(state.get("memory_context", [])) or "None",
    )

    response = llm.invoke([SystemMessage(content=prompt)])
    content = response.content.strip()

    # Parse the JSON array from the LLM response
    try:
        # Handle markdown code fences
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        plan = json.loads(content)
        if not isinstance(plan, list):
            plan = [str(plan)]
    except (json.JSONDecodeError, IndexError):
        # Fallback: split by newlines
        plan = [line.strip("- ").strip() for line in content.split("\n") if line.strip()]

    logger.info("📋 Plan created with %d steps", len(plan))
    for i, step in enumerate(plan, 1):
        logger.info("   Step %d: %s", i, step)

    return {
        "plan": plan,
        "plan_index": 0,
        "status": "running",
        "messages": [
            AIMessage(content=f"Plan created with {len(plan)} steps:\n" +
                      "\n".join(f"  {i+1}. {s}" for i, s in enumerate(plan)))
        ],
    }


# ═══════════════════════════════════════════════════════════════════════
# NODE: Agent — LLM Reasoning (Thought → Action)
# ═══════════════════════════════════════════════════════════════════════

def agent_node(state: dict, tools: list) -> dict:
    """
    Core reasoning node. The LLM analyses the current state and decides
    which tool to call next (or whether the goal is complete).
    """
    logger.info(
        "🧠 Agent reasoning — iteration %d/%d",
        state["iteration_count"] + 1,
        settings.max_iterations,
    )

    llm = _get_llm()
    llm_with_tools = llm.bind_tools(tools)

    # Build the system message with current state
    plan_display = "\n".join(
        f"  {'✅' if i < state['plan_index'] else '➡️' if i == state['plan_index'] else '⬜'} "
        f"{i+1}. {step}"
        for i, step in enumerate(state["plan"])
    ) if state["plan"] else "No plan yet."

    system_msg = AGENT_SYSTEM_PROMPT.format(
        goal=state["goal"],
        current_url=state.get("current_url", "Not navigated yet"),
        plan=plan_display,
        plan_index=state.get("plan_index", 0) + 1,
        iteration_count=state.get("iteration_count", 0) + 1,
        max_iterations=settings.max_iterations,
        page_content=(state.get("page_content", "")[:2000] or "No content extracted yet"),
        memory_context="\n".join(state.get("memory_context", [])) or "None",
    )

    messages = [SystemMessage(content=system_msg)] + state["messages"]

    response = llm_with_tools.invoke(messages)

    logger.info("🧠 Agent response: %s", response.content[:200] if response.content else "[tool call]")

    return {
        "messages": [response],
        "iteration_count": state["iteration_count"] + 1,
    }


# ═══════════════════════════════════════════════════════════════════════
# NODE: Tool Execution — Run the selected browser tool
# ═══════════════════════════════════════════════════════════════════════

def tool_node(state: dict, tool_map: dict[str, Any], page) -> dict:
    """
    Execute the tool call requested by the agent node.
    The last message should be an AIMessage with tool_calls.
    """
    last_message = state["messages"][-1]

    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        logger.warning("⚠️ tool_node called but no tool_calls found on last message")
        return {
            "messages": [AIMessage(content="No tool call was made. Let me reconsider.")],
        }

    results = []
    state_updates: dict = {}

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_id = tool_call["id"]

        logger.info("⚡ Executing tool: %s(%s)", tool_name, tool_args)

        if tool_name not in tool_map:
            error_msg = f"Unknown tool: {tool_name}"
            logger.error(error_msg)
            results.append(ToolMessage(content=error_msg, tool_call_id=tool_id))
            state_updates["error_log"] = [error_msg]
            continue

        try:
            tool_fn = tool_map[tool_name]
            # Pass the Playwright page to the tool
            result = tool_fn(page=page, **tool_args)

            logger.info("✅ Tool result: %s", str(result)[:300])
            results.append(ToolMessage(content=str(result), tool_call_id=tool_id))

            # Update state based on tool type
            if tool_name == "navigate_to_url":
                state_updates["current_url"] = tool_args.get("url", "")
            elif tool_name in ("extract_text", "extract_all_text"):
                state_updates["page_content"] = str(result)[:5000]
            elif tool_name == "take_screenshot":
                state_updates["screenshots"] = [str(result)]
            elif tool_name == "get_current_url":
                state_updates["current_url"] = str(result)

            # Reset retry count on success
            state_updates["retry_count"] = 0

        except Exception as e:
            error_msg = f"Tool '{tool_name}' failed: {type(e).__name__}: {str(e)}"
            logger.error("❌ %s", error_msg)
            results.append(ToolMessage(content=error_msg, tool_call_id=tool_id))
            state_updates["error_log"] = [error_msg]
            state_updates["retry_count"] = state.get("retry_count", 0) + 1
            state_updates["status"] = "reflecting"

    state_updates["messages"] = results
    return state_updates


# ═══════════════════════════════════════════════════════════════════════
# NODE: Reflection — Analyse failures and suggest corrections
# ═══════════════════════════════════════════════════════════════════════

def reflection_node(state: dict) -> dict:
    """
    Analyse the most recent error and produce a correction strategy.
    """
    logger.info("🔍 Reflecting on failure …")

    errors = state.get("error_log", [])
    last_error = errors[-1] if errors else "Unknown error"

    llm = _get_llm(temperature=0.3)

    prompt = REFLECTION_SYSTEM_PROMPT.format(
        failed_action=last_error,
        error_message=last_error,
        current_url=state.get("current_url", "unknown"),
        page_content=(state.get("page_content", "")[:2000] or "No content"),
        retry_count=state.get("retry_count", 0),
        retry_limit=settings.retry_limit,
    )

    response = llm.invoke([SystemMessage(content=prompt)])
    content = response.content.strip()

    logger.info("🔍 Reflection result: %s", content[:300])

    # Try parsing the JSON response
    try:
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        analysis = json.loads(content)
    except (json.JSONDecodeError, IndexError):
        analysis = {
            "root_cause": content,
            "correction_strategy": "Try a different approach",
            "confidence": "low",
            "should_replan": False,
        }

    # Determine next status
    should_replan = analysis.get("should_replan", False)
    if state.get("retry_count", 0) >= settings.retry_limit:
        should_replan = True

    new_status = "running"  # Default: try again
    if should_replan:
        new_status = "replanning"

    reflection_msg = (
        f"🔍 **Reflection Analysis**\n"
        f"- Root Cause: {analysis.get('root_cause', 'unknown')}\n"
        f"- Strategy: {analysis.get('correction_strategy', 'retry')}\n"
        f"- Confidence: {analysis.get('confidence', 'unknown')}\n"
        f"- Retries: {state.get('retry_count', 0)}/{settings.retry_limit}\n"
        f"- Action: {'Replanning' if should_replan else 'Retrying with correction'}"
    )

    return {
        "messages": [AIMessage(content=reflection_msg)],
        "status": new_status,
    }


# ═══════════════════════════════════════════════════════════════════════
# NODE: Replan — Dynamic plan adjustment
# ═══════════════════════════════════════════════════════════════════════

def replan_node(state: dict) -> dict:
    """
    Generate a revised plan when the current approach is unviable.
    """
    logger.info("🔄 Replanning — generating alternative approach …")

    errors = state.get("error_log", [])
    last_error = errors[-1] if errors else "Unknown issue"

    llm = _get_llm(temperature=0.3)

    prompt = REPLANNER_SYSTEM_PROMPT.format(
        goal=state["goal"],
        plan="\n".join(f"  {i+1}. {s}" for i, s in enumerate(state["plan"])),
        plan_index=state.get("plan_index", 0),
        current_url=state.get("current_url", "unknown"),
        error=last_error,
        page_content=(state.get("page_content", "")[:2000] or "No content"),
    )

    response = llm.invoke([SystemMessage(content=prompt)])
    content = response.content.strip()

    # Parse the updated plan
    try:
        if "```" in content:
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        new_plan = json.loads(content)
        if not isinstance(new_plan, list):
            new_plan = state["plan"]  # Keep original if parsing fails
    except (json.JSONDecodeError, IndexError):
        new_plan = [line.strip("- ").strip() for line in content.split("\n") if line.strip()]

    logger.info("🔄 Revised plan with %d steps", len(new_plan))

    return {
        "plan": new_plan,
        "retry_count": 0,
        "status": "running",
        "messages": [
            AIMessage(content=f"🔄 Plan revised. New plan has {len(new_plan)} steps:\n" +
                      "\n".join(f"  {i+1}. {s}" for i, s in enumerate(new_plan)))
        ],
    }


# ═══════════════════════════════════════════════════════════════════════
# NODE: Final Output — Produce the result
# ═══════════════════════════════════════════════════════════════════════

def final_output_node(state: dict) -> dict:
    """
    Generate a clean, structured final answer from the agent's work.
    """
    logger.info("📤 Generating final output …")

    llm = _get_llm()

    # Build action summary from messages
    action_summary = []
    for msg in state["messages"]:
        if isinstance(msg, AIMessage) and msg.content:
            action_summary.append(msg.content[:200])
        elif isinstance(msg, ToolMessage):
            action_summary.append(f"Tool result: {msg.content[:200]}")

    prompt = FINAL_ANSWER_PROMPT.format(
        goal=state["goal"],
        action_summary="\n".join(action_summary[-10:]),  # Last 10 actions
        extracted_data=state.get("page_content", "No data extracted"),
    )

    response = llm.invoke([SystemMessage(content=prompt)])

    logger.info("📤 Final output generated successfully")

    return {
        "final_output": response.content,
        "status": "success",
    }
