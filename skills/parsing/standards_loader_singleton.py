"""
Standards Loader Singleton - Pipeline-level caching for standards loading.

This module provides thread-safe singleton caching for standards parsing and validation,
eliminating redundant file I/O across multiple pipeline steps.

Architecture:
- Load Once: Standards loaded on first access
- Cache Always: All subsequent calls use cached data
- Validate Early: Pre-validation at pipeline init, not Step 5
- Thread-Safe: Uses lock for multi-threaded scenarios

Usage:
    from skills.parsing.standards_loader_singleton import (
        get_standards_loader,
        validate_standards_at_startup,
        get_cached_standards
    )

    # Pre-validate at pipeline init (Step 0)
    if not validate_standards_at_startup():
        raise RuntimeError("Standards validation failed")

    # Get cached standards anywhere in pipeline
    standards = get_cached_standards()

    # Or use the full singleton for more control
    loader = get_standards_loader()
    result = loader.apply_to_outline(outline)
"""

import threading
from typing import Dict, Optional, Any
from dataclasses import dataclass, field

from skills.parsing.standards_parser import StandardsParser, ParsedStandards
from skills.validation.standards_validator import (
    StandardsValidator,
    AllStandardsResult,
    EnhancedValidationResult
)


@dataclass
class StandardsLoaderState:
    """Internal state container for singleton."""
    initialized: bool = False
    parser: Optional[StandardsParser] = None
    validator: Optional[StandardsValidator] = None
    parsed_standards: Optional[ParsedStandards] = None
    validation_result: Optional[AllStandardsResult] = None
    is_valid: bool = False
    initialization_errors: list = field(default_factory=list)


