# Research and Data Agents: Goal, Metrics, and Patterns

> **Goal:** A research or data assistant shows the evidence and the method behind every answer, so the user can judge whether to trust it.

## Why this family exists
Research and data assistants answer questions with numbers and summaries. The user usually cannot see the query, the definitions, or the sources that were left out. A wrong join, a private meaning of "active user", or a summary built from sources that all agree can all look like a confident answer. This family covers the three written so far. The rest are catalogued in the [agent types roadmap](../../roadmap/agent-types.md); two of them are already covered by a chat example on an existing pattern page.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Result accuracy on a labeled query set | 95% or higher (starting point) | [wrong joins and double counting](failures/wrong-joins-and-double-counting.md) |
| Answers that use the governed definition | 100% | [wrong business definitions](failures/wrong-business-definitions.md) |
| Judge-rated balance on contested questions | 90% or higher rated balanced (starting point) | [one-sided or cherry-picked sources](failures/one-sided-or-cherry-picked-sources.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Wrong joins and double counting](failures/wrong-joins-and-double-counting.md) | A query runs but returns wrong numbers, narrated with confidence; show the SQL, state what is counted, run sanity checks |
| [Wrong business definitions](failures/wrong-business-definitions.md) | Uses the wrong meaning of "active user", "revenue", or "churn"; use the company's governed definitions |
| [One-sided or cherry-picked sources](failures/one-sided-or-cherry-picked-sources.md) | A research summary presents selected evidence as balanced; show disagreement and source quality |

## Chat examples on existing pages
- Claims to have read inaccessible sources: [fabricated citations](../../../knowledge-retrieval/goals/citation-accuracy/failures/fabricated-citations.md)
- Method and query not shown: [output provenance loss](../../../../cross-cutting/security/goals/agent-trust/failures/output-provenance-loss.md)

## Planned (not yet written)
None listed here. See the [roadmap](../../roadmap/index.md) for the rest.

## Related
- [Errors and recovery](../errors-and-recovery/README.md)
- [Dialogue management](../dialogue-management/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
