# Conversation Frameworks: Goal, Metrics, and Patterns

> **Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.

## Why this family exists
Human sales and support teams learn structures: find the need before pitching, handle an objection in steps, ask for a next step, follow up only as agreed. A chatbot that improvises each exchange skips them. It lists features, argues with "too expensive", or lets an interested buyer leave with nothing to do. These are design and business-rule problems, so a better model alone does not fix them.

## How the frameworks are used here
The frameworks (SPIN, Challenger, BANT and MEDDICC, objection-handling steps) come from human-to-human practice. None has been tested on chatbots in the sources found. Each page treats a framework as a hypothesis to test, not a proven fix. See the [framework register](../../roadmap/README.md#framework-and-source-register) for what was verified.

## How we measure it
Each pattern page defines its own primary metric. Targets are starting points to tune on your own data and are proposed, not measured.
| Metric | Defined in |
|---|---|
| Share of recommendations that cite the user's stated need (judge). Start: over 90% | [feature dump instead of insight](failures/feature-dump-instead-of-insight.md) |
| Share of objections followed by continued conversation or a next step | [mishandled objections](failures/mishandled-objections.md) |
| Next-step proposal rate in qualified chats. Start: over 90% | [no ask](failures/no-ask.md) |
| Consented-follow-up completion rate; opt-out rate | [no follow-up](failures/no-follow-up.md) |
| Stakeholders captured per qualified deal | [buying-committee blindness (B2B)](failures/buying-committee-blindness-b2b.md) |
| Recommendation-fit rate (judge); return and cancel rate | [wrong-fit recommendation](failures/wrong-fit-recommendation.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Feature dump instead of insight](failures/feature-dump-instead-of-insight.md) | The bot lists features and leaves the user to work out which ones fit their problem. |
| [Mishandled objections](failures/mishandled-objections.md) | The bot caves, argues, or skips the objection instead of acknowledging, asking, answering, and checking. |
| [No ask](failures/no-ask.md) | An interested user gets answers but no proposed next step. |
| [No follow-up](failures/no-follow-up.md) | The chat ends and the lead goes cold; follow up only as the user agreed. Carries a "Read this first" note. |
| [Buying-committee blindness (B2B)](failures/buying-committee-blindness-b2b.md) | The bot records one contact and never asks who else decides. |
| [Wrong-fit recommendation](failures/wrong-fit-recommendation.md) | The bot recommends a product that breaks a limit the user stated. |

## Chat examples in existing pages
These catalog rows have no page of their own. Each has a short chat example inside the closest existing pattern.
| Row | Example in |
|---|---|
| FW-S02 No qualification | [qualification flow violations](../../../speech-and-audio/goals/conversation-flow/failures/qualification-flow-violations.md) |
| FW-S06 Manipulative closing | [vague consent exploitation](../../../speech-and-audio/goals/conversation-flow/failures/vague-consent-exploitation.md) |
| FW-S07 Discount-first selling | [negotiation capitulation](../relational-and-boundaries/failures/negotiation-capitulation.md) |

## Planned (not yet written)
The rest of the catalog (supporting, matching style, delivering hard news) is listed in the [roadmap](../../roadmap/conversation-frameworks.md).

## Related
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md) · [Sales agents](../sales-agents/README.md)
