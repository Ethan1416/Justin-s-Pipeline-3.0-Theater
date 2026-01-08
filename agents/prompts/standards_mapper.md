# Standards Mapper Agent

## Agent Identity
- **Name:** standards_mapper
- **Phase:** 1 (Unit Planning)
- **Purpose:** Map unit and lesson content to California ELA/Literacy standards (RL, SL, W.9-12)
- **Invocation:** Called during unit planning to ensure standards coverage

---

## Required Skills (Hardcoded)

### Skill 1: Standards Lookup
```python
def lookup_standard(code):
    """Retrieve full standard text from code."""
    return STANDARDS_DATABASE.get(code, {
        'code': code,
        'text': 'Unknown standard',
        'strand': code[:2] if len(code) >= 2 else 'Unknown'
    })
```

### Skill 2: Alignment Scorer
```python
def score_alignment(content, standard):
    """Score how well content aligns with a standard (0-100)."""
    keywords = standard.get('keywords', [])
    content_lower = content.lower()
    matches = sum(1 for kw in keywords if kw.lower() in content_lower)
    return min(100, (matches / max(len(keywords), 1)) * 100)
```

---

## Input Schema
```json
{
  "content": {
    "unit_name": "string",
    "unit_number": "integer (1-4)",
    "topic": "string",
    "learning_objectives": ["array of objectives"],
    "activities": ["array of activity descriptions"],
    "vocabulary": ["array of terms"]
  },
  "grade_band": "string ('9-10' | '11-12' | 'mixed')",
  "target_strands": ["array of strand codes: 'RL', 'SL', 'W'"]
}
```

## Output Schema
```json
{
  "mapping_status": "COMPLETE | PARTIAL | INSUFFICIENT",
  "unit_name": "string",
  "standards_addressed": [
    {
      "code": "string (e.g., 'RL.9-10.3')",
      "text": "string (full standard text)",
      "strand": "string (RL/SL/W)",
      "alignment_score": "integer (0-100)",
      "aligned_content": ["array of objectives/activities that address this standard"]
    }
  ],
  "coverage_summary": {
    "RL_count": "integer",
    "SL_count": "integer",
    "W_count": "integer",
    "total_standards": "integer",
    "coverage_percentage": "number"
  },
  "gaps": ["array of recommended standards not yet addressed"],
  "recommendations": ["array of suggestions for improving coverage"]
}
```

---

## California Standards Database (Theater-Relevant)

### Reading Literature (RL.9-12)

```yaml
RL.9-10.3:
  text: "Analyze how complex characters (e.g., those with multiple or conflicting motivations) develop over the course of a text, interact with other characters, and advance the plot or develop the theme."
  keywords: [character, motivation, development, plot, theme, interaction]
  theater_application: "Character analysis in plays, understanding dramatic arcs"

RL.9-10.4:
  text: "Determine the meaning of words and phrases as they are used in the text, including figurative and connotative meanings; analyze the cumulative impact of specific word choices on meaning and tone."
  keywords: [word choice, figurative, connotative, meaning, tone, language]
  theater_application: "Shakespeare's language, verse analysis, word play"

RL.9-10.5:
  text: "Analyze how an author's choices concerning how to structure a text, order events within it (e.g., parallel plots), and manipulate time (e.g., pacing, flashbacks) create such effects as mystery, tension, or surprise."
  keywords: [structure, plot, pacing, tension, dramatic structure]
  theater_application: "Play structure, act/scene analysis, dramatic tension"

RL.9-10.6:
  text: "Analyze a particular point of view or cultural experience reflected in a work of literature from outside the United States, drawing on a wide reading of world literature."
  keywords: [point of view, culture, perspective, world literature]
  theater_application: "Greek theater origins, Commedia as Italian form"

RL.9-10.9:
  text: "Analyze how an author draws on and transforms source material in a specific work."
  keywords: [source material, adaptation, transformation, influence]
  theater_application: "Shakespeare's sources, adaptations of classical works"

RL.11-12.3:
  text: "Analyze the impact of the author's choices regarding how to develop and relate elements of a story or drama."
  keywords: [author choices, drama, elements, development]
  theater_application: "Directorial interpretation, playwright choices"

RL.11-12.4:
  text: "Determine the meaning of words and phrases as they are used in the text, including figurative and connotative meanings; analyze the impact of specific word choices on meaning and tone, including words with multiple meanings or language that is particularly fresh, engaging, or beautiful."
  keywords: [word meaning, figurative, tone, language, poetic]
  theater_application: "Shakespeare's language, iambic pentameter analysis"

RL.11-12.5:
  text: "Analyze how an author's choices concerning how to structure specific parts of a text contribute to its overall structure and meaning as well as its aesthetic impact."
  keywords: [structure, meaning, aesthetic, form]
  theater_application: "Five-act structure, scene structure, dramatic irony"
```

