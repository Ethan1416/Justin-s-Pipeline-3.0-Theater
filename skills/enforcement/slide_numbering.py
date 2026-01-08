"""
Slide Numbering Enforcement Skill
Ensures slides are numbered sequentially starting from 1.

Usage:
    from skills.enforcement.slide_numbering import enforce_sequential_numbering
    slides = enforce_sequential_numbering(slides)
"""

from typing import List, Dict, Any


def enforce_sequential_numbering(slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Enforce sequential slide numbering starting from 1.

    Args:
        slides: List of slide dictionaries with 'slide_number' field

    Returns:
        Slides with corrected sequential numbering
    """
    if not slides:
        return slides

    for i, slide in enumerate(slides, start=1):
        slide['slide_number'] = i

    return slides


def validate_sequential_numbering(slides: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate that slides are numbered sequentially.

    Returns:
        {
            'valid': bool,
            'expected': list,
            'actual': list,
            'issues': list
        }
    """
    if not slides:
        return {'valid': True, 'expected': [], 'actual': [], 'issues': []}

    actual = [s.get('slide_number') for s in slides]
    expected = list(range(1, len(slides) + 1))

    issues = []
    if actual != expected:
        issues.append(f"Non-sequential numbering: expected {expected}, got {actual}")

    return {
        'valid': actual == expected,
        'expected': expected,
        'actual': actual,
        'issues': issues
    }


if __name__ == "__main__":
    # Test
    test_slides = [
        {'slide_number': 1, 'title': 'Intro'},
        {'slide_number': 3, 'title': 'Content'},  # Wrong!
        {'slide_number': 5, 'title': 'End'},      # Wrong!
    ]

    print("Before:", [s['slide_number'] for s in test_slides])
    print("Valid before:", validate_sequential_numbering(test_slides))

    fixed = enforce_sequential_numbering(test_slides)
    print("\nAfter:", [s['slide_number'] for s in fixed])
    print("Valid after:", validate_sequential_numbering(fixed))
