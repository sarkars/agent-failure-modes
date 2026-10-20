# Sales Agents: Goal, Metrics, and Patterns

> **Goal:** Sales agents use verified information, respect opt-outs, and keep records clean.

## Why this family exists
An AI agent that writes, texts or chats for a sales team works at a scale where one bad rule repeats thousands of times. It can claim a history with a prospect that never happened, keep messaging someone who said stop, or update the wrong person's record. These are rules and data problems, so a better model alone does not fix them.

## How we measure it
Each pattern page defines its own primary metric. Targets are starting points to tune on your own data and are proposed, not measured.
| Metric | Defined in |
|---|---|
| Opt-outs honored within the required time (design target 100%) | [unsubscribe requests not honoured](failures/unsubscribe-requests-not-honoured.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Unsubscribe requests not honoured](failures/unsubscribe-requests-not-honoured.md) | An AI sales or outreach agent ignores "stop" or "unsubscribe", so messages keep arriving at scale. Carries a "Read this first" note. |

## Chat examples in existing pages
These catalog rows have no page of their own. Each has a short chat example inside the closest existing pattern.
| Row | Example in |
|---|---|
| SA-01 Invented personalization | [agent fabricates stated objection when call transcript tool returns empty](../../../../by-use-case/sales-crm/goals/lead-scoring/failures/agent-fabricates-stated-objection-when-call-transcript-tool-returns-empty.md) |
| SA-03 Wrong contact merged in the CRM | [entity confusion](../../../../cross-cutting/accuracy/goals/output-accuracy/failures/entity-confusion.md) |

## Planned (not yet written)
SA-04 (double-booked meetings) and the rest of the catalog are listed in the [roadmap](../../roadmap/index.md).

## Related
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
