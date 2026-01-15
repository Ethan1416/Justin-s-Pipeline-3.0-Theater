#!/usr/bin/env python3
"""
Component Orchestrators for Theater Pipeline
=============================================

Individual orchestrators for each component of the theater pipeline
unit generation. These orchestrators manage specific aspects of
lesson generation with integrated instructional frameworks.

Orchestrators:
1. LessonGenerationOrchestrator - Generates complete lessons with all frameworks
2. ScaffoldingOrchestrator - Manages scaffolding generation and validation
3. FormativeAssessmentOrchestrator - Manages formative check generation
4. CognitiveFrameworkOrchestrator - Integrates Bloom's and Webb's DOK
5. ReadingActivityOrchestrator - Manages reading activity generation
6. LectureFrontloadOrchestrator - Ensures lectures frontload activities
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Import enforcement skills
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from skills.enforcement.scaffolding_generator import (
    ScaffoldingPlan, generate_scaffolding_plan, validate_scaffolding_plan,
    scaffolding_plan_to_dict, MIN_SCAFFOLDS_PER_LESSON, MAX_SCAFFOLDS_PER_LESSON
)
from skills.enforcement.formative_activities_generator import (
    FormativeAssessmentPlan, generate_formative_plan, validate_formative_plan,
    formative_plan_to_dict, MIN_FORMATIVE_CHECKS_PER_LESSON
)
from skills.enforcement.blooms_taxonomy_integrator import (
    BloomIntegrationPlan, BloomLevel, generate_bloom_integration_plan,
    validate_bloom_integration, bloom_plan_to_dict, MIN_BLOOM_LEVELS_PER_LESSON
)
from skills.enforcement.webbs_dok_integrator import (
    DOKIntegrationPlan, DOKLevel, generate_dok_integration_plan,
    validate_dok_integration, dok_plan_to_dict, MIN_DOK_LEVELS_PER_LESSON
)
from skills.enforcement.instruction_integrator import (
    IntegratedLesson, generate_integrated_lesson, validate_integrated_lesson,
    integrated_lesson_to_dict, generate_romeo_juliet_unit_plan,
    MIN_LECTURE_DURATION, MAX_LECTURE_DURATION
)
from skills.enforcement.agenda_slide_generator import (
    AgendaSlide, generate_agenda_slide, generate_agenda_slide_visual,
    validate_agenda_slide, has_valid_agenda, get_agenda_issues,
    agenda_to_dict, agenda_to_slide_content,
    CLASS_PERIODS, STANDARD_COMPONENTS, MAX_OBJECTIVES, MIN_OBJECTIVES
)
from skills.enforcement.agenda_slide_validator import (
    validate_agenda_structure, is_valid_agenda, get_validation_issues,
    get_validation_score, generate_validation_report as generate_agenda_report,
    VALIDATION_RULES as AGENDA_VALIDATION_RULES
)

logger = logging.getLogger(__name__)


# =============================================================================
# ENUMS AND DATA CLASSES
# =============================================================================

class ComponentStatus(Enum):
    """Status of component generation."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VALIDATION_FAILED = "validation_failed"


@dataclass
class ComponentResult:
    """Result from a component orchestrator."""
    component_name: str
    status: ComponentStatus
    output: Dict[str, Any]
    validation_result: Dict[str, Any]
    duration_seconds: float
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class LessonContext:
    """Context for lesson generation."""
    unit_number: int
    unit_name: str
    day: int
    topic: str
    learning_objectives: List[str]
    text_reference: str = ""
    activity_description: str = ""
    lecture_duration_minutes: int = 15
    include_reading: bool = True


# =============================================================================
# BASE COMPONENT ORCHESTRATOR
# =============================================================================

