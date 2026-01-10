"""
Unit-Level Component Generators - Theater Education Pipeline v2.3

Generates unit-wide components that are created once per unit:
- Unit Overview Calendar
- Substitute Folder
- Parent Letter
- Character Tracking Sheet
- Standards Alignment Document
- Assessment Tracker Template

Generated for: Romeo and Juliet (6-week unit)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

# ============================================================================
# UNIT CALENDAR GENERATOR
# ============================================================================

ROMEO_JULIET_CALENDAR = {
    "week_1": {
        "title": "Week 1: Act 1",
        "days": [
            {"day": 1, "focus": "Prologue + 1.1", "activity": "Tableaux", "assessment": False},
            {"day": 2, "focus": "1.1 (Romeo)", "activity": "Character Chart", "assessment": False},
            {"day": 3, "focus": "1.2-1.3", "activity": "Fishbowl", "assessment": False},
            {"day": 4, "focus": "1.4 (Mab)", "activity": "Monologue Analysis", "assessment": False},
            {"day": 5, "focus": "1.5 (Ball)", "activity": "Sonnet Analysis", "assessment": True}
        ]
    },
    "week_2": {
        "title": "Week 2: Acts 1-2",
        "days": [
            {"day": 6, "focus": "1.5 (cont)", "activity": "Blocking", "assessment": False},
            {"day": 7, "focus": "2.2 Part 1", "activity": "Language Analysis", "assessment": False},
            {"day": 8, "focus": "2.2 Part 2", "activity": "Modern Translation", "assessment": False},
            {"day": 9, "focus": "2.2 Part 3", "activity": "Scene Prep", "assessment": True},
            {"day": 10, "focus": "2.3, 2.6", "activity": "Character Analysis", "assessment": False}
        ]
    },
    "week_3": {
        "title": "Week 3: Act 3",
        "days": [
            {"day": 11, "focus": "3.1 Part 1", "activity": "Conflict Mapping", "assessment": False},
            {"day": 12, "focus": "3.1 Part 2", "activity": "Stage Combat", "assessment": False},
            {"day": 13, "focus": "3.1-3.2", "activity": "Oxymoron Hunt", "assessment": False},
            {"day": 14, "focus": "3.3-3.4", "activity": "Hot Seat", "assessment": True},
            {"day": 15, "focus": "3.5 Part 1", "activity": "Aubade Analysis", "assessment": False}
        ]
    },
    "week_4": {
        "title": "Week 4: Acts 3-4",
        "days": [
            {"day": 16, "focus": "3.5 Part 2", "activity": "Power Map", "assessment": False},
            {"day": 17, "focus": "4.1", "activity": "Decision Tree", "assessment": False},
            {"day": 18, "focus": "4.3 Part 1", "activity": "Fear Inventory", "assessment": False},
            {"day": 19, "focus": "4.3 Part 2", "activity": "Monologue Coach", "assessment": True},
            {"day": 20, "focus": "4.5 + Review", "activity": "Gallery Walk", "assessment": False}
        ]
    },
    "week_5": {
        "title": "Week 5: Act 5",
        "days": [
            {"day": 21, "focus": "5.1", "activity": "Fate vs Choice", "assessment": False},
            {"day": 22, "focus": "5.2-5.3", "activity": "What If", "assessment": False},
            {"day": 23, "focus": "5.3 Deaths", "activity": "Final Staging", "assessment": False},
            {"day": 24, "focus": "5.3 End", "activity": "Theme Synthesis", "assessment": True},
            {"day": 25, "focus": "Full Review", "activity": "Scene Selection", "assessment": False}
        ]
    },
    "week_6": {
        "title": "Week 6: Performance",
        "days": [
            {"day": 26, "focus": "Rehearsal", "activity": "Workshop", "assessment": False},
            {"day": 27, "focus": "Rehearsal", "activity": "Peer Feedback", "assessment": False},
            {"day": 28, "focus": "Dress", "activity": "Run-Through", "assessment": False},
            {"day": 29, "focus": "Perform", "activity": "Day 1 Shows", "assessment": True},
            {"day": 30, "focus": "Perform", "activity": "Day 2 + Reflect", "assessment": True}
        ]
    }
}


def generate_unit_calendar(unit_name: str = "Romeo and Juliet", start_date: str = None) -> Dict:
    """Generate complete unit overview calendar."""
    calendar = {
        "header": {
            "title": f"Unit Calendar: {unit_name}",
            "duration": "6 weeks (30 days)",
            "essential_question": "How do love and fate collide to create tragedy?"
        },
        "weeks": [],
        "key": {
            "icons": {
                "📖": "Reading focus",
                "🎭": "Performance activity",
                "✏️": "Writing/Analysis",
                "💬": "Discussion",
                "⭐": "Graded assessment"
            },
            "color_coding": {
                "Act 1": "Blue",
                "Act 2": "Green",
                "Act 3": "Yellow",
                "Act 4": "Orange",
                "Act 5": "Red",
                "Performance": "Purple"
            }
        },
        "standards_summary": [
            "RL.9-10.3 - Character development",
            "RL.9-10.4 - Figurative language",
            "RL.9-10.5 - Text structure",
            "SL.9-10.1 - Collaborative discussion",
            "SL.9-10.6 - Formal presentation"
        ]
    }

    for week_key, week_data in ROMEO_JULIET_CALENDAR.items():
        week = {
            "title": week_data["title"],
            "days": []
        }
        for day in week_data["days"]:
            week["days"].append({
                "day_number": day["day"],
                "focus": day["focus"],
                "activity": day["activity"],
                "assessed": "⭐" if day["assessment"] else ""
            })
        calendar["weeks"].append(week)

    return calendar


# ============================================================================
# SUBSTITUTE FOLDER GENERATOR
# ============================================================================

SUB_FOLDER_TEMPLATE = {
    "classroom_info": {
        "seating_chart_location": "In sub folder on desk OR posted on wall",
        "emergency_contacts": "Main office: ext. 100, Dept. chair: ext. 205",
        "materials_location": "Copies in labeled drawer, projection computer logged in",
        "class_procedures": [
            "Students enter quietly and begin warm-up on screen",
            "No food/drink except water",
            "Raise hand to speak",
            "Pack up when teacher gives signal, not when bell rings"
        ]
    },
    "generic_activities": {
        "option_a_film": {
            "title": "Film Study (any day)",
            "instructions": [
                "Show: Romeo + Juliet (1996 Luhrmann) OR Romeo and Juliet (1968 Zeffirelli)",
                "Available on: [Teacher to fill in streaming/DVD location]",
                "Play from beginning of class period, pause with 10 min remaining",
                "Students complete Film Comparison Chart (copies in sub folder)",
                "Collect charts at end of period"
            ],
            "handout_included": True
        },
        "option_b_reading": {
            "title": "Silent Reading + Response",
            "instructions": [
                "Students read assigned scene independently",
                "Scene should be written on board: [Teacher fills in backup scene]",
                "Complete Reading Response Questions handout",
                "Partner discussion for last 10 minutes",
                "Collect responses at end of period"
            ],
            "handout_included": True
        },
        "option_c_vocabulary": {
            "title": "Vocabulary Review",
            "instructions": [
                "Distribute vocabulary review packet (in sub folder)",
                "Students work individually for 20 minutes",
                "Then pair up and quiz each other for 15 minutes",
                "Self-check with answer key for final 10 minutes",
                "Collect completed packets"
            ],
            "handout_included": True
        },
        "option_d_journal": {
            "title": "Character Journal",
            "instructions": [
                "Students write a diary entry from their assigned character's perspective",
                "Characters assigned: Romeo, Juliet, Mercutio, Nurse, Friar Lawrence",
                "Entry should be 1 full page minimum",
                "Share with partner in final 10 minutes",
                "Collect journals at end"
            ],
            "handout_included": True
        }
    },
    "safety_notes": {
        "prohibited_activities": [
            "NO stage combat without trained teacher present",
            "NO full performances without supervision",
            "NO scene work requiring physical contact",
            "NO moving furniture"
        ],
        "if_questions_arise": "Students know the procedures - ask a reliable student if unsure"
    }
}


def generate_sub_folder(unit_name: str = "Romeo and Juliet") -> Dict:
    """Generate complete substitute folder."""
    sub_folder = {
        "header": {
            "title": f"Substitute Folder: {unit_name}",
            "teacher_name": "[Teacher Name]",
            "room_number": "[Room Number]",
            "date_created": datetime.now().strftime("%Y-%m-%d")
        },
        "classroom_info": SUB_FOLDER_TEMPLATE["classroom_info"],
        "generic_activities": SUB_FOLDER_TEMPLATE["generic_activities"],
        "day_specific_plans": {},
        "safety_notes": SUB_FOLDER_TEMPLATE["safety_notes"]
    }

    # Add quick reference for each day
    for week_key, week_data in ROMEO_JULIET_CALENDAR.items():
        for day in week_data["days"]:
            sub_folder["day_specific_plans"][f"Day {day['day']}"] = {
                "focus": day["focus"],
                "if_sub_knows_day": f"Run Option A (film) for comparison to {day['focus']}",
                "collect": "Exit ticket if available"
            }

    return sub_folder


# ============================================================================
# PARENT LETTER GENERATOR
# ============================================================================

def generate_parent_letter(unit_name: str = "Romeo and Juliet", teacher_name: str = "[Teacher Name]") -> Dict:
    """Generate parent communication letter."""
    parent_letter = {
        "header": {
            "date": "[Date]",
            "school_name": "[School Name]",
            "teacher_name": teacher_name,
            "contact_email": "[teacher@school.edu]"
        },
        "greeting": "Dear Families,",
        "unit_overview": {
            "what": f"Your student is beginning our {unit_name} unit in English class.",
            "why": "This classic play develops critical reading skills, literary analysis abilities, and performance techniques while exploring timeless themes of love, family, and fate.",
            "timeline": "6 weeks total - 5 weeks of instruction and 1 week of performances"
        },
        "content_advisory": {
            "intro": "This unit includes content that may prompt discussion at home:",
            "topics": [
                "Stage combat (choreographed and safely supervised)",
                "Themes of death and suicide (addressed contextually with care)",
                "Romantic content (age-appropriate, focused on language and theme)",
                "Archaic language requiring translation and analysis"
            ]
        },
        "home_support": {
            "intro": "Ways you can support your student:",
            "suggestions": [
                "Watch a film adaptation together (1996 or 1968 versions recommended)",
                "Ask about daily journal prompts and discussion topics",
                "Practice lines if your student brings script home",
                "Discuss how themes connect to modern life"
            ]
        },
        "key_dates": {
            "performance_week": "[Week 6 dates]",
            "major_assessments": "Exit tickets daily, rubric-scored activities weekly, final performance"
        },
        "closing": {
            "questions": "Please don't hesitate to reach out with any questions or concerns.",
            "signature": f"Sincerely,\n{teacher_name}"
        }
    }

    return parent_letter


# ============================================================================
# CHARACTER TRACKER GENERATOR
# ============================================================================

CHARACTERS = [
    {"name": "Romeo", "house": "Montague", "role": "Protagonist"},
    {"name": "Juliet", "house": "Capulet", "role": "Protagonist"},
    {"name": "Mercutio", "house": "Neutral (Romeo's friend)", "role": "Catalyst"},
    {"name": "Tybalt", "house": "Capulet", "role": "Antagonist"},
    {"name": "Nurse", "house": "Capulet servant", "role": "Confidante"},
    {"name": "Friar Lawrence", "house": "Neutral", "role": "Mentor"},
    {"name": "Lord Capulet", "house": "Capulet", "role": "Authority"},
    {"name": "Lady Capulet", "house": "Capulet", "role": "Authority"},
    {"name": "Benvolio", "house": "Montague", "role": "Peacemaker"},
    {"name": "Paris", "house": "Neutral (Suitor)", "role": "Rival"}
]


def generate_character_tracker() -> Dict:
    """Generate student character tracking sheet."""
    tracker = {
        "header": {
            "title": "Romeo and Juliet Character Tracker",
            "student_name": "Name: _______________",
            "instructions": "Update this tracker as you read each act. Track how characters change throughout the play."
        },
        "character_grid": [],
        "relationship_map_template": {
            "instructions": "Draw lines between characters to show relationships. Use different colors for love, hate, family, friendship.",
            "starter_connections": [
                "Romeo ←love→ Juliet",
                "Montague ←feud→ Capulet",
                "Juliet ←nurse→ Nurse"
            ]
        },
        "final_reflection": {
            "questions": [
                "Which character changed the most over the course of the play? Explain with evidence.",
                "Which character do you sympathize with the most? Why?",
                "Which character made the worst decision? What should they have done instead?"
            ]
        }
    }

    for char in CHARACTERS:
        tracker["character_grid"].append({
            "character": char["name"],
            "house": char["house"],
            "role": char["role"],
            "acts": {
                "act_1": {"motivation": "", "key_quote": "", "relationship_changes": ""},
                "act_2": {"motivation": "", "key_quote": "", "relationship_changes": ""},
                "act_3": {"motivation": "", "key_quote": "", "relationship_changes": ""},
                "act_4": {"motivation": "", "key_quote": "", "relationship_changes": ""},
                "act_5": {"motivation": "", "key_quote": "", "relationship_changes": ""}
            }
        })

    return tracker


# ============================================================================
# STANDARDS ALIGNMENT GENERATOR
# ============================================================================

STANDARDS_ALIGNMENT = {
    "reading_literature": {
        "RL.9-10.1": {
            "standard": "Cite strong textual evidence to support analysis",
            "days": [2, 7, 8, 13, 18, 24],
            "activities": ["Character Chart", "Language Analysis", "Fear Inventory"],
            "assessments": ["Exit tickets", "Reading guides", "Annotations"]
        },
        "RL.9-10.2": {
            "standard": "Determine theme and analyze development",
            "days": [1, 5, 15, 21, 24],
            "activities": ["Prologue analysis", "Aubade Analysis", "Theme Synthesis"],
            "assessments": ["Exit tickets", "Final reflection"]
        },
        "RL.9-10.3": {
            "standard": "Analyze complex characters",
            "days": [2, 3, 10, 14, 16, 17],
            "activities": ["Character Chart", "Fishbowl", "Hot Seat", "Power Map"],
            "assessments": ["Character Tracker", "Rubric-scored activities"]
        },
        "RL.9-10.4": {
            "standard": "Determine meaning of words and phrases; analyze figurative language",
            "days": [4, 7, 8, 13, 15],
            "activities": ["Monologue Analysis", "Language Analysis", "Oxymoron Hunt"],
            "assessments": ["Vocabulary checks", "Exit tickets"]
        },
        "RL.9-10.5": {
            "standard": "Analyze structure and how parts relate to whole",
            "days": [1, 5, 24, 25],
            "activities": ["Sonnet Analysis", "Theme Synthesis", "Review"],
            "assessments": ["Exit tickets", "Final reflection"]
        }
    },
    "speaking_listening": {
        "SL.9-10.1": {
            "standard": "Collaborative discussions",
            "days": [3, 14, 21, 27],
            "activities": ["Fishbowl", "Hot Seat", "Fate Debate", "Peer Feedback"],
            "assessments": ["Discussion rubrics", "Participation notes"]
        },
        "SL.9-10.4": {
            "standard": "Present information clearly",
            "days": [20, 25, 29, 30],
            "activities": ["Gallery Walk", "Scene Selection", "Final Performances"],
            "assessments": ["Presentation rubrics"]
        },
        "SL.9-10.6": {
            "standard": "Adapt speech to context",
            "days": [6, 9, 19, 23, 29, 30],
            "activities": ["Blocking", "Scene Prep", "Monologue Coach", "Final Performances"],
            "assessments": ["Performance rubrics"]
        }
    },
    "writing": {
        "W.9-10.1": {
            "standard": "Write arguments with claims and evidence",
            "days": [21, 22],
            "activities": ["Fate vs Choice Debate", "What If Scenarios"],
            "assessments": ["Argument rubrics"]
        },
        "W.9-10.9": {
            "standard": "Draw evidence from texts",
            "days": [2, 7, 8, 13, 18],
            "activities": ["Character Chart", "Language Analysis", "Translation"],
            "assessments": ["Exit tickets", "Written responses"]
        }
    }
}


def generate_standards_alignment(unit_name: str = "Romeo and Juliet") -> Dict:
    """Generate standards alignment documentation."""
    alignment = {
        "header": {
            "title": f"Standards Alignment: {unit_name}",
            "grade_level": "9-10",
            "subject": "English Language Arts",
            "framework": "California Common Core State Standards"
        },
        "standards": STANDARDS_ALIGNMENT,
        "coverage_summary": [],
        "assessment_map": []
    }

    # Generate coverage summary
    for category, standards in STANDARDS_ALIGNMENT.items():
        for code, data in standards.items():
            alignment["coverage_summary"].append({
                "standard": code,
                "days_addressed": len(data["days"]),
                "primary_days": data["days"][:2],
                "secondary_days": data["days"][2:] if len(data["days"]) > 2 else []
            })

    # Generate assessment map
    alignment["assessment_map"] = [
        {"type": "Exit Tickets", "standards": ["RL.1", "RL.2", "RL.3", "RL.4"], "frequency": "Daily"},
        {"type": "Rubric Activities", "standards": ["RL.3", "SL.1", "SL.6"], "frequency": "Weekly"},
        {"type": "Character Tracker", "standards": ["RL.3", "W.9"], "frequency": "Ongoing"},
        {"type": "Final Performance", "standards": ["SL.4", "SL.6"], "frequency": "End of unit"}
    ]

    return alignment


# ============================================================================
# ASSESSMENT TRACKER GENERATOR
# ============================================================================

def generate_assessment_tracker(class_size: int = 32) -> Dict:
    """Generate gradebook template."""
    tracker = {
        "header": {
            "title": "Romeo and Juliet Assessment Tracker",
            "total_points_possible": 300,
            "grade_scale": {
                "A": "90-100%",
                "B": "80-89%",
                "C": "70-79%",
                "D": "60-69%",
                "F": "Below 60%"
            }
        },
        "columns": {
            "exit_tickets": {
                "count": 25,
                "points_each": 4,
                "total": 100
            },
            "rubric_activities": {
                "items": ["Sonnet (Day 5)", "Scene Prep (Day 9)", "Hot Seat (Day 14)",
                        "Monologue (Day 19)", "Theme (Day 24)"],
                "points_each": 12,
                "total": 60
            },
            "character_tracker": {
                "count": 1,
                "points": 40,
                "total": 40
            },
            "final_performance": {
                "count": 1,
                "points": 100,
                "total": 100
            }
        },
        "objective_mastery": [
            "Obj 1: Analyze character development",
            "Obj 2: Interpret figurative language",
            "Obj 3: Apply performance techniques",
            "Obj 4: Evaluate themes",
            "Obj 5: Create original interpretation"
        ],
        "student_rows": class_size,
        "formulas": {
            "unit_total": "=SUM(B:N)",
            "percentage": "=O2/300*100",
            "class_average": "=AVERAGE(O2:O33)"
        }
    }

    return tracker


# ============================================================================
# MASTER GENERATOR
# ============================================================================

def generate_all_unit_components(unit_name: str = "Romeo and Juliet", class_size: int = 32) -> Dict:
    """Generate all unit-level components at once."""
    return {
        "calendar": generate_unit_calendar(unit_name),
        "sub_folder": generate_sub_folder(unit_name),
        "parent_letter": generate_parent_letter(unit_name),
        "character_tracker": generate_character_tracker(),
        "standards_alignment": generate_standards_alignment(unit_name),
        "assessment_tracker": generate_assessment_tracker(class_size)
    }


def generate_unit_calendar_markdown(calendar: Dict) -> str:
    """Generate markdown format of unit calendar."""
    lines = [
        f"# {calendar['header']['title']}",
        f"**Duration:** {calendar['header']['duration']}",
        f"**Essential Question:** {calendar['header']['essential_question']}",
        "",
        "---",
        ""
    ]

    for week in calendar["weeks"]:
        lines.append(f"## {week['title']}")
        lines.append("")
        lines.append("| Day | Focus | Activity | ⭐ |")
        lines.append("|-----|-------|----------|---|")
        for day in week["days"]:
            lines.append(f"| {day['day_number']} | {day['focus']} | {day['activity']} | {day['assessed']} |")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Key",
        ""
    ])

    for icon, meaning in calendar["key"]["icons"].items():
        lines.append(f"- {icon} {meaning}")

    return "\n".join(lines)


# Export main components
__all__ = [
    'generate_unit_calendar',
    'generate_sub_folder',
    'generate_parent_letter',
    'generate_character_tracker',
    'generate_standards_alignment',
    'generate_assessment_tracker',
    'generate_all_unit_components',
    'generate_unit_calendar_markdown',
    'ROMEO_JULIET_CALENDAR',
    'CHARACTERS',
    'STANDARDS_ALIGNMENT'
]
