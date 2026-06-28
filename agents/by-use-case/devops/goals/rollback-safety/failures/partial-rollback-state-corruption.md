# Partial Rollback State Corruption

## Issue: Agent Initiates an Automated Rollback of a Bad Deployment Without Accounting for Stateful Side Effects (Schema Changes, Queued Messages, Cached Data) Already Caused by the Bad Version

**Frequency**: Common

**Symptoms**
- Application code is rolled back to the previous version, but a database migration applied by the bad version is not reverted, leaving the old code running against a schema it does not expect
- Messages already published to a queue in a new, incompatible format by the bad version are consumed by the rolled-back (old-format-expecting) consumer code, causing processing errors
- Caches populated with data shaped by the bad version's logic are not invalidated, so the rolled-back version reads stale or incompatibly-shaped cached data
- Rollback is reported as "successful" because the deployment step completed, even though downstream stateful inconsistency causes a second, different incident shortly after

**Root Cause**
Automated rollback agents typically treat rollback as reverting the deployed artifact (container image, binary, config) to a prior version, which is the only state that a deployment system directly controls. Schema changes, message formats, and cache contents are side effects of the bad version's execution that persist independently of the deployed artifact, so artifact-level rollback alone does not undo them — successful rollback of the code is necessary but not sufficient for actually restoring the system to a consistent prior state.

**Example**
```
Scenario: Bad deploy includes both application code and a database migration adding a new required column
Incident: Bad version causes errors; automated rollback agent reverts the application artifact to the previous version
Migration: Not rolled back (rollback agent has no migration-reversal step)
Result: Previous application version now queries a table with an unexpected required column it doesn't populate
Impact: New, different errors immediately following the "successful" rollback
```

**Key Statistics**
- Stateful side-effect inconsistency following code-only rollback is a long-documented operational risk in deployment safety practice, particularly for database migrations and message format changes
- Configuration drift and reconciliation research on AI agents for infrastructure highlights state-vs-artifact mismatch as a recurring class of automation failure
- Forward-compatible migration strategies (expand/contract pattern) are the standard mitigation recommended specifically because naive migration rollback is often unsafe or impossible once new data has been written

---

## Mitigation Strategies

1. **Stateful-Side-Effect Inventory**: Before any deploy that includes a schema change, queue format change, or cache-shape change, record what stateful side effects it introduces so a rollback plan can account for them explicitly
2. **Expand/Contract Migration Discipline**: Require schema and format changes to follow an expand/contract pattern (new field/format is additive and backward-compatible before old field/format is removed) so that artifact rollback alone remains safe
3. **Rollback Plan Validation Gate**: Automated rollback should refuse to proceed as "code-only" if the bad version's deploy included a non-backward-compatible stateful change, and instead trigger a broader, explicit remediation plan
4. **Post-Rollback Consistency Check**: After rollback completes, run an automated consistency check (schema compatibility, queue consumer compatibility) before declaring the rollback successful

### Metrics
- % of deploys following expand/contract discipline for any stateful change
- Rate of "successful" rollbacks followed by a second incident within a short window (rollback effectiveness)
- Time between rollback completion and post-rollback consistency check passing

### Alerts
- Rollback executed for a deploy that included a non-backward-compatible schema/format change, with no migration-reversal or compatibility step → P1
- New error signature appears within a short window following a "successful" rollback → P1

---

## References

- [RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection](https://arxiv.org/pdf/2603.02345)
- [Automated Cloud Infrastructure-as-Code Reconciliation with AI Agents](https://arxiv.org/pdf/2510.20211)
