# Failure to Ask for Clarification

## Issue: Agent Proceeds Despite Ambiguity

**Frequency**: Common (6.8% of MAS failures)

**Symptoms**
- Agent makes assumptions instead of asking
- Ambiguous requirements interpreted arbitrarily
- Different agents have different interpretations
- Task fails due to misunderstood requirements

**Root Cause**
Agent fails to ask for clarification when facing ambiguous or incomplete information. Instead of seeking clarity, the agent proceeds with assumptions that may be incorrect, leading to task failures that could have been avoided.

**Example**
```
Task: "Update the customer's address"

Ambiguity: Which customer? Which address field? What's the new value?

Agent behavior:
Agent: "I'll update the address now."
       [Searches for most recent customer]
       [Updates shipping address with billing address]
       "Done! Address has been updated."

Expected behavior:
Agent: "I need clarification:
       1. Which customer should I update?
       2. Which address (shipping or billing)?
       3. What is the new address?"

Result: Wrong customer's address changed incorrectly
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Failure to ask for clarification accounts for 6.8% of failures
- Part of "Inter-Agent Misalignment" category (32.3% total)
- Often cascades into larger task failures

**Clarification Failure Types**
- **Assumption making**: Guessing instead of asking
- **Partial understanding**: Proceeding with incomplete info
- **Overconfidence**: Believing interpretation is correct
- **Efficiency bias**: Avoiding "unnecessary" questions

**Contributing Factors**
- Training bias toward being "helpful" immediately
- No clear protocol for when to seek clarification
- Pressure to complete tasks quickly
- Unclear escalation paths for ambiguity
- Lack of uncertainty awareness

## Mitigation Strategies

### Prevention
1. **Ambiguity scoring before execution**: Before executing any request that references an unspecified entity (e.g., "the customer," "the address" without a customer ID or field), score the request for missing required slots and block execution until they're filled. Trade-off: adds a pre-flight latency cost to every request, even unambiguous ones.
2. **Mandatory field schemas for high-risk actions**: Define required fields (customer ID, address type, new value) for state-changing operations like the address update in the example, so the agent cannot silently default to "most recent customer" or "shipping address." Trade-off: requires enumerating required fields for every action type in advance, which doesn't scale to novel actions.
3. **Reward clarification in training/prompting**: Since training biases the agent toward being "helpful" immediately, explicitly instruct via system prompt that asking a clarifying question is a successful outcome, not a failure to act. Trade-off: over-tuned, this produces an agent that asks too many trivial questions, frustrating users.

### Detection & Response
1. **Assumption-without-verification flags**: Scan agent traces for language patterns like "I'll assume," "most likely," or actions taken on an unresolved reference (e.g., "the customer" resolved via a search rather than an explicit ID) and flag for review.
2. **Post-hoc correction rate**: Track how often users correct the agent's interpretation immediately after an action (as in the address example) — a high correction rate on a given task type indicates the clarification threshold is set too low.
3. **Multi-agent interpretation divergence**: In systems with multiple agents processing the same ambiguous request, compare their interpretations; divergence indicates the request needed clarification and none of the agents caught it.

### Architecture Patterns
1. **Human-in-the-loop clarification gate**: Insert a mandatory confirmation step for any action that resolves an ambiguous reference (customer, field, value) before execution, modeled on the "Expected behavior" block in the example. Deployment consideration: only gate state-changing actions, not read-only queries, to avoid annoying users.
2. **Structured clarification templates**: Use a fixed question template that itemizes exactly which slots are missing rather than a freeform "can you clarify?" — reduces back-and-forth. Deployment consideration: requires per-domain template authoring.
3. **Confidence-threshold routing**: Route any request whose slot-filling confidence falls below a set threshold to a clarification branch instead of the execution branch. Deployment consideration: needs a calibrated confidence signal, which most agents don't natively expose.

### Metrics
1. **clarification_request_rate**: Target: 8-15% of ambiguous-flagged requests trigger a clarifying question; Alert if < 3% (under-asking) or > 30% (over-asking).
2. **post_action_correction_rate**: Target: < 2% of completed actions require user correction of interpretation; Alert if > 5% over rolling 100 actions.
3. **required_field_completeness**: Target: 100% of state-changing actions have all mandatory fields resolved before execution; Alert on any execution with an unresolved required field.
4. **wrong_target_incident_rate**: Target: < 0.5% of actions affect the wrong entity (e.g., wrong customer); Alert on any single incident for high-risk action types.

### Alerts
1. **Unresolved Required Field Executed** (P1): Condition - an action with a defined required-field schema executes with one or more fields unresolved or defaulted. Action: halt the action pipeline for that task, roll back if already executed, and escalate to a human reviewer.
2. **Correction Spike** (P2): Condition - post_action_correction_rate exceeds 5% over a rolling 100-action window for a given task type. Action: review recent traces for that task type, tighten the ambiguity-detection rules, and consider adding it to the mandatory-clarification list.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 2.2: Fail to Ask for Clarification (6.8%)
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Assumptions leading to liability
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Misinterpretation of instructions
