# Tool Output Processing Failure

## Issue: Agent Makes Errors When Processing Tool Results

**Frequency**: Common

**Symptoms**
- Computational errors on tool output data
- Incorrect comparisons or rankings
- Aggregation mistakes (sums, averages, counts)
- Logic errors when applying filters

**Root Cause**
Agent makes computational errors (e.g., comparisons, ranking) when processing information gathered from tool outputs. LLMs are fundamentally language models, not calculators, and struggle with precise numerical operations on retrieved data.

**Example**
```
Task: "Find the employee with the highest sales last quarter"

Tool output (get_sales_data):
| Employee | Q3 Sales  |
|----------|-----------|
| Alice    | $127,450  |
| Bob      | $98,200   |
| Carol    | $142,800  |
| Dave     | $131,500  |

Agent processing:
"Looking at the numbers... Alice has $127,450 which 
appears to be the highest amount."

Agent answer: "Alice has the highest sales at $127,450"

Actual highest: Carol at $142,800

Result: Agent made comparison error, wrong answer
```

**Common Processing Errors**
- **Comparison errors**: Wrong ordering of numeric values
- **Aggregation errors**: Incorrect sums, averages, or counts
- **Filter errors**: Applying wrong conditions to data
- **Format errors**: Misreading numbers with commas, currencies
- **Ranking errors**: Selecting wrong top/bottom N items

**Key Statistics**
From Aegis study: Tool output processing failures are a major category under exploitation failures, accounting for significant task failures especially on data-heavy operations.

**Contributing Factors**
- LLMs not designed for precise computation
- Large result sets exceed reasoning capacity
- Number formatting inconsistencies
- Complex multi-column comparisons

## Mitigation Strategies

### Prevention
1. **Offload comparisons and rankings to a deterministic tool, never eyeball them in-context**: Since the root cause is explicitly that "LLMs are fundamentally language models, not calculators," never ask the agent to visually scan a table like the Q3 sales example and pick the max — provide a `find_max(data, field)` or `rank_by(data, field)` tool that returns the answer computed in code, guaranteeing Carol's $142,800 is correctly identified over Alice's $127,450. Trade-off: requires anticipating which computations agents will need and building tools for each, which can't cover every ad hoc analytical question.
2. **Pre-sort and pre-aggregate at the data source**: Have `get_sales_data` accept a `sort_by`/`order` parameter and return results already ranked, so "highest sales" is answered by reading row one of the response rather than the agent performing a four-way comparison itself. Trade-off: shifts complexity into tool parameter design and requires the agent to correctly request the sort in the first place.
3. **Normalize number formats before they reach the agent**: Strip currency symbols and thousands separators (`$142,800` → `142800`) in the tool response so formatting inconsistencies don't compound the comparison difficulty called out under format errors. Trade-off: losing the formatted display string means the agent must re-format for user-facing output, adding a separate formatting step.

### Detection & Response
1. **Ground-truth comparison audits on computed answers**: For any agent answer involving max/min/sum/average, recompute the correct value programmatically from the same tool output and diff against what the agent reported — this directly catches cases like the example where Alice ($127,450) was reported instead of the true max, Carol ($142,800).
2. **Ranking mismatch checks**: When the agent claims item N is "highest" or "lowest," verify against a sorted version of the same dataset; log every mismatch tagged with the specific comparison type (max/min/top-N).
3. **Aggregation total verification**: Where the agent reports a sum, average, or count derived from tool output, independently recompute it and flag divergence — this catches the "aggregation errors" category distinctly from ranking errors.

### Architecture Patterns
1. **Code-execution sandbox for numeric operations**: Route any multi-value comparison or aggregation through a sandboxed code interpreter (e.g., a Python execution tool) rather than LLM mental arithmetic, since this is the most direct fix for a model performing "computation" through pattern-matching rather than calculation; deployment consideration — needs sandboxing/resource limits to prevent runaway or malicious code execution.
2. **Summary-statistics tools as first-class citizens**: Ship dedicated `sum()`, `average()`, `top_n()` tools alongside data-retrieval tools so agents have a deterministic path for the "Aggregate functions" need identified in the root cause, rather than being forced to reason over raw tabular output; deployment consideration — adds tool surface area the agent must learn to select correctly (risk of wrong-tool-selection failures if not well-documented).
3. **Self-verification pass**: After the agent produces a computed answer, run a second deterministic check (not another LLM call) that recomputes the same value from source data and blocks/flags responses that don't match before they reach the user; deployment consideration — adds latency to every computation-involving response, so reserve it for high-stakes numeric claims (financial, ranking-based decisions).

### Metrics
1. **computation_accuracy_rate**: Target > 99% of agent-reported computed values (max/min/sum/avg) matching independently recomputed ground truth; Alert if < 95% over a sampled daily audit.
2. **ranking_mismatch_rate**: Target < 1% of top-N/highest/lowest claims disagreeing with a sorted recomputation; Alert if > 5% over a week.
3. **aggregation_error_rate**: Target < 1% of reported sums/averages/counts diverging from recomputed values; Alert if > 5%.
4. **large_dataset_error_rate** (rows > 20): Target: tracked separately from small datasets since large result sets are called out as a contributing factor; Alert if error rate on large datasets exceeds 2x the error rate on small datasets.

### Alerts
1. **Computation Accuracy Regression** (P1): Condition - computation_accuracy_rate drops below 95% in the daily audit. Action: page the team owning the affected tool chain, prioritize migrating that computation path to a code-execution or pre-aggregation tool.
2. **Ranking Mismatch Spike** (P2): Condition - ranking_mismatch_rate exceeds 5% for a given data domain (e.g., sales rankings) over a week. Action: add a sort_by parameter to the underlying data tool or introduce a dedicated top_n() tool for that domain.
3. **Large-Dataset Error Disparity** (P3): Condition - error rate on datasets > 20 rows exceeds 2x the small-dataset error rate. Action: investigate whether context truncation or reasoning-capacity limits are the driver, consider pagination or pre-aggregation for large result sets.

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Tool output processing as exploitation failure mode
- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Processing error patterns
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Computational failure analysis
