# Chat Agent Spec Builder: How the Interactive Page Is Made

**The builder is a single page that turns a chosen use case and goals into the failures to defend against, the rules to add, starter code, and a metric ledger.** It is generated from data, not written as prose.

| File | What it is |
|---|---|
| `content.py` | The authored content: goals, rules (instructions, guardrails, evals) with metrics, code snippets, and the 25 use cases |
| `data_gen.py` | Reads the failure library and catalog to get real titles, one-line summaries, and file paths for each failure |
| `page.tpl` | The page template (layout, styling, behavior) |
| `build.py` | Checks that every rule has a metric, a how-measured, and a counter-metric, then writes `data.json` and `index.html` |
| `data.json`, `index.html` | Generated. Do not edit by hand |

Rebuild after changing content: `python3 -I agents/by-capability/human-machine-interface/chat-use-cases/builder/build.py`

**Status.** Prompts, code, and eval snippets are illustrative drafts that have not been run against a model. Thresholds are never given, only the metric and how to measure it. For tier C use cases, instruction text is withheld in the page.

## Related
- [Chat use cases](../)
- [Content program](../../roadmap/content-program.md)
