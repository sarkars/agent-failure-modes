# Temporal Relevance Failure

## Issue: Retrieved Content Is Outdated or Superseded

**Frequency**: Common

**Symptoms**
- System cites overruled precedent or repealed statutes
- Answers based on old versions of documents
- Retrieved content was accurate at time of indexing but no longer valid
- Users receive legally or factually incorrect guidance
- No indication that cited sources may be outdated

**Root Cause**
RAG systems retrieve documents based on semantic similarity without considering temporal validity. In domains like law, medicine, and policy where information is regularly superseded, retrieving technically relevant but outdated content leads to dangerously incorrect answers.

**Example**
```
Query: "What constitutional standard protects abortion rights?"

Retrieval: Planned Parenthood v. Casey, 505 U.S. 833 (1992)
          Roe v. Wade, 410 U.S. 113 (1973)

RAG Response:
"The undue burden standard from Casey protects abortion rights.
Under this framework, regulations cannot place a substantial
obstacle in the path of a woman seeking an abortion."

Problem:
- Both Roe and Casey were OVERRULED in June 2022
- Dobbs v. Jackson Women's Health Organization changed the law
- RAG system has no awareness of subsequent legal developments
- Semantic similarity found "relevant" but superseded content

Result: User receives categorically incorrect legal information
        that could lead to serious harm
```

**Key Statistics**
From Stanford Legal RAG Hallucinations Study (2025):
- Legal RAG tools hallucinate 17-33% of the time
- Temporal issues are a distinct category of hallucination
- Particularly problematic in rapidly evolving legal areas
- Standard citation checking (does source exist?) misses this failure

**Temporal Failure Types**
- **Overruled precedent**: Court decisions superseded by later rulings
- **Repealed statutes**: Laws no longer in effect
- **Amended regulations**: Rules changed since indexing
- **Superseded guidance**: Agency guidance withdrawn or updated
- **Stale facts**: Factual information that has changed

**Affected Domains**
| Domain | Temporal Challenge |
|--------|-------------------|
| Law | Overruled cases, repealed statutes |
| Medicine | Superseded clinical guidelines |
| Tax | Annual code changes |
| Technology | Deprecated APIs, changed behavior |
| Policy | Updated regulations, new requirements |

**Contributing Factors**
- Embedding models don't encode temporal relationships
- Knowledge base indexes point-in-time snapshots
- No integration with "good law" checking services
- Retrieval doesn't weight recency appropriately
- Users can't easily see document dates

## Mitigation Strategies

### Prevention
1. **Supersession-Graph-Aware Retrieval**: Maintain an explicit graph of which documents/precedents have been overruled, repealed, or amended, and exclude or heavily demote superseded nodes from retrieval by default — directly targeting the Roe/Casey-overruled-by-Dobbs failure, where semantic similarity alone can't detect supersession.
2. **Integration With Authoritative Currency-Checking Services**: For legal domains, integrate citation validation services (Shepard's, KeyCite, or equivalent regulatory-currency APIs) as a mandatory post-retrieval filter step, since standard citation-existence checks miss the "still good law" question entirely.
3. **Recency-Weighted Retrieval Scoring**: Incorporate document effective date and last-confirmed-current timestamp as an explicit ranking feature, so even without a complete supersession graph, more recent authoritative sources are preferred over older ones discussing the same doctrine.

### Detection & Response
1. **Expert Currency-Review Sampling**: Route a sample of legal/medical/policy answers to domain experts specifically to check whether cited sources are still current, not just whether they exist — the review needed since normal citation checks miss temporal supersession.
2. **Currency-Service Cross-Check Logging**: Log every case where a citation validation service flags a retrieved source as overruled, repealed, or withdrawn, and treat any such case reaching the user as a critical incident given the risk of serious harm noted in the file.
3. **User-Reported "This Changed" Correction Tracking**: Track and trend user corrections indicating the law/policy/guideline has changed since the cited source, feeding directly into supersession-graph maintenance priorities.

### Architecture Patterns
1. **Point-in-Time Knowledge Graph With Supersession Edges**: Model each authoritative source as a node with explicit "superseded_by" edges; retrieval resolves to the current authoritative node in the chain, and any older node is only surfaced with an explicit historical-context disclaimer.
2. **Mandatory Staleness Disclaimer Generation**: Require the answer generator to state the retrieval/index date and explicitly flag domains (law, medicine, tax) where currency cannot be fully guaranteed, rather than presenting retrieved content as unconditionally current.
3. **Continuous Authoritative-Source Reindexing Pipeline**: For high-stakes domains, run a dedicated pipeline that ingests supersession/repeal/amendment notices from official sources (court dockets, federal register, regulatory bulletins) and propagates them into the retrieval index faster than general corpus reindexing cycles.

### Metrics
1. **supersession_graph_coverage_percent**: Target: > 95% of legal/policy corpus mapped; Alert threshold: < 85%
2. **overruled_source_retrieval_rate**: Target: 0%; Alert threshold: any nonzero occurrence
3. **currency_service_flag_rate**: Target: < 1% of legal queries; Alert threshold: > 3%
4. **expert_audit_temporal_error_rate**: Target: < 2%; Alert threshold: > 5%

### Alerts
1. **Overruled Source Surfaced** (P1): Condition - a document flagged by the currency-checking service as overruled/repealed appears in a synthesized answer. Action: immediately purge from the active index, issue a correction if already delivered to a user, audit the supersession graph gap.
2. **Currency Service Integration Failure** (P1): Condition - the currency-check step fails or times out and retrieval proceeds without it. Action: fail closed (block synthesis) rather than fail open, page on-call.
3. **Expert Audit Temporal Error Spike** (P2): Condition - expert_audit_temporal_error_rate exceeds 5% in a review cycle. Action: prioritize supersession-graph backfill for the affected domain area.

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Overruled precedent examples
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Staleness as hallucination source
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Verification failures
