# Stale Tool Confirmation Reused After a Post-Check Revision

## Issue: Agent Treats an Earlier Tool Confirmation as Still Valid After Making a Change the Tool Never Re-Evaluated

An agent calls a verification/compliance tool, receives a "not yet passing" result, makes a corrective change based on its own judgment about what the flagged issue requires, and then proceeds to an autonomous, hard-to-reverse action (publish, submit, execute) without issuing a fresh call to the same tool against the revised content. The agent's own belief that the revision addressed the flagged condition is substituted for the tool's actual, re-verified confirmation. This is distinct from [Action-Completion Claimed Without Status Check](./action-completion-claimed-without-status-check.md): there, the agent never reads a confirmation at all; here, a real confirmation was read once, but a subsequent change silently invalidates it and nothing forces a re-check against the new state.

**Frequency**: Common

**Symptoms**
- Workflow logs show a compliance/verification-tool call returning a failing result, followed by a revision, followed immediately by the autonomous action — with no second tool call between the revision and the action
- The action's output later found to still contain the originally flagged issue, because the revision addressed a related but different part of the flagged content
- Re-running the same tool against the revised content after the fact still returns a failing result, confirming the action proceeded on an unconfirmed and in fact still-failing state
- The agent's own reasoning trace narrates confidence ("this addresses the flagged issue") in place of an actual tool-confirmed pass
- The gap is more frequent on high-volume or late-session runs, where repeated tool calls are treated as redundant overhead rather than a required gate per revision cycle

## Root Cause
A verification/compliance tool's result is a snapshot of one specific version of the content or state at the moment it was called; it says nothing about any version produced after that call. Workflows that treat the tool as a one-time gate earlier in a pipeline, rather than a gate that must be re-passed after every subsequent change, create a window where the agent's own unverified belief that a revision "fixed" the issue is accepted as functionally equivalent to the tool's actual pass/fail determination — with no structural distinction between the two in the control logic. Because repeated tool calls have a real cost (latency, API quota), there is often implicit or explicit pressure to treat the first call as sufficient, especially once the agent has already reasoned its way to confidence that the fix is correct.

## Example
```
A content-generation agent drafts a product-launch blog post and calls
the brand-voice compliance tool before an autonomous-publish step.

The tool returns: "revisions needed -- second-person imperative tone
('Don't miss out!') violates the Q2 brand-voice update banning
urgency-based calls to action."

The agent regenerates the closing paragraph, removing the specific
flagged sentence, and reasons internally that the tone issue is now
resolved. It proceeds directly to the autonomous-publish action
without a second compliance-tool call on the revised draft.

A post-publish audit re-runs the compliance tool on the published text
and finds a different paragraph still contains urgency-based language
("Act now before the offer ends") that the agent's revision never
touched -- the original flagged condition was never actually cleared.
```

## Statistics
| Finding | Context |
|---|---|
| Research on miscalibration in tool-use agents finds that agents relying on their own reasoning about whether a flagged issue is resolved, rather than a fresh deterministic tool check, exhibit systematic overconfidence relative to agents that re-verify | The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents, arXiv:2601.07264 |
| Agent-environment interaction failure research notes agents frequently treat their own corrective action as sufficient to resolve a flagged condition without confirming the environment actually reflects the fix | Aegis: Agent-Environment Failures, arXiv:2508.19504 |
| Workflows with exactly one verification-tool call per output item, regardless of revision count, are a direct signal that the recheck-after-change rule is not being enforced | Consolidated from prior domain-specific documentation of this pattern |

## Mitigations
1. **Hard Gate on Fresh Tool Confirmation**: Make the autonomous action's preconditions require a tool "pass" result called against the exact content hash about to be acted on, not against an earlier version or the agent's own narrated belief.
2. **Revision-Triggers-Recheck Rule**: Any change to the content or state after a verification-tool call — however small — automatically invalidates the prior result and requires a new call before the action is permitted.
3. **Separate the Reviser From the Actor**: Structure the workflow so the agent that revises content cannot itself authorize the downstream action; a separate gate (automated or human) must observe an actual fresh "pass" result before the action executes.
4. **Post-Action Compliance Audit**: Run the verification tool again on a sample of already-actioned content on a fixed schedule to catch cases where the pre-action gate was bypassed or produced a false pass.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| stale_confirmation_at_action_rate | Share of actions where the most recent tool-confirmation call predates the most recent content revision | > 0% |
| post_action_audit_failure_rate | Rate of post-action audit failures versus pre-action gate pass rate; a gap indicates gate bypass or false-pass behavior | Any sustained gap |
| checks_per_action_item | Number of verification-tool calls per actioned item; a flat 1-per-item rate regardless of revision count indicates the recheck rule isn't enforced | Consistently 1, with revision count > 1 |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Stale confirmation at action | Action fires with a tool-confirmation result timestamp older than the most recent content revision | P1 | Block the action; force a fresh tool call on the current version |
| Post-action audit failure | Scheduled re-check of actioned content returns a failing result | P1 | Reverse/flag the action for immediate correction; investigate gate bypass |
| Recheck-skip rate rising | Percentage of actions with exactly one tool call (versus one per revision cycle) exceeds a defined threshold | P2 | Review the workflow for hard-gate enforcement |

## Related Patterns
- [Action-Completion Claimed Without Status Check](./action-completion-claimed-without-status-check.md) - a related but distinct failure where no confirmation is ever read at all, as opposed to this pattern's case of a real confirmation being read once and then reused past its validity
- [Silent Tool Failures](./silent-failures.md) - a related but distinct failure where the tool itself misreports its outcome, rather than the agent reusing a stale-but-accurate prior result
