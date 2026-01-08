"""
Content Structure Analyzer
Analyzes slide body content structure to improve visual type selection
beyond simple keyword matching.

Used by: Step 9 Visual Identification (visual_identifier agent)

Usage:
    from skills.generation.content_structure_analyzer import (
        count_bullet_points,
        detect_list_patterns,
        identify_comparison_structure,
        detect_sequential_markers,
        analyze_information_density,
        detect_hierarchical_structure,
        suggest_visual_type
    )
"""

import re
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

# Import VisualType from the pattern matcher for consistency
from .visual_pattern_matcher import VisualType


# =============================================================================
# BULLET POINT PATTERNS
# =============================================================================

# Patterns for different bullet styles
BULLET_PATTERNS = [
    r'^[\*\-\•]\s+',           # Asterisk, dash, bullet: * - or bullet char
    r'^\d+\.\s+',              # Numbered: 1. 2. 3.
    r'^\d+\)\s+',              # Numbered with paren: 1) 2) 3)
    r'^[a-zA-Z]\.\s+',         # Lettered: a. b. c.
    r'^[a-zA-Z]\)\s+',         # Lettered with paren: a) b) c)
    r'^\([a-zA-Z\d]+\)\s+',    # Parenthesized: (a) (1)
    r'^\[\d+\]\s+',            # Bracketed: [1] [2]
]

# Indentation patterns for nested bullets
INDENT_PATTERNS = [
    r'^(\s{2,}|\t+)',          # Two or more spaces or tabs
]


# =============================================================================
# COMPARISON KEYWORDS
# =============================================================================

COMPARISON_KEYWORDS = [
    'vs', 'versus', 'compare', 'compared', 'comparing', 'comparison',
    'contrast', 'contrasting', 'difference', 'differences', 'different',
    'similarity', 'similarities', 'similar', 'unlike', 'whereas',
    'while', 'although', 'however', 'but', 'alternatively'
]

COMPARISON_PHRASES = [
    r'\bvs\.?\b',
    r'\bversus\b',
    r'\bcompare[ds]?\b',
    r'\bcontrast(?:ing)?\b',
    r'\bdifferent(?:iate)?(?:s|d)?\b',
    r'\bsimilar(?:ity|ities)?\b',
    r'\bunlike\b',
    r'\bwhereas\b',
    r'\bon the other hand\b',
    r'\bin contrast\b',
    r'\bas opposed to\b',
]


# =============================================================================
# SEQUENTIAL MARKERS
# =============================================================================

SEQUENTIAL_KEYWORDS = [
    'first', 'second', 'third', 'fourth', 'fifth',
    'then', 'next', 'finally', 'lastly', 'subsequently',
    'initially', 'afterwards', 'before', 'after',
    'step', 'phase', 'stage', 'process', 'procedure'
]

SEQUENTIAL_PHRASES = [
    r'\bstep\s*\d+\b',
    r'\bphase\s*\d+\b',
    r'\bstage\s*\d+\b',
    r'\bfirst\b.*\bthen\b',
    r'\bleads?\s+to\b',
    r'\bresults?\s+in\b',
    r'\btriggers?\b',
    r'\bcauses?\b',
    r'\bfollowed\s+by\b',
    r'\bsequence\b',
    r'\bprogress(?:ion|es)?\b',
    r'\bnext\b',
    r'\bfinally\b',
    r'\beventually\b',
]

# Pattern types for sequential content
PROCESS_INDICATORS = ['mechanism', 'action', 'pathway', 'how', 'works', 'process']
TIMELINE_INDICATORS = ['year', 'month', 'week', 'day', 'hour', 'ago', 'later',
                       'early', 'late', 'during', 'period', 'era', 'age', 'century']
STEPS_INDICATORS = ['step', 'procedure', 'protocol', 'instructions', 'guide']


# =============================================================================
# HIERARCHICAL KEYWORDS
# =============================================================================

