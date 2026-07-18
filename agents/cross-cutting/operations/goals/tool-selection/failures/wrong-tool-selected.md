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

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent with two overlapping tools: `quick_web_search` (fast, low-authority, general web results) and `verified_legal_database` (slower, authoritative, curated legal citations), with no tool selection policy hierarchy or disambiguated descriptions distinguishing when each should be used
- No post-call relevance/authority scoring flags when a lower-authority tool was used for a task that warranted the higher-authority one
- A user asks a question requiring an authoritative legal citation

### Trigger Mechanism
1. The user asks for the current statute governing a specific legal question
2. The agent, with both tools superficially plausible matches for "look up legal information," selects `quick_web_search` because its description keyword-matches more closely with the phrasing of the query
3. The web search returns a plausible-looking but outdated or non-authoritative blog post discussing the statute
4. The agent presents this low-authority result as if it were an authoritative citation, with no indication that `verified_legal_database` (the higher-authority tool) was available and unused

### Example Reproduction Steps
```
1. User: "What's the current statute of limitations for this claim
   type in California?"
2. Agent calls: quick_web_search("California statute of limitations
   [claim type]") -- selects this over verified_legal_database
3. Result: a blog post from 2019 citing an since-amended statute
4. Agent presents the outdated figure as current fact, with no
   caveat about source authority
5. Check tool_selection_policy_violation_rate for this task category
   -> selection diverged from the documented hierarchy, which ranks
   verified_legal_database above quick_web_search for legal-citation
   tasks
6. Check low_authority_tool_usage_rate -> flags this case since a
   higher-authority tool was available and applicable but unused
```

### Expected Failure State
The agent presents an outdated statute from a low-authority blog post as current legal fact, because it selected the wrong tool for a task category with a clear higher-authority alternative available, and no scoring mechanism caught the mismatch before the answer was delivered. A correctly defended system enforces the documented tool-selection hierarchy at the arbitration layer, constraining the model's choice to `verified_legal_database` for legal-citation task types regardless of which tool's description superficially matches the query phrasing.

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
