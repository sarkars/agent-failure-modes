# Wrong Source Cited

## Issue: Citation Points to Different Document Than Information Came From

**Frequency**: Common

**Symptoms**
- Citation exists but document doesn't contain the claim
- Source attribution confused between similar documents
- User clicks citation, finds different content
- Multiple sources retrieved, wrong one cited

**Root Cause**
When multiple documents are in context, model may confuse which source contained which information, especially with similar documents.

**Example**
```
Retrieved documents:
[1] Q2 Report: "Revenue increased 12% year-over-year"
[2] Q3 Report: "Revenue increased 18% year-over-year"

Agent response: "Revenue increased 18% year-over-year [1]"

Error: 18% is from Q3 Report [2], not Q2 Report [1]

Result: User references Q2 report but finds 12%, not 18%
```

**Mitigation Strategies**
1. **Extractive citations**: Quote the exact text, attribute to source
2. **Source-claim verification**: Validate each citation before output
3. **Inline source marking**: Mark source while extracting, not after
4. **Single-source answers**: Answer from one document when possible
5. **Citation validation step**: Post-process to verify attribution
6. **Distinct source identifiers**: Make sources clearly distinguishable

**Detection**
- Automated citation verification
- Compare cited text to source content
- Track citation accuracy by source count
- User reports of wrong citations

## References
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Citation accuracy issues
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Source attribution errors
