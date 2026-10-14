# Execution Plan: 5 Patterns per Run, Every 5 Hours

> **What this is.** A prioritized queue of **294 patterns** to write, split into **59 runs of up to 5**, plus the procedure each scheduled run follows and the quality gate every pattern must pass. A scheduled task fires every 5 hours and works through the queue until it is empty. Each run is meant to be unattended: everything it needs is in this file.

## Settings (edit here to change behavior)
| Setting | Value |
|---|---|
| Patterns per run | 5 (raise or lower this number to change the pace; the schedule stays the same) |
| Quality gate | A pattern is **Done** only if it passes the Definition of done below. Anything that doesn't is marked **Needs review** and left for a person. |
| Run mode | **write** (research, write the full pattern, update the catalog). Change to **plan-only** to have each run only research and record briefs in `roadmap/briefs/` without writing patterns. |
| Cadence | Every 5 hours (set in the scheduled task, not in this file) |
| Branch | `claude/zealous-ramanujan-u8zwfk` (commit and push; never open a pull request) |
| Scope | Only files under `agents/by-capability/human-machine-interface/`. Do not edit the older patterns elsewhere in `agents/`. |
| Spelling and examples | American English, and US examples (US cities, dollars, US laws and regulators) |

## How the order was set
Priority combines five things: **(1)** demand evidence (customers' top frustrations: no human, "doesn't understand me", repeating themselves; builders' top barrier: quality), **(2)** gaps in the library (the Code Agent area is empty; upselling, forced re-login, and generic first responses have no patterns), **(3)** harm if wrong (crisis, scams, minors, unauthorized purchases), **(4)** evidence available now, and **(5)** dependencies (a family's first pattern also creates its README). The earlier "Suggested priority" tiers in the [roadmap README](README.md) are superseded by this order. Items the library already covers are not in the queue.

## Run procedure
Follow these steps on every run. Don't skip the checks: earlier work in this project had to be corrected for duplicating existing patterns and for a counting bug.

1. **Sync.** `git fetch origin claude/zealous-ramanujan-u8zwfk` and make sure the working tree is on that branch and up to date. Read this file, `_templates/hmi-pattern.md`, and the two flagship patterns (`core/conversation-leadership/failures/answer-and-go-conversation.md` and `channel-selection/failures/no-channel-switch-or-context-lost.md`) so style stays consistent.
2. **Pick the work.** Take rows marked *In progress* first, then the next **5** rows marked *Queued*, in order. Mark them *In progress*. Don't touch rows marked *Needs review*. If fewer than 5 remain, take what's left. If no *Queued* or *In progress* rows remain, write "Queue complete" in the Run log, disable the schedule (see the Schedule section), and stop.
3. **Write one pattern at a time, finishing each before starting the next:**
   1. **Re-check the library.** Search `agents/` (file names and keywords) for existing patterns on the topic and read the closest one to three. If it is already fully covered, mark the row *Skipped* with the link and take the next *Queued* row. If the row is **Extends**, write only the new human-interface angle and a fix, and link the existing pattern instead of restating it.
   2. **Research properly.** Run at least three web searches (loading the search tools first if needed). **Open the source itself** with the fetch tool whenever it is reachable; don't rely on a search summary alone. For every claim you plan to use, note the source link, what it actually says, and whether you opened it or only read a summary of it. Find every number in the source text; if you can't, don't use the number. Prefer one strong, neutral source over several weak ones. Label vendor, secondary, and single-source evidence. If there is no good evidence, say so in the pattern. **Never invent statistics.**
   3. **Draft the pattern** at the row's target file, using `_templates/hmi-pattern.md`: SEO comment block with real queries; H1 with the phrase people search plus the pattern name; header table with **Goal** and **Primary metric** matching the catalog row and the family README; before-and-after transcripts with US examples; why it happens; an evidence table with caveats; **the fix**; short tests; a metrics table (`Metric | Target | How to measure | Alert at`); related patterns; common questions; and a technical section when the fix needs engineering. For agent-type patterns, set the examples inside that agent's real workflow.
   4. **Flags.** Rows flagged **L** (legal) or **E** (expert) get a "Read this first" note near the top: design guidance, not legal, clinical, or other professional advice, and a review is needed before use. State any regulation only as far as you verified it.
   5. **Review pass.** Check the draft against every item in the **Definition of done** below. Then read the whole file once, top to bottom, as a skeptical reader who has not seen your notes. Fix what you find, and re-read what you changed.
   6. **Family README.** If the folder has no `README.md`, create one in the style of `core/vulnerable-users/README.md` using the family goal from the table below. Otherwise add the new pattern to its table.
   7. **Record the result.** If every item in the Definition of done is true, change the catalog row's last cell to the word `**Written**` followed by a colon and a markdown link to the new pattern (path relative to the roadmap folder), and set the queue row to *Done* with the run number. If any item still fails after a reasonable effort, set the queue row to *Needs review* with a one-line reason, leave the catalog row unchanged, and keep the draft file.
   8. **Verify and commit.** Run `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/rebuild_summary.py` then `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_links.py`, and fix every problem they report. Commit this one pattern with a message like `HMI run N: <id> <name>` plus the attribution lines from the session, then push with `git push -u origin claude/zealous-ramanujan-u8zwfk`. If the push fails on a network error, retry up to 4 times (waits of 2, 4, 8, 16 seconds). If it still fails, record it in the Run log and stop; the next run continues.
4. **Log.** Append an entry to the Run log: run number, UTC date and time, and for each pattern the ID, the result (Done, Needs review, or Skipped), how many sources you opened vs. read only through summaries, any claims left unverified, and what the review pass changed. Add anything you could not check or any correction to earlier files.

## Definition of done (quality gate)
A pattern is *Done* only if **every** item is true.

**Evidence**
- Every statistic, date, legal statement, and quotation in the file has a source link and appears in the source text, or is marked as read through a summary. No number appears without a source. Single-source numbers say so.
- The "Why it matters" caveat column is honest about vendor, secondary, or different-setting evidence, and about what you couldn't open.
- Nothing about law, medicine, or finance goes beyond what a source supports. Rows flagged **L** or **E** carry the "Read this first" note.

**Substance**
- A reader gets the failure and the fix idea from the first two sentences and the header table.
- The fix is concrete and copyable: numbered rules, a reference design (a prompt block, state schema, decision table, or improved transcript), a "Don't over-correct" paragraph, and a hand-off rule. Each rule is testable, so it could become an eval.
- The before-and-after examples are realistic US scenarios, and the "after" example visibly follows the rules. Nothing in the examples contradicts the text.
- "Why it happens" names real causes (three at most), not generic ones.
- The pattern states how it differs from the closest existing library pattern and links to it.

**Measurement**
- The goal and primary metric match the catalog row and the family README.
- The metrics table has Metric, Target, How to measure, and Alert at, and every metric can be computed from logs, evals, or sampled review. Targets are labeled starting points unless a source supports them.
- Each test in the short tests table maps to a rule in the fix.

**Form**
- The SEO comment block holds real search phrases; the H1 includes the phrase people search; questions in the FAQ are written as people ask them.
- Link text is descriptive, and `check_links.py` passes.
- The file is 120 to 250 lines. The technical section appears only when the fix needs engineering.
- American spelling, US examples, and the same layout, voice, and section numbering as the flagship patterns.

If any item can't be met in this run, the pattern is *Needs review*, not *Done*.

## Quality bar and limits
- **Quality beats the count.** A run may write fewer than 5. Never pad with a thin pattern, and never mark something *Done* that hasn't passed the gate.
- **No duplicates.** Don't rewrite a pattern the library already has. Link to it.
- **Honesty.** Mark unverified claims as unverified. Keep thresholds labeled as starting points unless sourced.
- **Don't change** the schedule (except to disable it when the queue is empty), other families' patterns, the older library, or this file's Settings. You may correct errors in files you wrote earlier, and say so in the log.
- **No pull requests.** Push to the branch only.

## Family folders and goals
Create a folder's README on its first pattern. Folders that already have a README (the ten core families and `channel-selection`) keep their goals.

| Folder | Family goal (use verbatim in the family README and each pattern's Goal row) |
|---|---|
| `core/embedded-copilots` | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| `core/response-structure` | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| `core/effort-and-memory` | The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't. |
| `core/response-time` | Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. |
| `core/language-and-locale` | Users are understood and answered in the language, reading level, and format that work for them. |
| `core/conversation-frameworks` | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| `core/privacy-and-governance` | The agent handles personal data and outside services under clear rules, acts only within the rights of the person it serves, explains its limits, and keeps to its rules when pushed. |
| `core/human-oversight` | People overseeing an agent can see what it is doing, understand why, and stop or correct it. |
| `core/measurement-and-feedback` | Teams can tell whether conversations really work, and users can tell the team when they don't. |
| `modalities/voice` | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| `modalities/visual` | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| `agent-types/coding-agents` | A coding agent changes only what was asked, reports truthfully on what it ran, and leaves the codebase safer than it found it. |
| `agent-types/research-and-data-agents` | Analytical agents give answers a person can verify: correct numbers, governed definitions, balanced sources, and a visible method. |
| `agent-types/workflow-automation-agents` | Automation agents change records safely: previewed, conflict-aware, itemised, and stopped when the world changes. |
| `agent-types/it-and-security-agents` | IT and security agents act within verified authority, explain what they close, and never contain or reset without the right approval. |
| `agent-types/finance-agents` | Finance agents post to the right place, reconcile only what exists, and can't be steered into unauthorised payments. |
| `agent-types/healthcare-agents` | Healthcare agents capture what happened accurately, flag what they're unsure of, and keep clinicians genuinely in the loop. |
| `agent-types/sales-agents` | Sales agents use verified information, respect opt-outs, and keep records clean. |
| `agent-types/voice-receptionist-agents` | Phone agents confirm critical details, catch emergencies, and meet disclosure and consent rules. |
| `agent-types/browser-agents` | Browsing agents stay within the user's intent and the site's rules, and ask before consequential actions. |
| `agent-types/shopping-agents` | Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed. |
| `agent-types/education-agents` | Tutors teach, are accurate, treat students fairly, and protect their data. |
| `agent-types/personal-assistants` | Assistants act for the user, with confirmation on anything sent, booked, or paid. |
| `agent-types/hr-agents` | HR agents route sensitive matters correctly and show each person only what they're entitled to see. |
| `agent-types/legal-agents` | Legal agents stay within permitted scope and protect confidential and privileged material. |
| `agent-types/multi-agent-platforms` | Multiple agents present one coherent, honest voice and don't expose their internal coordination. |
| `agent-types/tool-ecosystems` | Agents connect to tools only through authenticated, vetted, and clearly attributed channels. |
| `agent-types/meeting-agents` | Meeting assistants record with everyone's knowledge and summarise faithfully. |
| `agent-types/companion-and-wellbeing-agents` | Companion and wellbeing agents support users without exploiting them or standing in for professional care. |
| `agent-types/customer-support-agents` | Support agents are measured and paid by what customers confirm was solved. |

## Run schedule
Run N covers queue orders as shown. At one run every 5 hours, 59 runs take about 290 hours between the first and last start, roughly 12.1 days. A run that marks a pattern *Needs review* doesn't delay the queue, but those patterns need a person.

| Run | Orders | Themes |
|---|---|---|
| 1 | 1-5 (5) | Understood, in context, and a real first reply |
| 2 | 6-10 (5) | Understood, in context, and a real first reply |
| 3 | 11-15 (5) | Understood, in context, and a real first reply |
| 4 | 16-20 (5) | Understood, in context, and a real first reply; Upselling and conflicts of interest |
| 5 | 21-25 (5) | Upselling and conflicts of interest; Reply shape, length, and closers |
| 6 | 26-30 (5) | Reply shape, length, and closers |
| 7 | 31-35 (5) | Reply shape, length, and closers |
| 8 | 36-40 (5) | Reply shape, length, and closers |
| 9 | 41-45 (5) | Reply shape, length, and closers; Effort, completeness, and memory |
| 10 | 46-50 (5) | Effort, completeness, and memory |
| 11 | 51-55 (5) | Effort, completeness, and memory |
| 12 | 56-60 (5) | Effort, completeness, and memory; Response time and waiting |
| 13 | 61-65 (5) | Response time and waiting |
| 14 | 66-70 (5) | Response time and waiting; Measurement and feedback |
| 15 | 71-75 (5) | Measurement and feedback; High-harm picks |
| 16 | 76-80 (5) | High-harm picks |
| 17 | 81-85 (5) | High-harm picks; Coding agents |
| 18 | 86-90 (5) | Coding agents; Research and data-analysis agents |
| 19 | 91-95 (5) | Research and data-analysis agents; Workflow-automation agents |
| 20 | 96-100 (5) | Workflow-automation agents; IT and security agents |
| 21 | 101-105 (5) | IT and security agents; Healthcare agents |
| 22 | 106-110 (5) | Healthcare agents; Transcription and listening |
| 23 | 111-115 (5) | Transcription and listening |
| 24 | 116-120 (5) | Transcription and listening |
| 25 | 121-125 (5) | Transcription and listening; Finance agents |
| 26 | 126-130 (5) | Finance agents; Chat and core, the rest |
| 27 | 131-135 (5) | Chat and core, the rest |
| 28 | 136-140 (5) | Chat and core, the rest |
| 29 | 141-145 (5) | Chat and core, the rest; Selling and sales agents |
| 30 | 146-150 (5) | Selling and sales agents |
| 31 | 151-155 (5) | Selling and sales agents |
| 32 | 156-160 (5) | Selling and sales agents; Support and style frameworks |
| 33 | 161-165 (5) | Support and style frameworks |
| 34 | 166-170 (5) | Support and style frameworks |
| 35 | 171-175 (5) | Support and style frameworks |
| 36 | 176-180 (5) | Privacy, governance, and access |
| 37 | 181-185 (5) | Privacy, governance, and access |
| 38 | 186-190 (5) | Privacy, governance, and access |
| 39 | 191-195 (5) | Privacy, governance, and access; Emerging surfaces, the rest |
| 40 | 196-200 (5) | Emerging surfaces, the rest |
| 41 | 201-205 (5) | Emerging surfaces, the rest |
| 42 | 206-210 (5) | Emerging surfaces, the rest |
| 43 | 211-215 (5) | Emerging surfaces, the rest; Voice |
| 44 | 216-220 (5) | Voice |
| 45 | 221-225 (5) | Voice |
| 46 | 226-230 (5) | Voice |
| 47 | 231-235 (5) | Voice; Browser, shopping, and assistant agents |
| 48 | 236-240 (5) | Browser, shopping, and assistant agents |
| 49 | 241-245 (5) | Browser, shopping, and assistant agents; Language and locale |
| 50 | 246-250 (5) | Language and locale |
| 51 | 251-255 (5) | Language and locale |
| 52 | 256-260 (5) | Language and locale; Education, HR, legal, and multi-agent |
| 53 | 261-265 (5) | Education, HR, legal, and multi-agent |
| 54 | 266-270 (5) | Education, HR, legal, and multi-agent; Visual and oversight, the rest |
| 55 | 271-275 (5) | Visual and oversight, the rest |
| 56 | 276-280 (5) | Visual and oversight, the rest |
| 57 | 281-285 (5) | Visual and oversight, the rest |
| 58 | 286-290 (5) | Visual and oversight, the rest |
| 59 | 291-294 (4) | Visual and oversight, the rest |

## Queue
Status: *Queued*, *In progress*, *Done*, *Needs review*, or *Skipped*. The **Library** column is the status in the catalog when the queue was built (**New** or **Extends**).

| # | ID | Pattern | Library | Flags | Target file | Status | Run |
|---|---|---|---|---|---|---|---|
| 1 | CP-08 | Missing the obvious intent | Extends | - | `core/embedded-copilots/failures/missing-the-obvious-intent.md` | Queued |  |
| 2 | CP-10 | Irrelevant or already-answered clarifying questions | Extends | - | `core/embedded-copilots/failures/irrelevant-or-already-answered-clarifying-questions.md` | Queued |  |
| 3 | CP-13 | Ignores the page, selection, and form state | New | R | `core/embedded-copilots/failures/ignores-the-page-selection-and-form-state.md` | Queued |  |
| 4 | CP-14 | Re-asks for known information | Extends | V | `core/embedded-copilots/failures/re-asks-for-known-information.md` | Queued |  |
| 5 | CP-15 | Forces a fresh login | New | E | `core/embedded-copilots/failures/forces-a-fresh-login.md` | Queued |  |
| 6 | CP-16 | Ignores role, plan, locale, and device | Extends | - | `core/embedded-copilots/failures/ignores-role-plan-locale-and-device.md` | Queued |  |
| 7 | CP-17 | Ignores recent activity and history | Extends | - | `core/embedded-copilots/failures/ignores-recent-activity-and-history.md` | Queued |  |
| 8 | CP-19 | Context lost across a multi-session task | Extends | - | `core/embedded-copilots/failures/context-lost-across-a-multi-session-task.md` | Queued |  |
| 9 | CP-20 | Generic first response | New | R | `core/embedded-copilots/failures/generic-first-response.md` | Queued |  |
| 10 | CP-21 | Greeting-only first turn | New | - | `core/embedded-copilots/failures/greeting-only-first-turn.md` | Queued |  |
| 11 | CP-22 | No likely-next-action suggestions | New | R | `core/embedded-copilots/failures/no-likely-next-action-suggestions.md` | Queued |  |
| 12 | CP-23 | Boilerplate steps that don't match the user's setup | Extends | - | `core/embedded-copilots/failures/boilerplate-steps-that-don-t-match-the-user-s.md` | Queued |  |
| 13 | CP-09 | Over-complicating simple tasks | Extends | - | `core/embedded-copilots/failures/over-complicating-simple-tasks.md` | Queued |  |
| 14 | CP-11 | Keyword-matched documentation instead of an answer | Extends | - | `core/embedded-copilots/failures/keyword-matched-documentation-instead-of-an-answer.md` | Queued |  |
| 15 | CP-12 | Doesn't say what it can do | New | R | `core/embedded-copilots/failures/doesn-t-say-what-it-can-do.md` | Queued |  |
| 16 | XA-01 | Dead-end 'I don't understand' replies | Extends | V, R | `core/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md` | Queued |  |
| 17 | CP-01 | Help that becomes a sales pitch | New | V, R, L | `core/embedded-copilots/failures/help-that-becomes-a-sales-pitch.md` | Queued |  |
| 18 | CP-02 | Recommending features the user can't use | Extends | - | `core/embedded-copilots/failures/recommending-features-the-user-can-t-use.md` | Queued |  |
| 19 | CP-03 | Answers withheld behind an upgrade, unsaid | New | L | `core/embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md` | Queued |  |
| 20 | CP-06 | Obstructing cancellation, downgrade, or refund | Extends | V, L | `core/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md` | Queued |  |
| 21 | CP-04 | Self-preferencing | New | R, L | `core/embedded-copilots/failures/self-preferencing.md` | Queued |  |
| 22 | CP-05 | Paid content blended into answers | New | V, R, L | `core/embedded-copilots/failures/paid-content-blended-into-answers.md` | Queued |  |
| 23 | CP-07 | Helpfulness theatre | Extends | - | `core/embedded-copilots/failures/helpfulness-theatre.md` | Queued |  |
| 24 | RS-01 | Answer buried | New | - | `core/response-structure/failures/answer-buried.md` | Queued |  |
| 25 | RS-02 | Wall of text | Extends | - | `core/response-structure/failures/wall-of-text.md` | Queued |  |
| 26 | RS-03 | Over-long replies | Extends | V | `core/response-structure/failures/over-long-replies.md` | Queued |  |
| 27 | RS-04 | Over-short replies | Extends | - | `core/response-structure/failures/over-short-replies.md` | Queued |  |
| 28 | RS-05 | Message bursts | New | - | `core/response-structure/failures/message-bursts.md` | Queued |  |
| 29 | RS-06 | Unstructured procedures | New | - | `core/response-structure/failures/unstructured-procedures.md` | Queued |  |
| 30 | RS-07 | Key details buried | New | - | `core/response-structure/failures/key-details-buried.md` | Queued |  |
| 31 | RS-08 | Bullet and heading overuse | New | R | `core/response-structure/failures/bullet-and-heading-overuse.md` | Queued |  |
| 32 | RS-09 | Filler and padding | New | R | `core/response-structure/failures/filler-and-padding.md` | Queued |  |
| 33 | RS-10 | Structure flips between turns | Extends | - | `core/response-structure/failures/structure-flips-between-turns.md` | Queued |  |
| 34 | RS-11 | Formatting artifacts | Extends | - | `core/response-structure/failures/formatting-artifacts.md` | Queued |  |
| 35 | RS-12 | Wrong format for the medium | Extends | - | `core/response-structure/failures/wrong-format-for-the-medium.md` | Queued |  |
| 36 | RS-13 | Cut-off replies | Extends | - | `core/response-structure/failures/cut-off-replies.md` | Queued |  |
| 37 | RS-14 | No reply to acknowledgments and closers | Extends | - | `core/response-structure/failures/no-reply-to-acknowledgments-and-closers.md` | Queued |  |
| 38 | RS-15 | Over-reply to acknowledgments | New | - | `core/response-structure/failures/over-reply-to-acknowledgments.md` | Queued |  |
| 39 | RS-16 | Misreading 'ok' and minimal replies | Extends | V, R | `core/response-structure/failures/misreading-ok-and-minimal-replies.md` | Queued |  |
| 40 | RS-17 | Length mismatch with the user's effort | New | - | `core/response-structure/failures/length-mismatch-with-the-user-s-effort.md` | Queued |  |
| 41 | RS-18 | Link and resource dumps | New | R | `core/response-structure/failures/link-and-resource-dumps.md` | Queued |  |
| 42 | EM-01 | Lazy completion | New | V | `core/effort-and-memory/failures/lazy-completion.md` | Queued |  |
| 43 | EM-02 | Deferring work to the user | New | - | `core/effort-and-memory/failures/deferring-work-to-the-user.md` | Queued |  |
| 44 | EM-06 | Skipped steps with no receipt | Extends | - | `core/effort-and-memory/failures/skipped-steps-with-no-receipt.md` | Queued |  |
| 45 | EM-11 | No warning of context loss | Extends | - | `core/effort-and-memory/failures/no-warning-of-context-loss.md` | Queued |  |
| 46 | EM-09 | Early-assumption lock-in | Extends | V | `core/effort-and-memory/failures/early-assumption-lock-in.md` | Queued |  |
| 47 | EM-12 | Critical facts not pinned | Extends | - | `core/effort-and-memory/failures/critical-facts-not-pinned.md` | Queued |  |
| 48 | EM-03 | Underthinking | Extends | V | `core/effort-and-memory/failures/underthinking.md` | Queued |  |
| 49 | EM-08 | Partial answers to multi-part questions | New | - | `core/effort-and-memory/failures/partial-answers-to-multi-part-questions.md` | Queued |  |
| 50 | EM-13 | Fresh-session amnesia | New | - | `core/effort-and-memory/failures/fresh-session-amnesia.md` | Queued |  |
| 51 | EM-14 | Silent capability downgrade | Extends | - | `core/effort-and-memory/failures/silent-capability-downgrade.md` | Queued |  |
| 52 | EM-17 | Defensive over-deferral to professionals | Extends | R, E | `core/effort-and-memory/failures/defensive-over-deferral-to-professionals.md` | Queued |  |
| 53 | EM-21 | Giving up too early on a tool error | Extends | - | `core/effort-and-memory/failures/giving-up-too-early-on-a-tool-error.md` | Queued |  |
| 54 | EM-22 | Overclaiming effort | Extends | - | `core/effort-and-memory/failures/overclaiming-effort.md` | Queued |  |
| 55 | EM-23 | Scope shrink on long tasks | New | - | `core/effort-and-memory/failures/scope-shrink-on-long-tasks.md` | Queued |  |
| 56 | EM-25 | Handoff of incomplete work with no TODO list | Extends | - | `core/effort-and-memory/failures/handoff-of-incomplete-work-with-no-todo-list.md` | Queued |  |
| 57 | RT-01 | Slow first response | Extends | V, R | `core/response-time/failures/slow-first-response.md` | Queued |  |
| 58 | RT-02 | Silent long-running work | Extends | V | `core/response-time/failures/silent-long-running-work.md` | Queued |  |
| 59 | RT-03 | Unpredictable latency | Extends | V | `core/response-time/failures/unpredictable-latency.md` | Queued |  |
| 60 | RT-06 | Silent failure and timeout | Extends | - | `core/response-time/failures/silent-failure-and-timeout.md` | Queued |  |
| 61 | RT-07 | Queue wait with no ETA | Extends | - | `core/response-time/failures/queue-wait-with-no-eta.md` | Queued |  |
| 62 | RT-14 | Fast replies, slow resolution | Extends | V | `core/response-time/failures/fast-replies-slow-resolution.md` | Queued |  |
| 63 | RT-04 | Pacing mismatch | New | R | `core/response-time/failures/pacing-mismatch.md` | Queued |  |
| 64 | RT-05 | Deceptive typing indicators | New | L | `core/response-time/failures/deceptive-typing-indicators.md` | Queued |  |
| 65 | RT-08 | Missed async promises | Extends | - | `core/response-time/failures/missed-async-promises.md` | Queued |  |
| 66 | RT-09 | Session timeout and lost context | New | - | `core/response-time/failures/session-timeout-and-lost-context.md` | Queued |  |
| 67 | RT-10 | Impatient idle nudges | New | - | `core/response-time/failures/impatient-idle-nudges.md` | Queued |  |
| 68 | RT-11 | Urgency-blind pacing | New | - | `core/response-time/failures/urgency-blind-pacing.md` | Queued |  |
| 69 | RT-12 | Streaming that rewrites itself | Extends | - | `core/response-time/failures/streaming-that-rewrites-itself.md` | Queued |  |
| 70 | XA-02 | Conversation-quality measurement gaps | Extends | V, R | `core/measurement-and-feedback/failures/conversation-quality-measurement-gaps.md` | Queued |  |
| 71 | XA-03 | No way to report bad behaviour | New | R | `core/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md` | Queued |  |
| 72 | CC-08 | Scam victim not interrupted | New | E, L | `core/vulnerable-users/failures/scam-victim-not-interrupted.md` | Queued |  |
| 73 | CC-16 | Romantic or parasocial dependence | New | L, E | `core/relational-and-boundaries/failures/romantic-or-parasocial-dependence.md` | Queued |  |
| 74 | CC-11 | Teens: persuasion and dependence | Extends | L, E | `core/age-adaptation/failures/teens-persuasion-and-dependence.md` | Queued |  |
| 75 | CC-09 | Older or cognitively impaired users | New | E | `core/vulnerable-users/failures/older-or-cognitively-impaired-users.md` | Queued |  |
| 76 | CC-10 | Financial hardship mishandled | New | L, E | `core/vulnerable-users/failures/financial-hardship-mishandled.md` | Queued |  |
| 77 | CC-07 | Mishandled abuse | New | - | `core/difficult-customers/failures/mishandled-abuse.md` | Queued |  |
| 78 | VI-03 | Dark patterns | New | V, L | `modalities/visual/failures/dark-patterns.md` | Queued |  |
| 79 | OV-01 | Approval fatigue | Extends | V | `core/human-oversight/failures/approval-fatigue.md` | Queued |  |
| 80 | FW-S01 | Pitching before discovery | Extends | V | `core/conversation-frameworks/failures/pitching-before-discovery.md` | Queued |  |
| 81 | EX-07 | Hidden instructions hijack a browsing agent | Extends | V | `agent-types/browser-agents/failures/hidden-instructions-hijack-a-browsing-agent.md` | Queued |  |
| 82 | EX-01 | Purchase without clear authorisation | Extends | V, R, L | `agent-types/shopping-agents/failures/purchase-without-clear-authorisation.md` | Queued |  |
| 83 | EX-22 | Per-resolution pricing rewards counting things as resolved | Extends | V, R | `agent-types/customer-support-agents/failures/per-resolution-pricing-rewards-counting-things-as-resolved.md` | Queued |  |
| 84 | CD-01 | Edits beyond the request | Extends | R | `agent-types/coding-agents/failures/edits-beyond-the-request.md` | Queued |  |
| 85 | CD-02 | Claims tests pass without running them, or edits tests to pass | Extends | V, R | `agent-types/coding-agents/failures/claims-tests-pass-without-running-them-or-edits-tests.md` | Queued |  |
| 86 | CD-03 | Invented packages and APIs | New | R | `agent-types/coding-agents/failures/invented-packages-and-apis.md` | Queued |  |
| 87 | CD-04 | Secrets and insecure code accepted by non-experts | Extends | - | `agent-types/coding-agents/failures/secrets-and-insecure-code-accepted-by-non-experts.md` | Queued |  |
| 88 | CD-05 | Destroys uncommitted work | Extends | - | `agent-types/coding-agents/failures/destroys-uncommitted-work.md` | Queued |  |
| 89 | CD-06 | Forgets project conventions in long sessions | Extends | - | `agent-types/coding-agents/failures/forgets-project-conventions-in-long-sessions.md` | Queued |  |
| 90 | DA-01 | Wrong joins and double counting | New | R | `agent-types/research-and-data-agents/failures/wrong-joins-and-double-counting.md` | Queued |  |
| 91 | DA-02 | Wrong business definitions | New | - | `agent-types/research-and-data-agents/failures/wrong-business-definitions.md` | Queued |  |
| 92 | DA-03 | One-sided or cherry-picked sources | New | R | `agent-types/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md` | Queued |  |
| 93 | DA-04 | Claims to have read inaccessible sources | Extends | - | `agent-types/research-and-data-agents/failures/claims-to-have-read-inaccessible-sources.md` | Queued |  |
| 94 | DA-05 | Method and query not shown | Extends | - | `agent-types/research-and-data-agents/failures/method-and-query-not-shown.md` | Queued |  |
| 95 | WA-01 | No dry-run before bulk changes | Extends | - | `agent-types/workflow-automation-agents/failures/no-dry-run-before-bulk-changes.md` | Queued |  |
| 96 | WA-02 | Overwrites a person's recent edit | Extends | - | `agent-types/workflow-automation-agents/failures/overwrites-a-person-s-recent-edit.md` | Queued |  |
| 97 | WA-03 | Partial batch reported as done | Extends | - | `agent-types/workflow-automation-agents/failures/partial-batch-reported-as-done.md` | Queued |  |
| 98 | WA-04 | Silent breakage after a UI or schema change | Extends | - | `agent-types/workflow-automation-agents/failures/silent-breakage-after-a-ui-or-schema-change.md` | Queued |  |
| 99 | IT-01 | Credential reset for a manipulated caller | Extends | - | `agent-types/it-and-security-agents/failures/credential-reset-for-a-manipulated-caller.md` | Queued |  |
| 100 | IT-02 | True alerts closed as false positives | New | - | `agent-types/it-and-security-agents/failures/true-alerts-closed-as-false-positives.md` | Queued |  |
| 101 | IT-03 | Containment without human sign-off | Extends | - | `agent-types/it-and-security-agents/failures/containment-without-human-sign-off.md` | Queued |  |
| 102 | IT-04 | Outdated runbook followed with confidence | Extends | - | `agent-types/it-and-security-agents/failures/outdated-runbook-followed-with-confidence.md` | Queued |  |
| 103 | IT-05 | Fabricated indicators or vulnerability details | Extends | - | `agent-types/it-and-security-agents/failures/fabricated-indicators-or-vulnerability-details.md` | Queued |  |
| 104 | HC-01 | Scribe omissions and invented content | Extends | V, E, L | `agent-types/healthcare-agents/failures/scribe-omissions-and-invented-content.md` | Queued |  |
| 105 | HC-02 | Notes approved without being read | New | E | `agent-types/healthcare-agents/failures/notes-approved-without-being-read.md` | Queued |  |
| 106 | HC-03 | Recording consent not captured | New | L | `agent-types/healthcare-agents/failures/recording-consent-not-captured.md` | Queued |  |
| 107 | HC-04 | Fabricated clinical justification in appeals | New | R, L, E | `agent-types/healthcare-agents/failures/fabricated-clinical-justification-in-appeals.md` | Queued |  |
| 108 | HC-05 | Patient summaries too simple to be safe | New | E | `agent-types/healthcare-agents/failures/patient-summaries-too-simple-to-be-safe.md` | Queued |  |
| 109 | TR-04 | Transcription hallucination | New | V | `modalities/voice/failures/transcription-hallucination.md` | Queued |  |
| 110 | TR-03 | Non-speech heard as speech | Extends | - | `modalities/voice/failures/non-speech-heard-as-speech.md` | Queued |  |
| 111 | TR-01 | Names with no repair path | Extends | - | `modalities/voice/failures/names-with-no-repair-path.md` | Queued |  |
| 112 | TR-02 | Proper nouns beyond names | Extends | V, R | `modalities/voice/failures/proper-nouns-beyond-names.md` | Queued |  |
| 113 | TR-15 | Transcript treated as ground truth | Extends | V | `modalities/voice/failures/transcript-treated-as-ground-truth.md` | Queued |  |
| 114 | TR-16 | Word-error-rate-only evaluation | New | R | `modalities/voice/failures/word-error-rate-only-evaluation.md` | Queued |  |
| 115 | TR-09 | Dropped negations and small words | New | R, E | `modalities/voice/failures/dropped-negations-and-small-words.md` | Queued |  |
| 116 | TR-08 | Punctuation and segmentation errors | New | R | `modalities/voice/failures/punctuation-and-segmentation-errors.md` | Queued |  |
| 117 | TR-10 | Spelled-out strings | Extends | - | `modalities/voice/failures/spelled-out-strings.md` | Queued |  |
| 118 | TR-05 | Voice-activity-detection misfires | Extends | - | `modalities/voice/failures/voice-activity-detection-misfires.md` | Queued |  |
| 119 | TR-07 | Speaker attribution errors | Extends | - | `modalities/voice/failures/speaker-attribution-errors.md` | Queued |  |
| 120 | TR-17 | Spoken PII persists in transcripts and audio | Extends | L | `modalities/voice/failures/spoken-pii-persists-in-transcripts-and-audio.md` | Queued |  |
| 121 | TR-18 | Children's and atypical speech | Extends | V, E | `modalities/voice/failures/children-s-and-atypical-speech.md` | Queued |  |
| 122 | TR-19 | Wrong recognition model for the speaker | Extends | - | `modalities/voice/failures/wrong-recognition-model-for-the-speaker.md` | Queued |  |
| 123 | TR-20 | Machine audio treated as a person | Extends | - | `modalities/voice/failures/machine-audio-treated-as-a-person.md` | Queued |  |
| 124 | FN-01 | Posting to the wrong period or account | New | - | `agent-types/finance-agents/failures/posting-to-the-wrong-period-or-account.md` | Queued |  |
| 125 | FN-02 | Inventing reconciling items | New | R | `agent-types/finance-agents/failures/inventing-reconciling-items.md` | Queued |  |
| 126 | FN-03 | Splitting payments under approval limits | New | - | `agent-types/finance-agents/failures/splitting-payments-under-approval-limits.md` | Queued |  |
| 127 | FN-04 | Payment approved by a deepfake or spoofed email | Extends | - | `agent-types/finance-agents/failures/payment-approved-by-a-deepfake-or-spoofed-email.md` | Queued |  |
| 128 | CC-01 | Closing without confirmation | Extends | - | `core/conversation-leadership/failures/closing-without-confirmation.md` | Queued |  |
| 129 | CC-02 | Over-solemn handling of low-stakes requests | New | - | `core/stakes-calibration/failures/over-solemn-handling-of-low-stakes-requests.md` | Queued |  |
| 130 | CC-03 | Missed subtext | Extends | - | `core/emotional-intelligence/failures/missed-subtext.md` | Queued |  |
| 131 | CC-04 | Fixing before listening | New | - | `core/emotional-intelligence/failures/fixing-before-listening.md` | Queued |  |
| 132 | CC-05 | No follow-through | New | - | `core/trust-and-rapport/failures/no-follow-through.md` | Queued |  |
| 133 | CC-06 | Over-hedging | Extends | - | `core/trust-and-rapport/failures/over-hedging.md` | Queued |  |
| 134 | CC-12 | Technology-literacy mismatch | New | - | `core/cultural-adaptation/failures/technology-literacy-mismatch.md` | Queued |  |
| 135 | CC-13 | Regional and community styles | New | R | `core/cultural-adaptation/failures/regional-and-community-styles.md` | Queued |  |
| 136 | CC-14 | Accessibility in chat | New | E, L | `core/fairness-and-identity/failures/accessibility-in-chat.md` | Queued |  |
| 137 | CC-15 | Over-correcting for identity | New | - | `core/fairness-and-identity/failures/over-correcting-for-identity.md` | Queued |  |
| 138 | CC-18 | Channel chosen for organisational convenience | New | - | `channel-selection/failures/channel-chosen-for-organisational-convenience.md` | Queued |  |
| 139 | CC-19 | User-context channel mismatch | New | E | `channel-selection/failures/user-context-channel-mismatch.md` | Queued |  |
| 140 | CC-22 | Creepy personalisation and memory | Extends | L | `core/trust-and-rapport/failures/creepy-personalisation-and-memory.md` | Queued |  |
| 141 | CC-23 | Proactive outreach overreach | New | L | `core/relational-and-boundaries/failures/proactive-outreach-overreach.md` | Queued |  |
| 142 | SA-01 | Invented personalisation | Extends | - | `agent-types/sales-agents/failures/invented-personalisation.md` | Queued |  |
| 143 | SA-02 | Unsubscribe requests not honoured | New | L | `agent-types/sales-agents/failures/unsubscribe-requests-not-honoured.md` | Queued |  |
| 144 | SA-03 | Wrong contact merged in the CRM | Extends | - | `agent-types/sales-agents/failures/wrong-contact-merged-in-the-crm.md` | Queued |  |
| 145 | SA-04 | Double-booked meetings | Extends | - | `agent-types/sales-agents/failures/double-booked-meetings.md` | Queued |  |
| 146 | FW-S02 | No qualification | Extends | R | `core/conversation-frameworks/failures/no-qualification.md` | Queued |  |
| 147 | FW-S03 | Feature dump instead of insight | New | V | `core/conversation-frameworks/failures/feature-dump-instead-of-insight.md` | Queued |  |
| 148 | FW-S04 | Mishandled objections | New | R | `core/conversation-frameworks/failures/mishandled-objections.md` | Queued |  |
| 149 | FW-S05 | No ask | New | - | `core/conversation-frameworks/failures/no-ask.md` | Queued |  |
| 150 | FW-S06 | Manipulative closing | Extends | L, R | `core/conversation-frameworks/failures/manipulative-closing.md` | Queued |  |
| 151 | FW-S07 | Discount-first selling | Extends | - | `core/conversation-frameworks/failures/discount-first-selling.md` | Queued |  |
| 152 | FW-S08 | No follow-up | New | L | `core/conversation-frameworks/failures/no-follow-up.md` | Queued |  |
| 153 | FW-S09 | Buying-committee blindness (B2B) | New | R | `core/conversation-frameworks/failures/buying-committee-blindness-b2b.md` | Queued |  |
| 154 | FW-S10 | Wrong-fit recommendation | New | - | `core/conversation-frameworks/failures/wrong-fit-recommendation.md` | Queued |  |
| 155 | FW-S11 | Upsell at the wrong moment | New | - | `core/conversation-frameworks/failures/upsell-at-the-wrong-moment.md` | Queued |  |
| 156 | FW-S12 | Lead handoff without qualification | Extends | - | `core/conversation-frameworks/failures/lead-handoff-without-qualification.md` | Queued |  |
| 157 | FW-C01 | No triage or severity check | Extends | - | `core/conversation-frameworks/failures/no-triage-or-severity-check.md` | Queued |  |
| 158 | FW-C02 | Unstructured troubleshooting | New | - | `core/conversation-frameworks/failures/unstructured-troubleshooting.md` | Queued |  |
| 159 | FW-C03 | Symptom fixed, root cause missed | New | - | `core/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md` | Queued |  |
| 160 | FW-C04 | High customer effort | Extends | V | `core/conversation-frameworks/failures/high-customer-effort.md` | Queued |  |
| 161 | FW-C05 | No proactive updates | New | - | `core/conversation-frameworks/failures/no-proactive-updates.md` | Queued |  |
| 162 | FW-C06 | No learning loop | Extends | - | `core/conversation-frameworks/failures/no-learning-loop.md` | Queued |  |
| 163 | FW-C07 | Service recovery failure | New | R | `core/conversation-frameworks/failures/service-recovery-failure.md` | Queued |  |
| 164 | FW-C08 | Bad news without structure | New | V, E | `core/conversation-frameworks/failures/bad-news-without-structure.md` | Queued |  |
| 165 | FW-C09 | Instructions without comprehension checks | New | R | `core/conversation-frameworks/failures/instructions-without-comprehension-checks.md` | Queued |  |
| 166 | FW-C10 | Behaviour-change talk without listening skills | New | V, E | `core/conversation-frameworks/failures/behaviour-change-talk-without-listening-skills.md` | Queued |  |
| 167 | FW-M01 | No style matching | Extends | V, R | `core/conversation-frameworks/failures/no-style-matching.md` | Queued |  |
| 168 | FW-M02 | Over-mirroring | New | - | `core/conversation-frameworks/failures/over-mirroring.md` | Queued |  |
| 169 | FW-M03 | Mirroring hostility | New | - | `core/conversation-frameworks/failures/mirroring-hostility.md` | Queued |  |
| 170 | FW-M04 | Imitating dialect or errors | New | E | `core/conversation-frameworks/failures/imitating-dialect-or-errors.md` | Queued |  |
| 171 | FW-M06 | Style whiplash | Extends | - | `core/conversation-frameworks/failures/style-whiplash.md` | Queued |  |
| 172 | FW-M07 | No reflective listening | New | V | `core/conversation-frameworks/failures/no-reflective-listening.md` | Queued |  |
| 173 | FW-M08 | Misused tactical empathy | New | V, R | `core/conversation-frameworks/failures/misused-tactical-empathy.md` | Queued |  |
| 174 | FW-O01 | Cooperation violations | Extends | R | `core/conversation-frameworks/failures/cooperation-violations.md` | Queued |  |
| 175 | FW-O02 | Bad endings | Extends | R | `core/conversation-frameworks/failures/bad-endings.md` | Queued |  |
| 176 | GV-01 | Over-collection of personal data | Extends | - | `core/privacy-and-governance/failures/over-collection-of-personal-data.md` | Queued |  |
| 177 | GV-02 | Sensitive data echoed or read aloud | Extends | - | `core/privacy-and-governance/failures/sensitive-data-echoed-or-read-aloud.md` | Queued |  |
| 178 | GV-03 | Third-party data shared by users | New | R, L | `core/privacy-and-governance/failures/third-party-data-shared-by-users.md` | Queued |  |
| 179 | GV-05 | Sensitive-category inference | New | R, L, E | `core/privacy-and-governance/failures/sensitive-category-inference.md` | Queued |  |
| 180 | GV-07 | Memory the user can't see or control | Extends | L | `core/privacy-and-governance/failures/memory-the-user-can-t-see-or-control.md` | Queued |  |
| 181 | GV-08 | Privacy-rights requests not recognised | New | V, L, R | `core/privacy-and-governance/failures/privacy-rights-requests-not-recognised.md` | Queued |  |
| 182 | GV-09 | Weak or excessive identity verification | Extends | - | `core/privacy-and-governance/failures/weak-or-excessive-identity-verification.md` | Queued |  |
| 183 | GV-10 | No notice or consent at the moment of collection | Extends | L | `core/privacy-and-governance/failures/no-notice-or-consent-at-the-moment-of-collection.md` | Queued |  |
| 184 | GV-12 | Recording, transcription, and training-use notice | Extends | L | `core/privacy-and-governance/failures/recording-transcription-and-training-use-notice.md` | Queued |  |
| 185 | GV-14 | Role claims accepted from the conversation | Extends | - | `core/privacy-and-governance/failures/role-claims-accepted-from-the-conversation.md` | Queued |  |
| 186 | GV-23 | Denial messages that leak or dead-end | Extends | - | `core/privacy-and-governance/failures/denial-messages-that-leak-or-dead-end.md` | Queued |  |
| 187 | GV-34 | Rules not explainable to users | Extends | - | `core/privacy-and-governance/failures/rules-not-explainable-to-users.md` | Queued |  |
| 188 | GV-36 | No user-facing record of what the bot said or promised | New | L | `core/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md` | Queued |  |
| 189 | GV-37 | Consequential automated decisions with no explanation or review | Extends | R, L | `core/privacy-and-governance/failures/consequential-automated-decisions-with-no-explanation-or-review.md` | Queued |  |
| 190 | GV-38 | Manipulative persuasion | Extends | L, E | `core/privacy-and-governance/failures/manipulative-persuasion.md` | Queued |  |
| 191 | GV-39 | Deceptive anthropomorphism | Extends | - | `core/privacy-and-governance/failures/deceptive-anthropomorphism.md` | Queued |  |
| 192 | GV-40 | Engagement-maximising design that harms | New | L, E | `core/privacy-and-governance/failures/engagement-maximising-design-that-harms.md` | Queued |  |
| 193 | GV-41 | Exploiting vulnerable circumstances | New | L, E | `core/privacy-and-governance/failures/exploiting-vulnerable-circumstances.md` | Queued |  |
| 194 | GV-42 | Calibration between helping with wrongdoing and over-blocking | Extends | E | `core/privacy-and-governance/failures/calibration-between-helping-with-wrongdoing-and-over-blocking.md` | Queued |  |
| 195 | EX-02 | Wrong item or variant bought | Extends | - | `agent-types/shopping-agents/failures/wrong-item-or-variant-bought.md` | Queued |  |
| 196 | EX-03 | Merchant content steers the shopping agent | Extends | V | `agent-types/shopping-agents/failures/merchant-content-steers-the-shopping-agent.md` | Queued |  |
| 197 | EX-04 | Spend and category limits not enforced | Extends | - | `agent-types/shopping-agents/failures/spend-and-category-limits-not-enforced.md` | Queued |  |
| 198 | EX-05 | No clear route when an agent buys wrongly | New | R, L | `agent-types/shopping-agents/failures/no-clear-route-when-an-agent-buys-wrongly.md` | Queued |  |
| 199 | EX-06 | Sponsored ranking inside agent recommendations | New | L | `agent-types/shopping-agents/failures/sponsored-ranking-inside-agent-recommendations.md` | Queued |  |
| 200 | EX-08 | Agent uses the user's logged-in sessions with full reach | Extends | - | `agent-types/browser-agents/failures/agent-uses-the-user-s-logged-in-sessions-with.md` | Queued |  |
| 201 | EX-09 | Misreading the screen | New | R | `agent-types/browser-agents/failures/misreading-the-screen.md` | Queued |  |
| 202 | EX-11 | Tool-name collisions | Extends | V | `agent-types/tool-ecosystems/failures/tool-name-collisions.md` | Queued |  |
| 203 | EX-12 | Unauthenticated tool servers | Extends | V | `agent-types/tool-ecosystems/failures/unauthenticated-tool-servers.md` | Queued |  |
| 204 | EX-14 | Consent fatigue from tool sprawl | Extends | - | `agent-types/tool-ecosystems/failures/consent-fatigue-from-tool-sprawl.md` | Queued |  |
| 205 | EX-16 | Recorders that join without everyone's consent | New | V, L | `agent-types/meeting-agents/failures/recorders-that-join-without-everyone-s-consent.md` | Queued |  |
| 206 | EX-17 | Summaries that misattribute or invent action items | Extends | R | `agent-types/meeting-agents/failures/summaries-that-misattribute-or-invent-action-items.md` | Queued |  |
| 207 | EX-18 | Voiceprints captured without consent | New | R, L | `agent-types/meeting-agents/failures/voiceprints-captured-without-consent.md` | Queued |  |
| 208 | EX-19 | Emotional pressure when users try to leave | New | R, L, E | `agent-types/companion-and-wellbeing-agents/failures/emotional-pressure-when-users-try-to-leave.md` | Queued |  |
| 209 | EX-20 | AI offering therapy where the law restricts it | New | V, L, E | `agent-types/companion-and-wellbeing-agents/failures/ai-offering-therapy-where-the-law-restricts-it.md` | Queued |  |
| 210 | EX-21 | Hiring and screening tools with unequal impact | Extends | V, L | `agent-types/hr-agents/failures/hiring-and-screening-tools-with-unequal-impact.md` | Queued |  |
| 211 | EX-23 | Agent-to-agent negotiation without clear authority | Extends | R | `agent-types/multi-agent-platforms/failures/agent-to-agent-negotiation-without-clear-authority.md` | Queued |  |
| 212 | EX-24 | AI-voice outbound calls without consent | Extends | V, L | `agent-types/voice-receptionist-agents/failures/ai-voice-outbound-calls-without-consent.md` | Queued |  |
| 213 | EX-25 | Cloned voices defeat voice authentication | Extends | L, R | `modalities/voice/failures/cloned-voices-defeat-voice-authentication.md` | Queued |  |
| 214 | VO-05 | Repair failure | Extends | - | `modalities/voice/failures/repair-failure.md` | Queued |  |
| 215 | VO-06 | No repeat or recap controls | New | - | `modalities/voice/failures/no-repeat-or-recap-controls.md` | Queued |  |
| 216 | VO-08 | Atypical speech mishandled | New | E | `modalities/voice/failures/atypical-speech-mishandled.md` | Queued |  |
| 217 | VO-11 | Spoken-language misidentification | Extends | - | `modalities/voice/failures/spoken-language-misidentification.md` | Queued |  |
| 218 | VO-12 | Dense information read aloud | Extends | R | `modalities/voice/failures/dense-information-read-aloud.md` | Queued |  |
| 219 | VO-15 | Fixed speaking rate and volume | New | - | `modalities/voice/failures/fixed-speaking-rate-and-volume.md` | Queued |  |
| 220 | VO-16 | IVR-style menu maze | New | - | `modalities/voice/failures/ivr-style-menu-maze.md` | Queued |  |
| 221 | VO-17 | Spoken sensitive data | Extends | L | `modalities/voice/failures/spoken-sensitive-data.md` | Queued |  |
| 222 | VO-18 | Missing disclosure and recording notice | Extends | L | `modalities/voice/failures/missing-disclosure-and-recording-notice.md` | Queued |  |
| 223 | VO-19 | Voice cloning and spoofing | Extends | L, R | `modalities/voice/failures/voice-cloning-and-spoofing.md` | Queued |  |
| 224 | VO-20 | Answering-machine and voicemail errors | Extends | L, R | `modalities/voice/failures/answering-machine-and-voicemail-errors.md` | Queued |  |
| 225 | VO-21 | Wake-word false activation | New | L | `modalities/voice/failures/wake-word-false-activation.md` | Queued |  |
| 226 | VO-22 | Emotion inferred from voice | New | L, R, E | `modalities/voice/failures/emotion-inferred-from-voice.md` | Queued |  |
| 227 | VO-23 | Voice-to-visual handoff failure | New | - | `modalities/voice/failures/voice-to-visual-handoff-failure.md` | Queued |  |
| 228 | VO-24 | Hold and wait handling | Extends | - | `modalities/voice/failures/hold-and-wait-handling.md` | Queued |  |
| 229 | VA-01 | Bookings without confirming details | New | - | `agent-types/voice-receptionist-agents/failures/bookings-without-confirming-details.md` | Queued |  |
| 230 | VA-02 | Emergency phrases missed in routine calls | Extends | E | `agent-types/voice-receptionist-agents/failures/emergency-phrases-missed-in-routine-calls.md` | Queued |  |
| 231 | VA-03 | Collections calls without required disclosures | New | L, R | `agent-types/voice-receptionist-agents/failures/collections-calls-without-required-disclosures.md` | Queued |  |
| 232 | BA-01 | Bypasses CAPTCHAs or site terms | New | L | `agent-types/browser-agents/failures/bypasses-captchas-or-site-terms.md` | Queued |  |
| 233 | BA-02 | Accepts consent pop-ups for the user | New | L | `agent-types/browser-agents/failures/accepts-consent-pop-ups-for-the-user.md` | Queued |  |
| 234 | BA-03 | Navigation loops and cost blow-ups | Extends | - | `agent-types/browser-agents/failures/navigation-loops-and-cost-blow-ups.md` | Queued |  |
| 235 | BA-04 | Asks for credentials at login walls | Extends | - | `agent-types/browser-agents/failures/asks-for-credentials-at-login-walls.md` | Queued |  |
| 236 | SH-01 | Stale price or stock at checkout | New | - | `agent-types/shopping-agents/failures/stale-price-or-stock-at-checkout.md` | Queued |  |
| 237 | SH-02 | Free trials that become paid subscriptions | New | L | `agent-types/shopping-agents/failures/free-trials-that-become-paid-subscriptions.md` | Queued |  |
| 238 | SH-03 | Return policy ignored | New | - | `agent-types/shopping-agents/failures/return-policy-ignored.md` | Queued |  |
| 239 | SH-04 | Shared accounts reveal gifts | New | - | `agent-types/shopping-agents/failures/shared-accounts-reveal-gifts.md` | Queued |  |
| 240 | PA-01 | Sends in the wrong tone or to the wrong person | Extends | - | `agent-types/personal-assistants/failures/sends-in-the-wrong-tone-or-to-the-wrong.md` | Queued |  |
| 241 | PA-02 | Books non-refundable travel on a guess | Extends | - | `agent-types/personal-assistants/failures/books-non-refundable-travel-on-a-guess.md` | Queued |  |
| 242 | PA-03 | Time-zone and double-booking errors | Extends | - | `agent-types/personal-assistants/failures/time-zone-and-double-booking-errors.md` | Queued |  |
| 243 | LG-01 | Wrong-language reply | Extends | - | `core/language-and-locale/failures/wrong-language-reply.md` | Queued |  |
| 244 | LG-03 | Language switch ignored | Extends | - | `core/language-and-locale/failures/language-switch-ignored.md` | Queued |  |
| 245 | LG-04 | Unchecked translation in high-stakes text | New | E | `core/language-and-locale/failures/unchecked-translation-in-high-stakes-text.md` | Queued |  |
| 246 | LG-05 | Politeness and formality errors | New | R, E | `core/language-and-locale/failures/politeness-and-formality-errors.md` | Queued |  |
| 247 | LG-06 | Reading-level mismatch | New | R | `core/language-and-locale/failures/reading-level-mismatch.md` | Queued |  |
| 248 | LG-07 | Jargon, acronyms, and idioms | Extends | - | `core/language-and-locale/failures/jargon-acronyms-and-idioms.md` | Queued |  |
| 249 | LG-08 | Locale format errors | Extends | - | `core/language-and-locale/failures/locale-format-errors.md` | Queued |  |
| 250 | LG-09 | Name and transliteration errors | Extends | - | `core/language-and-locale/failures/name-and-transliteration-errors.md` | Queued |  |
| 251 | LG-10 | Gender and pronoun errors | New | E | `core/language-and-locale/failures/gender-and-pronoun-errors.md` | Queued |  |
| 252 | LG-11 | Dialect and slang misreading | Extends | - | `core/language-and-locale/failures/dialect-and-slang-misreading.md` | Queued |  |
| 253 | LG-12 | Typos, shorthand, and noisy input | New | - | `core/language-and-locale/failures/typos-shorthand-and-noisy-input.md` | Queued |  |
| 254 | LG-13 | Emoji and punctuation tone misreads | Extends | R | `core/language-and-locale/failures/emoji-and-punctuation-tone-misreads.md` | Queued |  |
| 255 | LG-14 | Profanity and slang handling | New | - | `core/language-and-locale/failures/profanity-and-slang-handling.md` | Queued |  |
| 256 | LG-15 | Mixed-language experience | New | - | `core/language-and-locale/failures/mixed-language-experience.md` | Queued |  |
| 257 | LG-16 | Right-to-left and mixed-script rendering | New | - | `core/language-and-locale/failures/right-to-left-and-mixed-script-rendering.md` | Queued |  |
| 258 | ED-01 | Gives answers instead of teaching | New | - | `agent-types/education-agents/failures/gives-answers-instead-of-teaching.md` | Queued |  |
| 259 | ED-02 | Wrong explanations taught as fact | New | R | `agent-types/education-agents/failures/wrong-explanations-taught-as-fact.md` | Queued |  |
| 260 | ED-03 | Unfair or inconsistent grading | Extends | R | `agent-types/education-agents/failures/unfair-or-inconsistent-grading.md` | Queued |  |
| 261 | ED-04 | Student data and surveillance | Extends | L | `agent-types/education-agents/failures/student-data-and-surveillance.md` | Queued |  |
| 262 | HR-01 | Employee-relations complaints routed wrongly | New | L | `agent-types/hr-agents/failures/employee-relations-complaints-routed-wrongly.md` | Queued |  |
| 263 | HR-02 | Pay or leave answers that leak confidential data | Extends | - | `agent-types/hr-agents/failures/pay-or-leave-answers-that-leak-confidential-data.md` | Queued |  |
| 264 | HR-03 | Manager and employee views mixed up | Extends | - | `agent-types/hr-agents/failures/manager-and-employee-views-mixed-up.md` | Queued |  |
| 265 | LA-01 | Crossing into practising law | New | L, E | `agent-types/legal-agents/failures/crossing-into-practising-law.md` | Queued |  |
| 266 | MA-01 | Agents contradict each other | Extends | - | `agent-types/multi-agent-platforms/failures/agents-contradict-each-other.md` | Queued |  |
| 267 | MA-02 | Internal coordination leaks into replies | Extends | - | `agent-types/multi-agent-platforms/failures/internal-coordination-leaks-into-replies.md` | Queued |  |
| 268 | VI-01 | Cognitive overload | New | R | `modalities/visual/failures/cognitive-overload.md` | Queued |  |
| 269 | VI-02 | No clear primary action | New | - | `modalities/visual/failures/no-clear-primary-action.md` | Queued |  |
| 270 | VI-04 | Accessibility gaps | New | V, L, E | `modalities/visual/failures/accessibility-gaps.md` | Queued |  |
| 271 | VI-05 | Motion and flashing harm | New | E, R | `modalities/visual/failures/motion-and-flashing-harm.md` | Queued |  |
| 272 | VI-06 | Colour-only encoding | New | E | `modalities/visual/failures/colour-only-encoding.md` | Queued |  |
| 273 | VI-07 | Small targets and small screens | New | V | `modalities/visual/failures/small-targets-and-small-screens.md` | Queued |  |
| 274 | VI-08 | Misleading generated visuals | New | L | `modalities/visual/failures/misleading-generated-visuals.md` | Queued |  |
| 275 | VI-09 | Unlabelled synthetic faces and avatars | Extends | L | `modalities/visual/failures/unlabelled-synthetic-faces-and-avatars.md` | Queued |  |
| 276 | VI-10 | Avatar overpromising | New | R | `modalities/visual/failures/avatar-overpromising.md` | Queued |  |
| 277 | VI-11 | Rich-card misuse | New | - | `modalities/visual/failures/rich-card-misuse.md` | Queued |  |
| 278 | VI-12 | Sensitive-data forms | Extends | L | `modalities/visual/failures/sensitive-data-forms.md` | Queued |  |
| 279 | VI-13 | Stakes-blind visual style | Extends | - | `modalities/visual/failures/stakes-blind-visual-style.md` | Queued |  |
| 280 | VI-14 | Misleading charts | New | - | `modalities/visual/failures/misleading-charts.md` | Queued |  |
| 281 | VI-15 | Missing loading, empty, and error states | New | V | `modalities/visual/failures/missing-loading-empty-and-error-states.md` | Queued |  |
| 282 | VI-16 | Generative UI instability | New | R | `modalities/visual/failures/generative-ui-instability.md` | Queued |  |
| 283 | VI-17 | Visuals that don't localise | New | R | `modalities/visual/failures/visuals-that-don-t-localise.md` | Queued |  |
| 284 | VI-18 | Notification overload | New | L | `modalities/visual/failures/notification-overload.md` | Queued |  |
| 285 | VI-19 | Manipulated consent UI | New | L | `modalities/visual/failures/manipulated-consent-ui.md` | Queued |  |
| 286 | VI-20 | Fake urgency and trust cues | New | L | `modalities/visual/failures/fake-urgency-and-trust-cues.md` | Queued |  |
| 287 | OV-02 | Hidden agent actions | Extends | - | `core/human-oversight/failures/hidden-agent-actions.md` | Queued |  |
| 288 | OV-04 | Poor action previews | Extends | - | `core/human-oversight/failures/poor-action-previews.md` | Queued |  |
| 289 | OV-05 | Miscalibrated confidence display | Extends | R | `core/human-oversight/failures/miscalibrated-confidence-display.md` | Queued |  |
| 290 | OV-07 | Invisible long-running status | Extends | V | `core/human-oversight/failures/invisible-long-running-status.md` | Queued |  |
| 291 | OV-08 | No stop or takeover | Extends | - | `core/human-oversight/failures/no-stop-or-takeover.md` | Queued |  |
| 292 | OV-09 | Permission fatigue or under-asking | Extends | - | `core/human-oversight/failures/permission-fatigue-or-under-asking.md` | Queued |  |
| 293 | OV-10 | Misleading explanations | Extends | R | `core/human-oversight/failures/misleading-explanations.md` | Queued |  |
| 294 | OV-12 | Confusion over who is acting | Extends | - | `core/human-oversight/failures/confusion-over-who-is-acting.md` | Queued |  |

## Run log
*(Each run appends an entry here.)*

## Backlog (not scheduled)
Ideas from earlier lists that were never chosen. They stay out of the queue until someone adds them.

AI-written help content in knowledge bases · voice in cars and wearables · agents using other agents' tools (user-facing side) · email and calendar agents (now partly PA) · group chats and shared assistants · proactive and ambient agents · document and spreadsheet copilots · workplace monitoring through copilots · shopping honesty (stale prices, affiliate bias) · benefits, government, and insurance chat · outbound AI sales at scale · elder-care assistants · household and family assistants · digital twins and cloned voices of real people · video and avatar service agents · "know your agent" identity · AI-generated reviews · scammers impersonating your support · assistant marketplaces · invisible model routing · memory shared across products · apps inside assistants · accessibility-first agents · jurisdiction-aware behaviour (state-by-state rules) · transcript mining and privacy · smart glasses and AR overlays · robots and embodied assistants · live camera and screen sharing · game characters and creative companions

## Schedule
| Item | Value |
|---|---|
| Status | **Paused** on 2026-10-14 until the user's credits reset. Runs resume only when the task is re-enabled. No queue items have been started. |
| Scheduled task name | `HMI roadmap: 5 patterns every 5 hours` |
| Task id | `trig_01J1rwvuKcpXBGmKkkRfihF7` |
| Created | 2026-10-14 19:05 UTC |
| Cron (UTC) | `5 */5 * * *`, so runs start at minute 5 of hours 0, 5, 10, 15, and 20 |
| First run | 2026-10-14 20:05 UTC |
| Gap at midnight | Hours 20 and 0 are only 4 hours apart, because 24 isn't divisible by 5. All other gaps are 5 hours. |
| Where it fires | Into the same session that created it, so the run has the repository checkout and tools |
| To pause or stop | Ask the session to disable the task, or call the scheduled-task update tool with `enabled=false` for the id above. The queue keeps its place, so re-enabling resumes where it stopped. |