class BaseComponentOrchestrator(ABC):
    """Base class for component orchestrators."""

    MAX_RETRIES = 2

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def generate(self, context: LessonContext) -> ComponentResult:
        """Generate the component output."""
        pass

    @abstractmethod
    def validate(self, output: Dict) -> Dict[str, Any]:
        """Validate the generated output."""
        pass

    def run_with_retry(self, context: LessonContext) -> ComponentResult:
        """Run generation with retry logic."""
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                result = self.generate(context)

                if result.status == ComponentStatus.COMPLETED:
                    return result

                if attempt < self.MAX_RETRIES:
                    self.logger.warning(f"Attempt {attempt + 1} failed, retrying...")

            except Exception as e:
                self.logger.error(f"Generation error: {str(e)}")
                if attempt == self.MAX_RETRIES:
                    return ComponentResult(
                        component_name=self.__class__.__name__,
                        status=ComponentStatus.FAILED,
                        output={},
                        validation_result={"valid": False, "errors": [str(e)]},
                        duration_seconds=0,
                        errors=[str(e)]
                    )

        return result


# =============================================================================
# SCAFFOLDING ORCHESTRATOR
# =============================================================================

class ScaffoldingOrchestrator(BaseComponentOrchestrator):
    """
    Orchestrator for scaffolding generation.

    Generates scaffolding plans that progress from high to low support
    following the gradual release model (I Do, We Do, You Do).
    """

    def generate(self, context: LessonContext) -> ComponentResult:
        """Generate scaffolding plan for the lesson."""
        start_time = datetime.now()
        self.logger.info(f"Generating scaffolding for: {context.topic}")

        try:
            # Determine content type from activity
            content_type = self._determine_content_type(context.activity_description)

            # Generate scaffolding plan
            plan = generate_scaffolding_plan(
                lesson_topic=context.topic,
                content_type=content_type,
                learning_objectives=context.learning_objectives,
                total_duration_minutes=context.lecture_duration_minutes + 15
            )

            # Validate the plan
            validation = validate_scaffolding_plan(plan)

            duration = (datetime.now() - start_time).total_seconds()

            if validation["valid"]:
                return ComponentResult(
                    component_name="scaffolding",
                    status=ComponentStatus.COMPLETED,
                    output=scaffolding_plan_to_dict(plan),
                    validation_result=validation,
                    duration_seconds=duration,
                    warnings=[w["message"] for w in validation.get("warnings", [])]
                )
            else:
                return ComponentResult(
                    component_name="scaffolding",
                    status=ComponentStatus.VALIDATION_FAILED,
                    output=scaffolding_plan_to_dict(plan),
                    validation_result=validation,
                    duration_seconds=duration,
                    errors=[i["message"] for i in validation.get("issues", [])]
                )

        except Exception as e:
            return ComponentResult(
                component_name="scaffolding",
                status=ComponentStatus.FAILED,
                output={},
                validation_result={"valid": False},
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                errors=[str(e)]
            )

    def validate(self, output: Dict) -> Dict[str, Any]:
        """Validate scaffolding output."""
        scaffolds = output.get("scaffolds", [])

        issues = []
        if len(scaffolds) < MIN_SCAFFOLDS_PER_LESSON:
            issues.append(f"Too few scaffolds: {len(scaffolds)}")
        if len(scaffolds) > MAX_SCAFFOLDS_PER_LESSON:
            issues.append(f"Too many scaffolds: {len(scaffolds)}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "scaffold_count": len(scaffolds)
        }

    def _determine_content_type(self, activity: str) -> str:
        """Determine content type from activity description."""
        activity_lower = activity.lower()
        if any(w in activity_lower for w in ["read", "text"]):
            return "reading"
        elif any(w in activity_lower for w in ["discuss", "debate"]):
            return "discussion"
        elif any(w in activity_lower for w in ["perform", "scene"]):
            return "performance"
        elif any(w in activity_lower for w in ["write", "compose"]):
            return "writing"
        return "analysis"


# =============================================================================
# FORMATIVE ASSESSMENT ORCHESTRATOR
# =============================================================================

