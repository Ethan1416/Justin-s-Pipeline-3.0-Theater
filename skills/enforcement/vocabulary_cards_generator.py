"""
Vocabulary Cards Generator (HARDCODED)
======================================

Generates printable vocabulary flashcards for word wall or student sets.
Includes Shakespeare-specific translations and pronunciation guides.

HARDCODED RULES (from COMPONENT_GENERATION_INSTRUCTIONS.txt):
- R1: 3-6 vocabulary terms per day
- R2: All Shakespeare terms must include pronunciation
- R3: All terms must have play-specific example
- R4: Common misconceptions must be flagged
- R5: Terms must appear in that day's reading
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


# =============================================================================
# CONSTANTS (HARDCODED - DO NOT MODIFY)
# =============================================================================

MIN_TERMS_PER_DAY = 3
MAX_TERMS_PER_DAY = 6
REQUIRED_CARD_ELEMENTS = ["term", "definition", "example", "modern_equivalent"]

# Romeo and Juliet Vocabulary Database
ROMEO_JULIET_VOCABULARY = {
    # Act 1 Vocabulary
    "wherefore": {
        "definition": "Why; for what reason",
        "pronunciation": "WAIR-for",
        "part_of_speech": "adverb",
        "example": "'Wherefore art thou Romeo?' (2.2.33)",
        "modern_equivalent": "Why",
        "misconception": "Does NOT mean 'where' - it means 'why'",
        "act": 1
    },
    "thee": {
        "definition": "You (object form, informal)",
        "pronunciation": "thee",
        "part_of_speech": "pronoun",
        "example": "'I love thee' = I love you",
        "modern_equivalent": "You",
        "misconception": None,
        "act": 1
    },
    "thou": {
        "definition": "You (subject form, informal)",
        "pronunciation": "thow",
        "part_of_speech": "pronoun",
        "example": "'Thou art a villain' = You are a villain",
        "modern_equivalent": "You",
        "misconception": "Used for close relationships or speaking down to someone",
        "act": 1
    },
    "art": {
        "definition": "Are (second person singular of 'to be')",
        "pronunciation": "art",
        "part_of_speech": "verb",
        "example": "'Wherefore art thou Romeo?' = Why are you Romeo?",
        "modern_equivalent": "Are",
        "misconception": None,
        "act": 1
    },
    "hath": {
        "definition": "Has",
        "pronunciation": "hath",
        "part_of_speech": "verb",
        "example": "'She hath not seen the change of fourteen years'",
        "modern_equivalent": "Has",
        "misconception": None,
        "act": 1
    },
    "doth": {
        "definition": "Does",
        "pronunciation": "duth",
        "part_of_speech": "verb",
        "example": "'What light through yonder window breaks? It is the east, and Juliet is the sun.'",
        "modern_equivalent": "Does",
        "misconception": None,
        "act": 1
    },
    "bite_thumb": {
        "definition": "An insulting gesture (like giving someone the finger today)",
        "pronunciation": "bite thum",
        "part_of_speech": "verb phrase",
        "example": "'Do you bite your thumb at us, sir?'",
        "modern_equivalent": "Make an obscene gesture",
        "misconception": "A deliberate provocation, not accidental",
        "act": 1
    },
    "ancient_grudge": {
        "definition": "A long-standing hatred or conflict between groups",
        "pronunciation": "AYN-shent gruj",
        "part_of_speech": "noun phrase",
        "example": "'From ancient grudge break to new mutiny'",
        "modern_equivalent": "Old feud",
        "misconception": None,
        "act": 1
    },
    "star_crossed": {
        "definition": "Destined for misfortune; opposed by fate",
        "pronunciation": "star-krossd",
        "part_of_speech": "adjective",
        "example": "'A pair of star-crossed lovers take their life'",
        "modern_equivalent": "Fated to fail, doomed",
        "misconception": "Not romantic - it means doomed by the stars",
        "act": 1
    },
    # Act 2 Vocabulary
    "soliloquy": {
        "definition": "A speech in which a character speaks their thoughts aloud while alone",
        "pronunciation": "suh-LIL-uh-kwee",
        "part_of_speech": "noun",
        "example": "Romeo's 'But soft, what light...' is a soliloquy",
        "modern_equivalent": "Thinking out loud (for the audience)",
        "misconception": "Different from a monologue - character must be alone",
        "act": 2
    },
    "aside": {
        "definition": "A remark spoken to the audience that other characters don't hear",
        "pronunciation": "uh-SIDE",
        "part_of_speech": "noun",
        "example": "When Romeo speaks to us while hiding from the Capulets",
        "modern_equivalent": "Breaking the fourth wall briefly",
        "misconception": None,
        "act": 2
    },
    "iambic_pentameter": {
        "definition": "A rhythm of 10 syllables per line: da-DUM da-DUM da-DUM da-DUM da-DUM",
        "pronunciation": "eye-AM-bik pen-TAM-uh-ter",
        "part_of_speech": "noun",
        "example": "'But SOFT what LIGHT through YON-der WIN-dow BREAKS'",
        "modern_equivalent": "Shakespeare's standard poetic rhythm",
        "misconception": "Not all lines follow this - prose has no set rhythm",
        "act": 2
    },
    "ere": {
        "definition": "Before",
        "pronunciation": "air",
        "part_of_speech": "preposition",
        "example": "'Ere the sun rise' = Before the sun rises",
        "modern_equivalent": "Before",
        "misconception": None,
        "act": 2
    },
    "anon": {
        "definition": "Soon; right away",
        "pronunciation": "uh-NON",
        "part_of_speech": "adverb",
        "example": "'I come, anon' = I'm coming right now",
        "modern_equivalent": "Coming!, Be right there!",
        "misconception": None,
        "act": 2
    },
    # Act 3 Vocabulary
    "banishment": {
        "definition": "Being forced to leave and never return",
        "pronunciation": "BAN-ish-ment",
        "part_of_speech": "noun",
        "example": "'Ha, banishment! Be merciful, say 'death''",
        "modern_equivalent": "Exile, deportation",
        "misconception": "Romeo sees this as worse than death",
        "act": 3
    },
    "exile": {
        "definition": "To be banned from one's home country or city",
        "pronunciation": "EK-zile",
        "part_of_speech": "noun/verb",
        "example": "'Romeo is banished' - exiled from Verona",
        "modern_equivalent": "Kicked out, deported",
        "misconception": None,
        "act": 3
    },
    "fray": {
        "definition": "A fight or brawl",
        "pronunciation": "fray",
        "part_of_speech": "noun",
        "example": "'Who began this bloody fray?'",
        "modern_equivalent": "Fight, brawl",
        "misconception": None,
        "act": 3
    },
    "plague": {
        "definition": "A curse; also a deadly disease",
        "pronunciation": "playg",
        "part_of_speech": "noun",
        "example": "'A plague on both your houses!'",
        "modern_equivalent": "A curse (also COVID-like disease)",
        "misconception": "Mercutio curses BOTH families, not just one",
        "act": 3
    },
    "oxymoron": {
        "definition": "A figure of speech combining contradictory terms",
        "pronunciation": "ok-see-MOR-on",
        "part_of_speech": "noun",
        "example": "'Beautiful tyrant! Fiend angelical!'",
        "modern_equivalent": "Jumbo shrimp, living dead",
        "misconception": None,
        "act": 3
    },
    # Act 4 Vocabulary
    "vial": {
        "definition": "A small glass container for liquid",
        "pronunciation": "VY-ul",
        "part_of_speech": "noun",
        "example": "The vial containing the sleeping potion",
        "modern_equivalent": "Small bottle",
        "misconception": None,
        "act": 4
    },
    "potion": {
        "definition": "A drink with magical or medicinal properties",
        "pronunciation": "POH-shun",
        "part_of_speech": "noun",
        "example": "The Friar's potion makes Juliet appear dead",
        "modern_equivalent": "Drug, medicine",
        "misconception": "It's meant to fake death, not cause real death",
        "act": 4
    },
    "vault": {
        "definition": "An underground burial chamber",
        "pronunciation": "vawlt",
        "part_of_speech": "noun",
        "example": "The Capulet family vault where Juliet will wake",
        "modern_equivalent": "Tomb, crypt",
        "misconception": None,
        "act": 4
    },
    "charnel_house": {
        "definition": "A building where dead bodies and bones are stored",
        "pronunciation": "CHAR-nel hows",
        "part_of_speech": "noun",
        "example": "Juliet fears waking in a charnel house",
        "modern_equivalent": "Morgue, bone house",
        "misconception": None,
        "act": 4
    },
    # Act 5 Vocabulary
    "apothecary": {
        "definition": "A person who prepares and sells medicine (pharmacist)",
        "pronunciation": "uh-POTH-uh-kair-ee",
        "part_of_speech": "noun",
        "example": "Romeo buys poison from a poor apothecary",
        "modern_equivalent": "Pharmacist, drug dealer",
        "misconception": "He's breaking the law by selling poison",
        "act": 5
    },
    "dram": {
        "definition": "A small amount (of liquid or medicine)",
        "pronunciation": "dram",
        "part_of_speech": "noun",
        "example": "'A dram of poison' - just enough to kill",
        "modern_equivalent": "A dose, a drop",
        "misconception": None,
        "act": 5
    },
    "reconcile": {
        "definition": "To restore friendly relations after conflict",
        "pronunciation": "REK-un-sile",
        "part_of_speech": "verb",
        "example": "The families reconcile after the deaths",
        "modern_equivalent": "Make up, end the feud",
        "misconception": None,
        "act": 5
    },
    # Theater Terms
    "monologue": {
        "definition": "A long speech by one character to other characters",
        "pronunciation": "MON-uh-log",
        "part_of_speech": "noun",
        "example": "The Nurse's long speech about Juliet's age",
        "modern_equivalent": "Long speech",
        "misconception": "Different from soliloquy - others can hear it",
        "act": 1
    },
    "blocking": {
        "definition": "The planned movement and positioning of actors on stage",
        "pronunciation": "BLOK-ing",
        "part_of_speech": "noun",
        "example": "Where Romeo stands during the balcony scene",
        "modern_equivalent": "Stage choreography",
        "misconception": None,
        "act": 1
    },
    "upstage": {
        "definition": "The area of stage farthest from the audience",
        "pronunciation": "UP-stayj",
        "part_of_speech": "noun/verb",
        "example": "Romeo enters from upstage in the ball scene",
        "modern_equivalent": "Back of stage",
        "misconception": "Called 'up' because stages used to be raked (tilted)",
        "act": 1
    },
    "downstage": {
        "definition": "The area of stage closest to the audience",
        "pronunciation": "DOWN-stayj",
        "part_of_speech": "noun",
        "example": "Juliet moves downstage for her soliloquy",
        "modern_equivalent": "Front of stage",
        "misconception": None,
        "act": 1
    }
}


@dataclass
class VocabularyCard:
    """A single vocabulary flashcard."""
    term: str
    definition: str
    pronunciation: str
    part_of_speech: str
    example: str
    modern_equivalent: str
    misconception: Optional[str] = None
    act: int = 1


@dataclass
class VocabularySet:
    """A set of vocabulary cards for one day."""
    day_number: int
    scene_focus: str
    cards: List[VocabularyCard]


# =============================================================================
# GENERATOR FUNCTIONS
# =============================================================================

def generate_vocabulary_cards(
    day_number: int,
    scene_focus: str,
    act_number: int = 1,
    custom_terms: List[str] = None
) -> VocabularySet:
    """
    Generate vocabulary cards for a lesson.

    Args:
        day_number: Day number in the unit
        scene_focus: Scene being studied
        act_number: Act number (1-5) for selecting relevant vocabulary
        custom_terms: Specific terms to include

    Returns:
        VocabularySet with 3-6 cards
    """
    cards = []

    # If custom terms provided, use those
    if custom_terms:
        for term in custom_terms[:MAX_TERMS_PER_DAY]:
            if term.lower().replace(" ", "_") in ROMEO_JULIET_VOCABULARY:
                vocab = ROMEO_JULIET_VOCABULARY[term.lower().replace(" ", "_")]
                cards.append(_create_card(term, vocab))
    else:
        # Select terms based on act and scene
        cards = _select_terms_for_scene(scene_focus, act_number)

    # Ensure minimum terms
    if len(cards) < MIN_TERMS_PER_DAY:
        cards.extend(_get_foundational_terms(len(cards)))

    return VocabularySet(
        day_number=day_number,
        scene_focus=scene_focus,
        cards=cards[:MAX_TERMS_PER_DAY]
    )


def _create_card(term: str, vocab_data: Dict) -> VocabularyCard:
    """Create a vocabulary card from database entry."""
    return VocabularyCard(
        term=term.replace("_", " ").title(),
        definition=vocab_data["definition"],
        pronunciation=vocab_data["pronunciation"],
        part_of_speech=vocab_data["part_of_speech"],
        example=vocab_data["example"],
        modern_equivalent=vocab_data["modern_equivalent"],
        misconception=vocab_data.get("misconception"),
        act=vocab_data.get("act", 1)
    )


def _select_terms_for_scene(scene_focus: str, act_number: int) -> List[VocabularyCard]:
    """Select appropriate terms based on scene content."""
    cards = []
    scene_lower = scene_focus.lower()

    # Scene-specific terms
    scene_keywords = {
        "prologue": ["star_crossed", "ancient_grudge"],
        "brawl": ["bite_thumb", "fray"],
        "ball": ["monologue", "blocking"],
        "balcony": ["wherefore", "soliloquy", "iambic_pentameter"],
        "fight": ["plague", "fray", "banishment"],
        "banish": ["banishment", "exile"],
        "friar": ["potion", "vial"],
        "potion": ["potion", "vial", "vault", "charnel_house"],
        "tomb": ["vault", "apothecary", "dram", "reconcile"],
        "death": ["reconcile", "vault"]
    }

    # Find matching scene keywords
    for keyword, terms in scene_keywords.items():
        if keyword in scene_lower:
            for term in terms:
                if term in ROMEO_JULIET_VOCABULARY:
                    cards.append(_create_card(term, ROMEO_JULIET_VOCABULARY[term]))

    # Add act-specific vocabulary if needed
    if len(cards) < MIN_TERMS_PER_DAY:
        for term, vocab in ROMEO_JULIET_VOCABULARY.items():
            if vocab.get("act") == act_number and len(cards) < MAX_TERMS_PER_DAY:
                if not any(c.term.lower().replace(" ", "_") == term for c in cards):
                    cards.append(_create_card(term, vocab))

    return cards


def _get_foundational_terms(current_count: int) -> List[VocabularyCard]:
    """Get foundational Shakespeare terms to fill minimum."""
    foundational = ["thee", "thou", "art", "hath", "doth"]
    cards = []

    for term in foundational:
        if current_count + len(cards) >= MIN_TERMS_PER_DAY:
            break
        if term in ROMEO_JULIET_VOCABULARY:
            cards.append(_create_card(term, ROMEO_JULIET_VOCABULARY[term]))

    return cards


def vocabulary_set_to_markdown(vocab_set: VocabularySet) -> str:
    """Convert VocabularySet to markdown format for printing."""
    lines = []

    lines.append(f"# Day {vocab_set.day_number} Vocabulary Cards")
    lines.append(f"**Scene:** {vocab_set.scene_focus}")
    lines.append(f"**Terms:** {len(vocab_set.cards)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for card in vocab_set.cards:
        lines.append(f"## {card.term}")
        lines.append(f"*{card.part_of_speech}* | Pronunciation: **{card.pronunciation}**")
        lines.append("")
        lines.append(f"**Definition:** {card.definition}")
        lines.append("")
        lines.append(f"**Example from play:** {card.example}")
        lines.append("")
        lines.append(f"**Modern equivalent:** {card.modern_equivalent}")
        if card.misconception:
            lines.append("")
            lines.append(f"**Watch out:** {card.misconception}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def vocabulary_set_to_dict(vocab_set: VocabularySet) -> Dict[str, Any]:
    """Convert VocabularySet to dictionary for JSON serialization."""
    return {
        "day_number": vocab_set.day_number,
        "scene_focus": vocab_set.scene_focus,
        "card_count": len(vocab_set.cards),
        "cards": [
            {
                "term": card.term,
                "definition": card.definition,
                "pronunciation": card.pronunciation,
                "part_of_speech": card.part_of_speech,
                "example": card.example,
                "modern_equivalent": card.modern_equivalent,
                "misconception": card.misconception,
                "act": card.act
            }
            for card in vocab_set.cards
        ]
    }


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_vocabulary_set(vocab_set: VocabularySet) -> Dict[str, Any]:
    """
    Validate vocabulary set against hardcoded rules.

    Returns:
        Dictionary with validation status and any issues
    """
    issues = []
    warnings = []

    # R1: 3-6 terms per day
    card_count = len(vocab_set.cards)
    if card_count < MIN_TERMS_PER_DAY:
        issues.append({
            "rule": "R1",
            "message": f"Too few terms: {card_count} (minimum: {MIN_TERMS_PER_DAY})"
        })
    if card_count > MAX_TERMS_PER_DAY:
        warnings.append({
            "rule": "R1",
            "message": f"Many terms: {card_count} (recommended max: {MAX_TERMS_PER_DAY})"
        })

    for card in vocab_set.cards:
        # R2: Shakespeare terms must include pronunciation
        if not card.pronunciation:
            issues.append({
                "rule": "R2",
                "message": f"Term '{card.term}' missing pronunciation"
            })

        # R3: Must have play-specific example
        if not card.example:
            issues.append({
                "rule": "R3",
                "message": f"Term '{card.term}' missing example from play"
            })

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "card_count": card_count,
        "all_have_pronunciation": all(c.pronunciation for c in vocab_set.cards),
        "all_have_examples": all(c.example for c in vocab_set.cards)
    }


def has_valid_vocabulary_set(vocab_set: VocabularySet) -> bool:
    """Quick check if vocabulary set is valid."""
    result = validate_vocabulary_set(vocab_set)
    return result["valid"]
