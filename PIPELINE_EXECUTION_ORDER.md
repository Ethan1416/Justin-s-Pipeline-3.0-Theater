# NCLEX Lecture Generation Pipeline - Execution Order

## CRITICAL: Steps Must Be Run IN ORDER

**DO NOT SKIP STEPS. Each step depends on the previous step's output.**

---

## Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PREPARATION PHASE                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 1: Load revised_standards.docx                                        │
│  Step 2: Anchor Mapping → mapping/step2_output_[domain]_[date].txt          │
│  Step 3: Sorting → sorting/step3_output_[domain]_[date].txt                 │
│  Step 4: Outline → outlines/step4_output_[domain]_[date].txt                │
│  Step 5: Load presentation standards (reference only)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      BLUEPRINT PHASE (Per Section)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 6: Blueprint Generation                                                │
│          → blueprints/step6_blueprint_[domain]_[section]_[date].txt         │
│                                                                              │
│  ⚠️  DO NOT PROCEED TO STEP 12 FROM HERE                                    │
│  ⚠️  STEPS 7-10 ARE MANDATORY                                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REVISION PHASE (Per Section)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 7: Formatting Revision                                                 │
│          - Enforces 8-line body maximum                                      │
│          - Enforces 66 chars/line                                            │
│          - Enforces 32 chars/line for headers                                │
│          → revisions/step7_revised_[domain]_[section]_[date].txt            │
│          → revisions/step7_changelog_[domain]_[section]_[date].txt          │
│                                                                              │
│  Step 8: Quality Assurance                                                   │
│          - Validates ALL constraints                                         │
│          - Must score ≥90/100 to proceed                                     │
│          - If FAIL: Return to Step 7                                         │
│          → qa_reports/step8_qa_report_[domain]_[section]_[date].txt         │
│          → qa_reports/step8_validation_score_[domain]_[section]_[date].txt  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      VISUAL PHASE (Per Section)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 9: Visual Aid Identification                                           │
│          - MANDATORY MINIMUM: 2-4 visuals per section                        │
│          - 7 visual types available                                          │
│          - Must show QUOTA STATUS: PASS                                      │
│          → visual_specs/step9_visual_specs_[domain]_[section]_[date].txt    │
│                                                                              │
│  Step 10: Visual Integration Revision                                        │
│          - Merges visuals into blueprint                                     │
│          - Adds Visual: Yes/No markers to EVERY slide                        │
│          → integrated/step10_integrated_[domain]_[section]_[date].txt       │
│          → integrated/step10_revision_changelog_[domain]_[section]_[date].txt│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      GENERATION PHASE                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Step 11: (Reserved for future use)                                          │
│                                                                              │
│  Step 12: PowerPoint Generation                                              │
│                                                                              │
│  ⛔ PRE-FLIGHT CHECK REQUIRED (see below)                                    │
│                                                                              │
│          - Reads from Step 10 integrated blueprints ONLY                     │
│          - Generates graphic organizers for Visual: Yes slides               │
│          → powerpoints/Section_[##]_[Name].pptx                             │
└─────────────────────────────────────────────────────────────────────────────┘

```

---

## Step 12 Pre-Flight Checklist

**⛔ DO NOT RUN STEP 12 UNTIL ALL BOXES ARE CHECKED:**

### Folder Structure Verification
- [ ] `integrated/` folder EXISTS and contains files
- [ ] `integrated/` folder has `step10_integrated_blueprint_*.txt` for EACH section
- [ ] `revisions/` folder has `step7_revised_*.txt` for each section
- [ ] `qa_reports/` folder has `step8_qa_report_*.txt` for each section
- [ ] `visual_specs/` folder has `step9_visual_specs_*.txt` for each section

### Content Verification
- [ ] Each Step 8 QA report shows score ≥90/100
- [ ] Each Step 9 visual spec shows QUOTA STATUS: PASS
- [ ] Each Step 10 integrated blueprint has `Visual: Yes` or `Visual: No` on EVERY slide

### Input File Verification
- [ ] PowerPoint generation script reads from `integrated/step10_*.txt` (NOT `blueprints/step6_*.txt`)

---

## Common Mistakes to Avoid

### ❌ WRONG: Skipping Steps 7-10
```
Step 6 Blueprint → Step 12 PowerPoint
```
**Result:** No graphic organizers, text constraints violated

### ✅ CORRECT: Full Pipeline
```
Step 6 → Step 7 → Step 8 → Step 9 → Step 10 → Step 12
```
**Result:** Graphic organizers included, all constraints enforced

---

## Quick Reference: What Each Step Produces

| Step | Output Folder | File Pattern | Key Purpose |
|------|---------------|--------------|-------------|
| 2 | mapping/ | step2_output_*.txt | Anchor extraction |
| 3 | sorting/ | step3_output_*.txt | Priority sorting |
| 4 | outlines/ | step4_output_*.txt | Section structure |
| 6 | blueprints/ | step6_blueprint_*.txt | Initial slide content |
| 7 | revisions/ | step7_revised_*.txt | **Text constraints enforced** |
| 8 | qa_reports/ | step8_qa_report_*.txt | Validation (must pass) |
| 9 | visual_specs/ | step9_visual_specs_*.txt | **Graphic organizers identified** |
| 10 | integrated/ | step10_integrated_*.txt | **Final blueprint with visuals** |
| 12 | powerpoints/ | Section_*.pptx | Final PowerPoints |

---

## Section Processing Checklist Template

For each section, verify completion:

```
Section: ________________________

[ ] Step 6: Blueprint created
[ ] Step 7: Formatting revision complete
[ ] Step 8: QA passed (score: ___/100)
[ ] Step 9: Visual specs created (visuals identified: ___)
    [ ] QUOTA STATUS: PASS
[ ] Step 10: Integrated blueprint created
    [ ] All slides have Visual: Yes/No marker
[ ] Step 12: PowerPoint generated
    [ ] Contains graphic organizers
    [ ] No slide body exceeds 8 lines
```

---

## If You're Starting Fresh

1. Create production folder: `[Domain]_Production_[Date]/`
2. Create ALL subfolders upfront:
   ```
   mkdir mapping
   mkdir sorting
   mkdir outlines
   mkdir blueprints
   mkdir revisions
   mkdir qa_reports
   mkdir visual_specs
   mkdir integrated
   mkdir powerpoints
   mkdir logs
   ```
3. Process Steps 2-4 (once for entire domain)
4. Process Steps 6-10 for EACH section
5. Run Step 12 Pre-Flight Checklist
6. Generate PowerPoints

---

## Reference Documents

All step documentation located in:
``

| Step | Reference Document |
|------|-------------------|
| 6 | step6_blueprint_generation.txt |
| 7 | step7_formatting_revision.txt |
| 8 | step8_quality_assurance.txt |
| 9 | step9_visual_aid_identification.txt |
| 10 | step10_visual_integration_revision.txt |
| 12 | step12_powerpoint_population.txt |
| Config | pipeline_config.json |
