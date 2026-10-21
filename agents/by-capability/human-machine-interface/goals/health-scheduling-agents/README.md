# Health Scheduling Agents: Goal, Metrics, and Patterns

> **Goal:** Health scheduling agents send urgent problems to a person, confirm that critical instructions were understood, and book the right visit with the right clinician.

> **Read this first.** This family is design guidance, not clinical or legal advice. Triage wording, medication instructions, and scheduling rules must come from clinicians and be reviewed by clinical and legal staff before use. A chat assistant should not decide urgency or give medication advice on its own.

## Why this family exists
Patients ask a scheduling or messaging assistant questions where a loose answer has real cost: a delayed visit for warning signs, a misread medication instruction, a visit booked with someone who cannot treat the problem. This family covers failures specific to patient scheduling and instruction chats.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Triage agreement with clinician review | Set with clinicians | [triage wording understates or overstates urgency](failures/triage-wording-understates-or-overstates-urgency.md) |
| Comprehension check pass rate on key instructions | Set with clinicians | [medication instructions misunderstood](failures/medication-instructions-misunderstood.md) |
| Rescheduled-for-wrong-type rate | Set from baseline | [scheduling picks the wrong provider or visit type](failures/scheduling-picks-the-wrong-provider-or-visit-type.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Triage wording understates or overstates urgency](failures/triage-wording-understates-or-overstates-urgency.md) | Tells someone with warning signs to book next week, or sends everyone to the ER (needs review) |
| [Medication instructions misunderstood](failures/medication-instructions-misunderstood.md) | Reminders leave out timing, food, or the missed-dose step, and nobody checks understanding (needs review) |
| [Scheduling picks the wrong provider or visit type](failures/scheduling-picks-the-wrong-provider-or-visit-type.md) | Books a follow-up as a new visit, or with a clinician who cannot treat the issue |

## Planned (not yet written)
Results delivered without context. See the [roadmap](../../roadmap/service-and-vertical-patterns.md).

## Related
- [Vulnerable users](../vulnerable-users/README.md)
- [Human handoff](../human-handoff/README.md): the person route
- [Stakes calibration](../stakes-calibration/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
