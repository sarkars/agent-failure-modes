# Multi-Agent Research and Report Agent: Business Goals, Failure Definitions, and Test List

A team of cooperating agents that gathers sources, analyzes them, and writes a sourced report for a business reader.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline.

## Scope (a starting point)

**The agent does:**
- Search and read sources, and extract claims
- Divide work among sub-agents and combine results
- Write a report that cites its sources and states its limits

**The agent does not:**
- Present unsupported claims as findings
- Run without a time or cost budget
- Hide disagreement between sources

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Make accurate, sourced claims | Every claim in the report is supported by a source that was actually read, at the right level of detail. | Head of research or the report's sponsor |
| G2 | Coordinate so nothing is lost or duplicated | Each sub-task is done once, and results and context reach the agent that needs them. | Platform owner for the agent system |
| G3 | Finish within time and cost limits | The run stops when the work is done or the budget is spent, and says which. | Platform owner and finance |
| G4 | Show the method, the limits, and the disagreement | A reader can see how the answer was produced, what could not be checked, and where sources disagree. | Report sponsor and research lead |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Make accurate, sourced claims

| Field | Definition |
|---|---|
| How to measure | Sampled check of claims against their cited sources: supported, partly supported, or unsupported. Count fabricated and mismatched citations separately. |
| A failure is | Invented citations, claims the cited source does not support, and wrong or missing sources. |
| Severity | Critical: a fabricated citation in a report that informs a decision. High: an unsupported claim. Medium: a missing citation. |
| Hand over to a person when | Any claim the agent cannot support; any source it could not open. |

