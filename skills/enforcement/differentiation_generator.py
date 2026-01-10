"""
Differentiation Quick-Sheet Generator - Theater Education Pipeline v2.3

Generates at-a-glance modification guides for diverse learners.
Includes ELL supports, struggling learner scaffolds, advanced extensions, and IEP/504 considerations.

Generated for: Romeo and Juliet (6-week unit)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DifferentiationSheet:
    """Complete differentiation quick-sheet for a day."""
    day: int
    activity_name: str
    ell_supports: Dict
    struggling_learner_supports: Dict
    advanced_extensions: Dict
    iep_504_considerations: Dict

# Activity-specific differentiation templates
DIFFERENTIATION_TEMPLATES = {
    "tableaux": {
        "ell": {
            "vocabulary": ["tableau", "frozen", "level", "focus"],
            "sentence_frames": [
                "My character feels ___ because ___.",
                "I am showing ___ in my body.",
                "This moment is important because ___."
            ],
            "modifications": [
                "Provide visual examples of tableaux before starting",
                "Pair with student who can demonstrate poses",
                "Allow use of native language for planning"
            ]
        },
        "struggling": {
            "scaffolds": [
                "Pre-select character position for student",
                "Provide photo reference of suggested pose",
                "Reduce group size to 2-3 students"
            ],
            "modified_expectations": "Focus on holding still and showing one clear emotion",
            "check_in": "Minute 2: Confirm student has chosen a pose"
        },
        "advanced": {
            "extensions": [
                "Create a series of 3 tableaux showing before, during, after",
                "Add symbolic gestures that reveal theme",
                "Direct peers in positioning for maximum impact"
            ],
            "leadership_role": "Can serve as tableau director for group"
        }
    },
    "character_analysis": {
        "ell": {
            "vocabulary": ["motivation", "desire", "obstacle", "change"],
            "sentence_frames": [
                "The character wants ___.",
                "The evidence that shows this is ___.",
                "This tells us that ___."
            ],
            "modifications": [
                "Provide character chart with visual icons",
                "Allow bullet points instead of complete sentences",
                "Use graphic organizer with pre-filled categories"
            ]
        },
        "struggling": {
            "scaffolds": [
                "Provide partially completed graphic organizer",
                "Focus on only one character instead of multiple",
                "Offer quote bank with relevant evidence"
            ],
            "modified_expectations": "Identify one motivation with one piece of evidence",
            "check_in": "Minute 3: Verify student has identified a quote"
        },
        "advanced": {
            "extensions": [
                "Compare character motivation across two acts",
                "Analyze how secondary characters affect protagonist",
                "Connect character study to psychological archetypes"
            ],
            "leadership_role": "Lead discussion on character connections"
        }
    },
    "discussion": {
        "ell": {
            "vocabulary": ["agree", "disagree", "because", "evidence"],
            "sentence_frames": [
                "I agree with ___ because ___.",
                "The text says ___, which shows ___.",
                "I have a different idea: ___."
            ],
            "modifications": [
                "Pre-teach discussion questions 5 minutes early",
                "Allow partner consultation before sharing",
                "Accept shorter responses with key vocabulary"
            ]
        },
        "struggling": {
            "scaffolds": [
                "Provide discussion question in advance",
                "Assign specific page to reference during discussion",
                "Pair with supportive peer"
            ],
            "modified_expectations": "Contribute one comment using evidence",
            "check_in": "Minute 5: Prompt participation if silent"
        },
        "advanced": {
            "extensions": [
                "Prepare counter-argument to anticipated positions",
                "Connect discussion to outside texts or current events",
                "Track and synthesize multiple perspectives during discussion"
            ],
            "leadership_role": "Discussion facilitator or summarizer"
        }
    },
    "language_analysis": {
        "ell": {
            "vocabulary": ["metaphor", "imagery", "effect", "meaning"],
            "sentence_frames": [
                "Shakespeare compares ___ to ___.",
                "This creates a feeling of ___.",
                "The image suggests ___."
            ],
            "modifications": [
                "Provide modern translation alongside original",
                "Highlight literary devices in different colors",
                "Use visual diagram showing metaphor connections"
            ]
        },
        "struggling": {
            "scaffolds": [
                "Reduce passage length - focus on 5 lines only",
                "Provide template: 'Shakespeare compares [X] to [Y]'",
                "Use highlighters to mark specific devices"
            ],
            "modified_expectations": "Identify and explain one literary device",
            "check_in": "Minute 3: Help locate first metaphor if needed"
        },
        "advanced": {
            "extensions": [
                "Track recurring imagery across multiple scenes",
                "Compare Shakespeare's techniques to modern poetry",
                "Analyze how imagery connects to themes"
            ],
            "leadership_role": "Present findings to class"
        }
    },
    "performance": {
        "ell": {
            "vocabulary": ["blocking", "projection", "emotion", "gesture"],
            "sentence_frames": [
                "My character moves to ___ because ___.",
                "I am showing ___ through my voice.",
                "The audience should feel ___."
            ],
            "modifications": [
                "Allow modified text length",
                "Provide gesture suggestions",
                "Accept performance in home language first, then English"
            ]
        },
        "struggling": {
            "scaffolds": [
                "Reduce speaking lines - focus on physicality",
                "Provide line-by-line coaching before performance",
                "Allow use of script during performance"
            ],
            "modified_expectations": "Maintain character through scene with teacher support",
            "check_in": "Minute 5: Run through opening lines together"
        },
        "advanced": {
            "extensions": [
                "Add subtext notes to script",
                "Experiment with non-traditional interpretations",
                "Direct peers in blocking choices"
            ],
            "leadership_role": "Scene director or peer coach"
        }
    },
    "writing": {
        "ell": {
            "vocabulary": ["claim", "evidence", "explain", "connect"],
            "sentence_frames": [
                "The text shows ___ when it says ___.",
                "This is important because ___.",
                "Another example of this is ___."
            ],
            "modifications": [
                "Provide sentence starters for each paragraph",
                "Allow bullet points for brainstorming",
                "Accept shorter responses with accurate content"
            ]
        },
        "struggling": {
            "scaffolds": [
                "Provide paragraph frame with blanks",
                "Offer quote bank with relevant evidence",
                "Allow oral response recorded as alternative"
            ],
            "modified_expectations": "One claim with one piece of evidence, explained",
            "check_in": "Minute 3: Verify claim is stated"
        },
        "advanced": {
            "extensions": [
                "Incorporate secondary sources in analysis",
                "Write in multiple genres (essay, letter, review)",
                "Analyze counterarguments"
            ],
            "leadership_role": "Peer editor for classmates"
        }
    },
    "reading": {
        "ell": {
            "vocabulary": ["context", "inference", "evidence", "interpret"],
            "sentence_frames": [
                "I notice that ___.",
                "This reminds me of ___.",
                "I think this means ___ because ___."
            ],
            "modifications": [
                "Pair with fluent reader for partner reading",
                "Provide modern translation side-by-side",
                "Allow audio recording of text"
            ]
        },
        "struggling": {
            "scaffolds": [
                "Pre-highlight key passages",
                "Reduce text to essential lines only",
                "Provide guided annotation template"
            ],
            "modified_expectations": "Annotate 3 key moments with teacher support",
            "check_in": "Minute 3: Check comprehension of first section"
        },
        "advanced": {
            "extensions": [
                "Compare multiple editions or translations",
                "Research historical/performance context",
                "Lead discussion of challenging passages"
            ],
            "leadership_role": "Reading leader or discussion facilitator"
        }
    }
}

# Day-specific activity mappings
DAY_ACTIVITY_TYPES = {
    1: "tableaux",
    2: "character_analysis",
    3: "discussion",
    4: "language_analysis",
    5: "language_analysis",
    6: "performance",
    7: "language_analysis",
    8: "writing",
    9: "performance",
    10: "character_analysis",
    11: "character_analysis",
    12: "performance",
    13: "language_analysis",
    14: "discussion",
    15: "language_analysis",
    16: "character_analysis",
    17: "character_analysis",
    18: "language_analysis",
    19: "performance",
    20: "writing",
    21: "discussion",
    22: "character_analysis",
    23: "performance",
    24: "language_analysis",
    25: "discussion"
}

# Day-specific vocabulary additions
DAY_VOCABULARY = {
    1: ["prologue", "feud", "brawl", "Montague", "Capulet"],
    2: ["melancholy", "oxymoron", "unrequited", "infatuation"],
    3: ["Nurse", "Paris", "suitor", "woo"],
    4: ["Queen Mab", "soliloquy", "imagery", "verse"],
    5: ["sonnet", "pilgrim", "shrine", "holy"],
    6: ["blocking", "staging", "subtext", "beat"],
    7: ["metaphor", "celestial", "envious", "balcony"],
    8: ["wherefore", "deny", "refuse", "rose"],
    9: ["performance", "delivery", "pacing", "projection"],
    10: ["Friar", "alliance", "herbs", "marriage"],
    11: ["tension", "escalation", "provoke", "fray"],
    12: ["climax", "turning point", "curse", "plague"],
    13: ["banishment", "exile", "oxymoron", "fiend"],
    14: ["despair", "advice", "philosophy", "comfort"],
    15: ["aubade", "lark", "nightingale", "dawn"],
    16: ["ultimatum", "disobedient", "disown", "betrayal"],
    17: ["vial", "potion", "tomb", "desperate"],
    18: ["soliloquy", "fear", "vault", "ghost"],
    19: ["beat", "build", "climax", "objective"],
    20: ["irony", "dramatic", "mourning", "grief"],
    21: ["Mantua", "apothecary", "poison", "fate"],
    22: ["quarantine", "letter", "tomb", "timing"],
    23: ["tragedy", "death", "sacrifice", "end"],
    24: ["resolution", "reconcile", "statue", "peace"],
    25: ["theme", "synthesis", "arc", "performance"]
}


def generate_differentiation_sheet(day: int, activity_name: str) -> Dict:
    """
    Generate a complete differentiation quick-sheet for a specific day.

    Args:
        day: Day number (1-30)
        activity_name: Name of the day's main activity

    Returns:
        Dict containing the complete differentiation quick-sheet
    """
    activity_type = DAY_ACTIVITY_TYPES.get(day, "character_analysis")
    template = DIFFERENTIATION_TEMPLATES.get(activity_type, DIFFERENTIATION_TEMPLATES["character_analysis"])

    # Get day-specific vocabulary
    day_vocab = DAY_VOCABULARY.get(day, [])

    sheet = {
        "day": day,
        "header": {
            "title": f"Day {day:02d} Differentiation Guide",
            "activity": activity_name
        },
        "ell_supports": {
            "vocabulary": {
                "pre_teach": day_vocab[:3] + template["ell"]["vocabulary"][:2],
                "translations_note": "Provide translations in student's home language if available"
            },
            "sentence_frames": template["ell"]["sentence_frames"],
            "reading_modifications": [
                "Pair with fluent reader",
                "Provide modern translation side-by-side",
                "Allow audio recording of text"
            ],
            "activity_modifications": template["ell"]["modifications"],
            "extended_time": "+5 minutes for activity"
        },
        "struggling_learner_supports": {
            "scaffolds": [
                "Graphic organizer provided",
                f"Reduced text passage (focus on key lines only)",
                f"Teacher check-in at {template['struggling']['check_in']}"
            ] + template["struggling"]["scaffolds"],
            "modified_expectations": template["struggling"]["modified_expectations"],
            "focus": "Focus on primary objective only",
            "support_note": "Seat near teacher for easy check-ins"
        },
        "advanced_learner_extensions": {
            "extensions": template["advanced"]["extensions"],
            "leadership_role": template["advanced"]["leadership_role"],
            "research_connection": f"Connect today's content to historical context of Elizabethan theater",
            "peer_support": "May be paired with struggling learner as peer tutor"
        },
        "iep_504_considerations": {
            "common_accommodations": [
                "Extended time: Add 5 minutes to activity",
                "Preferential seating: Near board/teacher",
                "Reduced written output: Oral response option",
                "Movement breaks: Built into warm-up",
                "Chunked instructions: One step at a time"
            ],
            "check_individual_ieps": [
                "Specific reading accommodations",
                "Assessment modifications",
                "Behavioral supports",
                "Technology needs"
            ],
            "note": "Review individual IEP/504 plans for student-specific requirements"
        }
    }

    return sheet


def validate_differentiation_sheet(sheet: Dict) -> Dict:
    """
    Validate a differentiation sheet against generation rules.

    Rules:
    - R1: Must include specific modifications for today's activity
    - R2: Sentence frames must relate to day's objective
    - R3: Extension must be genuinely challenging (not just "more")
    - R4: Must be scannable (bullet points, not paragraphs)
    - R5: Must fit on one page

    Returns:
        Dict with validation status and any issues found
    """
    issues = []

    # R1: Check activity modifications exist
    if not sheet.get("ell_supports", {}).get("activity_modifications"):
        issues.append("Missing ELL activity modifications")

    if not sheet.get("struggling_learner_supports", {}).get("scaffolds"):
        issues.append("Missing struggling learner scaffolds")

    # R2: Check sentence frames exist
    if len(sheet.get("ell_supports", {}).get("sentence_frames", [])) < 2:
        issues.append("Need at least 2 sentence frames")

    # R3: Check extension quality
    extensions = sheet.get("advanced_learner_extensions", {}).get("extensions", [])
    if len(extensions) < 2:
        issues.append("Need at least 2 extension activities")

    # Check for generic "more" extensions
    for ext in extensions:
        if "more" in ext.lower() and "compare" not in ext.lower() and "analyze" not in ext.lower():
            issues.append(f"Extension may be just 'more work': {ext}")

    # R4: Check format (should be lists, not paragraphs)
    # This is structural - verified by format

    # R5: Estimate page length
    total_items = (
        len(sheet.get("ell_supports", {}).get("vocabulary", {}).get("pre_teach", [])) +
        len(sheet.get("ell_supports", {}).get("sentence_frames", [])) +
        len(sheet.get("struggling_learner_supports", {}).get("scaffolds", [])) +
        len(sheet.get("advanced_learner_extensions", {}).get("extensions", []))
    )
    if total_items > 25:
        issues.append("Sheet may exceed one page - consider condensing")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "sheet": sheet
    }


def generate_differentiation_markdown(sheet: Dict) -> str:
    """Generate markdown format of the differentiation sheet for output."""
    lines = [
        f"# {sheet['header']['title']}",
        f"**Activity:** {sheet['header']['activity']}",
        "",
        "---",
        "",
        "## ELL SUPPORTS",
        "",
        "**Vocabulary to Pre-teach:**"
    ]

    for term in sheet["ell_supports"]["vocabulary"]["pre_teach"]:
        lines.append(f"- {term}")

    lines.extend([
        "",
        "**Sentence Frames:**"
    ])

    for frame in sheet["ell_supports"]["sentence_frames"]:
        lines.append(f"- \"{frame}\"")

    lines.extend([
        "",
        "**Reading Modifications:**"
    ])

    for mod in sheet["ell_supports"]["reading_modifications"]:
        lines.append(f"- {mod}")

    lines.extend([
        "",
        "**Activity Modifications:**"
    ])

    for mod in sheet["ell_supports"]["activity_modifications"]:
        lines.append(f"- {mod}")

    lines.extend([
        "",
        f"**Extended Time:** {sheet['ell_supports']['extended_time']}",
        "",
        "---",
        "",
        "## STRUGGLING LEARNERS",
        "",
        "**Scaffolds:**"
    ])

    for scaffold in sheet["struggling_learner_supports"]["scaffolds"]:
        lines.append(f"- {scaffold}")

    lines.extend([
        "",
        f"**Modified Expectations:** {sheet['struggling_learner_supports']['modified_expectations']}",
        "",
        f"**Focus:** {sheet['struggling_learner_supports']['focus']}",
        "",
        "---",
        "",
        "## ADVANCED LEARNERS",
        "",
        "**Extensions:**"
    ])

    for ext in sheet["advanced_learner_extensions"]["extensions"]:
        lines.append(f"- {ext}")

    lines.extend([
        "",
        f"**Leadership Role:** {sheet['advanced_learner_extensions']['leadership_role']}",
        "",
        f"**Research Connection:** {sheet['advanced_learner_extensions']['research_connection']}",
        "",
        "---",
        "",
        "## IEP/504 CONSIDERATIONS",
        "",
        "**Common Accommodations:**"
    ])

    for acc in sheet["iep_504_considerations"]["common_accommodations"]:
        lines.append(f"- {acc}")

    lines.extend([
        "",
        "**Check with individual IEPs for:**"
    ])

    for check in sheet["iep_504_considerations"]["check_individual_ieps"]:
        lines.append(f"- {check}")

    lines.extend([
        "",
        f"_{sheet['iep_504_considerations']['note']}_"
    ])

    return "\n".join(lines)


def generate_all_differentiation_sheets() -> List[Dict]:
    """Generate differentiation sheets for all 30 days."""
    from .instruction_integrator import ROMEO_AND_JULIET_STRUCTURE

    sheets = []

    for day_num in range(1, 31):
        day_key = f"day_{day_num}"
        if day_key in ROMEO_AND_JULIET_STRUCTURE:
            day_info = ROMEO_AND_JULIET_STRUCTURE[day_key]
            activity = day_info.get("activity", "Activity")
            activity_name = activity.split("→")[0].strip() if "→" in activity else activity

            sheet = generate_differentiation_sheet(
                day=day_num,
                activity_name=activity_name
            )
            validation = validate_differentiation_sheet(sheet)
            sheet["validation"] = validation
            sheets.append(sheet)

    return sheets


# Export main components
__all__ = [
    'generate_differentiation_sheet',
    'validate_differentiation_sheet',
    'generate_differentiation_markdown',
    'generate_all_differentiation_sheets',
    'DIFFERENTIATION_TEMPLATES',
    'DAY_ACTIVITY_TYPES',
    'DAY_VOCABULARY',
    'DifferentiationSheet'
]
