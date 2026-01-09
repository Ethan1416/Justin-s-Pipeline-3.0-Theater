"""
Daily Generation Agents (Phase 2)
=================================

Agents for generating daily lesson content.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
import random
from dataclasses import dataclass, field

from .base import Agent


@dataclass
class LessonData:
    """Unified lesson data structure for agents."""
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
    standards: List[str] = field(default_factory=list)


def extract_lesson_data(context: Dict[str, Any]) -> Optional[LessonData]:
    """
    Extract lesson data from either lesson_context or orchestrator format.

    Handles two input formats:
    1. lesson_context object (from pipeline runner)
    2. Orchestrator format: {unit: {}, day: N, topic: str, daily_input: {}}
    """
    def normalize_content_points(raw_points):
        """Normalize content_points to handle both string and dict formats."""
        normalized = []
        for cp in (raw_points or []):
            if isinstance(cp, dict):
                normalized.append(cp.get('point', ''))
            else:
                normalized.append(str(cp))
        return normalized

    # Try lesson_context first
    lesson_ctx = context.get('lesson_context')
    if lesson_ctx:
        return LessonData(
            unit_number=getattr(lesson_ctx, 'unit_number', 1),
            unit_name=getattr(lesson_ctx, 'unit_name', ''),
            day=getattr(lesson_ctx, 'day', 1),
            topic=getattr(lesson_ctx, 'topic', ''),
            learning_objectives=getattr(lesson_ctx, 'learning_objectives', []),
            vocabulary=getattr(lesson_ctx, 'vocabulary', []),
            content_points=normalize_content_points(getattr(lesson_ctx, 'content_points', [])),
            warmup=getattr(lesson_ctx, 'warmup', {}),
            activity=getattr(lesson_ctx, 'activity', {}),
            journal_prompt=getattr(lesson_ctx, 'journal_prompt', ''),
            exit_tickets=getattr(lesson_ctx, 'exit_tickets', []),
            materials_list=getattr(lesson_ctx, 'materials_list', []),
            standards=getattr(lesson_ctx, 'standards', [])
        )

    # Try orchestrator format
    daily_input = context.get('daily_input', {})
    unit_info = context.get('unit', {})

    if daily_input or context.get('topic'):
        return LessonData(
            unit_number=unit_info.get('number', context.get('unit_number', 1)),
            unit_name=unit_info.get('name', context.get('unit_name', '')),
            day=context.get('day', 1),
            topic=context.get('topic', daily_input.get('topic', '')),
            learning_objectives=daily_input.get('learning_objectives', []),
            vocabulary=daily_input.get('vocabulary', []),
            content_points=normalize_content_points(daily_input.get('content_points', [])),
            warmup=daily_input.get('warmup', {}),
            activity=daily_input.get('activity', {}),
            journal_prompt=daily_input.get('journal_prompt', ''),
            exit_tickets=daily_input.get('exit_tickets', []),
            materials_list=daily_input.get('materials_list', []),
            standards=daily_input.get('standards', [])
        )

    return None


# Warmup bank organized by unit and type
WARMUP_BANK = {
    1: {  # Greek Theater
        "physical": [
            {"name": "Chorus Formation Walk", "focus": "Moving as unified group",
             "instructions": "Walk in formation, maintaining equal spacing. On signal, change direction as one."},
            {"name": "Mask Neutral Face", "focus": "Expressing without facial movement",
             "instructions": "Hold neutral face while communicating emotion through body only."},
            {"name": "Amphitheater Projection", "focus": "Voice to back of room",
             "instructions": "Project voice to reach the 'last row' without straining."},
        ],
        "mental": [
            {"name": "Dithyramb Rhythm", "focus": "Group chanting patterns",
             "instructions": "Follow leader in rhythmic chanting, building intensity."},
        ],
        "content": [
            {"name": "Protagonist/Antagonist Quick Debate", "focus": "Identifying conflict",
             "instructions": "In pairs, take opposing sides of a theatrical conflict and defend positions."},
        ]
    },
    2: {  # Commedia dell'Arte
        "physical": [
            {"name": "Zanni Walk Variations", "focus": "Character physicality",
             "instructions": "Practice the low status zanni walk with exaggerated movements."},
            {"name": "Pantalone's Counting", "focus": "Old man movement",
             "instructions": "Move as Pantalone counting imaginary coins with bent posture."},
            {"name": "Lazzi Freeze", "focus": "Comic timing and physical comedy",
             "instructions": "Perform movement, freeze on signal in exaggerated pose."},
        ],
        "social": [
            {"name": "Status Lines", "focus": "Physical status communication",
             "instructions": "Arrange in line by status, communicate through posture only."},
        ],
        "content": [
            {"name": "Stock Character Guess", "focus": "Recognizing archetypes",
             "instructions": "One person embodies character, others guess the archetype."},
        ]
    },
    3: {  # Shakespeare
        "physical": [
            {"name": "Iambic Pentameter Walk", "focus": "Rhythm in movement",
             "instructions": "Walk to the rhythm of iambic pentameter, stepping on stressed syllables."},
        ],
        "mental": [
            {"name": "Antithesis Hand Gestures", "focus": "Contrasting concepts",
             "instructions": "Gesture with one hand for first concept, opposite hand for antithesis."},
        ],
        "social": [
            {"name": "Insult Tennis", "focus": "Shakespearean language play",
             "instructions": "Volley Shakespearean insults back and forth with partner."},
            {"name": "Soliloquy to Partner", "focus": "Direct address practice",
             "instructions": "Deliver lines directly to partner, maintaining eye contact."},
        ],
        "content": [
            {"name": "Modern Translation Race", "focus": "Language comprehension",
             "instructions": "Race to translate Shakespeare line into modern English."},
        ]
    },
    4: {  # Student-Directed One Acts
        "mental": [
            {"name": "Director's Eye", "focus": "Observation skills",
             "instructions": "Watch a scene and identify 3 blocking issues silently."},
        ],
        "social": [
            {"name": "Give and Take Focus", "focus": "Actor-director communication",
             "instructions": "Pass focus around circle, practice yielding and taking."},
            {"name": "Note Delivery Practice", "focus": "Constructive feedback",
             "instructions": "Practice giving and receiving director's notes positively."},
        ],
        "creative": [
            {"name": "Three Ways to Say It", "focus": "Directorial choices",
             "instructions": "Deliver same line three different ways, discuss directorial impact."},
        ],
        "content": [
            {"name": "Blocking Notation Quick Draw", "focus": "Technical vocabulary",
             "instructions": "Quick-draw blocking notation for given stage directions."},
        ]
    }
}

# Activity templates by type
ACTIVITY_TYPES = {
    "gallery_walk": {
        "setup_time": 2,
        "work_time": 10,
        "share_time": 3,
        "format": "Students rotate through stations examining materials and leaving feedback."
    },
    "jigsaw": {
        "setup_time": 2,
        "work_time": 8,
        "share_time": 5,
        "format": "Expert groups study then teach home groups."
    },
    "performance": {
        "setup_time": 2,
        "work_time": 8,
        "share_time": 5,
        "format": "Small groups prepare and present short performances."
    },
    "analysis": {
        "setup_time": 1,
        "work_time": 10,
        "share_time": 4,
        "format": "Partners or small groups analyze text/video with guiding questions."
    },
    "creation": {
        "setup_time": 2,
        "work_time": 10,
        "share_time": 3,
        "format": "Students create original work based on lesson content."
    }
}


class LessonPlanGeneratorAgent(Agent):
    """Agent for generating lesson plans."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        lesson_plan = {
            "metadata": {
                "unit": lesson_data.unit_name,
                "unit_number": lesson_data.unit_number,
                "day": lesson_data.day,
                "topic": lesson_data.topic,
                "duration": "56 minutes",
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            "standards": lesson_data.standards,
            "learning_objectives": lesson_data.learning_objectives,
            "vocabulary": lesson_data.vocabulary,
            "materials": lesson_data.materials_list or ["Presentation", "Handouts", "Exit tickets"],
            "procedure": {
                "opening": {
                    "duration": "5 minutes",
                    "activities": ["Display agenda", "Review objectives", "Journal prompt"],
                    "journal_prompt": lesson_data.journal_prompt or f"What do you know about {lesson_data.topic}?"
                },
                "warmup": {
                    "duration": "5 minutes",
                    "activity": lesson_data.warmup or {"name": "Theater warmup", "focus": "Engagement"}
                },
                "direct_instruction": {
                    "duration": "15 minutes",
                    "content_points": lesson_data.content_points,
                    "slide_count": 12
                },
                "guided_practice": {
                    "duration": "15 minutes",
                    "activity": lesson_data.activity or {"name": "Group activity", "format": "Small groups"}
                },
                "closure": {
                    "duration": "10 minutes",
                    "activities": ["Journal reflection", "Exit ticket"],
                    "journal_prompt": lesson_data.journal_prompt or f"Reflect on {lesson_data.topic}.",
                    "exit_tickets": lesson_data.exit_tickets or [f"What did you learn about {lesson_data.topic}?"]
                },
                "buffer": {
                    "duration": "6 minutes",
                    "purpose": "Transition, cleanup, dismissal"
                }
            },
            "differentiation": {
                "ell": "Sentence frames, visual supports, strategic pairing",
                "advanced": "Extension questions, peer tutoring role",
                "struggling": "Graphic organizer, word bank, chunked instructions"
            }
        }

        return {"lesson_plan": lesson_plan}


