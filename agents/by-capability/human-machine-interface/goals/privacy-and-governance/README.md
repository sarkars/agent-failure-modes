# Privacy and Governance: Goal, Metrics, and Patterns

> **Goal:** The agent handles personal data and outside services under clear rules, acts only within the rights of the person it serves, explains its limits, and keeps to its rules when pushed.

## Why this family exists
Chat assistants collect, repeat, infer, and store personal data. Users also paste other people's data and ask to see or delete their own. This family covers what the bot does with that data in the conversation. The guidance is design guidance only, not legal advice. Have a privacy or legal reviewer read it before launch, and check which laws apply to you.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Third-party private values discarded after use | Start: 100% | [third-party data shared by users](failures/third-party-data-shared-by-users.md) |
| Sensitive-trait inferences stored or used | 0 | [sensitive-category inference](failures/sensitive-category-inference.md) |
| Recognition recall on labeled privacy-rights requests | Start: over 95% | [privacy-rights requests not recognised](failures/privacy-rights-requests-not-recognised.md) |
| Commitments recorded and retrievable by the user | 100% (starting point) | [no user-facing record of what the bot said](failures/no-user-facing-record-of-what-the-bot-said.md) |
| Dependence signals escalated | Start: 100% | [engagement-maximising design that harms](failures/engagement-maximising-design-that-harms.md) |
| Pressure or upsell shown after vulnerability signals | 0 | [exploiting vulnerable circumstances](failures/exploiting-vulnerable-circumstances.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Third-party data shared by users](failures/third-party-data-shared-by-users.md) | A user pastes someone else's private details and the bot repeats or keeps them |
| [Sensitive-category inference](failures/sensitive-category-inference.md) | The bot guesses health, pregnancy, orientation, or immigration status and uses or stores the guess |
| [Privacy-rights requests not recognised](failures/privacy-rights-requests-not-recognised.md) | "Delete my data" or "what do you have on me?" is treated as small talk |
| [No user-facing record of what the bot said](failures/no-user-facing-record-of-what-the-bot-said.md) | Users cannot get a copy of the chat or of the promises the bot made |
| [Engagement-maximising design that harms](failures/engagement-maximising-design-that-harms.md) | The bot is tuned for time on platform and fosters dependence |
| [Exploiting vulnerable circumstances](failures/exploiting-vulnerable-circumstances.md) | An upsell or pressure line is aimed at a user in debt, distress, or isolation |

## Planned (not yet written)
The other rows of the family are tracked in the [privacy, governance, and access roadmap](../../roadmap/privacy-governance-and-access.md). Several already have a page elsewhere in the repository.

## Related
- [Vulnerable users](../vulnerable-users/README.md)
- [Channel selection](../channel-selection/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
