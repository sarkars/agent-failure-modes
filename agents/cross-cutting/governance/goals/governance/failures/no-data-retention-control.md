# No Data Retention Control

## Issue: Agent stores sensitive data unnecessarily.

**Frequency**: Common

**Symptoms**
- Unneeded PII in memory/logs/vector DB.
- Vector database embeddings retain PII from conversations that ended months ago, with no mechanism to purge them.
- A data subject access/deletion request cannot be fully honored because sensitive data has propagated into logs, caches, and memory stores outside the primary record.
- Storage costs and breach exposure grow silently as the agent accumulates data it never needed past the original interaction.

**Root Cause**
Agent stores sensitive data unnecessarily.

**Example**
```
A customer service agent stores full conversation transcripts, including
uploaded ID photos and account numbers, in a vector database to power
"similar past conversation" retrieval for future support tickets.

No TTL or classification tag is applied at ingestion. Eight months
later, the company receives a GDPR deletion request from a customer who
closed their account. Engineering discovers the customer's PII is
embedded across the vector index, the conversation logs, and a debug
cache used by the support dashboard — three separate locations no one
had inventoried.

The deletion request takes three weeks to fully honor instead of
comfortably meeting the required 30-day compliance window, and the
vector index has to be partially rebuilt to purge the embedded vectors.
```

**Contributing Factors**
- Data ingestion pipelines store data by default rather than requiring explicit justification for each stored field.
- No TTL or expiry is attached to records at write time, so data persists indefinitely absent manual cleanup.
- Sensitive data propagates into secondary stores (caches, embeddings, debug logs) that aren't covered by the primary system's retention policy.
- No classification step distinguishes PII/sensitive fields from routine operational data before storage.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Ingestion-time minimization | Raw input containing PII fields not needed for the task | Only necessary fields are persisted; PII is stripped/redacted | Unneeded PII fields are stored unmodified |
| TTL enforcement | A record reaches its TTL expiry | Record is automatically deleted | Record remains queryable past TTL expiry |
| Cross-store deletion propagation | A deletion request for a given user | User's data is removed from all stores (primary, cache, vector index) | Data remains in a secondary store after "successful" deletion |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| ingestion_minimization_rate | 100% | Feed test inputs with known extraneous PII and verify only necessary fields are persisted |
| ttl_deletion_success_rate | 100% | Seed records with short TTLs and verify all are purged on schedule |
| cross_store_deletion_completeness | 100% | Issue a test deletion request and scan all known stores to confirm no residual copies remain |

---

## Mitigation Strategies

### Prevention
1. **Data Minimization at Ingestion**: Define, per agent and per data source, exactly which fields are necessary for the task and strip or redact everything else (PII, secrets, free-text notes) before it enters memory, logs, or a vector store. Enforce this with a schema-based filter at the ingestion boundary rather than relying on the agent to self-censor.
2. **Retention-by-Default Expiry**: Tag every stored record (conversation memory, embeddings, cached tool outputs) with a TTL at write time based on a data classification policy (e.g., transient session data expires in 24h, PII in long-term memory expires in 30 days unless a legal hold applies). Storage systems auto-delete on TTL expiry rather than requiring manual cleanup.
3. **Purpose-Bound Storage Approval**: Require any new persistent storage of sensitive data (adding a field to long-term memory, a new vector index) to be justified against a specific downstream use case and approved by a data owner before it ships, closing off "store it in case we need it later" defaults.

### Detection & Response
1. **PII Discovery Scanning**: Run periodic scans (regex/NER-based PII detectors) across memory stores, logs, and vector databases to find sensitive data that shouldn't be there per the data classification policy, independent of whether it was tagged correctly at ingestion.
2. **Retention Violation Alerts**: Monitor for records past their TTL that were not deleted (deletion job failure, TTL not applied) and for records containing PII with no TTL set at all, both of which indicate the minimization/expiry controls were bypassed.
3. **Storage Growth Anomaly Detection**: Track growth rate of memory/vector/log stores per agent; a sudden increase in stored volume without a corresponding increase in legitimate use cases can indicate the agent is retaining more than intended.

### Architecture Patterns
1. **Data Classification Tagging Pipeline**: Route all data the agent stores through a classification step (rule-based or ML-based PII/sensitivity classifier) that attaches a retention tag before it reaches persistent storage, so downstream systems can enforce TTL and access policy based on that tag.
2. **TTL-Enforced Storage Layer**: Use storage backends with native TTL/expiry support (e.g., TTL indexes in the document store, lifecycle policies on object storage, scheduled purge jobs for the vector DB) so deletion is enforced by infrastructure, not agent behavior.
3. **Redaction Proxy for Logging**: Insert a redaction layer between the agent and the logging/observability pipeline that strips or masks sensitive fields before they're written to logs, so debugging visibility doesn't become a second, unmanaged copy of the sensitive data.

### Metrics
1. **untagged_sensitive_record_count**: Target: 0; Alert threshold: > 0 PII records without a retention tag
2. **ttl_enforcement_compliance_percent**: Target: 100% of records deleted within 24h of TTL expiry; Alert threshold: < 99%
3. **pii_discovery_scan_hit_rate**: Target: 0 unexpected PII hits per scan; Alert threshold: > 0
4. **storage_growth_rate_deviation_percent**: Target: within 10% of expected baseline; Alert threshold: > 25% deviation

### Alerts
1. **Unclassified PII Detected in Storage** (P1 - Critical): Condition - PII scan finds sensitive data with no retention tag or classification. Action: Quarantine the affected store/index, trigger emergency retention review, notify privacy/compliance.
2. **TTL Deletion Job Failure** (P2 - Warning): Condition - scheduled purge job fails or leaves expired records undeleted. Action: Re-run purge job, alert data platform on-call, verify no downstream leak occurred.
3. **Anomalous Storage Growth** (P3 - Info): Condition - stored data volume for an agent grows beyond expected baseline deviation. Action: Investigate ingestion pipeline for scope creep, review against purpose-bound storage approvals.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| untagged_sensitive_record_count | > 0 PII records without a retention tag |
| ttl_enforcement_compliance_percent | < 99% |
| pii_discovery_scan_hit_rate | > 0 unexpected PII hits per scan |
| storage_growth_rate_deviation_percent | > 25% deviation |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unclassified PII Detected in Storage | PII scan finds sensitive data with no retention tag or classification | Critical |
| TTL Deletion Job Failure | Scheduled purge job fails or leaves expired records undeleted | Warning |
| Anomalous Storage Growth | Stored data volume for an agent grows beyond expected baseline deviation | Info |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
