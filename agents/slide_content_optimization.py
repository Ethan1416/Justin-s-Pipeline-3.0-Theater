"""
Slide Content Optimization Agents (HARDCODED)
==============================================

Specialized agents for optimizing slide content by:
- Condensing slide text for student note-taking
- Detecting and fixing truncated statements
- Balancing content between slides and presenter notes
- Validating content quality and completeness

These agents ensure slides are concise while presenter notes
contain full elaboration for teacher delivery.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import re

from .base import Agent, AgentResult, AgentStatus


# =============================================================================
# HARDCODED CONFIGURATION
# =============================================================================

# HARDCODED: Slide content constraints
SLIDE_CONTENT_CONFIG = {
    "max_words_per_bullet": 12,        # Maximum words per bullet point
    "max_bullets_per_slide": 5,        # Maximum bullet points per slide
    "max_words_per_slide": 50,         # Maximum total words on content area
    "max_title_words": 8,              # Maximum words in slide title
    "min_font_readability_words": 6,   # Minimum words for readability
    "target_note_taking_time": 30,     # Seconds students need to write a point
    "words_per_minute_writing": 15,    # Average student writing speed
}

# HARDCODED: Truncation detection patterns
TRUNCATION_PATTERNS = {
    "ellipsis": [
        r'\.\.\.$',                     # Ends with ...
        r'…$',                          # Ends with ellipsis character
        r'\.\.\.["\']?$',              # Ends with ... and optional quote
    ],
    "incomplete_sentence": [
        r'[a-z]$',                      # Ends with lowercase (no punctuation)
        r'\b(the|a|an|and|or|but|to|of|in|for|with|that|which|who)\s*$',  # Ends with article/preposition
        r',\s*$',                       # Ends with comma
        r';\s*$',                       # Ends with semicolon
    ],
    "cut_off_words": [
        r'\b\w{1,2}$',                  # Ends with 1-2 letter word (likely cut off)
        r'--$',                         # Ends with double dash
        r'-$',                          # Ends with hyphen (mid-word)
    ],
    "missing_closing": [
        r'\([^)]*$',                    # Open parenthesis without close
        r'"[^"]*$',                     # Open quote without close
        r"'[^']*$",                     # Open single quote without close
    ],
}

# HARDCODED: Paraphrasing rules for condensation
PARAPHRASE_RULES = {
    "remove_filler_words": [
        "basically", "essentially", "actually", "really", "very",
        "just", "simply", "in order to", "due to the fact that",
        "it is important to note that", "as a matter of fact",
    ],
    "shorten_phrases": {
        "in order to": "to",
        "due to the fact that": "because",
        "at this point in time": "now",
        "in the event that": "if",
        "for the purpose of": "to",
        "with regard to": "about",
        "in spite of the fact that": "although",
        "a large number of": "many",
        "the majority of": "most",
        "in close proximity to": "near",
        "at the present time": "now",
        "is able to": "can",
        "has the ability to": "can",
        "make a decision": "decide",
        "come to a conclusion": "conclude",
        "take into consideration": "consider",
    },
    "verb_simplifications": {
        "utilize": "use",
        "demonstrate": "show",
        "implement": "use",
        "facilitate": "help",
        "commence": "begin",
        "terminate": "end",
        "endeavor": "try",
        "ascertain": "find",
        "communicate": "tell",
        "indicate": "show",
    }
}

# HARDCODED: Validation thresholds
VALIDATION_THRESHOLDS = {
    "truncation_score_max": 0,          # No truncations allowed
    "condensation_ratio_min": 0.4,      # Slide should be 40% or less of full content
    "condensation_ratio_max": 0.7,      # But not less than 40% (too sparse)
    "note_elaboration_min": 2.0,        # Notes should be 2x slide content minimum
    "readability_grade_max": 8,         # Maximum reading grade level for slides
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TruncationIssue:
    """Details about a detected truncation."""
    text: str
    location: str  # "title", "bullet", "content"
    pattern_matched: str
    severity: str  # "critical", "warning", "minor"
    suggested_fix: str


@dataclass
class ContentAnalysis:
    """Analysis of slide content."""
    original_text: str
    word_count: int
    bullet_count: int
    truncation_issues: List[TruncationIssue]
    is_condensed: bool
    condensation_ratio: float
    readability_score: float


@dataclass
class SlideOptimizationResult:
    """Result of slide content optimization."""
    original_content: Dict[str, Any]
    optimized_content: Dict[str, Any]
    presenter_notes: str
    truncation_issues_found: int
    truncation_issues_fixed: int
    words_reduced: int
    validation_passed: bool


# =============================================================================
# TruncationDetectorAgent
# =============================================================================

class TruncationDetectorAgent(Agent):
    """
    HARDCODED agent for detecting truncated statements in content.

    Searches for:
    - Ellipsis endings (...)
    - Incomplete sentences
    - Cut-off words
    - Missing closing punctuation/brackets
    """

    def __init__(self):
        super().__init__(name="TruncationDetectorAgent")
        self.patterns = TRUNCATION_PATTERNS

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Detect truncation issues in content."""
        content = context.get("content", "")
        content_type = context.get("content_type", "text")  # "slide", "bullet", "title"

        if isinstance(content, list):
            # Process list of items (bullets)
            all_issues = []
            for i, item in enumerate(content):
                issues = self._detect_truncation(item, f"bullet_{i+1}")
                all_issues.extend(issues)

            return {
                "success": True,
                "has_truncation": len(all_issues) > 0,
                "truncation_count": len(all_issues),
                "issues": [self._issue_to_dict(issue) for issue in all_issues],
                "severity_summary": self._summarize_severity(all_issues),
            }
        else:
            # Process single text
            issues = self._detect_truncation(str(content), content_type)

            return {
                "success": True,
                "has_truncation": len(issues) > 0,
                "truncation_count": len(issues),
                "issues": [self._issue_to_dict(issue) for issue in issues],
                "severity_summary": self._summarize_severity(issues),
            }

    def _detect_truncation(self, text: str, location: str) -> List[TruncationIssue]:
        """Detect truncation in a single text string."""
        issues = []
        text = text.strip()

        if not text:
            return issues

        # Check each pattern category
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    severity = self._determine_severity(category)
                    suggested_fix = self._suggest_fix(text, category, pattern)

                    issue = TruncationIssue(
                        text=text,
                        location=location,
                        pattern_matched=f"{category}: {pattern}",
                        severity=severity,
                        suggested_fix=suggested_fix
                    )
                    issues.append(issue)
                    break  # Only report one issue per category

        return issues

    def _determine_severity(self, category: str) -> str:
        """Determine severity based on truncation category."""
        severity_map = {
            "ellipsis": "critical",
            "incomplete_sentence": "critical",
            "cut_off_words": "critical",
            "missing_closing": "warning",
        }
        return severity_map.get(category, "minor")

    def _suggest_fix(self, text: str, category: str, pattern: str) -> str:
        """Suggest a fix for the truncation."""
        if category == "ellipsis":
            return "Complete the sentence or remove trailing ellipsis"
        elif category == "incomplete_sentence":
            return "Add proper ending punctuation and complete the thought"
        elif category == "cut_off_words":
            return "Complete the word or sentence"
        elif category == "missing_closing":
            return "Add closing bracket, quote, or parenthesis"
        return "Review and complete the content"

    def _issue_to_dict(self, issue: TruncationIssue) -> Dict:
        """Convert TruncationIssue to dictionary."""
        return {
            "text": issue.text[:100] + "..." if len(issue.text) > 100 else issue.text,
            "location": issue.location,
            "pattern_matched": issue.pattern_matched,
            "severity": issue.severity,
            "suggested_fix": issue.suggested_fix,
        }

    def _summarize_severity(self, issues: List[TruncationIssue]) -> Dict[str, int]:
        """Summarize issues by severity."""
        summary = {"critical": 0, "warning": 0, "minor": 0}
        for issue in issues:
            summary[issue.severity] = summary.get(issue.severity, 0) + 1
        return summary


