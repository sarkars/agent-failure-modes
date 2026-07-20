# Silent Model Update

## Issue
An agent references a model by a floating alias — a name like "latest," a bare model family name without a snapshot suffix, or a provider-managed default endpoint — rather than a pinned, immutable snapshot. The provider swaps the model backing that alias to a new version on its own schedule, with no code change, no deploy, and no action on the team's part. Because nothing in the team's own systems changed, none of their normal change-detection tooling (deploy logs, git history, config diffs) has any record of the update, and behavior drift shows up looking like an unexplained, spontaneous regression rather than the direct consequence of a version change that in fact happened underneath them.

**Frequency**: Common

**Symptoms**
- Agent behavior changes measurably with no corresponding code, prompt, or configuration change in the team's own deploy history
- Debugging the "regression" starts from the assumption that something the team controls must have changed, wasting investigation time before anyone checks whether the model itself moved
- The provider's own changelog or status page shows a model update on the exact date the behavior shift began, but nothing in the team's internal tooling surfaced that correlation automatically
- The same prompt, replayed later, produces different output characteristics (tone, verbosity, refusal rate, formatting) than a saved reference response from weeks earlier, with no other variable changed
- Multiple unrelated teams in the same organization, all using the same floating alias, report similar-looking "mystery regressions" around the same date

## Root Cause
Providers offer floating aliases specifically so that customers automatically receive improvements without needing to take explicit action — a deliberate design trade-off that favors staying current over staying stable. Because the alias resolves to different underlying model weights at different points in time without that resolution being recorded anywhere in the calling application's own version control, there is no local artifact (no commit, no config change, no deploy record) that a team's standard incident-investigation process would find, since that process is built around detecting changes the team itself made. The update is real and has a real cause, but it is invisible to any tooling that only watches the team's own systems rather than the provider's model-serving layer.

## Example
```
A voice-assistant agent calls a provider's chat completion endpoint
using the model string "assistant-chat" — the provider's documented
"always get our current default model" alias, chosen specifically so
the team wouldn't need to manually track version updates.

On a Tuesday, the provider rolls the "assistant-chat" alias over to a
new underlying model version as part of a routine capacity migration,
announced only in a provider status-page post that the team's on-call
process doesn't monitor.

Wednesday morning, an internal QA sweep flags that the assistant has
started responding to ambiguous scheduling requests with a clarifying
question instead of making a best-guess booking, as it reliably did the
week before. The team spends four hours combing through their own git
history, deploy logs, and prompt template changes looking for the
cause, finding nothing, because nothing in their own systems changed.

A engineer only discovers the real cause after independently testing
the same prompts against a colleague's separate project that happens to
pin an explicit snapshot version rather than the floating alias — that
project's behavior is unchanged, isolating the difference to the model
alias itself and confirming the provider silently rolled it over.
```

## Statistics
| Finding | Context |
|---|---|
| Investigations into unexplained agent behavior regressions that turn out to be provider-side model updates commonly consume several hours before the model version is identified as the cause | Estimated from postmortems where root cause was eventually traced to a floating alias |
| A substantial share of production LLM integrations reference a floating or default model alias rather than a pinned snapshot, particularly in early-stage or prototype-derived systems that never revisited the choice | Typical range observed across production LLM integration audits |
| Teams that log the resolved model version/snapshot identifier on every request cut time-to-diagnose for this pattern dramatically compared to teams that only log the alias string | Reported range across teams comparing request-level version logging practices |

## Mitigations
1. **Pin to an explicit, immutable model snapshot in production**: Replace floating aliases with a specific versioned model identifier for any production-critical agent, so a version change requires a deliberate team action rather than happening silently underneath a stable-looking reference.
2. **Log the resolved model version on every request, not just the requested alias**: Capture whatever version identifier the provider's response metadata exposes (even when calling a floating alias), so a behavior shift can be correlated against an actual version change after the fact instead of requiring manual cross-team comparison to isolate.
3. **Subscribe to and route provider status/changelog feeds into on-call tooling**: Ingest the provider's model-update announcements as a monitored input (an alert feed, not just a webpage), so a version rollover is a known, timestamped event in the team's own incident timeline rather than something discovered only through debugging.
4. **Behavioral regression canary on a fixed prompt set**: Continuously replay a small, stable set of reference prompts against the live model reference and diff the outputs against a saved baseline, so a silent version change is flagged by output drift even when no version-identifier metadata is available.
5. **If floating aliases are used deliberately for currency, pair them with staged rollout on the caller's side**: Where automatically receiving updates is genuinely wanted, gate the alias's effect behind an internal feature flag the team controls, so the team can still stage and observe the rollover rather than having it apply to 100% of traffic instantly and invisibly.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| resolved_model_version_change_count | Number of distinct resolved model version identifiers seen in request metadata over a rolling window for a given alias | Alert on any change for production-critical agents |
| reference_prompt_output_drift_score | Similarity score between current outputs and saved baseline outputs for a fixed canary prompt set | Alert if drift exceeds a calibrated threshold |
| unexplained_behavior_change_investigation_time | Time spent investigating a behavior regression before a root cause is identified | Alert/flag if investigation exceeds normal SLA without a matching internal deploy record |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Resolved model version changed under a floating alias | resolved_model_version_change_count increments for a production-pinned-by-policy agent still using a floating alias | High | Confirm the change against provider changelog, run the task-specific eval suite against the new resolved version, pin explicitly going forward |
| Canary output drift detected | reference_prompt_output_drift_score exceeds threshold with no corresponding internal deploy | Medium | Check provider status/changelog feed for a model update coinciding with the drift window |

## Related Patterns
- [Model Version Pinning Expiration](./model-version-pinning-expiration.md) - the inverse failure: pinning avoids this pattern but introduces a deferred expiration risk of its own
- [Model Behavior Change Detection Failure](./model-behavior-change-detection-failure.md) - once a version change (silent or deliberate) has occurred, this sibling pattern covers why evaluation may still fail to catch the resulting regression
- [Model AB Test Interference](./model-ab-test-interference.md) - both describe behavior changes that existing monitoring isn't structured to attribute correctly, one from concurrent experiments and one from an invisible provider-side swap
