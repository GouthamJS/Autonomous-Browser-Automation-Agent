"""
Agent State Schema
==================
Defines the TypedDict that flows through every node in the LangGraph graph.
Uses Annotated reducers so that list fields are *appended to* rather than overwritten.
"""

from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


def _append_list(existing: list, new: list) -> list:
    """Reducer that appends new items to the existing list."""
    return existing + new


class AgentState(TypedDict):
    """
    Shared state that travels through the LangGraph graph.

    Attributes
    ----------
    messages : list[BaseMessage]
        Full conversation / reasoning history (uses add_messages reducer).
    current_url : str
        The URL the browser is currently on.
    page_content : str
        Extracted text content of the current page (trimmed).
    plan : list[str]
        Ordered list of sub-task descriptions for the current goal.
    plan_index : int
        Index of the current step being executed in the plan.
    screenshots : list[str]
        File paths to captured screenshots (appended via reducer).
    memory_context : list[str]
        Relevant memories retrieved from long-term storage.
    iteration_count : int
        Number of ReAct loop iterations executed so far.
    error_log : list[str]
        Log of errors encountered during execution (appended via reducer).
    retry_count : int
        Number of retries attempted for the current action.
    final_output : str
        The final result / answer produced by the agent.
    goal : str
        The original user goal / task description.
    status : str
        Current agent status: "running", "success", "failed", "reflecting".
    """

    messages: Annotated[list[BaseMessage], add_messages]
    current_url: str
    page_content: str
    plan: list[str]
    plan_index: int
    screenshots: Annotated[list[str], _append_list]
    memory_context: list[str]
    iteration_count: int
    error_log: Annotated[list[str], _append_list]
    retry_count: int
    final_output: str
    goal: str
    status: str


def create_initial_state(goal: str) -> dict:
    """
    Create a fresh initial state for a new agent run.

    Args:
        goal: The user's natural-language task description.

    Returns:
        A dictionary compatible with AgentState.
    """
    return {
        "messages": [],
        "current_url": "",
        "page_content": "",
        "plan": [],
        "plan_index": 0,
        "screenshots": [],
        "memory_context": [],
        "iteration_count": 0,
        "error_log": [],
        "retry_count": 0,
        "final_output": "",
        "goal": goal,
        "status": "running",
    }
