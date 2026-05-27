# Misgrounded Citation

## Issue: Citation Exists But Doesn't Support the Claim

**Frequency**: Common (contributes to 17-33% hallucination rate in legal RAG)

**Symptoms**
- Citations link to real documents
- Cited source doesn't actually support the claim made
- Source may be irrelevant to the topic
- Source may contradict the claim
- Users verify citation exists but miss that it's misapplied

**Root Cause**
RAG system retrieves and cites real documents, but the generation model incorrectly asserts the source supports a claim it doesn't. Unlike fabricated citations (which are easy to catch), misgrounded citations pass basic verification because the source exists - the failure is in the semantic relationship between claim and source.

**Example**
```
Query: "What standard applies to abortion regulations after Dobbs?"

RAG Response:
"After Dobbs, abortion regulations are subject to the undue burden
standard established in Casey. See Planned Parenthood v. Casey, 
505 U.S. 833 (1992)."

Problem:
- Casey citation is REAL and correctly formatted
- BUT Casey's undue burden standard was OVERRULED by Dobbs
- Correct answer: rational basis review now applies
- System cited real case but claim is completely wrong

Verification trap:
- User clicks citation link → Casey exists ✓
- User assumes citation validates the claim
- User doesn't realize Casey is no longer controlling law
```

**Key Statistics**
From Stanford Legal RAG Hallucinations Study (2025):
- Legal RAG tools hallucinate 17-33% of time
- Westlaw AI-Assisted Research: hallucination rate ~2x other tools
- Misgrounding is distinct from "incorrect" - claim may seem plausible
- Particularly insidious because citations pass basic verification

**Misgrounding Patterns**
- **Semantic mismatch**: Source discusses topic but doesn't support specific claim
- **Overruled precedent**: Cites law that's been superseded
- **Wrong jurisdiction**: Cites law from inapplicable jurisdiction
- **Dicta vs. holding**: Cites dicta as if it were binding
- **Distinguishable facts**: Case has different material facts

**Contributing Factors**
- Retrieval based on text similarity, not legal relevance
- Model doesn't understand legal hierarchy (holdings vs. dicta)
- No temporal awareness of legal changes
- Jurisdictional context not properly weighted
- Generation model "looks for support" rather than validates claims

**Mitigation Strategies**
1. **Citation verification**: Check source actually supports claim
2. **Temporal validation**: Verify cited law is still good law
3. **Jurisdictional filtering**: Ensure sources match query jurisdiction
4. **Claim-source alignment scoring**: Measure semantic match
5. **Citation explanation**: Require explanation of how source supports claim

**Detection**
- Expert review of claim-source relationships
- Automated citation verification systems (Shepard's, KeyCite)
- User feedback on "citation didn't support claim"
- A/B testing with domain expert evaluation

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - 17-33% hallucination rate in legal RAG tools
- [Journal of Empirical Legal Studies](https://doi.org/10.1111/jels.12413) - First empirical study of legal AI hallucinations
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Verification failures
