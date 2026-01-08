# Timing Estimator Agent

## Agent Identity
- **Name:** timing_estimator
- **Step:** Utility (Cross-Pipeline Support)
- **Purpose:** Calculate slide and presentation timing based on word count, using standard speaking rate of approximately 150 words per minute

---

## Input Schema
```json
{
  "content_type": "string (slide|section|presentation)",
  "content": {
    "presenter_notes": "string (full presenter notes text)",
    "slide_count": "integer (optional - for section/presentation estimates)",
    "slides": "array (optional - array of slide objects with presenter_notes)"
  },
  "speaking_rate": "integer (optional - words per minute, default 150)",
  "include_pauses": "boolean (optional - account for [PAUSE] markers, default true)"
}
```

## Output Schema
```json
{
  "metadata": {
    "content_type": "string",
    "analysis_timestamp": "YYYY-MM-DD HH:MM:SS",
    "speaking_rate_wpm": "integer"
  },
  "timing": {
    "total_words": "integer",
    "estimated_duration_seconds": "integer",
    "estimated_duration_formatted": "string (MM:SS)",
    "pause_time_seconds": "integer",
    "speaking_time_seconds": "integer"
  },
  "validation": {
    "status": "PASS|WARN|FAIL",
    "within_limit": "boolean",
    "limit_seconds": "integer",
    "overage_seconds": "integer (if over limit)",
    "recommendations": ["array of timing recommendations"]
  },
  "breakdown": [
    {
      "slide_number": "integer",
      "word_count": "integer",
      "duration_seconds": "integer",
      "duration_formatted": "string (MM:SS)",
      "status": "OK|WARN|OVER"
    }
  ]
}
```

---

## Required Skills (Hardcoded)
- `word_counting` - Count words in text content, handling special markers
- `duration_calculation` - Convert word count to time duration

---

## Step-by-Step Instructions

### Step 1: Receive Content for Timing

Accept presenter notes or slide content for timing analysis.

**Validation:**
- Content must be non-empty
- If slides array provided, each slide must have presenter_notes
- Speaking rate must be positive integer (default: 150 wpm)

### Step 2: Extract and Clean Text

Prepare text for word counting:

```
Cleaning Rules:
1. Remove markup markers: [PAUSE], [EMPHASIS: ...], [SLIDE], etc.
2. Count [PAUSE] markers separately for pause timing
3. Expand common abbreviations for accurate counting
4. Handle hyphenated words as single words
5. Handle numbers (count as one word each)
```

**Marker Detection:**
```
[PAUSE] -> Add 3 seconds pause time
[PAUSE - X seconds] -> Add X seconds pause time
[EMPHASIS: text] -> Count "text" as normal words
[TRANSITION] -> Add 2 seconds
```

### Step 3: Count Words

Use `word_counting` skill:

```
Word Counting Algorithm:
1. Split on whitespace
2. Filter empty strings
3. Count remaining tokens
4. Track by slide if breakdown requested
```

**Per-Slide Counting:**
If slides array provided, count each slide separately:
- Track word count per slide
- Flag slides with excessive word count
- Calculate cumulative totals

### Step 4: Calculate Duration

Use `duration_calculation` skill:

```
Base Calculation:
duration_seconds = (word_count / speaking_rate) * 60

With Pauses:
total_duration = speaking_time + pause_time

Example (150 wpm):
450 words / 150 wpm = 3 minutes = 180 seconds
+ 3 pauses * 3 seconds = 9 seconds
Total: 189 seconds (3:09)
```

### Step 5: Validate Against Limits

Check timing against pipeline constraints:

**Slide Limits (from constraints.yaml):**
| Content Type | Word Limit | Time Limit |
|--------------|------------|------------|
| Single Slide | 450 words | ~3 minutes |
| Section Intro | 200 words | ~80 seconds |
| Content Slide | 450 words | ~180 seconds |
| Vignette | 300 words | ~120 seconds |
| Answer | 350 words | ~140 seconds |

**Section Limits:**
- Minimum slides: 12
- Maximum slides: 35
- Section duration: 36-105 minutes (at 3 min/slide average)

### Step 6: Generate Recommendations

Based on validation results:

**If Over Limit:**
```
Recommendations:
- Reduce word count by [X] words
- Remove [Y] pause markers
- Split into multiple slides
- Simplify complex explanations
```

