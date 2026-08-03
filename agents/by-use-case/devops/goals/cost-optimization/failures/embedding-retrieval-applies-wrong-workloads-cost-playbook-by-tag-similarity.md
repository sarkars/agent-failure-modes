# Embedding Retrieval Applies Wrong Workload's Cost Playbook by Tag Similarity

## Issue: A Cost-Optimization Agent That Selects a Cost-Reduction Playbook for a Flagged Resource by Semantic Similarity Over Its Tags, Name, and Description Pulls a Playbook Written for a Fault-Tolerant Batch Workload -- Recommending Migration to Spot/Preemptible Instances -- and Applies It to a Latency-Sensitive, Interruption-Intolerant Workload That Shares Overlapping Tag Vocabulary but Cannot Tolerate the Same Risk

**Frequency**: Occasional

**Symptoms**
- Cost-optimization recommendation proposes migrating a workload to spot/preemptible capacity, citing a matched playbook whose name and tags ("processing", "batch-tagged-but-not-actually-batch") closely resemble the target workload's own tags
- The target workload is actually a synchronous, customer-facing request path with strict latency and availability requirements incompatible with preemption risk
- Applying the recommendation causes intermittent request failures or latency spikes correlated with spot-instance reclamation events, only discovered after the migration is live
- A engineer manually reviewing the workload's actual traffic pattern (synchronous, low-tolerance-for-interruption) finds no real similarity to the batch workload the playbook was written for, beyond shared tags applied inconsistently across teams
- The mismatch recurs specifically for workloads whose tags were applied for unrelated organizational reasons (cost-center, team ownership) rather than to describe actual workload characteristics

**Root Cause**
Selecting a cost-reduction playbook by embedding or lexical similarity over tags, names, and descriptions captures vocabulary overlap from inconsistent or organizationally-motivated tagging practices, not the workload characteristics (interruption tolerance, latency sensitivity, statefulness) that actually determine whether a given cost strategy is safe to apply. A workload tagged similarly to a batch job for unrelated reasons can be selected as a close match despite having none of the properties that make spot-instance migration appropriate for batch workloads.

**Example**
```
Resource flagged for cost optimization: "checkout-request-handler", tagged "processing", "high-cpu", owned by "platform-cost-center-04"
Cost-optimization agent retrieves the most similar existing playbook by tag/description similarity
Closest match: "image-batch-processing" playbook, also tagged "processing", "high-cpu", written specifically for a fault-tolerant, checkpoint-resumable batch image pipeline
Agent's recommendation: "Migrate checkout-request-handler to spot instances per the high-cpu processing playbook; estimated 60% cost savings"
checkout-request-handler is actually a synchronous request path for live checkout transactions, with no checkpoint/resume capability and strict latency SLAs
Migration to spot instances is applied; subsequent spot-reclamation events cause dropped in-flight checkout requests and customer-visible errors during reclamation windows
Recommendation is reverted after the first reclamation-correlated incident, but not before measurable transaction loss
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems using embedding similarity over surface tags or descriptions are documented to surface lexically close but operationally mismatched matches when the determining attributes are not encoded in the text being embedded | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Error taxonomies for RAG systems identify retrieval of a topically related but substantively different reference as a distinct, common failure mode separate from outright retrieval failure | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Cloud cost-optimization research notes that interruption-tolerance and latency requirements, not surface workload labels, are the determining factors for whether spot/preemptible migration is safe | [Auto-Scaling in Cloud Systems](https://arxiv.org/abs/2007.00066) |

**Contributing Factors**
- No structured attribute schema (interruption tolerance, latency SLA, checkpoint/resume capability) used to constrain candidate playbooks before similarity-based matching
- Organizational tagging conventions (cost-center, team ownership) introduce tag-vocabulary overlap unrelated to actual workload characteristics
- No requirement that the agent disclose which structural attributes the matched playbook and the target workload actually share
- Cost-savings estimates in the recommendation are computed from the matched playbook's typical outcomes, not validated against the target workload's actual interruption tolerance

---

## Mitigation Strategies

1. **Structured-Attribute Pre-Filter**: Require candidate cost playbooks to match on interruption tolerance, latency sensitivity, and checkpoint/resume capability before tag or description similarity is used to select among compatible candidates
2. **Attribute Overlap Disclosure**: Require the recommendation to explicitly state which structural attributes the matched playbook and target workload share, surfacing a mismatch before migration
3. **Staged Rollout for Spot Migration**: Require any spot/preemptible migration recommendation to be validated against a canary subset of the workload's traffic before full migration, regardless of playbook match confidence
4. **Tag-Hygiene Decoupling**: Maintain workload-characteristic attributes (interruption tolerance, latency SLA) as a separate, explicitly-maintained field independent of organizational tags, and require playbook matching to use that field

### Metrics
- Rate of cost-optimization recommendations where the matched playbook's interruption-tolerance assumption differs from the target workload's actual tolerance
- Number of spot-instance migrations reverted within a short window due to reclamation-correlated incidents
- Mean time from a mismatched playbook recommendation being applied to it being identified and reverted

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Interruption-tolerance mismatch | Matched playbook assumes fault tolerance the target workload's SLA does not have | P1 | Block recommendation pending structured-attribute review |
| Reclamation-correlated incident | Customer-facing errors correlate with spot-instance reclamation events post-migration | P1 | Revert migration; re-evaluate playbook matching |
| Repeated tag-vocabulary mismatches | Multiple workloads matched to operationally incompatible playbooks within a rolling window | P3 | Audit tag-hygiene and structured-attribute coverage |

---

## Related Patterns

- [Semantic Similarity Retrieval Misses Structural Attributes (by-capability)](../../../../../by-capability/knowledge-retrieval/goals/retrieval-relevance/failures/semantic-similarity-retrieval-misses-structural-attributes.md) - the general mechanism behind this cost-optimization-specific instance

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Auto-Scaling in Cloud Systems](https://arxiv.org/abs/2007.00066)