class WarmupGeneratorAgent(Agent):
    """Generates structured, content-connected theater warmups."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Get warmup from context or generate one
        if lesson_data.warmup and lesson_data.warmup.get('name'):
            warmup = self._enhance_warmup(lesson_data.warmup, lesson_data)
        else:
            warmup = self._generate_warmup(lesson_data)

        return {"warmup": warmup}

    def _generate_warmup(self, lesson_data: LessonData) -> Dict:
        """Generate a warmup from the warmup bank."""
        unit_warmups = WARMUP_BANK.get(lesson_data.unit_number, WARMUP_BANK[1])

        # Select warmup type based on day position
        day = lesson_data.day
        if day <= 3:
            warmup_type = "physical"  # Early days: physical engagement
        elif day % 3 == 0:
            warmup_type = "content"  # Every 3rd day: content connection
        else:
            warmup_type = random.choice(["physical", "mental", "social"])

        available = unit_warmups.get(warmup_type, unit_warmups.get("physical", []))
        if not available:
            available = list(unit_warmups.values())[0]

        base_warmup = random.choice(available)

        return self._enhance_warmup(base_warmup, lesson_data)

    def _enhance_warmup(self, warmup: Dict, lesson_data: LessonData) -> Dict:
        """Enhance warmup with structured instructions and lesson connection."""
        warmup_name = warmup.get('name', 'Theater Warmup')
        topic = lesson_data.topic
        vocab_terms = [v.get('term', '') for v in lesson_data.vocabulary[:2]] if lesson_data.vocabulary else []

        return {
            "warmup_name": warmup_name,
            "type": warmup.get('type', 'physical'),
            "connection_to_lesson": {
                "statement": f"This warmup connects to today's lesson on {topic} by preparing students for the key skills and concepts we'll explore.",
                "vocabulary_referenced": vocab_terms,
                "skill_practiced": warmup.get('focus', 'performance skills'),
                "concept_previewed": topic
            },
            "structured_instructions": {
                "setup": {
                    "teacher_says": f"Everyone stand up and find your own space in the room. Today's warmup is called '{warmup_name}' and it connects directly to our lesson on {topic}.",
                    "student_positioning": "Standing, spread throughout room",
                    "duration_seconds": 30
                },
                "demonstration": {
                    "needed": True,
                    "teacher_models": warmup.get('instructions', 'Demonstrate the activity clearly.'),
                    "duration_seconds": 30
                },
                "execution": {
                    "steps": [
                        "Round 1: Practice individually",
                        "Round 2: Practice with a partner",
                        "Round 3: Combine with vocabulary from today's lesson"
                    ],
                    "teacher_role": "Circulate, provide feedback, encourage participation",
                    "expected_student_behavior": "Full participation, appropriate volume, focus on skill development",
                    "duration_seconds": 180
                },
                "wrapup": {
                    "debrief_question": f"How did this warmup prepare you for thinking about {topic}?",
                    "connection_statement": f"The skills you just practiced will help you engage with today's content on {topic}.",
                    "duration_seconds": 30
                },
                "transition": {
                    "teacher_says": "Great work! Take a seat and let's dive into today's lesson.",
                    "student_action": "Return to desks, take out journals, face front",
                    "duration_seconds": 30
                }
            },
            "timing_breakdown": {
                "total_seconds": 300,
                "total_minutes": 5
            },
            "materials_needed": warmup.get('materials', []),
            "space_requirements": "standing_at_desks",
            "noise_level": "performance_volume"
        }


class ActivityGeneratorAgent(Agent):
    """Generates classroom activities with structured instructions."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        if lesson_data.activity and lesson_data.activity.get('name'):
            activity = self._enhance_activity(lesson_data.activity, lesson_data)
        else:
            activity = self._generate_activity(lesson_data)

        return {"activity": activity}

    def _generate_activity(self, lesson_data: LessonData) -> Dict:
        """Generate an appropriate activity based on lesson content."""
        topic = lesson_data.topic
        unit = lesson_data.unit_number

        # Select activity type based on unit and day
        if unit == 1:  # Greek Theater
            activity_type = "analysis" if lesson_data.day < 10 else "performance"
        elif unit == 2:  # Commedia
            activity_type = "performance" if lesson_data.day > 5 else "analysis"
        elif unit == 3:  # Shakespeare
            activity_type = "analysis" if lesson_data.day < 15 else "performance"
        else:  # One Acts
            activity_type = "creation" if lesson_data.day > 7 else "analysis"

        base = ACTIVITY_TYPES.get(activity_type, ACTIVITY_TYPES["analysis"])

        return self._enhance_activity({
            "name": f"{topic} {activity_type.title()} Activity",
            "type": activity_type,
            "format": base["format"]
        }, lesson_data)

    def _enhance_activity(self, activity: Dict, lesson_data: LessonData) -> Dict:
        """Enhance activity with detailed structure."""
        activity_type = activity.get('type', 'analysis')
        base = ACTIVITY_TYPES.get(activity_type, ACTIVITY_TYPES["analysis"])
        topic = lesson_data.topic

        return {
            "name": activity.get('name', f'{topic} Activity'),
            "type": activity_type,
            "duration": 15,
            "format": activity.get('format', base['format']),
            "connection_to_lesson": f"This activity reinforces today's learning on {topic}.",
            "instructions": [
                f"First, form groups of 3-4 students",
                f"Then, review the activity materials",
                f"Next, work collaboratively on the task",
                f"Finally, prepare to share with the class"
            ],
            "structure": {
                "setup": base['setup_time'],
                "work_time": base['work_time'],
                "share_out": base['share_time']
            },
            "structured_instructions": {
                "setup": {
                    "teacher_actions": [
                        "Organize students into groups of 3-4",
                        "Distribute materials",
                        "Explain activity expectations"
                    ],
                    "duration_minutes": base['setup_time']
                },
                "work_time": {
                    "student_tasks": [
                        f"Engage with content related to {topic}",
                        "Collaborate with group members",
                        "Prepare to share findings/performance"
                    ],
                    "teacher_role": "Circulate, ask probing questions, provide support",
                    "duration_minutes": base['work_time']
                },
                "share_out": {
                    "format": "Groups share key insights or perform for class",
                    "teacher_facilitation": "Guide discussion, connect to learning objectives",
                    "duration_minutes": base['share_time']
                }
            },
            "materials_needed": activity.get('materials', [
                "Activity handout",
                "Writing materials",
                "Reference materials from lecture"
            ]),
            "grouping": activity.get('grouping', 'groups of 3-4'),
            "differentiation": {
                "struggling": "Provide sentence starters and graphic organizers",
                "advanced": "Add extension questions or leadership role",
                "ell": "Partner with strong English speaker, provide visual supports"
            },
            "time_warnings": [
                {"at_minutes": 5, "announcement": "5 minutes of work time remaining"},
                {"at_minutes": 2, "announcement": "2 minutes - start wrapping up"},
                {"at_minutes": 0, "announcement": "Time to share!"}
            ],
            "assessment": {
                "formative": "Observation of group work and participation",
                "evidence": "Completed activity product or performance"
            }
        }


