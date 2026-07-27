# What Are the Most Common Capacity Planning Failures in AI Agents?

**Capacity-planning agents make recommendations that look accurate at the aggregate level but fail operationally because they optimize against a single signal (average utilization, a reference profile's name similarity) without checking whether that signal applies to the service's actual architecture or load pattern.** Three patterns are documented, spanning reactive scaling that oscillates instead of converging, retrieval that surfaces an operationally incompatible reference profile by name similarity alone, and infrastructure-level provisioning lag that the decision logic never models. Each failure is silent in the sense that a capacity recommendation can look reasonable until the service is deployed and real traffic exposes the mismatch — average utilization looks low until a peak period arrives, a reference profile looks similar until a service tries to scale horizontally despite being single-writer, or a scale-up decision looks sound until new instances take five minutes to come online and the spike has already passed.

## Key Takeaways

- 3 patterns span reactive-scaling oscillation, reference-profile mismatches, and provisioning-lag blindness.
- Reactive scaling without lag modeling produces constant oscillation when provisioning lag is comparable to load-fluctuation timescale — cost rises from churn while latency also rises from capacity being absent exactly when needed, a lose-lose outcome.
- Reference-profile retrieval by name similarity produces mismatches on architectural dimensions that actually determine whether a strategy applies — statefulness, write topology, sharding — because those dimensions are not encoded in the text being embedded, only in the service catalog's structured attributes.
- Hyperscaler cold-start lag (2-5 minutes for instance startup) is a known, documented infrastructure characteristic, but scaling agents commonly make decisions on instantaneous metrics without this constant factored in, producing systematic under-provisioning during every spike.

## Scope

- **Reactive Scaling Oscillation** — [Autoscaling Thrash from Reactive Agent Decisions](failures/autoscaling-thrash.md). The agent makes scale-up and scale-down decisions on instantaneous metric values without modeling provisioning lag or recent volatility, producing rapid oscillation rather than convergence to the right capacity level.
- **Retrieval-Based Reference Mismatches** — [Embedding Retrieval Applies Wrong Service's Capacity Profile by Name Similarity](failures/embedding-retrieval-applies-wrong-services-capacity-profile-by-name-similarity.md). The agent selects a reference capacity profile by semantic similarity over name and description rather than by structured architectural attributes (statefulness, write topology, scaling mechanism), and applies a profile designed for a stateless service to a stateful one.
- **Provisioning-Lag Blindness** — [Hyperscaler Cold Start Lag in Auto-Scaling](failures/hyperscaler-cold-start-lag.md). The agent's scaling decision model treats instances as available instantly, but cloud instances require 2-5 minutes to boot and start application code, during which time traffic hits the under-provisioned cluster.

## When Capacity Planning Matters

- Workloads have bursty or cyclical load patterns where a capacity that is adequate for average load is insufficient for peak load
- Multiple services share a centralized capacity library or reference-profile matching system, and services have heterogeneous architectures (some stateless, some stateful, some sharded)
- Capacity decisions feed into autoscaling logic whose lag characteristics are non-trivial relative to load-fluctuation timescales

## Cross-Pattern Insight

The three capacity-planning patterns all share the same operational risk: an agent's decision is grounded in a simplified model of either the service (what it actually requires) or the infrastructure (how fast it responds), and the recommendation passes review because the simplified model is not wrong on aggregate — average utilization is low, the reference profile shares naming conventions, the scaling logic is mechanically sound. Failures emerge only when real load or architecture diverges from the assumptions. The shared mitigation across all three patterns is to surface and validate the dimensional assumptions underlying a recommendation before deploying it: not just "average utilization is low" but "peak-to-average ratio is this, and this service's SLA is that"; not just "profiles are similar" but "these structural attributes match"; not just "scaling logic is correct" but "provisioning lag is this, so scale decisions must lead demand by that window."

## Frequently Asked Questions

### What causes autoscaling to continuously add and remove capacity rather than stabilize?
When provisioning lag (time for new instances to boot and come online) is comparable to load-fluctuation timescale, reactive scaling based on instantaneous metric values produces systematic late decisions — new capacity comes online after the spike has passed, triggering immediate scale-down, then the cycle repeats. See [Autoscaling Thrash from Reactive Agent Decisions](failures/autoscaling-thrash.md).

### How do you select the right capacity profile or strategy for a service?
Use structured service-architecture attributes (is the service stateless, stateful, single-writer, sharded? what's the scaling mechanism?) to filter candidate profiles before ranking by similarity. Name and description similarity are poor predictors of whether a profile's strategy actually applies. See [Embedding Retrieval Applies Wrong Service's Capacity Profile by Name Similarity](failures/embedding-retrieval-applies-wrong-services-capacity-profile-by-name-similarity.md).

### Does average utilization alone predict whether a service is over- or under-provisioned?
No — average utilization is a misleading signal when a service has peaks that briefly exceed average by a factor of 2-5x. Capacity must be sized for the peak, not the average; a rightsizing recommendation based on average alone systematically under-provisions workloads with peaks. See [Capacity Optimization](../cost-optimization/) for related rightsizing failures.

### Can scaling decisions be made instantly once a load increase is detected?
No — cloud instances require 2-5 minutes to boot and start application code, so decisions must be made predictively (scaling ahead of expected load) or account for a lag window where capacity is being provisioned but not yet serving. Reactive scaling that assumes instant availability produces under-provisioning during every real spike. See [Hyperscaler Cold Start Lag in Auto-Scaling](failures/hyperscaler-cold-start-lag.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Autoscaling Thrash from Reactive Agent Decisions](failures/autoscaling-thrash.md) | Reactive scaling without lag modeling produces oscillation when provisioning lag is comparable to spike timescale |
| [Embedding Retrieval Applies Wrong Service's Capacity Profile by Name Similarity](failures/embedding-retrieval-applies-wrong-services-capacity-profile-by-name-similarity.md) | Reference profile selected by name similarity without checking architectural compatibility |
| [Hyperscaler Cold Start Lag in Auto-Scaling](failures/hyperscaler-cold-start-lag.md) | Scaling decisions assume instant instance availability, but cloud startup takes 2-5 minutes |

**Total: 3 patterns**

## Related Goals

- [Cost Optimization](../cost-optimization/) — rightsizing and resource-trimming decisions that depend on accurately modeling which capacity is actually needed
- [Monitoring](../monitoring/) — metric quality and availability that feed into capacity-planning decisions
- [Deployment Safety](../deployment-safety/) — infrastructure compatibility validation that runs alongside capacity changes
