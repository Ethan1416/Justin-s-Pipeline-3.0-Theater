#!/usr/bin/env python3
"""
Theater Education Pipeline Runner
==================================

Main entry point for generating complete theater education lesson packages.

Usage:
    # Generate a single day's lesson
    python run_theater_pipeline.py --unit 1 --day 1

    # Generate entire unit
    python run_theater_pipeline.py --unit 1 --all-days

    # Resume from a specific step
    python run_theater_pipeline.py --unit 1 --day 1 --resume-from step7

    # Dry run (validate only, no output)
    python run_theater_pipeline.py --unit 1 --day 1 --dry-run

    # Verbose output
    python run_theater_pipeline.py --unit 1 --day 1 --verbose

Output:
    production/
    └── Unit_1_Greek_Theater/
        └── Day_01/
            ├── lesson_plan.md
            ├── powerpoint.pptx
            ├── handout.pdf
            ├── journal_prompts.md
            └── exit_ticket.md
"""

import argparse
import json
import logging
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

# Import orchestrators
try:
    from orchestrators.orchestrators import (
        UnitPlanningOrchestrator,
        DailyGenerationOrchestrator,
        ValidationGateOrchestrator,
        AssemblyOrchestrator,
        AgentContext,
        create_orchestrator
    )
    ORCHESTRATORS_AVAILABLE = True
except ImportError:
    ORCHESTRATORS_AVAILABLE = False

# Import agents package
try:
    from agents import (
        Agent,
        AgentStatus,
        AgentResult,
        create_agent,
        # Unit Planning
        UnitPlannerAgent,
        StandardsMapperAgent,
        UnitScopeValidatorAgent,
        LearningObjectiveGeneratorAgent,
        # Daily Generation
        LessonPlanGeneratorAgent,
        WarmupGeneratorAgent,
        ActivityGeneratorAgent,
        HandoutGeneratorAgent,
        JournalExitGeneratorAgent,
        PresenterNotesWriterAgent,
        # Validation
        TruncationValidatorAgent,
        ElaborationValidatorAgent,
        TimingValidatorAgent,
        StructureValidatorAgent,
        # Assembly
        LessonAssemblerAgent,
        PowerPointAssemblerAgent,
        UnitFolderOrganizerAgent,
    )
    AGENTS_PACKAGE_AVAILABLE = True
except ImportError:
    AGENTS_PACKAGE_AVAILABLE = False

# Pipeline root directory
PIPELINE_ROOT = Path(__file__).parent


