"""
Section Calculator - Calculate section count for NCLEX pipeline.

This module calculates the appropriate number of lecture sections based on
the total anchor count, using the formula: total_anchors / 15-20.

The section count determines how content is divided into manageable lecture
units within the constraints defined in config/constraints.yaml.

Usage:
    from skills.utilities.section_calculator import SectionCalculator

    calculator = SectionCalculator()
    result = calculator.calculate_sections(total_anchors=75)
"""

import yaml
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SectionCalculation:
    """Container for section calculation results."""
    total_anchors: int
    section_count: int
    anchors_per_section: float
    min_sections: int
    max_sections: int
    slides_per_section_estimate: int
    total_slides_estimate: int
    within_constraints: bool
    warnings: list
    formula_used: str


class SectionCalculator:
    """Calculate section count based on anchor count and constraints."""

    # Default constraints (fallback if config not loaded)
    DEFAULT_MIN_SECTIONS = 4
    DEFAULT_MAX_SECTIONS = 12
    DEFAULT_ANCHORS_PER_SECTION_MIN = 15
    DEFAULT_ANCHORS_PER_SECTION_MAX = 20
    DEFAULT_SLIDES_PER_SECTION_MIN = 12
    DEFAULT_SLIDES_PER_SECTION_MAX = 35
    DEFAULT_TOTAL_SLIDES_MIN = 144
    DEFAULT_TOTAL_SLIDES_MAX = 180

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the SectionCalculator.

        Args:
            config_path: Optional path to constraints.yaml config file
        """
        self.config = self._load_config(config_path)

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """
        Load constraints configuration.

        Args:
            config_path: Path to constraints.yaml

        Returns:
            Configuration dictionary
        """
        if config_path is None:
            # Try to find config relative to this file
            base_path = Path(__file__).parent.parent.parent
            config_path = base_path / "config" / "constraints.yaml"
        else:
            config_path = Path(config_path)

        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")

        return {}

    def get_section_constraints(self) -> Tuple[int, int]:
        """
        Get section count constraints from config.

        Returns:
            Tuple of (min_sections, max_sections)
        """
        sections_config = self.config.get('sections', {})
        min_sections = sections_config.get('min', self.DEFAULT_MIN_SECTIONS)
        max_sections = sections_config.get('max', self.DEFAULT_MAX_SECTIONS)
        return min_sections, max_sections

    def get_slide_constraints(self) -> Dict:
        """
        Get slide count constraints from config.

        Returns:
            Dictionary with slide constraints
        """
        slides_config = self.config.get('slides', {})
        return {
            'section_min': slides_config.get('section', {}).get('min_default', self.DEFAULT_SLIDES_PER_SECTION_MIN),
            'section_max': slides_config.get('section', {}).get('max', self.DEFAULT_SLIDES_PER_SECTION_MAX),
            'total_min': slides_config.get('total', {}).get('min', self.DEFAULT_TOTAL_SLIDES_MIN),
            'total_max': slides_config.get('total', {}).get('max', self.DEFAULT_TOTAL_SLIDES_MAX),
        }

    def calculate_sections(
        self,
        total_anchors: int,
        target_anchors_per_section: Optional[int] = None
    ) -> SectionCalculation:
        """
        Calculate optimal section count for given anchor count.

        Uses formula: section_count = total_anchors / (15-20)
        Then clamps to configured min/max section constraints.

        Args:
            total_anchors: Total number of anchor points
            target_anchors_per_section: Optional override for anchors per section

        Returns:
            SectionCalculation with results and recommendations
        """
        min_sections, max_sections = self.get_section_constraints()
        slide_constraints = self.get_slide_constraints()
        warnings = []

        # Determine anchors per section target
        if target_anchors_per_section:
            divisor = target_anchors_per_section
        else:
            # Use midpoint of 15-20 range
            divisor = (self.DEFAULT_ANCHORS_PER_SECTION_MIN +
                      self.DEFAULT_ANCHORS_PER_SECTION_MAX) / 2  # 17.5

        # Calculate raw section count
        raw_section_count = total_anchors / divisor

        # Round to nearest integer
        section_count = round(raw_section_count)

        # Apply constraints
        if section_count < min_sections:
            warnings.append(
                f"Calculated {section_count} sections, adjusted to minimum {min_sections}"
            )
            section_count = min_sections
        elif section_count > max_sections:
            warnings.append(
                f"Calculated {section_count} sections, adjusted to maximum {max_sections}"
            )
            section_count = max_sections

        # Calculate anchors per section after adjustment
        anchors_per_section = total_anchors / section_count if section_count > 0 else 0

        # Estimate slides per section
        # Rough estimate: 1-2 slides per anchor, plus intro/summary
        slides_per_section = int(anchors_per_section * 1.5) + 2
        slides_per_section = max(slide_constraints['section_min'],
                                min(slide_constraints['section_max'], slides_per_section))

        # Calculate total slides estimate
        total_slides = section_count * slides_per_section

        # Check total slides constraint
        within_constraints = True
        if total_slides < slide_constraints['total_min']:
            warnings.append(
                f"Estimated {total_slides} slides is below minimum {slide_constraints['total_min']}"
            )
            within_constraints = False
        elif total_slides > slide_constraints['total_max']:
            warnings.append(
                f"Estimated {total_slides} slides exceeds maximum {slide_constraints['total_max']}"
            )
            within_constraints = False

        # Check anchors per section balance
        if anchors_per_section < self.DEFAULT_ANCHORS_PER_SECTION_MIN:
            warnings.append(
                f"Low anchor density: {anchors_per_section:.1f} anchors/section "
                f"(recommend {self.DEFAULT_ANCHORS_PER_SECTION_MIN}-{self.DEFAULT_ANCHORS_PER_SECTION_MAX})"
            )
        elif anchors_per_section > self.DEFAULT_ANCHORS_PER_SECTION_MAX:
            warnings.append(
                f"High anchor density: {anchors_per_section:.1f} anchors/section "
                f"(recommend {self.DEFAULT_ANCHORS_PER_SECTION_MIN}-{self.DEFAULT_ANCHORS_PER_SECTION_MAX})"
            )

        return SectionCalculation(
            total_anchors=total_anchors,
            section_count=section_count,
            anchors_per_section=anchors_per_section,
            min_sections=min_sections,
            max_sections=max_sections,
            slides_per_section_estimate=slides_per_section,
            total_slides_estimate=total_slides,
            within_constraints=within_constraints,
            warnings=warnings,
            formula_used=f"total_anchors ({total_anchors}) / {divisor} = {raw_section_count:.1f} -> {section_count}"
        )

    def distribute_anchors(
        self,
        total_anchors: int,
        section_count: int,
        section_names: Optional[list] = None
    ) -> list:
        """
        Distribute anchors evenly across sections.

        Args:
            total_anchors: Total anchor count
            section_count: Number of sections
            section_names: Optional list of section names

        Returns:
            List of section dictionaries with anchor allocations
        """
        if section_count <= 0:
            return []

        # Base anchors per section
        base_anchors = total_anchors // section_count
        remainder = total_anchors % section_count

        sections = []
        anchor_start = 1

        for i in range(section_count):
            # Distribute remainder to first sections
            section_anchors = base_anchors + (1 if i < remainder else 0)

            section_name = (section_names[i] if section_names and i < len(section_names)
                          else f"Section {i + 1}")

            sections.append({
                'section_number': i + 1,
                'section_name': section_name,
                'anchor_count': section_anchors,
                'anchor_start': anchor_start,
                'anchor_end': anchor_start + section_anchors - 1,
                'anchor_ids': [f"anchor_{j}" for j in range(anchor_start, anchor_start + section_anchors)]
            })

            anchor_start += section_anchors

        return sections

    def calculate_for_5plus_sections(self, total_anchors: int) -> SectionCalculation:
        """
        Calculate sections with adjusted minimum for 5+ section scenarios.

        Per constraints.yaml, if there are 5+ sections, minimum slides
        per section can be 10 instead of 12.

        Args:
            total_anchors: Total anchor count

        Returns:
            SectionCalculation with adjusted constraints
        """
        result = self.calculate_sections(total_anchors)

        # Check if we have 5+ sections
        if result.section_count >= 5:
            slides_config = self.config.get('slides', {}).get('section', {})
            adjusted_min = slides_config.get('min_if_5plus_sections', 10)

            # Recalculate with adjusted minimum
            result.slides_per_section_estimate = max(
                adjusted_min,
                min(35, int(result.anchors_per_section * 1.5) + 2)
            )
            result.total_slides_estimate = result.section_count * result.slides_per_section_estimate

        return result


def calculate_sections(total_anchors: int) -> SectionCalculation:
    """
    Convenience function to calculate sections.

    Args:
        total_anchors: Total anchor count

    Returns:
        SectionCalculation with results
    """
    calculator = SectionCalculator()
    return calculator.calculate_sections(total_anchors)


if __name__ == "__main__":
    import sys

    print("Section Calculator - NCLEX Pipeline Utility")
    print("=" * 50)

    calculator = SectionCalculator()

    # Get anchor count from command line or use demo values
    if len(sys.argv) > 1:
        try:
            anchor_count = int(sys.argv[1])
        except ValueError:
            print(f"Invalid anchor count: {sys.argv[1]}")
            sys.exit(1)
    else:
        anchor_count = 75  # Demo value

    print(f"\nCalculating sections for {anchor_count} anchors...")
    print()

    result = calculator.calculate_sections(anchor_count)

    print(f"Formula: {result.formula_used}")
    print()
    print(f"Results:")
    print(f"  Section count: {result.section_count}")
    print(f"  Anchors per section: {result.anchors_per_section:.1f}")
    print(f"  Slides per section (est): {result.slides_per_section_estimate}")
    print(f"  Total slides (est): {result.total_slides_estimate}")
    print(f"  Within constraints: {'Yes' if result.within_constraints else 'No'}")

    if result.warnings:
        print()
        print("Warnings:")
        for warn in result.warnings:
            print(f"  - {warn}")

    # Show distribution
    print()
    print("Anchor Distribution:")
    sections = calculator.distribute_anchors(anchor_count, result.section_count)
    for section in sections:
        print(f"  {section['section_name']}: {section['anchor_count']} anchors "
              f"(#{section['anchor_start']}-{section['anchor_end']})")