class StandardsLoaderSingleton:
    """
    Thread-safe singleton for standards loading and caching.

    Provides pipeline-level caching of parsed standards and validation results,
    ensuring standards are loaded once and reused throughout the pipeline.

    Features:
    - Thread-safe initialization with double-checked locking
    - Lazy loading on first access
    - Pre-validation support for pipeline init
    - Reset capability for testing
    - Comprehensive error handling
    """

    _instance: Optional['StandardsLoaderSingleton'] = None
    _lock = threading.Lock()
    _state: StandardsLoaderState = None

    def __new__(cls):
        """Thread-safe singleton creation with double-checked locking."""
        if cls._instance is None:
            with cls._lock:
                # Double-check after acquiring lock
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._state = StandardsLoaderState()
                    cls._instance = instance
        return cls._instance

    def _initialize(self) -> None:
        """
        Initialize standards loading on first access.

        Performs:
        1. Creates StandardsParser instance
        2. Parses all standards files
        3. Creates StandardsValidator instance
        4. Validates all standards
        5. Sets validity flag
        """
        if self._state.initialized:
            return

        try:
            # Initialize parser and parse standards
            self._state.parser = StandardsParser()
            self._state.parsed_standards = self._state.parser.parse_all_standards()

            # Check parsing success
            if not self._state.parsed_standards.success:
                self._state.initialization_errors.extend(
                    self._state.parsed_standards.errors
                )

            # Initialize validator and validate standards
            self._state.validator = StandardsValidator()
            self._state.validation_result = self._state.validator.validate_all_standards()

            # Set overall validity
            self._state.is_valid = (
                self._state.parsed_standards.success and
                self._state.validation_result.is_valid
            )

            self._state.initialized = True

        except Exception as e:
            self._state.initialization_errors.append(f"Initialization error: {str(e)}")
            self._state.is_valid = False
            self._state.initialized = True  # Mark as initialized to prevent retry

    def _ensure_initialized(self) -> None:
        """Ensure singleton is initialized before use."""
        if not self._state.initialized:
            self._initialize()

    def get_standards(self) -> Optional[ParsedStandards]:
        """
        Get cached parsed standards.

        Returns:
            ParsedStandards object or None if initialization failed
        """
        self._ensure_initialized()
        return self._state.parsed_standards

    def get_validation_result(self) -> Optional[AllStandardsResult]:
        """
        Get cached validation result.

        Returns:
            AllStandardsResult object or None if initialization failed
        """
        self._ensure_initialized()
        return self._state.validation_result

    def is_standards_valid(self) -> bool:
        """
        Check if standards are valid.

        Returns:
            True if standards parsed and validated successfully
        """
        self._ensure_initialized()
        return self._state.is_valid

    def get_initialization_errors(self) -> list:
        """
        Get any errors that occurred during initialization.

        Returns:
            List of error messages
        """
        self._ensure_initialized()
        return self._state.initialization_errors.copy()

    def apply_to_outline(self, outline: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply cached standards to a Step 4 outline.

        Args:
            outline: Step 4 outline dictionary

        Returns:
            Step 5 output with standards applied
        """
        self._ensure_initialized()
        if self._state.parser is None:
            raise RuntimeError("Standards parser not initialized")
        return self._state.parser.apply_standards_to_outline(outline)

    def validate_step5_output(self, output: Dict[str, Any]) -> EnhancedValidationResult:
        """
        Validate a Step 5 output against schema and cross-checks.

        Args:
            output: Step 5 output dictionary

        Returns:
            EnhancedValidationResult with schema, delivery mode, and timing validation
        """
        self._ensure_initialized()
        if self._state.validator is None:
            raise RuntimeError("Standards validator not initialized")
        return self._state.validator.validate_step5_output(output)

    def get_validation_report(self) -> str:
        """
        Get formatted validation report.

        Returns:
            Human-readable validation report string
        """
        self._ensure_initialized()
        if self._state.validator is None or self._state.validation_result is None:
            return "Validation not available - initialization failed"
        return self._state.validator.format_report(self._state.validation_result)

    def get_parser(self) -> Optional[StandardsParser]:
        """
        Get the cached parser instance for direct access.

        Returns:
            StandardsParser instance or None
        """
        self._ensure_initialized()
        return self._state.parser

    def get_validator(self) -> Optional[StandardsValidator]:
        """
        Get the cached validator instance for direct access.

        Returns:
            StandardsValidator instance or None
        """
        self._ensure_initialized()
        return self._state.validator

    @classmethod
    def reset(cls) -> None:
        """
        Reset singleton state (for testing).

        Clears the singleton instance, allowing re-initialization.
        Thread-safe operation.
        """
        with cls._lock:
            if cls._instance is not None:
                cls._instance._state = StandardsLoaderState()
                cls._instance = None

    @classmethod
    def is_initialized(cls) -> bool:
        """
        Check if singleton has been initialized.

        Returns:
            True if singleton exists and is initialized
        """
        return cls._instance is not None and cls._instance._state.initialized


# =============================================================================
# Module-Level Convenience Functions
# =============================================================================

def get_standards_loader() -> StandardsLoaderSingleton:
    """
    Get the standards loader singleton instance.

    Returns:
        StandardsLoaderSingleton instance (creates if needed)
    """
    return StandardsLoaderSingleton()


def get_cached_standards() -> Optional[ParsedStandards]:
    """
    Get cached parsed standards.

    Convenience function for quick access to parsed standards.

    Returns:
        ParsedStandards object or None if not available
    """
    return get_standards_loader().get_standards()


def validate_standards_at_startup() -> bool:
    """
    Validate standards at pipeline startup.

    Call this at pipeline initialization (Step 0) to:
    1. Load and cache all standards
    2. Validate standards completeness
    3. Report any errors before processing begins

    Returns:
        True if all standards are valid, False otherwise
    """
    loader = get_standards_loader()

    if not loader.is_standards_valid():
        # Print validation report for debugging
        print("=" * 60)
        print("STANDARDS VALIDATION FAILED AT STARTUP")
        print("=" * 60)

        errors = loader.get_initialization_errors()
        if errors:
            print("\nInitialization Errors:")
            for error in errors:
                print(f"  - {error}")

        result = loader.get_validation_result()
        if result:
            print(f"\nOverall Score: {result.overall_score:.1f}%")
            print(f"Valid: {result.is_valid}")

            for file_key, file_result in result.results.items():
                if not file_result.is_valid:
                    print(f"\n{file_key}:")
                    print(f"  Score: {file_result.completeness_score:.1f}%")
                    if file_result.missing_sections:
                        print(f"  Missing: {', '.join(file_result.missing_sections)}")
                    if file_result.issues:
                        print(f"  Issues: {', '.join(file_result.issues)}")

        print("=" * 60)
        return False

    return True


def get_standards_status() -> Dict[str, Any]:
    """
    Get current standards loading status.

    Returns:
        Dictionary with initialization and validation status
    """
    loader = get_standards_loader()

    return {
        "initialized": StandardsLoaderSingleton.is_initialized(),
        "is_valid": loader.is_standards_valid(),
        "errors": loader.get_initialization_errors(),
        "parsed_success": (
            loader.get_standards().success
            if loader.get_standards() else False
        ),
        "validation_score": (
            loader.get_validation_result().overall_score
            if loader.get_validation_result() else 0.0
        )
    }


def reset_standards_cache() -> None:
    """
    Reset the standards cache (for testing).

    Clears all cached standards and validation results,
    forcing re-initialization on next access.
    """
    StandardsLoaderSingleton.reset()


# =============================================================================
# Pre-validation Hook for Pipeline Integration
# =============================================================================

def prevalidate_pipeline() -> Dict[str, Any]:
    """
    Pre-validate all standards before pipeline execution.

    This function should be called at the very start of the pipeline
    (before Step 1) to ensure all standards are valid and cached.

    Returns:
        Dictionary with validation status and details:
        {
            "status": "PASS" | "FAIL",
            "standards_valid": bool,
            "cached": bool,
            "errors": list,
            "warnings": list,
            "report": str
        }
    """
    result = {
        "status": "UNKNOWN",
        "standards_valid": False,
        "cached": False,
        "errors": [],
        "warnings": [],
        "report": ""
    }

    try:
        # Force initialization and validation
        loader = get_standards_loader()

        # Get validation status
        result["standards_valid"] = loader.is_standards_valid()
        result["cached"] = StandardsLoaderSingleton.is_initialized()
        result["errors"] = loader.get_initialization_errors()

        # Get parsed standards warnings
        standards = loader.get_standards()
        if standards:
            result["warnings"].extend(standards.warnings)

        # Generate report
        result["report"] = loader.get_validation_report()

        # Set final status
        result["status"] = "PASS" if result["standards_valid"] else "FAIL"

    except Exception as e:
        result["status"] = "ERROR"
        result["errors"].append(f"Pre-validation error: {str(e)}")

    return result
