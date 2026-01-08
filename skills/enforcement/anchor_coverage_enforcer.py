"""
Anchor Coverage Enforcer
Generates slides for missing anchors if validation fails.

Usage:
    from skills.enforcement.anchor_coverage_enforcer import ensure_anchor_coverage
    slides = ensure_anchor_coverage(slides, input_anchors)
"""

from typing import List, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from validation.anchor_coverage_tracker import (
    AnchorCoverageTracker,
    Anchor
)


def generate_anchor_slide(anchor: Anchor, slide_number: int) -> Dict[str, Any]:
    """
    Generate a minimal slide to cover a missing anchor.

    This is a fallback - ideally anchors are covered during normal generation.

    Args:
        anchor: The missing anchor
        slide_number: Slide number to assign

    Returns:
        Slide dictionary
    """
    # Create header from anchor summary
    header = anchor.summary
    if len(header) > 32:
        header = header[:29] + "..."

    # Create body from anchor text
    body_lines = []

    # Add context from anchor text
    text = anchor.text
    if text:
        # Split into manageable lines
        sentences = text.split('. ')
        for sentence in sentences[:4]:  # Max 4 sentences
            if sentence.strip():
                body_lines.append(f"- {sentence.strip()}")

    body = '\n'.join(body_lines[:8])  # Max 8 lines

    # Create slide
    slide = {
        'slide_number': slide_number,
        'type': 'content',
        'header': header,
        'body': body,
        'subsection': anchor.subsection,
        'anchors_covered': [anchor.summary],
        'performance_tip': '',  # Will be filled by tip_generator
        'presenter_notes': '',  # Will be filled by presenter_notes_writer
        '_generated_for_coverage': True,  # Flag for tracking
    }

    return slide


def ensure_anchor_coverage(
    slides: List[Dict[str, Any]],
    step4_input: Dict[str, Any],
    max_attempts: int = 3
) -> Dict[str, Any]:
    """
    Ensure all anchors are covered, generating slides if needed.
    Implements retry logic with progressive fallback strategies.

    Args:
        slides: Generated slides
        step4_input: Step 4 output with anchors
        max_attempts: Max regeneration attempts (default 3)

    Returns:
        {
            'slides': list (possibly extended),
            'added_slides': int,
            'coverage_result': validation result,
            'attempts_used': int,
            'strategy_used': str
        }
    """
    result_slides = list(slides)  # Work with a copy
    total_added = 0
    all_generated = []
    attempts_used = 0
    strategy_used = 'none'

    # Strategy progression for retry attempts
    strategies = [
        ('standard', 2),      # Attempt 1: Standard 2 anchors per slide
        ('compact', 3),       # Attempt 2: Compact 3 anchors per slide
        ('minimal', 4)        # Attempt 3: Minimal 4 anchors per slide
    ]

    for attempt in range(max_attempts):
        attempts_used = attempt + 1
        strategy_name, anchors_per_slide = strategies[min(attempt, len(strategies) - 1)]
        strategy_used = strategy_name

        # Initialize tracker
        tracker = AnchorCoverageTracker.from_input(step4_input)

        # Mark existing coverage
        for slide in result_slides:
            anchors_covered = slide.get('anchors_covered', [])
            if anchors_covered:
                tracker.mark_covered(
                    anchors_covered,
                    slide_number=slide.get('slide_number', 0),
                    slide_type=slide.get('type', 'content')
                )

        # Check coverage
        result = tracker.validate()

        if result['valid']:
            return {
                'slides': result_slides,
                'added_slides': total_added,
                'coverage_result': result,
                'generated_slides': all_generated,
                'attempts_used': attempts_used,
                'strategy_used': 'already_covered' if attempt == 0 else strategy_used
            }

        # Get missing anchors
        missing_anchors = tracker.get_missing()
        if not missing_anchors:
            break

        # Generate slides for missing anchors based on strategy
        added_slides = []
        next_slide_num = max(s.get('slide_number', 0) for s in result_slides) + 1

        # Group anchors based on strategy (more per slide on later attempts)
        anchor_groups = []
        for i in range(0, len(missing_anchors), anchors_per_slide):
            anchor_groups.append(missing_anchors[i:i + anchors_per_slide])

        for group in anchor_groups:
            # Generate slide covering multiple anchors if needed
            if len(group) == 1:
                new_slide = generate_anchor_slide(group[0], next_slide_num)
            else:
                # Multi-anchor slide
                new_slide = _generate_multi_anchor_slide(group, next_slide_num)

            added_slides.append(new_slide)
            all_generated.append(new_slide)
            next_slide_num += 1

            # Update tracker
            for anchor in group:
                tracker.mark_covered(
                    [anchor.summary],
                    slide_number=new_slide['slide_number'],
                    slide_type='content'
                )

        # Insert new slides before vignette (if exists)
        vignette_index = None
        for i, slide in enumerate(result_slides):
            if slide.get('type', '').lower() == 'vignette':
                vignette_index = i
                break

        if vignette_index is not None:
            result_slides = result_slides[:vignette_index] + added_slides + result_slides[vignette_index:]
        else:
            result_slides = result_slides + added_slides

        total_added += len(added_slides)

        # Re-validate after this attempt
        final_result = tracker.validate()
        if final_result['valid']:
            return {
                'slides': result_slides,
                'added_slides': total_added,
                'coverage_result': final_result,
                'generated_slides': all_generated,
                'attempts_used': attempts_used,
                'strategy_used': strategy_used
            }

    # Final validation after all attempts
    final_tracker = AnchorCoverageTracker.from_input(step4_input)
    for slide in result_slides:
        anchors_covered = slide.get('anchors_covered', [])
        if anchors_covered:
            final_tracker.mark_covered(
                anchors_covered,
                slide_number=slide.get('slide_number', 0),
                slide_type=slide.get('type', 'content')
            )
    final_result = final_tracker.validate()

    return {
        'slides': result_slides,
        'added_slides': total_added,
        'coverage_result': final_result,
        'generated_slides': all_generated,
        'attempts_used': attempts_used,
        'strategy_used': strategy_used,
        'max_attempts_reached': True
    }


