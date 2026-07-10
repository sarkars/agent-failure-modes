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

### Prevention

1. **Enforce identifier-primary entity matching with fallback detection**: Implement entity resolution pipeline: (1) All entity matches must first attempt lookup via registration number/tax ID/LEI against authoritative registry (SEC EDGAR, national business registries, Refinitiv/FactSet), (2) Only if no identifier match found, apply semantic similarity scoring as secondary signal, (3) Require explicit user confirmation before including any similarity-matched entity, (4) Flag all similarity-matched entities with confidence metadata in structure chart, (5) Maintain audit trail: {matched_entity, match_method, confidence_score, override_reason}. Root cause mitigation: Prevents false positives by enforcing identifier-first methodology rather than similarity-first.

2. **High-collision jurisdiction/industry flagging with mandatory verification gates**: Build registry of high-collision-risk contexts: (a) jurisdictions with common naming conventions (e.g., Hong Kong holding companies), (b) industries with generic terms (e.g., "Holdings", "Capital", "Partners"), (c) multi-national subsidiary families where different countries use similar names. For any entity match in flagged contexts, require: secondary verification step (look up in alternative registry), document approval from compliance/legal reviewer before chart inclusion, cross-reference against filed ownership disclosures for contradictions. Root cause: Prevents matching based solely on similarity in high-risk scenarios.

3. **Ownership-filing validation before structure-chart inclusion**: Before adding any entity link to chart, require corroborating ownership filing from at least one independent source: (a) Specific SEC 13D/13G/Schedule 13A filing naming the relationship, (b) Foreign registry deed/certificate of incorporation naming parent, (c) UCC liens or financing statements naming control relationship, (d) Bankruptcy filings or creditor lists showing ownership. Match required filing document ID and effective date. If filing unavailable, mark entity as "[UNVERIFIED - no filed ownership document found]" and escalate to analyst. Root cause: Ensures relationships are documented, not inferred.

### Detection & Response

1. **Entity match audit logging with verification signals**: For each entity link in structure chart, capture: entity name, target company, match method (identifier vs. similarity), match confidence score (0-1.0), corroborating ownership filing (yes/no, document ID), analyst override (yes/no, reason), effective date. Alert if: >10% of chart entities linked via similarity only (no identifier confirmation), >1 entity per chart failed verification audit, entity linked without corroborating filing. Monitor weekly: audit random 10% of finalized charts; validate each link against alternative data sources (alternative registry lookups, document re-verification).

2. **Post-chart discovery reconciliation on new filings**: When new corporate filings received post-chart publication, parse for entity relationship data. If new filing contradicts previous chart (e.g., "this entity is not a subsidiary of target"), trigger automated chart audit: flag affected entities, re-run identifier-based matching, generate reconciliation report. Escalate to due-diligence team if contradiction affects material findings (e.g., liability exposure calculation).

### Architecture Patterns

1. **Entity Resolution Pipeline with Identifier-Priority Matching**: Ingestion → Parse Entity Names → Identifier Lookup (against SEC EDGAR, Refinitiv, national registries) → If match found, confirm via filing document → If no match, apply semantic similarity scoring with threshold (>0.85) → Require explicit verification/override → Add to chart with match metadata {entity_id, match_method, confidence, filing_doc_id}. Prevents similarity-only matches in primary path.

2. **High-Collision Jurisdiction Registry & Verification Gate**: Maintains curated list of high-collision contexts (e.g., "Hong Kong + Holding Company", "Singapore + Capital"). When entity matches in flagged context: (a) Cross-check against alternative registries (e.g., if EDGAR lookup succeeds but foreign subsidiary suspected, verify with foreign registration authority), (b) Flag for manual compliance review, (c) Require override confirmation before inclusion. Reduces false-positive family relationships.

3. **Ownership Filing Validator**: Searchable index of filed ownership documents (SEC 13D/13G, foreign deeds, UCC filings, corporate bylaws naming control). On entity link: query index for corroborating filing. If found, auto-confirm link + document ID. If not found, flag for analyst verification. Maintains audit trail of all lookup attempts.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Identifier Match Success Rate | >95% | <90% | # of entities matched via registration ID/LEI / total entity links in charts |
| Similarity-Only Fallback Rate | <5% | >10% | # of entities matched only via similarity (no identifier confirmation) / total chart entities |
| Corroborating Filing Coverage | 100% | <95% | # of entities with confirmed ownership filing / entities included in chart |
| Chart Audit Verification Rate | >99% | <98% | # of entities confirmed as legitimate on spot-check audit / audited entities |
| Post-Chart Reconciliation Discrepancies | <1% | >2% | # of entities found contradictory on later filings / total published chart entities |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unverified Entity Inclusion | Entity added to chart via similarity match with no corroborating ownership filing | CRITICAL | Block chart publication; require identifier verification or filing confirmation; re-analyze chart |
| High Similarity-Only Rate | >10% of entities in chart linked via similarity without identifier confirmation | HIGH | Audit entire chart; re-run identifier matching for all similarity-matched entities; reprioritize verification |
| Filing Contradiction Detected | Later filing contradicts entity relationship in published chart (entity claims non-subsidiary status) | HIGH | Escalate to due-diligence/compliance team; review any findings tied to contradicted entity; issue chart amendment if material |
| Collision Context Miss | Entity matched in high-collision jurisdiction without mandatory verification gate applied | MEDIUM | Log oversight; re-analyze entity link with secondary verification; update high-collision registry if jurisdiction pattern not previously captured |

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
