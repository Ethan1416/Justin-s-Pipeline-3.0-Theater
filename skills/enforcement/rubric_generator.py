"""
Rubric Generator - Theater Education Pipeline v2.3

Generates assessment rubrics aligned to lesson objectives.
Uses 4-point scale with specific, observable descriptors.

Generated for: Romeo and Juliet (6-week unit)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class RubricCriterion:
    """Individual criterion within a rubric."""
    name: str
    exemplary: str  # 4 points
    proficient: str  # 3 points
    developing: str  # 2 points
    beginning: str  # 1 point

@dataclass
class Rubric:
    """Complete rubric for an activity."""
    day: int
    activity_name: str
    criteria: List[RubricCriterion]
    total_points: int

# Rubric templates by activity type
RUBRIC_TEMPLATES = {
    "tableaux": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Physical Composition",
                exemplary="Creates visually striking frozen image with clear levels, focus, and use of space; every body part is intentional",
                proficient="Creates clear frozen image with good use of levels and space; most body positions are intentional",
                developing="Creates basic frozen image but lacks levels or spatial awareness; some poses are unfocused",
                beginning="Image is unclear or moving; lacks intention or focus"
            ),
            RubricCriterion(
                name="Emotional Expression",
                exemplary="Facial expression and body language powerfully convey character's emotion; audience immediately understands feeling",
                proficient="Expression and body language clearly convey emotion; audience can identify feeling",
                developing="Some expression present but unclear or inconsistent; emotion must be guessed",
                beginning="Little to no emotional expression; appears neutral or disconnected"
            ),
            RubricCriterion(
                name="Textual Connection",
                exemplary="Image directly and powerfully illustrates specific moment from text; captures essential meaning",
                proficient="Image connects to text and captures main idea of the moment",
                developing="Image loosely relates to text but misses key elements",
                beginning="Image does not clearly connect to the text"
            )
        ]
    },
    "character_motivation_chart": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Character Understanding",
                exemplary="Demonstrates deep insight into character's wants, needs, and fears with sophisticated analysis",
                proficient="Shows clear understanding of character's motivations with accurate analysis",
                developing="Shows basic understanding but analysis is surface-level or incomplete",
                beginning="Misunderstands character or provides minimal analysis"
            ),
            RubricCriterion(
                name="Textual Evidence",
                exemplary="Cites multiple specific quotes accurately; evidence directly supports all claims",
                proficient="Cites relevant quotes; evidence supports most claims",
                developing="Cites some evidence but it may be vague or not fully support claims",
                beginning="Little to no textual evidence provided"
            ),
            RubricCriterion(
                name="Organization",
                exemplary="Chart is exceptionally clear, logical, and easy to follow; categories are insightful",
                proficient="Chart is organized and clear; categories are appropriate",
                developing="Chart shows some organization but may be confusing in places",
                beginning="Chart is disorganized or difficult to read"
            )
        ]
    },
    "fishbowl_discussion": {
        "type": "discussion",
        "criteria": [
            RubricCriterion(
                name="Participation",
                exemplary="Contributes 3+ substantive comments; builds on others' ideas; asks probing questions",
                proficient="Contributes 2 substantive comments; engages with others' ideas",
                developing="Contributes 1 comment; limited engagement with discussion",
                beginning="Does not contribute to discussion or disrupts others"
            ),
            RubricCriterion(
                name="Evidence Use",
                exemplary="Every claim is supported by specific textual evidence with accurate citations",
                proficient="Most claims are supported by textual evidence",
                developing="Some evidence used but often vague or unsupported claims",
                beginning="No textual evidence used"
            ),
            RubricCriterion(
                name="Active Listening",
                exemplary="References others' points by name; synthesizes multiple perspectives; advances discussion",
                proficient="Responds to others' points; shows understanding of different views",
                developing="Occasionally responds to others but mostly makes independent points",
                beginning="Does not acknowledge or respond to others' contributions"
            )
        ]
    },
    "monologue_analysis": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Literary Device Identification",
                exemplary="Identifies and explains 4+ literary devices with precise terminology and insightful analysis",
                proficient="Identifies and explains 2-3 literary devices accurately",
                developing="Identifies 1-2 devices but explanation may be incomplete or imprecise",
                beginning="Does not identify literary devices or misidentifies them"
            ),
            RubricCriterion(
                name="Meaning Interpretation",
                exemplary="Provides sophisticated interpretation of meaning; connects devices to overall effect",
                proficient="Provides clear interpretation; explains how devices contribute to meaning",
                developing="Provides basic interpretation but may miss deeper meaning",
                beginning="Interpretation is inaccurate or missing"
            ),
            RubricCriterion(
                name="Written Expression",
                exemplary="Analysis is eloquent, precise, and uses literary terminology correctly throughout",
                proficient="Analysis is clear and uses most terminology correctly",
                developing="Analysis is understandable but may be vague or misuse terminology",
                beginning="Analysis is unclear or uses no literary terminology"
            )
        ]
    },
    "sonnet_analysis": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Form Recognition",
                exemplary="Accurately identifies all elements of sonnet form (14 lines, rhyme scheme, volta, couplet) and explains significance",
                proficient="Identifies most elements of sonnet form with accurate explanation",
                developing="Identifies some elements but may confuse or miss key features",
                beginning="Does not recognize sonnet form or misidentifies it"
            ),
            RubricCriterion(
                name="Imagery Analysis",
                exemplary="Provides deep analysis of religious, light/dark, and love imagery with textual evidence",
                proficient="Analyzes imagery patterns with some textual evidence",
                developing="Notes some imagery but analysis is surface-level",
                beginning="Does not identify or analyze imagery"
            ),
            RubricCriterion(
                name="Theme Connection",
                exemplary="Connects sonnet analysis to larger themes of love, fate, and identity in the play",
                proficient="Makes some connection to larger themes",
                developing="Limited connection to themes; analysis stays within the scene",
                beginning="No connection to larger themes"
            )
        ]
    },
    "blocking_exploration": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Stage Awareness",
                exemplary="Uses all areas of stage meaningfully; blocking reveals relationships and status",
                proficient="Uses stage space effectively; blocking supports character relationships",
                developing="Some use of stage space but may cluster or ignore areas",
                beginning="No awareness of stage space; stands in one spot"
            ),
            RubricCriterion(
                name="Character Physicality",
                exemplary="Movement and gesture reveal character's inner life; physicality is consistent and specific",
                proficient="Movement supports character; some specific choices evident",
                developing="Basic movement present but lacks specificity or intention",
                beginning="Movement does not reflect character; appears as self"
            ),
            RubricCriterion(
                name="Partner Awareness",
                exemplary="Blocking creates dynamic relationship; responds to and affects partner's movement",
                proficient="Blocking shows awareness of partner; some reaction present",
                developing="Limited partner awareness; movements seem isolated",
                beginning="No partner awareness; blocks partner or ignores them"
            )
        ]
    },
    "language_analysis": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Metaphor Identification",
                exemplary="Identifies and traces all major metaphor patterns (light/dark, celestial, nature) throughout passage",
                proficient="Identifies and explains most metaphor patterns",
                developing="Identifies some metaphors but may miss patterns or connections",
                beginning="Does not identify metaphors or confuses them with other devices"
            ),
            RubricCriterion(
                name="Effect Analysis",
                exemplary="Provides sophisticated analysis of how metaphors create emotional impact and meaning",
                proficient="Explains how metaphors contribute to meaning and effect",
                developing="Basic explanation of metaphor meaning; limited analysis of effect",
                beginning="No analysis of metaphor effect"
            ),
            RubricCriterion(
                name="Evidence Organization",
                exemplary="Evidence is organized thematically with clear progression of analysis",
                proficient="Evidence is organized and supports analysis",
                developing="Some organization but analysis may be scattered",
                beginning="No clear organization of evidence or analysis"
            )
        ]
    },
    "modern_translation": {
        "type": "writing",
        "criteria": [
            RubricCriterion(
                name="Accuracy",
                exemplary="Translation captures exact meaning of original with no misinterpretations",
                proficient="Translation captures main meaning with minor inaccuracies",
                developing="Translation captures general idea but misses nuances or has errors",
                beginning="Translation misunderstands the original or is incomplete"
            ),
            RubricCriterion(
                name="Voice Preservation",
                exemplary="Translation maintains character's voice, tone, and emotional register in modern language",
                proficient="Translation maintains most elements of character's voice",
                developing="Translation is flat or generic; voice is lost",
                beginning="Translation does not reflect character's voice"
            ),
            RubricCriterion(
                name="Natural Language",
                exemplary="Modern translation sounds like natural contemporary speech while remaining sophisticated",
                proficient="Translation sounds natural with minor awkwardness",
                developing="Translation is understandable but sounds forced or unnatural",
                beginning="Translation is confusing or uses unnatural phrasing"
            )
        ]
    },
    "scene_performance_prep": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Character Commitment",
                exemplary="Fully embodies character physically, vocally, and emotionally throughout performance",
                proficient="Shows clear character choices with consistent commitment",
                developing="Some character work present but inconsistent or breaks character",
                beginning="Does not embody character; appears as self throughout"
            ),
            RubricCriterion(
                name="Text Fluency",
                exemplary="Delivers lines with full fluency; paraphrases only enhance meaning",
                proficient="Delivers most lines accurately with minimal errors",
                developing="Knows general content but frequently paraphrases or stumbles",
                beginning="Does not know lines; relies heavily on script or prompts"
            ),
            RubricCriterion(
                name="Collaboration",
                exemplary="Works seamlessly with partner; listens and reacts genuinely in every moment",
                proficient="Good partner work with evident listening and reaction",
                developing="Some partner awareness but occasionally disconnected",
                beginning="Does not connect with partner; performs in isolation"
            )
        ]
    },
    "conflict_mapping": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Cause-Effect Analysis",
                exemplary="Traces complete chain of choices and consequences; identifies multiple causal factors",
                proficient="Identifies main causes and effects with clear connections",
                developing="Shows some cause-effect relationships but chain is incomplete",
                beginning="Does not identify cause-effect relationships"
            ),
            RubricCriterion(
                name="Character Agency",
                exemplary="Analyzes each character's role in escalation with sophisticated understanding of choice",
                proficient="Identifies each character's contributions to conflict",
                developing="Identifies some character choices but may miss key decisions",
                beginning="Does not analyze character agency in conflict"
            ),
            RubricCriterion(
                name="Visual Clarity",
                exemplary="Map is visually clear, logical, and enhances understanding of conflict progression",
                proficient="Map is clear and shows conflict progression",
                developing="Map is somewhat confusing but shows basic structure",
                beginning="Map is unclear or does not represent conflict"
            )
        ]
    },
    "staged_combat_workshop": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Safety",
                exemplary="Maintains complete control; follows all safety protocols; aware of surroundings at all times",
                proficient="Follows safety protocols; maintains good control",
                developing="Some safety lapses or loss of control; needs reminders",
                beginning="Unsafe; ignores protocols or loses control"
            ),
            RubricCriterion(
                name="Choreography Execution",
                exemplary="Executes all moves with precision, timing, and dramatic effect",
                proficient="Executes most moves accurately with good timing",
                developing="Knows sequence but execution is imprecise or rushed",
                beginning="Does not know sequence or cannot execute moves"
            ),
            RubricCriterion(
                name="Dramatic Storytelling",
                exemplary="Combat tells clear story; stakes and emotions are visible throughout",
                proficient="Combat shows story with evident emotional stakes",
                developing="Combat is technically correct but lacks dramatic impact",
                beginning="Combat does not tell a story; appears mechanical"
            )
        ]
    },
    "oxymoron_hunt": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Identification",
                exemplary="Identifies 5+ oxymorons with accurate line citations",
                proficient="Identifies 3-4 oxymorons with citations",
                developing="Identifies 1-2 oxymorons or has citation errors",
                beginning="Does not identify oxymorons or confuses with other devices"
            ),
            RubricCriterion(
                name="Analysis",
                exemplary="Explains how each oxymoron reveals Juliet's emotional conflict with sophisticated insight",
                proficient="Explains connection between oxymorons and Juliet's emotions",
                developing="Basic explanation with limited emotional analysis",
                beginning="No analysis of oxymoron meaning or effect"
            ),
            RubricCriterion(
                name="Pattern Recognition",
                exemplary="Identifies patterns in oxymoron use and connects to larger themes of duality",
                proficient="Notes some patterns in oxymoron use",
                developing="Treats each oxymoron in isolation without pattern recognition",
                beginning="No recognition of patterns"
            )
        ]
    },
    "hot_seat": {
        "type": "discussion",
        "criteria": [
            RubricCriterion(
                name="Character Accuracy",
                exemplary="All responses are fully consistent with character's knowledge, personality, and situation",
                proficient="Most responses are consistent with character",
                developing="Some responses reflect character but occasionally breaks consistency",
                beginning="Responses do not reflect character; answers as self"
            ),
            RubricCriterion(
                name="Textual Grounding",
                exemplary="Defenses are grounded in specific textual evidence; cites lines when appropriate",
                proficient="References text to support character's perspective",
                developing="Some textual reference but often relies on general impression",
                beginning="No textual grounding; invents information"
            ),
            RubricCriterion(
                name="Improvisational Skill",
                exemplary="Responds to unexpected questions with creativity while maintaining character",
                proficient="Handles most questions with appropriate character responses",
                developing="Struggles with unexpected questions; may break character",
                beginning="Cannot improvise; freezes or breaks character"
            )
        ]
    },
    "aubade_analysis": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Genre Understanding",
                exemplary="Demonstrates sophisticated understanding of aubade tradition and its conventions",
                proficient="Shows clear understanding of aubade as a genre",
                developing="Basic awareness of aubade but limited understanding of conventions",
                beginning="Does not understand the aubade genre"
            ),
            RubricCriterion(
                name="Symbol Analysis",
                exemplary="Provides deep analysis of lark/nightingale symbolism with connections to time, death, and parting",
                proficient="Analyzes symbols and connects to scene's themes",
                developing="Identifies symbols but analysis is surface-level",
                beginning="Does not identify or analyze symbols"
            ),
            RubricCriterion(
                name="Emotional Interpretation",
                exemplary="Captures the urgency, dread, and love in the passage with sophisticated emotional analysis",
                proficient="Identifies emotional content and connects to character motivation",
                developing="Notes some emotion but analysis lacks depth",
                beginning="Does not address emotional content"
            )
        ]
    },
    "power_dynamics_map": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Relationship Analysis",
                exemplary="Analyzes all power relationships with nuance; identifies shifting dynamics throughout scene",
                proficient="Identifies main power relationships accurately",
                developing="Identifies some relationships but may miss key dynamics",
                beginning="Does not identify power relationships"
            ),
            RubricCriterion(
                name="Evidence Base",
                exemplary="Supports analysis with specific quotes, actions, and stage directions",
                proficient="Uses some textual evidence to support analysis",
                developing="Limited evidence; relies on general impressions",
                beginning="No textual evidence provided"
            ),
            RubricCriterion(
                name="Social Context",
                exemplary="Connects power dynamics to historical/social context of gender, class, and family",
                proficient="Shows awareness of social context in analysis",
                developing="Limited awareness of social factors",
                beginning="No awareness of social context"
            )
        ]
    },
    "decision_tree": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Option Identification",
                exemplary="Identifies all possible options Juliet has with realistic assessment of each",
                proficient="Identifies main options with reasonable assessment",
                developing="Identifies limited options; may miss possibilities",
                beginning="Does not identify options or only one option"
            ),
            RubricCriterion(
                name="Consequence Analysis",
                exemplary="Traces consequences of each option with sophisticated understanding of character and context",
                proficient="Explains likely consequences of each option",
                developing="Basic consequence analysis with limited depth",
                beginning="Does not analyze consequences"
            ),
            RubricCriterion(
                name="Character Perspective",
                exemplary="Analysis fully inhabits Juliet's perspective and constraints while acknowledging alternatives",
                proficient="Shows awareness of Juliet's perspective and limitations",
                developing="Some awareness of perspective but may impose modern views",
                beginning="Analyzes from outside perspective without empathy"
            )
        ]
    },
    "fear_inventory": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Comprehensiveness",
                exemplary="Identifies all fears named in soliloquy (5+) with accurate line references",
                proficient="Identifies most fears (3-4) with line references",
                developing="Identifies some fears but may miss key ones",
                beginning="Identifies one or no fears"
            ),
            RubricCriterion(
                name="Categorization",
                exemplary="Creates insightful categories that reveal pattern in Juliet's fears (physical, psychological, social)",
                proficient="Creates reasonable categories for fears",
                developing="Attempts categorization but categories are unclear or overlap",
                beginning="No categorization attempted"
            ),
            RubricCriterion(
                name="Psychological Analysis",
                exemplary="Provides sophisticated analysis of what fears reveal about Juliet's psychological state",
                proficient="Connects fears to Juliet's emotional and mental state",
                developing="Basic connection to character psychology",
                beginning="No psychological analysis"
            )
        ]
    },
    "monologue_coaching": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Beat Identification",
                exemplary="Identifies all beats in soliloquy with clear understanding of emotional shifts",
                proficient="Identifies most beats with understanding of major shifts",
                developing="Identifies some beats but may miss key transitions",
                beginning="Does not identify beats; performs monologue as one unit"
            ),
            RubricCriterion(
                name="Vocal Variety",
                exemplary="Uses full range of pace, pitch, volume, and pause to serve meaning and emotion",
                proficient="Shows good vocal variety that supports text",
                developing="Some vocal variety but often monotone or inconsistent",
                beginning="No vocal variety; monotone delivery"
            ),
            RubricCriterion(
                name="Climax Execution",
                exemplary="Builds to powerful climax with clear arc; emotional peak lands effectively",
                proficient="Shows build toward climax; emotional peak is evident",
                developing="Some build present but climax may be rushed or unclear",
                beginning="No build or climax; flat throughout"
            )
        ]
    },
    "fate_vs_choice_debate": {
        "type": "discussion",
        "criteria": [
            RubricCriterion(
                name="Argument Construction",
                exemplary="Constructs sophisticated argument with clear thesis, evidence, and reasoning",
                proficient="Constructs clear argument with supporting evidence",
                developing="Basic argument present but may lack evidence or clear reasoning",
                beginning="No clear argument constructed"
            ),
            RubricCriterion(
                name="Counter-Argument",
                exemplary="Anticipates and addresses counter-arguments; acknowledges complexity of issue",
                proficient="Addresses some counter-arguments",
                developing="Limited engagement with opposing view",
                beginning="Does not address counter-arguments"
            ),
            RubricCriterion(
                name="Textual Evidence",
                exemplary="Marshals multiple specific textual examples to support argument",
                proficient="Uses several textual examples effectively",
                developing="Uses some text but evidence is limited or general",
                beginning="No textual evidence used"
            )
        ]
    },
    "what_if_scenarios": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Scenario Logic",
                exemplary="Scenario follows logically from change; traces ripple effects through remaining plot",
                proficient="Scenario is logical with reasonable consequences identified",
                developing="Basic scenario present but logic may have gaps",
                beginning="Scenario is illogical or does not connect to change"
            ),
            RubricCriterion(
                name="Character Consistency",
                exemplary="Characters behave consistently with established personalities even in altered scenario",
                proficient="Characters mostly behave consistently in scenario",
                developing="Some character inconsistencies in scenario",
                beginning="Characters do not behave consistently; scenario is arbitrary"
            ),
            RubricCriterion(
                name="Theme Connection",
                exemplary="Connects scenario to themes of fate, choice, and tragedy; considers implications",
                proficient="Some connection to themes present",
                developing="Limited thematic connection",
                beginning="No thematic connection"
            )
        ]
    },
    "final_moments_staging": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Emotional Impact",
                exemplary="Staging creates powerful emotional impact; audience is moved",
                proficient="Staging creates emotional response; impact is evident",
                developing="Some emotional impact but staging may undermine effect",
                beginning="No emotional impact; staging is flat or confused"
            ),
            RubricCriterion(
                name="Timing and Pacing",
                exemplary="Perfect timing on discoveries, reactions, deaths; pacing serves tragedy",
                proficient="Good timing on key moments; pacing mostly effective",
                developing="Some timing issues that undermine key moments",
                beginning="Poor timing; moments are rushed or dragged"
            ),
            RubricCriterion(
                name="Symbolic Staging",
                exemplary="Staging choices are symbolic and meaningful; positioning reflects relationships and themes",
                proficient="Some symbolic staging choices evident",
                developing="Limited symbolic awareness in staging",
                beginning="No symbolic or meaningful staging choices"
            )
        ]
    },
    "theme_synthesis": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Connection Quality",
                exemplary="Makes sophisticated connections between prologue and ending; identifies circular structure",
                proficient="Makes clear connections between beginning and end",
                developing="Basic connections present but may miss key parallels",
                beginning="Does not connect prologue to ending"
            ),
            RubricCriterion(
                name="Theme Articulation",
                exemplary="Articulates major themes with nuance and complexity; avoids oversimplification",
                proficient="Articulates themes clearly and accurately",
                developing="Basic theme identification with limited development",
                beginning="Cannot articulate themes or misidentifies them"
            ),
            RubricCriterion(
                name="Evidence Synthesis",
                exemplary="Synthesizes evidence from across entire play to support thematic claims",
                proficient="Uses evidence from multiple acts to support themes",
                developing="Evidence is limited to one or two sections",
                beginning="No evidence provided for themes"
            )
        ]
    },
    "scene_selection": {
        "type": "analysis",
        "criteria": [
            RubricCriterion(
                name="Selection Rationale",
                exemplary="Provides compelling rationale for scene choice with clear criteria",
                proficient="Provides clear reason for scene selection",
                developing="Basic rationale provided but may be vague",
                beginning="No rationale for selection"
            ),
            RubricCriterion(
                name="Performance Potential",
                exemplary="Identifies specific performance opportunities (emotion, physicality, language)",
                proficient="Shows awareness of performance potential",
                developing="Limited awareness of what makes scene performable",
                beginning="Does not consider performance aspects"
            ),
            RubricCriterion(
                name="Group Collaboration",
                exemplary="Works collaboratively with group; all members contribute to decision",
                proficient="Good collaboration with most members involved",
                developing="Limited collaboration; one member dominates",
                beginning="No collaboration; decision made individually"
            )
        ]
    },
    "rehearsal_workshop": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Focus and Productivity",
                exemplary="Fully focused throughout; time is used productively with clear progress",
                proficient="Good focus; makes evident progress during rehearsal",
                developing="Some focus but time is partially wasted",
                beginning="Unfocused; minimal progress during rehearsal"
            ),
            RubricCriterion(
                name="Technique Application",
                exemplary="Applies all learned techniques (blocking, vocal variety, character work) effectively",
                proficient="Applies most techniques with some effectiveness",
                developing="Applies some techniques inconsistently",
                beginning="Does not apply learned techniques"
            ),
            RubricCriterion(
                name="Coaching Integration",
                exemplary="Immediately integrates teacher feedback; shows rapid improvement",
                proficient="Integrates most feedback; shows improvement",
                developing="Some integration of feedback; limited improvement",
                beginning="Does not integrate feedback"
            )
        ]
    },
    "peer_feedback": {
        "type": "discussion",
        "criteria": [
            RubricCriterion(
                name="Feedback Quality",
                exemplary="Provides specific, actionable feedback with balance of strengths and areas for growth",
                proficient="Provides clear feedback that is helpful to recipient",
                developing="Provides feedback but may be vague or only positive/negative",
                beginning="Feedback is unhelpful, vague, or absent"
            ),
            RubricCriterion(
                name="Reception",
                exemplary="Receives feedback graciously; asks clarifying questions; plans to implement",
                proficient="Receives feedback openly; shows willingness to improve",
                developing="Receives feedback but may be defensive or dismiss suggestions",
                beginning="Cannot receive feedback; defensive or dismissive"
            ),
            RubricCriterion(
                name="Theater Terminology",
                exemplary="Uses correct theater terminology (blocking, beat, objective) in feedback",
                proficient="Uses some theater terminology correctly",
                developing="Limited use of theater terminology",
                beginning="No use of theater terminology"
            )
        ]
    },
    "performances_talkback": {
        "type": "performance",
        "criteria": [
            RubricCriterion(
                name="Performance Quality",
                exemplary="Delivers polished, compelling performance that demonstrates mastery of all techniques",
                proficient="Delivers clear, prepared performance with good technique",
                developing="Performance shows preparation but has notable weaknesses",
                beginning="Performance is unprepared or ineffective"
            ),
            RubricCriterion(
                name="Audience Engagement",
                exemplary="Fully engages audience; maintains focus and connection throughout",
                proficient="Good audience engagement; maintains connection",
                developing="Some audience awareness but may lose connection",
                beginning="No audience awareness; performs to self"
            ),
            RubricCriterion(
                name="Talkback Participation",
                exemplary="Provides thoughtful reflection on choices; engages meaningfully with questions",
                proficient="Participates in talkback with relevant comments",
                developing="Limited participation in talkback",
                beginning="Does not participate in talkback"
            )
        ]
    },
    "act_review_gallery": {
        "type": "writing",
        "criteria": [
            RubricCriterion(
                name="Visual Design",
                exemplary="Gallery is visually striking and organized; design supports content effectively",
                proficient="Gallery is clear and organized; design is appropriate",
                developing="Gallery shows effort but design may be confusing or cluttered",
                beginning="Gallery is disorganized or incomplete"
            ),
            RubricCriterion(
                name="Content Accuracy",
                exemplary="All key moments are accurately represented with correct details",
                proficient="Most key moments are accurately represented",
                developing="Some key moments present but may have inaccuracies",
                beginning="Content is inaccurate or missing key moments"
            ),
            RubricCriterion(
                name="Synthesis",
                exemplary="Gallery shows sophisticated understanding of act's arc and themes",
                proficient="Gallery shows understanding of act's main events and themes",
                developing="Gallery shows basic understanding but lacks thematic depth",
                beginning="Gallery does not show understanding of act"
            )
        ]
    }
}

# Map activity names to rubric templates
ACTIVITY_TO_RUBRIC = {
    "Tableaux Creation": "tableaux",
    "Character Motivation Chart": "character_motivation_chart",
    "Fishbowl Discussion": "fishbowl_discussion",
    "Monologue Analysis": "monologue_analysis",
    "Sonnet Analysis": "sonnet_analysis",
    "Blocking Exploration": "blocking_exploration",
    "Language Analysis": "language_analysis",
    "Modern Translation": "modern_translation",
    "Scene Performance Prep": "scene_performance_prep",
    "Conflict Mapping": "conflict_mapping",
    "Staged Combat Workshop": "staged_combat_workshop",
    "Oxymoron Hunt": "oxymoron_hunt",
    "Hot Seat": "hot_seat",
    "Aubade Analysis": "aubade_analysis",
    "Power Dynamics Map": "power_dynamics_map",
    "Decision Tree": "decision_tree",
    "Fear Inventory": "fear_inventory",
    "Monologue Coaching": "monologue_coaching",
    "Fate vs. Choice Debate": "fate_vs_choice_debate",
    "'What If' Scenarios": "what_if_scenarios",
    "Final Moments Staging": "final_moments_staging",
    "Theme Synthesis": "theme_synthesis",
    "Scene Selection": "scene_selection",
    "Rehearsal Workshop": "rehearsal_workshop",
    "Peer Feedback": "peer_feedback",
    "Performances + Talkback": "performances_talkback",
    "Performances + Unit Reflection": "performances_talkback",
    "Act 4 Review Gallery": "act_review_gallery",
    "Full Run-Through": "rehearsal_workshop"
}


def generate_rubric(day: int, activity_name: str, objectives: List[str] = None) -> Dict:
    """
    Generate a rubric for a specific day and activity.

    Args:
        day: Day number (1-30)
        activity_name: Name of the activity
        objectives: Optional list of learning objectives for the day

    Returns:
        Dict containing the complete rubric
    """
    template_key = ACTIVITY_TO_RUBRIC.get(activity_name)

    if not template_key:
        # Generate generic rubric if no template exists
        template_key = _get_closest_template(activity_name)

    template = RUBRIC_TEMPLATES.get(template_key, RUBRIC_TEMPLATES["character_motivation_chart"])

    rubric = {
        "day": day,
        "activity_name": activity_name,
        "activity_type": template["type"],
        "header": {
            "title": f"Day {day:02d} Rubric: {activity_name}",
            "date_line": "Date: _______________",
            "name_line": "Student Name: _______________"
        },
        "criteria": [],
        "total_points": len(template["criteria"]) * 4,
        "grade_equivalents": {
            "A": f"{len(template['criteria']) * 4 - 2}-{len(template['criteria']) * 4}",
            "B": f"{len(template['criteria']) * 3}-{len(template['criteria']) * 4 - 3}",
            "C": f"{len(template['criteria']) * 2}-{len(template['criteria']) * 3 - 1}",
            "D/F": f"Below {len(template['criteria']) * 2}"
        },
        "feedback_section": {
            "strengths": "Strengths: _______________________________________________",
            "growth_areas": "Areas for Growth: ________________________________________",
            "next_steps": "Next Steps: ______________________________________________"
        },
        "student_reflection": {
            "did_well": "What I did well: _________________________________________",
            "would_improve": "What I would improve: ____________________________________"
        }
    }

    for criterion in template["criteria"]:
        rubric["criteria"].append({
            "name": criterion.name,
            "levels": {
                "exemplary_4": criterion.exemplary,
                "proficient_3": criterion.proficient,
                "developing_2": criterion.developing,
                "beginning_1": criterion.beginning
            }
        })

    return rubric


def _get_closest_template(activity_name: str) -> str:
    """Find closest matching template for an unknown activity."""
    activity_lower = activity_name.lower()

    if any(word in activity_lower for word in ["analysis", "chart", "map", "tree", "inventory"]):
        return "character_motivation_chart"
    elif any(word in activity_lower for word in ["discussion", "debate", "hot seat", "fishbowl"]):
        return "fishbowl_discussion"
    elif any(word in activity_lower for word in ["performance", "staging", "blocking", "rehearsal"]):
        return "scene_performance_prep"
    elif any(word in activity_lower for word in ["writing", "translation", "gallery"]):
        return "modern_translation"
    else:
        return "character_motivation_chart"


def validate_rubric(rubric: Dict) -> Dict:
    """
    Validate a rubric against generation rules.

    Rules:
    - R1: Criteria must align to day's learning objectives
    - R2: Must use 4-point scale (not percentages)
    - R3: Descriptors must be specific and observable
    - R4: Must include student self-reflection section
    - R5: Must fit on one page

    Returns:
        Dict with validation status and any issues found
    """
    issues = []

    # R2: Check 4-point scale
    for criterion in rubric.get("criteria", []):
        levels = criterion.get("levels", {})
        if len(levels) != 4:
            issues.append(f"Criterion '{criterion['name']}' does not have 4 levels")

        # R3: Check descriptor length (should be specific, not too short)
        for level_name, description in levels.items():
            if len(description) < 20:
                issues.append(f"Descriptor for '{criterion['name']}' {level_name} may be too vague")

    # R4: Check self-reflection section
    if "student_reflection" not in rubric:
        issues.append("Missing student self-reflection section")

    # R5: Check one-page fit (estimate based on content)
    total_text = sum(
        len(c["levels"]["exemplary_4"]) + len(c["levels"]["proficient_3"]) +
        len(c["levels"]["developing_2"]) + len(c["levels"]["beginning_1"])
        for c in rubric.get("criteria", [])
    )
    if total_text > 2000:  # Rough estimate for one page
        issues.append("Rubric may exceed one page - consider condensing descriptors")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "rubric": rubric
    }


def generate_rubric_markdown(rubric: Dict) -> str:
    """Generate markdown format of the rubric for output."""
    lines = [
        f"# {rubric['header']['title']}",
        "",
        f"{rubric['header']['date_line']}",
        f"{rubric['header']['name_line']}",
        "",
        "## Criteria",
        "",
        "| Criterion | Exemplary (4) | Proficient (3) | Developing (2) | Beginning (1) |",
        "|-----------|---------------|----------------|----------------|---------------|"
    ]

    for criterion in rubric["criteria"]:
        levels = criterion["levels"]
        lines.append(
            f"| {criterion['name']} | {levels['exemplary_4']} | "
            f"{levels['proficient_3']} | {levels['developing_2']} | {levels['beginning_1']} |"
        )

    lines.extend([
        "",
        f"## Total Score: ___/{rubric['total_points']} points",
        "",
        "### Grade Equivalents",
    ])

    for grade, range_str in rubric["grade_equivalents"].items():
        lines.append(f"- {grade}: {range_str} points")

    lines.extend([
        "",
        "## Feedback",
        "",
        rubric["feedback_section"]["strengths"],
        rubric["feedback_section"]["growth_areas"],
        rubric["feedback_section"]["next_steps"],
        "",
        "## Student Reflection",
        "",
        rubric["student_reflection"]["did_well"],
        rubric["student_reflection"]["would_improve"]
    ])

    return "\n".join(lines)


def generate_all_rubrics() -> List[Dict]:
    """Generate rubrics for all activities in the Romeo and Juliet unit."""
    from .instruction_integrator import ROMEO_AND_JULIET_STRUCTURE

    rubrics = []

    for day_num, day_info in ROMEO_AND_JULIET_STRUCTURE.items():
        activity = day_info.get("activity")
        if activity:
            activity_name = activity.split("→")[0].strip() if "→" in activity else activity
            rubric = generate_rubric(
                day=int(day_num.replace("day_", "")),
                activity_name=activity_name,
                objectives=day_info.get("objectives", [])
            )
            validation = validate_rubric(rubric)
            rubric["validation"] = validation
            rubrics.append(rubric)

    return rubrics


# Export main components
__all__ = [
    'generate_rubric',
    'validate_rubric',
    'generate_rubric_markdown',
    'generate_all_rubrics',
    'RUBRIC_TEMPLATES',
    'ACTIVITY_TO_RUBRIC',
    'Rubric',
    'RubricCriterion'
]
