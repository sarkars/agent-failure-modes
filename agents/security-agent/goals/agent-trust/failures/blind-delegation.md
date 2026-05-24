# Blind Delegation

## Issue: Agents Delegate Tasks Without Verifying Delegate Capabilities or Trustworthiness

**Frequency**: Common

**Symptoms**
- Tasks assigned to incapable agents
- Sensitive operations delegated without authorization checks
- No verification that delegated task was completed correctly
- Agent claims capability it doesn't have
- Delegation chains become untraceable

**Root Cause**
Orchestrator agents delegate tasks to specialist agents based on declared capabilities or simple routing rules. They rarely verify that the specialist can actually perform the task, has appropriate permissions, or will execute it correctly. This blind trust enables both accidental failures (delegating to wrong agent) and intentional attacks (malicious agent claiming false capabilities).

**Example**
```
Code Review Multi-Agent System:

Orchestrator receives: "Review this smart contract for security"

Delegation logic:
  if "security" in task:
    delegate_to("SecurityReviewer")

SecurityReviewer agent:
  - Declared capability: "security review"
  - Actual training: General code review
  - Smart contract expertise: None

Execution:
  SecurityReviewer: "I've reviewed the contract. 
    It follows good coding practices. No issues found."

Reality:
  - Contract has reentrancy vulnerability
  - Agent couldn't detect smart contract-specific issues
  - Orchestrator accepted review as complete
  - Vulnerability deployed to production

6 months later: $2M drained via reentrancy attack

Post-mortem: "Why did we trust the security review?"
Answer: Orchestrator had no way to verify agent expertise
```

**Key Statistics**
From Multi-Agent Research (2026):
- 41.77% of failures from specification problems (MAST)
- Role ambiguity leads to wrong agent assignment
- Capability verification virtually non-existent
- "Which agent should handle this?" - common failure point
- Delegation depth increases error probability

**Delegation Failures**
| Failure | Cause | Frequency |
|---------|-------|-----------|
| Wrong specialist | Capability mismatch | Common |
| Missing capability check | No verification | Very Common |
| Permission bypass | Delegation inherits permissions | Occasional |
| Result not verified | Blind acceptance | Very Common |
| Lost accountability | Untraceable chains | Common |

**Contributing Factors**
- Agents self-declare capabilities
- No capability testing before delegation
- Orchestrators optimize for speed, not verification
- Delegation inherits orchestrator's permissions
- No standard capability verification protocol

**Mitigation Strategies**
1. **Capability testing**: Verify agent can perform task before delegation
2. **Delegation contracts**: Explicit agreements on what delegate will do
3. **Result verification**: Independent check of delegated work
4. **Permission scoping**: Delegate only minimum required permissions
5. **Delegation limits**: Cap delegation chain depth
6. **Audit trails**: Track full delegation history

**Detection**
- Monitor task completion quality by delegate
- Track capability claims vs. actual performance
- Audit permission usage during delegation
- Flag deep delegation chains
- Measure delegation success rates

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - 41.77% specification failures
- [AugmentCode: Fixing Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Coordinator patterns
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) - Task assignment issues
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Delegation failures
