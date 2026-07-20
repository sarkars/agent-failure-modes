# Knowledge Contradiction Unresolved

## Issue
An agent's retrieval step pulls two or more facts from different sources that directly contradict each other on the same question, and the agent proceeds to answer using one of them (often whichever appears first, scores marginally higher in relevance, or was retrieved last) without noticing, reconciling, or flagging the contradiction to the user. The user receives a confident single answer with no indication that the knowledge base itself disagrees on the point.

**Frequency**: Common

**Symptoms**
- Two retrieved sources present incompatible facts on the same question, and the response reflects only one
- The same query, run at different times or with slightly different phrasing, produces materially different answers because a different one of the contradicting sources was retrieved
- No hedge, caveat, or "sources disagree" language appears despite the contradiction being present in the retrieved context
- Users who separately consult both underlying sources discover the disagreement the agent never surfaced

## Root Cause
Retrieval systems are built to find and rank relevant content, not to detect logical or factual conflict between the pieces they retrieve — nothing in a standard ranking pipeline compares retrieved passages against each other for consistency, it only compares each to the query. When multiple contradicting passages land in context together, the generation step treats them as more information to synthesize, and language models are generally optimized to produce a single, coherent, confident answer rather than to explicitly represent and report unresolved disagreement between their own inputs — smoothing over a contradiction into one clean answer is often the path of least resistance, and highly rewarded by training objectives that favor fluent, decisive responses over hedged ones.

## Example
```
A user asks a company-policy agent: "How many days of remote work per
week are employees allowed?" The retrieval step pulls two documents:
an official HR policy document last revised 8 months ago stating "up to
2 days remote per week," and a more recently uploaded team-level
guidance document stating "remote work is at manager discretion, no
fixed cap" that was never reconciled against the official HR policy
when it was added to the knowledge base.

The agent's response states confidently: "Employees are allowed up to
2 days of remote work per week," citing only the HR document, with no
mention that a separate, more recent internal document describes a
different and arguably superseding policy.

An employee relying on the answer to plan their schedule follows the
2-day cap, while colleagues on other teams operating under the manager-
discretion guidance have considerably more flexibility, creating
inconsistent and confusing outcomes traceable to a contradiction the
agent silently resolved in favor of one source.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-15% of queries against knowledge bases with multiple independently-maintained sources retrieve at least two passages with a direct factual contradiction | Estimated from contradiction-audit studies of enterprise knowledge bases with overlapping documentation |
| Contradiction rates are markedly higher in knowledge bases combining centrally-maintained policy documents with team-level or user-generated content | Typical pattern observed in mixed-authority knowledge base audits |
| Adding an explicit contradiction-detection step between retrieved passages, before generation, surfaces and flags the large majority of contradictions that would otherwise be silently resolved | Reported range across teams that added pairwise consistency checks |

## Mitigations
1. **Pairwise contradiction detection**: Add an explicit step that checks retrieved passages against each other for factual contradiction (using NLI-style entailment/contradiction classification) before generation, flagging conflicts rather than passing them silently into context.
2. **Source-authority hierarchy**: Where sources have a defined authority ranking (e.g. official policy overrides team-level guidance), encode this explicitly and use it to resolve or at least prioritize contradictions rather than leaving resolution to implicit ranking-score differences.
3. **Mandatory disagreement disclosure**: When a detected contradiction cannot be authoritatively resolved, require the response to explicitly state that sources disagree and present both positions rather than silently picking one.
4. **Contradiction registry and review queue**: Log detected contradictions to a review queue for content owners to reconcile at the source (update, deprecate, or merge conflicting documents) rather than relying on per-query detection alone.
5. **Query-time reproducibility monitoring**: Track whether the same or near-identical query produces materially different answers across repeated runs, since instability driven by contradiction resolution is a strong signal of an unresolved conflict in the knowledge base.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| contradiction_detection_rate | Share of multi-source retrievals flagged for pairwise contradiction before generation | Track trend; investigate spikes and silent drops to zero |
| unresolved_contradiction_disclosure_rate | Share of detected contradictions that result in explicit disagreement disclosure in the response | Alert if < 95% |
| answer_instability_rate | Rate at which repeated/near-duplicate queries produce materially different answers | Alert if > 5% for policy/fact-lookup query types |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Contradiction silently resolved in high-stakes response | Review finds a response answered from one of two contradicting sources with no disclosure | High | Correct the response, route source pair to the contradiction review queue |
| Contradiction detection rate drop to near-zero | contradiction_detection_rate falls to near zero after a pipeline change, in a knowledge base with known overlapping sources | Medium | Audit the contradiction-detection step for a regression or disabled check |

## Related Patterns
- [Knowledge Source Reliability Unknown](./knowledge-source-reliability-unknown.md) - a missing authority hierarchy is a common root cause of contradictions going unresolved rather than adjudicated
- [Domain Exception Not Handled](./domain-exception-not-handled.md) - a general rule and its exception can be mistaken for a contradiction, or a true contradiction mistaken for an exception, without structural linking
- [Fact Timestamp Error](./fact-timestamp-error.md) - a common source of apparent contradiction is actually two time-bound facts from different valid periods, misread as conflicting rather than sequential
