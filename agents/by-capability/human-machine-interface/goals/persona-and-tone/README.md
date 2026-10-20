# Persona and Tone: Goal, Metrics, and Patterns

> **Goal:** The agent keeps one fitting character: on-brand, respectful, and never talking down or trying too hard.

## Why this family exists
A chat assistant has a voice, and users notice when it slips: it talks down, repeats the same canned opener, gets too familiar, or sounds like a different agent halfway through the session. None of these is a factual error, so they pass accuracy checks and show up only in complaints and drop-off.

## How we measure it
Each pattern page defines its own primary metric. Targets are starting points to tune on your own data and are proposed, not measured.
| Metric | Defined in |
|---|---|
| Replies judged patronizing per 100 (starting target under 2) | [condescending or patronizing tone](failures/condescending-or-patronizing-tone.md) |
| Share of replies opening with a stock phrase (starting target under 5%) | [stock phrases](failures/stock-phrases.md) |
| Over-familiar address per 1,000 replies (starting target 0) | [over-familiar address](failures/over-familiar-address.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Condescending or patronizing tone](failures/condescending-or-patronizing-tone.md) | Explains the obvious, praises trivial input, or softens a plain answer until it sounds like talking down |
| [Stock phrases](failures/stock-phrases.md) | Opens reply after reply with the same canned line such as "I'd be happy to help!" |
| [Over-familiar address](failures/over-familiar-address.md) | Uses first names, pet names or buddy language the user did not invite |

Related pages that live in other families (extended with chat examples): [persona drift within a conversation](../../../reasoning-and-thought/goals/model-behavior-and-capabilities/failures/model-style-drift.md), [voice drift after a model version upgrade](../../../../by-use-case/content-marketing/goals/brand-consistency/failures/voice-drift-after-model-version-upgrade.md), [forced cheerfulness](../stakes-calibration/failures/stakes-blind-register.md), [humor and sarcasm misused](../../../../by-use-case/support-services/goals/sentiment-escalation/failures/sarcasm-misread-as-satisfaction.md), [formality mismatch](../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-formality-mismatch.md).

## Related
- [Stakes calibration](../stakes-calibration/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