# =============================================================================
# TruncationFixerAgent
# =============================================================================

class TruncationFixerAgent(Agent):
    """
    HARDCODED agent for fixing truncated statements.

    Applies fixes based on truncation type:
    - Removes ellipsis and flags for completion
    - Completes common sentence patterns
    - Fixes missing punctuation
    """

    # HARDCODED: Common sentence completions
    COMPLETION_TEMPLATES = {
        "the": "the concept/element",
        "a": "a key point",
        "an": "an important aspect",
        "and": "and related concepts",
        "or": "or alternatives",
        "to": "to achieve the goal",
        "of": "of this topic",
        "in": "in this context",
        "for": "for this purpose",
        "with": "with these elements",
    }

    def __init__(self):
        super().__init__(name="TruncationFixerAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix truncation issues in content."""
        content = context.get("content", "")
        issues = context.get("issues", [])

        if isinstance(content, list):
            fixed_content = []
            fixes_applied = 0
            for item in content:
                fixed_item, was_fixed = self._fix_text(str(item))
                fixed_content.append(fixed_item)
                if was_fixed:
                    fixes_applied += 1

            return {
                "success": True,
                "original_content": content,
                "fixed_content": fixed_content,
                "fixes_applied": fixes_applied,
                "requires_review": fixes_applied > 0,
            }
        else:
            fixed_text, was_fixed = self._fix_text(str(content))

            return {
                "success": True,
                "original_content": content,
                "fixed_content": fixed_text,
                "fixes_applied": 1 if was_fixed else 0,
                "requires_review": was_fixed,
            }

    def _fix_text(self, text: str) -> Tuple[str, bool]:
        """Fix truncation in a single text string."""
        original = text
        text = text.strip()
        was_fixed = False

        if not text:
            return text, False

        # Fix ellipsis endings
        if text.endswith('...') or text.endswith('…'):
            text = re.sub(r'\.\.\.+$|…$', '.', text)
            was_fixed = True

        # Fix incomplete sentences ending with articles/prepositions
        for word, completion in self.COMPLETION_TEMPLATES.items():
            pattern = rf'\b{word}\s*$'
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, completion + '.', text, flags=re.IGNORECASE)
                was_fixed = True
                break

        # Fix missing closing punctuation
        if text and text[-1].isalpha():
            text = text + '.'
            was_fixed = True

        # Fix missing closing brackets/quotes
        if text.count('(') > text.count(')'):
            text = text + ')'
            was_fixed = True
        if text.count('"') % 2 == 1:
            text = text + '"'
            was_fixed = True

        # Fix comma/semicolon endings
        if text.endswith(',') or text.endswith(';'):
            text = text[:-1] + '.'
            was_fixed = True

        # Fix double-dash endings
        if text.endswith('--') or text.endswith('-'):
            text = re.sub(r'-+$', '.', text)
            was_fixed = True

        return text, was_fixed


