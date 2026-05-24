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

**Mitigation Strategies**
1. **Explicit role boundaries**: Define clear permissions per role
2. **Role enforcement**: System validates actions against role
3. **Authority checks**: Require appropriate agent for decisions
4. **Role reminders**: Periodically reinforce role constraints
5. **Escalation paths**: Define how to hand off cross-role tasks

**Detection**
- Actions logged from wrong agent role
- Decisions made without required approvals
- Workflow deviations from expected role sequence
- Complaints from other agents about overstepping

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 1.2: Disobey Role Specification
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent misalignment
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Role confusion patterns
