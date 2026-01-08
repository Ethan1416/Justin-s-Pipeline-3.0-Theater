"""
Unified Text Limits Enforcer
Applies all text limit enforcement in correct order.

UPDATED: Body character enforcement REMOVED.
PowerPoint handles text wrapping with word_wrap=True.
Only body LINE limits are enforced (12 lines max).

Usage:
    from skills.enforcement.text_limits_enforcer import enforce_all_text_limits
    fixed_slide = enforce_all_text_limits(slide)
"""

from typing import Dict, Any, List
from .header_enforcer import enforce_header_limits, validate_header
from .body_line_enforcer import enforce_body_lines, validate_body_lines
from .body_char_enforcer import validate_body_chars  # Only for validation, not enforcement


def enforce_all_text_limits(slide: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply all text limit enforcement to a slide.

    Order of operations:
    1. Enforce header limits (R1)
    2. Enforce body line limits (R2) - max 12 lines
    3. NO body character enforcement - PowerPoint wraps text

    Args:
        slide: Slide dictionary with 'header' and 'body' fields

    Returns:
        Slide with enforced limits
    """
    result = slide.copy()

    # R1: Header limits
    if 'header' in result:
        result['header'] = enforce_header_limits(result['header'])

    # R2: Body line limits ONLY (12 lines max)
    # NO R3 character enforcement - PowerPoint handles wrapping
    if 'body' in result:
        line_result = enforce_body_lines(result['body'], strategy='truncate')
        if isinstance(line_result['body'], str):
            result['body'] = line_result['body']
        else:
            # Content was split - return first chunk, flag for slide split
            result['body'] = line_result['body'][0]
            result['_overflow_bodies'] = line_result['body'][1:]
            result['_needs_split'] = True

    return result


def validate_all_text_limits(slide: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate all text limits on a slide.

    Returns:
        {
            'valid': bool,
            'r1_header': validation result,
            'r2_body_lines': validation result,
            'r3_body_info': informational only (no char limit),
            'issues': combined issues list
        }
    """
    results = {
        'r1_header': validate_header(slide.get('header', '')),
        'r2_body_lines': validate_body_lines(slide.get('body', '')),
        'r3_body_info': validate_body_chars(slide.get('body', '')),  # Informational only
    }

    # Only header and line limits count toward validity
    all_issues = []
    for key in ['r1_header', 'r2_body_lines']:
        all_issues.extend(results[key].get('issues', []))

    # Add any warnings from body chars (truncation markers)
    all_issues.extend(results['r3_body_info'].get('issues', []))

    results['valid'] = len([i for i in all_issues if not i.startswith('WARNING')]) == 0
    results['issues'] = all_issues

    return results


def enforce_all_slides(slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply text limit enforcement to all slides.

    Handles slide splitting if needed.

    Args:
        slides: List of slide dictionaries

    Returns:
        List of slides with enforced limits (may be longer if splits occurred)
    """
    result = []

    for slide in slides:
        enforced = enforce_all_text_limits(slide)

        if enforced.get('_needs_split'):
            # Original slide
            main_slide = {k: v for k, v in enforced.items()
                          if not k.startswith('_')}
            result.append(main_slide)

            # Overflow slides
            for i, overflow_body in enumerate(enforced.get('_overflow_bodies', [])):
                overflow_slide = main_slide.copy()
                overflow_slide['body'] = overflow_body
                overflow_slide['header'] = f"{main_slide['header']} (cont.)"
                result.append(overflow_slide)
        else:
            result.append(enforced)

    return result


if __name__ == "__main__":
    # Test
    test_slide = {
        'header': 'The World Health Organization Five Moments for Hand Hygiene Practice',
        'body': """The WHO identifies five critical moments requiring hand hygiene in healthcare:

1. Before patient contact - to protect the patient from colonization with healthcare-associated microorganisms
2. Before aseptic procedure - such as inserting catheters, accessing IV lines
3. After body fluid exposure risk - including after removing gloves
4. After patient contact - to protect yourself and the healthcare environment
5. After touching patient surroundings - including bed rails, monitors
6. Additional considerations include proper technique and duration
7. Hand hygiene compliance should be monitored regularly
8. Education and reminders are essential for maintaining compliance
9. Line nine
10. Line ten
11. Line eleven
12. Line twelve at limit
13. Line thirteen over limit"""
    }

    print("Original slide:")
    print(f"Header: {test_slide['header']}")
    print(f"Body lines: {len([l for l in test_slide['body'].split(chr(10)) if l.strip()])}")

    print("\n" + "="*60)
    fixed = enforce_all_text_limits(test_slide)
    print("\nAfter enforcement:")
    print(f"Header:\n{fixed['header']}")
    print(f"\nBody:\n{fixed['body']}")
    print(f"\nBody line count: {len([l for l in fixed['body'].split(chr(10)) if l.strip()])}")
    print(f"\nValidation: {validate_all_text_limits(fixed)}")
