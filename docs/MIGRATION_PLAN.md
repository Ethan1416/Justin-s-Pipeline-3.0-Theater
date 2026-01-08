# NCLEX Pipeline Migration Plan

## Overview

This document outlines the incremental migration from the legacy step-based pipeline (v3.0) to the new multi-agent orchestration architecture (v4.0).

**Goal:** Transform 12 sequential steps into 50 specialized agents coordinated by 5 orchestrators.

---

## Current State (v3.0)

```
Legacy Files:
├── step1_anchor_upload.txt
├── step2_lecture_mapping.txt
├── step3_official_sorting.txt
├── step4_outline_generation.txt
├── step5_presentation_standards.txt
├── step6_blueprint_generation.txt
├── step6_5_enforce_line_limit.txt
├── step7_formatting_revision.txt
├── step8_quality_assurance.txt
├── step9_visual_aid_identification.txt
├── step10_visual_integration_revision.txt
├── step11_blueprint_organization.txt
├── step12_*.txt (7 visual type files)
└── step12_powerpoint_population.py
```

---

## Target State (v4.0)

```
New Architecture:
├── orchestrators/ (5 workflow coordinators)
├── agents/prompts/ (50 specialized agents)
├── agents/schemas/ (input/output contracts)
├── skills/ (Python utilities)
├── standards/ (teaching/visual standards)
└── config/ (YAML configuration)
```

---

## Migration Phases

### Phase 1: Foundation (COMPLETED)
- [x] Create directory structure
- [x] Create AGENTS.md master instructions
- [x] Create CLAUDE.md alias
- [x] Create config/pipeline.yaml
- [x] Create config/nclex.yaml
- [x] Create config/constraints.yaml
- [x] Create config/visuals.yaml (colors, fonts, layouts)
- [x] Create core schemas (blueprint, visual_spec, pipeline_state)
- [x] Migrate standards to new location
- [x] Create visual_formats/format_catalog.yaml
- [x] Copy Python files to skills/ directories
- [x] Rename output/ to outputs/

### Phase 1.5: Additional Legacy Files Migration
Files discovered during QA review that need migration:

**pipeline_part2_enhancement/ directory:**
| File | Target Location | Purpose |
|------|-----------------|---------|
| README.txt | docs/pipeline_part2_readme.md | Part 2 documentation |
| QUICK_START.txt | docs/quick_start.md | Quick start guide |
| presenter_notes_tone_guidelines.txt | standards/presenter_notes_guidelines.md | Tone standards |
| visual_specs.txt | standards/visual_specs.md | Visual specifications |
| PROFESSIONAL_GRAPHIC_ORGANIZER_STANDARDS.md | standards/graphic_organizer_standards.md | GO standards |
| analyze_and_identify_slides.py | skills/parsing/analyze_slides.py | Slide analysis |
| apply_graphic_organizers.py | skills/generation/apply_organizers.py | GO application |
| generate_graphic_organizer_examples.py | skills/generation/generate_examples.py | Example generation |

**docs/ directory:**
| File | Target Location | Purpose |
|------|-----------------|---------|
| automated_pipeline_instructions.txt | docs/automation_guide.md | Automation docs |
| sample_anchors.txt | inputs/sample_lecture/anchors.txt | Sample input |

**outputs/ directory (legacy scripts):**
| File | Target Location | Purpose |
|------|-----------------|---------|
| validate_comprehensive.py | skills/validation/comprehensive_validator.py | Full validation |
| generate_section1_v2.py | Archive or delete | Legacy script |
| generate_neuroanatomy_v4.py | Archive or delete | Legacy script |

**templates/ directory:**
| File | Action | Notes |
|------|--------|-------|
| content_master.pptx | Keep in place | Referenced by config |
| visual_organizer.pptx | Keep in place | Referenced by config |

### Phase 2: Orchestrator Creation
Convert high-level workflow logic into orchestrator files.

| Orchestrator | Source Files | Priority |
|--------------|--------------|----------|
| lecture_pipeline.md | PIPELINE_EXECUTION_ORDER.md | HIGH |
| preparation_pipeline.md | steps 1-5 | HIGH |
| blueprint_pipeline.md | steps 6-10 | HIGH |
| visual_generation.md | step12_*.txt (visuals) | MEDIUM |
| powerpoint_pipeline.md | step12_powerpoint_population.txt | MEDIUM |

**Action Items:**
- [ ] Create `orchestrators/lecture_pipeline.md` from PIPELINE_EXECUTION_ORDER.md
- [ ] Create `orchestrators/preparation_pipeline.md` from steps 1-5
- [ ] Create `orchestrators/blueprint_pipeline.md` from steps 6-10
- [ ] Create `orchestrators/visual_generation.md` from step12 visual files
- [ ] Create `orchestrators/powerpoint_pipeline.md` from step12_powerpoint_population.txt

