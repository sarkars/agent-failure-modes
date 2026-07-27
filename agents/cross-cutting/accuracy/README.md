# What Are the Most Common Accuracy Failures in AI Agents?

**Agents generate plausible-sounding but false content, apply outdated knowledge, lose track of constraints over long conversations, deviate from reasoning requirements, and skip verification of outputs — accuracy failures are silent because the output is well-formed and the agent is confident, so errors propagate downstream before being caught.** Accuracy issues span the entire agent pipeline: context management (losing track of instructions), reasoning quality (planning incompletely), output generation (hallucination), and verification (skipping or biasing the check).

## Key Takeaways

- 66 distinct failure patterns affect accuracy across 8 goals, spanning context handling (8 patterns), evaluation methodology (8 patterns), knowledge staleness (1 pattern), generation quality (16 patterns), optimization of techniques (5 patterns), output verification (1 pattern), reasoning (12 patterns), and test-time validation (15 patterns).
- Accuracy failures are categorically invisible at generation time — a hallucinated fact reads like a true fact, a skipped verification step produces no error message, an instruction drift shows up only in subtle behavior change over many turns. Detection requires comparison to ground truth or external audit, not observation of the output itself.
- The reliable fix is multi-layered: (1) context architecture that maintains instruction durability and state tracking; (2) evidence-gating on high-stakes claims (require retrieval before generation); (3) confidence calibration and abstention affordances (let agents refuse when confidence is low); (4) multi-layered verification (format + business logic + human review); (5) comprehensive test methodology (not just happy paths).
- Accuracy failures concentrate wherever the real world is more complex than the training distribution (seasonal shifts, new entity types, adversarial inputs), where rules change faster than models can be retrained (regulatory thresholds, policy updates), or where agents must chain multiple reasoning steps correctly (multi-step planning, long-horizon reasoning).

## Goals

| Goal | Patterns | Coverage |
|------|----------|----------|
| [Context Management](goals/context-management/) | 8 | Instruction conflicts, context size limits, state tracking, session boundaries |
| [Evaluation Reliability](goals/evaluation-reliability/) | 8 | Coverage gaps, distribution shift, data quality, metric mismatch |
| [Knowledge Staleness](goals/knowledge-staleness/) | 1 | Agent defaults to training knowledge over live tools |
| [Output Accuracy](goals/output-accuracy/) | 16 | Hallucination, bias, fabrication, domain mismatch, inherited errors |
| [Output Optimization](goals/output-optimization/) | 5 | Missing abstention, confidence miscalibration, skipped verification, degenerate output |
| [Output Verification](goals/output-verification/) | 1 | Circular verification (same source checks itself) |
| [Reasoning Quality](goals/reasoning-quality/) | 12 | Planning failures, constraint violations, goal misalignment, self-correction gaps |
| [Verification](goals/verification/) | 15 | Missing verification, shallow checks, self-verification bias, methodology gaps |

**Total: 66 patterns across 8 goals**

## When Accuracy Matters

- Agent generates content that flows directly to end users or drives autonomous decisions without intermediate human review
- High-stakes domains (healthcare, finance, legal, compliance) where accuracy errors have safety, regulatory, or reputational impact
- Agent must maintain correctness over long conversations, requiring instruction durability and state tracking
- Vulnerable populations or underrepresented groups where accuracy degradation for specific segments goes undetected

## Architecture Principles for Accuracy

**The core insight across all 66 patterns:** accuracy requires architecture, not just model capability. A capable model can generate false content (hallucination), lose track of constraints (context drift), apply outdated knowledge (staleness), or be deployed without verification. The mitigations fall into three architectural categories:

1. **Context and state durability**: Keep instructions durable (separate external store, periodic re-injection), maintain state outside context window (database, external ledger), enforce session boundaries (no cross-session leakage).

2. **Evidence-gated generation**: Require retrieval or explicit evidence before generation; mark claims with sources; abstain when evidence is insufficient; evidence-gating eliminates fabrication more reliably than prompting.

3. **Verification and testing**: Make verification multi-layered (format + business logic + human sample), independent (not self-verification), and comprehensive (not just happy paths). Verify the verifier itself. Test on production distribution, not convenience samples.

## Related Categories

- [Operations](../operations/) — cost efficiency, tool reliability, and state tracking, upstream of accuracy
- [Security](../security/) — preventing adversarial attacks and prompt injection, which undermine accuracy guardrails
- [Learning](../learning/) — safe learning from feedback, which can degrade accuracy if feedback is biased
- [Governance](../governance/) — approval workflows and oversight, which gate high-stakes decisions accuracy must support

See [Core](../) for other cross-cutting patterns.
