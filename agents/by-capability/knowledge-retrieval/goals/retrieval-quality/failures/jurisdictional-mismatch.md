# Jurisdictional Mismatch

## Issue: Retrieved Content From Wrong Jurisdiction or Context

**Frequency**: Common

**Symptoms**
- System cites law from different state/country
- Retrieved documents don't apply to user's situation
- Answer technically correct but for wrong jurisdiction
- User receives inapplicable guidance
- No clear indication of jurisdictional scope

**Root Cause**
RAG retrieval based on text similarity finds documents that discuss similar topics but from different jurisdictions. The model cannot distinguish between California law and New York law when both discuss similar legal concepts. This is especially problematic because legal rules vary significantly by jurisdiction.

**Example**
```
Query: "Is non-compete agreement enforceable for my employee?"
Context: User is a California employer

Retrieval: 
- Texas Business & Commerce Code § 15.50
- Delaware case law on non-competes
- General article on non-compete enforceability

RAG Response:
"Non-compete agreements are generally enforceable if they are
reasonable in scope, duration, and geographic area. Courts
typically uphold 1-2 year restrictions."

Problem:
- California BANS most non-compete agreements (Bus. & Prof. Code § 16600)
- Texas and Delaware law (retrieved) allows them with restrictions
- RAG found semantically similar content from wrong jurisdictions
- User could create unenforceable contract or face legal issues

Result: Employer relies on wrong law, potentially facing
        penalties for unenforceable restrictive covenants
```

**Key Statistics**
From Stanford Legal RAG Hallucinations Study (2025):
- Jurisdictional mismatch is a key failure mode in legal RAG
- Text similarity retrieval ignores non-textual relevance factors
- Contributes to overall 17-33% hallucination rate
- Particularly problematic in multi-jurisdictional legal systems

**Mismatch Patterns**
- **State vs. state**: Different US state laws retrieved
- **Federal vs. state**: Federal law cited when state law applies
- **Country vs. country**: Foreign law in domestic query
- **Court level**: Trial court ruling cited as binding when it's not
- **Historical jurisdiction**: Old territorial or colonial law

**Contributing Factors**
- Text embeddings don't encode jurisdiction
- Similar legal language across jurisdictions
- Retrieval lacks geographic/contextual awareness
- Users don't specify jurisdiction in queries
- Knowledge base contains multi-jurisdictional content

## Mitigation Strategies

### Prevention
1. **Mandatory Jurisdiction Metadata Tagging**: Tag every legal/regulatory document with its governing jurisdiction(s) at ingestion; reject untagged content from entering jurisdiction-sensitive collections. This directly targets the root cause that embeddings can't distinguish California law from Texas or Delaware law based on text alone.
2. **Jurisdiction-First Pre-Filtering**: Detect or require the user's jurisdiction (from profile, query, or explicit prompt) and apply a hard pre-retrieval filter to jurisdiction-matching documents before semantic search runs, rather than relying on similarity ranking to surface the right jurisdiction after the fact. Trade-off: requires reliably capturing user jurisdiction, which isn't always available.
3. **Jurisdiction-Aware Query Classifier**: Route queries through a classifier that identifies whether jurisdiction is ambiguous or unspecified and, if so, forces a clarifying question instead of defaulting to whichever jurisdiction has the most indexed content (which skewed the Texas/Delaware result in the example).

### Detection & Response
1. **Jurisdiction-Mismatch Audit Sampling**: Have legal SMEs periodically review a sample of RAG legal answers, comparing the cited source jurisdiction against the stated or inferred user jurisdiction.
2. **Multi-Jurisdiction Retrieval Flagging**: Automatically flag any response where the top-k retrieved set spans more than one jurisdiction tag, since this is a leading indicator of the failure shown in the example (Texas, Delaware, and generic content retrieved together for a California question).
3. **User-Reported Inapplicability Tracking**: Tag and trend user feedback of the form "this doesn't apply in my state," feeding directly back into jurisdiction tagging QA.

### Architecture Patterns
1. **Jurisdiction-Partitioned Indices**: Maintain separate retrieval indices per jurisdiction (or a partition key) instead of one merged corpus, so cross-jurisdiction leakage requires an explicit multi-index query rather than being the default retrieval behavior.
2. **Post-Retrieval Jurisdiction Conflict Detection**: After retrieval, run a rules-based check comparing jurisdiction tags of the returned set; if conflicting jurisdictions are present, surface a warning banner or block synthesis until resolved.
3. **Explicit Jurisdiction Disclosure in Output**: Require the answer generator to cite the governing jurisdiction inline for every legal claim, so a wrong-jurisdiction citation (like the non-compete enforceability example) is visible and checkable rather than presented as universally applicable law.

### Metrics
1. **jurisdiction_tagging_coverage_percent**: Target: 100% of legal corpus; Alert threshold: < 98%
2. **cross_jurisdiction_retrieval_rate**: Target: < 5% of legal queries; Alert threshold: > 10%
3. **jurisdiction_mismatch_expert_flagged_rate**: Target: < 2%; Alert threshold: > 5%
4. **unresolved_jurisdiction_query_rate**: Target: < 10%; Alert threshold: > 20%

### Alerts
1. **Cross-Jurisdiction Contamination** (P1): Condition - the top-k retrieved set for a legal query contains 2+ conflicting jurisdiction tags and synthesis proceeds without disclosure. Action: block synthesis, require jurisdiction disambiguation, escalate to the legal content team.
2. **Untagged Legal Content Ingested** (P1): Condition - a document enters the legal corpus without jurisdiction metadata. Action: quarantine from retrieval until tagged.
3. **Expert-Flagged Mismatch Spike** (P2): Condition - jurisdiction_mismatch_expert_flagged_rate exceeds 5% in the weekly SME audit. Action: review the jurisdiction classifier/tagging pipeline, retrain if the pattern is systematic.

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Document relevance challenges in legal RAG
- [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) - NYC chatbot giving wrong legal advice
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Context handling failures
