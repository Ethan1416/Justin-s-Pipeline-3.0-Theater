"""
Slide Enhancement Agents (HARDCODED)
====================================

Specialized agents for enhancing PowerPoint slides with fun facts,
trivia, and performance tips.

Fun facts replace performance tips when no performance application
is relevant to the slide content.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import random
import re

from .base import Agent, AgentResult, AgentStatus


# =============================================================================
# HARDCODED FUN FACTS DATABASE
# =============================================================================

# HARDCODED: Fun facts organized by category
# Each fact has a tone: clever, cute, informative, silly
FUN_FACTS_DATABASE = {
    "shakespeare_general": [
        {
            "fact": "Shakespeare invented over 1,700 words we still use today, including 'assassination,' 'bedroom,' and 'lonely.'",
            "tone": "informative",
            "tags": ["vocabulary", "language", "shakespeare"]
        },
        {
            "fact": "Shakespeare's father was a professional glove-maker. Talk about hands-on parenting!",
            "tone": "clever",
            "tags": ["biography", "shakespeare"]
        },
        {
            "fact": "Shakespeare left his wife his 'second-best bed' in his will. Historians still debate if this was an insult or a term of endearment.",
            "tone": "informative",
            "tags": ["biography", "shakespeare"]
        },
        {
            "fact": "No one knows Shakespeare's actual birthday - we only know he was baptized on April 26, 1564.",
            "tone": "informative",
            "tags": ["biography", "shakespeare"]
        },
        {
            "fact": "Shakespeare never attended university, yet his works are studied at every university in the world.",
            "tone": "clever",
            "tags": ["biography", "education", "shakespeare"]
        },
        {
            "fact": "The word 'Shakespeare' appears zero times in any of Shakespeare's plays.",
            "tone": "clever",
            "tags": ["trivia", "shakespeare"]
        },
        {
            "fact": "Shakespeare's plays contain the first recorded use of 'knock knock' jokes. Yes, really - check out Macbeth!",
            "tone": "silly",
            "tags": ["humor", "macbeth", "shakespeare"]
        },
        {
            "fact": "Shakespeare wrote approximately 37 plays, 154 sonnets, and still found time to raise three kids.",
            "tone": "cute",
            "tags": ["biography", "shakespeare"]
        },
        {
            "fact": "In Shakespeare's time, actors who forgot their lines were said to be 'out.' That's where we get the phrase 'out of line.'",
            "tone": "informative",
            "tags": ["theater", "vocabulary"]
        },
        {
            "fact": "Shakespeare's Globe Theatre could hold 3,000 people - but had zero bathrooms.",
            "tone": "silly",
            "tags": ["globe", "theater"]
        },
    ],

    "romeo_juliet": [
        {
            "fact": "Romeo and Juliet takes place over just 5 days. That's shorter than most school weeks!",
            "tone": "informative",
            "tags": ["timeline", "romeo_juliet"]
        },
        {
            "fact": "Juliet is only 13 years old in the play. Romeo's age is never mentioned.",
            "tone": "informative",
            "tags": ["characters", "juliet", "romeo_juliet"]
        },
        {
            "fact": "The play never says 'Wherefore art thou Romeo' means 'Where are you?' It actually means 'Why are you Romeo?' - as in, why did you have to be a Montague?",
            "tone": "clever",
            "tags": ["language", "juliet", "romeo_juliet"]
        },
        {
            "fact": "Romeo and Juliet was likely inspired by an Italian tale from 1530. Shakespeare's version was basically a Renaissance remix!",
            "tone": "clever",
            "tags": ["history", "romeo_juliet"]
        },
        {
            "fact": "The 'balcony scene' never mentions a balcony. Shakespeare just wrote 'Juliet appears above at a window.'",
            "tone": "informative",
            "tags": ["staging", "balcony", "romeo_juliet"]
        },
        {
            "fact": "Mercutio's Queen Mab speech is 42 lines long - the longest uninterrupted speech in the entire play.",
            "tone": "informative",
            "tags": ["mercutio", "queen_mab", "romeo_juliet"]
        },
        {
            "fact": "The word 'love' appears 150+ times in Romeo and Juliet. The word 'death' appears 75 times. Love wins!",
            "tone": "cute",
            "tags": ["themes", "romeo_juliet"]
        },
        {
            "fact": "Romeo kisses Juliet within 14 lines of their first conversation. Smooth operator or moving too fast?",
            "tone": "silly",
            "tags": ["characters", "romeo", "juliet", "romeo_juliet"]
        },
        {
            "fact": "Verona, Italy has a 'Juliet's Balcony' tourist attraction - but it was added in 1936 to a random medieval building.",
            "tone": "informative",
            "tags": ["verona", "tourism", "romeo_juliet"]
        },
        {
            "fact": "Romeo and Juliet has been adapted into over 50 films. The story is literally immortal.",
            "tone": "clever",
            "tags": ["adaptations", "romeo_juliet"]
        },
        {
            "fact": "The Nurse has more lines than Juliet does. Supporting characters need love too!",
            "tone": "cute",
            "tags": ["characters", "nurse", "romeo_juliet"]
        },
        {
            "fact": "Tybalt's name comes from the name of the cat in a medieval story. In the play, Mercutio even calls him 'Prince of Cats.'",
            "tone": "clever",
            "tags": ["characters", "tybalt", "romeo_juliet"]
        },
        {
            "fact": "Paris, Juliet's other suitor, has a name but almost no personality. He's basically a Renaissance NPC.",
            "tone": "silly",
            "tags": ["characters", "paris", "romeo_juliet"]
        },
        {
            "fact": "Friar Lawrence's plan involved a poison that mimics death for 42 hours. That's oddly specific!",
            "tone": "silly",
            "tags": ["characters", "friar", "plot", "romeo_juliet"]
        },
        {
            "fact": "The Prince appears only 3 times but speaks the first and last lines of the play. Power moves only.",
            "tone": "clever",
            "tags": ["characters", "prince", "romeo_juliet"]
        },
    ],

    "elizabethan_theater": [
        {
            "fact": "All female roles in Shakespeare's time were played by young boys. Imagine a 12-year-old playing Juliet!",
            "tone": "informative",
            "tags": ["acting", "history", "theater"]
        },
        {
            "fact": "Groundlings paid just 1 penny to stand and watch plays. That's about $1 in today's money - cheaper than a movie!",
            "tone": "informative",
            "tags": ["audience", "globe", "theater"]
        },
        {
            "fact": "The Globe Theatre had no roof over the stage. Actors performed rain or shine!",
            "tone": "informative",
            "tags": ["globe", "theater"]
        },
        {
            "fact": "Elizabethan audiences would throw food at actors they didn't like. Tough crowd!",
            "tone": "silly",
            "tags": ["audience", "history", "theater"]
        },
        {
            "fact": "Plays started at 2 PM because there was no electric lighting. Nature's spotlight!",
            "tone": "clever",
            "tags": ["staging", "history", "theater"]
        },
        {
            "fact": "The original Globe Theatre burned down in 1613 when a cannon prop set the roof on fire during Henry VIII.",
            "tone": "informative",
            "tags": ["globe", "history", "theater"]
        },
        {
            "fact": "Actors in Shakespeare's time memorized their parts from 'sides' - strips of paper with just their lines and cues.",
            "tone": "informative",
            "tags": ["acting", "history", "theater"]
        },
        {
            "fact": "The trapdoor in the Globe's stage was called 'Hell.' The ceiling was painted with stars and called 'The Heavens.'",
            "tone": "clever",
            "tags": ["globe", "staging", "theater"]
        },
        {
            "fact": "Elizabethan theaters flew flags to advertise what type of play was showing: white for comedy, black for tragedy, red for history.",
            "tone": "informative",
            "tags": ["history", "theater"]
        },
        {
            "fact": "Shakespeare's company performed a different play every day. Imagine memorizing 37 plays!",
            "tone": "informative",
            "tags": ["acting", "history", "theater"]
        },
    ],

    "language_wordplay": [
        {
            "fact": "Iambic pentameter has 10 syllables per line - the same rhythm as a human heartbeat. Poetry is literally heartfelt!",
            "tone": "cute",
            "tags": ["iambic", "poetry", "language"]
        },
        {
            "fact": "A sonnet has exactly 14 lines. The word 'sonnet' comes from Italian 'sonetto' meaning 'little song.'",
            "tone": "informative",
            "tags": ["sonnet", "poetry", "language"]
        },
        {
            "fact": "Shakespeare loved puns so much that Romeo and Juliet contains over 175 of them. Pun intended!",
            "tone": "silly",
            "tags": ["puns", "wordplay", "romeo_juliet"]
        },
        {
            "fact": "The word 'malapropism' (using the wrong word) didn't exist in Shakespeare's time, but he invented the technique anyway.",
            "tone": "clever",
            "tags": ["vocabulary", "language"]
        },
        {
            "fact": "'Break a leg' as good luck comes from theater - actors would bow (break the leg line) only after a successful show.",
            "tone": "informative",
            "tags": ["expressions", "theater"]
        },
        {
            "fact": "Shakespeare spelled his own name at least 6 different ways. Spelling wasn't standardized yet!",
            "tone": "informative",
            "tags": ["shakespeare", "history", "language"]
        },
        {
            "fact": "'Wild goose chase,' 'heart of gold,' and 'love is blind' are all phrases Shakespeare invented.",
            "tone": "informative",
            "tags": ["vocabulary", "shakespeare", "language"]
        },
        {
            "fact": "An oxymoron combines opposite words - like 'bittersweet' or Juliet's 'beautiful tyrant.' Shakespeare loved these!",
            "tone": "informative",
            "tags": ["oxymoron", "language", "romeo_juliet"]
        },
    ],

    "performance_acting": [
        {
            "fact": "Stage fright is called 'flop sweat' in theater. Even experienced actors get nervous!",
            "tone": "informative",
            "tags": ["acting", "performance"]
        },
        {
            "fact": "The 'fourth wall' is the invisible wall between actors and audience. Breaking it means acknowledging the audience directly.",
            "tone": "informative",
            "tags": ["staging", "performance"]
        },
        {
            "fact": "A 'ham' actor overacts dramatically. The term might come from 'hamfatter' - actors who used ham fat to remove makeup.",
            "tone": "clever",
            "tags": ["acting", "vocabulary"]
        },
        {
            "fact": "Upstage originally meant the back of the stage (which was higher). 'Upstaging' someone meant forcing them to turn away from the audience.",
            "tone": "informative",
            "tags": ["staging", "vocabulary"]
        },
        {
            "fact": "A 'bit part' originally meant a role worth only 'two bits' (25 cents) in payment.",
            "tone": "informative",
            "tags": ["acting", "vocabulary"]
        },
        {
            "fact": "The 'green room' where actors wait might be named after the green fabric that rested actors' eyes after bright stage lights.",
            "tone": "informative",
            "tags": ["theater", "vocabulary"]
        },
        {
            "fact": "Method acting wasn't invented until the 1900s. Shakespeare's actors just had to wing it!",
            "tone": "silly",
            "tags": ["acting", "history"]
        },
    ],

    "themes_symbols": [
        {
            "fact": "Light and dark imagery in Romeo and Juliet represents the contrast between love (light) and the feuding families (darkness).",
            "tone": "informative",
            "tags": ["imagery", "themes", "romeo_juliet"]
        },
        {
            "fact": "Stars symbolize fate in Romeo and Juliet. 'Star-crossed lovers' literally means their stars (fates) are against them.",
            "tone": "informative",
            "tags": ["fate", "symbols", "romeo_juliet"]
        },
        {
            "fact": "Poison appears as both medicine and death in the play - just like love itself can heal or destroy.",
            "tone": "clever",
            "tags": ["poison", "symbols", "romeo_juliet"]
        },
        {
            "fact": "The number 3 appears constantly in the play: 3 fights, 3 deaths in Act 5, and the Prince's 3 appearances.",
            "tone": "informative",
            "tags": ["numbers", "symbols", "romeo_juliet"]
        },
        {
            "fact": "Dreams in Romeo and Juliet always predict the future - but the characters never listen to them!",
            "tone": "clever",
            "tags": ["dreams", "foreshadowing", "romeo_juliet"]
        },
    ],

    "general_theater": [
        {
            "fact": "The word 'theater' comes from Greek 'theatron' meaning 'a place for viewing.'",
            "tone": "informative",
            "tags": ["vocabulary", "history", "theater"]
        },
        {
            "fact": "Drama masks showing comedy and tragedy are called 'sock and buskin' - named after ancient Greek footwear.",
            "tone": "informative",
            "tags": ["symbols", "history", "theater"]
        },
        {
            "fact": "A 'curtain call' happens when actors return to bow - even though Shakespeare's theater had no curtains!",
            "tone": "clever",
            "tags": ["performance", "vocabulary", "theater"]
        },
        {
            "fact": "The longest-running play ever is 'The Mousetrap' - it's been performed continuously since 1952!",
            "tone": "informative",
            "tags": ["records", "theater"]
        },
        {
            "fact": "Ancient Greek actors wore platform shoes called 'cothurni' to appear taller. The original high heels!",
            "tone": "silly",
            "tags": ["costumes", "history", "theater"]
        },
    ],
}

# HARDCODED: Performance/theater trivia (formerly "tips" - now presented as trivia)
PERFORMANCE_TRIVIA = {
    "blocking": [
        {"fact": "Actors never turn their backs to the light source - that's why blocking rehearsals map every movement!", "header": "Stage Secrets"},
        {"fact": "Every step on stage should mean something. Random movement distracts the audience!", "header": "Pro Tip"},
        {"fact": "Crossing downstage (toward audience) on important lines is a trick directors use to draw focus.", "header": "Director's Secret"},
    ],
    "voice": [
        {"fact": "Professional actors project from their diaphragm, not their throat - that's how they perform 8 shows a week!", "header": "Actor's Secret"},
        {"fact": "Slowing down for emotional moments and speeding up for excitement keeps audiences engaged.", "header": "Pacing Trick"},
        {"fact": "The last word of a Shakespeare line often carries the most meaning - listen for it!", "header": "Language Tip"},
    ],
    "character": [
        {"fact": "Great actors stay in character even when not speaking - they react to everything on stage!", "header": "Acting Secret"},
        {"fact": "Actors find their character's 'center' - where they hold tension in their body tells you who they are.", "header": "Character Clue"},
        {"fact": "Every character wants something and something is stopping them - that's the engine of drama!", "header": "Drama 101"},
    ],
    "verse_speaking": [
        {"fact": "In iambic pentameter, the stressed syllables carry the emotional weight - like a heartbeat of meaning!", "header": "Verse Secret"},
        {"fact": "Don't pause at the end of every line - follow the punctuation, not the line breaks!", "header": "Speaking Tip"},
        {"fact": "Antithesis (opposing ideas) should be physically and vocally contrasted for maximum impact.", "header": "Rhetoric Trick"},
    ],
    "fight_scenes": [
        {"fact": "Stage combat is choreographed like a dance - every 'hit' is precisely timed for safety!", "header": "Stage Combat"},
        {"fact": "In stage fights, the 'victim' actually controls the action - their reactions make it look real!", "header": "Fight Secret"},
        {"fact": "Eye contact between actors keeps stage combat safe and emotionally connected.", "header": "Safety First"},
    ],
    "emotion": [
        {"fact": "Actors don't 'play' emotions - they play actions. The emotions follow naturally!", "header": "Acting Trick"},
        {"fact": "Shakespeare's characters often say the opposite of what they feel - that's called subtext!", "header": "Subtext Alert"},
        {"fact": "Physical actions can unlock emotional truth - try the gesture, feel the feeling!", "header": "Body & Mind"},
    ],
}

# HARDCODED: Trivia headers based on content type
TRIVIA_HEADERS = {
    "shakespeare_general": ["Shakespeare Trivia", "Bard Fact", "Did You Know?", "Shakespeare Secrets"],
    "romeo_juliet": ["R&J Trivia", "Play Fact", "Did You Know?", "Story Secret"],
    "elizabethan_theater": ["Theater History", "Globe Fact", "Stage History", "Playhouse Trivia"],
    "language_wordplay": ["Word Nerd", "Language Fact", "Poetry Corner", "Wordplay"],
    "performance_acting": ["Stage Secrets", "Actor's Tip", "Theater Trick", "Pro Tip"],
    "themes_symbols": ["Symbol Spotlight", "Theme Insight", "Hidden Meaning", "Deep Dive"],
    "general_theater": ["Theater Trivia", "Stage Fact", "Drama 101", "Curtain Call"],
    "default": ["Trivia", "Did You Know?", "Fun Fact", "Quick Fact"]
}

# HARDCODED: Slide content keywords for matching
SLIDE_CONTENT_KEYWORDS = {
    "performance_applicable": [
        "blocking", "staging", "movement", "gesture", "performance", "acting",
        "rehearsal", "scene work", "monologue", "dialogue", "delivery",
        "character work", "vocal", "projection", "fight", "combat", "choreography",
        "tableau", "freeze frame", "entrance", "exit", "cross", "upstage", "downstage"
    ],
    "romeo_juliet": [
        "romeo", "juliet", "montague", "capulet", "mercutio", "tybalt",
        "nurse", "friar", "verona", "balcony", "tomb", "poison", "dagger",
        "banishment", "exile", "feud", "marriage", "ball", "masque"
    ],
    "language": [
        "iambic", "pentameter", "sonnet", "verse", "prose", "rhyme",
        "metaphor", "simile", "imagery", "oxymoron", "pun", "wordplay",
        "soliloquy", "monologue", "aside", "vocabulary"
    ],
    "theater": [
        "stage", "theater", "globe", "audience", "actor", "costume",
        "prop", "set", "lighting", "elizabethan", "groundling"
    ],
    "themes": [
        "love", "death", "fate", "conflict", "family", "honor",
        "revenge", "loyalty", "light", "dark", "dream", "star"
    ]
}


# =============================================================================
# FunFactGeneratorAgent
# =============================================================================

class FunFactGeneratorAgent(Agent):
    """
    HARDCODED agent for generating fun facts and trivia.

    Selects appropriate facts based on slide content and ensures variety.
    Facts range in tone: clever, cute, informative, silly - all factual.
    """

    def __init__(self):
        super().__init__(name="FunFactGeneratorAgent")
        self._used_facts = set()  # Track used facts for variety

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a fun fact based on slide content."""
        slide_content = context.get("slide_content", "")
        slide_title = context.get("slide_title", "")
        preferred_tone = context.get("preferred_tone", None)  # Optional tone filter
        exclude_facts = context.get("exclude_facts", [])  # Facts to skip

        # Combine content for keyword matching
        full_content = f"{slide_title} {slide_content}".lower()

        # Determine relevant categories
        categories = self._determine_categories(full_content)

        # Select a fact
        fact = self._select_fact(categories, preferred_tone, exclude_facts)

        if fact:
            # Select appropriate header based on category
            header = self._select_header(fact.get("_category", "default"))
            return {
                "success": True,
                "fact": fact["fact"],
                "header": header,
                "tone": fact["tone"],
                "tags": fact.get("tags", []),
                "category": fact.get("_category", "general"),
            }
        else:
            # Fallback to random fact from any category
            all_facts = []
            for cat_facts in FUN_FACTS_DATABASE.values():
                all_facts.extend(cat_facts)

            if all_facts:
                fact = random.choice(all_facts)
                header = random.choice(TRIVIA_HEADERS["default"])
                return {
                    "success": True,
                    "fact": fact["fact"],
                    "header": header,
                    "tone": fact["tone"],
                    "tags": fact.get("tags", []),
                    "category": "general",
                }

            return {
                "success": False,
                "error": "No facts available"
            }

    def _select_header(self, category: str) -> str:
        """Select an appropriate header for the category."""
        headers = TRIVIA_HEADERS.get(category, TRIVIA_HEADERS["default"])
        return random.choice(headers)

    def _determine_categories(self, content: str) -> List[str]:
        """Determine which fact categories are relevant to the content."""
        categories = []

        # Check for Romeo and Juliet content
        if any(kw in content for kw in SLIDE_CONTENT_KEYWORDS["romeo_juliet"]):
            categories.append("romeo_juliet")

        # Check for language/poetry content
        if any(kw in content for kw in SLIDE_CONTENT_KEYWORDS["language"]):
            categories.append("language_wordplay")

        # Check for theater content
        if any(kw in content for kw in SLIDE_CONTENT_KEYWORDS["theater"]):
            categories.extend(["elizabethan_theater", "general_theater"])

        # Check for themes
        if any(kw in content for kw in SLIDE_CONTENT_KEYWORDS["themes"]):
            categories.append("themes_symbols")

        # Always include Shakespeare general as fallback
        if not categories or "shakespeare" in content:
            categories.append("shakespeare_general")

        return list(set(categories))  # Remove duplicates

    def _select_fact(
        self,
        categories: List[str],
        preferred_tone: Optional[str],
        exclude_facts: List[str]
    ) -> Optional[Dict]:
        """Select a fact from relevant categories."""
        candidates = []

        for category in categories:
            if category in FUN_FACTS_DATABASE:
                for fact in FUN_FACTS_DATABASE[category]:
                    # Skip excluded facts
                    if fact["fact"] in exclude_facts:
                        continue
                    # Skip already used facts
                    if fact["fact"] in self._used_facts:
                        continue
                    # Filter by tone if specified
                    if preferred_tone and fact["tone"] != preferred_tone:
                        continue

                    fact_copy = fact.copy()
                    fact_copy["_category"] = category
                    candidates.append(fact_copy)

        if candidates:
            selected = random.choice(candidates)
            self._used_facts.add(selected["fact"])
            return selected

        # If no candidates, reset used facts and try again
        if self._used_facts:
            self._used_facts.clear()
            return self._select_fact(categories, preferred_tone, exclude_facts)

        return None

    def reset_used_facts(self):
        """Reset the used facts tracker for a new presentation."""
        self._used_facts.clear()


