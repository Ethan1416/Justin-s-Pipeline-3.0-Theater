# Differentiation Annotator

## Purpose
Add differentiation annotations to lesson components to support diverse learners including ELL students, advanced learners, and struggling students. Annotations appear in presenter notes and handouts.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
  - sentence_completeness_checker
```

## Input Schema
```json
{
  "lesson_components": {
    "warmup": {
      "name": "Greek Chorus Walk",
      "instructions": ["Stand in a circle", "Walk as a unified group"]
    },
    "content": {
      "vocabulary": ["theatron", "orchestra", "skene"],
      "key_concepts": ["Greek theater architecture", "Audience-performer relationship"]
    },
    "activity": {
      "name": "Theater Blueprint Analysis",
      "type": "gallery_walk",
      "instructions": "Rotate through stations analyzing Greek theater components"
    },
    "journal_prompt": "How might the design of the Greek theater have affected the performance style of actors?"
  },
  "student_population": {
    "ell_percentage": 15,
    "iep_percentage": 12,
    "advanced_percentage": 10
  }
}
```

## Output Schema
```json
{
  "differentiation_annotations": {
    "warmup_modifications": {
      "ell": "Demonstrate movements before verbal instructions. Use simple command words.",
      "advanced": "Lead a portion of the warmup. Add complexity with rhythm changes.",
      "struggling": "Pair with peer model. Allow modified participation level."
    },
    "vocabulary_supports": [
      {
        "term": "theatron",
        "ell_support": "Show image of amphitheater seating. Root word 'thea' = to see (like 'theater').",
        "visual_cue": "Draw simple stadium shape",
        "cognate_note": "Similar to Spanish 'teatro'"
      }
    ],
    "activity_modifications": {
      "ell": "Provide sentence frames for analysis. Pair with bilingual peer.",
      "advanced": "Add comparison task - how does this differ from modern theaters?",
      "struggling": "Pre-teach vocabulary. Provide graphic organizer with word bank."
    },
    "assessment_accommodations": {
      "ell": "Allow drawing or labeling instead of full sentences.",
      "advanced": "Add extension question requiring synthesis.",
      "struggling": "Provide word bank for exit ticket."
    },
    "presenter_note_callouts": [
      {
        "location": "slide_6",
        "callout": "[DIFFERENTIATION: Point to diagram while saying 'theatron' - visual support for ELL]"
      }
    ]
  }
}
```

## Differentiation Categories

### 1. ELL (English Language Learners)

#### Strategies
| Strategy | Application |
|----------|-------------|
| Visual supports | Diagrams, images, gestures with vocabulary |
| Sentence frames | "The [term] is used for ___" |
| Cognates | Spanish, Vietnamese, Mandarin cognates when available |
| Pre-teaching | Frontload key vocabulary before lesson |
| Peer support | Strategic bilingual partner pairing |
| Simplified language | Reduce idioms, use clear syntax |

#### Presenter Note Markers
```
[ELL: Gesture while speaking]
[ELL: Point to visual]
[ELL: Provide sentence frame: "The theatron is where ___"]
```

### 2. Advanced Learners

#### Strategies
| Strategy | Application |
|----------|-------------|
| Extension questions | "How might this compare to...?" |
| Leadership roles | Lead warmup portion, facilitate discussion |
| Research connections | Connect to broader historical context |
| Creative challenge | Design alternative theater layout |
| Peer teaching | Explain concept to partner |
| Depth questions | "Why do you think the Greeks chose this design?" |

#### Presenter Note Markers
```
[ADVANCED: Ask extension question about modern comparisons]
[ADVANCED: Invite student to demonstrate]
[ADVANCED: Challenge to find additional examples]
```

### 3. Struggling Learners

#### Strategies
| Strategy | Application |
|----------|-------------|
| Chunking | Break instructions into smaller steps |
| Peer support | Strategic partner pairing |
| Graphic organizers | Visual frameworks for note-taking |
| Word banks | Pre-populated vocabulary lists |
| Check-ins | Frequent comprehension checks |
| Modified output | Drawing instead of writing |

#### Presenter Note Markers
```
[STRUGGLING: Check in with table groups]
[STRUGGLING: Provide graphic organizer]
[STRUGGLING: Allow partner work]
```

## Component-Specific Differentiation

### Warmup Differentiation
```
ELL: Demonstrate movements before verbal instructions. Use simple command words (stand, walk, stop).

Advanced: Lead a portion of the warmup after initial modeling. Add complexity with rhythm changes or call-and-response.

Struggling: Pair with peer model. Allow modified participation (e.g., watching first round before joining).
```

### Lecture Differentiation
```
ELL: Point to visuals while introducing vocabulary. Use consistent phrasing. Pause after key terms.

Advanced: Pose "why" questions during [CHECK FOR UNDERSTANDING]. Invite connections to prior knowledge.

Struggling: Provide skeleton notes or graphic organizer. Check in at transitions.
```

### Activity Differentiation
```
ELL: Provide sentence frames for written responses. Pair with bilingual peer when possible.

Advanced: Add synthesis task (compare/contrast, evaluate, create). Assign facilitator role.

Struggling: Pre-teach vocabulary. Provide graphic organizer with word bank. Reduce number of stations if needed.
```

### Journal Differentiation
```
ELL: Allow drawing or labeled diagram instead of full sentences. Provide sentence starters.

Advanced: Add extension question requiring synthesis across units or connection to personal experience.

Struggling: Provide word bank. Allow bullet points instead of paragraphs. Offer verbal response option.
```

## Vocabulary Support Format

For each vocabulary term, generate:

```json
{
  "term": "theatron",
  "pronunciation": "THEE-uh-tron",
  "definition": "The seating area for the audience in a Greek theater",
  "ell_support": {
    "visual_cue": "Draw stadium-shaped seating area",
    "cognate": "Spanish 'teatro', French 'theatre'",
    "root_word": "'thea' = to see/watch",
    "sentence_frame": "The theatron is where the ___ sits."
  },
  "advanced_connection": "Compare to modern stadium seating - what design principles remain?",
  "struggling_support": "Sounds like 'theater' - it's where people watch"
}
```

## Presenter Note Integration

Insert differentiation markers at strategic points:

```
...the theatron could seat up to 17,000 spectators. [PAUSE]

[ELL: Point to diagram and trace the seating area shape]
[STRUGGLING: Check - can everyone see the diagram clearly?]

That's more people than most modern theaters hold! [EMPHASIS: 17,000]

[ADVANCED: Why do you think Greek theaters were so large?]

[CHECK FOR UNDERSTANDING]
```

## Activity Handout Modifications

### Standard Version
Full instructions, standard vocabulary, complete sentences required.

### ELL Version
- Sentence frames provided
- Visuals included
- Simplified instructions
- Word bank included

### Advanced Version
- Extension questions added
- Research connections
- Creative challenge options

### Struggling Version
- Graphic organizer format
- Word bank included
- Reduced writing requirements
- Check boxes for completion

## Error Handling
- If no ELL population indicated, still include visual supports (benefits all)
- If vocabulary lacks cognates, use root words and visual cues
- If activity type doesn't lend to differentiation, focus on grouping strategies

## Validation Checklist
- [ ] All three learner categories addressed (ELL, Advanced, Struggling)
- [ ] Warmup, lecture, activity, and assessment all have modifications
- [ ] Vocabulary supports include visual cues and sentence frames
- [ ] Presenter note callouts use consistent marker format
- [ ] Modifications are practical and implementable
- [ ] No truncation in differentiation text
