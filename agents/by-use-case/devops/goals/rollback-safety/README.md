# What Are the Most Common Rollback Safety Failures in AI Agents?

**Rollback agents fail to actually restore working behavior because they treat orchestrator-level deployment success (pods are Ready, the rollout state is Succeeded) as sufficient validation that the application is healthy, ignore stateful side effects (schema changes, cache invalidation, feature-flag resets) that the rollback does not undo, or lose a critical override flag (do-not-revert marker on a hotfix) at the handoff boundary so an automated rollback reverts a separate, concurrent fix along with the bad change.** Three patterns are documented here, spanning orchestrator-state vs. application-health confusion, stateful-side-effect inconsistency, and protection-flag handoff loss. Each failure allows a rollback to be reported as successful when it has not actually restored the service to a working state — the change is reverted, but the state is corrupted, or the readiness probe passes while errors continue, or a concurrent hotfix gets collateral reverted — so the incident remains unresolved even though the automated system has marked itself complete.

## Key Takeaways

- 3 patterns span orchestrator-state misidentification, stateful-side-effect handling, and protection-flag handoff loss.
- Rollback declared successful based solely on orchestrator status (replicas at target revision, readiness probe passing) will miss cases where the pod readiness check is shallow and the application continues serving errors due to stale caches, unreset feature flags, or unrolled-back dependencies — orchestrator state and application health diverge in these cases.
- Database schema changes and message-format changes applied by a bad version are not reverted when the artifact is rolled back — a rollback that succeeds at the code level can fail at the state level if schema or message incompatibilities are left unresolved, producing a second, different incident post-rollback.
- Protection flags on hotfixes (do-not-revert markers) that exist only in deploy commentary, not in structured deploy-history fields, are invisible to the rollback agent's decision logic, allowing it to revert the hotfix along with the bad change and re-introduce the separate incident the hotfix had just fixed.

## Scope

- **Orchestrator-State Misidentification** — [Orchestrator Status Mistaken for Application Health After Rollback](failures/orchestrator-status-mistaken-for-application-health-after-rollback.md). Rollback is marked complete based on the deployment orchestrator reporting "Succeeded" and readiness probe passing, without checking whether the application's actual health signal (error rate, symptom metric) has returned to baseline.
- **Stateful-Side-Effect Corruption** — [Partial Rollback State Corruption](failures/partial-rollback-state-corruption.md). Code is rolled back but a schema migration or message-format change applied by the bad version remains, leaving the rolled-back (old-format-expecting) code running against incompatible state.
- **Protection-Flag Handoff Loss** — [Multi-Agent Handoff Drops Override Flag Between Deploy and Rollback Agent](failures/multi-agent-handoff-drops-override-flag-between-deploy-and-rollback-agent.md). A deploy agent notes a hotfix's protected status in free-text commentary, but the structured deploy-history record the rollback agent reads carries no corresponding field, so the rollback reverts the hotfix.

## When Rollback Safety Matters

- Automated rollback decisions are triggered based on metric regression, rather than requiring manual confirmation
- Services maintain state (in-process caches, connection pools, feature-flag values) that is not reset purely by redeploying the prior artifact
- Hotfixes or out-of-band patches are applied independently of scheduled releases, and distinguishing a hotfix-containing revision from an ordinary revision is important for selective rollback

## Cross-Pattern Insight

Rollback failures occur because an agent treats a proxy signal (orchestrator status, code-version reversion, lack of a protection flag) as equivalent to the actual outcome the rollback was supposed to achieve (the incident is resolved). Orchestrator status tells you whether the artifact reversion succeeded technically; it does not tell you whether the application is healthy. Code rollback tells you whether the prior artifact is back in the live path; it does not tell you whether that artifact is compatible with the state the bad version left behind. Absence of a protection-flag field tells you nothing about whether a field should exist. All three failures share the pattern that a rollback can be technically complete and still fail to restore working behavior because the agent never validated the outcome against the original problem. The shared mitigation across all three patterns is verification gates that separate concerns: (1) orchestrator completion is a precondition to check application health, not a substitute; (2) stateful side effects must be explicitly inventoried and remedied as part of the rollback plan, not assumed to be harmless; (3) protection flags must be structured fields the rollback logic reads, not optional commentary that can be lost at handoff boundaries.

## Frequently Asked Questions

### What does it mean when a rollback is marked successful but the problem persists?
Rollback agents commonly use orchestrator state (replicas at target revision, readiness probe passing) as the success criterion, but orchestrator state describes only whether the artifact was successfully reverted — not whether the application is actually healthy. If the application depends on state not reset by artifact-only rollback (an in-process cache, a feature flag set at startup, an unrolled-back dependency), the orchestrator success is premature. See [Orchestrator Status Mistaken for Application Health After Rollback](failures/orchestrator-status-mistaken-for-application-health-after-rollback.md).

### Can you safely roll back a deploy that included a database migration?
Not with artifact rollback alone. Code rollback reverts the artifact, but schema changes persist, leaving the rolled-back code incompatible with the schema the bad version introduced. A safe rollback plan must include either reverting the migration (if safe) or validating schema backward-compatibility. See [Partial Rollback State Corruption](failures/partial-rollback-state-corruption.md).

### What happens if an automated rollback reverts a concurrent hotfix?
If the hotfix is marked with a do-not-revert flag only in deploy commentary, not in a structured field the rollback agent reads, the rollback will revert the hotfix along with the bad change, re-introducing the separate incident the hotfix had just fixed. The deploy agent's protection note is lost at the handoff boundary. See [Multi-Agent Handoff Drops Override Flag Between Deploy and Rollback Agent](failures/multi-agent-handoff-drops-override-flag-between-deploy-and-rollback-agent.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Multi-Agent Handoff Drops Override Flag Between Deploy and Rollback Agent](failures/multi-agent-handoff-drops-override-flag-between-deploy-and-rollback-agent.md) | Deploy agent's protection note exists only in commentary, invisible to rollback agent's structured decision logic |
| [Orchestrator Status Mistaken for Application Health After Rollback](failures/orchestrator-status-mistaken-for-application-health-after-rollback.md) | Rollback marked successful based on orchestrator status, without confirming the original symptom metric has recovered |
| [Partial Rollback State Corruption](failures/partial-rollback-state-corruption.md) | Code rolled back but stateful side effects (schema changes, message-format changes) from bad version persist, corrupting state |

**Total: 3 patterns**

## Related Goals

- [Deployment Safety](../deployment-safety/) — preventing bad deploys that need to be rolled back in the first place
- [Incident Response](../incident-response/) — detection and triage that determines whether a rollback is the right response
- [Monitoring](../monitoring/) — health signals that validate whether a rollback has actually restored working behavior