**Failures to test for this goal (from the library):**
- [AI Agent Cites Sources That Don't Exist](../../by-capability/knowledge-retrieval/goals/citation-accuracy/failures/fabricated-citations.md): AI agent invents plausible-sounding citations — studies, articles, or case law — that don't actually exist
- [AI Agent Cites a Real Source That Doesn't Actually Support the Claim](../../by-capability/knowledge-retrieval/goals/citation-accuracy/failures/misgrounded-citation.md): AI agent cites a real, retrievable document, but the document doesn't actually support the specific claim being made — a citation that…
- [AI Agent's Citation Doesn't Actually Say What the Answer Claims](../../by-capability/knowledge-retrieval/goals/citation-accuracy/failures/unsupported-claim.md): AI agent attaches a real citation to a claim, but the cited source doesn't actually state what the agent says it does
- [AI Agent Cites the Wrong Document Among Multiple Retrieved Sources](../../by-capability/knowledge-retrieval/goals/citation-accuracy/failures/wrong-source.md): AI agent confuses which retrieved document a fact came from and attaches the citation to the wrong source

### G2. Coordinate so nothing is lost or duplicated

| Field | Definition |
|---|---|
| How to measure | Sub-tasks duplicated, dropped, or finished with missing context, from trace review of a sample of runs. |
| A failure is | Handoffs lose context, agents interpret roles differently, state diverges, or agents deadlock. |
| Severity | High: a key finding lost between agents. Medium: duplicated work. |
| Hand over to a person when | A run with no progress, or conflicting outputs from two agents. |

**Failures to test for this goal (from the library):**
- [Task Handoff Errors](../../cross-cutting/operations/goals/multi-agent-coordination/failures/task-handoff-errors.md): Work Lost or Duplicated During Agent Transitions
- [Agent State Divergence](../../cross-cutting/operations/goals/multi-agent-orchestration/failures/agent-state-divergence.md): Two or more agents that are supposed to maintain a shared view of the world — the current status of a task, a customer's conversation…
- [Handoff Context Incompleteness](../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md): When one agent hands a task to another, it passes along a summary or subset of the context it accumulated, rather than the full working…
- [Specification Ambiguity Causing Multi-Agent Role Misalignment](../../cross-cutting/operations/goals/multi-agent-coordination/failures/specification-ambiguity-causing-misalignment.md): Ambiguous Blueprint Specifications Cause Agents to Interpret Roles Differently
- [Deadlock in Multi-Agent](../../cross-cutting/operations/goals/multi-agent-orchestration/failures/deadlock-in-multi-agent.md): Two or more agents each hold a resource that another agent in the group needs, and each is waiting for the resource held by the next,…

### G3. Finish within time and cost limits

| Field | Definition |
|---|---|
| How to measure | Cost and time per report against budget; runs that hit a limit without saying so. |
| A failure is | Agents do not know when to stop, delegate without limit, loop, or burn tokens on speculative work. |
| Severity | High: a run that spends far above budget. Medium: an unfinished report presented as final. |
| Hand over to a person when | Budget reached; no stop condition met. |

**Failures to test for this goal (from the library):**
- [Termination Condition Unawareness](../../cross-cutting/operations/goals/multi-agent-coordination/failures/termination-unawareness.md): Agent Doesn't Know When to Stop
- [Delegation Depth Explosion](../../cross-cutting/operations/goals/multi-agent-coordination/failures/delegation-depth-explosion.md): Agents Delegate to Sub-Agents Creating Unbounded Depth
- [Infinite Loops](../../cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md): Agent Gets Stuck in Infinite Retry Loops
- [Speculative Execution Cost Waste](../../cross-cutting/operations/goals/inference-cost-management/failures/speculative-execution-cost-waste.md): Speculative decoding (using a small, cheap draft model to propose several tokens ahead, then verifying them in one pass with the large…
- [Token Explosion](../../cross-cutting/operations/goals/cost-efficiency/failures/token-explosion.md): Exponential Token Usage Growth

### G4. Show the method, the limits, and the disagreement

| Field | Definition |
|---|---|
| How to measure | Reports with a stated method and limits section; reviewer findings of hidden uncertainty. |
| A failure is | The path to a conclusion is untraceable, the agent verifies its own work with its own bias, or nothing triggers a human review. |
| Severity | High: confident conclusions the reviewer cannot trace. Medium: missing limits. |
| Hand over to a person when | Low-confidence or high-stakes conclusions go to a human reviewer. |

**Failures to test for this goal (from the library):**
- [Missing End-to-End Tracing](../../cross-cutting/operations/goals/observability-monitoring/failures/missing-end-to-end-tracing.md): Request Flows Through Multiple Components Without Unified Trace Context
- [Lost Decision Context](../../cross-cutting/operations/goals/traceability/failures/lost-decision-context.md): Cannot Understand Why Agent Made Specific Decisions
- [Self-Verification Bias](../../cross-cutting/accuracy/goals/verification/failures/self-verification-bias.md): Same model judges its own flawed output
- [No Human Review Trigger](../../cross-cutting/accuracy/goals/verification/failures/no-human-review-trigger.md): Agent cannot identify when to escalate

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Multi Agent Orchestration](../../cross-cutting/operations/goals/multi-agent-orchestration/) | The agents must be coordinated without deadlock or divergence | 10 |
| [Multi Agent Coordination](../../cross-cutting/operations/goals/multi-agent-coordination/) | Roles, handoffs, and stop conditions | 10 |
| [Agent Handoffs Delegation](../../cross-cutting/operations/goals/agent-handoffs-delegation/) | Context must survive each handoff | 10 |
| [Context Lifecycle](../../cross-cutting/operations/goals/context-lifecycle/) | Long runs push early findings out of the window | 6 |
| [Memory Management](../../cross-cutting/operations/goals/memory-management/) | Findings must be stored and retrieved coherently | 22 |
| [Planning and Decomposition](../../cross-cutting/operations/goals/planning-and-decomposition/) | The plan must adapt when sources change it | 10 |
| [Inference Cost Management](../../cross-cutting/operations/goals/inference-cost-management/) | Many agents multiply compute cost | 15 |
| [Cost Optimization](../../cross-cutting/operations/goals/cost-optimization/) | Reuse and caching across agents | 13 |
| [Cost Efficiency](../../cross-cutting/operations/goals/cost-efficiency/) | Loops and token growth | 15 |
| [Observability Monitoring](../../cross-cutting/operations/goals/observability-monitoring/) | Multi-stage runs fail silently without tracing | 3 |
| [Traceability](../../cross-cutting/operations/goals/traceability/) | The path to each claim | 8 |
| [Tool Selection](../../cross-cutting/operations/goals/tool-selection/) | Choosing among search and analysis tools | 10 |
| [Tool Integration Limits](../../cross-cutting/operations/goals/tool-integration-limits/) | Search and data APIs have limits | 6 |
| [Tool Capability Limits](../../cross-cutting/operations/goals/tool-capability-limits/) | Tools can't do everything the agent assumes | 6 |
| [Tool Special Constraints](../../cross-cutting/operations/goals/tool-special-constraints/) | Source-specific rules | 6 |
| [Tool SLA Quality Limits](../../cross-cutting/operations/goals/tool-sla-quality-limits/) | Source and tool quality varies | 5 |
| [Tool Allocation Limits](../../cross-cutting/operations/goals/tool-allocation-limits/) | Shared tool quotas across agents | 8 |
| [Tool Rate Quota Limits](../../cross-cutting/operations/goals/tool-rate-quota-limits/) | Rate limits across many parallel agents | 16 |
| [Established Framework Adoption](../../cross-cutting/operations/goals/established-framework-adoption/) | Use proven orchestration and evaluation frameworks | 6 |

## Security and governance to check

- [Agent Trust](../../cross-cutting/security/goals/agent-trust/) (security)
- [Runtime Security](../../cross-cutting/security/goals/runtime-security/) (security)
- [Governance](../../cross-cutting/governance/goals/governance/) (governance)
- [Output Accuracy](../../cross-cutting/accuracy/goals/output-accuracy/) (accuracy)
- [Verification](../../cross-cutting/accuracy/goals/verification/) (accuracy)

## Decisions your business owner must make

- Time and cost budget per report
- Which sources are in and out of bounds
- Who reviews a report before it informs a decision
- What the report must say about its limits

## Related

- [All agents by business goal](../)
