# Routing Failures

## Issue: Orchestrator Routes Task to Wrong Agent

**Frequency**: Common

**Symptoms**
- Tasks assigned to agents without required capabilities
- Specialist agents underutilized, generalist overloaded
- User queries bounced between agents
- Task completed but poorly due to wrong agent
- Routing decisions based on keywords, not semantics

**Root Cause**
Multi-agent systems rely on orchestrators to route tasks to appropriate specialist agents. When routing logic is naive (keyword matching), misconfigured, or the orchestrator misunderstands task requirements, tasks go to wrong agents. A complex financial analysis goes to a general assistant instead of the finance specialist. The task might still "complete" but with inferior quality.

**Example**
```
Scenario: Customer service multi-agent system

Available agents:
  - billing_agent: Handle invoices, payments, refunds
  - technical_agent: Debug issues, configuration help
  - sales_agent: Product info, upgrades, renewals
  - general_agent: Everything else

Customer query: "My bill seems wrong, I was charged for 
                 a feature I can't seem to access"

Routing logic: Keyword matching
  - "bill" → billing_agent
  - "feature" → sales_agent
  - "can't access" → technical_agent

Conflict resolution: First match wins

Result:
  Query routed to: billing_agent
  
Problem:
  - Billing agent only sees billing issue
  - Doesn't investigate access problem
  - Tells user "bill is correct"
  - User still can't access feature they're paying for
  
Correct routing:
  - Should go to technical_agent first
  - Discovers feature is broken (bug)
  - Then billing_agent for credit
  
Impact: Customer churns, negative review
```

**Key Statistics**
From Multi-Agent Research (2026):
- 25-35% of tasks routed to suboptimal agent
- Keyword-based routing accuracy: 60-70%
- Semantic routing accuracy: 85-95%
- Mis-routed tasks take 2-3x longer to resolve
- 41-86.7% of multi-agent systems fail (includes routing)

**Routing Failure Types**
| Type | Cause | Impact |
|------|-------|--------|
| Wrong specialist | Misunderstood task | Poor quality |
| Overloaded agent | No load balancing | Delays |
| Capability gap | No capable agent | Task failure |
| Circular routing | Agents bounce task | Infinite loop |
| Premature routing | Incomplete understanding | Rework |

**Contributing Factors**
- Keyword-only routing logic
- No semantic understanding of tasks
- Missing agent capability profiles
- No routing feedback loop
- Static routing rules
- No routing explainability

**Mitigation Strategies**
1. **Semantic routing**: Use embeddings to match task to agent capabilities
2. **Capability profiles**: Detailed agent capability declarations
3. **Multi-factor routing**: Consider complexity, load, expertise
4. **Routing validation**: Validate agent can handle task before handoff
5. **Rerouting protocol**: Easy path to correct routing mistakes
6. **Routing analytics**: Track routing decisions and outcomes

**Detection**
- Monitor task-agent capability alignment
- Track rerouting frequency
- Measure task completion quality by route
- Alert on circular routing patterns
- Compare actual vs. optimal routing

## References

- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Multi-agent failure modes
- [Redis: Multi-Agent Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination issues
- [Augment Code: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Routing patterns
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Orchestration
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Routing monitoring