### Phase 3: Agent Decomposition - Preparation (Steps 1-5)
Break preparation steps into focused agents.

| Legacy Step | New Agent(s) | Schema Files |
|-------------|--------------|--------------|
| step1_anchor_upload.txt | anchor_uploader.md | anchor_input.schema.json, anchor_output.schema.json |
| step2_lecture_mapping.txt | lecture_mapper.md | mapping_input.schema.json, mapping_output.schema.json |
| step3_official_sorting.txt | content_sorter.md | sorting_input.schema.json, sorting_output.schema.json |
| step4_outline_generation.txt | outline_generator.md | outline_input.schema.json, outline_output.schema.json |
| step5_presentation_standards.txt | standards_loader.md | standards_input.schema.json, standards_output.schema.json |

**Action Items:**
- [ ] Extract agent prompts from step1-5 files
- [ ] Create corresponding schema files
- [ ] Test each agent independently
- [ ] Verify schema contracts

### Phase 4: Agent Decomposition - Blueprint (Steps 6-10)
Break blueprint processing into focused agents.

| Legacy Step | New Agent(s) | Notes |
|-------------|--------------|-------|
| step6_blueprint_generation.txt | blueprint_generator.md | Core generation |
| step6_5_enforce_line_limit.txt | line_enforcer.md | Constraint enforcement |
| step7_formatting_revision.txt | formatting_reviser.md, constraint_validator.md | Split into two |
| step8_quality_assurance.txt | quality_reviewer.md, score_calculator.md, error_reporter.md | Split into three |
| step9_visual_aid_identification.txt | visual_identifier.md, visual_quota_checker.md | Split into two |
| step10_visual_integration_revision.txt | visual_integrator.md, changelog_writer.md | Split into two |
| step11_blueprint_organization.txt | blueprint_organizer.md | Organization logic |

**Action Items:**
- [ ] Decompose each step into single-responsibility agents
- [ ] Create schemas for each agent pair
- [ ] Map data flow between agents
- [ ] Test blueprint phase end-to-end

### Phase 5: Agent Decomposition - Visual Generation (Step 12)
Create specialized agents for each visual type.

| Legacy File | Generator Agent | Layout Selector Agent |
|-------------|-----------------|----------------------|
| step12_table_generation.txt | table_generator.md | table_layout_selector.md |
| step12_flowchart_generation.txt | flowchart_generator.md | flowchart_layout_selector.md |
| step12_decision_tree_generation.txt | decision_tree_generator.md | decision_tree_layout_selector.md |
| step12_timeline_generation.txt | timeline_generator.md | timeline_layout_selector.md |
| step12_hierarchy_diagram_generation.txt | hierarchy_generator.md | hierarchy_layout_selector.md |
| step12_spectrum_generation.txt | spectrum_generator.md | spectrum_layout_selector.md |
| step12_key_differentiators_generation.txt | key_diff_generator.md | key_diff_layout_selector.md |

**Action Items:**
- [ ] Create generator agent for each visual type
- [ ] Create layout selector agent for each visual type
- [ ] Create type-specific schemas
- [ ] Test each visual type independently
- [ ] Test parallel visual generation

### Phase 6: Agent Decomposition - PowerPoint Generation
Create specialized agents for final output.

| Function | Agent |
|----------|-------|
| Template population | pptx_populator.md |
| Slide assembly | slide_assembler.md |
| Shape rendering | shape_renderer.md |
| Text formatting | text_formatter.md |
| Color application | color_applier.md |
| Position calculation | position_calculator.md |
| Connector drawing | connector_drawer.md |
| Final validation | final_validator.md |

**Action Items:**
- [ ] Extract functions from step12_powerpoint_population.py
- [ ] Create agent prompt for each function
- [ ] Create corresponding schemas
- [ ] Test PowerPoint generation end-to-end

### Phase 7: Skills Migration
Convert Python utilities to skill modules.