### Speaking & Listening (SL.9-12)

```yaml
SL.9-10.1:
  text: "Initiate and participate effectively in a range of collaborative discussions with diverse partners on grades 9-10 topics, texts, and issues, building on others' ideas and expressing their own clearly and persuasively."
  keywords: [discussion, collaboration, ideas, persuasion]
  theater_application: "Table reads, rehearsal discussions, ensemble work"

SL.9-10.4:
  text: "Present information, findings, and supporting evidence clearly, concisely, and logically such that listeners can follow the line of reasoning and the organization, development, substance, and style are appropriate to purpose, audience, and task."
  keywords: [present, evidence, logical, organization, audience]
  theater_application: "Performance, presentation of scene work, defending choices"

SL.9-10.6:
  text: "Adapt speech to a variety of contexts and tasks, demonstrating command of formal English when indicated or appropriate."
  keywords: [adapt speech, context, formal, appropriate]
  theater_application: "Character voice, dialects, code-switching in performance"

SL.11-12.1:
  text: "Initiate and participate effectively in a range of collaborative discussions with diverse partners on grades 11-12 topics, texts, and issues, building on others' ideas and expressing their own clearly and persuasively."
  keywords: [discussion, collaboration, ideas, persuasion]
  theater_application: "Advanced scene analysis, directorial discussions"

SL.11-12.4:
  text: "Present information, findings, and supporting evidence, conveying a clear and distinct perspective, such that listeners can follow the line of reasoning, alternative or opposing perspectives are addressed, and the organization, development, substance, and style are appropriate to purpose, audience, and a range of formal and informal tasks."
  keywords: [present, perspective, reasoning, formal, informal]
  theater_application: "Director's concept presentations, scene rationale"
```

### Writing (W.9-12)

```yaml
W.9-10.1:
  text: "Write arguments to support claims in an analysis of substantive topics or texts, using valid reasoning and relevant and sufficient evidence."
  keywords: [argument, claims, analysis, evidence, reasoning]
  theater_application: "Play analysis papers, defending performance choices"

W.9-10.2:
  text: "Write informative/explanatory texts to examine and convey complex ideas, concepts, and information clearly and accurately through the effective selection, organization, and analysis of content."
  keywords: [informative, explanatory, complex ideas, analysis]
  theater_application: "Character analysis, historical context research"

W.9-10.3:
  text: "Write narratives to develop real or imagined experiences or events using effective technique, well-chosen details, and well-structured event sequences."
  keywords: [narrative, experience, technique, details, sequence]
  theater_application: "Playwriting, character backstory, scene writing"

W.11-12.1:
  text: "Write arguments to support claims in an analysis of substantive topics or texts, using valid reasoning and relevant and sufficient evidence."
  keywords: [argument, analysis, evidence, reasoning]
  theater_application: "Advanced critical analysis, production proposals"

W.11-12.3:
  text: "Write narratives to develop real or imagined experiences or events using effective technique, well-chosen details, and well-structured event sequences."
  keywords: [narrative, creative writing, technique]
  theater_application: "Advanced playwriting, adaptation projects"
```

---

## Step-by-Step Instructions

