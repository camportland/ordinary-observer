# Ordinary Observer
A copyright-infringement **risk analyzer** that maps technical text-similarity
signals to the legal *"substantial similarity"* standard. This follows the
principle that infringement turns on how an *ordinary observer* perceives copied
**expression**, not shared ideas or facts.

> Research/educational project. **Not legal advice.**

## Status
In Progress - building in weekly milestones

- [X] **Week 1** - Local similarity engine (semantic, verbatim, structural). Runs offline, $0 cost
- [ ] Week 2 - Legal reasoning layer (idea vs. expression, risk scoring)
- [ ] Week 3 - Web UI + live demo
- [ ] Week 4 - Calibration, docs, polish

## What it does today
Given two text works, it computes three families of local similarity signals:

- **Semantic** - meaning-level similarity via local sentence embeddings
- **Verbatim** - literal-copying signals (n-gram overlap, longest common run, fuzzy match)
- **Structural** - whether shared content appears in the same order

The interesting part is the *gap* between them: high semantic similarity with low verbatim overlap
is the signature of paraphrase which is exactly what later milestones will weight against legal 
*protectability*.

## Run it
'''bash
python3 -m venv .venv && source ./venv/bin/activate
pip install -r requirements.txt
python3 -m oo.cli samples/a_paraphrase.txt samples/b_original.txt

### Example output
{
  "semantic": {
    "document_similarity": 0.801,
    "max_sentence_similarity": 0.7974,
    "mean_best_sentence_similarity": 0.7659
  },
  "verbatim": {
    "ngram_containment_5": 0.0,
    "ngram_containment_8": 0.0,
    "longest_common_run_words": 3,
    "fuzzy_token_set_ratio": 0.619
  },
  "structural": {
    "aligned_pairs": 3,
    "order_agreement": 1.0
  },
  "meta": {
    "len_a_chars": 232,
    "len_b_chars": 226
  }
}