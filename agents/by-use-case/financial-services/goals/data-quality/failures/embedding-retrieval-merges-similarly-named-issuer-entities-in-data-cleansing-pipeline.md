# Embedding Retrieval Merges Similarly Named Issuer Entities in Data-Cleansing Pipeline

## Issue: A Data-Quality Agent Deduplicating Issuer Records Across Multiple Source Feeds Using Embedding Similarity Over Issuer Names, Rather Than Matching on a Unique Identifier Such as LEI or CUSIP Issuer Code, Merges Two Distinct Issuer Entities With Coincidentally Similar Names Into a Single Record, Corrupting Downstream Holdings and Exposure Calculations

**Frequency**: Occasional

**Symptoms**
- A holdings or exposure report aggregates positions from two genuinely distinct issuers under a single merged issuer record, because their names are highly similar across source feeds
- Querying either source feed by LEI or another unique issuer identifier shows the two issuers have different identifiers and no actual corporate relationship
- The merge concentrates on issuer name patterns that recur across unrelated entities -- common regional naming conventions, generic holding-company names, or issuers that share a name root after a corporate restructuring of one but not the other
- The merged record presents combined holdings and exposure figures with the same confidence and formatting as a correctly deduplicated record, with no indication the merge was based on name similarity rather than identifier confirmation
- The error surfaces only when a risk or compliance reviewer notices an exposure concentration that does not reconcile with either issuer's actual standalone position, prompting a manual identifier-level investigation

**Root Cause**
Deduplicating issuer records across heterogeneous source feeds by matching names via embedding similarity optimizes for the most textually similar name across feeds, not for confirming that two records share the same unique identifier or documented corporate relationship. When two genuinely distinct issuers happen to share a highly similar name -- common in sectors with generic naming conventions or after one issuer's corporate restructuring leaves a name resembling an unrelated entity -- the similarity signal driving the merge does not distinguish a coincidental match from a true cross-feed reference to the same legal entity.

**Example**
```
Data-quality agent reconciles issuer records from a custodian feed and a third-party reference-data feed for an emerging-markets bond portfolio
Custodian feed lists "Northbridge Energy Holdings Ltd"; reference-data feed separately lists "Northbridge Energy Ltd," a distinct, unrelated issuer with a different LEI and no corporate relationship to the first
Agent's embedding-similarity matching merges the two records into a single issuer entry based on name similarity alone
Combined exposure report shows a single issuer position that breaches the portfolio's single-issuer concentration limit, when neither underlying issuer individually breaches it
Risk reviewer flags the apparent breach, only to discover on identifier-level investigation that the two distinct issuers were incorrectly merged
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based matching systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically or lexically similar but substantively unrelated record when similarity search is used in place of identifier-based lookup | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify entity disambiguation across heterogeneous data sources as a distinct reliability challenge from single-source retrieval accuracy | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies entity-identity resolution as a distinct reliability requirement separate from the accuracy of downstream financial calculations | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- Issuer deduplication across source feeds is performed via name similarity rather than LEI, CUSIP issuer code, or another unique identifier
- No validation step confirms a matched pair of records shares a unique identifier or a documented corporate relationship before they are merged into a single issuer entity
- Sectors or regions with high issuer name-collision rates are not flagged for mandatory identifier-based verification before similarity matching is trusted

---

## Mitigation Strategies

1. **Identifier-Based Matching as Primary Path**: Require issuer deduplication to match on LEI, CUSIP issuer code, or another unique identifier first, falling back to name similarity only when no identifier is available in either source, and flagging that fallback explicitly
2. **Mandatory Identifier Confirmation Before Merge**: Before merging two issuer records into a single entity, require confirmation that both records share a unique identifier or a documented corporate-relationship filing, rather than merging on name similarity alone
3. **High-Collision Naming-Pattern Flagging**: Maintain a list of naming patterns and sectors with known high issuer name-collision rates and require any merge in those contexts to undergo mandatory secondary verification
4. **Surface Merge Method in Output**: Require any merged issuer record used in exposure or concentration reporting to indicate whether the merge was established by identifier match or by name similarity, so risk reviewers can prioritize verification of similarity-based merges

### Metrics
- Rate of merged issuer records whose merge was established by name similarity rather than identifier match
- Rate of similarity-matched merges that fail an identifier-based verification check when audited
- Number of concentration-limit alerts later found to be false positives due to an issuer-merge error

### Alerts
- A merged issuer record used in a concentration-limit calculation has no identifier-based confirmation of the merge → P1
- A similarity-matched merge fails identifier verification on audit after being used in a finalized report → P1
- Similarity-match fallback rate for issuer deduplication exceeds the defined threshold for a rolling window → P2

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
