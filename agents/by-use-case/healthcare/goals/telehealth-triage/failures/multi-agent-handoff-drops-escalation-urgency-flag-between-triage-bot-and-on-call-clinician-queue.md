# Multi-Agent Handoff Drops Escalation Urgency Flag Between Triage Bot and On-Call Clinician Queue

## Issue: A Telehealth Triage Bot That Reasons, in Its Own Free-Text Assessment, That a Patient's Symptoms Warrant Urgent Same-Hour Clinician Contact Hands the Case to an On-Call Clinician Queue Through a Structured Ticket That Carries Only a Generic Priority Field, So the Urgency the Bot Actually Concluded Never Reaches the Queue's Sort Order

**Frequency**: Occasional

**Symptoms**
- A stroke-consistent symptom combination receives the same "Urgent" ticket priority as a same-day complaint about ear pain, because both are more urgent than routine follow-up and the schema stops distinguishing past that point
- Within the "Urgent" tier the queue orders strictly by submission time, so a time-critical case submitted after several non-emergent "Urgent" tickets waits behind all of them
- The bot's own assessment text draws the exact clinical distinction a person would draw -- specific, readable, and correct -- immediately adjacent to the structured field that discards it
- The patient receives an automated reply to wait for a callback, which reinforces the queue's ordering rather than surfacing any signal that the wait itself is unsafe
- The gap is unrelated to any single symptom category -- any presentation whose urgency comes from a specific, unusual combination rather than a routine same-day complaint lands in the same undifferentiated top tier

**Root Cause**
The queue's priority field was built to differentiate ordinary telehealth demand -- same-day versus next-available versus routine follow-up -- and "Urgent" is its ceiling, covering everything from a minor same-day complaint to a genuine emergency, because until this class of presentation appeared, nothing needed a tier above same-day. Within that top tier the queue falls back to submission-time ordering, since the schema was never asked to differentiate degrees of urgency inside its own top category. The bot's own assessment can and does distinguish a stroke presentation from an ear infection, but that distinction has nowhere to go once it is mapped down into a field that was never designed to carry it.

**Example**
```
Patient reports new-onset unilateral facial drooping and slurred speech during a telehealth intake chat
Triage bot's internal assessment reasons: "Symptom combination is consistent with possible acute stroke presentation, requires immediate clinician contact, do not route as standard urgent care follow-up"
Bot creates a structured ticket with priority field set to "Urgent" -- the same value used for non-emergent same-day complaints like ear pain or minor lacerations
On-call queue sorts all "Urgent" tickets by submission time, placing this ticket behind several earlier, genuinely non-emergent "Urgent" tickets
Clinician reaches the ticket forty minutes later, reading the full transcript only then, by which point the patient had already been advised by the bot's auto-reply to "wait for a callback"
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a conclusion established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent simply reasoning incorrectly | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Tiered multi-agent healthcare systems are shown to require explicit, structured escalation signals between agent tiers because narrative assessments alone do not reliably propagate urgency to downstream routing logic | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |
| Surveys of LLM-based agents in medicine identify triage-to-clinician handoff fidelity as a distinct reliability challenge from triage accuracy itself | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- The ticket schema's priority field has a small, fixed set of values that does not capture the full range of urgency conclusions the triage bot's reasoning can reach
- The on-call queue's sort and surfacing logic acts only on the structured priority field, never on the bot's narrative assessment text
- No reconciliation step compares the urgency language in the bot's assessment against the structured priority value before the ticket enters the queue

---

## Mitigation Strategies

1. **Expanded Structured Urgency Schema With Free-Text-to-Field Mapping**: Replace the small fixed priority set with a schema granular enough to capture time-to-contact urgency directly, and require the bot's structured ticket to be generated from the same reasoning step that produced its narrative assessment, not a separate, coarser classification pass
2. **Pre-Queue Urgency Reconciliation Check**: Before a ticket enters the on-call queue, automatically scan the bot's full assessment text for urgency language and flag any mismatch against the structured priority field for immediate clinician review
3. **Symptom-Combination Hard Escalation Rules**: Maintain an explicit, regularly updated list of symptom combinations (such as acute neurological deficit patterns) that force the highest structured priority and an immediate clinician page, regardless of how the bot's general priority classification resolves
4. **Time-to-First-Clinician-View Tracking by Symptom Category**: Track and review wait time from ticket creation to first clinician view, broken out by symptom category rather than only by structured priority, to surface urgency-schema gaps

### Metrics
- Rate of tickets where the bot's assessment text contains urgency language not reflected in the structured priority field
- Time from ticket creation to first clinician view, stratified by symptom presentation rather than only priority value
- Rate of patient callbacks reporting worsening symptoms after a ticket was queued at standard priority

### Alerts
- A ticket's assessment text contains hard-escalation symptom language while the structured priority field is not set to the highest tier → P1
- Time-to-first-clinician-view for a high-urgency-language ticket exceeds the defined threshold → P1
- Mismatch rate between assessment urgency language and structured priority exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
