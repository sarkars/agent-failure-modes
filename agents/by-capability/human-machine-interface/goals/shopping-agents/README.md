# Shopping Agents: Goal, Metrics, and Patterns

> **Goal:** Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed.

## Why this family exists
Chat assistants now search for products, rank them, and sometimes buy. This family covers what goes wrong in the conversation when an agent spends the user's money: unclear routes to put a wrong purchase right, and ranking that follows payment instead of the user's criteria. The guidance is design guidance only, not legal advice. Have counsel read the pages marked "Read this first" before launch, and check which rules apply to you. Voice and web checkout are planned, not written.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Agent purchases that have a receipt and a spending cap | Start: 100% | [no clear route when an agent buys wrongly](failures/no-clear-route-when-an-agent-buys-wrongly.md) |
| Paid placements labelled | Start: 100% | [sponsored ranking inside agent recommendations](failures/sponsored-ranking-inside-agent-recommendations.md) |
| Price or stock mismatches at purchase the user was not told about | Start: 0 | [stale price or stock at checkout](failures/stale-price-or-stock-at-checkout.md) |
| Auto-renewing purchases made with explicit consent | Start: 100% | [free trials that become paid subscriptions](failures/free-trials-that-become-paid-subscriptions.md) |
| Purchases that show return terms before payment | Start: 100% | [return policy ignored](failures/return-policy-ignored.md) |
| Gift purchases exposed to other account users | Start: 0 | [shared accounts reveal gifts](failures/shared-accounts-reveal-gifts.md) |

## Patterns
| Pattern | One line |
|---|---|
| [No clear route when an agent buys wrongly](failures/no-clear-route-when-an-agent-buys-wrongly.md) | The agent buys the wrong thing and the user has no receipt, no cap, and no dispute path |
| [Sponsored ranking inside agent recommendations](failures/sponsored-ranking-inside-agent-recommendations.md) | Paid placement decides what the agent suggests, and nobody says so |
| [Stale price or stock at checkout](failures/stale-price-or-stock-at-checkout.md) | The agent quotes an earlier price or stock status and the cart differs at purchase |
| [Free trials that become paid subscriptions](failures/free-trials-that-become-paid-subscriptions.md) | The agent starts a trial that renews at full price without telling the user |
| [Return policy ignored](failures/return-policy-ignored.md) | The agent buys an item that cannot be returned and does not say so before payment |
| [Shared accounts reveal gifts](failures/shared-accounts-reveal-gifts.md) | A gift purchase shows up in shared recommendations, history or memory |

## Planned (not yet written)
The other rows of the family are tracked in the [emerging surfaces roadmap](../../roadmap/emerging-surfaces.md). Several already have an example added to a pattern elsewhere in the repository.

## Related
- [Embedded copilots](../embedded-copilots/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
