# What Are the Most Common Handoff-Reliability Failures in Multi-Agent AI Systems?

**A multi-agent handoff loses the upstream agent's confidence signal because the handoff schema is designed to carry only a final value and a status flag, not the confidence level or methodology the upstream agent expressed in its free-text reasoning — so a downstream agent consumes a value the upstream agent explicitly flagged as low-confidence or in need of specialist review with full, unwarranted confidence.** The gap is structural: the confidence exists in the upstream agent's transcript, but the schema between agents has no field for it, so the information is invisible to any system that only reads the structured handoff record.

## Key Takeaways

- A single documented pattern, [Handoff Schema Loses Upstream Confidence Signal](failures/handoff-schema-loses-upstream-confidence-signal.md), covers handoff reliability, illustrated across financial services, healthcare, legal, and supply-chain domain examples.
- In every domain example, the upstream agent's free-text notes explicitly recommend caution (flag for specialist review, note a competing interpretation, state a wide confidence interval) — the caution is present in the transcript but absent from the structured handoff record consumed downstream.
- The mismatch is diagnosable: a downstream agent given the full upstream transcript behaves materially differently than the same agent given only the structured `{value, status}` handoff record, per the pattern's stated symptom.
- The mismatch surfaces only after the fact — when a downstream output is challenged and someone traces back through the upstream transcript to find the caveat that never made it into the schema.

## Scope

The single mechanism handoff reliability covers is **narrow handoff schemas that carry a final value and status but no confidence, methodology, or provenance field**, so a downstream agent's decision logic — built to operate on the fixed schema — has no structured path to the upstream agent's own uncertainty. See [Handoff Schema Loses Upstream Confidence Signal](failures/handoff-schema-loses-upstream-confidence-signal.md) for four worked examples: a bond maturity-date reconciliation, a diagnosis confidence handoff, a contract-ambiguity handoff, and a demand-forecast handoff.

## When Handoff Reliability Matters

- An upstream agent's output includes free-text reasoning or caveats (competing interpretations, confidence intervals, "recommend specialist review") that a downstream agent's structured input schema has no field to carry
- A pipeline's handoff record is a fixed `{value, status}` shape rather than something that can express degrees of confidence or methodology
- A downstream error is traced back to a value the upstream agent had already flagged as uncertain, but the flag never reached the downstream decision point

## Cross-Pattern Insight

The pattern's own mitigations mirror the broader coordination toolkit: handoff schema validation with explicit required fields (including confidence/methodology, not just value/status), consensus checkpoints that can catch a downstream agent proceeding on unverified state, and saga-style compensating actions if a low-confidence value turns out to be wrong. The core fix is narrower than the general tooling suggests, though — it is specifically about widening the handoff schema itself to have a place for confidence and methodology to live as structured data, not just free text the downstream agent never reads.

## Frequently Asked Questions

### Can the downstream agent just read the upstream agent's full reasoning instead?
In practice, downstream agents are built to consume a structured handoff record for reliability and parseability, not to re-parse another agent's free-text chain of reasoning. That design choice is reasonable for consistency, but it means any signal the upstream agent expressed only in prose — like a confidence caveat — is architecturally invisible to the downstream agent's decision logic.

### Is the handoff-reliability failure the same as Task Handoff Failure in the Coordination goal?
They're related but not identical. [Coordination](../coordination/)'s Task Handoff Failure describes an agent passing incomplete or incorrect state generally. Handoff reliability's pattern is more specific: the state passed is technically complete and correct (the value itself is right), but the confidence/methodology context needed to use that value safely is what's missing.

### What's the simplest fix for the handoff-schema-confidence gap?
Add explicit confidence and methodology fields to the handoff schema itself — not as an afterthought free-text field, but as structured data the downstream agent's decision logic actually branches on (for example, routing low-confidence values to human review instead of auto-processing low-confidence values with full confidence).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Handoff Schema Loses Upstream Confidence Signal](failures/handoff-schema-loses-upstream-confidence-signal.md) | Handoff schema carries only final value and status, so upstream confidence/methodology caveats never reach the downstream agent |

**Total: 1 pattern**

## Related Goals

- [Coordination](../coordination/) — the broader set of handoff and communication failures, including Task Handoff Failure and Communication Loss, that handoff reliability's pattern specializes
- [Error Propagation](../error-propagation/) — what happens next if a low-confidence value silently accepted at handoff turns out to be wrong and compounds downstream
- [Reasoning Quality](../reasoning-quality/) — a related trust failure where the problem is agents agreeing on a wrong answer rather than a confidence signal getting lost in transit
