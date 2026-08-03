# Embedding Retrieval Applies Wrong Service's Deployment Checklist

## Issue: A Deployment-Safety Agent That Retrieves the Applicable Pre-Deploy Safety Checklist by Semantic Similarity Over the Service's Name and Description Pulls a Lexically Similar but Substantively Different Checklist -- One Written for a Stateless Service -- When Deploying a Stateful Service, Omitting a Required Migration-Compatibility Gate

**Frequency**: Occasional

**Symptoms**
- A stateful service's deploy proceeds using a checklist that includes no schema-migration-compatibility gate, even though the organization maintains a separate, correct checklist specifically for stateful services with such a gate
- The retrieved checklist's title and structure closely resemble the correct one (both are "Standard Service Deploy Checklist" variants), differing mainly in a section the stateless-service version omits entirely
- Re-running the same retrieval query with the service's `stateful: true` tag included as an explicit filter (rather than relying on description-text similarity alone) returns the correct checklist, isolating the failure to retrieval scope rather than the correct checklist being absent from the library
- The mismatch concentrates on newer services whose description text most closely resembles an existing stateless-service template, since checklist retrieval favors the most textually similar past entry regardless of the structural difference that actually matters
- A deploy that skips the migration-compatibility gate succeeds at the artifact level but causes a schema-incompatibility incident shortly after, traced back to the wrong checklist having been applied

**Root Cause**
The checklist-retrieval step selects a checklist by semantic similarity over the service's name and free-text description rather than by a structured `stateful` or `service_class` attribute, so two checklists with highly similar prose (both describing a generic "deploy review") can sit close together in embedding space despite one being missing a section that is only relevant for stateful services. The agent has no signal distinguishing "describes a similar-sounding deploy process" from "is the checklist that actually applies to this service's structural class," because retrieval never constrains the candidate set by that structural attribute before ranking by similarity.

**Example**
```
New service "order-ledger-service" is described in its service catalog entry as "Handles order state transitions and persists ledger records to a relational store"
Deployment-safety agent retrieves the pre-deploy checklist by semantic similarity over this description, returning the highest-scoring match: "Standard Service Deploy Checklist," originally written for a stateless API gateway service, which does not include a migration-compatibility gate
The correct checklist, "Stateful Service Deploy Checklist," exists in the library and includes the migration-compatibility gate, but scored lower on semantic similarity due to differences in its description's phrasing
Deploy proceeds using the stateless checklist; a schema change included in the deploy is not checked for backward compatibility
Previous-version service instances querying the changed schema during the rollout window begin failing, an incident traced back to the missing migration-compatibility gate from the wrong checklist
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM orchestration for incident and deployment workflows is evaluated specifically against deterministic, structured decision support, underscoring that similarity-based template selection without structured constraints is a known gap | [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755) |
| Retrieval reliability research finds that semantically similar but substantively different documents are frequently confused by similarity-only retrieval when structured filtering is unavailable | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Automated infrastructure-reconciliation research on AI agents highlights template- and checklist-selection mismatch as a recurring class of automation failure in deployment pipelines | [Automated Cloud Infrastructure-as-Code Reconciliation with AI Agents](https://arxiv.org/pdf/2510.20211) |

**Contributing Factors**
- Checklist retrieval ranks candidates by free-text semantic similarity over service description without first filtering by a structured `stateful` or `service_class` attribute
- Checklist library contains multiple variants with highly similar prose structure, maximizing embedding-space proximity between checklists that differ in one structurally important section
- No automated check compares the retrieved checklist's applicable service-class tag against the deploying service's actual structural attributes before the deploy proceeds

---

## Mitigation Strategies

1. **Structured Service-Class Filter Before Semantic Ranking**: Require checklist retrieval to filter candidates by the deploying service's structured attributes (stateful/stateless, data-store dependencies) before ranking by semantic similarity over description text
2. **Checklist-to-Service-Class Verification Gate**: Before a deploy proceeds, automatically verify the selected checklist's tagged applicability matches the deploying service's structural attributes, and block the deploy if they do not match
3. **Mandatory Migration-Compatibility Section for Any Service With a Data-Store Dependency**: Independent of which checklist is retrieved, require any service tagged as having a data-store dependency to pass a migration-compatibility gate before deploy, as a structural backstop against checklist-selection errors
4. **Checklist Selection Audit on New Services**: For any newly onboarded service, require a one-time manual confirmation that the automatically selected checklist matches the service's actual structural class before automated checklist selection is trusted for subsequent deploys

### Metrics
- Rate of deploys where the selected checklist's tagged service-class does not match the deploying service's structural attributes
- Number of incidents traced back to a missing checklist section attributable to wrong-checklist selection
- Percentage of newly onboarded services with a manually confirmed checklist-selection audit on file

### Alerts
- A deploy proceeds using a checklist whose tagged service-class does not match the deploying service's structural attributes → P1
- A service tagged with a data-store dependency deploys without a migration-compatibility gate having run → P1
- Checklist-selection mismatch rate across deploys exceeds baseline for two consecutive reporting periods → P2

---

## Related Patterns

- [Semantic Similarity Retrieval Misses Structural Attributes (by-capability)](../../../../../by-capability/knowledge-retrieval/goals/retrieval-relevance/failures/semantic-similarity-retrieval-misses-structural-attributes.md) - the general mechanism behind this deployment-safety-specific instance

## References

- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [Automated Cloud Infrastructure-as-Code Reconciliation with AI Agents](https://arxiv.org/pdf/2510.20211)
