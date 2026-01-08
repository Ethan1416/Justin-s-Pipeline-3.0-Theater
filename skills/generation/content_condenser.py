"""
Content Condenser Skill
Intelligently condenses slide content while preserving key information.
Prioritizes NCLEX-testable content and clinical relevance.

Usage:
    from skills.generation.content_condenser import ContentCondenser, condense_content

    condenser = ContentCondenser()
    result = condenser.condense(slide, target_lines=8)
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class ContentCondenseResult:
    """Result of content condensation."""
    original_slide: Dict[str, Any]
    condensed_slide: Dict[str, Any]
    original_body_lines: int
    condensed_body_lines: int
    content_moved_to_notes: List[str] = field(default_factory=list)
    techniques_applied: List[str] = field(default_factory=list)
    priority_preserved: List[str] = field(default_factory=list)
    was_modified: bool = False
    meets_limits: bool = True
    annotation: str = ""


class ContentCondenser:
    """Intelligently condense content with priority preservation."""

    # Content priority levels (higher = more important to keep)
    PRIORITY_PATTERNS = {
        'nclex_testable': {
            'patterns': [
                r'NCLEX',
                r'exam tip',
                r'test[- ]taking',
                r'priority',
                r'first action',
                r'most important',
            ],
            'priority': 10
        },
        'clinical_critical': {
            'patterns': [
                r'life.?threatening',
                r'emergency',
                r'critical',
                r'urgent',
                r'contraindicated',
                r'adverse',
                r'toxic',
            ],
            'priority': 9
        },
        'key_differences': {
            'patterns': [
                r'differ(s|ence)',
                r'distinguish',
                r'versus|vs\.?',
                r'compared to',
                r'unlike',
                r'whereas',
            ],
            'priority': 8
        },
        'diagnostic': {
            'patterns': [
                r'diagnos(is|tic)',
                r'assess(ment)?',
                r'sign(s)?',
                r'symptom(s)?',
                r'manifestation',
            ],
            'priority': 7
        },
        'intervention': {
            'patterns': [
                r'intervention',
                r'treatment',
                r'nursing action',
                r'implement',
                r'administer',
            ],
            'priority': 7
        },
        'example': {
            'patterns': [
                r'for example',
                r'such as',
                r'e\.g\.',
                r'including',
                r'like',
            ],
            'priority': 3
        },
        'elaboration': {
            'patterns': [
                r'in other words',
                r'that is',
                r'meaning',
                r'essentially',
                r'basically',
            ],
            'priority': 2
        }
    }

    def __init__(self,
                 max_body_lines: int = 8,
                 max_chars_per_line: int = 66,
                 preserve_nclex_content: bool = True,
                 move_examples_to_notes: bool = True):
        """
        Initialize ContentCondenser.

        Args:
            max_body_lines: Maximum lines in body
            max_chars_per_line: Maximum characters per line
            preserve_nclex_content: Prioritize NCLEX-testable content
            move_examples_to_notes: Move examples to presenter notes
        """
        self.max_body_lines = max_body_lines
        self.max_chars_per_line = max_chars_per_line
        self.preserve_nclex_content = preserve_nclex_content
        self.move_examples_to_notes = move_examples_to_notes

    def _score_line_priority(self, line: str) -> Tuple[int, List[str]]:
        """
        Score a line's priority based on content patterns.

        Args:
            line: Line to score

        Returns:
            Tuple of (priority score, matching categories)
        """
        total_score = 5  # Default priority
        matches = []

        for category, config in self.PRIORITY_PATTERNS.items():
            for pattern in config['patterns']:
                if re.search(pattern, line, re.IGNORECASE):
                    total_score = max(total_score, config['priority'])
                    matches.append(category)
                    break

        return total_score, matches

    def _parse_body_lines(self, body: str) -> List[Dict[str, Any]]:
        """
        Parse body text into scored lines.

        Args:
            body: Body text

        Returns:
            List of line dictionaries with scores
        """
        lines = []
        for i, line in enumerate(body.split('\n')):
            stripped = line.strip()
            if stripped:
                score, categories = self._score_line_priority(stripped)
                lines.append({
                    'index': i,
                    'text': line,
                    'stripped': stripped,
                    'score': score,
                    'categories': categories,
                    'is_bullet': stripped.startswith(('*', '-', '•', '·')),
                    'is_sub_bullet': line.startswith(('  ', '\t'))
                })

        return lines

    def _condense_by_priority(self,
                               lines: List[Dict],
                               target_lines: int) -> Tuple[List[str], List[str]]:
        """
        Condense lines by priority, keeping high-priority content.

        Args:
            lines: Scored lines
            target_lines: Target line count

        Returns:
            Tuple of (kept lines, removed lines)
        """
        if len(lines) <= target_lines:
            return [l['text'] for l in lines], []

        # Sort by priority (higher first), then by original position
        sorted_lines = sorted(lines, key=lambda x: (-x['score'], x['index']))

        # Keep highest priority lines up to target
        kept_indices = set()
        for line in sorted_lines:
            if len(kept_indices) < target_lines:
                kept_indices.add(line['index'])

        # Preserve original order
        kept = []
        removed = []
        for line in lines:
            if line['index'] in kept_indices:
                kept.append(line['text'])
            else:
                removed.append(line['stripped'])

        return kept, removed

    def _combine_related_subbullets(self, lines: List[Dict]) -> List[str]:
        """
        Combine related sub-bullets into main bullets.

        Args:
            lines: Parsed lines

        Returns:
            Combined lines
        """
        result = []
        i = 0

        while i < len(lines):
            line = lines[i]

            if line['is_bullet'] and not line['is_sub_bullet']:
                # Collect sub-bullets
                sub_bullets = []
                j = i + 1
                while j < len(lines) and lines[j]['is_sub_bullet']:
                    sub_bullets.append(lines[j]['stripped'].lstrip('-•·* '))
                    j += 1

                if sub_bullets:
                    # Combine if reasonable
                    main_text = line['stripped'].rstrip(':')
                    combined = f"{main_text}: {', '.join(sub_bullets)}"
                    if len(combined) <= self.max_chars_per_line:
                        result.append(combined)
                        i = j
                        continue

            result.append(line['text'])
            i += 1

        return result

    def condense(self,
                 slide: Dict[str, Any],
                 target_lines: Optional[int] = None) -> ContentCondenseResult:
        """
        Condense slide content intelligently.

        Args:
            slide: Slide dictionary with body and presenter_notes
            target_lines: Target line count (default: max_body_lines)

        Returns:
            ContentCondenseResult with condensed slide
        """
        target = target_lines or self.max_body_lines
        result_slide = slide.copy()

        body = slide.get('body', '')
        notes = slide.get('presenter_notes', '') or ''

        if not body:
            return ContentCondenseResult(
                original_slide=slide,
                condensed_slide=result_slide,
                original_body_lines=0,
                condensed_body_lines=0,
                meets_limits=True
            )

        # Parse and score lines
        parsed_lines = self._parse_body_lines(body)
        original_line_count = len(parsed_lines)

        if original_line_count <= target:
            return ContentCondenseResult(
                original_slide=slide,
                condensed_slide=result_slide,
                original_body_lines=original_line_count,
                condensed_body_lines=original_line_count,
                meets_limits=True
            )

        techniques = []
        moved_to_notes = []
        preserved = []

        # Strategy 1: Combine sub-bullets
        combined = self._combine_related_subbullets(parsed_lines)
        if len(combined) < len(parsed_lines):
            techniques.append("Combined related sub-bullets")

        # Re-parse after combination
        new_body = '\n'.join(combined)
        parsed_lines = self._parse_body_lines(new_body)

        # Strategy 2: Move low-priority content to notes
        if len(parsed_lines) > target:
            kept, removed = self._condense_by_priority(parsed_lines, target)
            new_body = '\n'.join(kept)

            if removed:
                moved_to_notes = removed
                techniques.append(f"Moved {len(removed)} lines to notes")
                # Append to presenter notes
                if notes:
                    notes += "\n\n[Additional context from slide condensation]\n"
                else:
                    notes = "[Additional context from slide condensation]\n"
                notes += "\n".join(f"- {r}" for r in removed)

        # Track preserved high-priority content
        for line in self._parse_body_lines(new_body):
            if line['score'] >= 8:
                preserved.append(line['categories'][0] if line['categories'] else 'high_priority')

        result_slide['body'] = new_body
        result_slide['presenter_notes'] = notes

        # Final line count
        final_lines = len([l for l in new_body.split('\n') if l.strip()])

        # Generate annotation
        annotation = f"[CONDENSED FROM {original_line_count} LINES: "
        if moved_to_notes:
            annotation += f"Moved {len(moved_to_notes)} items to notes]"
        elif techniques:
            annotation += f"{'; '.join(techniques)}]"
        else:
            annotation += "Content reorganized]"

        return ContentCondenseResult(
            original_slide=slide,
            condensed_slide=result_slide,
            original_body_lines=original_line_count,
            condensed_body_lines=final_lines,
            content_moved_to_notes=moved_to_notes,
            techniques_applied=techniques,
            priority_preserved=list(set(preserved)),
            was_modified=slide != result_slide,
            meets_limits=final_lines <= target,
            annotation=annotation
        )


def condense_content(slide: Dict[str, Any], target_lines: int = 8) -> Dict[str, Any]:
    """
    Convenience function to condense slide content.

    Args:
        slide: Slide dictionary
        target_lines: Target line count

    Returns:
        Condensed slide dictionary
    """
    condenser = ContentCondenser()
    result = condenser.condense(slide, target_lines)
    return result.condensed_slide


def condense_body(body: str, target_lines: int = 8) -> str:
    """
    Condense body text only.

    Args:
        body: Body text
        target_lines: Target line count

    Returns:
        Condensed body text
    """
    slide = {'body': body}
    result = condense_content(slide, target_lines)
    return result.get('body', '')


if __name__ == "__main__":
    # Test
    condenser = ContentCondenser()

    test_slide = {
        'header': 'Parasympathetic Response',
        'body': """The parasympathetic nervous system reverses sympathetic activation:

