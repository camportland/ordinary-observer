from sentence_transformers import util
from .embeddings import _model
from .textutils import sentences

def structural_signals(text_a: str, text_b: str, threshold: float=0.6) -> dict:
    sents_a, sents_b=sentences(text_a), sentences(text_b)
    if len(sents_a)<2 or len(sents_b)<2:
        return {"aligned_pairs": 0, "order_agreement": 0.0}

    model=_model()
    emb_a=model.encode(sents_a, convert_to_tensor=True, normalize_embeddings=True)
    emb_b=model.encode(sents_b, convert_to_tensor=True, normalize_embeddings=True)
    sim=util.cos_sim(emb_a, emb_b)

    #for each a sentence its best b match if above threshold
    matches=[] #(a_index, b_index)
    for i in range(len(sents_a)):
        j=int(sim[i].argmax().item())
        if float(sim[i][j].item())>=threshold:
            matches.append((i,j))

    if len(matches)<2:
        return {"aligned_pairs": len(matches), "order_agreement": 0.0}

    #order agreement: frac of matched pair orderings preserved in b
    b_order=[j for _, j in matches]
    concordant=sum(
        1 for x in range(len(b_order)) for y in range(x+1, len(b_order)) if b_order[x]<b_order[y]
    )
    total=len(b_order)*(len(b_order)-1)/2
    return {
        "aligned_pairs": len(matches),
        "order_agreement": round(concordant/total, 4) if total else 0.0
    }