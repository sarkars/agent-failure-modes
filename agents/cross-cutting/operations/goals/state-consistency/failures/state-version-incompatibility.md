# State Version Incompatibility

## Issue
State written to persistent storage by one version of an agent's code is later read by a different version — typically an older reader encountering a newer schema, or a rolled-forward deployment encountering state written before a schema change — and the reader either crashes, silently drops fields it doesn't recognize, or misinterprets a field whose meaning changed between versions. This is especially common during rolling deployments, where old and new code versions run simultaneously against the same shared state store.

**Frequency**: Occasional

**Symptoms**
- Deserialization errors or unexpected-field warnings that correlate exactly with a deployment window, then stop appearing once the rollout completes
- A subset of records processed correctly while others (written by a different code version) fail or produce different behavior
- A field that changed meaning or type between versions (e.g. `priority` going from an integer 1-5 to an enum) is silently misread as the old type by not-yet-upgraded readers
- Rollbacks after a bad deploy leave the old code unable to read state the new code already wrote
- Data quality issues that only appear in records with a timestamp inside a specific deploy window

## Root Cause
Rolling deployments and multi-service agent architectures mean that, for some window of time, more than one version of the code that reads and writes a given piece of state is active simultaneously — and unless the schema is explicitly versioned and every reader/writer is written to handle both old and new versions during that window, one side will encounter data it wasn't built to understand. Because most serialization formats don't enforce forward/backward compatibility by default (adding a required field, renaming a field, or changing a field's type are all backward-incompatible changes that pass code review if the reviewer doesn't specifically reason about in-flight old readers), the incompatibility is invisible until the two versions actually coexist in production, which is often only during the deploy window itself — making it hard to catch in a single-version test environment.

## Example
```
An agent's task-checkpoint schema is updated in v2.14 to change the
"retry_count" field from an integer to an object:
  v2.13: {"retry_count": 3}
  v2.14: {"retry_count": {"attempts": 3, "last_error": "timeout"}}

The team does a standard rolling deployment: 30% of instances upgrade
to v2.14 first, the remaining 70% stay on v2.13 for the next 20
minutes while health checks pass.

During those 20 minutes, a v2.14 instance writes a checkpoint for
task #5502 with the new object-shaped retry_count. A still-running
v2.13 instance picks up task #5502 for a scheduled retry, reads the
checkpoint, and attempts to treat retry_count as an integer for a
comparison (`retry_count >= max_retries`). The comparison throws a
type error because retry_count is now a dict.

The v2.13 instance's task-processing loop crashes on this exception
and doesn't restart the loop (no retry-safe wrapper around the
comparison), silently stopping task processing for that instance
until the rolling deploy finishes and all instances are on v2.14 -
a 20-minute window where roughly a third of scheduled retries were
never attempted.
```

## Statistics
| Finding | Context |
|---------|---------|
| 15-30% of rolling-deployment incidents in stateful agent services trace back to schema changes that weren't backward/forward compatible | Typical range observed in production deployment postmortems |
| Deploy-window-correlated error spikes account for a large share of "intermittent, unreproducible" bug reports later found to be version-skew issues | Estimated from incident triage across teams running rolling deployments |
| Enforcing additive-only schema changes (new optional fields, no type changes or removals) eliminates the large majority of version-incompatibility incidents | Reported range across teams that adopted a formal compatibility policy |

## Mitigations
1. **Explicit schema versioning with dual-read support**: Tag every persisted state record with a schema version, and write readers to handle at least the current and immediately-prior version during any period where both may coexist.
2. **Additive-only, backward-compatible changes**: Restrict schema changes to adding new optional fields; avoid renaming, retyping, or removing fields in a single change, instead deprecating old fields over a full release cycle before removal.
3. **Expand-contract migration pattern**: For genuinely breaking changes, split the migration into an "expand" phase (write both old and new shapes, read either) fully deployed everywhere, followed by a separate "contract" phase (stop writing the old shape) only after the expand phase has fully rolled out.
4. **Version-skew-aware deployment gating**: Slow or gate rolling deployments for services with shared mutable state so the mixed-version window is minimized, and monitor error rates specifically during that window rather than only after rollout completes.
5. **Defensive deserialization**: Write readers to tolerate unknown fields (ignore rather than error) and to explicitly validate expected types before using a field, converting a hard crash into a graceful degraded-handling path with a logged warning.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| schema_version_mismatch_error_rate | Rate of deserialization or type errors tagged as version-related | Alert if > 0 during a deploy window |
| deploy_window_error_spike | Comparative error rate during an active rolling deployment versus steady state | Alert if > 3x baseline |
| unknown_field_encounter_rate | Rate at which readers encounter fields not present in their known schema | Alert if trending upward outside a planned migration |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Version-skew crash during deploy | A reader crashes on state written by a newer/older code version during an active rollout | High | Pause the rollout, roll back if necessary, patch the reader for backward compatibility before resuming |
| Sustained unknown-field rate | unknown_field_encounter_rate stays elevated after a deploy window should have closed | Medium | Check for stuck instances still running old code, verify rollout actually completed |

## Related Patterns
- [State Serialization Failure](./state-serialization-failure.md) - a related but distinct failure where the serialization mechanism itself breaks, rather than two valid but incompatible schema versions colliding
- [State Encoding Mismatch](./state-encoding-mismatch.md) - both are boundary failures where writer and reader assumptions diverge, one on encoding and one on schema
- [State Garbage Collection Failure](./state-garbage-collection-failure.md) - a schema change can be exactly what causes a collector on an older or newer version to silently stop processing records it can't deserialize
