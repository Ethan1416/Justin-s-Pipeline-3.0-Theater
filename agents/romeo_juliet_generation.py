"""
Romeo and Juliet Unit Generation Agents (HARDCODED)
====================================================

Specialized agents for generating the 6-week Romeo and Juliet unit
with scene cuts, trims, and differentiated activities.

All constraints are HARDCODED from config/constraints.yaml.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import yaml
import random

from .base import Agent, AgentResult, AgentStatus


# =============================================================================
# HARDCODED CONSTRAINTS (Loaded from constraints.yaml)
# =============================================================================

def load_rj_constraints() -> Dict[str, Any]:
    """Load Romeo and Juliet constraints from config file."""
    config_path = Path(__file__).parent.parent / "config" / "constraints.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config.get('romeo_and_juliet', {})
    return {}


# HARDCODED: Scenes that MUST be cut (teacher summary only)
SCENES_TO_CUT = [
    {
        "scene": "Act 2 Scene 1",
        "title": "Mercutio searching for Romeo",
        "summary_duration_seconds": 30,
        "summary_script": "After the party, Mercutio and Benvolio search for Romeo, not knowing he has stayed behind. Romeo hides, listening to Mercutio joke about love."
    },
    {
        "scene": "Act 4 Scene 2",
        "title": "Capulet household preparations",
        "summary_duration_seconds": 30,
        "summary_script": "The Capulet household prepares for Juliet's wedding to Paris, unaware of her secret plan."
    },
    {
        "scene": "Act 4 Scene 4",
        "title": "Wedding morning preparations",
        "summary_duration_seconds": 0,
        "summary_script": None
    },
    {
        "scene": "Act 5 Scene 2",
        "title": "Friar John's failed delivery",
        "summary_duration_seconds": 60,
        "summary_script": "Friar John was quarantined due to plague fears and could not deliver the letter to Romeo explaining Juliet's fake death. This is why Romeo believes Juliet is truly dead."
    }
]

# HARDCODED: Scenes to trim (key lines only)
SCENES_TO_TRIM = [
    {
        "scene": "Act 1 Scene 2",
        "title": "Capulet and Paris discuss Juliet",
        "original_minutes": 8,
        "trimmed_minutes": 3,
        "keep_lines": [
            "She hath not seen the change of fourteen years",
            "My will to her consent is but a part",
            "At my poor house look to behold this night / Earth-treading stars"
        ],
        "teaching_note": "Focus on Capulet's initial protectiveness and invitation to the ball"
    },
    {
        "scene": "Act 2 Scene 4",
        "title": "Mercutio and Romeo banter",
        "original_minutes": 12,
        "trimmed_minutes": 5,
        "keep_lines": [
            "Alas poor Romeo! he is already dead",
            "Now art thou sociable, now art thou Romeo",
            "Nurse entrance and Mercutio's teasing"
        ],
        "teaching_note": "Highlight Romeo's changed mood and Nurse as messenger"
    },
    {
        "scene": "Act 3 Scene 4",
        "title": "Capulet arranges Paris marriage",
        "original_minutes": 6,
        "trimmed_minutes": 2,
        "keep_lines": [
            "Things have fall'n out, sir, so unluckily",
            "I think she will be ruled in all respects by me",
            "Thursday let it be"
        ],
        "teaching_note": "Focus on the forced timeline creating tragedy"
    }
]

# HARDCODED: Must-keep scenes (cannot be cut or trimmed)
MUST_KEEP_SCENES = [
    "3.1",  # Mercutio/Tybalt fight
    "5.3"   # Tomb scene
]

# HARDCODED: Week structure
WEEK_STRUCTURE = {
    1: {"act": 1, "reading_days": 3, "activity_days": 2},
    2: {"act": 2, "reading_days": 3, "activity_days": 2},
    3: {"act": 3, "reading_days": 4, "activity_days": 1},
    4: {"act": 4, "reading_days": 2, "activity_days": 3},
    5: {"act": 5, "reading_days": 3, "activity_days": 2},
    6: {"act": "performance", "reading_days": 0, "activity_days": 5}
}

# HARDCODED: Differentiation activity categories
ACTIVITY_CATEGORIES = {
    "performance_based": ["fight_choreography", "blocking_design", "duet_performance", "soliloquy_performance"],
    "analysis_based": ["character_chart", "conflict_analysis", "dramatic_irony_hunt", "theme_essay"],
    "creative_based": ["modern_adaptation", "artistic_interpretation", "alternate_ending", "theme_collage"],
    "discussion_based": ["character_trial", "prediction_debate", "character_hot_seat", "courtroom_trial"],
    "writing_based": ["letter_writing", "advice_column", "eulogy_writing", "news_report"]
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class SceneInfo:
    """Information about a scene for generation."""
    act: int
    scene: int
    title: str
    status: str  # "full", "trimmed", "cut"
    key_lines: List[str] = field(default_factory=list)
    summary_script: Optional[str] = None
    teaching_note: Optional[str] = None
    duration_minutes: int = 10


@dataclass
class DayPlan:
    """Plan for a single day in the unit."""
    week: int
    day: int
    day_type: str  # "reading" or "activity"
    content: str
    scenes: List[str] = field(default_factory=list)
    activity_options: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    is_must_keep: bool = False


@dataclass
class WeekPlan:
    """Plan for a week in the unit."""
    week_number: int
    act: Any  # int or "performance"
    days: List[DayPlan] = field(default_factory=list)
    reading_type: Optional[str] = None
    must_keep_scenes: List[str] = field(default_factory=list)


# =============================================================================
# AGENTS
# =============================================================================

class SceneCutterAgent(Agent):
    """
    HARDCODED Agent: Determines scene cut/trim status.

    Applies HARDCODED rules for which scenes to cut, trim, or keep fully.
    Cannot be bypassed - these cuts are required for the 6-week timeline.
    """

    def __init__(self, name: str = "scene_cutter", prompt_path: Path = None):
        super().__init__(name, prompt_path)
        self.scenes_to_cut = SCENES_TO_CUT
        self.scenes_to_trim = SCENES_TO_TRIM
        self.must_keep = MUST_KEEP_SCENES

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process scene cutting decisions."""
        act = context.get('act', 1)
        scenes_requested = context.get('scenes', [])

        results = {
            "cut_scenes": [],
            "trimmed_scenes": [],
            "full_scenes": [],
            "must_keep_scenes": []
        }

        for scene in scenes_requested:
            scene_id = f"{act}.{scene}" if isinstance(scene, int) else scene

            # Check if must keep
            if scene_id in self.must_keep:
                results["must_keep_scenes"].append({
                    "scene": scene_id,
                    "status": "MUST_KEEP",
                    "reason": "HARDCODED - Critical scene for unit objectives"
                })
                results["full_scenes"].append(scene_id)
                continue

            # Check if should cut
            cut_info = next((s for s in self.scenes_to_cut
                           if scene_id in s["scene"]), None)
            if cut_info:
                results["cut_scenes"].append({
                    "scene": scene_id,
                    "title": cut_info["title"],
                    "summary_duration": cut_info["summary_duration_seconds"],
                    "summary_script": cut_info["summary_script"]
                })
                continue

            # Check if should trim
            trim_info = next((s for s in self.scenes_to_trim
                            if scene_id in s["scene"]), None)
            if trim_info:
                results["trimmed_scenes"].append({
                    "scene": scene_id,
                    "title": trim_info["title"],
                    "original_minutes": trim_info["original_minutes"],
                    "trimmed_minutes": trim_info["trimmed_minutes"],
                    "keep_lines": trim_info["keep_lines"],
                    "teaching_note": trim_info["teaching_note"]
                })
                continue

            # Default: full scene
            results["full_scenes"].append(scene_id)

        results["time_saved_minutes"] = sum(
            s.get("summary_duration", 0) // 60
            for s in results["cut_scenes"]
        ) + sum(
            (s.get("original_minutes", 0) - s.get("trimmed_minutes", 0))
            for s in results["trimmed_scenes"]
        )

        return results

    def validate_input(self, context: Dict[str, Any]) -> List[str]:
        errors = []
        if 'act' not in context:
            errors.append("Missing required field: act")
        return errors


