# Ordinary Observer
A copyright-infringement **risk analyzer** that maps technical text-similarity
signals to the legal *"substantial similarity"* standard. This follows the
principle that infringement turns on how an *ordinary observer* perceives copied
**expression**, not shared ideas or facts.

> Research/educational project. **Not legal advice.**

## Status
In Progress - building in weekly milestones

- [X] **Week 1** - Local similarity engine (semantic, verbatim, structural). Runs offline, $0 cost
- [X] **Week 2** - Legal reasoning layer (idea vs. expression, risk scoring)
- [ ] Week 3 - Web UI + live demo
- [ ] Week 4 - Calibration, docs, polish

## What it does today
Given two text works (Work A = suspect/AI generated, Work B = original), it produces a **copyright-risk assessment** by combining three layers:

- **Local similarity** - semantic similarity (sentence embeddings), verbatim overlap (n-gram/longest-common-run/fuzzy), and structural alignment. Runs offline, no API.
- **Legal reasoninng** - an LLM classifies each cshared element as protectable expression vs. unprotectable idea/fact/scene-a-faire, estimates a protected-expression ratio,a dn writes an "ordinary observer" verdict. Responses are cached to disk, so the demo runs at **$0**.
- **Risk score** - a transparent, deterministic score combining the signals into a Low/Moderate/High tier, modeling infringement as the stronger of two pathways: literal copying vs. non-literal copying of protected expression.

The interesting result: **high semantic similarity != high legal risk.** Two articles about the same event are ~90% semantically similar but score LOW, because the shared material is unprotectable facts - while a paraphrase of protected prose scores higher despite little verbatim overlap. Modeling that gap is the point.

## Run it
```bash
python3 -m venv .venv && source ./venv/bin/activate
pip install -r requirements.txt
python -m scripts.build_showcases

#quick local-similarity check on any two files
python3 -m oo.cli samples/a_paraphrase.txt samples/b_original.txt
```

### Example output
```json
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
```

## Tech
Python - `sentence-transformers` (local, no API) - `rapidfuzz` - `numpy` - Anthropic API (cached)

## Design
Key design decisions and their rationale are logged in [DECISIONS.md](DECISIONS.md).
