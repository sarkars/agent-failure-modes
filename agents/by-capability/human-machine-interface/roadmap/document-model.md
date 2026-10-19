# Document Model: One Pattern, Many Views

**Approved 2026-10-19 by the owner.** Most of the new document types in the plan are not independent. They are facets of one failure pattern, keyed by its Pattern ID. This page sets one rule for where each kind of content lives, so the folder stops growing a new document type for every idea.

## The rule
1. **A fact about one pattern lives on that pattern's page.** That includes the fix, the guide moves, the detection signals, the starter rule and the short tests. Pattern pages are the only HMI pages the website publishes today (the site importer reads `goals/<family>/failures/`), so content placed there is published without any site change.
2. **A list across patterns is an index, not a new document.** It is a table that links to pattern pages and adds no facts of its own. There is one index: the [failure taxonomy](specs/failure-taxonomy-v1.md), with extra columns.
3. **Only content that spans many patterns gets its own page.** Examples are the event schema, an incident, a study and the glossary.
4. **Plans, logs and templates are internal.** They stay in `roadmap/` and `_templates/` and are never linked as reader content.
5. **No file is renamed, moved or deleted** once it is on main. This model applies to new content only.

## Every document type, classified
| Type | Kind | Lives in | Status |
|---|---|---|---|
| Fix, principle, don't over-correct, hand-off rule | Pattern facet | Pattern page, section 5 | Exists |
| Guide moves (lead with answer, ask one question, offer choices, admit uncertainty, hand off) | Pattern facet | Pattern page, section 5, "Moves" table | In the template 2026-10-19 |
| Guide spec block (fixed format, for later code) | Pattern facet | Pattern page, end of section 7 | In the template 2026-10-19 |
| Detection signals and starter rule | Pattern facet | Pattern page, section 7 | Exists on 19 of 44 |
| Short tests | Pattern facet | Pattern page, section 6 | Exists |
| Full test file | Pattern companion | `tests/<pattern-id>.md` | Exists for flagships |
| Failure taxonomy | Index | `roadmap/specs/failure-taxonomy-v1.md` | Exists; gains columns for starter rule, guide moves, test file and incident |
| Starter rules library (asset 7) | Index | A column in the taxonomy | Was a separate asset; folded in |
| Scenario pack (asset 3) | Index plus content | Scenarios in `tests/<pattern-id>.md`; the taxonomy links them | Was a separate asset; becomes test files plus a column |
| Guides index | Index | A column in the taxonomy | Was a separate page; folded in |
| Conversation moves, explained once | Cross-pattern | `solutions-library/conversation-moves.md` (a framework, like SPIN) | Done 2026-10-19 |
| Event schema | Cross-pattern | `roadmap/specs/` | Exists |
| Evidence review | Cross-pattern | `roadmap/evidence/` | Exists |
| Incident teardowns (asset 4) | Cross-pattern | `incidents/` | Some exist |
| Metrics hub (asset 5) | Cross-pattern | `reference/metrics.md` | Not started |
| Study preregistrations (asset 6) | Cross-pattern | `reference/studies/` | Not started |
| Glossary (asset 9) | Cross-pattern | `reference/glossary.md` | Not started |
| Explainer: output guardrails vs. conversation guidance | Cross-pattern | `reference/` | Not started |
| Comparison with existing guardrail tools | Cross-pattern | `reference/` | Not started, Needs review |
| Failure-audit offer (asset 8) | Cross-pattern | `reference/` | Not started |
| Reference code module | Code | Its own repo, after a design note | Approved, last |

`reference/` is one new folder for every new cross-pattern page that a reader should see. Pages already in `roadmap/specs/` and `roadmap/evidence/` stay where they are.

## What this changes in the hourly run
- **Retrofit and guide become one edit.** When a run adds detection signals to a pattern (Part A2), it adds the Moves table and the Guide spec block in the same pass. For the 19 patterns that already have signals, it adds only the Moves table and the Guide spec. Part E as separate guide files is dropped.
- **Assets 3 and 7 shrink.** The scenario pack becomes scenarios in the test files plus a taxonomy column. The starter rules library becomes a taxonomy column. Both finish when the retrofits finish.
- **Independent assets left:** teardowns, metrics hub, studies, glossary, the explainer, the tool comparison and the audit offer. They all go in `reference/` or `incidents/`.
- **Front page:** a "Start here" section with three doors: patterns (what goes wrong and what to do), the taxonomy (every pattern at a glance) and reference (specs, metrics and studies).

## Owner decisions (2026-10-19)
- This model: approved.
- Cross-pattern pages on the website: approved. The site importer change is in [sarkars/agent-kb-autopublish#1](https://github.com/sarkars/agent-kb-autopublish/pull/1); pages in `solutions-library/`, `roadmap/specs/` and `reference/` are published once it merges.
- Reference code module: approved, last. A design note comes first, then code in its own repository.
- The queued catalog rows: approved. The hourly run writes them after the flagships, up to 5 per run.

## Related
- [Distribution plan](distribution-plan.md)
- [Execution plan](execution-plan.md)
- [Pattern template](../_templates/hmi-pattern.md)
