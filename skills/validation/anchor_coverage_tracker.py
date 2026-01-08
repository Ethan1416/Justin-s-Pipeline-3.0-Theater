"""
Anchor Coverage Tracker
Tracks which anchors from input have been covered in output.

Usage:
    tracker = AnchorCoverageTracker(input_anchors)
    for slide in slides:
        tracker.mark_covered(slide['anchors_covered'])
    result = tracker.validate()
"""

from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass, field
import re


@dataclass
class Anchor:
    """Represents an anchor from Step 4 input."""
    number: int
    summary: str
    text: str
    flags: List[str] = field(default_factory=list)
    subsection: str = ""

    @property
    def is_frontload(self) -> bool:
        return 'FRONTLOAD' in self.flags

    @property
    def is_xref(self) -> bool:
        return 'XREF' in self.flags

    def __hash__(self):
        return hash(self.summary)

    def __eq__(self, other):
        if isinstance(other, Anchor):
            return self.summary == other.summary
        return self.summary == other


class AnchorCoverageTracker:
    """
    Tracks anchor coverage throughout blueprint generation.

    Usage:
        tracker = AnchorCoverageTracker.from_input(step4_output)
        tracker.mark_covered("Hand hygiene principles", slide_number=2)
        result = tracker.validate()
    """

    def __init__(self, anchors: List[Anchor] = None):
        self.anchors: Dict[str, Anchor] = {}
        self.covered: Dict[str, Dict[str, Any]] = {}  # summary -> coverage info
        self._slide_assignments: Dict[int, List[str]] = {}  # slide_num -> anchors

        if anchors:
            for anchor in anchors:
                self.anchors[anchor.summary] = anchor

    @classmethod
    def from_input(cls, step4_output: Dict[str, Any]) -> 'AnchorCoverageTracker':
        """
        Create tracker from Step 4 output.

        Args:
            step4_output: Dictionary with section.subsections[].anchors[]

        Returns:
            Configured tracker
        """
        tracker = cls()
        section = step4_output.get('section', step4_output)

        for subsection in section.get('subsections', []):
            subsection_name = subsection.get('subsection_name', '')

            for anchor_data in subsection.get('anchors', []):
                anchor = Anchor(
                    number=anchor_data.get('anchor_number', 0),
                    summary=anchor_data.get('anchor_summary', ''),
                    text=anchor_data.get('anchor_text', ''),
                    flags=anchor_data.get('flags', []),
                    subsection=subsection_name
                )
                tracker.anchors[anchor.summary] = anchor

        return tracker

    def mark_covered(
        self,
        anchor_summaries: List[str],
        slide_number: int,
        slide_type: str = 'content'
    ) -> None:
        """
        Mark anchors as covered by a slide.

        Args:
            anchor_summaries: List of anchor summaries covered
            slide_number: Slide number that covers them
            slide_type: Type of slide (content, vignette, etc.)
        """
        if isinstance(anchor_summaries, str):
            anchor_summaries = [anchor_summaries]

        for summary in anchor_summaries:
            # Normalize for matching
            normalized = summary.strip().lower()

            # Find matching anchor
            matched_anchor = None
            for key, anchor in self.anchors.items():
                if key.lower() == normalized or normalized in key.lower():
                    matched_anchor = key
                    break

            if matched_anchor:
                if matched_anchor not in self.covered:
                    self.covered[matched_anchor] = {
                        'slides': [],
                        'first_slide': slide_number
                    }
                self.covered[matched_anchor]['slides'].append({
                    'slide_number': slide_number,
                    'slide_type': slide_type
                })

        # Track slide assignments
        self._slide_assignments[slide_number] = anchor_summaries

    def get_missing(self) -> List[Anchor]:
        """Get list of anchors not yet covered."""
        missing = []
        for summary, anchor in self.anchors.items():
            if summary not in self.covered:
                missing.append(anchor)
        return missing

    def get_covered(self) -> List[Anchor]:
        """Get list of covered anchors."""
        return [self.anchors[summary] for summary in self.covered]

    def validate(self) -> Dict[str, Any]:
        """
        Validate anchor coverage.

        Returns:
            {
                'valid': bool,
                'total_anchors': int,
                'covered_count': int,
                'missing_count': int,
                'missing_anchors': list,
                'coverage_details': dict,
                'frontload_violations': list,
                'issues': list
            }
        """
        missing = self.get_missing()
        issues = []

        # Check for missing anchors
        if missing:
            for anchor in missing:
                issues.append(f"Missing anchor: {anchor.summary}")

        # Check FRONTLOAD positioning
        frontload_violations = []
        for summary, coverage in self.covered.items():
            anchor = self.anchors[summary]
            if anchor.is_frontload:
                # FRONTLOAD anchors should appear on early slides
                first_slide = coverage['first_slide']
                # This is a soft check - early means within first few slides
                if first_slide > 3:
                    frontload_violations.append({
                        'anchor': summary,
                        'first_appearance': first_slide,
                        'expected': 'within first 3 slides of subsection'
                    })

        if frontload_violations:
            for v in frontload_violations:
                issues.append(f"FRONTLOAD anchor '{v['anchor']}' appears late (slide {v['first_appearance']})")

        return {
            'valid': len(missing) == 0,
            'total_anchors': len(self.anchors),
            'covered_count': len(self.covered),
            'missing_count': len(missing),
            'missing_anchors': [{'summary': a.summary, 'subsection': a.subsection} for a in missing],
            'coverage_details': self.covered,
            'frontload_violations': frontload_violations,
            'issues': issues
        }

    def get_coverage_report(self) -> str:
        """Generate human-readable coverage report."""
        result = self.validate()

        lines = [
            "=" * 60,
            "ANCHOR COVERAGE REPORT",
            "=" * 60,
            f"Total anchors: {result['total_anchors']}",
            f"Covered: {result['covered_count']}",
            f"Missing: {result['missing_count']}",
            "",
        ]

        if result['missing_anchors']:
            lines.append("MISSING ANCHORS:")
            for anchor in result['missing_anchors']:
                lines.append(f"  - {anchor['summary']} ({anchor['subsection']})")
            lines.append("")

        if result['frontload_violations']:
            lines.append("FRONTLOAD VIOLATIONS:")
            for v in result['frontload_violations']:
                lines.append(f"  - {v['anchor']}: slide {v['first_appearance']}")
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"STATUS: {'PASS' if result['valid'] else 'FAIL'}")
        lines.append("=" * 60)

        return '\n'.join(lines)


