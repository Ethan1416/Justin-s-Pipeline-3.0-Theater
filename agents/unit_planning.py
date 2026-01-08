"""
Unit Planning Agents (Phase 1)
==============================

Agents for unit-level planning and standards mapping.
"""

from typing import Any, Dict, List
from pathlib import Path

from .base import Agent


# California ELA Standards Database (Theater-Relevant)
STANDARDS_DATABASE = {
    # Reading Literature (RL.9-12)
    "RL.9-10.3": {
        "text": "Analyze how complex characters develop over the course of a text, interact with other characters, and advance the plot or develop the theme.",
        "keywords": ["character", "motivation", "development", "plot", "theme", "interaction"],
        "theater_application": "Character analysis in plays, understanding dramatic arcs"
    },
    "RL.9-10.4": {
        "text": "Determine the meaning of words and phrases as they are used in the text, including figurative and connotative meanings.",
        "keywords": ["word choice", "figurative", "connotative", "meaning", "tone", "language"],
        "theater_application": "Shakespeare's language, verse analysis, word play"
    },
    "RL.9-10.5": {
        "text": "Analyze how an author's choices concerning how to structure a text create effects as mystery, tension, or surprise.",
        "keywords": ["structure", "plot", "pacing", "tension", "dramatic structure"],
        "theater_application": "Play structure, act/scene analysis, dramatic tension"
    },
    "RL.9-10.6": {
        "text": "Analyze a particular point of view or cultural experience reflected in a work of literature from outside the United States.",
        "keywords": ["point of view", "culture", "perspective", "world literature"],
        "theater_application": "Greek theater origins, Commedia as Italian form"
    },
    "RL.9-10.9": {
        "text": "Analyze how an author draws on and transforms source material in a specific work.",
        "keywords": ["source material", "adaptation", "transformation", "influence"],
        "theater_application": "Shakespeare's sources, adaptations of classical works"
    },
    "RL.11-12.3": {
        "text": "Analyze the impact of the author's choices regarding how to develop and relate elements of a story or drama.",
        "keywords": ["author choices", "drama", "elements", "development"],
        "theater_application": "Directorial interpretation, playwright choices"
    },
    "RL.11-12.4": {
        "text": "Determine the meaning of words and phrases including figurative and connotative meanings; analyze the impact of specific word choices.",
        "keywords": ["word meaning", "figurative", "tone", "language", "poetic"],
        "theater_application": "Shakespeare's language, iambic pentameter analysis"
    },
    "RL.11-12.5": {
        "text": "Analyze how an author's choices concerning how to structure specific parts of a text contribute to its overall structure and meaning.",
        "keywords": ["structure", "meaning", "aesthetic", "form"],
        "theater_application": "Five-act structure, scene structure, dramatic irony"
    },
    # Speaking & Listening (SL.9-12)
    "SL.9-10.1": {
        "text": "Initiate and participate effectively in a range of collaborative discussions with diverse partners.",
        "keywords": ["discussion", "collaboration", "ideas", "persuasion"],
        "theater_application": "Table reads, rehearsal discussions, ensemble work"
    },
    "SL.9-10.4": {
        "text": "Present information, findings, and supporting evidence clearly, concisely, and logically.",
        "keywords": ["present", "evidence", "logical", "organization", "audience"],
        "theater_application": "Performance, presentation of scene work, defending choices"
    },
    "SL.9-10.6": {
        "text": "Adapt speech to a variety of contexts and tasks, demonstrating command of formal English.",
        "keywords": ["adapt speech", "context", "formal", "appropriate"],
        "theater_application": "Character voice, dialects, code-switching in performance"
    },
    "SL.11-12.1": {
        "text": "Initiate and participate effectively in a range of collaborative discussions on complex topics.",
        "keywords": ["discussion", "collaboration", "ideas", "persuasion"],
        "theater_application": "Advanced scene analysis, directorial discussions"
    },
    "SL.11-12.4": {
        "text": "Present information conveying a clear and distinct perspective such that listeners can follow the line of reasoning.",
        "keywords": ["present", "perspective", "reasoning", "formal", "informal"],
        "theater_application": "Director's concept presentations, scene rationale"
    },
    # Writing (W.9-12)
    "W.9-10.1": {
        "text": "Write arguments to support claims in an analysis of substantive topics or texts, using valid reasoning.",
        "keywords": ["argument", "claims", "analysis", "evidence", "reasoning"],
        "theater_application": "Play analysis papers, defending performance choices"
    },
    "W.9-10.2": {
        "text": "Write informative/explanatory texts to examine and convey complex ideas clearly and accurately.",
        "keywords": ["informative", "explanatory", "complex ideas", "analysis"],
        "theater_application": "Character analysis, historical context research"
    },
    "W.9-10.3": {
        "text": "Write narratives to develop real or imagined experiences using effective technique and well-chosen details.",
        "keywords": ["narrative", "experience", "technique", "details", "sequence"],
        "theater_application": "Playwriting, character backstory, scene writing"
    },
    "W.11-12.1": {
        "text": "Write arguments to support claims in an analysis of substantive topics, using valid reasoning and relevant evidence.",
        "keywords": ["argument", "analysis", "evidence", "reasoning"],
        "theater_application": "Advanced critical analysis, production proposals"
    },
    "W.11-12.3": {
        "text": "Write narratives to develop real or imagined experiences using effective technique.",
        "keywords": ["narrative", "creative writing", "technique"],
        "theater_application": "Advanced playwriting, adaptation projects"
    },
}

