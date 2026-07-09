# No Risk Tiering

## Issue: Low-risk and high-risk actions treated the same.

**Frequency**: Common

**Symptoms**
- Same autonomy level for all tasks.
- [Add more specific symptoms]

**Root Cause**
Low-risk and high-risk actions treated the same.

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
1. **Risk Classification Framework**: Define explicit risk tiers (e.g., Tier 1: read-only/reversible, Tier 2: reversible with external effect, Tier 3: irreversible or high financial/legal/safety impact) and classify every action type the agent can take against this framework before deployment, so autonomy level is a function of risk tier rather than uniform default.
2. **Tiered Autonomy Enforcement**: Configure the agent runtime so each risk tier maps to a distinct autonomy mode (Tier 1: full autonomy, Tier 2: human-in-the-loop confirmation, Tier 3: human-in-command approval required), enforced at the execution layer, not left to prompt instructions the agent could deviate from.
3. **New Action Risk Assessment**: Require every new tool or action type added to the agent to go through a risk assessment step assigning it a tier before it's wired into the toolset, so risk tiering keeps pace with capability growth instead of being a one-time exercise that goes stale.

### Detection & Response
1. **Uniform-Autonomy Anomaly Detection**: Monitor for high-risk-tier actions (Tier 3) executing with the same autonomy pattern as low-risk actions (no human checkpoint, no elevated logging) — this indicates either a misclassification or a bypass of the tiering enforcement, both requiring investigation.
2. **Risk Tier Distribution Monitoring**: Track the proportion of agent actions by tier over time; a sudden shift toward higher-risk actions without a corresponding increase in human review capacity signals the autonomy controls may not be keeping pace with actual usage.
3. **Post-Incident Tier Recalibration**: When an incident occurs, review whether the responsible action's risk tier was accurate; systematically under-tiered actions (classified as low-risk but causing high-impact failures) should trigger a tiering correction, not just a one-off incident fix.

### Architecture Patterns
1. **Risk Tier Registry**: Maintain a registry mapping action_type → risk_tier → required_autonomy_mode → approval_requirements, consumed by the same approval gateway that enforces action execution, so tiering and enforcement share one source of truth.
2. **Tier-Aware Execution Gateway**: Route every action through a gateway that looks up its risk tier and applies the corresponding autonomy mode (auto-execute, confirm-then-execute, approve-then-execute) before dispatching to the underlying tool, making tier enforcement structural rather than advisory.
3. **Elevated Observability for High Tiers**: Apply stricter logging, real-time alerting, and mandatory review sampling to Tier 3 actions specifically, so higher-risk actions get proportionally more scrutiny rather than the same monitoring level as routine ones.

### Metrics
1. **untiered_action_type_count**: Target: 0; Alert threshold: > 0 action types with no assigned risk tier
2. **tier_autonomy_mismatch_count**: Target: 0; Alert threshold: > 0 high-tier actions executed without required checkpoint
3. **tier3_human_review_rate_percent**: Target: 100% of Tier 3 actions reviewed/approved; Alert threshold: < 100%
4. **misclassified_tier_incidents_per_quarter**: Target: 0; Alert threshold: > 1

### Alerts
1. **High-Risk Action Executed Without Required Checkpoint** (P1 - Critical): Condition - a Tier 3 action executed without the mandated human approval. Action: Halt the agent's ability to execute that action type, page security/on-call, initiate incident review.
2. **Unclassified Action Type Detected** (P2 - Warning): Condition - agent executes an action type absent from the risk tier registry. Action: Default to highest-risk handling for that action type until classified, notify capability owner.
3. **Tier Distribution Shift** (P3 - Info): Condition - proportion of high-tier actions increases significantly week-over-week. Action: Review human review capacity, confirm autonomy controls are scaling with usage.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
