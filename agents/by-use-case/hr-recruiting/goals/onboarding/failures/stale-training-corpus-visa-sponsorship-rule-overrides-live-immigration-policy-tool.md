# Stale Training-Corpus Visa-Sponsorship Rule Overrides Live Immigration-Policy Tool

## Issue: An Onboarding Agent Answering a New International Hire's Question About Visa-Sponsorship Steps, Timelines, or Document Requirements Answers from Generic Immigration-Process Knowledge It Absorbed During Pretraining Rather Than Calling the Company's Live Immigration-Policy Tool, Producing Guidance That Reflects an Outdated Visa Category, Processing Timeline, or Document List Instead of the Company's Actual Current Sponsorship Process

**Frequency**: Common

**Symptoms**
- The agent states specific visa-category names, processing timelines, or document requirements that match generic, commonly-referenced immigration knowledge rather than the company's actual current sponsorship policy and vendor process
- The same onboarding session has a live immigration-policy tool available and successfully callable, but the tool is never invoked before the agent answers the visa question
- When the agent is explicitly instructed to call the immigration-policy tool before answering, the tool's current response differs from what the agent originally stated, in document list, required lead time, or current processing stage
- New hires report confusion or missed deadlines after following the agent's stated timeline, which does not match what the company's immigration counsel or HR mobility team later confirms is the actual current process
- The discrepancy is most pronounced for recently changed sponsorship steps (a new internal pre-filing step, a changed document checklist, a revised internal SLA with outside counsel) that postdate the model's training data but are reflected in the live policy tool

**Example**
```
New international hire, mid-onboarding, asks the onboarding agent what documents and timeline to expect for their visa sponsorship process
Onboarding agent has a live immigration-policy tool available that returns the company's current sponsorship workflow, including a document checklist and an internal SLA with outside immigration counsel
Agent answers directly from generic pretraining knowledge about typical employer-sponsored visa processes, citing a document list and timeline that do not include a document the company added eight months ago after an internal compliance review, and does not call the live policy tool at all
New hire submits the document set the agent described, missing the additional document the live tool would have surfaced
Filing is delayed when outside counsel flags the missing document weeks later, pushing the new hire's effective work-authorization date past their original expected timeline
Mobility team traces the gap to the onboarding agent's answer and confirms the live policy tool, never called, had the correct and current document list the entire time
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Failure-mode taxonomies for LLM systems identify reliance on parametric/pretrained knowledge over an available live tool as a distinct and recurring failure category, particularly for domains with frequently updated rules or policies that postdate the model's training cutoff | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Agent-environment interaction research finds that agents frequently default to internally generated answers even when an authoritative external tool for the same question is available and callable, especially when the question can be plausibly answered from general knowledge | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |
| Analyses of cascading agent failures show that an initial failure to invoke an available tool for a domain-specific, frequently-changing policy question propagates uncorrected through the rest of the interaction unless the agent is explicitly required to verify tool availability before answering | [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370) |

**Contributing Factors**
- The agent's prompt does not explicitly require it to check for and call an available live policy tool before answering any compliance-relevant immigration question
- Visa-sponsorship rules, document checklists, and counsel SLAs change more frequently than the agent's training data is refreshed, and the agent has no built-in signal indicating its background knowledge here may be stale
- The agent's general immigration-process knowledge is fluent and plausible enough that neither the new hire nor a reviewing HR coordinator has reason to suspect the answer is not sourced from the live tool
- No automated check compares the agent's stated document list or timeline against the live policy tool's current values before the answer is sent to the new hire

---

## Mitigation Strategies

1. **Mandatory Tool-First Policy for Compliance Questions**: Require the agent to call the live immigration-policy tool for any visa-, sponsorship-, or work-authorization-related question before generating any answer, and prohibit answering from general knowledge when the tool is available
2. **Tool-Call Verification Gate**: Add an automated check that blocks any onboarding response touching visa or sponsorship topics from being sent unless a corresponding live policy-tool call occurred earlier in the same turn
3. **Explicit Staleness Disclaimer as Fallback Only**: If the live policy tool is genuinely unavailable, require the agent to state explicitly that it could not confirm current policy and to direct the new hire to HR mobility rather than answering from general knowledge
4. **Periodic Drift Audit**: Regularly compare a sample of the agent's visa/sponsorship answers against the live policy tool's current values to detect cases where general knowledge was used instead of the tool, even when the tool was technically available

### Metrics
- Percentage of visa/sponsorship-related onboarding answers preceded by a live policy-tool call in the same turn
- Number of document-list or timeline discrepancies found between agent answers and the live policy tool during periodic drift audits
- New-hire-reported visa-process delays traced to onboarding-agent guidance that did not match the live policy tool

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Visa answer without tool call | Agent answers a visa/sponsorship question without a corresponding live policy-tool call in the same turn | P1 | Withhold the response from the new hire; regenerate with the live tool call enforced |
| Drift audit discrepancy | Periodic audit finds an agent answer diverges from the live policy tool's current document list or timeline | P1 | Notify HR mobility team to contact any new hires who may have received the divergent answer |
| Tool unavailable fallback used | Agent answers a visa/sponsorship question using the unavailable-tool disclaimer path | P3 | Confirm the new hire was directed to HR mobility; investigate tool outage |

---

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
- [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370)
