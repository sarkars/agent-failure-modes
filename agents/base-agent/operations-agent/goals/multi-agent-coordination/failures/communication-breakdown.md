# Communication Breakdown

## Issue: Information Lost or Corrupted Between Agents

**Frequency**: Common

**Symptoms**
- Downstream agent missing context from upstream
- Agent outputs based on incomplete information
- Repeated requests for already-provided information
- Inconsistent understanding across agents

**Root Cause**
When agents communicate through natural language or structured messages, information can be lost due to summarization, misinterpretation, or context window limitations. Each agent-to-agent handoff is an opportunity for information degradation.

**Example**
```
Research Agent: Finds 10 relevant papers, summarizes key findings
               Includes important caveat: "Results only valid for datasets > 1M rows"

Summary Agent: Condenses research into bullet points
              Caveat omitted for brevity

Decision Agent: Recommends approach based on summary
               Applied to 10K row dataset

Result: Invalid recommendation due to lost caveat
```

**Information Loss Points**
- **Summarization**: Details lost when condensing information
- **Context truncation**: Earlier context dropped for new input
- **Format conversion**: Structure lost in text serialization
- **Semantic drift**: Meaning shifts through paraphrasing
- **Priority filtering**: Agent drops "unimportant" details

**Potential Effects**
- Decisions made on incomplete information
- Important caveats or warnings lost
- Duplicated work due to lost state
- Cascading errors through agent chain

**Mitigation Strategies**
1. **Structured message passing**: Use schemas instead of free text
2. **Critical information flags**: Mark must-preserve content
3. **Bidirectional confirmation**: Receiving agent confirms understanding
4. **Provenance chains**: Track information origin through pipeline
5. **Compression verification**: Check that summaries preserve key facts
6. **Dedicated memory**: Store critical context outside message flow

**Detection**
- Downstream agents asking for information already provided
- Output quality degrading through longer agent chains
- Key facts present in early stages missing from final output
- Agents making decisions that contradict earlier context

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Communication as failure category
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination breakdowns
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow patterns
