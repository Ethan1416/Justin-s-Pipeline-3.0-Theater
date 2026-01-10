"""
Materials Checklist Generator - Theater Education Pipeline v2.3

Generates 5-minute "grab list" for daily teacher prep.
Includes copies needed, technology checks, physical materials, and pre-class prep.

Generated for: Romeo and Juliet (6-week unit)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MaterialsChecklist:
    """Complete materials checklist for a day."""
    day: int
    copies_needed: List[Dict]
    technology: List[str]
    physical_materials: List[str]
    before_class: List[str]
    during_class: List[str]

# Activity-specific materials requirements
ACTIVITY_MATERIALS = {
    "tableaux": {
        "physical": ["Open floor space (desks pushed back)", "No special props needed"],
        "technology": ["Camera/phone for photos (optional)"],
        "copies": [],
        "prep": ["Clear performance area", "Mark stage area with tape if desired"]
    },
    "character_motivation_chart": {
        "physical": ["Highlighters (optional)"],
        "technology": ["PowerPoint loaded with chart template"],
        "copies": ["Character chart graphic organizer - 1 per student"],
        "prep": ["Pre-distribute graphic organizers at seats"]
    },
    "fishbowl_discussion": {
        "physical": ["Chairs arranged in two circles (inner and outer)"],
        "technology": ["Timer visible", "Discussion questions projected"],
        "copies": ["Discussion notes template - 1 per student"],
        "prep": ["Arrange chairs in fishbowl formation", "Post discussion norms"]
    },
    "monologue_analysis": {
        "physical": ["Highlighters (3 colors per student)"],
        "technology": ["Text of monologue projected", "Video clips if using"],
        "copies": ["Monologue text with wide margins - 1 per student", "Analysis worksheet - 1 per student"],
        "prep": ["Distribute highlighters", "Cue video to exact timestamp"]
    },
    "sonnet_analysis": {
        "physical": ["Colored pencils or highlighters"],
        "technology": ["Sonnet text projected", "Audio of sonnet (optional)"],
        "copies": ["Sonnet worksheet - 1 per student"],
        "prep": ["Print sonnets large enough to annotate"]
    },
    "blocking_exploration": {
        "physical": ["Open floor space", "Tape for marking stage", "Scripts for reference"],
        "technology": ["None required"],
        "copies": ["Scene excerpt - 1 per pair"],
        "prep": ["Clear performance area", "Mark stage areas for groups"]
    },
    "language_analysis": {
        "physical": ["Highlighters or colored pencils"],
        "technology": ["Passage projected", "Document camera if annotating together"],
        "copies": ["Text excerpt with wide margins - 1 per student", "Imagery tracking chart - 1 per student"],
        "prep": ["Pre-highlight key passages for struggling learners"]
    },
    "modern_translation": {
        "physical": ["None special"],
        "technology": ["Original text projected", "No Fear Shakespeare access (optional)"],
        "copies": ["Translation worksheet with original and blank - 1 per student"],
        "prep": ["Distribute worksheets"]
    },
    "scene_performance_prep": {
        "physical": ["Open floor space", "Props if using (minimal)", "Scripts"],
        "technology": ["Timer for rehearsal rotations"],
        "copies": ["Scene scripts - 1 per performer"],
        "prep": ["Assign rehearsal spaces to groups", "Have scripts ready"]
    },
    "conflict_mapping": {
        "physical": ["Large chart paper", "Markers (multiple colors)"],
        "technology": ["Model conflict map projected"],
        "copies": ["Conflict map template - 1 per group"],
        "prep": ["Set up chart paper stations", "Distribute markers"]
    },
    "staged_combat_workshop": {
        "physical": ["Open floor space", "First aid kit accessible", "Foam swords if using props"],
        "technology": ["None required"],
        "copies": ["Safety rules handout - 1 per student", "Choreography sequence - 1 per pair"],
        "prep": ["SAFETY CHECK: Clear all hazards from performance area", "Review safety protocols"]
    },
    "oxymoron_hunt": {
        "physical": ["Highlighters"],
        "technology": ["Text projected", "Timer"],
        "copies": ["Text excerpt - 1 per student", "Oxymoron collection sheet - 1 per student"],
        "prep": ["Distribute highlighters"]
    },
    "hot_seat": {
        "physical": ["One 'hot seat' chair at front of room"],
        "technology": ["Character image projected (optional)"],
        "copies": ["Question bank for audience - 1 per table/group"],
        "prep": ["Position hot seat chair", "Distribute question prompts"]
    },
    "aubade_analysis": {
        "physical": ["Audio recording equipment if recording student readings"],
        "technology": ["Audio of aubade scene", "Text projected"],
        "copies": ["Aubade text with annotation space - 1 per student"],
        "prep": ["Cue audio to correct track"]
    },
    "power_dynamics_map": {
        "physical": ["Chart paper", "Markers"],
        "technology": ["Model power map projected"],
        "copies": ["Power map template - 1 per student or pair"],
        "prep": ["Post chart paper for group maps"]
    },
    "decision_tree": {
        "physical": ["Large paper for tree diagrams"],
        "technology": ["Decision tree model projected"],
        "copies": ["Decision tree template - 1 per student"],
        "prep": ["Draw sample tree structure on board"]
    },
    "fear_inventory": {
        "physical": ["Sticky notes or note cards"],
        "technology": ["Soliloquy text projected"],
        "copies": ["Fear inventory chart - 1 per student"],
        "prep": ["Distribute sticky notes for categorization activity"]
    },
    "monologue_coaching": {
        "physical": ["Open space for movement work", "Mirror (optional)"],
        "technology": ["Timer", "Recording device for playback (optional)"],
        "copies": ["Monologue text - 1 per performer", "Coaching notes sheet - 1 per student"],
        "prep": ["Set up coaching stations", "Assign partners"]
    },
    "fate_vs_choice_debate": {
        "physical": ["Debate position signs (Fate side / Choice side)"],
        "technology": ["Timer for speaking turns", "Debate rules projected"],
        "copies": ["Evidence collection sheet - 1 per student", "Debate scoring rubric - 1 per pair"],
        "prep": ["Divide room into Fate and Choice sides", "Post debate rules"]
    },
    "what_if_scenarios": {
        "physical": ["Chart paper for scenario mapping"],
        "technology": ["Scenario prompts projected"],
        "copies": ["Scenario worksheet - 1 per group"],
        "prep": ["Assign groups to scenarios"]
    },
    "final_moments_staging": {
        "physical": ["Props for death scene (daggers, vials - safe versions)", "Platforms or levels if available"],
        "technology": ["Reference video clips (optional)"],
        "copies": ["Death scene script - 1 per group", "Blocking notation sheet - 1 per director"],
        "prep": ["Set up tomb staging area", "Gather safe props"]
    },
    "theme_synthesis": {
        "physical": ["Chart paper for theme posters"],
        "technology": ["Key quotes projected"],
        "copies": ["Theme tracking sheet - 1 per student", "Quote compilation - 1 per student"],
        "prep": ["Post theme categories around room"]
    },
    "scene_selection": {
        "physical": ["Scene list posted on board"],
        "technology": ["Scene clips for preview (optional)"],
        "copies": ["Scene options list - 1 per group", "Selection criteria rubric - 1 per group"],
        "prep": ["Post scene options", "Have sign-up sheet ready"]
    },
    "rehearsal_workshop": {
        "physical": ["Props for scenes", "Scripts", "Rehearsal space dividers"],
        "technology": ["Timer for rotation"],
        "copies": ["Director notes template - 1 per group", "Line-check sheet - 1 per performer"],
        "prep": ["Assign rehearsal spaces", "Set rotation timer"]
    },
    "peer_feedback": {
        "physical": ["Feedback forms"],
        "technology": ["Feedback guidelines projected"],
        "copies": ["Peer feedback form - 2 per student (one to give, one to receive)"],
        "prep": ["Distribute feedback forms", "Review feedback norms"]
    },
    "performances_talkback": {
        "physical": ["Performance area cleared", "Audience seating arranged"],
        "technology": ["Rubric for assessment", "Recording device (optional)"],
        "copies": ["Audience response sheet - 1 per student", "Performance rubric - 1 per teacher copy"],
        "prep": ["Set up performance area", "Prepare order of performances"]
    },
    "act_review_gallery": {
        "physical": ["Chart paper/poster board", "Markers, colored pencils", "Tape for posting"],
        "technology": ["Act summary slides"],
        "copies": ["Gallery walk response sheet - 1 per student"],
        "prep": ["Set up poster stations around room", "Distribute art supplies"]
    }
}

# Day-to-activity mapping
DAY_ACTIVITIES = {
    1: "tableaux",
    2: "character_motivation_chart",
    3: "fishbowl_discussion",
    4: "monologue_analysis",
    5: "sonnet_analysis",
    6: "blocking_exploration",
    7: "language_analysis",
    8: "modern_translation",
    9: "scene_performance_prep",
    10: "character_motivation_chart",
    11: "conflict_mapping",
    12: "staged_combat_workshop",
    13: "oxymoron_hunt",
    14: "hot_seat",
    15: "aubade_analysis",
    16: "power_dynamics_map",
    17: "decision_tree",
    18: "fear_inventory",
    19: "monologue_coaching",
    20: "act_review_gallery",
    21: "fate_vs_choice_debate",
    22: "what_if_scenarios",
    23: "final_moments_staging",
    24: "theme_synthesis",
    25: "scene_selection",
    26: "rehearsal_workshop",
    27: "peer_feedback",
    28: "rehearsal_workshop",
    29: "performances_talkback",
    30: "performances_talkback"
}

# Standard materials for every day
STANDARD_DAILY_MATERIALS = {
    "technology": [
        "PowerPoint loaded and tested",
        "Projector/screen ready",
        "Timer visible (phone/online/slide)"
    ],
    "copies": [
        "Exit ticket - 1 per student"
    ],
    "before_class": [
        "Warm-up instructions projected",
        "Word wall updated with new terms"
    ],
    "during_class": [
        "Collect exit tickets",
        "Note participation observations"
    ]
}


def generate_materials_checklist(day: int, activity_name: str = None, class_size: int = 32) -> Dict:
    """
    Generate a complete materials checklist for a specific day.

    Args:
        day: Day number (1-30)
        activity_name: Optional activity name override
        class_size: Number of students for copy counts

    Returns:
        Dict containing the complete materials checklist
    """
    activity_key = DAY_ACTIVITIES.get(day, "character_motivation_chart")
    activity_materials = ACTIVITY_MATERIALS.get(activity_key, {})

    checklist = {
        "day": day,
        "header": {
            "title": f"Day {day:02d} Materials Checklist",
            "class_size": class_size,
            "prep_time": "~5 minutes"
        },
        "copies_needed": [],
        "technology": [],
        "physical_materials": [],
        "before_students_arrive": [],
        "during_class_reminders": []
    }

    # Add standard copies
    for copy_item in STANDARD_DAILY_MATERIALS["copies"]:
        checklist["copies_needed"].append({
            "item": copy_item.replace("1 per student", ""),
            "quantity": class_size,
            "per": "student"
        })

    # Add activity-specific copies
    for copy_item in activity_materials.get("copies", []):
        if "per student" in copy_item.lower():
            checklist["copies_needed"].append({
                "item": copy_item.replace(" - 1 per student", ""),
                "quantity": class_size,
                "per": "student"
            })
        elif "per pair" in copy_item.lower():
            checklist["copies_needed"].append({
                "item": copy_item.replace(" - 1 per pair", ""),
                "quantity": class_size // 2,
                "per": "pair"
            })
        elif "per group" in copy_item.lower():
            checklist["copies_needed"].append({
                "item": copy_item.replace(" - 1 per group", ""),
                "quantity": 8,  # Assume ~8 groups
                "per": "group"
            })
        else:
            checklist["copies_needed"].append({
                "item": copy_item,
                "quantity": class_size,
                "per": "student"
            })

    # Add reading guide for reading days (1-25)
    if day <= 25:
        checklist["copies_needed"].append({
            "item": "Reading guide",
            "quantity": class_size,
            "per": "student"
        })

    # Add vocabulary cards for days with new vocabulary
    if day <= 25 and day % 2 == 1:  # Every other day
        checklist["copies_needed"].append({
            "item": "Vocabulary cards (for word wall)",
            "quantity": 1,
            "per": "set"
        })

    # Add technology items
    checklist["technology"] = STANDARD_DAILY_MATERIALS["technology"].copy()
    for tech_item in activity_materials.get("technology", []):
        if tech_item not in checklist["technology"]:
            checklist["technology"].append(tech_item)

    # Add physical materials
    checklist["physical_materials"] = activity_materials.get("physical", []).copy()

    # Add before class items
    checklist["before_students_arrive"] = STANDARD_DAILY_MATERIALS["before_class"].copy()
    for prep_item in activity_materials.get("prep", []):
        checklist["before_students_arrive"].append(prep_item)

    # Add distribution task
    if activity_materials.get("copies"):
        checklist["before_students_arrive"].append("Handouts at stations OR ready to distribute")

    # Add during class items
    checklist["during_class_reminders"] = STANDARD_DAILY_MATERIALS["during_class"].copy()

    # Add day-specific prep for tomorrow
    if day < 30:
        next_activity = DAY_ACTIVITIES.get(day + 1, "")
        next_materials = ACTIVITY_MATERIALS.get(next_activity, {})
        if next_materials.get("copies"):
            checklist["during_class_reminders"].append(f"Prep for tomorrow: Make copies of {next_materials['copies'][0].split(' -')[0]}")

    return checklist


def validate_materials_checklist(checklist: Dict) -> Dict:
    """
    Validate a materials checklist against generation rules.

    Rules:
    - R1: Must be checkable (checkbox format)
    - R2: Must include copy counts
    - R3: Must include technology checks
    - R4: Must include "before students arrive" section

    Returns:
        Dict with validation status and any issues found
    """
    issues = []

    # R2: Check copy counts
    for copy in checklist.get("copies_needed", []):
        if "quantity" not in copy:
            issues.append(f"Missing quantity for: {copy.get('item', 'unknown')}")

    # R3: Check technology section exists
    if not checklist.get("technology"):
        issues.append("Missing technology checklist")

    # R4: Check before class section exists
    if not checklist.get("before_students_arrive"):
        issues.append("Missing 'before students arrive' section")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "checklist": checklist
    }


def generate_materials_checklist_markdown(checklist: Dict) -> str:
    """Generate markdown format of the materials checklist for output."""
    lines = [
        f"# {checklist['header']['title']}",
        f"**Class Size:** {checklist['header']['class_size']} students",
        f"**Prep Time:** {checklist['header']['prep_time']}",
        "",
        "---",
        "",
        "## COPIES NEEDED",
        ""
    ]

    for copy in checklist["copies_needed"]:
        lines.append(f"- [ ] {copy['item']}: **{copy['quantity']}** copies ({copy['per']})")

    lines.extend([
        "",
        "## TECHNOLOGY",
        ""
    ])

    for tech in checklist["technology"]:
        lines.append(f"- [ ] {tech}")

    lines.extend([
        "",
        "## PHYSICAL MATERIALS",
        ""
    ])

    if checklist["physical_materials"]:
        for material in checklist["physical_materials"]:
            lines.append(f"- [ ] {material}")
    else:
        lines.append("- [ ] No special materials needed")

    lines.extend([
        "",
        "## BEFORE STUDENTS ARRIVE",
        ""
    ])

    for prep in checklist["before_students_arrive"]:
        lines.append(f"- [ ] {prep}")

    lines.extend([
        "",
        "## DURING CLASS REMINDERS",
        ""
    ])

    for reminder in checklist["during_class_reminders"]:
        lines.append(f"- [ ] {reminder}")

    return "\n".join(lines)


def generate_all_materials_checklists(class_size: int = 32) -> List[Dict]:
    """Generate materials checklists for all 30 days."""
    checklists = []

    for day in range(1, 31):
        checklist = generate_materials_checklist(day, class_size=class_size)
        validation = validate_materials_checklist(checklist)
        checklist["validation"] = validation
        checklists.append(checklist)

    return checklists


# Export main components
__all__ = [
    'generate_materials_checklist',
    'validate_materials_checklist',
    'generate_materials_checklist_markdown',
    'generate_all_materials_checklists',
    'ACTIVITY_MATERIALS',
    'DAY_ACTIVITIES',
    'STANDARD_DAILY_MATERIALS',
    'MaterialsChecklist'
]
