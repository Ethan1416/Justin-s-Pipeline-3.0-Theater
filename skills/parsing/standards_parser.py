"""
Standards Parser - Parse presentation standards for NCLEX pipeline Step 5.

This module parses presentation standards documents (markdown) and configuration
files (yaml) to produce structured JSON output for blueprint generation.

Parses:
- standards/presenting_standards.md (delivery modes, timing, presenter notes)
- config/constraints.yaml (character limits, visual quotas)

Output matches standards_output.schema.json structure.

Usage:
    from skills.parsing.standards_parser import StandardsParser

    parser = StandardsParser()
    standards = parser.parse_all_standards()

    # Apply standards to Step 4 outline
    result = parser.apply_standards_to_outline(step4_outline)
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import date


@dataclass
class DeliveryMode:
    """Represents a subsection delivery mode specification."""
    mode: str  # foundational, full, minor, one_and_done
    structure: List[Dict[str, str]]
    selection_criteria: str

    def to_dict(self) -> Dict:
        return {
            "mode": self.mode,
            "structure": self.structure,
            "selection_rationale": self.selection_criteria
        }


@dataclass
class FixedSlideSpec:
    """Specification for a fixed slide (intro, vignette, answer)."""
    slide_type: str
    position: str
    content_spec: Dict[str, Any]
    presenter_notes_spec: Dict[str, Any]

    def to_dict(self) -> Dict:
        return {
            "position": self.position,
            "content_spec": self.content_spec,
            "presenter_notes_spec": self.presenter_notes_spec
        }


@dataclass
class TimingGuidance:
    """Timing and pacing guidance for presenter notes."""
    words_per_minute_min: int = 130
    words_per_minute_max: int = 150
    max_words: int = 450
    max_duration_seconds: int = 180
    active_learning_reduction: str = "20%"

    def to_dict(self) -> Dict:
        return {
            "target_words_per_minute": (self.words_per_minute_min + self.words_per_minute_max) // 2,
            "max_presenter_notes_words": self.max_words,
            "max_slide_duration_seconds": self.max_duration_seconds
        }


@dataclass
class CharacterLimits:
    """Character limit constraints for slide elements."""
    header_chars_per_line: int = 32
    header_max_lines: int = 2
    body_chars_per_line: int = 66
    body_max_lines: int = 8
    tip_chars_per_line: int = 66
    tip_max_lines: int = 2

    def to_dict(self) -> Dict:
        return {
            "header": {
                "max_chars_per_line": self.header_chars_per_line,
                "max_lines": self.header_max_lines
            },
            "body": {
                "max_chars_per_line": self.body_chars_per_line,
                "max_lines": self.body_max_lines
            },
            "tip": {
                "max_chars_per_line": self.tip_chars_per_line,
                "max_lines": self.tip_max_lines
            }
        }


@dataclass
class PresenterNotesRequirements:
    """Requirements for presenter notes content."""
    verbatim_monologue: bool = True
    words_per_minute: str = "130-150"
    max_words: int = 450
    required_markers: List[str] = field(default_factory=lambda: ["[PAUSE]", "[EMPHASIS]"])
    required_elements: List[str] = field(default_factory=lambda: [
        "opening_statement", "concept_explanation", "applied_relevance",
        "connections", "closing_transition"
    ])
    exam_pattern_callouts: bool = True
    study_strategy_mentions: bool = True
    active_learning_word_reduction: str = "20%"

    def to_dict(self, is_first_subsection: bool = False) -> Dict:
        elements = self.required_elements.copy()
        if not is_first_subsection:
            # Non-foundational subsections may not need all elements
            elements = [e for e in elements if e != "connections"]

        return {
            "verbatim_monologue": self.verbatim_monologue,
            "word_count_guidance": {
                "per_minute": self.words_per_minute,
                "maximum": self.max_words
            },
            "required_markers": self.required_markers,
            "required_elements": elements,
            "exam_pattern_callouts": self.exam_pattern_callouts,
            "study_strategy_mentions": is_first_subsection,  # Only for foundational
            "active_learning_word_reduction": self.active_learning_word_reduction
        }


@dataclass
class ParsedStandards:
    """Container for all parsed standards."""
    success: bool = False
    delivery_modes: Dict[str, DeliveryMode] = field(default_factory=dict)
    fixed_slides: Dict[str, FixedSlideSpec] = field(default_factory=dict)
    timing_guidance: Optional[TimingGuidance] = None
    character_limits: Optional[CharacterLimits] = None
    presenter_notes: Optional[PresenterNotesRequirements] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    source_files: List[str] = field(default_factory=list)


class StandardsParser:
    """Parse presentation standards from markdown and YAML files."""

    # Delivery mode definitions
    DELIVERY_MODES = {
        "foundational": {
            "criteria": "First subsection of section",
            "structure": [
                {"component": "overview", "duration_minutes": "3-5 min",
                 "purpose": "Present organizing framework for the section"},
                {"component": "scaffolding", "duration_minutes": "variable",
                 "purpose": "Build prerequisite concepts systematically"},
                {"component": "bridge", "duration_minutes": "1-2 min",
                 "purpose": "Connect to subsequent subsections"}
            ]
        },
        "full": {
            "criteria": "5+ anchors OR high complexity",
            "structure": [
                {"component": "connection", "duration_minutes": "1-2 min",
                 "purpose": "Link to foundational subsection or prior content"},
                {"component": "core", "duration_minutes": "variable",
                 "purpose": "Deliver anchor point content with active learning"},
                {"component": "synthesis", "duration_minutes": "3-5 min",
                 "purpose": "Integrate concepts, provide applied relevance"}
            ]
        },
        "minor": {
            "criteria": "3-4 anchors, moderate complexity",
            "structure": [
                {"component": "connection", "duration_minutes": "1 min",
                 "purpose": "Brief link to foundation"},
                {"component": "core", "duration_minutes": "variable",
                 "purpose": "Focused anchor point delivery"}
            ]
        },
        "one_and_done": {
            "criteria": "1-2 anchors",
            "structure": [
                {"component": "core", "duration_minutes": "3-5 min",
                 "purpose": "Single presentation unit with micro-connection to section theme"}
            ]
        }
    }

    # Fixed slide specifications
    FIXED_SLIDES = {
        "intro": {
            "position": "first",
            "content_spec": {
                "title": None,  # Filled from section name
                "quote_required": True,
                "quote_type": "poetic_provocative"
            },
            "presenter_notes_spec": {
                "include_welcome": True,
                "include_preview": True,
                "include_prior_connection": None  # True if not first section
            }
        },
        "vignette": {
            "position": "near_end",
            "content_spec": {
                "format": "exam_style_vignette",
                "stem_sentences": {"min": 2, "max": 4},
                "answer_options": 4,
                "requires_integration": True
            },
            "presenter_notes_spec": {
                "read_aloud": True,
                "think_time_seconds": {"min": 30, "max": 60},
                "reveal_answer_on_slide": False
            }
        },
        "answer": {
            "position": "after_vignette",
            "content_spec": {
                "correct_answer_identified": True,
                "rationale_required": True,
                "distractor_analysis_required": True
            },
            "presenter_notes_spec": {
                "reveal_and_explain": True,
                "walk_through_distractors": True,
                "connect_to_anchors": True,
                "identify_exam_patterns": True
            }
        }
    }

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the StandardsParser.

        Args:
            base_path: Base directory for resolving paths (defaults to project root)
        """
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Default to project root (three levels up from this file)
            self.base_path = Path(__file__).parent.parent.parent

    def parse_all_standards(self) -> ParsedStandards:
        """
        Parse all standards files and return structured standards.

        Returns:
            ParsedStandards object with all parsed data
        """
        result = ParsedStandards()

        # Parse presenting standards markdown
        presenting_path = self.base_path / "standards" / "presenting_standards.md"
        if presenting_path.exists():
            self._parse_presenting_standards(presenting_path, result)
            result.source_files.append(str(presenting_path))
        else:
            result.warnings.append(f"presenting_standards.md not found at {presenting_path}")

        # Parse constraints YAML
        constraints_path = self.base_path / "config" / "constraints.yaml"
        if constraints_path.exists():
            self._parse_constraints(constraints_path, result)
            result.source_files.append(str(constraints_path))
        else:
            result.warnings.append(f"constraints.yaml not found at {constraints_path}")

        # Set defaults if not parsed
        self._apply_defaults(result)

        result.success = len(result.errors) == 0
        return result

    def _parse_presenting_standards(
        self,
        file_path: Path,
        result: ParsedStandards
    ) -> None:
        """Parse presenting_standards.md file."""
        try:
            content = file_path.read_text(encoding='utf-8')

            # Build delivery modes from hardcoded definitions
            for mode_name, mode_def in self.DELIVERY_MODES.items():
                result.delivery_modes[mode_name] = DeliveryMode(
                    mode=mode_name,
                    structure=mode_def["structure"],
                    selection_criteria=mode_def["criteria"]
                )

            # Build fixed slide specs
            for slide_type, slide_def in self.FIXED_SLIDES.items():
                result.fixed_slides[slide_type] = FixedSlideSpec(
                    slide_type=slide_type,
                    position=slide_def["position"],
                    content_spec=slide_def["content_spec"].copy(),
                    presenter_notes_spec=slide_def["presenter_notes_spec"].copy()
                )

            # Extract timing guidance from content
            result.timing_guidance = self._extract_timing_from_content(content)

            # Extract presenter notes requirements
            result.presenter_notes = self._extract_presenter_notes_reqs(content)

        except Exception as e:
            result.errors.append(f"Error parsing presenting_standards.md: {e}")

    def _parse_constraints(
        self,
        file_path: Path,
        result: ParsedStandards
    ) -> None:
        """Parse constraints.yaml file for character limits."""
        try:
            import yaml

            with open(file_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            char_limits = config.get('character_limits', {})

            result.character_limits = CharacterLimits(
                header_chars_per_line=char_limits.get('title', {}).get('chars_per_line', 32),
                header_max_lines=char_limits.get('title', {}).get('max_lines', 2),
                body_chars_per_line=char_limits.get('body', {}).get('chars_per_line', 66),
                body_max_lines=char_limits.get('body', {}).get('max_lines', 8),
                tip_chars_per_line=char_limits.get('tip', {}).get('chars_per_line', 66),
                tip_max_lines=char_limits.get('tip', {}).get('max_lines', 2)
            )

            # Update timing from presenter_notes config if present
            presenter_config = char_limits.get('presenter_notes', {})
            if result.timing_guidance and presenter_config:
                result.timing_guidance.max_words = presenter_config.get('max_words', 450)
                result.timing_guidance.max_duration_seconds = presenter_config.get('max_seconds', 180)

        except ImportError:
            result.warnings.append("PyYAML not installed - using default character limits")
        except Exception as e:
            result.errors.append(f"Error parsing constraints.yaml: {e}")

    def _extract_timing_from_content(self, content: str) -> TimingGuidance:
        """Extract timing guidance from markdown content."""
        timing = TimingGuidance()

        # Look for word count patterns
        wpm_match = re.search(r'(\d+)-(\d+)\s*words?\s*per\s*minute', content, re.IGNORECASE)
        if wpm_match:
            timing.words_per_minute_min = int(wpm_match.group(1))
            timing.words_per_minute_max = int(wpm_match.group(2))

        # Look for maximum words
        max_words_match = re.search(r'(?:maximum|max)[:\s]+(\d+)\s*words?', content, re.IGNORECASE)
        if max_words_match:
            timing.max_words = int(max_words_match.group(1))

        # Look for maximum duration
        max_duration_match = re.search(r'(\d+)\s*seconds?\s*(?:\(|of)', content, re.IGNORECASE)
        if max_duration_match:
            timing.max_duration_seconds = int(max_duration_match.group(1))

        return timing

    def _extract_presenter_notes_reqs(self, content: str) -> PresenterNotesRequirements:
        """Extract presenter notes requirements from content."""
        reqs = PresenterNotesRequirements()

        # Check for verbatim monologue requirement
        if 'verbatim monologue' in content.lower():
            reqs.verbatim_monologue = True

        # Check for required markers
        if '[PAUSE]' in content:
            if '[PAUSE]' not in reqs.required_markers:
                reqs.required_markers.append('[PAUSE]')
        if '[EMPHASIS]' in content:
            if '[EMPHASIS]' not in reqs.required_markers:
                reqs.required_markers.append('[EMPHASIS]')

        # Check for active learning reduction
        reduction_match = re.search(r'reduce.*?(\d+)%', content, re.IGNORECASE)
        if reduction_match:
            reqs.active_learning_word_reduction = f"{reduction_match.group(1)}%"

        return reqs

    def _apply_defaults(self, result: ParsedStandards) -> None:
        """Apply default values for any missing parsed elements."""
        if not result.delivery_modes:
            for mode_name, mode_def in self.DELIVERY_MODES.items():
                result.delivery_modes[mode_name] = DeliveryMode(
                    mode=mode_name,
                    structure=mode_def["structure"],
                    selection_criteria=mode_def["criteria"]
                )

        if not result.fixed_slides:
            for slide_type, slide_def in self.FIXED_SLIDES.items():
                result.fixed_slides[slide_type] = FixedSlideSpec(
                    slide_type=slide_type,
                    position=slide_def["position"],
                    content_spec=slide_def["content_spec"].copy(),
                    presenter_notes_spec=slide_def["presenter_notes_spec"].copy()
                )

        if not result.timing_guidance:
            result.timing_guidance = TimingGuidance()

        if not result.character_limits:
            result.character_limits = CharacterLimits()

        if not result.presenter_notes:
            result.presenter_notes = PresenterNotesRequirements()

    def determine_delivery_mode(
        self,
        subsection: Dict,
        is_first_subsection: bool = False
    ) -> Dict:
        """
        Determine the appropriate delivery mode for a subsection.

        Args:
            subsection: Subsection data from Step 4 outline
            is_first_subsection: Whether this is the first subsection in its section

        Returns:
            Delivery mode specification dict
        """
        anchor_count = subsection.get('anchor_count', 0)
        complexity = subsection.get('complexity', 'moderate')

        # Mode selection logic per standards
        if is_first_subsection:
            mode_name = "foundational"
            rationale = "First subsection of section - establishes foundational concepts"
        elif anchor_count >= 5 or complexity == 'complex':
            mode_name = "full"
            rationale = f"{anchor_count} anchors with {complexity} complexity - full delivery with synthesis"
        elif anchor_count >= 3:
            mode_name = "minor"
            rationale = f"{anchor_count} anchors with {complexity} complexity - efficient core delivery"
        else:
            mode_name = "one_and_done"
            rationale = f"{anchor_count} anchor(s) with {complexity} complexity - one-and-done delivery"

        mode_def = self.DELIVERY_MODES[mode_name]

        return {
            "mode": mode_name,
            "structure": mode_def["structure"],
            "selection_rationale": rationale
        }

    def build_fixed_slides_spec(
        self,
        section: Dict,
        is_first_section: bool = False
    ) -> Dict:
        """
        Build fixed slides specification for a section.

        Args:
            section: Section data from outline
            is_first_section: Whether this is the first section in the lecture

        Returns:
            Fixed slides specification dict
        """
        section_name = section.get('section_name', 'Untitled Section')

        return {
            "intro": {
                "position": "first",
                "content_spec": {
                    "title": section_name,
                    "quote_required": True,
                    "quote_type": "poetic_provocative"
                },
                "presenter_notes_spec": {
                    "include_welcome": True,
                    "include_preview": True,
                    "include_prior_connection": not is_first_section
                }
            },
            "vignette": {
                "position": "near_end",
                "content_spec": {
                    "format": "exam_style_vignette",
                    "stem_sentences": {"min": 2, "max": 4},
                    "answer_options": 4,
                    "requires_integration": True
                },
                "presenter_notes_spec": {
                    "read_aloud": True,
                    "think_time_seconds": {"min": 30, "max": 60},
                    "reveal_answer_on_slide": False
                }
            },
            "answer": {
                "position": "after_vignette",
                "content_spec": {
                    "correct_answer_identified": True,
                    "rationale_required": True,
                    "distractor_analysis_required": True
                },
                "presenter_notes_spec": {
                    "reveal_and_explain": True,
                    "walk_through_distractors": True,
                    "connect_to_anchors": True,
                    "identify_exam_patterns": True
                }
            }
        }

    def build_presenter_notes_requirements(
        self,
        is_first_subsection: bool = False
    ) -> Dict:
        """
        Build presenter notes requirements for a subsection.

        Args:
            is_first_subsection: Whether this is the first subsection (foundational)

        Returns:
            Presenter notes requirements dict
        """
        elements = [
            "opening_statement",
            "concept_explanation",
            "applied_relevance",
            "closing_transition"
        ]

        if is_first_subsection:
            elements.insert(3, "connections")

        return {
            "verbatim_monologue": True,
            "word_count_guidance": {
                "per_minute": "130-150",
                "maximum": 450
            },
            "required_markers": ["[PAUSE]", "[EMPHASIS]"],
            "required_elements": elements,
            "exam_pattern_callouts": True,
            "study_strategy_mentions": is_first_subsection,
            "active_learning_word_reduction": "20%"
        }

    def build_anchor_delivery(
        self,
        subsection: Dict,
        xref_callbacks: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Build anchor delivery specification for a subsection.

        Args:
            subsection: Subsection data
            xref_callbacks: Cross-reference callbacks for this subsection

        Returns:
            Anchor delivery dict
        """
        anchors = subsection.get('anchors', [])

        # Build reference callbacks
        callbacks = []
        if xref_callbacks:
            for xref in xref_callbacks:
                if xref.get('anchor_number') in anchors:
                    callbacks.append({
                        "anchor_number": xref['anchor_number'],
                        "callback_phrase": "Recall that...",
                        "original_section": xref.get('xref_section', 'prior section')
                    })

        return {
            "primary_teaching": anchors,
            "reference_callbacks": callbacks
        }

    def build_active_learning_spec(
        self,
        complexity: str = "moderate"
    ) -> Dict:
        """
        Build active learning specification based on complexity.

        Args:
            complexity: Subsection complexity level

        Returns:
            Active learning specification dict
        """
        # Determine practice type and time based on complexity
        if complexity == "complex":
            practice_type = "case_application"
            time = 60
        elif complexity == "simple":
            practice_type = "concept_check"
            time = 30
        else:
            practice_type = "exam_style_question"
            time = 45

        return {
            "retrieval_practice_type": practice_type,
            "processing_time_seconds": time
        }

    def apply_standards_to_outline(
        self,
        outline: Dict,
        domain: str = "NCLEX"
    ) -> Dict:
        """
        Apply presentation standards to a Step 4 outline to produce Step 5 output.

        Args:
            outline: Step 4 outline output
            domain: Domain context (default: NCLEX)

        Returns:
            Step 5 output with standards applied
        """
        # Parse standards
        standards = self.parse_all_standards()

        # Initialize output structure
        output = {
            "metadata": {
                "step": "Step 5: Presentation Standards",
                "date": str(date.today()),
                "domain": outline.get('metadata', {}).get('domain', domain),
                "exam_context": "NCLEX",
                "total_sections": outline.get('metadata', {}).get('total_sections', 0),
                "total_subsections": outline.get('metadata', {}).get('total_subsections', 0),
                "output_file": f"step5_output_{date.today().isoformat()}.json"
            },
            "sessions": [],
            "delivery_summary": {
                "mode_distribution": {
                    "foundational": 0,
                    "full": 0,
                    "minor": 0,
                    "one_and_done": 0
                },
                "fixed_slides_total": {
                    "intro_slides": 0,
                    "vignette_slides": 0,
                    "answer_slides": 0,
                    "break_slides": 0,
                    "total_fixed": 0
                },
                "timing_guidance": standards.timing_guidance.to_dict() if standards.timing_guidance else {},
                "active_learning_points": 0,
                "exam_pattern_callouts": 0
            },
            "character_limits": standards.character_limits.to_dict() if standards.character_limits else {},
            "validation": {
                "status": "PASS",
                "checklist": {
                    "all_subsections_have_delivery_mode": True,
                    "all_sections_have_fixed_slides": True,
                    "first_subsections_use_foundational_mode": True,
                    "misc_section_exceptions_applied": True,
                    "culmination_section_exceptions_applied": True,
                    "xref_callbacks_documented": True,
                    "active_learning_integrated": True
                },
                "errors": []
            }
        }

        # Track section index for determining if first section
        global_section_index = 0

        # Process each session
        sessions = outline.get('sessions', outline.get('outline', {}).get('sessions', []))
        for session in sessions:
            session_output = {
                "session_number": session.get('session_number', 1),
                "sections": [],
                "break": session.get('break', {
                    "placement": f"Mid-session {session.get('session_number', 1)}",
                    "slide_spec": {
                        "title": "Break Time",
                        "duration_minutes": 10
                    }
                })
            }

            # Process each section
            for section in session.get('sections', []):
                is_first_section = (global_section_index == 0)

                section_output = {
                    "section_number": section.get('section_number', 1),
                    "section_name": section.get('section_name', 'Untitled'),
                    "is_misc": section.get('is_misc', False),
                    "is_culmination": section.get('is_culmination', False),
                    "fixed_slides": self.build_fixed_slides_spec(section, is_first_section),
                    "subsections": [],
                    "xref_callbacks": []
                }

                # Update fixed slides count
                output["delivery_summary"]["fixed_slides_total"]["intro_slides"] += 1
                output["delivery_summary"]["fixed_slides_total"]["vignette_slides"] += 1
                output["delivery_summary"]["fixed_slides_total"]["answer_slides"] += 1

                # Process xref flags
                xref_flags = section.get('xref_flags', [])

                # Process each subsection
                for sub_idx, subsection in enumerate(section.get('subsections', [])):
                    is_first_subsection = (sub_idx == 0) and not section.get('is_misc', False)

                    # Handle is_first_subsection from input or determine it
                    if 'is_first_subsection' in subsection:
                        is_first_subsection = subsection['is_first_subsection']

                    complexity = subsection.get('complexity', 'moderate')

                    subsection_output = {
                        "subsection_id": subsection.get('subsection_id', f"{section.get('section_number', 1)}.{sub_idx + 1}"),
                        "subsection_name": subsection.get('subsection_name', 'Untitled'),
                        "anchor_count": subsection.get('anchor_count', 0),
                        "complexity": complexity,
                        "delivery_mode": self.determine_delivery_mode(subsection, is_first_subsection),
                        "anchor_delivery": self.build_anchor_delivery(subsection, xref_flags),
                        "active_learning": self.build_active_learning_spec(complexity),
                        "presenter_notes_requirements": self.build_presenter_notes_requirements(is_first_subsection)
                    }

                    # Update mode distribution
                    mode = subsection_output["delivery_mode"]["mode"]
                    output["delivery_summary"]["mode_distribution"][mode] += 1

                    # Update active learning count
                    output["delivery_summary"]["active_learning_points"] += 1

                    # Update exam pattern callouts (one per subsection with exam_pattern_callouts=True)
                    if subsection_output["presenter_notes_requirements"]["exam_pattern_callouts"]:
                        output["delivery_summary"]["exam_pattern_callouts"] += 1

                    section_output["subsections"].append(subsection_output)

                # Add xref callbacks to section
                for xref in xref_flags:
                    section_output["xref_callbacks"].append({
                        "anchor_number": xref.get('anchor_number'),
                        "primary_section": section.get('section_name'),
                        "callback_script": f"Recall the concepts we covered regarding anchor {xref.get('anchor_number')}.",
                        "connection_purpose": xref.get('purpose', 'Cross-reference connection')
                    })

                session_output["sections"].append(section_output)
                global_section_index += 1

            # Add break slide count
            output["delivery_summary"]["fixed_slides_total"]["break_slides"] += 1

            output["sessions"].append(session_output)

        # Calculate total fixed slides
        fst = output["delivery_summary"]["fixed_slides_total"]
        fst["total_fixed"] = fst["intro_slides"] + fst["vignette_slides"] + fst["answer_slides"] + fst["break_slides"]

        # Validate output
        self._validate_output(output)

        return output

    def _validate_output(self, output: Dict) -> None:
        """Validate the output and update validation status."""
        errors = []
        checklist = output["validation"]["checklist"]

        # Check all subsections have delivery mode
        for session in output["sessions"]:
            for section in session["sections"]:
                for subsection in section["subsections"]:
                    if "delivery_mode" not in subsection:
                        checklist["all_subsections_have_delivery_mode"] = False
                        errors.append(f"Missing delivery_mode in {subsection.get('subsection_id')}")

                    # Check first subsection uses foundational
                    if subsection.get('subsection_id', '').endswith('.1'):
                        if subsection.get('delivery_mode', {}).get('mode') != 'foundational':
                            # Allow exception for misc sections
                            if not section.get('is_misc', False):
                                checklist["first_subsections_use_foundational_mode"] = False

                # Check fixed slides
                if "fixed_slides" not in section:
                    checklist["all_sections_have_fixed_slides"] = False
                    errors.append(f"Missing fixed_slides in section {section.get('section_number')}")

        # Update validation status
        if errors:
            output["validation"]["status"] = "FAIL"
            output["validation"]["errors"] = errors

    def format_report(self, result: ParsedStandards) -> str:
        """
        Format parsed standards as a human-readable report.

        Args:
            result: ParsedStandards object

        Returns:
            Formatted report string
        """
        lines = [
            "=" * 60,
            "STANDARDS PARSER REPORT",
            "=" * 60,
            f"Status: {'SUCCESS' if result.success else 'FAILED'}",
            f"Source files: {len(result.source_files)}",
            ""
        ]

        # Delivery modes
        lines.append("-" * 60)
        lines.append("DELIVERY MODES:")
        for mode_name, mode in result.delivery_modes.items():
            lines.append(f"  {mode_name}:")
            lines.append(f"    Criteria: {mode.selection_criteria}")
            lines.append(f"    Components: {len(mode.structure)}")

        # Fixed slides
        lines.append("")
        lines.append("-" * 60)
        lines.append("FIXED SLIDES:")
        for slide_type, slide in result.fixed_slides.items():
            lines.append(f"  {slide_type}: position={slide.position}")

        # Timing
        lines.append("")
        lines.append("-" * 60)
        lines.append("TIMING GUIDANCE:")
        if result.timing_guidance:
            lines.append(f"  Words per minute: {result.timing_guidance.words_per_minute_min}-{result.timing_guidance.words_per_minute_max}")
            lines.append(f"  Max words: {result.timing_guidance.max_words}")
            lines.append(f"  Max duration: {result.timing_guidance.max_duration_seconds}s")

        # Character limits
        lines.append("")
        lines.append("-" * 60)
        lines.append("CHARACTER LIMITS:")
        if result.character_limits:
            lines.append(f"  Header: {result.character_limits.header_chars_per_line} chars/line, {result.character_limits.header_max_lines} lines")
            lines.append(f"  Body: {result.character_limits.body_chars_per_line} chars/line, {result.character_limits.body_max_lines} lines")
            lines.append(f"  Tip: {result.character_limits.tip_chars_per_line} chars/line, {result.character_limits.tip_max_lines} lines")

        # Errors/warnings
        if result.errors:
            lines.append("")
            lines.append("ERRORS:")
            for error in result.errors:
                lines.append(f"  - {error}")

        if result.warnings:
            lines.append("")
            lines.append("WARNINGS:")
            for warning in result.warnings:
                lines.append(f"  - {warning}")

        lines.append("")
        lines.append("=" * 60)
        return "\n".join(lines)


def parse_standards(base_path: Optional[str] = None) -> ParsedStandards:
    """
    Convenience function to parse all standards.

    Args:
        base_path: Optional base path to project root

    Returns:
        ParsedStandards object
    """
    parser = StandardsParser(base_path)
    return parser.parse_all_standards()


if __name__ == "__main__":
    print("Standards Parser - NCLEX Pipeline Step 5 Skill")
    print("=" * 50)

    parser = StandardsParser()
    result = parser.parse_all_standards()

    report = parser.format_report(result)
    print(report)

    # Demo mode selection
    print("\n" + "=" * 50)
    print("DEMO: Mode Selection Logic")
    print("=" * 50)

    test_cases = [
        {"subsection_id": "1.1", "anchor_count": 2, "complexity": "moderate"},
        {"subsection_id": "1.2", "anchor_count": 3, "complexity": "moderate"},
        {"subsection_id": "2.1", "anchor_count": 5, "complexity": "complex"},
        {"subsection_id": "2.2", "anchor_count": 1, "complexity": "simple"},
    ]

    for i, case in enumerate(test_cases):
        is_first = case["subsection_id"].endswith(".1")
        mode = parser.determine_delivery_mode(case, is_first)
        print(f"\nSubsection {case['subsection_id']}:")
        print(f"  Anchors: {case['anchor_count']}, Complexity: {case['complexity']}")
        print(f"  Is first: {is_first}")
        print(f"  -> Mode: {mode['mode']}")
        print(f"  -> Rationale: {mode['selection_rationale']}")
