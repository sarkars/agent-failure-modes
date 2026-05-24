# Cherry-Picking Evidence

## Issue: Model Selectively Uses Supporting Evidence, Ignores Contradicting

**Frequency**: Common

**Symptoms**
- Answer presents one-sided view when context is balanced
- Caveats, exceptions, or limitations omitted
- User gets incomplete picture
- Decisions made on partial information

**Root Cause**
Model may select evidence that best fits a coherent narrative, ignoring qualifying information or exceptions that would complicate the answer.

**Example**
```
Retrieved context:
"Clinical trials showed the treatment was effective in 67% of 
patients. However, 23% experienced significant side effects 
including nausea and headaches. The treatment is not recommended 
for patients with heart conditions or those over 65."

Query: "Is this treatment effective?"

Agent: "Yes, clinical trials showed the treatment was effective 
in 67% of patients."

Omitted: Side effects, contraindications, age restrictions

Result: User not informed of risks and limitations
```

**Mitigation Strategies**
1. **Balanced response instructions**: "Include caveats and limitations"
2. **Structured extraction**: Require pros/cons, conditions, exceptions
3. **Comprehensiveness scoring**: Measure coverage of context
4. **Devil's advocate check**: Ask "what did you leave out?"
5. **Multi-turn clarification**: Follow up on omissions
6. **Template responses**: Ensure sections for limitations

**Detection**
- Compare answer coverage to context content
- Track caveat/limitation inclusion rates
- User feedback on incomplete answers
- Measure answer comprehensiveness

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Selective evidence use
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Incomplete synthesis
