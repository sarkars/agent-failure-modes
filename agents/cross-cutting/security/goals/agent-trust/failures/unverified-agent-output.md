# Unverified Agent Output

## Issue: Agents Accept Other Agents' Outputs Without Verification

**Frequency**: Very Common

**Symptoms**
- Errors from one agent propagate through entire system
- Hallucinations amplified across agent chain
- No detection of incorrect intermediate results
- Final output contains compounded errors
- System confidently returns wrong answers

**Root Cause**
In multi-agent systems, downstream agents typically accept upstream agent outputs as ground truth. When Agent A passes results to Agent B, Agent B processes them without independent verification. If Agent A hallucinates, makes errors, or is compromised, these errors propagate unchallenged through the entire agent chain, often amplifying at each step.

**Example**
```
Research Agent System:

Agent A (Researcher):
  Task: "Find the market cap of TechCorp"
  Output: "$450 billion" (HALLUCINATED - actual is $45 billion)

Agent B (Analyst):
  Receives: "$450 billion market cap"
  Task: "Compare to competitors"
  Output: "TechCorp is 10x larger than its nearest competitor"
  (Compounds the error with confident analysis)

Agent C (Writer):
  Receives: "10x larger than competitors"
  Task: "Write investment summary"
  Output: "TechCorp dominates the market with unprecedented scale,
           making it a must-buy for any tech portfolio..."
  (Error now buried in persuasive narrative)

Final output: Completely wrong investment advice
Error source: Invisible to end user
Each agent trusted the previous agent's output implicitly
```

**Key Statistics**
From Multi-Agent Research (2026):
- 21.30% of multi-agent failures from verification gaps (MAST)
- Independent judge agents improve accuracy 7x (PwC)
- STRATUS multi-agent SRE improved mitigation 1.5x with validation agents
- Error amplification increases with agent chain length
- Most systems have zero inter-agent verification

**Trust Patterns**
| Pattern | Risk | Prevalence |
|---------|------|------------|
| Direct passthrough | High | Very Common |
| Format validation only | Medium | Common |
| Semantic validation | Low | Rare |
| Independent verification | Very Low | Very Rare |
| Cross-agent consensus | Very Low | Rare |

**Contributing Factors**
- Agents designed to "be helpful" and accept input
- Verification adds latency and cost
- No standard inter-agent verification protocols
- Downstream agents lack context to verify
- System assumes all agents are correct

**Mitigation Strategies**
1. **Independent verifier agents**: Dedicated agents that validate outputs
2. **Cross-reference checks**: Verify facts against authoritative sources
3. **Confidence propagation**: Track and decay confidence across chain
4. **Semantic validation**: Check if output makes sense in context
5. **Human checkpoints**: Insert human review at critical junctures
6. **Consensus mechanisms**: Multiple agents must agree on key facts

**Detection**
- Track error rates at each agent boundary
- Compare final outputs to ground truth
- Monitor for confidence without verification
- Audit agent chain for validation steps
- Test with known-bad inputs to detect propagation

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - 21.30% verification gap failures
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Independent validation patterns
- [Redis: Why Multi-Agent Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Error propagation analysis
- [STRATUS Multi-Agent SRE](https://arxiv.org/abs/) - Validation agent improvements
