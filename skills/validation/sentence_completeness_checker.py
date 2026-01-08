"""
Sentence Completeness Checker Skill
Validates that all sentences are complete and not truncated.

This is a HARDCODED validator - content MUST pass to proceed.

Requirements (from config/constraints.yaml):
- Every sentence must end with . ! ? or :
- No trailing ellipsis (...)
- No mid-word cuts
- No incomplete thoughts
- No orphaned phrases

Usage:
    from skills.validation.sentence_completeness_checker import (
        check_sentence_completeness,
        validate_text,
        find_truncations,
        auto_fix_truncations
    )
"""

import re
from typing import Dict, Any, List, Optional, Tuple


# Valid sentence-ending punctuation
TERMINAL_PUNCTUATION = '.!?:'

# Patterns that indicate truncation
TRUNCATION_PATTERNS = [
    (r'\.\.\.$', 'trailing_ellipsis', 'Trailing ellipsis indicates incomplete thought'),
    (r'\.\.\.\s*$', 'trailing_ellipsis', 'Trailing ellipsis indicates incomplete thought'),
    (r'…$', 'unicode_ellipsis', 'Unicode ellipsis indicates incomplete thought'),
    (r'\s+$', 'trailing_whitespace', 'Trailing whitespace may indicate truncation'),
    (r'[,;]\s*$', 'trailing_comma_semicolon', 'Ends with comma or semicolon, not complete'),
    (r'\band\s*$', 'trailing_and', 'Ends with "and", sentence incomplete'),
    (r'\bor\s*$', 'trailing_or', 'Ends with "or", sentence incomplete'),
    (r'\bthe\s*$', 'trailing_article', 'Ends with article, sentence incomplete'),
    (r'\ba\s*$', 'trailing_article', 'Ends with article, sentence incomplete'),
    (r'\ban\s*$', 'trailing_article', 'Ends with article, sentence incomplete'),
    (r'\bto\s*$', 'trailing_to', 'Ends with "to", sentence incomplete'),
    (r'\bof\s*$', 'trailing_of', 'Ends with "of", sentence incomplete'),
    (r'\bin\s*$', 'trailing_in', 'Ends with "in", sentence incomplete'),
    (r'\bfor\s*$', 'trailing_for', 'Ends with "for", sentence incomplete'),
    (r'\bwith\s*$', 'trailing_with', 'Ends with "with", sentence incomplete'),
    (r'\bthat\s*$', 'trailing_that', 'Ends with "that", sentence incomplete'),
    (r'\bwhich\s*$', 'trailing_which', 'Ends with "which", sentence incomplete'),
    (r'\bwho\s*$', 'trailing_who', 'Ends with "who", sentence incomplete'),
    (r'-\s*$', 'trailing_hyphen', 'Ends with hyphen, word may be cut'),
]

# Common incomplete phrase patterns
INCOMPLETE_PHRASE_PATTERNS = [
    r'^[a-z]',  # Starts with lowercase (may be fragment)
    r'^\s*[-•]\s*[a-z]',  # Bullet point starting lowercase
]

# Words that shouldn't start a sentence (likely fragments)
FRAGMENT_STARTERS = [
    'and', 'or', 'but', 'so', 'because', 'which', 'that', 'who',
    'including', 'such as', 'for example', 'like', 'as well as'
]


def is_complete_sentence(text: str) -> Tuple[bool, Optional[str]]:
    """
    Check if text is a complete sentence.

    Args:
        text: Text to check

    Returns:
        Tuple of (is_complete, reason_if_not)
    """
    if not text or not text.strip():
        return False, 'Empty text'

    text = text.strip()

    # Check for truncation patterns
    for pattern, code, message in TRUNCATION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, message

    # Check for terminal punctuation
    # Allow markers at the end like [PAUSE]
    text_without_markers = re.sub(r'\[[^\]]+\]\s*$', '', text).strip()

    if not text_without_markers:
        return True, None  # Just markers is OK

    last_char = text_without_markers[-1]
    if last_char not in TERMINAL_PUNCTUATION:
        return False, f'Missing terminal punctuation (ends with "{last_char}")'

    return True, None


