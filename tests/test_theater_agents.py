"""
Theater Education Pipeline - Comprehensive Agent Tests
======================================================

Tests for all 26 agents in the Theater Education Pipeline.
"""

import sys
sys.path.insert(0, '/home/mcdanielmjustin/Justin-s-Pipeline-3.0-Theater')

from agents import (
    create_agent,
    AgentStatus,
    # Phase 1
    UnitPlannerAgent, StandardsMapperAgent, UnitScopeValidatorAgent, LearningObjectiveGeneratorAgent,
    # Phase 2
    LessonPlanGeneratorAgent, WarmupGeneratorAgent, PowerPointGeneratorAgent, ActivityGeneratorAgent,
    HandoutGeneratorAgent, JournalExitGeneratorAgent, PresenterNotesWriterAgent,
    AuxiliarySlideGeneratorAgent, DifferentiationAnnotatorAgent, MaterialsListGeneratorAgent,
    # Phase 3
    TruncationValidatorAgent, ElaborationValidatorAgent, TimingValidatorAgent, StructureValidatorAgent,
    StandardsCoverageValidatorAgent, CoherenceValidatorAgent, PedagogyValidatorAgent, ContentAccuracyValidatorAgent,
    # Phase 4
    LessonAssemblerAgent, PowerPointAssemblerAgent, UnitFolderOrganizerAgent, FinalQAReporterAgent,
)


def get_test_context():
    """Get test context for agents."""
    return {
        'unit': {'number': 1, 'name': 'Greek Theater'},
        'day': 1,
        'topic': 'Introduction to Greek Theater: Origins and the Festival of Dionysus',
        'daily_input': {
            'topic': 'Introduction to Greek Theater: Origins and the Festival of Dionysus',
            'learning_objectives': [
                'Identify the origins of Greek theater',
                'Describe the role of Dionysus',
                'Explain theater structure'
            ],
            'vocabulary': [
                {'term': 'Dionysus', 'definition': 'Greek god of wine and theater'},
                {'term': 'Dithyramb', 'definition': 'Choral hymn'},
                {'term': 'Orchestra', 'definition': 'Dancing area'}
            ],
            'content_points': [f'Content point {i}' for i in range(1, 13)],
            'standards': ['RL.9-10.3', 'SL.9-10.1'],
            'warmup': {'name': 'Chorus Walk', 'type': 'physical'},
            'activity': {'name': 'Analysis', 'type': 'analysis'},
            'journal_prompt': 'Reflect on Greek theater',
            'exit_tickets': ['What did you learn?', 'How does it connect?'],
            'materials_list': ['Presentation', 'Handouts']
        },
        'previous_outputs': {},
        'content': 'This is test content. Complete sentences here.'
    }


