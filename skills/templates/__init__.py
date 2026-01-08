"""
Template Skills for NCLEX Pipeline
Provides structured templates for vignettes and answer slides.
"""

from .vignette_template import (
    VignetteTemplate,
    parse_vignette_body,
    enforce_vignette_structure,
    validate_vignette,
    VIGNETTE_TEMPLATES
)

from .answer_template import (
    AnswerTemplate,
    parse_answer_body,
    enforce_answer_structure,
    validate_answer
)

__all__ = [
    'VignetteTemplate',
    'parse_vignette_body',
    'enforce_vignette_structure',
    'validate_vignette',
    'VIGNETTE_TEMPLATES',
    'AnswerTemplate',
    'parse_answer_body',
    'enforce_answer_structure',
    'validate_answer'
]
