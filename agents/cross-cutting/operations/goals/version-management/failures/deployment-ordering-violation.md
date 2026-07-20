# Deployment Ordering Violation

## Issue
A release requires a specific sequence — for example, a database migration adding a new column that the updated agent orchestrator code depends on must land before the orchestrator itself is deployed — but the deployment pipeline applies the two changes out of order, or applies them concurrently without an enforced dependency. The new orchestrator code starts up and immediately queries or writes the column that doesn't exist yet, crashing on startup or, worse, silently defaulting to null/empty values that corrupt downstream agent state (e.g., losing a conversation's tool-permission scope because the column that stored it isn't there yet).

**Frequency**: Occasional

**Symptoms**
- New service version crashes on startup or on first request with a schema/column/table-not-found error
- Errors reference a resource (column, config key, feature flag, API field) that a companion change was supposed to have created first
- The failure appears only in production or staging, not locally, because local dev environments run migrations synchronously before app startup while the pipeline doesn't enforce the same order
- Rolling back the code deploy "fixes" the symptom even though the actual root cause was ordering, not the code itself
- Post-incident review finds both changes were merged and both pipelines ran, just not in the required sequence

## Root Cause
Deployment pipelines for different artifact types (database migrations, application code, infrastructure config, feature flags) are frequently owned by separate tools or separate CI jobs that trigger independently — a migration runs via one Terraform/Flyway job, the application deploys via a separate Kubernetes rollout — with no shared dependency graph between them. When a change genuinely requires ordering ("column must exist before code that reads it deploys"), that requirement usually lives only as a comment in a PR description or a runbook step, not as a machine-enforced gate. If the two pipelines are triggered by the same merge event, or by two people merging in quick succession, they can run concurrently or in reverse order, and nothing in either system checks the precondition before proceeding.

## Example
```
"AgentSessionStore" service stores tool-permission scopes per
conversation. Migration 0047 adds a new "scope_version" column
(NOT NULL, no default) to the sessions table. Orchestrator v31 reads
scope_version on every tool-call authorization check and treats a
missing value as "no permission granted" per its updated logic.

Planned order: run migration 0047, confirm it applied, then deploy
orchestrator v31.

Actual sequence: the migration job and the orchestrator v31 deploy
are both triggered by the same merge to main, via two separate
GitHub Actions workflows with no explicit dependency between them.
The orchestrator deploy workflow happens to complete first because
its build cache was warm; the migration job is still running.

For approximately 6 minutes, orchestrator v31 pods are live against
a database that doesn't yet have scope_version. Every tool-call
authorization check throws a column-not-found error, which the code
catches and — per its "missing value = no permission" logic — denies
every tool call platform-wide. Every agent session that attempts a
tool call during this window silently falls back to "I don't have
permission to do that" for actions that should have been allowed.

Migration completes 6 minutes later; errors stop without anyone
having intervened, which delays diagnosis because the "incident"
appears to resolve itself before on-call finishes investigating.
```

## Statistics
| Finding | Context |
|---------|---------|
| Migration-before-code ordering violations are a commonly cited cause of brief, self-resolving production incidents that are hard to diagnose after the fact | Typical pattern reported in post-incident reviews of decoupled deploy pipelines |
| A meaningful share of these incidents are self-resolving within minutes (once the delayed step catches up), which correlates with lower detection and higher recurrence rates | Estimated from teams tracking incident duration versus root-cause persistence |
| Explicit pipeline dependency gating (migration job blocking the dependent app deploy) eliminates the large majority of ordering-violation incidents in teams that adopt it | Reported range across teams that added cross-pipeline dependency gates |

## Mitigations
1. **Explicit cross-pipeline dependency gates**: Make the application deployment pipeline programmatically wait on and verify completion of any migration or config change it depends on, rather than relying on merge-order timing or human sequencing.
2. **Backward-compatible-first schema changes**: Follow an expand-contract pattern for schema changes — add the new column as nullable with application-level defaulting first, deploy code that can handle both states, then tighten the constraint in a later migration — so strict ordering is rarely required in the first place.
3. **Startup precondition checks**: Have the application verify its required schema/config preconditions on startup and fail fast with a clear, unambiguous error (rather than degrading silently) if a dependency hasn't been applied yet.
4. **Single orchestrated release pipeline**: Where genuine ordering is unavoidable, model the full release (migration + deploy) as one pipeline with explicit sequential stages rather than two independently triggered systems.
5. **Ordering-violation postmortem tagging**: Explicitly tag incidents caused by deployment ordering as a distinct root-cause category in postmortems, so recurring instances are visible in aggregate rather than each one looking like an isolated one-off.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| schema_dependency_error_rate | Rate of errors referencing a missing column/table/config key within 15 minutes of a deploy | Alert if > 0 immediately following any deploy |
| deploy_migration_sequence_gap | Time gap between a dependent app deploy completing and its required migration completing | Alert if app deploy completes before migration in the same release |
| startup_precondition_failure_count | Count of pods/instances failing startup precondition checks | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Schema/config dependency error spike | Errors referencing a missing resource spike immediately after a deploy | High | Roll back or pause the dependent deploy, verify migration/config status, re-sequence |
| Out-of-order pipeline completion detected | Dependent app deploy pipeline completes before its declared upstream dependency | High | Block further traffic shift, alert deploying team, verify data integrity for the affected window |

## Related Patterns
- [Deployment Dependency Deadlock](./deployment-dependency-deadlock.md) - the inverse problem: an ordering requirement is respected so conservatively that neither side deploys
- [Deployment Validation Skipped](./deployment-validation-skipped.md) - a missing precondition check is a specific form of a skipped validation gate
- [Version Rollout Coordination](./version-rollout-coordination.md) - broader failures in sequencing dependent services' version updates, of which strict ordering violations are one case
