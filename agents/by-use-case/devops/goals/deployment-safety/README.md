# What Are the Most Common Deployment Safety Failures in AI Agents?

**Deployment-safety agents fail to catch unsafe conditions before go-live because they apply the wrong checklist, miss dependency incompatibilities, base approval on segment-obscured aggregate metrics, or never encode a precondition in the structured deploy manifest that a downstream executor needs to verify.** Four patterns are documented here, spanning checklist-retrieval mismatches, hidden dependency version conflicts, canary approval based on aggregate-only metrics, and cross-system preconditions that vanish at the handoff boundary. Each failure allows a deploy to proceed that should have been blocked, and the unsafe condition is not discovered until production traffic hits the change and an incident surfaces the gap — a schema incompatibility, a dependency version break, a segment-specific regression, or a missing prerequisite flag flip.

## Key Takeaways

- 4 patterns span checklist-retrieval mismatches, dependency-compatibility blindness, segment-obscured canary analysis, and precondition handoff loss.
- Canary analysis that compares only aggregate metrics (overall error rate, overall latency) will miss segment-concentrated regressions where a minority traffic segment experiences severe impact that is diluted into the aggregate — documented to occur with low-traffic segments as small as 5% of total volume.
- Semantic versioning is violated by an estimated 10-30% of packages, making "minor version bump assumed safe" a risky heuristic — deployment safety requires either locked dependencies or active compatibility checking, not trust in semver discipline.
- Checklist-selection mismatches concentrate on services where the description text most closely resembles an existing template, particularly for newly onboarded services where the description is the only signal available for retrieval, since no service-specific deployment history yet exists.

## Scope

- **Checklist-Retrieval Mismatches** — [Embedding Retrieval Applies Wrong Service's Deployment Checklist](failures/embedding-retrieval-applies-wrong-services-deployment-checklist.md). A pre-deploy safety checklist is selected by semantic similarity over description, pulling a checklist for a stateless service when deploying a stateful service, omitting a required schema-migration gate.
- **Dependency-Compatibility Blindness** — [Dependency Hell & Version Compatibility Blindness](failures/dependency-hell-blindness.md). A deploy proceeds despite a dependency update that violates semver — a "minor" version bump that contains a breaking change — because the agent does not validate semver compliance before deployment.
- **Segment-Obscured Canary Approval** — [Canary Analysis False Pass](failures/canary-analysis-false-pass.md). Canary approval is based on aggregate health metrics, and a regression concentrated in a low-traffic segment (e.g., mobile-app-v2 users at 5% of traffic) is diluted below the detection threshold.
- **Cross-Agent Precondition Loss** — [Multi-Agent Handoff Drops Feature-Flag Precondition Between Deploy Agent and Config Agent](failures/multi-agent-handoff-drops-feature-flag-precondition-between-deploy-agent-and-config-agent.md). A deployment agent determines a feature flag must be set before deploy is safe, but the deploy manifest has no field for cross-system preconditions, so the config agent applies the deploy without the flag ever being flipped.

## When Deployment Safety Matters

- New or renamed services have no deployment history and checklist selection falls back to name/description similarity
- Dependency updates are applied without locked versions or automated compatibility checking
- Canary traffic is a small percentage of production traffic or is not representative of production's segment mix
- Deployment and configuration management are separate systems, and preconditions in one system must propagate to the other

## Cross-Pattern Insight

Deployment-safety failures all occur because an agent authorizes a deploy based on a check that is structurally sound but informationally incomplete. A checklist that is correctly applied for a stateless service is the wrong checklist for a stateful one, but retrieval by name similarity cannot distinguish the two. A dependency version was updated, but semver discipline was not verified before promotion. A canary passed health checks, but segment-level analysis was never performed alongside aggregate analysis. A precondition was correctly identified and reasoned through, but never encoded as a field the downstream executor reads. None of the four failures originates in a flawed safety check; each check ran correctly against its input, and the input was incomplete. The shared mitigation is the same across all four patterns: encode the structural assumption (service class, semver discipline, segment-level requirements, cross-system dependencies) explicitly and validate it before deploy is authorized, not after incidents surface the gap.

## Frequently Asked Questions

### What causes a deploy checklist to omit a critical safety gate?
When checklist selection is based on semantic similarity over service description rather than structured service attributes, two checklists with similar prose (both describing "a standard deploy review") can score equally in embedding space despite one being missing a section required for stateful services. The retrieval step has no signal distinguishing "describes a similar deploy process" from "actually applies to this service's class." See [Embedding Retrieval Applies Wrong Service's Deployment Checklist](failures/embedding-retrieval-applies-wrong-services-deployment-checklist.md).

### Can you assume a "minor" version bump is safe due to semantic versioning?
No — semver is a convention, not enforced by package managers. An estimated 10-30% of packages violate semver and include breaking changes in "minor" versions. Deployment safety requires either locked dependencies to ensure staging and prod use the same version, or automated breaking-change detection before deployment. See [Dependency Hell & Version Compatibility Blindness](failures/dependency-hell-blindness.md).

### How do you catch a regression that affects only a specific user segment in canary testing?
Require canary analysis to break down health metrics by the highest-cardinality dimensions relevant to the service (client version, region, request type, customer tier), not aggregate-only. A severe regression concentrated in a 5% traffic segment will be diluted below detection thresholds if only aggregate metrics are compared. See [Canary Analysis False Pass](failures/canary-analysis-false-pass.md).

### What happens if a deploy requires a feature flag to be set first, but that requirement is only mentioned in planning notes?
The flag flip never happens. If the deploy manifest has no field for preconditions, and the configuration agent acts only on the manifest, the prerequisite dependency is invisible to the downstream executor. The deploy proceeds with the flag in the wrong state, causing the new code path to execute against old assumptions. See [Multi-Agent Handoff Drops Feature-Flag Precondition Between Deploy Agent and Config Agent](failures/multi-agent-handoff-drops-feature-flag-precondition-between-deploy-agent-and-config-agent.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Canary Analysis False Pass](failures/canary-analysis-false-pass.md) | Aggregate metrics pass, but a regression concentrated in a low-traffic segment is invisible to aggregate-only analysis |
| [Dependency Hell & Version Compatibility Blindness](failures/dependency-hell-blindness.md) | Deploy proceeds with a dependency update that contains a breaking change, violating semver |
| [Embedding Retrieval Applies Wrong Service's Deployment Checklist](failures/embedding-retrieval-applies-wrong-services-deployment-checklist.md) | Checklist selected by name similarity, omitting a section required for the service's actual structural class |
| [Multi-Agent Handoff Drops Feature-Flag Precondition Between Deploy Agent and Config Agent](failures/multi-agent-handoff-drops-feature-flag-precondition-between-deploy-agent-and-config-agent.md) | Deploy precondition exists only in deployment agent's reasoning, not in the structured deploy manifest config agent reads |

**Total: 4 patterns**

## Related Goals

- [Monitoring](../monitoring/) — observability and alerting that validates a deploy's correctness once it reaches production
- [Rollback Safety](../rollback-safety/) — recovery when a deploy that passed safety checks proves unsafe in production
- [Capacity Planning](../capacity-planning/) — resource requirements validation that may be needed alongside deployment checklists
