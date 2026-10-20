# Healthcare Agents: Goal, Metrics, and Patterns

> **Goal:** Healthcare agents capture what happened accurately, flag what they're unsure of, and keep clinicians genuinely in the loop.

> **Read this first.** These pages are design guidance for testing your own product. They are not clinical, legal, or insurance advice. Clinicians and counsel must review any design based on them.

## Why this family exists
Healthcare assistants write notes, draft appeals, and rewrite medical text for patients. A signed note, a sent letter, or a plain-language summary becomes part of someone's care. A clean-looking draft hides what was invented, left out, or never asked. This family covers the four written so far plus one chat example on an existing page. The rest are catalogued in the [agent types roadmap](../../roadmap/agent-types.md).

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Seeded-error catch rate in drills | 90% or higher on high-risk items (starting point) | [notes approved without being read](failures/notes-approved-without-being-read.md) |
| Visits with recorded consent | 100% of recorded visits | [recording consent not captured](failures/recording-consent-not-captured.md) |
| Unsupported claims in appeals | 0 per letter | [fabricated clinical justification in appeals](failures/fabricated-clinical-justification-in-appeals.md) |
| Critical caveats preserved on a labelled set | 100% | [patient summaries too simple to be safe](failures/patient-summaries-too-simple-to-be-safe.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Notes approved without being read](failures/notes-approved-without-being-read.md) | Clinicians sign AI-drafted notes unread; mark high-risk and inferred items and tie each to what was said |
| [Recording consent not captured](failures/recording-consent-not-captured.md) | A scribe records with no clear consent; ask first, log the answer, keep recording off until a yes |
| [Fabricated clinical justification in appeals](failures/fabricated-clinical-justification-in-appeals.md) | An appeal states treatments or results not in the chart; tie every claim to a chart entry |
| [Patient summaries too simple to be safe](failures/patient-summaries-too-simple-to-be-safe.md) | A plain-language rewrite drops stop-orders and return warnings; list critical caveats first and check each survives |

## Chat examples on existing pages
- Scribe omissions and invented content: [empty allergy query result documented as confirmed no known allergies](../../../../by-use-case/healthcare/goals/clinical-documentation/failures/empty-allergy-query-result-documented-as-confirmed-no-known-allergies.md)

## Planned (not yet written)
None listed here. See the [roadmap](../../roadmap/index.md) for the rest.

## Related
- [Errors and recovery](../errors-and-recovery/README.md)
- [Research and data agents](../research-and-data-agents/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
