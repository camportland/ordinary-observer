import os
from typing import Literal

from anthropic import Anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

from . import cache

load_dotenv()

#bump when changing prompt to invalidate cache
PROMPT_VERSION="v1"

MODEL="claude-opus-5"

ElementKind=Literal["verbatim", "paraphrase", "idea_or_fact", "scene_a_faire"]

class SharedElement(BaseModel):
    text: str
    kind: ElementKind
    protectable: bool
    rationale: str

class LegalAnalysis(BaseModel):
    shared_elements: list[SharedElement]
    protected_expression_ratio: float
    ordinary_observer_narrative: str
    fair_use_consideration: str

SYSTEM="""You are a copyright-law analyst. You assess whether one text \
    infringes another under U.S copyright's "substantial similarity" standard.
    
    Core doctrine you must apply:
    - Copyright protects EXPRESSION, not ideas, facts, or procedures (idea-expression dichotomy).
    - Stock, genre standard elements are unprotectable (scenes a faire).
    - When there is essentially only one way to express an idea, expression meres \
    with the idea and is unprotectable (merger).
    - Infringement is judged holistically by an "ordinary observer": does the second work \
    appropriate the protectable expression of the first?

    For the two works, identify the elements they share: classify each as verbatim \
    copying, close paraphrase, shared idea/fact, or scene a faire; and mark whether \
    each is legally PROTECTABLE. Then estimate the fraction of the overlap that is \
    protectable expression (proected_expression_ratio, 0-1), write a concise \
    plain-English ordinary-observer verdict, and briefly note any obvious fair-use \
    consideration (eg. paradoy/transformative use). You assess risk; you do not give \
    legal advice."""

def analyze_legal(text_a: str, text_b: str) -> dict:
    """
    work a (suspect) vs work b (original). cached, only calls API on a miss
    """
    cached=cache.get(PROMPT_VERSION, MODEL, text_a, text_b)
    if cached is not None:
        return cached

    client=Anthropic()
    user=(
        f"WORK A (potentially infringing):\n{text_a}\n\n"
        f"WORK B (original/copyrighted):\n{text_b}"
    )
    response=client.messages.parse(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user}],
        output_format=LegalAnalysis
    )
    result=response.parsed_output.model_dump()
    cache.put(result, PROMPT_VERSION, MODEL, text_a, text_b)
    return result
