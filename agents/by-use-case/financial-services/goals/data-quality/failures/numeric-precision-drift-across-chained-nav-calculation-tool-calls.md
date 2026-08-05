# Numeric Precision Drift Across Chained NAV-Calculation Tool Calls

## Issue: An Agent Computing Net Asset Value Through a Multi-Hop Sequence of Tool Calls Re-Types the Intermediate Numeric Result as Text Between Steps Instead of Passing the Exact Value Forward, Introducing Rounding and Truncation Drift That Compounds Across the Chain

**Frequency**: Occasional

**Symptoms**
- A fund's reported NAV per share, computed by an agent chaining "fetch security prices" -> "compute per-security market value" -> "sum portfolio value" -> "divide by shares outstanding," differs from the NAV produced by the deterministic accounting system by a small but non-zero amount that grows with the number of holdings and calculation hops
- The discrepancy is not present when the same tool outputs are fed directly into a script that keeps exact values in memory; it only appears when an LLM agent restates an intermediate total in natural-language or freeform text before passing it to the next tool call
- Intermediate values in the agent's visible reasoning trace show values that have been rounded, truncated to a smaller number of decimal places, or reformatted (e.g., "$12,458,932.17" summarized as "approximately $12.46 million") before being used as literal input to a subsequent calculation step
- The error magnitude scales with the number of chained hops and the number of line items summed, consistent with compounding rounding rather than a single fixed offset
- Re-running the identical calculation twice with the same inputs produces slightly different final NAV figures, because the model's restatement of intermediate values is not perfectly deterministic across generations

**Root Cause**
When an LLM agent chains multiple tool calls to perform a multi-step numeric calculation, the value produced by one tool call is not always passed programmatically and exactly into the next call's arguments; instead, the model frequently generates the next call's arguments by reading and re-expressing the prior step's output as part of its own text-based reasoning, which is a lossy transcription rather than an exact value transfer. Text generation is not obligated to preserve full floating-point precision — the model may round for readability, truncate trailing digits, or informally summarize a large number — and because each of these transformations looks individually harmless, nothing in the pipeline flags the loss. In a single-hop calculation this produces a negligible, often invisible rounding difference; in a multi-hop calculation summing many line items and passing an aggregate through several further steps, each hop's small transcription loss compounds, and the final figure can diverge materially from the value a deterministic script would have produced by keeping the exact number in memory throughout. This failure mode does not occur in a purely deterministic pipeline, where the same intermediate values are passed by reference or as exact machine-precision figures between calculation stages rather than being mediated through natural-language text.

**Example**
```
Fund NAV calculation: 340 holdings, each priced individually via a price-lookup tool
Step 1: Agent calls get_price() for each holding, computing per-security market value (price x shares held)
Step 2: Agent sums the 340 per-security values, restating the running total in its reasoning text after each batch of holdings: "so far the total is approximately $48.2 million" instead of retaining the exact cumulative float
Step 3: Agent carries the rounded running total forward into subsequent batches, so each new batch is added to an already-rounded base rather than an exact cumulative sum
Step 4: Final portfolio value, as computed by the agent: $482,193,000 (rounded at multiple intermediate steps)
Deterministic accounting system's portfolio value (same underlying prices, exact arithmetic): $482,197,684.23
Step 5: Agent divides its rounded portfolio value by shares outstanding (18,400,000) to report NAV per share: $26.2061
Deterministic system's NAV per share: $26.2064
Impact: A $0.0003 per-share NAV discrepancy is below typical materiality thresholds for a single day, but the same chained-restatement pattern recurs daily, and on days with more holdings or larger position counts the compounding drift exceeds the fund's published NAV-error tolerance, triggering a reconciliation break against the deterministic system of record
```

**Key Statistics**
- Benchmarks evaluating LLMs on financial-statement verification tasks find that model performance on numeric consistency checks is sensitive to whether figures are presented rounded or unrounded, and that models struggle disproportionately with multi-step or cross-statement arithmetic compared to single-figure lookups
- Studies of tool-using agent chains find that a parameter-level error or precision loss introduced at one step propagates to an incorrect final answer in a majority of affected traces, and that agents' ability to detect and self-correct such propagated errors is inconsistent across models
- Multi-hop numeric reasoning tasks in LLM agent benchmarks show accuracy degrading as the number of chained calculation steps increases, consistent with compounding error rather than a single point-of-failure

---

## Mitigation Strategies

1. **Programmatic Value Passing Instead of Text-Mediated Restatement**: Architect the tool-calling pipeline so intermediate numeric results are passed directly between calculation steps by reference or as exact machine-precision values, never requiring the model to retype or summarize an intermediate figure as a precondition for the next call.
2. **Deterministic Aggregation Sidecar**: Run the summation, division, and other arithmetic operations in a deterministic function outside the LLM's text generation, with the agent only orchestrating which tool to call next rather than performing the arithmetic itself in prose.
3. **Full-Precision Echo Requirement**: Where text-mediated restatement cannot be avoided, require the agent to echo the full-precision value verbatim (not a rounded or "approximately" phrasing) and validate that echo against the source value before it is used downstream.
4. **Independent Reconciliation Against Deterministic NAV**: Compare every agent-computed NAV figure against the deterministic accounting system's NAV before publication, flagging any discrepancy beyond a tight, pre-defined tolerance rather than assuming small drift is immaterial.

### Metrics
- Per-hop and cumulative numeric drift between agent-computed intermediate values and their exact-precision equivalents
- NAV reconciliation break rate between agent-computed and deterministic-system NAV, and break magnitude
- Rate of intermediate values in the agent's reasoning trace that are rounded, truncated, or verbally summarized rather than passed at full precision

### Alerts
- Agent-computed NAV per share deviates from the deterministic accounting system's NAV per share beyond the fund's published tolerance → P1
- An intermediate calculation step's numeric restatement drops more decimal precision than the source tool call provided → P2

---

## Related Patterns
- [Tool Output Format Mismatch](../../../../../cross-cutting/operations/goals/tool-selection-sequencing/failures/tool-output-format-mismatch.md) — related tool-chaining failure from format/unit disagreement between tools, distinct from precision loss introduced by text-mediated restatement of an otherwise-compatible numeric value
- [Point-in-Time Data Violations](./point-in-time-data-violations.md) — related NAV/data-integrity failure in financial-services data pipelines, driven by temporal misalignment rather than numeric transcription loss
- [Fill-Confirmation Status Trusted Without Diffing Against Submitted Order Intent](../../trading-execution/failures/fill-confirmation-status-trusted-without-diffing-against-submitted-order-intent.md) — related failure to reconcile a chained tool-call output against ground truth before relying on it

## References

- [FinVerBench: Benchmark Validity and Calibration in Large Language Model Financial Statement Verification](https://arxiv.org/pdf/2605.29586)
- [Evaluating Tool-Using Language Agents: Judge Reliability, Propagation Cascades, and Runtime Mitigation in AgentProp-Bench](https://arxiv.org/html/2604.16706)
