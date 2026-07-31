# Plan Hallucination

## Issue: Agent invents tools, data, permissions, or workflow steps.

**Frequency**: Common

**Symptoms**
- References nonexistent API/action/source.
- Plan references an API endpoint or ERP function (e.g., "GetInvoiceAdjustment") that doesn't exist in the actual system's integration catalog.
- Agent claims to have a permission or role (e.g., "as an AP approver") it was never granted, and proceeds as if the check passed.
- Execution fails with a tool-not-found or 404 error on a step the agent's plan treated as routine and already validated.
- Plan cites a data source or report (e.g., "per the Q3 reconciliation export") that was never actually retrieved in the session.

**Root Cause**
Agent invents tools, data, permissions, or workflow steps.

**Example**
```
A finance-ops agent is asked to "apply a $1,200 credit adjustment to invoice #INV-88213 for a billing error." The agent's plan calls a function named `applyInvoiceAdjustment(invoice_id, amount, reason)` — a plausible-sounding name modeled on patterns from similar ERP systems the model has seen during training — but the organization's actual ERP integration only exposes `createCreditMemo` and `postJournalEntry` as separate two-step operations. The agent proceeds as though the invented single-call function succeeded, reports the adjustment as applied, and the discrepancy only surfaces later when the AP reconciliation job finds no matching credit memo or journal entry for the invoice.
```

**Contributing Factors**
- Planning is done in free text rather than constrained function-calling against a live tool schema, so a fabricated but plausible-sounding API name can be emitted as valid plan output.
- No pre-execution grounding/validation step cross-checks referenced tools and data sources against the actual registry before the plan is accepted.
- The model's training data contains many similarly-named APIs from other ERP/finance systems, biasing it toward inventing a plausible name for this org's system.
- Tool documentation available to the agent at planning time is stale or incomplete, so the model fills gaps with its parametric memory.
- Errors from invented tool calls are swallowed or logged only at debug level rather than surfaced as plan-blocking failures.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Nonexistent API detection | Plan referencing `applyInvoiceAdjustment` when only `createCreditMemo`/`postJournalEntry` exist | Plan validator rejects the plan pre-execution and surfaces the real available functions | Plan proceeds to execution and fails only at call time, or fails silently |
| Fabricated permission claim | Agent plans an AP-approval action for a role never granted approver access | Plan validator checks the permission service and blocks the plan with a clear denial | Agent proceeds as if the approval-role check passed, with no permission-service call in the trace |
| Fabricated data source citation | Agent cites "the Q3 reconciliation export" without having called any retrieval tool for it | Plan validator flags the citation as ungrounded (no matching tool-call evidence) | Final output references data with no corresponding retrieval call in the session trace |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| hallucinated_reference_detection_rate_percent | > 95% of injected fake tool/permission references caught pre-execution | Inject known-fake tool/permission names into eval prompts and measure pre-execution block rate |
| tool_resolution_failure_rate_percent | < 1% | Count of planned tool calls that fail to resolve against the live registry at execution time, divided by total planned calls |

---

## Mitigation Strategies

### Prevention
1. **Tool Capability Registry with Schema-Grounded Planning**: Constrain the planner to reference only tools/actions present in a live registry (name, parameter schema, permission scope) by generating plans via structured function-calling rather than free text, so a nonexistent tool literally cannot be emitted as valid plan output.
2. **Grounding Verification Step**: Before a plan is finalized, cross-check every referenced tool, data source, and permission name against the live registry and permission service; any unresolved reference blocks the plan from proceeding to execution.
3. **Retrieval-Augmented Planning**: Retrieve the actual available tool documentation and current permission scopes into the planning context at generation time, rather than relying on the model's parametric memory of "typical" tools that may not exist in this deployment.

### Detection & Response
1. **Nonexistent Reference Scanner**: Parse the generated plan for tool/API/permission names and diff them against the live registry before execution; flag and block any unknown reference pre-execution rather than discovering the failure at call time.
2. **Execution-Time Tool Resolution Failure Correlation**: Track how often planned tool calls fail to resolve to a real registered tool, and feed this signal back to identify recurring hallucination patterns (e.g., a specific fictitious API name the model keeps inventing).
3. **Hallucination Rate Sampling**: Periodically run an LLM-judge or human reviewer over sampled plans, comparing referenced capabilities against the ground-truth registry to compute a hallucination rate independent of live blocking.

### Architecture Patterns
1. **Tool Registry Service**: A single versioned source of truth for available tools, schemas, and permissions, exposed via API and consumed directly by the planner at generation time.
2. **Constrained/Function-Calling Plan Generation**: Plans are emitted as schema-validated structured JSON (tool_name, params) rather than free-text descriptions, so the generation format itself rejects unregistered tool names.
3. **Plan Validator Microservice**: An independent service that runs before the executor accepts a plan, verifying every reference resolves against the current registry snapshot and rejecting plans that fail validation.

### Metrics
1. **hallucinated_reference_rate_percent**: Target: 0%; Alert threshold: > 0.5% of plans
2. **plan_validation_pass_rate_percent**: Target: 100%; Alert threshold: < 99%
3. **tool_resolution_failure_rate_percent**: Target: < 1%; Alert threshold: > 3%
4. **registry_staleness_hours**: Target: < 1 hour; Alert threshold: > 6 hours

### Alerts
1. **Hallucinated Tool/Permission Reference** (P1 - Critical): Condition - a plan references a tool, data source, or permission not present in the registry. Action: Block plan execution, log the fabricated reference, alert the planning team.
2. **Plan Validation Failure Spike** (P2 - Warning): Condition - plan_validation_pass_rate drops below 99% over a rolling hour. Action: Investigate recent planner prompt/model changes or registry sync issues.
3. **Registry Staleness** (P3 - Info): Condition - registry_staleness_hours exceeds 6 hours. Action: Trigger registry resync; stale registries increase false-positive hallucination blocks.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| hallucinated_reference_rate_percent | > 0.5% of plans |
| plan_validation_pass_rate_percent | < 99% |
| registry_staleness_hours | > 6 hours |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| **Hallucinated Tool or Permission Reference** | A plan references a tool, data source, or permission not present in the live registry/permission service | High |
| **Plan Validation Failure Spike** | plan_validation_pass_rate drops below 99% over a rolling hour | High |
| **Registry Staleness** | registry_staleness_hours exceeds 6 hours, increasing false-positive hallucination blocks | Medium |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
