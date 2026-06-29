# Multi-Agent Handoff Drops Failed-Resolution-Attempt Detail Between Intake Bot and Specialist Deflection Agent

## Issue: An Intake Bot Hands Off a Conversation to a Specialist Deflection Agent Using a Structured Intent Label, but the Free-Text Detail That the Customer Already Attempted and Failed at the Standard Self-Service Step Is Not Part of That Structured Schema, So the Specialist Agent Re-Suggests the Same Failed Step

**Frequency**: Common

**Symptoms**
- The specialist deflection agent suggests the same self-service article or action the customer described having already tried, even though that detail appears in the conversation the intake bot handled moments earlier
- The structured handoff payload between intake bot and specialist agent contains only an intent or category label (e.g., "billing-refund"), with no field carrying the free-text detail that the standard remedy was already attempted and failed
- Specialist agents operating purely from the structured handoff fields produce a materially higher repeat-suggestion rate than specialist agents given the full upstream transcript alongside the structured fields
- Customers re-describe the same already-tried detail a second time to the specialist agent, and that repetition is logged as new information rather than as evidence the handoff dropped it
- The mismatch concentrates on intents where the standard remedy is narrow (e.g., a single refund-request flow), since a single missed detail is more likely to trigger an exact repeat suggestion than in intents with many candidate remedies

**Root Cause**
Structured handoff schemas between staged agents are designed to carry the fields a downstream agent's decision logic explicitly consumes, and a free-text detail like "I already tried that and it didn't work" has no corresponding field unless the schema was deliberately built to carry it. Because the specialist agent's deflection logic operates only over its structured inputs, a detail that exists in the upstream transcript but was never extracted into the schema is invisible to it, even though the same model, given the full transcript, would readily recognize and act on it.

**Example**
```
Customer tells the intake bot they requested a refund three days ago through the standard self-service flow and it never posted to their statement
Intake bot classifies the conversation as intent=billing-refund and hands off to the specialist billing-deflection agent with that structured label
Specialist agent, working only from intent=billing-refund, surfaces the standard "how to request a refund" self-service article
Customer repeats that they already did this and it failed, now for the second time across two different agents
Conversation eventually escalates to a human agent who discovers the original refund request is still stuck in a processing queue, a detail neither bot ever surfaced
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify information loss at agent-to-agent handoff boundaries, where a downstream agent's structured input omits context the upstream agent had available, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent architectures document that handoff interfaces between specialized agents must be deliberately designed to carry task-relevant context beyond a single classification label, or downstream agents systematically underperform agents with full context access | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed schema is a primary mechanism by which task-relevant detail present upstream fails to reach a downstream stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- Handoff schema between intake bot and specialist deflection agent carries only an intent/category label, with no field for "standard remedy already attempted and failed"
- Specialist agent's deflection logic is implemented to consume only the structured handoff fields, not the full upstream transcript, for latency and cost reasons
- No detection step flags when a customer's free-text message describing a prior failed attempt was present in the upstream transcript but absent from the structured handoff

---

## Mitigation Strategies

1. **Add an Attempted-Remedy Field to the Handoff Schema**: Require the intake bot to extract and pass forward a structured "remedy already attempted" field whenever the conversation contains language indicating the customer tried the standard self-service step, rather than relying solely on an intent label
2. **Specialist Agent Reviews Upstream Transcript Before First Suggestion**: Require the specialist deflection agent's first suggestion to be checked against the full upstream transcript (or the attempted-remedy field) before surfacing the standard remedy, not just the structured intent
3. **Repeat-Suggestion Detection**: Detect when a specialist agent is about to suggest a remedy whose description closely matches language already present in the upstream transcript as something the customer tried, and block that suggestion pending review
4. **Track Cross-Agent Repeat-Suggestion Rate**: Continuously measure how often a specialist agent suggests a remedy the customer described as already attempted to the intake bot, segmented by whether the handoff included an attempted-remedy field

### Metrics
- Rate of specialist-agent first suggestions that match a remedy the customer already described as attempted in the intake conversation
- Repeat-suggestion rate, segmented by presence vs. absence of an attempted-remedy field in the handoff
- Escalation rate to a human agent following a repeat-suggestion incident

### Alerts
- A specialist agent suggests a remedy that exact-matches language in the upstream transcript describing it as already attempted and failed → P2
- Repeat-suggestion rate across a rolling window exceeds the defined threshold for any single intent category → P2
- Handoff payload for a conversation containing "already tried" language is missing the attempted-remedy field → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
