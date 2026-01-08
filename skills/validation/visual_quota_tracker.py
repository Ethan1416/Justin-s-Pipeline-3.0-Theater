"""
Visual Quota Tracker
Tracks and validates visual aid quota compliance.

Usage:
    from skills.validation.visual_quota_tracker import (
        VisualQuotaTracker, check_quota, get_quota_requirements
    )
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class QuotaStatus(Enum):
    """Visual quota compliance status."""
    PASS = "PASS"
    BELOW_MINIMUM = "BELOW_MINIMUM"
    BELOW_TARGET = "BELOW_TARGET"
    AT_TARGET = "AT_TARGET"
    ABOVE_TARGET = "ABOVE_TARGET"
    EXCEEDS_MAXIMUM = "EXCEEDS_MAXIMUM"


# Quota definitions by slide count range
VISUAL_QUOTAS = {
    (12, 15): {'minimum': 2, 'target_min': 3, 'target_max': 4, 'maximum': 6},
    (16, 20): {'minimum': 3, 'target_min': 4, 'target_max': 5, 'maximum': 8},
    (21, 25): {'minimum': 3, 'target_min': 5, 'target_max': 6, 'maximum': 10},
    (26, 35): {'minimum': 4, 'target_min': 6, 'target_max': 8, 'maximum': 14},
}

# Maximum percentage of slides that can be visuals
MAX_VISUAL_PERCENTAGE = 0.40  # 40%


@dataclass
class VisualQuotaTracker:
    """Tracks visual quota for a section."""
    section_name: str
    total_slides: int
    visuals: List[Dict[str, Any]] = field(default_factory=list)

    def add_visual(self, slide_number: int, visual_type: str):
        """Add a visual to tracking."""
        self.visuals.append({
            'slide_number': slide_number,
            'visual_type': visual_type
        })

    @property
    def visual_count(self) -> int:
        """Get current visual count."""
        return len(self.visuals)

    @property
    def visual_percentage(self) -> float:
        """Get visual percentage of total slides."""
        if self.total_slides == 0:
            return 0.0
        return self.visual_count / self.total_slides

    def get_quota(self) -> Dict[str, int]:
        """Get quota requirements for this section's slide count."""
        return get_quota_requirements(self.total_slides)

    def check_status(self) -> QuotaStatus:
        """Check current quota status."""
        return check_quota(self.total_slides, self.visual_count)

    def validate(self) -> Dict[str, Any]:
        """
        Validate visual quota compliance.

        Returns:
            Validation result with status and details
        """
        quota = self.get_quota()
        status = self.check_status()

        return {
            'status': status.value,
            'valid': status in [QuotaStatus.PASS, QuotaStatus.AT_TARGET, QuotaStatus.ABOVE_TARGET],
            'visual_count': self.visual_count,
            'total_slides': self.total_slides,
            'percentage': f"{self.visual_percentage * 100:.1f}%",
            'quota': quota,
            'visuals': self.visuals,
            'issues': self._get_issues(status, quota)
        }

    def _get_issues(self, status: QuotaStatus, quota: Dict[str, int]) -> List[str]:
        """Get list of issues based on status."""
        issues = []

        if status == QuotaStatus.BELOW_MINIMUM:
            issues.append(f"Only {self.visual_count} visuals, minimum is {quota['minimum']}")
        elif status == QuotaStatus.BELOW_TARGET:
            issues.append(f"Below target range ({quota['target_min']}-{quota['target_max']})")
        elif status == QuotaStatus.EXCEEDS_MAXIMUM:
            issues.append(f"Exceeds maximum ({quota['maximum']} visuals or {MAX_VISUAL_PERCENTAGE*100}%)")

        if self.visual_percentage > MAX_VISUAL_PERCENTAGE:
            issues.append(f"Visual percentage {self.visual_percentage*100:.1f}% exceeds 40% limit")

        return issues


def get_quota_requirements(slide_count: int) -> Dict[str, int]:
    """
    Get quota requirements for a given slide count.

    Args:
        slide_count: Total number of slides

    Returns:
        Dict with minimum, target_min, target_max, maximum
    """
    for (low, high), quota in VISUAL_QUOTAS.items():
        if low <= slide_count <= high:
            return quota

    # Default for out-of-range
    if slide_count < 12:
        return {'minimum': 1, 'target_min': 2, 'target_max': 3, 'maximum': 4}
    else:  # > 35
        return {'minimum': 5, 'target_min': 8, 'target_max': 10, 'maximum': 15}


def check_quota(slide_count: int, visual_count: int) -> QuotaStatus:
    """
    Check if visual count meets quota for slide count.

    Args:
        slide_count: Total number of slides
        visual_count: Number of visuals

    Returns:
        QuotaStatus indicating compliance level
    """
    quota = get_quota_requirements(slide_count)
    percentage = visual_count / slide_count if slide_count > 0 else 0

    # Check percentage limit first
    if percentage > MAX_VISUAL_PERCENTAGE:
        return QuotaStatus.EXCEEDS_MAXIMUM

    # Check against quota
    if visual_count < quota['minimum']:
        return QuotaStatus.BELOW_MINIMUM
    elif visual_count < quota['target_min']:
        return QuotaStatus.BELOW_TARGET
    elif visual_count <= quota['target_max']:
        return QuotaStatus.AT_TARGET
    elif visual_count <= quota['maximum']:
        return QuotaStatus.ABOVE_TARGET
    else:
        return QuotaStatus.EXCEEDS_MAXIMUM


def needs_more_visuals(slide_count: int, visual_count: int) -> int:
    """
    Calculate how many more visuals needed to meet minimum.

    Args:
        slide_count: Total slides
        visual_count: Current visual count

    Returns:
        Number of additional visuals needed (0 if quota met)
    """
    quota = get_quota_requirements(slide_count)
    needed = quota['minimum'] - visual_count
    return max(0, needed)


if __name__ == "__main__":
    # Test
    tracker = VisualQuotaTracker(
        section_name="Infection Control",
        total_slides=18
    )

    # Add some visuals
    tracker.add_visual(3, "TABLE")
    tracker.add_visual(7, "FLOWCHART")
    tracker.add_visual(12, "DECISION_TREE")

    result = tracker.validate()
    print(f"Status: {result['status']}")
    print(f"Visual count: {result['visual_count']}/{result['total_slides']}")
    print(f"Percentage: {result['percentage']}")
    print(f"Valid: {result['valid']}")
    print(f"Issues: {result['issues']}")
