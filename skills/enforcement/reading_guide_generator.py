"""
Reading Guide Generator - Theater Education Pipeline v2.3

Generates annotation guides with embedded questions for Romeo and Juliet.
Includes pre-reading context, annotation prompts, and scaffolded discussion questions.

Generated for: Romeo and Juliet (6-week unit)
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class AnnotationPrompt:
    """Single annotation prompt for a section of text."""
    line_range: str  # e.g., "Lines 1-15"
    key_quote: str
    prompt: str
    margin_note_suggestion: str

@dataclass
class ReadingGuide:
    """Complete reading guide for a day."""
    day: int
    scene: str
    reading_type: str
    pre_reading: Dict
    annotations: List[AnnotationPrompt]
    discussion_questions: Dict
    modern_translation: Dict

# Reading types with descriptions
READING_TYPES = {
    "shared": "Shared Reading with Annotation - Teacher reads aloud while students follow and annotate",
    "close": "Close Reading with Discussion - Small chunks analyzed deeply with partner discussion",
    "partner": "Partner Reading with Roles - Students take character roles and read together",
    "choral": "Choral Reading for Verse - Full class reads together to feel rhythm and meter",
    "rehearsal": "Rehearsal Reading - Students practice lines for performance",
    "individual": "Individual Reading - Silent reading with annotation guide",
    "summary": "Summary + Key Quotes - Brief overview with focus on essential passages"
}

# Complete Romeo and Juliet reading guide database
READING_GUIDE_DATABASE = {
    1: {  # Day 1: Prologue + 1.1
        "scene": "Prologue and Act 1, Scene 1",
        "reading_type": "shared",
        "page_lines": "Prologue (14 lines) + 1.1 (lines 1-100)",
        "pre_reading": {
            "context": "The play opens with a sonnet that tells us the entire story before it begins - a bold choice by Shakespeare that creates dramatic irony throughout.",
            "vocabulary": ["star-crossed", "fatal", "loins", "foe", "civil", "mutiny"],
            "focus_question": "As you read, look for: How does Shakespeare signal that this love story will end in tragedy?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="Prologue, lines 1-4",
                key_quote="Two households, both alike in dignity, / In fair Verona, where we lay our scene",
                prompt="What do we learn about the setting and the families? Why does 'both alike in dignity' matter?",
                margin_note_suggestion="Setting: Verona. Two equal families = equal power = stalemate"
            ),
            AnnotationPrompt(
                line_range="Prologue, lines 5-8",
                key_quote="From forth the fatal loins of these two foes / A pair of star-crossed lovers take their life",
                prompt="What is Shakespeare telling us will happen? What does 'star-crossed' mean?",
                margin_note_suggestion="SPOILER: They die. 'Star-crossed' = fate is against them"
            ),
            AnnotationPrompt(
                line_range="1.1, lines 1-20",
                key_quote="Do you bite your thumb at us, sir?",
                prompt="What starts the fight? What does this tell us about the feud?",
                margin_note_suggestion="Feud starts over NOTHING - shows how petty/dangerous it is"
            ),
            AnnotationPrompt(
                line_range="1.1, lines 70-100",
                key_quote="Here's much to do with hate, but more with love",
                prompt="When Romeo enters, how is his mood different from the fighting? What is he focused on?",
                margin_note_suggestion="Romeo = lovesick, not interested in feud. Irony: love/hate together"
            )
        ],
        "discussion_questions": {
            "literal": "What happens in the opening of the play? Who fights and why?",
            "interpretive": "Why do you think Shakespeare tells us the ending in the very first lines?",
            "evaluative": "Do you think the servants are to blame for the fight, or is the feud itself the problem?"
        },
        "modern_translation": {
            "original": "From forth the fatal loins of these two foes / A pair of star-crossed lovers take their life",
            "modern": "From these two enemy families, two lovers will be born who are doomed by fate - and they will kill themselves."
        }
    },
    2: {  # Day 2: 1.1 continued
        "scene": "Act 1, Scene 1 (continued)",
        "reading_type": "close",
        "page_lines": "1.1, lines 155-240",
        "pre_reading": {
            "context": "After the brawl is broken up, we meet Romeo for the first time. He's not thinking about the feud at all - he's completely consumed by his love for a woman named Rosaline.",
            "vocabulary": ["Rosaline", "unrequited", "melancholy", "paradox", "oxymoron"],
            "focus_question": "As you read, look for: How does Romeo describe love? What contradictions do you notice?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="1.1, lines 171-180",
                key_quote="Why then, O brawling love, O loving hate, / O anything of nothing first create",
                prompt="Romeo uses oxymorons (contradictions). Why might love feel like these opposites?",
                margin_note_suggestion="Love = contradictory feelings. Romeo feels confused/overwhelmed"
            ),
            AnnotationPrompt(
                line_range="1.1, lines 190-200",
                key_quote="She will not stay the siege of loving terms",
                prompt="What military language does Romeo use? What does this reveal about how he sees love?",
                margin_note_suggestion="Love as WAR - conquest, siege, attack. Is this healthy?"
            ),
            AnnotationPrompt(
                line_range="1.1, lines 220-240",
                key_quote="She hath forsworn to love, and in that vow / Do I live dead that live to tell it now",
                prompt="Rosaline has sworn off love. How does Romeo react to rejection?",
                margin_note_suggestion="Romeo = dramatic about rejection. 'Live dead' = another oxymoron"
            )
        ],
        "discussion_questions": {
            "literal": "Who is Rosaline and what is Romeo's relationship with her?",
            "interpretive": "Do you think Romeo is truly in love with Rosaline, or is he in love with the idea of being in love?",
            "evaluative": "Is Romeo's reaction to Rosaline's rejection healthy or concerning? Why?"
        },
        "modern_translation": {
            "original": "Why then, O brawling love, O loving hate, / O anything of nothing first create",
            "modern": "Love is fighting and hating at the same time - it creates something out of nothing, but it feels like everything."
        }
    },
    3: {  # Day 3: 1.2 + 1.3
        "scene": "Act 1, Scenes 2-3 (condensed)",
        "reading_type": "partner",
        "page_lines": "1.2 (key lines) + 1.3 (lines 60-100)",
        "pre_reading": {
            "context": "We now meet Juliet for the first time. She's being asked about marriage by her mother and the Nurse. Meanwhile, Paris has asked Lord Capulet for permission to marry Juliet.",
            "vocabulary": ["Nurse", "Paris", "suitor", "woo", "fortnight"],
            "focus_question": "As you read, look for: What do we learn about Juliet from how others describe her?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="1.2, lines 7-14",
                key_quote="My child is yet a stranger in the world, / She hath not seen the change of fourteen years",
                prompt="How old is Juliet? What is Capulet's initial reaction to Paris's proposal?",
                margin_note_suggestion="Juliet = 13! Capulet hesitant at first - 'too young'"
            ),
            AnnotationPrompt(
                line_range="1.3, lines 65-75",
                key_quote="Tell me, daughter Juliet, / How stands your disposition to be married?",
                prompt="How does Lady Capulet ask about marriage? How is her relationship with Juliet?",
                margin_note_suggestion="Formal, awkward. Lady C doesn't know her own daughter well"
            ),
            AnnotationPrompt(
                line_range="1.3, lines 80-100",
                key_quote="It is an honor that I dream not of",
                prompt="What is Juliet's response about marriage? What does this tell us about her?",
                margin_note_suggestion="Juliet = obedient, reserved, not thinking about romance yet"
            )
        ],
        "discussion_questions": {
            "literal": "What do we learn about Juliet from the Nurse's stories?",
            "interpretive": "Why is the Nurse closer to Juliet than Lady Capulet is?",
            "evaluative": "Do you think Juliet is ready for marriage? Why or why not?"
        },
        "modern_translation": {
            "original": "It is an honor that I dream not of",
            "modern": "Marriage? That's an honor I haven't even thought about yet."
        }
    },
    4: {  # Day 4: 1.4
        "scene": "Act 1, Scene 4 - Queen Mab Speech",
        "reading_type": "choral",
        "page_lines": "1.4, lines 53-95",
        "pre_reading": {
            "context": "Romeo, Benvolio, and Mercutio are on their way to crash the Capulet party. Romeo has had a dream and fears something bad will happen. Mercutio tries to dismiss his fears with a famous speech about Queen Mab.",
            "vocabulary": ["Queen Mab", "fairies", "midwife", "dreamers", "vain fantasy"],
            "focus_question": "As you read, look for: How does Mercutio's speech start vs. how it ends? What changes?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="1.4, lines 53-60",
                key_quote="O, then I see Queen Mab hath been with you. / She is the fairies' midwife",
                prompt="Who is Queen Mab? What is Mercutio's tone at the beginning?",
                margin_note_suggestion="Queen Mab = fairy who brings dreams. Tone: playful, whimsical"
            ),
            AnnotationPrompt(
                line_range="1.4, lines 70-80",
                key_quote="And in this state she gallops night by night / Through lovers' brains, and then they dream of love",
                prompt="What does Queen Mab make different people dream about?",
                margin_note_suggestion="She gives each person dreams of what they want most"
            ),
            AnnotationPrompt(
                line_range="1.4, lines 85-95",
                key_quote="This is the hag, when maids lie on their backs, / That presses them and learns them first to bear",
                prompt="How does the speech change in tone? What is happening to Mercutio?",
                margin_note_suggestion="Tone gets DARK, violent, sexual. Mercutio losing control?"
            )
        ],
        "discussion_questions": {
            "literal": "According to Mercutio, what is Queen Mab and what does she do?",
            "interpretive": "Why does Mercutio's speech start playful but become dark and frantic?",
            "evaluative": "What does this speech reveal about Mercutio's worldview and character?"
        },
        "modern_translation": {
            "original": "True, I talk of dreams, / Which are the children of an idle brain, / Begot of nothing but vain fantasy",
            "modern": "Yeah, I'm just talking about dreams - they're made up by bored minds with nothing better to do than imagine things."
        }
    },
    5: {  # Day 5: 1.5
        "scene": "Act 1, Scene 5 - The Ball",
        "reading_type": "shared",
        "page_lines": "1.5, lines 44-110",
        "pre_reading": {
            "context": "Romeo enters the Capulet party and sees Juliet for the first time. He completely forgets about Rosaline. But Tybalt recognizes Romeo's voice and wants to fight him.",
            "vocabulary": ["sonnet", "pilgrim", "shrine", "profane", "holy"],
            "focus_question": "As you read, look for: How do Romeo and Juliet speak to each other? What poetic form do they share?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="1.5, lines 44-53",
                key_quote="O, she doth teach the torches to burn bright! / It seems she hangs upon the cheek of night",
                prompt="How does Romeo describe Juliet? What light/dark imagery do you notice?",
                margin_note_suggestion="Juliet = light in darkness. Same imagery as 'star-crossed' - fate"
            ),
            AnnotationPrompt(
                line_range="1.5, lines 93-106",
                key_quote="If I profane with my unworthiest hand / This holy shrine, the gentle sin is this",
                prompt="Romeo and Juliet share a sonnet (14 lines, rhyme scheme). Why is this significant?",
                margin_note_suggestion="They SHARE a sonnet = they are meant for each other, equals"
            ),
            AnnotationPrompt(
                line_range="1.5, lines 107-110",
                key_quote="You kiss by th' book",
                prompt="What religious imagery do Romeo and Juliet use? What are they compared to?",
                margin_note_suggestion="Love = religion. Romeo = pilgrim, Juliet = saint. Sacred love"
            )
        ],
        "discussion_questions": {
            "literal": "What happens when Romeo first sees Juliet? What do they do?",
            "interpretive": "Why does Shakespeare have Romeo and Juliet share a sonnet? What does this symbolize?",
            "evaluative": "Is this 'love at first sight' real love, or infatuation? How can you tell the difference?"
        },
        "modern_translation": {
            "original": "If I profane with my unworthiest hand / This holy shrine, the gentle sin is this: / My lips, two blushing pilgrims, ready stand / To smooth that rough touch with a tender kiss",
            "modern": "If it's wrong for me to touch your hand - which is like a holy shrine - then let me make up for it by kissing you gently."
        }
    },
    6: {  # Day 6: 1.5 continued
        "scene": "Act 1, Scene 5 (continued) - Performance Focus",
        "reading_type": "partner",
        "page_lines": "1.5, lines 93-144",
        "pre_reading": {
            "context": "We're returning to the shared sonnet and the moment of the first kiss to work on it as performers. Focus on how the scene is staged and what choices actors must make.",
            "vocabulary": ["blocking", "stage directions", "subtext", "beat"],
            "focus_question": "As you read, look for: What are the physical moments in this scene? Where do characters move?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="1.5, lines 93-100",
                key_quote="If I profane with my unworthiest hand...",
                prompt="When does Romeo first touch Juliet? Is it bold or hesitant?",
                margin_note_suggestion="Performance choice: Does he grab her hand? Wait for permission?"
            ),
            AnnotationPrompt(
                line_range="1.5, lines 106-108",
                key_quote="Then move not while my prayer's effect I take. / Thus from my lips, by thine, my sin is purged",
                prompt="The first kiss! What is the lead-up? Who initiates?",
                margin_note_suggestion="He tells her not to move - then kisses her. She lets him."
            ),
            AnnotationPrompt(
                line_range="1.5, lines 134-144",
                key_quote="My only love sprung from my only hate! / Too early seen unknown, and known too late!",
                prompt="Juliet discovers Romeo is a Montague. What is her reaction?",
                margin_note_suggestion="Devastated but already in love. 'Too late' = can't undo it"
            )
        ],
        "discussion_questions": {
            "literal": "What happens after their first kiss? How do they find out who each other is?",
            "interpretive": "Why does Juliet say 'Too early seen unknown, and known too late'?",
            "evaluative": "If you were staging this scene, how would you show the moment they realize they're enemies?"
        },
        "modern_translation": {
            "original": "My only love sprung from my only hate! / Too early seen unknown, and known too late!",
            "modern": "The only person I've ever loved is from the only family I'm supposed to hate! I fell for him before I knew who he was - and now it's too late."
        }
    },
    7: {  # Day 7: 2.2 Part 1
        "scene": "Act 2, Scene 2 - Balcony Scene (Romeo's Discovery)",
        "reading_type": "close",
        "page_lines": "2.2, lines 1-32",
        "pre_reading": {
            "context": "After the party, Romeo sneaks into the Capulet orchard and finds himself below Juliet's window. This is one of the most famous scenes in all of literature.",
            "vocabulary": ["balcony", "orchard", "vestal", "envious", "spheres"],
            "focus_question": "As you read, look for: What does Romeo compare Juliet to? Track all the light imagery."
        },
        "annotations": [
            AnnotationPrompt(
                line_range="2.2, lines 1-6",
                key_quote="But soft, what light through yonder window breaks? / It is the east, and Juliet is the sun",
                prompt="What is Romeo's first metaphor for Juliet? What does comparing her to the sun mean?",
                margin_note_suggestion="Juliet = sun = center of his universe, source of all life/warmth"
            ),
            AnnotationPrompt(
                line_range="2.2, lines 15-22",
                key_quote="Two of the fairest stars in all the heaven, / Having some business, do entreat her eyes / To twinkle in their spheres till they return",
                prompt="Now he compares her eyes to stars. Why does Romeo keep using celestial imagery?",
                margin_note_suggestion="Stars = 'star-crossed' - connecting love to fate again"
            ),
            AnnotationPrompt(
                line_range="2.2, lines 26-32",
                key_quote="O, speak again, bright angel, for thou art / As glorious to this night, being o'er my head",
                prompt="What does Romeo call Juliet? What does this religious imagery suggest?",
                margin_note_suggestion="Angel = Juliet is divine, perfect. He worships her"
            )
        ],
        "discussion_questions": {
            "literal": "What does Romeo say about Juliet before she knows he's there?",
            "interpretive": "Why does Romeo use so much light and celestial imagery to describe Juliet?",
            "evaluative": "Is Romeo's language about Juliet beautiful or excessive? Is he idealizing her too much?"
        },
        "modern_translation": {
            "original": "But soft, what light through yonder window breaks? / It is the east, and Juliet is the sun",
            "modern": "Wait - what's that light in the window? It's like the sun rising, and Juliet is the sun itself."
        }
    },
    8: {  # Day 8: 2.2 Part 2
        "scene": "Act 2, Scene 2 - The Exchange",
        "reading_type": "partner",
        "page_lines": "2.2, lines 33-84",
        "pre_reading": {
            "context": "Juliet comes to her window and speaks her thoughts aloud - not knowing Romeo is listening below. Her famous 'What's in a name?' speech questions whether names really matter.",
            "vocabulary": ["wherefore", "deny", "refuse", "sworn", "forswear"],
            "focus_question": "As you read, look for: What is Juliet's argument about names? Does she convince you?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="2.2, lines 33-36",
                key_quote="O Romeo, Romeo! Wherefore art thou Romeo? / Deny thy father and refuse thy name",
                prompt="'Wherefore' means 'why' - not 'where.' What is Juliet actually asking?",
                margin_note_suggestion="Juliet asks WHY is he Romeo = why a Montague? Change your name!"
            ),
            AnnotationPrompt(
                line_range="2.2, lines 43-48",
                key_quote="What's in a name? That which we call a rose / By any other name would smell as sweet",
                prompt="This is one of the most famous lines in literature. What is Juliet's argument?",
                margin_note_suggestion="Names are arbitrary labels - they don't change what something IS"
            ),
            AnnotationPrompt(
                line_range="2.2, lines 66-78",
                key_quote="How camest thou hither, tell me, and wherefore? / The orchard walls are high and hard to climb",
                prompt="When Juliet discovers Romeo is there, what are her concerns?",
                margin_note_suggestion="Practical Juliet: worried about danger. Romeo is impulsive."
            )
        ],
        "discussion_questions": {
            "literal": "What is Juliet's argument about Romeo's name?",
            "interpretive": "Is Juliet right that names don't matter, or do names shape who we are?",
            "evaluative": "Who seems more practical in this scene - Romeo or Juliet? Give evidence."
        },
        "modern_translation": {
            "original": "What's in a name? That which we call a rose / By any other name would smell as sweet",
            "modern": "What's so important about a name? If we called a rose something else, it would still smell just as good."
        }
    },
    9: {  # Day 9: 2.2 Part 3
        "scene": "Act 2, Scene 2 - Performance",
        "reading_type": "rehearsal",
        "page_lines": "2.2, lines 85-141 (selected)",
        "pre_reading": {
            "context": "We're focusing on the balcony scene as performance text today. Read with your scene partner and make choices about how to deliver the lines.",
            "vocabulary": ["troth", "perjury", "contract", "exchange", "vows"],
            "focus_question": "As you read, look for: What are the key moments that need to land in performance?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="2.2, lines 107-111",
                key_quote="Lady, by yonder blessed moon I swear, / That tips with silver all these fruit-tree tops",
                prompt="Romeo tries to swear by the moon. What is Juliet's response?",
                margin_note_suggestion="Juliet: Don't swear by the moon - it changes! She's practical."
            ),
            AnnotationPrompt(
                line_range="2.2, lines 116-120",
                key_quote="I have no joy of this contract tonight. / It is too rash, too unadvised, too sudden",
                prompt="Juliet expresses doubts. What concerns her?",
                margin_note_suggestion="Moving too fast. But she can't stop herself either."
            ),
            AnnotationPrompt(
                line_range="2.2, lines 133-141",
                key_quote="Good night, good night! Parting is such sweet sorrow / That I shall say good night till it be morrow",
                prompt="The famous ending. Why is parting 'sweet sorrow'?",
                margin_note_suggestion="Sweet = love. Sorrow = separation. Another oxymoron of love"
            )
        ],
        "discussion_questions": {
            "literal": "What do Romeo and Juliet decide by the end of this scene?",
            "interpretive": "Juliet says their love is 'too rash, too sudden.' Does she believe her own warning?",
            "evaluative": "What line would you choose as the most important to get right in performance? Why?"
        },
        "modern_translation": {
            "original": "Good night, good night! Parting is such sweet sorrow / That I shall say good night till it be morrow",
            "modern": "Good night, good night! Saying goodbye hurts so much but feels so good that I'll keep saying it until morning."
        }
    },
    10: {  # Day 10: 2.3 + 2.4/2.6
        "scene": "Act 2, Scenes 3, 4, 6 (condensed) - Friar Lawrence & Marriage",
        "reading_type": "shared",
        "page_lines": "2.3 (lines 1-30, 65-94) + summary of 2.4/2.6",
        "pre_reading": {
            "context": "Romeo goes to Friar Lawrence for help. The Friar is a complex character - he's religious, he knows about plants and potions, and he agrees to marry Romeo and Juliet secretly.",
            "vocabulary": ["Friar", "cell", "rosamond", "holy church", "alliance"],
            "focus_question": "As you read, look for: Why does Friar Lawrence agree to help? Is his reasoning sound?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="2.3, lines 1-22",
                key_quote="The grey-eyed morn smiles on the frowning night, / Chequering the eastern clouds with streaks of light",
                prompt="What is the Friar doing when we meet him? What does this tell us about him?",
                margin_note_suggestion="Gathering herbs at dawn. Friar knows plants, medicine, poison..."
            ),
            AnnotationPrompt(
                line_range="2.3, lines 65-80",
                key_quote="Holy Saint Francis! What a change is here! / Is Rosaline, that thou didst love so dear, / So soon forsaken?",
                prompt="How does Friar react to Romeo's news about Juliet?",
                margin_note_suggestion="Shocked! Romeo just loved Rosaline yesterday. Friar is skeptical."
            ),
            AnnotationPrompt(
                line_range="2.3, lines 87-94",
                key_quote="In one respect I'll thy assistant be, / For this alliance may so happy prove / To turn your households' rancor to pure love",
                prompt="Why does the Friar agree to marry them? What is his hope?",
                margin_note_suggestion="POLITICAL: hopes marriage will end feud. Good motive, bad plan?"
            )
        ],
        "discussion_questions": {
            "literal": "What is Friar Lawrence doing when Romeo arrives? What does he collect?",
            "interpretive": "Why does the Friar agree to help Romeo, even though he thinks Romeo is being rash?",
            "evaluative": "Is Friar Lawrence a wise counselor or a meddler who makes things worse?"
        },
        "modern_translation": {
            "original": "For this alliance may so happy prove / To turn your households' rancor to pure love",
            "modern": "This marriage might just work out well enough to turn your families' hatred into love for each other."
        }
    },
    11: {  # Day 11: 3.1 Part 1
        "scene": "Act 3, Scene 1 - Rising Tension (Mercutio vs. Tybalt)",
        "reading_type": "close",
        "page_lines": "3.1, lines 1-55",
        "pre_reading": {
            "context": "Act 3 is the turning point of the play. On a hot day in Verona's streets, Mercutio and Benvolio encounter Tybalt, who is looking for Romeo. Everything changes in this scene.",
            "vocabulary": ["apt", "fray", "consort", "ally", "villain"],
            "focus_question": "As you read, look for: How does the tension build? What choices lead toward violence?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="3.1, lines 1-10",
                key_quote="The day is hot, the Capulets abroad, / And if we meet we shall not 'scape a brawl",
                prompt="What is the atmosphere at the opening? What does Benvolio predict?",
                margin_note_suggestion="Hot day = hot tempers. Benvolio KNOWS there will be a fight"
            ),
            AnnotationPrompt(
                line_range="3.1, lines 35-45",
                key_quote="Mercutio, thou consortest with Romeo",
                prompt="How does Tybalt try to provoke Mercutio? What does 'consort' mean?",
                margin_note_suggestion="'Consort' = hang out with, but also = musicians. Mercutio takes offense"
            ),
            AnnotationPrompt(
                line_range="3.1, lines 50-55",
                key_quote="Here comes my man... / Romeo, the love I bear thee can afford / No better term than this: thou art a villain",
                prompt="When Romeo arrives, what does Tybalt call him? What is Tybalt expecting?",
                margin_note_suggestion="Tybalt insults Romeo to start a fight. But Romeo is now his kinsman..."
            )
        ],
        "discussion_questions": {
            "literal": "Why is Tybalt looking for Romeo? What happened to make Tybalt angry?",
            "interpretive": "Why does Mercutio take Tybalt's insults personally when they're aimed at Romeo?",
            "evaluative": "Could this fight have been avoided? At what point did it become inevitable?"
        },
        "modern_translation": {
            "original": "Romeo, the love I bear thee can afford / No better term than this: thou art a villain",
            "modern": "Romeo, I don't love you enough to call you anything but this: you're a scumbag."
        }
    },
    12: {  # Day 12: 3.1 Part 2
        "scene": "Act 3, Scene 1 - The Deaths",
        "reading_type": "choral",
        "page_lines": "3.1, lines 56-108",
        "pre_reading": {
            "context": "Romeo tries to stop the fight because Tybalt is now his kinsman (through his secret marriage to Juliet). But Mercutio doesn't know this and sees Romeo's refusal to fight as cowardice.",
            "vocabulary": ["submit", "tender", "dishonor", "plague", "curse"],
            "focus_question": "As you read, look for: How does Romeo's attempt to make peace lead to disaster?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="3.1, lines 56-70",
                key_quote="I do protest I never injured thee, / But love thee better than thou canst devise",
                prompt="Why won't Romeo fight Tybalt? What does Romeo know that Tybalt doesn't?",
                margin_note_suggestion="Romeo is now Tybalt's COUSIN by marriage. He can't explain why."
            ),
            AnnotationPrompt(
                line_range="3.1, lines 85-90",
                key_quote="A plague o' both your houses! / They have made worms' meat of me",
                prompt="Mercutio is stabbed. What is his dying curse? Who does he blame?",
                margin_note_suggestion="Curses BOTH families. Blames the feud, not just Tybalt."
            ),
            AnnotationPrompt(
                line_range="3.1, lines 100-108",
                key_quote="O, I am fortune's fool!",
                prompt="After Romeo kills Tybalt, what does he say about himself? What does this mean?",
                margin_note_suggestion="'Fortune's fool' = victim of fate. But was it fate or his choice?"
            )
        ],
        "discussion_questions": {
            "literal": "How does Mercutio get stabbed? Who is responsible?",
            "interpretive": "What does Mercutio mean by 'A plague o' both your houses'?",
            "evaluative": "Is Romeo 'fortune's fool' or did he make choices that led to this moment?"
        },
        "modern_translation": {
            "original": "A plague o' both your houses! / They have made worms' meat of me",
            "modern": "Curse both your families! Their stupid feud has killed me - I'm going to be food for worms."
        }
    },
    13: {  # Day 13: 3.1 Part 3 + 3.2
        "scene": "Act 3, Scene 1-2 - Aftermath",
        "reading_type": "partner",
        "page_lines": "3.1 (lines 130-150) + 3.2 (lines 73-126)",
        "pre_reading": {
            "context": "Romeo is banished for killing Tybalt. Meanwhile, Juliet waits for Romeo to come to her on their wedding night - not knowing what has happened.",
            "vocabulary": ["banished", "exile", "oxymoron", "tyrant", "fiend"],
            "focus_question": "As you read, look for: How does Juliet react to the news? Notice her use of oxymorons."
        },
        "annotations": [
            AnnotationPrompt(
                line_range="3.1, lines 130-142",
                key_quote="And for that offense / Immediately we do exile him hence",
                prompt="What is Romeo's punishment? Why isn't he executed?",
                margin_note_suggestion="Banishment, not death. Because Tybalt started it by killing Mercutio."
            ),
            AnnotationPrompt(
                line_range="3.2, lines 73-79",
                key_quote="O serpent heart hid with a flow'ring face! / Did ever dragon keep so fair a cave?",
                prompt="When Juliet first hears the news, she blames Romeo. What does she call him?",
                margin_note_suggestion="Oxymorons: serpent/flower, dragon/fair. Shows her confusion."
            ),
            AnnotationPrompt(
                line_range="3.2, lines 97-104",
                key_quote="Shall I speak ill of him that is my husband? / Ah, poor my lord, what tongue shall smooth thy name",
                prompt="Juliet quickly shifts to defending Romeo. What causes this change?",
                margin_note_suggestion="She realizes: Romeo is her husband now. Loyalty comes first."
            )
        ],
        "discussion_questions": {
            "literal": "What is Romeo's punishment? What are the terms of his banishment?",
            "interpretive": "Why does Juliet use so many oxymorons to describe Romeo after hearing the news?",
            "evaluative": "Should Juliet forgive Romeo for killing her cousin? Is her loyalty to her husband reasonable?"
        },
        "modern_translation": {
            "original": "O serpent heart hid with a flow'ring face! / Did ever dragon keep so fair a cave?",
            "modern": "You're a snake hiding behind a pretty face! Did a monster ever live in such a beautiful body?"
        }
    },
    14: {  # Day 14: 3.3 + 3.4
        "scene": "Act 3, Scenes 3-4 (condensed) - Romeo with Friar",
        "reading_type": "close",
        "page_lines": "3.3, lines 29-70 + summary of 3.4",
        "pre_reading": {
            "context": "Romeo hides with Friar Lawrence after killing Tybalt. He's devastated by his banishment. Meanwhile, Lord Capulet has decided Juliet will marry Paris in three days.",
            "vocabulary": ["banishment", "philosophy", "minstrel", "adversity"],
            "focus_question": "As you read, look for: How does Romeo handle his punishment? Is the Friar helpful?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="3.3, lines 29-40",
                key_quote="There is no world without Verona walls, / But purgatory, torture, hell itself",
                prompt="How does Romeo react to banishment? Is he being rational?",
                margin_note_suggestion="Dramatic, suicidal. Sees banishment as worse than death."
            ),
            AnnotationPrompt(
                line_range="3.3, lines 52-60",
                key_quote="Wert thou as young as I, Juliet thy love, / An hour but married, Tybalt murdered",
                prompt="Romeo criticizes the Friar. What is his complaint?",
                margin_note_suggestion="'You don't understand because you're old and celibate'"
            ),
            AnnotationPrompt(
                line_range="3.3, lines 108-120",
                key_quote="Go, get thee to thy love, as was decreed. / Ascend her chamber, hence and comfort her",
                prompt="What is the Friar's plan? What does he tell Romeo to do?",
                margin_note_suggestion="Go to Juliet tonight. Then flee to Mantua. Wait for news."
            )
        ],
        "discussion_questions": {
            "literal": "Where does the Friar tell Romeo to go? What is the plan?",
            "interpretive": "Why is Romeo acting so dramatically about banishment when he could be dead?",
            "evaluative": "Do you think the Friar is giving good advice? What would you tell Romeo?"
        },
        "modern_translation": {
            "original": "There is no world without Verona walls, / But purgatory, torture, hell itself",
            "modern": "Anywhere outside Verona isn't a real world - it's just different versions of hell to me."
        }
    },
    15: {  # Day 15: 3.5 Part 1
        "scene": "Act 3, Scene 5 - Dawn Parting",
        "reading_type": "partner",
        "page_lines": "3.5, lines 1-36",
        "pre_reading": {
            "context": "Romeo and Juliet have spent their wedding night together. As dawn breaks, Romeo must leave for Mantua or face death if he's caught in Verona.",
            "vocabulary": ["aubade", "lark", "nightingale", "envious", "severing"],
            "focus_question": "As you read, look for: What is the argument about the bird? What does it really mean?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="3.5, lines 1-11",
                key_quote="Wilt thou be gone? It is not yet near day. / It was the nightingale, and not the lark",
                prompt="What is Juliet arguing? Why does she want it to be a nightingale?",
                margin_note_suggestion="Nightingale = night. Lark = dawn. If it's night, Romeo can stay."
            ),
            AnnotationPrompt(
                line_range="3.5, lines 17-25",
                key_quote="It was the lark, the herald of the morn, / No nightingale. Look, love, what envious streaks",
                prompt="Why does Romeo insist it's the lark? What is at stake?",
                margin_note_suggestion="Romeo = realistic. He'll be killed if caught. Streaks of dawn = danger"
            ),
            AnnotationPrompt(
                line_range="3.5, lines 26-36",
                key_quote="Let me be ta'en, let me be put to death. / I am content, so thou wilt have it so",
                prompt="When Juliet finally accepts it's dawn, Romeo suddenly says he'll stay. Why?",
                margin_note_suggestion="Reverse psychology? Or he'd rather die than leave her."
            )
        ],
        "discussion_questions": {
            "literal": "Why are Romeo and Juliet arguing about whether they hear a lark or nightingale?",
            "interpretive": "What is an 'aubade' and how does this scene fit the tradition?",
            "evaluative": "In this scene, who is more practical - Romeo or Juliet? Has this changed since Act 2?"
        },
        "modern_translation": {
            "original": "It was the nightingale, and not the lark, / That pierced the fearful hollow of thine ear",
            "modern": "That was a nightingale you heard, not a lark - nightingales sing at night, so you don't have to leave yet."
        }
    },
    16: {  # Day 16: 3.5 Part 2
        "scene": "Act 3, Scene 5 - Capulet's Ultimatum",
        "reading_type": "close",
        "page_lines": "3.5, lines 126-205",
        "pre_reading": {
            "context": "After Romeo leaves, Lady Capulet comes to tell Juliet she must marry Paris on Thursday. When Juliet refuses, Lord Capulet erupts in rage.",
            "vocabulary": ["disobedient", "wretch", "minion", "graze", "starve"],
            "focus_question": "As you read, look for: How does each character react to Juliet's refusal?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="3.5, lines 140-150",
                key_quote="I will not marry yet, and when I do, I swear / It shall be Romeo, whom you know I hate",
                prompt="How does Juliet refuse the marriage without revealing her secret?",
                margin_note_suggestion="Clever double meaning: She'll marry Romeo. Uses irony to hide truth."
            ),
            AnnotationPrompt(
                line_range="3.5, lines 160-175",
                key_quote="Hang thee, young baggage! Disobedient wretch! / I tell thee what: get thee to church o' Thursday, / Or never after look me in the face",
                prompt="How does Lord Capulet react to Juliet's refusal? What does he threaten?",
                margin_note_suggestion="RAGE. Insults her. Threatens to disown her, throw her out."
            ),
            AnnotationPrompt(
                line_range="3.5, lines 195-205",
                key_quote="I think it best you married with the County... / I think you are happy in this second match, / For it excels your first",
                prompt="What advice does the Nurse give? How does this affect Juliet?",
                margin_note_suggestion="Nurse betrays Juliet: 'Marry Paris, forget Romeo.' Trust broken."
            )
        ],
        "discussion_questions": {
            "literal": "What ultimatum does Lord Capulet give Juliet?",
            "interpretive": "Why is the Nurse's betrayal so devastating to Juliet?",
            "evaluative": "Is Lord Capulet a villain in this scene, or is he acting as a typical father of his time?"
        },
        "modern_translation": {
            "original": "Hang thee, young baggage! Disobedient wretch! / I tell thee what: get thee to church o' Thursday, / Or never after look me in the face",
            "modern": "You little brat! How dare you disobey me! Listen up: you're going to that church on Thursday to marry Paris, or don't ever come near me again."
        }
    },
    17: {  # Day 17: 4.1
        "scene": "Act 4, Scene 1 - The Desperate Plan",
        "reading_type": "shared",
        "page_lines": "4.1, lines 44-120",
        "pre_reading": {
            "context": "Juliet goes to Friar Lawrence for help. She's desperate - she'll kill herself before marrying Paris. The Friar has an idea: a potion that will make her appear dead.",
            "vocabulary": ["vial", "potion", "sepulcher", "charnel house", "vault"],
            "focus_question": "As you read, look for: What are the risks of the Friar's plan?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="4.1, lines 53-67",
                key_quote="O, bid me leap, rather than marry Paris, / From off the battlements of any tower",
                prompt="What is Juliet willing to do to avoid marrying Paris?",
                margin_note_suggestion="Suicide imagery: She'll jump, be chained with bears, anything."
            ),
            AnnotationPrompt(
                line_range="4.1, lines 89-106",
                key_quote="Take thou this vial, being then in bed, / And this distilling liquor drink thou off",
                prompt="What will the potion do? How long will it last?",
                margin_note_suggestion="Fake death for 42 hours. No pulse, no breath, cold body."
            ),
            AnnotationPrompt(
                line_range="4.1, lines 113-120",
                key_quote="In the meantime, against thou shalt awake, / Shall Romeo by my letters know our drift",
                prompt="What is the crucial part of the plan? What could go wrong?",
                margin_note_suggestion="LETTER to Romeo. What if it doesn't arrive? (FORESHADOWING)"
            )
        ],
        "discussion_questions": {
            "literal": "What are the steps of the Friar's plan?",
            "interpretive": "Why does the Friar think this complicated plan is the best option?",
            "evaluative": "Is the Friar helping Juliet or making things worse? Should he refuse?"
        },
        "modern_translation": {
            "original": "Take thou this vial, being then in bed, / And this distilling liquor drink thou off, / When presently through all thy veins shall run / A cold and drowsy humor",
            "modern": "Take this bottle and drink the whole thing before bed. A cold, sleepy feeling will spread through your entire body."
        }
    },
    18: {  # Day 18: 4.3 Part 1
        "scene": "Act 4, Scene 3 - Potion Soliloquy (Fears)",
        "reading_type": "close",
        "page_lines": "4.3, lines 14-59",
        "pre_reading": {
            "context": "Juliet is alone in her room with the potion. She must drink it tonight, but she's terrified. This soliloquy shows us inside her mind as she wrestles with her fears.",
            "vocabulary": ["soliloquy", "vault", "ancestors", "mandrakes", "receptacle"],
            "focus_question": "As you read, look for: What fears does Juliet name? How do they escalate?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="4.3, lines 14-23",
                key_quote="What if it be a poison which the friar / Subtly hath ministered to have me dead",
                prompt="What is Juliet's first fear about the potion?",
                margin_note_suggestion="Fear 1: What if it's actual poison? What if Friar wants her dead?"
            ),
            AnnotationPrompt(
                line_range="4.3, lines 30-35",
                key_quote="How if, when I am laid into the tomb, / I wake before the time that Romeo / Come to redeem me?",
                prompt="What is her second fear?",
                margin_note_suggestion="Fear 2: What if she wakes up too early, alone in the tomb?"
            ),
            AnnotationPrompt(
                line_range="4.3, lines 36-54",
                key_quote="Shall I not then be stifled in the vault, / To whose foul mouth no healthsome air breathes in, / And there die strangled ere my Romeo comes?",
                prompt="How does Juliet's imagination make her fears worse?",
                margin_note_suggestion="Fears escalate: suffocation, smell of death, Tybalt's corpse, ghosts, madness"
            )
        ],
        "discussion_questions": {
            "literal": "List all the fears Juliet names in this soliloquy.",
            "interpretive": "How can we see Juliet's fear building through the structure of the speech?",
            "evaluative": "Is Juliet being rational or irrational? Which of her fears are realistic?"
        },
        "modern_translation": {
            "original": "How if, when I am laid into the tomb, / I wake before the time that Romeo / Come to redeem me?",
            "modern": "What if I wake up in the tomb before Romeo gets there to rescue me?"
        }
    },
    19: {  # Day 19: 4.3 Part 2
        "scene": "Act 4, Scene 3 - Soliloquy Performance",
        "reading_type": "individual",
        "page_lines": "4.3, lines 14-59",
        "pre_reading": {
            "context": "Today we work on Juliet's soliloquy as a performance piece. Focus on beats, builds, and the climax of the speech.",
            "vocabulary": ["beat", "build", "climax", "objective", "tactic"],
            "focus_question": "As you read, look for: Where are the emotional shifts in this speech?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="4.3, lines 14-29",
                key_quote="I have a faint cold fear thrills through my veins... / What if this mixture do not work at all?",
                prompt="What is the emotional quality of the opening section?",
                margin_note_suggestion="BEAT 1: Hesitation. Cold. Fear is physical, not yet panic."
            ),
            AnnotationPrompt(
                line_range="4.3, lines 30-45",
                key_quote="The horrible conceit of death and night, / Together with the terror of the place",
                prompt="How does the emotion change here? What is happening to her voice?",
                margin_note_suggestion="BEAT 2: Building panic. Images get more vivid. Speed increases."
            ),
            AnnotationPrompt(
                line_range="4.3, lines 54-58",
                key_quote="O, look! Methinks I see my cousin's ghost / Seeking out Romeo that did spit his body / Upon a rapier's point. Stay, Tybalt, stay!",
                prompt="What happens at the climax? Is Juliet hallucinating?",
                margin_note_suggestion="CLIMAX: Seeing visions. Madness? Or courage? She drinks anyway."
            )
        ],
        "discussion_questions": {
            "literal": "How many distinct 'beats' or sections can you identify in this speech?",
            "interpretive": "What gives Juliet the courage to drink the potion after imagining such horrors?",
            "evaluative": "If you were directing this scene, where would you tell the actress to pause? To speed up?"
        },
        "modern_translation": {
            "original": "O, look! Methinks I see my cousin's ghost / Seeking out Romeo that did spit his body / Upon a rapier's point",
            "modern": "Oh my God! I think I see Tybalt's ghost, looking for Romeo - the one who stabbed him through the body with his sword."
        }
    },
    20: {  # Day 20: 4.5 + Review
        "scene": "Act 4, Scene 5 (condensed) + Act 4 Review",
        "reading_type": "summary",
        "page_lines": "4.5, lines 14-65 (key moments)",
        "pre_reading": {
            "context": "The morning after Juliet drinks the potion, she's discovered 'dead.' The Capulets, the Nurse, and Paris all grieve. But we know the truth - she's only asleep.",
            "vocabulary": ["dramatic irony", "lamentable", "deflowered", "solemnity"],
            "focus_question": "As you read, look for: How does our knowledge change how we view the mourning?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="4.5, lines 23-32",
                key_quote="She's dead, deceased. She's dead, alack the day!",
                prompt="The Nurse discovers Juliet. What is the dramatic irony here?",
                margin_note_suggestion="IRONY: We know she's alive. Their grief is 'real' but based on falsehood."
            ),
            AnnotationPrompt(
                line_range="4.5, lines 38-54",
                key_quote="Death lies on her like an untimely frost / Upon the sweetest flower of all the field",
                prompt="How does Lord Capulet describe Juliet's 'death'?",
                margin_note_suggestion="Tender metaphor. Same father who threatened to disown her yesterday."
            ),
            AnnotationPrompt(
                line_range="4.5, lines 55-65",
                key_quote="All things that we ordained festival / Turn from their office to black funeral",
                prompt="What changes from wedding to funeral?",
                margin_note_suggestion="Wedding → funeral. Feast → fast. Joy → grief. Total reversal."
            )
        ],
        "discussion_questions": {
            "literal": "What do the Capulets believe has happened to Juliet?",
            "interpretive": "How does dramatic irony affect our experience of this scene?",
            "evaluative": "Should we feel sympathy for the Capulets in this scene? Why or why not?"
        },
        "modern_translation": {
            "original": "Death lies on her like an untimely frost / Upon the sweetest flower of all the field",
            "modern": "Death has killed her like an early frost that destroys the most beautiful flower in the garden."
        }
    },
    21: {  # Day 21: 5.1
        "scene": "Act 5, Scene 1 - Romeo in Mantua",
        "reading_type": "shared",
        "page_lines": "5.1, lines 1-86",
        "pre_reading": {
            "context": "Romeo is in Mantua, waiting for news from Verona. He's had a dream that Juliet found him dead and kissed him back to life. Then his servant Balthasar arrives with news.",
            "vocabulary": ["Mantua", "apothecary", "dram", "mortal", "cordial"],
            "focus_question": "As you read, look for: How quickly does Romeo make his decision? Does he consider alternatives?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="5.1, lines 1-11",
                key_quote="If I may trust the flattering truth of sleep, / My dreams presage some joyful news at hand",
                prompt="What is Romeo's mood at the opening? What has he dreamed?",
                margin_note_suggestion="Optimistic! Dreams Juliet kissed him back to life. IRONY: reverse will happen"
            ),
            AnnotationPrompt(
                line_range="5.1, lines 17-26",
                key_quote="Is it e'en so? Then I defy you, stars!",
                prompt="When Romeo hears Juliet is 'dead,' what is his immediate reaction?",
                margin_note_suggestion="'I DEFY YOU, STARS!' = defying fate. But is he proving fate right?"
            ),
            AnnotationPrompt(
                line_range="5.1, lines 59-72",
                key_quote="Let me have / A dram of poison, such soon-speeding gear / As will disperse itself through all the veins",
                prompt="What does Romeo decide to do? How quickly?",
                margin_note_suggestion="Buys poison immediately. No hesitation. No checking facts. Impulsive."
            )
        ],
        "discussion_questions": {
            "literal": "What does Balthasar tell Romeo? What does Romeo decide to do?",
            "interpretive": "When Romeo says 'I defy you, stars,' is he defying fate or fulfilling it?",
            "evaluative": "If Romeo had waited one day before acting, how might the story be different?"
        },
        "modern_translation": {
            "original": "Is it e'en so? Then I defy you, stars!",
            "modern": "Is that really true? Then screw you, fate - I'll take matters into my own hands!"
        }
    },
    22: {  # Day 22: 5.2 + 5.3 Part 1
        "scene": "Act 5, Scenes 2-3 - Failed Letter & Tomb",
        "reading_type": "close",
        "page_lines": "5.2 (summary) + 5.3, lines 1-73",
        "pre_reading": {
            "context": "The Friar's letter never reached Romeo because Friar John was quarantined for plague. Romeo arrives at the tomb the same night Juliet is supposed to wake.",
            "vocabulary": ["tomb", "vault", "mattock", "wrenching iron", "banquet"],
            "focus_question": "As you read, look for: What 'if onlys' can you identify? Moments where tragedy could be avoided?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="5.2, summary",
                key_quote="I could not send it - here it is again - / Nor get a messenger to bring it thee",
                prompt="Why didn't Romeo receive the letter?",
                margin_note_suggestion="Plague quarantine! Random chance. Could happen to anyone."
            ),
            AnnotationPrompt(
                line_range="5.3, lines 12-21",
                key_quote="Give me that mattock and the wrenching iron. / Hold, take this letter. Early in the morning / See thou deliver it to my lord and father",
                prompt="What does Romeo bring to the tomb? What is he planning?",
                margin_note_suggestion="Tools to open tomb. Poison. Letter for his father. He plans to die."
            ),
            AnnotationPrompt(
                line_range="5.3, lines 45-57",
                key_quote="Stop thy unhallowed toil, vile Montague! / Condemned villain, I do apprehend thee",
                prompt="Who does Romeo encounter at the tomb? What happens?",
                margin_note_suggestion="Paris! At Juliet's tomb. Romeo kills him too. More death."
            )
        ],
        "discussion_questions": {
            "literal": "Why didn't Friar Lawrence's letter reach Romeo?",
            "interpretive": "Is the failed letter fate, or just bad luck? Does the difference matter?",
            "evaluative": "What 'what if' scenario would be most likely to save Romeo and Juliet?"
        },
        "modern_translation": {
            "original": "I could not send it - here it is again - / Nor get a messenger to bring it thee",
            "modern": "I couldn't send the letter - it's still right here - and I couldn't find anyone to deliver it to you."
        }
    },
    23: {  # Day 23: 5.3 Part 2
        "scene": "Act 5, Scene 3 - The Deaths",
        "reading_type": "choral",
        "page_lines": "5.3, lines 74-120",
        "pre_reading": {
            "context": "Romeo enters the tomb and sees Juliet, still appearing dead. He drinks the poison just moments before she wakes. The timing of the tragedy is heartbreaking.",
            "vocabulary": ["sepulcher", "dateless", "engrossing", "conduct", "pilot"],
            "focus_question": "As you read, look for: How close does Romeo come to realizing Juliet is alive?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="5.3, lines 91-96",
                key_quote="Death, that hath sucked the honey of thy breath, / Hath had no power yet upon thy beauty. / Thou art not conquered",
                prompt="What does Romeo notice about Juliet's appearance?",
                margin_note_suggestion="She still looks alive! Pink lips, no decay. HE ALMOST REALIZES!"
            ),
            AnnotationPrompt(
                line_range="5.3, lines 101-105",
                key_quote="Why art thou yet so fair? Shall I believe / That unsubstantial death is amorous?",
                prompt="Romeo questions why Juliet looks so alive. What explanation does he give himself?",
                margin_note_suggestion="He thinks Death is keeping her beautiful as a bride. Wrong answer."
            ),
            AnnotationPrompt(
                line_range="5.3, lines 115-120",
                key_quote="Here's to my love! [Drinks] O true apothecary, / Thy drugs are quick. Thus with a kiss I die",
                prompt="Romeo's final words. What is the last thing he does?",
                margin_note_suggestion="Toast to Juliet. Drinks poison. Kisses her. Dies. Seconds before she wakes."
            )
        ],
        "discussion_questions": {
            "literal": "What does Romeo say about how Juliet looks? What does he do?",
            "interpretive": "Romeo almost figures out Juliet is alive. Why doesn't he wait?",
            "evaluative": "Is this tragedy caused by fate, by human choices, or by both?"
        },
        "modern_translation": {
            "original": "Why art thou yet so fair? Shall I believe / That unsubstantial death is amorous, / And that the lean abhorred monster keeps / Thee here in dark to be his paramour?",
            "modern": "Why do you still look so beautiful? Am I supposed to believe that Death himself has fallen in love with you and is keeping you down here in the dark as his girlfriend?"
        }
    },
    24: {  # Day 24: 5.3 Part 3
        "scene": "Act 5, Scene 3 - Resolution",
        "reading_type": "shared",
        "page_lines": "5.3, lines 148-310",
        "pre_reading": {
            "context": "Juliet wakes to find Romeo dead. She kills herself with his dagger. The Prince, Capulets, and Montagues gather at the tomb as the Friar explains everything.",
            "vocabulary": ["sheathe", "reconcile", "statue", "glooming", "sacrifice"],
            "focus_question": "As you read, look for: How does the ending echo the prologue?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="5.3, lines 160-170",
                key_quote="O happy dagger, / This is thy sheath. There rust, and let me die",
                prompt="How does Juliet die? How is it different from Romeo's death?",
                margin_note_suggestion="Faster, more decisive. No long speech. 'Happy' = fitting. She acts."
            ),
            AnnotationPrompt(
                line_range="5.3, lines 285-295",
                key_quote="See what a scourge is laid upon your hate, / That heaven finds means to kill your joys with love",
                prompt="What is the Prince's judgment on the tragedy?",
                margin_note_suggestion="Your hatred caused this. Heaven used their love to punish you."
            ),
            AnnotationPrompt(
                line_range="5.3, lines 303-310",
                key_quote="For never was a story of more woe / Than this of Juliet and her Romeo",
                prompt="How does the play end? What is the final note?",
                margin_note_suggestion="Back to rhyming couplets like prologue. Circular structure. Closure."
            )
        ],
        "discussion_questions": {
            "literal": "What do the Montagues and Capulets promise at the end?",
            "interpretive": "How does the ending connect to the prologue's promise that their death 'doth bury their parents' strife'?",
            "evaluative": "Is the ending hopeful or tragic? Did the lovers' deaths mean anything?"
        },
        "modern_translation": {
            "original": "See what a scourge is laid upon your hate, / That heaven finds means to kill your joys with love",
            "modern": "Look at the punishment you've received for your hatred - God found a way to use love to destroy the things you cared about most."
        }
    },
    25: {  # Day 25: Review + Scene Selection
        "scene": "Full Play Review",
        "reading_type": "summary",
        "page_lines": "Selected key passages from all acts",
        "pre_reading": {
            "context": "Today we review the entire play and select scenes for final performances. Think about which moments affected you most and which you'd like to perform.",
            "vocabulary": ["selection", "cutting", "excerpt", "staging"],
            "focus_question": "As you review, look for: Which scenes are most powerful? Which would be best for performance?"
        },
        "annotations": [
            AnnotationPrompt(
                line_range="Prologue",
                key_quote="A pair of star-crossed lovers take their life",
                prompt="How does the prologue set up everything that follows?",
                margin_note_suggestion="Foreshadowing. We know the end from the beginning."
            ),
            AnnotationPrompt(
                line_range="2.2, lines 43-48",
                key_quote="What's in a name?",
                prompt="Why is this one of the most famous lines?",
                margin_note_suggestion="Central theme: Do names/families define us? Can love overcome identity?"
            ),
            AnnotationPrompt(
                line_range="5.3, lines 303-310",
                key_quote="For never was a story of more woe",
                prompt="How does the ending relate to the beginning?",
                margin_note_suggestion="Circular structure. Promise of prologue fulfilled."
            )
        ],
        "discussion_questions": {
            "literal": "What are the five acts of the play, and what happens in each?",
            "interpretive": "What is the main theme you take away from Romeo and Juliet?",
            "evaluative": "Which scene would you most want to perform? Why?"
        },
        "modern_translation": {
            "original": "For never was a story of more woe / Than this of Juliet and her Romeo",
            "modern": "There has never been a sadder story than the one about Juliet and Romeo."
        }
    }
}


def generate_reading_guide(day: int) -> Dict:
    """
    Generate a complete reading guide for a specific day.

    Args:
        day: Day number (1-25 for reading days)

    Returns:
        Dict containing the complete reading guide
    """
    if day not in READING_GUIDE_DATABASE:
        raise ValueError(f"No reading guide available for day {day}")

    day_data = READING_GUIDE_DATABASE[day]

    guide = {
        "day": day,
        "header": {
            "title": f"Day {day:02d} Reading Guide",
            "scene": day_data["scene"],
            "page_lines": day_data["page_lines"],
            "reading_type": READING_TYPES.get(day_data["reading_type"], day_data["reading_type"])
        },
        "pre_reading": {
            "context": day_data["pre_reading"]["context"],
            "vocabulary_preview": day_data["pre_reading"]["vocabulary"],
            "focus_question": day_data["pre_reading"]["focus_question"]
        },
        "annotations": [],
        "discussion_questions": day_data["discussion_questions"],
        "modern_translation": day_data["modern_translation"]
    }

    for annotation in day_data["annotations"]:
        guide["annotations"].append({
            "line_range": annotation.line_range,
            "key_quote": annotation.key_quote,
            "annotation_prompt": annotation.prompt,
            "margin_note_suggestion": annotation.margin_note_suggestion
        })

    return guide


def validate_reading_guide(guide: Dict) -> Dict:
    """
    Validate a reading guide against generation rules.

    Rules:
    - R1: Must include specific line numbers from actual play
    - R2: Must have 3 annotation prompts minimum
    - R3: Must include at least one modern translation
    - R4: Questions must scaffold (literal → interpretive → evaluative)
    - R5: Must connect to day's learning objectives

    Returns:
        Dict with validation status and any issues found
    """
    issues = []

    # R1: Check line numbers
    for annotation in guide.get("annotations", []):
        if "lines" not in annotation.get("line_range", "").lower() and "prologue" not in annotation.get("line_range", "").lower():
            issues.append(f"Annotation missing line numbers: {annotation.get('line_range')}")

    # R2: Check annotation count
    if len(guide.get("annotations", [])) < 3:
        issues.append("Fewer than 3 annotation prompts")

    # R3: Check modern translation
    if not guide.get("modern_translation") or not guide["modern_translation"].get("modern"):
        issues.append("Missing modern translation")

    # R4: Check discussion question scaffolding
    questions = guide.get("discussion_questions", {})
    required_types = ["literal", "interpretive", "evaluative"]
    for q_type in required_types:
        if q_type not in questions:
            issues.append(f"Missing {q_type} discussion question")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "guide": guide
    }


def generate_reading_guide_markdown(guide: Dict) -> str:
    """Generate markdown format of the reading guide for output."""
    lines = [
        f"# {guide['header']['title']}",
        "",
        f"**Scene:** {guide['header']['scene']}",
        f"**Pages/Lines:** {guide['header']['page_lines']}",
        f"**Reading Type:** {guide['header']['reading_type']}",
        "",
        "---",
        "",
        "## Pre-Reading",
        "",
        f"**Context:** {guide['pre_reading']['context']}",
        "",
        "**Vocabulary Preview:**",
    ]

    for term in guide["pre_reading"]["vocabulary_preview"]:
        lines.append(f"- {term}")

    lines.extend([
        "",
        f"**Focus Question:** {guide['pre_reading']['focus_question']}",
        "",
        "---",
        "",
        "## During Reading: Annotation Guide",
        ""
    ])

    for i, annotation in enumerate(guide["annotations"], 1):
        lines.extend([
            f"### Section {i}: {annotation['line_range']}",
            "",
            f"**Key Quote to Mark:**",
            f"> \"{annotation['key_quote']}\"",
            "",
            f"**Annotation Prompt:** {annotation['annotation_prompt']}",
            "",
            f"**Margin Note Suggestion:** _{annotation['margin_note_suggestion']}_",
            ""
        ])

    lines.extend([
        "---",
        "",
        "## Discussion Questions",
        "",
        f"1. **Literal:** {guide['discussion_questions']['literal']}",
        f"2. **Interpretive:** {guide['discussion_questions']['interpretive']}",
        f"3. **Evaluative:** {guide['discussion_questions']['evaluative']}",
        "",
        "---",
        "",
        "## Modern Translation Box",
        "",
        "**Most Challenging Passage:**",
        "",
        f"**Original:** \"{guide['modern_translation']['original']}\"",
        "",
        f"**Modern:** \"{guide['modern_translation']['modern']}\""
    ])

    return "\n".join(lines)


def generate_all_reading_guides() -> List[Dict]:
    """Generate reading guides for all 25 reading days."""
    guides = []

    for day in range(1, 26):
        if day in READING_GUIDE_DATABASE:
            guide = generate_reading_guide(day)
            validation = validate_reading_guide(guide)
            guide["validation"] = validation
            guides.append(guide)

    return guides


# Export main components
__all__ = [
    'generate_reading_guide',
    'validate_reading_guide',
    'generate_reading_guide_markdown',
    'generate_all_reading_guides',
    'READING_GUIDE_DATABASE',
    'READING_TYPES',
    'ReadingGuide',
    'AnnotationPrompt'
]
