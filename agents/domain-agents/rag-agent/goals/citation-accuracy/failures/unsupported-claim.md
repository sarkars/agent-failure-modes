# Citation Doesn't Support Claim

## Issue: Cited Source Doesn't Actually Support the Claim Made

**Frequency**: Common

**Symptoms**
- Citation exists and source exists, but claim isn't in source
- Source says something different than claim
- Claim is inference not stated in source
- Citation is tangentially related but doesn't support specific claim

**Root Cause**
Model may make a claim, then attach a citation to a related source that doesn't actually support the specific statement made.

**Example**
```
Agent response: "The company guarantees 99.9% uptime [1]"

Source [1] actual text: "We strive to maintain high availability 
for all services."

Gap: "Strive to maintain high availability" ≠ "guarantees 99.9%"

Result: User believes guarantee exists when it doesn't
```

**Mitigation Strategies**
1. **Extractive verification**: Require quoted text to match citation
2. **NLI checking**: Use entailment model to verify support
3. **Claim-source matching**: Explicitly verify claim is in source
4. **Conservative claims**: Only state what source explicitly says
5. **Inference labeling**: Mark when claim is inference vs. stated
6. **Quote requirements**: Include direct quote alongside citation

**Detection**
- NLI-based claim-source entailment checking
- Compare claim text to cited content
- Track support verification failure rate
- User reports of misleading citations

## References
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Claims without support
- [Self-Healing RAG Layer](https://towardsdatascience.com/rag-hallucinates-i-built-a-self-healing-layer-that-fixes-it-in-real-time/) - Citation verification
