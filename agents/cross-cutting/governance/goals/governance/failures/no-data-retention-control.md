# No Data Retention Control

## Issue: Agent stores sensitive data unnecessarily.

**Frequency**: Common

**Symptoms**
- Unneeded PII in memory/logs/vector DB.
- [Add more specific symptoms]

**Root Cause**
Agent stores sensitive data unnecessarily.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