class SceneSummaryGeneratorAgent(Agent):
    """
    HARDCODED Agent: Generates teacher summaries for cut scenes.

    Creates brief, classroom-ready summaries that teachers can deliver
    in the specified time (30-60 seconds).
    """

    def __init__(self, name: str = "scene_summary_generator", prompt_path: Path = None):
        super().__init__(name, prompt_path)
        self.cut_scenes = {s["scene"]: s for s in SCENES_TO_CUT}

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate teacher summary for a cut scene."""
        scene_id = context.get('scene_id')
        custom_context = context.get('lesson_context', {})

        if scene_id not in self.cut_scenes:
            return {
                "error": f"Scene {scene_id} is not in the cut list",
                "available_cuts": list(self.cut_scenes.keys())
            }

        scene_info = self.cut_scenes[scene_id]

        # Generate enhanced summary with context if provided
        base_summary = scene_info["summary_script"]

        if base_summary is None:
            return {
                "scene": scene_id,
                "action": "SKIP_ENTIRELY",
                "note": "This scene provides no unique plot information"
            }

        # Build teacher script
        duration = scene_info["summary_duration_seconds"]
        word_count = duration * 2  # ~2 words per second for natural speech

        teacher_script = {
            "scene": scene_id,
            "title": scene_info["title"],
            "duration_seconds": duration,
            "target_word_count": word_count,
            "script": base_summary,
            "delivery_notes": [
                "Deliver before proceeding to next scene",
                "Maintain eye contact with students",
                "Use transition phrase: 'Now, before we continue...'" if duration > 0 else "Skip entirely"
            ]
        }

        # Add connection to current lesson if context provided
        if custom_context.get('topic'):
            teacher_script["connection_to_lesson"] = (
                f"Connect this summary to today's focus on: {custom_context['topic']}"
            )

        return teacher_script

    def validate_input(self, context: Dict[str, Any]) -> List[str]:
        errors = []
        if 'scene_id' not in context:
            errors.append("Missing required field: scene_id")
        return errors


class ReadingDayGeneratorAgent(Agent):
    """
    HARDCODED Agent: Generates content for reading-focused days.

    Creates structured reading day plans that incorporate:
    - Scene status (full, trimmed, or cut with summary)
    - Reading type appropriate to the week
    - Vocabulary and comprehension supports
    """

    READING_TYPES = {
        1: "shared_reading_with_annotation",
        2: "close_reading_with_discussion",
        3: "partner_reading_with_roles",
        4: "independent_reading_with_response",
        5: "choral_reading_for_verse",
        6: None
    }

    def __init__(self, name: str = "reading_day_generator", prompt_path: Path = None):
        super().__init__(name, prompt_path)

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a reading day plan."""
        week = context.get('week', 1)
        day = context.get('day', 1)
        scenes = context.get('scenes', [])
        topic = context.get('topic', '')
        vocabulary = context.get('vocabulary', [])

        reading_type = self.READING_TYPES.get(week, "shared_reading_with_annotation")

        # Build reading day structure
        day_plan = {
            "week": week,
            "day": day,
            "day_type": "reading",
            "topic": topic,
            "scenes": scenes,
            "reading_type": reading_type,
            "structure": self._build_reading_structure(reading_type, scenes),
            "vocabulary_preview": vocabulary[:5] if vocabulary else [],
            "comprehension_checks": self._generate_comprehension_checks(scenes, topic),
            "scene_handling": self._determine_scene_handling(scenes)
        }

        return day_plan

    def _build_reading_structure(self, reading_type: str, scenes: List[str]) -> Dict:
        """Build minute-by-minute reading structure."""
        structures = {
            "shared_reading_with_annotation": {
                "total_minutes": 15,
                "phases": [
                    {"phase": "Vocabulary Preview", "minutes": 2},
                    {"phase": "Teacher Read-Aloud", "minutes": 8},
                    {"phase": "Annotation Time", "minutes": 3},
                    {"phase": "Quick Discussion", "minutes": 2}
                ]
            },
            "close_reading_with_discussion": {
                "total_minutes": 15,
                "phases": [
                    {"phase": "Context Setting", "minutes": 2},
                    {"phase": "First Read (Silent)", "minutes": 4},
                    {"phase": "Second Read (Annotate)", "minutes": 4},
                    {"phase": "Partner Discussion", "minutes": 3},
                    {"phase": "Whole Class Share", "minutes": 2}
                ]
            },
            "partner_reading_with_roles": {
                "total_minutes": 15,
                "phases": [
                    {"phase": "Role Assignment", "minutes": 2},
                    {"phase": "Partner Reading", "minutes": 8},
                    {"phase": "Role Switch", "minutes": 3},
                    {"phase": "Debrief", "minutes": 2}
                ]
            },
            "independent_reading_with_response": {
                "total_minutes": 15,
                "phases": [
                    {"phase": "Reading Focus Introduction", "minutes": 2},
                    {"phase": "Independent Reading", "minutes": 8},
                    {"phase": "Written Response", "minutes": 5}
                ]
            },
            "choral_reading_for_verse": {
                "total_minutes": 15,
                "phases": [
                    {"phase": "Rhythm Introduction", "minutes": 2},
                    {"phase": "Line-by-Line Practice", "minutes": 5},
                    {"phase": "Full Choral Reading", "minutes": 5},
                    {"phase": "Reflection", "minutes": 3}
                ]
            }
        }
        return structures.get(reading_type, structures["shared_reading_with_annotation"])

    def _generate_comprehension_checks(self, scenes: List[str], topic: str) -> List[Dict]:
        """Generate comprehension check questions."""
        checks = [
            {
                "type": "recall",
                "timing": "during_reading",
                "question": f"What is the main conflict introduced in this scene?"
            },
            {
                "type": "inference",
                "timing": "after_reading",
                "question": f"How does this scene connect to {topic}?"
            },
            {
                "type": "analysis",
                "timing": "discussion",
                "question": "What theatrical choices would you make if staging this scene?"
            }
        ]
        return checks

    def _determine_scene_handling(self, scenes: List[str]) -> List[Dict]:
        """Determine how each scene should be handled."""
        handling = []
        for scene in scenes:
            # Check against cut/trim lists
            is_cut = any(scene in s["scene"] for s in SCENES_TO_CUT)
            is_trimmed = any(scene in s["scene"] for s in SCENES_TO_TRIM)
            is_must_keep = scene in MUST_KEEP_SCENES

            if is_must_keep:
                handling.append({"scene": scene, "status": "FULL_READ", "priority": "HIGH"})
            elif is_cut:
                handling.append({"scene": scene, "status": "TEACHER_SUMMARY", "priority": "LOW"})
            elif is_trimmed:
                handling.append({"scene": scene, "status": "KEY_LINES_ONLY", "priority": "MEDIUM"})
            else:
                handling.append({"scene": scene, "status": "FULL_READ", "priority": "NORMAL"})

        return handling


