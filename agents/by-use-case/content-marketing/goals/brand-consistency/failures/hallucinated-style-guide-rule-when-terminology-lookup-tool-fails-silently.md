# Hallucinated Style-Guide Rule When Terminology Lookup Tool Fails Silently

## Issue: A Content-Generation Agent's Call to the Brand-Terminology Lookup Tool Fails or Returns a Stale Cached Fragment, and Instead of Flagging the Failed Lookup, the Agent Fabricates a Plausible-Sounding Terminology Rule Consistent With General Brand-Voice Patterns It Has Seen Elsewhere, Publishing Content With Incorrect Product Terminology

**Frequency**: Occasional

**Symptoms**
- Published content uses a deprecated product name or an internally retired feature term, even though the brand style guide was updated months ago to require the current terminology
- The content-generation agent's terminology-lookup tool call returned an error or a stale cached fragment, but the agent's output presents a confident, specific terminology rule as though it were freshly retrieved from the current style guide
- Asking the agent to cite its source for the terminology choice either produces no citation or cites a general impression of "how the brand usually refers to this," rather than the actual current style-guide entry
- The miss concentrates on terminology that changed recently, since the agent's fabricated rule is plausible precisely because it matches how the brand referred to the product before the change
- Re-running the same terminology lookup once the tool call succeeds returns the current, correct rule, which differs from what the agent published

**Root Cause**
When the terminology-lookup tool call fails or returns a stale fragment, the content-generation agent does not have a hard stop requiring it to flag the lookup as unavailable; instead, it falls back to generating a plausible terminology choice consistent with brand-voice patterns it has internalized, which reflects how the brand referred to the product before the most recent change. Because the fabricated rule is fluent and stylistically consistent with genuine brand voice, it is indistinguishable in tone from output that actually consulted the current, correct style-guide entry.

**Example**
```
Brand style guide was updated two months ago to retire the term "SmartSync" in favor of the current product name "AutoConnect"
Content-generation agent calls the terminology-lookup tool while drafting a blog post; the tool call returns a cached fragment from before the update, due to a cache-invalidation gap
Agent's draft confidently uses "SmartSync" throughout the post, consistent with the stale cached fragment and with general brand-voice patterns from before the rename
Editor approves the post without independently checking every terminology instance against the current style guide
Published content uses a retired product name for an extended period before a customer comment flags the inconsistency
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use agents frequently fail to distinguish a tool call that returned an error or stale cached result from one that returned current data, producing confident downstream output from outdated information | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Surveys of LLM agent hallucination identify fabrication of plausible values consistent with prior patterns, in place of flagging a failed or incomplete tool call, as a distinct and recurring failure category | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Audits of agentic workflow failures in production platforms identify silent tool-call failures and stale cache reads as a recurring root cause of downstream content and decision errors | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The terminology-lookup tool's caching layer does not reliably invalidate on style-guide updates, producing stale fragments that are structurally indistinguishable from current data
- No hard rule requires the content-generation agent to treat a failed or stale terminology lookup as a blocking condition rather than falling back to internalized brand-voice patterns
- Recently changed terminology is not flagged for a stricter verification check, even though it is exactly the case where a fabricated rule based on prior patterns will be wrong

---

## Mitigation Strategies

1. **Hard Stop on Failed or Stale Lookup**: Require the content-generation agent to treat a failed terminology-lookup tool call, or one flagged as serving a stale cache, as blocking, refusing to generate terminology-dependent content until a fresh lookup succeeds
2. **Cache-Invalidation on Style-Guide Update**: Ensure the terminology-lookup tool's cache is invalidated immediately on any style-guide update, rather than relying on a time-based expiry that can leave a stale fragment servable for an extended window
3. **Recently Changed Terminology Flagging**: Maintain a list of recently changed terminology and route any content draft referencing those terms through a stricter independent verification step before publishing
4. **Post-Publish Terminology Audit**: Run a periodic automated scan of published content against the current style guide to catch terminology drift that was not caught before publishing

### Metrics
- Rate of published content found, on audit, to use deprecated or retired terminology that was current at some point but has since changed
- Rate of terminology-lookup tool calls returning a stale cached fragment, by time since the most recent style-guide update
- Average time between a style-guide terminology change and full propagation of the change across newly generated content

### Alerts
- Published content is found to use a terminology term that was retired by the style guide more than the defined grace period ago → P2
- A terminology-lookup tool call fails or returns a flagged-stale result during content generation and the draft proceeds without a hard stop → P1
- Stale-cache rate for the terminology-lookup tool exceeds the defined threshold for a rolling window → P3

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
