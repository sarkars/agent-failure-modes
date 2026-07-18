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

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent with a `customer_search` tool that supports only exact-ID lookup, but whose model-facing schema description doesn't explicitly state that fuzzy/partial name matching is unsupported
- No capability manifest separate from the schema description exists, and no capability regression test suite runs in CI to catch mismatches between what the model believes and what the tool actually does
- The tool silently no-ops or returns an empty result (rather than a typed "UNSUPPORTED_OPERATION" error) when given a partial name instead of an exact ID

### Trigger Mechanism
1. A user asks the agent to find a customer by a partial name ("someone named Johnson")
2. The agent, believing the search tool supports fuzzy name matching (since the schema doesn't say otherwise), calls it with the partial name as if it were a valid query
3. The tool returns an empty result set rather than a typed capability error, since it silently doesn't support this query shape
4. The agent, receiving an ambiguous empty result, either reports "no customer found" (incorrect) or retries the same impossible query multiple times

### Example Reproduction Steps
```
1. User: "Find the customer named Johnson"
2. Agent calls: customer_search(query="Johnson")  // tool only
   supports exact ID lookup, not name fuzzy-match
3. Tool returns: [] (empty result, no error indicating unsupported
   operation)
4. Agent: "I couldn't find a customer named Johnson" (incorrect --
   the customer exists, but the search was fundamentally the wrong
   shape for this tool)
5. Check repeated_impossible_request_rate for this session -> agent
   retries with slight query variations ("Johnson", "johnson",
   "Mr. Johnson"), all failing the same way
```

### Expected Failure State
The agent incorrectly tells the user no matching customer exists, when in fact the customer_search tool simply doesn't support the fuzzy name-matching operation the agent assumed it could perform, and the silent empty-result failure gives no signal to correct the agent's belief. A correctly defended system either has the capability manifest reject the fuzzy-name call before dispatch (since it's outside the tool's documented supported operations) or has the tool return a typed `UNSUPPORTED_OPERATION` error that lets the agent recognize it needs a different approach (e.g., asking the user for an exact customer ID).

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
