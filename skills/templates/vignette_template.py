"""
Vignette Template and Structure Enforcer
Ensures vignettes have proper NCLEX-style structure.

Usage:
    from skills.templates.vignette_template import (
        VignetteTemplate, enforce_vignette_structure, validate_vignette
    )
    vignette = VignetteTemplate(stem, options, correct_answer)
    body = vignette.render()
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class VignetteTemplate:
    """
    Structured vignette representation.

    Ensures:
    - Stem is 2-4 sentences
    - Exactly 4 options (A, B, C, D)
    - One correct answer marked
    """
    stem: str
    options: Dict[str, str]  # {'A': 'text', 'B': 'text', ...}
    correct_answer: str  # 'A', 'B', 'C', or 'D'
    scenario_type: str = "general"  # general, priority, delegation, etc.

    def __post_init__(self):
        # Normalize correct answer
        self.correct_answer = self.correct_answer.upper().strip()
        if self.correct_answer not in ['A', 'B', 'C', 'D']:
            raise ValueError(f"Invalid correct answer: {self.correct_answer}")

        # Ensure all 4 options exist
        for opt in ['A', 'B', 'C', 'D']:
            if opt not in self.options:
                self.options[opt] = f"[Option {opt} missing]"

    def count_sentences(self) -> int:
        """Count sentences in stem."""
        # Simple sentence counting (. ! ?)
        sentences = re.split(r'[.!?]+', self.stem)
        return len([s for s in sentences if s.strip()])

    def validate(self) -> Dict[str, Any]:
        """Validate vignette structure."""
        issues = []

        # Check stem length
        sentence_count = self.count_sentences()
        if sentence_count < 2:
            issues.append(f"Stem has only {sentence_count} sentences, need at least 2")
        if sentence_count > 4:
            issues.append(f"Stem has {sentence_count} sentences, max is 4")

        # Check options
        for opt in ['A', 'B', 'C', 'D']:
            if opt not in self.options or not self.options[opt].strip():
                issues.append(f"Option {opt} is missing or empty")

        # Check correct answer
        if self.correct_answer not in self.options:
            issues.append(f"Correct answer {self.correct_answer} not in options")

        return {
            'valid': len(issues) == 0,
            'sentence_count': sentence_count,
            'option_count': len([o for o in self.options.values() if o.strip()]),
            'issues': issues
        }

    def render(self) -> str:
        """Render vignette body text."""
        lines = [self.stem, ""]

        for opt in ['A', 'B', 'C', 'D']:
            text = self.options.get(opt, f"[Option {opt}]")
            lines.append(f"{opt}) {text}")

        return '\n'.join(lines)


def parse_vignette_body(body: str) -> Optional[VignetteTemplate]:
    """
    Parse existing vignette body into structured format.

    Args:
        body: Raw vignette body text

    Returns:
        VignetteTemplate if parseable, None otherwise
    """
    # Split into stem and options
    # Look for first option marker
    option_pattern = r'\n\s*[A-D][).\:]'
    match = re.search(option_pattern, body)

    if not match:
        return None

    stem = body[:match.start()].strip()
    options_text = body[match.start():].strip()

    # Parse options
    options = {}
    for opt in ['A', 'B', 'C', 'D']:
        # Try different formats: A) A. A:
        pattern = rf'{opt}\s*[).\:]\s*(.+?)(?=\n\s*[B-D][).\:]|$)'
        opt_match = re.search(pattern, options_text, re.DOTALL | re.IGNORECASE)
        if opt_match:
            options[opt] = opt_match.group(1).strip()

    if len(options) < 4:
        return None

    return VignetteTemplate(
        stem=stem,
        options=options,
        correct_answer='A'  # Will be updated by caller
    )


def enforce_vignette_structure(body: str, correct_answer: str = 'A') -> str:
    """
    Enforce vignette structure, fixing common issues.

    Args:
        body: Raw vignette body
        correct_answer: The correct option letter

    Returns:
        Properly formatted vignette body
    """
    # Try to parse existing
    parsed = parse_vignette_body(body)

    if parsed:
        parsed.correct_answer = correct_answer
        return parsed.render()

    # If parsing fails, attempt to extract what we can
    lines = body.strip().split('\n')
    stem_lines = []
    options = {}

    current_option = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is an option line
        opt_match = re.match(r'^([A-D])\s*[).\:]\s*(.*)$', line, re.IGNORECASE)
        if opt_match:
            current_option = opt_match.group(1).upper()
            options[current_option] = opt_match.group(2)
        elif current_option:
            # Continuation of option
            options[current_option] += ' ' + line
        else:
            # Part of stem
            stem_lines.append(line)

    stem = ' '.join(stem_lines)

    # Ensure we have all options
    for opt in ['A', 'B', 'C', 'D']:
        if opt not in options:
            options[opt] = f"[Missing option {opt}]"

    template = VignetteTemplate(
        stem=stem,
        options=options,
        correct_answer=correct_answer
    )

    return template.render()


def validate_vignette(body: str) -> Dict[str, Any]:
    """
    Validate vignette body meets R10 requirements.

    Returns:
        {
            'valid': bool,
            'has_stem': bool,
            'stem_sentences': int,
            'has_all_options': bool,
            'missing_options': list,
            'issues': list
        }
    """
    issues = []

    # Check for options
    missing_options = []
    for opt in ['A', 'B', 'C', 'D']:
        if f'{opt})' not in body and f'{opt}.' not in body and f'{opt}:' not in body:
            missing_options.append(opt)
            issues.append(f"Missing option {opt})")

    # Check stem
    parsed = parse_vignette_body(body)
    stem_sentences = 0
    if parsed:
        stem_sentences = parsed.count_sentences()
        if stem_sentences < 2:
            issues.append(f"Stem has {stem_sentences} sentences, need 2-4")
        if stem_sentences > 4:
            issues.append(f"Stem has {stem_sentences} sentences, max is 4")

    return {
        'valid': len(issues) == 0,
        'has_stem': stem_sentences > 0,
        'stem_sentences': stem_sentences,
        'has_all_options': len(missing_options) == 0,
        'missing_options': missing_options,
        'issues': issues
    }


# Standard vignette templates by type
VIGNETTE_TEMPLATES = {
    'priority': """
