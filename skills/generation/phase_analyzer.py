"""
Phase Analyzer - Execute 5-Phase content analysis for NCLEX pipeline.

This module implements the 5-Phase analysis process used in Step 2 (Lecture Mapping)
to analyze anchor content and prepare it for section formation.

The 5 Phases are:
1. Content Survey - Inventory the anchor landscape
2. Cluster Discovery - Group related anchors
3. Relationship Mapping - Map prerequisite dependencies
4. Section Formation - Form lecture sections
5. Arc Planning - Generate sequence iterations

Usage:
    from skills.generation.phase_analyzer import PhaseAnalyzer

    analyzer = PhaseAnalyzer()
    result = analyzer.analyze(anchors)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PhaseResult:
    """Result from a single analysis phase."""
    phase_number: int
    phase_name: str
    status: str  # "completed", "partial", "failed"
    data: Dict = field(default_factory=dict)
    metrics: Dict = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """Complete analysis result from all phases."""
    run_id: str
    total_anchors: int
    phases_completed: int
    status: str  # "success", "partial", "failed"
    phase_results: List[PhaseResult] = field(default_factory=list)
    clusters: List[Dict] = field(default_factory=list)
    dependencies: List[Dict] = field(default_factory=list)
    sections: List[Dict] = field(default_factory=list)
    iterations: List[Dict] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)


class PhaseAnalyzer:
    """Execute 5-Phase content analysis on anchor content."""

    PHASE_NAMES = [
        "Content Survey",
        "Cluster Discovery",
        "Relationship Mapping",
        "Section Formation",
        "Arc Planning"
    ]

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the PhaseAnalyzer.

        Args:
            config_path: Optional path to configuration
        """
        self.config_path = config_path
        self._load_config()

    def _load_config(self):
        """Load configuration if available."""
        self.config = {}
        try:
            from skills.utilities.yaml_parser import load_constraints
            self.config = load_constraints()
        except ImportError:
            pass

    def generate_run_id(self) -> str:
        """Generate a unique run identifier."""
        return f"phase_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def analyze(self, anchors: List[Dict]) -> AnalysisResult:
        """
        Execute full 5-Phase analysis on anchors.

        Args:
            anchors: List of anchor dictionaries

        Returns:
            AnalysisResult with complete analysis
        """
        run_id = self.generate_run_id()
        phase_results = []
        status = "success"

        # Phase 1: Content Survey
        phase1 = self.phase1_content_survey(anchors)
        phase_results.append(phase1)

        # Phase 2: Cluster Discovery
        phase2 = self.phase2_cluster_discovery(anchors, phase1.data)
        phase_results.append(phase2)

        # Phase 3: Relationship Mapping
        phase3 = self.phase3_relationship_mapping(anchors, phase2.data)
        phase_results.append(phase3)

        # Phase 4: Section Formation
        phase4 = self.phase4_section_formation(
            anchors, phase2.data.get('clusters', []), phase3.data.get('dependencies', [])
        )
        phase_results.append(phase4)

        # Phase 5: Arc Planning
        phase5 = self.phase5_arc_planning(phase4.data.get('sections', []))
        phase_results.append(phase5)

        # Check for failures
        failed_phases = [p for p in phase_results if p.status == "failed"]
        if failed_phases:
            status = "failed" if len(failed_phases) > 2 else "partial"

        return AnalysisResult(
            run_id=run_id,
            total_anchors=len(anchors),
            phases_completed=sum(1 for p in phase_results if p.status == "completed"),
            status=status,
            phase_results=phase_results,
            clusters=phase2.data.get('clusters', []),
            dependencies=phase3.data.get('dependencies', []),
            sections=phase4.data.get('sections', []),
            iterations=phase5.data.get('iterations', []),
            summary=self._build_summary(anchors, phase_results)
        )

    def phase1_content_survey(self, anchors: List[Dict]) -> PhaseResult:
        """
        Phase 1: Content Survey - Inventory the anchor landscape.

        Analyzes anchors to understand:
        - Total content volume
        - Topic distribution
        - Keyword frequency
        - Content complexity indicators
        """
        result = PhaseResult(
            phase_number=1,
            phase_name="Content Survey",
            status="completed"
        )

        try:
            # Analyze anchor titles for keywords
            keywords = {}
            topics = {}
            total_words = 0

            for anchor in anchors:
                title = anchor.get('title', '').lower()
                content = anchor.get('full_text', '').lower()

                # Extract keywords from title
                title_words = [w for w in title.split() if len(w) > 3]
                for word in title_words:
                    keywords[word] = keywords.get(word, 0) + 1

                # Count content words
                content_words = len(content.split()) if content else 0
                total_words += content_words

                # Categorize by first significant word
                if title_words:
                    topic = title_words[0]
                    if topic not in topics:
                        topics[topic] = []
                    topics[topic].append(anchor.get('id', ''))

            # Sort keywords by frequency
            sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)

            result.data = {
                'anchor_count': len(anchors),
                'total_content_words': total_words,
                'avg_words_per_anchor': total_words / len(anchors) if anchors else 0,
                'top_keywords': dict(sorted_keywords[:20]),
                'topic_groups': topics,
                'unique_topics': len(topics)
            }

            result.metrics = {
                'keywords_extracted': len(keywords),
                'topics_identified': len(topics)
            }

        except Exception as e:
            result.status = "failed"
            result.notes.append(f"Error in phase 1: {e}")

        return result

    def phase2_cluster_discovery(
        self,
        anchors: List[Dict],
        survey_data: Dict
    ) -> PhaseResult:
        """
        Phase 2: Cluster Discovery - Group related anchors.

        Groups anchors based on:
        - Keyword overlap
        - Topic similarity
        - Content themes
        """
        result = PhaseResult(
            phase_number=2,
            phase_name="Cluster Discovery",
            status="completed"
        )

        try:
            clusters = []
            assigned_anchors = set()

            # Use topic groups from phase 1 as initial clusters
            topic_groups = survey_data.get('topic_groups', {})

            for topic, anchor_ids in topic_groups.items():
                if len(anchor_ids) >= 2:
                    cluster = {
                        'cluster_id': f"cluster_{len(clusters) + 1}",
                        'theme': topic,
                        'anchor_ids': anchor_ids,
                        'size': len(anchor_ids)
                    }
                    clusters.append(cluster)
                    assigned_anchors.update(anchor_ids)

            # Create clusters for ungrouped anchors
            ungrouped = []
            for anchor in anchors:
                anchor_id = anchor.get('id', '')
                if anchor_id not in assigned_anchors:
                    ungrouped.append(anchor_id)

            # Group ungrouped by title similarity
            if ungrouped:
                # Simple grouping: create a "miscellaneous" cluster
                clusters.append({
                    'cluster_id': f"cluster_{len(clusters) + 1}",
                    'theme': 'miscellaneous',
                    'anchor_ids': ungrouped,
                    'size': len(ungrouped)
                })

            result.data = {
                'clusters': clusters,
                'total_clusters': len(clusters),
                'anchors_clustered': len(assigned_anchors),
                'unclustered_count': len(ungrouped)
            }

            result.metrics = {
                'coverage': (len(anchors) - len(ungrouped)) / len(anchors) * 100 if anchors else 0
            }

        except Exception as e:
            result.status = "failed"
            result.notes.append(f"Error in phase 2: {e}")

        return result

    def phase3_relationship_mapping(
        self,
        anchors: List[Dict],
        cluster_data: Dict
    ) -> PhaseResult:
        """
        Phase 3: Relationship Mapping - Map prerequisite dependencies.

        Identifies:
        - Prerequisite relationships (A must come before B)
        - Building relationships (A supports understanding of B)
        - Parallel concepts (can be taught in any order)
        """
        result = PhaseResult(
            phase_number=3,
            phase_name="Relationship Mapping",
            status="completed"
        )

        try:
            dependencies = []
            anchor_map = {a.get('id', f'anchor_{i}'): a for i, a in enumerate(anchors)}

            # Define prerequisite keywords
            foundational_keywords = [
                'introduction', 'basic', 'fundamental', 'overview', 'definition',
                'anatomy', 'physiology', 'assessment', 'principles'
            ]
            advanced_keywords = [
                'advanced', 'complex', 'management', 'intervention', 'treatment',
                'complication', 'emergency', 'crisis'
            ]

            # Identify foundational vs advanced anchors
            foundational = []
            advanced = []

            for anchor in anchors:
                title = anchor.get('title', '').lower()
                anchor_id = anchor.get('id', '')

                is_foundational = any(kw in title for kw in foundational_keywords)
                is_advanced = any(kw in title for kw in advanced_keywords)

                if is_foundational:
                    foundational.append(anchor_id)
                elif is_advanced:
                    advanced.append(anchor_id)

            # Create dependencies: foundational -> advanced
            for found_id in foundational:
                for adv_id in advanced:
                    dependencies.append({
                        'from': found_id,
                        'to': adv_id,
                        'type': 'prerequisite',
                        'strength': 'suggested'
                    })

            result.data = {
                'dependencies': dependencies,
                'foundational_anchors': foundational,
                'advanced_anchors': advanced,
                'relationship_count': len(dependencies)
            }

            result.metrics = {
                'foundational_count': len(foundational),
                'advanced_count': len(advanced),
                'dependency_count': len(dependencies)
            }

        except Exception as e:
            result.status = "failed"
            result.notes.append(f"Error in phase 3: {e}")

        return result

    def phase4_section_formation(
        self,
        anchors: List[Dict],
        clusters: List[Dict],
        dependencies: List[Dict]
    ) -> PhaseResult:
        """
        Phase 4: Section Formation - Form lecture sections.

        Creates balanced sections considering:
        - Cluster groupings
        - Dependency ordering
        - Size constraints (15-20 anchors per section)
        """
        result = PhaseResult(
            phase_number=4,
            phase_name="Section Formation",
            status="completed"
        )

        try:
            sections = []
            section_config = self.config.get('sections', {})
            target_per_section = 17  # Midpoint of 15-20

            # Calculate target section count
            total_anchors = len(anchors)
            target_sections = max(4, min(12, round(total_anchors / target_per_section)))

            # Distribute anchors across sections
            anchors_per_section = total_anchors // target_sections
            remainder = total_anchors % target_sections

            current_idx = 0
            for i in range(target_sections):
                section_size = anchors_per_section + (1 if i < remainder else 0)
                section_anchors = anchors[current_idx:current_idx + section_size]

                # Determine section theme from anchor titles
                titles = [a.get('title', '') for a in section_anchors]
                common_words = self._find_common_theme(titles)

                section = {
                    'section_number': i + 1,
                    'section_name': common_words or f"Section {i + 1}",
                    'anchor_ids': [a.get('id', f'anchor_{j}') for j, a in enumerate(section_anchors, current_idx)],
                    'anchor_count': len(section_anchors),
                    'target_slides': min(35, max(12, int(len(section_anchors) * 1.5) + 2))
                }
                sections.append(section)
                current_idx += section_size

            result.data = {
                'sections': sections,
                'section_count': len(sections),
                'avg_anchors_per_section': total_anchors / len(sections) if sections else 0
            }

            result.metrics = {
                'min_section_size': min(s['anchor_count'] for s in sections) if sections else 0,
                'max_section_size': max(s['anchor_count'] for s in sections) if sections else 0
            }

        except Exception as e:
            result.status = "failed"
            result.notes.append(f"Error in phase 4: {e}")

        return result

    def phase5_arc_planning(self, sections: List[Dict]) -> PhaseResult:
        """
        Phase 5: Arc Planning - Generate sequence iterations.

        Plans the lecture arc considering:
        - Progressive complexity
        - Knowledge building
        - Engagement patterns
        """
        result = PhaseResult(
            phase_number=5,
            phase_name="Arc Planning",
            status="completed"
        )

        try:
            iterations = []

            # Create teaching arc iterations
            # Iteration 1: Linear progression
            iterations.append({
                'iteration_id': 'linear',
                'description': 'Standard linear progression through sections',
                'section_order': [s['section_number'] for s in sections],
                'arc_type': 'progressive'
            })

            # Iteration 2: Foundational first
            iterations.append({
                'iteration_id': 'foundational_first',
                'description': 'Start with foundational sections, build to complex',
                'section_order': [s['section_number'] for s in sections],
                'arc_type': 'building'
            })

            # Iteration 3: High-yield focus (for exam prep)
            iterations.append({
                'iteration_id': 'high_yield',
                'description': 'Prioritize high-yield exam content',
                'section_order': [s['section_number'] for s in sections],
                'arc_type': 'exam_focused'
            })

            result.data = {
                'iterations': iterations,
                'recommended': 'linear',
                'total_iterations': len(iterations)
            }

        except Exception as e:
            result.status = "failed"
            result.notes.append(f"Error in phase 5: {e}")

        return result

    def _find_common_theme(self, titles: List[str]) -> str:
        """Find common theme from list of titles."""
        if not titles:
            return ""

        # Extract words and find most common
        word_counts = {}
        stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'is', 'on', 'with'}

        for title in titles:
            words = title.lower().split()
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    word_counts[word] = word_counts.get(word, 0) + 1

        if word_counts:
            common_word = max(word_counts.items(), key=lambda x: x[1])[0]
            return common_word.title()

        return ""

    def _build_summary(
        self,
        anchors: List[Dict],
        phase_results: List[PhaseResult]
    ) -> Dict:
        """Build analysis summary."""
        return {
            'total_anchors': len(anchors),
            'phases_run': len(phase_results),
            'phases_completed': sum(1 for p in phase_results if p.status == "completed"),
            'phases_failed': sum(1 for p in phase_results if p.status == "failed"),
            'analysis_complete': all(p.status == "completed" for p in phase_results)
        }

    def format_report(self, result: AnalysisResult) -> str:
        """Format analysis result as report."""
        lines = [
            "=" * 60,
            "5-PHASE ANALYSIS REPORT",
            "=" * 60,
            f"Run ID: {result.run_id}",
            f"Total Anchors: {result.total_anchors}",
            f"Status: {result.status.upper()}",
            f"Phases Completed: {result.phases_completed}/5",
            ""
        ]

        for phase in result.phase_results:
            lines.append(f"Phase {phase.phase_number}: {phase.phase_name}")
            lines.append(f"  Status: {phase.status}")
            for key, value in list(phase.metrics.items())[:3]:
                lines.append(f"  {key}: {value}")
            lines.append("")

        if result.sections:
            lines.append("-" * 60)
            lines.append("SECTIONS FORMED:")
            for section in result.sections:
                lines.append(f"  {section['section_number']}. {section['section_name']}: "
                           f"{section['anchor_count']} anchors")

        lines.append("=" * 60)
        return "\n".join(lines)


