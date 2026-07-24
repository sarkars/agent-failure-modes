# Unit-Conversion Arithmetic Drift in LLM-Generated Reorder Quantity

## Issue: A Replenishment Agent Calls a Demand-Forecast Tool and a Lead-Time/Pack-Size Tool, Both of Which Return Correct Values, but Combines Them Into a Final Purchase-Order Quantity via Free-Text Reasoning Rather Than a Deterministic Calculation, Introducing Arithmetic and Unit-Conversion Errors the Individual Tool Calls Never Made

**Frequency**: Occasional

**Symptoms**
- Individual tool calls (demand forecast, lead-time, pack size, minimum order quantity) each return correct, verifiable values when checked independently, but the final recommended order quantity does not match what applying those values through the actual reorder formula would produce
- Errors cluster specifically around SKUs involving a unit conversion between the forecast's unit (eaches) and the ordering unit (cases, pallets), or a non-round pack size (e.g., 24-count cases, 18-unit inner packs)
- The agent's stated reasoning in its response narrative shows it performing the calculation in prose ("we need about 840 units, which at 24 per case is roughly 35 cases, so let's round up to 36") rather than invoking a calculation tool, and the intermediate arithmetic step contains a rounding or division error not present in any tool's actual output
- Re-prompting the identical tool outputs through a deterministic formula (rather than free-text reasoning) produces a different, correct quantity, isolating the error to the combination step rather than to any individual retrieved value
- Order-quantity errors are more frequent and larger in magnitude for SKUs with multiple chained unit conversions (eaches to inner packs to master cases to pallets) than for SKUs ordered directly in single units

**Root Cause**
Large language models generate numeric reasoning as token sequences rather than executing arithmetic operations, and multi-step unit conversions chained through natural-language reasoning are a well-documented weak point even when every input value is correct, because each conversion step is a fresh generation conditioned on the model's own prior (and potentially already-drifted) intermediate output rather than a verified computation. When a replenishment agent is prompted to "combine the forecast, lead time, and pack size into a recommended order quantity" as an open-ended reasoning step instead of populating a fixed formula with the retrieved values, the correctness of each individual tool call provides no guarantee about the correctness of the arithmetic performed on top of them.

**Example**
```
Demand-forecast tool returns: 840 units expected demand over the lead-time window (verified correct)
Lead-time tool returns: 3 weeks (verified correct)
Pack-size tool returns: 24 units per case, minimum order 5 cases (verified correct)
Agent's free-text combination: "Expected demand is 840 units. At 24 units per case, that's
  840 / 24 = 32 cases. Adding a small buffer, let's order 35 cases."
Actual arithmetic: 840 / 24 = 35 cases exactly (not 32); the agent's own division step introduced
  a 3-case (72-unit) shortfall before any buffer was even applied
Impact: Purchase order under-orders by roughly 2 cases net of the intended buffer, contributing
  to a stockout risk the demand forecast and lead-time data never actually indicated
```

**Key Statistics**
| Finding | Context |
|---|---|
| A synthesis of tool-use, planning, and reasoning failures across 27 benchmark and audit papers identifies numerical reasoning performed via free-form generation, rather than delegated to a deterministic computation step, as a recurring, distinct failure category from tool-invocation errors -- the tools can be called correctly while the reasoning layered on top of their outputs still introduces error | Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents (arXiv:2607.05775) |
| Tool-use error taxonomies for LLM agents document that misinterpretation or mishandling of tool outputs during downstream combination is a recurring error category separate from incorrect tool invocation itself, since the tool call and its correctness are independent of what the agent subsequently does with the returned value | ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems (arXiv:2510.17052) |
| In production inventory-replenishment systems, order-quantity discrepancies traced to multi-step unit-conversion arithmetic (rather than to forecast or lead-time data errors) typically concentrate on SKUs with non-round pack sizes or multi-tier packaging hierarchies | Illustrative range from inventory-operations audit practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Non-round pack size division | Forecast 840 units, pack size 24/case | Order quantity reflects exact division (35 cases) plus any explicitly-applied buffer | Recommended quantity implies an incorrect division result (e.g., 32 cases) |
| Multi-tier packaging conversion | Forecast in eaches, ordering unit is pallets (eaches to inner packs to cases to pallets) | Final pallet count matches a verified chained conversion | Final quantity diverges from the deterministic chained conversion by more than rounding tolerance |
| Minimum-order-quantity interaction | Forecast implies fewer units than the MOQ | Agent correctly applies MOQ as a floor without arithmetic drift in the comparison | Agent's stated comparison between calculated need and MOQ is arithmetically inconsistent |
| Deterministic-vs-freeform comparison | Same tool outputs run through (a) free-text agent reasoning and (b) a fixed formula | Both produce the same final quantity | Free-text reasoning result differs from the deterministic formula result |

