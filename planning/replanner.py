"""
Task Replanner
==============
Dynamically adjusts the execution plan when the current approach fails
or when new information changes the optimal path.
"""

import json
import logging
from typing import Optional

from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from agent.prompts import REPLANNER_SYSTEM_PROMPT
from config.settings import settings

logger = logging.getLogger("browser_agent.planning.replanner")


class TaskReplanner:
    """
    Revises an existing plan based on errors or new observations.
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.model_name,
            temperature=0.3,
            max_tokens=settings.max_tokens,
        )

    def replan(
        self,
        goal: str,
        current_plan: list[str],
        completed_steps: int,
        error: str,
        current_url: str = "",
        page_content: str = "",
    ) -> list[str]:
        """
        Generate a revised plan that works around the encountered error.

        Args:
            goal:            Original user goal.
            current_plan:    The original step list.
            completed_steps: Number of steps already completed.
            error:           Description of the error encountered.
            current_url:     The URL the browser is currently on.
            page_content:    Trimmed text content of the current page.

        Returns:
            Updated list of plan steps.
        """
        logger.info("🔄 Replanning after error at step %d: %s", completed_steps + 1, error[:100])

        prompt = REPLANNER_SYSTEM_PROMPT.format(
            goal=goal,
            plan="\n".join(f"  {i+1}. {s}" for i, s in enumerate(current_plan)),
            plan_index=completed_steps,
            current_url=current_url or "unknown",
            error=error,
            page_content=page_content[:2000] if page_content else "No content",
        )

        response = self.llm.invoke([SystemMessage(content=prompt)])
        content = response.content.strip()

        new_plan = self._parse_revised_plan(content, current_plan)

        logger.info("🔄 Revised plan has %d steps", len(new_plan))
        for i, step in enumerate(new_plan, 1):
            logger.info("   Step %d: %s", i, step)

        return new_plan

    @staticmethod
    def _parse_revised_plan(content: str, fallback_plan: list[str]) -> list[str]:
        """Parse the LLM response, falling back to the original plan if parsing fails."""
        try:
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            plan = json.loads(content)
            if isinstance(plan, list) and len(plan) > 0:
                return [str(step) for step in plan]
        except (json.JSONDecodeError, IndexError):
            pass

        # Fallback: line-by-line
        lines = content.strip().split("\n")
        plan = []
        for line in lines:
            line = line.strip()
            for prefix in ["- ", "* ", "• "]:
                if line.startswith(prefix):
                    line = line[len(prefix):]
            if len(line) > 2 and line[0].isdigit() and line[1] in ".) ":
                line = line[2:].strip()
            if line:
                plan.append(line)

        return plan if plan else fallback_plan
