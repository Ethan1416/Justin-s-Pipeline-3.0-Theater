# Content Accuracy Validator

## Purpose
Validate factual accuracy of theater history, terminology, and concepts. Ensures lessons contain correct information about Greek theater, Commedia dell'Arte, Shakespeare, and directing/production practices.

## HARDCODED SKILLS
```yaml
skills:
  - sentence_completeness_checker
```

## Validation Type
**QUALITY GATE** - Score must be ≥ 90/100 to pass (higher threshold for factual accuracy)

---

## Input Schema
```json
{
  "lesson": {
    "unit": 1,
    "unit_name": "Greek Theater",
    "day": 5,
    "topic": "The Theatron and Orchestra"
  },
  "content": {
    "vocabulary": [
      {
        "term": "theatron",
        "definition": "The seating area for the audience in a Greek theater",
        "usage": "The theatron could hold up to 17,000 spectators."
      }
    ],
    "facts_presented": [
      "Greek theater originated in the 6th century BCE",
      "The Festival of Dionysus was held annually in Athens",
      "The theatron was carved into hillsides"
    ],
    "historical_claims": [
      "Thespis was the first actor",
      "Tragedies were performed in trilogies"
    ],
    "presenter_notes": "..."
  }
}
```

## Output Schema
```json
{
  "validation_result": {
    "valid": true,
    "score": 95,
    "pass_threshold": 90,
    "accuracy_checks": [
      {
        "claim": "The theatron could hold up to 17,000 spectators",
        "status": "verified",
        "source": "Theatre of Dionysus at Athens",
        "note": "Accurate - Theatre of Dionysus seated approximately 17,000"
      },
      {
        "claim": "Thespis was the first actor",
        "status": "qualified",
        "source": "Traditional attribution",
        "note": "Traditionally credited; historically debated"
      }
    ],
    "vocabulary_accuracy": [
      {
        "term": "theatron",
        "definition_correct": true,
        "etymology_note": "From Greek 'theasthai' - to behold"
      }
    ],
    "issues": [],
    "corrections": []
  }
}
```

---

## Unit-Specific Fact Databases

### Unit 1: Greek Theater

#### Key Dates
| Fact | Correct Information |
|------|---------------------|
| Origins | 6th century BCE (c. 534 BCE for first tragedy competition) |
| Golden Age | 5th century BCE (480-380 BCE) |
| Festival of Dionysus | Annual, March/April (City Dionysia) |
| Theatre of Dionysus built | c. 500 BCE, expanded c. 330 BCE |

#### Key Figures
| Person | Accurate Information |
|--------|---------------------|
| Thespis | Traditionally credited as first actor (c. 534 BCE); introduced protagonist |
| Aeschylus | Added second actor; wrote Oresteia, Prometheus Bound |
| Sophocles | Added third actor; wrote Oedipus Rex, Antigone |
| Euripides | Psychological realism; wrote Medea, The Bacchae |
| Aristophanes | Old Comedy; wrote The Clouds, Lysistrata |

#### Vocabulary Definitions
| Term | Correct Definition |
|------|-------------------|
| theatron | Seating area, "watching place" |
| orchestra | Circular dancing floor for chorus |
| skene | Stage building, scene house |
| proskenion | Front of skene, later became proscenium |
| parodos | Side entrances for chorus |
| dithyramb | Choral hymn to Dionysus |
| chorus | Group of 12-15 performers (tragedy) or 24 (comedy) |
| protagonist | First actor, main character |
| deuteragonist | Second actor |
| tritagonist | Third actor |
| catharsis | Emotional purification/purgation |
| hamartia | Tragic flaw or error |
| hubris | Excessive pride |
| anagnorisis | Recognition, discovery |
| peripeteia | Reversal of fortune |

