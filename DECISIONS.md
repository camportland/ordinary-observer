# Design Decisions

A running log of non-obvious choices and why I made them :)

## 1. Risk scoring: max of two pathways, not a verbatim-weighted sum

**Date:** 08/12/26

**Context.** The first scoring model was a weighted sum: 
`0.6 x verbatim + 0.4 x (semantic x protectability)`.

**Problem.** On the curated case set, an AI-paraphrase case (an LLM rewording of
protected fictional prose) scored 0.195 -> LOW when it should be MODERATE. Because
verbatim carried 60% of the weight and paraphrase has ~0 verbatim overlap, the
formula structurally capped paraphrase risk at ~0.43 eveen with perfect protectatbility.
That's backwards: paraphrase is exactly the generative-AI copyright risk this tool
exitsts to catch.

**Decision.** Reframed risk as the **max of two infringemenet pathways**, mirroring
copyright law (you infringe via literal copying OR non-literal copying of protected
expression):
- `literal = verbatim`
- `nonliteral = semantic x protectability`
- `risk = max(liternal, nonliteral)`

**Result.** ALL three showcase tiers now match expectations, and the thesis case (same
facts -> LOW despite high semanitc similarity) still holds, because facts have low
protectability.

**Known limitation.** The `literal` pathway isn't scaled by protectability, so verbatim
copying of *unprotectable facts* (cf. *Fiest v. Rural*) would over-flag. Left simple
deliberately, noted as future work.

## 2. Fair use is flagged, not scored

**Date:** 08/17/26

**Context.** The parody case scored MODERATE (nonliteral pathway 0.47), not LOW.

**Why that's correct.** Parody copies real protectable expression - the risk score
measures *sustantial similarity* (the prima facie copying), which is high here. What
makes parody non-infriging is *fair use*, a separate legal defense.

**Decision.** The risk score answers only "did this copy protected expression?" Fair
use is surfaced as a **flag** (`legal.fair_use_consideration`), not folded into the
score. Rationale: fair use is the least predictable area of copyright law; an automated
tool that quietly decided it would be over-claiming. Better to flag the consideration
and leave the judgement to a human.

## 3. Static frontend, no backend

**Date:** 08/27/26

**Context.** The web app is a Next.js site that reads a pre-computed `showcases.json`; there is no server or database. All LLM analysis happens offline at build time and is cached into the repo.

**Rationale.** A governance tool that's expensive or fragile to run doesn't get adopted. Serving static, pre-computed results means the demo is always up, costs $0 to host, and needs no API key - anyone can clone and run it! The tradeoff is no live "analyze arbitrary text" mode in the deployed site; that's deferred to an optional local/bring-your-own-key mode (Week 4).