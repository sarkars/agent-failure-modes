# Tool Output Misinterpretation

## Issue: Agent Misunderstands Tool Response

**Frequency**: Common

**Symptoms**
- Agent extracts wrong value from tool output
- Array interpreted as single item
- Null/empty confused with failure
- Units or formats misunderstood

**Root Cause**
- Ambiguous or complex tool output formats
- Missing context about output structure
- Agent assumptions about output schema
- Inconsistent output formats across tools

**Example**
```
Tool response: { 
  "users": [
    { "name": "Alice", "balance": 100 },
    { "name": "Bob", "balance": 200 }
  ],
  "total_balance": 300
}

Agent interpretation: "The user has a balance of 300"

User asked about: Alice's balance (100)

Result: Agent reports wrong balance
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Tool response combines a per-item list and an aggregate field with no disambiguating field-level description
- No deterministic extraction layer between raw tool output and agent reasoning for single-entity queries
- No extracted-value-vs-raw-output diffing in place

### Trigger Mechanism
1. Call the tool for a response containing both a list of items and a rolled-up aggregate field (as in the example)
2. Ask the agent a question scoped to one specific item (e.g., "What's Alice's balance?")
3. Observe whether the agent's answer matches the per-item value or the aggregate value

**Example Reproduction Steps:**
```
1. Return { "users": [{"name": "Alice", "balance": 100}, {"name": "Bob", "balance": 200}], "total_balance": 300 } from the tool
2. Ask the agent: "What's Alice's balance?"
3. Capture the agent's stated number
4. Compare against the ground-truth per-item value (100) vs. the aggregate (300)
5. Measure: extraction accuracy across repeated trials with similarly shaped responses
```

### Expected Failure State
- Agent reports the aggregate value (300) instead of the queried individual's value (100)
- No field-level annotation or extraction layer disambiguated which field answered the question
- No diffing mechanism flagged the mismatch between the reported answer and the ground-truth field

---

## Mitigation Strategies

### Prevention
1. **Field-level descriptions that disambiguate aggregates from individual values**: Annotate fields like `total_balance` explicitly as "sum across all returned users, not any individual user's balance" in the schema, directly targeting the failure shown where the agent conflated a 300 aggregate with Alice's individual 100 balance. Trade-off: verbose per-field annotations increase schema size and token cost on every tool-definition load.
2. **Scope responses to the actual question instead of returning everything**: If the tool knows the caller asked about a specific user, return only that user's record rather than the full `users` array plus a `total_balance` the agent has to sift through — the ambiguity in the example only exists because both individual and aggregate values were present together. Trade-off: requires the tool layer to parse query intent, which shifts complexity from the LLM to the tool and can itself introduce new misrouting bugs.
3. **Consistent field-naming conventions across tools**: Standardize that aggregate fields always carry a `total_` or `_sum` prefix and are never positioned as the "answer" field, so agents build a reliable prior about which field is per-item vs. rolled-up. Trade-off: retrofitting naming conventions onto existing tool outputs is a breaking change for any caller already parsing the old field names.

### Detection & Response
1. **Extracted-value vs. raw-output diffing**: Automatically compare the specific number/field the agent reports in its final answer against the actual matching field in the raw tool JSON; a mismatch (agent said 300, ground truth for the queried entity was 100) is the exact failure pattern here and should be logged per-tool.
2. **User-correction tracking on interpretation**: Tag support tickets or chat corrections where the user says "no, I meant X's balance, not the total" as tool-output-misinterpretation events, and aggregate by which tool's output caused the confusion.
3. **Aggregate-field confusion audits**: Specifically flag cases where a response contains both a list of items and a summary/aggregate field, and check whether the agent's answer used the wrong one — this narrow check catches the exact array-vs-total ambiguity in the example efficiently.

### Architecture Patterns
1. **Schema-annotated tool outputs (JSON Schema with field descriptions)**: Attach a JSON Schema to every tool's return type with per-field semantic descriptions, not just types, so "what is total_balance" is answered structurally rather than inferred; deployment consideration — schema authoring becomes part of the tool-review checklist, adding friction to shipping new tools quickly.
2. **Response post-processing/extraction layer**: Insert a deterministic (non-LLM) extraction step between the raw tool output and the agent's context when the query specifies a single named entity, so the agent never sees the ambiguous multi-value payload for simple lookups. deployment consideration — only works when query intent is unambiguous enough to parse programmatically; complex queries still need the full payload.
3. **Few-shot output-parsing examples embedded in the tool description**: Include one example input/output/correct-extraction triple directly in the tool's docstring (as recommended for AI-oriented documentation), showing explicitly "if asked about Alice, use users[].balance where name=='Alice', not total_balance"; deployment consideration — examples must be kept in sync as the schema evolves or they become actively misleading.

### Metrics
1. **extraction_accuracy_rate**: Target > 97% of agent-extracted values matching the correct field in raw tool output (sampled audit); Alert if < 90% over a weekly sample.
2. **aggregate_vs_individual_confusion_rate**: Target < 2% of responses containing both aggregate and per-item fields resulting in wrong-field extraction; Alert if > 8%.
3. **user_correction_rate_on_tool_answers**: Target < 3% of tool-derived answers corrected by users; Alert if > 10% for any single tool over a week.
4. **agent_reclarification_rate**: Target: track as a baseline signal (not inherently bad) — a rising trend alongside falling extraction_accuracy indicates the agent is compensating for ambiguous outputs; Alert on a >50% relative increase week-over-week.

### Alerts
1. **Extraction Accuracy Drop** (P1): Condition - extraction_accuracy_rate falls below 90% for a given tool. Action: audit that tool's output schema for ambiguous or co-located aggregate/individual fields, add or clarify field descriptions, consider splitting the response.
2. **Aggregate Confusion Spike** (P2): Condition - aggregate_vs_individual_confusion_rate exceeds 8% for a tool with both list and summary fields. Action: restructure the response to separate or rename aggregate fields, add explicit disambiguating descriptions.
3. **Rising User Corrections** (P3): Condition - user_correction_rate_on_tool_answers exceeds 10% for a tool over a week. Action: review recent correction examples, identify the specific field/format causing confusion, update schema and few-shot examples.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research on output parsing and interpretation failures
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - How agents misinterpret tool outputs
