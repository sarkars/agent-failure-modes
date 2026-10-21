# Banking Agents: Goal, Metrics, and Patterns

> **Goal:** Banking agents tell customers what was seen and what to do in a way that real alerts can be told apart from scams, and they never ask for a full code or password in chat.

> **Read this first.** This family is design guidance, not legal, fraud-operations, or compliance advice. Alert wording, authentication rules, and what you may disclose about suspected fraud depend on your bank, your regulator, and your fraud team. Have fraud, compliance, and legal staff review before use.

## Why this family exists
Customers get a bank message about their money and must decide quickly whether it is real. Scammers copy the same wording, so an alert that asks for a link click or a code looks the same as a scam. A vague alert gives the customer nothing to decide with. This family covers failures specific to banking chat and alert conversations.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Fraud-alert flows reviewed against anti-phishing guidance | 100% | [fraud-alert conversations that look like phishing](failures/fraud-alert-conversations-that-look-like-phishing.md) |
| Customers who can act on the alert without calling | Set from baseline | [unusual activity explained too vaguely](failures/unusual-activity-explained-too-vaguely.md) |
| Disputes needing a second contact for missing data | Set from baseline | Covered as a chat example in [handoff context incompleteness](../../../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Fraud-alert conversations that look like phishing](failures/fraud-alert-conversations-that-look-like-phishing.md) | The alert asks the customer to click a link, share a code, or confirm a card number, as scammers do (needs review) |
| [Unusual activity explained too vaguely](failures/unusual-activity-explained-too-vaguely.md) | "We saw something suspicious" with no merchant, amount, date, or next step (needs review) |

Disputed-transaction intake that loses details is covered as a chat example in [handoff context incompleteness](../../../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md).

## Related
- [Vulnerable users](../vulnerable-users/README.md): scam victims and hardship
- [Human handoff](../human-handoff/README.md): the person route
- [Stakes calibration](../stakes-calibration/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