class FormativeAssessmentOrchestrator(BaseComponentOrchestrator):
    """
    Orchestrator for formative assessment generation.

    Generates formative checks aligned to learning objectives
    with variety in assessment types.
    """

    def generate(self, context: LessonContext) -> ComponentResult:
        """Generate formative assessment plan for the lesson."""
        start_time = datetime.now()
        self.logger.info(f"Generating formatives for: {context.topic}")

        try:
            # Generate formative plan
            plan = generate_formative_plan(
                lesson_topic=context.topic,
                learning_objectives=context.learning_objectives,
                lecture_duration_minutes=context.lecture_duration_minutes
            )

            # Validate the plan
            validation = validate_formative_plan(plan)

            duration = (datetime.now() - start_time).total_seconds()

            status = ComponentStatus.COMPLETED if validation["valid"] else ComponentStatus.VALIDATION_FAILED

            return ComponentResult(
                component_name="formative_assessment",
                status=status,
                output=formative_plan_to_dict(plan),
                validation_result=validation,
                duration_seconds=duration,
                errors=[i["message"] for i in validation.get("issues", [])] if not validation["valid"] else [],
                warnings=[w["message"] for w in validation.get("warnings", [])]
            )

        except Exception as e:
            return ComponentResult(
                component_name="formative_assessment",
                status=ComponentStatus.FAILED,
                output={},
                validation_result={"valid": False},
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                errors=[str(e)]
            )

    def validate(self, output: Dict) -> Dict[str, Any]:
        """Validate formative assessment output."""
        formatives = output.get("formative_activities", [])

        issues = []
        if len(formatives) < MIN_FORMATIVE_CHECKS_PER_LESSON:
            issues.append(f"Too few formative checks: {len(formatives)}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "formative_count": len(formatives)
        }


# =============================================================================
# COGNITIVE FRAMEWORK ORCHESTRATOR
# =============================================================================

class CognitiveFrameworkOrchestrator(BaseComponentOrchestrator):
    """
    Orchestrator for Bloom's Taxonomy and Webb's DOK integration.

    Ensures lessons address multiple cognitive levels and
    appropriate depth of knowledge.
    """

    def generate(self, context: LessonContext) -> ComponentResult:
        """Generate cognitive framework integration."""
        start_time = datetime.now()
        self.logger.info(f"Generating cognitive frameworks for: {context.topic}")

        try:
            # Generate Bloom's integration
            blooms = generate_bloom_integration_plan(
                lesson_topic=context.topic,
                learning_objectives=context.learning_objectives
            )

            # Generate DOK integration
            activities = [{"description": context.activity_description, "duration_minutes": 15}]
            dok = generate_dok_integration_plan(
                lesson_topic=context.topic,
                activities=activities
            )

            # Validate both
            bloom_validation = validate_bloom_integration(blooms)
            dok_validation = validate_dok_integration(dok)

            combined_valid = bloom_validation["valid"] and dok_validation["valid"]

            duration = (datetime.now() - start_time).total_seconds()

            return ComponentResult(
                component_name="cognitive_frameworks",
                status=ComponentStatus.COMPLETED if combined_valid else ComponentStatus.VALIDATION_FAILED,
                output={
                    "blooms": bloom_plan_to_dict(blooms),
                    "dok": dok_plan_to_dict(dok)
                },
                validation_result={
                    "valid": combined_valid,
                    "blooms": bloom_validation,
                    "dok": dok_validation
                },
                duration_seconds=duration,
                errors=(
                    [i["message"] for i in bloom_validation.get("issues", [])] +
                    [i["message"] for i in dok_validation.get("issues", [])]
                ) if not combined_valid else [],
                warnings=(
                    [w["message"] for w in bloom_validation.get("warnings", [])] +
                    [w["message"] for w in dok_validation.get("warnings", [])]
                )
            )

        except Exception as e:
            return ComponentResult(
                component_name="cognitive_frameworks",
                status=ComponentStatus.FAILED,
                output={},
                validation_result={"valid": False},
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                errors=[str(e)]
            )

    def validate(self, output: Dict) -> Dict[str, Any]:
        """Validate cognitive framework output."""
        blooms = output.get("blooms", {})
        dok = output.get("dok", {})

        issues = []
        bloom_levels = len(blooms.get("level_coverage", []))
        dok_levels = len(dok.get("level_coverage", []))

        if bloom_levels < MIN_BLOOM_LEVELS_PER_LESSON:
            issues.append(f"Insufficient Bloom's levels: {bloom_levels}")
        if dok_levels < MIN_DOK_LEVELS_PER_LESSON:
            issues.append(f"Insufficient DOK levels: {dok_levels}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "bloom_levels": bloom_levels,
            "dok_levels": dok_levels
        }


