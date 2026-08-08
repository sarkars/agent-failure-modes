# Incorrect Memory Recall

## Issue: Agent recalls wrong past preference or fact.

**Frequency**: Occasional

**Symptoms**
- Personalized answer contradicts known current context.
- Agent attributes one user's stated fact to a different, similar-sounding entity (wrong order, wrong past trip, wrong contact).
- Retrieval surfaces a semantically similar but factually different record, and the model treats the near-neighbor as an exact match.
- Agent blends two distinct stored facts into a single incorrect composite answer.
- The same recall query returns different facts across sessions even though no update event occurred in between.

**Root Cause**
Retrieval relies on pure vector similarity with no exact-match or provenance verification step, so when the record store contains many users with similarly phrased preferences, an embedding near-neighbor gets treated as the true match purely because it scored highest. Nothing forces the model to quote the stored record verbatim, so it paraphrases from whatever fuzzy match retrieval handed it instead of surfacing a discrepancy, and without an enforced confidence threshold, low-similarity matches pass through to generation unchallenged. Stale or partially reindexed embeddings compound the problem by leaving outdated or cross-linked vectors in place, so the same query can even return different "facts" across sessions with no update event to explain the change.

**Example**
```
User (Session 1, March): "My name is Alicia, I prefer an aisle seat and I'm flying with my toddler."
[Stored: subject=Alicia, predicate=seat_preference, object=aisle]

User (Session 2, June): "Hi, it's Alice. Can you book my usual seat for the Denver flight?"
Agent: "Sure Alice, booking your usual window seat, as requested for your solo trips."
User: "I never said window seat, and I always travel with my kid."

[Retrieval matched "Alice" against the embedding-nearest record for "Alicia" (high
semantic similarity, no exact-provenance check), pulling in a different customer's
seat preference and travel-companion fact.]
```

**Contributing Factors**
- Retrieval relies on pure vector similarity without an exact-match or provenance verification step, so near-duplicate names/entities collide.
- High density of similar records (many users with similarly phrased preferences) increases the odds of an embedding near-neighbor being mistaken for the true match.
- No verbatim citation requirement lets the model paraphrase from a fuzzy match instead of quoting the actual stored string.
- Embedding index staleness or partial reindexing leaves outdated or cross-linked vectors in place.
- Missing or unenforced confidence thresholding lets low-similarity matches through to generation.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Near-duplicate entity disambiguation | Two users with near-identical stored preferences ("Alice: window seat" vs "Alicia: aisle seat"); query recalls Alice's preference | Returns Alice's exact record | Response reflects Alicia's preference instead |
| Verbatim citation check | Query recalling a stored fact that has a source pointer | Response quotes the stored value verbatim with its source | Response paraphrases into a materially different value |
| High-stakes confirm-before-use | Recall of a payment or medical fact used to take an action | Agent restates the recalled fact and asks for confirmation before acting | Agent acts directly on the recalled value without confirmation |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| embedding_near_duplicate_confusion_rate | < 1% | Inject confusable near-duplicate record pairs into a test store and measure how often retrieval returns the wrong entity's record |
| verbatim_match_rate | > 99% | Compare the model's stated fact against the ground-truth stored string for a sample of recall-driven responses |
| confidence_gate_precision | > 95% | Of eval retrievals that pass the confidence/provenance threshold, measure the fraction that are actually the correct record |

---

## Mitigation Strategies

### Prevention
1. **Provenance-Tagged Memory Records**: Every stored fact carries source (user_stated, inferred, third_party), timestamp, and originating conversation_id. At recall time, only facts with verifiable provenance and a confidence score above threshold are eligible for injection into the prompt, reducing the chance of resurfacing an inferred or stale guess as if it were confirmed.
2. **Verbatim Citation Requirement**: When the agent uses a recalled fact in a response, it must quote the stored record verbatim (with its source pointer) rather than paraphrasing from a fuzzy embedding match. This forces retrieval to return the actual stored string instead of a semantically-close but factually different neighbor.
3. **Confirm-Before-Use for High-Stakes Recall**: For consequential recalls (payment details, medical/legal facts, safety-critical preferences), the agent restates the recalled fact and asks for confirmation before acting on it, catching retrieval errors before they affect the user.

### Detection & Response
1. **Recall-vs-Ground-Truth Sampling**: Periodically replay stored facts against the live conversation transcript that created them; compute an exact/semantic match rate between what was recalled and what was actually said. A drop in match rate signals embedding drift or index corruption. Route below-threshold sessions to human review.
2. **User Contradiction Signal**: Monitor for user utterances like "that's not right" or "I never said that" immediately following a personalized statement. Tag the preceding recall event as a suspected incorrect-recall and log the memory_id for audit.
3. **Cross-Session Consistency Check**: Run a batch job comparing facts recalled about the same user across sessions; flag entities where the recalled value diverges between two recent sessions without an intervening update event, since that indicates retrieval instability rather than a genuine preference change.

### Architecture Patterns
1. **Retrieval Confidence Gate**: Wrap the memory retrieval call in a scoring layer that returns (fact, similarity_score, provenance); the prompt-construction step only injects facts above a similarity/provenance threshold, and below-threshold facts are omitted rather than guessed.
2. **Fact Store with Source Pointers**: Store memory as structured records (subject, predicate, object, source_conversation_id, timestamp) in a queryable store, not as raw embedded text blobs, so recall can be exact-matched and audited instead of purely vector-similarity based.
3. **Recall Audit Log**: Every recall event (query, returned fact, confidence score, whether it was used in the response) is logged immutably, enabling after-the-fact analysis of recall accuracy and replay for regression testing.

### Metrics
1. **recall_accuracy_rate_percent**: Target: > 98%; Alert threshold: < 95% over rolling 24h window
2. **user_contradiction_rate_percent**: Target: < 1% of personalized responses; Alert threshold: > 2%
3. **low_confidence_recall_injection_rate_percent**: Target: 0% (facts below threshold should never be injected); Alert threshold: > 0%
4. **cross_session_fact_divergence_count**: Target: < 5 per 10k users/week; Alert threshold: > 20 per 10k users/week

### Alerts
1. **Recall Accuracy Degradation** (P2 - Warning): Condition - recall_accuracy_rate_percent falls below 95% for any 24h window. Action: Freeze embedding index updates, run root-cause diff against ground-truth transcripts, roll back to last known-good index if corruption confirmed.
2. **High-Stakes Incorrect Recall** (P1 - Critical): Condition - user contradiction detected on a confirmed high-stakes fact (payment, medical, legal) that the agent acted on. Action: Immediate human review, notify user of the error, audit downstream actions taken based on the bad recall.
3. **Confidence Gate Bypass** (P2 - Warning): Condition - any low-confidence fact injected into a response despite the gate. Action: Investigate retrieval pipeline for gate bypass bug, patch, and re-run affected sessions through the audit log.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| recall_accuracy_rate_percent | < 95% over rolling 24h window |
| user_contradiction_rate_percent | > 2% of personalized responses |
| low_confidence_recall_injection_rate_percent | > 0% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Recall Accuracy Degradation | recall_accuracy_rate_percent falls below 95% for any 24h window | Medium |
| High-Stakes Incorrect Recall | User contradiction detected on a confirmed high-stakes fact (payment, medical, legal) the agent acted on | Critical |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
