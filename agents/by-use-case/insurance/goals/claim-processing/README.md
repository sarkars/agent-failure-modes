# What Are the Most Common Claim Processing Failures in AI Agents?

**Claim-processing agents fail in three distinct, recurring ways: a retrieval step pulls a superseded or wrong-jurisdiction policy document that looks textually similar to the correct one, a multi-agent handoff drops an exclusion or hazard flag between pipeline stages because the finding lived only in free text and never reached a structured field, and an agent answers a regulatory-deadline question from memorized pretraining knowledge instead of calling the live regulatory-requirements tool it has available.** All three patterns produce a confident, well-formed adjudication decision that is wrong in a way no downstream step catches, because each mechanism defeats a different kind of verification: similarity search defeats source-identity verification, schema-bounded handoffs defeat cross-stage information transfer, and parametric memory defeats tool-grounding. The result in every case is a claim paid, denied, or timed incorrectly — an outcome discovered only during a later audit, claw-back, or compliance review, well after the payment or notice has already gone out.

## Key Takeaways

- 3 patterns are documented for claim processing, one per failure mechanism: embedding-retrieval mismatch, multi-agent handoff loss, and stale-training-corpus override.
- The embedding-retrieval pattern found a claims agent applying a $25,000 sub-limit from a superseded 2023 endorsement instead of the current $10,000 limit, a $15,000 overpayment caught only during a routine reinsurance-treaty audit three months later.
- The multi-agent-handoff pattern shows the exclusion determination was correctly reasoned by an earlier pipeline stage — the loss was never a reasoning failure, only a transfer failure at the stage boundary where free text never reached a structured field the payment agent reads.
- The stale-training-corpus pattern documents an agent using a memorized 15-business-day prompt-payment deadline after a state shortened its statute to 10 calendar days, producing a compliance violation despite a live regulatory-requirements tool being available and unused.

## Scope

- **Retrieval mismatch** — [Embedding-Retrieval Wrong Endorsement Version Applied](failures/embedding-retrieval-wrong-endorsement-version-applied.md). A RAG step ranks endorsement forms by textual similarity across a document store holding multiple historical revisions, and returns the wrong revision because boilerplate language dominates the embedding while the revision date does not.
- **Handoff information loss** — [Multi-Agent Handoff Drops Noted Exclusion Before Payment Step](failures/multi-agent-handoff-drops-noted-exclusion-before-payment-step.md). An earlier pipeline stage's own reasoning identifies a disqualifying exclusion, but the finding lives only in free text and never reaches the structured field the payment agent actually consults.
- **Stale parametric override** — [Stale Training-Corpus Prompt-Payment Deadline Overrides Current State Statute](failures/stale-training-corpus-prompt-payment-deadline-overrides-current-state-statute.md). An agent answers a jurisdiction-specific deadline question from pretraining-era general knowledge instead of the live regulatory-requirements tool it has available.

## When Claim Processing Matters

- A claims pipeline spans multiple agent stages (intake, triage, adjudication, payment) with each stage bounded to its own context window and structured output contract
- A carrier's document store or endorsement library contains multiple historical or near-duplicate versions of the same policy language
- A claim's jurisdiction has state-specific, independently amendable statutory deadlines that a general-purpose model may have memorized in an outdated form

## Cross-Pattern Insight

Every claim-processing pattern documented here shares a single structural gap: the claims agent treats a plausible-looking signal — a high-similarity retrieved clause, a structured field with no exclusion flag, a fluently-stated deadline — as sufficient grounds for a payment decision, without an independent, deterministic check against the actual source of truth. The fix is architecturally identical across all three: gate the decision on a verification step that does not depend on the same mechanism that produced the error, whether that is a declarations-schedule cross-check, a mandatory structured exclusion field with reconciliation against upstream free text, or a forced regulatory-tool call with provenance logging.

## Frequently Asked Questions

### What causes a claims-adjudication agent to apply the wrong coverage terms?
Most commonly, a retrieval step selects a policy endorsement or clause by embedding similarity rather than by a deterministic match on form number and effective date, so a superseded or wrong-jurisdiction version with near-identical boilerplate gets applied instead of the version actually attached to the policy. See [Embedding-Retrieval Wrong Endorsement Version Applied](failures/embedding-retrieval-wrong-endorsement-version-applied.md).

### How do you stop an exclusion from disappearing between claims pipeline stages?
Require every pipeline stage to emit a structured exclusion field, even when empty, and block the handoff to the next stage if the field is missing rather than inferring an exclusion from prose. See [Multi-Agent Handoff Drops Noted Exclusion Before Payment Step](failures/multi-agent-handoff-drops-noted-exclusion-before-payment-step.md).

### Can a claims agent be trusted to know current state prompt-payment deadlines on its own?
No. State prompt-payment statutes are independently and frequently amended, and a general-purpose model's memorized sense of "typical" deadlines will not reflect a recent amendment; the reliable fix is a forced regulatory-tool-call gate before any deadline is set, not improved memorization. See [Stale Training-Corpus Prompt-Payment Deadline Overrides Current State Statute](failures/stale-training-corpus-prompt-payment-deadline-overrides-current-state-statute.md).

### Is claim-processing the same goal as claims-processing?
No, despite the near-identical name. Claim Processing documents three agentic-mechanism failures (retrieval mismatch, handoff loss, stale-corpus override) in a claims-adjudication pipeline, while [Claims Processing](../claims-processing/) documents a single, differently-scoped pattern about catastrophe-correlation blindness in reserve modeling — an actuarial assumption failure rather than an agent-mechanism failure. The overlap is in name only; a human maintainer may want to rename one folder to avoid confusion, since the content does not overlap.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Embedding-Retrieval Wrong Endorsement Version Applied](failures/embedding-retrieval-wrong-endorsement-version-applied.md) | RAG retrieval ranks endorsement forms by textual similarity, returning a superseded revision with different sub-limits |
| [Multi-Agent Handoff Drops Noted Exclusion Before Payment Step](failures/multi-agent-handoff-drops-noted-exclusion-before-payment-step.md) | An upstream stage's free-text exclusion finding never reaches the structured field the payment agent reads |
| [Stale Training-Corpus Prompt-Payment Deadline Overrides Current State Statute](failures/stale-training-corpus-prompt-payment-deadline-overrides-current-state-statute.md) | Agent answers a jurisdiction-specific deadline from memorized knowledge instead of calling the live regulatory tool |

**Total: 3 patterns**

## Related Goals

- [Claims Processing](../claims-processing/) — same-sounding name, but documents a distinct actuarial reserve-modeling failure rather than an agentic-mechanism failure
- [Fraud Detection](../fraud-detection/) — the same three mechanism clusters recur in SIU referral and fraud-screening workflows
- [Policy Management](../policy-management/) — the same three mechanism clusters recur in renewal and endorsement-servicing workflows
