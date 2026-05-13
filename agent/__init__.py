"""
Agent package — Core LangGraph-based autonomous browser agent.

Exports:
    create_agent_graph : Build and return the compiled agent graph.
    AgentState         : The shared state schema for the graph.
"""

from agent.graph import create_agent_graph
from agent.state import AgentState

__all__ = ["create_agent_graph", "AgentState"]