def check_bullet_point(line: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a bullet point is complete.

    Args:
        line: Bullet point line

    Returns:
        Tuple of (is_complete, reason_if_not)
    """
    # Remove bullet marker
    content = re.sub(r'^[-•*]\s*', '', line.strip())

    if not content:
        return False, 'Empty bullet point'

    # Bullet points can be phrases, but shouldn't be cut off
    for pattern, code, message in TRUNCATION_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return False, message

    # Check for obviously incomplete content
    if len(content) < 3:
        return False, 'Content too short, likely truncated'

    return True, None


def find_truncations(text: str) -> List[Dict[str, Any]]:
    """
    Find all truncated content in text.

    Args:
        text: Text to analyze

    Returns:
        List of truncation issues found
    """
    issues = []

    if not text:
        return issues

    # Split into lines
    lines = text.split('\n')

    for line_num, line in enumerate(lines, 1):
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Check if it's a bullet point
        is_bullet = bool(re.match(r'^[-•*]\s', line_stripped))

        if is_bullet:
            is_complete, reason = check_bullet_point(line_stripped)
        else:
            is_complete, reason = is_complete_sentence(line_stripped)

        if not is_complete:
            issues.append({
                'line_number': line_num,
                'content': line_stripped[:100] + ('...' if len(line_stripped) > 100 else ''),
                'reason': reason,
                'is_bullet': is_bullet
            })

    # Also check the entire text as a whole
    full_text_stripped = text.strip()
    if full_text_stripped:
        is_complete, reason = is_complete_sentence(full_text_stripped)
        if not is_complete:
            # Only add if not already captured by line check
            if not any(i['line_number'] == len(lines) for i in issues):
                issues.append({
                    'line_number': len(lines),
                    'content': full_text_stripped[-100:],
                    'reason': f'Overall text: {reason}',
                    'is_bullet': False
                })

    return issues


def validate_text(
    text: str,
    context: str = 'general'
) -> Dict[str, Any]:
    """
    Validate text for completeness.

    Args:
        text: Text to validate
        context: Context hint (presenter_notes, body, header, etc.)

    Returns:
        Validation result
    """
    issues = find_truncations(text)

    return {
        'valid': len(issues) == 0,
        'issue_count': len(issues),
        'issues': issues,
        'context': context,
        'text_length': len(text) if text else 0
    }


def check_sentence_completeness(
    slides: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Check all slides for sentence completeness.

    This is the main entry point for the truncation validator.

    Args:
        slides: List of slide dictionaries

    Returns:
        Complete validation result
    """
    all_issues = []
    slides_checked = 0
    slides_with_issues = 0

    for slide in slides:
        slide_num = slide.get('slide_number', slides_checked + 1)
        slides_checked += 1

        slide_issues = []

        # Check header
        header = slide.get('header', slide.get('title', ''))
        if header:
            result = validate_text(header, 'header')
            if not result['valid']:
                for issue in result['issues']:
                    issue['slide_number'] = slide_num
                    issue['field'] = 'header'
                    slide_issues.append(issue)

        # Check body
        body = slide.get('body', '')
        if body:
            result = validate_text(body, 'body')
            if not result['valid']:
                for issue in result['issues']:
                    issue['slide_number'] = slide_num
                    issue['field'] = 'body'
                    slide_issues.append(issue)

        # Check presenter notes
        notes = slide.get('notes', slide.get('presenter_notes', ''))
        if notes:
            result = validate_text(notes, 'presenter_notes')
            if not result['valid']:
                for issue in result['issues']:
                    issue['slide_number'] = slide_num
                    issue['field'] = 'presenter_notes'
                    slide_issues.append(issue)

        # Check performance tip
        tip = slide.get('performance_tip', '')
        if tip:
            result = validate_text(tip, 'performance_tip')
            if not result['valid']:
                for issue in result['issues']:
                    issue['slide_number'] = slide_num
                    issue['field'] = 'performance_tip'
                    slide_issues.append(issue)

        if slide_issues:
            slides_with_issues += 1
            all_issues.extend(slide_issues)

    return {
        'valid': len(all_issues) == 0,
        'slides_checked': slides_checked,
        'slides_with_issues': slides_with_issues,
        'total_issues': len(all_issues),
        'issues': all_issues,
        'pass_rate': ((slides_checked - slides_with_issues) / slides_checked * 100) if slides_checked > 0 else 100
    }


def auto_fix_truncations(text: str) -> Tuple[str, List[str]]:
    """
    Attempt to auto-fix common truncation issues.

    Args:
        text: Text to fix

    Returns:
        Tuple of (fixed_text, list_of_fixes_applied)
    """
    if not text:
        return text, []

    fixes_applied = []
    result = text

    # Fix trailing ellipsis - remove it
    if re.search(r'\.\.\.\s*$', result):
        result = re.sub(r'\.\.\.\s*$', '.', result)
        fixes_applied.append('Replaced trailing ellipsis with period')

    if re.search(r'…\s*$', result):
        result = re.sub(r'…\s*$', '.', result)
        fixes_applied.append('Replaced unicode ellipsis with period')

    # Fix trailing comma/semicolon - add period
    if re.search(r'[,;]\s*$', result):
        result = re.sub(r'[,;]\s*$', '.', result)
        fixes_applied.append('Replaced trailing comma/semicolon with period')

    # Add period if missing terminal punctuation
    result_stripped = result.rstrip()
    if result_stripped and result_stripped[-1] not in TERMINAL_PUNCTUATION:
        # Check if it ends with a marker
        if not re.search(r'\[[^\]]+\]\s*$', result_stripped):
            result = result_stripped + '.'
            fixes_applied.append('Added missing period at end')

    # Fix each line in multi-line text
    lines = result.split('\n')
    fixed_lines = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            fixed_lines.append(line)
            continue

        # Check if bullet point
        is_bullet = bool(re.match(r'^[-•*]\s', line_stripped))

        if is_bullet:
            # Extract content after bullet
            match = re.match(r'^([-•*]\s*)(.*)', line_stripped)
            if match:
                bullet, content = match.groups()
                content = content.rstrip()
                if content and content[-1] not in TERMINAL_PUNCTUATION:
                    # Don't add period to phrases, but do fix obvious issues
                    pass  # Bullet points can be phrases
        else:
            # Regular sentence - ensure terminal punctuation
            if line_stripped and line_stripped[-1] not in TERMINAL_PUNCTUATION:
                if not re.search(r'\[[^\]]+\]\s*$', line_stripped):
                    line = line.rstrip() + '.'
                    fixes_applied.append(f'Added period to line')

        fixed_lines.append(line)

    result = '\n'.join(fixed_lines)

    return result, fixes_applied


def fix_slide_truncations(slide: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """
    Auto-fix truncations in a slide.

    Args:
        slide: Slide dictionary

    Returns:
        Tuple of (fixed_slide, list_of_fixes)
    """
    fixed = dict(slide)
    all_fixes = []

    # Fix header
    if 'header' in fixed:
        fixed['header'], fixes = auto_fix_truncations(fixed['header'])
        for f in fixes:
            all_fixes.append(f'Header: {f}')

    # Fix body
    if 'body' in fixed:
        fixed['body'], fixes = auto_fix_truncations(fixed['body'])
        for f in fixes:
            all_fixes.append(f'Body: {f}')

    # Fix presenter notes
    notes_key = 'notes' if 'notes' in fixed else 'presenter_notes'
    if notes_key in fixed:
        fixed[notes_key], fixes = auto_fix_truncations(fixed[notes_key])
        for f in fixes:
            all_fixes.append(f'Notes: {f}')

    # Fix performance tip
    if 'performance_tip' in fixed:
        fixed['performance_tip'], fixes = auto_fix_truncations(fixed['performance_tip'])
        for f in fixes:
            all_fixes.append(f'Tip: {f}')

    return fixed, all_fixes


if __name__ == "__main__":
    # Test
    print("Sentence Completeness Checker Test")
    print("=" * 50)

    # Test cases
    test_texts = [
        ("Complete sentence.", True),
        ("This is fine!", True),
        ("What do you think?", True),
        ("Note: remember this", True),
        ("Incomplete thought...", False),
        ("Ends with comma,", False),
        ("Ends with and", False),
        ("Missing punctuation", False),
        ("Has [PAUSE] marker.", True),
        ("Ends with [PAUSE]", True),
    ]

    print("\nIndividual text tests:")
    for text, expected in test_texts:
        is_complete, reason = is_complete_sentence(text)
        status = "✓" if is_complete == expected else "✗"
        print(f"  {status} '{text}' -> {is_complete} {f'({reason})' if reason else ''}")

    # Test slide validation
    print("\nSlide validation test:")
    test_slides = [
        {
            'slide_number': 1,
            'header': 'Greek Theater Origins',
            'body': '- Religious rituals\n- Festival of Dionysus\n- Dithyramb performances',
            'notes': 'Today we explore Greek theater. [PAUSE] This is fascinating...',
            'performance_tip': 'Project your voice!'
        },
        {
            'slide_number': 2,
            'header': 'The Theatron',
            'body': '- Seating area\n- Could hold 17000 spectators',
            'notes': 'The theatron was massive. Imagine the scale.',
            'performance_tip': 'Use your whole body.'
        }
    ]

    result = check_sentence_completeness(test_slides)
    print(f"  Valid: {result['valid']}")
    print(f"  Issues found: {result['total_issues']}")

    if result['issues']:
        print("\n  Issues:")
        for issue in result['issues']:
            print(f"    Slide {issue['slide_number']} ({issue['field']}): {issue['reason']}")

    # Test auto-fix
    print("\nAuto-fix test:")
    bad_text = "This sentence ends with..."
    fixed, fixes = auto_fix_truncations(bad_text)
    print(f"  Original: '{bad_text}'")
    print(f"  Fixed: '{fixed}'")
    print(f"  Fixes applied: {fixes}")
