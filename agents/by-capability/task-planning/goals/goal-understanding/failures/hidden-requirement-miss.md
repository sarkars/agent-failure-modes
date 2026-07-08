# Hidden Requirement Miss

## Issue: Agent misses unstated but critical constraints such as policy, geography, role, or SLA.

**Frequency**: Occasional

**Symptoms**
- User correction mentions a constraint already implied by context.
- [Add more specific symptoms]

**Root Cause**
Agent misses unstated but critical constraints such as policy, geography, role, or SLA.

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
1. **Domain Requirement Checklist Injection**: For each task type, maintain and retrieve a checklist of commonly-implicit constraints (jurisdiction, role/permission tier, SLA class, regulatory flags), and require each item to be explicitly checked off before execution instead of relying on the agent to infer them from free-text context.
2. **Context Enrichment Pre-Fetch**: Before planning, automatically pull structured metadata about the actor/entity involved (customer region, account tier, contract terms) from source-of-truth systems, so constraints exist as explicit facts in context rather than being left for the model to guess from surrounding conversation.
3. **"What Am I Assuming" Self-Check Step**: Have the agent generate an explicit list of assumptions it is making about unstated constraints before acting. Assumptions matching known high-risk categories (geography, role, SLA) trigger a mandatory lookup or clarifying question rather than being left as silent assumptions.

### Detection & Response
1. **Post-Hoc Constraint Violation Scan**: After execution, an independent check cross-references the actor's actual attributes (region, tier, role) against what the action assumed or required, logging mismatches as hidden-requirement misses even when the action itself "succeeded."
2. **Correction-Triggered Constraint Mining**: When a user correction reveals a missed constraint already implied by available context, capture it and add it to the domain checklist (via a reviewed pipeline) so the same context signal is caught automatically next time.
3. **Coverage Gap Analysis**: Periodically audit which fields in the available context/metadata were never referenced by the agent's reasoning trace, surfacing systematically-ignored data sources that likely hold hidden requirements the checklist hasn't captured yet.

### Architecture Patterns
1. **Requirement Checklist Service**: A versioned, task-type-keyed checklist store is queried by the planner at task start; every item resolves to true/false/unknown before the plan is allowed to execute, and "unknown" forces a lookup or a clarifying question rather than a silent default.
2. **Entity Context Resolver**: A pre-planning step resolves the full attribute set of relevant entities (customer, account, region) from source-of-truth systems and injects them as structured context, reducing reliance on inference from free text alone.
3. **Constraint Feedback Loop Pipeline**: A pipeline ingests user corrections and compliance findings, extracts the missed-constraint pattern, and proposes checklist updates for human review, closing the loop between production misses and prevention.

### Metrics
1. **checklist_completion_rate_percent**: Target: 100% of items resolved before execution; Alert threshold: < 95%
2. **hidden_requirement_miss_rate_percent**: Target: < 2% (from user corrections); Alert threshold: > 5%
3. **unknown_field_resolution_time_p95**: Target: within defined SLA (e.g., < 5s for automated lookup); Alert threshold: exceeded
4. **checklist_update_lag_days**: Target: < 7 days from identified gap to checklist update; Alert threshold: > 30 days

### Alerts
1. **Critical Constraint Miss in Production** (P1 - Critical): Condition - an action executed that violated a known-critical hidden requirement (geography/regulatory, role/permission). Action: halt further actions of that type for the affected scope, remediate, notify compliance.
2. **Checklist Item Unresolved at Execution** (P2 - Warning): Condition - a plan executed despite one or more checklist items marked "unknown." Action: block future occurrences by fixing the gate, investigate why the bypass occurred.
3. **Recurring Missed Constraint Pattern** (P3 - Info): Condition - the same constraint type is missed 3+ times across sessions within a month. Action: prioritize a checklist/context-resolver update for that constraint category.

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
