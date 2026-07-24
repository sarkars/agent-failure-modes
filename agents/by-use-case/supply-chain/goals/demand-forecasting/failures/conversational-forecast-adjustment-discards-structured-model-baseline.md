# Conversational Forecast Adjustment Discards Structured Model Baseline

## Issue: When a Planner Asks the Agent to Adjust a Forecast Conversationally ("Bump Up SKU X for the New Campaign"), the Agent Regenerates an Entirely New Forecast Number Through Free-Text Reasoning Instead of Applying a Bounded Delta to the Existing Statistical Model's Output, Silently Discarding the Baseline's Seasonality and Trend Components

**Frequency**: Occasional

**Symptoms**
- The post-adjustment forecast number bears little numerical relationship to the pre-adjustment statistical baseline, even for SKUs where the requested adjustment was a modest, targeted change ("increase for the campaign week")
- Seasonality and trend components that were present in the underlying statistical model's output (e.g., a known weekday pattern, a documented seasonal ramp) are not visible in the adjusted number, which instead reads as a smoothed, round approximation
- The agent's conversational response states a specific adjusted quantity but the execution trace shows no call back to the forecasting model with a structured delta parameter — the number was produced directly by the language model reasoning over the request and the previous forecast value in prose
- Forecast accuracy (measured against actual demand) for conversationally-adjusted SKU-weeks is measurably worse than for the same SKUs' non-adjusted, model-generated baseline weeks, despite the adjustment nominally being an improvement (accounting for new information the base model didn't have)
- Re-deriving the adjustment by applying the planner's stated delta (e.g., "+15%") programmatically to the original baseline produces a materially different, and more internally consistent, number than what the agent actually returned

**Root Cause**
The agent is prompted to be helpful and responsive to conversational forecast-adjustment requests, and producing a plausible-sounding adjusted number is something the model can do directly through generation, without necessarily invoking the forecasting model's own adjustment or override interface. Because the model's free-text reasoning over "the old forecast was N, apply this campaign effect" is a fresh generative act rather than a computation performed on N's actual internal structure (its seasonality index, trend component, base rate), the resulting number reflects the model's approximation of what a reasonable adjusted forecast might look like rather than the original statistical model's decomposition with a validated delta applied on top — and nothing in the interaction requires the agent to route the request back through the structured model rather than answering conversationally.

**Example**
```
Baseline statistical forecast for SKU X, week of promotion: 1,240 units (composed of a
  680-unit base rate, a 1.4x seasonal index for that week, and a documented weekday pattern)
Planner: "Can you bump this up to account for the new social media campaign we're running
  that week?"
Agent's conversational response: "Sure, accounting for the campaign, I'd estimate around
  1,500 units for that week." -- produced by reasoning in prose over the stated baseline and a
  generic sense of "campaigns usually help," with no call to the forecasting model's
  adjustment/override endpoint
Correct approach: Call apply_demand_adjustment(sku="X", week=..., adjustment_type="campaign_lift",
  delta_pct=X) so the seasonal index and trend components are preserved and the delta is applied
  on top of, not instead of, the structured baseline
Impact: The adjusted 1,500 figure has silently dropped the documented weekday pattern that
  the original 1,240 baseline was built on, and the actual campaign lift factor used is
  whatever the model happened to generate rather than a validated, reviewable delta
```

**Key Statistics**
| Finding | Context |
|---|---|
| A synthesis of tool-use, planning, and reasoning failures in LLM agents identifies free-form generation substituting for a structured computation or tool invocation as a recurring, distinct failure category, present even when the agent has access to and has previously used the correct structured interface | Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents (arXiv:2607.05775) |
| Survey work on multi-agent and agentic LLM system failures finds that conversational, natural-language handling of what should be a structured update operation is a recurring source of state divergence between what a system of record reflects and what an agent reports to a user | Why Do Multi-Agent LLM Systems Fail? (MAST) (arXiv:2503.13657) |
| In production demand-planning tools, forecast-accuracy metrics are typically tracked in aggregate rather than segmented by whether a given SKU-week's forecast passed through a conversational adjustment path versus the unmodified statistical baseline, obscuring an accuracy gap between the two if one exists | Illustrative range from demand-planning operations practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Percentage-delta adjustment request | Planner requests "+15% for the campaign week" | Agent calls the structured adjustment endpoint with delta_pct=15 applied to the baseline; resulting number preserves seasonality/trend structure | Adjusted number has no traceable relationship to baseline x 1.15, and no adjustment-tool call in trace |
| Vague qualitative adjustment request | Planner requests "bump it up a bit for the campaign" | Agent asks for or proposes a specific delta and applies it via the structured endpoint | Agent silently generates a new absolute number with no delta parameter or tool call |
| Adjustment then re-query | Planner requests an adjustment, then later asks "what's the current forecast for that SKU-week" | Second answer reflects the same structured-endpoint-derived number, consistent with the first | Second answer differs from the first, indicating the "adjustment" was never actually persisted to the model |
| No-adjustment-needed baseline comparison | Same SKU-week forecast requested with and without an intervening adjustment conversation | Non-adjusted baseline is reproducible and matches the model's direct output | Baseline number drifts across repeated queries even without any adjustment request |

