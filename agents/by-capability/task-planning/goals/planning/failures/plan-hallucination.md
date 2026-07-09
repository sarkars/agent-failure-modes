# Plan Hallucination

## Issue: Agent invents tools, data, permissions, or workflow steps.

**Frequency**: Common

**Symptoms**
- References nonexistent API/action/source.
- [Add more specific symptoms]

**Root Cause**
Agent invents tools, data, permissions, or workflow steps.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