# =============================================================================
# SlideContentCondensationAgent
# =============================================================================

class SlideContentCondensationAgent(Agent):
    """
    HARDCODED agent for condensing slide content.

    Paraphrases verbose content into concise bullet points
    suitable for student note-taking while preserving meaning.
    """

    def __init__(self):
        super().__init__(name="SlideContentCondensationAgent")
        self.config = SLIDE_CONTENT_CONFIG
        self.rules = PARAPHRASE_RULES

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Condense content for slide display."""
        content = context.get("content", "")
        content_type = context.get("content_type", "bullet")  # "title", "bullet", "paragraph"

        if isinstance(content, list):
            condensed = []
            for item in content:
                condensed_item = self._condense_text(str(item), content_type)
                condensed.append(condensed_item)

            original_words = sum(len(str(item).split()) for item in content)
            condensed_words = sum(len(item.split()) for item in condensed)

            return {
                "success": True,
                "original_content": content,
                "condensed_content": condensed,
                "original_word_count": original_words,
                "condensed_word_count": condensed_words,
                "reduction_percentage": round((1 - condensed_words/max(original_words, 1)) * 100, 1),
            }
        else:
            condensed = self._condense_text(str(content), content_type)
            original_words = len(str(content).split())
            condensed_words = len(condensed.split())

            return {
                "success": True,
                "original_content": content,
                "condensed_content": condensed,
                "original_word_count": original_words,
                "condensed_word_count": condensed_words,
                "reduction_percentage": round((1 - condensed_words/max(original_words, 1)) * 100, 1),
            }

    def _condense_text(self, text: str, content_type: str) -> str:
        """Condense a single text string."""
        if not text:
            return text

        # Get max words based on content type
        if content_type == "title":
            max_words = self.config["max_title_words"]
        elif content_type == "bullet":
            max_words = self.config["max_words_per_bullet"]
        else:
            max_words = self.config["max_words_per_slide"]

        # Step 1: Remove filler words
        condensed = text
        for filler in self.rules["remove_filler_words"]:
            pattern = rf'\b{re.escape(filler)}\b\s*'
            condensed = re.sub(pattern, '', condensed, flags=re.IGNORECASE)

        # Step 2: Apply phrase shortenings
        for long_phrase, short_phrase in self.rules["shorten_phrases"].items():
            pattern = rf'\b{re.escape(long_phrase)}\b'
            condensed = re.sub(pattern, short_phrase, condensed, flags=re.IGNORECASE)

        # Step 3: Simplify verbs
        for complex_verb, simple_verb in self.rules["verb_simplifications"].items():
            pattern = rf'\b{re.escape(complex_verb)}\b'
            condensed = re.sub(pattern, simple_verb, condensed, flags=re.IGNORECASE)

        # Step 4: Clean up whitespace
        condensed = ' '.join(condensed.split())

        # Step 5: Truncate to max words if still too long (but mark for review)
        words = condensed.split()
        if len(words) > max_words:
            # Extract key noun phrases instead of just truncating
            condensed = self._extract_key_phrase(condensed, max_words)

        return condensed

    def _extract_key_phrase(self, text: str, max_words: int) -> str:
        """Extract the most important phrase from text."""
        words = text.split()

        # Look for key patterns to preserve
        # Pattern: Subject + Verb + Object (keep core meaning)

        # Simple approach: keep first max_words but end at sentence boundary
        truncated = ' '.join(words[:max_words])

        # Ensure it doesn't end mid-thought
        if not truncated.endswith(('.', '!', '?', ':')):
            # Find last complete phrase
            last_punct = max(
                truncated.rfind('.'),
                truncated.rfind(':'),
                truncated.rfind(';'),
                truncated.rfind(',')
            )
            if last_punct > len(truncated) // 2:
                truncated = truncated[:last_punct + 1]

        return truncated


# =============================================================================
# PresenterNotesElaboratorAgent
# =============================================================================

class PresenterNotesElaboratorAgent(Agent):
    """
    HARDCODED agent for creating elaborated presenter notes.

    Takes condensed slide content and generates detailed
    presenter notes with:
    - Full explanations
    - Teaching cues
    - Discussion prompts
    - Timing guidance
    """

    # HARDCODED: Note templates by slide type
    NOTE_TEMPLATES = {
        "content": """CONTENT: {title}

