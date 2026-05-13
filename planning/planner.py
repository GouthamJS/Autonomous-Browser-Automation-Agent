"""
Task Planner
============
Decomposes a high-level user goal into an ordered list of concrete,
actionable browser automation steps using LLM reasoning.
"""

import json
import logging
from typing import Optional

from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from agent.prompts import PLANNER_SYSTEM_PROMPT
from config.settings import settings

logger = logging.getLogger("browser_agent.planning.planner")


class TaskPlanner:
    """
    Uses an LLM to break down a user goal into executable sub-tasks.
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.model_name,
            temperature=0.2,
            max_tokens=settings.max_tokens,
        )

    def create_plan(
        self,
        goal: str,
        memory_context: Optional[list[str]] = None,
    ) -> list[str]:
        """
        Generate a step-by-step plan for achieving the given goal.

        Args:
            goal:           Natural-language description of the user's objective.
            memory_context: Optional list of relevant past memories to inform planning.

        Returns:
            Ordered list of step descriptions.
        """
        logger.info("📋 Creating plan for goal: %s", goal[:100])

        prompt = PLANNER_SYSTEM_PROMPT.format(
            goal=goal,
            memory_context="\n".join(memory_context) if memory_context else "None",
        )

        response = self.llm.invoke([SystemMessage(content=prompt)])
        content = response.content.strip()

        plan = self._parse_plan(content)

        logger.info("📋 Plan created with %d steps", len(plan))
        for i, step in enumerate(plan, 1):
            logger.info("   Step %d: %s", i, step)

        return plan

    @staticmethod
    def _parse_plan(content: str) -> list[str]:
        """Parse the LLM response into a list of plan steps."""
        # Try JSON parsing first
        try:
            # Handle markdown code fences
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            plan = json.loads(content)
            if isinstance(plan, list):
                return [str(step) for step in plan]
        except (json.JSONDecodeError, IndexError):
            pass

        # Fallback: line-by-line parsing
        lines = content.strip().split("\n")
        plan = []
        for line in lines:
            line = line.strip()
            # Remove numbering and bullet points
            for prefix in ["- ", "* ", "• "]:
                if line.startswith(prefix):
                    line = line[len(prefix):]
            # Remove "1. ", "2. ", etc.
            if len(line) > 2 and line[0].isdigit() and line[1] in ".) ":
                line = line[2:].strip()
            elif len(line) > 3 and line[:2].isdigit() and line[2] in ".) ":
                line = line[3:].strip()
            if line:
                plan.append(line)

        return plan if plan else ["Execute the goal directly"]
