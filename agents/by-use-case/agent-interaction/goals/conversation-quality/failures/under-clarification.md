# Under-Clarification

## Issue
The agent proceeds directly on a request that is genuinely ambiguous — multiple plausible interpretations with materially different outcomes — without asking anything, and produces output built on whichever interpretation it silently picked. Unlike assumption-validation-failure, which is about one unstated parameter inside an otherwise clear request, under-clarification is about the core intent of the request itself being unresolved; the agent guesses at what was actually being asked for, not just a detail of how to do it.

**Frequency**: Common

**Symptoms**
- Output fully addresses one plausible interpretation of the request while ignoring that other, equally plausible interpretations existed
- User's correction indicates the request meant something the agent never considered at all, not just a detail it got wrong
- No question was asked despite the request containing genuinely conflicting or underspecified signals
- The interpretation chosen happens to be the easier one to execute rather than the more likely one
- Rework requires restarting from scratch rather than adjusting a detail, because the whole premise was wrong

## Root Cause
A model under pressure to be immediately helpful treats producing *some* complete answer as inherently better than pausing, and when multiple interpretations are plausible, it will pick one (often the statistically most common phrasing-to-intent mapping in its training distribution) and commit to it fully rather than surfacing the fork. This is exacerbated when the interface or evaluation rewards fast, confident single-shot answers over interaction, so there's no structural incentive for the model to recognize "this request has two genuinely different meanings" as a distinct case requiring different handling than "this request is clear."

## Example
```
User: "Can you archive the Q1 project?"

Two genuinely different, both-plausible readings exist in this
workspace: "Q1 project" could mean the project literally named
"Q1 Planning," or it could mean whichever project was the active one
during Q1 (which is a different project, named "Website Relaunch,"
that ran January-March).

Agent picks the literal name match without flagging the alternative,
and archives "Q1 Planning" — a project that, unlike "Website Relaunch,"
still has two open tasks and a teammate actively working in it.

User: "Wait, that's the wrong project — I meant the one we were
running during Q1, not the one literally named Q1. And why did you
archive something with open tasks without checking?"

The ambiguity (name-match vs. time-period-match) was resolvable with
one short question before acting, but the agent went straight to
execution on an interpretation it never surfaced as a choice.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of agent actions on requests with genuine multi-way ambiguity are executed against the wrong interpretation | Typical range across task-execution agent deployments |
| Under-clarified requests involving an irreversible or hard-to-reverse action (archive, delete, send) show disproportionately higher-cost corrections than reversible ones | Estimated from production incident review |
| Requiring explicit interpretation-count checking before action reduces wrong-interpretation executions substantially | Reported range across teams that added pre-action ambiguity detection |

## Mitigations
1. **Pre-action interpretation check**: Before executing (especially hard-to-reverse actions), explicitly enumerate whether more than one materially different interpretation of the request exists; if so, ask before proceeding.
2. **Reversibility-gated confirmation**: Require confirmation specifically when the action is destructive or hard to undo and genuine ambiguity is present, even if the agent would otherwise default to acting.
3. **Interpretation divergence scoring**: Distinguish ambiguity that doesn't change the outcome much (safe to guess) from ambiguity where interpretations diverge sharply in effect (unsafe to guess), and gate on the latter.
4. **Post-hoc interpretation disclosure**: When the agent does proceed without asking, state which interpretation it used so the user can catch a wrong guess immediately rather than discovering it later.
5. **Under-clarification incident review**: Track cases where a wrong-interpretation correction occurred and had a real cost (redone work, undone actions), and use them to tighten the reversibility-gated confirmation rules.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| wrong_interpretation_rate | Share of ambiguous requests executed against the interpretation the user didn't mean | Alert if > 15% |
| irreversible_action_under_ambiguity_rate | Rate of destructive/hard-to-reverse actions executed without confirmation despite detected multi-way ambiguity | Alert if > 0% |
| interpretation_disclosure_rate | Share of ambiguous requests where the chosen interpretation was explicitly stated to the user | Alert if < 70% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Irreversible action taken under unresolved ambiguity | A destructive action executes despite detected multiple plausible interpretations | High | Halt further destructive actions on ambiguous requests, require confirmation, audit recent actions |
| Rising wrong-interpretation corrections | wrong_interpretation_rate trends upward for a request category | Medium | Review ambiguity-detection coverage for that category |

## Related Patterns
- [Assumption Validation Failure](./assumption-validation-failure.md) - narrower version limited to a single unstated parameter rather than the core intent of the request
- [Over-Clarification](./over-clarification.md) - the opposite miscalibration, asking when the request was actually clear
- [Disambiguation Strategy Ineffective](./disambiguation-strategy-ineffective.md) - under-clarification is the specific failure mode where the chosen strategy is "guess silently" and that choice was wrong for the ambiguity's stakes
