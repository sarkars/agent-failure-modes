# Hallucinated On-Hand Quantity When Inventory API Fails Silently

## Issue: When an Inventory-Optimization Agent's Call to the Live Inventory-Lookup Tool Returns a Malformed, Partial, or Empty Response for a Given SKU, the Agent's Replenishment or Allocation Recommendation States a Specific On-Hand Quantity Presented as Retrieved Data, Fabricated to Complete the Recommendation Rather Than Reflecting Any Actual API Value

**Frequency**: Occasional

**Symptoms**
- A replenishment recommendation cites a specific on-hand unit count for a SKU that does not match the actual inventory-system record when independently queried for the same SKU and timestamp
- The inventory-lookup tool call immediately preceding the recommendation, visible in the agent's trace, shows an error response, timeout, or empty payload rather than a successful data return
- Re-running the same recommendation after the inventory-lookup tool call succeeds (e.g., after retry) produces a recommendation citing a genuinely different, verifiable on-hand quantity, isolating the fabrication to the prior tool failure
- The fabricated quantity is plausible relative to the SKU's typical stocking pattern, making it indistinguishable from a real value without independently querying the inventory system
- A purchase order is issued based on the fabricated on-hand figure, resulting in either an unnecessary reorder or a missed reorder once the true on-hand quantity is later reconciled

**Root Cause**
When the inventory-lookup tool fails or returns incomplete data, the model can complete its expected recommendation output by generating a plausible on-hand quantity consistent with the SKU's typical stocking pattern, rather than explicitly reporting that the lookup failed and no current on-hand data is available. This produces a recommendation that is stylistically indistinguishable from one grounded in real data, because nothing in the default workflow forces the agent to treat a failed inventory-lookup call as a hard stop rather than a gap to fill with a plausible completion.

**Example**
```
Inventory-optimization agent is asked to recommend a reorder quantity for SKU-48213 ahead of the weekend replenishment cycle
Inventory-lookup tool call for SKU-48213 returns a malformed response due to a backend sync delay between the warehouse management system and the inventory API
Agent's recommendation nonetheless states: "Current on-hand for SKU-48213 is 340 units; recommend reordering 200 units to reach target stock level," presenting 340 as a retrieved figure
Actual on-hand for SKU-48213, confirmed by direct warehouse query, is 95 units; the 340 figure was fabricated to complete the recommendation
Purchase order is issued for only 200 units based on the fabricated baseline, leaving the SKU under-stocked relative to its actual need once the real on-hand figure is later reconciled
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible-sounding content to fill gaps left by failed or incomplete tool calls, a well-characterized hallucination subtype distinct from a reasoning error over real data | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that agents frequently do not surface a failed or degraded tool call as a hard stop, instead proceeding to generate output as if the call had succeeded | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Calibration research in tool-using agents notes that confidence in a generated figure is not equivalent to that figure being grounded in an actual successful tool response | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- Replenishment-recommendation prompt implicitly rewards a complete, well-supported-sounding recommendation, with no explicit instruction that reporting a failed inventory-lookup call as a hard stop is an acceptable output
- No automated step verifies that the on-hand quantity cited in a finalized recommendation matches the value actually returned by the inventory-lookup tool call in the same session
- Inventory-lookup tool failures (malformed responses, timeouts) are not surfaced prominently in the agent's output, so a reviewer has no visible signal that the underlying data call did not succeed

---

## Mitigation Strategies

1. **Mandatory Value Resolution Check**: Before a replenishment recommendation is finalized, automatically verify that the cited on-hand quantity matches the value actually returned by the inventory-lookup tool call logged in the same session, flagging any mismatch
2. **Hard Stop on Lookup Failure**: Require the agent to explicitly report a failed, malformed, or empty inventory-lookup response as a blocking gap, rather than proceeding to generate a recommendation as if the call had succeeded
3. **Retry-Before-Recommend Policy**: Require a failed inventory-lookup call to be retried at least once, and escalated to a human if it continues to fail, before the agent proceeds to recommendation generation
4. **Tool-Call Provenance Logging**: Log which specific tool call produced the on-hand quantity cited in each recommendation, so any cited quantity with no corresponding successful tool-call log entry is automatically flagged as a likely fabrication

### Metrics
- Rate of finalized recommendations whose cited on-hand quantity does not match the logged inventory-lookup tool-call result
- Number of purchase orders issued following a recommendation generated despite a logged inventory-lookup failure
- Mean time-to-detection for fabricated on-hand figures, measured from recommendation issuance to reconciliation discrepancy

### Alerts
- A purchase order is issued based on a recommendation whose cited on-hand quantity fails value-resolution check against the logged tool-call result → P1
- A replenishment recommendation is generated despite a logged inventory-lookup tool failure with no retry → P2
- Fabricated-quantity rate across replenishment recommendations exceeds baseline for two consecutive reporting periods → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
