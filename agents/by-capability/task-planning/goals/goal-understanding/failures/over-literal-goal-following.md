# Over-Literal Goal Following

## Issue: Agent follows wording but violates user intent or common-sense constraints.

**Frequency**: Occasional

**Symptoms**
- Technically correct output causes user frustration or harm.
- [Add more specific symptoms]

**Root Cause**
Agent follows wording but violates user intent or common-sense constraints.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Intent-vs-Literal Dual Interpretation**: Generate both a literal-instruction plan and an intent-inferred plan for the same request; when the two diverge materially, surface the divergence explicitly instead of silently executing the literal reading because it was easier to justify.
2. **Common-Sense Constraint Library**: Maintain a set of domain-general guardrails (don't take actions that are technically requested but obviously harmful or absurd given the surrounding context) and check every plan against them regardless of how literally it satisfies the wording.
3. **Semantic Acceptance Criteria Instead of Literal Match**: Define task success via intent-level outcome criteria (what real-world state should exist) rather than a literal instruction-completion checklist, so the model is evaluated and optimized against intent, not against wording compliance.

### Detection & Response
1. **Frustration/Harm Signal Detection**: Monitor immediate user reactions (negative sentiment, "that's not what I meant," escalation requests) following technically-compliant outputs, and tag them as candidate over-literal failures for review.
2. **Literal-vs-Intent Divergence Logging**: Every time the dual-interpretation check detects divergence and the literal path was still chosen, log the event; track the rate and route recurring patterns into prompt or guardrail updates.
3. **Outcome Sanity Review Sampling**: Sample completed tasks and have a reviewer (human or a stronger judge model) assess whether the literal output actually served the plausible underlying intent, independent of whether the instructions were technically followed.

### Architecture Patterns
1. **Intent Inference Layer**: A component runs alongside literal instruction parsing to produce an explicit intent model (goal, implicit constraints, plausible expectations); the planner consults both before finalizing actions rather than acting on the literal parse alone.
2. **Common-Sense Guardrail Filter**: A rule or classifier layer applied after plan generation checks for known over-literal failure patterns (e.g., destructive interpretation of an ambiguous imperative) and blocks or requests confirmation before execution.
3. **Judge-Based Outcome Evaluator**: An independent evaluation service scores sampled outputs against "did this serve the user's actual goal" rather than "did this follow the letter of the instruction," feeding a training or prompt-tuning signal back into the system.

### Metrics
1. **literal_intent_divergence_rate_percent**: Target: < 5% of tasks; Alert threshold: > 15%
2. **user_frustration_signal_rate_percent**: Target: < 3%; Alert threshold: > 8%
3. **outcome_sanity_pass_rate_percent**: Target: > 95% (from sampled review); Alert threshold: < 85%
4. **guardrail_block_rate_percent**: Target: tracked baseline; Alert threshold: 2x baseline spike (may indicate upstream prompt regression)

### Alerts
1. **Harmful Literal Compliance Executed** (P1 - Critical): Condition - agent executed a literally-compliant but clearly harmful or absurd action (guardrail miss). Action: attempt immediate rollback, run incident review, add the pattern to the common-sense guardrail library.
2. **Divergence Rate Spike** (P2 - Warning): Condition - literal_intent_divergence_rate exceeds 2x rolling baseline. Action: audit recent prompt/model changes, review sampled divergent cases.
3. **Outcome Sanity Score Decline** (P3 - Info): Condition - sampled outcome_sanity_pass_rate drops below 90% over a review cycle. Action: schedule a targeted prompt/guardrail tuning session.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
