# Embedding Retrieval Applies Wrong Service's Capacity Profile by Name Similarity

## Issue: A Capacity-Planning Agent That Selects a Reference Capacity Profile for a New or Under-Profiled Service by Semantic Similarity Over the Service's Name and Description Pulls a Lexically Similar but Operationally Different Profile -- One Built for a Stateless, Horizontally-Scalable API Service -- When Planning Capacity for a Stateful, Single-Writer Cache Service, Recommending an Autoscaling Strategy That Does Not Apply

**Frequency**: Occasional

**Symptoms**
- Capacity recommendation for the new service includes a horizontal autoscaling policy (add replicas under load) that is structurally inapplicable to a single-writer or sharded-by-key service
- The retrieved reference profile's name and description ("checkout-api", "checkout-cache") overlap heavily with the target service's name in tokens and domain vocabulary, despite very different scaling characteristics
- Provisioning based on the recommendation causes either ineffective autoscaling (new replicas added but unable to take write traffic) or, in the inverse case, under-provisioning when a genuinely horizontally-scalable service is matched to a single-writer profile and capped accordingly
- A capacity engineer manually comparing the two services' architecture docs finds no actual operational similarity beyond shared naming conventions
- The mismatch recurs specifically for newly onboarded or renamed services where no team-specific capacity history yet exists, forcing the retrieval step to lean entirely on name/description similarity

**Root Cause**
Selecting a reference capacity profile by embedding or lexical similarity over service name and description captures surface vocabulary overlap (shared domain terms like "checkout," "cache," "session") but not the structural attributes that actually determine whether a capacity strategy transfers: statefulness, write topology, sharding strategy, and scaling mechanism. Two services can be highly similar in the embedding space used for the match while being fundamentally different in exactly the dimensions that matter for capacity planning.

**Example**
```
New service: "checkout-session-cache" (single-writer, key-sharded, no horizontal read replicas)
Capacity-planning agent has no prior capacity history for this service and retrieves the most similar existing profile by semantic similarity over name/description
Closest match returned: "checkout-api-service" (stateless, horizontally autoscaled, scales linearly with request volume)
Agent's recommendation: "Apply checkout-api-service's autoscaling policy: add replicas when CPU exceeds 70%"
checkout-session-cache is deployed with the recommended autoscaling policy; under load, new replicas spin up but cannot take write traffic (single-writer constraint), so the actual bottleneck (the single writer instance) remains unaddressed
Service degrades under peak load despite "successfully" autoscaling to 3x its normal replica count
Root cause identified only when an engineer compares the two services' actual architecture and finds no structural similarity beyond shared naming
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems using embedding similarity over surface descriptions are documented to surface lexically close but structurally mismatched matches when the determining attributes are not encoded in the text being embedded | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Error taxonomies for RAG systems identify retrieval of a topically related but substantively different reference as a distinct, common failure mode separate from retrieval failure (no result) | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Reliability research on retrieval over structured technical domains finds free-text similarity matching underperforms retrieval keyed on the structured attributes that actually determine applicability | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |

**Contributing Factors**
- No structured attribute schema (statefulness, write topology, sharding strategy) used to constrain or re-rank candidate reference profiles before or alongside the similarity match
- Naming conventions across services in the same product area produce high lexical overlap independent of actual architectural similarity
- No fallback path for newly onboarded services with no capacity history other than falling through to similarity-based retrieval
- The agent's recommendation does not surface which structural attributes the matched reference profile shares (or does not share) with the target service, so the mismatch is not visible without manual comparison

---

## Mitigation Strategies

1. **Structured-Attribute Pre-Filter**: Require candidate reference profiles to match on structural attributes (statefulness, write topology, scaling mechanism) before semantic similarity is used to rank among the structurally compatible candidates
2. **Attribute Overlap Disclosure**: Require the agent's recommendation to explicitly list which structural attributes the matched reference profile shares with the target service, making a mismatch visible to a reviewer
3. **New-Service Capacity Intake**: For services with no capacity history, require a minimal structured intake (write topology, expected scaling mechanism) before any reference-profile matching is attempted, rather than relying solely on name/description similarity
4. **Post-Deploy Validation**: Monitor whether an applied autoscaling policy actually changes effective capacity under load within the first deployment cycle, flagging cases where added replicas show no corresponding throughput increase

### Metrics
- Rate of capacity recommendations where the matched reference profile's structural attributes differ from the target service's
- Number of autoscaling events that add replicas with no measurable throughput increase (signal of a structurally mismatched policy)
- Mean time from a structurally-mismatched recommendation being applied to it being identified and corrected

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Structural mismatch in matched profile | Retrieved reference profile's write topology or statefulness differs from target service | P2 | Block recommendation pending structured-attribute review |
| Ineffective autoscaling | Replica count increases under load with no corresponding throughput increase | P2 | Investigate capacity profile applicability; revert to manual sizing |
| Repeated new-service mismatches | Multiple newly onboarded services receive structurally mismatched profiles within a rolling window | P3 | Audit new-service capacity intake process |

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
