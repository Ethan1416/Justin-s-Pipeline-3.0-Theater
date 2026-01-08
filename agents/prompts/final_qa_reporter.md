# Final QA Reporter

## Purpose
Generate comprehensive quality assurance reports for generated theater curriculum. Aggregates validation results, identifies patterns, provides actionable recommendations, and certifies lessons as production-ready.

## HARDCODED SKILLS
```yaml
skills:
  - word_count_analyzer
  - duration_estimator
```

## Pipeline Position
**Phase 4: Assembly** - Final step in pipeline

---

## Input Schema
```json
{
  "unit": {
    "number": 1,
    "name": "Greek Theater",
    "total_days": 20
  },
  "lesson_results": [
    {
      "day": 1,
      "package_id": "U1D01_Greek_Intro",
      "validation_results": {
        "truncation": {"passed": true, "score": 100, "issues": []},
        "structure": {"passed": true, "score": 100, "issues": []},
        "elaboration": {"passed": true, "score": 88, "issues": []},
        "timing": {"passed": true, "score": 95, "issues": []},
        "standards": {"passed": true, "score": 85, "issues": []},
        "coherence": {"passed": true, "score": 90, "issues": []},
        "pedagogy": {"passed": true, "score": 82, "issues": []},
        "accuracy": {"passed": true, "score": 98, "issues": []}
      },
      "metrics": {
        "presenter_notes_words": 2050,
        "slide_count": 16,
        "pause_markers": 24,
        "emphasis_markers": 10
      }
    }
    // ... days 2-20
  ],
  "organization_result": {
    "files_organized": 85,
    "completeness": "100%"
  }
}
```

## Output Schema
```json
{
  "qa_report": {
    "metadata": {
      "unit": "Unit 1: Greek Theater",
      "days_evaluated": 20,
      "report_generated": "2026-01-08T14:30:00Z",
      "pipeline_version": "1.0"
    },
    "certification": {
      "status": "CERTIFIED",
      "ready_for_production": true,
      "certification_level": "A",
      "signature": "QA-U1-2026-01-08-A94"
    },
    "summary": {
      "overall_quality_score": 94.2,
      "validation_pass_rate": "100%",
      "days_certified": 20,
      "days_with_warnings": 3,
      "critical_issues": 0
    },
    "detailed_scores": {...},
    "trends_and_patterns": {...},
    "recommendations": [...],
    "production_checklist": {...}
  }
}
```

---

## Report Sections

### Section 1: Executive Summary

```
╔══════════════════════════════════════════════════════════════════╗
║                    QA CERTIFICATION REPORT                        ║
║                    Unit 1: Greek Theater                          ║
╠══════════════════════════════════════════════════════════════════╣
║  CERTIFICATION STATUS: ✅ CERTIFIED - GRADE A                    ║
║  Overall Quality Score: 94.2/100                                 ║
║  Days Evaluated: 20/20 (100%)                                    ║
║  Validation Pass Rate: 100%                                      ║
╠══════════════════════════════════════════════════════════════════╣
║  Certification ID: QA-U1-2026-01-08-A94                         ║
║  Generated: January 8, 2026 at 2:30 PM                          ║
║  Pipeline Version: 1.0                                           ║
╚══════════════════════════════════════════════════════════════════╝
```

### Section 2: Validation Gate Results

| Gate | Pass Rate | Avg Score | Min Score | Issues |
|------|-----------|-----------|-----------|--------|
| Truncation | 100% | 100 | 100 | 0 |
| Structure | 100% | 100 | 100 | 0 |
| Elaboration | 100% | 87.5 | 82 | 3 |
| Timing | 100% | 94.2 | 89 | 2 |
| Standards | 100% | 86.4 | 80 | 5 |
| Coherence | 100% | 89.1 | 84 | 4 |
| Pedagogy | 100% | 81.3 | 76 | 6 |
| Accuracy | 100% | 97.8 | 95 | 1 |

### Section 3: Per-Day Breakdown

| Day | Topic | Overall | Trunc | Struct | Elab | Time | Stds | Coher | Peda | Accur |
|-----|-------|---------|-------|--------|------|------|------|-------|------|-------|
| 1 | Introduction | 92 | 100 | 100 | 88 | 95 | 85 | 90 | 82 | 98 |
| 2 | Dithyramb | 94 | 100 | 100 | 90 | 93 | 88 | 92 | 84 | 97 |
| 3 | Tragedy | 95 | 100 | 100 | 92 | 96 | 90 | 88 | 80 | 99 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Section 4: Trends and Patterns

```
POSITIVE TRENDS:
✅ Consistent truncation prevention (100% across all days)
✅ Strong content accuracy (avg 97.8%)
✅ Reliable timing estimates (avg 94.2%)

AREAS FOR ATTENTION:
⚠️ Pedagogy scores lowest category (avg 81.3%)
   - Days 3, 7, 12 below 80% threshold
   - Recommend: Add more differentiation strategies

⚠️ Standards coverage variable (range: 80-92)
   - Days 5, 10, 15 at minimum threshold
   - Recommend: Strengthen standards-objective alignment

CONSISTENCY ANALYSIS:
📊 Score variance: Low (std dev: 4.2)
📊 Day-to-day improvement: Stable
📊 No regression patterns detected
```

### Section 5: Recommendations

