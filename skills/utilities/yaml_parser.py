"""
YAML Parser - Parse YAML configuration files for NCLEX pipeline.

This module provides utilities for loading and parsing YAML configuration
files used throughout the pipeline, including constraints.yaml, nclex.yaml,
and pipeline.yaml.

Usage:
    from skills.utilities.yaml_parser import YAMLParser

    parser = YAMLParser()
    config = parser.load("config/constraints.yaml")
    value = parser.get_nested(config, "character_limits.title.max_lines")
"""

import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field


@dataclass
class YAMLLoadResult:
    """Container for YAML load results."""
    file_path: str
    success: bool
    data: Dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class YAMLParser:
    """Parse and validate YAML configuration files."""

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the YAMLParser.

        Args:
            base_path: Base directory for resolving relative paths
        """
        if base_path:
            self.base_path = Path(base_path)
        else:
            # Default to project root
            self.base_path = Path(__file__).parent.parent.parent

    def load(self, file_path: str) -> YAMLLoadResult:
        """
        Load a YAML file.

        Args:
            file_path: Path to YAML file (relative to base_path or absolute)

        Returns:
            YAMLLoadResult with parsed data
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = self.base_path / path

        result = YAMLLoadResult(
            file_path=str(path),
            success=False
        )

        if not path.exists():
            result.errors.append(f"File not found: {path}")
            return result

        if path.suffix.lower() not in ['.yaml', '.yml']:
            result.warnings.append(f"Unexpected extension: {path.suffix}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if data is None:
                result.data = {}
                result.warnings.append("YAML file is empty or contains only null")
            elif not isinstance(data, dict):
                result.errors.append(f"Expected dictionary at root, got {type(data).__name__}")
                return result
            else:
                result.data = data

            result.success = True

        except yaml.YAMLError as e:
            result.errors.append(f"YAML parse error: {e}")
        except Exception as e:
            result.errors.append(f"Error reading file: {e}")

        return result

    def load_multiple(self, file_paths: List[str]) -> Dict[str, YAMLLoadResult]:
        """
        Load multiple YAML files.

        Args:
            file_paths: List of paths to YAML files

        Returns:
            Dictionary mapping file paths to YAMLLoadResults
        """
        results = {}
        for path in file_paths:
            results[path] = self.load(path)
        return results

    def get_nested(
        self,
        data: Dict,
        key_path: str,
        default: Any = None,
        separator: str = "."
    ) -> Any:
        """
        Get a nested value from a dictionary using dot notation.

        Args:
            data: Dictionary to search
            key_path: Dot-separated path (e.g., "character_limits.title.max_lines")
            default: Default value if path not found
            separator: Path separator (default ".")

        Returns:
            Value at path or default
        """
        keys = key_path.split(separator)
        current = data

        for key in keys:
            if not isinstance(current, dict):
                return default

            if key not in current:
                return default

            current = current[key]

        return current

    def set_nested(
        self,
        data: Dict,
        key_path: str,
        value: Any,
        separator: str = "."
    ) -> Dict:
        """
        Set a nested value in a dictionary using dot notation.

        Args:
            data: Dictionary to modify
            key_path: Dot-separated path
            value: Value to set
            separator: Path separator

        Returns:
            Modified dictionary
        """
        keys = key_path.split(separator)
        current = data

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value
        return data

    def merge_configs(self, *configs: Dict) -> Dict:
        """
        Deep merge multiple configuration dictionaries.

        Later configs override earlier ones.

        Args:
            *configs: Configuration dictionaries to merge

        Returns:
            Merged configuration
        """
        result = {}

        for config in configs:
            result = self._deep_merge(result, config)

        return result

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """
        Recursively merge two dictionaries.

        Args:
            base: Base dictionary
            override: Dictionary with overriding values

        Returns:
            Merged dictionary
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    def validate_schema(
        self,
        data: Dict,
        required_keys: List[str],
        optional_keys: Optional[List[str]] = None
    ) -> Dict:
        """
        Validate that a config has required keys.

        Args:
            data: Configuration dictionary
            required_keys: List of required key paths
            optional_keys: List of optional key paths (for reporting)

        Returns:
            Validation result dictionary
        """
        result = {
            'valid': True,
            'missing_required': [],
            'present_required': [],
            'present_optional': [],
            'unknown_keys': []
        }

        all_known = set(required_keys or []) | set(optional_keys or [])

        for key_path in required_keys:
            value = self.get_nested(data, key_path)
            if value is None:
                result['valid'] = False
                result['missing_required'].append(key_path)
            else:
                result['present_required'].append(key_path)

        for key_path in (optional_keys or []):
            value = self.get_nested(data, key_path)
            if value is not None:
                result['present_optional'].append(key_path)

        return result

    def save(self, data: Dict, file_path: str) -> bool:
        """
        Save data to a YAML file.

        Args:
            data: Dictionary to save
            file_path: Path to output file

        Returns:
            True if successful, False otherwise
        """
        path = Path(file_path)
        if not path.is_absolute():
            path = self.base_path / path

        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

            return True
        except Exception as e:
            print(f"Error saving YAML: {e}")
            return False


def load_yaml(file_path: str) -> Dict:
    """
    Convenience function to load a YAML file.

    Args:
        file_path: Path to YAML file

    Returns:
        Parsed dictionary or empty dict on error
    """
    parser = YAMLParser()
    result = parser.load(file_path)
    return result.data if result.success else {}


def load_constraints() -> Dict:
    """Load constraints.yaml from default location."""
    parser = YAMLParser()
    result = parser.load("config/constraints.yaml")
    return result.data if result.success else {}


def load_nclex_config() -> Dict:
    """Load nclex.yaml from default location."""
    parser = YAMLParser()
    result = parser.load("config/nclex.yaml")
    return result.data if result.success else {}


if __name__ == "__main__":
    import sys

    print("YAML Parser - NCLEX Pipeline Utility")
    print("=" * 50)

    parser = YAMLParser()

    # Load from command line or demo with constraints.yaml
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "config/constraints.yaml"

    print(f"\nLoading: {file_path}")
    result = parser.load(file_path)

    if result.success:
        print("Status: SUCCESS")
        print()

        # Show top-level keys
        print("Top-level keys:")
        for key in result.data.keys():
            value = result.data[key]
            if isinstance(value, dict):
                print(f"  {key}: <dict with {len(value)} keys>")
            elif isinstance(value, list):
                print(f"  {key}: <list with {len(value)} items>")
            else:
                print(f"  {key}: {value}")

        # Demo nested access
        print()
        print("Nested access examples:")

        # Try some common paths
        test_paths = [
            "character_limits.title.max_lines",
            "character_limits.body.chars_per_line",
            "slides.section.max",
            "visual_quotas.enforcement",
            "brand.name",
            "content.domains.fundamentals.name"
        ]

        for path in test_paths:
            value = parser.get_nested(result.data, path)
            if value is not None:
                print(f"  {path} = {value}")
    else:
        print("Status: FAILED")
        for error in result.errors:
            print(f"  Error: {error}")

    if result.warnings:
        print()
        print("Warnings:")
        for warn in result.warnings:
            print(f"  - {warn}")
