# Tool Parameter Errors

## Issue: Tool Parameter Errors

**Frequency**: Common

**Symptoms**
- Tools called with wrong parameters
- Page ranges incorrect
- Region coordinates misspecified
- Output format mismatches downstream needs

**Root Cause**
Agent must translate document understanding into specific tool parameters. Errors in this translation cause extraction failures.

**Example**
```
Agent intent: Extract table from page 5
Tool call: extract_table(page=4)  # Off-by-one error

Result: Wrong table extracted, agent proceeds with incorrect data
```

**Key Statistic**
37% of tool calls have silent parameter mismatches according to developer analysis.

## Mitigation Strategies

### Prevention
1. **Strict schema-enforced tool parameters**: Define tight, typed parameter schemas (e.g., page must be a positive integer within the document's actual page count, region must be within page bounds) and reject out-of-range or malformed calls at the tool boundary before execution, rather than letting the tool silently execute on a slightly-wrong parameter. Trade-off: requires the tool interface to know document metadata (page count, dimensions) upfront to validate against.
2. **Pre-execution intent-to-parameter confirmation**: Before executing an extraction tool call, have the agent restate its intent in natural language alongside the literal parameters it's about to pass (e.g., "extracting the table on page 5, calling with page=4") so an off-by-one or misalignment is visible in the trace and can be caught by a lightweight consistency check. Trade-off: adds a verification step and slight latency per tool call.
3. **Visual/structural region confirmation**: For spatial parameters (bounding boxes, page regions), have the agent — or a cheap secondary check — confirm the specified region actually contains the expected content type (e.g., "does this region look like a table?") before committing to the extraction, catching coordinate misspecification before it produces wrong data silently.

### Detection & Response
1. **Silent-mismatch monitoring via output-type validation**: Since parameter errors are often silent (the tool executes successfully but on the wrong input), validate tool *output* against expected characteristics of the intended target (e.g., expected table extraction should have a plausible column count matching the document's known table structure) to catch silent mismatches after the fact.
2. **Tool call parameter distribution monitoring**: Track the distribution of parameter values (page numbers relative to document length, region sizes) passed to each tool; parameters far outside the normal distribution for a document type are worth flagging even if individually valid.
3. **Retry-with-correction on detected mismatch**: When a downstream check indicates the wrong region/page was extracted, trigger an automatic retry with an adjusted parameter (e.g., page+1) before escalating to a full re-extraction or human review, since off-by-one errors are a common and cheaply-correctable subclass.

### Architecture Patterns
1. **Typed, validated tool interfaces (schema-first design)**: Design every document-processing tool with an explicit, strictly-typed parameter schema validated at the interface layer, independent of the calling agent's own self-checking — the tool itself should refuse impossible parameters (negative page numbers, regions outside page bounds) rather than trusting the caller.
2. **Verification-augmented tool wrapper**: Wrap raw extraction tools with a verification layer that checks output plausibility against the stated intent before returning results to the agent, closing the loop between "what was asked for" and "what was returned" within the tool call itself rather than leaving it to the agent's downstream reasoning.
3. **Structured tool-call logging with replay capability**: Log full tool call parameters and outputs so that, when a silent parameter mismatch is discovered downstream, the exact failing call can be replayed with corrected parameters without re-running the entire agent session.

### Metrics
1. **tool_parameter_validation_rejection_rate**: Target: track as baseline; Alert if it changes > 3x week-over-week (signals upstream reasoning about parameters has degraded)
2. **silent_parameter_mismatch_rate**: Target: < 2% of tool calls (measured via output-plausibility checks); Alert if > 5%
3. **off_by_one_error_rate**: Target: < 1% of page/region-based tool calls; Alert if > 3%
4. **retry_with_correction_success_rate**: Target: > 80% of flagged mismatches resolved by automatic parameter correction; Alert if < 50%

### Alerts
1. **Silent Mismatch Rate Spike** (P2): Condition - output-plausibility validation flags mismatches on more than 5% of tool calls for a document type. Action: Review recent changes to document templates or the tool's parameter-generation prompt; sample flagged calls for root cause.
2. **Validation Rejection Anomaly** (P3): Condition - tool parameter validation rejection rate changes more than 3x from baseline. Action: Investigate whether document structure changed (e.g., page counts, layout) in a way the agent's parameter-generation logic doesn't account for.
3. **Auto-Correction Failure** (P2): Condition - automatic retry-with-correction success rate falls below 50%. Action: Escalate to human review for that document type rather than continuing to burn retries on a correction strategy that isn't working.

## References

- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - 37% parameter mismatch rate
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Parameter validation
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Tool call error patterns
