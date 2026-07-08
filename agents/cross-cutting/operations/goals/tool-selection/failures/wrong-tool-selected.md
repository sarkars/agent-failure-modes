# Wrong Tool Selected

## Issue: Agent chooses an inappropriate tool for the task.

**Frequency**: Common

**Symptoms**
- Tool result irrelevant or low-authority.
- [Add more specific symptoms]

**Root Cause**
Agent chooses an inappropriate tool for the task.

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
1. **Tool Selection Policy with Source Hierarchy**: Define an explicit decision tree mapping task-intent features (data type needed, required authority/freshness, cost/latency tolerance) to a ranked list of preferred tools, and require the planner to justify selection against this hierarchy rather than picking whichever tool's description sounds closest to a keyword match in the query.
2. **Disambiguated Tool Descriptions with Boundary Examples**: Audit tool schema descriptions for overlap with similar tools in the catalog and rewrite them to include explicit "use this tool when X, use tool Y instead when Z" guidance; ambiguous or overlapping descriptions are a leading cause of the model reaching for a plausible-but-wrong tool.
3. **Few-Shot Disambiguation Examples in System Prompt**: For tool pairs/groups with known historical confusion (e.g., two search tools with different authority levels), embed few-shot examples in the system prompt showing correct selection for representative queries, directly countering the specific confusions observed in production logs.

### Detection & Response
1. **Post-Call Relevance Scoring**: After each tool call, score the returned result's relevance to the inferred task intent (embedding similarity, keyword overlap, or a small judge model); low-relevance results are flagged as potential wrong-tool-selection events and routed to the eval sampling queue.
2. **Low-Authority-Source Usage Flag**: When a higher-authority tool was available and applicable but the agent used a lower-ranked one instead (per the source hierarchy), flag the selection even if the result "worked," since it indicates the policy isn't being followed and may fail on a harder query.
3. **Selection-vs-Policy Divergence Audit**: Periodically sample sessions and compare the tool actually selected against what the documented selection policy would have recommended given the same task features; a rising divergence rate indicates policy drift or an undertrained selection mechanism.

### Architecture Patterns
1. **Tool Selection Arbitration Layer**: Insert a router between task understanding and tool dispatch that scores candidate tools against task features using the documented hierarchy and either pre-selects the top candidate or constrains the model's choice set to policy-compliant options.
2. **Tool Metadata Catalog with Authority Tags**: Maintain a catalog entry per tool with authority tier, cost, latency, and freshness metadata that both the arbitration layer and the model's prompt draw from, keeping selection criteria consistent across the system rather than duplicated in ad hoc prompt text.
3. **Selection-Outcome Feedback Loop**: Log every (task features, tool selected, outcome quality) tuple and periodically retrain/tune the selection policy or few-shot examples from cases where a non-preferred tool was chosen and produced a worse outcome than the policy-recommended one would have.

### Metrics
1. **tool_selection_policy_violation_rate**: Target: < 3% of calls diverge from documented hierarchy; Alert threshold: > 10%
2. **irrelevant_result_rate**: Target: < 5%; Alert threshold: > 15%
3. **low_authority_tool_usage_rate**: Target: < 5% of cases where a higher-authority tool was available; Alert threshold: > 15%
4. **policy_override_success_rate**: Target: arbitration layer correctly constrains selection > 98% of time; Alert threshold: < 90%

### Alerts
1. **High-Stakes Task Using Low-Authority Tool** (P2 - Warning): Condition - agent selects a low-authority/low-precision tool for a task flagged as high-stakes despite a higher-authority tool being available. Action: Review session, reinforce selection policy examples, consider hard-constraining the choice set for that task category.
2. **Policy Violation Rate Spike** (P2 - Warning): Condition - tool_selection_policy_violation_rate exceeds threshold over a rolling week. Action: Audit recent tool catalog changes for new ambiguity, review few-shot examples for staleness.
3. **Irrelevant Result Rate Above Threshold** (P3 - Info): Condition - irrelevant_result_rate crosses baseline threshold. Action: Sample affected sessions for the next eval cycle, no immediate production action required.

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