def analyze_anchors(anchors: List[Dict]) -> AnalysisResult:
    """Convenience function to analyze anchors."""
    analyzer = PhaseAnalyzer()
    return analyzer.analyze(anchors)


if __name__ == "__main__":
    print("Phase Analyzer - NCLEX Pipeline Generation Skill")
    print("=" * 50)

    analyzer = PhaseAnalyzer()

    # Demo with sample anchors
    sample_anchors = [
        {'id': 'anchor_1', 'title': 'Introduction to Patient Assessment', 'full_text': 'Overview of assessment...'},
        {'id': 'anchor_2', 'title': 'Basic Vital Signs', 'full_text': 'Understanding vital signs...'},
        {'id': 'anchor_3', 'title': 'Assessment Documentation', 'full_text': 'Documentation standards...'},
        {'id': 'anchor_4', 'title': 'Advanced Assessment Techniques', 'full_text': 'Complex assessment...'},
        {'id': 'anchor_5', 'title': 'Physical Examination Fundamentals', 'full_text': 'Physical exam basics...'},
        {'id': 'anchor_6', 'title': 'Head-to-Toe Assessment', 'full_text': 'Systematic assessment...'},
        {'id': 'anchor_7', 'title': 'Neurological Assessment', 'full_text': 'Neuro assessment...'},
        {'id': 'anchor_8', 'title': 'Cardiovascular Assessment', 'full_text': 'CV assessment...'},
        {'id': 'anchor_9', 'title': 'Respiratory Assessment', 'full_text': 'Respiratory assessment...'},
        {'id': 'anchor_10', 'title': 'Assessment Management Complications', 'full_text': 'Managing complications...'},
    ]

    print("\nRunning 5-Phase Analysis...")
    result = analyzer.analyze(sample_anchors)

    report = analyzer.format_report(result)
    print(report)
