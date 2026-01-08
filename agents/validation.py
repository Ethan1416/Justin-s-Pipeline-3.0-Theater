"""
Validation Agents (Phase 3)
===========================

HARDCODED validation gates for content quality assurance.
These validators enforce non-negotiable quality standards.
"""

from typing import Any, Dict, List
from pathlib import Path

from .base import Agent


class TruncationValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate no truncated sentences.

    Checks that all content has complete sentences with no
    truncation markers (ellipsis, double dash, incomplete thoughts).
    """

    # Truncation indicators to check for
    TRUNCATION_MARKERS = ['...', '--', '…', '—']

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = self._extract_content(context)

        issues = []
        sentences_checked = 0

        # Split content into sentences
        sentences = content.replace('\n', ' ').replace('  ', ' ').split('.')

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue

            sentences_checked += 1

            # Check for truncation markers
            for marker in self.TRUNCATION_MARKERS:
                if sentence.endswith(marker):
                    issues.append({
                        "type": "truncation",
                        "position": i,
                        "text": f"{sentence[:50]}..." if len(sentence) > 50 else sentence,
                        "marker": marker
                    })

            # Check for incomplete sentence (ends mid-word)
            if sentence and len(sentence) > 10:
                # Very short last word might indicate truncation
                words = sentence.split()
                if words:
                    last_word = words[-1]
                    if len(last_word) == 1 and last_word not in ['a', 'I']:
                        issues.append({
                            "type": "possible_truncation",
                            "position": i,
                            "text": f"{sentence[:50]}...",
                            "reason": "Single character ending"
                        })

        passed = len(issues) == 0

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "truncation",
            "passed": passed,
            "issues": issues,
            "sentences_checked": sentences_checked,
            "score": 100 if passed else max(0, 100 - (len(issues) * 10))
        }

    def _extract_content(self, context: Dict) -> str:
        """Extract text content from various context formats."""
        content = context.get('content', '')

        if isinstance(content, dict):
            # Try to get text from common keys
            for key in ['text', 'presenter_notes', 'body', 'description']:
                if key in content:
                    return str(content[key])
            return str(content)

        # Also check for lesson_context presenter notes
        lesson_ctx = context.get('lesson_context')
        if lesson_ctx:
            notes = context.get('presenter_notes_writer_output', {})
            if notes:
                return notes.get('presenter_notes', str(content))

        return str(content)


class ElaborationValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate professional elaboration depth.

    Ensures content meets minimum quality standards for:
    - Depth (word count relative to target)
    - Examples (illustrative content)
    - Procedure (step-by-step clarity)
    - Tone (professional language)
    - Connections (logical flow)

    THRESHOLD: 85/100 minimum score
    """

    # Hardcoded threshold - DO NOT MODIFY
    THRESHOLD = 85

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = self._extract_content(context)
        target_words = context.get('target_words', 2000)

        # Calculate elaboration scores
        scores = self._calculate_scores(content, target_words)

        # Calculate weighted total
        # Weights: Depth 30%, Examples 20%, Procedure 20%, Tone 15%, Connections 15%
        total_score = (
            scores["depth"] * 0.30 +
            scores["examples"] * 0.20 +
            scores["procedure"] * 0.20 +
            scores["tone"] * 0.15 +
            scores["connections"] * 0.15
        )

        passed = total_score >= self.THRESHOLD

        # Generate feedback for low scores
        feedback = self._generate_feedback(scores)

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "elaboration",
            "passed": passed,
            "total_score": round(total_score, 1),
            "threshold": self.THRESHOLD,
            "category_scores": scores,
            "word_count": len(content.split()),
            "feedback": feedback if not passed else [],
            "retry_strategy": "ENRICHMENT_PASS" if not passed else None
        }

    def _extract_content(self, context: Dict) -> str:
        """Extract text content from context."""
        content = context.get('content', '')
        if isinstance(content, dict):
            return str(content)

        # Check presenter notes
        notes = context.get('presenter_notes_writer_output', {})
        if notes:
            return notes.get('presenter_notes', str(content))

        return str(content)

    def _calculate_scores(self, content: str, target_words: int) -> Dict[str, float]:
        """Calculate individual category scores."""
        content_lower = content.lower()
        word_count = len(content.split())

        return {
            "depth": min(100, (word_count / target_words) * 100),
            "examples": self._score_examples(content_lower),
            "procedure": self._score_procedure(content_lower),
            "tone": self._score_tone(content_lower),
            "connections": self._score_connections(content_lower)
        }

    def _score_examples(self, content: str) -> float:
        """Score based on presence of examples."""
        example_indicators = [
            "example", "for instance", "such as", "like when",
            "consider", "imagine", "suppose", "let's say"
        ]
        count = sum(1 for ind in example_indicators if ind in content)
        return min(100, count * 25)  # 4+ examples = 100

    def _score_procedure(self, content: str) -> float:
        """Score based on procedural clarity."""
        procedure_indicators = [
            "first", "then", "next", "finally", "step",
            "begin by", "start with", "after that", "following this"
        ]
        count = sum(1 for ind in procedure_indicators if ind in content)
        return min(100, count * 20)  # 5+ = 100

    def _score_tone(self, content: str) -> float:
        """Score based on professional tone."""
        informal_words = [
            "gonna", "wanna", "kinda", "sorta", "gotta",
            "yeah", "nope", "ok", "okay cool"
        ]
        informal_count = sum(1 for word in informal_words if word in content)
        return max(0, 100 - (informal_count * 15))

    def _score_connections(self, content: str) -> float:
        """Score based on logical connections."""
        connection_words = [
            "because", "therefore", "thus", "consequently",
            "as a result", "this means", "in other words", "similarly"
        ]
        count = sum(1 for word in connection_words if word in content)
        return min(100, count * 20)  # 5+ = 100

    def _generate_feedback(self, scores: Dict[str, float]) -> List[str]:
        """Generate actionable feedback for low scores."""
        feedback = []

        if scores["depth"] < 80:
            feedback.append("Add more detail and explanation to increase content depth")
        if scores["examples"] < 80:
            feedback.append("Include more concrete examples to illustrate concepts")
        if scores["procedure"] < 80:
            feedback.append("Add step-by-step language for clearer progression")
        if scores["tone"] < 80:
            feedback.append("Replace informal language with professional phrasing")
        if scores["connections"] < 80:
            feedback.append("Add transition words to improve logical flow")

        return feedback


class TimingValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate content fits timing constraints.

    Ensures presenter notes fit within the 15-minute lecture window
    based on speaking rate of 130-150 WPM.

    THRESHOLDS:
    - Duration: 14-16 minutes (within 1 minute of target)
    - Word count: 1,950-2,250 words
    """

    # Hardcoded thresholds - DO NOT MODIFY
    MIN_DURATION_MINUTES = 14
    MAX_DURATION_MINUTES = 16
    MIN_WORDS = 1950
    MAX_WORDS = 2250
    SPEAKING_RATE_WPM = 140

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Get presenter notes
        presenter_notes = context.get('presenter_notes', '')
        if not presenter_notes:
            notes_output = context.get('presenter_notes_writer_output', {})
            presenter_notes = notes_output.get('presenter_notes', '')

        word_count = len(presenter_notes.split())
        estimated_minutes = word_count / self.SPEAKING_RATE_WPM

        # Check thresholds
        duration_ok = self.MIN_DURATION_MINUTES <= estimated_minutes <= self.MAX_DURATION_MINUTES
        word_count_ok = self.MIN_WORDS <= word_count <= self.MAX_WORDS

        passed = duration_ok and word_count_ok

        # Determine adjustment needed
        adjustment = None
        if word_count < self.MIN_WORDS:
            adjustment = f"Add approximately {self.MIN_WORDS - word_count} words"
        elif word_count > self.MAX_WORDS:
            adjustment = f"Remove approximately {word_count - self.MAX_WORDS} words"

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "timing",
            "passed": passed,
            "word_count": word_count,
            "estimated_minutes": round(estimated_minutes, 1),
            "target_minutes": 15,
            "acceptable_range_minutes": f"{self.MIN_DURATION_MINUTES}-{self.MAX_DURATION_MINUTES}",
            "acceptable_range_words": f"{self.MIN_WORDS}-{self.MAX_WORDS}",
            "adjustment_needed": adjustment,
            "retry_strategy": "ADJUSTMENT_PASS" if not passed else None
        }


class StructureValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate all lesson components present.

    Ensures the lesson package contains all required components
    with proper structure and formatting.
    """

    # Required components - DO NOT MODIFY
    REQUIRED_COMPONENTS = [
        "learning_objectives",
        "vocabulary",
        "warmup",
        "content_points",
        "activity",
        "journal_prompt",
        "exit_tickets",
        "materials_list"
    ]

    # Component to agent output mapping
    COMPONENT_AGENT_MAP = {
        "warmup": "warmup_generator",
        "activity": "activity_generator",
        "journal_prompt": "journal_exit_generator",
        "exit_tickets": "journal_exit_generator"
    }

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        daily_input = context.get('daily_input', {})
        previous_outputs = context.get('previous_outputs', {})

        present = []
        missing = []

        for component in self.REQUIRED_COMPONENTS:
            value = None

            # Check lesson_context first
            if lesson_ctx:
                value = getattr(lesson_ctx, component, None)

            # Check daily_input (orchestrator format)
            if not value and component in daily_input:
                value = daily_input.get(component)

            # Check direct context keys
            if not value:
                value = context.get(component)

            # Check previous_outputs for generated components
            if not value:
                agent_name = self.COMPONENT_AGENT_MAP.get(component)
                if agent_name and agent_name in previous_outputs:
                    agent_output = previous_outputs[agent_name]
                    if component == "warmup":
                        value = agent_output.get('warmup')
                    elif component == "activity":
                        value = agent_output.get('activity')
                    elif component == "journal_prompt":
                        journal = agent_output.get('journal', {})
                        value = journal.get('prompt') if isinstance(journal, dict) else journal
                    elif component == "exit_tickets":
                        tickets = agent_output.get('exit_tickets', {})
                        value = tickets.get('questions') if isinstance(tickets, dict) else tickets

            # Check {component}_output style
            if not value:
                output_key = f"{component}_output"
                if output_key in context:
                    value = context[output_key]

            if value:
                present.append(component)
            else:
                missing.append(component)

        passed = len(missing) == 0
        completeness = round(len(present) / len(self.REQUIRED_COMPONENTS) * 100, 1)

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "structure",
            "passed": passed,
            "components_present": present,
            "components_missing": missing,
            "completeness_percentage": completeness,
            "retry_strategy": "COMPONENT_REGEN" if not passed else None,
            "missing_components": missing
        }


class StandardsCoverageValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate all learning objectives have standards mapped.

    Ensures every learning objective is connected to at least one
    California ELA/Literacy standard (RL, SL, W.9-12).

    THRESHOLD: 100% coverage required
    """

    # Valid standard prefixes - DO NOT MODIFY
    VALID_STANDARD_PREFIXES = [
        "RL.9-10", "RL.11-12",  # Reading Literature
        "SL.9-10", "SL.11-12",  # Speaking & Listening
        "W.9-10", "W.11-12",    # Writing
    ]

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Extract learning objectives
        objectives = self._extract_objectives(context)
        standards = self._extract_standards(context)

        # Check coverage
        covered_objectives = []
        uncovered_objectives = []
        standards_used = set()

        for i, objective in enumerate(objectives):
            # Check if objective has associated standard
            obj_standards = self._find_standards_for_objective(objective, standards, context)
            if obj_standards:
                covered_objectives.append({
                    "objective": objective,
                    "standards": obj_standards
                })
                standards_used.update(obj_standards)
            else:
                uncovered_objectives.append({
                    "index": i,
                    "objective": objective
                })

        total = len(objectives)
        covered = len(covered_objectives)
        coverage_percentage = (covered / total * 100) if total > 0 else 0

        passed = coverage_percentage == 100 and total > 0

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "standards_coverage",
            "passed": passed,
            "total_objectives": total,
            "covered_objectives": covered,
            "coverage_percentage": round(coverage_percentage, 1),
            "uncovered_objectives": uncovered_objectives,
            "standards_used": list(standards_used),
            "retry_strategy": "STANDARDS_MAPPING" if not passed else None
        }

    def _extract_objectives(self, context: Dict) -> List[str]:
        """Extract learning objectives from context."""
        # Check direct context
        objectives = context.get('learning_objectives', [])
        if objectives:
            return objectives if isinstance(objectives, list) else [objectives]

        # Check daily_input
        daily_input = context.get('daily_input', {})
        objectives = daily_input.get('learning_objectives', [])
        if objectives:
            return objectives if isinstance(objectives, list) else [objectives]

        # Check lesson_context
        lesson_ctx = context.get('lesson_context')
        if lesson_ctx:
            objectives = getattr(lesson_ctx, 'learning_objectives', [])
            if objectives:
                return objectives if isinstance(objectives, list) else [objectives]

        return []

    def _extract_standards(self, context: Dict) -> List[str]:
        """Extract standards from context."""
        standards = context.get('standards', [])
        if standards:
            return standards if isinstance(standards, list) else [standards]

        daily_input = context.get('daily_input', {})
        standards = daily_input.get('standards', [])
        if standards:
            return standards if isinstance(standards, list) else [standards]

        lesson_ctx = context.get('lesson_context')
        if lesson_ctx:
            standards = getattr(lesson_ctx, 'standards', [])
            if standards:
                return standards if isinstance(standards, list) else [standards]

        return []

    def _find_standards_for_objective(self, objective: str, standards: List[str], context: Dict) -> List[str]:
        """Find standards that apply to this objective."""
        # If we have a standards map, use it
        standards_map = context.get('standards_map', {})
        if standards_map and objective in standards_map:
            return standards_map[objective]

        # Otherwise, return all standards if objectives exist
        # (assume standards apply to all objectives if not explicitly mapped)
        if standards:
            return standards

        return []


class CoherenceValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate logical lesson flow.

    Ensures lesson components flow logically:
    - Warmup connects to content
    - Content builds progressively
    - Activity applies learning
    - Journal reflects on learning

    THRESHOLD: 80/100 minimum score
    """

    # Hardcoded threshold - DO NOT MODIFY
    THRESHOLD = 80

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Extract lesson components
        warmup = self._get_component(context, 'warmup')
        content = self._get_component(context, 'content_points')
        activity = self._get_component(context, 'activity')
        journal = self._get_component(context, 'journal_prompt')
        vocabulary = self._get_component(context, 'vocabulary')
        topic = context.get('topic') or context.get('daily_input', {}).get('topic', '')

        # Calculate coherence scores
        scores = {
            "warmup_to_content": self._score_warmup_connection(warmup, content, topic, vocabulary),
            "content_progression": self._score_content_progression(content),
            "activity_alignment": self._score_activity_alignment(activity, content, topic),
            "journal_reflection": self._score_journal_reflection(journal, content, topic),
            "vocabulary_integration": self._score_vocabulary_integration(vocabulary, content)
        }

        # Weighted average (equal weights)
        total_score = sum(scores.values()) / len(scores)

        passed = total_score >= self.THRESHOLD

        feedback = self._generate_feedback(scores)

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "coherence",
            "passed": passed,
            "total_score": round(total_score, 1),
            "threshold": self.THRESHOLD,
            "category_scores": scores,
            "feedback": feedback if not passed else [],
            "retry_strategy": "COHERENCE_FIX" if not passed else None
        }

    def _get_component(self, context: Dict, key: str) -> str:
        """Extract component text from context."""
        # Direct key
        value = context.get(key, '')
        if value:
            return str(value) if not isinstance(value, dict) else str(value)

        # From daily_input
        daily_input = context.get('daily_input', {})
        value = daily_input.get(key, '')
        if value:
            return str(value) if not isinstance(value, dict) else str(value)

        # From previous_outputs
        previous = context.get('previous_outputs', {})
        agent_map = {
            'warmup': 'warmup_generator',
            'activity': 'activity_generator',
            'journal_prompt': 'journal_exit_generator'
        }
        if key in agent_map and agent_map[key] in previous:
            output = previous[agent_map[key]]
            if key == 'journal_prompt':
                journal = output.get('journal', {})
                return journal.get('prompt', '') if isinstance(journal, dict) else str(journal)
            return str(output.get(key, ''))

        return ''

    def _score_warmup_connection(self, warmup: str, content: str, topic: str, vocabulary: Any) -> float:
        """Score how well warmup connects to lesson content."""
        if not warmup:
            return 50  # Neutral if missing

        warmup_lower = warmup.lower()
        score = 60  # Base score

        # Check if topic mentioned in warmup
        if topic and topic.lower() in warmup_lower:
            score += 20

        # Check if vocabulary terms appear
        if vocabulary:
            vocab_list = vocabulary if isinstance(vocabulary, list) else [vocabulary]
            vocab_count = sum(1 for v in vocab_list if str(v).lower() in warmup_lower)
            score += min(20, vocab_count * 5)

        return min(100, score)

    def _score_content_progression(self, content: str) -> float:
        """Score logical progression of content."""
        if not content:
            return 50

        content_lower = content.lower()
        score = 60

        # Check for progression indicators
        progression_words = ["first", "next", "then", "finally", "building on", "now that"]
        count = sum(1 for word in progression_words if word in content_lower)
        score += min(25, count * 5)

        # Check for transitions
        transitions = ["this leads", "as a result", "therefore", "moving on", "let's now"]
        trans_count = sum(1 for t in transitions if t in content_lower)
        score += min(15, trans_count * 5)

        return min(100, score)

    def _score_activity_alignment(self, activity: str, content: str, topic: str) -> float:
        """Score how well activity aligns with content."""
        if not activity:
            return 50

        activity_lower = activity.lower()
        score = 60

        # Check topic connection
        if topic and topic.lower() in activity_lower:
            score += 15

        # Check for application language
        application_words = ["apply", "practice", "demonstrate", "create", "perform", "try"]
        count = sum(1 for word in application_words if word in activity_lower)
        score += min(25, count * 10)

        return min(100, score)

    def _score_journal_reflection(self, journal: str, content: str, topic: str) -> float:
        """Score journal prompt's reflection on learning."""
        if not journal:
            return 50

        journal_lower = journal.lower()
        score = 60

        # Check for reflection language
        reflection_words = ["reflect", "think about", "consider", "what did you learn",
                           "how might", "why is", "what connections"]
        count = sum(1 for word in reflection_words if word in journal_lower)
        score += min(25, count * 10)

        # Topic connection
        if topic and topic.lower() in journal_lower:
            score += 15

        return min(100, score)

    def _score_vocabulary_integration(self, vocabulary: Any, content: str) -> float:
        """Score how well vocabulary is integrated into content."""
        if not vocabulary or not content:
            return 70  # Default if not applicable

        vocab_list = vocabulary if isinstance(vocabulary, list) else [vocabulary]
        content_lower = content.lower()

        integrated = sum(1 for v in vocab_list if str(v).lower() in content_lower)
        total = len(vocab_list)

        if total == 0:
            return 70

        return min(100, (integrated / total) * 100)

    def _generate_feedback(self, scores: Dict[str, float]) -> List[str]:
        """Generate feedback for low coherence scores."""
        feedback = []

        if scores["warmup_to_content"] < 70:
            feedback.append("Strengthen connection between warmup and lesson content")
        if scores["content_progression"] < 70:
            feedback.append("Add clearer progression and transitions in content")
        if scores["activity_alignment"] < 70:
            feedback.append("Ensure activity directly applies lesson concepts")
        if scores["journal_reflection"] < 70:
            feedback.append("Make journal prompt more explicitly reflective on learning")
        if scores["vocabulary_integration"] < 70:
            feedback.append("Integrate vocabulary terms more thoroughly into content")

        return feedback