class AgentStatus(Enum):
    """Status of agent execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class PipelinePhase(Enum):
    """Pipeline execution phases."""
    UNIT_PLANNING = "unit_planning"
    DAILY_GENERATION = "daily_generation"
    VALIDATION = "validation"
    ASSEMBLY = "assembly"


@dataclass
class AgentResult:
    """Result from agent execution."""
    agent_name: str
    status: AgentStatus
    output: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0


@dataclass
class LessonContext:
    """Context for lesson generation."""
    unit_number: int
    unit_name: str
    day: int
    topic: str
    standards: List[Dict[str, str]]
    learning_objectives: List[str]
    vocabulary: List[Dict[str, str]]
    prior_knowledge: str
    warmup: Dict[str, Any]
    activity: Dict[str, Any]
    journal_prompt: str
    exit_tickets: List[str]
    content_points: List[str]
    materials_list: List[str]


class ConfigLoader:
    """Load and manage pipeline configuration."""

    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or PIPELINE_ROOT / "config"
        self._pipeline_config = None
        self._constraints = None
        self._theater_config = None

    @property
    def pipeline(self) -> Dict:
        """Load pipeline.yaml configuration."""
        if self._pipeline_config is None:
            config_path = self.config_dir / "pipeline.yaml"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._pipeline_config = yaml.safe_load(f)
            else:
                self._pipeline_config = {}
        return self._pipeline_config

    @property
    def constraints(self) -> Dict:
        """Load constraints.yaml configuration."""
        if self._constraints is None:
            config_path = self.config_dir / "constraints.yaml"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._constraints = yaml.safe_load(f)
            else:
                self._constraints = {}
        return self._constraints

    @property
    def theater(self) -> Dict:
        """Load theater.yaml configuration."""
        if self._theater_config is None:
            config_path = self.config_dir / "theater.yaml"
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self._theater_config = yaml.safe_load(f)
            else:
                self._theater_config = {}
        return self._theater_config

    def get_execution_order(self, phase: str) -> List[str]:
        """Get agent execution order for a phase."""
        return self.pipeline.get('execution_order', {}).get(phase, [])

    def get_quality_gate(self, gate_name: str) -> Dict:
        """Get quality gate configuration."""
        return self.pipeline.get('quality_gates', {}).get(gate_name, {})


class InputLoader:
    """Load lesson input data."""

    def __init__(self, inputs_dir: Path = None):
        self.inputs_dir = inputs_dir or PIPELINE_ROOT / "inputs" / "sample_theater"

    def load_lesson(self, unit: int, day: int) -> Optional[Dict]:
        """Load lesson input for a specific unit and day."""
        # Map unit numbers to names
        unit_names = {
            1: "unit1_greek",
            2: "unit2_commedia",
            3: "unit3_shakespeare",
            4: "unit4_oneacts"
        }

        unit_key = unit_names.get(unit)
        if not unit_key:
            return None

        # Check multiple possible locations (prefer Romeo and Juliet inputs first for Unit 3)
        possible_paths = []

        # For Unit 3 (Shakespeare), prefer Romeo and Juliet inputs
        if unit == 3:
            possible_paths.extend([
                PIPELINE_ROOT / "inputs" / "romeo_and_juliet" / f"day{day:02d}_meet_the_bard.json",
                PIPELINE_ROOT / "inputs" / "romeo_and_juliet" / f"day{day:02d}.json",
            ])

        # Standard sample_theater location (fallback)
        possible_paths.append(self.inputs_dir / f"sample_{unit_key}_day{day}.json")

        for filepath in possible_paths:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)

        return None

    def create_lesson_context(self, data: Dict) -> LessonContext:
        """Create LessonContext from input data."""
        unit_info = data.get('unit', {})

        # Normalize content_points to handle both formats:
        # Old format: ["string1", "string2", ...]
        # New format: [{"point": "...", "expanded": [...]}, ...]
        raw_points = data.get('content_points', [])
        normalized_points = []
        for cp in raw_points:
            if isinstance(cp, dict):
                normalized_points.append(cp.get('point', ''))
            else:
                normalized_points.append(cp)

        return LessonContext(
            unit_number=unit_info.get('number', 1),
            unit_name=unit_info.get('name', 'Unknown Unit'),
            day=data.get('day', 1),
            topic=data.get('topic', ''),
            standards=data.get('standards', []),
            learning_objectives=data.get('learning_objectives', []),
            vocabulary=data.get('vocabulary', []),
            prior_knowledge=data.get('prior_knowledge', ''),
            warmup=data.get('warmup', {}),
            activity=data.get('activity', {}),
            journal_prompt=data.get('journal_prompt', ''),
            exit_tickets=data.get('exit_tickets', []),
            content_points=normalized_points,
            materials_list=data.get('materials_list', [])
        )


class Agent:
    """Base class for pipeline agents."""

    def __init__(self, name: str, prompt_path: Path):
        self.name = name
        self.prompt_path = prompt_path
        self.prompt_content = self._load_prompt()

    def _load_prompt(self) -> str:
        """Load agent prompt from file."""
        if self.prompt_path.exists():
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Execute the agent with given context."""
        start_time = datetime.now()

        try:
            output = self._process(context)
            status = AgentStatus.COMPLETED
            errors = []
        except Exception as e:
            output = {}
            status = AgentStatus.FAILED
            errors = [str(e)]

        duration = (datetime.now() - start_time).total_seconds()

        return AgentResult(
            agent_name=self.name,
            status=status,
            output=output,
            errors=errors,
            duration_seconds=duration
        )

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process the agent logic. Override in subclasses."""
        # Default implementation - return context as-is
        return {"processed": True, "agent": self.name}


class UnitPlannerAgent(Agent):
    """Agent for planning unit structure."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        if not lesson_ctx:
            return {"error": "No lesson context provided"}

        return {
            "unit_plan": {
                "unit_number": lesson_ctx.unit_number,
                "unit_name": lesson_ctx.unit_name,
                "total_days": 20 if lesson_ctx.unit_number == 1 else 18,
                "current_day": lesson_ctx.day,
                "topic": lesson_ctx.topic,
                "standards": lesson_ctx.standards,
                "objectives": lesson_ctx.learning_objectives
            }
        }