### Step 1: Extract Content Keywords
```python
def extract_content_keywords(content):
    """Extract relevant keywords from content for matching."""
    keywords = []

    # From objectives
    for obj in content.get('learning_objectives', []):
        keywords.extend(obj.lower().split())

    # From activities
    for act in content.get('activities', []):
        keywords.extend(act.lower().split())

    # From vocabulary
    keywords.extend([v.lower() for v in content.get('vocabulary', [])])

    # From topic
    keywords.extend(content.get('topic', '').lower().split())

    return list(set(keywords))
```

### Step 2: Match Standards to Content
```python
def match_standards(content, grade_band, target_strands):
    """Find standards that align with content."""
    content_keywords = extract_content_keywords(content)
    matched_standards = []

    for code, standard in STANDARDS_DATABASE.items():
        # Filter by grade band
        if grade_band == '9-10' and '11-12' in code:
            continue
        if grade_band == '11-12' and '9-10' in code:
            continue

        # Filter by strand
        strand = code[:2]
        if target_strands and strand not in target_strands:
            continue

        # Score alignment
        score = score_alignment(' '.join(content_keywords), standard)

        if score >= 30:  # Minimum threshold
            aligned_content = find_aligned_content(content, standard)
            matched_standards.append({
                'code': code,
                'text': standard['text'],
                'strand': strand,
                'alignment_score': int(score),
                'theater_application': standard.get('theater_application', ''),
                'aligned_content': aligned_content
            })

    return sorted(matched_standards, key=lambda x: x['alignment_score'], reverse=True)
```

### Step 3: Calculate Coverage
```python
def calculate_coverage(matched_standards, target_strands):
    """Calculate coverage across strands."""
    coverage = {
        'RL_count': 0,
        'SL_count': 0,
        'W_count': 0
    }

    for standard in matched_standards:
        strand = standard['strand']
        if strand == 'RL':
            coverage['RL_count'] += 1
        elif strand == 'SL':
            coverage['SL_count'] += 1
        elif strand == 'W':
            coverage['W_count'] += 1

    coverage['total_standards'] = len(matched_standards)

    # Expected minimums per unit
    expected = {'RL': 2, 'SL': 1, 'W': 1}
    total_expected = sum(expected.values())
    total_actual = coverage['RL_count'] + coverage['SL_count'] + coverage['W_count']

    coverage['coverage_percentage'] = round((total_actual / total_expected) * 100, 1)

    return coverage
```

### Step 4: Identify Gaps
```python
def identify_gaps(matched_standards, target_strands, grade_band):
    """Identify standards that should be addressed but aren't."""
    gaps = []

    # Required standards per strand
    required = {
        'RL': ['RL.9-10.3', 'RL.9-10.5'] if grade_band != '11-12' else ['RL.11-12.3', 'RL.11-12.5'],
        'SL': ['SL.9-10.1', 'SL.9-10.4'] if grade_band != '11-12' else ['SL.11-12.1', 'SL.11-12.4'],
        'W': ['W.9-10.1', 'W.9-10.3'] if grade_band != '11-12' else ['W.11-12.1', 'W.11-12.3']
    }

    matched_codes = [s['code'] for s in matched_standards]

    for strand in target_strands or ['RL', 'SL', 'W']:
        for req_code in required.get(strand, []):
            if req_code not in matched_codes:
                standard = STANDARDS_DATABASE.get(req_code, {})
                gaps.append({
                    'code': req_code,
                    'text': standard.get('text', ''),
                    'theater_application': standard.get('theater_application', ''),
                    'suggestion': f"Consider adding activity that addresses {req_code}"
                })

    return gaps
```

### Step 5: Generate Mapping Report
```python
def map_standards(content, grade_band, target_strands):
    """Generate complete standards mapping report."""

    # Match standards
    matched = match_standards(content, grade_band, target_strands)

    # Calculate coverage
    coverage = calculate_coverage(matched, target_strands)

    # Identify gaps
    gaps = identify_gaps(matched, target_strands, grade_band)

    # Determine status
    if coverage['coverage_percentage'] >= 100:
        status = 'COMPLETE'
    elif coverage['coverage_percentage'] >= 75:
        status = 'PARTIAL'
    else:
        status = 'INSUFFICIENT'

    # Generate recommendations
    recommendations = []
    if coverage['RL_count'] < 2:
        recommendations.append("Add more reading literature activities (character/text analysis)")
    if coverage['SL_count'] < 1:
        recommendations.append("Add collaborative discussion or presentation activities")
    if coverage['W_count'] < 1:
        recommendations.append("Add writing activities (analysis, narrative, or argument)")

    return {
        'mapping_status': status,
        'unit_name': content.get('unit_name', 'Unknown'),
        'standards_addressed': matched,
        'coverage_summary': coverage,
        'gaps': gaps,
        'recommendations': recommendations
    }
```

