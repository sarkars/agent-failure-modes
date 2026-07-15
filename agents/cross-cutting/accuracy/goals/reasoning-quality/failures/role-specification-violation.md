# Role Specification Violation

## Issue: Agent Breaks Out of Assigned Role

**Frequency**: Occasional (1.5% of MAS failures)

**Symptoms**
- Agent performs actions outside its designated role
- Agent makes decisions reserved for other agents
- Role boundaries blurred during execution
- Agent assumes authority it wasn't granted

**Root Cause**
Agent disobeys role specification by taking actions or making decisions that fall outside its assigned responsibilities. In multi-agent systems, each agent typically has a defined role, but agents may overstep these boundaries, disrupting the intended workflow.

**Example**
```
Multi-agent system: ChatDev software development

Role definitions:
- CEO Agent: Makes final decisions, approves designs
- CPO Agent: Proposes product features
- Programmer Agent: Writes code

Failure scenario:
CPO Agent: "I've decided we should use React for the frontend.
           Here's the final architecture. Let's proceed."
           [Terminates conversation]

Problem: CPO terminated conversation without CEO's consensus
         CPO made architectural decisions (CEO's role)
         
Result: Workflow short-circuited, wrong decisions made
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Role specification violations account for 1.5% of failures
- Part of "System Design Issues" category (44.2% of all failures)
- Often leads to cascading workflow failures

**Contributing Factors**
- Unclear role boundaries in system prompts
- Overlapping responsibilities between agents
- Agent confidence overriding role constraints
- Missing role enforcement mechanisms
- Ambiguous authority hierarchies

## Mitigation Strategies

### Prevention
1. **Explicit per-role permission boundaries**: Encode which decision types each role may make (e.g., CPO proposes features, only CEO approves final architecture/terminates the workflow) as enforced permissions rather than relying on the system prompt's role description alone, which the CPO agent in the example simply disregarded. Trade-off: requires upfront mapping of every decision type to an authorized role, which can be incomplete for novel decision types.
2. **Workflow-terminating actions gated by role**: Specifically restrict conversation/workflow-terminating actions (like the CPO's "Let's proceed" that ended the discussion) to the role(s) explicitly authorized to conclude that phase, since this was the concrete mechanism of the failure. Trade-off: adds friction if the authorized role is slow to respond, potentially stalling the workflow.
3. **Periodic role reminders in long-running multi-agent sessions**: Re-inject each agent's role boundaries into its context at intervals during extended interactions, since role adherence can degrade as conversation history grows and the original system prompt's constraints get diluted. Trade-off: consumes context budget that could otherwise go to task content.

### Detection & Response
1. **Role-vs-action-type audit logging**: Log every decision/action tagged with both the acting agent's role and the decision category, then flag any case where the category (e.g., "architecture decision" or "workflow termination") doesn't match the role's authorized set — this would have caught the CPO's architecture decision immediately.
2. **Missing-approval detection**: For decisions requiring another role's consensus (e.g., CEO approval before finalizing architecture), detect and flag cases where the downstream role's sign-off is absent from the trace, as happened when the CPO proceeded without CEO consensus.
3. **Cross-agent complaint signals**: In multi-agent systems, treat one agent flagging another's overstep (e.g., CEO agent noting it never approved the CPO's decision) as a first-class detection signal rather than only relying on post-hoc trace audits.

### Architecture Patterns
1. **Role-based access control (RBAC) for agent actions**: Apply an RBAC model to agent action types the same way it's applied to human system permissions — the CPO agent's role simply wouldn't have the "finalize architecture" or "terminate workflow" permission, making the violation structurally impossible rather than just discouraged. Deployment consideration: requires a permission-enforcement layer outside the LLM itself, since prompt-based role instructions proved insufficient here.
2. **Escalation/handoff protocol for cross-role decisions**: Define an explicit handoff mechanism (e.g., CPO proposes then routes to CEO agent for approval, CEO confirms before workflow proceeds) instead of allowing any agent to unilaterally conclude a decision that spans roles. Deployment consideration: adds coordination latency and requires all roles to be responsive participants in the workflow.
3. **Authority-check middleware before high-impact actions**: Insert a check before any decision or workflow-terminating action verifying the acting agent's role is authorized for that specific action type, functioning as a runtime guardrail independent of the agent's own self-restraint. Deployment consideration: needs a maintained mapping of action types to authorized roles that's updated as the multi-agent system evolves.

### Metrics
1. **role_boundary_violation_rate**: Target: < 0.5% of actions taken outside the acting agent's authorized role scope; Alert if > 1.5% of MAS traces show a violation (baseline from MAST study).
2. **unauthorized_workflow_termination_count**: Target: 0 workflow-terminating actions taken by a non-authorized role; Alert on any single incident.
3. **cross_role_approval_completeness**: Target: 100% of decisions requiring multi-role consensus have all required approvals logged before proceeding; Alert on any decision missing a required approval.
4. **cascading_failure_rate_from_role_violations**: Target: < 10% of role violations lead to downstream workflow failures; Alert if > 30%, indicating violations are going uncaught until late.

### Alerts
1. **Unauthorized Decision or Termination** (P1): Condition - an agent takes a decision or terminates a workflow phase outside its documented role authority (e.g., CPO finalizing architecture). Action: halt the workflow, roll back to the last valid state, and route the decision to the correctly authorized role.
2. **Missing Cross-Role Approval** (P2): Condition - a decision requiring multi-role consensus proceeds without all required approvals logged. Action: pause downstream steps dependent on that decision and request the missing approval before continuing.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 1.2: Disobey Role Specification
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent misalignment
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Role confusion patterns
