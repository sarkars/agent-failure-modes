# Multi-Agent Handoff Drops Escalation Urgency Flag Between Triage Bot and On-Call Clinician Queue

## Issue: A Telehealth Triage Bot That Reasons, in Its Own Free-Text Assessment, That a Patient's Symptoms Warrant Urgent Same-Hour Clinician Contact Hands the Case to an On-Call Clinician Queue Through a Structured Ticket That Carries Only a Generic Priority Field, So the Urgency the Bot Actually Concluded Never Reaches the Queue's Sort Order

**Frequency**: Occasional

**Symptoms**
- The triage bot's internal assessment text states the case should be seen "urgently" or "within the hour," but the structured ticket it creates is queued at standard priority alongside routine follow-ups
- Re-reading the bot's full triage transcript, after the fact, clearly shows it reasoned the case as urgent; the structured ticket fields show no trace of that conclusion
- The on-call clinician queue sorts and surfaces cases solely by the structured priority field, never by re-parsing the triage bot's narrative assessment
- The gap concentrates on symptom presentations that do not map to one of the queue's small set of pre-defined high-priority ticket categories, even though the bot's reasoning correctly identified urgency from the specific combination of symptoms described
- The delay is caught only when a patient calls back to report worsening symptoms, or when a clinician happens to open the ticket and reads the full transcript rather than relying on the queue's priority sort

**Root Cause**
The triage bot and the on-call clinician queue communicate through a structured ticket schema with a small, fixed set of priority values, rather than through the bot's full assessment. When the bot's actual urgency conclusion is more nuanced or specific than the schema's categories capture -- for example, urgency driven by a particular symptom combination the schema has no dedicated flag for -- that conclusion exists only in the bot's narrative reasoning and is never mapped into the structured field the queue actually sorts on, so the downstream system has no way to act on it.

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
