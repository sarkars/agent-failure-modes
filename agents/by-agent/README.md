# AI Agents by Business Goal: Find the Failures That Threaten Yours

**Pick the agent you are building, see the business goals it has to protect, and go straight to the failures that threaten each one.** Each agent page links to the goal pages and to the fix on every failure.

## How to use this

1. **Pick your agent** from the table below.
2. **Read its goals.** Each goal is an outcome the agent must protect.
3. **Define your own measure** of each goal (metric, baseline, owner, what counts as failure).
4. **Test against the failures** listed under each goal, and apply the fixes.

## Agents covered

| Agent | What it does | Goals | Patterns |
|---|---|---|---|
| [Customer Support Agents](customer-support-agents.md) | Answer questions, resolve issues, and hand off to people for customers. | 9 | 69 |
| [Healthcare Agents](healthcare-agents.md) | Support diagnosis, treatment planning, medication safety, documentation, and triage. | 9 | 38 |
| [Financial Services Agents](financial-services-agents.md) | Analyze portfolios, check compliance, and support trading and data-heavy decisions. | 5 | 50 |
| [Insurance Agents](insurance-agents.md) | Process claims, support underwriting, and flag fraud. | 5 | 13 |
| [Sales and CRM Agents](sales-and-crm-agents.md) | Score leads, manage deals, and forecast pipeline. | 4 | 16 |
| [Legal and Contract Agents](legal-and-contract-agents.md) | Review, draft, and check contracts and support due diligence. | 8 | 30 |
| [HR and Recruiting Agents](hr-and-recruiting-agents.md) | Screen candidates, generate offers, and support onboarding. | 4 | 19 |
| [DevOps Agents](devops-agents.md) | Watch systems, route alerts, respond to incidents, and manage deployments. | 8 | 30 |
| [Supply Chain Agents](supply-chain-agents.md) | Forecast demand, optimize inventory, route logistics, and assess suppliers. | 5 | 25 |
| [Document Processing Agents](document-processing-agents.md) | Read, classify, extract, and validate information from documents such as loan files. | 14 | 99 |
| [Content and Marketing Agents](content-and-marketing-agents.md) | Produce and manage content, keep it on-brand, and keep it compliant. | 4 | 18 |

## Specific use-case agents (with goal definitions)

These pages define business goals and failures for one concrete agent, with measures, severities, and hand-over triggers. More are coming.

| Agent | What it does | Goals | Customer-facing |
|---|---|---|---|
| [Support Resolution Agent](use-cases/support-resolution-agent.md) | A chat agent that resolves common customer issues (order status, account questions, plan changes) using the company's systems, and hands off to a person when it should | 4 | Yes |
| [Refunds and Billing-Disputes Agent](use-cases/refunds-and-billing-disputes-agent.md) | An agent that handles refund requests and billing disputes: checks the customer's plan and records, applies policy, and issues or recommends credits within set limits | 4 | Yes |
| [Insurance Claims Intake and Triage Agent](use-cases/claims-intake-and-triage-agent.md) | An agent that takes a first notice of loss, collects the facts, and routes the claim to the right queue at the right priority | 5 | Yes |
| [Lead Qualification (SDR) Agent](use-cases/lead-qualification-agent.md) | An agent that talks to inbound or outbound leads, finds out whether there is a fit, and hands qualified leads to a salesperson with the facts | 4 | Yes |
| [DevOps Incident Triage Agent](use-cases/incident-triage-agent.md) | An agent that reads alerts, classifies incidents, notifies the right on-call person, and takes only safe, pre-approved actions | 4 | No |
| [Mortgage Document Verification Agent](use-cases/mortgage-document-verification-agent.md) | An agent that reads a loan file, extracts the data, checks documents against each other, flags problems, and routes exceptions to an underwriter | 4 | No |
| [Accounts-Payable Invoice Processing Agent](use-cases/invoice-processing-agent.md) | An agent that reads vendor invoices, matches them to orders and receipts, and prepares or releases payments within set limits | 4 | No |
| [Multi-Agent Research and Report Agent](use-cases/research-report-agent.md) | A team of cooperating agents that gathers sources, analyzes them, and writes a sourced report for a business reader | 4 | No |

Operations failures are split by concern and by agent in [operations by agent](operations-by-agent.md).

## Not covered yet

| Agent | Status |
|---|---|
| Coding agents | No written patterns. Six candidates are in the [human-machine interface roadmap](../by-capability/human-machine-interface/roadmap/agent-types.md) |
| E-commerce and retail agents | Planned goal, no written patterns |
| Data-extraction and customer-support (duplicate folders) | Folders exist with no patterns; see the customer support and document processing pages |

## Every agent needs these

| Area | What it covers | Patterns |
|---|---|---|
| [Security](../cross-cutting/security/) | Prompt injection, data leakage, tool and credential abuse | 75 |
| [Accuracy](../cross-cutting/accuracy/) | Hallucination, reasoning quality, context management | 66 |
| [Governance](../cross-cutting/governance/) | Oversight, approvals, policy, and audit | 33 |
| [Operations](../cross-cutting/operations/) | Cost, memory, tools, state, handoffs, and reliability | 409 |
| [Learning](../cross-cutting/learning/) | Feedback, in-context learning, and safe adaptation | 12 |

## Frequently Asked Questions

### Why organize by business goal?

Because teams are accountable for outcomes, not for technical failure types. A goal view lets you ask what could stop this agent from achieving what it is for.

### Are the goals here the same as my business goals?

No. These are the goals the library uses to group failures. Your own goals, metrics, and baselines have to be defined with your business owners.

## Related

- [All agent failure patterns](../)
- [Human-machine interface](../by-capability/human-machine-interface/)