class HandoutGeneratorAgent(Agent):
    """Generates handout content for lessons."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        handouts = []

        # Generate vocabulary handout if vocab exists
        if lesson_data.vocabulary:
            handouts.append(self._generate_vocab_handout(lesson_data))

        # Generate activity handout if activity exists
        if lesson_data.activity:
            handouts.append(self._generate_activity_handout(lesson_data))

        # Always generate at least a basic handout
        if not handouts:
            handouts.append({
                "name": f"{lesson_data.topic} Reference",
                "type": "reference",
                "content": {
                    "title": f"Unit {lesson_data.unit_number} Day {lesson_data.day}: {lesson_data.topic}",
                    "sections": ["Key concepts", "Notes section", "Reflection"]
                },
                "format": "full_page",
                "copies_needed": "1 per student"
            })

        return {"handouts": handouts}

    def _generate_vocab_handout(self, lesson_data: LessonData) -> Dict:
        """Generate vocabulary handout."""
        return {
            "name": f"{lesson_data.topic} Vocabulary",
            "type": "vocabulary",
            "content": {
                "title": f"Unit {lesson_data.unit_number} Day {lesson_data.day}: Key Vocabulary",
                "terms": [
                    {
                        "term": v.get('term', ''),
                        "definition": v.get('definition', ''),
                        "usage_example": v.get('usage_example', '')
                    }
                    for v in lesson_data.vocabulary
                ],
                "practice_section": "Use each term in a sentence related to theater."
            },
            "format": "half_page",
            "copies_needed": "1 per student"
        }

    def _generate_activity_handout(self, lesson_data: LessonData) -> Dict:
        """Generate activity handout."""
        activity = lesson_data.activity
        return {
            "name": f"{activity.get('name', 'Activity')} Handout",
            "type": "activity_guide",
            "content": {
                "title": activity.get('name', 'Activity'),
                "instructions": activity.get('instructions', 'Follow teacher directions.'),
                "guiding_questions": [
                    f"How does this connect to {lesson_data.topic}?",
                    "What patterns do you notice?",
                    "What questions do you have?"
                ],
                "reflection_space": True
            },
            "format": "full_page",
            "copies_needed": "1 per group or 1 per student"
        }


class JournalExitGeneratorAgent(Agent):
    """Generates journal prompts and exit tickets."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Generate or enhance journal prompt
        journal = self._generate_journal(lesson_data)

        # Generate or enhance exit tickets
        exit_tickets = self._generate_exit_tickets(lesson_data)

        return {
            "journal": journal,
            "exit_tickets": exit_tickets
        }

    def _generate_journal(self, lesson_data: LessonData) -> Dict:
        """Generate journal prompt with structure."""
        if lesson_data.journal_prompt:
            prompt_text = lesson_data.journal_prompt
        else:
            prompt_text = f"Reflect on today's learning about {lesson_data.topic}. What connections can you make to your own experience or previous theatrical knowledge?"

        return {
            "prompt": prompt_text,
            "duration_minutes": 5,
            "format": {
                "minimum_sentences": 3,
                "reflection_focus": "connection and application",
                "optional_sentence_starters": [
                    "Today I learned that...",
                    "This connects to... because...",
                    "I'm still wondering about..."
                ]
            },
            "teacher_instructions": "Give students quiet writing time. Circulate to check engagement."
        }

    def _generate_exit_tickets(self, lesson_data: LessonData) -> Dict:
        """Generate exit ticket questions."""
        if lesson_data.exit_tickets:
            questions = lesson_data.exit_tickets
        else:
            questions = [
                f"Name one key concept from today's lesson on {lesson_data.topic}.",
                f"How might you apply what you learned about {lesson_data.topic} in a performance?"
            ]

        return {
            "questions": questions,
            "duration_minutes": 3,
            "format": {
                "type": "half_page",
                "answer_format": "1-2 sentences each",
                "alignment": [obj for obj in lesson_data.learning_objectives[:2]] if lesson_data.learning_objectives else []
            },
            "assessment_purpose": "Check for understanding of key concepts",
            "teacher_instructions": "Collect as students leave. Use to inform next day's instruction."
        }


