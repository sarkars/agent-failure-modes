# Tool Capability Misunderstanding

## Issue: Agent assumes a tool can do something it cannot.

**Frequency**: Common

**Symptoms**
- Invalid tool arguments or impossible requested action.
- [Add more specific symptoms]

**Root Cause**
Agent assumes a tool can do something it cannot.

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
1. **Capability Registry as Source of Truth**: Maintain a machine-readable capability manifest per tool (supported operations, parameter ranges, rate limits, explicitly unsupported actions) separate from the free-text schema description shown to the model. The planner validates every proposed tool call against this manifest before dispatch, not just against the loosely-worded docstring the model is prompted with.
2. **Negative Capability Examples in Schema**: Extend tool schema descriptions with explicit "cannot do X" statements and near-miss examples (e.g., "this tool searches by exact ID, it cannot fuzzy-match names") rather than only describing what the tool supports. Models pattern-match on documented capabilities more reliably when the boundary is stated, not implied by omission.
3. **Capability Regression Test Suite in CI**: Run a fixed set of "golden capability probes" against each tool version in CI — calls that should succeed and calls that should be correctly rejected/unsupported. Block deployment of a new tool version or prompt if the probe suite shows the model attempting actions the manifest marks unsupported.

### Detection & Response
1. **Invalid-Argument/Impossible-Action Monitor**: Instrument the tool gateway to classify every rejected call by reason (invalid argument, unsupported operation, out-of-range parameter) and stream this to a dashboard. A spike in "unsupported operation" rejections indicates the model's belief about the tool has drifted from reality, often after a silent tool API change.
2. **Capability Mismatch Classifier**: Run an automated diff between the tool's actual OpenAPI/manifest capabilities and the schema text the model was prompted with; flag any manifest change that isn't reflected in the prompt-facing description within one release cycle.
3. **Repeated-Impossible-Request Pattern Detection**: Track per-agent-version counts of requests for the same impossible action; three or more repeats within a session indicates the model is not learning from the tool's error response and needs an explicit capability correction injected into context.

### Architecture Patterns
1. **Capability-Aware Planner Filter**: Before the model selects a tool, the planner pre-filters the candidate tool list to only those whose manifest supports the inferred task requirements, reducing the chance the model reaches for a plausible-sounding but incapable tool.
2. **Typed Error Adapter Layer**: Wrap every tool with an adapter that returns structured, typed errors ("UNSUPPORTED_OPERATION", "PARAMETER_OUT_OF_RANGE") instead of generic failures or silent no-ops, so the agent's error-handling logic can distinguish "retry with different args" from "this tool fundamentally cannot do this."
3. **Manifest-Prompt Sync Pipeline**: Auto-generate the model-facing tool schema description from the same manifest used for validation, eliminating drift between what the model is told a tool can do and what the enforcement layer actually allows.

### Metrics
1. **invalid_tool_call_rate**: Target: < 2% of tool calls; Alert threshold: > 5%
2. **unsupported_operation_rejection_rate**: Target: < 1%; Alert threshold: > 3% or sudden spike after a tool version change
3. **manifest_prompt_drift_count**: Target: 0 undocumented manifest changes; Alert threshold: any capability change not reflected in prompt within 1 release cycle
4. **repeated_impossible_request_rate**: Target: < 0.5% of sessions; Alert threshold: > 2%

### Alerts
1. **Capability Drift After Tool Update** (P1 - Critical): Condition - unsupported_operation_rejection_rate spikes immediately following a tool/API version bump. Action: Freeze the tool version, verify manifest sync, hotfix schema description.
2. **Repeated Impossible-Action Loop** (P2 - Warning): Condition - same agent session issues 3+ requests for an action the manifest marks unsupported. Action: Inject explicit capability correction into context, log for prompt-tuning review.
3. **New Unsupported-Operation Pattern** (P3 - Info): Condition - a previously unseen invalid-argument pattern appears in logs. Action: Add to capability regression test suite, no immediate production action.

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
