# Unclear Next Step

## Issue: User does not know what happens next.

**Frequency**: Rare

**Symptoms**
- User asks 'now what?' or repeats request.
- Agent marks a multi-step process as underway (e.g., "your refund is processing") but never states an expected timeline, owner, or how the user will be notified.
- User sends a follow-up message shortly after a turn the agent considered resolved, indicating the closing message didn't clearly communicate that the conversation was complete.

**Root Cause**
User does not know what happens next.

**Example**
```
Agent: "I've submitted your refund request."
User: "Okay... so is that it? Do I need to do anything else?"
Agent: "Your request has been submitted."
User: "When will I actually get the money back?"
```

**Contributing Factors**
- No mandatory next-step slot in the response template, so a response can be sent that's otherwise complete but omits the forward-looking statement.
- Multi-turn/multi-system processes (refunds, ticket escalations) have no persistent status indicator, so users lose track of where they are after the triggering turn.
- Closing/resolution messages aren't gated by a template requiring an explicit "what happens next" statement before the conversation is marked resolved.
- Agent prioritizes brevity over completeness, dropping the next-step sentence to keep the response short.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Multi-step process closing turn | Agent submits a refund request | Response states expected timing, how the user will be notified, and whether further action is needed | Response ends with "submitted"/"processing" and no next-step detail |
| Resolution closing message | Agent believes the issue is fully resolved | Closing message explicitly states resolution status and confirms no further action is needed | User sends an immediate follow-up asking "is that it?" or repeats the original request |
| Ambiguous-ending detection | Agent gives a complete factual answer with no natural next step | Response still closes with either "no further action needed" or an offer of further help | Response ends abruptly with no next-step framing at all |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Next-step statement coverage (eval set) | >95% | Percentage of eval non-terminal turns that include an explicit next-step statement |
| "Now what" / repeat-request rate (eval set) | <2% | Percentage of eval conversations where a follow-up user turn indicates confusion about next steps |
| Post-resolution follow-up rate (eval set) | <8% | Percentage of eval conversations where the user sends another message immediately after the agent marks the conversation resolved |

---

## Mitigation Strategies

### Prevention
1. **Mandatory next-step statement template**: require every agent turn that doesn't end the conversation to close with an explicit, concrete next-step statement (what happens next, who does it, expected timing), since the failure is the agent completing an action or answer without stating what the user should expect afterward. Trade-off: adds a formulaic closing line to every response, which can feel repetitive or scripted in short exchanges.
2. **Status-line pattern for multi-step processes**: for any process spanning multiple turns or systems (e.g., "your refund is processing"), include a persistent status indicator (current step, remaining steps, ETA) rather than a one-time statement, since users lose track of where they are in a process that started several turns ago. Trade-off: requires the agent to track and re-surface process state, adding complexity for state that must stay in sync with backend reality.
3. **Ambiguous-ending detection before send**: before finalizing a response, check whether it ends on an action/information statement without a directive next step, and append one if so, since many "unclear next step" instances come from a response that is otherwise complete but simply omits the forward-looking sentence. Trade-off: naive rule-based appending can produce redundant or nonsensical next-step lines when the conversation is genuinely finished.

### Detection & Response
1. **"Now what" / repeat-request phrase detection**: scan for the literal behavioral signature — user asking "now what," "what happens next," or repeating their original request shortly after an agent turn. Response: in real time, have the agent immediately provide the missing next-step statement rather than repeating prior content.
2. **Turn-after-resolution follow-up rate**: track how often users send another message immediately after the agent marks a conversation resolved, since a healthy resolution should end the conversation; a high rate suggests the closing turn isn't clearly communicating status. Response: sample and check whether the closing turn included a next-step statement.
3. **CSAT comment mining for confusion language**: mine CSAT free-text for confusion-indicating phrases ("wasn't sure what to do," "didn't know if it was fixed") and treat as a distinct signal from general dissatisfaction. Response: add matched transcripts to the eval set as labeled examples.

### Architecture Patterns
1. **Response-composer with mandatory next-step slot**: structure response generation with a required "next step" field that must be populated, even if the value is "no further action needed," before a response can be sent, making an unclear ending structurally unreachable rather than prompt-dependent.
2. **Process-state tracker surfaced every turn**: for multi-step workflows, maintain an explicit state object (step N of M, current owner, ETA) that's rendered into every relevant response automatically, decoupling "the user knows where they stand" from the model's freeform recall of earlier turns.
3. **Conversation-closure confirmation gate**: before marking a conversation resolved, require an explicit closing message template that states resolution status and next steps, if any, gating the "closed" state transition on that message actually being sent.

### Metrics
1. **now_what_phrase_rate**: Target: <2% of conversations; Alert on >4% weekly
2. **post_resolution_followup_rate**: Target: <8%; Alert on >15%
3. **next_step_statement_coverage**: Target: >95% of non-terminal turns include an explicit next-step statement; Alert on <85%
4. **confusion_csat_mention_rate**: Target: <3%; Alert on >6%

### Alerts
1. **Now-What Rate Spike** (P3): Condition - now_what_phrase_rate exceeds 4% over 7 days. Action: sample transcripts, check next-step template compliance on recent prompt changes.
2. **Post-Resolution Follow-up Surge** (P2): Condition - post_resolution_followup_rate exceeds 15% weekly. Action: review the closing-message template for clarity, check process-state tracker accuracy.
3. **Next-Step Coverage Drop** (P2): Condition - next_step_statement_coverage falls below 85% in automated scan. Action: investigate the response-composer regression, redeploy with mandatory slot enforcement.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| now_what_phrase_rate | >4% weekly |
| post_resolution_followup_rate | >15% weekly |
| next_step_statement_coverage | <85% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Now-What Rate Spike | now_what_phrase_rate exceeds 4% over 7 days | Low |
| Post-Resolution Follow-up Surge | post_resolution_followup_rate exceeds 15% weekly | Medium |
| Next-Step Coverage Drop | next_step_statement_coverage falls below 85% in automated scan | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