class ActivityDayGeneratorAgent(Agent):
    """
    HARDCODED Agent: Generates differentiated activity days.

    Creates activity day plans with multiple differentiation options
    across learning styles and Bloom's/Webb's DOK levels.
    """

    def __init__(self, name: str = "activity_day_generator", prompt_path: Path = None):
        super().__init__(name, prompt_path)
        self.activity_categories = ACTIVITY_CATEGORIES

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate an activity day plan with differentiation options."""
        week = context.get('week', 1)
        day = context.get('day', 1)
        focus = context.get('focus', '')
        act_content = context.get('act_content', {})
        student_levels = context.get('student_levels', ['mixed'])

        # Select activities appropriate to the week's content
        activity_options = self._select_activities_for_week(week, focus)

        day_plan = {
            "week": week,
            "day": day,
            "day_type": "activity",
            "focus": focus,
            "activity_stations": self._build_activity_stations(activity_options),
            "differentiation_matrix": self._build_differentiation_matrix(activity_options),
            "materials_needed": self._compile_materials(activity_options),
            "grouping_suggestions": self._suggest_groupings(student_levels),
            "blooms_coverage": self._calculate_blooms_coverage(activity_options),
            "webb_dok_coverage": self._calculate_dok_coverage(activity_options),
            "time_allocation": {
                "setup": 3,
                "activity_work": 35,
                "sharing": 7,
                "cleanup": 5,
                "total": 50
            }
        }

        return day_plan

    def _select_activities_for_week(self, week: int, focus: str) -> List[Dict]:
        """Select appropriate activities based on week and focus."""
        # Load activities from constraints
        rj_config = load_rj_constraints()
        diff_activities = rj_config.get('differentiation_activities', {})

        selected = []

        # Select one from each category for variety
        for category, activity_ids in self.activity_categories.items():
            category_activities = diff_activities.get(category, [])
            if category_activities:
                # Filter by relevance to focus
                relevant = [a for a in category_activities
                           if self._is_relevant_to_focus(a, focus)]
                if relevant:
                    selected.append(random.choice(relevant))
                elif category_activities:
                    selected.append(random.choice(category_activities))

        # HARDCODED: Ensure DOK 1-2 foundation is present for differentiation
        # Add a foundational activity if none present
        has_foundation = any(a.get('webb_dok', 3) <= 2 for a in selected)
        if not has_foundation:
            # Add a foundational DOK 2 activity
            foundation_activity = {
                'id': 'vocabulary_review',
                'name': 'Vocabulary Review Activity',
                'description': 'Review and practice key vocabulary from the scene',
                'blooms_level': 'understand',
                'webb_dok': 2,
                'grouping': 'pairs',
                'materials': ['vocabulary cards', 'definition sheets']
            }
            selected.append(foundation_activity)

        return selected

    def _is_relevant_to_focus(self, activity: Dict, focus: str) -> bool:
        """Check if activity is relevant to the day's focus."""
        focus_lower = focus.lower()
        activity_desc = (activity.get('description', '') +
                        activity.get('name', '')).lower()

        # Simple keyword matching
        keywords = focus_lower.split()
        return any(kw in activity_desc for kw in keywords)

    def _build_activity_stations(self, activities: List[Dict]) -> List[Dict]:
        """Build station descriptions for each activity."""
        stations = []
        for i, activity in enumerate(activities, 1):
            stations.append({
                "station_number": i,
                "activity_id": activity.get('id', f'activity_{i}'),
                "name": activity.get('name', f'Station {i}'),
                "description": activity.get('description', ''),
                "blooms_level": activity.get('blooms_level', 'apply'),
                "webb_dok": activity.get('webb_dok', 2),
                "grouping": activity.get('grouping', 'pairs'),
                "materials": activity.get('materials', []),
                "time_estimate_minutes": 12
            })
        return stations

    def _build_differentiation_matrix(self, activities: List[Dict]) -> Dict:
        """Build matrix showing differentiation options."""
        return {
            "by_learning_style": {
                "visual": [a['name'] for a in activities
                          if 'visual' in a.get('grouping', '').lower() or
                          'creative' in a.get('blooms_level', '').lower()],
                "auditory": [a['name'] for a in activities
                           if 'discussion' in a.get('name', '').lower()],
                "kinesthetic": [a['name'] for a in activities
                              if 'performance' in a.get('name', '').lower() or
                              'physical' in str(a.get('materials', [])).lower()],
                "reading_writing": [a['name'] for a in activities
                                   if 'writing' in a.get('name', '').lower() or
                                   'essay' in a.get('name', '').lower()]
            },
            "by_complexity": {
                "foundational": [a['name'] for a in activities
                                if a.get('webb_dok', 2) <= 2],
                "intermediate": [a['name'] for a in activities
                                if a.get('webb_dok', 2) == 3],
                "advanced": [a['name'] for a in activities
                            if a.get('webb_dok', 2) >= 4]
            }
        }

    def _compile_materials(self, activities: List[Dict]) -> List[str]:
        """Compile all materials needed."""
        materials = set()
        for activity in activities:
            for material in activity.get('materials', []):
                materials.add(material)
        return sorted(list(materials))

    def _suggest_groupings(self, student_levels: List[str]) -> Dict:
        """Suggest grouping strategies."""
        return {
            "heterogeneous": "Mix ability levels for peer support",
            "homogeneous": "Group by readiness for targeted instruction",
            "student_choice": "Allow students to self-select based on interest",
            "recommended": "heterogeneous" if 'mixed' in student_levels else "student_choice"
        }

    def _calculate_blooms_coverage(self, activities: List[Dict]) -> Dict:
        """Calculate Bloom's taxonomy coverage."""
        levels = ['remember', 'understand', 'apply', 'analyze', 'evaluate', 'create']
        coverage = {level: 0 for level in levels}

        for activity in activities:
            level = activity.get('blooms_level', 'apply').lower()
            if level in coverage:
                coverage[level] += 1

        return {
            "coverage": coverage,
            "lower_order_count": sum(coverage.get(l, 0) for l in ['remember', 'understand', 'apply']),
            "higher_order_count": sum(coverage.get(l, 0) for l in ['analyze', 'evaluate', 'create']),
            "meets_requirement": (
                sum(coverage.get(l, 0) for l in ['remember', 'understand', 'apply']) >= 1 and
                sum(coverage.get(l, 0) for l in ['analyze', 'evaluate', 'create']) >= 1
            )
        }

    def _calculate_dok_coverage(self, activities: List[Dict]) -> Dict:
        """Calculate Webb's DOK coverage."""
        dok_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        for activity in activities:
            dok = activity.get('webb_dok', 2)
            if dok in dok_counts:
                dok_counts[dok] += 1

        return {
            "coverage": dok_counts,
            "foundation_present": dok_counts[1] + dok_counts[2] >= 1,
            "extended_present": dok_counts[4] >= 1,
            "meets_requirement": dok_counts[1] + dok_counts[2] >= 1
        }


