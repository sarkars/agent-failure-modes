# Partial Result Misuse

## Issue: Agent treats partial/incomplete output as complete.

**Frequency**: Common

**Symptoms**
- Tool response has warning, omitted fields, or truncation.
- Agent's summary or downstream calculation is based on a truncated page or list, silently dropped fields ignored.

**Root Cause**
Pagination and truncation metadata typically travels alongside the data itself, but the parsing layer that hands tool output to the model often extracts only the record array and drops the accompanying `has_more`/`truncated` flag, so the signal that would trigger a second fetch never reaches the reasoning step. Because a partial result set is byte-for-byte the same shape as a complete one, there is no structural cue — no error, no odd formatting — that would make the agent pause and double-check. That gap is compounded by an optimization toward fast single-pass answers: verifying completeness costs an extra round trip, and nothing in the agent's objective rewards taking it before aggregating or summarizing.

**Example**
```
A paginated order-history API returns the first 50 of 200 records with a
`has_more: true` flag. The agent's summarization step reads only the
returned array and computes "customer lifetime spend" from the 50 records
it has, presenting the partial sum as the customer's full total.
```

**Contributing Factors**
- Tool response includes a pagination/truncation flag that the agent's prompt or parsing logic doesn't surface or check.
- Partial results look structurally identical to complete ones (same shape, no obvious error), so nothing prompts a second look.
- Agent is optimized to answer quickly rather than verify completeness before aggregating or reasoning over a result set.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Truncated-list aggregation | Return a paginated result with has_more=true and only a fraction of total records | Agent fetches remaining pages (or explicitly caveats the answer as partial) before computing an aggregate | Agent computes a sum/count/summary from only the first page and presents it as complete |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| partial_result_treated_as_complete_rate | < 2% of paginated/truncated responses | Instrument tool responses with completeness flags and check whether the agent's subsequent action accounted for them |

---

## Mitigation Strategies

### Prevention
1. **Explicit Completeness Contract Parsing**: Tool responses that can be partial (truncated text, `omitted_fields`, `warning: partial`) must surface a structured completeness indicator; the agent-calling layer parses this indicator before handing the response to the model and refuses to label downstream output as authoritative if it is false.
2. **Truncation-Aware Prompting**: System/tool-use prompts explicitly instruct the agent to check for and surface truncation/warning fields to the user (e.g., "showing 20 of 340 results") rather than presenting partial data as if it were the full answer.
3. **Confidence Labeling on Partial Data**: Any answer built partly or wholly from a flagged-partial tool response is automatically tagged with a lowered confidence level and a caveat sentence template, preventing partial data from being presented with full-confidence phrasing by default.

### Detection & Response
1. **Partial-Flag-to-Answer Correlation Check**: Automated review compares whether tool responses containing `partial=true`/truncation warnings were acknowledged in the agent's final answer; unacknowledged partial responses are logged as misuse incidents.
2. **Truncation Rate Monitoring per Tool**: The rate at which each tool returns partial/truncated responses is tracked; sustained high rates may indicate the agent should be using pagination, higher limits, or a different endpoint rather than repeatedly hitting truncation.
3. **User Correction Signal Mining**: Conversations where the user later corrects the agent with more complete information ("actually there are more than that") are flagged and cross-referenced against whether the original tool response was flagged partial, confirming misuse patterns.

### Architecture Patterns
1. **Completeness-Gated Response Assembly**: The answer-generation step receives a structured completeness manifest (which sub-results are full versus partial) alongside the data itself, and the templating/prompting layer enforces caveat insertion whenever any input is marked partial.
2. **Partial-Result Escalation Path**: When a tool response is partial and the missing portion is material (financial totals, safety-critical data), the orchestrator automatically attempts a follow-up call (increase limit, paginate, retry) before allowing the agent to answer, rather than passing the partial state straight through.
3. **Warning-Field Passthrough Enforcement**: A response-validation middleware blocks any agent-generated summary that omits a required caveat when the source tool response carried a `warning`/`truncated` field, acting as a hard gate rather than relying on the model to remember.

### Metrics
1. **unacknowledged_partial_response_rate_percent**: Target: 0%; Alert threshold: > 2%
2. **tool_partial_response_rate_percent**: Target: tool-specific baseline; Alert threshold: > 2x baseline
3. **caveat_presence_on_partial_answers_percent**: Target: 100%; Alert threshold: < 98%
4. **user_completeness_correction_rate_per_week**: Target: < 2; Alert threshold: >= 5

### Alerts
1. **Partial Data Presented as Complete** (P1 - Critical): Condition - an answer was generated from a partial/truncated tool response with no caveat on a high-stakes topic (finance, safety). Action: Block/retract response, force re-fetch of complete data, notify user of correction.
2. **Truncation Rate Spike for Tool** (P2 - Warning): Condition - tool_partial_response_rate_percent exceeds 2x baseline. Action: Investigate limit/pagination configuration for that tool, consider raising the default page size.
3. **Missing Caveat Pattern** (P3 - Info): Condition - caveat_presence_on_partial_answers_percent drops below target over a week. Action: Review and reinforce the prompt template enforcing caveat insertion.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| unflagged_partial_result_rate_percent | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Partial Result Used As Complete | Agent produces an aggregate/answer from a response flagged has_more/truncated without fetching the rest | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
