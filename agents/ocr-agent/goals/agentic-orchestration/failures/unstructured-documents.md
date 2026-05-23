# Unstructured Documents

## Issue: Unstructured Document Confusion

**Frequency**: Common

**Symptoms**
- Agent cannot determine document structure
- Important information buried in narrative text
- No clear extraction schema applies

**Root Cause**
Agents work well on structured forms but struggle with free-form documents like correspondence, reports, or legal narratives where key information isn't in labeled fields.

**Example**
```
Input: Email chain discussing contract amendment

"...as we discussed on the call, we're okay with moving forward 
at the revised price of $475k instead of the original $500k, 
assuming delivery by end of Q2..."

Agent task: Extract contract value
Challenge: Value is in narrative, not labeled field
```

**Mitigation Strategies**
1. **Information extraction models**: NER and relation extraction for unstructured text
2. **Question-answering approach**: Frame extraction as Q&A over document
3. **Structured prompts**: Guide agent to identify key information types
4. **Hybrid extraction**: Combine rule-based and ML approaches