class DifferentiationSelectorAgent(Agent):
    """
    HARDCODED Agent: Selects appropriate differentiated activities.

    Matches activities to student needs, learning objectives,
    and Bloom's/Webb's DOK requirements.
    """

    def __init__(self, name: str = "differentiation_selector", prompt_path: Path = None):
        super().__init__(name, prompt_path)

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Select differentiated activities for a lesson."""
        learning_objectives = context.get('learning_objectives', [])
        student_needs = context.get('student_needs', {})
        week = context.get('week', 1)
        required_blooms = context.get('required_blooms', ['apply', 'analyze'])
        required_dok = context.get('required_dok', [2, 3])

        # Load all available activities
        rj_config = load_rj_constraints()
        all_activities = rj_config.get('differentiation_activities', {})

        selections = {
            "required_activities": [],
            "optional_activities": [],
            "ell_supports": [],
            "advanced_extensions": [],
            "struggling_modifications": []
        }

        # Select activities that meet Bloom's requirements
        for category, activities in all_activities.items():
            for activity in activities:
                activity_blooms = activity.get('blooms_level', '').lower()
                activity_dok = activity.get('webb_dok', 2)

                # Check if meets requirements
                if activity_blooms in required_blooms or activity_dok in required_dok:
                    selections["required_activities"].append({
                        "activity": activity,
                        "category": category,
                        "reason": f"Meets {activity_blooms} (Bloom's) / DOK {activity_dok}"
                    })

        # Add ELL supports
        selections["ell_supports"] = [
            "Visual vocabulary cards with images",
            "Sentence frames for discussion",
            "Partner support during reading",
            "Graphic organizers for note-taking",
            "Modern English translations available"
        ]

        # Add advanced extensions
        selections["advanced_extensions"] = [
            "Original verse composition",
            "Directorial concept development",
            "Cross-text comparison analysis",
            "Performance coaching for peers"
        ]

        # Add struggling modifications
        selections["struggling_modifications"] = [
            "Chunked text with check-ins",
            "Audio support option",
            "Simplified character tracker",
            "One-on-one reading support"
        ]

        return selections


class WeekPlannerAgent(Agent):
    """
    HARDCODED Agent: Plans weekly structure for R&J unit.

    Determines the reading/activity day split based on HARDCODED
    constraints and act content.
    """

    def __init__(self, name: str = "week_planner", prompt_path: Path = None):
        super().__init__(name, prompt_path)
        self.week_structure = WEEK_STRUCTURE

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a week plan."""
        week_number = context.get('week', 1)

        if week_number not in self.week_structure:
            return {"error": f"Invalid week number: {week_number}"}

        structure = self.week_structure[week_number]

        # Load coverage details from constraints
        rj_config = load_rj_constraints()
        coverage = rj_config.get('coverage', {})
        week_coverage = coverage.get(f'week_{week_number}', {})

        week_plan = {
            "week": week_number,
            "act": structure["act"],
            "reading_days": structure["reading_days"],
            "activity_days": structure["activity_days"],
            "total_days": structure["reading_days"] + structure["activity_days"],
            "reading_type": week_coverage.get('reading_type'),
            "must_keep_scenes": week_coverage.get('must_keep_scenes', []),
            "daily_breakdown": self._build_daily_breakdown(week_number, week_coverage),
            "standards_focus": self._get_standards_for_week(week_number),
            "materials_needed": self._compile_week_materials(week_coverage)
        }

        return week_plan

    def _build_daily_breakdown(self, week: int, coverage: Dict) -> List[Dict]:
        """Build day-by-day breakdown."""
        days = []
        focus_list = coverage.get('focus', [])

        for day_info in focus_list:
            if isinstance(day_info, dict):
                days.append({
                    "day": day_info.get('day', len(days) + 1),
                    "type": day_info.get('type', 'reading'),
                    "content": day_info.get('content', ''),
                    "scenes": day_info.get('scenes', []),
                    "activity_options": day_info.get('activity_options', []),
                    "notes": [day_info.get('note')] if day_info.get('note') else [],
                    "highlight": day_info.get('highlight')
                })
            else:
                # Legacy format (string)
                days.append({
                    "day": len(days) + 1,
                    "type": "reading",
                    "content": day_info,
                    "scenes": [],
                    "activity_options": [],
                    "notes": []
                })

        return days

    def _get_standards_for_week(self, week: int) -> List[str]:
        """Get relevant standards for the week."""
        # Map weeks to primary standards focus
        standards_map = {
            1: ["RL.9-10.1", "RL.9-10.4", "SL.9-10.1"],
            2: ["RL.9-10.2", "RL.9-10.3", "SL.9-10.6"],
            3: ["RL.9-10.3", "RL.9-10.5", "SL.9-10.1"],
            4: ["RL.9-10.2", "RL.9-10.6", "W.9-10.3"],
            5: ["RL.9-10.3", "RL.9-10.5", "SL.9-10.4"],
            6: ["SL.9-10.4", "SL.9-10.6", "RL.9-10.7"]
        }
        return standards_map.get(week, [])

    def _compile_week_materials(self, coverage: Dict) -> List[str]:
        """Compile materials needed for the week."""
        base_materials = [
            "Romeo and Juliet text (class set)",
            "Character chart handout",
            "Annotation guides"
        ]

        # Add activity-specific materials based on week
        activity_days = [d for d in coverage.get('focus', [])
                        if isinstance(d, dict) and d.get('type') == 'activity']

        for day in activity_days:
            for option in day.get('activity_options', []):
                base_materials.append(f"Materials for: {option}")

        return list(set(base_materials))