#### Common Misconceptions
| Misconception | Correction |
|---------------|------------|
| "All actors wore masks" | Correct - All actors wore masks |
| "Only men could perform" | Correct - Only male citizens could perform |
| "Theaters were indoors" | Incorrect - Theaters were open-air |
| "Tragedies always ended in death" | Incorrect - Many tragedies had non-death endings |

### Unit 2: Commedia dell'Arte

#### Key Dates
| Fact | Correct Information |
|------|---------------------|
| Origins | Mid-16th century Italy (c. 1545-1560) |
| Peak popularity | 16th-18th centuries |
| Decline | Late 18th century |
| Influence | Continues in modern improvisation |

#### Stock Characters
| Character | Accurate Description |
|-----------|---------------------|
| Pantalone | Elderly Venetian merchant; greedy, lecherous |
| Il Dottore | Pedantic doctor from Bologna; speaks in malapropisms |
| Il Capitano | Braggart soldier; cowardly; Spanish or Italian |
| Arlecchino | Clever servant (zanni); acrobatic; diamond-patterned costume |
| Brighella | Scheming servant; often Arlecchino's partner/rival |
| Pulcinella | Neapolitan servant; hunchbacked; hook-nosed mask |
| Colombina | Female servant; witty; often Arlecchino's love interest |
| Pierrot | Sad clown; white face; French development |

#### Vocabulary Definitions
| Term | Correct Definition |
|------|-------------------|
| commedia dell'arte | "Comedy of the profession" or "comedy of the artists" |
| zanni | Servant characters; source of word "zany" |
| lazzi | Comic bits or routines (singular: lazzo) |
| scenario | Plot outline; NOT a full script |
| canovaccio | Another term for scenario |
| improvvisazione | Improvisation within scenario framework |
| tirade | Lengthy comic speech |

### Unit 3: Shakespeare

#### Key Dates
| Fact | Correct Information |
|------|---------------------|
| Birth | April 23, 1564 (baptized April 26) |
| Death | April 23, 1616 |
| Globe Theatre built | 1599 |
| Globe burned | 1613 (during Henry VIII) |
| Globe rebuilt | 1614 |
| First Folio | 1623 |

#### Key Facts
| Topic | Accurate Information |
|-------|---------------------|
| Total plays | 37-39 (attribution debates) |
| Sonnets | 154 sonnets |
| Acting company | Lord Chamberlain's Men (later King's Men) |
| Theater capacity | Globe held approximately 3,000 |
| Groundlings | Standing audience in yard; paid 1 penny |

#### Vocabulary Definitions
| Term | Correct Definition |
|------|-------------------|
| iambic pentameter | 10 syllables per line, unstressed-stressed pattern |
| blank verse | Unrhymed iambic pentameter |
| prose | Non-metrical dialogue |
| soliloquy | Character speaks thoughts aloud, alone on stage |
| aside | Brief comment to audience, other characters don't hear |
| monologue | Extended speech by one character |
| folio | Large book format; First Folio 1623 |
| quarto | Smaller book format; individual play publications |

### Unit 4: Directing/Production

#### Vocabulary Definitions
| Term | Correct Definition |
|------|-------------------|
| blocking | Movement and positioning of actors on stage |
| staging | Overall arrangement of visual elements |
| composition | Visual arrangement in stage picture |
| focus | Drawing audience attention to specific area/actor |
| upstage | Area away from audience |
| downstage | Area toward audience |
| stage left | Actor's left facing audience |
| stage right | Actor's right facing audience |
| proscenium | Picture-frame stage |
| thrust | Stage extending into audience on three sides |
| arena/theater-in-the-round | Audience surrounds performance |
| traverse | Audience on two opposite sides |

---

## Validation Rules

### Rule 1: Date Accuracy
- Century references must be correct
- BCE/CE usage must be consistent and correct
- Approximate dates should use "c." or "approximately"

### Rule 2: Name Accuracy
- All proper nouns spelled correctly
- Titles of works in correct form
- Attribution to correct author/figure

