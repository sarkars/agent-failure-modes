# PII Retention Policy Violation

## Issue
Personally identifiable information collected or processed by an agent through a tool call — a support transcript, a form submission, an uploaded document — is subject to a policy-defined maximum retention period, after which it's supposed to be automatically deleted or anonymized. No automated expiry mechanism actually enforces that period; the data simply persists in whatever store the tool wrote it to until someone manually notices and removes it, which in practice rarely or never happens.

**Frequency**: Very Common

**Symptoms**
- PII older than the policy-defined retention window is still present and queryable in production data stores
- The retention policy exists as a written document, but no scheduled job, TTL, or lifecycle rule implements it against the actual storage
- Different tools that collect the same category of PII (e.g. a chat tool and a form-upload tool) have inconsistent or absent retention enforcement, even though policy specifies one retention period for that data category
- New tools that collect PII are deployed without any retention/expiry configuration, because retention enforcement isn't part of the tool-deployment checklist
- A data-minimization or privacy audit finds PII records with creation timestamps far older than the policy's maximum retention period

## Root Cause
Retention policies are typically authored by a legal or privacy team as a document describing intent ("delete customer support PII after 24 months"), but implementing that intent requires an engineering mechanism — a database TTL, a scheduled deletion job, an object-storage lifecycle rule — configured against every store where that PII category actually lands. Because policy authorship and infrastructure implementation are separate workstreams with no enforced handoff, and because new tools are added over time without revisiting retention configuration, the gap between "policy says delete it" and "something actually deletes it" persists indefinitely unless specifically engineered closed.

## Example
```
1. Company privacy policy states that customer support chat transcripts, which may contain PII disclosed
   during a conversation, must be deleted or anonymized 24 months after the conversation ends.
2. The support agent's transcript-storage tool was built to durably store every conversation for quality
   and training purposes, with no expiry logic -- retention wasn't considered during the tool's design,
   only durability.
3. No scheduled job or lifecycle rule exists anywhere in the data pipeline to identify and remove
   transcripts older than 24 months.
4. Three years after launch, the transcript store contains every conversation ever handled by the agent,
   including PII from conversations that should have been deleted a year earlier under policy.
5. A privacy audit samples the transcript store, finds records well beyond the 24-month retention limit,
   and flags the organization as out of compliance with its own stated policy.
```

## Statistics
| Finding | Context |
|---------|---------|
| PII stored by newly-added agent tools frequently ships without any retention/expiry enforcement configured against the policy-defined period | Common finding in data-minimization and privacy audits |
| Retention policy documents commonly cover more data categories than have corresponding automated enforcement mechanisms in production | Typical gap identified in privacy-program maturity assessments |
| Implementing retention as an automated, storage-level TTL rather than a manual process closes the large majority of these violations | Standard remediation for retention-compliance findings |

## Mitigations
1. **Implement retention as an automated storage-level control**: Use database TTL fields, object-storage lifecycle rules, or scheduled deletion jobs tied directly to each PII category's policy-defined period, rather than relying on manual review.
2. **Tag data with its retention category and collection timestamp at write time**: Have every tool that writes PII record which retention category applies and when the clock started, so automated expiry logic can act on it without manual classification later.
3. **Require retention configuration as part of new-tool deployment review**: Add "what is this data's retention category and how is expiry enforced" as a mandatory question in the checklist for deploying any tool that collects PII.
4. **Reconcile actual data age against policy on a recurring schedule**: Run periodic audits querying for PII records older than their category's retention limit, independent of whether automated deletion is believed to be working.
5. **Anonymize rather than delete where retention conflicts with other requirements**: Where legal hold or analytics value conflicts with deletion, implement irreversible anonymization (stripping identifying fields) as a compliant alternative to outright deletion.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| pii_records_exceeding_retention_window | Count of PII records older than their category's policy-defined retention period | > 0 |
| pii_writing_tools_without_ttl | Tools that write PII with no configured expiry/TTL mechanism | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Retention window exceeded | Reconciliation audit finds PII records past their policy-defined retention limit | High | Trigger deletion/anonymization immediately, investigate why automated expiry didn't fire |
| PII-writing tool deployed without TTL | A new tool begins writing a PII category with no corresponding expiry configuration | High | Block further writes until a retention mechanism is configured |

## Related Patterns
- [Data Deletion Compliance](./data-deletion-compliance.md) - both concern personal data persisting beyond when it should be gone, via missed scheduled expiry versus incomplete request-driven deletion
- [Audit Retention Policy](./audit-retention-policy.md) - the inverse failure mode: records deleted too early rather than personal data retained too long
- [Data Residency Violation](./data-residency-violation.md) - both are data-governance requirements that must be enforced consistently across every tool that touches the data, not just the primary store
