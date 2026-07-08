# Tool Conflict Unresolved

## Issue: Agent receives conflicting tool outputs and picks one without rationale.

**Frequency**: Common

**Symptoms**
- Contradictory data appears in trace.
- [Add more specific symptoms]

**Root Cause**
Agent receives conflicting tool outputs and picks one without rationale.

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
1. **Source Authority Ranking with Tie-Break Rules**: Assign every tool/data source a static authority tier (e.g., system-of-record > internal cache > third-party API > public web) and configure explicit tie-break rules for same-tier conflicts (most recent timestamp wins, majority-of-N-sources wins). The agent is required to consult this ranking whenever two tool outputs disagree on a material fact, rather than picking whichever result it processed last.
2. **Mandatory Conflict-Reasoning Step**: When outputs from two or more tool calls diverge on the same entity/fact, force the agent through an explicit reconciliation step in its trace — it must name both values, state which source it trusts and why, before it is allowed to produce a final answer. Responses that skip this step when divergence is detected are blocked at the output layer.
3. **Corroboration Requirement for Contested Claims**: For high-stakes facts (pricing, legal terms, safety-relevant data), require at least two independent sources to agree before the claim is presented as fact; if only one source is available or sources disagree, the agent must present the uncertainty explicitly rather than silently choosing one value.

### Detection & Response
1. **Contradiction Detector on Parallel Tool Outputs**: Run an automated fact-extraction diff across all tool outputs returned within a single turn/session; when two extracted values for the same entity/field disagree, flag the trace for the conflict-reasoning check and alert if no reconciliation step is present.
2. **Silent-Pick Pattern Detection**: Specifically look for traces where divergent tool outputs exist but the final answer's reasoning text contains no acknowledgment of the discrepancy — this is the signature of the failure mode (picking one value without rationale) and is scored separately from cases where conflicts were explicitly reasoned through.
3. **Escalation on Authority Tie**: When two conflicting sources sit at the same authority tier and tie-break rules don't resolve them, escalate to a human reviewer or downgrade the response to "uncertain" rather than letting the agent arbitrarily choose; track how often this escalation path fires.

### Architecture Patterns
1. **Post-Tool-Call Conflict Resolution Service**: Insert a dedicated reconciliation stage after parallel/sequential tool calls complete and before the generation step — a diff engine compares structured outputs, applies the authority ranking, and either produces a resolved value with rationale or raises an unresolved-conflict signal.
2. **Evidence Ledger**: Persist every tool output with its source, timestamp, and authority tier alongside the final resolution decision and rationale, so any answer involving a conflict is fully auditable after the fact.
3. **Human-in-the-Loop Escalation Path**: For unresolved ties or high-stakes contested claims, route to a review queue rather than forcing an automatic pick; the agent's response degrades gracefully to "conflicting information found, confirming" rather than asserting one source as fact.

### Metrics
1. **unresolved_conflict_rate**: Target: 0% of detected conflicts reach the user unresolved; Alert threshold: > 2%
2. **silent_conflict_pick_rate**: Target: < 1% of conflicting-output traces lack reconciliation reasoning; Alert threshold: > 5%
3. **cross_source_corroboration_rate**: Target: > 95% of high-stakes claims backed by 2+ sources; Alert threshold: < 85%
4. **conflict_escalation_count**: Target: tracked baseline, no fixed target; Alert threshold: sudden spike (2x week-over-week) indicating upstream data quality issue

### Alerts
1. **High-Stakes Decision on Unresolved Conflict** (P1 - Critical): Condition - agent presented a contested pricing/legal/safety fact as certain despite contradictory tool outputs in trace. Action: Pull transcript, issue correction to user if already sent, review authority ranking config.
2. **Silent-Pick Rate Spike** (P2 - Warning): Condition - silent_conflict_pick_rate exceeds threshold over a rolling 24h window. Action: Review recent prompt/tool changes, re-verify conflict-reasoning gate is enforced.
3. **Authority Tie Escalation Surge** (P3 - Info): Condition - escalation queue volume rises significantly. Action: Investigate whether a source's data quality has degraded, no immediate agent-side action.

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

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
