# Ordinary Observer

**🔗 Live demo: https://ordinary-observer.vercel.app/**

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
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m scripts.build_showcases

#quick local-similarity check on any two files
python3 -m oo.cli samples/a_paraphrase.txt samples/b_original.txt
```

### Example output
For the "two articles about the same event" case - nearly identical meaning, but **not** infringing, 
because overlap is unprotectable facts:

```json
{
    "id": "same_facts",
    "title": "Two articles, same event (the divergence case)",
    "expected": "LOW",
    "work_a": "Tuesday's 5.2 quake near Ridgecrest caused no injuries. Authories reported only minor damage, mainly to roadways.",
    "work_b": "A 5.2-magnitude earthquare struck near Ridgecrest on Tuesday morning. No injuries were reported, and officials said damage was limited to cracked roads.",
    "analysis": {
      "risk": {
        "score": 0.1,
        "tier": "LOW",
        "components": {
          "verbatim": 0.1,
          "semantic": 0.6472,
          "protectability": 0.05,
          "literal_pathway": 0.1,
          "nonliteral_pathway": 0.0324
        }
      },
      "similarity": {
        "semantic": {
          "document_similarity": 0.6472,
          "max_sentence_similarity": 0.699,
          "mean_best_sentence_similarity": 0.6
        },
        "verbatim": {
          "ngram_containment_5": 0.0,
          "ngram_containment_8": 0.0,
          "longest_common_run_words": 2,
          "fuzzy_token_set_ratio": 0.6264
        },
        "structural": {
          "aligned_pairs": 1,
          "order_agreement": 0.0
        },
        "meta": {
          "len_a_chars": 113,
          "len_b_chars": 152
        }
      },
      "legal": {
        "shared_elements": [
          {
            "text": "Magnitude 5.2 earthquake",
            "kind": "idea_or_fact",
            "protectable": false,
            "rationale": "Objective seismological fact; facts are not copyrightable regardless of who reports them first."
          },
          {
            "text": "Location near Ridgecrest",
            "kind": "idea_or_fact",
            "protectable": false,
            "rationale": "Geographic fact about the event; no expressive originality."
          },
          {
            "text": "Occurred on Tuesday",
            "kind": "idea_or_fact",
            "protectable": false,
            "rationale": "Temporal fact. Work A also omits 'morning,' showing independent condensation."
          },
          {
            "text": "No injuries reported",
            "kind": "idea_or_fact",
            "protectable": false,
            "rationale": "Standard newsworthy fact; there are very few ways to state it, so expression merges with the idea."
          },
          {
            "text": "Damage limited/minor, confined to roads",
            "kind": "paraphrase",
            "protectable": false,
            "rationale": "Work A restates 'damage was limited to cracked roads' as 'only minor damage, mainly to roadways.' The paraphrase tracks the underlying fact rather than distinctive wording; word choice differs materially."
          },
          {
            "text": "Attribution to officials/authorities",
            "kind": "scene_a_faire",
            "protectable": false,
            "rationale": "Sourcing damage assessments to 'officials' or 'authorities' is a standard journalistic convention in disaster reporting."
          },
          {
            "text": "Inverted-pyramid ordering: magnitude/location/time, then casualties, then damage",
            "kind": "scene_a_faire",
            "protectable": false,
            "rationale": "Conventional hard-news structure for quake briefs; dictated by genre practice, not creative selection."
          },
          {
            "text": "The proper noun 'Ridgecrest' and the numeral '5.2'",
            "kind": "verbatim",
            "protectable": false,
            "rationale": "Verbatim overlap is confined to unavoidable identifiers of the underlying event; no alternative expression exists."
          }
        ],
        "protected_expression_ratio": 0.05,
        "ordinary_observer_narrative": "An ordinary reader would say these two passages report the same news, not that one copies the other's writing. Every shared element is a hard fact about a real earthquake \\u2014 magnitude, place, day, no injuries, road damage \\u2014 plus the standard news habit of crediting 'officials.' The sentences themselves are built differently: Work B uses a single flowing compound sentence with 'struck near Ridgecrest on Tuesday morning' and 'cracked roads'; Work A leads with a possessive construction ('Tuesday's 5.2 quake'), splits into two clipped sentences, and substitutes 'minor damage, mainly to roadways.' No distinctive phrase, metaphor, or unusual sequencing survives the comparison. Infringement risk is low. The main residual caution is not copyright but hot-news/misappropriation-style concerns if Work A systematically free-rides on another outlet's original reporting, and the factual drift from 'limited to cracked roads' to 'mainly to roadways' is an editorial accuracy issue rather than a similarity issue.",
        "fair_use_consideration": "Even if any protectable expression were found, fair use would weigh strongly for Work A: the use is news reporting of factual matter, the original is a thin factual news brief at the low end of the protection spectrum, the amount taken is a handful of unavoidable data points, and a condensed rewrite does not substitute for or harm the market for the original article. The condensation into a shorter brief adds modest transformative value in purpose and audience."
      },
      "works": {
        "a_chars": 113,
        "b_chars": 152
      }
    }
  }
```
High semantic similarity, low risk - the shared material is fact, not expression.

## Tech
Python - `sentence-transformers` (local, no API) - `rapidfuzz` - `numpy` - Anthropic API (cached)

## Design
Key design decisions and their rationale are logged in [DECISIONS.md](DECISIONS.md).
