# Hallucinated Corporate-Action Adjustment Factor on Incomplete Vendor Record

## Issue: When a Portfolio Agent's Call to the Market-Data Vendor API for a Corporate Action (a Stock Split, Spin-Off, or Special Dividend) Returns an Incomplete Record -- the Adjustment Ratio Field Is Null Due to a Vendor Data Gap -- the Agent's Recalculated Position or Price Adjustment States a Specific Adjustment Factor Presented as Retrieved From the Vendor Feed, Fabricated to Complete the Recalculation Rather Than Reflecting Any Actual Vendor Data

**Frequency**: Occasional

**Symptoms**
- A recalculated position size, cost basis, or historical price series cites a specific corporate-action adjustment ratio that does not match the value actually on file with the vendor or the issuer's official corporate-action announcement when independently checked
- The vendor API call immediately preceding the recalculation, visible in the agent's trace, shows a null or missing adjustment-ratio field rather than a complete corporate-action record
- Re-running the same recalculation after the vendor feed's data gap is resolved (e.g., on a subsequent sync) produces a recalculation citing the genuinely correct adjustment factor, isolating the fabrication to the prior incomplete vendor record
- The fabricated ratio is plausible for the type of corporate action involved (a common split ratio, a round-number spin-off allocation), making it indistinguishable from a real vendor-reported value without independently checking the issuer's official announcement
- Position sizes or historical performance figures computed using the fabricated ratio are silently wrong, surfacing only when reconciled against a custodian statement or a corrected vendor feed

**Root Cause**
When the market-data vendor's corporate-action record is incomplete, the model can complete its expected recalculation by generating a plausible adjustment ratio consistent with common patterns for that type of corporate action, rather than explicitly reporting that the vendor record is incomplete and the recalculation cannot proceed without it. This produces a recalculated figure that is stylistically indistinguishable from one grounded in real vendor data, because nothing in the default workflow forces the agent to treat an incomplete corporate-action record as a hard stop rather than a gap to fill with a plausible completion.

**Example**
```
Portfolio agent processes a recently announced stock split for a held security and calls the market-data vendor API for the corporate-action adjustment ratio
Vendor API returns a record confirming the split occurred but with a null adjustment-ratio field, due to a known vendor data-sync gap for same-day corporate-action announcements
Agent's recalculation nonetheless states: "Position adjusted for 2-for-1 split; new share count and cost basis recalculated accordingly," presenting "2-for-1" as a retrieved vendor value
The actual split, confirmed by the issuer's official announcement, is a 3-for-2 split; the "2-for-1" ratio was fabricated based on it being the most common split ratio pattern
Position's share count and cost basis are recalculated incorrectly, and the resulting performance figures are silently wrong until reconciled against a custodian statement reflecting the correct 3-for-2 adjustment
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible-sounding content to fill gaps left by failed or incomplete tool and API calls, a well-characterized hallucination subtype distinct from a reasoning error over complete data | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that agents frequently do not surface a failed or incomplete tool response as a hard stop, instead proceeding to generate output as if the call had succeeded | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Calibration research in tool-using agents notes that confidence in a generated figure is not equivalent to that figure being grounded in an actual successful, complete tool response | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- Recalculation prompt implicitly rewards a complete, confident-sounding adjustment, with no explicit instruction that reporting an incomplete vendor record as a hard stop is an acceptable output
- No automated step verifies that the adjustment ratio cited in a finalized recalculation matches the value actually returned by the vendor API call in the same session
- Vendor data-sync gaps for same-day corporate-action announcements are a known, recurring pattern that is not flagged prominently enough in the agent's output for a reviewer to notice the underlying record was incomplete

---

## Mitigation Strategies

1. **Mandatory Value Resolution Check**: Before a corporate-action recalculation is finalized, automatically verify that the cited adjustment ratio matches the value actually returned by the vendor API call logged in the same session, flagging any mismatch
2. **Hard Stop on Incomplete Vendor Record**: Require the agent to explicitly report a null or missing adjustment-ratio field as a blocking gap, holding the affected position's recalculation pending rather than fabricating a plausible ratio
3. **Cross-Source Confirmation for Corporate Actions**: Require any corporate-action adjustment to be confirmed against a second source (the issuer's official announcement or a secondary vendor feed) before being applied, rather than relying on a single vendor API call
4. **Retry-and-Hold Policy for Known Sync-Gap Windows**: For corporate-action types known to have same-day vendor data-sync gaps, require an automatic retry after a defined delay and hold the recalculation pending rather than proceeding on an incomplete record

### Metrics
- Rate of finalized corporate-action recalculations whose cited adjustment ratio does not match the logged vendor API response
- Number of position recalculations proceeding despite a logged incomplete corporate-action vendor record
- Mean time-to-detection for fabricated adjustment ratios, measured from recalculation to custodian-reconciliation discrepancy

### Alerts
- A position recalculation is applied using an adjustment ratio that fails value-resolution check against the logged vendor response → P1
- A corporate-action recalculation proceeds despite a logged incomplete vendor record with no retry or hold → P1
- Fabricated-adjustment-ratio rate across corporate-action recalculations exceeds baseline for two consecutive reporting periods → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