class PowerPointGeneratorAgent(Agent):
    """Generates PowerPoint slide blueprint for the lesson."""

    # Standard slide structure for 56-minute lesson
    SLIDE_STRUCTURE = [
        {"type": "title", "duration": 0},
        {"type": "warmup", "duration": 5},
        {"type": "content", "count": 12, "duration": 15},
        {"type": "activity", "duration": 15},
        {"type": "journal", "duration": 10}
    ]

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        daily_input = context.get('daily_input', {})

        # Build from context or daily_input
        topic = context.get('topic', daily_input.get('topic', 'Lesson Topic'))
        unit_number = context.get('unit', {}).get('number', 1)
        day = context.get('day', 1)
        learning_objectives = daily_input.get('learning_objectives', [])
        vocabulary = daily_input.get('vocabulary', [])

        # Normalize content_points - handle both string and dict formats
        raw_content_points = daily_input.get('content_points', [])
        content_points = []
        for cp in raw_content_points:
            if isinstance(cp, dict):
                content_points.append(cp.get('point', ''))
            else:
                content_points.append(str(cp))

        # Helper to ensure punctuation
        def ensure_punctuation(text):
            text = str(text).strip()
            if text and text[-1] not in '.!?:':
                return text + '.'
            return text

        slides = []

        # Slide 1: Title/Agenda
        slides.append({
            "slide_number": 1,
            "type": "title",
            "header": ensure_punctuation(topic[:36]),
            "body": [
                f"Unit {unit_number} | Day {day}.",
                "Today's Objectives:",
                *[f"- {obj[:60]}." if not obj.endswith('.') else f"- {obj[:60]}" for obj in learning_objectives[:3]]
            ]
        })

        # Slide 2: Warmup
        slides.append({
            "slide_number": 2,
            "type": "warmup",
            "header": "Warmup Activity.",
            "body": ["Duration: 5 minutes.", "Follow teacher instructions."]
        })

        # Slides 3-14: Content (12 slides)
        for i, point in enumerate(content_points[:12], 3):
            body_text = ensure_punctuation(point[:66])
            slides.append({
                "slide_number": i,
                "type": "content",
                "header": ensure_punctuation(point[:36] if len(point) > 36 else point),
                "body": [body_text]
            })

        # Pad to 12 content slides
        while len(slides) < 14:
            slides.append({
                "slide_number": len(slides) + 1,
                "type": "content",
                "header": f"Key Point {len(slides) - 1}.",
                "body": ["Content to be determined."]
            })

        # Slide 15: Activity
        slides.append({
            "slide_number": 15,
            "type": "activity",
            "header": "Activity.",
            "body": ["Duration: 15 minutes.", "Group work activity."]
        })

        # Slide 16: Journal/Exit
        slides.append({
            "slide_number": 16,
            "type": "journal",
            "header": "Reflection & Exit.",
            "body": ["Journal: 5 minutes.", "Exit Ticket: 3 minutes."]
        })

        return {
            "powerpoint_blueprint": {
                "slides": slides,
                "total_slides": len(slides),
                "template": "template_theater.pptx"
            }
        }


