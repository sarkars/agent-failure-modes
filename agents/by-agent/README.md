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