### Evaluation Dataset
- **Source**: SKU replenishment scenarios constructed from real forecast/lead-time/pack-size combinations, each paired with the deterministically-correct order quantity per the actual reorder formula
- **Size**: 250+ scenarios, weighted toward non-round pack sizes and multi-tier packaging hierarchies
- **Key variations**: round vs. non-round pack sizes; single-tier vs. multi-tier unit conversion; MOQ binding vs. non-binding; buffer/safety-stock addition present vs. absent

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Arithmetic-consistency rate | > 99.5% | % of recommended order quantities matching the deterministic-formula result on the same tool outputs |
| Deterministic-computation coverage | 100% of order-quantity generation uses a calculation tool/function rather than free-text arithmetic | % of order-quantity outputs traceable to a calculator/formula tool call in the trace |
| Conversion-error magnitude | < 1 unit of ordering-unit deviation | Mean absolute deviation between recommended and deterministically-correct quantity, in cases/pallets |

### Automated Checks
```python
def check_arithmetic_drift(tool_outputs: dict, recommended_qty: float) -> dict:
    """Recompute the reorder quantity deterministically and compare to the agent's recommendation."""
    forecast = tool_outputs["forecast_units"]
    pack_size = tool_outputs["pack_size"]
    moq = tool_outputs.get("moq_cases", 0)
    import math
    deterministic_cases = max(math.ceil(forecast / pack_size), moq)
    delta = abs(recommended_qty - deterministic_cases)
    return {
        "deterministic_quantity": deterministic_cases,
        "recommended_quantity": recommended_qty,
        "delta": delta,
        "arithmetic_drift_detected": delta > 0.5,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Deterministic Formula Tool for Final Combination**: Require the agent to call a calculation tool/function that takes the retrieved forecast, lead-time, pack-size, and MOQ values as structured arguments and returns the order quantity, rather than allowing the final number to be produced by free-text reasoning
2. **Structured-Argument Handoff**: Pass tool outputs to the combination step as typed, structured values rather than embedding them in a natural-language prompt the model then reasons over in prose, removing the opportunity for token-level arithmetic drift
3. **Unit-Conversion-Aware Validation**: For SKUs with multi-tier packaging, require the calculation step to explicitly carry and validate the unit at each conversion stage rather than performing an implicit end-to-end conversion in one generative step

### Detection & Response
1. **Deterministic Cross-Check on Every Recommendation**: Automatically recompute every agent-recommended order quantity using the deterministic formula and the same tool outputs, flagging any deviation beyond rounding tolerance
2. **Conversion-Error Pattern Monitoring**: Track order-quantity deviations by packaging-hierarchy complexity (single-tier vs. multi-tier) to detect whether drift concentrates on specific conversion patterns

### Architecture Patterns
- **Tool-Outputs-to-Formula Pipeline**: Structurally separate retrieval (forecast, lead-time, pack-size tools) from computation (a dedicated deterministic calculation function) from narrative (buffer/rationale explanation in prose), so only the last stage is open-ended generation
- **Recommendation-with-Recomputation Gate**: Require every generated order-quantity recommendation to pass an automated deterministic-recomputation check before being surfaced to a buyer, blocking silent arithmetic drift from reaching a purchase order

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `reorder.arithmetic_drift.count` | Recommendations deviating from the deterministic-formula result beyond rounding tolerance | > 0 per day |
| `reorder.deterministic_tool_coverage` | % of order-quantity outputs traceable to a calculation-tool call | < 100% |
| `reorder.conversion_error_magnitude.mean` | Mean absolute deviation between recommended and deterministic quantity | > 0.5 ordering units |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Arithmetic Drift Detected | Recommended order quantity deviates from deterministic recomputation beyond tolerance | P2 | Block the purchase order pending buyer review; recompute and resubmit |
| Deterministic Tool Bypass | Order-quantity recommendation generated with no calculation-tool call in trace | P1 | Halt autonomous ordering for affected SKU category pending architecture fix |

---

## References
- [Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents](https://arxiv.org/abs/2607.05775)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/abs/2510.17052)
