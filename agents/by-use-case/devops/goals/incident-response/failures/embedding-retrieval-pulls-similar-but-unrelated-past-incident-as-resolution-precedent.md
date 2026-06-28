# Embedding Retrieval Pulls Similar-but-Unrelated Past Incident as Resolution Precedent

## Issue: An Incident-Response Agent That Retrieves a Past Incident's Resolution Steps via Semantic Similarity Search Over Incident Descriptions, Rather Than Matching on Root-Cause Signature or Affected-Component Identity, Surfaces a Past Incident That Reads Similarly but Had a Different Underlying Cause, and Applies That Incident's Resolution Steps to the Current One

**Frequency**: Occasional

**Symptoms**
- The applied resolution steps come from a past incident whose symptom description is textually similar to the current one -- both described as "elevated latency on checkout service" -- but whose actual root cause and fix were unrelated
- The applied fix does not resolve the current incident, or resolves it only partially, because it targets a different underlying mechanism than the one actually causing the current symptoms
- Querying the incident database by affected component and metric signature, rather than by description similarity, surfaces a different past incident whose resolution steps do in fact match the current root cause
- The mismatch concentrates on generic symptom phrasing ("elevated latency," "increased error rate") that recurs across many unrelated incidents with different causes, since the similarity signal weights the generic phrasing heavily
- The agent presents the retrieved precedent's resolution steps with the same confidence as a root-cause-matched precedent, with no indication that the match was based on description similarity rather than causal-signature matching

**Root Cause**
Retrieving a resolution precedent via semantic similarity over incident descriptions optimizes for textual or topical similarity between symptom narratives, not for matching the current incident's actual root-cause signature (specific failing dependency, error code pattern, or affected subsystem). When two incidents share generic symptom language but differ in root cause, the similarity signal that drives retrieval cannot distinguish them, because the distinguishing information lives in causal-signature fields the similarity search does not weight.

**Example**
```
Current incident: checkout service showing elevated p99 latency, traced eventually to a downstream payment-gateway connection pool exhaustion
Incident-response agent queries the incident database via semantic similarity using the symptom description "elevated latency on checkout service"
Top-ranked match returned is a past incident with the same symptom description, but whose actual root cause was a database index regression introduced by an unrelated migration
Agent applies the matched incident's resolution -- rebuilding the database index -- which has no effect on the current connection-pool exhaustion
Time-to-resolution extends by the duration spent applying and verifying the irrelevant fix before root-cause analysis identifies the actual connection-pool issue
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including retrieving a topically similar but substantively wrong record when similarity search is used in place of structured-signature matching | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Multi-agent orchestration research for incident-response workflows identifies grounding resolution recommendations in structured root-cause signatures, rather than symptom-description similarity, as a distinct reliability requirement | [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755) |
| Knowledge-oriented retrieval-augmented generation surveys identify retrieval over generic, recurring symptom language as a distinct failure mode from retrieval over rare, distinguishing terms | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |

**Contributing Factors**
- Resolution-precedent retrieval is implemented over incident symptom descriptions via similarity search rather than over structured root-cause signature fields (failing dependency, error code, affected subsystem)
- No validation step confirms a retrieved precedent's root-cause signature matches the current incident's signature before its resolution steps are recommended
- Generic, recurring symptom phrasing is not down-weighted or flagged as low-discriminating in the similarity-search index

---

## Mitigation Strategies

1. **Structured Root-Cause-Signature Matching as Primary Path**: Require resolution-precedent retrieval to match on structured fields (affected dependency, error signature, subsystem identifier) first, falling back to symptom-description similarity only when no structured-signature match exists, and flagging that fallback explicitly
2. **Root-Cause Confirmation Before Applying Precedent Fix**: Require confirmation that the current incident's actual or suspected root cause matches the retrieved precedent's documented root cause before applying its resolution steps, rather than applying on symptom-description similarity alone
3. **Generic-Phrasing Down-Weighting in Retrieval Index**: Identify and down-weight generic, recurring symptom phrases in the similarity-search index so that retrieval relies more heavily on distinguishing, root-cause-specific terms
4. **Surface Retrieval Basis in Resolution Recommendation**: Require any resolution-precedent recommendation to indicate whether the match was based on structured root-cause signature or symptom-description similarity, so responders can weight their trust accordingly

### Metrics
- Rate of applied resolution-precedent recommendations whose root-cause signature does not match the current incident's eventual confirmed root cause
- Rate of resolution-precedent retrievals falling back to symptom-description similarity due to no structured-signature match
- Time-to-resolution delta between incidents resolved via structured-signature-matched precedents versus similarity-matched precedents

### Alerts
- A resolution-precedent recommendation is applied whose root-cause signature does not match the current incident's confirmed signature after the fact → P2
- Symptom-description-similarity fallback rate for resolution-precedent retrieval exceeds the defined threshold for a rolling window → P3
- An applied precedent fix produces no measurable improvement in the incident's primary symptom metric within the expected response window → P2

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
