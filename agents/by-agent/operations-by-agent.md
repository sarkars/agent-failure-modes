# Operations Failures by Agent: Which Concerns Matter for Which Use Case

**The operations area holds the most failure patterns in the library (409), so it is split here by concern and by agent.** Each concern lists the use-case agents where it matters most. The mapping is my judgment from each agent's job, not a measurement.

## Key Takeaways

- Operations has 37 goals with written patterns, grouped into 6 concerns below.
- Each use-case agent page lists the operations concerns that matter for it and why.
- Every operations goal is mapped to at least one use-case agent.

## Concerns and the agents they matter for

### Tools and integrations

| Goal | Patterns | Matters most for |
|---|---|---|
| [Tool Reliability](../cross-cutting/operations/goals/tool-reliability/) | 19 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [Refunds and Billing-Disputes Agent](use-cases/refunds-and-billing-disputes-agent.md), [Insurance Claims Intake and Triage Agent](use-cases/claims-intake-and-triage-agent.md), [Lead Qualification (SDR) Agent](use-cases/lead-qualification-agent.md), [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md), [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md), [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Tool Invocation](../cross-cutting/operations/goals/tool-invocation/) | 12 | [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Tool Selection](../cross-cutting/operations/goals/tool-selection/) | 10 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Tool Selection Sequencing](../cross-cutting/operations/goals/tool-selection-sequencing/) | 8 | [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Tool Error Handling](../cross-cutting/operations/goals/tool-error-handling/) | 2 | [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Tool Integration Limits](../cross-cutting/operations/goals/tool-integration-limits/) | 6 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Tool Capability Limits](../cross-cutting/operations/goals/tool-capability-limits/) | 6 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Tool Access Scope Limits](../cross-cutting/operations/goals/tool-access-scope-limits/) | 16 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md) |
| [Tool Rate Quota Limits](../cross-cutting/operations/goals/tool-rate-quota-limits/) | 16 | [Lead Qualification (SDR) Agent](use-cases/lead-qualification-agent.md), [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Tool Operational Limits](../cross-cutting/operations/goals/tool-operational-limits/) | 14 | [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Tool Financial Limits](../cross-cutting/operations/goals/tool-financial-limits/) | 11 | [Refunds and Billing-Disputes Agent](use-cases/refunds-and-billing-disputes-agent.md) |
| [Tool Allocation Limits](../cross-cutting/operations/goals/tool-allocation-limits/) | 8 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Tool Special Constraints](../cross-cutting/operations/goals/tool-special-constraints/) | 6 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Tool SLA Quality Limits](../cross-cutting/operations/goals/tool-sla-quality-limits/) | 5 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Dependency Management](../cross-cutting/operations/goals/dependency-management/) | 23 | [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Version Management](../cross-cutting/operations/goals/version-management/) | 22 | [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md), [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |

### Memory and context

| Goal | Patterns | Matters most for |
|---|---|---|
| [Memory Management](../cross-cutting/operations/goals/memory-management/) | 22 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [Lead Qualification (SDR) Agent](use-cases/lead-qualification-agent.md), [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Memory Safety](../cross-cutting/operations/goals/memory-safety/) | 10 | [Insurance Claims Intake and Triage Agent](use-cases/claims-intake-and-triage-agent.md) |
| [Context Lifecycle](../cross-cutting/operations/goals/context-lifecycle/) | 6 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Input Output Handling](../cross-cutting/operations/goals/input-output-handling/) | 22 | [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md), [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |

### State, planning, and resilience

| Goal | Patterns | Matters most for |
|---|---|---|
| [State Tracking](../cross-cutting/operations/goals/state-tracking/) | 9 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [Insurance Claims Intake and Triage Agent](use-cases/claims-intake-and-triage-agent.md), [Lead Qualification (SDR) Agent](use-cases/lead-qualification-agent.md) |
| [State Consistency](../cross-cutting/operations/goals/state-consistency/) | 8 | [Refunds and Billing-Disputes Agent](use-cases/refunds-and-billing-disputes-agent.md), [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md), [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md), [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Planning and Decomposition](../cross-cutting/operations/goals/planning-and-decomposition/) | 10 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Fault Tolerance](../cross-cutting/operations/goals/fault-tolerance/) | 20 | [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md), [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md), [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Reliability and Resilience](../cross-cutting/operations/goals/reliability-and-resilience/) | 2 | [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |

### Multi-agent work and human oversight

| Goal | Patterns | Matters most for |
|---|---|---|
| [Multi Agent Orchestration](../cross-cutting/operations/goals/multi-agent-orchestration/) | 10 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Multi Agent Coordination](../cross-cutting/operations/goals/multi-agent-coordination/) | 10 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Agent Handoffs Delegation](../cross-cutting/operations/goals/agent-handoffs-delegation/) | 10 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [Refunds and Billing-Disputes Agent](use-cases/refunds-and-billing-disputes-agent.md), [Insurance Claims Intake and Triage Agent](use-cases/claims-intake-and-triage-agent.md), [Lead Qualification (SDR) Agent](use-cases/lead-qualification-agent.md), [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md), [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Human Oversight Reliability](../cross-cutting/operations/goals/human-oversight-reliability/) | 8 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [Refunds and Billing-Disputes Agent](use-cases/refunds-and-billing-disputes-agent.md), [Insurance Claims Intake and Triage Agent](use-cases/claims-intake-and-triage-agent.md), [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md), [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md), [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |

### Cost and speed

| Goal | Patterns | Matters most for |
|---|---|---|
| [Inference Cost Management](../cross-cutting/operations/goals/inference-cost-management/) | 15 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Cost Efficiency](../cross-cutting/operations/goals/cost-efficiency/) | 15 | [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md), [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Cost Optimization](../cross-cutting/operations/goals/cost-optimization/) | 13 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Cost Tracking](../cross-cutting/operations/goals/cost-tracking/) | 6 | [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) |
| [Real Time Performance](../cross-cutting/operations/goals/real-time-performance/) | 12 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md) |

### Records and observability

| Goal | Patterns | Matters most for |
|---|---|---|
| [Traceability](../cross-cutting/operations/goals/traceability/) | 8 | [Support Resolution Agent](use-cases/support-resolution-agent.md), [Refunds and Billing-Disputes Agent](use-cases/refunds-and-billing-disputes-agent.md), [Insurance Claims Intake and Triage Agent](use-cases/claims-intake-and-triage-agent.md), [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md), [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md), [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md), [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Observability Monitoring](../cross-cutting/operations/goals/observability-monitoring/) | 3 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |
| [Established Framework Adoption](../cross-cutting/operations/goals/established-framework-adoption/) | 6 | [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) |

## Frequently Asked Questions

### Why split operations by agent?

Because a refund agent and an incident-triage agent need different parts of it. A refund agent cares about tool limits, state, and approvals; an incident agent about fault tolerance, rollbacks, and speed.

### Are the mappings final?

No. They come from each agent's described job. As more use-case agents are defined, more goals will be mapped.

## Related

- [All agents by business goal](./)
