from .engine import analyze
from .llm import analyze_legal
from .scoring import risk_score

def full_analysis(text_a: str, text_b: str) -> dict:
    similarity=analyze(text_a, text_b)
    legal=analyze_legal(text_a, text_b)
    risk=risk_score(similarity, legal)
    return {
        "risk": risk,
        "similarity": similarity,
        "legal": legal,
        "works": {"a_chars": len(text_a), "b_chars": len(text_b)}
    }