# =============================================================================
# READING ACTIVITY ORCHESTRATOR
# =============================================================================

class ReadingActivityOrchestrator(BaseComponentOrchestrator):
    """
    Orchestrator for reading activity generation.

    Generates reading activities for text-based lessons,
    especially for Shakespeare unit.
    """

    def generate(self, context: LessonContext) -> ComponentResult:
        """Generate reading activity for the lesson."""
        start_time = datetime.now()
        self.logger.info(f"Generating reading activity for: {context.topic}")

        try:
            if not context.include_reading or not context.text_reference:
                return ComponentResult(
                    component_name="reading_activity",
                    status=ComponentStatus.COMPLETED,
                    output={"included": False, "reason": "No reading required"},
                    validation_result={"valid": True},
                    duration_seconds=(datetime.now() - start_time).total_seconds()
                )

            # Generate reading activity
            from skills.enforcement.instruction_integrator import generate_reading_activity

            reading = generate_reading_activity(
                text_reference=context.text_reference,
                lesson_topic=context.topic,
                duration_minutes=10
            )

            output = {
                "included": True,
                "type": reading.reading_type,
                "text": reading.text_reference,
                "duration_minutes": reading.duration_minutes,
                "purpose": reading.purpose,
                "supports": reading.supports,
                "follow_up": reading.follow_up
            }

            duration = (datetime.now() - start_time).total_seconds()

            return ComponentResult(
                component_name="reading_activity",
                status=ComponentStatus.COMPLETED,
                output=output,
                validation_result={"valid": True, "has_reading": True},
                duration_seconds=duration
            )

        except Exception as e:
            return ComponentResult(
                component_name="reading_activity",
                status=ComponentStatus.FAILED,
                output={},
                validation_result={"valid": False},
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                errors=[str(e)]
            )

    def validate(self, output: Dict) -> Dict[str, Any]:
        """Validate reading activity output."""
        if not output.get("included", False):
            return {"valid": True, "has_reading": False}

        issues = []
        if not output.get("text"):
            issues.append("Missing text reference")
        if not output.get("supports"):
            issues.append("Missing reading supports")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "has_reading": True
        }


# =============================================================================
# LECTURE FRONTLOAD ORCHESTRATOR
# =============================================================================

class LectureFrontloadOrchestrator(BaseComponentOrchestrator):
    """
    Orchestrator for lecture frontloading.

    Ensures lectures properly frontload concepts before activities,
    with appropriate duration (5-20 minutes).
    """

    def generate(self, context: LessonContext) -> ComponentResult:
        """Generate lecture frontload component."""
        start_time = datetime.now()
        self.logger.info(f"Generating lecture frontload for: {context.topic}")

        try:
            from skills.enforcement.instruction_integrator import generate_lecture_component

            # Validate and clamp duration
            duration = max(MIN_LECTURE_DURATION, min(MAX_LECTURE_DURATION, context.lecture_duration_minutes))

            # Generate lecture component
            lecture = generate_lecture_component(
                topic=context.topic,
                duration=duration,
                activity_to_frontload=context.activity_description,
                objectives=context.learning_objectives
            )

            output = {
                "topic": lecture.topic,
                "duration_minutes": lecture.duration_minutes,
                "key_concepts": lecture.key_concepts,
                "vocabulary_frontload": lecture.vocabulary_frontload,
                "connects_to_activity": lecture.connects_to_activity,
                "frontloading_strategy": lecture.frontloading_strategy
            }

            # Validate
            validation = self.validate(output)

            return ComponentResult(
                component_name="lecture_frontload",
                status=ComponentStatus.COMPLETED if validation["valid"] else ComponentStatus.VALIDATION_FAILED,
                output=output,
                validation_result=validation,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                errors=[i for i in validation.get("issues", [])] if not validation["valid"] else []
            )

        except Exception as e:
            return ComponentResult(
                component_name="lecture_frontload",
                status=ComponentStatus.FAILED,
                output={},
                validation_result={"valid": False},
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                errors=[str(e)]
            )

    def validate(self, output: Dict) -> Dict[str, Any]:
        """Validate lecture frontload output."""
        issues = []

        duration = output.get("duration_minutes", 0)
        if duration < MIN_LECTURE_DURATION:
            issues.append(f"Lecture too short: {duration} min (minimum: {MIN_LECTURE_DURATION})")
        if duration > MAX_LECTURE_DURATION:
            issues.append(f"Lecture too long: {duration} min (maximum: {MAX_LECTURE_DURATION})")

        if not output.get("frontloading_strategy"):
            issues.append("Missing frontloading strategy")

        if not output.get("connects_to_activity"):
            issues.append("Lecture not connected to activity")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "duration_minutes": duration,
            "has_frontload": bool(output.get("frontloading_strategy"))
        }


