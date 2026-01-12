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

# HARDCODED: Performance tips for theater-relevant content
PERFORMANCE_TIPS = {
    "blocking": [
        "When blocking a scene, always know where your light source is - never turn your back to it!",
        "Stage movement should have purpose. Every step should mean something to your character.",
        "Cross downstage (toward audience) on important lines to draw focus.",
    ],
    "voice": [
        "Project from your diaphragm, not your throat. Your voice should fill the space!",
        "Vary your pace - slow down for emotional moments, speed up for excitement.",
        "The last word of a line often carries the most meaning. Land it with intention.",
    ],
    "character": [
        "Your character exists even when not speaking. React to everything happening on stage.",
        "Find your character's 'center' - where do they hold tension in their body?",
        "Ask yourself: What does my character want in this scene? What's stopping them?",
    ],
    "verse_speaking": [
        "In iambic pentameter, stressed syllables often carry the emotional weight of the line.",
        "Don't pause at the end of every line - follow the punctuation, not the line breaks.",
        "Antithesis (opposing ideas) should be physically and vocally contrasted.",
    ],
    "fight_scenes": [
        "Stage combat is choreographed like a dance. Safety first, drama second!",
        "The 'victim' controls the fight - they react to make hits look real.",
        "Eye contact with your scene partner keeps stage combat safe and connected.",
    ],
    "emotion": [
        "Don't 'play' an emotion - play an action. Emotions come from pursuing objectives.",
        "Shakespeare's characters often say the opposite of what they feel. Look for the subtext!",
        "Physical actions can unlock emotional truth. Try the gesture, feel the feeling.",
    ],
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
            return {
                "success": True,
                "fact": fact["fact"],
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
                return {
                    "success": True,
                    "fact": fact["fact"],
                    "tone": fact["tone"],
                    "tags": fact.get("tags", []),
                    "category": "general",
                }

            return {
                "success": False,
                "error": "No facts available"
            }

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
    HARDCODED agent for generating performance tips.

    Provides relevant tips for slides with performance applications.
    """

    def __init__(self):
        super().__init__(name="PerformanceTipGeneratorAgent")
        self._used_tips = set()

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a performance tip based on slide content."""
        slide_content = context.get("slide_content", "")
        slide_title = context.get("slide_title", "")
        exclude_tips = context.get("exclude_tips", [])

        full_content = f"{slide_title} {slide_content}".lower()

        # Determine relevant tip categories
        categories = self._determine_tip_categories(full_content)

        if not categories:
            return {
                "success": False,
                "has_performance_application": False,
                "reason": "No performance application for this content"
            }

        # Select a tip
        tip = self._select_tip(categories, exclude_tips)

        if tip:
            return {
                "success": True,
                "has_performance_application": True,
                "tip": tip["tip"],
                "category": tip["category"],
            }

        return {
            "success": False,
            "has_performance_application": True,
            "reason": "All tips exhausted for this category"
        }

    def _determine_tip_categories(self, content: str) -> List[str]:
        """Determine which performance tip categories are relevant."""
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

    def _select_tip(self, categories: List[str], exclude_tips: List[str]) -> Optional[Dict]:
        """Select a performance tip from relevant categories."""
        candidates = []

        for category in categories:
            if category in PERFORMANCE_TIPS:
                for tip in PERFORMANCE_TIPS[category]:
                    if tip not in exclude_tips and tip not in self._used_tips:
                        candidates.append({
                            "tip": tip,
                            "category": category
                        })

        if candidates:
            selected = random.choice(candidates)
            self._used_tips.add(selected["tip"])
            return selected

        return None

    def reset_used_tips(self):
        """Reset used tips tracker."""
        self._used_tips.clear()


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
        """Enhance slide with either performance tip or fun fact."""
        slide_content = context.get("slide_content", "")
        slide_title = context.get("slide_title", "")
        force_fact = context.get("force_fact", False)  # Always use fact
        force_tip = context.get("force_tip", False)    # Always use tip

        # First, try to get a performance tip (unless forced to use fact)
        if not force_fact:
            tip_result = self.tip_generator.execute({
                "slide_content": slide_content,
                "slide_title": slide_title,
            })

            if tip_result.output.get("has_performance_application") and tip_result.output.get("success"):
                return {
                    "success": True,
                    "enhancement_type": "performance_tip",
                    "content": tip_result.output["tip"],
                    "category": tip_result.output.get("category"),
                    "label": "Performance Tip"
                }

        # If no performance tip applicable (or forced), use fun fact
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
                    "label": "Did You Know?"
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
        self.tip_generator.reset_used_tips()

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
        self.tip_generator.reset_used_tips()


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
