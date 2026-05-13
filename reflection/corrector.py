"""
Strategy Corrector
==================
Given a failure analysis, generates concrete alternative actions
the agent can try to recover from the error.
"""

import logging
from dataclasses import dataclass
from typing import Optional

from reflection.analyzer import FailureAnalysis

logger = logging.getLogger("browser_agent.reflection.corrector")


@dataclass
class CorrectionStrategy:
    """A concrete correction action for the agent to attempt."""
    description: str
    action: str
    args: dict
    confidence: str


class StrategyCorrector:
    """
    Translates a FailureAnalysis into actionable correction strategies.
    Uses a rule-based approach for common failure patterns,
    falling back to the LLM-suggested strategy.
    """

    # Common failure patterns and their corrections
    PATTERN_CORRECTIONS = {
        "element not found": [
            "Try using a text-based selector (text='{text}')",
            "Try using a more general CSS selector",
            "Scroll the page to reveal the element",
            "Wait for the element to appear with a longer timeout",
        ],
        "timeout": [
            "Increase the timeout duration",
            "Wait for the page to fully load",
            "Refresh the page and try again",
        ],
        "not clickable": [
            "Scroll the element into view first",
            "Close any overlay/modal blocking the element",
            "Try clicking with JavaScript instead",
        ],
        "navigation": [
            "Check if the URL is correct",
            "Try an alternative URL",
            "Clear cookies and retry",
        ],
    }

    def generate_corrections(
        self,
        analysis: FailureAnalysis,
        max_strategies: int = 3,
    ) -> list[CorrectionStrategy]:
        """
        Generate correction strategies based on the failure analysis.

        Args:
            analysis:        The FailureAnalysis from the analyzer.
            max_strategies:  Maximum number of strategies to return.

        Returns:
            List of CorrectionStrategy objects ordered by confidence.
        """
        strategies = []

        # 1. Use the LLM-suggested correction (highest priority)
        strategies.append(
            CorrectionStrategy(
                description=analysis.correction_strategy,
                action="llm_suggested",
                args={},
                confidence=analysis.confidence,
            )
        )

        # 2. Check pattern-based corrections
        root_cause_lower = analysis.root_cause.lower()
        for pattern, corrections in self.PATTERN_CORRECTIONS.items():
            if pattern in root_cause_lower:
                for correction in corrections[:max_strategies - 1]:
                    strategies.append(
                        CorrectionStrategy(
                            description=correction,
                            action="pattern_based",
                            args={"pattern": pattern},
                            confidence="medium",
                        )
                    )
                break

        # 3. If alternative selector was suggested, add it
        if analysis.alternative_selector:
            strategies.insert(1, CorrectionStrategy(
                description=f"Use alternative selector: {analysis.alternative_selector}",
                action="alternative_selector",
                args={"selector": analysis.alternative_selector},
                confidence="high",
            ))

        logger.info("🛠️ Generated %d correction strategies", len(strategies))
        return strategies[:max_strategies]

    def get_best_correction(self, analysis: FailureAnalysis) -> CorrectionStrategy:
        """
        Return the single best correction strategy.

        Args:
            analysis: The FailureAnalysis from the analyzer.

        Returns:
            The highest-confidence CorrectionStrategy.
        """
        strategies = self.generate_corrections(analysis, max_strategies=1)
        return strategies[0]
