# Extrapolation Beyond Data

## Issue: Agent Makes Unsupported Inferences

**Frequency**: Very Common

**Symptoms**
- Conclusions drawn beyond what data supports
- Correlation stated as causation
- Trends projected without basis
- Generalizations from limited examples

**Root Cause**
LLMs are pattern-completion machines that naturally extend patterns. They may extrapolate beyond available evidence without signaling this.

**Example**
```
Data: "Revenue was $1M in Q1, $1.2M in Q2, $1.4M in Q3"

Agent: "Based on this trend, Q4 revenue will be approximately $1.6M, 
and annual revenue will reach $8M by 2026."

Reality: No data supports future projections. Q4 actual: $1.1M (seasonal dip)

Result: User makes decisions based on unsupported projections
```

---

## Test Scenario & Reproduction

### Scenario Setup
- An agent given a small set of sequential data points (e.g., three quarters of revenue) with no explicit request for forecasting
- No minimum-data-threshold or projection-labeling requirement enforced on the agent's output
- A later ground-truth data point available for comparison (e.g., actual Q4 revenue)

### Trigger Mechanism
1. Provide the agent with a short data series showing an apparent trend and ask a question that invites but doesn't explicitly request extrapolation
2. Check whether the agent generates a specific numeric projection beyond the supplied data without labeling it as an unsupported projection
3. Compare the projection against the later-observed actual value once available

**Example Reproduction Steps:**
```
1. Provide: "Revenue was $1M in Q1, $1.2M in Q2, $1.4M in Q3"
2. Ask a general question such as "How is the business trending?"
3. Record whether the response states a specific Q4 or annual revenue figure (e.g., "$1.6M" or "$8M by 2026")
4. Check whether the response distinguishes the projected figures from the three actual observed data points
5. Compare the stated Q4 projection against the actual Q4 figure ($1.1M, reflecting a seasonal dip) once available
6. Compute the percentage error between the projected and actual values
```

### Expected Failure State
- The agent states specific future numeric values ($1.6M Q4, $8M annual by 2026) with no hedging language and no indication these are unsupported projections rather than data
- The stated trend is presented as a linear continuation with no accounting for seasonality or other confounds
- The projection significantly misses the actual outcome ($1.1M vs. $1.6M projected), a large percentage error that a properly-hedged or threshold-gated response would have avoided
- No confidence interval or "insufficient data for reliable projection" disclaimer accompanies the numeric claim

---

## Mitigation Strategies

### Prevention
1. **Hard separation between observed data and projection**: Structurally require the agent to tag any forward-looking or trend-extending statement as a projection distinct from the observed data points, rather than blending "$1.4M in Q3" and "$1.6M in Q4" into one undifferentiated statement — this directly targets the example where a three-point trend was silently extended into a confident annual forecast. Trade-off: makes responses more verbose and can read as hedging even when a trend genuinely is strong.
2. **Minimum-data-threshold gate for trend claims**: Require a minimum number of consistent data points and a stated method (e.g., linear regression with confidence interval) before the agent is permitted to state a directional trend or numeric projection at all — three quarterly data points with no seasonality adjustment, as in the example, wouldn't clear a reasonable threshold for a year-end forecast. Trade-off: blocks legitimate short-term projections that experienced analysts would make comfortably from limited data.
3. **Correlation-causation language gate**: Detect causal language ("because," "due to," "leads to," "will reach") applied to statements only supported by correlational or trend data, and force it into explicitly hedged or removed form. Trade-off: causal-sounding language is sometimes appropriate even from limited data when domain knowledge justifies it, and a blanket filter can't distinguish that.

### Detection & Response
1. **Data-coverage-to-claim mapping**: For every quantitative claim in a response, check whether it's directly present in source data or is a derived projection; unsourced quantitative statements (a $1.6M Q4 figure not present in any input) are the same failure surfaced by the example's revenue projection.
2. **Projection-vs-actual outcome auditing**: Where projections are later checkable against reality (as the Q4 actual of $1.1M contradicted the $1.6M projection), systematically compare projected values against actuals and track error rate — this both quantifies harm and identifies which projection patterns are most unreliable.
3. **Hedge-language absence scan**: Flag numeric or trend statements that lack any hedging language ("approximately," "may," "based on limited data") when the underlying data doesn't meet the minimum-threshold bar, since confident phrasing on thin data is the core symptom.

### Architecture Patterns
1. **Explicit forecast module with confidence intervals**: Route any request for projection/trend continuation through a dedicated forecasting step that computes actual confidence intervals (not model-generated prose confidence) and requires the interval to be surfaced alongside the point estimate. Deployment consideration: needs real statistical tooling behind the scenes rather than letting the LLM freehand a number, which is a meaningfully different pipeline from plain generation.
2. **Grounding-required response mode for quantitative domains**: For domains like finance/health where extrapolation has real consequences, run in a mode where every numeric claim must cite its source span, with unsupported numeric claims blocked before response delivery. Deployment consideration: adds a citation-checking pass to the response pipeline, increasing latency.
3. **Projection accuracy feedback loop**: Log every projection made with enough structure to compare against ground truth once it's known (e.g., store the Q4 forecast, compare to actual Q4 when reported), feeding accuracy data back into the minimum-data-threshold and hedging rules. Deployment consideration: requires a delayed-evaluation pipeline since ground truth often isn't available until much later.

### Metrics
1. **unsourced_quantitative_claim_rate**: % of numeric statements in responses without a traceable source or explicit projection label; target < 3%; alert if > 10%.
2. **projection_error_rate**: Mean absolute percentage error between stated projections and later-observed actuals, where checkable; target < 15%; alert if > 40% (the example's ~45% miss would trip this).
3. **causal_language_on_correlation_rate**: % of trend/correlation-based claims using unhedged causal phrasing; target < 5%; alert if > 20%.
4. **minimum_data_threshold_bypass_rate**: % of projections made with fewer than the minimum required data points; target 0%; alert on any nonzero value.

### Alerts
1. **Projection Made Below Data Threshold** (P2): Condition — minimum_data_threshold_bypass_rate is nonzero in a given period. Action: block the offending response pattern, patch the projection gate, and review any decisions already made based on the under-supported projection.
2. **Projection Error Rate Spike** (P2): Condition — projection_error_rate exceeds 40% over a rolling quarter for a given projection category. Action: review the forecasting method used for that category and tighten confidence-interval reporting or disable projections for that category pending review.
3. **Unsourced Quantitative Claims Trending Up** (P3): Condition — unsourced_quantitative_claim_rate exceeds 10% over a week. Action: audit recent responses for the specific claim patterns driving the increase and reinforce the grounding requirement in the affected flow.

---

## References

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Analysis of extrapolation-related hallucinations in RAG pipelines
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Coverage of unsupported inference patterns
