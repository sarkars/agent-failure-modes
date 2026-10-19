# Human Handoff: Goal, Metrics, and Patterns

> **Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.

## Why this family exists
Not being able to reach a person is a recurring complaint about service chatbots (see the [CFPB report](../../incidents/cfpb-bank-chatbot-doom-loops.md)). This family covers the moments around a handoff: whether a request for a person is honored, when the bot escalates, and what the person knows when they arrive.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Human-request fulfillment rate (requests that end in a transfer, callback, or stated route within 2 bot turns) | 100% | [talk to a human ignored or looped](failures/talk-to-a-human-ignored-or-looped.md) |
| Escalation recall and precision against labeled conversations | Recall over 95%, precision over 80% | [escalates too early or too late](failures/escalates-too-early-or-too-late.md) |
| Re-ask rate after handoff | Under 5% | [cold transfer](failures/cold-transfer.md) |

## Patterns
| Pattern | One line |
|---|---|
| Talk to a human ignored or looped | The customer asks for a person and the bot loops or deflects |
| Escalates too early, or too late | The bot hands off questions it could answer, or holds on to ones it cannot |
| Cold transfer | The person who picks up knows nothing and asks everything again |

## Planned (not yet written)
- Handoff summary is wrong or misleading
- Humans can't see what the bot said or promised
- Handoff outside staffed hours with no alternative

## Related
- [Channel selection](../channel-selection/README.md): switching channels without losing context
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
