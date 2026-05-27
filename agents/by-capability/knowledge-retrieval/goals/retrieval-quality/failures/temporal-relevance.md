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

**Mitigation Strategies**
1. **Citation validation services**: Integrate Shepard's, KeyCite for legal
2. **Recency weighting**: Prefer newer documents in retrieval
3. **Supersession tracking**: Maintain graph of superseding relationships
4. **Date display**: Prominently show document dates
5. **Staleness warnings**: Alert when citing old sources
6. **Continuous reindexing**: Update knowledge base regularly

**Detection**
- Expert review identifies outdated citations
- Automated checking against update services
- User corrections for "this law changed"
- Comparison of response dates vs. current date

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Overruled precedent examples
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Staleness as hallucination source
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Verification failures
