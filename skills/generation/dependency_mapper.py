"""
Dependency Mapper - Map prerequisite relationships for NCLEX pipeline.

This module identifies prerequisite and dependency relationships between
anchor points to ensure proper ordering in lecture generation. Used in
Phase 3 of the 5-Phase content analysis.

Dependency types:
- prerequisite: A must be taught before B
- builds_on: B expands on concepts from A
- parallel: Can be taught in any order
- optional: A provides helpful but not required background for B

Usage:
    from skills.generation.dependency_mapper import DependencyMapper

    mapper = DependencyMapper()
    result = mapper.map_dependencies(anchors)
"""

import re
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class Dependency:
    """Represents a dependency relationship between anchors."""
    from_anchor: str
    to_anchor: str
    dependency_type: str  # "prerequisite", "builds_on", "parallel", "optional"
    strength: str  # "required", "suggested", "weak"
    reason: str = ""
    confidence: float = 0.0


@dataclass
class DependencyMappingResult:
    """Container for dependency mapping results."""
    total_anchors: int
    total_dependencies: int
    dependencies: List[Dependency] = field(default_factory=list)
    foundational_anchors: List[str] = field(default_factory=list)
    terminal_anchors: List[str] = field(default_factory=list)
    dependency_graph: Dict = field(default_factory=dict)
    suggested_order: List[str] = field(default_factory=list)
    metrics: Dict = field(default_factory=dict)