class PresenterNotesWriterAgent(Agent):
    """Writes presenter notes for lecture slides."""

    # Target words per minute for speaking
    SPEAKING_RATE_WPM = 140
    # Target lecture duration in minutes
    TARGET_DURATION = 15

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Calculate target word count
        target_words = self.SPEAKING_RATE_WPM * self.TARGET_DURATION  # ~2100 words

        # Generate notes
        notes = self._generate_notes(lesson_data, target_words)

        word_count = len(notes.split())
        estimated_duration = word_count / self.SPEAKING_RATE_WPM

        return {
            "presenter_notes": notes,
            "word_count": word_count,
            "estimated_duration_minutes": round(estimated_duration, 1),
            "target_duration_minutes": self.TARGET_DURATION,
            "markers": {
                "pause_count": notes.count("[PAUSE]"),
                "emphasis_count": notes.count("[EMPHASIS"),
                "check_understanding_count": notes.count("[CHECK")
            }
        }

    def _generate_notes(self, lesson_data: LessonData, target_words: int) -> str:
        """Generate comprehensive presenter notes with scoring indicators."""
        notes = []
        topic = lesson_data.topic or "today's topic"
        objectives = lesson_data.learning_objectives or ["understand key concepts", "apply learning"]
        vocab = lesson_data.vocabulary or []
        content_points = lesson_data.content_points or ["Key concept to explore"]

        # Title slide - includes depth indicators
        notes.append(f"[SLIDE 1: Title - {topic}]\n")
        notes.append(f"Welcome everyone! Today we're diving into an exciting topic: {topic}. ")
        notes.append(f"This means we'll explore fundamental concepts that connect to theatrical tradition. ")
        notes.append(f"[PAUSE] Take a moment to look at our learning objectives on the screen. ")
        notes.append("By the end of today's class, you'll be able to:\n")
        for i, obj in enumerate(objectives, 1):
            notes.append(f"[EMPHASIS: Objective {i}] {obj}. This means you'll have practical skills to apply in performance. ")
        notes.append(f"\n[PAUSE] Let's begin our journey into {topic} and discover how it connects to your growth as performers.\n\n")

        # Vocabulary slide - includes examples
        notes.append("[SLIDE 2: Key Vocabulary]\n")
        notes.append("Before we dive into the content, let's review some key terms. ")
        notes.append("Specifically, these terms will help you understand our main topic. [PAUSE]\n")
        for v in vocab[:4]:
            term = v.get('term', '')
            definition = v.get('definition', '')
            if term:
                notes.append(f"[EMPHASIS: {term}] - {definition}. ")
                notes.append(f"For instance, imagine a performer using this concept on stage. ")
                notes.append(f"This connects to our overall theme because it helps us understand theatrical tradition. [PAUSE]\n")
        notes.append("\n")

        # Content slides - enhanced with scoring indicators (generates ~160 words per content point)
        # Target: 12 content points x 160 words = ~1920 + ~180 for intro/transition = ~2100 total
        for i, point in enumerate(content_points, 1):
            slide_num = i + 2
            notes.append(f"[SLIDE {slide_num}: {point[:40]}...]\n")
            notes.append(f"First, let's explore {point}. [PAUSE]\n\n")

            # Depth indicators
            notes.append(f"The reason this matters is because it forms the foundation of our understanding. ")
            notes.append(f"In the context of theater education, this concept helps performers connect with their audiences. ")
            notes.append(f"Therefore, when we understand this principle, we can apply it practically in our work. ")
            notes.append(f"Historically, this idea emerged from ancient theatrical traditions. [PAUSE]\n\n")

            # Example indicators
            notes.append(f"For example, consider how professional actors use this technique in their craft. ")
            notes.append(f"Think about a famous performance you've seen - imagine how the actor applied these principles. ")
            notes.append(f"Such as when a performer enters the stage, they embody this concept immediately. ")
            notes.append(f"Like skilled craftspeople, actors internalize these fundamentals through practice. [PAUSE]\n\n")

            # Procedure indicators
            notes.append(f"Let me explain the step-by-step process. First, you observe the technique in action. ")
            notes.append(f"Then, you practice it yourself with guidance. Next, you refine your approach based on feedback. ")
            notes.append(f"Following this, you receive constructive criticism. Finally, you master the skill through repetition. [PAUSE]\n\n")

            notes.append(f"[CHECK FOR UNDERSTANDING] In other words, how does this connect to what we've learned previously? ")
            notes.append(f"Consequently, your performances will become more authentic and engaging. [PAUSE]\n\n")

        # Transition slide
        notes.append(f"[SLIDE {len(content_points) + 3}: Transition to Activity]\n")
        notes.append(f"Now that we've explored the key concepts of {topic}, it's time to put this knowledge into practice. ")
        notes.append(f"[PAUSE] Consequently, in our activity, you'll have the opportunity to apply what you've learned. ")
        notes.append(f"Begin by reviewing the instructions. Start with a warm-up exercise. ")
        notes.append(f"After that, move into the main activity. Remember to think about how these concepts connect. ")
        notes.append(f"[PAUSE] Let's move into our activity!\n")

        return "".join(notes)


