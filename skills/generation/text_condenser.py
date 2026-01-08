"""
Text Condenser Skill
Condenses text to fit within character and line limits.

Usage:
    from skills.generation.text_condenser import TextCondenser, condense_text

    condenser = TextCondenser()
    result = condenser.condense(text, max_chars=66, max_lines=8)
    # or
    condensed = condense_text(text, max_lines=8)
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


# Common filler phrases to remove
FILLER_PHRASES = [
    "It is important to note that",
    "It should be noted that",
    "It is worth mentioning that",
    "In other words",
    "Essentially",
    "Basically",
    "Actually",
    "In fact",
    "As a matter of fact",
    "In order to",
    "For the purpose of",
    "With respect to",
    "In terms of",
    "Due to the fact that",
    "As you can see",
    "As mentioned earlier",
    "It goes without saying",
    "Needless to say",
]

# Phrase condensation mappings
CONDENSATION_MAP = {
    "is characterized by": "features",
    "results in the occurrence of": "causes",
    "plays an important role in": "affects",
    "in order to": "to",
    "for the purpose of": "for",
    "with respect to": "regarding",
    "in terms of": "for",
    "due to the fact that": "because",
    "at this point in time": "now",
    "in the event that": "if",
    "is able to": "can",
    "has the ability to": "can",
    "a number of": "several",
    "a large number of": "many",
    "in close proximity to": "near",
    "in the near future": "soon",
    "at the present time": "now",
    "prior to": "before",
    "subsequent to": "after",
    "in spite of the fact that": "although",
    "with the exception of": "except",
    "for the reason that": "because",
}


@dataclass
class CondenseResult:
    """Result of text condensation."""
    original_text: str
    condensed_text: str
    original_lines: int
    condensed_lines: int
    original_chars: int
    condensed_chars: int
    techniques_applied: List[str] = field(default_factory=list)
    removed_content: List[str] = field(default_factory=list)
    was_modified: bool = False
    meets_limits: bool = True


class TextCondenser:
    """Condense text to fit constraints."""

    def __init__(self,
                 remove_fillers: bool = True,
                 apply_phrase_condensation: bool = True,
                 preserve_bullets: bool = True):
        """
        Initialize TextCondenser.

        Args:
            remove_fillers: Remove filler phrases
            apply_phrase_condensation: Apply phrase shortening
            preserve_bullets: Maintain bullet point structure
        """
        self.remove_fillers = remove_fillers
        self.apply_phrase_condensation = apply_phrase_condensation
        self.preserve_bullets = preserve_bullets

    def _remove_filler_phrases(self, text: str) -> Tuple[str, List[str]]:
        """Remove common filler phrases from text."""
        removed = []
        result = text

        for filler in FILLER_PHRASES:
            pattern = re.compile(re.escape(filler), re.IGNORECASE)
            if pattern.search(result):
                result = pattern.sub("", result)
                removed.append(f"Removed: '{filler}'")

        # Clean up double spaces
        result = re.sub(r'\s+', ' ', result)
        result = re.sub(r'\s+([.,;:])', r'\1', result)

        return result.strip(), removed

    def _apply_condensation_map(self, text: str) -> Tuple[str, List[str]]:
        """Apply phrase condensation mappings."""
        changes = []
        result = text

        for long_phrase, short_phrase in CONDENSATION_MAP.items():
            pattern = re.compile(re.escape(long_phrase), re.IGNORECASE)
            if pattern.search(result):
                result = pattern.sub(short_phrase, result)
                changes.append(f"'{long_phrase}' -> '{short_phrase}'")

        return result, changes

    def _condense_bullets(self, text: str, target_lines: int) -> Tuple[str, List[str]]:
        """Condense bullet points to reduce line count."""
        lines = text.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]

        if len(non_empty_lines) <= target_lines:
            return text, []

        changes = []

        # Strategy 1: Combine related sub-bullets
        combined_lines = []
        i = 0
        while i < len(non_empty_lines):
            line = non_empty_lines[i]

            # Check if next lines are sub-bullets
            sub_bullets = []
            j = i + 1
            while j < len(non_empty_lines) and non_empty_lines[j].strip().startswith(('-', '  ')):
                sub_bullets.append(non_empty_lines[j].strip().lstrip('-').strip())
                j += 1

            if sub_bullets and len(combined_lines) + (len(non_empty_lines) - j) + 1 > target_lines:
                # Combine sub-bullets into main bullet
                main_content = line.strip().rstrip(':')
                combined = f"{main_content}: {', '.join(sub_bullets)}"
                combined_lines.append(combined)
                changes.append(f"Combined {len(sub_bullets)} sub-bullets into line")
                i = j
            else:
                combined_lines.append(line)
                i += 1

        return '\n'.join(combined_lines), changes

    def condense(self,
                 text: str,
                 max_chars: Optional[int] = None,
                 max_lines: Optional[int] = None) -> CondenseResult:
        """
        Condense text to fit within limits.

        Args:
            text: Text to condense
            max_chars: Maximum characters per line (optional)
            max_lines: Maximum lines (optional)

        Returns:
            CondenseResult with condensed text and metadata
        """
        if not text:
            return CondenseResult(
                original_text="",
                condensed_text="",
                original_lines=0,
                condensed_lines=0,
                original_chars=0,
                condensed_chars=0,
                meets_limits=True
            )

        original_lines = len([l for l in text.split('\n') if l.strip()])
        original_chars = len(text)

        result = text
        techniques = []
        removed = []

        # Step 1: Remove filler phrases
        if self.remove_fillers:
            result, removals = self._remove_filler_phrases(result)
            if removals:
                techniques.append("Removed filler phrases")
                removed.extend(removals)

        # Step 2: Apply condensation mappings
        if self.apply_phrase_condensation:
            result, changes = self._apply_condensation_map(result)
            if changes:
                techniques.append("Applied phrase condensation")

        # Step 3: Condense bullets if needed
        if max_lines and self.preserve_bullets:
            current_lines = len([l for l in result.split('\n') if l.strip()])
            if current_lines > max_lines:
                result, changes = self._condense_bullets(result, max_lines)
                if changes:
                    techniques.append("Combined bullet points")

        # Check final state
        condensed_lines = len([l for l in result.split('\n') if l.strip()])
        condensed_chars = len(result)

        meets_limits = True
        if max_lines and condensed_lines > max_lines:
            meets_limits = False
        if max_chars:
            for line in result.split('\n'):
                if len(line) > max_chars:
                    meets_limits = False
                    break

        return CondenseResult(
            original_text=text,
            condensed_text=result,
            original_lines=original_lines,
            condensed_lines=condensed_lines,
            original_chars=original_chars,
            condensed_chars=condensed_chars,
            techniques_applied=techniques,
            removed_content=removed,
            was_modified=text != result,
            meets_limits=meets_limits
        )

    def condense_header(self, header: str) -> CondenseResult:
        """Condense header with 32 chars/line, 2 lines max."""
        return self.condense(header, max_chars=32, max_lines=2)

    def condense_body(self, body: str) -> CondenseResult:
        """Condense body with 66 chars/line, 8 lines max."""
        return self.condense(body, max_chars=66, max_lines=8)

    def condense_tip(self, tip: str) -> CondenseResult:
        """Condense NCLEX tip with 66 chars/line, 2 lines max."""
        return self.condense(tip, max_chars=66, max_lines=2)

    def condense_slide(self, slide: Dict[str, Any]) -> Dict[str, Any]:
        """
        Condense all text fields in a slide.

        Args:
            slide: Slide dictionary

        Returns:
            Slide with condensed text
        """
        result = slide.copy()

        if 'header' in result:
            condense_result = self.condense_header(result['header'])
            result['header'] = condense_result.condensed_text

        if 'body' in result:
            condense_result = self.condense_body(result['body'])
            result['body'] = condense_result.condensed_text

        tip_key = 'nclex_tip' if 'nclex_tip' in result else 'tip'
        if tip_key in result and result[tip_key]:
            condense_result = self.condense_tip(result[tip_key])
            result[tip_key] = condense_result.condensed_text

        return result


def condense_text(text: str,
                  max_chars: Optional[int] = None,
                  max_lines: Optional[int] = None) -> str:
    """
    Convenience function to condense text.

    Args:
        text: Text to condense
        max_chars: Maximum characters per line
        max_lines: Maximum lines

    Returns:
        Condensed text
    """
    condenser = TextCondenser()
    result = condenser.condense(text, max_chars=max_chars, max_lines=max_lines)
    return result.condensed_text


def condense_to_lines(text: str, max_lines: int) -> str:
    """Condense text to fit within line limit."""
    return condense_text(text, max_lines=max_lines)


def remove_fillers(text: str) -> str:
    """Remove filler phrases from text."""
    condenser = TextCondenser(apply_phrase_condensation=False)
    result = condenser.condense(text)
    return result.condensed_text


if __name__ == "__main__":
    # Test
    condenser = TextCondenser()

    test_text = """It is important to note that the parasympathetic nervous system plays an important role in reversing sympathetic activation:

* Slows heart rate and respiration
* Results in the occurrence of lowered blood pressure
* Redirects blood to digestive organs
  - Primary mechanism
  - Secondary pathway
  - Tertiary route
* In order to promote relaxation and recovery
* Is characterized by "rest and digest" response

Due to the fact that it is activated by deep breathing, it is able to reduce anxiety."""

    print("TextCondenser Test")
    print("=" * 60)
    print("Original:")
    print(test_text)
    print(f"\nOriginal lines: {len([l for l in test_text.split(chr(10)) if l.strip()])}")
    print()

    result = condenser.condense(test_text, max_lines=8)

    print("Condensed:")
    print(result.condensed_text)
    print()
    print(f"Condensed lines: {result.condensed_lines}")
    print(f"Meets limits: {result.meets_limits}")
    print(f"Was modified: {result.was_modified}")
    print()
    print("Techniques applied:")
    for tech in result.techniques_applied:
        print(f"  - {tech}")
