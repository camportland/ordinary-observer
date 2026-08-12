def _tier(score: float) -> str:
    if score>=0.66:
        return "HIGH"
    if score>=0.33:
        return "MODERATE"
    return "LOW"

def risk_score(similarity: dict, legal: dict) -> dict:
    """
    combine week 1 similarity signals with LLM's protectatbility judgement
    """
    verbatim=max(
        similarity["verbatim"]["ngram_containment_5"],
        min(similarity["verbatim"]["longest_common_run_words"]/20.0, 1.0)
    )
    semantic=similarity["semantic"]["document_similarity"]
    protectability=max(0.0, min(legal["protected_expression_ratio"], 1.0))

    #two independent infringement pathways (see DECISIONS.md #1)
    literal=verbatim #copied word-sequences
    nonliteral=semantic*protectability # reworded, but copies protected expression
    score=round(max(literal, nonliteral), 4)

    return {
        "score": score,
        "tier": _tier(score),
        "components": {
            "verbatim": round(verbatim, 4),
            "semantic": round(semantic, 4),
            "protectability": round(protectability, 4),
            "literal_pathway": round(literal, 4),
            "nonliteral_pathway": round(nonliteral, 4)
        }
    }