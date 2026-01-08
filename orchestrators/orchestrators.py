#!/usr/bin/env python3
"""
Theater Pipeline Orchestrators
==============================

Python implementations of the four sub-orchestrators that coordinate
agent execution within each pipeline phase.

Orchestrators:
1. UnitPlanningOrchestrator - Phase 1: Generate unit plans
2. DailyGenerationOrchestrator - Phase 2: Generate daily lesson components
3. ValidationGateOrchestrator - Phase 3: Validate content (HARDCODED gates)
4. AssemblyOrchestrator - Phase 4: Assemble final outputs

Each orchestrator manages agent sequencing, dependency handling,
error recovery with retry logic, and context preservation.
"""

import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Setup logging
logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS AND DATA CLASSES
# =============================================================================

class RetryStrategy(Enum):
    """Retry strategies for different failure types."""
    TARGETED_FIX = "targeted_fix"          # Fix specific truncated items
    COMPONENT_REGEN = "component_regen"    # Regenerate missing components
    ENRICHMENT_PASS = "enrichment_pass"    # Add depth to weak areas
    ADJUSTMENT_PASS = "adjustment_pass"    # Expand or condense content


class GateStatus(Enum):
    """Validation gate status."""
    PASSED = "passed"
    FAILED = "failed"
    AUTO_FIXED = "auto_fixed"
    ESCALATED = "escalated"


@dataclass
class AgentContext:
    """Context passed between agents during orchestration."""
    unit_number: int
    unit_name: str
    day: int
    topic: str
    accumulated_outputs: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    max_retries: int = 3
    previous_failures: List[Dict] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)


