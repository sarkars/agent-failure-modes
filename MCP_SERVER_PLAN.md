# MCP Server Implementation Plan

Goal: turn this pattern library into an MCP server that helps people write better agents — not just a searchable catalog, but something that surfaces relevant failure modes proactively (code review, runtime, design time).

## Problem

1267 pattern files, no frontmatter, inconsistent headings (`## Issue` vs `## Issue: <sentence>`, `## Mitigations` vs `## Mitigation Strategies`, `## Related Patterns` present on some files, absent on others). Can't query this as data without a tolerant parser first.

Guardrails.ai-style runtime validators (wrap one LLM output, check it, retry/fix) only fit a minority of patterns — the ones that are single-output-shaped (PII exposure, insecure output handling, HIPAA deident, schema/field extraction). Most patterns here are architectural/sequence failures (handoff timing, webhook delivery guarantees, stale state after own action) that span multiple tool calls and system state — a single-output validator can't catch those.

## Phase 0 — Structured index (prerequisite for everything below)

- One tolerant parser over the existing heading dialects (sample covers ~90% of variants: H1, `## Issue`/`## Issue: ...`, `## Root Cause`, `## Mitigations`/`## Mitigation Strategies`, `## Related Patterns`/absent).
- Derive `category`/`goal` from file path (`agents/<category>/goals/<goal>/failures/<name>.md`), not content — free faceted taxonomy, no authoring needed.
- Emit `index.json`: one record per pattern — id, title, issue, fix_summary, mitigations[] (with stable ids), related[] (ids, not markdown links), tags.
- No source file rewrites. Frontmatter added only to files already being edited for content reasons going forward, not backfilled across all 1267.

## Phase 1 — MCP server (read-only)

Tools, served from `index.json`, keyword/tag match (no DB, no embeddings until keyword search is proven insufficient):
- `search_failure_modes(query, category?, goal?, framework?)`
- `get_pattern(id)`
- `list_goals(category?)`
- `get_checklist(goal)` — merged, deduped mitigations across all failures under a goal

Ship as stdio MCP package, publish npm/pip.

## Phase 2 — Detection heuristics + static scan

- Author heuristics (keyword/regex code or architecture smells) incrementally — start with the goals being wired into review first, not all 1267 up front.
- `scan_design(text)` MCP tool using heuristics.json.
- Register as a finding-source inside the existing `/code-review` diff pipeline — reuse its trigger, don't build a new one.

## Phase 3 — Guardrails-style output validators

- Scope to the single-output-shaped subset only (~15-20% of patterns: PII exposure, insecure output handling, HIPAA deident, schema/field extraction errors).
- `Guard`-style wrapper, one validator per pattern, backed by Phase 2 heuristics where they overlap.

## Phase 4 — Sequence/state invariant middleware

- Framework callback hooks (LangGraph/CrewAI) for cross-call invariants: "state read after your own mutating call on the same resource must be a fresh fetch," "handoff message must carry a freshness timestamp checked on receipt."
- Separate package from Phase 3 — different integration point (framework hook vs. call wrapper).

## Phase 5 — Fault-injection eval harness

- Harvest existing "Eval Recipes"/"Test Cases" sections where already authored (present on a handful of files).
- Harness injects the triggering fault (timeout, dropped webhook, concurrent trigger) and asserts expected handling.
- Author new eval recipes only for goals already covered by Phase 4, not all patterns.

## Phase 6 — Publish/polish the website

- Confirm `agent-kb-autopublish`'s `static/js/search.js` indexes the new structured fields (title/issue/tags from Phase 0) via `/index.json`, not just raw Hugo content.
- Verify the left-sidebar nav (category → goal tree) and search share one taxonomy from Phase 0, not two divergent trees.
- Deploy via existing `vercel --prod` flow — no new infra.

Phases 1-6 each ship independently; only Phase 0 blocks the rest (all read from its index).