def _generate_multi_anchor_slide(anchors: List[Anchor], slide_number: int) -> Dict[str, Any]:
    """
    Generate a slide covering multiple anchors (compact strategy).

    Args:
        anchors: List of anchors to cover
        slide_number: Slide number to assign

    Returns:
        Slide dictionary
    """
    # Create header from first anchor
    header = anchors[0].summary
    if len(header) > 32:
        header = header[:29] + "..."

    # Create body from all anchors
    body_lines = []
    covered_summaries = []

    for anchor in anchors:
        covered_summaries.append(anchor.summary)
        # Add 1-2 lines per anchor
        text = anchor.text
        if text:
            sentences = text.split('. ')
            for sentence in sentences[:2]:  # Max 2 sentences per anchor
                if sentence.strip() and len(body_lines) < 8:
                    body_lines.append(f"- {sentence.strip()[:63]}")

    body = '\n'.join(body_lines[:8])

    return {
        'slide_number': slide_number,
        'type': 'content',
        'header': header,
        'body': body,
        'subsection': anchors[0].subsection,
        'anchors_covered': covered_summaries,
        'performance_tip': '',
        'presenter_notes': '',
        '_generated_for_coverage': True,
        '_multi_anchor': True,
        '_anchor_count': len(anchors)
    }


def get_anchor_assignment_plan(
    step4_input: Dict[str, Any],
    slides_per_anchor: int = 1
) -> List[Dict[str, Any]]:
    """
    Generate anchor-to-slide assignment plan.

    Used by slide_planner to pre-assign anchors to slides.

    Args:
        step4_input: Step 4 output
        slides_per_anchor: How many slides per anchor (default 1)

    Returns:
        List of assignments: [{slide_number, anchors, subsection}]
    """
    assignments = []
    slide_num = 2  # Start after intro slide

    section = step4_input.get('section', step4_input)

    for subsection in section.get('subsections', []):
        subsection_name = subsection.get('subsection_name', '')
        anchors = subsection.get('anchors', [])

        # Sort: FRONTLOAD first
        sorted_anchors = sorted(
            anchors,
            key=lambda a: (0 if 'FRONTLOAD' in a.get('flags', []) else 1)
        )

        # Group anchors into slides (2 per slide typical)
        anchors_per_slide = 2
        for i in range(0, len(sorted_anchors), anchors_per_slide):
            batch = sorted_anchors[i:i + anchors_per_slide]
            assignments.append({
                'slide_number': slide_num,
                'subsection': subsection_name,
                'anchors': [a.get('anchor_summary') for a in batch],
                'anchor_details': batch
            })
            slide_num += 1

    return assignments


def renumber_slides(slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Renumber slides sequentially after insertion.

    Args:
        slides: List of slide dictionaries

    Returns:
        Slides with updated slide_number values
    """
    for i, slide in enumerate(slides, start=1):
        slide['slide_number'] = i
    return slides


if __name__ == "__main__":
    # Test
    sample_input = {
        "section": {
            "subsections": [
                {
                    "subsection_name": "Hand Hygiene",
                    "anchors": [
                        {"anchor_number": 1, "anchor_summary": "Hand hygiene principles",
                         "anchor_text": "Proper hand hygiene is essential.", "flags": ["FRONTLOAD"]},
                        {"anchor_number": 2, "anchor_summary": "ABHR vs soap",
                         "anchor_text": "Use ABHR for routine, soap for C.diff.", "flags": []},
                    ]
                }
            ]
        }
    }

    # Simulate slides missing one anchor
    slides = [
        {'slide_number': 1, 'type': 'section_intro', 'anchors_covered': []},
        {'slide_number': 2, 'type': 'content', 'anchors_covered': ['Hand hygiene principles']},
        # Missing: "ABHR vs soap"
        {'slide_number': 3, 'type': 'vignette', 'anchors_covered': []},
        {'slide_number': 4, 'type': 'answer', 'anchors_covered': []},
    ]

    result = ensure_anchor_coverage(slides, sample_input)
    print(f"Added {result['added_slides']} slides")
    print(f"Coverage valid: {result['coverage_result']['valid']}")

    if result['generated_slides']:
        print("\nGenerated slide:")
        print(result['generated_slides'][0])
