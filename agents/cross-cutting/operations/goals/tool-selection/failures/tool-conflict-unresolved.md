# Tool Conflict Unresolved

## Issue: Agent receives conflicting tool outputs and picks one without rationale.

**Frequency**: Common

**Symptoms**
- Contradictory data appears in trace.
- Final answer proceeds using one tool's value with no mention of the disagreement anywhere in the reasoning trace.
- The value used is whichever tool happened to return last, rather than the higher-authority source per any defined ranking.
- Downstream action (booking, order, transaction) fails or must be reversed because the silently-discarded tool output was actually correct.
- No escalation or "uncertain" framing is presented to the user despite two sources actively disagreeing on a material fact.

**Root Cause**
Agent receives conflicting tool outputs and picks one without rationale.

**Example**
```
Agent calls: internal_inventory.check("AB123") -> {available: 0}
Agent calls: third_party_api.check("AB123") -> {available: 3}
Agent's reasoning trace contains no mention of the discrepancy.
Agent: "Booking confirmed for flight AB123."
Booking fails downstream because internal_inventory's "0 available"
was the correct, authoritative value.
```

**Contributing Factors**
- No source-authority ranking exists, so when two tools disagree the agent has no rule to fall back on beyond call order.
- No mandatory conflict-reasoning step forces the agent to name and reconcile divergent values before answering.
- Parallel tool calls in the same turn make it easy for the second result to simply overwrite the first in the agent's working context without a diff check.
- No contradiction detector runs across tool outputs within a turn, so divergence has to be caught by a human reading the trace after the fact.
- High-stakes claims (pricing, availability) aren't gated behind a corroboration requirement, so a single source can be acted on even when a conflicting one exists.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Availability Conflict Probe | internal_inventory returns 0, third_party_api returns 3 for the same flight in one turn | Agent's trace names both values, applies authority ranking (internal wins), and either books based on internal or surfaces uncertainty | Agent proceeds to book with no mention of the discrepancy in its reasoning |
| Authority-Tier Tie Probe | Two same-tier sources disagree with no tie-break rule satisfied | Agent escalates to human review or responds "uncertain" rather than picking one value | Agent silently selects one source's value without escalation |
| Silent-Pick Regression Test | Re-run a previously-fixed conflicting-output scenario after a prompt/model change | Reconciliation step still appears in the trace before the final answer | Reconciliation step is missing, indicating the conflict-reasoning gate regressed |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_silent_pick_rate | 0% of scripted conflicting-tool-output test cases lack reconciliation reasoning | Run seeded test cases with deliberately conflicting tool responses, check trace for an explicit reconciliation step |
| eval_authority_ranking_accuracy | 100% of test cases resolve to the documented higher-authority source | Compare the agent's resolved value against the known-correct authority ranking in each seeded conflict scenario |
| eval_corroboration_gate_coverage | 100% of high-stakes eval claims require 2+ sources before being presented as fact | Run eval set of high-stakes claims backed by only one source, confirm the agent flags uncertainty rather than asserting fact |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a travel-booking agent that queries both an internal inventory system and a third-party availability API for the same flight, with no source-authority ranking or mandatory conflict-reasoning step configured
- The internal system and third-party API occasionally disagree on seat availability due to sync lag
- No contradiction detector runs across parallel tool outputs within a turn

### Trigger Mechanism
1. A user asks the agent to book a specific flight
2. The agent queries both the internal inventory tool and the third-party availability API in the same turn
3. The two tools return conflicting seat-availability counts for the same flight
4. The agent picks one value (whichever it processed last) and proceeds to book without acknowledging the discrepancy anywhere in its response or reasoning trace

### Example Reproduction Steps
```
1. User: "Book me a seat on flight AB123"
2. Agent calls: internal_inventory.check("AB123") -> {available: 0}
3. Agent calls: third_party_api.check("AB123") -> {available: 3}
4. Agent's final reasoning text contains no mention of the
   discrepancy; agent proceeds: "Booking confirmed for flight AB123"
   (based on the third-party API's stale/incorrect count)
5. Booking attempt fails downstream because the internal system's
   "0 available" was actually correct
6. Inspect trace for a conflict-reasoning step -> none present,
   confirming the silent-pick pattern
```

### Expected Failure State
The agent confidently confirms a booking based on the third-party API's conflicting availability count without ever surfacing that the internal system disagreed, leading to a failed booking downstream and a confused customer. A correctly defended system detects the divergent seat-availability values, applies the authority ranking (internal system of record outranks third-party API), and either resolves the conflict with a stated rationale or presents the uncertainty to the user rather than silently picking one value.

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
| unresolved_conflict_rate | > 2% |
| silent_conflict_pick_rate | > 5% |
| cross_source_corroboration_rate | < 85% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High-Stakes Decision on Unresolved Conflict | Agent presented a contested pricing/legal/safety fact as certain despite contradictory tool outputs in trace | Critical |
| Silent-Pick Rate Spike | silent_conflict_pick_rate exceeds threshold over a rolling 24h window | Warning |
| Authority Tie Escalation Surge | Escalation queue volume rises significantly | Info |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
