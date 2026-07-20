# Deployment Dependency Deadlock

## Issue
Two services in an agent pipeline — for example, the orchestrator that calls tools and the tool-schema registry it depends on — each have a deployment that is written to wait for the other to update first, so neither team is willing to deploy. The orchestrator team wants the registry to publish the new tool schema before they roll out code that assumes it exists; the registry team wants the orchestrator's new validation logic live before they push a schema change that would otherwise break the old validator. Both releases sit staged and ready, and the system stays on outdated, incompatible-in-the-making versions indefinitely because each side is correctly avoiding breaking the other, but nobody has sequenced who actually moves first.

**Frequency**: Occasional

**Symptoms**
- Two or more release branches sit "ready to deploy" for days or weeks with no forward progress
- Deployment runbooks for each service explicitly reference "waiting on [other service] to deploy first"
- Slack/ticket threads show both teams independently confirming they're blocked on the other
- Neither service's change is technically difficult; the delay is entirely coordination, not implementation
- The eventual resolution is a manually negotiated joint deployment window rather than either pipeline resolving it automatically

## Root Cause
This arises when a compatibility constraint is genuinely bidirectional at the boundary between two independently deployed services — service A's new behavior only works with service B's new contract, and service B's new contract would break service A's old behavior — but the constraint is expressed informally (tribal knowledge, a comment in a design doc) rather than as an explicit compatibility contract the deployment tooling can reason about. Without a formal ordering mechanism, each team defaults to the conservative, locally-correct decision — "don't deploy until the other side is ready" — and because both teams are applying the same logic symmetrically, there is no natural asymmetry to break the tie. The deadlock only resolves when a human notices the mutual blocking and imposes an explicit order, typically by finding a backward/forward-compatible intermediate step that neither team had designed for because the pipeline didn't require one.

## Example
```
"ToolRegistry" service is adding a new required "cost_estimate" field
to its tool-schema API response. "AgentOrchestrator" service is
adding validation logic that requires "cost_estimate" to be present
before allowing a tool call to execute.

ToolRegistry team's reasoning: "If we ship the new field before
Orchestrator's validator is live, nothing changes for old
orchestrator versions - the extra field is just ignored. But if we
publish it and something else about the schema changed, we don't
want to find out only after Orchestrator is depending on it - let's
wait for their green light."

Orchestrator team's reasoning: "Our validator will reject every tool
call if cost_estimate is missing. We cannot deploy the validator
until the registry is actually serving that field, or every agent
session in production starts failing tool calls immediately."

Both PRs sit approved and merged-to-staging for 11 days. Each team's
weekly sync notes say "blocked on [other team]." Neither pipeline has
a mechanism to express "registry field is additive and safe to ship
independently; validator is the only piece that actually needs
sequencing" - that judgment call only gets made when an engineering
manager from both teams gets on a call and manually agrees: registry
ships the field first (safe, additive), soaks for 48h, then
orchestrator ships the validator against the now-live field.
```

## Statistics
| Finding | Context |
|---------|---------|
| Cross-service deployment deadlocks are commonly resolved via ad hoc human coordination (a meeting or thread) rather than tooling, in teams without explicit compatibility contracts | Typical pattern reported across microservice/agent-pipeline teams |
| Additive, backward-compatible schema changes are frequently over-conservatively sequenced as if they were breaking changes, when only one side of the pair actually requires ordering | Estimated from post-incident review of resolved deployment deadlocks |
| Teams that adopt explicit "expand-contract" deployment conventions report meaningfully fewer cross-service deployment stalls | Reported range across teams adopting formal compatibility-contract practices |

## Mitigations
1. **Expand-contract deployment convention**: Require breaking-looking changes to be split into an additive "expand" phase (new field/behavior added, old path still works) that can always deploy first independently, followed by a "contract" phase (old path removed/enforced) that deploys only after the expand phase has soaked — removing the false symmetry that causes deadlock.
2. **Explicit machine-readable compatibility contracts**: Encode cross-service version compatibility (e.g., "orchestrator v14+ requires registry v8+") in a shared manifest that deployment tooling can check, so ordering constraints are explicit and automatable rather than living in Slack threads.
3. **Deployment dependency graph visibility**: Maintain a live view of which pending releases are waiting on which other releases, so a mutual-block pattern is visible to any engineer or manager rather than discovered only when two people happen to compare notes.
4. **Default to additive-first ordering**: When a change can be made backward-compatible, establish a team norm that the backward-compatible side always ships first without waiting for agreement, breaking the symmetric-caution deadlock by convention.
5. **Joint deployment windows for genuinely coupled changes**: For the subset of changes that truly cannot be made independently safe (rare, if expand-contract is followed), schedule an explicit joint deployment window with both teams present rather than an indefinite wait-and-see.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| release_staged_duration | Time a release has been approved/ready but not deployed | Alert if > 72 hours with an identified cross-service blocker |
| cross_service_block_count | Number of active releases whose blocking reason references another team's pending release | Alert if > 0 sustained for more than a week |
| mutual_block_pairs | Count of release pairs where each blocks on the other | Alert on any detected occurrence |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Mutual deployment block detected | Two releases each list the other as a blocking dependency | Medium | Escalate to both team leads, evaluate expand-contract split, schedule joint window if needed |
| Stale staged release | A release has sat ready-to-deploy beyond the staleness threshold | Low | Review blocking reason, confirm still valid, unblock or reprioritize |

## Related Patterns
- [Deployment Ordering Violation](./deployment-ordering-violation.md) - the inverse failure mode: an ordering constraint exists but gets violated rather than over-conservatively enforced
- [Version Rollout Coordination](./version-rollout-coordination.md) - broader coordination failures across dependent services' rollouts, of which mutual deadlock is one specific shape
- [Version Compatibility Matrix Explosion](./version-compatibility-matrix-explosion.md) - both stem from under-specified cross-service version compatibility contracts
