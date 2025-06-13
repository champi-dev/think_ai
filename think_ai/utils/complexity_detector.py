"""Detect question complexity for dynamic token allocation."""

import re

from think_ai.utils.logging import get_logger

logger = get_logger(__name__)

# Keywords indicating complex topics
PHD_KEYWORDS = {
    # Hard sciences
    "quantum",
    "relativity",
    "thermodynamics",
    "entropy",
    "hamiltonian",
    "lagrangian",
    "differential equation",
    "tensor",
    "manifold",
    "topology",
    "homology",
    "cohomology",
    "galois",
    "riemann",
    "hilbert",
    # Philosophy
    "ontology",
    "epistemology",
    "phenomenology",
    "metaphysics",
    "dialectic",
    "hermeneutics",
    "existentialism",
    "deontology",
    "consequentialism",
    # Advanced CS
    "np-complete",
    "turing machine",
    "lambda calculus",
    "category theory",
    "type theory",
    "formal verification",
    "byzantine",
    "consensus algorithm",
    # Medicine/Biology
    "pathophysiology",
    "pharmacokinetics",
    "epigenetics",
    "proteomics",
    "neuroplasticity",
    "immunotherapy",
    "crispr",
    "methylation",
    # Economics
    "econometrics",
    "stochastic",
    "equilibrium",
    "game theory",
    "pareto",
    "nash equilibrium",
    "behavioral economics",
    "heteroskedasticity",
}

COMPLEX_KEYWORDS = {
    "explain",
    "analyze",
    "compare",
    "contrast",
    "evaluate",
    "synthesize",
    "derive",
    "prove",
    "demonstrate",
    "examine",
    "investigate",
    "critique",
    "comprehensive",
    "detailed",
    "in-depth",
    "thorough",
    "elaborate",
}

SIMPLE_PATTERNS = [
    r"^(hi|hello|hey)[\s!?]*$",
    r"^how are you",
    r"^what is your name",
    r"^who are you",
    r"^(yes|no|ok|okay|sure|thanks|thank you)[\s!?]*$",
    r"^\d+\s*[\+\-\*/]\s*\d+",  # Simple math
    r"^what time",
    r"^what day",
    r"^(can|will|do) you",
    r"^what is 2\+2",  # Common simple math
    r"^\d+\s*\+\s*\d+\s*[=?]*$",  # Any simple addition
]


def detect_complexity(question: str) -> tuple[int, str]:
    """Detect question complexity and return appropriate max tokens.

    Returns:
        Tuple of (max_tokens, complexity_level)
        - max_tokens: 100-5000 based on complexity
        - complexity_level: 'simple', 'moderate', 'complex', 'phd'

    """
    question_lower = question.lower().strip()

    # Check for simple patterns first (O(1) for each pattern)
    for pattern in SIMPLE_PATTERNS:
        if re.match(pattern, question_lower):
            return (100, "simple")

    # Word count check
    word_count = len(question.split())

    # Check for PhD-level keywords
    phd_count = sum(1 for keyword in PHD_KEYWORDS if keyword in question_lower)
    if phd_count >= 2 or (phd_count >= 1 and word_count > 20):
        return (500, "phd")  # Cap at 500 max

    # Check for complex analysis keywords
    complex_count = sum(
        1 for keyword in COMPLEX_KEYWORDS if keyword in question_lower)

    # Special handling for specific complex topics
    if any(
        word in question_lower
        for word in ["schrödinger", "schrodinger", "husserl", "navier-stokes"]
    ):
        return (500, "phd")  # Cap at 500 max

    # Check for sorting algorithm request specifically
    if re.search(
        r"(write|implement|create).*sort(ing)?\s*(algorithm|function|code)",
        question_lower,
    ):
        return (200, "moderate")

    # Multiple questions or parts
    question_marks = question.count("?")
    and_count = question_lower.count(" and ")

    # Calculate complexity score
    complexity_score = (
        word_count * 0.1
        + complex_count * 10
        + phd_count * 20
        + question_marks * 5
        + and_count * 3
    )

    # Check for "meaning of life" type questions
    if "meaning of life" in question_lower or "purpose of existence" in question_lower:
        return (350, "complex")

    # Determine token allocation (100 min, 500 max as requested)
    if complexity_score < 5:
        return (100, "simple")
    if complexity_score < 15:
        return (200, "moderate")
    if complexity_score < 30:
        return (350, "complex")
    return (500, "complex")  # Hard cap at 500 tokens
