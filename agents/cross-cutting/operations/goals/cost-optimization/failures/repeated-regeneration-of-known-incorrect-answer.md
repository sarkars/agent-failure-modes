# Repeated Regeneration of Known-Incorrect Answer

## Issue: Agent Has No Negative-Cache/Failure-Memory, So It Regenerates and Re-Serves an Answer Already Confirmed Wrong When the Same or a Similar Question Recurs

**Frequency**: Common

**Symptoms**
- The same factual error is produced again for a question the agent (or a prior user) already got corrected on
- User-correction or downstream-validation-failure signals are logged but never fed back into anything the agent consults before answering again
- Support/QA teams recognize "we already told the bot this was wrong" as a recurring complaint category
- Full-price generation is spent recomputing an answer that a cheap lookup against known-wrong answers would have flagged in advance

**Root Cause**
Standard response caching (see [Caching Failures](../../cost-efficiency/failures/caching-failures.md)) is built to serve known-good answers faster and cheaper on repeat questions, but almost no equivalent exists for known-bad answers: when a user correction, a downstream validation failure, or a human review flags a specific answer as wrong, that signal is rarely written back into any store the generation pipeline checks before answering the same or a semantically similar question again. Each recurrence is treated as fresh, so the agent burns a full-price generation call re-deriving the same already-falsified answer, and repeats the customer-facing failure a second (or third, or tenth) time.

**Example**
```
Week 1: Customer asks "Does my Pro plan include API access?"
Agent answers: "No, API access is only available on the Enterprise plan."
Customer replies: "That's wrong, I have API access on Pro right now."
Support agent confirms in the ticket: Pro plan DOES include API access;
the agent's answer was incorrect (based on stale pricing-page data).

The correction is logged in the support ticket system. It is never
written to any store the agent's generation pipeline consults.

Week 3: A different customer asks the same question in different words:
"Is API access part of the Pro tier?"
Agent regenerates from the same stale source data:
"No, API access is only available on Enterprise."

Result: Full-price generation call spent reproducing an answer already
confirmed incorrect two weeks earlier, and the same customer-facing
error recurs, this time to a second customer.
```

**Contributing Factors**
- Correction/feedback signals live in a support ticketing or QA system entirely separate from the generation or caching pipeline
- No negative-cache or "known-bad-answer" store exists alongside the positive response cache
- Semantic similarity matching, where it exists, is applied only to decide cache hits for reuse, not to check "does this resemble a question we already got wrong"
- No process converts an individual correction into an update to the underlying source data (e.g., the stale pricing page) that caused the wrong answer in the first place

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent answers from a source (document, database, or model knowledge) that is currently stale/incorrect on a specific fact
- A user has already corrected the agent on this exact fact, and the correction is logged in a ticketing/QA system
- No negative-cache or feedback-loop mechanism connects that correction back to the generation pipeline

### Trigger Mechanism
1. Ask the agent a question that triggers the known-stale answer; capture the response
2. Simulate/log a user correction identifying the response as wrong (as would happen in production)
3. Ask the agent a semantically similar (but differently worded) version of the same question and check whether the same incorrect answer is regenerated

**Example Reproduction Steps:**
```
1. Ask: "Does my Pro plan include API access?" and capture the answer
2. Record a correction: the answer was wrong, Pro does include API access
3. Confirm the correction is stored only in the ticketing/QA system, not
   fed back to the generation/caching pipeline
4. Ask a paraphrased version: "Is API access part of the Pro tier?"
5. Compare the new answer against the previously-corrected wrong answer
6. Measure whether the same incorrect claim is reproduced despite the
   logged correction existing in an adjacent system
```

### Expected Failure State
- The paraphrased question reproduces the same incorrect claim as the original, already-corrected answer
- No negative-cache lookup or correction-check intercepts the second occurrence before generation
- The correction recorded in the ticketing system had zero effect on subsequent agent behavior for the same fact
- Full generation cost is paid a second time to reproduce an answer already known, by the system's own prior interaction, to be wrong

---

## Mitigation Strategies

