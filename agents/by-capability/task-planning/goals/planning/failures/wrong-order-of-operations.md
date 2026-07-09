# Wrong Order Of Operations

## Issue: Agent executes steps in unsafe or ineffective order.

**Frequency**: Common

**Symptoms**
- Write before read; deploy before tests; email before review.
- [Add more specific symptoms]

**Root Cause**
Agent executes steps in unsafe or ineffective order.

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
1. **DAG-Based Workflow Policy**: Represent valid action sequences for a domain as a dependency graph (e.g., read-before-write, test-before-deploy, review-before-send); the executor validates every proposed step's position against the DAG before allowing execution, rejecting out-of-order calls outright.
2. **Sequence Validators / Ordering Rules**: Encode domain-specific ordering constraints as declarative rules (e.g., "deploy requires a passing test result recorded within this session") that are checked independently of what the agent's plan claims it already did.
3. **Order-Aware Plan Templates**: For known workflow types (deployment, financial transaction, customer communication), provide templates with correct sequencing baked in by default, so the agent starts from a valid order rather than constructing one from scratch and getting it wrong.

### Detection & Response
1. **Real-Time Sequence Validator Middleware**: Checks each action against the DAG/ordering constraints immediately before execution and blocks any call whose prerequisites haven't been satisfied in the correct order, logging the violation.
2. **Post-Hoc Ordering Audit**: Review execution traces offline for near-miss or edge-case orderings not covered by explicit DAG rules (e.g., a new tool combination the ruleset hasn't seen), and use these to extend the DAG.
3. **Downstream Incident Correlation**: Track production incidents (failed deploys, unreviewed sends, corrupted writes) back to whether the triggering action sequence violated the defined DAG, prioritizing which ordering rules matter most.

### Architecture Patterns
1. **Workflow DAG Engine**: A dependency-graph service enforcing ordering edges between actions; the tool-call gateway consults this graph on every call and rejects calls whose dependencies aren't yet satisfied.
2. **Ordering Constraint Service**: A declarative rules table per domain/tool (e.g., "tool X requires tool Y success within this session") that the executor queries at call time, decoupled from the agent's own plan representation.
3. **Pre-Flight Simulation / Dry-Run Layer**: Walks a proposed multi-step plan through DAG validation before any real execution begins, surfacing ordering violations up front rather than mid-execution.

### Metrics
1. **ordering_violation_rate_percent**: Target: 0%; Alert threshold: > 0.5% of multi-step tasks
2. **blocked_out_of_order_calls_count**: Target: tracked, not necessarily zero (working-as-intended blocks); Alert threshold: sudden spike vs. baseline
3. **dag_coverage_percent_of_tools**: Target: 100% of ordering-sensitive tools; Alert threshold: < 90%
4. **downstream_incident_rate_from_ordering_percent**: Target: 0%; Alert threshold: > 0

### Alerts
1. **Out-of-Order Execution Blocked** (P3 - Info): Condition - executor blocks a call for violating DAG ordering. Action: Log for pattern analysis; no immediate action needed since the safeguard worked.
2. **Ordering Violation Reached Production** (P1 - Critical): Condition - an out-of-order action executed despite DAG enforcement (indicates a gap in the ruleset or a bypass). Action: Immediate incident review, patch the DAG/ruleset, assess production impact.
3. **DAG Coverage Gap Detected** (P2 - Warning): Condition - a newly added tool has no ordering rules defined in the DAG. Action: Require ordering rules be defined before the tool is enabled for autonomous use.

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
