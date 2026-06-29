# Context-Window Loss Reintroduces Ruled-Out Troubleshooting Step in Long Chat

## Issue: During a Long, Multi-Turn Support Chat Where a Customer Explicitly States Early On That They Have Already Tried a Specific Troubleshooting Step (and It Did Not Work), the Agent Continues the Conversation Through Many More Turns of Diagnostic Questions, and as the Early Turn Falls Out of the Agent's Effective Context, It Re-Suggests the Same Already-Ruled-Out Step Later in the Same Session as if Hearing It for the First Time

**Frequency**: Common

**Symptoms**
- Agent suggests a troubleshooting step the customer explicitly stated, in an earlier turn of the same conversation, that they had already tried and that did not resolve the issue
- The ruled-out step appears verbatim or near-verbatim earlier in the same chat transcript, confirming the information was available in the session and not merely never mentioned
- Customer's response expresses frustration at being asked to repeat something already stated ("I told you I already tried that")
- The re-suggestion tends to occur after many additional turns of diagnostic back-and-forth, consistent with the original statement aging out of the portion of the conversation the model is effectively attending to rather than the agent never having processed it
- Shortening the conversation or re-stating the ruled-out step closer to the point of the repeated suggestion prevents the recurrence, indicating a position-in-context effect rather than a comprehension failure

**Example**
```
Customer opens a chat: "My smart thermostat won't connect to WiFi. I've already power-cycled it twice and reset network settings -- neither worked."
Agent proceeds through 15 more turns of diagnostic questions: router model, firmware version, app version, signal strength, other devices on the network, etc.
On turn 17, agent suggests: "Let's try power-cycling the thermostat and see if that resolves the connection issue"
Customer: "I told you in my very first message that I already power-cycled it. Twice."
Transcript review confirms the original statement was present in turn 1 of the same session and was never contradicted or superseded
The repeated suggestion is best explained by the early turn falling out of the portion of the long conversation the model's response generation was effectively attending to by turn 17, not by the agent failing to read turn 1 at the time
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Performance on tasks requiring use of information from a long context degrades substantially when the relevant information sits earlier in the context rather than at the very start or end, even when the model's context window is nominally large enough to contain it | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Failure-mode taxonomies for LLM systems identify loss of earlier-established facts or constraints across a long interaction as a distinct and recurring category of agentic failure, separate from the model simply never having seen the information | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Survey of hallucination in LLM-based agents notes that long multi-turn interactions are a known risk factor for the model generating content inconsistent with earlier-established facts in the same session | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- No running, explicitly-maintained list of ruled-out troubleshooting steps that persists and is re-injected near the point of generation as the conversation grows long
- Diagnostic-question flow is generated turn-by-turn based on the model's general troubleshooting knowledge rather than being checked against a structured record of what has already been tried in this session
- Customer's original statement was made in passing as part of the opening message rather than as a structured, separately-tracked field, making it easy for it to blend into a long transcript rather than persist as salient state
- No automated check comparing a proposed next troubleshooting step against earlier turns before the agent sends its suggestion

---

## Mitigation Strategies

1. **Structured Ruled-Out-Steps Tracker**: Maintain an explicit, separately-tracked list of troubleshooting steps the customer has stated were already tried, and inject that list into the prompt context near generation time regardless of how long the conversation has grown
2. **Pre-Send Duplicate-Suggestion Check**: Automatically compare any proposed troubleshooting step against the ruled-out-steps tracker before sending, blocking or rewriting suggestions that match an already-tried step
3. **Periodic Context Recap**: Have the agent periodically restate a compact summary of established facts (ruled-out steps, confirmed details) back into its own working context at intervals during long conversations, rather than relying on the full raw transcript to remain equally salient throughout
4. **Conversation-Length Triggered Escalation**: Route conversations exceeding a turn-count threshold to a human agent or to a structured-summary handoff, reducing the window in which early-turn information is at risk of falling out of effective context

### Metrics
- Rate of agent suggestions matching a troubleshooting step the customer explicitly stated earlier in the same session was already tried
- Distribution of turn-distance between a ruled-out statement and its later re-suggestion, to confirm the position-in-context pattern
- Customer-expressed-frustration rate ("I already told you") per long conversation

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Ruled-out step re-suggested | Proposed troubleshooting step matches an already-tried step from earlier in the same session | P2 | Block suggestion; pull from ruled-out-steps tracker instead |
| Long-conversation risk threshold | Conversation turn count exceeds threshold without a context recap having been performed | P3 | Trigger recap injection or human handoff |
| Customer repeats correction | Customer message indicates information was already provided earlier in the session | P2 | Flag conversation for tracker-accuracy review |

---

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
