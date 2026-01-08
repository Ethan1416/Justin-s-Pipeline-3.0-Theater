"""
Priority Ranker - Rank content by exam relevance for NCLEX pipeline.

This module ranks anchor content by NCLEX exam relevance based on:
- Client Needs category weights from the NCLEX test plan
- High-yield topic indicators
- Commonly tested content areas
- Critical safety topics

Used in Step 3 (Official Sorting) to prioritize content for lectures.

Usage:
    from skills.generation.priority_ranker import PriorityRanker

    ranker = PriorityRanker()
    result = ranker.rank_anchors(anchors)
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class PriorityRanking:
    """Priority ranking for a single anchor."""
    anchor_id: str
    priority_score: float  # 0-100
    priority_level: str  # "critical", "high", "medium", "low"
    exam_relevance: float  # 0-1
    safety_relevance: bool
    matched_indicators: List[str] = field(default_factory=list)
    client_needs_category: str = ""
    rationale: str = ""


@dataclass
class RankingResult:
    """Container for ranking results."""
    total_anchors: int
    rankings: List[PriorityRanking] = field(default_factory=list)
    priority_distribution: Dict[str, int] = field(default_factory=dict)
    ranked_order: List[str] = field(default_factory=list)
    metrics: Dict = field(default_factory=dict)


class PriorityRanker:
    """Rank content by NCLEX exam relevance."""

    # NCLEX Client Needs Categories with weights (approximate percentage of test)
    CLIENT_NEEDS = {
        'management_of_care': {
            'weight': 0.20,  # 17-23%
            'keywords': [
                'delegation', 'supervision', 'prioritization', 'advocacy',
                'informed consent', 'advance directive', 'confidentiality',
                'ethics', 'legal', 'client rights', 'case management',
                'collaboration', 'referral', 'continuity of care', 'quality'
            ]
        },
        'safety_infection_control': {
            'weight': 0.12,  # 9-15%
            'keywords': [
                'safety', 'infection control', 'standard precautions',
                'hand hygiene', 'isolation', 'sterile technique', 'asepsis',
                'fall prevention', 'restraint', 'error prevention',
                'hazardous materials', 'emergency response', 'security'
            ]
        },
        'health_promotion': {
            'weight': 0.09,  # 6-12%
            'keywords': [
                'health promotion', 'disease prevention', 'screening',
                'immunization', 'lifestyle', 'wellness', 'education',
                'developmental', 'aging', 'self-care', 'high risk behavior'
            ]
        },
        'psychosocial_integrity': {
            'weight': 0.09,  # 6-12%
            'keywords': [
                'therapeutic communication', 'coping', 'grief', 'crisis',
                'mental health', 'abuse', 'neglect', 'substance abuse',
                'stress', 'family dynamics', 'support systems', 'cultural'
            ]
        },
        'basic_care_comfort': {
            'weight': 0.09,  # 6-12%
            'keywords': [
                'mobility', 'nutrition', 'elimination', 'hygiene',
                'rest', 'sleep', 'comfort', 'pain management',
                'nonpharmacological', 'assistive device', 'personal care'
            ]
        },
        'pharmacological': {
            'weight': 0.15,  # 12-18%
            'keywords': [
                'medication', 'drug', 'pharmacology', 'dose calculation',
                'side effect', 'adverse effect', 'contraindication',
                'drug interaction', 'blood products', 'parenteral', 'iv'
            ]
        },
        'risk_reduction': {
            'weight': 0.12,  # 9-15%
            'keywords': [
                'complication', 'risk assessment', 'prevention',
                'diagnostic test', 'lab values', 'monitoring',
                'vital signs', 'therapeutic procedure', 'system assessment'
            ]
        },
        'physiological_adaptation': {
            'weight': 0.14,  # 11-17%
            'keywords': [
                'emergency', 'critical care', 'life-threatening',
                'acute', 'chronic', 'pathophysiology', 'hemodynamic',
                'fluid balance', 'medical emergency', 'intervention'
            ]
        }
    }

    # High-yield topic indicators (commonly tested)
    HIGH_YIELD_INDICATORS = [
        'priority', 'first', 'immediate', 'emergency', 'critical',
        'life-threatening', 'safety', 'delegation', 'infection control',
        'medication error', 'adverse effect', 'contraindication',
        'assessment', 'intervention', 'evaluation', 'nursing diagnosis',
        'therapeutic communication', 'patient education', 'discharge'
    ]

    # Safety-critical topics (always high priority)
    SAFETY_CRITICAL = [
        'fall', 'aspiration', 'choking', 'anaphylaxis', 'overdose',
        'medication error', 'wrong patient', 'restraint', 'suicide',
        'violence', 'elopement', 'infection', 'bleeding', 'shock',
        'respiratory distress', 'cardiac arrest', 'seizure', 'stroke',
        'hypoglycemia', 'hyperglycemia', 'electrolyte imbalance'
    ]

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the PriorityRanker.

        Args:
            config_path: Optional path to nclex.yaml config
        """
        self.config_path = config_path

    def rank_anchor(self, anchor: Dict) -> PriorityRanking:
        """
        Calculate priority ranking for a single anchor.

        Args:
            anchor: Anchor dictionary

        Returns:
            PriorityRanking result
        """
        anchor_id = anchor.get('id', 'unknown')
        title = anchor.get('title', '').lower()
        content = anchor.get('full_text', '').lower()
        full_text = f"{title} {content}"

        # Calculate client needs score
        client_needs_score, primary_category, cn_matches = self._score_client_needs(full_text)

        # Calculate high-yield score
        high_yield_score, hy_matches = self._score_high_yield(full_text)

        # Check for safety-critical content
        is_safety_critical, safety_matches = self._check_safety_critical(full_text)

        # Calculate overall priority score
        base_score = (client_needs_score * 0.4) + (high_yield_score * 0.3)

        # Safety multiplier
        if is_safety_critical:
            base_score = min(100, base_score + 30)

        # Title match bonus (content in title is more important)
        title_bonus = 0
        for indicator in self.HIGH_YIELD_INDICATORS:
            if indicator in title:
                title_bonus += 5
        base_score = min(100, base_score + title_bonus)

        # Determine priority level
        if base_score >= 80 or is_safety_critical:
            priority_level = "critical"
        elif base_score >= 60:
            priority_level = "high"
        elif base_score >= 40:
            priority_level = "medium"
        else:
            priority_level = "low"

        # Compile matched indicators
        all_matches = list(set(cn_matches + hy_matches + safety_matches))

        # Generate rationale
        rationale_parts = []
        if is_safety_critical:
            rationale_parts.append("Safety-critical content")
        if primary_category:
            weight = self.CLIENT_NEEDS[primary_category]['weight'] * 100
            rationale_parts.append(f"Client Needs: {primary_category} ({weight:.0f}% of exam)")
        if hy_matches:
            rationale_parts.append(f"High-yield indicators: {', '.join(hy_matches[:3])}")

        return PriorityRanking(
            anchor_id=anchor_id,
            priority_score=round(base_score, 1),
            priority_level=priority_level,
            exam_relevance=client_needs_score / 100,
            safety_relevance=is_safety_critical,
            matched_indicators=all_matches[:10],
            client_needs_category=primary_category,
            rationale="; ".join(rationale_parts) if rationale_parts else "General nursing content"
        )

    def _score_client_needs(self, text: str) -> Tuple[float, str, List[str]]:
        """Score based on Client Needs category matching."""
        category_scores = {}
        category_matches = {}

        for category, info in self.CLIENT_NEEDS.items():
            matches = []
            for keyword in info['keywords']:
                if keyword in text:
                    matches.append(keyword)

            # Weight by category importance on exam
            score = len(matches) * info['weight'] * 20
            category_scores[category] = score
            category_matches[category] = matches

        # Find best category
        if not any(category_scores.values()):
            return 30, '', []  # Base score for unmatched content

        best_category = max(category_scores.items(), key=lambda x: x[1])
        total_score = sum(category_scores.values())

        return min(100, total_score), best_category[0], category_matches[best_category[0]]

    def _score_high_yield(self, text: str) -> Tuple[float, List[str]]:
        """Score based on high-yield indicators."""
        matches = []
        for indicator in self.HIGH_YIELD_INDICATORS:
            if indicator in text:
                matches.append(indicator)

        score = len(matches) * 8  # 8 points per high-yield match
        return min(100, score), matches

    def _check_safety_critical(self, text: str) -> Tuple[bool, List[str]]:
        """Check for safety-critical content."""
        matches = []
        for topic in self.SAFETY_CRITICAL:
            if topic in text:
                matches.append(topic)

        return len(matches) >= 1, matches

    def rank_anchors(self, anchors: List[Dict]) -> RankingResult:
        """
        Rank multiple anchors by priority.

        Args:
            anchors: List of anchor dictionaries

        Returns:
            RankingResult with all rankings
        """
        rankings = []
        priority_distribution = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }

        for anchor in anchors:
            ranking = self.rank_anchor(anchor)
            rankings.append(ranking)
            priority_distribution[ranking.priority_level] += 1

        # Sort by priority score descending
        rankings.sort(key=lambda x: x.priority_score, reverse=True)
        ranked_order = [r.anchor_id for r in rankings]

        # Calculate metrics
        total = len(anchors)
        metrics = {
            'avg_priority_score': sum(r.priority_score for r in rankings) / total if total > 0 else 0,
            'safety_critical_count': sum(1 for r in rankings if r.safety_relevance),
            'high_priority_percent': (priority_distribution['critical'] + priority_distribution['high']) / total * 100 if total > 0 else 0
        }

        return RankingResult(
            total_anchors=total,
            rankings=rankings,
            priority_distribution=priority_distribution,
            ranked_order=ranked_order,
            metrics=metrics
        )

    def get_top_priority(
        self,
        result: RankingResult,
        n: int = 10
    ) -> List[PriorityRanking]:
        """Get top N priority anchors."""
        return result.rankings[:n]

    def filter_by_level(
        self,
        result: RankingResult,
        levels: List[str]
    ) -> List[PriorityRanking]:
        """Filter rankings by priority level."""
        return [r for r in result.rankings if r.priority_level in levels]

    def format_report(self, result: RankingResult) -> str:
        """Format ranking result as report."""
        lines = [
            "=" * 60,
            "PRIORITY RANKING REPORT",
            "=" * 60,
            f"Total Anchors: {result.total_anchors}",
            f"Average Priority Score: {result.metrics.get('avg_priority_score', 0):.1f}",
            f"Safety-Critical Count: {result.metrics.get('safety_critical_count', 0)}",
            ""
        ]

        lines.append("-" * 60)
        lines.append("PRIORITY DISTRIBUTION:")
        for level in ['critical', 'high', 'medium', 'low']:
            count = result.priority_distribution[level]
            percent = count / result.total_anchors * 100 if result.total_anchors > 0 else 0
            bar = "#" * int(percent / 2)
            lines.append(f"  {level.upper():<10} {count:>3} ({percent:>5.1f}%) {bar}")

        lines.append("")
        lines.append("-" * 60)
        lines.append("TOP PRIORITY ANCHORS:")
        for ranking in result.rankings[:10]:
            lines.append(f"\n  {ranking.anchor_id}")
            lines.append(f"    Score: {ranking.priority_score:.1f} ({ranking.priority_level.upper()})")
            if ranking.safety_relevance:
                lines.append(f"    ** SAFETY CRITICAL **")
            if ranking.client_needs_category:
                lines.append(f"    Category: {ranking.client_needs_category}")
            if ranking.matched_indicators:
                lines.append(f"    Indicators: {', '.join(ranking.matched_indicators[:3])}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def rank_anchors(anchors: List[Dict]) -> RankingResult:
    """Convenience function to rank anchors."""
    ranker = PriorityRanker()
    return ranker.rank_anchors(anchors)


if __name__ == "__main__":
    print("Priority Ranker - NCLEX Pipeline Generation Skill")
    print("=" * 50)

    ranker = PriorityRanker()

    # Demo with sample anchors
    sample_anchors = [
        {'id': 'a1', 'title': 'Fall Prevention Safety', 'full_text': 'Fall risk assessment, safety measures, restraint alternatives...'},
        {'id': 'a2', 'title': 'Priority Setting and Delegation', 'full_text': 'Delegation to UAP, prioritization of patient care...'},
        {'id': 'a3', 'title': 'Medication Error Prevention', 'full_text': 'Safe medication administration, rights of medication...'},
        {'id': 'a4', 'title': 'Basic Hygiene Care', 'full_text': 'Bathing, oral care, personal hygiene assistance...'},
        {'id': 'a5', 'title': 'Emergency Response to Anaphylaxis', 'full_text': 'Anaphylactic shock, epinephrine, airway management...'},
        {'id': 'a6', 'title': 'Therapeutic Communication', 'full_text': 'Communication techniques, active listening, empathy...'},
        {'id': 'a7', 'title': 'Infection Control Precautions', 'full_text': 'Standard precautions, isolation, PPE...'},
        {'id': 'a8', 'title': 'Patient Education Principles', 'full_text': 'Teaching methods, learning needs assessment...'},
    ]

    print("\nRanking anchors by NCLEX priority...")
    result = ranker.rank_anchors(sample_anchors)

    report = ranker.format_report(result)
    print(report)