def run_tests():
    """Run all agent tests."""
    context = get_test_context()
    passed = 0
    failed = 0
    results = []

    # =========================================================================
    # PHASE 1: Unit Planning
    # =========================================================================
    print("\n" + "=" * 60)
    print("PHASE 1: Unit Planning Tests")
    print("=" * 60)

    phase1_agents = [
        ('unit_planner', UnitPlannerAgent),
        ('standards_mapper', StandardsMapperAgent),
        ('learning_objective_generator', LearningObjectiveGeneratorAgent),
        ('unit_scope_validator', UnitScopeValidatorAgent),
    ]

    for name, expected_class in phase1_agents:
        try:
            agent = create_agent(name)
            assert isinstance(agent, expected_class), f"Wrong class type"
            result = agent.execute(context)
            assert result.status == AgentStatus.COMPLETED, f"Status: {result.status}"
            assert result.output is not None, "No output"
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {str(e)[:50]}")
            failed += 1

    # =========================================================================
    # PHASE 2: Daily Generation
    # =========================================================================
    print("\n" + "=" * 60)
    print("PHASE 2: Daily Generation Tests")
    print("=" * 60)

    phase2_agents = [
        ('lesson_plan_generator', LessonPlanGeneratorAgent, 'lesson_plan'),
        ('warmup_generator', WarmupGeneratorAgent, 'warmup'),
        ('powerpoint_generator', PowerPointGeneratorAgent, 'powerpoint_blueprint'),
        ('presenter_notes_writer', PresenterNotesWriterAgent, 'presenter_notes'),
        ('activity_generator', ActivityGeneratorAgent, 'activity'),
        ('journal_exit_generator', JournalExitGeneratorAgent, 'journal'),
        ('handout_generator', HandoutGeneratorAgent, 'handouts'),
        ('auxiliary_slide_generator', AuxiliarySlideGeneratorAgent, 'auxiliary_slides'),
        ('differentiation_annotator', DifferentiationAnnotatorAgent, 'differentiation_annotations'),
        ('materials_list_generator', MaterialsListGeneratorAgent, 'materials_list'),
    ]

    for name, expected_class, expected_key in phase2_agents:
        try:
            agent = create_agent(name)
            assert isinstance(agent, expected_class), f"Wrong class type"
            result = agent.execute(context)
            assert result.status == AgentStatus.COMPLETED, f"Status: {result.status}"
            assert result.output is not None, "No output"
            assert expected_key in result.output, f"Missing key: {expected_key}"
            # Store for dependent agents
            context['previous_outputs'][name] = result.output
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {str(e)[:50]}")
            failed += 1

    # =========================================================================
    # PHASE 3: Validation
    # =========================================================================
    print("\n" + "=" * 60)
    print("PHASE 3: Validation Tests")
    print("=" * 60)

    # Add presenter notes for validation
    context['presenter_notes_writer_output'] = context['previous_outputs'].get('presenter_notes_writer', {
        'presenter_notes': 'Test notes',
        'word_count': 2000,
        'estimated_duration_minutes': 15
    })

    phase3_validators = [
        ('truncation_validator', TruncationValidatorAgent),
        ('structure_validator', StructureValidatorAgent),
        ('elaboration_validator', ElaborationValidatorAgent),
        ('timing_validator', TimingValidatorAgent),
        ('standards_coverage_validator', StandardsCoverageValidatorAgent),
        ('coherence_validator', CoherenceValidatorAgent),
        ('pedagogy_validator', PedagogyValidatorAgent),
        ('content_accuracy_validator', ContentAccuracyValidatorAgent),
    ]

    for name, expected_class in phase3_validators:
        try:
            agent = create_agent(name)
            assert isinstance(agent, expected_class), f"Wrong class type"
            result = agent.execute(context)
            assert result.status == AgentStatus.COMPLETED, f"Status: {result.status}"
            assert result.output is not None, "No output"
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {str(e)[:50]}")
            failed += 1

    # Test validator thresholds
    print("\n  Threshold Tests:")
    try:
        agent = create_agent('elaboration_validator')
        assert agent.THRESHOLD == 85, f"Expected 85, got {agent.THRESHOLD}"
        print("    ✓ elaboration_validator threshold = 85")
        passed += 1
    except Exception as e:
        print(f"    ✗ elaboration threshold: {e}")
        failed += 1

    try:
        agent = create_agent('coherence_validator')
        assert agent.THRESHOLD == 80, f"Expected 80, got {agent.THRESHOLD}"
        print("    ✓ coherence_validator threshold = 80")
        passed += 1
    except Exception as e:
        print(f"    ✗ coherence threshold: {e}")
        failed += 1

    try:
        agent = create_agent('pedagogy_validator')
        assert agent.THRESHOLD == 80, f"Expected 80, got {agent.THRESHOLD}"
        print("    ✓ pedagogy_validator threshold = 80")
        passed += 1
    except Exception as e:
        print(f"    ✗ pedagogy threshold: {e}")
        failed += 1

    try:
        agent = create_agent('timing_validator')
        assert agent.MIN_WORDS == 1950, f"Expected 1950, got {agent.MIN_WORDS}"
        assert agent.MAX_WORDS == 2250, f"Expected 2250, got {agent.MAX_WORDS}"
        print("    ✓ timing_validator word range = 1950-2250")
        passed += 1
    except Exception as e:
        print(f"    ✗ timing word range: {e}")
        failed += 1

    # =========================================================================
    # PHASE 4: Assembly
    # =========================================================================
    print("\n" + "=" * 60)
    print("PHASE 4: Assembly Tests")
    print("=" * 60)

    phase4_agents = [
        ('lesson_assembler', LessonAssemblerAgent),
        ('powerpoint_assembler', PowerPointAssemblerAgent),
        ('unit_folder_organizer', UnitFolderOrganizerAgent),
        ('final_qa_reporter', FinalQAReporterAgent),
    ]

    for name, expected_class in phase4_agents:
        try:
            agent = create_agent(name)
            assert isinstance(agent, expected_class), f"Wrong class type"
            result = agent.execute(context)
            assert result.status == AgentStatus.COMPLETED, f"Status: {result.status}"
            assert result.output is not None, "No output"
            print(f"  ✓ {name}")
            passed += 1
        except Exception as e:
            print(f"  ✗ {name}: {str(e)[:50]}")
            failed += 1

    # Test specific outputs
    print("\n  Output Tests:")
    try:
        agent = create_agent('powerpoint_assembler')
        result = agent.execute(context)
        assert result.output['powerpoint_blueprint']['total_slides'] == 16
        print("    ✓ powerpoint_assembler creates 16 slides")
        passed += 1
    except Exception as e:
        print(f"    ✗ powerpoint 16 slides: {e}")
        failed += 1

    try:
        agent = create_agent('final_qa_reporter')
        result = agent.execute(context)
        assert 'qa_report' in result.output
        assert 'executive_summary' in result.output['qa_report']
        assert 'production_readiness' in result.output['qa_report']
        assert 'scores' in result.output['qa_report']
        print("    ✓ final_qa_reporter generates complete report")
        passed += 1
    except Exception as e:
        print(f"    ✗ qa report: {e}")
        failed += 1

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    total = passed + failed
    print(f"Total Tests: {total}")
    print(f"Passed: {passed} ({100*passed//total}%)")
    print(f"Failed: {failed}")
    print("=" * 60)

    return passed, failed


if __name__ == '__main__':
    passed, failed = run_tests()
    exit(0 if failed == 0 else 1)