• Slows heart rate and respiration
• Lowers blood pressure through vasodilation
• Redirects blood to digestive organs
  - Primary mechanism involves vagal stimulation
  - Secondary pathway through acetylcholine
  - Tertiary effects on smooth muscle
• Promotes relaxation and recovery
• Known as "rest and digest" or "feed and breed"
• Activated by deep breathing, relaxation techniques
• NCLEX tip: Priority is assessing breathing pattern first
• Clinical example: Post-operative recovery monitoring""",
        'presenter_notes': 'Explain the rest-and-digest response.'
    }

    print("ContentCondenser Test")
    print("=" * 60)
    print("Original body:")
    print(test_slide['body'])
    print(f"\nOriginal lines: {len([l for l in test_slide['body'].split(chr(10)) if l.strip()])}")
    print()

    result = condenser.condense(test_slide, target_lines=8)

    print("Condensed body:")
    print(result.condensed_slide['body'])
    print()
    print(f"Condensed lines: {result.condensed_body_lines}")
    print(f"Meets limits: {result.meets_limits}")
    print(f"Annotation: {result.annotation}")
    print()
    print("Techniques applied:")
    for tech in result.techniques_applied:
        print(f"  - {tech}")
    print()
    print("Content moved to notes:")
    for content in result.content_moved_to_notes:
        print(f"  - {content}")
    print()
    print("High-priority content preserved:")
    for p in result.priority_preserved:
        print(f"  - {p}")
