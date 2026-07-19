# Phase Replan — 2026-07-19

Five scheduled routines write into this repo independently (`agent-pattern-mitigation-backfill-4am`, `implement-agent-failure-patterns`, `daily-pattern-authorship`, `early-pattern-authorship`, `two-hourly-pattern-authorship`). Each carries its own hardcoded "current progress" numbers in its `SKILL.md`, and every one of those numbers is stale — some by an order of magnitude. This document re-derives ground truth directly from the repo and reconciles the four independent "phase"/"batch" tracks into one picture. It does not modify any routine's `SKILL.md` (those are standing automation config — changing them needs explicit sign-off, not an autonomous edit).

**Total failure-pattern files today: 1219** (was 862 as of 2026-07-16; +357 from the 2026-07-17 placeholder-reservation commit `e34d7eb`).

---

## Track A — New Pattern Authorship ("Batch 1", by-use-case)

Owned by: `daily-pattern-authorship`, `early-pattern-authorship`, `two-hourly-pattern-authorship` (three separate schedules writing the same target set — no coordination between them beyond category choice).

Their shared `SKILL.md` figures ("639 total patterns, 73/255 Batch 1, 28.6%") are **stale by roughly 2.5x**. Actual current state:

| Category | Current files | Original target | Status |
|---|---|---|---|
| financial-services | 37 | ~50 | 74% |
| healthcare | 35 | ~45 | 78% |
| legal-contracts | 28 | ~40 | 70% |
| devops | 27 | ~40 | 68% |
| supply-chain | 22 | ~35 | 63% |
| support-services | 23 | ~40 | 58% |
| **Batch 1 subtotal** | **172** | **~250** | **69%** |
| hr-recruiting (expansion) | 21 | — | — |
| sales-crm (expansion) | 17 | — | — |
| content-marketing (expansion) | 20 | — | — |
| insurance (expansion) | 15 | — | — |
| agent-interaction (untracked in SKILL) | 23 | — | — |
| mortgage-documents (untracked in SKILL) | 53 | — | — |

**Replan for Track A:**
1. Batch 1 core is 69% done (~78 patterns short), not 28.6%. Priority order should flip to the categories furthest behind in absolute terms: **support-services (17 short), supply-chain (13), devops (13), financial-services (13), legal-contracts (12), healthcare (10)** — roughly even now, so any consistent order is fine; support-services and supply-chain are the largest remaining gaps.
2. **Five empty scaffold directories exist with only a README**: `code`, `customer-support`, `data-extraction`, `devops-infrastructure`, `ecommerce-retail`. These look like orphaned duplicates of populated categories (`customer-support` vs. the populated `customer-service`; `devops-infrastructure` vs. the populated `devops`) rather than genuine new categories — needs a human call on whether to delete them or treat them as real Batch-2 targets. **Do not delete or repurpose without asking** — flagging only.
3. Three schedules (4 AM adjacent early-run, daily, two-hourly) targeting the identical category list risks duplicate work on the same day; recommend the human owner either stagger categories explicitly across the three, or fold them into one schedule now that the count shows steady organic progress rather than the stall the original 28.6% figure implied.

---

## Track B — Placeholder Pattern Completion ("Phase 1")

Owned by: `implement-agent-failure-patterns` (5:30 AM).

Source: 354 placeholder files reserved by commit `e34d7eb` (2026-07-17) across `by-capability`, `by-use-case`, and `cross-cutting`, using the "new" template (`## Issue`/`## Root Cause`/`## Example`/`## Statistics`/`## Mitigations`/`## Production Signals`/`## Related Patterns`).

**Current state: 328/354 done (93%). Only 26 stub files remain**, still literally containing `[PLACEHOLDER] Pattern Under Implementation`:
- `by-capability/reasoning-and-thought/goals/model-updates-and-versioning/failures/`: 4 files
- `cross-cutting/operations/goals/dependency-management/failures/`: 5 files
- `cross-cutting/operations/goals/fault-tolerance/failures/`: 2 files
- `cross-cutting/operations/goals/input-output-handling/failures/`: 4 files
- `cross-cutting/operations/goals/planning-and-decomposition/failures/`: 3 files
- `cross-cutting/operations/goals/version-management/failures/`: 8 files

