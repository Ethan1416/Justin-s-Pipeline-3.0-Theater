"""
Outline Builder - Build section outline structure for NCLEX pipeline.

This module creates the section outline structure used in Step 4 (Outline Generation).
It organizes anchors into balanced sections with appropriate slide count estimates.

Usage:
    from skills.generation.outline_builder import OutlineBuilder

    builder = OutlineBuilder()
    outline = builder.build_outline(anchors, domain="medical_surgical")
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Section:
    """Represents a lecture section."""
    section_number: int
    section_name: str
    anchor_ids: List[str] = field(default_factory=list)
    anchor_count: int = 0
    target_slides: int = 0
    theme_keywords: List[str] = field(default_factory=list)
    priority_level: str = "medium"


@dataclass
class Outline:
    """Complete lecture outline."""
    outline_id: str
    domain: str
    domain_id: int
    total_anchors: int
    section_count: int
    sections: List[Section] = field(default_factory=list)
    total_slides_estimate: int = 0
    constraints_met: bool = True
    warnings: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)


class OutlineBuilder:
    """Build section outline structure."""

    # Default constraints (from constraints.yaml)
    DEFAULT_MIN_SECTIONS = 4
    DEFAULT_MAX_SECTIONS = 12
    DEFAULT_ANCHORS_PER_SECTION_MIN = 15
    DEFAULT_ANCHORS_PER_SECTION_MAX = 20
    DEFAULT_SLIDES_PER_SECTION_MIN = 12
    DEFAULT_SLIDES_PER_SECTION_MAX = 35
    DEFAULT_TOTAL_SLIDES_MIN = 144
    DEFAULT_TOTAL_SLIDES_MAX = 180

    # Domain information
    DOMAINS = {
        'fundamentals': {'id': 1, 'name': 'Fundamentals of Nursing'},
        'pharmacology': {'id': 2, 'name': 'Pharmacology'},
        'medical_surgical': {'id': 3, 'name': 'Medical-Surgical Nursing'},
        'ob_maternity': {'id': 4, 'name': 'OB/Maternity Nursing'},
        'pediatric': {'id': 5, 'name': 'Pediatric Nursing'},
        'mental_health': {'id': 6, 'name': 'Mental Health Nursing'}
    }

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the OutlineBuilder.

        Args:
            config_path: Optional path to constraints.yaml
        """
        self.config_path = config_path
        self.constraints = self._load_constraints()

    def _load_constraints(self) -> Dict:
        """Load constraints from configuration."""
        try:
            from skills.utilities.yaml_parser import load_constraints
            return load_constraints()
        except ImportError:
            return {}

    def build_outline(
        self,
        anchors: List[Dict],
        domain: str = "fundamentals",
        clusters: Optional[List[Dict]] = None,
        priority_rankings: Optional[List[Dict]] = None
    ) -> Outline:
        """
        Build a complete section outline.

        Args:
            anchors: List of anchor dictionaries
            domain: NCLEX domain for this content
            clusters: Optional pre-computed clusters
            priority_rankings: Optional priority rankings

        Returns:
            Outline with sections
        """
        # Generate outline ID
        outline_id = f"outline_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Get domain info
        domain_info = self.DOMAINS.get(domain, {'id': 1, 'name': domain})

        # Calculate optimal section count
        section_count = self._calculate_section_count(len(anchors))

        # Create sections
        if clusters:
            sections = self._create_sections_from_clusters(
                anchors, clusters, section_count
            )
        else:
            sections = self._create_sections_balanced(
                anchors, section_count, priority_rankings
            )

        # Calculate slide estimates
        total_slides = 0
        for section in sections:
            section.target_slides = self._estimate_slides(section.anchor_count)
            total_slides += section.target_slides

        # Check constraints
        warnings = []
        constraints_met = True

        sections_config = self.constraints.get('sections', {})
        slides_config = self.constraints.get('slides', {})

        min_sections = sections_config.get('min', self.DEFAULT_MIN_SECTIONS)
        max_sections = sections_config.get('max', self.DEFAULT_MAX_SECTIONS)

        if section_count < min_sections:
            warnings.append(f"Section count {section_count} below minimum {min_sections}")
            constraints_met = False
        elif section_count > max_sections:
            warnings.append(f"Section count {section_count} above maximum {max_sections}")
            constraints_met = False

        total_min = slides_config.get('total', {}).get('min', self.DEFAULT_TOTAL_SLIDES_MIN)
        total_max = slides_config.get('total', {}).get('max', self.DEFAULT_TOTAL_SLIDES_MAX)

        if total_slides < total_min:
            warnings.append(f"Total slides {total_slides} below minimum {total_min}")
        elif total_slides > total_max:
            warnings.append(f"Total slides {total_slides} above maximum {total_max}")

        return Outline(
            outline_id=outline_id,
            domain=domain,
            domain_id=domain_info['id'],
            total_anchors=len(anchors),
            section_count=len(sections),
            sections=sections,
            total_slides_estimate=total_slides,
            constraints_met=constraints_met,
            warnings=warnings,
            metadata={
                'created': datetime.now().isoformat(),
                'domain_name': domain_info['name'],
                'avg_anchors_per_section': len(anchors) / len(sections) if sections else 0
            }
        )

    def _calculate_section_count(self, total_anchors: int) -> int:
        """Calculate optimal section count."""
        # Formula: total_anchors / 17.5 (midpoint of 15-20)
        target = 17.5
        raw_count = total_anchors / target

        # Round and clamp
        section_count = round(raw_count)
        section_count = max(self.DEFAULT_MIN_SECTIONS, section_count)
        section_count = min(self.DEFAULT_MAX_SECTIONS, section_count)

        return section_count

    def _estimate_slides(self, anchor_count: int) -> int:
        """Estimate slides needed for anchor count."""
        # Rough estimate: 1.5 slides per anchor + intro/summary
        estimate = int(anchor_count * 1.5) + 2

        # Clamp to constraints
        estimate = max(self.DEFAULT_SLIDES_PER_SECTION_MIN, estimate)
        estimate = min(self.DEFAULT_SLIDES_PER_SECTION_MAX, estimate)

        return estimate

    def _create_sections_balanced(
        self,
        anchors: List[Dict],
        section_count: int,
        priority_rankings: Optional[List[Dict]] = None
    ) -> List[Section]:
        """Create balanced sections without cluster data."""
        sections = []

        # Calculate distribution
        base_per_section = len(anchors) // section_count
        remainder = len(anchors) % section_count

        # Sort by priority if available
        if priority_rankings:
            priority_map = {r.get('anchor_id', r.get('id')): r.get('priority_score', 50)
                          for r in priority_rankings}
            anchors = sorted(anchors,
                           key=lambda a: priority_map.get(a.get('id', ''), 50),
                           reverse=True)

        # Distribute anchors
        current_idx = 0
        for i in range(section_count):
            section_size = base_per_section + (1 if i < remainder else 0)
            section_anchors = anchors[current_idx:current_idx + section_size]

            # Generate section name from anchor titles
            section_name = self._generate_section_name(section_anchors, i + 1)

            # Extract keywords
            keywords = self._extract_keywords(section_anchors)

            section = Section(
                section_number=i + 1,
                section_name=section_name,
                anchor_ids=[a.get('id', f'anchor_{j}')
                           for j, a in enumerate(section_anchors, current_idx)],
                anchor_count=len(section_anchors),
                theme_keywords=keywords[:5]
            )
            sections.append(section)
            current_idx += section_size

        return sections

    def _create_sections_from_clusters(
        self,
        anchors: List[Dict],
        clusters: List[Dict],
        target_section_count: int
    ) -> List[Section]:
        """Create sections based on pre-computed clusters."""
        sections = []
        used_anchors = set()

        # Use clusters as section basis
        for i, cluster in enumerate(clusters[:target_section_count]):
            anchor_ids = cluster.get('anchor_ids', [])

            section = Section(
                section_number=i + 1,
                section_name=cluster.get('theme', f'Section {i + 1}').title(),
                anchor_ids=anchor_ids,
                anchor_count=len(anchor_ids),
                theme_keywords=cluster.get('keywords', [])[:5]
            )
            sections.append(section)
            used_anchors.update(anchor_ids)

        # Handle unclustered anchors
        all_ids = {a.get('id', f'anchor_{i}') for i, a in enumerate(anchors)}
        unclustered = all_ids - used_anchors

        if unclustered:
            # Add to existing sections or create new one
            if len(sections) < target_section_count:
                section = Section(
                    section_number=len(sections) + 1,
                    section_name="Additional Topics",
                    anchor_ids=list(unclustered),
                    anchor_count=len(unclustered)
                )
                sections.append(section)
            else:
                # Distribute among existing sections
                unclustered_list = list(unclustered)
                for i, anchor_id in enumerate(unclustered_list):
                    target_section = i % len(sections)
                    sections[target_section].anchor_ids.append(anchor_id)
                    sections[target_section].anchor_count += 1

        return sections

    def _generate_section_name(self, anchors: List[Dict], section_num: int) -> str:
        """Generate a descriptive section name from anchors."""
        if not anchors:
            return f"Section {section_num}"

        # Extract common theme from titles
        titles = [a.get('title', '') for a in anchors]
        words = []

        for title in titles:
            title_words = title.lower().split()
            words.extend([w for w in title_words if len(w) > 3])

        if not words:
            return f"Section {section_num}"

        # Find most common significant word
        word_counts = {}
        stop_words = {'the', 'and', 'for', 'with', 'from', 'that', 'this'}

        for word in words:
            if word not in stop_words:
                word_counts[word] = word_counts.get(word, 0) + 1

        if word_counts:
            common_word = max(word_counts.items(), key=lambda x: x[1])[0]
            return common_word.title()

        return f"Section {section_num}"

    def _extract_keywords(self, anchors: List[Dict]) -> List[str]:
        """Extract keywords from anchor content."""
        all_words = []
        stop_words = {'the', 'and', 'or', 'of', 'in', 'to', 'a', 'for', 'is', 'on', 'with'}

        for anchor in anchors:
            title = anchor.get('title', '').lower()
            content = anchor.get('full_text', '').lower()

            words = re.findall(r'\b[a-z]+\b', f"{title} {content}")
            all_words.extend([w for w in words if len(w) > 3 and w not in stop_words])

        # Count and sort
        word_counts = {}
        for word in all_words:
            word_counts[word] = word_counts.get(word, 0) + 1

        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [w for w, c in sorted_words[:10]]

    def export_to_dict(self, outline: Outline) -> Dict:
        """Export outline to dictionary format."""
        return {
            'outline_id': outline.outline_id,
            'domain': outline.domain,
            'domain_id': outline.domain_id,
            'total_anchors': outline.total_anchors,
            'section_count': outline.section_count,
            'total_slides_estimate': outline.total_slides_estimate,
            'constraints_met': outline.constraints_met,
            'warnings': outline.warnings,
            'metadata': outline.metadata,
            'sections': [
                {
                    'section_number': s.section_number,
                    'section_name': s.section_name,
                    'anchor_ids': s.anchor_ids,
                    'anchor_count': s.anchor_count,
                    'target_slides': s.target_slides,
                    'theme_keywords': s.theme_keywords
                }
                for s in outline.sections
            ]
        }

    def format_report(self, outline: Outline) -> str:
        """Format outline as report."""
        lines = [
            "=" * 60,
            "LECTURE OUTLINE",
            "=" * 60,
            f"Outline ID: {outline.outline_id}",
            f"Domain: {outline.metadata.get('domain_name', outline.domain)}",
            f"Total Anchors: {outline.total_anchors}",
            f"Sections: {outline.section_count}",
            f"Estimated Slides: {outline.total_slides_estimate}",
            f"Constraints Met: {'Yes' if outline.constraints_met else 'No'}",
            ""
        ]

        if outline.warnings:
            lines.append("WARNINGS:")
            for warn in outline.warnings:
                lines.append(f"  - {warn}")
            lines.append("")

        lines.append("-" * 60)
        lines.append("SECTIONS:")
        for section in outline.sections:
            lines.append(f"\n  Section {section.section_number}: {section.section_name}")
            lines.append(f"    Anchors: {section.anchor_count}")
            lines.append(f"    Target Slides: {section.target_slides}")
            if section.theme_keywords:
                lines.append(f"    Keywords: {', '.join(section.theme_keywords[:3])}")
            if section.anchor_ids:
                lines.append(f"    Anchor IDs: {', '.join(section.anchor_ids[:5])}")
                if len(section.anchor_ids) > 5:
                    lines.append(f"      ... and {len(section.anchor_ids) - 5} more")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def build_outline(anchors: List[Dict], domain: str = "fundamentals") -> Outline:
    """Convenience function to build outline."""
    builder = OutlineBuilder()
    return builder.build_outline(anchors, domain)


if __name__ == "__main__":
    print("Outline Builder - NCLEX Pipeline Generation Skill")
    print("=" * 50)

    builder = OutlineBuilder()

    # Demo with sample anchors
    sample_anchors = [
        {'id': f'anchor_{i}', 'title': f'Topic {i}: Sample Content', 'full_text': f'Content for topic {i}...'}
        for i in range(1, 76)  # 75 anchors
    ]

    print(f"\nBuilding outline for {len(sample_anchors)} anchors...")
    outline = builder.build_outline(sample_anchors, domain="medical_surgical")

    report = builder.format_report(outline)
    print(report)