HIERARCHY_KEYWORDS = [
    'type', 'types', 'category', 'categories', 'class', 'classes',
    'classification', 'subtype', 'subtypes', 'subcategory',
    'division', 'subdivided', 'consists', 'includes', 'comprises',
    'taxonomy', 'group', 'groups', 'level', 'levels'
]

HIERARCHY_PHRASES = [
    r'\btypes?\s+of\b',
    r'\bcategor(?:y|ies)\b',
    r'\bclass(?:es|ification)?\b',
    r'\bsubtype\b',
    r'\bsubdivided?\s+into\b',
    r'\bconsists?\s+of\b',
    r'\bincludes?\b',
    r'\bcomprises?\b',
    r'\blevels?\s+of\b',
    r'\bhierarch(?:y|ical)\b',
]


# =============================================================================
# FUNCTION 1: count_bullet_points
# =============================================================================

def count_bullet_points(body: str) -> int:
    """
    Count bullet points in body text.

    Handles different bullet styles:
    - Asterisks: * item
    - Dashes: - item
    - Bullets: bullet character item
    - Numbered: 1. item, 2. item
    - Lettered: a. item, b. item

    Args:
        body: The slide body text to analyze

    Returns:
        Count of top-level bullet points (non-nested)
    """
    if not body or not body.strip():
        return 0

    lines = body.strip().split('\n')
    bullet_count = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check if line is a top-level bullet (not indented)
        is_indented = line.startswith('  ') or line.startswith('\t')

        if is_indented:
            continue  # Skip nested bullets

        # Check against all bullet patterns
        for pattern in BULLET_PATTERNS:
            if re.match(pattern, stripped, re.IGNORECASE):
                bullet_count += 1
                break

    return bullet_count


# =============================================================================
# FUNCTION 2: detect_list_patterns
# =============================================================================