class PedagogyValidatorAgent(Agent):
    """
    HARDCODED GATE: Validate sound teaching practices.

    Ensures lesson follows best practices:
    - Active engagement opportunities
    - Differentiation considerations
    - Clear learning objectives
    - Appropriate scaffolding
    - Formative assessment

    THRESHOLD: 80/100 minimum score
    """

    # Hardcoded threshold - DO NOT MODIFY
    THRESHOLD = 80

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Extract relevant content
        content = self._extract_all_content(context)
        objectives = context.get('learning_objectives', []) or context.get('daily_input', {}).get('learning_objectives', [])
        activity = self._get_component(context, 'activity')

        scores = {
            "engagement": self._score_engagement(content, activity),
            "differentiation": self._score_differentiation(content),
            "objectives_clarity": self._score_objectives(objectives),
            "scaffolding": self._score_scaffolding(content),
            "assessment": self._score_assessment(context)
        }

        total_score = sum(scores.values()) / len(scores)
        passed = total_score >= self.THRESHOLD

        feedback = self._generate_feedback(scores)

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "pedagogy",
            "passed": passed,
            "total_score": round(total_score, 1),
            "threshold": self.THRESHOLD,
            "category_scores": scores,
            "feedback": feedback if not passed else [],
            "retry_strategy": "PEDAGOGY_ENHANCEMENT" if not passed else None
        }

    def _extract_all_content(self, context: Dict) -> str:
        """Combine all lesson content for analysis."""
        parts = []

        # Get presenter notes
        notes = context.get('presenter_notes_writer_output', {})
        if notes:
            parts.append(notes.get('presenter_notes', ''))

        # Get content points
        content = context.get('content_points', '') or context.get('daily_input', {}).get('content_points', '')
        if content:
            parts.append(str(content))

        return ' '.join(parts)

    def _get_component(self, context: Dict, key: str) -> str:
        """Get component from context."""
        value = context.get(key, '')
        if value:
            return str(value)

        previous = context.get('previous_outputs', {})
        agent_map = {'activity': 'activity_generator'}
        if key in agent_map and agent_map[key] in previous:
            return str(previous[agent_map[key]].get(key, ''))

        return ''

    def _score_engagement(self, content: str, activity: str) -> float:
        """Score student engagement opportunities."""
        combined = (content + ' ' + activity).lower()
        score = 60

        # Active learning indicators
        engagement_words = [
            "discuss", "practice", "create", "analyze", "compare",
            "collaborate", "explore", "investigate", "demonstrate", "perform",
            "pair", "group", "share", "present"
        ]
        count = sum(1 for word in engagement_words if word in combined)
        score += min(40, count * 5)

        return min(100, score)

    def _score_differentiation(self, content: str) -> float:
        """Score differentiation considerations."""
        content_lower = content.lower()
        score = 60

        # Differentiation indicators
        diff_words = [
            "differentiat", "accommodat", "modif", "scaffold",
            "ell", "support", "extension", "challenge", "struggling",
            "advanced", "visual", "auditory", "kinesthetic"
        ]
        count = sum(1 for word in diff_words if word in content_lower)
        score += min(40, count * 8)

        return min(100, score)

    def _score_objectives(self, objectives: List) -> float:
        """Score clarity of learning objectives."""
        if not objectives:
            return 50

        obj_list = objectives if isinstance(objectives, list) else [objectives]
        score = 60

        # Check for measurable verbs (Bloom's taxonomy)
        blooms_verbs = [
            "identify", "explain", "describe", "analyze", "compare",
            "create", "evaluate", "demonstrate", "apply", "interpret",
            "define", "list", "classify", "summarize"
        ]

        objectives_text = ' '.join(str(o) for o in obj_list).lower()
        verb_count = sum(1 for verb in blooms_verbs if verb in objectives_text)
        score += min(40, verb_count * 10)

        return min(100, score)

    def _score_scaffolding(self, content: str) -> float:
        """Score scaffolding and support structures."""
        content_lower = content.lower()
        score = 60

        # Scaffolding indicators
        scaffold_words = [
            "model", "guide", "step", "example", "demonstrate",
            "support", "check for understanding", "review", "preview",
            "remind", "recall", "remember when"
        ]
        count = sum(1 for word in scaffold_words if word in content_lower)
        score += min(40, count * 5)

        return min(100, score)

    def _score_assessment(self, context: Dict) -> float:
        """Score formative assessment opportunities."""
        score = 60

        # Check for exit ticket
        exit_tickets = context.get('exit_tickets', [])
        if not exit_tickets:
            previous = context.get('previous_outputs', {})
            journal_gen = previous.get('journal_exit_generator', {})
            exit_tickets = journal_gen.get('exit_tickets', {}).get('questions', [])

        if exit_tickets:
            score += 20

        # Check for check-for-understanding indicators
        content = self._extract_all_content(context).lower()
        assessment_words = ["check", "assess", "ask", "question", "observe", "monitor"]
        count = sum(1 for word in assessment_words if word in content)
        score += min(20, count * 5)

        return min(100, score)

    def _generate_feedback(self, scores: Dict[str, float]) -> List[str]:
        """Generate pedagogy improvement feedback."""
        feedback = []

        if scores["engagement"] < 70:
            feedback.append("Add more active learning and student engagement opportunities")
        if scores["differentiation"] < 70:
            feedback.append("Include differentiation strategies for diverse learners")
        if scores["objectives_clarity"] < 70:
            feedback.append("Use measurable Bloom's taxonomy verbs in objectives")
        if scores["scaffolding"] < 70:
            feedback.append("Add scaffolding through modeling and guided practice")
        if scores["assessment"] < 70:
            feedback.append("Include formative assessment checkpoints")

        return feedback


