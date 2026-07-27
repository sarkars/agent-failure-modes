# What Are the Most Common Output Verification Failures in AI Agents?

**Agents perform "verification" by re-querying the same upstream data source that provided the initial answer, so when the upstream source is stale, corrupted, or incorrect, re-querying returns the same wrong value — the agent reports "verified correct" with false confidence, and downstream systems trust the verified output and propagate the error.** True verification requires an independent data source; circular validation only confirms consistency, not correctness.

## Key Takeaways

- Self-verification using the same source creates circular validation — if the upstream source is wrong, re-checking against the same source returns the same wrong answer, falsely increasing confidence rather than catching the error.
- Verification failures concentrate in multi-system architectures where different systems own different subsets of truth (EHR system, ticketing system, contract-management system) and no single authoritative source exists — the agent verifies against one system without awareness that another system is the real authority.
- The reliable fix is to route verification through an independent data source (an authoritative master record, a second reference system, a live business rule engine) rather than the original source — architectural separation of verification source from primary source is non-negotiable.
- Detection is hard because the verification report itself looks authoritative — a downstream system reading "verified: sector is Industrials" has no way to know the verification was circular.

## Scope

- **Circular verification through same source** — [self-verification-cannot-catch-upstream-errors](failures/self-verification-cannot-catch-upstream-errors.md). Agent checks extracted value against same system that returned it; finds no discrepancy because source hasn't changed; reports false confidence.

## When Output Verification Matters

- Agent's output feeds downstream systems that act without independent re-verification (portfolio reporting, EHR clinical decision support, contract-obligation tracking, deployment automation)
- Multiple systems-of-record exist for the same domain (EHR is live, warehouse is stale; contract repo is cached, amendment history is separate) and the agent may verify against the wrong one
- Verification failures result in false positives (false confidence in wrong data), not false negatives — they're harder to detect because the error doesn't surface as a validation failure; the wrong data just propagates downstream

## Cross-Pattern Insight

Every documented case of verification failure follows the same pattern: the agent verified against Source A (the original source), but Source B (an independent authoritative source) contained the correct value. The fix in every case was to route verification through an independent source. Cases where verification queries a different source from the one that provided the initial answer consistently catch errors that circular verification misses. Architectural separation is the universal mitigation.

## Frequently Asked Questions

### How does output verification differ from output accuracy failures?
Output accuracy failures cover hallucination, fabrication, and confident-wrong-answers where the agent generates content not supported by any source. Output verification covers validation of already-extracted values — the agent is checking content it already has, not generating new content. See [Output Accuracy](../output-accuracy/) for fabrication and hallucination patterns.

### How should confidence scores be used in verification?
Confidence scores don't correlate with verification correctness — a model can be highly confident when re-checking a source because it sees the same value again (consistency breeds confidence) regardless of whether the source itself is wrong. Verification confidence reflects consistency, not correctness. You need an independent source, not a higher confidence threshold.

### Can you catch circular verification by comparing multiple verification runs?
Comparing multiple queries against the same source detects whether the source is changing (drift detection) but not whether the source is wrong. If a source is consistently wrong, multiple queries against it will consistently return the wrong value. You need a second, independent source to catch systematic source errors.

### What systems should be used as independent verification sources?
Authoritative master data stores (regulatory reference databases, official exchange-holiday calendars, system-of-record databases), external validation services (GICS classification for sectors, official government registries), or business-rule engines that encode business logic independently from the queried system. Anything that doesn't derive its authority from the same source you're verifying against.

## Patterns

| Pattern | Mechanism |
|---------|-----------|
| [Self-Verification Cannot Catch Upstream Errors](failures/self-verification-cannot-catch-upstream-errors.md) | Agent queries same source twice to verify; finds no discrepancy because source itself is stale/wrong, not the agent's extraction |

**Total: 1 pattern**

## Related Goals

- [Output Accuracy](../output-accuracy/) — hallucination and fabrication, contrasted with extraction-from-correct-source scenarios
- [Verification](../verification/) — test-time evaluation and validation, upstream of production verification
- [Evaluation Reliability](../evaluation-reliability/) — golden-data problems that can surface circular-verification issues in testing