class DependencyMapper:
    """Map prerequisite and dependency relationships between anchors."""

    # Keywords indicating foundational/introductory content
    FOUNDATIONAL_KEYWORDS = [
        'introduction', 'intro', 'basic', 'basics', 'fundamental', 'fundamentals',
        'overview', 'definition', 'definitions', 'anatomy', 'physiology',
        'principles', 'concepts', 'background', 'foundation', 'review',
        'what is', 'understanding', 'elements', 'components', 'types'
    ]

    # Keywords indicating advanced/complex content
    ADVANCED_KEYWORDS = [
        'advanced', 'complex', 'complicated', 'management', 'intervention',
        'treatment', 'complication', 'complications', 'emergency', 'crisis',
        'critical', 'severe', 'acute', 'chronic', 'evaluation', 'integration',
        'synthesis', 'application', 'implementation', 'monitoring', 'outcomes'
    ]

    # Keywords indicating assessment content (usually comes early)
    ASSESSMENT_KEYWORDS = [
        'assessment', 'assess', 'evaluation', 'evaluate', 'diagnosis',
        'diagnostic', 'signs', 'symptoms', 'presentation', 'manifestations',
        'findings', 'identification', 'screening', 'history', 'examination'
    ]

    # Keywords indicating intervention content (usually comes after assessment)
    INTERVENTION_KEYWORDS = [
        'intervention', 'interventions', 'treatment', 'therapy', 'management',
        'nursing care', 'nursing actions', 'implementation', 'medication',
        'medications', 'procedure', 'procedures', 'prevention', 'education',
        'discharge', 'follow-up', 'outcomes'
    ]

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the DependencyMapper.

        Args:
            config_path: Optional path to configuration
        """
        self.config_path = config_path

    def map_dependencies(
        self,
        anchors: List[Dict],
        include_weak: bool = False
    ) -> DependencyMappingResult:
        """
        Map dependencies between anchors.

        Args:
            anchors: List of anchor dictionaries
            include_weak: Include weak/optional dependencies

        Returns:
            DependencyMappingResult with mapped relationships
        """
        # Step 1: Classify anchors by content type
        classifications = self._classify_anchors(anchors)

        # Step 2: Identify foundational and terminal anchors
        foundational = classifications['foundational']
        advanced = classifications['advanced']
        assessment = classifications['assessment']
        intervention = classifications['intervention']

        # Step 3: Generate dependency relationships
        dependencies = []

        # Foundational -> All others
        dependencies.extend(self._create_foundational_dependencies(
            foundational, anchors, classifications
        ))

        # Assessment -> Intervention
        dependencies.extend(self._create_assessment_intervention_dependencies(
            assessment, intervention
        ))

        # Topic-based dependencies
        dependencies.extend(self._create_topic_dependencies(anchors))

        # Filter weak dependencies if not included
        if not include_weak:
            dependencies = [d for d in dependencies if d.strength != "weak"]

        # Step 4: Build dependency graph
        graph = self._build_dependency_graph(anchors, dependencies)

        # Step 5: Calculate suggested order (topological sort)
        suggested_order = self._calculate_suggested_order(anchors, dependencies)

        # Step 6: Identify terminal anchors (no outgoing dependencies)
        terminal = self._identify_terminal_anchors(anchors, dependencies)

        return DependencyMappingResult(
            total_anchors=len(anchors),
            total_dependencies=len(dependencies),
            dependencies=dependencies,
            foundational_anchors=foundational,
            terminal_anchors=terminal,
            dependency_graph=graph,
            suggested_order=suggested_order,
            metrics={
                'foundational_count': len(foundational),
                'terminal_count': len(terminal),
                'assessment_count': len(assessment),
                'intervention_count': len(intervention),
                'avg_dependencies_per_anchor': len(dependencies) / len(anchors) if anchors else 0
            }
        )

    def _classify_anchors(self, anchors: List[Dict]) -> Dict[str, List[str]]:
        """
        Classify anchors by content type based on keywords.

        Args:
            anchors: List of anchors

        Returns:
            Dict with classified anchor IDs
        """
        classifications = {
            'foundational': [],
            'advanced': [],
            'assessment': [],
            'intervention': [],
            'other': []
        }

        for i, anchor in enumerate(anchors):
            anchor_id = anchor.get('id', f'anchor_{i}')
            title = anchor.get('title', '').lower()
            content = anchor.get('full_text', '').lower()
            full_text = f"{title} {content}"

            # Check each category
            is_foundational = any(kw in full_text for kw in self.FOUNDATIONAL_KEYWORDS)
            is_advanced = any(kw in full_text for kw in self.ADVANCED_KEYWORDS)
            is_assessment = any(kw in full_text for kw in self.ASSESSMENT_KEYWORDS)
            is_intervention = any(kw in full_text for kw in self.INTERVENTION_KEYWORDS)

            # Assign to categories (can be multiple)
            if is_foundational:
                classifications['foundational'].append(anchor_id)
            if is_advanced:
                classifications['advanced'].append(anchor_id)
            if is_assessment:
                classifications['assessment'].append(anchor_id)
            if is_intervention:
                classifications['intervention'].append(anchor_id)

            # If none matched, put in other
            if not any([is_foundational, is_advanced, is_assessment, is_intervention]):
                classifications['other'].append(anchor_id)

        return classifications

    def _create_foundational_dependencies(
        self,
        foundational: List[str],
        anchors: List[Dict],
        classifications: Dict
    ) -> List[Dependency]:
        """Create dependencies from foundational anchors to others."""
        dependencies = []

        # Get non-foundational anchors
        non_foundational = (
            set(classifications['advanced']) |
            set(classifications['other'])
        ) - set(foundational)

        for found_id in foundational:
            for other_id in non_foundational:
                dependencies.append(Dependency(
                    from_anchor=found_id,
                    to_anchor=other_id,
                    dependency_type="builds_on",
                    strength="suggested",
                    reason="Foundational content should precede advanced content",
                    confidence=0.6
                ))

        return dependencies

    def _create_assessment_intervention_dependencies(
        self,
        assessment: List[str],
        intervention: List[str]
    ) -> List[Dependency]:
        """Create dependencies from assessment to intervention anchors."""
        dependencies = []

        # Find pairs with similar topics
        for assess_id in assessment:
            for interv_id in intervention:
                # Skip if same anchor
                if assess_id == interv_id:
                    continue

                dependencies.append(Dependency(
                    from_anchor=assess_id,
                    to_anchor=interv_id,
                    dependency_type="prerequisite",
                    strength="suggested",
                    reason="Assessment typically precedes intervention",
                    confidence=0.7
                ))

        return dependencies

    def _create_topic_dependencies(self, anchors: List[Dict]) -> List[Dependency]:
        """Create dependencies based on topic relationships."""
        dependencies = []
        anchor_map = {a.get('id', f'anchor_{i}'): a for i, a in enumerate(anchors)}

        # Extract topics from titles
        topic_anchors = {}
        for i, anchor in enumerate(anchors):
            anchor_id = anchor.get('id', f'anchor_{i}')
            title = anchor.get('title', '').lower()

            # Extract main topic (first significant word)
            words = [w for w in title.split() if len(w) > 3]
            if words:
                topic = words[0]
                if topic not in topic_anchors:
                    topic_anchors[topic] = []
                topic_anchors[topic].append((anchor_id, title))

        # Within same topic, order by complexity indicators
        for topic, anchor_list in topic_anchors.items():
            if len(anchor_list) < 2:
                continue

            # Sort by complexity (basic/intro first)
            sorted_anchors = sorted(
                anchor_list,
                key=lambda x: self._complexity_score(x[1])
            )

            # Create chain dependencies
            for i in range(len(sorted_anchors) - 1):
                from_id = sorted_anchors[i][0]
                to_id = sorted_anchors[i + 1][0]

                dependencies.append(Dependency(
                    from_anchor=from_id,
                    to_anchor=to_id,
                    dependency_type="builds_on",
                    strength="suggested",
                    reason=f"Same topic '{topic}' - ordered by complexity",
                    confidence=0.5
                ))

        return dependencies

    def _complexity_score(self, title: str) -> int:
        """Calculate complexity score for ordering (lower = simpler)."""
        score = 50  # Base score

        # Lower score for foundational keywords
        for kw in self.FOUNDATIONAL_KEYWORDS:
            if kw in title:
                score -= 20
                break

        # Higher score for advanced keywords
        for kw in self.ADVANCED_KEYWORDS:
            if kw in title:
                score += 20
                break

        return score

    def _build_dependency_graph(
        self,
        anchors: List[Dict],
        dependencies: List[Dependency]
    ) -> Dict:
        """Build adjacency list representation of dependency graph."""
        graph = {
            'nodes': {},
            'edges': []
        }

        # Add nodes
        for i, anchor in enumerate(anchors):
            anchor_id = anchor.get('id', f'anchor_{i}')
            graph['nodes'][anchor_id] = {
                'title': anchor.get('title', ''),
                'incoming': [],
                'outgoing': []
            }

        # Add edges
        for dep in dependencies:
            edge = {
                'from': dep.from_anchor,
                'to': dep.to_anchor,
                'type': dep.dependency_type,
                'strength': dep.strength
            }
            graph['edges'].append(edge)

            # Update node references
            if dep.from_anchor in graph['nodes']:
                graph['nodes'][dep.from_anchor]['outgoing'].append(dep.to_anchor)
            if dep.to_anchor in graph['nodes']:
                graph['nodes'][dep.to_anchor]['incoming'].append(dep.from_anchor)

        return graph

    def _calculate_suggested_order(
        self,
        anchors: List[Dict],
        dependencies: List[Dependency]
    ) -> List[str]:
        """Calculate suggested ordering using simplified topological sort."""
        # Build adjacency list
        anchor_ids = [a.get('id', f'anchor_{i}') for i, a in enumerate(anchors)]
        incoming_count = {aid: 0 for aid in anchor_ids}
        outgoing = {aid: [] for aid in anchor_ids}

        for dep in dependencies:
            if dep.from_anchor in outgoing and dep.to_anchor in incoming_count:
                outgoing[dep.from_anchor].append(dep.to_anchor)
                incoming_count[dep.to_anchor] += 1

        # Kahn's algorithm
        order = []
        no_incoming = [aid for aid in anchor_ids if incoming_count[aid] == 0]

        while no_incoming:
            # Pick anchor with no incoming dependencies
            current = no_incoming.pop(0)
            order.append(current)

            # Remove edges from current
            for neighbor in outgoing[current]:
                incoming_count[neighbor] -= 1
                if incoming_count[neighbor] == 0:
                    no_incoming.append(neighbor)

        # Add any remaining (cycles) at end
        remaining = [aid for aid in anchor_ids if aid not in order]
        order.extend(remaining)

        return order

    def _identify_terminal_anchors(
        self,
        anchors: List[Dict],
        dependencies: List[Dependency]
    ) -> List[str]:
        """Identify anchors with no outgoing dependencies."""
        anchor_ids = {a.get('id', f'anchor_{i}') for i, a in enumerate(anchors)}
        has_outgoing = {dep.from_anchor for dep in dependencies}
        return list(anchor_ids - has_outgoing)

    def format_report(self, result: DependencyMappingResult) -> str:
        """Format dependency mapping result as report."""
        lines = [
            "=" * 60,
            "DEPENDENCY MAPPING REPORT",
            "=" * 60,
            f"Total Anchors: {result.total_anchors}",
            f"Total Dependencies: {result.total_dependencies}",
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

        if result.foundational_anchors:
            lines.append(f"Foundational: {', '.join(result.foundational_anchors[:5])}")
            if len(result.foundational_anchors) > 5:
                lines.append(f"  ... and {len(result.foundational_anchors) - 5} more")

        if result.terminal_anchors:
            lines.append(f"Terminal: {', '.join(result.terminal_anchors[:5])}")
            if len(result.terminal_anchors) > 5:
                lines.append(f"  ... and {len(result.terminal_anchors) - 5} more")

        lines.append("")
        lines.append("-" * 60)
        lines.append("SUGGESTED ORDER:")
        for i, anchor_id in enumerate(result.suggested_order[:10], 1):
            lines.append(f"  {i}. {anchor_id}")
        if len(result.suggested_order) > 10:
            lines.append(f"  ... and {len(result.suggested_order) - 10} more")

        lines.append("")
        lines.append("-" * 60)
        lines.append("SAMPLE DEPENDENCIES:")
        for dep in result.dependencies[:5]:
            lines.append(f"  {dep.from_anchor} -> {dep.to_anchor}")
            lines.append(f"    Type: {dep.dependency_type}, Strength: {dep.strength}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def map_dependencies(anchors: List[Dict]) -> DependencyMappingResult:
    """Convenience function to map dependencies."""
    mapper = DependencyMapper()
    return mapper.map_dependencies(anchors)


if __name__ == "__main__":
    print("Dependency Mapper - NCLEX Pipeline Generation Skill")
    print("=" * 50)

    mapper = DependencyMapper()

    # Demo with sample anchors
    sample_anchors = [
        {'id': 'a1', 'title': 'Introduction to Cardiovascular System', 'full_text': 'Basic cardiovascular anatomy...'},
        {'id': 'a2', 'title': 'Cardiovascular Assessment', 'full_text': 'Assessing cardiovascular status...'},
        {'id': 'a3', 'title': 'Heart Failure Management', 'full_text': 'Managing heart failure patients...'},
        {'id': 'a4', 'title': 'Cardiac Medications', 'full_text': 'Drug therapy for cardiac conditions...'},
        {'id': 'a5', 'title': 'Basic ECG Interpretation', 'full_text': 'Understanding ECG basics...'},
        {'id': 'a6', 'title': 'Advanced Dysrhythmia Management', 'full_text': 'Complex rhythm management...'},
        {'id': 'a7', 'title': 'Cardiac Emergency Interventions', 'full_text': 'Emergency cardiac care...'},
        {'id': 'a8', 'title': 'Patient Education for Heart Disease', 'full_text': 'Teaching heart patients...'},
    ]

    print("\nMapping dependencies...")
    result = mapper.map_dependencies(sample_anchors)

    report = mapper.format_report(result)
    print(report)
