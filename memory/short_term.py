"""
Short-Term Memory
=================
Wraps the LangGraph MemorySaver checkpointer for session-scoped state persistence.
This keeps conversation history and agent state within a single run / thread.
"""

import logging
from functools import lru_cache

from langgraph.checkpoint.memory import MemorySaver

logger = logging.getLogger("browser_agent.memory.short_term")


@lru_cache(maxsize=1)
def get_checkpointer() -> MemorySaver:
    """
    Return a singleton MemorySaver instance.

    The MemorySaver stores graph state in-memory, allowing the agent
    to maintain conversation history and checkpoint/resume within a session.

    For production persistence across restarts, swap this for
    SqliteSaver or PostgresSaver.

    Returns:
        MemorySaver instance.
    """
    logger.info("Initialising short-term memory (MemorySaver)")
    return MemorySaver()
