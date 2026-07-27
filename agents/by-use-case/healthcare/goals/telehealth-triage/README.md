# What Are the Most Common Telehealth-Triage Failures in AI Agents?

**Telehealth-triage failures happen when an agent's internal reasoning correctly identifies urgency based on symptoms, but the structured routing ticket it generates is queued at a generic priority level that the downstream clinician queue sorts on, so the urgency conclusion never reaches the queue's sort order; or when vital signs are simply unavailable (no home device), and the agent treats the missing data as a neutral signal rather than as elevated uncertainty requiring escalation.** A triage bot reasoning that acute stroke symptoms require same-hour contact can be silently queued behind routine complaints because the structured priority field has no category for "emergency that doesn't fit a pre-defined flag."

## Scope

The 2 telehealth-triage patterns split into distinct failure mechanisms: information-loss at the triage-to-queue handoff (the structured schema is too coarse to capture the bot's actual urgency reasoning) and missing-data handling (vitals absent is treated as normal rather than as unknown).

## When Telehealth-Triage Matters

- Symptom presentations that do not map to one of the queue's small set of pre-defined high-priority categories, even though the triage logic correctly identifies urgency
- Remote or telehealth encounters without connected monitoring devices, where vital signs are unavailable
- Workflows where the triage bot and the on-call clinician queue communicate through a structured ticket rather than through the bot's full assessment

## Cross-Pattern Insight

Both telehealth-triage patterns reflect a gap between the triage bot's actual reasoning and what the downstream routing system can act on. The bot reasons "this symptom combination warrants urgent contact" but the ticket schema has no urgency value more granular than the generic "Urgent" flag shared with non-emergent same-day complaints. The bot notes that vitals are unavailable, but the acuity scoring defaults that absence to normal rather than elevating uncertainty. The recurring mitigation is making urgency and uncertainty explicit in the routing layer: expand the structured urgency schema to capture the bot's actual reasoning, treat missing objective data as a signal for escalation rather than a default-to-normal imputation, and maintain symptom-combination hard-escalation rules for known high-risk patterns.

## Frequently Asked Questions

### How do you prevent urgent symptoms from being queued at routine priority?
Expand the structured priority schema beyond "urgent" to capture gradations (e.g., "urgent-neurological," "urgent-cardiac," "urgent-trauma"); run a reconciliation check before the ticket enters the queue comparing the bot's assessment text for urgency language against the structured field, and route any mismatch to immediate clinician review; maintain hard-escalation rules for symptom combinations known to warrant immediate contact (acute neurological deficits, chest pain + dyspnea, altered mental status).

### How should missing vitals be treated in escalation decisions?
Vital signs are objective data; their absence increases diagnostic uncertainty. A patient reporting dyspnea without a recorded oxygen saturation should be escalated to in-person/urgent evaluation, not treated as if oxygen saturation were known-normal. Mitigate by explicitly representing missingness as a distinct state in the acuity model and raising acuity tier when key objective data is absent.

### How do you catch triage-to-queue handoff gaps?
Track time-to-first-clinician-view by symptom category (not just priority value) to surface cases where urgent-language symptoms languish in the queue; run automated checks comparing bot assessment urgency language against the ticket's structured priority field; implement a pre-queue gate that flags any mismatch for manual routing adjustment.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Multi-Agent Handoff Drops Escalation Urgency Flag Between Triage Bot and On-Call Clinician Queue](failures/multi-agent-handoff-drops-escalation-urgency-flag-between-triage-bot-and-on-call-clinician-queue.md) | Bot's urgency reasoning exists only in narrative; structured ticket's generic priority field does not capture it |
| [Remote Vital-Sign Absence Blindness in Telehealth Triage](failures/remote-vital-sign-absence-blindness.md) | Missing vitals (no home device) treated as neutral/normal rather than unknown, lowering acuity score inappropriately |

**Total: 2 patterns**

## Related Goals

- [Mental-Health Triage](../mental-health-triage/) — shares multi-agent handoff information-loss mechanism and missing-data-handling gaps
- [Diagnosis Safety](../diagnosis-safety/) — telehealth-triage outputs feed downstream diagnosis; missing vitals reduce diagnostic certainty upstream as well