class ContentAccuracyValidatorAgent(Agent):
    """
    HARDCODED GATE: Verify theater content accuracy.

    Ensures theater history and terminology is accurate:
    - Historical dates and facts
    - Theater terminology
    - Play and playwright information
    - Theater conventions by era

    Note: This validator checks for known inaccuracies
    rather than verifying all facts (which would require external DB).
    """

    # Common theater misconceptions and incorrect facts to flag
    KNOWN_INACCURACIES = {
        # Greek Theater
        "greek theater started in rome": "Greek theater originated in Athens, not Rome",
        "dionysus was god of war": "Dionysus was god of wine and theater, not war",
        "the chorus had only one person": "Greek chorus typically had 12-15 members",

        # Shakespeare
        "shakespeare was born in london": "Shakespeare was born in Stratford-upon-Avon",
        "globe theatre was round": "The Globe was actually polygonal (20-sided), not circular",
        "shakespeare wrote 50 plays": "Shakespeare wrote approximately 37-39 plays",

        # Commedia dell'Arte
        "commedia originated in france": "Commedia dell'Arte originated in Italy",
        "commedia was scripted": "Commedia was largely improvised from scenarios",
    }

    # Theater terminology with correct definitions
    TERMINOLOGY_CHECKS = {
        "soliloquy": ["alone", "thoughts", "audience"],
        "aside": ["audience", "other characters", "hear"],
        "monologue": ["speech", "character", "extended"],
        "blocking": ["movement", "stage", "positions"],
        "upstage": ["away", "audience", "back"],
        "downstage": ["toward", "audience", "front"],
    }

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = self._extract_all_content(context)
        content_lower = content.lower()

        issues = []

        # Check for known inaccuracies
        for inaccuracy, correction in self.KNOWN_INACCURACIES.items():
            if inaccuracy in content_lower:
                issues.append({
                    "type": "factual_error",
                    "found": inaccuracy,
                    "correction": correction
                })

        # Check terminology usage (light check)
        terminology_score = self._check_terminology(content_lower)

        # Calculate overall score
        base_score = 100
        score = base_score - (len(issues) * 15)  # -15 per inaccuracy
        score = max(0, score)

        # Boost score for correct terminology usage
        score = min(100, score + (terminology_score * 0.1))

        passed = len(issues) == 0

        return {
            "validation_status": "PASS" if passed else "FAIL",
            "gate_name": "content_accuracy",
            "passed": passed,
            "score": round(score, 1),
            "issues": issues,
            "terminology_score": terminology_score,
            "retry_strategy": "FACT_CHECK_FIX" if not passed else None
        }

    def _extract_all_content(self, context: Dict) -> str:
        """Extract all lesson content."""
        parts = []

        # Presenter notes
        notes = context.get('presenter_notes_writer_output', {})
        if notes:
            parts.append(notes.get('presenter_notes', ''))

        # Content points
        content = context.get('content_points', '')
        if content:
            parts.append(str(content))

        # Daily input topic
        daily = context.get('daily_input', {})
        if daily.get('topic'):
            parts.append(daily['topic'])

        return ' '.join(parts)

    def _check_terminology(self, content: str) -> float:
        """Check for correct terminology usage."""
        correct_uses = 0
        total_terms = 0

        for term, indicators in self.TERMINOLOGY_CHECKS.items():
            if term in content:
                total_terms += 1
                # Check if any context indicators are nearby
                term_pos = content.find(term)
                context_window = content[max(0, term_pos - 100):term_pos + 100]

                indicators_found = sum(1 for ind in indicators if ind in context_window)
                if indicators_found >= 1:
                    correct_uses += 1

        if total_terms == 0:
            return 50  # Neutral if no terms found

        return (correct_uses / total_terms) * 100
