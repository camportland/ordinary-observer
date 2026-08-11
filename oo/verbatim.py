from rapidfuzz import fuzz
from .textutils import words

def _ngrams(tokens: list[str], n: int) -> set[tuple]:
    return {tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)} if len(tokens) >=n else set()

def _ngram_containment(a: list[str], b: list[str], n: int) -> float:
    """
    fraction of a's n-grams that appear in b (directional)
    """
    ga, gb=_ngrams(a,n), _ngrams(b, n)
    if not ga: 
        return 0.0
    return len(ga & gb)/len(ga)

def _longest_common_run(a: list[str], b: list[str]) -> int:
    """
    length (in words) of longest identical contiguous run
    """
    if not a or not b:
        return 0
    prev=[0]*(len(b)+1)
    best=0
    for i in range(1, len(a)+1):
        cur=[0]*(len(b)+1)
        for j in range(1, len(b)+1):
            if a[i-1]==b[j-1]:
                cur[j]=prev[j-1]+1
                best=max(best, cur[j])
        prev=cur
    return best

def verbatim_signals(text_a: str, text_b: str) -> dict:
    a, b=words(text_a), words(text_b)
    return {
        "ngram_containment_5": round(_ngram_containment(a, b, 5), 4),
        "ngram_containment_8": round(_ngram_containment(a, b, 8), 4),
        "longest_common_run_words": _longest_common_run(a, b),
        "fuzzy_token_set_ratio": round(fuzz.token_set_ratio(text_a, text_b)/100, 4)
    }