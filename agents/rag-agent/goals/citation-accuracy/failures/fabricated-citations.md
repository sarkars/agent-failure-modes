# Fabricated Citations

## Issue: Model Cites Sources That Don't Exist

**Frequency**: Occasional

**Symptoms**
- Citation references non-existent document
- Made-up document titles or authors
- URLs that lead nowhere
- Plausible-sounding but fake references

**Root Cause**
When model generates content beyond retrieved context, it may also generate citations for that content, creating entirely fabricated references.

**Example**
```
Query: "What research supports this treatment?"

Agent response: "According to the Johnson et al. (2023) study 
published in the Journal of Medical Research, the treatment 
showed 89% efficacy [1]."

Reality: 
- No such study exists
- No "Journal of Medical Research"
- Citation is completely fabricated

Result: User can't verify, may cite fake study themselves
```

**Real Incidents**
- Lawyers cited 6 fake ChatGPT-generated cases (Avianca lawsuit)
- Legal RAG tools generate plausible-looking fake citations

**Mitigation Strategies**
1. **Citation validation**: Verify all references exist
2. **Closed-book prevention**: Only cite from retrieved content
3. **URL verification**: Check URLs are valid before including
4. **Source registry**: Only allow citations to known sources
5. **Citation generation from extraction**: Build citations from metadata
6. **Warning labels**: Flag citations that couldn't be verified

**Detection**
- Validate all citations against source index
- Check URLs for accessibility
- Cross-reference author/title combinations
- Flag citations not in retrieved documents

## References
- [Avianca Lawyers](https://www.cnn.com/2023/05/27/business/chat-gpt-avianca-mata-lawyers/index.html) - 6 fake cases cited
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Fabricated legal citations
