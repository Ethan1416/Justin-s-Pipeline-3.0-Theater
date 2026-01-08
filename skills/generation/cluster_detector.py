"""
Cluster Detector - Identify related anchor clusters for NCLEX pipeline.

This module identifies clusters of related anchor points based on content
similarity, keyword overlap, and thematic connections. Used in Phase 2
of the 5-Phase content analysis.

Usage:
    from skills.generation.cluster_detector import ClusterDetector

    detector = ClusterDetector()
    clusters = detector.detect_clusters(anchors)
"""

import re
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Cluster:
    """Represents a cluster of related anchors."""
    cluster_id: str
    theme: str
    anchor_ids: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    cohesion_score: float = 0.0
    size: int = 0


@dataclass
class ClusteringResult:
    """Container for clustering results."""
    total_anchors: int
    total_clusters: int
    clusters: List[Cluster] = field(default_factory=list)
    unclustered_anchors: List[str] = field(default_factory=list)
    coverage_percent: float = 0.0
    metrics: Dict = field(default_factory=dict)


class ClusterDetector:
    """Detect clusters of related anchors."""

    # Stop words to exclude from keyword analysis
    STOP_WORDS = {
        'the', 'and', 'or', 'of', 'in', 'to', 'a', 'an', 'for', 'is', 'on',
        'with', 'by', 'as', 'at', 'from', 'be', 'are', 'was', 'were', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'this', 'that', 'these', 'those', 'what', 'which', 'who', 'whom',
        'their', 'there', 'where', 'when', 'why', 'how', 'all', 'each',
        'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'only', 'own', 'same', 'than', 'too', 'very'
    }

    # Minimum cluster size
    MIN_CLUSTER_SIZE = 2

    # Minimum keyword length
    MIN_KEYWORD_LENGTH = 3

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the ClusterDetector.

        Args:
            config_path: Optional path to configuration
        """
        self.config_path = config_path

    def detect_clusters(
        self,
        anchors: List[Dict],
        min_cluster_size: int = None,
        similarity_threshold: float = 0.3
    ) -> ClusteringResult:
        """
        Detect clusters of related anchors.

        Args:
            anchors: List of anchor dictionaries
            min_cluster_size: Minimum anchors per cluster
            similarity_threshold: Minimum similarity for clustering

        Returns:
            ClusteringResult with detected clusters
        """
        if min_cluster_size is None:
            min_cluster_size = self.MIN_CLUSTER_SIZE

        # Step 1: Extract keywords from each anchor
        anchor_keywords = self._extract_anchor_keywords(anchors)

        # Step 2: Build keyword-to-anchor index
        keyword_index = self._build_keyword_index(anchor_keywords)

        # Step 3: Find clusters based on keyword overlap
        clusters = self._cluster_by_keywords(
            anchors, anchor_keywords, keyword_index, min_cluster_size
        )

        # Step 4: Identify unclustered anchors
        clustered_ids = set()
        for cluster in clusters:
            clustered_ids.update(cluster.anchor_ids)

        all_ids = {a.get('id', f'anchor_{i}') for i, a in enumerate(anchors)}
        unclustered = list(all_ids - clustered_ids)

        # Step 5: Calculate coverage and metrics
        coverage = len(clustered_ids) / len(anchors) * 100 if anchors else 0

        return ClusteringResult(
            total_anchors=len(anchors),
            total_clusters=len(clusters),
            clusters=clusters,
            unclustered_anchors=unclustered,
            coverage_percent=coverage,
            metrics={
                'avg_cluster_size': sum(c.size for c in clusters) / len(clusters) if clusters else 0,
                'max_cluster_size': max(c.size for c in clusters) if clusters else 0,
                'min_cluster_size': min(c.size for c in clusters) if clusters else 0,
                'unique_keywords': len(keyword_index)
            }
        )

    def _extract_anchor_keywords(self, anchors: List[Dict]) -> Dict[str, Set[str]]:
        """
        Extract keywords from each anchor.

        Args:
            anchors: List of anchors

        Returns:
            Dictionary mapping anchor ID to set of keywords
        """
        anchor_keywords = {}

        for i, anchor in enumerate(anchors):
            anchor_id = anchor.get('id', f'anchor_{i}')
            title = anchor.get('title', '').lower()
            content = anchor.get('full_text', '').lower()

            # Extract words from title and content
            all_text = f"{title} {content}"
            words = re.findall(r'\b[a-z]+\b', all_text)

            # Filter to meaningful keywords
            keywords = {
                w for w in words
                if len(w) >= self.MIN_KEYWORD_LENGTH
                and w not in self.STOP_WORDS
            }

            anchor_keywords[anchor_id] = keywords

        return anchor_keywords

    def _build_keyword_index(
        self,
        anchor_keywords: Dict[str, Set[str]]
    ) -> Dict[str, Set[str]]:
        """
        Build inverted index from keywords to anchor IDs.

        Args:
            anchor_keywords: Dict mapping anchor ID to keywords

        Returns:
            Dict mapping keyword to set of anchor IDs
        """
        index = defaultdict(set)

        for anchor_id, keywords in anchor_keywords.items():
            for keyword in keywords:
                index[keyword].add(anchor_id)

        return dict(index)

    def _cluster_by_keywords(
        self,
        anchors: List[Dict],
        anchor_keywords: Dict[str, Set[str]],
        keyword_index: Dict[str, Set[str]],
        min_size: int
    ) -> List[Cluster]:
        """
        Create clusters based on keyword overlap.

        Args:
            anchors: List of anchors
            anchor_keywords: Keywords per anchor
            keyword_index: Keyword to anchor index
            min_size: Minimum cluster size

        Returns:
            List of Cluster objects
        """
        clusters = []
        used_anchors = set()

        # Find high-frequency keywords that could be cluster themes
        keyword_freq = [(kw, len(ids)) for kw, ids in keyword_index.items()]
        keyword_freq.sort(key=lambda x: x[1], reverse=True)

        cluster_num = 0
        for keyword, freq in keyword_freq:
            if freq < min_size:
                continue

            # Get anchors with this keyword that haven't been clustered
            anchor_ids = keyword_index[keyword] - used_anchors

            if len(anchor_ids) >= min_size:
                cluster_num += 1

                # Find common keywords among these anchors
                common_keywords = self._find_common_keywords(
                    anchor_ids, anchor_keywords
                )

                # Calculate cohesion score
                cohesion = self._calculate_cohesion(anchor_ids, anchor_keywords)

                cluster = Cluster(
                    cluster_id=f"cluster_{cluster_num}",
                    theme=keyword.title(),
                    anchor_ids=list(anchor_ids),
                    keywords=common_keywords[:5],  # Top 5 keywords
                    cohesion_score=cohesion,
                    size=len(anchor_ids)
                )
                clusters.append(cluster)
                used_anchors.update(anchor_ids)

        return clusters

    def _find_common_keywords(
        self,
        anchor_ids: Set[str],
        anchor_keywords: Dict[str, Set[str]]
    ) -> List[str]:
        """
        Find keywords common to multiple anchors in a cluster.

        Args:
            anchor_ids: Set of anchor IDs in cluster
            anchor_keywords: Keywords per anchor

        Returns:
            List of common keywords sorted by frequency
        """
        keyword_counts = defaultdict(int)

        for anchor_id in anchor_ids:
            keywords = anchor_keywords.get(anchor_id, set())
            for kw in keywords:
                keyword_counts[kw] += 1

        # Sort by count and return
        sorted_kw = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        return [kw for kw, count in sorted_kw if count > 1]

    def _calculate_cohesion(
        self,
        anchor_ids: Set[str],
        anchor_keywords: Dict[str, Set[str]]
    ) -> float:
        """
        Calculate cohesion score for a cluster.

        Cohesion is based on average keyword overlap between anchors.

        Args:
            anchor_ids: Set of anchor IDs
            anchor_keywords: Keywords per anchor

        Returns:
            Cohesion score between 0 and 1
        """
        if len(anchor_ids) < 2:
            return 1.0

        anchor_list = list(anchor_ids)
        total_similarity = 0
        comparisons = 0

        for i in range(len(anchor_list)):
            for j in range(i + 1, len(anchor_list)):
                kw1 = anchor_keywords.get(anchor_list[i], set())
                kw2 = anchor_keywords.get(anchor_list[j], set())

                if kw1 and kw2:
                    # Jaccard similarity
                    intersection = len(kw1 & kw2)
                    union = len(kw1 | kw2)
                    similarity = intersection / union if union > 0 else 0
                    total_similarity += similarity
                    comparisons += 1

        return total_similarity / comparisons if comparisons > 0 else 0

    def merge_small_clusters(
        self,
        clusters: List[Cluster],
        min_size: int = 3
    ) -> List[Cluster]:
        """
        Merge small clusters into larger related ones.

        Args:
            clusters: List of clusters
            min_size: Minimum size after which to stop merging

        Returns:
            List of merged clusters
        """
        if not clusters:
            return []

        # Sort by size descending
        sorted_clusters = sorted(clusters, key=lambda c: c.size, reverse=True)

        merged = []
        small_clusters = []

        for cluster in sorted_clusters:
            if cluster.size >= min_size:
                merged.append(cluster)
            else:
                small_clusters.append(cluster)

        # Try to merge small clusters into existing ones
        for small in small_clusters:
            best_match = None
            best_overlap = 0

            for i, large in enumerate(merged):
                # Check keyword overlap
                overlap = len(set(small.keywords) & set(large.keywords))
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_match = i

            if best_match is not None and best_overlap > 0:
                # Merge into best matching cluster
                merged[best_match].anchor_ids.extend(small.anchor_ids)
                merged[best_match].size = len(merged[best_match].anchor_ids)
            else:
                # Keep as separate cluster
                merged.append(small)

        return merged

    def format_report(self, result: ClusteringResult) -> str:
        """Format clustering result as report."""
        lines = [
            "=" * 60,
            "CLUSTER DETECTION REPORT",
            "=" * 60,
            f"Total Anchors: {result.total_anchors}",
            f"Total Clusters: {result.total_clusters}",
            f"Coverage: {result.coverage_percent:.1f}%",
            f"Unclustered: {len(result.unclustered_anchors)}",
            ""
        ]

        if result.metrics:
            lines.append("Metrics:")
            for key, value in result.metrics.items():
                if isinstance(value, float):
                    lines.append(f"  {key}: {value:.2f}")
                else:
                    lines.append(f"  {key}: {value}")
            lines.append("")

        lines.append("-" * 60)
        lines.append("CLUSTERS:")
        for cluster in result.clusters:
            lines.append(f"\n  {cluster.cluster_id}: {cluster.theme}")
            lines.append(f"    Size: {cluster.size}")
            lines.append(f"    Cohesion: {cluster.cohesion_score:.2f}")
            lines.append(f"    Keywords: {', '.join(cluster.keywords[:3])}")
            lines.append(f"    Anchors: {', '.join(cluster.anchor_ids[:5])}")
            if len(cluster.anchor_ids) > 5:
                lines.append(f"      ... and {len(cluster.anchor_ids) - 5} more")

        if result.unclustered_anchors:
            lines.append("")
            lines.append(f"Unclustered: {', '.join(result.unclustered_anchors[:10])}")
            if len(result.unclustered_anchors) > 10:
                lines.append(f"  ... and {len(result.unclustered_anchors) - 10} more")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def detect_clusters(anchors: List[Dict]) -> ClusteringResult:
    """Convenience function to detect clusters."""
    detector = ClusterDetector()
    return detector.detect_clusters(anchors)


if __name__ == "__main__":
    print("Cluster Detector - NCLEX Pipeline Generation Skill")
    print("=" * 50)

    detector = ClusterDetector()

    # Demo with sample anchors
    sample_anchors = [
        {'id': 'a1', 'title': 'Vital Signs Assessment', 'full_text': 'Temperature, pulse, respiration, blood pressure...'},
        {'id': 'a2', 'title': 'Blood Pressure Measurement', 'full_text': 'Techniques for measuring blood pressure...'},
        {'id': 'a3', 'title': 'Temperature Assessment', 'full_text': 'Methods of temperature measurement...'},
        {'id': 'a4', 'title': 'Medication Administration', 'full_text': 'Routes and techniques for medication...'},
        {'id': 'a5', 'title': 'Oral Medication Administration', 'full_text': 'Administering oral medications safely...'},
        {'id': 'a6', 'title': 'Injectable Medications', 'full_text': 'Intramuscular and subcutaneous injections...'},
        {'id': 'a7', 'title': 'Patient Documentation', 'full_text': 'Charting and documentation standards...'},
        {'id': 'a8', 'title': 'Wound Care Assessment', 'full_text': 'Assessing wounds and healing...'},
        {'id': 'a9', 'title': 'Wound Dressing Techniques', 'full_text': 'Types of wound dressings...'},
        {'id': 'a10', 'title': 'Pain Assessment', 'full_text': 'Pain scales and assessment tools...'},
    ]

    print("\nDetecting clusters...")
    result = detector.detect_clusters(sample_anchors)

    report = detector.format_report(result)
    print(report)
