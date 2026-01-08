"""
Slide Builder
Builds slide structure from slide plan and section content.

Usage:
    from skills.generation.slide_builder import (
        build_slide, build_section_intro, build_content_slide,
        allocate_content
    )
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class SlideStructure:
    """Represents a slide structure before content generation."""
    slide_number: int
    slide_type: str  # 'Section Intro', 'Content', 'Vignette', 'Answer'
    header: str = ""
    body: str = ""
    anchors_covered: List[str] = field(default_factory=list)
    nclex_tip: str = ""
    presenter_notes: str = ""
    visual_marker: str = "Visual: No"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'slide_number': self.slide_number,
            'slide_type': self.slide_type,
            'header': self.header,
            'body': self.body,
            'anchors_covered': self.anchors_covered,
            'nclex_tip': self.nclex_tip,
            'presenter_notes': self.presenter_notes,
            'visual_marker': self.visual_marker
        }


def build_slide(
    slide_plan_item: Dict[str, Any],
    anchor_content: List[Dict[str, Any]],
    section_context: Dict[str, Any]
) -> SlideStructure:
    """
    Build a slide structure from plan and content.

    Args:
        slide_plan_item: Single item from slide plan
        anchor_content: List of anchor content dictionaries
        section_context: Section metadata

    Returns:
        SlideStructure with header, body, and metadata
    """
    slide_type = slide_plan_item.get('slide_type', 'Content')
    slide_number = slide_plan_item.get('slide_number', 1)

    if slide_type == 'Section Intro':
        return build_section_intro(slide_number, section_context)
    elif slide_type == 'Content':
        return build_content_slide(slide_plan_item, anchor_content, section_context)
    elif slide_type == 'Vignette':
        return build_vignette_placeholder(slide_number, section_context)
    elif slide_type == 'Answer':
        return build_answer_placeholder(slide_number, section_context)
    else:
        return build_content_slide(slide_plan_item, anchor_content, section_context)


def build_section_intro(
    slide_number: int,
    section_context: Dict[str, Any]
) -> SlideStructure:
    """
    Build section introduction slide.

    Args:
        slide_number: Slide number (typically 1)
        section_context: Section metadata

    Returns:
        SlideStructure for section intro
    """
    section_name = section_context.get('section_name', 'Section')
    domain = section_context.get('domain', '')

    header = section_name[:32]  # Enforce R1 limit

    body_lines = [
        f"Welcome to {section_name}",
        "",
        "In this section, you will learn:",
        "* Key concepts and definitions",
        "* Clinical applications",
        "* NCLEX preparation strategies"
    ]
    body = '\n'.join(body_lines)

    return SlideStructure(
        slide_number=slide_number,
        slide_type='Section Intro',
        header=header,
        body=body,
        anchors_covered=[]
    )


def build_content_slide(
    slide_plan_item: Dict[str, Any],
    anchor_content: List[Dict[str, Any]],
    section_context: Dict[str, Any]
) -> SlideStructure:
    """
    Build content slide from anchors.

    Args:
        slide_plan_item: Slide plan with assigned anchors
        anchor_content: Anchor content list
        section_context: Section metadata

    Returns:
        SlideStructure for content slide
    """
    slide_number = slide_plan_item.get('slide_number', 1)
    assigned_anchors = slide_plan_item.get('assigned_anchors', [])
    title_hint = slide_plan_item.get('title_hint', 'Content')

    # Build header from title hint
    header = title_hint[:32]  # Enforce R1 basic limit

    # Build body from anchor content
    body_lines = []
    covered_anchors = []

    for anchor in anchor_content:
        anchor_id = anchor.get('anchor_id', '')
        if anchor_id in assigned_anchors:
            covered_anchors.append(anchor_id)
            key_points = anchor.get('key_points', [])
            for point in key_points[:3]:  # Limit points per anchor
                if len(body_lines) < 8:  # R2 limit
                    body_lines.append(f"* {point[:63]}")  # R3 limit with bullet

    body = '\n'.join(body_lines)

    return SlideStructure(
        slide_number=slide_number,
        slide_type='Content',
        header=header,
        body=body,
        anchors_covered=covered_anchors
    )


def build_vignette_placeholder(
    slide_number: int,
    section_context: Dict[str, Any],
    concepts_tested: Optional[List[str]] = None
) -> SlideStructure:
    """
    Build placeholder for vignette slide (filled by vignette_generator).

    Args:
        slide_number: Slide number
        section_context: Section metadata
        concepts_tested: Optional list of anchor concepts the vignette tests.
                        These are tracked for R8 anchor coverage.

    Returns:
        SlideStructure for vignette placeholder
    """
    section_name = section_context.get('section_name', 'Section')

    # Extract concepts tested from section context if not provided
    if concepts_tested is None:
        concepts_tested = section_context.get('vignette_concepts', [])

    return SlideStructure(
        slide_number=slide_number,
        slide_type='Vignette',
        header=f"{section_name[:20]} - Clinical Application",
        body="[Vignette content to be generated]",
        anchors_covered=concepts_tested  # Track concepts for R8 coverage
    )


def build_answer_placeholder(
    slide_number: int,
    section_context: Dict[str, Any],
    concepts_explained: Optional[List[str]] = None
) -> SlideStructure:
    """
    Build placeholder for answer slide (filled by vignette_generator).

    Args:
        slide_number: Slide number
        section_context: Section metadata
        concepts_explained: Optional list of anchor concepts explained in the answer.
                           These reinforce the vignette concepts for R8 tracking.

    Returns:
        SlideStructure for answer placeholder
    """
    # Extract concepts from section context if not provided
    if concepts_explained is None:
        concepts_explained = section_context.get('answer_concepts', [])

    return SlideStructure(
        slide_number=slide_number,
        slide_type='Answer',
        header="Answer: [Letter]",
        body="[Answer content to be generated]",
        anchors_covered=concepts_explained  # Track concepts for R8 coverage
    )


def allocate_content(
    anchors: List[Dict[str, Any]],
    slide_count: int
) -> Dict[int, List[str]]:
    """
    Allocate anchors to slide numbers.

    Args:
        anchors: List of anchor content
        slide_count: Total number of content slides

    Returns:
        Dict mapping slide_number to list of anchor_ids
    """
    if not anchors or slide_count <= 0:
        return {}

    allocation = {}
    anchors_per_slide = max(1, len(anchors) // slide_count)

    anchor_ids = [a.get('anchor_id', f'anchor_{i}') for i, a in enumerate(anchors)]

    for i in range(slide_count):
        start_idx = i * anchors_per_slide
        end_idx = start_idx + anchors_per_slide
        if i == slide_count - 1:  # Last slide gets remaining
            end_idx = len(anchor_ids)
        allocation[i + 2] = anchor_ids[start_idx:end_idx]  # +2 for intro slide offset

    return allocation


if __name__ == "__main__":
    # Test
    section_context = {
        'section_name': 'Infection Control',
        'domain': 'fundamentals'
    }

    slide_plan_item = {
        'slide_number': 2,
        'slide_type': 'Content',
        'title_hint': 'Standard Precautions',
        'assigned_anchors': ['anchor_1', 'anchor_2']
    }

    anchor_content = [
        {
            'anchor_id': 'anchor_1',
            'summary': 'Hand hygiene basics',
            'key_points': ['Wash hands before patient contact', 'Use alcohol-based rub']
        },
        {
            'anchor_id': 'anchor_2',
            'summary': 'PPE usage',
            'key_points': ['Gloves for body fluid contact', 'Gowns for splash risk']
        }
    ]

    slide = build_slide(slide_plan_item, anchor_content, section_context)
    print(f"Slide {slide.slide_number}: {slide.header}")
    print(f"Body:\n{slide.body}")
    print(f"Anchors covered: {slide.anchors_covered}")