class LessonPlanGeneratorAgent(Agent):
    """Agent for generating lesson plans."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        if not lesson_ctx:
            return {"error": "No lesson context provided"}

        # Generate lesson plan structure
        lesson_plan = {
            "metadata": {
                "unit": lesson_ctx.unit_name,
                "day": lesson_ctx.day,
                "topic": lesson_ctx.topic,
                "duration": "56 minutes",
                "date": datetime.now().strftime("%Y-%m-%d")
            },
            "standards": lesson_ctx.standards,
            "learning_objectives": lesson_ctx.learning_objectives,
            "vocabulary": lesson_ctx.vocabulary,
            "materials": lesson_ctx.materials_list,
            "procedure": {
                "opening": {
                    "duration": "5 minutes",
                    "journal_prompt": lesson_ctx.journal_prompt
                },
                "warmup": {
                    "duration": "5 minutes",
                    "activity": lesson_ctx.warmup
                },
                "direct_instruction": {
                    "duration": "15 minutes",
                    "content_points": lesson_ctx.content_points
                },
                "guided_practice": {
                    "duration": "15 minutes",
                    "activity": lesson_ctx.activity
                },
                "closure": {
                    "duration": "10 minutes",
                    "exit_tickets": lesson_ctx.exit_tickets
                }
            }
        }

        return {"lesson_plan": lesson_plan}


class PresenterNotesWriterAgent(Agent):
    """Agent for writing presenter notes."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')
        if not lesson_ctx:
            return {"error": "No lesson context provided"}

        # Generate presenter notes (15 minutes = ~2000 words at 130-150 WPM)
        notes = []

        # Opening
        notes.append(f"[SLIDE 1: Title]\n")
        notes.append(f"Good morning, everyone! Today we begin our exploration of {lesson_ctx.topic}. ")
        notes.append(f"[PAUSE] Take a moment to look at the learning objectives on the screen. ")
        notes.append(f"By the end of our time together, you'll be able to: ")
        for obj in lesson_ctx.learning_objectives:
            notes.append(f"[EMPHASIS: {obj.split()[0]}] {obj}. ")
        notes.append(f"[PAUSE]\n\n")

        # Content slides
        for i, point in enumerate(lesson_ctx.content_points, 1):
            notes.append(f"[SLIDE {i+2}: {point[:30]}...]\n")
            notes.append(f"{point}. [PAUSE] ")
            notes.append(f"Let's think about why this matters. [CHECK FOR UNDERSTANDING] ")
            notes.append(f"Can anyone share what stands out to them about this? [PAUSE]\n\n")

        # Vocabulary integration
        notes.append(f"[SLIDE: Key Vocabulary]\n")
        notes.append(f"Now let's make sure we understand our key terms for today. ")
        for vocab in lesson_ctx.vocabulary[:3]:  # First 3 terms
            notes.append(f"[EMPHASIS: {vocab['term']}] - {vocab['definition']}. ")
            notes.append(f"For example, {vocab.get('usage_example', '')} [PAUSE] ")

        return {
            "presenter_notes": "".join(notes),
            "word_count": len("".join(notes).split()),
            "estimated_duration_minutes": len("".join(notes).split()) / 140  # ~140 WPM
        }


class TruncationValidatorAgent(Agent):
    """HARDCODED: Validate no truncated sentences."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = context.get('content', '')
        if isinstance(content, dict):
            content = str(content)

        issues = []
        sentences = content.replace('\n', ' ').split('.')

        for i, sentence in enumerate(sentences[:-1]):  # Skip last (may be empty)
            sentence = sentence.strip()
            if sentence and not sentence[-1] in '.!?:':
                # Check for truncation indicators
                if sentence.endswith('...') or sentence.endswith('--'):
                    issues.append(f"Truncated sentence at position {i}: '{sentence[:50]}...'")

        return {
            "validation_status": "PASS" if not issues else "FAIL",
            "issues": issues,
            "sentences_checked": len(sentences)
        }


class ElaborationValidatorAgent(Agent):
    """HARDCODED: Validate professional elaboration depth."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = context.get('content', '')
        if isinstance(content, dict):
            content = str(content)

        # Calculate elaboration scores
        word_count = len(content.split())
        sentence_count = len([s for s in content.split('.') if s.strip()])

        # Scoring criteria
        scores = {
            "depth": min(100, (word_count / 2000) * 100),  # Target 2000 words
            "examples": 100 if "example" in content.lower() or "for instance" in content.lower() else 50,
            "procedure": 100 if any(kw in content.lower() for kw in ['first', 'then', 'next', 'finally']) else 60,
            "tone": 100 if not any(kw in content.lower() for kw in ['gonna', 'wanna', 'kinda']) else 70,
            "connections": 100 if "because" in content.lower() or "therefore" in content.lower() else 60
        }

        # Weighted average: Depth 30%, Examples 20%, Procedure 20%, Tone 15%, Connections 15%
        total_score = (
            scores["depth"] * 0.30 +
            scores["examples"] * 0.20 +
            scores["procedure"] * 0.20 +
            scores["tone"] * 0.15 +
            scores["connections"] * 0.15
        )

        return {
            "validation_status": "PASS" if total_score >= 85 else "FAIL",
            "total_score": round(total_score, 1),
            "category_scores": scores,
            "word_count": word_count,
            "threshold": 85
        }


