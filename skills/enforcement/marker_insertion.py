"""
Presenter Notes Marker Insertion
Ensures notes have required [PAUSE] and [EMPHASIS] markers.

Usage:
    from skills.enforcement.marker_insertion import (
        insert_markers, validate_markers
    )
"""

import re
from typing import Dict, Any, List, Tuple


MIN_PAUSE_MARKERS = 2
MIN_EMPHASIS_MARKERS_CONTENT = 1


def count_markers(notes: str) -> Dict[str, int]:
    """Count markers in notes."""
    return {
        'pause': len(re.findall(r'\[PAUSE[^\]]*\]', notes, re.IGNORECASE)),
        'emphasis': len(re.findall(r'\[EMPHASIS[:\s][^\]]+\]', notes, re.IGNORECASE)),
    }


def find_key_terms(text: str, domain: str = 'general') -> List[str]:
    """
    Find key clinical terms that should be emphasized.

    Args:
        text: Notes text
        domain: Clinical domain for context

    Returns:
        List of terms to emphasize
    """
    # Common nursing/clinical terms to emphasize
    key_patterns = [
        # Clinical terms
        r'\b(assessment|intervention|evaluation)\b',
        r'\b(airway|breathing|circulation)\b',
        r'\b(priority|first|immediate)\b',
        r'\b(infection|isolation|precaution)\b',
        r'\b(safety|sterile|aseptic)\b',

        # Medication terms
        r'\b(medication|drug|dose|administration)\b',
        r'\b(adverse|side effect|contraindication)\b',

        # Body systems
        r'\b(cardiac|respiratory|neurological|renal)\b',

        # Specific conditions
        r'\b(diabetes|hypertension|infection)\b',
        r'\b(tuberculosis|TB|MRSA|C\.\s*diff)\b',

        # Equipment/procedures
        r'\b(catheter|IV|ventilator|monitor)\b',
        r'\b(hand\s+hygiene|PPE|N95|gown)\b',

        # NCLEX keywords
        r'\b(NCLEX|test|exam|question)\b',
    ]

    found_terms = []
    text_lower = text.lower()

    for pattern in key_patterns:
        matches = re.findall(pattern, text_lower)
        found_terms.extend(matches)

    # Return unique terms, capitalized
    return list(set(term.title() for term in found_terms))


def insert_pause_markers(notes: str) -> str:
    """
    Insert [PAUSE] markers at natural break points.

    Strategy:
    - After first sentence
    - Before transitional phrases
    - Before final sentence (to ensure minimum 2 pauses)

    Args:
        notes: Original presenter notes

    Returns:
        Notes with [PAUSE] markers (minimum 2)
    """
    if '[PAUSE' in notes:
        # Already has markers, check if enough
        if count_markers(notes)['pause'] >= MIN_PAUSE_MARKERS:
            return notes

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', notes)

    if len(sentences) < 3:
        # Too short, add pause at midpoint if possible
        if len(sentences) == 2:
            return sentences[0] + ' [PAUSE] ' + sentences[1] + ' [PAUSE]'
        return notes

    result = []
    pause_count = 0

    for i, sentence in enumerate(sentences):
        result.append(sentence)

        # Add pause after first sentence
        if i == 0:
            result.append(' [PAUSE]')
            pause_count += 1

        # Add pause before transition words
        elif i < len(sentences) - 1:
            next_sentence_lower = sentences[i + 1].lower()
            transition_words = ['now', 'next', 'let\'s', 'remember', 'on the nclex',
                                'this is important', 'the key', 'so,']
            if any(next_sentence_lower.startswith(tw) for tw in transition_words):
                result.append(' [PAUSE]')
                pause_count += 1

    # Ensure minimum 2 pauses by adding before last sentence if needed
    if pause_count < MIN_PAUSE_MARKERS and len(sentences) >= 3:
        # Find the last sentence and insert pause before it
        final_text = ' '.join(result)
        # Insert pause before the last sentence
        last_period_idx = final_text.rfind('.')
        if last_period_idx > 0:
            # Find the second-to-last period (start of last sentence)
            second_last = final_text.rfind('.', 0, last_period_idx)
            if second_last > 0 and '[PAUSE]' not in final_text[second_last:last_period_idx]:
                final_text = final_text[:second_last+1] + ' [PAUSE]' + final_text[second_last+1:]
        return final_text

    return ' '.join(result)