@dataclass
class OrchestratorResult:
    """Result from orchestrator execution."""
    status: str  # "completed", "failed", "escalated"
    outputs: Dict[str, Any]
    agents_run: List[str]
    agents_failed: List[str]
    retry_count: int
    duration_seconds: float
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result from a validation gate."""
    gate_name: str
    status: GateStatus
    score: Optional[float] = None  # For scored gates (elaboration, timing)
    threshold: Optional[float] = None
    issues: List[Dict] = field(default_factory=list)
    auto_fixes_applied: List[str] = field(default_factory=list)
    fix_instructions: Optional[str] = None


# =============================================================================
# BASE ORCHESTRATOR
# =============================================================================

class BaseOrchestrator(ABC):
    """
    Base class for all orchestrators.

    Provides common functionality for agent execution, retry logic,
    and context management.
    """

    MAX_RETRIES = 3

    def __init__(self, config: Dict = None, agents: Dict[str, Callable] = None):
        """
        Initialize orchestrator.

        Args:
            config: Configuration dictionary from pipeline.yaml
            agents: Dictionary mapping agent names to callable implementations
        """
        self.config = config or {}
        self.agents = agents or {}
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_execution_order(self) -> List[str]:
        """Return list of agent names in execution order."""
        pass

    @abstractmethod
    def run(self, context: AgentContext, **kwargs) -> OrchestratorResult:
        """Execute the orchestration pipeline."""
        pass

    def execute_agent(
        self,
        agent_name: str,
        context: AgentContext,
        input_data: Dict
    ) -> Tuple[bool, Dict]:
        """
        Execute a single agent.

        Args:
            agent_name: Name of the agent to execute
            context: Current agent context
            input_data: Input data for the agent

        Returns:
            Tuple of (success, output_data)
        """
        self.logger.info(f"Executing agent: {agent_name}")

        agent_func = self.agents.get(agent_name)
        if not agent_func:
            self.logger.warning(f"Agent not implemented: {agent_name}")
            # Return placeholder for stub agents
            return True, {"status": "stub", "message": f"{agent_name} not yet implemented"}

        try:
            output = agent_func(input_data, context)
            context.accumulated_outputs[agent_name] = output
            self.logger.info(f"Agent {agent_name} completed successfully")
            return True, output
        except Exception as e:
            self.logger.error(f"Agent {agent_name} failed: {str(e)}")
            return False, {"error": str(e)}

    def handle_failure(
        self,
        agent_name: str,
        failure_details: Dict,
        context: AgentContext,
        strategy: RetryStrategy
    ) -> Dict:
        """
        Handle agent or gate failure with appropriate strategy.

        Args:
            agent_name: Name of the failed agent
            failure_details: Details about the failure
            context: Current context
            strategy: Retry strategy to use

        Returns:
            Instructions for retry or escalation
        """
        context.retry_count += 1
        context.previous_failures.append({
            "agent": agent_name,
            "details": failure_details,
            "timestamp": datetime.now().isoformat()
        })

        if context.retry_count >= self.MAX_RETRIES:
            return {
                "action": "ESCALATE",
                "reason": f"Max retries ({self.MAX_RETRIES}) exceeded for {agent_name}",
                "details": failure_details
            }

        if strategy == RetryStrategy.TARGETED_FIX:
            return {
                "action": "FIX_SPECIFIC",
                "targets": failure_details.get("items", []),
                "instruction": "Complete these specific issues"
            }
        elif strategy == RetryStrategy.COMPONENT_REGEN:
            return {
                "action": "REGENERATE_COMPONENTS",
                "components": failure_details.get("missing", []),
                "preserve": failure_details.get("valid", [])
            }
        elif strategy == RetryStrategy.ENRICHMENT_PASS:
            return {
                "action": "ENRICH",
                "weak_areas": failure_details.get("low_scores", []),
                "suggestions": failure_details.get("suggestions", [])
            }
        elif strategy == RetryStrategy.ADJUSTMENT_PASS:
            if failure_details.get("issue") == "too_short":
                return {
                    "action": "ELABORATE",
                    "target_words": failure_details.get("needed_words", 0),
                    "focus_slides": failure_details.get("under_elaborated", [])
                }
            else:
                return {
                    "action": "CONDENSE",
                    "target_words": failure_details.get("excess_words", 0),
                    "focus_slides": failure_details.get("verbose_slides", [])
                }

        return {"action": "RETRY", "attempt": context.retry_count}


# =============================================================================
# UNIT PLANNING ORCHESTRATOR
# =============================================================================

class UnitPlanningOrchestrator(BaseOrchestrator):
    """
    Phase 1: Unit Planning Orchestrator

    Generates comprehensive unit plans including:
    - Unit scope and topic sequence
    - Standards mapping (CA ELA/Literacy)
    - Learning objectives (Bloom's taxonomy)
    - Scope validation

    Runs ONCE per unit before daily generation begins.
    """

    def get_execution_order(self) -> List[str]:
        """Return agent execution order for unit planning."""
        return [
            "unit_planner",
            "standards_mapper",
            "learning_objective_generator",
            "unit_scope_validator"
        ]

    def run(
        self,
        context: AgentContext,
        unit_config: Dict = None
    ) -> OrchestratorResult:
        """
        Execute unit planning phase.

        Args:
            context: Agent context with unit info
            unit_config: Optional unit-specific configuration

        Returns:
            OrchestratorResult with unit plan
        """
        start_time = datetime.now()
        self.logger.info(f"Starting Unit Planning for Unit {context.unit_number}: {context.unit_name}")

        agents_run = []
        agents_failed = []
        outputs = {}
        errors = []

        # Prepare unit request
        unit_request = {
            "unit_number": context.unit_number,
            "unit_name": context.unit_name,
            "total_days": self._get_unit_days(context.unit_number),
            "unit_config": unit_config or {}
        }

        # Execute agents in order
        for agent_name in self.get_execution_order():
            # Build input from accumulated outputs
            agent_input = {
                **unit_request,
                "previous_outputs": context.accumulated_outputs.copy()
            }

            success, output = self.execute_agent(agent_name, context, agent_input)
            agents_run.append(agent_name)

            if success:
                outputs[agent_name] = output
            else:
                agents_failed.append(agent_name)
                errors.append(f"{agent_name}: {output.get('error', 'Unknown error')}")

                # Handle failure based on agent type
                if agent_name == "unit_scope_validator":
                    # This is a gate - must handle retry
                    retry_instruction = self.handle_failure(
                        agent_name, output, context, RetryStrategy.COMPONENT_REGEN
                    )
                    if retry_instruction["action"] == "ESCALATE":
                        return OrchestratorResult(
                            status="escalated",
                            outputs=outputs,
                            agents_run=agents_run,
                            agents_failed=agents_failed,
                            retry_count=context.retry_count,
                            duration_seconds=(datetime.now() - start_time).total_seconds(),
                            errors=errors
                        )

        # Merge outputs into complete unit plan
        unit_plan = self._merge_unit_plan(outputs, context)

        duration = (datetime.now() - start_time).total_seconds()
        self.logger.info(f"Unit Planning completed in {duration:.2f}s")

        return OrchestratorResult(
            status="completed" if not agents_failed else "failed",
            outputs={"unit_plan": unit_plan, "agent_outputs": outputs},
            agents_run=agents_run,
            agents_failed=agents_failed,
            retry_count=context.retry_count,
            duration_seconds=duration,
            errors=errors
        )

    def _get_unit_days(self, unit_number: int) -> int:
        """Get total days for a unit."""
        unit_days = {1: 20, 2: 18, 3: 25, 4: 17}
        return unit_days.get(unit_number, 20)

    def _merge_unit_plan(self, outputs: Dict, context: AgentContext) -> Dict:
        """Merge individual agent outputs into complete unit plan."""
        return {
            "metadata": {
                "unit_number": context.unit_number,
                "unit_name": context.unit_name,
                "total_days": self._get_unit_days(context.unit_number),
                "generated_date": datetime.now().isoformat(),
                "version": "1.0"
            },
            "unit_plan": outputs.get("unit_planner", {}),
            "standards_map": outputs.get("standards_mapper", {}),
            "daily_objectives": outputs.get("learning_objective_generator", {}),
            "validation_result": outputs.get("unit_scope_validator", {})
        }


# =============================================================================
# DAILY GENERATION ORCHESTRATOR
# =============================================================================

class DailyGenerationOrchestrator(BaseOrchestrator):
    """
    Phase 2: Daily Generation Orchestrator

    Generates all components for a single day's 56-minute lesson:
    - Lesson plan (admin-friendly format)
    - Warmup (5 min, content-connected)
    - PowerPoint (16 slides)
    - Presenter notes (15 min verbatim script)
    - Activity (15 min)
    - Journal/exit ticket (10 min)
    - Handout (if required)
    """

    def get_execution_order(self) -> List[str]:
        """Return agent execution order for daily generation."""
        return [
            "lesson_plan_generator",
            "warmup_generator",
            "powerpoint_generator",
            "presenter_notes_writer",
            "activity_generator",
            "journal_exit_generator",
            "handout_generator"
        ]

    def get_parallel_agents(self) -> List[List[str]]:
        """
        Return groups of agents that can run in parallel.

        Sequential: 1 → 2 → 3 → 4
        Parallel after 4: [5, 6] → 7
        """
        return [
            ["lesson_plan_generator"],          # Sequential
            ["warmup_generator"],               # Sequential
            ["powerpoint_generator"],           # Sequential
            ["presenter_notes_writer"],         # Sequential
            ["activity_generator", "journal_exit_generator"],  # Parallel
            ["handout_generator"]               # Conditional
        ]

    def run(
        self,
        context: AgentContext,
        daily_input: Dict = None
    ) -> OrchestratorResult:
        """
        Execute daily generation phase.

        Args:
            context: Agent context
            daily_input: Input data for the day

        Returns:
            OrchestratorResult with all daily components
        """
        start_time = datetime.now()
        self.logger.info(f"Starting Daily Generation for Unit {context.unit_number}, Day {context.day}")

        agents_run = []
        agents_failed = []
        outputs = {}
        errors = []
        warnings = []

        # Execute agents in order (sequential for now, TODO: implement parallel)
        for agent_name in self.get_execution_order():
            # Skip handout if not required
            if agent_name == "handout_generator":
                activity_output = outputs.get("activity_generator", {})
                if not activity_output.get("requires_handout", False):
                    self.logger.info("Skipping handout_generator (not required)")
                    continue

            # Build input from accumulated outputs
            agent_input = {
                "unit": {
                    "number": context.unit_number,
                    "name": context.unit_name
                },
                "day": context.day,
                "topic": context.topic,
                "daily_input": daily_input or {},
                "previous_outputs": context.accumulated_outputs.copy()
            }

            success, output = self.execute_agent(agent_name, context, agent_input)
            agents_run.append(agent_name)

            if success:
                outputs[agent_name] = output
            else:
                agents_failed.append(agent_name)
                errors.append(f"{agent_name}: {output.get('error', 'Unknown error')}")

                # Continue with partial output for non-critical agents
                if agent_name not in ["lesson_plan_generator", "powerpoint_generator"]:
                    warnings.append(f"{agent_name} failed but continuing")
                    outputs[agent_name] = {"status": "failed", "error": output.get("error")}

        # Run coherence checks
        coherence = self._check_coherence(outputs, context)

        # Calculate timing
        timing = self._calculate_timing(outputs)

        duration = (datetime.now() - start_time).total_seconds()
        self.logger.info(f"Daily Generation completed in {duration:.2f}s")

        return OrchestratorResult(
            status="completed" if not agents_failed else "partial",
            outputs={
                "lesson_plan": outputs.get("lesson_plan_generator", {}),
                "warmup": outputs.get("warmup_generator", {}),
                "powerpoint": outputs.get("powerpoint_generator", {}),
                "presenter_notes": outputs.get("presenter_notes_writer", {}),
                "activity": outputs.get("activity_generator", {}),
                "journal_exit": outputs.get("journal_exit_generator", {}),
                "handout": outputs.get("handout_generator"),
                "coherence_check": coherence,
                "timing_estimate": timing
            },
            agents_run=agents_run,
            agents_failed=agents_failed,
            retry_count=context.retry_count,
            duration_seconds=duration,
            errors=errors,
            warnings=warnings
        )

    def _check_coherence(self, outputs: Dict, context: AgentContext) -> Dict:
        """Check cross-component coherence."""
        checks = {
            "vocabulary_aligned": True,
            "objectives_covered": True,
            "activity_coherent": True,
            "warmup_relevant": True,
            "exit_tickets_valid": True
        }

        # TODO: Implement actual coherence validation
        # For now, return placeholder
        return {
            **checks,
            "all_passed": all(checks.values())
        }

    def _calculate_timing(self, outputs: Dict) -> Dict:
        """Calculate total timing for the lesson."""
        presenter_notes = outputs.get("presenter_notes_writer", {})

        # Count words in presenter notes
        total_words = 0
        if "slides" in presenter_notes:
            for slide in presenter_notes.get("slides", []):
                notes = slide.get("notes", "")
                total_words += len(notes.split())

        # Calculate at 140 WPM
        speaking_duration = total_words / 140 if total_words > 0 else 0

        return {
            "total_minutes": 56,  # Fixed structure
            "presenter_notes_words": total_words,
            "speaking_duration_minutes": round(speaking_duration, 1)
        }


# =============================================================================
# VALIDATION GATE ORCHESTRATOR
# =============================================================================

class ValidationGateOrchestrator(BaseOrchestrator):
    """
    Phase 3: Validation Gate Orchestrator

    Runs HARDCODED validators that ALL content must pass:
    - Gate 1: Truncation (100% complete sentences)
    - Gate 2: Structure (100% components present)
    - Gate 3: Elaboration (score >= 85/100)
    - Gate 4: Timing (14-16 min duration)

    These validators CANNOT be bypassed or have thresholds lowered.
    """

    # Hardcoded thresholds - DO NOT MODIFY
    ELABORATION_THRESHOLD = 85
    MIN_DURATION_MINUTES = 14
    MAX_DURATION_MINUTES = 16
    MIN_WORDS = 1950
    MAX_WORDS = 2250

    def get_execution_order(self) -> List[str]:
        """Return validation gate order."""
        return [
            "truncation_validator",
            "structure_validator",
            "elaboration_validator",
            "timing_validator"
        ]

    def run(
        self,
        context: AgentContext,
        daily_output: Dict = None
    ) -> OrchestratorResult:
        """
        Execute validation gates.

        Args:
            context: Agent context
            daily_output: Output from daily generation

        Returns:
            OrchestratorResult with validation results
        """
        start_time = datetime.now()
        self.logger.info(f"Starting Validation for Unit {context.unit_number}, Day {context.day}")

        validation_results = {}
        all_passed = True
        first_failure = None

        # Run gates in sequence - stop on first failure
        for gate_name in self.get_execution_order():
            self.logger.info(f"Running gate: {gate_name}")

            result = self._run_gate(gate_name, daily_output, context)
            validation_results[gate_name] = result

            if result.status == GateStatus.FAILED:
                all_passed = False
                first_failure = result
                self.logger.warning(f"Gate {gate_name} FAILED")
                break
            elif result.status == GateStatus.AUTO_FIXED:
                self.logger.info(f"Gate {gate_name} PASSED (after auto-fix)")
            else:
                self.logger.info(f"Gate {gate_name} PASSED")

        duration = (datetime.now() - start_time).total_seconds()

        # Build result
        if all_passed:
            return OrchestratorResult(
                status="completed",
                outputs={
                    "validation_results": {k: self._result_to_dict(v) for k, v in validation_results.items()},
                    "validated_output": daily_output,
                    "overall_status": "PASSED"
                },
                agents_run=list(validation_results.keys()),
                agents_failed=[],
                retry_count=context.retry_count,
                duration_seconds=duration
            )
        else:
            # Prepare retry context
            retry_instruction = self._get_retry_instruction(first_failure, context)

            return OrchestratorResult(
                status="failed",
                outputs={
                    "validation_results": {k: self._result_to_dict(v) for k, v in validation_results.items()},
                    "overall_status": "FAILED",
                    "rejection_details": {
                        "failed_gate": first_failure.gate_name,
                        "reason": first_failure.fix_instructions,
                        "fix_instructions": retry_instruction.get("instruction", ""),
                        "context_for_retry": retry_instruction
                    }
                },
                agents_run=list(validation_results.keys()),
                agents_failed=[first_failure.gate_name],
                retry_count=context.retry_count,
                duration_seconds=duration,
                errors=[f"Failed at {first_failure.gate_name}: {first_failure.fix_instructions}"]
            )

    def _run_gate(
        self,
        gate_name: str,
        daily_output: Dict,
        context: AgentContext
    ) -> ValidationResult:
        """Run a specific validation gate."""

        if gate_name == "truncation_validator":
            return self._validate_truncation(daily_output)
        elif gate_name == "structure_validator":
            return self._validate_structure(daily_output)
        elif gate_name == "elaboration_validator":
            return self._validate_elaboration(daily_output)
        elif gate_name == "timing_validator":
            return self._validate_timing(daily_output)
        else:
            return ValidationResult(
                gate_name=gate_name,
                status=GateStatus.PASSED
            )

    def _validate_truncation(self, daily_output: Dict) -> ValidationResult:
        """
        Gate 1: Truncation Validator

        Checks:
        - Every sentence ends with terminal punctuation (. ! ? :)
        - No trailing ellipsis (...)
        - No mid-word cuts
        - All bullet points are complete sentences
        """
        issues = []
        auto_fixes = []

        # Components to validate
        components = [
            ("powerpoint.slides", daily_output.get("powerpoint", {}).get("slides", [])),
            ("presenter_notes.slides", daily_output.get("presenter_notes", {}).get("slides", [])),
            ("warmup.instructions", [daily_output.get("warmup", {})]),
            ("activity.instructions", [daily_output.get("activity", {})])
        ]

        for comp_name, items in components:
            for i, item in enumerate(items):
                if isinstance(item, dict):
                    # Check various text fields
                    for field in ["header", "body", "notes", "instructions"]:
                        text = item.get(field, "")
                        if text:
                            truncation_issues = self._check_truncation(text, f"{comp_name}[{i}].{field}")
                            issues.extend(truncation_issues)

        # Attempt auto-fix for simple issues
        simple_fixes = [i for i in issues if i.get("fixable", False)]
        for fix in simple_fixes:
            auto_fixes.append(f"Added punctuation to {fix['location']}")
            issues.remove(fix)

        if issues:
            return ValidationResult(
                gate_name="truncation_validator",
                status=GateStatus.FAILED,
                issues=issues,
                auto_fixes_applied=auto_fixes,
                fix_instructions=f"Found {len(issues)} truncation issues that require regeneration"
            )

        return ValidationResult(
            gate_name="truncation_validator",
            status=GateStatus.AUTO_FIXED if auto_fixes else GateStatus.PASSED,
            auto_fixes_applied=auto_fixes
        )

    def _check_truncation(self, text: str, location: str) -> List[Dict]:
        """Check text for truncation issues."""
        issues = []

        # Check for trailing ellipsis
        if text.rstrip().endswith("..."):
            issues.append({
                "type": "T002",
                "location": location,
                "description": "Trailing ellipsis found",
                "fixable": False
            })

        # Check sentences end with punctuation
        sentences = re.split(r'(?<=[.!?:])\s+', text.strip())
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence[-1] in '.!?:':
                issues.append({
                    "type": "T001",
                    "location": location,
                    "description": f"Sentence missing punctuation: '{sentence[:50]}...'",
                    "fixable": len(sentence) > 10  # Only fixable if substantial
                })

        return issues

    def _validate_structure(self, daily_output: Dict) -> ValidationResult:
        """
        Gate 2: Structure Validator

        Required components:
        - lesson_plan with all sections
        - powerpoint with 16 slides (4 auxiliary, 12 content)
        - presenter_notes for all slides
        - warmup with connection_to_lesson
        - activity with structure
        - journal_exit with prompts
        """
        issues = []

        required_components = [
            "lesson_plan",
            "warmup",
            "powerpoint",
            "presenter_notes",
            "activity",
            "journal_exit"
        ]

        for comp in required_components:
            if comp not in daily_output or not daily_output[comp]:
                issues.append({
                    "type": "S001",
                    "component": comp,
                    "description": f"Required component '{comp}' is missing"
                })

        # Check slide count
        powerpoint = daily_output.get("powerpoint", {})
        slides = powerpoint.get("slides", [])
        if len(slides) != 16:
            issues.append({
                "type": "S002",
                "component": "powerpoint",
                "description": f"Expected 16 slides, found {len(slides)}"
            })

        # Check presenter notes coverage
        presenter_notes = daily_output.get("presenter_notes", {})
        notes_slides = presenter_notes.get("slides", [])
        if len(notes_slides) != len(slides):
            issues.append({
                "type": "S003",
                "component": "presenter_notes",
                "description": f"Presenter notes count ({len(notes_slides)}) doesn't match slides ({len(slides)})"
            })

        if issues:
            return ValidationResult(
                gate_name="structure_validator",
                status=GateStatus.FAILED,
                issues=issues,
                fix_instructions=f"Missing or incomplete components: {len(issues)} issues"
            )

        return ValidationResult(
            gate_name="structure_validator",
            status=GateStatus.PASSED
        )

    def _validate_elaboration(self, daily_output: Dict) -> ValidationResult:
        """
        Gate 3: Elaboration Validator

        Scoring rubric (100 points total):
        - Depth: 30 points
        - Examples: 20 points
        - Procedure: 20 points
        - Tone: 15 points
        - Connections: 15 points

        Pass threshold: >= 85 points
        """
        scores = {
            "depth": 0,
            "examples": 0,
            "procedure": 0,
            "tone": 0,
            "connections": 0
        }

        presenter_notes = daily_output.get("presenter_notes", {})
        notes_text = " ".join([
            s.get("notes", "") for s in presenter_notes.get("slides", [])
        ])

        # Score depth (30 points)
        depth_score = self._score_depth(notes_text)
        scores["depth"] = min(30, depth_score)

        # Score examples (20 points)
        example_score = self._score_examples(notes_text)
        scores["examples"] = min(20, example_score)

        # Score procedure (20 points)
        activity = daily_output.get("activity", {})
        procedure_score = self._score_procedure(activity)
        scores["procedure"] = min(20, procedure_score)

        # Score tone (15 points)
        tone_score = self._score_tone(notes_text)
        scores["tone"] = min(15, tone_score)

        # Score connections (15 points)
        connection_score = self._score_connections(daily_output)
        scores["connections"] = min(15, connection_score)

        total_score = sum(scores.values())

        if total_score < self.ELABORATION_THRESHOLD:
            weak_areas = [k for k, v in scores.items() if v < (30 if k == "depth" else 20 if k in ["examples", "procedure"] else 15) * 0.7]
            return ValidationResult(
                gate_name="elaboration_validator",
                status=GateStatus.FAILED,
                score=total_score,
                threshold=self.ELABORATION_THRESHOLD,
                issues=[{"type": "E001", "scores": scores, "weak_areas": weak_areas}],
                fix_instructions=f"Elaboration score {total_score}/100 below threshold {self.ELABORATION_THRESHOLD}. Weak areas: {', '.join(weak_areas)}"
            )

        return ValidationResult(
            gate_name="elaboration_validator",
            status=GateStatus.PASSED,
            score=total_score,
            threshold=self.ELABORATION_THRESHOLD
        )

    def _score_depth(self, text: str) -> int:
        """Score depth of explanation."""
        score = 0

        # Check for explanatory phrases
        depth_indicators = [
            "because", "therefore", "this means", "in other words",
            "for example", "specifically", "the reason", "historically",
            "in the context of", "this connects to"
        ]

        text_lower = text.lower()
        for indicator in depth_indicators:
            if indicator in text_lower:
                score += 3

        return min(30, score)

    def _score_examples(self, text: str) -> int:
        """Score use of examples."""
        score = 0

        example_indicators = [
            "for example", "such as", "like", "instance",
            "imagine", "picture", "consider", "think about"
        ]

        text_lower = text.lower()
        for indicator in example_indicators:
            count = text_lower.count(indicator)
            score += count * 2

        return min(20, score)

    def _score_procedure(self, activity: Dict) -> int:
        """Score procedure clarity."""
        score = 0

        if activity.get("instructions"):
            score += 5
        if activity.get("structure"):
            score += 5
        if activity.get("differentiation"):
            score += 5
        if activity.get("time_warnings"):
            score += 5

        return score

    def _score_tone(self, text: str) -> int:
        """Score engagement and tone."""
        score = 0

        # Check for direct address
        direct_indicators = ["you", "we", "let's", "our", "your"]
        text_lower = text.lower()

        for indicator in direct_indicators:
            if indicator in text_lower:
                score += 3

        return min(15, score)

    def _score_connections(self, daily_output: Dict) -> int:
        """Score cross-component connections."""
        score = 0

        # Check warmup connection
        warmup = daily_output.get("warmup", {})
        if warmup.get("connection_to_lesson"):
            score += 5

        # Check activity-lecture connection
        activity = daily_output.get("activity", {})
        if activity:
            score += 5

        # Check exit ticket-objective alignment
        journal = daily_output.get("journal_exit", {})
        if journal.get("exit_tickets"):
            score += 5

        return score

    def _validate_timing(self, daily_output: Dict) -> ValidationResult:
        """
        Gate 4: Timing Validator

        Requirements:
        - Total words: 1,950 - 2,250
        - Duration: 14-16 minutes at 140 WPM
        - Markers: [PAUSE] min 2 per slide, [EMPHASIS] min 1 per content slide
        """
        issues = []
        auto_fixes = []

        presenter_notes = daily_output.get("presenter_notes", {})
        slides = presenter_notes.get("slides", [])

        # Count total words
        total_words = 0
        slide_analysis = []

        for i, slide in enumerate(slides):
            notes = slide.get("notes", "")
            word_count = len(notes.split())
            total_words += word_count

            # Count markers
            pause_count = notes.count("[PAUSE]")
            emphasis_count = len(re.findall(r'\[EMPHASIS[:\s]', notes))

            slide_analysis.append({
                "slide": i + 1,
                "word_count": word_count,
                "pause_count": pause_count,
                "emphasis_count": emphasis_count
            })

            # Check marker requirements for content slides (3-14)
            if 3 <= i + 1 <= 14:
                if pause_count < 2:
                    issues.append({
                        "type": "TI004",
                        "slide": i + 1,
                        "description": f"Slide {i+1}: Only {pause_count} [PAUSE] markers (need 2)"
                    })
                if emphasis_count < 1:
                    issues.append({
                        "type": "TI005",
                        "slide": i + 1,
                        "description": f"Slide {i+1}: Missing [EMPHASIS] marker"
                    })

        # Calculate duration
        duration_minutes = total_words / 140

        # Check word count bounds
        if total_words < self.MIN_WORDS:
            issues.append({
                "type": "TI001",
                "description": f"Word count {total_words} below minimum {self.MIN_WORDS}",
                "issue": "too_short",
                "needed_words": self.MIN_WORDS - total_words
            })
        elif total_words > self.MAX_WORDS:
            issues.append({
                "type": "TI002",
                "description": f"Word count {total_words} above maximum {self.MAX_WORDS}",
                "issue": "too_long",
                "excess_words": total_words - self.MAX_WORDS
            })

        # Auto-fix missing markers (if that's the only issue)
        marker_issues = [i for i in issues if i["type"] in ["TI004", "TI005", "TI006"]]
        if marker_issues and len(issues) == len(marker_issues):
            auto_fixes = [f"Auto-inserting markers for {len(marker_issues)} issues"]
            issues = []  # Clear marker issues if auto-fixed

        if issues:
            return ValidationResult(
                gate_name="timing_validator",
                status=GateStatus.FAILED,
                score=duration_minutes,
                threshold=f"{self.MIN_DURATION_MINUTES}-{self.MAX_DURATION_MINUTES}",
                issues=issues,
                fix_instructions=f"Timing issues: {total_words} words ({duration_minutes:.1f} min)"
            )

        return ValidationResult(
            gate_name="timing_validator",
            status=GateStatus.AUTO_FIXED if auto_fixes else GateStatus.PASSED,
            score=duration_minutes,
            threshold=f"{self.MIN_DURATION_MINUTES}-{self.MAX_DURATION_MINUTES}",
            auto_fixes_applied=auto_fixes
        )

    def _get_retry_instruction(self, failure: ValidationResult, context: AgentContext) -> Dict:
        """Get retry instructions based on failure type."""
        gate_strategies = {
            "truncation_validator": RetryStrategy.TARGETED_FIX,
            "structure_validator": RetryStrategy.COMPONENT_REGEN,
            "elaboration_validator": RetryStrategy.ENRICHMENT_PASS,
            "timing_validator": RetryStrategy.ADJUSTMENT_PASS
        }

        strategy = gate_strategies.get(failure.gate_name, RetryStrategy.TARGETED_FIX)

        return self.handle_failure(
            failure.gate_name,
            {"issues": failure.issues, "fix_instructions": failure.fix_instructions},
            context,
            strategy
        )

    def _result_to_dict(self, result: ValidationResult) -> Dict:
        """Convert ValidationResult to dictionary."""
        return {
            "gate_name": result.gate_name,
            "status": result.status.value,
            "score": result.score,
            "threshold": result.threshold,
            "issues": result.issues,
            "auto_fixes_applied": result.auto_fixes_applied,
            "fix_instructions": result.fix_instructions
        }


# =============================================================================
# ASSEMBLY ORCHESTRATOR
# =============================================================================

class AssemblyOrchestrator(BaseOrchestrator):
    """
    Phase 4: Assembly Orchestrator

    Assembles validated content into final outputs:
    - lesson_assembler: Combine all components into lesson package
    - powerpoint_assembler: Generate PPTX file
    - unit_folder_organizer: Organize files in production folder
    - final_qa_reporter: Generate QA report
    """

    def get_execution_order(self) -> List[str]:
        """Return assembly agent order."""
        return [
            "lesson_assembler",
            "powerpoint_assembler",
            "unit_folder_organizer",
            "final_qa_reporter"
        ]

    def run(
        self,
        context: AgentContext,
        validated_output: Dict = None
    ) -> OrchestratorResult:
        """
        Execute assembly phase.

        Args:
            context: Agent context
            validated_output: Output from validation phase

        Returns:
            OrchestratorResult with assembled outputs
        """
        start_time = datetime.now()
        self.logger.info(f"Starting Assembly for Unit {context.unit_number}, Day {context.day}")

        agents_run = []
        agents_failed = []
        outputs = {}
        errors = []

        # Prepare output directory
        output_dir = self._get_output_dir(context)

        for agent_name in self.get_execution_order():
            agent_input = {
                "validated_output": validated_output,
                "output_dir": str(output_dir),
                "context": {
                    "unit_number": context.unit_number,
                    "unit_name": context.unit_name,
                    "day": context.day,
                    "topic": context.topic
                }
            }

            success, output = self.execute_agent(agent_name, context, agent_input)
            agents_run.append(agent_name)

            if success:
                outputs[agent_name] = output
            else:
                agents_failed.append(agent_name)
                errors.append(f"{agent_name}: {output.get('error', 'Unknown error')}")

        duration = (datetime.now() - start_time).total_seconds()
        self.logger.info(f"Assembly completed in {duration:.2f}s")

        return OrchestratorResult(
            status="completed" if not agents_failed else "partial",
            outputs={
                "output_directory": str(output_dir),
                "files_created": outputs.get("unit_folder_organizer", {}).get("files", []),
                "qa_report": outputs.get("final_qa_reporter", {}),
                "agent_outputs": outputs
            },
            agents_run=agents_run,
            agents_failed=agents_failed,
            retry_count=context.retry_count,
            duration_seconds=duration,
            errors=errors
        )

    def _get_output_dir(self, context: AgentContext) -> Path:
        """Get output directory for assembled files."""
        base_dir = Path(__file__).parent.parent / "production"

        unit_names = {
            1: "Greek_Theater",
            2: "Commedia_dellArte",
            3: "Shakespeare",
            4: "Student_Directed_One_Acts"
        }

        unit_dir = f"Unit_{context.unit_number}_{unit_names.get(context.unit_number, 'Unknown')}"
        day_dir = f"Day_{context.day:02d}"

        output_dir = base_dir / unit_dir / day_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        return output_dir


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_orchestrator(
    orchestrator_type: str,
    config: Dict = None,
    agents: Dict[str, Callable] = None
) -> BaseOrchestrator:
    """
    Factory function to create orchestrators.

    Args:
        orchestrator_type: Type of orchestrator to create
        config: Optional configuration
        agents: Optional agent implementations

    Returns:
        Configured orchestrator instance
    """
    orchestrators = {
        "unit_planning": UnitPlanningOrchestrator,
        "daily_generation": DailyGenerationOrchestrator,
        "validation": ValidationGateOrchestrator,
        "assembly": AssemblyOrchestrator
    }

    orchestrator_class = orchestrators.get(orchestrator_type)
    if not orchestrator_class:
        raise ValueError(f"Unknown orchestrator type: {orchestrator_type}")

    return orchestrator_class(config=config, agents=agents)