# =============================================================================
# LESSON GENERATION ORCHESTRATOR
# =============================================================================

class LessonGenerationOrchestrator(BaseComponentOrchestrator):
    """
    Master orchestrator for complete lesson generation.

    Coordinates all component orchestrators to generate
    a fully integrated lesson.
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.scaffolding_orch = ScaffoldingOrchestrator(config)
        self.formative_orch = FormativeAssessmentOrchestrator(config)
        self.cognitive_orch = CognitiveFrameworkOrchestrator(config)
        self.reading_orch = ReadingActivityOrchestrator(config)
        self.frontload_orch = LectureFrontloadOrchestrator(config)

    def generate(self, context: LessonContext) -> ComponentResult:
        """Generate complete integrated lesson."""
        start_time = datetime.now()
        self.logger.info(f"Generating integrated lesson for: {context.topic}")

        component_results = {}
        all_valid = True

        # Run all component orchestrators
        components = [
            ("scaffolding", self.scaffolding_orch),
            ("formative", self.formative_orch),
            ("cognitive", self.cognitive_orch),
            ("reading", self.reading_orch),
            ("frontload", self.frontload_orch)
        ]

        for name, orchestrator in components:
            result = orchestrator.run_with_retry(context)
            component_results[name] = result
            if result.status not in [ComponentStatus.COMPLETED]:
                all_valid = False

        # Generate full integrated lesson
        try:
            integrated = generate_integrated_lesson(
                lesson_topic=context.topic,
                unit_name=context.unit_name,
                day_number=context.day,
                learning_objectives=context.learning_objectives,
                activity_description=context.activity_description,
                lecture_duration_minutes=context.lecture_duration_minutes,
                include_reading=context.include_reading,
                text_reference=context.text_reference
            )

            integrated_validation = validate_integrated_lesson(integrated)
            all_valid = all_valid and integrated_validation["valid"]

            output = {
                "integrated_lesson": integrated_lesson_to_dict(integrated),
                "components": {
                    name: {
                        "status": result.status.value,
                        "output": result.output,
                        "validation": result.validation_result
                    }
                    for name, result in component_results.items()
                }
            }

            duration = (datetime.now() - start_time).total_seconds()

            return ComponentResult(
                component_name="lesson_generation",
                status=ComponentStatus.COMPLETED if all_valid else ComponentStatus.VALIDATION_FAILED,
                output=output,
                validation_result={
                    "valid": all_valid,
                    "integrated": integrated_validation,
                    "components": {
                        name: result.validation_result
                        for name, result in component_results.items()
                    }
                },
                duration_seconds=duration,
                errors=[e for r in component_results.values() for e in r.errors],
                warnings=[w for r in component_results.values() for w in r.warnings]
            )

        except Exception as e:
            return ComponentResult(
                component_name="lesson_generation",
                status=ComponentStatus.FAILED,
                output={"components": component_results},
                validation_result={"valid": False},
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                errors=[str(e)]
            )

    def validate(self, output: Dict) -> Dict[str, Any]:
        """Validate complete lesson output."""
        integrated = output.get("integrated_lesson", {})
        components = output.get("components", {})

        issues = []

        if not integrated.get("integration_valid"):
            issues.append("Integrated lesson validation failed")

        for name, comp in components.items():
            if comp.get("status") != "completed":
                issues.append(f"Component {name} not completed")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "component_count": len(components)
        }

    def generate_unit(
        self,
        unit_name: str,
        unit_number: int,
        days: int,
        base_topic: str,
        is_romeo_juliet: bool = False
    ) -> List[ComponentResult]:
        """Generate an entire unit of lessons."""
        results = []

        if is_romeo_juliet:
            # Use Romeo and Juliet specific plan
            lesson_plans = generate_romeo_juliet_unit_plan(start_day=1)

            for plan in lesson_plans[:days]:
                context = LessonContext(
                    unit_number=unit_number,
                    unit_name=unit_name,
                    day=plan["day"],
                    topic=plan["focus"],
                    learning_objectives=[
                        f"Analyze {plan['focus']} in Romeo and Juliet",
                        f"Apply understanding of {plan['focus']} to performance"
                    ],
                    text_reference=plan["text_reference"],
                    activity_description=plan["suggested_activity"],
                    lecture_duration_minutes=15,
                    include_reading=plan["reading_required"]
                )

                result = self.generate(context)
                results.append(result)
        else:
            # Generate generic unit lessons
            for day in range(1, days + 1):
                context = LessonContext(
                    unit_number=unit_number,
                    unit_name=unit_name,
                    day=day,
                    topic=f"{base_topic} - Day {day}",
                    learning_objectives=[f"Objective for day {day}"],
                    activity_description="Practice activity",
                    lecture_duration_minutes=15,
                    include_reading=False
                )

                result = self.generate(context)
                results.append(result)

        return results


# =============================================================================
# AGENDA ORCHESTRATOR (HARDCODED)
# =============================================================================

class AgendaOrchestrator(BaseComponentOrchestrator):
    """
    HARDCODED orchestrator for agenda slide generation.

    Ensures consistent agenda generation with:
    - Proper visual layout (Unit info, lesson title, components, objectives)
    - Validation of timing, objectives, and materials
    - Support for multiple class periods (standard, block, shortened, extended)

    This orchestrator CANNOT be bypassed during pipeline execution.
    """

    COMPONENT_NAME = "agenda"

    # HARDCODED validation rules
    RULES = {
        "R1": "Total duration must equal class period",
        "R2": "All 6 components required (agenda, warmup, lecture, activity, reflection, buffer)",
        "R3": "1-3 learning objectives required",
        "R4": "3-5 materials required",
        "R5": "Time markers must be sequential and non-overlapping",
        "R6": "Descriptions must be under 60 characters",
    }

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self.class_period = config.get("class_period", "standard") if config else "standard"

    def generate(self, context: LessonContext) -> ComponentResult:
        """
        Generate agenda slide content.

        Args:
            context: LessonContext with unit/day information

        Returns:
            ComponentResult with agenda slide data
        """
        import time
        start_time = time.time()
        errors = []
        warnings = []

        try:
            # Determine warmup and activity types based on context
            warmup_type = "physical" if "performance" in context.topic.lower() else "mental"
            activity_type = "scene_work" if context.include_reading else "group_discussion"

            # Generate agenda using HARDCODED skill
            agenda_slide = generate_agenda_slide(
                unit_number=context.unit_number,
                unit_name=context.unit_name,
                day_number=context.day,
                total_days=30,  # Default for theater units
                lesson_topic=context.topic,
                learning_objectives=context.learning_objectives,
                warmup_type=warmup_type,
                warmup_connection=f"Prepares students for {context.topic}",
                activity_type=activity_type,
                activity_topic=context.activity_description or context.topic,
                additional_materials=[],
                class_period=self.class_period,
            )

            # Generate visual representation
            agenda_visual = generate_agenda_slide_visual(agenda_slide)

            # Convert to output format
            output = {
                "agenda_data": agenda_to_dict(agenda_slide),
                "slide_content": agenda_to_slide_content(agenda_slide),
                "visual_markdown": agenda_visual.to_markdown(),
                "class_period": self.class_period,
                "total_duration": agenda_slide.total_duration,
            }

            # Validate
            validation_result = self.validate(output)

            duration = time.time() - start_time

            if validation_result["valid"]:
                status = ComponentStatus.COMPLETED
            else:
                status = ComponentStatus.VALIDATION_FAILED
                errors.extend(validation_result.get("issues", []))

            return ComponentResult(
                component_name=self.COMPONENT_NAME,
                status=status,
                output=output,
                validation_result=validation_result,
                duration_seconds=duration,
                errors=errors,
                warnings=warnings
            )

        except Exception as e:
            self.logger.error(f"Agenda generation failed: {str(e)}")
            return ComponentResult(
                component_name=self.COMPONENT_NAME,
                status=ComponentStatus.FAILED,
                output={},
                validation_result={"valid": False, "errors": [str(e)]},
                duration_seconds=time.time() - start_time,
                errors=[str(e)]
            )

    def validate(self, output: Dict) -> Dict[str, Any]:
        """
        Validate agenda output against HARDCODED rules.

        Args:
            output: Generated agenda output

        Returns:
            Validation result with valid flag and issues
        """
        agenda_data = output.get("agenda_data", {})

        # Use HARDCODED validator
        result = validate_agenda_structure(agenda_data)

        return {
            "valid": result.valid,
            "issues": result.issues,
            "warnings": result.warnings,
            "score": result.score,
            "rules_checked": list(self.RULES.keys()),
        }

    def generate_for_unit(
        self,
        unit_number: int,
        unit_name: str,
        days: int,
        topics: List[str],
        objectives_per_day: List[List[str]],
        class_period: str = "standard"
    ) -> List[ComponentResult]:
        """
        Generate agenda slides for an entire unit.

        Args:
            unit_number: Unit number (1-4)
            unit_name: Unit name
            days: Number of days in unit
            topics: List of topics per day
            objectives_per_day: List of objectives per day
            class_period: Class period type

        Returns:
            List of ComponentResult for each day
        """
        self.class_period = class_period
        results = []

        for day in range(1, days + 1):
            topic = topics[day - 1] if day <= len(topics) else f"Day {day}"
            objectives = objectives_per_day[day - 1] if day <= len(objectives_per_day) else [f"Objective for day {day}"]

            context = LessonContext(
                unit_number=unit_number,
                unit_name=unit_name,
                day=day,
                topic=topic,
                learning_objectives=objectives,
                activity_description=topic,
                lecture_duration_minutes=15,
                include_reading=True
            )

            result = self.generate(context)
            results.append(result)

        return results


# =============================================================================
# FACTORY FUNCTION
# =============================================================================

def create_component_orchestrator(
    component_type: str,
    config: Dict = None
) -> BaseComponentOrchestrator:
    """
    Factory function to create component orchestrators.

    Args:
        component_type: Type of orchestrator to create
        config: Optional configuration

    Returns:
        Configured component orchestrator instance
    """
    orchestrators = {
        "scaffolding": ScaffoldingOrchestrator,
        "formative": FormativeAssessmentOrchestrator,
        "cognitive": CognitiveFrameworkOrchestrator,
        "reading": ReadingActivityOrchestrator,
        "frontload": LectureFrontloadOrchestrator,
        "lesson": LessonGenerationOrchestrator,
        "agenda": AgendaOrchestrator,
    }

    orchestrator_class = orchestrators.get(component_type)
    if not orchestrator_class:
        raise ValueError(f"Unknown component type: {component_type}")

    return orchestrator_class(config=config)