def insert_emphasis_markers(notes: str, domain: str = 'general') -> str:
    """
    Insert [EMPHASIS: term] markers for key vocabulary.

    Args:
        notes: Original presenter notes
        domain: Clinical domain

    Returns:
        Notes with [EMPHASIS] markers
    """
    if '[EMPHASIS' in notes:
        # Already has markers, check if enough
        if count_markers(notes)['emphasis'] >= MIN_EMPHASIS_MARKERS_CONTENT:
            return notes

    key_terms = find_key_terms(notes, domain)

    if not key_terms:
        return notes

    result = notes
    emphasized = 0
    max_emphasis = 3  # Don't over-emphasize

    for term in key_terms[:max_emphasis]:
        # Find the term in text (case insensitive, whole word)
        pattern = rf'\b({re.escape(term)})\b'
        match = re.search(pattern, result, re.IGNORECASE)

        if match and '[EMPHASIS' not in result[max(0, match.start()-10):match.end()+10]:
            # Replace first occurrence only
            original_term = match.group(1)
            result = result[:match.start()] + f'[EMPHASIS: {original_term}]' + result[match.end():]
            emphasized += 1

    return result


def insert_markers(
    notes: str,
    slide_type: str,
    domain: str = 'general'
) -> str:
    """
    Insert all required markers into presenter notes.

    Args:
        notes: Original presenter notes
        slide_type: Type of slide (content, vignette, answer, etc.)
        domain: Clinical domain

    Returns:
        Notes with all required markers
    """
    result = notes

    # Insert [PAUSE] markers
    result = insert_pause_markers(result)

    # Insert [EMPHASIS] markers for content slides
    if slide_type.lower() == 'content':
        result = insert_emphasis_markers(result, domain)

    return result


def validate_markers(notes: str, slide_type: str) -> Dict[str, Any]:
    """
    Validate presenter notes have required markers.

    Returns:
        {
            'valid': bool,
            'pause_count': int,
            'emphasis_count': int,
            'issues': list
        }
    """
    counts = count_markers(notes)
    issues = []

    # Check [PAUSE] markers
    if counts['pause'] < MIN_PAUSE_MARKERS:
        issues.append(f"Only {counts['pause']} [PAUSE] markers, need at least {MIN_PAUSE_MARKERS}")

    # Check [EMPHASIS] markers for content slides
    if slide_type.lower() == 'content':
        if counts['emphasis'] < MIN_EMPHASIS_MARKERS_CONTENT:
            issues.append(f"Only {counts['emphasis']} [EMPHASIS] markers, need at least {MIN_EMPHASIS_MARKERS_CONTENT}")

    return {
        'valid': len(issues) == 0,
        'pause_count': counts['pause'],
        'emphasis_count': counts['emphasis'],
        'issues': issues
    }


if __name__ == "__main__":
    # Test
    test_notes = """Standard precautions are the foundation of infection control.
We treat every patient's body fluids as potentially infectious.
The components include hand hygiene and PPE.
Safe injection practices are also critical.
On the NCLEX, standard precautions questions are common."""

    print("Original:")
    print(test_notes)
    print(f"\nMarker counts: {count_markers(test_notes)}")

    print("\n\nAfter marker insertion:")
    fixed = insert_markers(test_notes, slide_type='content', domain='fundamentals')
    print(fixed)
    print(f"\nMarker counts: {count_markers(fixed)}")
    print(f"Validation: {validate_markers(fixed, 'content')}")
