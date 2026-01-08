"""
Base Agent Classes
==================

Foundation classes for all pipeline agents.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class AgentStatus(Enum):
    """Status of agent execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class AgentResult:
    """Result from agent execution."""
    agent_name: str
    status: AgentStatus
    output: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0


class Agent:
    """Base class for pipeline agents."""

    def __init__(self, name: str, prompt_path: Path = None):
        self.name = name
        self.prompt_path = prompt_path
        self.prompt_content = self._load_prompt() if prompt_path else ""

    def _load_prompt(self) -> str:
        """Load agent prompt from file."""
        if self.prompt_path and self.prompt_path.exists():
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
            warnings = output.pop('_warnings', []) if isinstance(output, dict) else []
        except Exception as e:
            output = {"error": str(e)}
            status = AgentStatus.FAILED
            errors = [str(e)]
            warnings = []

        duration = (datetime.now() - start_time).total_seconds()

        return AgentResult(
            agent_name=self.name,
            status=status,
            output=output,
            errors=errors,
            warnings=warnings,
            duration_seconds=duration
        )

    def _process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process the agent logic. Override in subclasses."""
        return {"processed": True, "agent": self.name}

    def validate_input(self, context: Dict[str, Any]) -> List[str]:
        """Validate required input fields. Override in subclasses."""
        return []  # No validation errors by default

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
