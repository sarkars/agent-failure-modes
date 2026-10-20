# Fairness and Identity: Goal, Metrics, and Patterns

> **Goal:** Quality of service does not depend on dialect, name, or other identity cues, and everyone can complete the task in chat, including people who use assistive technology.

## Why this family exists
Language models carry societal associations. The only reliable check is paired testing on your own system, before and after every change.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Paired-test parity ratio | Within about 0.9 to 1.1 (a heuristic) | [dialect and name quality gap](failures/dialect-and-name-quality-gap.md) |
| Parity regressions after changes | 0 | dialect and name quality gap |
| Task-completion parity for assistive-technology users | 0.9 or higher (starting point) | [accessibility in chat](failures/accessibility-in-chat.md) |
| Unprompted identity references | 0 (starting point) | [over correcting for identity](failures/over-correcting-for-identity.md) |

## Patterns
| Pattern | One line |
|---|---|
| Dialect and name quality gap | Unequal service by dialect, name, or identity cues |
| [Accessibility in chat](failures/accessibility-in-chat.md) | Chat works part by part but not for assistive-technology users end to end |
| [Over-correcting for identity](failures/over-correcting-for-identity.md) | Fairness fixes lead to announced or stereotyped tailoring |

## Related
- [Cultural adaptation](../cultural-adaptation/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
