from functools import lru_cache
from sentence_transformers import SentenceTransformer, util
from .textutils import sentences

@lru_cache(maxsize=1)
def _model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2")

def semantic_signals(text_a: str, text_b: str) -> dict:
    model=_model()

    #whole doc similarity
    doc_emb=model.encode([text_a, text_b], convert_to_tensor=True, normalize_embeddings=True)
    doc_sim=float(util.cos_sim(doc_emb[0], doc_emb[1]).item())

    #sentence similarity
    sents_a, sents_b=sentences(text_a), sentences(text_b)
    if not sents_a or not sents_b:
        return {"document_similarity": doc_sim,
                "max_sentence_similarity": doc_sim,
                "mean_best_sentence_similarity": doc_sim}

    emb_a=model.encode(sents_a, convert_to_tensor=True, normalize_embeddings=True)
    emb_b=model.encode(sents_b, convert_to_tensor=True, normalize_embeddings=True)
    sim_matrix=util.cos_sim(emb_a, emb_b) #rows are a sents, cols are b sents
    best_per_a=sim_matrix.max(dim=1).values #best b sent for each a sent

    return {"document_similarity": round(doc_sim, 4),
                    "max_sentence_similarity": round(float(best_per_a.max().item()), 4),
                    "mean_best_sentence_similarity": round(float(best_per_a.mean().item()), 4)}