class AuxiliarySlideGeneratorAgent(Agent):
    """
    Generates auxiliary (non-content) slides for the lesson.

    Creates 4 slides:
    - Slide 1: Agenda/Title
    - Slide 2: Warmup Instructions
    - Slide 15: Activity Instructions
    - Slide 16: Journal & Exit Ticket
    """

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Get previous outputs for warmup, activity, journal
        previous = context.get('previous_outputs', {})
        warmup_output = previous.get('warmup_generator', {})
        activity_output = previous.get('activity_generator', {})
        journal_output = previous.get('journal_exit_generator', {})

        # Generate the 4 auxiliary slides
        slides = []

        # Slide 1: Agenda
        slides.append(self._generate_agenda_slide(lesson_data))

        # Slide 2: Warmup
        slides.append(self._generate_warmup_slide(
            lesson_data,
            warmup_output.get('warmup', {})
        ))

        # Slide 15: Activity
        slides.append(self._generate_activity_slide(
            lesson_data,
            activity_output.get('activity', {})
        ))

        # Slide 16: Journal & Exit
        slides.append(self._generate_journal_slide(
            lesson_data,
            journal_output.get('journal', {}),
            journal_output.get('exit_tickets', {})
        ))

        return {
            "auxiliary_slides": slides,
            "slide_positions": {
                "agenda": 1,
                "warmup": 2,
                "activity": 15,
                "journal_exit": 16
            }
        }

    def _generate_agenda_slide(self, lesson_data: LessonData) -> Dict:
        """Generate agenda/title slide."""
        objectives = lesson_data.learning_objectives[:3]
        vocab_terms = [v.get('term', '') for v in lesson_data.vocabulary[:5]]

        return {
            "slide_number": 1,
            "type": "agenda",
            "header": lesson_data.topic[:36] + ".",
            "body": [
                f"Unit {lesson_data.unit_number} | Day {lesson_data.day}.",
                "",
                "Today's Schedule:",
                "• Journal-In & Agenda (5 min).",
                "• Warmup (5 min).",
                "• Lecture & Discussion (15 min).",
                "• Activity (15 min).",
                "• Reflection & Exit (10 min)."
            ],
            "sidebar": {
                "objectives": objectives,
                "vocabulary_preview": vocab_terms
            },
            "duration_on_screen": "5 minutes"
        }

    def _generate_warmup_slide(self, lesson_data: LessonData, warmup: Dict) -> Dict:
        """Generate warmup instructions slide."""
        warmup_name = warmup.get('warmup_name', 'Theater Warmup')
        connection = warmup.get('connection_to_lesson', {})

        return {
            "slide_number": 2,
            "type": "warmup",
            "header": f"Warmup: {warmup_name[:30]}.",
            "body": [
                "Duration: 5 minutes.",
                "",
                "Instructions:",
                "1. Stand and find your space.",
                "2. Follow teacher demonstration.",
                "3. Practice with a partner.",
                "4. Connect to today's lesson."
            ],
            "connection_statement": connection.get('statement', f"This warmup connects to {lesson_data.topic}."),
            "skill_focus": warmup.get('type', 'physical'),
            "duration_on_screen": "5 minutes"
        }

    def _generate_activity_slide(self, lesson_data: LessonData, activity: Dict) -> Dict:
        """Generate activity instructions slide."""
        activity_name = activity.get('name', f'{lesson_data.topic} Activity')
        instructions = activity.get('instructions', [
            "Form groups of 3-4.",
            "Review materials.",
            "Complete the task.",
            "Prepare to share."
        ])

        # Ensure instructions is a list
        if isinstance(instructions, str):
            instructions = [instructions]

        structure = activity.get('structure', {})

        return {
            "slide_number": 15,
            "type": "activity",
            "header": f"Activity: {activity_name[:30]}.",
            "body": [
                f"Duration: {activity.get('duration', 15)} minutes.",
                "",
                "Instructions:",
                *[f"• {inst[:60]}." if not inst.endswith('.') else f"• {inst[:60]}" for inst in instructions[:4]]
            ],
            "timing": {
                "setup": f"{structure.get('setup', 2)} min",
                "work": f"{structure.get('work_time', 10)} min",
                "share": f"{structure.get('share_out', 3)} min"
            },
            "grouping": activity.get('grouping', 'groups of 3-4'),
            "duration_on_screen": "15 minutes"
        }

    def _generate_journal_slide(self, lesson_data: LessonData, journal: Dict, exit_tickets: Dict) -> Dict:
        """Generate journal & exit ticket slide."""
        journal_prompt = journal.get('prompt', f"Reflect on today's learning about {lesson_data.topic}.")
        exit_questions = exit_tickets.get('questions', [
            f"What is one key concept from today's lesson?",
            f"How will you apply what you learned?"
        ])

        return {
            "slide_number": 16,
            "type": "journal_exit",
            "header": "Reflection & Exit Ticket.",
            "body": [
                "Journal (5 min):",
                f"• {journal_prompt[:60]}.",
                "",
                "Exit Ticket (3 min):",
                *[f"• {q[:55]}." if not q.endswith('.') else f"• {q[:55]}" for q in exit_questions[:2]]
            ],
            "sentence_starters": journal.get('format', {}).get('optional_sentence_starters', [
                "Today I learned...",
                "This connects to...",
                "I'm wondering about..."
            ]),
            "duration_on_screen": "10 minutes"
        }


