# Knowledge Temporal Context Lost

## Issue
A source document explicitly scopes a fact with "as of" framing — "as of Q3 2025," "current as of the last policy revision," "prices shown are for the current promotional period" — but that framing is stripped during retrieval, summarization, or generation, leaving the agent's stated fact presented as timeless and universally current rather than tied to the specific moment the source actually anchored it to. The number or claim itself is preserved correctly; only the temporal anchor that made it interpretable is lost.

**Frequency**: Common

**Symptoms**
- Source explicitly includes "as of [date]" or equivalent framing; agent output states the same fact with no date reference at all
- The fact is presented in present tense as though permanently true, when the source tied it to a specific, possibly past, point in time
- Users have no way to judge how current the information is, since the temporal anchor that would let them judge it was removed
- Follow-up questions like "is this still accurate" cannot be answered by the agent, since it no longer has (or never surfaced) the anchor date

## Root Cause
"As of" framing is a modifier attached to a fact, and modifiers are exactly the kind of secondary detail that summarization and compression tend to drop when condensing a passage to its core claim — the headline number survives, the temporal scaffolding around it doesn't, because the scaffolding isn't the "answer" to a typical query even though it's essential to correctly interpreting the answer. This is compounded by generation's default tendency toward present-tense, timeless-sounding phrasing, which is more fluent and more typical of confident answers than explicitly time-stamped phrasing, so even when a date is present in the retrieved context, the generation step has a systematic pull toward dropping it in favor of a cleaner-sounding, undated statement.

## Example
```
A source document states: "As of the March 2025 board meeting, the
company's official remote work policy allows up to 2 days per week,
pending a scheduled review in Q1 2026."

An internal assistant, asked about the remote work policy nine months
later, responds: "The company's remote work policy allows up to 2 days
per week" — dropping both the "as of March 2025" anchor and the
explicit note that the policy was scheduled for review in Q1 2026,
which by the time of the question may have already occurred.

An employee relying on the answer has no way to know the information
might be nine months old and potentially superseded by a review that
was explicitly flagged as scheduled in the source, since the agent's
phrasing gives no indication the fact was ever time-anchored at all.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 30-45% of summarized responses drop an explicit "as of [date]" anchor present in the source, defaulting to timeless present-tense phrasing | Estimated from temporal-framing preservation audits of summarization pipelines |
| Responses that retain the source's temporal anchor show markedly higher user ability to correctly judge information currency in usability testing | Typical pattern observed in comparative response-framing studies |
| Explicit prompting/verification requiring preservation of "as of" language recovers most of the dropped temporal anchors in tested pipelines | Reported range across teams that added temporal-anchor preservation checks |

## Mitigations
1. **Mandatory temporal-anchor preservation**: Require the generation step to preserve and surface any explicit "as of" or date-anchoring language present in retrieved source content, rather than defaulting to timeless present-tense phrasing.
2. **Automated anchor-stripping detection**: Run a check comparing whether temporal-anchor phrases present in the source survive into the generated response, flagging responses where they were dropped for review or regeneration.
3. **Default date-stamping for time-sensitive categories**: For content categories known to be time-sensitive (policy, pricing, staffing, regulatory limits), require every response citing them to include an explicit date reference regardless of whether the model would otherwise include one.
4. **Scheduled-review flagging**: When source content mentions a scheduled future review or expiration ("pending review in Q1 2026"), surface this explicitly in responses issued after that date has passed, prompting the user to verify currency rather than silently treating the content as still valid.
5. **User-facing "as of" display**: Where feasible, display the source's last-verified or as-of date directly alongside the answer in the interface, independent of whether the generated text itself includes it, as a structural safeguard against generation-level stripping.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|------------------|
| temporal_anchor_retention_rate | Share of responses citing source content with an explicit "as of" anchor that preserve that anchor in the output | Alert if < 85% |
| undated_time_sensitive_response_rate | Share of responses about time-sensitive content categories (pricing, policy, staffing) issued with no date reference at all | Alert if > 15% |
| stale_anchor_correction_rate | Rate of expert/user corrections noting the response gave no indication of how current the information was | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Temporal anchor dropped in time-sensitive response | Review confirms an "as of" anchor present in source was absent from a pricing/policy/regulatory response | Medium | Correct the response, add case to anchor-preservation test set |
| Anchor retention rate drop | temporal_anchor_retention_rate falls below threshold after a summarization pipeline change | Medium | Review recent generation prompt/pipeline changes for anchor-stripping regressions |

## Related Patterns
- [Fact Timestamp Error](./fact-timestamp-error.md) - closely related; this pattern is the generation-time stripping of temporal framing, that one is the retrieval-time misapplication of a fact outside its valid window
- [Fact Context Loss](./fact-context-loss.md) - the general "qualifier dropped" mechanism, of which temporal-anchor loss is a specific, common instance
- [Knowledge Update Lag](./knowledge-update-lag.md) - related in that both concern currency, one about the index lagging the source and one about currency framing being stripped even when the source itself is current