**Replan for Track B:** small enough now (26 files) for a single run to close entirely — no need for the 7-parallel-subagent approach used when 240 remained; 1-2 subagents suffice. This track is nearly done; next run should finish it and can then stand down (repurpose that 5:30 AM slot toward Track C or D once Track B hits 0).

---

## Track C — Mitigation Strategies Backfill ("Phase 2")

Owned by: `agent-pattern-mitigation-backfill-4am` (this task).

**Status: CLOSED, reconfirmed today.** Of the 865 files using the original template, all have complete `## Mitigation Strategies` content (Prevention/Detection & Response/Architecture Patterns/Metrics/Alerts) or the equally-complete `## Mitigations` + `## Production Signals` variant used by Track B's template. Zero genuine gaps outside the 26 stubs that belong to Track B.

**Replan for Track C:** this routine has no more Phase-2-scoped work. Per its own task file's "Notes" section, it should transition fully into Track D (Test Scenarios) as its ongoing mandate — which is already what's been happening since 2026-07-17. Recommend renaming/repointing this scheduled task's description to reflect that it's now a Test-Scenario-backfill routine, not a Mitigation-backfill routine, since the "Mitigation Strategies" framing in its name and SKILL.md no longer matches its actual daily work.

---

## Track D — Test Scenario & Reproduction Backfill ("Phase 4")

Owned by: `agent-pattern-mitigation-backfill-4am` (same routine as Track C, post-transition).

Ground-truth scope: the 865-file "old template" pool (Track C's completed set) is also the *only* valid pool for this backlog — the 328 Track-B files and 26 Track-B stubs use a different template and are explicitly out of scope here (confirmed again today; still true).

**Current state: 675/865 missing `## Test Scenario` (78% remaining, 190 done)** — unchanged since the 2026-07-18 count of ~675, meaning no run touched this track between then and today (my 2026-07-19 run this session focused on the Track C re-verification instead and found no Track C work to do).

Breakdown of the 675 remaining, by top-level directory:

| Directory | Remaining | Total in pool | % done |
|---|---|---|---|
| cross-cutting | 105 | 570 | 82% |
| by-capability | 255 | 311 | 18% |
| by-use-case | 315 | 338 | 7% |

**Replan for Track D:**
1. Cross-cutting is nearly exhausted (105 left) — finish it first, it's the cheapest remaining win.
2. Then move into `by-capability` (255 remaining) before `by-use-case` (315 remaining), continuing the established priority order (cross-cutting → by-capability → by-use-case).
3. At the ~46-50 files/run pace this routine has sustained, cross-cutting closes in ~2-3 more runs, and the full 675 backlog takes roughly **14-15 more daily runs** at current velocity. If that cadence is too slow, the parallel-subagent-batch approach (proven at ~46 files in one run) should become the default rather than the occasional choice.
4. Continue checking `git log origin/main..HEAD` before every run — this repo has repeatedly picked up stray unpushed commits from the other four routines (SSL/credential push failures are silent unless checked).

---

## Cross-track notes

- **Naming collision**: "Phase 1/2/4" (this routine's internal numbering) and "Batch 1" (Track A's numbering) are unrelated schemes that happen to run in the same repo. Anyone reading SESSION_*.md or SKILL.md files needs to know which track's numbering is in play — this doc uses Track A/B/C/D to avoid the ambiguity going forward.
- **No SKILL.md files were modified by this replan.** Updating the stale progress figures baked into `daily-pattern-authorship`, `early-pattern-authorship`, `two-hourly-pattern-authorship`, and `implement-agent-failure-patterns` would change standing automation config owned by routines other than this one — recommend the repo owner review and update those directly, using the Track A/B figures above.
- **Total pattern count will keep moving** across all four tracks concurrently (Track A adds new files; Track B/C/D only edit existing ones) — any snapshot here is stale within a day or two by design. Re-derive, don't trust cached numbers, exactly as Sessions 13-18 already learned for Track A.

**Generated by**: `agent-pattern-mitigation-backfill-4am` scheduled run, 2026-07-19. Contact: soumen@operama.ai
