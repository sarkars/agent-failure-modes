# Plan Hallucination Detection Failure

## Issue
The planning step generates a plan that references a tool, API endpoint, file, or capability that does not actually exist — invented because it sounds plausible given the task description, not because the planner verified it against the real set of available tools. Because there is no validation step checking each planned action against the actual tool registry before execution begins, the hallucinated step isn't caught until the executor tries to invoke it and fails, or worse, silently matches it to the wrong real tool with a similar name.

**Frequency**: Common

**Symptoms**
- Execution errors like "tool not found" or "unknown function" for a tool name that was never registered or available
- Plans referencing plausible-sounding but nonexistent parameters, endpoints, or file paths that fit the task's domain but weren't in the actual available tool list
- The planner producing the same hallucinated tool name across multiple unrelated tasks, suggesting it's drawing on generic training knowledge rather than the actual registered toolset
- A hallucinated tool name being silently matched via fuzzy-matching or aliasing to a different, real tool, producing a plausible-looking but wrong execution
- Plan validation, if it exists at all, checking step structure/format but not verifying tool existence against the live registry

## Root Cause
LLM-driven planners generate plans by predicting plausible next steps based on patterns learned during training, which includes enormous exposure to tool names, API conventions, and library functions that are common across many systems but not necessarily present in this specific deployment's actual tool registry. Unless the planning prompt explicitly and completely enumerates the real available tools (and the model reliably attends to and constrains itself to that list rather than drawing on broader training knowledge), the planner can produce a syntactically well-formed step invoking a tool that simply doesn't exist in this environment. Without a validation gate that checks every planned tool call against the live registry before execution — separate from and prior to actually attempting the call — the hallucination survives all the way to runtime.

## Example
```
A data-analysis agent has access to three real tools: query_database,
generate_chart, and export_csv. It's asked to "pull last quarter's churn
numbers and email a summary to the leadership team."

Generated plan:
  1. query_database("SELECT churn_rate FROM metrics WHERE quarter =
     'Q2-2026'")
  2. generate_chart(data, type="trend_line")
  3. send_email(to="leadership@company.com", subject="Q2 Churn Summary",
     attachment=chart)

Step 3 invokes send_email -- a tool that sounds like a natural, expected
capability for this kind of task, and appears frequently in the model's
training data as a common agent tool, but was never registered in this
deployment's actual tool list. No pre-execution validation checked step 3
against the real registry. Steps 1 and 2 execute successfully, then step
3 fails at runtime with "unknown function: send_email," and the user is
left staring at a partially-completed task with a chart generated but
never delivered, and no clear next action suggested.
```

## Statistics
| Finding | Context |
|---------|---------|
| Hallucinated tool or function references are estimated to appear in a meaningful minority of LLM-generated plans when the planning prompt doesn't tightly constrain the model to an explicit, complete tool list | Typical range observed across agent benchmark evaluations involving tool use |
| Hallucination rate is reported to rise notably when the task domain has a strong "expected" capability (like sending email or writing files) that isn't actually available in the deployed toolset | Estimated from comparative studies of constrained versus unconstrained tool-planning prompts |
| Adding a pre-execution tool-existence validation gate is reported to catch effectively all hallucinated tool references before they reach the executor, converting a runtime failure into a plan-time correction | Reported range across teams that added registry validation to their planning pipeline |

## Mitigations
1. **Pre-execution tool-existence validation**: Before any step executes, validate every planned tool call's name and signature against the live tool registry, rejecting or flagging the plan if any referenced tool doesn't exist rather than discovering this at invocation time.
2. **Explicit, complete tool enumeration in the planning prompt**: Provide the planner with the full, exact list of available tools (names, signatures, descriptions) directly in context, and instruct it to select only from that list rather than relying on general knowledge of what tools "should" exist.
3. **Constrained decoding or structured tool selection**: Where the underlying framework supports it, restrict the planner's tool-selection output to a fixed enumeration of real tool identifiers, making hallucination structurally impossible rather than merely discouraged.
4. **Fuzzy-match rejection over silent aliasing**: When a planned tool name doesn't exactly match a registered tool, fail loudly and ask the planner to reselect, rather than silently mapping it to the closest-sounding real tool, which can invoke the wrong capability without anyone noticing.
5. **Capability-gap surfacing to the user**: When validation reveals the plan needs a capability that genuinely doesn't exist in the toolset (not just a naming mismatch), surface this explicitly to the user as a known limitation rather than letting the plan proceed to a step that will fail.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| hallucinated_tool_reference_rate | Fraction of generated plans containing at least one tool reference not found in the live registry | Alert if > 2% |
| unknown_function_runtime_errors | Count of execution failures specifically due to a tool/function not existing | Alert if > 0 (should be caught pre-execution) |
| fuzzy_match_silent_substitution_count | Instances where a hallucinated tool name was auto-mapped to a different real tool without explicit confirmation | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Plan rejected for nonexistent tool reference | Pre-execution validation finds a planned tool call with no matching registry entry | Medium | Route back to planner with the real tool list re-emphasized, or surface capability gap to user |
| Runtime tool-not-found error | A step fails during execution because its tool doesn't exist, indicating validation was bypassed | High | Halt remaining plan execution, investigate why pre-execution validation didn't catch it |

## Related Patterns
- [Plan Cost Estimation Failure](./plan-cost-estimation-failure.md) - a cost estimate built on a hallucinated step is meaningless, since the fabricated tool has no real cost profile to draw from
- [Contingency Plan Missing](./contingency-plan-missing.md) - even a well-validated plan needs a fallback for the case where a needed capability turns out not to exist
- [Plan Invalidation Not Detected](./plan-invalidation-not-detected.md) - both concern the plan being disconnected from ground truth, one from the start (hallucination) and one developing during execution (invalidation)
