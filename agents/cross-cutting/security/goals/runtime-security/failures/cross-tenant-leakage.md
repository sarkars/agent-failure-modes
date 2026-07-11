# Cross-Tenant Data Leakage

## Issue: AI Agent Exposes Data Between Isolated Customer Environments

**Frequency**: Occasional

**Symptoms**
- Customer A sees Customer B's data in responses
- Shared context contains cross-tenant information
- Model responses reference other customers' specifics
- API keys or credentials from wrong tenant exposed
- Compliance violations from data mixing

**Root Cause**
Multi-tenant AI deployments share infrastructure for efficiency. When tenant isolation is incomplete—through shared model context, cached embeddings, or pooled tool connections—data from one tenant can leak into another tenant's sessions. This is especially dangerous in enterprise deployments where competitors may share the same AI infrastructure.

**Example**
```
Enterprise RAG Cross-Tenant Leak:

Setup:
- SaaS AI assistant serving multiple enterprise customers
- Shared vector database with tenant_id filtering
- Shared LLM inference endpoint

Failure scenario:
1. Customer A uploads confidential M&A documents
2. Documents embedded and stored with tenant_id="A"

3. Bug: Similarity search returns top-k globally, 
   then filters by tenant_id (wrong order)

4. Customer B asks: "What acquisitions are planned?"
5. System retrieves Customer A's M&A docs (high similarity)
   Then filters... but snippets already in context

6. Response to Customer B includes:
   "Based on the documents, there are plans to acquire 
    CompanyX for $500M in Q3..."
   
Impact:
- Confidential M&A plans leaked to competitor
- Regulatory violation (material non-public info)
- Customer trust destroyed
```

**Key Statistics**
From Security Research (2026):
- 61% of AI security incidents involved sensitive data exposure (CSA)
- Cross-tenant isolation failures in enterprise AI stacks documented
- Meta AI agent data exposure incident (April 2026)
- 82% of organizations discovered unknown AI agents accessing data

**Leakage Vectors**
| Vector | Mechanism | Detection Difficulty |
|--------|-----------|---------------------|
| Shared embedding cache | Similar queries return cached results | Hard |
| Context window bleed | Prior conversation persists | Medium |
| Shared model fine-tuning | Training data memorization | Very Hard |
| Connection pooling | DB connections shared between tenants | Medium |
| Log aggregation | Multi-tenant logs expose data | Easy |

**Contributing Factors**
- Cost optimization through shared infrastructure
- Tenant isolation as afterthought
- Filter-after-retrieve architectures
- Shared caching layers
- Insufficient testing of isolation boundaries

## Mitigation Strategies

### Prevention
1. **Filter-before-retrieve query construction**: Apply the tenant_id filter as part of the similarity-search query itself (restricting the candidate set before ranking) rather than running an unfiltered top-k search and filtering results afterward — the documented failure mode is specifically this "filter-after-retrieve" ordering, where high-similarity cross-tenant documents already entered the context before filtering removed them from the final response. Trade-off: tenant-scoped queries can be less efficient than a single global index if the vector database isn't optimized for filtered search, and require verifying every retrieval code path uses the correct query construction.
2. **Hard infrastructure isolation for high-sensitivity tenants**: For tenants with the highest sensitivity requirements (competitors sharing infrastructure, regulated industries), provision fully separate vector stores, caches, and potentially model deployment instances rather than relying solely on logical/filter-based isolation within shared infrastructure. Trade-off: significantly increases infrastructure cost and operational complexity versus shared multi-tenant infrastructure.
3. **Explicit context clearing between tenant sessions**: Ensure no residual context, cache entries, or embeddings from one tenant's session can persist into a subsequent session serving a different tenant, verified through automated testing rather than assumed from application logic. Trade-off: requires disciplined state-management across every layer that might retain data (model context, cache, connection pool) and adds overhead to session teardown.

### Detection & Response
1. **Response scanning for cross-tenant identifiers**: Scan outgoing responses for identifiers, names, or content patterns associated with a different tenant than the one being served, catching leakage that occurred despite retrieval-time filtering, since this is a documented failure mode where filtering order bugs let cross-tenant content into context before the tenant check ran.
2. **Similarity-search pattern monitoring across tenants**: Track retrieval patterns for anomalies such as unusually high cross-tenant similarity matches or queries that structurally resemble a filter-bypass, since these can indicate either a genuine architectural flaw or an active probing attempt.
3. **Regular penetration testing of tenant boundaries**: Conduct scheduled, adversarial testing specifically targeting tenant isolation (attempting to retrieve or infer another tenant's data through crafted queries) rather than relying solely on passive monitoring, since isolation bugs like the filter-order issue can persist undetected until specifically tested for.

### Architecture Patterns
1. **Tenant-scoped retrieval as a structural guarantee**: Architect the retrieval layer so tenant_id is a mandatory, non-optional parameter of the underlying query API itself (not an application-level filter that can be omitted or misordered), making the filter-before-retrieve pattern the only way to query the system at all.
2. **Tiered isolation architecture by sensitivity level**: Offer isolation tiers (shared infrastructure with strict logical isolation for standard tenants, dedicated infrastructure for high-sensitivity tenants) as an explicit architectural and commercial offering, rather than a uniform one-size-fits-all isolation model.
3. **Cross-tenant audit logging as a standing control**: Log every retrieval query with its tenant scope and the tenant scope of any results returned, enabling both real-time anomaly detection and forensic reconstruction if a leak is later discovered.

### Metrics
1. **cross_tenant_retrieval_rate**: Target: 0% of retrieved documents belong to a tenant other than the requester; Alert on any occurrence
2. **filter_order_audit_pass_rate**: Target: 100% of retrieval code paths verified to filter-before-retrieve; Alert on any code path found to filter-after-retrieve
3. **cross_tenant_identifier_in_response_rate**: Target: 0%; Alert on any occurrence
4. **penetration_test_finding_rate**: Target: 0 critical tenant-isolation findings per test cycle; Alert on any critical finding

### Alerts
1. **Cross-Tenant Data in Response** (P1): Condition - a response to one tenant is found to contain another tenant's data. Action: Treat as a confirmed critical incident, notify affected tenants per contractual/regulatory breach obligations, halt the responsible retrieval path immediately.
2. **Filter-After-Retrieve Pattern Found** (P1): Condition - code audit or testing finds a retrieval path that filters by tenant after (not before) the similarity search. Action: Fix immediately as a P1 defect; treat as a confirmed vulnerability even absent evidence of actual exploitation.
3. **Penetration Test Critical Finding** (P1): Condition - scheduled penetration testing finds a way to access or infer another tenant's data. Action: Remediate before the next production deployment; treat findings as blocking release.

## References

- [CSA Report April 2026](https://cloudsecurityalliance.org/) - 61% sensitive data exposure
- [Foresiet: AI Security Incidents April 2026](https://foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/) - Meta AI exposure
- [VentureBeat: 88% Enterprises Breached](https://venturebeat.com/security/most-enterprises-cant-stop-stage-three-ai-agent-threats-venturebeat-survey-finds/) - Enterprise AI security
- [Kiteworks: AI Agent Security Incidents 2026](https://www.kiteworks.com/cybersecurity-risk-management/ai-agent-security-incidents-2026/) - Enterprise survey