# Unit-specific standard recommendations
UNIT_STANDARDS = {
    1: {  # Greek Theater
        "primary": ["RL.9-10.5", "RL.9-10.6", "SL.9-10.1", "W.9-10.2"],
        "rationale": {
            "RL.9-10.5": "Structure analysis (tragedy, comedy, 3-act form)",
            "RL.9-10.6": "Cultural perspective (ancient Greek culture)",
            "SL.9-10.1": "Chorus work, ensemble discussions",
            "W.9-10.2": "Research on Greek theater history"
        }
    },
    2: {  # Commedia dell'Arte
        "primary": ["RL.9-10.3", "RL.9-10.6", "SL.9-10.6", "W.9-10.3"],
        "rationale": {
            "RL.9-10.3": "Stock character analysis",
            "RL.9-10.6": "Italian Renaissance cultural context",
            "SL.9-10.6": "Character voice work, physicality",
            "W.9-10.3": "Scenario writing, lazzi creation"
        }
    },
    3: {  # Shakespeare
        "primary": ["RL.11-12.4", "RL.9-10.9", "SL.9-10.4", "W.9-10.1"],
        "rationale": {
            "RL.11-12.4": "Language analysis (verse, figurative language)",
            "RL.9-10.9": "Source material analysis",
            "SL.9-10.4": "Monologue performance",
            "W.9-10.1": "Character analysis arguments"
        }
    },
    4: {  # Student-Directed One Acts
        "primary": ["RL.11-12.3", "SL.11-12.4", "SL.11-12.1", "W.11-12.1"],
        "rationale": {
            "RL.11-12.3": "Director's analysis of playwright choices",
            "SL.11-12.4": "Directing concept presentations",
            "SL.11-12.1": "Rehearsal collaboration",
            "W.11-12.1": "Director's notes, production proposals"
        }
    }
}


