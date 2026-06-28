# Embedding Retrieval Surfaces Similarly Named, Unrelated Subsidiary in Corporate-Structure Chart

## Issue: A Due-Diligence Agent Building a Target Company's Corporate-Structure Chart From Filings and Registry Data, Using Semantic Similarity Search to Match Entity Names Across Documents, Merges or Links a Subsidiary Into the Target's Structure Based on Name Similarity Alone, When the Matched Entity Is in Fact an Unrelated Company With a Coincidentally Similar Name

**Frequency**: Occasional

**Symptoms**
- The generated corporate-structure chart includes a subsidiary or affiliate that does not actually belong to the target's ownership chain, linked there because its name closely resembles a genuine subsidiary's name
- Querying the entity registry directly by registration or tax ID, rather than by name similarity, shows the matched entity has no ownership or control relationship to the target
- The mismatch concentrates on common business name patterns -- regional naming conventions, generic descriptive names, or holding companies with near-identical names in different jurisdictions -- where many unrelated entities share highly similar names
- The structure chart presents the erroneous link with the same confidence and formatting as correctly verified relationships, with no indication that the link was established by name similarity rather than registry confirmation
- The error surfaces only when a reviewer cross-checks a specific entity against the target's actual filed ownership disclosures and finds no relationship recorded

**Root Cause**
Building a corporate-structure chart from heterogeneous filings and registry data by matching entity names via semantic or lexical similarity optimizes for the most textually similar name across sources, not for an entity confirmed to share the same registration identifier or a documented ownership relationship. When two genuinely unrelated entities happen to share a highly similar name -- common in jurisdictions with limited naming conventions or generic industry terms -- the similarity signal driving the match does not distinguish a coincidental match from a true cross-document reference to the same legal entity.

**Example**
```
Due-diligence agent compiles a corporate-structure chart for "Meridian Logistics Holdings" from a mix of SEC filings, a foreign companies registry, and a UCC lien database
Target's actual filings reference a subsidiary "Meridian Logistics Holdings (Asia) Pte Ltd"
Foreign registry separately lists an unrelated company "Meridian Logistics Pte Ltd," coincidentally similar in name but with a different registration number and no filed relationship to the target
Agent's name-similarity matching links the unrelated "Meridian Logistics Pte Ltd" into the target's structure chart as a subsidiary
Buyer's risk assessment, relying on the chart, flags exposure to a litigation matter actually involving the unrelated entity, while missing that the target's real Asia subsidiary carries a different, undisclosed liability
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically or lexically similar but substantively unrelated record when similarity search is used in place of identifier-based lookup | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Retrieval-augmented legal research systems are shown to require exact-identifier verification rather than similarity-based matching when assembling structured legal or corporate relationships from multiple source documents | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Knowledge-oriented retrieval-augmented generation surveys identify entity disambiguation across heterogeneous sources as a distinct reliability challenge from single-source retrieval accuracy | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |

**Contributing Factors**
- Entity matching across filings, registry data, and lien databases is performed via name similarity rather than registration number, tax ID, or other unique identifier
- No validation step confirms a matched entity shares a registration identifier or a documented ownership filing with the target before it is added to the structure chart
- Jurisdictions or industries with high naming-convention overlap are not flagged for mandatory identifier-based verification before similarity matching is trusted

---

## Mitigation Strategies

1. **Identifier-Based Matching as Primary Path**: Require entity linkage in the structure chart to be established by matching registration number, tax ID, or another unique identifier first, falling back to name similarity only when no identifier match exists, and flagging that fallback explicitly
2. **Mandatory Ownership-Filing Confirmation Before Chart Inclusion**: Before adding any entity to the structure chart, require confirmation that a specific ownership or control filing documents the relationship to the target, rather than including any name-similar entity by default
3. **High-Collision Naming-Pattern Flagging**: Maintain a list of jurisdictions and industry sectors with known high name-collision rates and require any entity match in those contexts to undergo mandatory secondary verification before inclusion
4. **Surface Match Method in Chart Output**: Require the structure chart to indicate, for each entity, whether the link was established by identifier match or by name similarity, so reviewers can prioritize verification of similarity-based links

### Metrics
- Rate of structure-chart entities whose link to the target was established by name similarity rather than identifier match
- Rate of similarity-matched entities that fail an identifier-based verification check when audited
- Number of due-diligence findings later found to be misattributed due to an entity-matching error

### Alerts
- A structure-chart entity is included with no identifier-based confirmation of its relationship to the target → P1
- A similarity-matched entity fails identifier verification on audit after being included in a finalized chart → P1
- Similarity-match fallback rate for entity linkage exceeds the defined threshold for a rolling window → P2

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