```
PRIORITY 1 (Implement Before Use):
None - All critical requirements met

PRIORITY 2 (Implement Soon):
1. Days 3, 7, 12: Add explicit differentiation for struggling learners
2. Days 5, 10, 15: Strengthen exit ticket alignment to objectives
3. Day 8: Increase [CHECK FOR UNDERSTANDING] markers from 2 to 3

PRIORITY 3 (Consider for Future):
1. Add more advanced learner extensions across unit
2. Increase visual variety in content slides
3. Strengthen warmup-content connections in days 6, 11
```

### Section 6: Production Checklist

```
PRE-DELIVERY CHECKLIST:
✅ All 20 lesson plans generated
✅ All 20 PowerPoints assembled
✅ All handouts print-ready
✅ All exit tickets compiled
✅ Unit folder organized
✅ Index files generated
✅ Materials lists complete

QUALITY GATES:
✅ Truncation validation: PASSED (20/20)
✅ Structure validation: PASSED (20/20)
✅ Elaboration validation: PASSED (20/20)
✅ Timing validation: PASSED (20/20)

CERTIFICATION:
✅ Overall score ≥ 90: YES (94.2)
✅ No critical issues: YES
✅ All days certified: YES

READY FOR PRODUCTION: ✅ YES
```

---

## Certification Levels

| Grade | Score Range | Status | Meaning |
|-------|-------------|--------|---------|
| A+ | 98-100 | CERTIFIED | Exceptional quality |
| A | 95-97 | CERTIFIED | Excellent quality |
| A- | 90-94 | CERTIFIED | Very good quality |
| B+ | 85-89 | CERTIFIED | Good quality |
| B | 80-84 | CERTIFIED WITH WARNINGS | Acceptable quality |
| C | 70-79 | CONDITIONAL | Requires review |
| F | <70 | NOT CERTIFIED | Requires regeneration |

### Certification Requirements
To be CERTIFIED, unit must have:
- Overall score ≥ 80
- All HARDCODED gates passed (truncation, structure)
- No critical issues
- ≥90% of days individually passing

---

## Issue Categorization

### Critical Issues (Block Certification)
| Issue | Impact |
|-------|--------|
| Truncated sentences | Incomplete content delivered |
| Missing required component | Lesson cannot be taught |
| Timing >18 min or <12 min | Class period mismatch |
| Content accuracy error | Factual misinformation |

### Major Issues (Warnings)
| Issue | Impact |
|-------|--------|
| Elaboration score <85 | Shallow content |
| Pedagogy score <75 | Missing best practices |
| Standards coverage <80 | Weak standards alignment |
| Missing differentiation | Excludes learners |

### Minor Issues (Recommendations)
| Issue | Impact |
|-------|--------|
| Low marker count | Reduced engagement cues |
| Weak warmup connection | Missed engagement opportunity |
| Variable pacing | Inconsistent experience |

---

## Report Formats

### Full Report (PDF)
- All sections
- Detailed per-day breakdown
- Charts and visualizations
- 15-20 pages

### Summary Report (1-page)
- Executive summary
- Certification status
- Key metrics
- Top 3 recommendations

### Data Export (JSON)
- Machine-readable format
- All scores and metrics
- For integration with other systems

### Dashboard View (HTML)
- Interactive charts
- Drill-down capability
- Color-coded status indicators

---

## Metrics Calculations

### Overall Quality Score
```
Overall = (
  Truncation × 0.15 +
  Structure × 0.15 +
  Elaboration × 0.15 +
  Timing × 0.10 +
  Standards × 0.15 +
  Coherence × 0.10 +
  Pedagogy × 0.10 +
  Accuracy × 0.10
)
```

### Unit Consistency Score
```
Consistency = 100 - (Standard Deviation of Day Scores)
```

### Production Readiness Score
```
Readiness = (
  (Days Certified / Total Days) × 50 +
  (Gates Passed / Total Gates) × 30 +
  (No Critical Issues ? 20 : 0)
)
```

---

## Trend Analysis

### Cross-Day Patterns
```python
# Identify improvement/regression
for i in range(1, len(days)):
    diff = days[i].score - days[i-1].score
    if diff < -5:
        flag_regression(days[i])
    elif diff > 5:
        flag_improvement(days[i])
```

### Category Patterns
```python
# Identify consistently weak categories
for category in categories:
    avg = mean(day.scores[category] for day in days)
    if avg < threshold[category]:
        recommend_improvement(category)
```

### Outlier Detection
```python
# Identify anomalous days
mean_score = mean(day.overall for day in days)
std_dev = std(day.overall for day in days)
for day in days:
    if abs(day.overall - mean_score) > 2 * std_dev:
        flag_outlier(day)
```

---

## Integration with Pipeline

### Input From
- All validators (validation results)
- `lesson_assembler` (package data)
- `powerpoint_assembler` (metrics)
- `unit_folder_organizer` (organization result)

### Output To
- File system (report files)
- Pipeline orchestrator (certification status)
- Teacher/admin review (if conditional)

---

## Validation Checklist

- [ ] All day results collected
- [ ] All validation scores aggregated
- [ ] Overall score calculated
- [ ] Certification level determined
- [ ] Trends analyzed
- [ ] Recommendations generated
- [ ] Production checklist completed
- [ ] Report files generated (PDF, JSON, HTML)
- [ ] Certification signature created
- [ ] Report validated for completeness