class UnitPlannerAgent(Agent):
    """Agent for planning unit structure."""

    # Unit configurations
    UNIT_CONFIGS = {
        1: {"name": "Greek Theater", "days": 20},
        2: {"name": "Commedia dell'Arte", "days": 18},
        3: {"name": "Shakespeare", "days": 25},
        4: {"name": "Student-Directed One Acts", "days": 17}
    }

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        if not lesson_ctx:
            return {"error": "No lesson context provided"}

        unit_config = self.UNIT_CONFIGS.get(lesson_ctx.unit_number, {"name": "Unknown", "days": 20})

        return {
            "unit_plan": {
                "unit_number": lesson_ctx.unit_number,
                "unit_name": lesson_ctx.unit_name or unit_config["name"],
                "total_days": unit_config["days"],
                "current_day": lesson_ctx.day,
                "topic": lesson_ctx.topic,
                "standards": lesson_ctx.standards,
                "objectives": lesson_ctx.learning_objectives,
                "day_position": self._categorize_day_position(lesson_ctx.day, unit_config["days"])
            }
        }

    def _categorize_day_position(self, day: int, total_days: int) -> str:
        """Categorize day position within unit."""
        progress = day / total_days
        if progress <= 0.25:
            return "early"
        elif progress <= 0.75:
            return "middle"
        else:
            return "late"


class StandardsMapperAgent(Agent):
    """Maps unit and lesson content to California ELA/Literacy standards."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        if not lesson_ctx:
            return {"error": "No lesson context provided"}

        # Build content for matching
        content = {
            "unit_name": lesson_ctx.unit_name,
            "unit_number": lesson_ctx.unit_number,
            "topic": lesson_ctx.topic,
            "learning_objectives": lesson_ctx.learning_objectives,
            "activities": [lesson_ctx.warmup.get('name', ''), lesson_ctx.activity.get('name', '')],
            "vocabulary": [v.get('term', '') for v in lesson_ctx.vocabulary]
        }

        grade_band = "9-10" if lesson_ctx.unit_number in [1, 2] else "mixed"
        target_strands = ["RL", "SL", "W"]

        # Match standards
        matched_standards = self._match_standards(content, grade_band, target_strands)

        # Calculate coverage
        coverage = self._calculate_coverage(matched_standards)

        # Identify gaps
        gaps = self._identify_gaps(matched_standards, lesson_ctx.unit_number)

        # Determine status
        if coverage['coverage_percentage'] >= 100:
            status = 'COMPLETE'
        elif coverage['coverage_percentage'] >= 75:
            status = 'PARTIAL'
        else:
            status = 'INSUFFICIENT'

        # Generate recommendations
        recommendations = self._generate_recommendations(coverage, lesson_ctx.unit_number)

        return {
            "mapping_status": status,
            "unit_name": lesson_ctx.unit_name,
            "standards_addressed": matched_standards,
            "coverage_summary": coverage,
            "gaps": gaps,
            "recommendations": recommendations
        }

    def _extract_keywords(self, content: Dict) -> List[str]:
        """Extract keywords from content."""
        keywords = []

        for obj in content.get('learning_objectives', []):
            keywords.extend(obj.lower().split())

        for act in content.get('activities', []):
            if act:
                keywords.extend(act.lower().split())

        keywords.extend([v.lower() for v in content.get('vocabulary', [])])
        keywords.extend(content.get('topic', '').lower().split())

        return list(set(keywords))

    def _score_alignment(self, content_keywords: List[str], standard: Dict) -> int:
        """Score alignment between content and a standard."""
        standard_keywords = standard.get('keywords', [])
        if not standard_keywords:
            return 0

        matches = sum(1 for kw in standard_keywords if any(kw.lower() in ckw for ckw in content_keywords))
        return min(100, int((matches / len(standard_keywords)) * 100))

    def _match_standards(self, content: Dict, grade_band: str, target_strands: List[str]) -> List[Dict]:
        """Find standards that align with content."""
        content_keywords = self._extract_keywords(content)
        matched = []

        # Also include unit-specific primary standards
        unit_number = content.get('unit_number', 1)
        primary_standards = UNIT_STANDARDS.get(unit_number, {}).get('primary', [])

        for code, standard in STANDARDS_DATABASE.items():
            # Filter by grade band
            if grade_band == '9-10' and '11-12' in code:
                continue
            if grade_band == '11-12' and '9-10' in code:
                continue

            # Filter by strand
            strand = code[:2] if len(code) >= 2 else ""
            if strand not in target_strands:
                continue

            # Score alignment
            score = self._score_alignment(content_keywords, standard)

            # Boost score for unit-specific primary standards
            if code in primary_standards:
                score = max(score, 70)  # Minimum 70 for primary standards

            if score >= 30:
                matched.append({
                    'code': code,
                    'text': standard['text'],
                    'strand': strand,
                    'alignment_score': score,
                    'theater_application': standard.get('theater_application', ''),
                    'is_primary': code in primary_standards
                })

        return sorted(matched, key=lambda x: x['alignment_score'], reverse=True)

    def _calculate_coverage(self, matched_standards: List[Dict]) -> Dict:
        """Calculate coverage across strands."""
        coverage = {
            'RL_count': sum(1 for s in matched_standards if s['strand'] == 'RL'),
            'SL_count': sum(1 for s in matched_standards if s['strand'] == 'SL'),
            'W_count': sum(1 for s in matched_standards if s['strand'] == 'W'),
            'total_standards': len(matched_standards)
        }

        # Expected minimums per unit
        expected = {'RL': 2, 'SL': 1, 'W': 1}
        total_expected = sum(expected.values())
        total_actual = min(coverage['RL_count'], expected['RL']) + \
                      min(coverage['SL_count'], expected['SL']) + \
                      min(coverage['W_count'], expected['W'])

        coverage['coverage_percentage'] = round((total_actual / total_expected) * 100, 1)

        return coverage

    def _identify_gaps(self, matched_standards: List[Dict], unit_number: int) -> List[Dict]:
        """Identify standards that should be addressed but aren't."""
        gaps = []
        matched_codes = [s['code'] for s in matched_standards]

        primary_standards = UNIT_STANDARDS.get(unit_number, {}).get('primary', [])
        rationales = UNIT_STANDARDS.get(unit_number, {}).get('rationale', {})

        for code in primary_standards:
            if code not in matched_codes:
                standard = STANDARDS_DATABASE.get(code, {})
                gaps.append({
                    'code': code,
                    'text': standard.get('text', ''),
                    'theater_application': standard.get('theater_application', ''),
                    'rationale': rationales.get(code, ''),
                    'suggestion': f"Consider adding activity that addresses {code}"
                })

        return gaps

    def _generate_recommendations(self, coverage: Dict, unit_number: int) -> List[str]:
        """Generate recommendations for improving coverage."""
        recommendations = []

        if coverage['RL_count'] < 2:
            recommendations.append("Add more reading literature activities (character/text analysis)")
        if coverage['SL_count'] < 1:
            recommendations.append("Add collaborative discussion or presentation activities")
        if coverage['W_count'] < 1:
            recommendations.append("Add writing activities (analysis, narrative, or argument)")

        return recommendations


