"""
Assembly Agents (Phase 4)
=========================

Agents for assembling final lesson packages and outputs.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from .base import Agent


@dataclass
class AssemblyLessonData:
    """Unified lesson data structure for assembly agents."""
    unit_number: int = 1
    unit_name: str = ""
    day: int = 1
    topic: str = ""
    learning_objectives: List[str] = field(default_factory=list)
    vocabulary: List[Dict] = field(default_factory=list)
    content_points: List[str] = field(default_factory=list)
    warmup: Dict = field(default_factory=dict)
    activity: Dict = field(default_factory=dict)
    journal_prompt: str = ""
    exit_tickets: List[str] = field(default_factory=list)
    materials_list: List[str] = field(default_factory=list)


def extract_assembly_data(context: Dict[str, Any]) -> Optional[AssemblyLessonData]:
    """Extract lesson data from either lesson_context or orchestrator format."""
    # Try lesson_context first
    lesson_ctx = context.get('lesson_context')
    if lesson_ctx:
        return AssemblyLessonData(
            unit_number=getattr(lesson_ctx, 'unit_number', 1),
            unit_name=getattr(lesson_ctx, 'unit_name', ''),
            day=getattr(lesson_ctx, 'day', 1),
            topic=getattr(lesson_ctx, 'topic', ''),
            learning_objectives=getattr(lesson_ctx, 'learning_objectives', []),
            vocabulary=getattr(lesson_ctx, 'vocabulary', []),
            content_points=getattr(lesson_ctx, 'content_points', []),
            warmup=getattr(lesson_ctx, 'warmup', {}),
            activity=getattr(lesson_ctx, 'activity', {}),
            journal_prompt=getattr(lesson_ctx, 'journal_prompt', ''),
            exit_tickets=getattr(lesson_ctx, 'exit_tickets', []),
            materials_list=getattr(lesson_ctx, 'materials_list', [])
        )

    # Try orchestrator format
    daily_input = context.get('daily_input', {})
    unit_info = context.get('unit', {})
    previous = context.get('previous_outputs', {})

    if daily_input or context.get('topic'):
        return AssemblyLessonData(
            unit_number=unit_info.get('number', context.get('unit_number', 1)),
            unit_name=unit_info.get('name', context.get('unit_name', '')),
            day=context.get('day', 1),
            topic=context.get('topic', daily_input.get('topic', '')),
            learning_objectives=daily_input.get('learning_objectives', []),
            vocabulary=daily_input.get('vocabulary', []),
            content_points=daily_input.get('content_points', []),
            warmup=previous.get('warmup_generator', {}).get('warmup', daily_input.get('warmup', {})),
            activity=previous.get('activity_generator', {}).get('activity', daily_input.get('activity', {})),
            journal_prompt=daily_input.get('journal_prompt', ''),
            exit_tickets=daily_input.get('exit_tickets', []),
            materials_list=daily_input.get('materials_list', [])
        )

    return None


class LessonAssemblerAgent(Agent):
    """
    Combines all daily lesson components into a complete lesson package.

    Merges: lesson plan, warmup, PowerPoint blueprint, presenter notes,
    activity, handouts, journal prompts, and exit tickets.
    """

    REQUIRED_COMPONENTS = [
        "lesson_plan",
        "warmup",
        "presenter_notes",
        "activity",
        "journal",
        "exit_tickets"
    ]

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_assembly_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Collect all components
        components = self._collect_components(context, lesson_data)

        # Validate all present - be more lenient for orchestrator mode
        missing = [c for c in self.REQUIRED_COMPONENTS if c not in components or not components[c]]

        # If many missing, still proceed with what we have
        if len(missing) > 3:
            return {
                "status": "INCOMPLETE",
                "missing_components": missing,
                "error": f"Cannot assemble: missing {', '.join(missing)}"
            }

        # Generate package ID
        package_id = self._generate_package_id(lesson_data)

        # Create file manifest
        manifest = self._create_file_manifest(lesson_data, package_id)

        # Generate quick reference
        quick_ref = self._generate_quick_reference(lesson_data, components)

        # Compile validation summary
        validation = self._compile_validation(context)

        return {
            "status": "ASSEMBLED",
            "lesson_package": {
                "metadata": {
                    "package_id": package_id,
                    "unit": f"Unit {lesson_data.unit_number}: {lesson_data.unit_name}",
                    "day": lesson_data.day,
                    "topic": lesson_data.topic,
                    "generated": datetime.now().isoformat(),
                    "version": "1.0"
                },
                "components": components,
                "deliverables": manifest,
                "quick_reference": quick_ref,
                "validation_summary": validation
            }
        }

    def _collect_components(self, context: Dict, lesson_data: AssemblyLessonData) -> Dict:
        """Collect all lesson components from context."""
        components = {}
        previous = context.get('previous_outputs', {})

        # Lesson plan - try multiple sources
        lp_output = context.get('lesson_plan_generator_output', previous.get('lesson_plan_generator', {}))
        components['lesson_plan'] = lp_output.get('lesson_plan', {"topic": lesson_data.topic})

        # Warmup
        warmup_output = context.get('warmup_generator_output', previous.get('warmup_generator', {}))
        components['warmup'] = warmup_output.get('warmup', lesson_data.warmup or {"warmup_name": "Theater warmup"})

        # Presenter notes
        notes_output = context.get('presenter_notes_writer_output', previous.get('presenter_notes_writer', {}))
        components['presenter_notes'] = {
            'content': notes_output.get('presenter_notes', 'Presenter notes to be generated.'),
            'word_count': notes_output.get('word_count', 0),
            'duration_minutes': notes_output.get('estimated_duration_minutes', 0)
        }

        # Activity
        activity_output = context.get('activity_generator_output', previous.get('activity_generator', {}))
        components['activity'] = activity_output.get('activity', lesson_data.activity or {"name": "Group Activity"})

        # Journal and exit tickets
        journal_output = context.get('journal_exit_generator_output', previous.get('journal_exit_generator', {}))
        components['journal'] = journal_output.get('journal', {'prompt': lesson_data.journal_prompt or f"Reflect on {lesson_data.topic}."})
        components['exit_tickets'] = journal_output.get('exit_tickets', {'questions': lesson_data.exit_tickets or [f"What did you learn about {lesson_data.topic}?"]})

        # Handouts
        handout_output = context.get('handout_generator_output', previous.get('handout_generator', {}))
        components['handouts'] = handout_output.get('handouts', [])

        return components

    def _generate_package_id(self, lesson_data: AssemblyLessonData) -> str:
        """Generate unique package ID."""
        # Format: U{unit}D{day}_{TopicAbbrev}
        topic = lesson_data.topic or "Lesson"
        topic_abbrev = ''.join(word[:4].title() for word in topic.split()[:2])
        return f"U{lesson_data.unit_number}D{lesson_data.day:02d}_{topic_abbrev}"

    def _create_file_manifest(self, lesson_data: AssemblyLessonData, package_id: str) -> Dict:
        """Create file manifest for deliverables."""
        return {
            "lesson_plan": {
                "filename": f"{package_id}_LessonPlan.md",
                "format": "markdown",
                "pages": 2
            },
            "powerpoint": {
                "filename": f"{package_id}_Presentation.pptx",
                "slides": 16,
                "includes_notes": True
            },
            "handouts": [
                {"filename": f"{package_id}_Vocab.pdf", "copies_needed": "1 per student"},
                {"filename": f"{package_id}_Activity.pdf", "copies_needed": "1 per group"}
            ],
            "exit_ticket": {
                "filename": f"{package_id}_ExitTicket.pdf",
                "copies_needed": "1 per student"
            }
        }

    def _generate_quick_reference(self, lesson_data: AssemblyLessonData, components: Dict) -> Dict:
        """Generate one-page quick reference for teacher."""
        return {
            "timing_summary": {
                "agenda": "5 min",
                "warmup": "5 min",
                "lecture": "15 min",
                "activity": "15 min",
                "reflection": "10 min",
                "buffer": "6 min",
                "total": "56 min"
            },
            "materials_checklist": lesson_data.materials_list or [
                "Computer with presentation",
                "Projector/screen",
                "Handouts (class set)",
                "Exit tickets (class set)",
                "Student journals"
            ],
            "vocabulary": [v.get('term', '') for v in lesson_data.vocabulary[:5]] if lesson_data.vocabulary else [],
            "learning_objectives": lesson_data.learning_objectives[:3] if lesson_data.learning_objectives else [],
            "warmup_name": components.get('warmup', {}).get('warmup_name', ''),
            "activity_name": components.get('activity', {}).get('name', '')
        }

    def _compile_validation(self, context: Dict) -> Dict:
        """Compile validation results from all gates."""
        gates = ['truncation', 'structure', 'elaboration', 'timing']
        scores = {}
        all_passed = True

        for gate in gates:
            validator_key = f"{gate}_validator_output"
            result = context.get(validator_key, {})
            scores[gate] = result.get('score', result.get('total_score', 0))
            if result.get('validation_status') == 'FAIL':
                all_passed = False

        return {
            "all_gates_passed": all_passed,
            "scores": scores,
            "average_quality": sum(scores.values()) / len(scores) if scores else 0,
            "ready_for_production": all_passed
        }


class PowerPointAssemblerAgent(Agent):
    """
    Assembles PowerPoint presentation from blueprint and content.

    Integrates: slide content, presenter notes, visual elements,
    and applies template formatting.
    """

    # Standard slide structure for 56-minute lesson
    SLIDE_STRUCTURE = [
        {"type": "title", "name": "Title/Agenda"},
        {"type": "warmup", "name": "Warmup"},
        {"type": "content", "name": "Content Slide", "count": 12},
        {"type": "activity", "name": "Activity"},
        {"type": "journal", "name": "Journal/Exit"}
    ]

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_assembly_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Build slide blueprint
        slides = self._build_slides(context, lesson_data)

        # Attach presenter notes
        slides = self._attach_notes(slides, context)

        return {
            "status": "ASSEMBLED",
            "powerpoint_blueprint": {
                "slides": slides,
                "total_slides": len(slides),
                "template": "template_theater.pptx",
                "includes_notes": True,
                "estimated_duration_minutes": 15
            }
        }

    def _build_slides(self, context: Dict, lesson_data: AssemblyLessonData) -> List[Dict]:
        """Build slide list from lesson content."""
        slides = []
        previous = context.get('previous_outputs', {})

        # Slide 1: Title/Agenda
        objectives = lesson_data.learning_objectives or ["Understand key concepts"]
        slides.append({
            "slide_number": 1,
            "type": "title",
            "title": lesson_data.topic or "Lesson Topic",
            "subtitle": f"Unit {lesson_data.unit_number} | Day {lesson_data.day}",
            "body": [
                "Today's Objectives:",
                *[f"• {obj}" for obj in objectives[:3]]
            ]
        })

        # Slide 2: Warmup
        warmup_output = context.get('warmup_generator_output', previous.get('warmup_generator', {}))
        warmup = warmup_output.get('warmup', lesson_data.warmup or {})
        slides.append({
            "slide_number": 2,
            "type": "warmup",
            "title": warmup.get('warmup_name', 'Warmup'),
            "body": [
                f"Duration: 5 minutes",
                f"Focus: {warmup.get('connection_to_lesson', {}).get('skill_practiced', 'Performance skills')}"
            ],
            "tip": warmup.get('connection_to_lesson', {}).get('statement', '')[:132]
        })

        # Slides 3-14: Content
        content_points = lesson_data.content_points or []
        for i, point in enumerate(content_points[:12]):
            slides.append({
                "slide_number": i + 3,
                "type": "content",
                "title": point[:36] if len(point) > 36 else point,
                "body": self._format_content_body(point, lesson_data),
                "tip": self._generate_tip(i)
            })

        # Fill remaining content slides if needed
        while len(slides) < 14:
            slides.append({
                "slide_number": len(slides) + 1,
                "type": "content",
                "title": f"Key Point {len(slides) - 1}",
                "body": ["Content to be determined"],
                "tip": ""
            })

        # Slide 15: Activity
        activity_output = context.get('activity_generator_output', previous.get('activity_generator', {}))
        activity = activity_output.get('activity', lesson_data.activity or {})
        slides.append({
            "slide_number": 15,
            "type": "activity",
            "title": activity.get('name', 'Activity'),
            "body": [
                f"Duration: {activity.get('duration', 15)} minutes",
                f"Format: {activity.get('format', 'Group work')}",
                f"Grouping: {activity.get('grouping', 'Groups of 3-4')}"
            ],
            "tip": f"Remember to circulate and provide feedback"
        })

        # Slide 16: Journal/Exit
        journal_output = context.get('journal_exit_generator_output', previous.get('journal_exit_generator', {}))
        journal = journal_output.get('journal', {})
        exit_tickets = journal_output.get('exit_tickets', {})

        slides.append({
            "slide_number": 16,
            "type": "journal",
            "title": "Reflection & Exit",
            "body": [
                "Journal Prompt:",
                journal.get('prompt', lesson_data.journal_prompt or f"Reflect on {lesson_data.topic}.")[:150],
                "",
                "Exit Ticket:",
                *[q[:80] for q in (exit_tickets.get('questions', lesson_data.exit_tickets) or [])[:2]]
            ],
            "tip": "Collect exit tickets as students leave"
        })

        return slides

    def _format_content_body(self, point: str, lesson_data: AssemblyLessonData) -> List[str]:
        """Format content point into slide body lines."""
        # Split long content into bullet points
        body = []

        # Main point
        body.append(f"• {point[:66]}")

        # Add relevant vocabulary if available
        vocab = lesson_data.vocabulary
        if vocab:
            relevant_vocab = [v for v in vocab if v.get('term', '').lower() in point.lower()]
            if relevant_vocab:
                body.append(f"Key term: {relevant_vocab[0].get('term', '')}")

        return body[:8]  # Max 8 lines

    def _generate_tip(self, index: int) -> str:
        """Generate performance tip for slide."""
        tips = [
            "Check for understanding before moving on",
            "Connect this to prior learning",
            "Allow time for student questions",
            "Use visual examples when possible",
            "Encourage student discussion"
        ]
        return tips[index % len(tips)]

    def _attach_notes(self, slides: List[Dict], context: Dict) -> List[Dict]:
        """Attach presenter notes to slides."""
        previous = context.get('previous_outputs', {})
        notes_output = context.get('presenter_notes_writer_output', previous.get('presenter_notes_writer', {}))
        full_notes = notes_output.get('presenter_notes', '')

        # Split notes by slide markers
        note_sections = full_notes.split('[SLIDE')

        for i, slide in enumerate(slides):
            # Try to find matching note section
            if i < len(note_sections) - 1:
                slide['presenter_notes'] = note_sections[i + 1][:500]  # First 500 chars
            else:
                slide['presenter_notes'] = f"Present content for: {slide.get('title', 'Slide')}"

        return slides


class UnitFolderOrganizerAgent(Agent):
    """
    Organizes output files into proper folder structure.

    Creates:
    - Unit folders
    - Day subfolders
    - Moves files to appropriate locations
    """

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_assembly_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Generate folder structure
        unit_name = lesson_data.unit_name.replace(' ', '_') if lesson_data.unit_name else "Unit"
        unit_folder = f"Unit_{lesson_data.unit_number}_{unit_name}"
        day_folder = f"Day_{lesson_data.day:02d}"

        structure = {
            "root": "production",
            "unit_folder": unit_folder,
            "day_folder": day_folder,
            "full_path": f"production/{unit_folder}/{day_folder}",
            "files": [
                f"lesson_plan.md",
                f"presentation.pptx",
                f"vocab_handout.pdf",
                f"activity_handout.pdf",
                f"exit_ticket.pdf"
            ]
        }

        return {
            "status": "ORGANIZED",
            "folder_structure": structure,
            "output_directory": structure["full_path"]
        }