class DifferentiationAnnotatorAgent(Agent):
    """
    Annotates lesson components with differentiation strategies.

    Adds support for:
    - ELL (English Language Learners)
    - Students with IEPs/504s
    - Advanced learners
    - Struggling learners
    """

    # Differentiation strategy templates
    STRATEGIES = {
        "ell": {
            "visual_supports": [
                "Graphic organizers with visual cues",
                "Word walls with images",
                "Sentence frames on handouts",
                "Video clips with subtitles"
            ],
            "language_supports": [
                "Vocabulary pre-teaching",
                "Native language glossary if available",
                "Simplified instructions",
                "Strategic pairing with bilingual peers"
            ],
            "assessment_modifications": [
                "Extended time for written responses",
                "Oral demonstration options",
                "Drawing to show understanding",
                "Home language responses accepted"
            ]
        },
        "struggling": {
            "scaffolding": [
                "Chunked instructions (one step at a time)",
                "Graphic organizers pre-filled",
                "Word banks provided",
                "Check-ins every 5 minutes"
            ],
            "supports": [
                "Peer tutor assigned",
                "Reduced quantity expectations",
                "Alternative ways to demonstrate learning",
                "Extra modeling before independent work"
            ]
        },
        "advanced": {
            "extensions": [
                "Leadership role in group work",
                "Research connections to other periods",
                "Create teaching materials for peers",
                "Analysis of primary sources"
            ],
            "challenges": [
                "Higher-order thinking questions",
                "Cross-curricular connections",
                "Independent project options",
                "Peer mentoring opportunities"
            ]
        }
    }

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Generate differentiation for each component
        annotations = {
            "lesson_overview": self._annotate_lesson(lesson_data),
            "warmup": self._annotate_warmup(lesson_data),
            "lecture": self._annotate_lecture(lesson_data),
            "activity": self._annotate_activity(lesson_data),
            "assessment": self._annotate_assessment(lesson_data)
        }

        return {
            "differentiation_annotations": annotations,
            "student_groups_addressed": ["ell", "struggling", "advanced", "iep_504"],
            "implementation_notes": self._generate_implementation_notes(lesson_data)
        }

    def _annotate_lesson(self, lesson_data: LessonData) -> Dict:
        """Generate lesson-level differentiation overview."""
        return {
            "ell": {
                "pre_teaching": f"Pre-teach vocabulary: {', '.join([v.get('term', '') for v in lesson_data.vocabulary[:3]])}",
                "visual_support": "Provide visual anchor chart for key concepts",
                "partner_work": "Pair ELL students with supportive English speakers"
            },
            "struggling": {
                "scaffolding": "Provide graphic organizer for note-taking",
                "chunking": "Break lecture into 5-minute segments with processing time",
                "check_ins": "Brief individual check-ins during transitions"
            },
            "advanced": {
                "extension": f"Research connections between {lesson_data.topic} and contemporary theater",
                "leadership": "Assign group leader role during activity",
                "depth": "Provide primary source documents for analysis"
            }
        }

    def _annotate_warmup(self, lesson_data: LessonData) -> Dict:
        """Generate warmup-specific differentiation."""
        return {
            "ell": {
                "strategy": "Demonstrate warmup visually, minimize verbal instructions",
                "support": "Partner with student who can model"
            },
            "struggling": {
                "strategy": "Simplify warmup steps, provide visual cue cards",
                "support": "Position near teacher for guidance"
            },
            "advanced": {
                "strategy": "Add complexity or leadership role",
                "support": "Ask to demonstrate for class"
            }
        }

    def _annotate_lecture(self, lesson_data: LessonData) -> Dict:
        """Generate lecture-specific differentiation."""
        return {
            "ell": {
                "visual_supports": "Use images, videos, gestures to support verbal content",
                "vocabulary": "Highlight and define key terms as they appear",
                "pacing": "Slower pace with frequent comprehension checks"
            },
            "struggling": {
                "note_taking": "Provide guided notes with fill-in-the-blank sections",
                "processing": "Pause every 5 minutes for partner discussion",
                "review": "Brief recap before moving to new content"
            },
            "advanced": {
                "questions": "Higher-order questions during lecture",
                "connections": "Ask to identify connections to previous learning",
                "analysis": "Provide supplementary primary sources"
            }
        }

    def _annotate_activity(self, lesson_data: LessonData) -> Dict:
        """Generate activity-specific differentiation."""
        return {
            "ell": {
                "instructions": "Written and verbal instructions with visual steps",
                "grouping": "Strategic group placement with language support",
                "output": "Allow drawing or acting instead of writing"
            },
            "struggling": {
                "instructions": "Step-by-step checklist, one task at a time",
                "support": "Assign peer buddy, frequent teacher check-ins",
                "modification": "Reduced output expectations, focus on key skills"
            },
            "advanced": {
                "extension": "Additional challenge questions or tasks",
                "role": "Facilitator or timekeeper role in group",
                "depth": "Research or creative extension option"
            }
        }

    def _annotate_assessment(self, lesson_data: LessonData) -> Dict:
        """Generate assessment-specific differentiation."""
        return {
            "ell": {
                "exit_ticket": "Simplified language, visual response options",
                "journal": "Sentence starters, home language acceptable",
                "alternative": "Verbal response to teacher if needed"
            },
            "struggling": {
                "exit_ticket": "Reduced number of questions, word bank",
                "journal": "Sentence starters required, reduced length",
                "alternative": "Drawing with labels acceptable"
            },
            "advanced": {
                "exit_ticket": "Additional analysis question",
                "journal": "Deeper reflection prompt available",
                "extension": "Optional take-home challenge"
            }
        }

    def _generate_implementation_notes(self, lesson_data: LessonData) -> List[str]:
        """Generate practical implementation notes for teacher."""
        return [
            "Review IEP/504 accommodations before class",
            "Prepare materials in advance for differentiated groups",
            "Have visual supports ready (anchor charts, images)",
            "Plan strategic seating/grouping before students arrive",
            "Prepare simplified and extended versions of key handouts",
            f"Pre-teach vocabulary for ELL students: {', '.join([v.get('term', '') for v in lesson_data.vocabulary[:3]])}"
        ]


