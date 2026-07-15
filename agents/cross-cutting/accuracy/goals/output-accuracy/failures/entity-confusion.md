# Entity Confusion

## Issue: Agent Confuses Similar Entities

**Frequency**: Common

**Symptoms**
- Attributes of one entity applied to another
- People with similar names confused
- Companies with similar names mixed up
- Products or versions conflated

**Root Cause**
Entities with similar names, contexts, or attributes can be confused, especially when context doesn't clearly disambiguate.

**Example**
```
User: "Tell me about Michael Jordan the statistician"

Agent: "Michael Jordan is famous for his incredible basketball 
career with the Chicago Bulls..."

Reality: Michael I. Jordan is a renowned statistician and ML researcher

Result: Completely wrong information about wrong person
```

## Mitigation Strategies

### Prevention
1. **Mandatory disambiguation on multi-referent names**: When a name resolves to multiple known entities (as "Michael Jordan" resolves to both the basketball player and the statistician), require the agent to ask a clarifying question or surface the qualifying context the user gave ("the statistician") rather than defaulting to the most popular referent. Trade-off: adds a round-trip for genuinely unambiguous queries where the model over-triggers disambiguation.
2. **Qualifier-anchored entity linking**: Treat user-supplied qualifiers ("the statistician," "the one at Company X," "version 2") as hard constraints on entity resolution, not soft hints that popularity/frequency can override — the example's failure is specifically that "statistician" was present in the query but ignored in favor of the more famous entity. Trade-off: requires entity-linking logic to weight explicit qualifiers above training-data frequency, which is a nontrivial ranking change.
3. **Full-identifier requirement for high-stakes lookups**: For contexts where entity confusion has real consequences (financial records, medical records, legal entities), require resolution against a unique ID rather than a name match, falling back to name-based fuzzy matching only for low-stakes conversational queries. Trade-off: unique-ID requirements add friction for casual users who only know an entity by name.

### Detection & Response
1. **Qualifier-ignored audit**: Sample responses where the user query included a disambiguating qualifier and check whether the agent's answer actually matches that qualifier (e.g., did a response to "the statistician" describe basketball) — this is a directly testable, deterministic check against the example's exact failure.
2. **Ambiguous-entity regression suite**: Maintain a test set of known ambiguous entities (shared names, similar company names, product/version pairs) and periodically run them through the agent to check disambiguation still triggers correctly as the underlying model or retrieval index changes.
3. **User-correction clustering by entity pair**: When a user corrects a wrong-entity answer, log the confused-entity pair and track recurrence; a persistent pattern on the same pair indicates a systemic disambiguation gap rather than a one-off model slip.

### Architecture Patterns
1. **Entity-linking layer with canonical IDs**: Resolve every entity mention to a canonical ID in an entity graph before generation, and pass the qualifier context into the resolution step rather than leaving disambiguation to the generation model's implicit knowledge. Deployment consideration: requires maintaining an entity graph/knowledge base with disambiguation metadata, which is nontrivial to build and keep current for open-domain entities.
2. **Clarification-gate for low-confidence resolution**: When entity-linking confidence is below threshold (multiple plausible candidates with similar scores), force a clarifying question instead of picking the top candidate silently. Deployment consideration: needs a well-calibrated confidence score from the entity linker, not just top-1 vs. top-2 margin, to avoid over-asking on genuinely clear queries.
3. **Context-anchored retrieval**: When retrieving background for an entity, bias retrieval using all qualifiers present in the query (domain, field, location) rather than retrieving by name alone. Deployment consideration: retrieval systems need qualifier-aware indexing, which is more complex than plain name-based lookup.

### Metrics
1. **qualifier_ignored_rate**: % of sampled responses where a user-supplied qualifier was present but the answer doesn't match it; target < 2%; alert if > 8%.
2. **entity_confusion_correction_rate**: User corrections attributable to wrong-entity answers per 1,000 entity-referencing queries; target < 5; alert if > 20.
3. **disambiguation_trigger_rate**: % of genuinely ambiguous queries (per regression suite) that correctly trigger clarification or qualifier-matched resolution; target > 95%; alert if < 80%.
4. **entity_link_confidence_calibration**: Correlation between entity-linker confidence score and actual resolution correctness on a labeled sample; target > 0.8; alert if < 0.5 (signals the confidence score is unreliable for gating clarification).

### Alerts
1. **Qualifier-Ignored Spike** (P2): Condition — qualifier_ignored_rate exceeds 8% over a rolling week. Action: review recent qualifier-present queries for a ranking regression in the entity linker and patch qualifier weighting.
2. **Disambiguation Regression Suite Failure** (P2): Condition — disambiguation_trigger_rate on the known-ambiguous-entity test set drops below 80% after a model or index update. Action: block the update from full rollout and investigate the entity-linking change that caused the regression.
3. **Entity Confusion Correction Cluster** (P3): Condition — entity_confusion_correction_rate exceeds 20 per 1,000 queries for a specific entity pair. Action: add an explicit disambiguation rule or canonical-entity mapping for that specific pair.

---

## References

- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Coverage of entity confusion patterns in LLM outputs
- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Academic survey on entity hallucinations in multimodal models
