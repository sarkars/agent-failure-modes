# Hidden Requirement Miss

## Issue: Agent misses unstated but critical constraints such as policy, geography, role, or SLA.

**Frequency**: Occasional

**Symptoms**
- User correction mentions a constraint already implied by context.
- Agent completes onboarding/processing steps that are valid for one jurisdiction/role but not for the specific case's actual jurisdiction/role.
- A downstream system rejects or flags the action because an implicit eligibility constraint (visa status, tax jurisdiction, seniority tier) wasn't checked.
- User correction reveals the missed constraint was already available in a system the agent had access to but didn't query.
- The same category of hidden requirement (e.g., regional compliance) is missed repeatedly across different cases.

**Root Cause**
The constraining data — jurisdiction, visa status, account tier — often already exists in a system of record, but the agent's workflow was never built to pull it into context for the decision at hand; it reads adjacent fields for one purpose and never cross-references them for eligibility. Task instructions describe only the common, "happy path" scenario, and with no checklist of commonly-implicit constraints required before execution, the agent has no prompt to check for the variant it's actually facing. Because the requester assumes the constraint is obvious from context and the underlying tool call still succeeds technically, the mismatch produces no error at the time of action and surfaces only once a downstream system enforces the rule the agent never checked.

**Example**
```
An HR onboarding agent is asked to "set up payroll and benefits for the new hire, Priya,
starting Monday." The agent completes the standard US benefits enrollment flow and
provisions a standard-tier equity grant. What it didn't check: Priya is based in Germany
on a company-sponsored visa, which means she needs to be enrolled through the company's
German entity for payroll/tax compliance, and equity grants for that entity require a
different, board-approved template due to local securities regulations. The
employee-location field was present in the HRIS record the agent had access to, but the
agent's workflow only reads it for mailing-address purposes, not for routing the
payroll/equity decision. The mistake surfaces two weeks later when the German entity's
payroll run fails compliance validation.
```

**Contributing Factors**
- Jurisdiction/role/eligibility data exists in a source-of-truth system but isn't pulled into the agent's working context for the specific decision being made.
- Task instructions describe the "happy path" (standard domestic hire) and don't enumerate the full space of location/role variants.
- No checklist of commonly-implicit constraints (jurisdiction, visa status, SLA tier, regulatory flag) required before execution.
- Requester assumes the constraint is "obvious" from context (e.g., name, office) and doesn't state it explicitly.
- Agent's action succeeds technically (the tool call doesn't error), masking that the wrong workflow variant was used.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Jurisdiction-triggered workflow branch | New-hire request with employee_location = "Germany" embedded in the HRIS record but not restated in the ticket text | Agent resolves the location field and routes to the German-entity payroll/equity workflow | Agent defaults to the standard/US workflow, ignoring the location field |
| Visa-status constraint | New hire flagged as visa-sponsored in HRIS | Agent checks visa status before finalizing start-date-dependent paperwork and flags any deadline risk | Agent proceeds with the standard timeline, missing visa-driven deadline constraints |
| Checklist completeness under partial info | Onboarding request missing an explicit role/tier field | Agent looks up the field from the source-of-truth rather than assuming a default tier | Agent assumes a default tier and provisions incorrect benefits |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| checklist_field_resolution_rate_on_benchmark_percent | 100% of applicable checklist items resolved (not left as silent defaults) | Run a labeled benchmark of scenarios covering multiple jurisdictions/roles; measure whether the agent explicitly resolves each hidden-requirement field |
| cross_reference_usage_rate_percent | > 95% | Measure how often the agent actually queries the source-of-truth field (location, visa, tier) that was available versus ignoring it |

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
| checklist_completion_rate_percent | < 95% |
| hidden_requirement_miss_rate_percent | > 5% (from user corrections) |
| checklist_update_lag_days | > 30 days |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Constraint Miss in Production | An action executed that violated a known-critical hidden requirement (geography/regulatory, role/permission) | High |
| Checklist Item Unresolved at Execution | A plan executed despite one or more checklist items marked "unknown" | Medium |
| Recurring Missed Constraint Pattern | The same constraint type is missed 3+ times across sessions within a month | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
