# Domain Mismatch

## Issue: Agent Fails on Out-of-Distribution or Specialized Inputs

**Frequency**: Common

**Symptoms**
- Responses remain coherent but align to wrong domain
- Shallow or irrelevant content for specialized queries
- Agent applies general knowledge to domain-specific questions
- Accuracy collapse on real-world inputs vs. benchmarks

**Root Cause**
Agent encounters inputs from unfamiliar or highly specialized domains that differ from its training distribution. While broad pre-training enables general competence, it "presents distinct challenges" when facing novel domains. The agent produces internally coherent responses that are aligned to the wrong domain rather than being obviously incorrect.

**Example**
```
Domain: Industrial chemical processing

User: "What's the optimal residence time for a CSTR 
       with A → B reaction, k=0.05/min, target 95% conversion?"

Agent response:
"For optimal conversion, you should allow sufficient time
for the reaction to complete. Consider monitoring temperature
and pressure to ensure safety. Chemical reactions typically
require careful attention to stoichiometry..."

Problem: 
- Response is coherent but doesn't apply chemical engineering math
- Agent avoided τ = X/(k(1-X)) calculation it doesn't know
- Provided general chemistry advice instead of process engineering

Result: User gets unhelpful generic response, may not realize
        the agent lacks domain expertise
```

**Key Statistics**
From Failure Modes in LLM Systems (arxiv:2511.19933):
- Domain mismatch identified as distinct from hallucination
- Pre-training on broad corpora creates challenges for specialized domains
- Accuracy collapse occurs when real-world inputs differ from benchmark prompts
- Errors manifest as shallow content rather than obvious fabrication

**Mismatch Patterns**
- **Domain confusion**: Agent applies wrong field's knowledge
- **Depth limitation**: Surface-level response to deep technical query
- **Terminology mismatch**: Uses general terms instead of domain-specific ones
- **Method avoidance**: Skips domain-specific calculations or procedures

**Contributing Factors**
- Training data weighted toward general knowledge
- Limited exposure to specialized professional domains
- No mechanism to recognize domain boundaries
- Benchmark tests don't capture domain-specific depth
- Confidence masks lack of expertise

**Mitigation Strategies**
1. **Domain detection**: Identify when queries require specialized knowledge
2. **Explicit uncertainty**: Express uncertainty in unfamiliar domains
3. **Domain-specific RAG**: Retrieve authoritative domain content
4. **Expert routing**: Route specialized queries to fine-tuned models
5. **Confidence calibration**: Lower confidence on out-of-distribution inputs

**Detection**
- Expert review reveals shallow or incorrect domain application
- Terminology analysis shows generic vs. specialized language
- Comparison against domain-specific benchmarks
- User feedback indicating "not relevant" or "too general"

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) - Domain mismatch/out-of-distribution failure mode
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Pre-training bias overriding context
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Specialized domain challenges