| Current File | New Location | Purpose |
|--------------|--------------|---------|
| pipeline_validator.py | skills/validation/pipeline_validator.py | Full validation |
| blueprint_line_validator.py | skills/validation/check_line_limits.py | Line limits |
| pipeline_state_manager.py | skills/utilities/state_manager.py | State persistence |
| step12_powerpoint_population.py | skills/generation/*.py | Split into modules |

**Skill Modules to Create:**
```
skills/
├── parsing/
│   ├── extract_structure.py
│   ├── extract_styles.py
│   └── extract_placeholders.py
├── generation/
│   ├── build_shapes.py
│   ├── render_tables.py
│   ├── render_flowcharts.py
│   ├── render_decision_trees.py
│   ├── render_timelines.py
│   ├── render_hierarchies.py
│   ├── render_spectrums.py
│   ├── render_key_diffs.py
│   └── inject_content.py
├── validation/
│   ├── check_line_limits.py
│   ├── check_char_limits.py
│   ├── check_visual_quota.py
│   ├── check_brand.py
│   └── check_pedagogy.py
└── utilities/
    ├── glossary_lookup.py
    ├── timing_estimator.py
    └── state_manager.py
```

### Phase 8: Quality Assurance Agents
Create dedicated QA agents.

| Agent | Purpose |
|-------|---------|
| line_limit_checker.md | Verify line limits |
| char_limit_checker.md | Verify character limits |
| visual_quota_checker.md | Verify visual minimums |
| brand_compliance_checker.md | Check brand standards |
| pedagogy_checker.md | Check learning objectives |
| consistency_checker.md | Check terminology |
| score_calculator.md | Calculate QA scores |
| error_reporter.md | Generate error reports |

### Phase 9: Testing & Validation
- [ ] Create test fixtures in tests/sample_inputs/
- [ ] Create integration tests in tests/integration/
- [ ] Run full pipeline with sample NCLEX content
- [ ] Validate all schemas
- [ ] Performance testing (parallel vs sequential)

### Phase 10: Documentation & Cleanup
- [ ] Update AGENTS.md with final agent list
- [ ] Document each orchestrator
- [ ] Create agent reference guide
- [ ] Archive legacy step files
- [ ] Update version to 4.0

---

## File Mapping Reference

### Legacy → New Mapping

| Legacy File | New File(s) |
|-------------|-------------|
| CLAUDE_INSTRUCTIONS.md | AGENTS.md, CLAUDE.md |
| PIPELINE_EXECUTION_ORDER.md | orchestrators/lecture_pipeline.md |
| PIPELINE_DOCUMENTATION_INDEX.md | docs/README.md |
| pipeline_config.json | config/pipeline.yaml, config/nclex.yaml, config/constraints.yaml |
| VISUAL_LAYOUT_STANDARDS.md | standards/VISUAL_LAYOUT_STANDARDS.md |
| SHAPE_ROTATION_GUIDELINES.md | standards/SHAPE_ROTATION_GUIDELINES.md |
| MASTER_REQUIREMENTS_CHECKLIST.md | standards/teaching_standards.md |
| CHECKLIST_ADDING_NEW_VISUAL_TYPES.md | docs/adding_visual_types.md |

### New Files Created

| File | Purpose |
|------|---------|
| config/pipeline.yaml | Pipeline settings, timeouts, execution order |
| config/nclex.yaml | NCLEX-specific brand config |
| config/constraints.yaml | Character/line limits, visual quotas |
| agents/schemas/blueprint.schema.json | Blueprint data contract |
| agents/schemas/visual_spec.schema.json | Visual specification contract |
| agents/schemas/pipeline_state.schema.json | Pipeline state contract |
| standards/visual_formats/format_catalog.yaml | Visual type definitions |

---

## Incremental Migration Strategy

### Recommended Order

1. **Week 1-2:** Complete Phases 1-2 (Foundation + Orchestrators)
2. **Week 3-4:** Complete Phase 3 (Preparation agents)
3. **Week 5-6:** Complete Phase 4 (Blueprint agents)
4. **Week 7-8:** Complete Phase 5 (Visual generation agents)
5. **Week 9-10:** Complete Phases 6-7 (PowerPoint + Skills)
6. **Week 11-12:** Complete Phases 8-10 (QA + Testing + Docs)

### Parallel Development Approach

Run both systems simultaneously during migration:
1. Keep legacy steps functional
2. Build new agents one phase at a time
3. Compare outputs between systems
4. Switch to new system when validated

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Keep legacy files until validated |
| Schema incompatibility | Test schemas with sample data first |
| Performance regression | Benchmark before/after each phase |
| Missing edge cases | Create comprehensive test fixtures |

---

## Success Criteria

- [ ] All 50 agents created and documented
- [ ] All 5 orchestrators functional
- [ ] All schemas validated
- [ ] End-to-end test passes
- [ ] Output matches or exceeds legacy quality
- [ ] Performance within acceptable range

---

## Next Steps

1. **Immediate:** Begin Phase 2 - Create orchestrator files
2. **This session:** Extract first agent from step1
3. **Ongoing:** Iterate through phases incrementally

---

**Last Updated:** 2026-01-03