### Evaluation Dataset
- **Source**: Historical conversational forecast-adjustment requests paired with the original statistical baseline and the actual downstream demand outcome
- **Size**: 150+ adjustment conversations across a range of adjustment types (percentage delta, qualitative "increase/decrease," event-based lift)
- **Key variations**: quantitative vs. qualitative adjustment requests; single adjustment vs. sequential adjustments to the same SKU-week; adjustment requested well before vs. close to the forecast week

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Structured-adjustment coverage | 100% of conversational adjustments routed through the adjustment endpoint | % of adjustment responses with a logged `apply_demand_adjustment` call carrying an explicit delta |
| Baseline-consistency rate | > 99% | % of adjusted forecasts whose seasonality/trend components remain traceable to the original baseline's decomposition |
| Adjusted-vs-baseline accuracy gap | ≤ baseline forecast error | Compare forecast error (vs. actual demand) for conversationally-adjusted SKU-weeks against non-adjusted baseline SKU-weeks |

### Automated Checks
```python
def check_ungrounded_forecast_adjustment(trace: list[dict], baseline: float, adjusted: float) -> dict:
    """Flag a forecast adjustment with no structured delta call, or a magnitude inconsistent with any stated delta."""
    adjustment_calls = [c for c in trace if c["tool"] == "apply_demand_adjustment"]
    if not adjustment_calls:
        return {"ungrounded_adjustment": True, "reason": "no structured adjustment call in trace"}
    stated_delta_pct = adjustment_calls[-1]["args"].get("delta_pct")
    if stated_delta_pct is not None:
        expected = baseline * (1 + stated_delta_pct / 100)
        drift = abs(adjusted - expected) / expected if expected else None
        return {
            "ungrounded_adjustment": drift is not None and drift > 0.05,
            "expected_value": expected,
            "actual_value": adjusted,
        }
    return {"ungrounded_adjustment": False}
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Structured-Adjustment Endpoint**: Require any conversational forecast-change request to be translated into an explicit, typed delta (percentage, absolute units, or named adjustment reason) passed to the forecasting model's own adjustment interface, rather than allowing the agent to generate a replacement number directly
2. **Delta-Confirmation Before Application**: When the planner's request is qualitative ("bump it up"), require the agent to propose and confirm a specific delta before applying it, making the adjustment magnitude an explicit, reviewable value rather than an implicit generative choice
3. **Baseline-Decomposition Preservation Check**: Validate that the adjusted forecast's seasonality and trend components remain traceable to the original baseline's decomposition, rejecting adjustments that would replace rather than augment the structured components

### Detection & Response
1. **Adjustment-Call-Absence Scanning**: Scan agent responses for forecast-adjustment language with no corresponding structured adjustment-tool call in the same session
2. **Segmented Accuracy Monitoring**: Track forecast accuracy separately for conversationally-adjusted vs. unmodified SKU-weeks to detect an emerging accuracy gap attributable to this failure mode

### Architecture Patterns
- **Delta-on-Baseline Pipeline**: Structurally require that any adjustment is computed as an operation applied to the retrieved baseline's structured fields (base rate, seasonal index, trend), not as an independent generative act that produces a new number from scratch
- **Adjustment Audit Log**: Log every conversational adjustment with its baseline value, requested delta, and resulting value as three explicit, separately-stored fields, so a delta-less adjustment (this failure's signature) is immediately visible in review

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `forecast.ungrounded_adjustment.count` | Conversational adjustments with no structured delta call | > 0 per week |
| `forecast.adjusted_vs_baseline_accuracy_gap` | Forecast error difference between adjusted and non-adjusted SKU-weeks | Adjusted error exceeds baseline error by > 10% |
| `forecast.adjustment_call.coverage` | % of adjustment responses with a logged structured adjustment call | < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Ungrounded Adjustment Applied | Forecast adjustment response given with no structured delta call in trace | P2 | Recompute via the structured endpoint; audit the affected SKU's purchasing implications |
| Adjustment Accuracy Gap Widening | Adjusted-forecast accuracy falls materially below baseline accuracy over a rolling window | P2 | Review adjustment-handling path; consider requiring human approval for conversational adjustments |

---

## References
- [Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents](https://arxiv.org/abs/2607.05775)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
