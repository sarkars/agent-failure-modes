# Data Deletion Compliance

## Issue
A user or data-subject deletion request (e.g. a GDPR/CCPA erasure request) is supposed to propagate through every tool, cache, vector store, and downstream system the agent has ever written that person's data to. In practice, the agent's deletion logic only reaches the primary data store it knows about, missing copies written to secondary systems — search indexes, embedding/vector stores, analytics warehouses, third-party tool integrations, or logs — that the agent wrote to during normal operation but that the deletion workflow was never extended to cover.

**Frequency**: Common

**Symptoms**
- A deletion request completes successfully against the primary database but the subject's data still appears in search results, recommendation outputs, or RAG retrieval a week later
- The agent's deletion tool only knows about the systems that existed when it was first built, not every downstream store subsequently added
- Vector embeddings derived from a user's data remain in the vector store after the source record is deleted, because embeddings were never treated as "the user's data" by the deletion workflow
- Third-party integrations the agent writes to (a CRM, a support-ticket system, an email marketing tool) retain the data because the deletion tool has no corresponding delete call for that integration
- No verification step confirms deletion actually completed across all known stores before marking the request "done"

## Root Cause
Data written by an agent frequently fans out across multiple systems as a side effect of normal operation — a customer record gets cached, indexed for search, embedded into a vector store for RAG, summarized into an analytics table, and forwarded to third-party tools — but the deletion workflow is usually built against a mental model of "the database," not a complete, maintained inventory of every store the agent has ever written to. As new tools and integrations are added over time, deletion logic isn't automatically extended to cover them, so the set of "systems we delete from" silently falls behind the set of "systems we write to."

## Example
```
1. A support agent handles customer conversations, storing conversation transcripts in a primary database
   and also generating vector embeddings of each transcript for a semantic-search tool used to find
   similar past tickets.
2. A customer submits a data-erasure request. The deletion workflow, built when the agent only wrote to
   the primary database, deletes the transcript rows successfully.
3. The vector embeddings generated from those transcripts were never included in the deletion workflow's
   scope, because the semantic-search feature was added later by a different team without updating the
   deletion tool's list of systems to purge.
4. The customer's conversation content, including personal details, remains retrievable through the
   semantic-search tool's embedding store indefinitely.
5. A compliance audit later discovers the customer's data is still retrievable months after their erasure
   request was marked complete, constituting a compliance violation.
```

## Statistics
| Finding | Context |
|---------|---------|
| Deletion requests are commonly found, on audit, to leave data behind in at least one downstream or derived store (caches, search indexes, vector stores, analytics) | Common finding in data-subject-request compliance audits |
| Vector/embedding stores are disproportionately missed by deletion workflows relative to primary relational data stores | Typical pattern as RAG and semantic-search features are added to existing agent systems |
| Maintaining an explicit, automatically-enforced data-flow inventory closes most deletion-completeness gaps | Standard remediation for erasure-compliance findings |

## Mitigations
1. **Maintain a live data-flow inventory of every store the agent writes to**: Require every new tool or integration that writes personal data to register itself in a central inventory that the deletion workflow consults, rather than hand-maintaining a deletion checklist.
2. **Tag writes with a subject identifier at write time**: Propagate a consistent subject/user ID through every downstream write (including derived data like embeddings and cache entries) so a deletion job can query "everything tagged with this subject" across all registered stores.
3. **Verify deletion completion across all registered stores before closing the request**: Have the deletion workflow query each registered store post-deletion to confirm no matching records remain, rather than assuming success once the primary delete call returns.
4. **Include derived/computed data explicitly in deletion scope**: Treat embeddings, summaries, cached aggregates, and search-index entries derived from personal data as subject to the same deletion obligation as the source record.
5. **Extend deletion workflows automatically when new integrations are added**: Make registering a deletion hook a required step in the review checklist for any new tool or third-party integration that writes personal data.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| deletion_request_incomplete_stores | Registered data stores where a subject's data still exists after a deletion request was marked complete | > 0 |
| unregistered_pii_writing_tools | Tools observed writing personal data that aren't registered in the deletion-scope inventory | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Deletion verification failure | Post-deletion verification finds subject data remaining in a registered store | Critical | Reopen the deletion request, purge the remaining data, notify compliance of the delay |
| New PII-writing tool unregistered | A tool writes personal data without a corresponding entry in the deletion-scope inventory | High | Block further writes from that tool until it's registered with a deletion hook |

## Related Patterns
- [PII Retention Policy Violation](./pii-retention-policy-violation.md) - both concern personal data persisting beyond the point it should have been removed, via retention expiry versus incomplete deletion propagation
- [Data Residency Violation](./data-residency-violation.md) - both stem from an incomplete inventory of where the agent's data actually ends up across downstream systems
- [Audit Retention Policy](./audit-retention-policy.md) - the inverse compliance risk: retaining audit records too briefly versus retaining personal data too long