FULL EXPLANATION:
{full_content}

KEY POINTS TO EMPHASIZE:
{key_points}

[TEACHING CUES]
- Pause after each point for student note-taking (30 seconds)
- Check for understanding: "Can someone summarize this point?"
- Use specific examples from the text

[DISCUSSION PROMPT]
{discussion_prompt}

[TIMING] Spend approximately {timing} minutes on this slide.
""",
        "vocabulary": """VOCABULARY: {term}

DEFINITION: {definition}

ELABORATION:
{elaboration}

[TEACHING METHOD]
1. Say the word clearly: "{term}"
2. Have students repeat
3. Read definition together
4. Provide example in context
5. Students write in notes (allow 30 seconds)

[EXAMPLE IN CONTEXT]
{example}
""",
        "activity": """ACTIVITY: {title}

FULL INSTRUCTIONS:
{full_instructions}

[SETUP STEPS]
{setup_steps}

[FACILITATION NOTES]
- Circulate and monitor progress
- Provide scaffolding for struggling students
- Challenge advanced students with extension

[TIMING]
- Introduction: 2 minutes
- Work time: {work_time} minutes
- Debrief: 3 minutes
"""
    }

    def __init__(self):
        super().__init__(name="PresenterNotesElaboratorAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate elaborated presenter notes from condensed content."""
        slide_type = context.get("slide_type", "content")
        condensed_content = context.get("condensed_content", "")
        full_content = context.get("full_content", "")
        additional_context = context.get("additional_context", {})

        # Generate elaborated notes based on slide type
        if slide_type == "vocabulary":
            notes = self._elaborate_vocabulary(condensed_content, full_content, additional_context)
        elif slide_type == "activity":
            notes = self._elaborate_activity(condensed_content, full_content, additional_context)
        else:
            notes = self._elaborate_content(condensed_content, full_content, additional_context)

        return {
            "success": True,
            "slide_type": slide_type,
            "presenter_notes": notes,
            "word_count": len(notes.split()),
            "estimated_speaking_time": round(len(notes.split()) / 150, 1),  # minutes at 150 WPM
        }

    def _elaborate_content(self, condensed: str, full: str, context: Dict) -> str:
        """Elaborate content slide notes."""
        title = context.get("title", condensed[:50])

        # Generate key points from full content
        key_points = self._extract_key_points(full or condensed)

        # Generate discussion prompt
        discussion = self._generate_discussion_prompt(title, full or condensed)

        # Estimate timing
        timing = max(2, len((full or condensed).split()) // 50)

        return self.NOTE_TEMPLATES["content"].format(
            title=title,
            full_content=full or condensed,
            key_points=key_points,
            discussion_prompt=discussion,
            timing=timing
        )

    def _elaborate_vocabulary(self, condensed: str, full: str, context: Dict) -> str:
        """Elaborate vocabulary slide notes."""
        term = context.get("term", "")
        definition = context.get("definition", condensed)

        # Generate elaboration
        elaboration = f"This term is essential for understanding Shakespeare's work. {full or definition}"

        # Generate example
        example = context.get("example", f'For example, we see this concept when characters discuss "{term}" in the play.')

        return self.NOTE_TEMPLATES["vocabulary"].format(
            term=term,
            definition=definition,
            elaboration=elaboration,
            example=example
        )

    def _elaborate_activity(self, condensed: str, full: str, context: Dict) -> str:
        """Elaborate activity slide notes."""
        title = context.get("title", "Activity")
        work_time = context.get("duration", 15)

        setup_steps = context.get("setup_steps", "1. Distribute materials\n2. Form groups\n3. Explain expectations")

        return self.NOTE_TEMPLATES["activity"].format(
            title=title,
            full_instructions=full or condensed,
            setup_steps=setup_steps,
            work_time=work_time
        )

    def _extract_key_points(self, content: str) -> str:
        """Extract key points from content."""
        sentences = content.split('.')
        key_points = []

        for i, sentence in enumerate(sentences[:5]):  # First 5 sentences
            sentence = sentence.strip()
            if sentence and len(sentence) > 20:
                key_points.append(f"- {sentence}")

        return '\n'.join(key_points) if key_points else "- Review the main concept with students"

    def _generate_discussion_prompt(self, title: str, content: str) -> str:
        """Generate a discussion prompt based on content."""
        prompts = [
            f"Ask students: 'Why do you think {title.lower()} is important to the story?'",
            f"Discussion: 'How does this connect to what we learned yesterday?'",
            f"Think-Pair-Share: 'What surprised you about this?'",
            f"Quick write: 'In your own words, explain this concept.'",
        ]
        # Select based on content hash for consistency
        return prompts[len(content) % len(prompts)]


# =============================================================================
# SlideContentValidatorAgent
# =============================================================================

class SlideContentValidatorAgent(Agent):
    """
    HARDCODED validator agent for slide content optimization.

    Validates:
    - No truncation in content
    - Proper condensation ratio
    - Adequate presenter notes elaboration
    - Note-taking feasibility
    """

    def __init__(self):
        super().__init__(name="SlideContentValidatorAgent")
        self.config = SLIDE_CONTENT_CONFIG
        self.thresholds = VALIDATION_THRESHOLDS

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate slide content optimization."""
        slide_content = context.get("slide_content", {})
        presenter_notes = context.get("presenter_notes", "")
        truncation_issues = context.get("truncation_issues", [])

        errors = []
        warnings = []

        # Validate no truncation
        if truncation_issues:
            critical_count = sum(1 for i in truncation_issues if i.get("severity") == "critical")
            if critical_count > 0:
                errors.append(f"Found {critical_count} critical truncation issues - must be fixed")
            warning_count = sum(1 for i in truncation_issues if i.get("severity") == "warning")
            if warning_count > 0:
                warnings.append(f"Found {warning_count} truncation warnings - should review")

        # Validate slide content length
        slide_words = self._count_slide_words(slide_content)
        if slide_words > self.config["max_words_per_slide"]:
            errors.append(f"Slide has {slide_words} words (max: {self.config['max_words_per_slide']})")

        # Validate bullet count
        bullet_count = self._count_bullets(slide_content)
        if bullet_count > self.config["max_bullets_per_slide"]:
            warnings.append(f"Slide has {bullet_count} bullets (max: {self.config['max_bullets_per_slide']})")

        # Validate individual bullet length
        long_bullets = self._check_bullet_lengths(slide_content)
        if long_bullets:
            warnings.append(f"{len(long_bullets)} bullets exceed {self.config['max_words_per_bullet']} words")

        # Validate presenter notes elaboration
        notes_words = len(presenter_notes.split()) if presenter_notes else 0
        if notes_words < slide_words * self.thresholds["note_elaboration_min"]:
            warnings.append(f"Presenter notes ({notes_words} words) should be at least {self.thresholds['note_elaboration_min']}x slide content")

        # Validate note-taking feasibility
        note_taking_time = self._estimate_note_taking_time(slide_content)
        if note_taking_time > 120:  # More than 2 minutes to take notes
            warnings.append(f"Estimated note-taking time ({note_taking_time}s) may be too long")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "metrics": {
                "slide_word_count": slide_words,
                "bullet_count": bullet_count,
                "notes_word_count": notes_words,
                "estimated_note_taking_seconds": note_taking_time,
                "truncation_issues": len(truncation_issues),
            }
        }

    def _count_slide_words(self, content: Dict) -> int:
        """Count total words in slide content."""
        total = 0
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, str):
                    total += len(value.split())
                elif isinstance(value, list):
                    total += sum(len(str(item).split()) for item in value)
        elif isinstance(content, str):
            total = len(content.split())
        elif isinstance(content, list):
            total = sum(len(str(item).split()) for item in content)
        return total

    def _count_bullets(self, content: Dict) -> int:
        """Count bullet points in slide content."""
        if isinstance(content, dict):
            for key, value in content.items():
                if isinstance(value, list):
                    return len(value)
        elif isinstance(content, list):
            return len(content)
        return 0

    def _check_bullet_lengths(self, content: Dict) -> List[str]:
        """Find bullets that exceed max word count."""
        long_bullets = []
        max_words = self.config["max_words_per_bullet"]

        items = []
        if isinstance(content, dict):
            for value in content.values():
                if isinstance(value, list):
                    items.extend(value)
        elif isinstance(content, list):
            items = content

        for item in items:
            if len(str(item).split()) > max_words:
                long_bullets.append(str(item))

        return long_bullets

    def _estimate_note_taking_time(self, content: Dict) -> int:
        """Estimate seconds needed for students to take notes."""
        words = self._count_slide_words(content)
        wpm = self.config["words_per_minute_writing"]
        return int((words / wpm) * 60)


# =============================================================================
# ContentBalanceOrchestratorAgent
# =============================================================================

class ContentBalanceOrchestratorAgent(Agent):
    """
    HARDCODED orchestrator agent for balancing slide content and presenter notes.

    Coordinates:
    1. Truncation detection
    2. Truncation fixing
    3. Content condensation
    4. Notes elaboration
    5. Final validation
    """

    def __init__(self):
        super().__init__(name="ContentBalanceOrchestratorAgent")
        self.truncation_detector = TruncationDetectorAgent()
        self.truncation_fixer = TruncationFixerAgent()
        self.condenser = SlideContentCondensationAgent()
        self.elaborator = PresenterNotesElaboratorAgent()
        self.validator = SlideContentValidatorAgent()

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate full content optimization pipeline."""
        original_content = context.get("content", "")
        slide_type = context.get("slide_type", "content")
        additional_context = context.get("additional_context", {})

        results = {
            "success": True,
            "steps_completed": [],
            "errors": [],
            "warnings": [],
        }

        # Step 1: Detect truncation
        detection_result = self.truncation_detector.execute({
            "content": original_content,
            "content_type": slide_type
        })
        results["steps_completed"].append("truncation_detection")
        results["truncation_detected"] = detection_result.output.get("has_truncation", False)

        # Step 2: Fix truncation if found
        if detection_result.output.get("has_truncation"):
            fix_result = self.truncation_fixer.execute({
                "content": original_content,
                "issues": detection_result.output.get("issues", [])
            })
            results["steps_completed"].append("truncation_fixing")
            working_content = fix_result.output.get("fixed_content", original_content)
            results["truncation_fixes_applied"] = fix_result.output.get("fixes_applied", 0)
        else:
            working_content = original_content
            results["truncation_fixes_applied"] = 0

        # Step 3: Condense content for slides
        condense_result = self.condenser.execute({
            "content": working_content,
            "content_type": slide_type
        })
        results["steps_completed"].append("content_condensation")
        condensed_content = condense_result.output.get("condensed_content", working_content)
        results["condensation_stats"] = {
            "original_words": condense_result.output.get("original_word_count", 0),
            "condensed_words": condense_result.output.get("condensed_word_count", 0),
            "reduction_percentage": condense_result.output.get("reduction_percentage", 0),
        }

        # Step 4: Elaborate presenter notes
        elaborate_result = self.elaborator.execute({
            "slide_type": slide_type,
            "condensed_content": condensed_content,
            "full_content": working_content,
            "additional_context": additional_context
        })
        results["steps_completed"].append("notes_elaboration")
        presenter_notes = elaborate_result.output.get("presenter_notes", "")
        results["notes_stats"] = {
            "word_count": elaborate_result.output.get("word_count", 0),
            "speaking_time_minutes": elaborate_result.output.get("estimated_speaking_time", 0),
        }

        # Step 5: Validate final output
        # Re-check for truncation in condensed content
        final_detection = self.truncation_detector.execute({
            "content": condensed_content,
            "content_type": slide_type
        })

        validation_result = self.validator.execute({
            "slide_content": condensed_content,
            "presenter_notes": presenter_notes,
            "truncation_issues": final_detection.output.get("issues", [])
        })
        results["steps_completed"].append("validation")
        results["validation_passed"] = validation_result.output.get("valid", False)
        results["errors"].extend(validation_result.output.get("errors", []))
        results["warnings"].extend(validation_result.output.get("warnings", []))
        results["validation_metrics"] = validation_result.output.get("metrics", {})

        # Final output
        results["original_content"] = original_content
        results["optimized_slide_content"] = condensed_content
        results["presenter_notes"] = presenter_notes
        results["success"] = validation_result.output.get("valid", False) and len(results["errors"]) == 0

        return results

    def optimize_slide_deck(self, slides: List[Dict]) -> List[Dict]:
        """Optimize an entire slide deck."""
        optimized_slides = []

        for slide in slides:
            result = self.execute({
                "content": slide.get("content", ""),
                "slide_type": slide.get("type", "content"),
                "additional_context": slide.get("context", {})
            })

            optimized_slide = slide.copy()
            optimized_slide["content"] = result.output.get("optimized_slide_content", slide.get("content"))
            optimized_slide["presenter_notes"] = result.output.get("presenter_notes", "")
            optimized_slide["optimization_results"] = {
                "success": result.output.get("success"),
                "warnings": result.output.get("warnings", []),
            }
            optimized_slides.append(optimized_slide)

        return optimized_slides
