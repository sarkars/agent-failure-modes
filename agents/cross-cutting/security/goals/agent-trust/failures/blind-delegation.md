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

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a multi-agent code-review system with an Orchestrator that routes tasks by keyword matching against a self-declared capability list, no benchmark certification, and no independent verification step for high-stakes reviews
- Register a "SecurityReviewer" agent that self-declares "security review" as a capability but was actually trained only on general code review, with no smart-contract-specific training
- The delegation contract grants no explicit scope limits and requires no independent verification before the review is accepted as final

### Trigger Mechanism
1. A user submits a smart contract for security review
2. The Orchestrator matches the task to "SecurityReviewer" based on the keyword "security" appearing in both the task and the agent's declared capability
3. SecurityReviewer performs a general code-quality pass (the only kind of review it's actually capable of) and reports no issues found
4. The Orchestrator accepts the report as complete with no independent verification, since none is required for this task category

### Example Reproduction Steps
```
1. User: "Review this smart contract for security" (contract contains
   a reentrancy vulnerability)
2. Orchestrator: if "security" in task: delegate_to("SecurityReviewer")
3. SecurityReviewer output: "I've reviewed the contract. It follows
   good coding practices. No issues found."
4. Orchestrator marks task complete, contract is deployed to production
5. Run an actual smart-contract security benchmark against
   SecurityReviewer's historical outputs -> 0% detection rate for
   reentrancy-class vulnerabilities
```

### Expected Failure State
The contract is deployed to production with an undetected reentrancy vulnerability because the Orchestrator trusted a self-declared "security review" capability without benchmark certification, and no independent verification caught the gap before deployment. A correctly defended system requires SecurityReviewer to have passed a smart-contract-specific benchmark before being eligible for this task category, or routes high-stakes security reviews through an independent second verification step regardless of the delegate's self-reported confidence.

## Mitigation Strategies

### Prevention
1. **Pre-delegation capability testing against benchmark tasks**: Before delegating a specialized task (e.g., smart-contract security review), require the delegate agent to have passed a benchmark test specific to that capability domain, rather than accepting a self-declared capability label like "security review" at face value. Trade-off: requires building and maintaining domain-specific benchmark suites for every capability category the system delegates to.
2. **Explicit delegation contracts with scoped permissions**: Define an explicit contract for each delegation specifying exactly what the delegate is expected to do, what permissions it's granted for that specific task (minimum necessary, not inherited wholesale from the orchestrator), and what "done" looks like, rather than an implicit hand-off that inherits broad permissions by default. Trade-off: adds overhead to define and enforce contracts for every delegation, which can slow down simple/low-risk tasks.
3. **Delegation chain depth limits**: Cap how many hops a task can be delegated through before requiring explicit re-authorization or human review, since accountability and verification both degrade as delegation chains deepen and become harder to trace. Trade-off: may require restructuring workflows that legitimately need deep specialization chains.

### Detection & Response
1. **Independent result verification for high-stakes delegated tasks**: For delegated tasks with material consequences (security reviews, compliance checks, financial decisions), require an independent verification step — a different agent, a deterministic check, or human review — rather than accepting the delegate's own report of "no issues found" as sufficient evidence of correctness.
2. **Capability-claim-vs-performance tracking**: Continuously track each agent's actual task outcomes against its claimed capabilities, and flag agents whose claimed-capability success rate falls below an acceptable threshold for re-certification or removal from that capability's delegate pool.
3. **Delegation audit trail with full chain visibility**: Maintain a complete, queryable audit trail of every delegation (who delegated to whom, what permissions were granted, what was the declared vs. actual outcome), so a failure can be traced to the specific delegation step responsible rather than requiring a full system review.

### Architecture Patterns
1. **Capability-certification registry**: Maintain a registry mapping agents to capabilities they have been independently tested and certified for (not self-declared), with orchestrators required to consult this registry before delegating rather than trusting an agent's own capability announcement.
2. **Scoped, expiring delegation tokens**: Issue delegation with time-limited, task-scoped permission tokens rather than durable inherited permissions, so a delegate's access automatically expires at task completion and cannot be reused or extended beyond its original grant.
3. **Verification-gated delegation completion**: Architect the delegation workflow so a task is only marked "complete" after passing an independent verification step appropriate to its risk tier, rather than the delegate's own self-report being sufficient to close out the task.

### Metrics
1. **capability_claim_verification_rate**: Target: 100% of capability claims tested before first delegation in that category; Alert if any untested claim is used for delegation
2. **delegate_success_rate_by_claimed_capability**: Target: > 90% per capability category; Alert if a specific agent's rate for a claimed capability falls below 70%
3. **delegation_chain_depth**: Target: <= 3 hops for standard workflows; Alert if any task exceeds the configured maximum depth without explicit re-authorization
4. **independent_verification_coverage**: Target: 100% of high-stakes delegated tasks (security, compliance, financial) receive independent verification; Alert on any bypass

### Alerts
1. **High-Stakes Delegation Without Verification** (P1): Condition - a security/compliance/financial delegated task is marked complete without the required independent verification step. Action: Halt downstream use of the delegated result, trigger the missing verification retroactively, treat as an incident given the risk category.
2. **Capability Success Rate Degradation** (P2): Condition - an agent's success rate for a claimed capability falls below 70%. Action: Suspend that agent from the delegate pool for that capability pending re-certification.
3. **Delegation Chain Depth Exceeded** (P2): Condition - a task delegation chain exceeds the configured maximum depth without explicit re-authorization. Action: Halt further delegation, escalate to human review to confirm the chain is legitimate before allowing completion.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - 41.77% specification failures
- [AugmentCode: Fixing Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Coordinator patterns
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) - Task assignment issues
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Delegation failures
