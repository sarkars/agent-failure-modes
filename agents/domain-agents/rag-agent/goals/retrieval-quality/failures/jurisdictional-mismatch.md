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

**Mitigation Strategies**
1. **Jurisdiction detection**: Infer jurisdiction from user context
2. **Explicit filtering**: Require jurisdiction parameter in queries
3. **Jurisdiction metadata**: Tag all documents with applicable jurisdiction
4. **Post-retrieval filtering**: Remove inapplicable jurisdictions
5. **Jurisdiction highlighting**: Clearly display source jurisdiction
6. **Conflict warnings**: Alert when sources span multiple jurisdictions

**Detection**
- Expert review identifies jurisdiction mismatches
- User feedback "this doesn't apply in my state"
- Automated jurisdiction extraction and comparison
- Query vs. result jurisdiction analysis

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Document relevance challenges in legal RAG
- [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) - NYC chatbot giving wrong legal advice
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Context handling failures