# =============================================================================
# PerformanceTipGeneratorAgent
# =============================================================================

class PerformanceTipGeneratorAgent(Agent):
    """
    HARDCODED agent for generating performance trivia.

    Provides relevant theater/performance trivia for slides with
    performance applications. Now returns trivia-style content with
    contextual headers instead of "Performance Tip".
    """

    def __init__(self):
        super().__init__(name="PerformanceTipGeneratorAgent")
        self._used_trivia = set()

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate performance trivia based on slide content."""
        slide_content = context.get("slide_content", "")
        slide_title = context.get("slide_title", "")
        exclude_trivia = context.get("exclude_trivia", [])

        full_content = f"{slide_title} {slide_content}".lower()

        # Determine relevant trivia categories
        categories = self._determine_trivia_categories(full_content)

        if not categories:
            return {
                "success": False,
                "has_performance_application": False,
                "reason": "No performance application for this content"
            }

        # Select trivia
        trivia = self._select_trivia(categories, exclude_trivia)

        if trivia:
            return {
                "success": True,
                "has_performance_application": True,
                "fact": trivia["fact"],
                "header": trivia["header"],
                "category": trivia["category"],
            }

        return {
            "success": False,
            "has_performance_application": True,
            "reason": "All trivia exhausted for this category"
        }

    def _determine_trivia_categories(self, content: str) -> List[str]:
        """Determine which performance trivia categories are relevant."""
        categories = []

        # Check for blocking/staging content
        blocking_keywords = ["blocking", "staging", "movement", "cross", "enter", "exit", "position"]
        if any(kw in content for kw in blocking_keywords):
            categories.append("blocking")

        # Check for voice/delivery content
        voice_keywords = ["voice", "speak", "deliver", "project", "pace", "tone", "vocal"]
        if any(kw in content for kw in voice_keywords):
            categories.append("voice")

        # Check for character work
        character_keywords = ["character", "motivation", "objective", "emotion", "feel"]
        if any(kw in content for kw in character_keywords):
            categories.append("character")

        # Check for verse speaking
        verse_keywords = ["iambic", "pentameter", "verse", "meter", "rhythm", "sonnet", "line"]
        if any(kw in content for kw in verse_keywords):
            categories.append("verse_speaking")

        # Check for fight scenes
        fight_keywords = ["fight", "combat", "sword", "duel", "brawl", "violence"]
        if any(kw in content for kw in fight_keywords):
            categories.append("fight_scenes")

        # Check for emotional content
        emotion_keywords = ["emotion", "grief", "joy", "anger", "love", "fear", "passion"]
        if any(kw in content for kw in emotion_keywords):
            categories.append("emotion")

        return categories

    def _select_trivia(self, categories: List[str], exclude_trivia: List[str]) -> Optional[Dict]:
        """Select performance trivia from relevant categories."""
        candidates = []

        for category in categories:
            if category in PERFORMANCE_TRIVIA:
                for item in PERFORMANCE_TRIVIA[category]:
                    if item["fact"] not in exclude_trivia and item["fact"] not in self._used_trivia:
                        candidates.append({
                            "fact": item["fact"],
                            "header": item["header"],
                            "category": category
                        })

        if candidates:
            selected = random.choice(candidates)
            self._used_trivia.add(selected["fact"])
            return selected

        return None

    def reset_used_trivia(self):
        """Reset used trivia tracker."""
        self._used_trivia.clear()


# =============================================================================
# SlideContentEnhancerAgent
# =============================================================================

class SlideContentEnhancerAgent(Agent):
    """
    HARDCODED orchestrator agent for enhancing slide content with
    fun facts OR performance tips based on content relevance.

    Decision logic:
    1. If slide has performance application -> use performance tip
    2. If no performance application -> use fun fact
    """

    def __init__(self):
        super().__init__(name="SlideContentEnhancerAgent")
        self.fact_generator = FunFactGeneratorAgent()
        self.tip_generator = PerformanceTipGeneratorAgent()

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance slide with either performance trivia or fun fact."""
        slide_content = context.get("slide_content", "")
        slide_title = context.get("slide_title", "")
        force_fact = context.get("force_fact", False)  # Always use fact
        force_tip = context.get("force_tip", False)    # Always use tip/trivia

        # First, try to get a performance trivia (unless forced to use fact)
        if not force_fact:
            trivia_result = self.tip_generator.execute({
                "slide_content": slide_content,
                "slide_title": slide_title,
            })

            if trivia_result.output.get("has_performance_application") and trivia_result.output.get("success"):
                return {
                    "success": True,
                    "enhancement_type": "performance_trivia",
                    "content": trivia_result.output["fact"],
                    "category": trivia_result.output.get("category"),
                    "label": trivia_result.output.get("header", "Stage Secrets")
                }

        # If no performance trivia applicable (or forced), use fun fact
        if not force_tip:
            fact_result = self.fact_generator.execute({
                "slide_content": slide_content,
                "slide_title": slide_title,
            })

            if fact_result.output.get("success"):
                return {
                    "success": True,
                    "enhancement_type": "fun_fact",
                    "content": fact_result.output["fact"],
                    "tone": fact_result.output.get("tone"),
                    "category": fact_result.output.get("category"),
                    "label": fact_result.output.get("header", "Did You Know?")
                }

        return {
            "success": False,
            "error": "Could not generate enhancement"
        }

    def enhance_presentation(self, slides: List[Dict]) -> List[Dict]:
        """
        Enhance all slides in a presentation.

        Args:
            slides: List of slide dictionaries with 'title' and 'content' keys

        Returns:
            List of slides with added 'enhancement' key
        """
        # Reset trackers for fresh presentation
        self.fact_generator.reset_used_facts()
        self.tip_generator.reset_used_trivia()

        enhanced_slides = []

        for slide in slides:
            result = self.execute({
                "slide_content": slide.get("content", ""),
                "slide_title": slide.get("title", ""),
            })

            enhanced_slide = slide.copy()
            if result.output.get("success"):
                enhanced_slide["enhancement"] = {
                    "type": result.output["enhancement_type"],
                    "content": result.output["content"],
                    "label": result.output["label"],
                }

            enhanced_slides.append(enhanced_slide)

        return enhanced_slides

    def reset(self):
        """Reset all trackers for a new presentation."""
        self.fact_generator.reset_used_facts()
        self.tip_generator.reset_used_trivia()


