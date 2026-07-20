# Version Skipping Unsupported

## Issue
A system upgrades a component directly from an old version to a much newer one — skipping several intermediate major versions in one jump, often because the intermediate upgrades were deferred for a long time — and the vendor or maintainer only officially supports sequential, one-major-at-a-time upgrade paths (or specific documented multi-version jumps), not the arbitrary skip actually being attempted. The upgrade proceeds anyway, because nothing enforces the supported-path requirement at execution time, and it fails partway through, corrupts state that assumed intermediate migration steps had run, or "succeeds" while leaving the system in an undefined state the vendor never tested or committed to supporting.

**Frequency**: Occasional

**Symptoms**
- An upgrade or migration script fails referencing a migration step, schema version, or compatibility check that assumes an intermediate version was passed through, which was skipped
- Vendor documentation or release notes explicitly state "upgrade path from version N to N+3 is not supported; upgrade sequentially through each major version," and that guidance wasn't followed
- Data or configuration migrations meant to run once per major-version boundary are skipped entirely for the versions jumped over, leaving the system in a state no single version's migration logic was designed to produce
- Support requests to the vendor for an issue following a large version jump get a response that the specific upgrade path taken isn't a supported configuration and troubleshooting can't proceed until a supported path is followed
- Feature flags, config formats, or API contracts that changed incrementally across the skipped intermediate versions are only partially updated, since the upgrade logic that would have handled each individual transition never ran

## Root Cause
Vendors and maintainers commonly design and test upgrade logic (schema migrations, config transformations, deprecation handling) as a sequence of one-version-at-a-time transitions, each of which assumes the system arriving at that step is in the state the previous version's transition left it in — this is both easier to test exhaustively and matches how most users upgrade incrementally. When a system instead jumps directly from version N to version N+4, none of the intermediate transition logic runs, so any state transformation, deprecation cleanup, or compatibility shim that was supposed to happen at each intermediate boundary simply doesn't happen, and the final state doesn't match what any of the tested upgrade paths (N→N+1, N+1→N+2, etc., or an explicitly-supported N→N+4 fast path if one exists) actually produce. The failure often doesn't surface immediately at the jump itself — the upgrade may complete without error — because "did the upgrade script run" and "did it produce a state equivalent to having gone through each intermediate step" are different questions, and only the first one is typically checked.

## Example
```
A team has deferred upgrading their workflow-orchestration platform
for two years, remaining on major version 6 while the vendor has
since released versions 7, 8, and 9. Version 9 includes a new
required field in the task-definition schema that versions 7 and 8's
upgrade scripts were responsible for backfilling from a deprecated
field present in version 6.

The team runs the vendor's version-9 installer directly against their
version-6 deployment, skipping 7 and 8 entirely. The installer
completes without error - it only checks that the currently-installed
version is "older than 9," not that it's the immediately preceding
supported version - but the backfill logic that would have populated
the new required field lives in the version-7 upgrade script, which
never ran.

Task definitions created before the jump now have the new required
field missing rather than backfilled. The orchestrator's version-9
runtime, which assumes the field is always present post-upgrade,
throws null-reference errors intermittently whenever it processes one
of the pre-existing task definitions, while newly created ones work
fine - a failure pattern that takes the team significant time to
connect back to the skipped intermediate upgrade steps, since the
installer itself reported success.
```

## Statistics
| Finding | Context |
|---|---|
| A meaningful share of major-version upgrade incidents occur specifically on systems that deferred upgrades long enough to require skipping multiple intermediate versions, rather than on systems upgrading one version at a time | Estimated from vendor support-ticket patterns for large version jumps |
| Vendors commonly test and officially support only sequential one-major-version upgrade paths, or a small number of explicitly validated fast-path jumps, leaving arbitrary larger skips untested by definition | Typical pattern observed across major-version software release practices |
| Systems that defer upgrades for multiple release cycles and then attempt a single large jump report substantially higher migration-incident rates than systems upgrading incrementally on each release | Typical range observed comparing incremental vs. deferred-then-batched upgrade strategies |

## Mitigations
1. **Enforce supported-path checks before upgrade execution**: Have upgrade tooling explicitly verify the current version is on a documented supported upgrade path (sequential or an explicitly validated fast path) before proceeding, rather than only checking that the target version is newer.
2. **Sequential intermediate upgrades for large version gaps**: When a system has fallen multiple major versions behind, script the upgrade to pass through each intermediate version's migration logic in sequence, even if that means a longer overall upgrade process, rather than jumping directly to the target.
3. **Regular incremental upgrade cadence to prevent large gaps from accumulating**: Adopt a policy of upgrading within one major version of current on a defined cadence, so the "skip multiple versions" scenario doesn't arise from years of deferral in the first place.
4. **Post-upgrade state validation against expected schema/config, not just upgrade-script exit code**: After any upgrade, validate that data and configuration actually match what the target version expects (e.g., required fields present, deprecated fields cleaned up), rather than treating a zero exit code from the upgrade script as sufficient proof of success.
5. **Vendor engagement before attempting an unsupported jump**: For version gaps larger than the documented supported path, engage the vendor or consult migration guides for an explicitly validated multi-version path before attempting a direct jump, rather than assuming the installer's willingness to run implies support.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| version_gap_at_upgrade_time | Number of major versions being skipped in a planned or attempted upgrade | Alert/require review if gap exceeds the vendor's documented supported single-step path |
| post_upgrade_schema_validation_failures | Count of records/configs failing validation against the target version's expected schema after an upgrade | Alert on any nonzero count following a multi-version-skip upgrade |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Unsupported version jump attempted | Upgrade tooling detects a target-version gap exceeding the documented supported path | High | Block the upgrade pending a sequential path or vendor-validated fast path |
| Post-upgrade state inconsistency detected | Validation finds records/configs not matching the target version's expected schema after a completed upgrade | High | Roll back if possible, run the skipped intermediate migration logic explicitly, re-validate |

## Related Patterns
- [Version Compatibility Matrix Explosion](./version-compatibility-matrix-explosion.md) - a related pattern about the combinatorial difficulty of tracking compatibility across many versioned components, which compounds the risk of an unsupported version skip going unnoticed
- [Version Deprecation Timeline Miss](../../tool-capability-limits/failures/deprecated-endpoint-retirement.md) - deferred upgrades that lead to a large version-skip situation often originate from the same missed-timeline pattern applied repeatedly across several release cycles
- [Rollback Data Consistency](./rollback-data-consistency.md) - shares the same underlying mechanism (state left in a form no single version's logic was designed to handle), applied to a rollback rather than a forward version skip
