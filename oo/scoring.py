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

    #semantic similarity only counts toward risk to extent that shared material
    #is legally protectable expression
    protected_semantic=semantic*protectability

    score=round(0.6*verbatim+0.4*protected_semantic, 4)
    return {
        "score": score,
        "tier": _tier(score),
        "components": {
            "verbatim": round(verbatim, 4),
            "semantic": round(semantic, 4),
            "protectability": round(protectability, 4),
            "protected_semantic": round(protected_semantic, 4)
        }
    }