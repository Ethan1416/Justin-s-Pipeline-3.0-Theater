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
        "lesson": LessonGenerationOrchestrator
    }

    orchestrator_class = orchestrators.get(component_type)
    if not orchestrator_class:
        raise ValueError(f"Unknown component type: {component_type}")

    return orchestrator_class(config=config)
