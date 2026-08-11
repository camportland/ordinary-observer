from .embeddings import semantic_signals
from .verbatim import verbatim_signals
from .structural import structural_signals

def analyze(text_a: str, text_b: str) -> dict:
    """
    run all local similarity signals
    """
    return {
        "semantic": semantic_signals(text_a, text_b),
        "verbatim": verbatim_signals(text_a, text_b),
        "structural": structural_signals(text_a, text_b),
        "meta": {
            "len_a_chars": len(text_a),
            "len_b_chars": len(text_b)
        }
    }