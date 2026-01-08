"""
Visual Pattern Matcher
Identifies visual aid opportunities in slide content using multi-factor scoring.

Enhanced with:
- Multi-factor weighted scoring (keyword, structure, density, domain, position)
- Proactive visual triggers based on content structure
- Priority ranking when multiple visual types match
- Fallback visual generation for quota compliance

Usage:
    from skills.generation.visual_pattern_matcher import (
        identify_visual_opportunity, score_visual_fit, get_visual_type,
        score_visual_opportunity_multifactor, rank_slides_for_visuals,
        apply_proactive_triggers, generate_fallback_visual
    )
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass


class VisualType(Enum):
    """Supported visual aid types."""
    TABLE = "TABLE"
    FLOWCHART = "FLOWCHART"
    DECISION_TREE = "DECISION_TREE"
    TIMELINE = "TIMELINE"
    HIERARCHY = "HIERARCHY"
    SPECTRUM = "SPECTRUM"
    KEY_DIFFERENTIATORS = "KEY_DIFFERENTIATORS"
    NONE = "NONE"


@dataclass
class VisualOpportunityScore:
    """Detailed scoring breakdown for visual opportunity."""
    visual_type: VisualType
    total_score: float
    keyword_score: float
    structure_score: float
    content_density_score: float
    domain_relevance_score: float
    slide_position_score: float
    proactive_trigger: Optional[str] = None


# =============================================================================
# MULTI-FACTOR SCORING WEIGHTS (from diagnostic recommendations)
# =============================================================================

SCORING_WEIGHTS = {
    'keyword_score': 0.30,       # Pattern/keyword matching
    'structure_score': 0.25,     # Bullet count, nesting
    'content_density': 0.20,     # Information per line
    'domain_relevance': 0.15,    # NCLEX domain fit
    'slide_position': 0.10       # Beginning/middle/end
}


# =============================================================================
# PROACTIVE TRIGGERS (content-structure based)
# =============================================================================

PROACTIVE_TRIGGERS = {
    'high_bullet_count': {
        'condition': lambda slide: _count_bullets(slide.get('body', '')) >= 4,
        'visual_type': VisualType.TABLE,
        'boost': 0.3
    },
    'multiple_items': {
        'condition': lambda slide: _has_multiple_items(slide.get('body', ''), 2),
        'visual_type': VisualType.KEY_DIFFERENTIATORS,
        'boost': 0.2
    },
    'criteria_list': {
        'condition': lambda slide: _has_criteria_list(slide.get('body', ''), 3),
        'visual_type': VisualType.TABLE,
        'boost': 0.25
    },
    'process_indicators': {
        'condition': lambda slide: _has_process_indicators(slide.get('body', ''), 2),
        'visual_type': VisualType.FLOWCHART,
        'boost': 0.25
    }
}


# =============================================================================
# NCLEX DOMAIN KEYWORDS (for domain_relevance scoring)
# =============================================================================

NCLEX_DOMAIN_KEYWORDS = {
    'pharmacology': [
        'medication', 'drug', 'dose', 'adverse', 'side effect', 'interaction',
        'contraindication', 'therapeutic', 'antidote', 'mechanism'
    ],
    'medical_surgical': [
        'assessment', 'intervention', 'complication', 'symptom', 'sign',
        'diagnosis', 'treatment', 'procedure', 'postoperative', 'preoperative'
    ],
    'fundamentals': [
        'vital signs', 'hygiene', 'mobility', 'safety', 'infection control',
        'documentation', 'communication', 'delegation', 'prioritization'
    ],
    'mental_health': [
        'anxiety', 'depression', 'therapeutic communication', 'crisis',
        'substance', 'psychosis', 'bipolar', 'schizophrenia', 'coping'
    ],
    'maternal_child': [
        'pregnancy', 'labor', 'delivery', 'postpartum', 'newborn', 'pediatric',
        'developmental', 'immunization', 'growth', 'milestone'
    ]
}


# Pattern indicators for each visual type
VISUAL_PATTERNS = {
    VisualType.TABLE: [
        r'\bcompare\b', r'\bversus\b', r'\bvs\.?\b', r'\bdifference\b',
        r'\bcharacteristics\b', r'\btypes of\b', r'\bcategories\b',
        r'\bclassification\b', r'\bsimilar\b', r'\bcontrast\b'
    ],
    VisualType.FLOWCHART: [
        r'\bprocess\b', r'\bsteps\b', r'\bprocedure\b', r'\bsequence\b',
        r'\bflow\b', r'\bpathway\b', r'\balgorithm\b', r'\bif.*then\b',
        r'\bfirst.*then\b', r'\bfollow\b'
    ],
    VisualType.DECISION_TREE: [
        r'\bdecision\b', r'\bchoose\b', r'\bselect\b', r'\bdetermine\b',
        r'\bassess.*then\b', r'\bbased on\b', r'\bdepending\b',
        r'\bcriteria\b', r'\bif.*else\b'
    ],
    VisualType.TIMELINE: [
        r'\bstages\b', r'\bphases\b', r'\bprogression\b', r'\bdevelopment\b',
        r'\bchronolog\b', r'\bover time\b', r'\bhistory\b', r'\bevolution\b',
        r'\bfirst.*second.*third\b', r'\bearly.*late\b'
    ],
    VisualType.HIERARCHY: [
        r'\bhierarchy\b', r'\blevels\b', r'\borganization\b', r'\bstructure\b',
        r'\bsuperior\b', r'\bsubordinate\b', r'\breports to\b',
        r'\bchain of\b', r'\btop.*bottom\b'
    ],
    VisualType.SPECTRUM: [
        r'\bspectrum\b', r'\brange\b', r'\bcontinuum\b', r'\bscale\b',
        r'\bmild.*severe\b', r'\blow.*high\b', r'\bminimal.*maximal\b',
        r'\bgradient\b', r'\bdegrees of\b'
    ],
    VisualType.KEY_DIFFERENTIATORS: [
        r'\bkey\s+difference\b', r'\bmain\s+distinction\b',
        r'\bcritical\s+difference\b', r'\bimportant.*distinguish\b',
        r'\bhow.*different\b', r'\bunlike\b'
    ]
}


def identify_visual_opportunity(
    slide_content: str
) -> Optional[VisualType]:
    """
    Identify if slide content would benefit from a visual aid.

    Args:
        slide_content: Combined header and body text

    Returns:
        VisualType if opportunity found, None otherwise
    """
    content_lower = slide_content.lower()

    best_type = None
    best_score = 0.0

    for visual_type, patterns in VISUAL_PATTERNS.items():
        score = score_visual_fit(content_lower, visual_type)
        if score > best_score and score >= 0.3:  # Minimum threshold
            best_score = score
            best_type = visual_type

    return best_type


def score_visual_fit(
    content: str,
    visual_type: VisualType
) -> float:
    """
    Score how well content fits a visual type.

    Args:
        content: Slide content (lowercase)
        visual_type: Type of visual to score against

    Returns:
        Score from 0.0 to 1.0
    """
    if visual_type not in VISUAL_PATTERNS:
        return 0.0

    patterns = VISUAL_PATTERNS[visual_type]
    matches = 0

    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            matches += 1

    # Score based on pattern matches
    return min(1.0, matches / 3)  # 3+ matches = 1.0


def get_visual_type(
    slide: Dict[str, Any]
) -> Tuple[VisualType, float]:
    """
    Get recommended visual type for a slide.

    Args:
        slide: Slide dictionary with header and body

    Returns:
        Tuple of (VisualType, confidence_score)
    """
    header = slide.get('header', '')
    body = slide.get('body', '')
    content = f"{header} {body}"

    visual_type = identify_visual_opportunity(content)

    if visual_type:
        score = score_visual_fit(content.lower(), visual_type)
        return (visual_type, score)

    return (VisualType.NONE, 0.0)


def get_all_visual_scores(content: str) -> Dict[VisualType, float]:
    """
    Get scores for all visual types.

    Args:
        content: Slide content

    Returns:
        Dict mapping VisualType to score
    """
    content_lower = content.lower()
    scores = {}

    for visual_type in VisualType:
        if visual_type != VisualType.NONE:
            scores[visual_type] = score_visual_fit(content_lower, visual_type)

    return scores


# =============================================================================
# HELPER FUNCTIONS FOR PROACTIVE TRIGGERS
# =============================================================================

def _count_bullets(body: str) -> int:
    """Count top-level bullet points in body text."""
    if not body:
        return 0

    bullet_patterns = [
        r'^[\*\-\•]\s+',
        r'^\d+\.\s+',
        r'^\d+\)\s+',
        r'^[a-zA-Z]\.\s+',
        r'^[a-zA-Z]\)\s+'
    ]

    count = 0
    for line in body.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        # Skip indented (nested) bullets
        if line.startswith('  ') or line.startswith('\t'):
            continue
        for pattern in bullet_patterns:
            if re.match(pattern, stripped):
                count += 1
                break
    return count


def _has_multiple_items(body: str, min_count: int) -> bool:
    """Check if body contains multiple distinct items (for comparison)."""
    if not body:
        return False

    # Check for "X vs Y" or "X versus Y" patterns
    vs_matches = re.findall(r'\b\w+\s+(?:vs\.?|versus)\s+\w+', body, re.IGNORECASE)
    if vs_matches:
        return True

    # Check for colon-prefixed items (e.g., "Drug A: ...\nDrug B: ...")
    colon_items = re.findall(r'^[\*\-\•]?\s*([A-Za-z][A-Za-z0-9\s]+):', body, re.MULTILINE)
    return len(colon_items) >= min_count


def _has_criteria_list(body: str, min_criteria: int) -> bool:
    """Check if body contains a list of criteria or attributes."""
    if not body:
        return False

    criteria_keywords = [
        'criteria', 'assessment', 'findings', 'signs', 'symptoms',
        'characteristics', 'features', 'indicators', 'parameters'
    ]

    body_lower = body.lower()
    has_keyword = any(kw in body_lower for kw in criteria_keywords)
    bullet_count = _count_bullets(body)

    return has_keyword and bullet_count >= min_criteria


def _has_process_indicators(body: str, min_indicators: int) -> bool:
    """Check if body describes a process or sequence."""
    if not body:
        return False

    process_patterns = [
        r'\bstep\s*\d+', r'\bfirst\b', r'\bthen\b', r'\bnext\b',
        r'\bfinally\b', r'\bleads?\s+to\b', r'\bresults?\s+in\b',
        r'\bfollowed\s+by\b', r'\bafter\b', r'\bbefore\b'
    ]

    body_lower = body.lower()
    count = sum(1 for p in process_patterns if re.search(p, body_lower))
    return count >= min_indicators


def _calculate_content_density(body: str) -> float:
    """Calculate content density score (0-1)."""
    if not body or not body.strip():
        return 0.0

    lines = [l for l in body.split('\n') if l.strip()]
    words = re.findall(r'\b\w+\b', body)

    if not lines:
        return 0.0

    words_per_line = len(words) / len(lines)

    # Higher density = more words per line (8+ words is dense)
    density = min(1.0, words_per_line / 8)

    # Boost for multiple lines
    line_factor = min(1.0, len(lines) / 5)

    return (density * 0.6) + (line_factor * 0.4)


def _calculate_domain_relevance(content: str) -> float:
    """Calculate NCLEX domain relevance score (0-1)."""
    if not content:
        return 0.0

    content_lower = content.lower()
    max_score = 0.0

    for domain, keywords in NCLEX_DOMAIN_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in content_lower)
        domain_score = min(1.0, matches / 3)  # 3+ matches = full score
        max_score = max(max_score, domain_score)

    return max_score


def _calculate_position_score(slide_number: int, total_slides: int) -> float:
    """
    Calculate position score based on slide position in section.

    Middle slides (3rd through second-to-last) get higher scores
    as they're better candidates for visuals.
    """
    if total_slides <= 2:
        return 0.5

    # First and last slides are typically intro/summary - lower score
    if slide_number == 1 or slide_number == total_slides:
        return 0.3

    # Second and second-to-last are transitional
    if slide_number == 2 or slide_number == total_slides - 1:
        return 0.6

    # Middle slides are prime candidates
    return 0.8


# =============================================================================
# MULTI-FACTOR SCORING FUNCTIONS
# =============================================================================

def score_visual_opportunity_multifactor(
    slide: Dict[str, Any],
    slide_number: int = 0,
    total_slides: int = 0
) -> VisualOpportunityScore:
    """
    Calculate multi-factor visual opportunity score for a slide.

    Uses weighted factors:
    - keyword_score (30%): Pattern/keyword matching
    - structure_score (25%): Bullet count, nesting
    - content_density (20%): Information per line
    - domain_relevance (15%): NCLEX domain fit
    - slide_position (10%): Beginning/middle/end

    Args:
        slide: Slide dictionary with header, body, slide_type
        slide_number: Position of slide in section (1-indexed)
        total_slides: Total slides in section

    Returns:
        VisualOpportunityScore with detailed breakdown
    """
    header = slide.get('header', '')
    body = slide.get('body', '')
    content = f"{header} {body}"
    content_lower = content.lower()

    # Skip fixed slide types
    slide_type = slide.get('slide_type', '').lower()
    if any(t in slide_type for t in ['intro', 'vignette', 'answer', 'summary']):
        return VisualOpportunityScore(
            visual_type=VisualType.NONE,
            total_score=0.0,
            keyword_score=0.0,
            structure_score=0.0,
            content_density_score=0.0,
            domain_relevance_score=0.0,
            slide_position_score=0.0
        )

    # Calculate individual factor scores
    all_keyword_scores = {}
    for visual_type, patterns in VISUAL_PATTERNS.items():
        matches = sum(1 for p in patterns if re.search(p, content_lower))
        all_keyword_scores[visual_type] = min(1.0, matches / 3)

    # Find best visual type by keyword
    best_type = max(all_keyword_scores, key=all_keyword_scores.get)
    keyword_score = all_keyword_scores[best_type]

    # Structure score (bullet count and nesting)
    bullet_count = _count_bullets(body)
    structure_score = min(1.0, bullet_count / 4)  # 4+ bullets = full score

    # Content density
    density_score = _calculate_content_density(body)

    # Domain relevance
    domain_score = _calculate_domain_relevance(content)

    # Position score
    position_score = _calculate_position_score(slide_number, total_slides) if total_slides > 0 else 0.5

    # Check proactive triggers
    proactive_trigger = None
    trigger_boost = 0.0
    for trigger_name, trigger_config in PROACTIVE_TRIGGERS.items():
        if trigger_config['condition'](slide):
            proactive_trigger = trigger_name
            trigger_boost = trigger_config['boost']
            if trigger_config['visual_type'] != best_type:
                # Proactive trigger suggests different type
                best_type = trigger_config['visual_type']
            break

    # Calculate weighted total
    total_score = (
        keyword_score * SCORING_WEIGHTS['keyword_score'] +
        structure_score * SCORING_WEIGHTS['structure_score'] +
        density_score * SCORING_WEIGHTS['content_density'] +
        domain_score * SCORING_WEIGHTS['domain_relevance'] +
        position_score * SCORING_WEIGHTS['slide_position'] +
        trigger_boost
    )

    # Ensure total doesn't exceed 1.0
    total_score = min(1.0, total_score)

    # If total score is too low, return NONE
    if total_score < 0.3 and not proactive_trigger:
        best_type = VisualType.NONE

    return VisualOpportunityScore(
        visual_type=best_type,
        total_score=total_score,
        keyword_score=keyword_score,
        structure_score=structure_score,
        content_density_score=density_score,
        domain_relevance_score=domain_score,
        slide_position_score=position_score,
        proactive_trigger=proactive_trigger
    )


def rank_slides_for_visuals(
    slides: List[Dict[str, Any]],
    min_visuals: int = 2,
    max_percentage: float = 0.4
) -> List[Tuple[int, VisualOpportunityScore]]:
    """
    Rank all slides by visual opportunity score.

    Used for:
    - Priority ranking when multiple types match
    - Fallback visual generation when quota not met

    Args:
        slides: List of slide dictionaries
        min_visuals: Minimum visuals required
        max_percentage: Maximum percentage of slides as visuals

    Returns:
        Sorted list of (slide_number, VisualOpportunityScore) tuples
    """
    total_slides = len(slides)
    max_visuals = int(total_slides * max_percentage)

    scored_slides = []

    for i, slide in enumerate(slides):
        slide_num = slide.get('slide_number', i + 1)
        score = score_visual_opportunity_multifactor(slide, slide_num, total_slides)
        if score.visual_type != VisualType.NONE:
            scored_slides.append((slide_num, score))

    # Sort by total score descending
    scored_slides.sort(key=lambda x: x[1].total_score, reverse=True)

    return scored_slides


def apply_proactive_triggers(slide: Dict[str, Any]) -> Optional[Tuple[VisualType, str]]:
    """
    Check if any proactive triggers apply to the slide.

    Proactive triggers fire based on content structure rather than keywords,
    ensuring visuals are suggested even without explicit visual keywords.

    Args:
        slide: Slide dictionary

    Returns:
        Tuple of (VisualType, trigger_name) if triggered, None otherwise
    """
    for trigger_name, trigger_config in PROACTIVE_TRIGGERS.items():
        if trigger_config['condition'](slide):
            return (trigger_config['visual_type'], trigger_name)
    return None


def generate_fallback_visual(
    slides: List[Dict[str, Any]],
    current_visual_count: int,
    min_required: int
) -> List[int]:
    """
    Identify slides to convert to visuals to meet quota.

    When visual quota isn't met through normal identification,
    this function ranks non-visual slides and suggests the best
    candidates for forced visual conversion (using TABLE as fallback).

    Args:
        slides: List of slide dictionaries
        current_visual_count: Current number of visual slides
        min_required: Minimum visuals required for quota

    Returns:
        List of slide_numbers to convert to visuals
    """
    if current_visual_count >= min_required:
        return []

    needed = min_required - current_visual_count

    # Get ranked slides
    ranked = rank_slides_for_visuals(slides)

    # Find slides that don't already have visuals
    candidates = []
    for slide_num, score in ranked:
        slide = next((s for s in slides if s.get('slide_number') == slide_num), None)
        if slide and not slide.get('visual_marker', '').startswith('Visual: Yes'):
            candidates.append(slide_num)

    # Return top candidates
    return candidates[:needed]


def get_visual_recommendation(
    slide: Dict[str, Any],
    slide_number: int = 0,
    total_slides: int = 0
) -> Dict[str, Any]:
    """
    Get comprehensive visual recommendation for a slide.

    Combines multi-factor scoring with all available context.

    Args:
        slide: Slide dictionary
        slide_number: Position in section
        total_slides: Total slides in section

    Returns:
        Dictionary with recommendation details
    """
    score = score_visual_opportunity_multifactor(slide, slide_number, total_slides)
    proactive = apply_proactive_triggers(slide)

    return {
        'slide_number': slide_number,
        'recommended_type': score.visual_type.value,
        'confidence': score.total_score,
        'should_have_visual': score.total_score >= 0.4 or proactive is not None,
        'scoring_breakdown': {
            'keyword_score': score.keyword_score,
            'structure_score': score.structure_score,
            'content_density_score': score.content_density_score,
            'domain_relevance_score': score.domain_relevance_score,
            'slide_position_score': score.slide_position_score
        },
        'proactive_trigger': score.proactive_trigger,
        'all_scores': get_all_visual_scores(f"{slide.get('header', '')} {slide.get('body', '')}")
    }


if __name__ == "__main__":
    print("=" * 60)
    print("VISUAL PATTERN MATCHER - MULTI-FACTOR SCORING TEST")
    print("=" * 60)

    # Test cases with full slide structure
    test_slides = [
        {
            'slide_number': 3,
            'header': 'ACE Inhibitors vs ARBs',
            'body': '''* ACE-I: Block angiotensin converting enzyme
* ARBs: Block AT1 receptor directly
* ACE-I: May cause dry cough (10%)
* ARBs: No cough side effect
* Both: First-line for hypertension''',
            'slide_type': 'Content'
        },
        {
            'slide_number': 5,
            'header': 'Steps in Medication Administration',
            'body': '''Step 1: Verify the medication order
Step 2: Check patient identification
Step 3: Review allergies and contraindications
Step 4: Prepare the medication
Step 5: Administer and document''',
            'slide_type': 'Content'
        },
        {
            'slide_number': 7,
            'header': 'Types of Heart Failure',
            'body': '''* Systolic HF (HFrEF)
  - Reduced ejection fraction
  - Weak contraction
* Diastolic HF (HFpEF)
  - Preserved ejection fraction
  - Impaired relaxation''',
            'slide_type': 'Content'
        },
        {
            'slide_number': 1,
            'header': 'Section Intro: Cardiovascular Medications',
            'body': 'Overview of key cardiovascular drug classes',
            'slide_type': 'Section Intro'
        }
    ]

    total = len(test_slides)

    print("\nIndividual Slide Analysis:")
    print("-" * 60)

    for slide in test_slides:
        rec = get_visual_recommendation(slide, slide['slide_number'], total)
        print(f"\nSlide {rec['slide_number']}: {slide['header'][:40]}...")
        print(f"  Recommended Type: {rec['recommended_type']}")
        print(f"  Confidence: {rec['confidence']:.2f}")
        print(f"  Should Have Visual: {rec['should_have_visual']}")
        if rec['proactive_trigger']:
            print(f"  Proactive Trigger: {rec['proactive_trigger']}")
        print(f"  Score Breakdown:")
        for k, v in rec['scoring_breakdown'].items():
            print(f"    {k}: {v:.2f}")

    print("\n" + "-" * 60)
    print("Ranked Slides for Visuals:")
    ranked = rank_slides_for_visuals(test_slides, min_visuals=2)
    for slide_num, score in ranked:
        print(f"  #{slide_num}: {score.visual_type.value} (score: {score.total_score:.2f})")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
