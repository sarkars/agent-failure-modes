# Data Classification Access Not Enforced

## Issue
Records or fields are tagged with a sensitivity classification (e.g., `public`, `internal`, `confidential`, `restricted`) in the data catalog, but the tool-serving layer the agent calls through doesn't actually check that classification before returning results. The classification exists as documentation and governance metadata, not as a runtime enforcement rule, so an agent with generic tool access retrieves `restricted`-tagged data exactly as easily as `public`-tagged data.

**Frequency**: Common

**Symptoms**
- Agent returns documents or fields labeled "confidential" or "restricted" in the same response format as public data, with no visible distinction
- Data-loss-prevention (DLP) scans flag agent output containing classified content that should have been filtered before reaching the agent
- Classification labels exist in the metadata store but the tool's query/response path never references them
- Different tools accessing the same underlying dataset enforce classification inconsistently — one respects it, another doesn't
- Post-incident review finds the classification schema was implemented for human-facing dashboards but never extended to the agent tool layer

## Root Cause
Classification schemes are frequently built and maintained by a data-governance or compliance function that owns the tagging process, while the tool/API layer agents call through is built and maintained separately by a platform or product engineering team. Without an explicit contract requiring every read path to consult the classification tag at query time, the two systems drift apart: the tags are correct and current, but nothing in the request path actually looks at them before serving a response.

## Example
```
A document-search tool indexes all internal wikis and file shares,
including HR policy documents (classified "internal") and a small set
of pending-litigation legal memos (classified "restricted", intended
only for the legal team). The search index stores the classification
tag alongside each document but the search tool's ranking and retrieval
pipeline was built purely for relevance — it never filters or checks
the tag.

A general-purpose research agent, asked by an employee to "find
everything about the recent product recall," issues a broad semantic
search against the index. The restricted legal memos rank highly for
relevance and are returned in the agent's synthesized answer, exposing
litigation strategy to an employee with no legal-hold clearance, purely
because the retrieval path never consulted the classification field
that was sitting right next to the content the whole time.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large share of data-classification programs report incomplete enforcement coverage across all systems that read the classified data, with newer tool/API layers lagging furthest behind | Common finding in enterprise data-governance maturity assessments |
| Search and retrieval tools (as opposed to direct record-lookup APIs) are disproportionately represented in classification-enforcement gaps, since relevance ranking pipelines are rarely built with a filtering hook | Typical of retrieval-augmented agent architectures |
| Incidents involving classified-but-unfiltered content are frequently traced to a new tool or index being stood up without inheriting the enforcement logic of the original system | Common root cause in agent-tooling rollouts |

## Mitigations
1. **Classification as a mandatory query filter, not metadata**: Require every read path (search, direct lookup, export) to apply a classification filter as a non-optional stage of query execution, enforced by a shared middleware layer rather than reimplemented per tool.
2. **Classification-aware indexing**: Bake the classification tag into the index/storage layer itself (e.g., separate indices or partitions per classification tier) so a retrieval bug can't accidentally surface restricted content — the restricted content simply isn't in the queried index.
3. **Requester clearance mapping**: Maintain an explicit mapping from agent/requester identity to the maximum classification tier it's permitted to retrieve, and reject or redact any result exceeding that tier at the tool boundary.
4. **Cross-tool enforcement audits**: Periodically test every tool that reads from a classified dataset with synthetic restricted-tier content and confirm each one filters it correctly, rather than assuming enforcement inherited from one tool applies to all.
5. **Fail-closed on missing classification metadata**: If a record has no classification tag at all, treat it as the most restrictive tier by default rather than assuming it's safe to return.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `classified_content_unfiltered_returns` | Count of tool responses containing content tagged above the requester's clearance tier | Alert threshold: > 0 (any occurrence) |
| `enforcement_coverage_ratio` | Share of tools reading from classified datasets that have verified, tested classification filtering | Alert threshold: < 100% for any dataset with a restricted tier |
| `untagged_record_serve_rate` | Rate at which records with no classification tag are served through agent tools | Alert threshold: > 1% of served records |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Restricted Content Surfaced | A tool response includes content classified above the requester's verified clearance | P1 | Halt the tool, notify data-governance and security, review blast radius |
| New Tool Missing Enforcement | A newly deployed tool reads from a classified dataset without a registered enforcement check | P2 | Block production rollout until the classification filter is verified |

## Related Patterns
- [Sensitive Field Access Not Restricted](./sensitive-field-access-not-restricted.md) - a narrower case where the classification is field-level rather than record/document-level
- [Field-Level Access Not Restricted](./field-level-access-not-restricted.md) - both describe access controls that exist in policy but aren't wired into the serving path
- [Geographic Data Access Restriction](./geographic-data-access-restriction.md) - a specific instance of classification-style restriction (residency) not being enforced
