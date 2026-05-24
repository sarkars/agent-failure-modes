# Consensus Deadlock

## Issue: Multi-Agent Voting or Agreement Fails to Resolve

**Frequency**: Occasional

**Symptoms**
- System unable to reach decision
- Agents repeatedly propose conflicting solutions
- Timeout on consensus operations
- Oscillation between options without convergence

**Root Cause**
Multi-agent systems often use voting, debate, or consensus mechanisms to make decisions. These can fail to converge due to balanced opposing views, strategic behavior, or incompatible evaluation criteria.

**Example**
```
Code Review Multi-Agent System:
Agent A (Security): "Reject - potential SQL injection"
Agent B (Performance): "Reject - inefficient query pattern"
Agent C (Readability): "Approve - clean, well-documented"
Agent D (Testing): "Approve - good test coverage"

Consensus rule: 3/4 majority required

Round 1: 2-2 split, no consensus
Round 2: Agents re-evaluate, same split
Round 3-10: Deadlock continues

Result: Code review never completes
```

**Deadlock Patterns**
- **Balanced opposition**: Equal votes for opposing options
- **Circular preferences**: A > B > C > A
- **Evaluation divergence**: Agents use incompatible criteria
- **Strategic blocking**: Agent holds out to force preferred outcome
- **Information asymmetry**: Agents make different assessments from different data

**Potential Effects**
- System hangs without decision
- Resource exhaustion from repeated deliberation
- Timeout with arbitrary or no decision
- User frustration with unresponsive system

**Mitigation Strategies**
1. **Tie-breaking rules**: Predetermined method to resolve splits
2. **Weighted voting**: Priority agents have more weight
3. **Escalation**: Route to human after N failed rounds
4. **Timeout defaults**: Default action if consensus not reached
5. **Deliberation limits**: Cap number of voting rounds
6. **Consensus alternatives**: Use ranked choice or approval voting

**Detection**
- Voting rounds exceeding threshold
- Same proposals repeatedly submitted
- System metrics showing deliberation without progress
- Timeout events in consensus operations

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - System design issues including consensus
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Multi-agent decision failures
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination deadlocks
