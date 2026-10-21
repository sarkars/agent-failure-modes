# Outbound Messaging Agents: Goal, Metrics, and Patterns

> **Goal:** Outbound texts and calls respect consent, quiet hours, and suppression lists.

> **Read this first.** This family is design guidance, not legal advice. Consent, calling hours, and do-not-call rules differ by country and state and change over time. A lawyer must review your consent wording, lists, and schedules before launch.

## Why this family exists
An agent that starts the conversation can reach people who never agreed to it, at hours they never expected, or after they said stop. This family covers the three checks that must run before any outbound text or call is sent.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Messages sent without recorded consent | Set with counsel | [marketing texts without consent](failures/marketing-texts-without-consent.md) |
| Contacts outside permitted hours | Set with counsel | [quiet hours and time zones ignored](failures/quiet-hours-and-time-zones-ignored.md) |
| Contacts to suppressed numbers | Set with counsel | [do-not-call lists not checked](failures/do-not-call-lists-not-checked.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Marketing texts without consent](failures/marketing-texts-without-consent.md) | Sends promotional texts to numbers that never opted in, because the send step never checks a consent record (needs review) |
| [Quiet hours and time zones ignored](failures/quiet-hours-and-time-zones-ignored.md) | Schedules in the sender's time zone or guesses the recipient's, and reaches people at night (needs review) |
| [Do-not-call lists not checked](failures/do-not-call-lists-not-checked.md) | Contacts opted-out numbers because lists are checked once per campaign or not across channels (needs review) |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/service-and-vertical-patterns.md).

## Related
- [Voice receptionist agents](../voice-receptionist-agents/README.md)
- [Privacy and governance](../privacy-and-governance/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