def detect_list_patterns(body: str) -> Dict[str, Any]:
    """
    Detect list patterns in content.

    Analyzes the structure of lists in the body text, including:
    - Whether numbered lists are present
    - Whether bulleted lists are present
    - Nesting depth
    - Item counts per level

    Args:
        body: The slide body text to analyze

    Returns:
        Dictionary containing:
        - has_numbered_list: bool
        - has_bulleted_list: bool
        - list_depth: int (maximum nesting level, 1 = flat)
        - items_per_level: List[int] (count of items at each level)
    """
    result = {
        'has_numbered_list': False,
        'has_bulleted_list': False,
        'list_depth': 0,
        'items_per_level': []
    }

    if not body or not body.strip():
        return result

    lines = body.strip().split('\n')

    # Track items at each indentation level
    level_counts: Dict[int, int] = {}
    max_depth = 0

    # Numbered patterns
    numbered_patterns = [
        r'^\s*\d+\.\s+',
        r'^\s*\d+\)\s+',
        r'^\s*\[\d+\]\s+',
    ]

    # Bulleted patterns
    bulleted_patterns = [
        r'^\s*[\*\-\•]\s+',
        r'^\s*[a-zA-Z]\.\s+',
        r'^\s*[a-zA-Z]\)\s+',
        r'^\s*\([a-zA-Z]+\)\s+',
    ]

    for line in lines:
        if not line.strip():
            continue

        # Calculate indentation level
        stripped = line.lstrip()
        indent_chars = len(line) - len(stripped)
        # Convert to level: 0-1 chars = level 1, 2-3 = level 2, etc.
        level = (indent_chars // 2) + 1 if indent_chars > 0 else 1

        # Check for numbered list
        for pattern in numbered_patterns:
            if re.match(pattern, line):
                result['has_numbered_list'] = True
                level_counts[level] = level_counts.get(level, 0) + 1
                max_depth = max(max_depth, level)
                break
        else:
            # Check for bulleted list
            for pattern in bulleted_patterns:
                if re.match(pattern, line):
                    result['has_bulleted_list'] = True
                    level_counts[level] = level_counts.get(level, 0) + 1
                    max_depth = max(max_depth, level)
                    break

    result['list_depth'] = max_depth

    # Convert level_counts to ordered list
    if level_counts:
        max_level = max(level_counts.keys())
        result['items_per_level'] = [
            level_counts.get(i, 0) for i in range(1, max_level + 1)
        ]

    return result


# =============================================================================
# FUNCTION 3: identify_comparison_structure
# =============================================================================

def identify_comparison_structure(body: str) -> Dict[str, Any]:
    """
    Identify if content has comparison structure.

    Looks for comparison indicators:
    - vs, versus keywords
    - compare, contrast language
    - similarities, differences mentions
    - Side-by-side structure patterns

    Args:
        body: The slide body text to analyze

    Returns:
        Dictionary containing:
        - is_comparison: bool
        - comparison_items: List[str] (items being compared)
        - comparison_type: 'binary' | 'multiple' | None
    """
    result = {
        'is_comparison': False,
        'comparison_items': [],
        'comparison_type': None
    }

    if not body or not body.strip():
        return result

    body_lower = body.lower()

    # Check for comparison phrases
    comparison_found = False
    for pattern in COMPARISON_PHRASES:
        if re.search(pattern, body_lower, re.IGNORECASE):
            comparison_found = True
            break

    if not comparison_found:
        return result

    result['is_comparison'] = True

    # Try to extract comparison items
    items = _extract_comparison_items(body)
    result['comparison_items'] = items

    # Determine comparison type
    if len(items) == 2:
        result['comparison_type'] = 'binary'
    elif len(items) > 2:
        result['comparison_type'] = 'multiple'
    else:
        # Still a comparison even if we can't extract items
        result['comparison_type'] = 'binary'  # Default assumption

    return result


def _extract_comparison_items(body: str) -> List[str]:
    """
    Helper to extract items being compared from text.

    Args:
        body: Text to analyze

    Returns:
        List of comparison item names
    """
    items = []

    # Pattern: "X vs Y" or "X versus Y"
    vs_pattern = r'(\b[\w\-]+)\s+(?:vs\.?|versus)\s+(\b[\w\-]+)'
    vs_matches = re.findall(vs_pattern, body, re.IGNORECASE)
    for match in vs_matches:
        items.extend([m.strip() for m in match if m.strip()])

    # Pattern: "Compare X and Y"
    compare_pattern = r'compare[sd]?\s+(\b[\w\-]+)\s+(?:and|with|to)\s+(\b[\w\-]+)'
    compare_matches = re.findall(compare_pattern, body, re.IGNORECASE)
    for match in compare_matches:
        items.extend([m.strip() for m in match if m.strip()])

    # Pattern: "X: ...\nY: ..." (parallel structure in bullets)
    lines = body.strip().split('\n')
    colon_items = []
    for line in lines:
        stripped = line.strip()
        # Remove bullet markers
        stripped = re.sub(r'^[\*\-\•]\s*', '', stripped)
        stripped = re.sub(r'^\d+[\.\)]\s*', '', stripped)

        if ':' in stripped:
            before_colon = stripped.split(':')[0].strip()
            if before_colon and len(before_colon) < 30:  # Reasonable item name
                colon_items.append(before_colon)

    if len(colon_items) >= 2:
        # Check if these look like comparison items (similar length/structure)
        items.extend(colon_items)

    # Remove duplicates while preserving order
    seen = set()
    unique_items = []
    for item in items:
        item_lower = item.lower()
        if item_lower not in seen and len(item) > 1:
            seen.add(item_lower)
            unique_items.append(item)

    return unique_items[:6]  # Limit to reasonable number


# =============================================================================
# FUNCTION 4: detect_sequential_markers
# =============================================================================

def detect_sequential_markers(body: str) -> Dict[str, Any]:
    """
    Detect sequence/process indicators in content.

    Looks for:
    - Ordinal markers: first, then, next, finally
    - Step indicators: step 1, step 2, etc.
    - Process language: leads to, results in, triggers
    - Phase/stage markers

    Args:
        body: The slide body text to analyze

    Returns:
        Dictionary containing:
        - is_sequential: bool
        - sequence_type: 'process' | 'timeline' | 'steps' | None
        - step_count: int (estimated number of steps)
    """
    result = {
        'is_sequential': False,
        'sequence_type': None,
        'step_count': 0
    }

    if not body or not body.strip():
        return result

    body_lower = body.lower()

    # Count sequential phrase matches
    sequential_score = 0
    for pattern in SEQUENTIAL_PHRASES:
        matches = re.findall(pattern, body_lower, re.IGNORECASE)
        sequential_score += len(matches)

    if sequential_score < 1:
        return result

    result['is_sequential'] = True

    # Determine sequence type
    process_score = sum(1 for kw in PROCESS_INDICATORS if kw in body_lower)
    timeline_score = sum(1 for kw in TIMELINE_INDICATORS if kw in body_lower)
    steps_score = sum(1 for kw in STEPS_INDICATORS if kw in body_lower)

    # Also check for explicit step numbering
    step_numbers = re.findall(r'\bstep\s*(\d+)', body_lower)
    if step_numbers:
        steps_score += 2

    max_score = max(process_score, timeline_score, steps_score)

    if max_score > 0:
        if timeline_score == max_score:
            result['sequence_type'] = 'timeline'
        elif steps_score == max_score:
            result['sequence_type'] = 'steps'
        else:
            result['sequence_type'] = 'process'
    else:
        result['sequence_type'] = 'process'  # Default

    # Estimate step count
    result['step_count'] = _estimate_step_count(body)

    return result


def _estimate_step_count(body: str) -> int:
    """
    Estimate the number of steps in sequential content.

    Args:
        body: Text to analyze

    Returns:
        Estimated step count
    """
    # Count explicit step numbers
    step_numbers = re.findall(r'\bstep\s*(\d+)', body.lower())
    if step_numbers:
        return max(int(n) for n in step_numbers)

    # Count ordinals
    ordinal_count = 0
    ordinals = ['first', 'second', 'third', 'fourth', 'fifth',
                'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    for ordinal in ordinals:
        if ordinal in body.lower():
            ordinal_count += 1

    if ordinal_count >= 2:
        return ordinal_count

    # Count "then"/"next" transitions
    transitions = len(re.findall(r'\bthen\b|\bnext\b|\bfinally\b', body.lower()))
    if transitions > 0:
        return transitions + 1

    # Fall back to bullet count
    return count_bullet_points(body)


# =============================================================================
# FUNCTION 5: analyze_information_density
# =============================================================================

def analyze_information_density(body: str) -> Dict[str, Any]:
    """
    Analyze content density of the body text.

    Calculates:
    - Total word count
    - Average words per line
    - Unique concept estimation
    - Overall density score (0-1)

    Args:
        body: The slide body text to analyze

    Returns:
        Dictionary containing:
        - total_words: int
        - words_per_line: float
        - unique_concepts: int
        - density_score: float (0-1, higher = more dense)
    """
    result = {
        'total_words': 0,
        'words_per_line': 0.0,
        'unique_concepts': 0,
        'density_score': 0.0
    }

    if not body or not body.strip():
        return result

    # Calculate total words
    words = re.findall(r'\b\w+\b', body)
    result['total_words'] = len(words)

    # Calculate words per line
    lines = [l for l in body.strip().split('\n') if l.strip()]
    if lines:
        result['words_per_line'] = result['total_words'] / len(lines)

    # Estimate unique concepts (proper nouns, technical terms, capitalized words)
    unique_concepts = _count_unique_concepts(body)
    result['unique_concepts'] = unique_concepts

    # Calculate density score
    result['density_score'] = _calculate_density_score(
        total_words=result['total_words'],
        words_per_line=result['words_per_line'],
        unique_concepts=unique_concepts,
        line_count=len(lines)
    )

    return result


def _count_unique_concepts(body: str) -> int:
    """
    Count unique concepts/terms in the text.

    Considers:
    - Capitalized words (potential proper nouns/terms)
    - Technical terms (words with specific patterns)
    - Colon-prefixed items (often key terms)

    Args:
        body: Text to analyze

    Returns:
        Estimated count of unique concepts
    """
    concepts = set()

    # Capitalized words that aren't sentence starters
    words = re.findall(r'\b([A-Z][a-zA-Z]+)\b', body)

    # Filter out common sentence starters
    starters = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'has', 'have',
                'this', 'that', 'these', 'those', 'it', 'they', 'we', 'you', 'i'}

    for word in words:
        if word.lower() not in starters:
            concepts.add(word.lower())

    # Terms before colons (often key terms)
    colon_terms = re.findall(r'(\b[\w\s]+):', body)
    for term in colon_terms:
        term_clean = term.strip().lower()
        if term_clean and len(term_clean) < 50:
            concepts.add(term_clean)

    # Terms in parentheses (often clarifications/technical terms)
    paren_terms = re.findall(r'\(([^)]+)\)', body)
    for term in paren_terms:
        term_clean = term.strip().lower()
        if term_clean and len(term_clean) < 50:
            concepts.add(term_clean)

    return len(concepts)


def _calculate_density_score(
    total_words: int,
    words_per_line: float,
    unique_concepts: int,
    line_count: int
) -> float:
    """
    Calculate overall content density score.

    Args:
        total_words: Total word count
        words_per_line: Average words per line
        unique_concepts: Count of unique concepts
        line_count: Number of non-empty lines

    Returns:
        Density score from 0.0 to 1.0
    """
    score = 0.0

    # Word count factor (more words = more dense)
    # 50+ words is considered high density
    word_factor = min(1.0, total_words / 50)
    score += word_factor * 0.3

    # Words per line factor
    # 8+ words per line is considered dense
    wpl_factor = min(1.0, words_per_line / 8)
    score += wpl_factor * 0.2

    # Unique concepts factor
    # 5+ concepts is considered information-rich
    concept_factor = min(1.0, unique_concepts / 5)
    score += concept_factor * 0.3

    # Line count factor (more lines = more content)
    # 5+ lines is considered substantial
    line_factor = min(1.0, line_count / 5)
    score += line_factor * 0.2

    return round(score, 2)


# =============================================================================
# FUNCTION 6: detect_hierarchical_structure
# =============================================================================

def detect_hierarchical_structure(body: str) -> Dict[str, Any]:
    """
    Detect hierarchy in content.

    Looks for:
    - Category/type language
    - Classification patterns
    - Parent-child relationship indicators
    - Nested list structures

    Args:
        body: The slide body text to analyze

    Returns:
        Dictionary containing:
        - is_hierarchical: bool
        - levels_detected: int
        - root_concept: str or None (the top-level category)
    """
    result = {
        'is_hierarchical': False,
        'levels_detected': 0,
        'root_concept': None
    }

    if not body or not body.strip():
        return result

    body_lower = body.lower()

    # Check for hierarchy phrases
    hierarchy_score = 0
    for pattern in HIERARCHY_PHRASES:
        if re.search(pattern, body_lower, re.IGNORECASE):
            hierarchy_score += 1

    # Check for nested list structure
    list_info = detect_list_patterns(body)
    if list_info['list_depth'] >= 2:
        hierarchy_score += 2
        result['levels_detected'] = list_info['list_depth']

    # Check for classification keywords
    for keyword in HIERARCHY_KEYWORDS:
        if keyword in body_lower:
            hierarchy_score += 0.5

    if hierarchy_score < 1.5:
        return result

    result['is_hierarchical'] = True

    # Determine levels if not already set from list structure
    if result['levels_detected'] == 0:
        result['levels_detected'] = _estimate_hierarchy_levels(body)

    # Try to extract root concept
    result['root_concept'] = _extract_root_concept(body)

    return result


def _estimate_hierarchy_levels(body: str) -> int:
    """
    Estimate the number of hierarchy levels in content.

    Args:
        body: Text to analyze

    Returns:
        Estimated number of levels
    """
    body_lower = body.lower()

    # Check for explicit level mentions
    level_matches = re.findall(r'level\s*(\d+)', body_lower)
    if level_matches:
        return max(int(n) for n in level_matches)

    # Check for "types of X" -> "subtypes of Y" pattern
    has_types = bool(re.search(r'\btypes?\s+of\b', body_lower))
    has_subtypes = bool(re.search(r'\bsub(?:types?|categor)', body_lower))

    if has_types and has_subtypes:
        return 3
    elif has_types or has_subtypes:
        return 2

    # Check list nesting
    list_info = detect_list_patterns(body)
    if list_info['list_depth'] > 0:
        return list_info['list_depth']

    # Default for hierarchical content
    return 2


def _extract_root_concept(body: str) -> Optional[str]:
    """
    Extract the root/top-level concept from hierarchical content.

    Args:
        body: Text to analyze

    Returns:
        Root concept name or None
    """
    # Pattern: "Types of X" -> X is root
    types_match = re.search(r'types?\s+of\s+(\b[\w\s]+?)(?:\s*:|$|\n)',
                            body, re.IGNORECASE)
    if types_match:
        return types_match.group(1).strip()

    # Pattern: "X categories" -> X is root
    cat_match = re.search(r'(\b[\w\s]+?)\s+categor(?:y|ies)',
                          body, re.IGNORECASE)
    if cat_match:
        return cat_match.group(1).strip()

    # Pattern: "Classification of X" -> X is root
    class_match = re.search(r'classification\s+of\s+(\b[\w\s]+?)(?:\s*:|$|\n)',
                            body, re.IGNORECASE)
    if class_match:
        return class_match.group(1).strip()

    return None


# =============================================================================
# FUNCTION 7: suggest_visual_type
# =============================================================================

def suggest_visual_type(body: str) -> Dict[str, Any]:
    """
    Comprehensive analysis combining all detectors to suggest the best
    visual type for the content.

    This function runs all structure analysis functions and uses their
    results to recommend the most appropriate visual type.

    Visual Type Mapping:
    - High bullet count (4+) + comparison -> TABLE
    - Sequential markers -> FLOWCHART
    - Binary comparison -> KEY_DIFFERENTIATORS
    - Hierarchical structure -> HIERARCHY
    - Time-based sequence -> TIMELINE
    - Range/scale data -> SPECTRUM
    - Complex decision logic -> DECISION_TREE

    Args:
        body: The slide body text to analyze

    Returns:
        Dictionary containing:
        - primary_suggestion: VisualType
        - confidence: float (0-1)
        - secondary_suggestions: List[Tuple[VisualType, float]]
        - analysis: {
            bullet_count: int,
            is_comparison: bool,
            is_sequential: bool,
            is_hierarchical: bool,
            density_score: float
        }
    """
    result = {
        'primary_suggestion': VisualType.NONE,
        'confidence': 0.0,
        'secondary_suggestions': [],
        'analysis': {
            'bullet_count': 0,
            'is_comparison': False,
            'is_sequential': False,
            'is_hierarchical': False,
            'density_score': 0.0
        }
    }

    if not body or not body.strip():
        return result

    # Run all analyses
    bullet_count = count_bullet_points(body)
    list_patterns = detect_list_patterns(body)
    comparison = identify_comparison_structure(body)
    sequential = detect_sequential_markers(body)
    density = analyze_information_density(body)
    hierarchical = detect_hierarchical_structure(body)

    # Store analysis results
    result['analysis'] = {
        'bullet_count': bullet_count,
        'is_comparison': comparison['is_comparison'],
        'is_sequential': sequential['is_sequential'],
        'is_hierarchical': hierarchical['is_hierarchical'],
        'density_score': density['density_score']
    }

    # Score each visual type
    scores: Dict[VisualType, float] = {}

    # TABLE scoring
    table_score = 0.0
    if comparison['is_comparison'] and bullet_count >= 4:
        table_score += 0.9
    elif comparison['is_comparison']:
        table_score += 0.6
    if bullet_count >= 4 and density['density_score'] >= 0.6:
        table_score += 0.3
    if list_patterns['has_bulleted_list'] and density['unique_concepts'] >= 4:
        table_score += 0.2
    scores[VisualType.TABLE] = min(1.0, table_score)

    # FLOWCHART scoring
    flowchart_score = 0.0
    if sequential['is_sequential'] and sequential['sequence_type'] == 'process':
        flowchart_score += 0.8
    elif sequential['is_sequential'] and sequential['sequence_type'] == 'steps':
        flowchart_score += 0.7
    if sequential['step_count'] >= 3:
        flowchart_score += 0.2
    # Check for mechanism/action keywords
    body_lower = body.lower()
    if 'mechanism' in body_lower or 'action' in body_lower or 'pathway' in body_lower:
        flowchart_score += 0.3
    scores[VisualType.FLOWCHART] = min(1.0, flowchart_score)

    # KEY_DIFFERENTIATORS scoring
    keydiff_score = 0.0
    if comparison['is_comparison'] and comparison['comparison_type'] == 'binary':
        keydiff_score += 0.7
    if len(comparison['comparison_items']) == 2:
        keydiff_score += 0.3
    # Check for discrimination keywords
    if any(kw in body_lower for kw in ['differentiate', 'distinguish', 'key difference']):
        keydiff_score += 0.3
    scores[VisualType.KEY_DIFFERENTIATORS] = min(1.0, keydiff_score)

    # HIERARCHY scoring
    hierarchy_score = 0.0
    if hierarchical['is_hierarchical']:
        hierarchy_score += 0.6
    if hierarchical['levels_detected'] >= 3:
        hierarchy_score += 0.3
    if list_patterns['list_depth'] >= 2:
        hierarchy_score += 0.2
    if hierarchical['root_concept']:
        hierarchy_score += 0.1
    scores[VisualType.HIERARCHY] = min(1.0, hierarchy_score)

    # TIMELINE scoring
    timeline_score = 0.0
    if sequential['is_sequential'] and sequential['sequence_type'] == 'timeline':
        timeline_score += 0.8
    # Check for time-related keywords
    time_keywords = ['year', 'month', 'week', 'day', 'period', 'era', 'phase',
                     'early', 'late', 'progression', 'development']
    time_matches = sum(1 for kw in time_keywords if kw in body_lower)
    timeline_score += min(0.4, time_matches * 0.1)
    scores[VisualType.TIMELINE] = min(1.0, timeline_score)

    # SPECTRUM scoring
    spectrum_score = 0.0
    spectrum_keywords = ['spectrum', 'range', 'continuum', 'scale', 'mild',
                         'severe', 'low', 'high', 'gradient', 'degree']
    spectrum_matches = sum(1 for kw in spectrum_keywords if kw in body_lower)
    spectrum_score = min(0.9, spectrum_matches * 0.2)
    scores[VisualType.SPECTRUM] = spectrum_score

    # DECISION_TREE scoring
    dtree_score = 0.0
    decision_keywords = ['if', 'then', 'else', 'based on', 'depending',
                         'choose', 'select', 'determine', 'assess']
    decision_matches = sum(1 for kw in decision_keywords if kw in body_lower)
    dtree_score = min(0.8, decision_matches * 0.15)
    # Boost if multiple branching indicators
    if re.search(r'\bif\b.*\bthen\b', body_lower):
        dtree_score += 0.3
    scores[VisualType.DECISION_TREE] = min(1.0, dtree_score)

    # Find primary and secondary suggestions
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Filter out scores below threshold
    significant_scores = [(vt, sc) for vt, sc in sorted_scores if sc >= 0.3]

    if significant_scores:
        result['primary_suggestion'] = significant_scores[0][0]
        result['confidence'] = significant_scores[0][1]
        result['secondary_suggestions'] = significant_scores[1:4]  # Top 3 alternatives

    return result


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def analyze_slide_content(slide: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to analyze a full slide dictionary.

    Args:
        slide: Slide dictionary with 'body' and optionally 'header' keys

    Returns:
        Full analysis including visual suggestion
    """
    body = slide.get('body', '')
    header = slide.get('header', slide.get('title', ''))

    # Combine header and body for analysis
    full_content = f"{header}\n{body}" if header else body

    suggestion = suggest_visual_type(full_content)

    return {
        'slide_number': slide.get('slide_number'),
        'title': header,
        'visual_suggestion': suggestion['primary_suggestion'].value,
        'confidence': suggestion['confidence'],
        'alternatives': [
            {'type': vt.value, 'confidence': conf}
            for vt, conf in suggestion['secondary_suggestions']
        ],
        'analysis': suggestion['analysis']
    }


# =============================================================================
# TEST RUNNER
# =============================================================================

if __name__ == "__main__":
    # Test cases for each function
    print("=" * 60)
    print("CONTENT STRUCTURE ANALYZER - TEST SUITE")
    print("=" * 60)

    # Test 1: count_bullet_points
    print("\n--- Test 1: count_bullet_points ---")
    test_body_1 = """* First item
* Second item
* Third item
  - Nested item
* Fourth item"""
    print(f"Input:\n{test_body_1}")
    print(f"Bullet count: {count_bullet_points(test_body_1)}")

    # Test 2: detect_list_patterns
    print("\n--- Test 2: detect_list_patterns ---")
    test_body_2 = """1. First step
2. Second step
   a. Sub-step
   b. Another sub-step
3. Third step"""
    print(f"Input:\n{test_body_2}")
    print(f"List patterns: {detect_list_patterns(test_body_2)}")

    # Test 3: identify_comparison_structure
    print("\n--- Test 3: identify_comparison_structure ---")
    test_body_3 = """ACE-I vs ARBs:
* ACE-I: Block conversion
* ARBs: Block receptor
* ACE-I: May cause cough
* ARBs: No cough side effect"""
    print(f"Input:\n{test_body_3}")
    print(f"Comparison: {identify_comparison_structure(test_body_3)}")

    # Test 4: detect_sequential_markers
    print("\n--- Test 4: detect_sequential_markers ---")
    test_body_4 = """Step 1: Verify the order
Step 2: Check patient ID
Step 3: Review allergies
Step 4: Prepare medication
This leads to proper administration."""
    print(f"Input:\n{test_body_4}")
    print(f"Sequential: {detect_sequential_markers(test_body_4)}")

    # Test 5: analyze_information_density
    print("\n--- Test 5: analyze_information_density ---")
    test_body_5 = """Digoxin (Lanoxin) is a cardiac glycoside used for heart failure.
Mechanism: Inhibits Na+/K+ ATPase pump
Effects: Positive inotropic, negative chronotropic
Toxicity: Yellow-green halos, nausea, bradycardia
Antidote: Digibind (digoxin immune fab)"""
    print(f"Input:\n{test_body_5}")
    print(f"Density: {analyze_information_density(test_body_5)}")

    # Test 6: detect_hierarchical_structure
    print("\n--- Test 6: detect_hierarchical_structure ---")
    test_body_6 = """Types of Beta Blockers:
* Cardioselective
  - Metoprolol
  - Atenolol
* Non-selective
  - Propranolol
  - Nadolol
* Alpha/Beta combination
  - Carvedilol
  - Labetalol"""
    print(f"Input:\n{test_body_6}")
    print(f"Hierarchical: {detect_hierarchical_structure(test_body_6)}")

    # Test 7: suggest_visual_type
    print("\n--- Test 7: suggest_visual_type ---")
    test_bodies = [
        ("Comparison", test_body_3),
        ("Sequential", test_body_4),
        ("Hierarchical", test_body_6),
        ("Dense Info", test_body_5),
    ]

    for name, body in test_bodies:
        result = suggest_visual_type(body)
        print(f"\n{name}:")
        print(f"  Primary: {result['primary_suggestion'].value} "
              f"(confidence: {result['confidence']:.2f})")
        if result['secondary_suggestions']:
            alts = ", ".join([f"{vt.value}({c:.2f})"
                             for vt, c in result['secondary_suggestions']])
            print(f"  Alternatives: {alts}")

    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)