class MaterialsListGeneratorAgent(Agent):
    """
    Generates comprehensive materials and preparation lists.

    Includes:
    - Materials needed
    - Teacher preparation tasks
    - Room setup requirements
    - Technology requirements
    """

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_data = extract_lesson_data(context)
        if not lesson_data:
            return {"error": "No lesson data provided"}

        # Get previous outputs
        previous = context.get('previous_outputs', {})

        materials = self._generate_materials_list(lesson_data, previous)
        prep_tasks = self._generate_prep_tasks(lesson_data, previous)
        room_setup = self._generate_room_setup(lesson_data)
        tech_requirements = self._generate_tech_requirements(lesson_data)

        return {
            "materials_list": materials,
            "preparation_tasks": prep_tasks,
            "room_setup": room_setup,
            "technology_requirements": tech_requirements,
            "prep_time_estimate": self._estimate_prep_time(materials, prep_tasks)
        }

    def _generate_materials_list(self, lesson_data: LessonData, previous: Dict) -> Dict:
        """Generate categorized materials list."""
        # Base materials for every lesson
        base_materials = {
            "presentation": [
                {"item": "PowerPoint presentation", "quantity": "1", "source": "digital"},
                {"item": "Projector/display", "quantity": "1", "source": "classroom"}
            ],
            "handouts": [],
            "activity_materials": [],
            "assessment_materials": []
        }

        # Add handouts
        handout_output = previous.get('handout_generator', {})
        handouts = handout_output.get('handouts', [])
        for handout in handouts:
            base_materials["handouts"].append({
                "item": handout.get('name', 'Handout'),
                "quantity": handout.get('copies_needed', '1 per student'),
                "source": "print"
            })

        # Always include exit ticket
        base_materials["assessment_materials"].append({
            "item": "Exit tickets",
            "quantity": "1 per student",
            "source": "print"
        })

        # Add vocabulary cards if vocabulary exists
        if lesson_data.vocabulary:
            base_materials["handouts"].append({
                "item": "Vocabulary reference sheet",
                "quantity": "1 per student",
                "source": "print"
            })

        # Add activity-specific materials
        activity = lesson_data.activity or previous.get('activity_generator', {}).get('activity', {})
        activity_materials = activity.get('materials_needed', [])
        for mat in activity_materials:
            if isinstance(mat, str):
                base_materials["activity_materials"].append({
                    "item": mat,
                    "quantity": "as needed",
                    "source": "classroom supplies"
                })

        return base_materials

    def _generate_prep_tasks(self, lesson_data: LessonData, previous: Dict) -> List[Dict]:
        """Generate teacher preparation checklist."""
        tasks = [
            {
                "task": "Review and finalize PowerPoint presentation",
                "when": "day before",
                "time_minutes": 10,
                "priority": "high"
            },
            {
                "task": "Print handouts and exit tickets",
                "when": "day before",
                "time_minutes": 10,
                "priority": "high"
            },
            {
                "task": "Prepare differentiated materials for ELL/struggling students",
                "when": "day before",
                "time_minutes": 15,
                "priority": "medium"
            },
            {
                "task": "Test technology (projector, audio if needed)",
                "when": "before class",
                "time_minutes": 5,
                "priority": "high"
            },
            {
                "task": "Set up room for warmup activity",
                "when": "before class",
                "time_minutes": 5,
                "priority": "medium"
            },
            {
                "task": "Review lesson plan and presenter notes",
                "when": "before class",
                "time_minutes": 10,
                "priority": "high"
            }
        ]

        # Add vocabulary prep if needed
        if lesson_data.vocabulary:
            tasks.append({
                "task": f"Prepare vocabulary visual aids for: {', '.join([v.get('term', '') for v in lesson_data.vocabulary[:3]])}",
                "when": "day before",
                "time_minutes": 15,
                "priority": "medium"
            })

        return tasks

    def _generate_room_setup(self, lesson_data: LessonData) -> Dict:
        """Generate room setup requirements."""
        return {
            "desk_arrangement": {
                "default": "rows facing front",
                "for_warmup": "cleared center space or standing at desks",
                "for_activity": "clusters of 3-4 for group work"
            },
            "front_of_room": [
                "Projector screen visible",
                "Whiteboard accessible",
                "Agenda posted"
            ],
            "materials_station": [
                "Handouts organized by class period",
                "Extra pencils available",
                "Exit ticket collection bin"
            ],
            "special_requirements": [
                "Space for physical warmup",
                "Clear pathways for circulation"
            ]
        }

    def _generate_tech_requirements(self, lesson_data: LessonData) -> Dict:
        """Generate technology requirements."""
        return {
            "required": [
                {"item": "Computer with PowerPoint", "purpose": "Presentation"},
                {"item": "Projector or display", "purpose": "Showing slides"}
            ],
            "optional": [
                {"item": "Document camera", "purpose": "Showing handouts"},
                {"item": "Timer display", "purpose": "Activity timing"},
                {"item": "Audio speakers", "purpose": "Video clips if included"}
            ],
            "backup_plan": "Have printed copies of key slides in case of tech failure"
        }

    def _estimate_prep_time(self, materials: Dict, tasks: List[Dict]) -> Dict:
        """Estimate total preparation time."""
        total_minutes = sum(task.get('time_minutes', 0) for task in tasks)

        return {
            "day_before_minutes": sum(
                t.get('time_minutes', 0) for t in tasks if t.get('when') == 'day before'
            ),
            "before_class_minutes": sum(
                t.get('time_minutes', 0) for t in tasks if t.get('when') == 'before class'
            ),
            "total_minutes": total_minutes,
            "recommendation": f"Plan approximately {total_minutes} minutes total preparation time"
        }
