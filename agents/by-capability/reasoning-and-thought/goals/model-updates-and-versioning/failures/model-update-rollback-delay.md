# Model Update Rollback Delay

## Issue
After a model version update is confirmed to have caused a production regression, the time between confirming the problem and actually reverting to the prior version is far longer than reverting a normal code deploy would take. Unlike a code rollback (redeploy the previous artifact), reverting a model version can require re-requesting access to a snapshot the provider is already sunsetting, re-running a change-approval process because "swap the model" is treated as a higher-risk action than it should be, or untangling in-flight state (cached responses, multi-turn conversations, fine-tuned adapters) that already assumes the new version. The delay between "we know this is bad" and "we're back on the known-good version" is where most of the damage from a model regression actually accumulates.

**Frequency**: Common

**Symptoms**
- Time-to-rollback for a model version regression is measured in hours to days, while time-to-rollback for a code deploy on the same team is measured in minutes
- The rollback is technically simple (flip a config value or API parameter) but is blocked on an approval chain designed for major changes, not reversions
- The team discovers mid-rollback that the prior model version is no longer available (deprecated, sunset, or removed from the provider's API) and has to find or negotiate an alternative instead of simply reverting
- In-flight multi-turn sessions or cached artifacts created under the new version cause visible inconsistency when some traffic is reverted and some isn't (a conversation partially handled by each version)
- Post-incident review notes that the regression was identified quickly but the fix (revert) sat in a review or deployment queue

## Root Cause
Reverting application code is a well-practiced, low-risk, and usually automated action because it returns the system to a state that was already running in production moments ago. Reverting a model version doesn't have the same guarantees: the "previous" version may be a resource the provider actively deprecates on its own schedule (making rollback impossible rather than merely slow), the update may have been adopted via a floating alias that has no explicit "previous" pin to return to, and many organizations route any model-facing change — including a revert — through the same change-management process used for the original forward change, since the tooling doesn't distinguish "reverting to known-good" from "introducing something new." The result is that the fastest theoretically possible fix (flip back) is gated by the slowest available process (full change approval), and if the prior version has already been deprecated, there may be no fast path at all.
## Example
```
14:02 - New model version is fully rolled out to a document-summarization
        agent after passing standard eval gates.

14:40 - Support tickets begin flagging summaries that omit key financial
        figures the previous version reliably included. On-call engineer
        confirms the regression is version-specific by testing the same
        prompts against the old version's endpoint.

14:55 - Regression confirmed and documented. The fix is understood:
        revert the model version parameter from "v3" back to "v2."

15:00 - Engineer opens a change request to revert, but the deployment
        pipeline requires the same two-approver sign-off for any model
        version change, forward or backward, because the tooling has no
        "emergency revert" path distinct from a normal version change.

16:30 - Approvers are in meetings; the change request sits unactioned.

17:15 - Change is approved and reverted. Total time from confirmed
        regression to resolution: 2 hours 20 minutes, during which the
        agent produced financially-incomplete summaries for every
        document it processed.

17:16 - A second issue surfaces: the provider had begun a scheduled
        deprecation of v2 that same week. The revert works today, but
        the team now realizes their "known good" fallback has a
        30-day expiration they hadn't tracked.
```

## Statistics
| Finding | Context |
|---|---|
| Model version rollbacks routed through standard (non-emergency) change approval take several multiples longer than code rollbacks on the same team | Typical range observed where rollback and forward-change share one approval path |
| A material share of attempted model version rollbacks are complicated or blocked by the prior version already being deprecated by the provider | Estimated from incidents where "revert" required substituting an alternative version rather than a simple pin |
| Teams with a pre-authorized emergency model-rollback path resolve version regressions substantially faster than teams without one | Reported range across teams comparing incident resolution time before/after adding a fast-path revert process |

## Mitigations
1. **Pre-authorized emergency rollback path**: Establish a separate, pre-approved change path specifically for reverting a model version to its immediately-prior known-good state, distinct from the approval chain used for forward changes, so a confirmed regression doesn't wait on a general change-review queue.
2. **Keep the previous version warm and reachable**: Maintain the ability to route traffic to the prior model version (a live endpoint, a retained snapshot reference) for a defined grace period after every cutover, rather than assuming the old version stays available indefinitely or discarding the reference immediately.
3. **Track provider deprecation calendars for the currently-live version's predecessor**: Explicitly monitor when the "rollback target" version is scheduled for sunset, since a rollback plan is only as good as the availability of the version being rolled back to.
4. **Idempotent, version-tagged state handling**: Tag cached responses, session state, and multi-turn context with the model version that produced them, so a rollback doesn't leave in-flight sessions in an inconsistent state straddling two versions.
5. **Rehearse the rollback, not just the rollout**: Include a rollback drill as part of every model version migration plan, so the mechanics (config change, cache invalidation, session handling) are tested before they're needed under incident pressure, not discovered for the first time during one.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| model_rollback_time_to_resolution | Time from confirmed model-version regression to full traffic reverted | Alert if exceeds the team's code-rollback SLA by a defined multiple |
| rollback_target_version_ttl | Time remaining before the provider-scheduled deprecation of the currently-live version's predecessor | Alert when remaining window drops below the team's minimum safe rollback buffer |
| mixed_version_session_rate | Rate of in-flight sessions or cached artifacts spanning two model versions during a rollback | Alert if nonzero during an active rollback |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Rollback exceeds SLA | model_rollback_time_to_resolution running longer than the defined emergency-path target | High | Escalate to bypass standard approval queue, invoke pre-authorized emergency rollback path |
| Rollback target nearing deprecation | rollback_target_version_ttl below safety buffer while it is the only fallback for the currently-live version | Medium | Pin or archive an accessible copy of the fallback version, or identify an alternative before it disappears |

## Related Patterns
- [Model Update Accuracy Regression](./model-update-accuracy-regression.md) - the regression this pattern's delay applies to; the two together span detection-to-resolution
- [Model Behavior Change Detection Failure](./model-behavior-change-detection-failure.md) - a slow detection process compounds directly with a slow rollback process to extend total incident duration
- [Model Version Pinning Expiration](./model-version-pinning-expiration.md) - the same provider-deprecation dynamic that blocks rollback also forces unwanted forward migrations when a pinned version expires
- [Failover Delay Too Long](../../../../../cross-cutting/operations/goals/fault-tolerance/failures/failover-delay-too-long.md) - the general infrastructure pattern of a correct recovery mechanism taking too long to execute, here specialized to model version reverts