### Prevention
1. **Negative-cache layer alongside the positive response cache**: Maintain a store of question-embedding-to-known-wrong-answer pairs, populated whenever a correction, downstream validation failure, or human review flags a specific answer as incorrect; check incoming questions against this store (using the same semantic-similarity matching as the positive cache) before generation, and if a close match is found, avoid regenerating the same claim and instead flag for review or route to a corrected source. Trade-off: the negative-cache lookup adds a similarity-search step to every request, and an overly broad similarity threshold risks false-positive suppression of answers that are actually correct for a subtly different question.
2. **Correction-to-source-data feedback loop**: Since the root cause is frequently a stale underlying source (as in the pricing-page example), route confirmed corrections back to whoever owns the source data with the specific fact and its correction, closing the loop at the data level rather than only at the individual-answer level; this fixes the root cause so future paraphrases never hit the negative cache in the first place. Trade-off: requires an owner and process for source-data updates, which may lag behind the immediate need to suppress the wrong answer.
3. **Confidence downgrade on negative-cache proximity**: Even when a question doesn't exactly match a known-wrong answer but falls within a looser similarity band, downgrade the agent's confidence and prompt it to hedge or verify against a fresher source rather than answering with full confidence from unreviewed generation. Trade-off: over-broad downgrading increases hedging/caveat noise for genuinely distinct questions that happen to be lexically similar to a previously-wrong one.

### Detection & Response
1. **Repeated-error-after-correction tracking**: Explicitly track cases where a correction was logged for a specific fact and the same or a paraphrased version of the incorrect claim reappears afterward; a nonzero rate here is a direct, unambiguous signal that the negative-cache/feedback-loop is missing or not being consulted.
2. **Correction-to-generation-pipeline latency**: Measure the time between a correction being logged and it becoming enforceable (i.e., available in the negative-cache lookup); a correction that takes weeks to become effective leaves a wide window for repeat failures.
3. **Negative-cache-hit-without-suppression audit**: If a negative cache exists, periodically sample cases where a new question was similar enough to a known-wrong answer to register a near-match, and confirm whether the suppression/flagging action actually fired; a gap here indicates the cache exists but isn't wired into the generation decision.

### Architecture Patterns
1. **Feedback-adaptive cache**: Extend the existing semantic response cache so that a client- or reviewer-reported error on a cached (or freshly generated) response triggers an update — either invalidating the entry or converting it into a negative-cache entry — rather than leaving corrections to live only in a separate ticketing system, directly closing the loop between user feedback and future generation. Deployment consideration: requires a reliable signal path from wherever corrections are recorded (support tickets, QA review, thumbs-down) back into the caching layer.
2. **Two-tier cache: positive reuse and negative suppression**: Run both a standard semantic cache for known-good answers and a parallel negative-cache for known-bad ones, checking both on every request; a positive-cache hit serves the cached good answer, a negative-cache hit blocks direct generation and routes to a "verify before answering" path instead. Deployment consideration: needs clear precedence rules for the (hopefully rare) case where a question is close to both a good and a bad cached entry.
3. **Source-of-truth staleness detection tied to corrections**: When a correction is logged, automatically flag the specific source document/database field that produced the wrong answer as "disputed" until a human confirms and updates it, so any other agent path reading that same source is warned rather than silently propagating the same stale fact through a different question phrasing. Deployment consideration: requires traceability from a generated answer back to the specific source fields it drew from.

### Metrics
1. **repeated_error_after_correction_rate**: Target 0% of confirmed-wrong facts reappear in a subsequent answer; Alert if > 0% within 30 days of the original correction.
2. **correction_to_enforcement_latency**: Target < 24 hours from correction logged to negative-cache entry active; Alert if > 7 days.
3. **negative_cache_hit_rate**: Target > 80% of questions matching a known-wrong fact are caught before generation, once the negative cache is populated; Alert if < 30%.
4. **source_data_staleness_open_incidents**: Target < 5 open "disputed" source facts at any time; Alert if > 20.

### Alerts
1. **Repeated-Confirmed-Error** (P1): Condition - a fact already confirmed wrong via correction reappears in a new answer. Action: immediately suppress further generation from the same source field, escalate for a source-data fix, and backfill the negative cache with the paraphrase that slipped through.
2. **Correction-Enforcement-Lag** (P2): Condition - correction_to_enforcement_latency exceeds 7 days for an open correction. Action: check whether the feedback-adaptive cache pipeline is running or backlogged.

## References

- [Generative Caching for Structurally Similar Prompts and Responses](https://www.microsoft.com/en-us/research/wp-content/uploads/2025/09/GenCache_NeurIPS25.pdf) - Microsoft Research (NeurIPS 2025), on adapting a cache when client feedback indicates a cached/generated response resulted in an error
- [Semantic Caching for LLMs: How to Measure Latency, Cost, and Quality Before You Optimize](https://medium.com/@mohantaastha/semantic-caching-for-llms-how-to-measure-latency-cost-and-quality-before-you-optimize-64ff73b0f370) - false-positive/incorrect-hit-rate monitoring as a safety metric for semantic caches, applicable to negative-cache design
- [Related Pattern: Caching Failures](../../cost-efficiency/failures/caching-failures.md) - the positive-cache counterpart; this pattern is the missing negative-cache/failure-memory half of the same caching architecture
