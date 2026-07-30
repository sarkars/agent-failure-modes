# No Risk Tiering

## Issue: Low-risk and high-risk actions treated the same.

**Frequency**: Common

**Symptoms**
- Same autonomy level for all tasks.
- A single "auto-approve" setting applies equally to a read-only lookup and an irreversible fund transfer.
- Incident review reveals a high-impact action executed with the same lack of oversight as a routine, low-stakes one.
- Adding a new, higher-risk capability doesn't trigger any change in the level of human oversight applied to the agent.

**Root Cause**
Low-risk and high-risk actions treated the same.

**Example**
```
An operations agent is authorized to both "look up shipment status"
(read-only) and "issue a supplier payment" (irreversible, financial)
under the same autonomy setting: full auto-execute, since risk tiering
was never applied per action type.

A malformed upstream data feed causes the agent to compute an incorrect
payment amount. Because the payment action has the same unrestricted
autonomy as the shipment lookup, it executes without any human
checkpoint.

By the time finance reconciliation catches the anomaly three days
later, $40,000 has been sent to the wrong supplier account, and there is
no tier-appropriate control that would have caught it before execution.
```

**Contributing Factors**
- Action types are not classified by potential impact (reversibility, financial/legal/safety exposure) before deployment.
- Autonomy configuration is applied uniformly across the agent rather than per action type.
- New actions added to the toolset inherit the agent's default autonomy setting instead of going through a risk assessment.
- No architectural enforcement point exists to apply different oversight levels based on risk tier.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Tier-based routing | A Tier 3 (irreversible/high-impact) action | Routed to human-in-command approval | Action executes with no human checkpoint |
| Untiered action fail-safe | Agent invokes an action type absent from the risk tier registry | Defaults to highest-risk handling until classified | Action executes with default/low-risk autonomy |
| Tier consistency across inputs | Same action type invoked with varying impact parameters (e.g., transfer amount) | Routing reflects actual risk, not just action name | High-impact instance routed the same as low-impact instance |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| tier_routing_accuracy | 100% | Inject test actions across all tiers and verify each receives its mandated autonomy mode |
| untiered_action_failsafe_rate | 100% | Invoke test action types absent from the registry and confirm they default to highest-risk handling |
| tier3_checkpoint_enforcement_rate | 100% | Sample Tier 3 actions and confirm all passed through a human checkpoint before execution |

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
| untiered_action_type_count | > 0 action types with no assigned risk tier |
| tier_autonomy_mismatch_count | > 0 high-tier actions executed without required checkpoint |
| tier3_human_review_rate_percent | < 100% |
| misclassified_tier_incidents_per_quarter | > 1 |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High-Risk Action Executed Without Required Checkpoint | A Tier 3 action executed without the mandated human approval | Critical |
| Unclassified Action Type Detected | Agent executes an action type absent from the risk tier registry | Warning |
| Tier Distribution Shift | Proportion of high-tier actions increases significantly week-over-week | Info |

---

## References

- [CSA-Agentic-Profile](https://labs.cloudsecurityalliance.org/agentic/agentic-nist-ai-rmf-profile-v1/)
- Note: Agentic AI governance profile built around NIST RMF.