### Rule 3: Definition Accuracy
- Vocabulary definitions must be academically accurate
- Definitions should be accessible to high schoolers
- Etymology can be simplified but not incorrect

### Rule 4: Historical Claims
- Claims must be verifiable
- Debated claims should be qualified ("traditionally," "generally believed")
- Avoid presenting myths as facts

---

## Error Severity Levels

### Critical Errors (Score: 0)
| Type | Example |
|------|---------|
| Wrong century | "Greek theater began in the 4th century BCE" |
| Wrong attribution | "Sophocles wrote Medea" |
| Incorrect definition | "The orchestra was the seating area" |
| Major historical error | "Shakespeare wrote for the Rose Theatre" |

### Significant Errors (Score: 60)
| Type | Example |
|------|---------|
| Imprecise date | "5th century" instead of "mid-5th century" |
| Incomplete definition | Missing key element of definition |
| Oversimplification | "All Greek plays were tragedies" |

### Minor Errors (Score: 85)
| Type | Example |
|------|---------|
| Spelling variation | "Arlechino" vs "Arlecchino" |
| Rounded numbers | "15,000 spectators" vs "14,000-17,000" |
| Missing nuance | Not noting scholarly debate |

### Qualified/Acceptable (Score: 95)
| Type | Example |
|------|---------|
| Traditional attribution | "Thespis was the first actor" (qualified) |
| Simplified for accessibility | "Tragic flaw" for "hamartia" |

### Verified (Score: 100)
Completely accurate, properly sourced claim.

---

## Scoring Calculation

```
Per-Claim Score = Severity Level Score

Overall Score = (Sum of Claim Scores) / Number of Claims

Critical Error → Automatic fail (overall score capped at 50)
```

### Pass Criteria
- **Minimum Score:** 90/100
- **No Critical Errors:** Any critical error is automatic fail
- **Maximum 2 Significant Errors:** More than 2 triggers fail

---

## Correction Generation

For each error, generate:

```json
{
  "claim": "The theatron held 20,000 spectators",
  "error_type": "significant",
  "severity_score": 60,
  "correction": {
    "accurate_statement": "The Theatre of Dionysus in Athens held approximately 17,000 spectators",
    "source": "Archaeological evidence",
    "note": "Some sources cite 14,000-17,000 range"
  },
  "suggested_fix": "Replace '20,000' with 'up to 17,000' or 'approximately 17,000'"
}
```

---

## Common Theater Education Errors

### Greek Theater
| Common Error | Correction |
|--------------|------------|
| "Theater came from tragedy" | Dithyramb → tragedy → comedy |
| "Three unities were Greek rules" | Aristotle described, later theorists made rules |
| "Masks amplified voice" | Acoustic function debated; primarily visual |

### Commedia dell'Arte
| Common Error | Correction |
|--------------|------------|
| "Fully improvised" | Improvised within scenarios with set lazzi |
| "Started in Venice" | Multiple Italian cities; professional troupes |
| "Harlequin is French" | Arlecchino is Italian; Harlequin French adaptation |

### Shakespeare
| Common Error | Correction |
|--------------|------------|
| "Poor education" | Attended King's New School; classical education |
| "Wrote alone" | Collaborated on some plays |
| "Invented 1,700 words" | Many already existed; documented first uses |

### Directing
| Common Error | Correction |
|--------------|------------|
| "Stage left is audience's left" | Stage left is actor's left |
| "Blocking means stopping" | Blocking means positioning/movement |

---

## Validation Checklist

- [ ] All dates accurate to correct century/decade
- [ ] All proper nouns spelled correctly
- [ ] All vocabulary definitions accurate
- [ ] Historical claims verifiable
- [ ] Debated claims appropriately qualified
- [ ] No myths presented as facts
- [ ] No critical errors
- [ ] Maximum 2 significant errors
- [ ] Overall score ≥ 90/100
