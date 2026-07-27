# What Are the Most Common Underwriting Failures in AI Agents?

**Underwriting agents fail when an occupation-class retrieval step matches applicants by job-title lexical similarity to a prior case without verifying that the retrieved precedent's actual hazard profile matches the current applicant's stated duties, when a multi-agent handoff loses an inspection-flagged hazard requiring a mandatory exclusion rider, and when the agent answers a catastrophe-zone question from memorized training-era geographic data instead of calling the live catastrophe-modeling or mapping tool.** The three failure mechanisms replicate across all insurance workflows: retrieval without corroborating structural verification, handoff without schema fields for task-relevant determinations, and parametric memory defeating tool-grounding for actively maintained data. Each failure produces an underwriting decision that looks well-reasoned — an applicant classified to a precedent occupation, a policy bound without a flagged-hazard rider, a property assigned to a memorized flood zone — but is wrong in ways that emerge later, after underwriting has closed and a loss occurs, or during a risk-management review.

## Key Takeaways

- 3 patterns are documented for underwriting, one per failure mechanism: embedding-retrieval job-title mismatch, multi-agent handoff loss, and stale-training-corpus override.
- The embedding-retrieval pattern shows an applicant classified as a high-risk industrial technician based on matching job-title keywords with a lower-risk field technician, with no verification that the applicant's actual stated duties align with the applied rate class.
- The multi-agent-handoff pattern documents an underwriting-assistant agent correctly identifying an inspection-flagged hazard requiring a mandatory rider in its risk narrative, but the structured binding schema passed to the policy-issuance agent has no field for inspection-flagged riders.
- The stale-training-corpus pattern shows an agent assigning a property to a FEMA flood zone based on pretraining-era zone data, missing a subsequent map revision that reclassified the property to a higher-risk zone, an error caught only when a claim triggers a coverage review.

## Scope

- **Retrieval mismatch** — [Embedding-Retrieval Applies Wrong Occupation-Class Rate Precedent by Lexical Similarity](failures/embedding-retrieval-applies-wrong-occupation-class-rate-precedent-by-lexical-similarity.md). Occupation classification retrieves a precedent case by job-title text similarity without verifying the retrieved case's actual duty profile (work environment, hazard exposure) matches the applicant's stated duties.
- **Handoff information loss** — [Multi-Agent Handoff Drops Inspection-Flagged Hazard Before Policy Binding](failures/multi-agent-handoff-drops-inspection-flagged-hazard-before-policy-binding.md). An underwriting-assistant agent identifies an inspection-flagged hazard requiring a mandatory rider in its risk narrative, but the structured binding schema has no field for inspection-identified riders.
- **Stale parametric override** — [Stale Training-Corpus Catastrophe-Zone Data Overrides Live Feed](failures/stale-training-corpus-catastrophe-zone-data-overrides-live-feed.md). An agent answers a property's flood zone, wildfire tier, or hurricane exposure from pretraining-era geographic knowledge instead of calling the live catastrophe-modeling or mapping tool.

## When Underwriting Matters

- An underwriting system classifies applicant occupations by retrieval against a corpus of prior cases with varying hazard profiles
- Property inspections identify hazards that require non-standard riders or exclusions not present in the standard binding templates
- Geographic risk zones (flood zones, wildfire tiers, hurricane exposure) have been remapped or updated since the underwriting model's training data

## Cross-Pattern Insight

The same three structural failures documented across claim processing, fraud detection, and policy management recur in underwriting with identical mechanisms: pre-filter retrieval by structured hazard attributes before similarity ranking, extend handoff schemas to carry task-relevant findings the upstream stage identified, and force tool calls to live data for any field subject to periodic revision or carrier-specific curation. The business impact differs — an underwriting error affects the policies issued and the risk profile of the bound book — but the failure pattern is structurally identical across all four insurance use cases.

## Frequently Asked Questions

### Can two occupations with similar job titles belong to different risk classes?
Yes. "Field service technician" can refer to a low-hazard role (telecom cabling, indoor work) or a high-hazard role (industrial refrigeration repair with platform work and hazardous materials). Classification by job-title lexical similarity alone misses the hazard-profile differences and can misapply rate factors. See [Embedding-Retrieval Applies Wrong Occupation-Class Rate Precedent by Lexical Similarity](failures/embedding-retrieval-applies-wrong-occupation-class-rate-precedent-by-lexical-similarity.md).

### How does an inspection-flagged hazard get lost between underwriting and policy binding?
If the underwriting agent's risk narrative notes a flagged hazard requiring a rider, but the structured binding schema has no field for "inspection-identified riders," the finding never reaches the policy-issuance agent. The fix is adding a structured rider-requirement field and reconciliation against upstream narratives. See [Multi-Agent Handoff Drops Inspection-Flagged Hazard Before Policy Binding](failures/multi-agent-handoff-drops-inspection-flagged-hazard-before-policy-binding.md).

### Should an underwriting agent know a property's flood zone without looking it up?
No. Flood zones, wildfire tiers, and hurricane exposure bands are remapped periodically by authoritative sources (FEMA, state agencies), and the agent's memorized geographic knowledge reflects data from its training cutoff. The fix is a forced mapping/catastrophe-model tool call for every risk-zone-relevant field. See [Stale Training-Corpus Catastrophe-Zone Data Overrides Live Feed](failures/stale-training-corpus-catastrophe-zone-data-overrides-live-feed.md).

### How do you verify an occupational classification is hazard-appropriate?
Compare the applicant's stated duty description against the retrieved precedent case's duty description using structured hazard-attribute tags (work environment, hazard exposure category, equipment handled), not just job-title text similarity.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Embedding-Retrieval Applies Wrong Occupation-Class Rate Precedent by Lexical Similarity](failures/embedding-retrieval-applies-wrong-occupation-class-rate-precedent-by-lexical-similarity.md) | Occupation retrieved by job-title text similarity without verifying hazard-attribute match against applicant's duties |
| [Multi-Agent Handoff Drops Inspection-Flagged Hazard Before Policy Binding](failures/multi-agent-handoff-drops-inspection-flagged-hazard-before-policy-binding.md) | Underwriting-assistant identifies hazard in risk narrative; binding schema has no field for inspection-flagged riders |
| [Stale Training-Corpus Catastrophe-Zone Data Overrides Live Feed](failures/stale-training-corpus-catastrophe-zone-data-overrides-live-feed.md) | Agent assigns risk zone from memorized training-era data instead of querying live catastrophe-modeling or mapping tool |

**Total: 3 patterns**

## Related Goals

- [Claim Processing](../claim-processing/) — the same three mechanism clusters (retrieval, handoff, stale-corpus) recur in claims adjudication
- [Fraud Detection](../fraud-detection/) — the same three mechanism clusters recur in SIU referral workflows
- [Policy Management](../policy-management/) — the same three mechanism clusters recur in renewal and endorsement workflows