class UnitScopeValidatorAgent(Agent):
    """Validates unit scope and day alignment."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        if not lesson_ctx:
            return {"error": "No lesson context provided"}

        issues = []
        warnings = []

        # Validate day is within unit bounds
        unit_days = {1: 20, 2: 18, 3: 25, 4: 17}
        max_days = unit_days.get(lesson_ctx.unit_number, 20)

        if lesson_ctx.day < 1 or lesson_ctx.day > max_days:
            issues.append(f"Day {lesson_ctx.day} is out of bounds for Unit {lesson_ctx.unit_number} (1-{max_days})")

        # Validate required fields
        if not lesson_ctx.topic:
            issues.append("Topic is required")
        if not lesson_ctx.learning_objectives:
            warnings.append("No learning objectives provided")
        if not lesson_ctx.vocabulary:
            warnings.append("No vocabulary provided")

        # Validate objectives count
        obj_count = len(lesson_ctx.learning_objectives)
        if obj_count < 2:
            warnings.append(f"Only {obj_count} learning objectives (recommended: 2-4)")
        elif obj_count > 4:
            warnings.append(f"{obj_count} learning objectives may be too many (recommended: 2-4)")

        return {
            "validation_status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "warnings": warnings,
            "unit_number": lesson_ctx.unit_number,
            "day": lesson_ctx.day,
            "max_days": max_days,
            "_warnings": warnings  # Will be extracted by base class
        }


class LearningObjectiveGeneratorAgent(Agent):
    """Generates measurable learning objectives using Bloom's Taxonomy."""

    BLOOM_VERBS = {
        'remember': ['identify', 'list', 'name', 'recall', 'recognize', 'state', 'define', 'label'],
        'understand': ['describe', 'explain', 'summarize', 'interpret', 'paraphrase', 'discuss', 'classify'],
        'apply': ['demonstrate', 'perform', 'use', 'execute', 'implement', 'practice', 'apply'],
        'analyze': ['analyze', 'compare', 'contrast', 'examine', 'differentiate', 'distinguish', 'investigate'],
        'evaluate': ['evaluate', 'assess', 'critique', 'judge', 'justify', 'defend', 'argue'],
        'create': ['create', 'design', 'develop', 'compose', 'construct', 'produce', 'devise']
    }

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        if not lesson_ctx:
            return {"error": "No lesson context provided"}

        # If objectives already exist, validate them
        if lesson_ctx.learning_objectives:
            objectives = self._validate_objectives(lesson_ctx.learning_objectives)
        else:
            objectives = self._generate_objectives(lesson_ctx)

        # Calculate bloom distribution
        bloom_dist = self._calculate_bloom_distribution(objectives)

        return {
            "objectives": objectives,
            "summary": {
                "total_objectives": len(objectives),
                "bloom_distribution": bloom_dist,
                "standards_coverage": [s.get('code', '') for s in lesson_ctx.standards[:3]]
            }
        }

    def _classify_bloom_level(self, verb: str) -> str:
        """Classify a verb according to Bloom's Taxonomy."""
        verb_lower = verb.lower()
        for level, verbs in self.BLOOM_VERBS.items():
            if verb_lower in verbs:
                return level
        return 'understand'  # Default

    def _validate_objectives(self, objectives: List[str]) -> List[Dict]:
        """Validate existing objectives and add metadata."""
        validated = []
        for obj in objectives:
            words = obj.split()
            verb = words[0] if words else ''
            bloom_level = self._classify_bloom_level(verb)

            validated.append({
                "objective_text": obj,
                "bloom_level": bloom_level,
                "verb": verb,
                "assessment_suggestion": self._suggest_assessment(bloom_level)
            })
        return validated

    def _generate_objectives(self, lesson_ctx) -> List[Dict]:
        """Generate objectives if none provided."""
        objectives = []
        topic = lesson_ctx.topic

        # Generate 3 objectives at different Bloom levels
        templates = [
            ("understand", f"Explain the key concepts of {topic}"),
            ("apply", f"Demonstrate understanding of {topic} through practical application"),
            ("analyze", f"Analyze the relationship between {topic} and theatrical practice")
        ]

        for level, obj_text in templates:
            objectives.append({
                "objective_text": obj_text,
                "bloom_level": level,
                "verb": obj_text.split()[0].lower(),
                "assessment_suggestion": self._suggest_assessment(level)
            })

        return objectives

    def _calculate_bloom_distribution(self, objectives: List[Dict]) -> Dict:
        """Calculate distribution across Bloom levels."""
        dist = {level: 0 for level in self.BLOOM_VERBS.keys()}
        for obj in objectives:
            level = obj.get('bloom_level', 'understand')
            if level in dist:
                dist[level] += 1
        return dist

    def _suggest_assessment(self, bloom_level: str) -> str:
        """Suggest assessment method based on Bloom level."""
        suggestions = {
            'remember': 'Quiz, matching, or labeling activity',
            'understand': 'Short answer discussion or written explanation',
            'apply': 'Performance demonstration or hands-on practice',
            'analyze': 'Written analysis or comparison activity',
            'evaluate': 'Critique or peer review activity',
            'create': 'Original project or performance creation'
        }
        return suggestions.get(bloom_level, 'Observation and discussion')
