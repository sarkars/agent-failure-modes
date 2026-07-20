# Version Rollout Coordination

## Issue
A new version rolling out touches multiple independently-deployed components that must move together for the system to keep working — an agent orchestrator and its tool-adapter plugins, a client SDK and the server API it calls, a message producer and consumer sharing a schema — but each component is deployed on its own pipeline, timeline, and approval process. When one component's rollout gets ahead of or behind the others (deployed early because its pipeline is faster, delayed because of an unrelated approval holdup, rolled back independently after its own issue), the system spends time running an untested combination of versions that were only ever validated to work together as a matched set, producing failures that have nothing to do with a bug in any single component and everything to do with the combination being new.

**Frequency**: Common

**Symptoms**
- Errors appear at the interface between two components immediately after one of them deploys, referencing a contract (message schema, API shape, protocol version) that changed in the version being rolled out but that the other component hasn't been updated to match yet
- Rollout tracking shows components A and B, which are supposed to move together for a given release, at different versions for a period of time with no coordination gate preventing that gap
- One component's independent rollback (triggered by an issue specific to that component) leaves it paired with a newer version of a sibling component it was never tested against
- Incident review finds that each component's change, in isolation, passed its own tests and was individually correct — the failure only manifests in the specific cross-version combination that occurred during the uncoordinated rollout window
- Rollout runbooks or checklists don't reference the other components that need to move in lockstep, because each component's deployment process was built independently

## Root Cause
Independently deployed components are, by construction, independently deployable — each has its own pipeline, its own approval gates, its own rollback mechanism — and nothing about that independence inherently enforces that two components whose compatibility was validated only as a matched pair actually deploy as a matched pair. Compatibility testing for a release typically validates "new version of A works with new version of B," but once each component's deployment is executed by a separate pipeline with its own timing, there's no structural guarantee that the moment between A's deployment and B's deployment doesn't leave the system running old-A/new-B or new-A/old-B, a combination that was never actually tested because it was never intended to exist, even momentarily. This gets worse under partial failure: if only one component in a coordinated release needs to be rolled back due to an issue specific to it, doing so independently reintroduces an untested cross-version combination just as surely as an uncoordinated forward rollout would.

## Example
```
An agent platform ships a coordinated release: a new orchestrator
version (v14) that sends tool-call requests in a new message format,
paired with a corresponding tool-adapter version (v9) that expects
that new format. The two are deployed via separate CI/CD pipelines -
orchestrator deploys are gated by a manual approval from the platform
team, tool-adapter deploys auto-promote after passing integration
tests.

The tool-adapter's automated pipeline finishes and auto-promotes v9
to production two hours before the orchestrator's manual approval is
granted, because the approver was in a different timezone and hadn't
seen the request yet. For those two hours, the still-running
orchestrator v13 sends tool-call requests in the old message format
to a tool-adapter v9 that only expects the new format.

Tool calls fail silently during the gap - v9 doesn't recognize the
old-format field names and returns default/empty values rather than
an error, because it was never tested against v13's request shape.
Agent tasks relying on tool results during that window complete with
silently wrong (empty) tool outputs, and the issue isn't caught until
a user reports an agent that "did nothing" despite claiming success -
by which point the orchestrator has since caught up to v14 and the
mismatched window has already passed, making the failure hard to
reproduce.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of multi-component rollout incidents trace back to components moving out of sync during deployment, rather than a defect in any single component's code | Estimated from postmortem review of coordinated-release incidents |
| Coordinated releases lacking an explicit cross-component deployment gate show measurably more version-mismatch incidents than releases using a single orchestrated deployment step for all paired components | Typical range observed comparing gated vs. ungated coordinated rollouts |
| Version-mismatch windows during coordinated rollouts are typically short (minutes to a few hours) but incidents occurring within them are disproportionately hard to reproduce after the fact, since the mismatched state no longer exists once both components catch up | Typical pattern reported in postmortems of transient cross-version incidents |

## Mitigations
1. **Single orchestrated deployment gate for paired components**: For components whose compatibility was validated only as a matched version pair, deploy them through one coordinated pipeline step (or an explicit cross-component approval gate) rather than letting each component's independent pipeline determine timing.
2. **Backward/forward-compatible transition windows by design**: Where lockstep deployment isn't feasible, design the changed contract (message format, API shape) to tolerate at least one version of skew in either direction, so a temporary mismatch degrades gracefully rather than silently producing wrong results.
3. **Explicit compatibility-gap monitoring during rollout**: Track the live version of each component in a coordinated release pair and alert immediately if they diverge beyond the tested-compatible window, rather than only discovering the mismatch via downstream error symptoms.
4. **Coordinated rollback, not independent rollback**: When one component in a matched pair needs to roll back, treat that as triggering a rollback evaluation for its paired components too, rather than rolling back the one component in isolation and reintroducing an untested combination.
5. **Fail loud on unrecognized contract version, not silent default**: Have each component reject or error on a request/message it doesn't recognize the format of, rather than falling back to default/empty values, so a version-mismatch window produces visible failures instead of silently wrong results.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| paired_component_version_skew | Difference between the live versions of components that are supposed to deploy in lockstep | Alert if skew exceeds the tested-compatible window for any coordinated pair |
| cross_version_error_rate | Error or default-fallback rate specifically at the interface between two components during an active coordinated rollout | Alert on any increase during a rollout window |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Coordinated components deployed out of sync | paired_component_version_skew exceeds the validated-compatible range | High | Pause further rollout, accelerate the lagging component's deployment or roll back the leading one |
| Silent contract mismatch detected | A component logs an unrecognized message/request format consistent with a version-skew window | High | Investigate immediately; treat any silent-default fallback found as a data-integrity risk requiring backfill assessment |

## Related Patterns
- [Deployment Ordering Violation](./deployment-ordering-violation.md) - closely related: that pattern covers ordering violations within a single deployment pipeline's steps, while this pattern covers coordination gaps across separately-piped components
- [Deployment Dependency Deadlock](./deployment-dependency-deadlock.md) - a related coordination failure where components waiting on each other block progress entirely, as opposed to this pattern's silent, ungated cross-version window
- [Handoff Protocol Version Mismatch](../../agent-handoffs-delegation/failures/handoff-protocol-version-mismatch.md) - a related but narrower pattern focused on version mismatch specifically during an agent-to-agent handoff, rather than general component rollout coordination
