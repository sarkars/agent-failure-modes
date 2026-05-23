# Parametric Override

## Issue: Model Uses Training Data Over Retrieved Context

**Frequency**: Common

**Symptoms**
- Answer reflects general knowledge, not specific retrieved content
- Outdated information from training data used
- Domain-specific details replaced with generic knowledge
- Context contradicts parametric knowledge, model uses latter

**Root Cause**
LLMs have strong priors from training. When context conflicts with these priors or model is more "confident" in training data, it may override retrieved information.

**Example**
```
Retrieved context (company wiki):
"Our company headquarters is in Austin, Texas. We moved from 
San Francisco in 2023."

Query: "Where is the company headquarters?"

Agent: "Based on my information, the company is headquartered 
in San Francisco."

Reality: Model's training data (pre-2023) overrides current context

Result: User given outdated location
```

**Mitigation Strategies**
1. **Context supremacy prompting**: "Trust the provided documents over your knowledge"
2. **Conflict detection**: Identify when parametric and context disagree
3. **Source attribution**: Require explicit context citations
4. **Knowledge cutoff awareness**: Model admits when training data may be stale
5. **Fine-tuning for context-following**: Train to defer to context
6. **Retrieval-only mode**: Restrict to extractive answers

**Detection**
- Compare answers to both context and known training data
- Track context vs. parametric knowledge conflicts
- Monitor outdated information in answers
- Test with deliberately conflicting context