class TimingValidatorAgent(Agent):
    """HARDCODED: Validate content fits timing constraints."""

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        content = context.get('presenter_notes', '')
        target_minutes = context.get('target_minutes', 15)
        speaking_rate = context.get('speaking_rate_wpm', 140)

        word_count = len(content.split())
        estimated_minutes = word_count / speaking_rate

        # Within 10% of target
        min_acceptable = target_minutes * 0.9
        max_acceptable = target_minutes * 1.1

        status = "PASS" if min_acceptable <= estimated_minutes <= max_acceptable else "FAIL"

        return {
            "validation_status": status,
            "word_count": word_count,
            "estimated_minutes": round(estimated_minutes, 1),
            "target_minutes": target_minutes,
            "acceptable_range": f"{min_acceptable:.1f}-{max_acceptable:.1f} minutes"
        }


class StructureValidatorAgent(Agent):
    """HARDCODED: Validate all lesson components present."""

    REQUIRED_COMPONENTS = [
        "learning_objectives",
        "vocabulary",
        "warmup",
        "content_points",
        "activity",
        "journal_prompt",
        "exit_tickets",
        "materials_list"
    ]

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        lesson_ctx = context.get('lesson_context')

        missing = []
        present = []

        for component in self.REQUIRED_COMPONENTS:
            value = getattr(lesson_ctx, component, None) if lesson_ctx else None
            if value:
                present.append(component)
            else:
                missing.append(component)

        return {
            "validation_status": "PASS" if not missing else "FAIL",
            "components_present": present,
            "components_missing": missing,
            "completeness_percentage": round(len(present) / len(self.REQUIRED_COMPONENTS) * 100, 1)
        }


class OrchestratorManager:
    """Manages agent orchestration and execution flow."""

    def __init__(self, config: ConfigLoader):
        self.config = config
        self.agents_dir = PIPELINE_ROOT / "agents" / "prompts"
        self.results: List[AgentResult] = []
        self.logger = logging.getLogger("OrchestratorManager")

    def create_agent(self, agent_name: str):
        """Create an agent instance by name."""
        prompt_path = self.agents_dir / f"{agent_name}.md"

        # Use the agents package factory if available
        if AGENTS_PACKAGE_AVAILABLE:
            return create_agent(agent_name, prompt_path)

        # Fallback to inline classes (for backwards compatibility)
        agent_classes = {
            "unit_planner": UnitPlannerAgent,
            "lesson_plan_generator": LessonPlanGeneratorAgent,
            "presenter_notes_writer": PresenterNotesWriterAgent,
            "truncation_validator": TruncationValidatorAgent,
            "elaboration_validator": ElaborationValidatorAgent,
            "timing_validator": TimingValidatorAgent,
            "structure_validator": StructureValidatorAgent,
        }

        agent_class = agent_classes.get(agent_name, Agent)
        return agent_class(agent_name, prompt_path)

    def execute_phase(self, phase: PipelinePhase, context: Dict[str, Any]) -> List[AgentResult]:
        """Execute all agents in a pipeline phase."""
        phase_results = []

        # Get agents for this phase
        if phase == PipelinePhase.UNIT_PLANNING:
            agents = ["unit_planner", "standards_mapper", "unit_scope_validator"]
        elif phase == PipelinePhase.DAILY_GENERATION:
            agents = [
                "lesson_plan_generator",
                "warmup_generator",
                "presenter_notes_writer",
                "activity_generator",
                "handout_generator",
                "journal_exit_generator"
            ]
        elif phase == PipelinePhase.VALIDATION:
            agents = [
                "truncation_validator",
                "elaboration_validator",
                "timing_validator",
                "structure_validator"
            ]
        elif phase == PipelinePhase.ASSEMBLY:
            agents = ["lesson_assembler", "powerpoint_assembler"]
        else:
            agents = []

        self.logger.info(f"Executing phase: {phase.value} with {len(agents)} agents")

        for agent_name in agents:
            self.logger.info(f"  Running agent: {agent_name}")
            agent = self.create_agent(agent_name)
            result = agent.execute(context)
            phase_results.append(result)
            self.results.append(result)

            # Update context with agent output
            context[f"{agent_name}_output"] = result.output

            if result.status == AgentStatus.FAILED:
                self.logger.error(f"  Agent {agent_name} FAILED: {result.errors}")
                # Check if we should continue or halt
                if agent_name in ["truncation_validator", "structure_validator"]:
                    self.logger.error("  CRITICAL validator failed - halting phase")
                    break
            else:
                self.logger.info(f"  Agent {agent_name} completed successfully")

        return phase_results


