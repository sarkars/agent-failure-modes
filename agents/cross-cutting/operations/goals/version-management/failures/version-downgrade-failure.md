# Version Downgrade Failure

## Issue
An operator (or an automated rollback script) attempts to revert a specific dependency, library, runtime, or container base image to an older version — commonly to work around a regression introduced by a recent upgrade — and the downgrade operation itself fails to produce a working system. This happens in one of two ways: the target older version is no longer actually installable (it's been yanked from the package registry, the container tag was deleted or overwritten, the release was pulled for a security issue), or the downgrade installs cleanly at the artifact level but the surrounding application code, configuration, or transitively-pinned peer dependencies have already drifted forward to depend on APIs, config keys, or behavior that only exist in the newer version — so the "successfully downgraded" component is now missing something the rest of the system requires.

**Frequency**: Occasional

**Symptoms**
- A downgrade command (`pip install package==old_version`, `docker pull image:old_tag`) fails outright because the specified version is no longer resolvable in the registry
- A downgrade installs without error, but the application immediately throws `AttributeError`/`ImportError`/"unknown config key" errors referencing something only present in the newer version the code was written against
- A downgrade fixes the original regression but reintroduces a different, previously-fixed bug that the newer version's changelog shows was resolved after the target downgrade version
- Downgrading one component succeeds, but a different, already-upgraded peer dependency now declares a minimum-version floor that conflicts with the just-downgraded component, breaking dependency resolution for the whole install
- Post-downgrade smoke tests fail on functionality unrelated to the original regression, because the downgrade silently removed capabilities the rest of the system had already come to depend on

## Root Cause
Downgrading is implicitly assumed to be the inverse of upgrading — install the old artifact and the system returns to its prior working state — but this assumption only holds if nothing else in the system changed while the newer version was active. In practice, application code, configuration, and other dependencies often continue evolving forward during the time a component was on the newer version (a developer starts using a new API the upgrade unlocked, another dependency bumps its own minimum-version requirement to match), so by the time a downgrade is attempted, the rest of the system is no longer compatible with the older target. Separately, package registries and container registries are not guaranteed to retain every historical version indefinitely — versions can be yanked for security reasons, licensing issues, or storage cleanup — so the specific older version an operator wants to revert to may simply no longer be available to install, a failure mode invisible until the downgrade is actually attempted during an incident.

## Example
```
A team upgrades their PDF-parsing library from v3 to v4 to pick up a
performance improvement. Two weeks later, v4 is found to mis-handle a
class of scanned documents, corrupting extracted text for a subset of
agent workflows. The on-call engineer decides to downgrade back to v3
as an emergency mitigation.

In the two weeks since the v4 upgrade, another developer refactored
the document-ingestion code to use a v4-only streaming API that
doesn't exist in v3, unrelated to the original performance work. The
downgrade to v3 installs cleanly, but the ingestion service now
throws AttributeError on every request, because the streaming method
the refactored code calls was never part of v3's interface.

The emergency mitigation makes the outage worse, not better: instead
of a subset of scanned documents being mis-handled, ingestion is now
completely broken. The team has to forward-fix the v4 mis-handling
bug directly rather than downgrade, since the downgrade path was no
longer actually viable once the surrounding code had moved forward.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of emergency downgrade attempts during incidents fail or make the incident worse, rather than cleanly reverting to the prior working state | Estimated from incident postmortems involving attempted dependency rollbacks |
| Downgrade failures caused by forward-drifted application code (rather than registry/artifact unavailability) are more common the longer the newer version has been live before the downgrade is attempted | Typical pattern observed correlating time-since-upgrade with downgrade failure rate |
| Teams that validate a downgrade path (via a rollback rehearsal or a pinned "last known good" artifact retained independently of the registry) report a substantially lower downgrade failure rate during real incidents | Typical range reported by teams practicing rollback drills versus those relying on ad hoc registry lookups |

## Mitigations
1. **Retain a verified last-known-good artifact independent of the registry**: Don't rely on the package/container registry still holding the exact prior version at incident time; mirror or cache a verified working artifact internally so a downgrade target is guaranteed available.
2. **Track forward-only code dependencies on new-version features**: When adopting an API or config option introduced by a recent upgrade, flag it so a later downgrade attempt can identify exactly which code paths would break, rather than discovering it via a production stack trace.
3. **Rehearse downgrades, not just upgrades**: Periodically test that reverting to the previous pinned version actually works end-to-end (not just that the artifact installs), since a downgrade path that hasn't been exercised is not a validated rollback path.
4. **Prefer forward-fix over downgrade once code has drifted**: When a downgrade is found to conflict with code that has already moved forward, default to a targeted forward fix or feature flag disabling the specific regression, rather than a downgrade likely to introduce a worse incompatibility.
5. **Pin peer dependencies together during downgrade planning**: Before executing a downgrade, check whether other components have bumped their minimum-version requirements against the component being downgraded, and downgrade the full compatible set together rather than one component in isolation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| downgrade_attempt_failure_rate | Share of attempted version downgrades (dependency, image tag, runtime) that fail to install or fail post-install smoke tests | Investigate any occurrence during an active incident |
| forward_only_api_usage_count | Count of code paths using an API/config option introduced only in the currently active (non-baseline) version | Track growth over time; rising count signals increasing downgrade risk |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Downgrade target unavailable | A rollback attempt fails because the target version is not resolvable in the registry | Critical | Fall back to last-known-good mirrored artifact or pivot to forward-fix |
| Post-downgrade smoke test failure | Smoke tests fail after a downgrade completes installation successfully | Critical | Halt further rollout of the downgrade, assess forward-code compatibility, consider forward-fix instead |

## Related Patterns
- [Rollback Data Consistency](./rollback-data-consistency.md) - a related but distinct rollback failure focused on data written by the newer version being incompatible with the reverted code's schema expectations, rather than the downgrade artifact/install itself failing
- [Rollback Partial Failure](./rollback-partial-failure.md) - a related but distinct failure at the fleet-orchestration level, where the rollback stalls partway across instances, rather than the downgrade target itself being broken or unavailable
- [Version Lock File Staleness](./version-lock-file-staleness.md) - a related dependency-management pattern; a stale lockfile can mask exactly which version was previously working, complicating identification of a valid downgrade target
- [Model Downgrade Silent Failure](../../../../../by-capability/reasoning-and-thought/goals/model-selection-and-routing/failures/model-downgrade-silent-failure.md) - a related but distinct pattern in a different domain, about a model-routing downgrade being invisible to quality monitoring rather than the downgrade operation itself failing to execute
