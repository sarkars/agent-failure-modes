# Travel and Utility Agents: Goal, Metrics, and Patterns

> **Goal:** Travel and utility agents give the real rule, the real status and the next step, and offer a person when a customer is stranded or without service.

> **Read this first.** This family is design guidance, not legal advice. Refund, rebooking and service-credit rules depend on the carrier, the utility, the ticket or plan, and the jurisdiction. Check them against your own policies and with counsel before use.

## Why this family exists
Travelers and customers in an outage are stuck, often at a bad hour, and they ask a bot what to do. A wrong rule or a vague "we are working on it" costs money or leaves them without a plan. This family covers failures specific to travel and utility service chats.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Rebooking outcomes that match the policy; wait to reach a person during disruptions | Set from baseline | [disruption rebooking with wrong rules and no human path](failures/disruption-rebooking-with-wrong-rules-and-no-human-path.md) |
| Outage updates that give cause, area and a next update time | Set from baseline | [outage updates generic or late](failures/outage-updates-generic-or-late.md) |
| Traveler-attribute errors per group booking | Set from baseline | [group bookings mix up travelers](failures/group-bookings-mix-up-travelers.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Disruption rebooking with wrong rules and no human path](failures/disruption-rebooking-with-wrong-rules-and-no-human-path.md) | The bot tells a stranded traveler a rule that is wrong for their ticket, or loops them in chat when they need a person (needs review) |
| [Outage updates generic or late](failures/outage-updates-generic-or-late.md) | The bot says crews are working, and the customer still cannot tell what broke, who is affected, or when they will hear again |
| [Group bookings mix up travelers](failures/group-bookings-mix-up-travelers.md) | Names, seats, meals, or needs get swapped or merged across people in one booking, and the change is committed before anyone sees the list |

Refund and credit rules misquoted is covered as a chat example in [knowledgebase staleness](../../../../by-use-case/support-services/goals/issue-resolution/failures/knowledgebase-staleness.md).

## Related
- [Human handoff](../human-handoff/README.md): the person route
- [Errors and recovery](../errors-and-recovery/README.md): sources and uncertainty
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
