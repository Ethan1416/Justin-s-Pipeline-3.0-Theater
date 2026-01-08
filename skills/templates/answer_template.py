"""
Answer Slide Template and Structure Enforcer
Ensures answer slides have rationale and distractor analysis.

Usage:
    from skills.templates.answer_template import (
        AnswerTemplate, enforce_answer_structure, validate_answer
    )
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class AnswerTemplate:
    """
    Structured answer slide representation.

    Ensures:
    - Correct answer clearly stated
    - Rationale provided (2-3 sentences)
    - All distractors analyzed
    """
    correct_letter: str
    correct_text: str
    rationale: str
    distractors: Dict[str, str]  # {'A': 'why wrong', 'B': 'why wrong', ...}

    def __post_init__(self):
        self.correct_letter = self.correct_letter.upper().strip()

    def validate(self) -> Dict[str, Any]:
        """Validate answer structure."""
        issues = []

        # Check correct answer
        if not self.correct_letter or self.correct_letter not in ['A', 'B', 'C', 'D']:
            issues.append("Invalid or missing correct answer letter")

        if not self.correct_text or len(self.correct_text.strip()) < 5:
            issues.append("Correct answer text missing or too short")

        # Check rationale
        if not self.rationale or len(self.rationale.strip()) < 20:
            issues.append("Rationale missing or too short")

        # Check distractors
        expected_distractors = [l for l in ['A', 'B', 'C', 'D'] if l != self.correct_letter]
        for letter in expected_distractors:
            if letter not in self.distractors or not self.distractors[letter].strip():
                issues.append(f"Missing distractor analysis for option {letter}")

        return {
            'valid': len(issues) == 0,
            'has_rationale': bool(self.rationale and self.rationale.strip()),
            'distractor_count': len([d for d in self.distractors.values() if d.strip()]),
            'issues': issues
        }

    def render(self) -> str:
        """Render answer body text."""
        lines = [
            f"Correct Answer: {self.correct_letter}) {self.correct_text}",
            "",
            "Rationale:",
            self.rationale,
            "",
            "Why not the others:",
        ]

        for letter in ['A', 'B', 'C', 'D']:
            if letter != self.correct_letter:
                analysis = self.distractors.get(letter, f"[Analysis for {letter} missing]")
                lines.append(f"- {letter}) {analysis}")

        return '\n'.join(lines)


def parse_answer_body(body: str) -> Optional[AnswerTemplate]:
    """
    Parse existing answer body into structured format.

    Args:
        body: Raw answer body text

    Returns:
        AnswerTemplate if parseable, None otherwise
    """
    # Extract correct answer
    correct_match = re.search(
        r'Correct\s*Answer\s*:?\s*([A-D])\s*[).\:]?\s*(.+?)(?=\n|Rationale|$)',
        body, re.IGNORECASE | re.DOTALL
    )

    if not correct_match:
        return None

    correct_letter = correct_match.group(1).upper()
    correct_text = correct_match.group(2).strip()

    # Extract rationale
    rationale = ""
    rationale_match = re.search(
        r'Rationale\s*:?\s*(.+?)(?=Why not|Incorrect|Wrong|$)',
        body, re.IGNORECASE | re.DOTALL
    )
    if rationale_match:
        rationale = rationale_match.group(1).strip()

    # Extract distractors
    distractors = {}
    distractor_section = re.search(
        r'(Why not|Incorrect|Wrong).*?:(.*?)$',
        body, re.IGNORECASE | re.DOTALL
    )

    if distractor_section:
        distractor_text = distractor_section.group(2)
        for letter in ['A', 'B', 'C', 'D']:
            if letter != correct_letter:
                pattern = rf'[-•]?\s*{letter}\s*[).\:]?\s*(.+?)(?=[-•]?\s*[A-D]\s*[).\:]|$)'
                match = re.search(pattern, distractor_text, re.IGNORECASE | re.DOTALL)
                if match:
                    distractors[letter] = match.group(1).strip()

    return AnswerTemplate(
        correct_letter=correct_letter,
        correct_text=correct_text,
        rationale=rationale,
        distractors=distractors
    )


def enforce_answer_structure(
    body: str,
    correct_letter: str,
    correct_text: str = None,
    options: Dict[str, str] = None
) -> str:
    """
    Enforce answer structure, adding missing sections.

    Args:
        body: Raw answer body
        correct_letter: The correct option letter
        correct_text: Full text of correct option (optional)
        options: Dict of all options from vignette (optional)

    Returns:
        Properly formatted answer body
    """
    # Try to parse existing
    parsed = parse_answer_body(body)

    if parsed and parsed.validate()['valid']:
        return parsed.render()

    # Build from what we have
    if parsed:
        correct_letter = parsed.correct_letter
        correct_text = correct_text or parsed.correct_text
        rationale = parsed.rationale or "[Rationale needed]"
        distractors = parsed.distractors
    else:
        rationale = "[Rationale needed]"
        distractors = {}

    # Fill in missing distractors
    for letter in ['A', 'B', 'C', 'D']:
        if letter != correct_letter and letter not in distractors:
            if options and letter in options:
                distractors[letter] = f"Incorrect - {options[letter][:50]}..."
            else:
                distractors[letter] = f"[Analysis for option {letter} needed]"

    template = AnswerTemplate(
        correct_letter=correct_letter,
        correct_text=correct_text or "[Correct answer text]",
        rationale=rationale,
        distractors=distractors
    )

    return template.render()


def validate_answer(body: str) -> Dict[str, Any]:
    """
    Validate answer body meets R11 requirements.

    Returns:
        {
            'valid': bool,
            'has_correct_answer': bool,
            'has_rationale': bool,
            'has_distractor_analysis': bool,
            'issues': list
        }
    """
    issues = []
    body_lower = body.lower()

    # Check for rationale
    has_rationale = 'rationale' in body_lower
    if not has_rationale:
        issues.append("Missing rationale section")

    # Check for distractor analysis
    has_distractor = any(phrase in body_lower for phrase in
                         ['why not', 'incorrect', 'wrong', 'other options'])
    if not has_distractor:
        issues.append("Missing distractor analysis")

    # Check for correct answer
    has_correct = bool(re.search(r'correct\s*answer', body_lower))
    if not has_correct:
        issues.append("Missing correct answer statement")

    return {
        'valid': len(issues) == 0,
        'has_correct_answer': has_correct,
        'has_rationale': has_rationale,
        'has_distractor_analysis': has_distractor,
        'issues': issues
    }


if __name__ == "__main__":
    # Test
    test_body = """Correct Answer: B) N95 respirator

TB requires airborne precautions."""  # Missing rationale label and distractors

    print("Original:")
    print(test_body)
    print(f"\nValidation: {validate_answer(test_body)}")

    print("\n\nAfter enforcement:")
    fixed = enforce_answer_structure(test_body, 'B', 'N95 respirator')
    print(fixed)
    print(f"\nValidation: {validate_answer(fixed)}")
