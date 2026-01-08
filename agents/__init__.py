"""
Theater Education Pipeline Agents
=================================

Agent implementations for the Theater Education Pipeline.
Each agent processes specific content generation or validation tasks.
"""

from .base import Agent, AgentStatus, AgentResult
from .unit_planning import (
    UnitPlannerAgent,
    StandardsMapperAgent,
    UnitScopeValidatorAgent,
    LearningObjectiveGeneratorAgent,
)
from .daily_generation import (
    LessonPlanGeneratorAgent,
    WarmupGeneratorAgent,
    PowerPointGeneratorAgent,
    ActivityGeneratorAgent,
    HandoutGeneratorAgent,
    JournalExitGeneratorAgent,
    PresenterNotesWriterAgent,
)
from .validation import (
    TruncationValidatorAgent,
    ElaborationValidatorAgent,
    TimingValidatorAgent,
    StructureValidatorAgent,
    StandardsCoverageValidatorAgent,
    CoherenceValidatorAgent,
    PedagogyValidatorAgent,
    ContentAccuracyValidatorAgent,
)
from .assembly import (
    LessonAssemblerAgent,
    PowerPointAssemblerAgent,
    UnitFolderOrganizerAgent,
)


def create_agent(agent_name: str, prompt_path=None):
    """Factory function to create agents by name."""
    from pathlib import Path

    if prompt_path is None:
        prompt_path = Path(__file__).parent / "prompts" / f"{agent_name}.md"

    AGENT_REGISTRY = {
        # Unit Planning (Phase 1)
        "unit_planner": UnitPlannerAgent,
        "standards_mapper": StandardsMapperAgent,
        "unit_scope_validator": UnitScopeValidatorAgent,
        "learning_objective_generator": LearningObjectiveGeneratorAgent,

        # Daily Generation (Phase 2)
        "lesson_plan_generator": LessonPlanGeneratorAgent,
        "warmup_generator": WarmupGeneratorAgent,
        "powerpoint_generator": PowerPointGeneratorAgent,
        "activity_generator": ActivityGeneratorAgent,
        "handout_generator": HandoutGeneratorAgent,
        "journal_exit_generator": JournalExitGeneratorAgent,
        "presenter_notes_writer": PresenterNotesWriterAgent,

        # Validation (Phase 3)
        "truncation_validator": TruncationValidatorAgent,
        "elaboration_validator": ElaborationValidatorAgent,
        "timing_validator": TimingValidatorAgent,
        "structure_validator": StructureValidatorAgent,
        "standards_coverage_validator": StandardsCoverageValidatorAgent,
        "coherence_validator": CoherenceValidatorAgent,
        "pedagogy_validator": PedagogyValidatorAgent,
        "content_accuracy_validator": ContentAccuracyValidatorAgent,

        # Assembly (Phase 4)
        "lesson_assembler": LessonAssemblerAgent,
        "powerpoint_assembler": PowerPointAssemblerAgent,
        "unit_folder_organizer": UnitFolderOrganizerAgent,
    }

    agent_class = AGENT_REGISTRY.get(agent_name, Agent)
    return agent_class(agent_name, prompt_path)


__all__ = [
    # Base
    "Agent",
    "AgentStatus",
    "AgentResult",
    "create_agent",

    # Unit Planning
    "UnitPlannerAgent",
    "StandardsMapperAgent",
    "UnitScopeValidatorAgent",
    "LearningObjectiveGeneratorAgent",

    # Daily Generation
    "LessonPlanGeneratorAgent",
    "WarmupGeneratorAgent",
    "PowerPointGeneratorAgent",
    "ActivityGeneratorAgent",
    "HandoutGeneratorAgent",
    "JournalExitGeneratorAgent",
    "PresenterNotesWriterAgent",

    # Validation
    "TruncationValidatorAgent",
    "ElaborationValidatorAgent",
    "TimingValidatorAgent",
    "StructureValidatorAgent",
    "StandardsCoverageValidatorAgent",
    "CoherenceValidatorAgent",
    "PedagogyValidatorAgent",
    "ContentAccuracyValidatorAgent",

    # Assembly
    "LessonAssemblerAgent",
    "PowerPointAssemblerAgent",
    "UnitFolderOrganizerAgent",
]
