# SEO Improvement Plan (Failure Pattern Pages)

**Status**: **Active — Phase 1 (top priority)** in `.claude/scheduled-tasks/agent-pattern-mitigation-backfill-4am/SKILL.md`. Originally queued as Phase 2 (behind field-duplication/template-cluster remediation, effective 2026-08-16), then promoted to Phase 1 later the same day per explicit user request to start execution immediately rather than wait for that phase's backlog to clear. Field-duplication/template-cluster remediation is now Phase 2. This document remains the source-of-truth rationale — SKILL.md Phase 1 is the executable spec derived from it.

**Scope**: `agents/**/failures/*.md` only. Does not apply to goal-index pages, category READMEs, or root-level docs (`README.md`, `DUPLICATE_AUDIT_PLAN.md`, etc.).

**Purpose**: Capture the rationale and content rules for how failure-pattern pages should be titled and phrased so they match how people actually search for these problems. The executable version of this plan lives in `.claude/scheduled-tasks/agent-pattern-mitigation-backfill-4am/SKILL.md` as Phase 1 — that file is what the scheduled task actually reads each run; this document explains the *why* behind it.

---

## Planned changes

### 1. Rewrite page titles around actual search queries

Retitle pattern pages (the `# ...` H1, and where relevant the filename) to match how someone would type the problem into a search engine, rather than the current internal/mechanism-first naming style.

Examples of the target phrasing:
- `AI Agent Infinite Loop: Causes and Fixes`
- `RAG Retrieves Wrong Documents: Causes and Fixes`

### 2. Use symptom-based language

Favor the phrasing a frustrated practitioner would actually type or say, worked into titles, Issue lines, and Symptoms bullets:
- "agent gets stuck"
- "agent calls wrong tool"
- "agent forgets context"
- "agent hallucinates"

### 3. Add "how to fix" explicitly to pages

Make the fix-oriented framing explicit on the page itself (title and/or a clearly labeled section), not just implied by the existing `## Mitigations` / `## Mitigation Strategies` headings.

### 4. Add framework-specific terminology

Incorporate the concrete framework/tooling names practitioners search alongside a failure mode, where genuinely applicable to the pattern (not force-fit into unrelated patterns):
- LangGraph
- LangChain
- CrewAI
- OpenAI Agents SDK
- MCP
- LlamaIndex
- Google ADK

---

## Resolved questions

- **Filename/URL stability**: title rewrites happen in place — new H1 text only, filenames and URLs stay unchanged. Renaming would require fixing every inbound `## Related Patterns` link across the repo (the same link-repair work Phase 0 already does for merges), which is unnecessary risk for a wording-only change.
- **Where framework terminology goes**: woven into existing prose (title, Issue line, Symptoms, or a "commonly reported when using frameworks like X" note near the fix) rather than a new dedicated section — avoids adding a section that's empty on most files, since not every pattern has a genuine framework tie-in. Framework names are only added where the mechanism plausibly applies; forcing one into an unrelated pattern is explicitly disallowed.
- **Sequencing against the pipeline**: it's its own numbered phase — **Phase 1, top priority** — ahead of field-duplication/template-cluster remediation (now Phase 2) and everything after it, rather than a per-file pass folded into Phase 7 (Maintenance & Expansion). See `.claude/scheduled-tasks/agent-pattern-mitigation-backfill-4am/SKILL.md` for the full executable spec (ground truth tracking, per-file fix steps, batching, commit-message convention).
