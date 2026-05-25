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

**Mitigation Strategies**
1. **Computation offloading**: Move calculations to environment
2. **Pre-computed rankings**: Return data already sorted
3. **Aggregate functions**: Provide tools that compute summaries
4. **Structured output**: Return data in machine-processable format
5. **Validation tools**: Let agent verify its calculations

**Detection**
- Numerical results that don't match source data
- Ranking mismatches between agent output and tool data
- Aggregation totals that don't sum correctly
- User corrections on computational errors

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Tool output processing as exploitation failure mode
- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Processing error patterns
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Computational failure analysis