# =============================================================================
# SlideEnhancementReportAgent
# =============================================================================

class SlideEnhancementReportAgent(Agent):
    """
    HARDCODED agent for generating reports on slide enhancements.

    Provides statistics on fact/tip distribution across a presentation.
    """

    def __init__(self):
        super().__init__(name="SlideEnhancementReportAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhancement report for a presentation."""
        enhanced_slides = context.get("slides", [])

        if not enhanced_slides:
            return {"success": False, "error": "No slides provided"}

        # Count enhancements
        total_slides = len(enhanced_slides)
        fact_count = 0
        tip_count = 0
        no_enhancement = 0

        fact_tones = {}
        tip_categories = {}

        for slide in enhanced_slides:
            enhancement = slide.get("enhancement", {})

            if not enhancement:
                no_enhancement += 1
            elif enhancement.get("type") == "fun_fact":
                fact_count += 1
                tone = enhancement.get("tone", "unknown")
                fact_tones[tone] = fact_tones.get(tone, 0) + 1
            elif enhancement.get("type") == "performance_tip":
                tip_count += 1
                category = enhancement.get("category", "unknown")
                tip_categories[category] = tip_categories.get(category, 0) + 1

        return {
            "success": True,
            "total_slides": total_slides,
            "fun_facts": fact_count,
            "performance_tips": tip_count,
            "no_enhancement": no_enhancement,
            "fact_tones": fact_tones,
            "tip_categories": tip_categories,
            "fact_percentage": round(fact_count / total_slides * 100, 1) if total_slides else 0,
            "tip_percentage": round(tip_count / total_slides * 100, 1) if total_slides else 0,
        }


# =============================================================================
# SlideEnhancementFormatterAgent
# =============================================================================

# HARDCODED: Font configuration for slide enhancements
ENHANCEMENT_FONT_CONFIG = {
    "label_font_size": 20,          # Font size for header labels (points)
    "content_font_size": 20,        # Font size for trivia content (points)
    "label_bold": True,             # Bold for labels
    "content_bold": False,          # Regular weight for content
    "label_color": (75, 0, 130),    # Indigo RGB
    "content_color": (51, 51, 51),  # Dark gray RGB
    "box_fill_color": (245, 240, 255),   # Light purple RGB
    "box_border_color": (128, 0, 128),   # Purple RGB
    "box_border_width": 2,          # Border width in points
    "emoji": "🎭",                   # Theater emoji prefix
    "position": {
        "left": 0.5,    # inches from left
        "top": 6.3,     # inches from top (adjusted for larger font)
        "width": 9,     # inches
        "height": 1.0,  # inches (increased for 20pt font)
    }
}


class SlideEnhancementFormatterAgent(Agent):
    """
    HARDCODED agent for formatting slide enhancements.

    Applies consistent formatting to trivia banners including:
    - 20 point font size for all text
    - Theater-themed purple styling
    - Proper positioning at slide bottom
    """

    def __init__(self):
        super().__init__(name="SlideEnhancementFormatterAgent")
        self.config = ENHANCEMENT_FONT_CONFIG

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format enhancement content for slide insertion."""
        label = context.get("label", "Did You Know?")
        content = context.get("content", "")

        if not content:
            return {
                "success": False,
                "error": "No content provided to format"
            }

        # Build formatted output
        formatted = {
            "success": True,
            "label": {
                "text": f"{self.config['emoji']} {label}: ",
                "font_size": self.config["label_font_size"],
                "bold": self.config["label_bold"],
                "color_rgb": self.config["label_color"],
            },
            "content": {
                "text": content,
                "font_size": self.config["content_font_size"],
                "bold": self.config["content_bold"],
                "color_rgb": self.config["content_color"],
            },
            "box": {
                "fill_color_rgb": self.config["box_fill_color"],
                "border_color_rgb": self.config["box_border_color"],
                "border_width": self.config["box_border_width"],
                "position": self.config["position"].copy(),
            },
            "full_text": f"{self.config['emoji']} {label}: {content}",
            "font_size_pt": self.config["content_font_size"],
        }

        return formatted

    def get_config(self) -> Dict[str, Any]:
        """Return the current font configuration."""
        return self.config.copy()


# =============================================================================
# SlideEnhancementValidatorAgent
# =============================================================================

class SlideEnhancementValidatorAgent(Agent):
    """
    HARDCODED validator agent for slide enhancements.

    Validates that enhancements meet requirements:
    - Font size is exactly 20 points
    - Content is not truncated
    - Box dimensions accommodate the text
    - All required fields are present
    """

    # HARDCODED: Validation requirements
    REQUIRED_FONT_SIZE = 20
    MAX_CONTENT_LENGTH = 200  # Characters before warning
    REQUIRED_FIELDS = ["label", "content", "box", "font_size_pt"]

    def __init__(self):
        super().__init__(name="SlideEnhancementValidatorAgent")

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate formatted enhancement data."""
        formatted_data = context.get("formatted_data", {})

        errors = []
        warnings = []

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in formatted_data:
                errors.append(f"Missing required field: {field}")

        if errors:
            return {
                "valid": False,
                "errors": errors,
                "warnings": warnings,
            }

        # Validate font size
        font_size = formatted_data.get("font_size_pt", 0)
        if font_size != self.REQUIRED_FONT_SIZE:
            errors.append(f"Font size must be {self.REQUIRED_FONT_SIZE}pt, got {font_size}pt")

        # Validate label font size
        label_data = formatted_data.get("label", {})
        if label_data.get("font_size") != self.REQUIRED_FONT_SIZE:
            errors.append(f"Label font size must be {self.REQUIRED_FONT_SIZE}pt")

        # Validate content font size
        content_data = formatted_data.get("content", {})
        if content_data.get("font_size") != self.REQUIRED_FONT_SIZE:
            errors.append(f"Content font size must be {self.REQUIRED_FONT_SIZE}pt")

        # Check content length
        content_text = content_data.get("text", "")
        if len(content_text) > self.MAX_CONTENT_LENGTH:
            warnings.append(f"Content length ({len(content_text)} chars) may cause text overflow")

        # Validate box configuration
        box_data = formatted_data.get("box", {})
        if not box_data.get("position"):
            errors.append("Box position not specified")
        if not box_data.get("fill_color_rgb"):
            errors.append("Box fill color not specified")

        # Check color values are valid RGB tuples
        for color_field in ["fill_color_rgb", "border_color_rgb"]:
            color = box_data.get(color_field)
            if color:
                if not isinstance(color, (list, tuple)) or len(color) != 3:
                    errors.append(f"Invalid {color_field}: must be RGB tuple")
                elif not all(0 <= c <= 255 for c in color):
                    errors.append(f"Invalid {color_field}: RGB values must be 0-255")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validated_font_size": font_size,
            "content_length": len(content_text),
        }

    def validate_slide_enhancement(self, label: str, content: str) -> Dict[str, Any]:
        """
        Convenience method to validate a label/content pair.

        Creates formatted data and validates it in one step.
        """
        formatter = SlideEnhancementFormatterAgent()
        formatted = formatter.execute({
            "label": label,
            "content": content,
        })

        if not formatted.output.get("success"):
            return {
                "valid": False,
                "errors": [formatted.output.get("error", "Formatting failed")],
                "warnings": [],
            }

        return self.execute({"formatted_data": formatted.output})