def parse_blueprint_coverage(blueprint_content: str) -> Dict[str, List[int]]:
    """
    Parse blueprint file to extract anchor coverage.

    Args:
        blueprint_content: Raw blueprint text

    Returns:
        Dict mapping anchor summaries to slide numbers
    """
    coverage = {}

    # Pattern to match slide and its anchors
    slide_pattern = r'SLIDE (\d+):.*?Anchors Covered:\s*(.+?)(?=\n\n|\nHEADER:)'

    for match in re.finditer(slide_pattern, blueprint_content, re.DOTALL):
        slide_num = int(match.group(1))
        anchors_text = match.group(2).strip()

        # Parse comma-separated or newline-separated anchors
        anchors = [a.strip() for a in re.split(r'[,\n]', anchors_text) if a.strip()]

        for anchor in anchors:
            if anchor not in coverage:
                coverage[anchor] = []
            coverage[anchor].append(slide_num)

    return coverage


if __name__ == "__main__":
    # Test with sample input
    sample_input = {
        "section": {
            "subsections": [
                {
                    "subsection_name": "Hand Hygiene",
                    "anchors": [
                        {"anchor_number": 1, "anchor_summary": "Hand hygiene principles", "flags": ["FRONTLOAD"]},
                        {"anchor_number": 2, "anchor_summary": "ABHR vs soap and water", "flags": []},
                    ]
                },
                {
                    "subsection_name": "Precautions",
                    "anchors": [
                        {"anchor_number": 3, "anchor_summary": "Standard precautions", "flags": []},
                        {"anchor_number": 4, "anchor_summary": "Transmission-based", "flags": ["XREF"]},
                    ]
                }
            ]
        }
    }

    tracker = AnchorCoverageTracker.from_input(sample_input)

    # Simulate coverage
    tracker.mark_covered(["Hand hygiene principles"], slide_number=2)
    tracker.mark_covered(["ABHR vs soap and water"], slide_number=3)
    tracker.mark_covered(["Standard precautions"], slide_number=4)
    # Note: "Transmission-based" not covered

    print(tracker.get_coverage_report())
