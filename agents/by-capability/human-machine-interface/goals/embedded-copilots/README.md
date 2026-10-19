# Embedded Copilots: Goal, Metrics, and Patterns

> **Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs.

## Why this family exists
Assistants inside products (support widgets, in-app help, copilots) differ from general chatbots. They sit next to a sales motive, they can reach account and screen context, and users expect them to know it. This family covers the failures that follow.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Re-ask rate on known fields | Under 2% | [re-asks for known information](failures/re-asks-for-known-information.md) |
| Re-authentication prompts on low-risk actions for signed-in users | Near 0 | [forces a fresh login](failures/forces-a-fresh-login.md) |
| Openers that reference user-specific context or a likely need | Over 70% (tune) | [generic first response](failures/generic-first-response.md) |
| Top-intent accuracy on simple requests | Over 95% | [missing the obvious intent](failures/missing-the-obvious-intent.md) |
| New users who complete a successful first task | Set from baseline | [doesn't say what it can do](failures/doesn-t-say-what-it-can-do.md) |
| Upsell-in-help rate on support intents | Under 5% (tune) | [help that becomes a sales pitch](failures/help-that-becomes-a-sales-pitch.md) |
| Cancellation parity (steps to cancel vs steps to subscribe) | Parity | [obstructing cancellation](failures/obstructing-cancellation-downgrade-or-refund.md) |

## Patterns
| Pattern | One line |
|---|---|
| Re-asks for known information | The assistant asks for details the product already holds |
| Forces a fresh login | The signed-in user is asked to sign in or verify again, even for low-risk help |
| Generic first response | The first message is a stock greeting that ignores what the product knows |
| Missing the obvious intent | A plain request gets a neighboring answer or an over-reading |
| Doesn't say what it can do | An empty box that never says what the assistant can and cannot do |
| Help that becomes a sales pitch | A how-to or fix question is answered with an upgrade or add-on |
| Obstructing cancellation, downgrade, or refund | Leaving is harder than joining; the assistant argues, loops, or hides the path |

## Planned (not yet written)
- Answers withheld behind an upgrade, unsaid

## Related
- [Human handoff](../human-handoff/README.md): what happens when the assistant passes the customer to a person
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
