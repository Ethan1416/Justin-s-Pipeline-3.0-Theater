"""
Answer Key Generator - Theater Education Pipeline v2.3

Generates answer keys for exit tickets and handouts.
Includes exemplar responses, acceptable variations, and common misconceptions.

Generated for: Romeo and Juliet (6-week unit)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class AnswerKeyEntry:
    """Single answer key entry for a question."""
    question: str
    correct_answer: str
    acceptable_variations: List[str]
    common_misconceptions: List[str]
    partial_credit_guidance: str

# Complete exit ticket answer database for Romeo and Juliet
EXIT_TICKET_ANSWERS = {
    1: {  # Day 1: Prologue + 1.1
        "questions": [
            {
                "question": "What does 'star-crossed' mean in the prologue?",
                "correct_answer": "'Star-crossed' means the lovers' fate is doomed by the stars/destiny. They are destined for tragedy because fate is against them.",
                "acceptable_variations": [
                    "Doomed by fate",
                    "Their stars/destinies are crossed/opposed",
                    "Fate is working against their love",
                    "Bad luck from the stars"
                ],
                "common_misconceptions": [
                    "It means they're from different families (incorrect - that's part of why, but not what the phrase means)",
                    "It means they cross paths like stars (incorrect - it means cosmic opposition)"
                ],
                "partial_credit_guidance": "Award half credit if student mentions fate/destiny but doesn't explain the doomed aspect"
            },
            {
                "question": "What starts the brawl in the opening scene?",
                "correct_answer": "Sampson bites his thumb at Abraham/the Montague servants, which was an insulting gesture. This small provocation escalates into a full street fight.",
                "acceptable_variations": [
                    "A thumb-biting insult",
                    "The servants insulted each other",
                    "Capulet and Montague servants fought over an insult"
                ],
                "common_misconceptions": [
                    "Romeo started it (incorrect - Romeo isn't even in this part)",
                    "The families are fighting over something specific (incorrect - it's a petty insult)"
                ],
                "partial_credit_guidance": "Award half credit for identifying it was the servants, even without the specific insult"
            }
        ]
    },
    2: {  # Day 2: Romeo's Melancholy
        "questions": [
            {
                "question": "Who is Rosaline and why is Romeo sad?",
                "correct_answer": "Rosaline is a woman Romeo claims to love, but she has sworn off love/romance and rejects him. Romeo is sad because his love is unrequited.",
                "acceptable_variations": [
                    "A woman who won't love Romeo back",
                    "The woman Romeo thinks he loves but who ignores him",
                    "A woman who has vowed to be chaste/celibate"
                ],
                "common_misconceptions": [
                    "Rosaline is Juliet (incorrect - Juliet comes later)",
                    "Rosaline is mean to Romeo (incorrect - she's just not interested)",
                    "Romeo is sad about the feud (incorrect at this point)"
                ],
                "partial_credit_guidance": "Award half credit for identifying Rosaline as a love interest, even without the rejection detail"
            },
            {
                "question": "Give an example of an oxymoron Romeo uses about love.",
                "correct_answer": "Examples include: 'brawling love,' 'loving hate,' 'heavy lightness,' 'serious vanity,' 'cold fire,' 'sick health,' 'feather of lead,' 'bright smoke'",
                "acceptable_variations": [
                    "Any two-word phrase with opposite meanings from Romeo's speech"
                ],
                "common_misconceptions": [
                    "Just using any metaphor (incorrect - must be contradictory terms)",
                    "'Star-crossed lovers' (incorrect - this is from prologue, not Romeo's speech)"
                ],
                "partial_credit_guidance": "Award half credit if student identifies contradictory concepts but not exact phrases from text"
            }
        ]
    },
    3: {  # Day 3: Juliet Introduced
        "questions": [
            {
                "question": "What does Juliet say about marriage when her mother asks?",
                "correct_answer": "Juliet says 'It is an honor that I dream not of' - meaning she hasn't thought about marriage yet. She's obedient and says she'll look at Paris and try to like him if her parents want.",
                "acceptable_variations": [
                    "She hasn't thought about it",
                    "She'll do what her parents say",
                    "She's not dreaming of marriage but will try to like Paris"
                ],
                "common_misconceptions": [
                    "She's excited about Paris (incorrect - she's neutral/obedient)",
                    "She refuses to marry (incorrect - she agrees to look at him)"
                ],
                "partial_credit_guidance": "Award half credit for either the 'not thinking about it' part OR the obedience part"
            }
        ]
    },
    4: {  # Day 4: Queen Mab Speech
        "questions": [
            {
                "question": "According to Mercutio, what does Queen Mab do?",
                "correct_answer": "Queen Mab is a tiny fairy who visits people at night and gives them dreams about what they desire most - soldiers dream of battles, lovers dream of love, etc.",
                "acceptable_variations": [
                    "She brings dreams to people",
                    "She makes people dream about their desires",
                    "A fairy who controls dreams"
                ],
                "common_misconceptions": [
                    "She's a real queen (incorrect - she's imaginary/fairy)",
                    "She gives people nightmares (incorrect - dreams of desires, though speech gets dark)"
                ],
                "partial_credit_guidance": "Award half credit for identifying her as dream-related"
            },
            {
                "question": "How does Mercutio's speech change from beginning to end?",
                "correct_answer": "The speech starts playful and whimsical describing a tiny fairy, but becomes darker, more frantic, and disturbing by the end - suggesting loss of control or hidden rage.",
                "acceptable_variations": [
                    "Starts fun, ends dark",
                    "Gets more violent and sexual as it goes",
                    "He loses control of his own speech"
                ],
                "common_misconceptions": [
                    "It stays funny throughout (incorrect - tone shifts dramatically)",
                    "It becomes romantic (incorrect - becomes violent)"
                ],
                "partial_credit_guidance": "Award half credit for noting a change in tone even without specifics"
            }
        ]
    },
    5: {  # Day 5: First Meeting
        "questions": [
            {
                "question": "What is special about how Romeo and Juliet speak when they first meet?",
                "correct_answer": "They share a sonnet - their first 14 lines of dialogue together form a perfect sonnet with proper rhyme scheme (ABAB CDCD EFEF GG). This shows they are meant for each other.",
                "acceptable_variations": [
                    "They complete each other's sentences in a sonnet",
                    "Their dialogue forms a poem together",
                    "Shakespeare makes them share a love poem"
                ],
                "common_misconceptions": [
                    "Romeo speaks a sonnet to Juliet (incorrect - they share it)",
                    "They just flirt normally (incorrect - it's structured poetry)"
                ],
                "partial_credit_guidance": "Award half credit for identifying that their speech is poetic, even without naming the sonnet form"
            }
        ]
    },
    7: {  # Day 7: Balcony Scene Part 1
        "questions": [
            {
                "question": "What does Romeo compare Juliet to? Give at least two examples.",
                "correct_answer": "Romeo compares Juliet to: the sun, stars in heaven, an angel, a winged messenger, the brightness of day. These are all light/celestial imagery.",
                "acceptable_variations": [
                    "Sun and stars",
                    "Light, angel, heaven",
                    "Any two celestial/light images from the speech"
                ],
                "common_misconceptions": [
                    "A rose (incorrect - that's Juliet's line)",
                    "Night (incorrect - she's contrasted WITH night)"
                ],
                "partial_credit_guidance": "Award half credit for one example, full credit for two or more"
            }
        ]
    },
    8: {  # Day 8: What's in a Name
        "questions": [
            {
                "question": "What is Juliet's argument about Romeo's name?",
                "correct_answer": "Juliet argues that names are just arbitrary labels - a rose by any other name would smell as sweet. Romeo's name 'Montague' is not part of who he really is, so he should give it up to be with her.",
                "acceptable_variations": [
                    "Names don't define who you are",
                    "If you called a rose something else, it would still be the same",
                    "His name is not his essential self"
                ],
                "common_misconceptions": [
                    "'Wherefore' means 'where' (incorrect - it means 'why')",
                    "She's asking where Romeo is (incorrect - she's asking why he has that name)"
                ],
                "partial_credit_guidance": "Award half credit for understanding that she wants him to give up his name, even without the philosophical argument"
            }
        ]
    },
    10: {  # Day 10: Friar Lawrence
        "questions": [
            {
                "question": "Why does Friar Lawrence agree to marry Romeo and Juliet?",
                "correct_answer": "The Friar hopes that the marriage will unite the two families and end the feud. His motivation is political/peaceful - he wants to turn their 'households' rancor to pure love.'",
                "acceptable_variations": [
                    "To end the family feud",
                    "He thinks it could bring peace to Verona",
                    "To unite the Montagues and Capulets"
                ],
                "common_misconceptions": [
                    "Because he thinks they're truly in love (he's actually skeptical)",
                    "Because Romeo asks nicely (he has ulterior motives)"
                ],
                "partial_credit_guidance": "Award half credit for 'to help Romeo' without the peace/feud reasoning"
            }
        ]
    },
    12: {  # Day 12: The Deaths
        "questions": [
            {
                "question": "What does Mercutio mean by 'A plague o' both your houses'?",
                "correct_answer": "Mercutio is cursing BOTH families - Montagues and Capulets. He blames the feud itself for his death, not just Tybalt. He sees that the senseless conflict has killed him.",
                "acceptable_variations": [
                    "He curses both families for the feud that killed him",
                    "He blames both sides equally",
                    "He wishes disaster on both families"
                ],
                "common_misconceptions": [
                    "He only blames the Capulets (incorrect - he curses BOTH)",
                    "He's talking about literal plague disease (incorrect - it's a curse)"
                ],
                "partial_credit_guidance": "Award half credit for understanding it's a curse, even without the 'both families' insight"
            }
        ]
    },
    13: {  # Day 13: Aftermath
        "questions": [
            {
                "question": "Why does Juliet use oxymorons like 'beautiful tyrant' and 'fiend angelical' to describe Romeo?",
                "correct_answer": "Juliet is experiencing contradictory emotions - she loves Romeo but he killed her cousin. The oxymorons express her internal conflict and confusion about how to feel.",
                "acceptable_variations": [
                    "She feels conflicting emotions about Romeo",
                    "She loves him but hates what he did",
                    "Her feelings are contradictory"
                ],
                "common_misconceptions": [
                    "She hates Romeo now (incorrect - she defends him shortly after)",
                    "She's just being poetic (incorrect - it expresses real emotional conflict)"
                ],
                "partial_credit_guidance": "Award half credit for identifying emotional conflict without connecting it to the oxymoron form"
            }
        ]
    },
    15: {  # Day 15: Aubade
        "questions": [
            {
                "question": "Why do Romeo and Juliet argue about the lark and nightingale?",
                "correct_answer": "The nightingale sings at night (meaning Romeo can stay) while the lark sings at dawn (meaning Romeo must leave or die). Juliet wants it to be night so he can stay; Romeo knows it's dawn.",
                "acceptable_variations": [
                    "Nightingale = night = safe. Lark = day = danger",
                    "Juliet pretends it's night so Romeo can stay",
                    "They're really arguing about whether he has to leave"
                ],
                "common_misconceptions": [
                    "They actually care about birds (incorrect - it's symbolic)",
                    "Romeo wants to stay (incorrect - he knows he must go)"
                ],
                "partial_credit_guidance": "Award half credit for understanding one bird symbolizes Romeo leaving, even without the full explanation"
            }
        ]
    },
    17: {  # Day 17: Friar's Plan
        "questions": [
            {
                "question": "What is the Friar's plan for Juliet?",
                "correct_answer": "Juliet will drink a potion that makes her appear dead for 42 hours. Her family will put her in the tomb. Friar will send a letter to Romeo in Mantua. Romeo will rescue her when she wakes.",
                "acceptable_variations": [
                    "Fake her death with a potion, then escape with Romeo",
                    "Potion makes her seem dead, Romeo gets letter, saves her from tomb"
                ],
                "common_misconceptions": [
                    "She actually dies and comes back (incorrect - it's fake death)",
                    "The potion makes her sleep forever (incorrect - it's 42 hours)"
                ],
                "partial_credit_guidance": "Award half credit for knowing about the potion, even without the rescue plan details"
            }
        ]
    },
    18: {  # Day 18: Juliet's Fears
        "questions": [
            {
                "question": "List at least 3 fears Juliet names in her soliloquy before drinking the potion.",
                "correct_answer": "Fears include: 1) The potion won't work 2) It's actually poison to kill her 3) She'll wake too early alone 4) She'll suffocate in the tomb 5) She'll go mad from the smell of death 6) She'll see Tybalt's ghost 7) She'll see other ghosts/spirits",
                "acceptable_variations": [
                    "Any 3 of the listed fears in any phrasing"
                ],
                "common_misconceptions": [
                    "Fear of marrying Paris (this is motivation, not what she names in soliloquy)",
                    "Fear of her parents (not specifically named)"
                ],
                "partial_credit_guidance": "Award 1/3 credit per fear correctly identified, up to full credit"
            }
        ]
    },
    21: {  # Day 21: I Defy You Stars
        "questions": [
            {
                "question": "When Romeo says 'I defy you, stars!' what does he mean? Is he really defying fate?",
                "correct_answer": "Romeo is declaring that he will take control of his own destiny rather than accept fate's plan. However, ironically, by rushing to die with Juliet, he may actually be fulfilling the 'star-crossed' prophecy.",
                "acceptable_variations": [
                    "He's rejecting fate but actually fulfilling it",
                    "He thinks he's defying fate but he's playing into it",
                    "He's trying to control his destiny"
                ],
                "common_misconceptions": [
                    "He successfully defies fate (incorrect - he dies as prophesied)",
                    "It's just an angry outburst (incorrect - it's thematically significant)"
                ],
                "partial_credit_guidance": "Award half credit for explaining what Romeo THINKS he's doing, full credit for the irony"
            }
        ]
    },
    23: {  # Day 23: The Deaths
        "questions": [
            {
                "question": "How close does Romeo come to realizing Juliet is alive? What does he notice?",
                "correct_answer": "Romeo notices that Juliet still has color in her cheeks, her lips are still red, and 'death' hasn't affected her beauty. He even asks 'Why art thou yet so fair?' but concludes death is keeping her as a bride.",
                "acceptable_variations": [
                    "He notices she looks alive but assumes death preserved her",
                    "Her lips are red, she's not pale - he almost figures it out",
                    "He questions why she looks so good but draws wrong conclusion"
                ],
                "common_misconceptions": [
                    "He knows she's alive (incorrect - he thinks she's dead)",
                    "He doesn't notice anything unusual (incorrect - he explicitly notes her appearance)"
                ],
                "partial_credit_guidance": "Award half credit for knowing he notices something, full credit for the tragic irony"
            }
        ]
    },
    24: {  # Day 24: Resolution
        "questions": [
            {
                "question": "How does the ending connect back to the prologue's promise?",
                "correct_answer": "The prologue said their death would 'bury their parents' strife.' In the end, the Montagues and Capulets reconcile over the bodies of their children, promising to build golden statues. The deaths ended the feud.",
                "acceptable_variations": [
                    "The lovers' deaths end the feud as the prologue predicted",
                    "The parents make peace because of the tragedy",
                    "The circular structure - starts with feud, ends with peace through death"
                ],
                "common_misconceptions": [
                    "The ending is just sad (incomplete - there's resolution)",
                    "The families keep fighting (incorrect - they reconcile)"
                ],
                "partial_credit_guidance": "Award half credit for noting the families make peace, full credit for connecting to the prologue"
            }
        ]
    }
}

# Handout answer templates by activity type
HANDOUT_ANSWER_TEMPLATES = {
    "character_chart": {
        "exemplar_structure": "Each character should have: motivation (what they want), obstacle (what's in their way), key quote (textual evidence), and development notes (how they change)",
        "look_for": ["Accurate motivations", "Relevant textual evidence", "Correct act/scene citations"]
    },
    "annotation_guide": {
        "exemplar_structure": "Annotations should identify: key quotes, literary devices, character revelations, and connections to themes",
        "look_for": ["3+ annotations per section", "Evidence of close reading", "Connections between sections"]
    },
    "vocabulary_practice": {
        "exemplar_structure": "Correct definitions, proper context usage, accurate examples from the play",
        "look_for": ["Correct meanings (not just dictionary)", "Play-specific examples", "Pronunciation for Shakespeare terms"]
    }
}


def generate_answer_key(day: int) -> Dict:
    """
    Generate a complete answer key for a specific day.

    Args:
        day: Day number (1-30)

    Returns:
        Dict containing the complete answer key
    """
    day_answers = EXIT_TICKET_ANSWERS.get(day, {})

    answer_key = {
        "day": day,
        "header": {
            "title": f"Day {day:02d} Answer Key",
            "for_teacher_use_only": "CONFIDENTIAL - For Teacher Use Only"
        },
        "exit_ticket_answers": [],
        "handout_answers": None,
        "grading_notes": {
            "quick_check": "Use this key to quickly grade exit tickets. Look for key concepts, not exact wording.",
            "partial_credit": "Award partial credit for correct reasoning with minor errors.",
            "time_saver": "Star responses that demonstrate exceptional insight to share with class."
        }
    }

    for q_data in day_answers.get("questions", []):
        answer_key["exit_ticket_answers"].append({
            "question": q_data["question"],
            "correct_answer": q_data["correct_answer"],
            "acceptable_variations": q_data["acceptable_variations"],
            "common_misconceptions": q_data["common_misconceptions"],
            "partial_credit": q_data["partial_credit_guidance"]
        })

    return answer_key


def validate_answer_key(answer_key: Dict) -> Dict:
    """
    Validate an answer key against generation rules.

    Rules:
    - R1: Must include exemplar for open-ended questions
    - R2: Must note common misconceptions
    - R3: Must include partial credit guidance
    - R4: Must list acceptable variations for interpretation questions

    Returns:
        Dict with validation status and any issues found
    """
    issues = []

    for q_answer in answer_key.get("exit_ticket_answers", []):
        # R1: Check for exemplar/correct answer
        if not q_answer.get("correct_answer"):
            issues.append(f"Missing correct answer for: {q_answer.get('question', 'unknown')}")

        # R2: Check for misconceptions
        if not q_answer.get("common_misconceptions"):
            issues.append(f"Missing misconceptions for: {q_answer.get('question', 'unknown')[:30]}...")

        # R3: Check for partial credit guidance
        if not q_answer.get("partial_credit"):
            issues.append(f"Missing partial credit guidance for: {q_answer.get('question', 'unknown')[:30]}...")

        # R4: Check for acceptable variations
        if not q_answer.get("acceptable_variations"):
            issues.append(f"Missing acceptable variations for: {q_answer.get('question', 'unknown')[:30]}...")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "answer_key": answer_key
    }


def generate_answer_key_markdown(answer_key: Dict) -> str:
    """Generate markdown format of the answer key for output."""
    lines = [
        f"# {answer_key['header']['title']}",
        "",
        f"**{answer_key['header']['for_teacher_use_only']}**",
        "",
        "---",
        "",
        "## Exit Ticket Answers",
        ""
    ]

    for i, q_answer in enumerate(answer_key["exit_ticket_answers"], 1):
        lines.extend([
            f"### Question {i}",
            f"**{q_answer['question']}**",
            "",
            f"**Correct Answer:** {q_answer['correct_answer']}",
            "",
            "**Acceptable Variations:**"
        ])

        for var in q_answer["acceptable_variations"]:
            lines.append(f"- {var}")

        lines.extend([
            "",
            "**Common Misconceptions to Watch For:**"
        ])

        for misc in q_answer["common_misconceptions"]:
            lines.append(f"- ⚠️ {misc}")

        lines.extend([
            "",
            f"**Partial Credit Guidance:** _{q_answer['partial_credit']}_",
            "",
            "---",
            ""
        ])

    lines.extend([
        "## Grading Notes",
        "",
        f"- **Quick Check:** {answer_key['grading_notes']['quick_check']}",
        f"- **Partial Credit:** {answer_key['grading_notes']['partial_credit']}",
        f"- **Time Saver:** {answer_key['grading_notes']['time_saver']}"
    ])

    return "\n".join(lines)


def generate_all_answer_keys() -> List[Dict]:
    """Generate answer keys for all days with exit ticket data."""
    answer_keys = []

    for day in sorted(EXIT_TICKET_ANSWERS.keys()):
        answer_key = generate_answer_key(day)
        validation = validate_answer_key(answer_key)
        answer_key["validation"] = validation
        answer_keys.append(answer_key)

    return answer_keys


# Export main components
__all__ = [
    'generate_answer_key',
    'validate_answer_key',
    'generate_answer_key_markdown',
    'generate_all_answer_keys',
    'EXIT_TICKET_ANSWERS',
    'HANDOUT_ANSWER_TEMPLATES',
    'AnswerKeyEntry'
]
