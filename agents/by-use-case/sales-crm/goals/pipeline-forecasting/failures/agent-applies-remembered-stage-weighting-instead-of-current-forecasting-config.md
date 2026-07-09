# Agent Applies a Remembered Stage-Weighting Scheme Instead of the Current Forecasting Config

## Issue: A Pipeline-Forecasting Agent Computes Weighted-Pipeline Totals Using a Stage-to-Probability Weighting Scheme It Recalls From Earlier in Its Training or From an Older Cached Session, Rather Than Calling the Live Forecasting-Configuration Tool That Returns the Currently Active Weighting Scheme After RevOps Updated It, Producing a Forecast That Reflects a Retired Methodology

**Frequency**: Occasional

**Symptoms**
- The forecast narrative or computation references stage-probability weights (e.g., "Negotiation stage weighted at 70%") that do not match the weights currently returned by the forecasting-configuration tool for the same stage
- Querying the forecasting-configuration tool directly shows RevOps updated the weighting scheme (e.g., Negotiation now weighted at 55% following a methodology change), but the agent's output is consistent with the prior, now-retired scheme
- The mismatch concentrates in forecasts run shortly after a known weighting-scheme change, and disappears in forecasts run when the configuration tool's response is explicitly included in the prompt rather than left to the agent's own recall
- Asking the agent which weighting scheme it used produces a description matching the old scheme, even when the live tool was nominally available to it during that run
- Two forecasts run in immediate succession against the same pipeline snapshot, one with the configuration tool's response explicitly quoted back to the agent and one without, produce different weighted totals despite identical underlying deal data

**Example**
```
RevOps updates the official stage-weighting scheme: Negotiation stage moves from 70%
probability weight to 55%, reflecting observed close-rate data from the last two quarters
Forecasting agent is asked to compute this week's weighted pipeline total
Agent calls the forecasting-configuration tool, which returns the current scheme
including the updated 55% Negotiation weight, but the agent's computation narrative
states "Negotiation-stage deals weighted at 70% per standard methodology" -- the
retired figure -- and the total reflects that retired weight rather than the tool's
actual returned value
RevOps reviews the forecast, recognizes the weighting figure as the one retired two
months ago, and finds the configuration tool's logged response for that run did
contain the correct 55% figure
The weighted pipeline total is overstated because deals in Negotiation are counted
at a higher conversion likelihood than the currently active methodology supports
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Research on agent memory validity finds models frequently fail to recognize when a previously valid belief or remembered configuration has been invalidated by a more recent, structurally related observation, instead continuing to apply the outdated belief in subsequent reasoning | [STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?](https://arxiv.org/html/2605.06527v1) |
| Survey work on retrieval-augmented generation finds that when a model's parametric knowledge conflicts with retrieved or tool-returned evidence, the conflict resolution is unpredictable and models do not reliably defer to the more current, externally retrieved source | [When Retrieval Succeeds and Fails: Rethinking Retrieval-Augmented Generation for LLMs](https://arxiv.org/html/2510.09106v1) |
| General agent failure taxonomies identify reliance on remembered or cached configuration over a live tool's returned value as a distinct mechanism separate from simple tool-call omission, since the tool is actually called but its result is not what drives the final output | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The forecasting agent's prompt calls the configuration tool but does not require the agent to quote the tool's returned weighting values verbatim into its computation before applying them, leaving room for the agent's own recalled scheme to leak into the actual calculation
- The previous stage-weighting scheme was stable for a long enough period that it is well-represented in cached session history and the agent's general familiarity with "standard" sales-forecasting weights, making the retired scheme the more fluent default
- No automated check compares the weighting figures cited in the forecast narrative against the configuration tool's actual logged response for that run
- RevOps weighting-scheme changes are not flagged as a high-salience event that forces a forecast-pipeline cache invalidation or explicit re-grounding step

---

## Mitigation Strategies

1. **Mandatory Verbatim Config Echo**: Require the agent to quote the forecasting-configuration tool's returned weighting scheme verbatim in its computation narrative before applying any weight, so a mismatch between cited and tool-returned values is mechanically detectable
2. **Config-Result Diffing**: Automatically diff the weighting values used in the agent's final computation against the configuration tool's logged response for that run, rejecting any forecast where they do not match
3. **Weighting-Change Cache Invalidation**: Treat a RevOps stage-weighting update as a forced cache-invalidation event for the forecasting agent, requiring an explicit re-grounding call rather than allowing session or recall-based continuity across the change
4. **Deterministic Weighting Application**: Move the actual probability-weight multiplication out of the LLM's free-form computation and into a deterministic post-processing step that takes the configuration tool's values as direct input, leaving the agent responsible only for narrative explanation, not the arithmetic itself

### Metrics
- Rate of forecast runs where cited weighting figures do not match the configuration tool's logged response for that run
- Time elapsed since the most recent weighting-scheme change versus rate of stale-weight mismatches
- Number of weighted-total corrections issued after a RevOps audit traced back to a stale remembered weighting scheme

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Stale weighting mismatch | Forecast narrative's cited stage-weighting values do not match the configuration tool's logged response for the same run | P1 | Withhold forecast from distribution; recompute using deterministic post-processing against logged config |
| Post-change forecast without re-grounding | A forecast runs within a defined window after a known weighting-scheme change without an explicit re-grounding call to the configuration tool | P2 | Force re-grounding before accepting the forecast |
| Arithmetic drift | Deterministic recomputation of the weighted total from the configuration tool's values differs from the agent-reported total by more than a defined tolerance | P2 | Flag for methodology audit |

---

## References

- [STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?](https://arxiv.org/html/2605.06527v1)
- [When Retrieval Succeeds and Fails: Rethinking Retrieval-Augmented Generation for LLMs](https://arxiv.org/html/2510.09106v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