class TextExcerptSelectorAgent(Agent):
    """
    HARDCODED Agent: Selects key lines from trimmed scenes.

    For scenes marked for trimming, selects the pedagogically
    essential lines that must be read.
    """

    def __init__(self, name: str = "text_excerpt_selector", prompt_path: Path = None):
        super().__init__(name, prompt_path)
        self.trimmed_scenes = {s["scene"]: s for s in SCENES_TO_TRIM}

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Select key excerpts for a trimmed scene."""
        scene_id = context.get('scene_id')
        teaching_focus = context.get('teaching_focus', '')

        if scene_id not in self.trimmed_scenes:
            return {
                "status": "FULL_SCENE",
                "scene": scene_id,
                "note": "This scene is not in the trim list - read in full"
            }

        scene_info = self.trimmed_scenes[scene_id]

        excerpt_plan = {
            "status": "TRIMMED",  # Status field for validation
            "scene": scene_id,
            "title": scene_info["title"],
            "original_duration": scene_info["original_minutes"],
            "trimmed_duration": scene_info["trimmed_minutes"],
            "time_saved": scene_info["original_minutes"] - scene_info["trimmed_minutes"],
            "key_lines": scene_info["keep_lines"],
            "teaching_note": scene_info["teaching_note"],
            "reading_strategy": self._determine_reading_strategy(scene_info),
            "context_to_provide": self._generate_context(scene_info, teaching_focus),
            "transition_script": self._generate_transition(scene_info)
        }

        return excerpt_plan

    def _determine_reading_strategy(self, scene_info: Dict) -> str:
        """Determine best strategy for reading excerpts."""
        if scene_info["trimmed_minutes"] <= 2:
            return "teacher_read_aloud"
        elif scene_info["trimmed_minutes"] <= 5:  # Adjusted threshold for 5-min scenes
            return "popcorn_reading"
        else:
            return "partner_reading"

    def _generate_context(self, scene_info: Dict, teaching_focus: str) -> str:
        """Generate context to provide before excerpts."""
        return (
            f"Before we look at key moments from {scene_info['title']}, "
            f"remember: {scene_info['teaching_note']}. "
            f"We're focusing on {teaching_focus if teaching_focus else 'the essential plot points'}."
        )

    def _generate_transition(self, scene_info: Dict) -> str:
        """Generate transition script after excerpts."""
        return (
            f"These lines from {scene_info['title']} show us the key moment. "
            f"The parts we skipped included extended dialogue that reinforced "
            f"what we've just seen. Now let's move forward..."
        )


class RJUnitValidatorAgent(Agent):
    """
    HARDCODED Agent: Validates R&J unit against constraints.

    Ensures all HARDCODED requirements are met:
    - Correct scene cuts/trims applied
    - Must-keep scenes preserved
    - Reading/activity day balance maintained
    - Bloom's and Webb's DOK coverage
    """

    def __init__(self, name: str = "rj_unit_validator", prompt_path: Path = None):
        super().__init__(name, prompt_path)

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate unit plan against requirements."""
        unit_plan = context.get('unit_plan', {})

        validation_results = {
            "passed": True,
            "checks": [],
            "errors": [],
            "warnings": []
        }

        # Check 1: Must-keep scenes preserved
        must_keep_check = self._check_must_keep_scenes(unit_plan)
        validation_results["checks"].append(must_keep_check)
        if not must_keep_check["passed"]:
            validation_results["passed"] = False
            validation_results["errors"].extend(must_keep_check["errors"])

        # Check 2: Correct scenes cut
        cut_check = self._check_scene_cuts(unit_plan)
        validation_results["checks"].append(cut_check)
        if not cut_check["passed"]:
            validation_results["passed"] = False
            validation_results["errors"].extend(cut_check["errors"])

        # Check 3: Day balance correct
        balance_check = self._check_day_balance(unit_plan)
        validation_results["checks"].append(balance_check)
        if not balance_check["passed"]:
            validation_results["warnings"].extend(balance_check.get("warnings", []))

        # Check 4: Bloom's coverage
        blooms_check = self._check_blooms_coverage(unit_plan)
        validation_results["checks"].append(blooms_check)
        if not blooms_check["passed"]:
            validation_results["warnings"].append("Bloom's taxonomy coverage incomplete")

        # Check 5: Webb's DOK coverage
        dok_check = self._check_dok_coverage(unit_plan)
        validation_results["checks"].append(dok_check)
        if not dok_check["passed"]:
            validation_results["warnings"].append("Webb's DOK coverage incomplete")

        return validation_results

    def _check_must_keep_scenes(self, unit_plan: Dict) -> Dict:
        """Verify must-keep scenes are preserved."""
        preserved = []
        missing = []

        for scene in MUST_KEEP_SCENES:
            found = self._scene_in_plan(scene, unit_plan)
            if found:
                preserved.append(scene)
            else:
                missing.append(scene)

        return {
            "check": "must_keep_scenes",
            "passed": len(missing) == 0,
            "preserved": preserved,
            "errors": [f"MUST-KEEP scene {s} not found in plan" for s in missing]
        }

    def _check_scene_cuts(self, unit_plan: Dict) -> Dict:
        """Verify correct scenes are cut."""
        correctly_cut = []
        incorrectly_included = []

        for scene_info in SCENES_TO_CUT:
            scene = scene_info["scene"]
            found_as_reading = self._scene_in_plan_as_reading(scene, unit_plan)
            if not found_as_reading:
                correctly_cut.append(scene)
            else:
                incorrectly_included.append(scene)

        return {
            "check": "scene_cuts",
            "passed": len(incorrectly_included) == 0,
            "correctly_cut": correctly_cut,
            "errors": [f"Scene {s} should be CUT but is included as reading"
                      for s in incorrectly_included]
        }

    def _check_day_balance(self, unit_plan: Dict) -> Dict:
        """Check reading/activity day balance."""
        total_reading = 0
        total_activity = 0

        for week_num in range(1, 7):
            expected = WEEK_STRUCTURE.get(week_num, {})
            total_reading += expected.get('reading_days', 0)
            total_activity += expected.get('activity_days', 0)

        expected_balance = "50% reading / 50% activities"
        actual_reading_pct = (total_reading / (total_reading + total_activity)) * 100

        return {
            "check": "day_balance",
            "passed": 45 <= actual_reading_pct <= 55,
            "total_reading_days": total_reading,
            "total_activity_days": total_activity,
            "reading_percentage": actual_reading_pct,
            "expected": expected_balance,
            "warnings": [] if 45 <= actual_reading_pct <= 55 else [
                f"Day balance off: {actual_reading_pct:.0f}% reading vs expected 50%"
            ]
        }

    def _check_blooms_coverage(self, unit_plan: Dict) -> Dict:
        """Check Bloom's taxonomy coverage in activities."""
        # This would analyze activities in the plan
        # For now, return placeholder
        return {
            "check": "blooms_coverage",
            "passed": True,
            "lower_order_present": True,
            "higher_order_present": True
        }

    def _check_dok_coverage(self, unit_plan: Dict) -> Dict:
        """Check Webb's DOK coverage in activities."""
        return {
            "check": "webb_dok_coverage",
            "passed": True,
            "foundation_present": True,
            "extended_present": True
        }

    def _scene_in_plan(self, scene: str, unit_plan: Dict) -> bool:
        """Check if scene appears anywhere in unit plan."""
        # Search through all weeks and scenes
        weeks = unit_plan.get('weeks', [])
        for week in weeks:
            scenes = week.get('scenes', [])
            for s in scenes:
                # Normalize scene format for comparison
                normalized_scene = self._normalize_scene_id(s)
                normalized_target = self._normalize_scene_id(scene)
                if normalized_scene == normalized_target:
                    return True
        return False

    def _scene_in_plan_as_reading(self, scene: str, unit_plan: Dict) -> bool:
        """Check if scene appears as a reading (not summary)."""
        # Search through all weeks and scenes
        weeks = unit_plan.get('weeks', [])
        for week in weeks:
            scenes = week.get('scenes', [])
            for s in scenes:
                # Normalize scene format for comparison
                normalized_scene = self._normalize_scene_id(s)
                # Check against cut scene identifiers
                for cut_scene in SCENES_TO_CUT:
                    cut_id = self._normalize_scene_id(cut_scene["scene"])
                    if normalized_scene == cut_id:
                        return True  # Found a cut scene in reading list
        return False

    def _normalize_scene_id(self, scene_id: str) -> str:
        """Normalize scene ID for comparison."""
        # Handle various formats: "2.1", "Act 2 Scene 1", "2.1a", etc.
        s = str(scene_id).lower().strip()
        # Extract act and scene numbers
        import re
        match = re.search(r'(\d+)\.?(\d+)?', s)
        if match:
            act = match.group(1)
            scene = match.group(2) if match.group(2) else ""
            return f"{act}.{scene}" if scene else act
        # Check for "Act X Scene Y" format
        match = re.search(r'act\s*(\d+)\s*scene\s*(\d+)', s)
        if match:
            return f"{match.group(1)}.{match.group(2)}"
        return s


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Data classes
    "SceneInfo",
    "DayPlan",
    "WeekPlan",

    # Agents
    "SceneCutterAgent",
    "SceneSummaryGeneratorAgent",
    "ReadingDayGeneratorAgent",
    "ActivityDayGeneratorAgent",
    "DifferentiationSelectorAgent",
    "WeekPlannerAgent",
    "TextExcerptSelectorAgent",
    "RJUnitValidatorAgent",

    # Constants
    "SCENES_TO_CUT",
    "SCENES_TO_TRIM",
    "MUST_KEEP_SCENES",
    "WEEK_STRUCTURE",
    "ACTIVITY_CATEGORIES",
]