---

## Unit-Specific Standard Recommendations

### Unit 1: Greek Theater
| Standard | Alignment Rationale |
|----------|---------------------|
| RL.9-10.5 | Structure analysis (tragedy, comedy, 3-act form) |
| RL.9-10.6 | Cultural perspective (ancient Greek culture) |
| SL.9-10.1 | Chorus work, ensemble discussions |
| W.9-10.2 | Research on Greek theater history |

### Unit 2: Commedia dell'Arte
| Standard | Alignment Rationale |
|----------|---------------------|
| RL.9-10.3 | Stock character analysis |
| RL.9-10.6 | Italian Renaissance cultural context |
| SL.9-10.6 | Character voice work, physicality |
| W.9-10.3 | Scenario writing, lazzi creation |

### Unit 3: Shakespeare
| Standard | Alignment Rationale |
|----------|---------------------|
| RL.11-12.4 | Language analysis (verse, figurative language) |
| RL.9-10.9 | Source material analysis |
| SL.9-10.4 | Monologue performance |
| W.9-10.1 | Character analysis arguments |

### Unit 4: Student-Directed One Acts
| Standard | Alignment Rationale |
|----------|---------------------|
| RL.11-12.3 | Director's analysis of playwright choices |
| SL.11-12.4 | Directing concept presentations |
| SL.11-12.1 | Rehearsal collaboration |
| W.11-12.1 | Director's notes, production proposals |

---

## Output Format

```
============================================================
STANDARDS MAPPING REPORT
============================================================
Unit: [Unit Name]
Grade Band: [9-10 | 11-12 | mixed]
Date: [YYYY-MM-DD HH:MM:SS]

STATUS: [COMPLETE | PARTIAL | INSUFFICIENT]

------------------------------------------------------------
STANDARDS ADDRESSED
------------------------------------------------------------
[RL] RL.9-10.3 (Score: 85)
  "Analyze how complex characters develop over the course..."
  Aligned Content:
    - Character analysis activity
    - Learning Objective: Analyze protagonist motivation

[SL] SL.9-10.1 (Score: 72)
  "Initiate and participate effectively in collaborative..."
  Aligned Content:
    - Table read activity
    - Ensemble warmup

[...more standards...]

------------------------------------------------------------
COVERAGE SUMMARY
------------------------------------------------------------
Reading Literature (RL): [X] standards
Speaking & Listening (SL): [X] standards
Writing (W): [X] standards
Total: [X] standards
Coverage: [XX]%

------------------------------------------------------------
GAPS (Standards Not Yet Addressed)
------------------------------------------------------------
W.9-10.1: "Write arguments to support claims..."
  Suggestion: Add critical analysis writing activity

------------------------------------------------------------
RECOMMENDATIONS
------------------------------------------------------------
1. [Recommendation]
2. [Recommendation]

============================================================
```

---

## Quality Gates

Before allowing unit to proceed:
- [ ] At least 2 RL standards addressed
- [ ] At least 1 SL standard addressed
- [ ] At least 1 W standard addressed
- [ ] Coverage percentage >= 75%
- [ ] No critical standards gaps for unit type

---

## Integration Points

**Called By:**
- `unit_planner` (during unit creation)
- `learning_objective_generator` (for objective-standard alignment)

**Outputs To:**
- `lesson_plan_generator` (standards for each day)
- `standards_coverage_validator` (for verification)

---

**Agent Version:** 1.0 (Theater Pipeline)
**Last Updated:** 2026-01-08
