"""
Validation Agents (Phase 3)
===========================

HARDCODED validation gates for content quality assurance.
These validators enforce non-negotiable quality standards.
"""

from typing import Any, Dict, List
from pathlib import Path

from .base import Agent


class TruncationValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate no truncated sentences.

    Checks that all content has complete sentences with no
    truncation markers (ellipsis, double dash, incomplete thoughts).
    """

    # Truncation indicators to check for
    TRUNCATION_MARKERS = ['...', '--', '…', '—']

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = self._extract_content(context)

        issues = []
        sentences_checked = 0

        # Split content into sentences
        sentences = content.replace('\n', ' ').replace('  ', ' ').split('.')

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            sentences_checked += 1

            # Check for truncation markers
            for marker in self.TRUNCATION_MARKERS:
                if sentence.endswith(marker):
                    issues.append({
                        "type": "truncation",
                        "position": i,
                        "text": f"{sentence[:50]}..." if len(sentence) > 50 else sentence,
                        "marker": marker
                    })

            # Check for incomplete sentence (ends mid-word)
            if sentence and len(sentence) > 10:
                # Very short last word might indicate truncation
                words = sentence.split()
                if words:
                    last_word = words[-1]
                    if len(last_word) == 1 and last_word not in ['a', 'I']:
                        issues.append({
                            "type": "possible_truncation",
                            "position": i,
                            "text": f"{sentence[:50]}...",
                            "reason": "Single character ending"
                        })

        passed = len(issues) == 0

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "truncation",
            "passed": passed,
            "issues": issues,
            "sentences_checked": sentences_checked,
            "score": 100 if passed else max(0, 100 - (len(issues) * 10))
        }

    def _extract_content(self, context: Dict) -> str:
        """Extract text content from various context formats."""
        content = context.get('content', '')

        if isinstance(content, dict):
            # Try to get text from common keys
            for key in ['text', 'presenter_notes', 'body', 'description']:
                if key in content:
                    return str(content[key])
            return str(content)

        # Also check for lesson_context presenter notes
        lesson_ctx = context.get('lesson_context')
        if lesson_ctx:
            notes = context.get('presenter_notes_writer_output', {})
            if notes:
                return notes.get('presenter_notes', str(content))

        return str(content)


class ElaborationValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate professional elaboration depth.

    Ensures content meets minimum quality standards for:
    - Depth (word count relative to target)
    - Examples (illustrative content)
    - Procedure (step-by-step clarity)
    - Tone (professional language)
    - Connections (logical flow)

    THRESHOLD: 85/100 minimum score
    """

    # Hardcoded threshold - DO NOT MODIFY
    THRESHOLD = 85

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = self._extract_content(context)
        target_words = context.get('target_words', 2000)

        # Calculate elaboration scores
        scores = self._calculate_scores(content, target_words)

        # Calculate weighted total
        # Weights: Depth 30%, Examples 20%, Procedure 20%, Tone 15%, Connections 15%
        total_score = (
            scores["depth"] * 0.30 +
            scores["examples"] * 0.20 +
            scores["procedure"] * 0.20 +
            scores["tone"] * 0.15 +
            scores["connections"] * 0.15
        )

        passed = total_score >= self.THRESHOLD

        # Generate feedback for low scores
        feedback = self._generate_feedback(scores)

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "elaboration",
            "passed": passed,
            "total_score": round(total_score, 1),
            "threshold": self.THRESHOLD,
            "category_scores": scores,
            "word_count": len(content.split()),
            "feedback": feedback if not passed else [],
            "retry_strategy": "ENRICHMENT_PASS" if not passed else None
        }

    def _extract_content(self, context: Dict) -> str:
        """Extract text content from context."""
        content = context.get('content', '')
        if isinstance(content, dict):
            return str(content)

        # Check presenter notes
        notes = context.get('presenter_notes_writer_output', {})
        if notes:
            return notes.get('presenter_notes', str(content))

        return str(content)

    def _calculate_scores(self, content: str, target_words: int) -> Dict[str, float]:
        """Calculate individual category scores."""
        content_lower = content.lower()
        word_count = len(content.split())

        return {
            "depth": min(100, (word_count / target_words) * 100),
            "examples": self._score_examples(content_lower),
            "procedure": self._score_procedure(content_lower),
            "tone": self._score_tone(content_lower),
            "connections": self._score_connections(content_lower)
        }

    def _score_examples(self, content: str) -> float:
        """Score based on presence of examples."""
        example_indicators = [
            "example", "for instance", "such as", "like when",
            "consider", "imagine", "suppose", "let's say"
        ]
        count = sum(1 for ind in example_indicators if ind in content)
        return min(100, count * 25)  # 4+ examples = 100

    def _score_procedure(self, content: str) -> float:
        """Score based on procedural clarity."""
        procedure_indicators = [
            "first", "then", "next", "finally", "step",
            "begin by", "start with", "after that", "following this"
        ]
        count = sum(1 for ind in procedure_indicators if ind in content)
        return min(100, count * 20)  # 5+ = 100

    def _score_tone(self, content: str) -> float:
        """Score based on professional tone."""
        informal_words = [
            "gonna", "wanna", "kinda", "sorta", "gotta",
            "yeah", "nope", "ok", "okay cool"
        ]
        informal_count = sum(1 for word in informal_words if word in content)
        return max(0, 100 - (informal_count * 15))

    def _score_connections(self, content: str) -> float:
        """Score based on logical connections."""
        connection_words = [
            "because", "therefore", "thus", "consequently",
            "as a result", "this means", "in other words", "similarly"
        ]
        count = sum(1 for word in connection_words if word in content)
        return min(100, count * 20)  # 5+ = 100

    def _generate_feedback(self, scores: Dict[str, float]) -> List[str]:
        """Generate actionable feedback for low scores."""
        feedback = []

        if scores["depth"] < 80:
            feedback.append("Add more detail and explanation to increase content depth")
        if scores["examples"] < 80:
            feedback.append("Include more concrete examples to illustrate concepts")
        if scores["procedure"] < 80:
            feedback.append("Add step-by-step language for clearer progression")
        if scores["tone"] < 80:
            feedback.append("Replace informal language with professional phrasing")
        if scores["connections"] < 80:
            feedback.append("Add transition words to improve logical flow")

        return feedback


class TimingValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate content fits timing constraints.

    Ensures presenter notes fit within the 15-minute lecture window
    based on speaking rate of 130-150 WPM.

    THRESHOLDS:
    - Duration: 14-16 minutes (within 1 minute of target)
    - Word count: 1,950-2,250 words
    """

    # Hardcoded thresholds - DO NOT MODIFY
    MIN_DURATION_MINUTES = 14
    MAX_DURATION_MINUTES = 16
    MIN_WORDS = 1950
    MAX_WORDS = 2250
    SPEAKING_RATE_WPM = 140

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Get presenter notes
        presenter_notes = context.get('presenter_notes', '')
        if not presenter_notes:
            notes_output = context.get('presenter_notes_writer_output', {})
            presenter_notes = notes_output.get('presenter_notes', '')

        word_count = len(presenter_notes.split())
        estimated_minutes = word_count / self.SPEAKING_RATE_WPM

        # Check thresholds
        duration_ok = self.MIN_DURATION_MINUTES <= estimated_minutes <= self.MAX_DURATION_MINUTES
        word_count_ok = self.MIN_WORDS <= word_count <= self.MAX_WORDS

        passed = duration_ok and word_count_ok

        # Determine adjustment needed
        adjustment = None
        if word_count < self.MIN_WORDS:
            adjustment = f"Add approximately {self.MIN_WORDS - word_count} words"
        elif word_count > self.MAX_WORDS:
            adjustment = f"Remove approximately {word_count - self.MAX_WORDS} words"

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "timing",
            "passed": passed,
            "word_count": word_count,
            "estimated_minutes": round(estimated_minutes, 1),
            "target_minutes": 15,
            "acceptable_range_minutes": f"{self.MIN_DURATION_MINUTES}-{self.MAX_DURATION_MINUTES}",
            "acceptable_range_words": f"{self.MIN_WORDS}-{self.MAX_WORDS}",
            "adjustment_needed": adjustment,
            "retry_strategy": "ADJUSTMENT_PASS" if not passed else None
        }


class StructureValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate all lesson components present.

    Ensures the lesson package contains all required components
    with proper structure and formatting.
    """

    # Required components - DO NOT MODIFY
    REQUIRED_COMPONENTS = [
        "learning_objectives",
        "vocabulary",
        "warmup",
        "content_points",
        "activity",
        "journal_prompt",
        "exit_tickets",
        "materials_list"
    ]

    # Component to agent output mapping
    COMPONENT_AGENT_MAP = {
        "warmup": "warmup_generator",
        "activity": "activity_generator",
        "journal_prompt": "journal_exit_generator",
        "exit_tickets": "journal_exit_generator"
    }

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        daily_input = context.get('daily_input', {})
        previous_outputs = context.get('previous_outputs', {})

        present = []
        missing = []

        for component in self.REQUIRED_COMPONENTS:
            value = None

            # Check lesson_context first
            if lesson_ctx:
                value = getattr(lesson_ctx, component, None)

            # Check daily_input (orchestrator format)
            if not value and component in daily_input:
                value = daily_input.get(component)

            # Check direct context keys
            if not value:
                value = context.get(component)

            # Check previous_outputs for generated components
            if not value:
                agent_name = self.COMPONENT_AGENT_MAP.get(component)
                if agent_name and agent_name in previous_outputs:
                    agent_output = previous_outputs[agent_name]
                    if component == "warmup":
                        value = agent_output.get('warmup')
                    elif component == "activity":
                        value = agent_output.get('activity')
                    elif component == "journal_prompt":
                        journal = agent_output.get('journal', {})
                        value = journal.get('prompt') if isinstance(journal, dict) else journal
                    elif component == "exit_tickets":
                        tickets = agent_output.get('exit_tickets', {})
                        value = tickets.get('questions') if isinstance(tickets, dict) else tickets

            # Check {component}_output style
            if not value:
                output_key = f"{component}_output"
                if output_key in context:
                    value = context[output_key]

            if value:
                present.append(component)
            else:
                missing.append(component)

        passed = len(missing) == 0
        completeness = round(len(present) / len(self.REQUIRED_COMPONENTS) * 100, 1)

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "structure",
            "passed": passed,
            "components_present": present,
            "components_missing": missing,
            "completeness_percentage": completeness,
            "retry_strategy": "COMPONENT_REGEN" if not passed else None,
            "missing_components": missing
        }