A {age}-year-old {gender} is admitted with {condition}. The nurse assesses {findings}. {additional_context}

Which action should the nurse take first?

A) {option_a}
B) {option_b}
C) {option_c}
D) {option_d}
""",
    'assessment': """
A nurse is caring for a {age}-year-old {patient_type} with {condition}. The patient reports {symptoms}. {vital_signs}

Which assessment finding requires immediate intervention?

A) {option_a}
B) {option_b}
C) {option_c}
D) {option_d}
""",
    'medication': """
A nurse is preparing to administer {medication} {dose} to a {age}-year-old patient. Before administration, the nurse reviews {relevant_info}. {additional_context}

What action should the nurse take?

A) {option_a}
B) {option_b}
C) {option_c}
D) {option_d}
""",
    'delegation': """
A charge nurse is making assignments for the shift. The available staff includes {staff_list}. The patients include {patient_list}.

Which task can the nurse delegate to the UAP?

A) {option_a}
B) {option_b}
C) {option_c}
D) {option_d}
""",
}


if __name__ == "__main__":
    # Test
    test_body = """A nurse is caring for a patient with TB. The patient is in isolation.

A) Surgical mask
B) N95 respirator
C) Gown only"""  # Missing D!

    print("Original:")
    print(test_body)
    print(f"\nValidation: {validate_vignette(test_body)}")

    print("\n\nAfter enforcement:")
    fixed = enforce_vignette_structure(test_body, correct_answer='B')
    print(fixed)
    print(f"\nValidation: {validate_vignette(fixed)}")
