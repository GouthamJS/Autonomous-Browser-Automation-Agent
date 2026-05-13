"""
Failure Analyzer
================
Analyses why a browser action failed and determines the root cause.
Uses the LLM to reason about the failure in the context of the current
page state and action history.
"""

import json
import logging
from dataclasses import dataclass
from typing import Optional

from langchain_core.messages import SystemMessage
from langchain_groq import ChatGroq

from agent.prompts import REFLECTION_SYSTEM_PROMPT
from config.settings import settings

logger = logging.getLogger("browser_agent.reflection.analyzer")


@dataclass
class FailureAnalysis:
    """Structured result of a failure analysis."""
    root_cause: str
    correction_strategy: str
    confidence: str  # "high", "medium", "low"
    should_replan: bool
    alternative_selector: Optional[str] = None


class FailureAnalyzer:
    """
    Analyses failed browser actions and produces structured diagnoses
    to guide the correction/retry logic.
    """

    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.model_name,
            temperature=0.3,
            max_tokens=settings.max_tokens,
        )

    def analyze(
        self,
        failed_action: str,
        error_message: str,
        current_url: str = "",
        page_content: str = "",
        retry_count: int = 0,
    ) -> FailureAnalysis:
        """
        Analyse a failed action and produce a structured diagnosis.

        Args:
            failed_action:  Description of the action that failed.
            error_message:  The error/exception message.
            current_url:    Current browser URL.
            page_content:   Trimmed page text for context.
            retry_count:    How many times this action has been retried.

        Returns:
            FailureAnalysis with root cause, strategy, and confidence.
        """
        logger.info("🔍 Analysing failure: %s", failed_action[:100])

        prompt = REFLECTION_SYSTEM_PROMPT.format(
            failed_action=failed_action,
            error_message=error_message,
            current_url=current_url or "unknown",
            page_content=page_content[:2000] if page_content else "No content",
            retry_count=retry_count,
            retry_limit=settings.retry_limit,
        )

        response = self.llm.invoke([SystemMessage(content=prompt)])
        content = response.content.strip()

        analysis = self._parse_analysis(content)

        # Force replan if retries exhausted
        if retry_count >= settings.retry_limit:
            analysis.should_replan = True

        logger.info(
            "🔍 Analysis: cause=%s, confidence=%s, replan=%s",
            analysis.root_cause[:80],
            analysis.confidence,
            analysis.should_replan,
        )

        return analysis

    @staticmethod
    def _parse_analysis(content: str) -> FailureAnalysis:
        """Parse LLM response into a FailureAnalysis object."""
        try:
            if "```" in content:
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            data = json.loads(content)
            return FailureAnalysis(
                root_cause=data.get("root_cause", "Unknown"),
                correction_strategy=data.get("correction_strategy", "Retry with different approach"),
                confidence=data.get("confidence", "low"),
                should_replan=data.get("should_replan", False),
                alternative_selector=data.get("alternative_selector"),
            )
        except (json.JSONDecodeError, IndexError, KeyError):
            return FailureAnalysis(
                root_cause=content[:200] if content else "Analysis failed",
                correction_strategy="Try an alternative approach",
                confidence="low",
                should_replan=False,
            )