class OutputGenerator:
    """Generate output files from pipeline results."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or PIPELINE_ROOT / "production"

    def generate_lesson_plan_md(self, lesson_plan: Dict, output_path: Path):
        """Generate lesson plan markdown file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        metadata = lesson_plan.get('metadata', {})
        procedure = lesson_plan.get('procedure', {})

        content = f"""# Lesson Plan: {metadata.get('unit', '')} - Day {metadata.get('day', '')}

## Basic Information
| Field | Value |
|-------|-------|
| Unit | {metadata.get('unit', '')} |
| Day | {metadata.get('day', '')} |
| Topic | {metadata.get('topic', '')} |
| Duration | {metadata.get('duration', '56 minutes')} |
| Date | {metadata.get('date', '')} |

## Standards Addressed
"""
        for std in lesson_plan.get('standards', []):
            content += f"- **{std.get('code', '')}**: {std.get('full_text', '')}\n"

        content += "\n## Learning Objectives\n"
        content += "By the end of this lesson, students will be able to:\n"
        for i, obj in enumerate(lesson_plan.get('learning_objectives', []), 1):
            content += f"{i}. {obj}\n"

        content += "\n## Vocabulary\n"
        for vocab in lesson_plan.get('vocabulary', []):
            content += f"- **{vocab.get('term', '')}**: {vocab.get('definition', '')}\n"

        content += "\n## Materials Needed\n"
        for material in lesson_plan.get('materials', []):
            content += f"- [ ] {material}\n"

        content += f"""
## Lesson Procedure

### Opening ({procedure.get('opening', {}).get('duration', '5 minutes')})
**Journal Prompt:** {procedure.get('opening', {}).get('journal_prompt', '')}

### Warmup ({procedure.get('warmup', {}).get('duration', '5 minutes')})
"""
        warmup = procedure.get('warmup', {}).get('activity', {})
        content += f"**{warmup.get('name', '')}**\n"
        content += f"{warmup.get('instructions', '')}\n"
        content += f"*Connection to lesson: {warmup.get('connection_to_lesson', '')}*\n"

        content += f"""
### Direct Instruction ({procedure.get('direct_instruction', {}).get('duration', '15 minutes')})
**Key Points:**
"""
        for point in procedure.get('direct_instruction', {}).get('content_points', []):
            content += f"- {point}\n"

        content += f"""
### Guided Practice ({procedure.get('guided_practice', {}).get('duration', '15 minutes')})
"""
        activity = procedure.get('guided_practice', {}).get('activity', {})
        content += f"**{activity.get('name', '')}**\n"
        content += f"{activity.get('instructions', '')}\n"

        content += f"""
### Closure ({procedure.get('closure', {}).get('duration', '10 minutes')})
**Exit Ticket Questions:**
"""
        for i, q in enumerate(procedure.get('closure', {}).get('exit_tickets', []), 1):
            content += f"{i}. {q}\n"

        content += """
---
*Generated by Theater Education Pipeline*
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return output_path


class TheaterPipeline:
    """Main pipeline orchestration class."""

    def __init__(self, verbose: bool = False, use_orchestrators: bool = True):
        self.config = ConfigLoader()
        self.input_loader = InputLoader()
        self.orchestrator = OrchestratorManager(self.config)
        self.output_generator = OutputGenerator()
        self.verbose = verbose
        self.use_orchestrators = use_orchestrators and ORCHESTRATORS_AVAILABLE
        self._setup_logging()

        # Initialize orchestrators if available
        if self.use_orchestrators:
            self.unit_planning_orch = UnitPlanningOrchestrator()
            self.daily_gen_orch = DailyGenerationOrchestrator()
            self.validation_orch = ValidationGateOrchestrator()
            self.assembly_orch = AssemblyOrchestrator()

    def _setup_logging(self):
        """Configure logging."""
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        self.logger = logging.getLogger("TheaterPipeline")

    def run(self, unit: int, day: int, dry_run: bool = False) -> Dict[str, Any]:
        """Run the pipeline for a specific unit and day."""
        self.logger.info("=" * 60)
        self.logger.info("THEATER EDUCATION PIPELINE")
        self.logger.info("=" * 60)
        self.logger.info(f"Unit: {unit}, Day: {day}")
        self.logger.info(f"Dry Run: {dry_run}")
        self.logger.info(f"Using Orchestrators: {self.use_orchestrators}")
        self.logger.info("")

        # Load input
        self.logger.info("Loading lesson input...")
        lesson_data = self.input_loader.load_lesson(unit, day)
        if not lesson_data:
            self.logger.error(f"No input found for Unit {unit} Day {day}")
            return {"status": "FAILED", "error": "Input not found"}

        lesson_context = self.input_loader.create_lesson_context(lesson_data)
        self.logger.info(f"Topic: {lesson_context.topic}")

        # Use enhanced orchestrators if available
        if self.use_orchestrators:
            return self._run_with_orchestrators(unit, day, lesson_context, lesson_data, dry_run)

        # Create execution context
        context = {
            "lesson_context": lesson_context,
            "config": {
                "pipeline": self.config.pipeline,
                "constraints": self.config.constraints,
                "theater": self.config.theater
            },
            "dry_run": dry_run
        }

        # Execute phases
        all_results = []

        # Phase 1: Unit Planning
        self.logger.info("\n" + "-" * 40)
        self.logger.info("PHASE 1: UNIT PLANNING")
        self.logger.info("-" * 40)
        results = self.orchestrator.execute_phase(PipelinePhase.UNIT_PLANNING, context)
        all_results.extend(results)

        # Phase 2: Daily Generation
        self.logger.info("\n" + "-" * 40)
        self.logger.info("PHASE 2: DAILY GENERATION")
        self.logger.info("-" * 40)
        results = self.orchestrator.execute_phase(PipelinePhase.DAILY_GENERATION, context)
        all_results.extend(results)

        # Phase 3: Validation
        self.logger.info("\n" + "-" * 40)
        self.logger.info("PHASE 3: VALIDATION")
        self.logger.info("-" * 40)
        results = self.orchestrator.execute_phase(PipelinePhase.VALIDATION, context)
        all_results.extend(results)

        # Check validation results
        validation_passed = all(
            r.output.get('validation_status') == 'PASS'
            for r in results
            if 'validation_status' in r.output
        )

        if not validation_passed:
            self.logger.warning("Some validations failed - check results")

        # Phase 4: Assembly (if not dry run and validation passed)
        if not dry_run and validation_passed:
            self.logger.info("\n" + "-" * 40)
            self.logger.info("PHASE 4: ASSEMBLY")
            self.logger.info("-" * 40)
            results = self.orchestrator.execute_phase(PipelinePhase.ASSEMBLY, context)
            all_results.extend(results)

            # Generate output files
            self._generate_outputs(context, lesson_context)

        # Generate summary
        summary = self._generate_summary(all_results)

        self.logger.info("\n" + "=" * 60)
        self.logger.info("PIPELINE COMPLETE")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Agents: {summary['total_agents']}")
        self.logger.info(f"Completed: {summary['completed']}")
        self.logger.info(f"Failed: {summary['failed']}")
        self.logger.info(f"Duration: {summary['total_duration']:.1f}s")

        return {
            "status": "SUCCESS" if summary['failed'] == 0 else "PARTIAL",
            "summary": summary,
            "results": [
                {
                    "agent": r.agent_name,
                    "status": r.status.value,
                    "duration": r.duration_seconds
                }
                for r in all_results
            ]
        }

    def _generate_outputs(self, context: Dict, lesson_context: LessonContext):
        """Generate output files."""
        # Create output directory
        unit_folder = f"Unit_{lesson_context.unit_number}_{lesson_context.unit_name.replace(' ', '_')}"
        day_folder = f"Day_{lesson_context.day:02d}"
        output_dir = self.output_generator.output_dir / unit_folder / day_folder
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate lesson plan
        lesson_plan = context.get('lesson_plan_generator_output', {}).get('lesson_plan', {})
        if lesson_plan:
            lesson_path = output_dir / "lesson_plan.md"
            self.output_generator.generate_lesson_plan_md(lesson_plan, lesson_path)
            self.logger.info(f"Generated: {lesson_path}")

        # Generate PowerPoint using Theater PPTX Generator
        try:
            from skills.generation.theater_pptx_generator import generate_pptx

            # Use raw lesson data if available (preserves expanded content)
            # Otherwise fall back to lesson_context
            raw_data = context.get('raw_lesson_data', {})

            lesson_data = {
                "topic": lesson_context.topic,
                "day": lesson_context.day,
                "learning_objectives": lesson_context.learning_objectives,
                "vocabulary": lesson_context.vocabulary,
                "warmup": lesson_context.warmup,
                "activity": lesson_context.activity,
                "journal_prompt": lesson_context.journal_prompt,
                "exit_tickets": lesson_context.exit_tickets,
                # Use raw content_points with expanded content if available
                "content_points": raw_data.get('content_points', lesson_context.content_points),
                "presenter_notes": context.get('presenter_notes_writer_output', {})
            }

            result = generate_pptx(
                lesson_data=lesson_data,
                output_dir=output_dir,
                unit_number=lesson_context.unit_number,
                day=lesson_context.day
            )

            if result['status'] == 'success':
                self.logger.info(f"Generated: {result['file_path']}")
            else:
                self.logger.error(f"PowerPoint generation failed: {result.get('error', 'Unknown error')}")

        except ImportError as e:
            self.logger.warning(f"PowerPoint generation unavailable: {e}")
            # Create placeholder
            pptx_placeholder = output_dir / "powerpoint_placeholder.txt"
            with open(pptx_placeholder, 'w') as f:
                f.write("PowerPoint generation requires python-pptx library.\n")
                f.write(f"Install with: pip install python-pptx\n")
                f.write(f"Topic: {lesson_context.topic}\n")
                f.write(f"Slides needed: 16 (12 content + 4 auxiliary)\n")
            self.logger.info(f"Generated placeholder: {pptx_placeholder}")

    def _generate_summary(self, results: List[AgentResult]) -> Dict:
        """Generate execution summary."""
        return {
            "total_agents": len(results),
            "completed": sum(1 for r in results if r.status == AgentStatus.COMPLETED),
            "failed": sum(1 for r in results if r.status == AgentStatus.FAILED),
            "skipped": sum(1 for r in results if r.status == AgentStatus.SKIPPED),
            "total_duration": sum(r.duration_seconds for r in results)
        }

    def _run_with_orchestrators(
        self,
        unit: int,
        day: int,
        lesson_context: LessonContext,
        lesson_data: Dict,
        dry_run: bool
    ) -> Dict[str, Any]:
        """Run pipeline using enhanced orchestrators with retry logic."""
        from datetime import datetime
        start_time = datetime.now()

        # Get unit name mapping
        unit_names = {
            1: "Greek Theater",
            2: "Commedia dell'Arte",
            3: "Shakespeare",
            4: "Student-Directed One Acts"
        }

        # Create agent context
        agent_context = AgentContext(
            unit_number=unit,
            unit_name=unit_names.get(unit, "Unknown"),
            day=day,
            topic=lesson_context.topic
        )

        all_results = []
        phase_outputs = {}

        # Phase 1: Unit Planning
        self.logger.info("\n" + "-" * 40)
        self.logger.info("PHASE 1: UNIT PLANNING (with orchestrator)")
        self.logger.info("-" * 40)

        unit_result = self.unit_planning_orch.run(agent_context)
        all_results.append(("unit_planning", unit_result))
        phase_outputs["unit_planning"] = unit_result.outputs

        if unit_result.status == "escalated":
            self.logger.error("Unit planning failed after max retries")
            return {"status": "FAILED", "error": "Unit planning escalated", "results": all_results}

        # Phase 2: Daily Generation
        self.logger.info("\n" + "-" * 40)
        self.logger.info("PHASE 2: DAILY GENERATION (with orchestrator)")
        self.logger.info("-" * 40)

        daily_result = self.daily_gen_orch.run(agent_context, daily_input=lesson_data)
        all_results.append(("daily_generation", daily_result))
        phase_outputs["daily_generation"] = daily_result.outputs

        if daily_result.status == "failed":
            self.logger.warning(f"Daily generation had failures: {daily_result.errors}")

        # Phase 3: Validation
        self.logger.info("\n" + "-" * 40)
        self.logger.info("PHASE 3: VALIDATION (with orchestrator)")
        self.logger.info("-" * 40)

        validation_result = self.validation_orch.run(agent_context, daily_output=daily_result.outputs)
        all_results.append(("validation", validation_result))
        phase_outputs["validation"] = validation_result.outputs

        validation_passed = validation_result.outputs.get("overall_status") == "PASSED"

        if not validation_passed:
            self.logger.warning("Validation failed - check results for retry instructions")
            rejection = validation_result.outputs.get("rejection_details", {})
            self.logger.warning(f"  Failed gate: {rejection.get('failed_gate', 'unknown')}")
            self.logger.warning(f"  Reason: {rejection.get('reason', 'unknown')}")

        # Phase 4: Assembly (if not dry run and validation passed)
        if not dry_run and validation_passed:
            self.logger.info("\n" + "-" * 40)
            self.logger.info("PHASE 4: ASSEMBLY (with orchestrator)")
            self.logger.info("-" * 40)

            assembly_result = self.assembly_orch.run(
                agent_context,
                validated_output=validation_result.outputs.get("validated_output", daily_result.outputs)
            )
            all_results.append(("assembly", assembly_result))
            phase_outputs["assembly"] = assembly_result.outputs

            self.logger.info(f"Output directory: {assembly_result.outputs.get('output_directory', 'N/A')}")

            # Generate actual output files (pass raw lesson_data for expanded content)
            context = {
                "lesson_context": lesson_context,
                "lesson_plan_generator_output": daily_result.outputs.get("lesson_plan", {}),
                "presenter_notes_writer_output": daily_result.outputs.get("presenter_notes", {}),
                "raw_lesson_data": lesson_data  # Pass raw data with expanded content
            }
            self._generate_outputs(context, lesson_context)

        # Calculate summary
        total_duration = (datetime.now() - start_time).total_seconds()
        total_agents = sum(len(r[1].agents_run) for r in all_results)
        failed_agents = sum(len(r[1].agents_failed) for r in all_results)
        total_retries = sum(r[1].retry_count for r in all_results)

        self.logger.info("\n" + "=" * 60)
        self.logger.info("PIPELINE COMPLETE (Orchestrator Mode)")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Agents: {total_agents}")
        self.logger.info(f"Failed: {failed_agents}")
        self.logger.info(f"Retries: {total_retries}")
        self.logger.info(f"Duration: {total_duration:.1f}s")
        self.logger.info(f"Validation: {'PASSED' if validation_passed else 'FAILED'}")

        return {
            "status": "SUCCESS" if failed_agents == 0 and validation_passed else "PARTIAL",
            "validation_passed": validation_passed,
            "summary": {
                "total_agents": total_agents,
                "completed": total_agents - failed_agents,
                "failed": failed_agents,
                "retries": total_retries,
                "total_duration": total_duration
            },
            "phase_outputs": phase_outputs,
            "results": [
                {
                    "phase": phase,
                    "status": result.status,
                    "agents_run": result.agents_run,
                    "agents_failed": result.agents_failed,
                    "duration": result.duration_seconds
                }
                for phase, result in all_results
            ]
        }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Theater Education Pipeline - Generate complete lesson packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --unit 1 --day 1              Generate Greek Theater Day 1
  %(prog)s --unit 2 --day 1              Generate Commedia dell'Arte Day 1
  %(prog)s --unit 3 --day 1              Generate Shakespeare Day 1
  %(prog)s --unit 4 --day 1              Generate One Acts Day 1
  %(prog)s --unit 1 --day 1 --dry-run    Validate only, no output
  %(prog)s --unit 1 --day 1 --verbose    Show detailed logging
        """
    )

    parser.add_argument('--unit', type=int, required=True, choices=[1, 2, 3, 4],
                        help='Unit number (1=Greek, 2=Commedia, 3=Shakespeare, 4=One Acts)')
    parser.add_argument('--day', type=int, required=True,
                        help='Day number within the unit')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate only, do not generate output files')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')
    parser.add_argument('--resume-from', type=str,
                        help='Resume from a specific step (e.g., step7)')
    parser.add_argument('--output-dir', type=str,
                        help='Custom output directory')

    args = parser.parse_args()

    # Validate day number based on unit
    unit_days = {1: 20, 2: 18, 3: 25, 4: 17}
    max_days = unit_days.get(args.unit, 20)
    if args.day < 1 or args.day > max_days:
        parser.error(f"Day must be between 1 and {max_days} for Unit {args.unit}")

    # Run pipeline
    pipeline = TheaterPipeline(verbose=args.verbose)
    result = pipeline.run(unit=args.unit, day=args.day, dry_run=args.dry_run)

    # Exit code based on result
    if result['status'] == 'SUCCESS':
        return 0
    elif result['status'] == 'PARTIAL':
        return 1
    else:
        return 2


if __name__ == "__main__":
    sys.exit(main())