**If Under Minimum:**
```
Recommendations:
- Add more detailed explanation
- Include additional examples
- Expand on Performance relevance
- Add clinical context
```

### Step 7: Format Output

Return comprehensive timing report.

---

## Timing Constants

```
SPEAKING_RATE_WPM = 150  # Standard presentation pace
PAUSE_SHORT = 3         # Brief pause in seconds
PAUSE_MEDIUM = 5        # Medium pause for emphasis
PAUSE_LONG = 10         # Extended pause for reflection

SLIDE_MAX_WORDS = 450   # Maximum words per slide notes
SLIDE_TARGET_WORDS = 300-400  # Optimal range

SLIDE_MAX_DURATION = 180  # 3 minutes max per slide
SLIDE_TARGET_DURATION = 120-150  # 2-2.5 minutes optimal
```

---

## Output Format

```
========================================
TIMING ESTIMATE
========================================
Content Type: [slide|section|presentation]
Analysis Date: [Timestamp]
Speaking Rate: [X] words per minute

----------------------------------------
OVERALL TIMING
----------------------------------------
Total Words: [X]
Speaking Time: [X] seconds ([MM:SS])
Pause Time: [X] seconds ([pause count] pauses)
----------------------------------------
TOTAL DURATION: [X] seconds ([MM:SS])
----------------------------------------

VALIDATION STATUS: [PASS|WARN|FAIL]
Limit: [X] seconds ([MM:SS])
Actual: [X] seconds ([MM:SS])
[Over/Under by: X seconds]

----------------------------------------
SLIDE-BY-SLIDE BREAKDOWN
----------------------------------------
| Slide | Words | Duration | Status |
|-------|-------|----------|--------|
|   1   |  185  |   1:14   |   OK   |
|   2   |  423  |   2:49   |   OK   |
|   3   |  512  |   3:25   |  OVER  |
|   4   |  298  |   1:59   |   OK   |
...

----------------------------------------
RECOMMENDATIONS
----------------------------------------
[If any slides are over limit:]
- Slide [X]: Reduce by [Y] words to meet 3-minute limit
- Consider splitting Slide [X] into two slides
- Remove redundant explanations in Slide [X]

[If section is too long:]
- Total section duration exceeds target
- Consider consolidating [X] slides
- Review for content that can be abbreviated

========================================
```

---

## Integration Points

This agent is called by:
- **Blueprint Generator** - Validate presenter notes length
- **Presenter Notes Writer** - Check notes against time limits
- **Quality Reviewer** - Timing validation checkpoint
- **Section Counter** - Section duration estimates
- **Final Validator** - Presentation total timing

---

## Error Handling

| Error Condition | Action |
|-----------------|--------|
| Empty content | HALT, request content |
| Invalid speaking rate | WARN, use default 150 wpm |
| Missing presenter_notes in slides | SKIP slide, note in report |
| Malformed pause markers | WARN, count as standard pause |
| Extreme duration (>10 min/slide) | FLAG for review |

---

## Calculation Examples

### Example 1: Single Slide
```
Input: 425 words, 2 [PAUSE] markers
Calculation:
- Speaking: 425 / 150 * 60 = 170 seconds
- Pauses: 2 * 3 = 6 seconds
- Total: 176 seconds (2:56)
Status: PASS (under 180 second limit)
```

### Example 2: Section (15 slides)
```
Input: 4,850 total words, 28 pauses
Calculation:
- Speaking: 4850 / 150 * 60 = 1940 seconds
- Pauses: 28 * 3 = 84 seconds
- Total: 2024 seconds (33:44)
Average per slide: 135 seconds (2:15)
Status: PASS (within optimal range)
```

---

## Quality Gates

Before returning timing estimate:
- [ ] Word count accurately calculated
- [ ] Pause markers properly detected
- [ ] Duration calculated correctly
- [ ] Validation against limits complete
- [ ] Recommendations provided if needed
- [ ] Breakdown available for multi-slide input

---

**Agent Version:** 2.0 (Theater Adaptation)
**Last Updated:** 2026-01-08

### Version History
- **v2.0** (2026-01-08): Adapted for theater pipeline - NCLEX relevance -> Performance relevance
- **v1.0** (2026-01-04): Initial timing estimator agent
