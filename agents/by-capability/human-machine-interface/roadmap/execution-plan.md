# Execution Plan: 3 to 5 Patterns plus One Content-Program Task per Run, Every Hour

> **What this is.** A prioritized queue of **432 patterns** to write, split into **91 runs** (the first 30 flagship patterns at 3 per run, the rest at up to 5), each with one task from the [content program](content-program.md), plus the procedure each scheduled run follows and the quality gate every pattern must pass. A scheduled task fires every 5 hours and works through the queue until it is empty. Each run is meant to be unattended: everything it needs is in this file.

## Settings (edit here to change behavior)
| Setting | Value |
|---|---|
| Patterns per run | 3 while flagship patterns remain, then 5 (raise or lower these numbers to change the pace; the schedule stays the same) |
| Content-program task per run | 1 task from [content-program.md](content-program.md), after the patterns; skip it when none is ready |
| Tiers | **Flagship**: the 30 patterns listed in content-program.md, held to the extra flagship items in the Definition of done. **Catalog**: all others. |
| Quality gate | A pattern is **Done** only if it passes the Definition of done below. Anything that doesn't is marked **Needs review** and left for a person. |
| Run mode | **write** (research, write the full pattern, update the catalog). Change to **plan-only** to have each run only research and record briefs in `roadmap/briefs/` without writing patterns. |
| Cadence | Every hour (set in the scheduled task, not in this file) |
| Branch | `claude/zealous-ramanujan-u8zwfk` (commit and push). At the end of each run a pull request into `main` is opened and merged, as set out in [deploy.md](deploy.md) |
| Scope | Only files under `agents/by-capability/human-machine-interface/` and `agents/solutions/`. Do not edit the older patterns elsewhere in `agents/`. Anything that would change files outside this folder goes into `roadmap/merge-proposals.md` as a proposal for a person to approve. |
| Repositories | Content lives here; the website lives in `sarkars/agent-kb-autopublish`. The run reads that repo and never edits it. Site changes become proposals. See [REPOSITORIES.md](../../../../REPOSITORIES.md) |
| Spelling and examples | American English, and US examples (US cities, dollars, US laws and regulators) |

## How the order was set
Priority combines five things: **(1)** demand evidence (customers' top frustrations: no human, "doesn't understand me", repeating themselves; builders' top barrier: quality), **(2)** gaps in the library (the Code Agent area is empty; upselling, forced re-login, and generic first responses have no patterns), **(3)** harm if wrong (crisis, scams, minors, unauthorized purchases), **(4)** evidence available now, and **(5)** dependencies (a family's first pattern also creates its README). The earlier "Suggested priority" tiers in the [roadmap README](README.md) are superseded by this order. Items the library already covers are not in the queue.

## Run procedure
Follow these steps on every run. Don't skip the checks: earlier work in this project had to be corrected for duplicating existing patterns and for a counting bug.

0. **Check network access first (takes one minute).** Try to open one source site (for example `curl -sS -m 15 -o /dev/null -w "%{http_code}" https://www.consumerfinance.gov`; 000 or a proxy refusal means blocked). If sources cannot be opened, **write nothing from summaries**. Append a "Blocked: sources unreachable" entry to the Run log and `seo/log.md`, commit and push those two files, and stop. A run that cannot open sources may not mark any pattern Done. Search-result summaries do not count as opened sources.
1. **Sync.** `git fetch origin claude/zealous-ramanujan-u8zwfk` and make sure the working tree is on that branch and up to date. Read this file, `_templates/hmi-pattern.md`, and the two flagship patterns (`goals/conversation-leadership/failures/answer-and-go-conversation.md` and `goals/channel-selection/failures/no-channel-switch-or-context-lost.md`) so style stays consistent.
2. **Pick the work.** Take rows marked *In progress* first, then the next **3** rows marked *Queued* while any flagship row remains, otherwise the next **5**, in order. Mark them *In progress*. Don't touch rows marked *Needs review*. If fewer remain, take what's left. Never take a catalog row while a flagship row is still *Queued*. If no *Queued* or *In progress* rows remain, write "Queue complete" in the Run log, disable the schedule (see the Schedule section), and stop.
3. **Write one pattern at a time, finishing each before starting the next:**
   1. **Re-check the library.** Search `agents/` (file names and keywords) for existing patterns on the topic and read the closest one to three. If it is already fully covered, mark the row *Skipped* with the link and take the next *Queued* row. If the row is **Extends**, write only the new human-interface angle and a fix, and link the existing pattern instead of restating it.
   2. **Research properly.** Run at least three web searches and count them: a pattern cannot be marked Done with fewer than three, and its Run log entry states the count. Run at least three web searches (loading the search tools first if needed). **Open the source itself** with the fetch tool whenever it is reachable; don't rely on a search summary alone. For every claim you plan to use, note the source link, what it actually says, and whether you opened it or only read a summary of it. Find every number in the source text; if you can't, don't use the number. Prefer one strong, neutral source over several weak ones. Label vendor, secondary, and single-source evidence. If there is no good evidence, say so in the pattern. **Never invent statistics.**
   3. **Draft the pattern** at the row's target file, using `_templates/hmi-pattern.md`: SEO comment block with real queries; H1 with the phrase people search plus the pattern name; header table with **Goal** and **Primary metric** matching the catalog row and the family README; before-and-after transcripts with US examples; why it happens; an evidence table with caveats; **the fix**; short tests; a metrics table (`Metric | Target | How to measure | Alert at`); related patterns; common questions; and a technical section when the fix needs engineering. For agent-type patterns, set the examples inside that agent's real workflow.
   4. **Flags.** Rows flagged **L** (legal) or **E** (expert) get a "Read this first" note near the top: design guidance, not legal, clinical, or other professional advice, and a review is needed before use. State any regulation only as far as you verified it.
   5. **Review pass.** Check the draft against every item in the **Definition of done** below. Then read the whole file once, top to bottom, as a skeptical reader who has not seen your notes. Fix what you find, and re-read what you changed.
   6. **Family README.** If the folder has no `README.md`, create one in the style of `goals/vulnerable-users/README.md` using the family goal from the table below. Otherwise add the new pattern to its table.
   7. **Record the result.** If every item in the Definition of done is true, change the catalog row's last cell to the word `**Written**` followed by a colon and a markdown link to the new pattern (path relative to the roadmap folder), and set the queue row to *Done* with the run number. If any item still fails after a reasonable effort, set the queue row to *Needs review* with a one-line reason, leave the catalog row unchanged, and keep the draft file.
   8. **Verify and commit.** Run `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/rebuild_summary.py` then `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_links.py` and `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_site_compat.py`, and `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_public_urls.py`, and `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_solutions.py`, and fix every problem they report. Commit this one pattern with a message like `HMI run N: <id> <name>` plus the attribution lines from the session, then push with `git push -u origin claude/zealous-ramanujan-u8zwfk`. If the push fails on a network error, retry up to 4 times (waits of 2, 4, 8, 16 seconds). If it still fails, record it in the Run log and stop; the next run continues.
4. **Daily SEO review.** If `seo/log.md` has no entry for today's UTC date, do the review in [seo/README.md](seo/README.md) first: read the Search Console search terms (Chrome if its tools are available, otherwise an export in `seo/inbox/`, otherwise log "Blocked" and run the public checks), act on the opportunities inside the allowed scope, log it, and commit and push it on its own. Never invent search data.
5. **Content-program task.** After the patterns, do the first ready task in the Task queue of [content-program.md](content-program.md), under the rules there, then commit and push it on its own. Skip it if no task is ready.
6. **Log.** Append an entry to the Run log: run number, UTC date and time, and for each pattern the ID, the result (Done, Needs review, or Skipped), how many sources you opened vs. read only through summaries, any claims left unverified, and what the review pass changed. Add anything you could not check or any correction to earlier files.
7. **Deploy.** Follow [deploy.md](deploy.md): merge the branch into `main`, reset the branch to `main`, publish the new and changed pages to the website repo, verify the build and the live URLs, and add a Deploy line to the Run log entry. If a run wrote nothing new, skip this step. If any check in deploy.md fails, stop and record why.

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
- Link text is descriptive, and `check_links.py`, `check_site_compat.py`, `check_public_urls.py`, and `check_solutions.py` pass.
- The file is 120 to 250 lines. The technical section appears only when the fix needs engineering.
- American spelling, US examples, and the same layout, voice, and section numbering as the flagship patterns.

**Every pattern (both tiers)**
- The header table has a **Maturity** row (*Researched* when it passes this gate) and a **Will a better model fix this?** row (Yes, Partly, or No, with one sentence of why, and whether that is "our judgment" or "tested").

**Flagship patterns, in addition**
- At least one dated, public incident with a source you opened, linked from an `incidents/` page; or the sentence "No public incident found" with the searches you ran. Never describe an incident you did not read.
- A test file at `tests/<pattern-file-name>.md` in the format set by `tests/README.md`: 10 to 20 conversations, a pass/fail rubric that maps to each rule in the fix. The results table says "Not yet run" unless a person or an automated harness actually ran the tests and the run is recorded. **Never write results you did not obtain.** Maturity is then *Tests written*, not *Tested*.

If any item can't be met in this run, the pattern is *Needs review*, not *Done*.

## Quality bar and limits
- **Quality beats the count.** A run may write fewer than 5. Never pad with a thin pattern, and never mark something *Done* that hasn't passed the gate.
- **No duplicates.** Don't rewrite a pattern the library already has. Link to it.
- **Honesty.** Mark unverified claims as unverified. Keep thresholds labeled as starting points unless sourced.
- **Don't change** the schedule (except to disable it when the queue is empty), other families' patterns, the older library, or this file's Settings. You may correct errors in files you wrote earlier, and say so in the log.
- **No pull requests.** Push to the branch only.

## Family folders and goals
Create a folder's README on its first pattern. Folders that already have a README (the ten core families and `goals/channel-selection`) keep their goals.

| Folder | Family goal (use verbatim in the family README and each pattern's Goal row) |
|---|---|
| `goals/embedded-copilots` | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| `goals/response-structure` | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| `goals/effort-and-memory` | The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't. |
| `goals/response-time` | Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. |
| `goals/language-and-locale` | Users are understood and answered in the language, reading level, and format that work for them. |
| `goals/conversation-frameworks` | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| `goals/privacy-and-governance` | The agent handles personal data and outside services under clear rules, acts only within the rights of the person it serves, explains its limits, and keeps to its rules when pushed. |
| `goals/human-oversight` | People overseeing an agent can see what it is doing, understand why, and stop or correct it. |
| `goals/measurement-and-feedback` | Teams can tell whether conversations really work, and users can tell the team when they don't. |
| `goals/voice` | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| `goals/visual` | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| `goals/coding-agents` | A coding agent changes only what was asked, reports truthfully on what it ran, and leaves the codebase safer than it found it. |
| `goals/research-and-data-agents` | Analytical agents give answers a person can verify: correct numbers, governed definitions, balanced sources, and a visible method. |
| `goals/workflow-automation-agents` | Automation agents change records safely: previewed, conflict-aware, itemised, and stopped when the world changes. |
| `goals/it-and-security-agents` | IT and security agents act within verified authority, explain what they close, and never contain or reset without the right approval. |
| `goals/finance-agents` | Finance agents post to the right place, reconcile only what exists, and can't be steered into unauthorised payments. |
| `goals/healthcare-agents` | Healthcare agents capture what happened accurately, flag what they're unsure of, and keep clinicians genuinely in the loop. |
| `goals/sales-agents` | Sales agents use verified information, respect opt-outs, and keep records clean. |
| `goals/voice-receptionist-agents` | Phone agents confirm critical details, catch emergencies, and meet disclosure and consent rules. |
| `goals/browser-agents` | Browsing agents stay within the user's intent and the site's rules, and ask before consequential actions. |
| `goals/shopping-agents` | Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed. |
| `goals/education-agents` | Tutors teach, are accurate, treat students fairly, and protect their data. |
| `goals/personal-assistants` | Assistants act for the user, with confirmation on anything sent, booked, or paid. |
| `goals/hr-agents` | HR agents route sensitive matters correctly and show each person only what they're entitled to see. |
| `goals/legal-agents` | Legal agents stay within permitted scope and protect confidential and privileged material. |
| `goals/multi-agent-platforms` | Multiple agents present one coherent, honest voice and don't expose their internal coordination. |
| `goals/tool-ecosystems` | Agents connect to tools only through authenticated, vetted, and clearly attributed channels. |
| `goals/meeting-agents` | Meeting assistants record with everyone's knowledge and summarise faithfully. |
| `goals/companion-and-wellbeing-agents` | Companion and wellbeing agents support users without exploiting them or standing in for professional care. |
| `goals/customer-support-agents` | Support agents are measured and paid by what customers confirm was solved. |
| `goals/dialogue-management` | The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. |
| `goals/refusals-and-boundaries` | When the agent can't or won't do something, it says so plainly, helps with what it can, and applies the same rule every time. |
| `goals/errors-and-recovery` | When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it. |
| `goals/persona-and-tone` | The agent keeps one fitting character: on-brand, respectful, and never talking down or trying too hard. |
| `goals/onboarding-and-discoverability` | People know what the assistant can do and how to start, without needing to guess or to engineer prompts. |
| `goals/chat-interface` | The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost. |
| `goals/accessibility` | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| `goals/multimodal-input` | What people show, say, or upload is read properly, and the agent says what it could not read. |
| `goals/human-handoff` | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| `goals/model-and-prompt-changes` | Changes to the model or prompt never surprise users: they are tested, announced, and reversible. |
| `goals/proactive-and-ambient` | Proactive and always-listening agents speak up only when invited or useful, and respect a no. |
| `goals/group-and-shared-chats` | In shared conversations the agent knows who is speaking to it, keeps private information private, and does not take over. |
| `goals/drive-thru-agents` | Voice ordering gets the order right, shows it, and never pressures or risks someone's health. |
| `goals/in-car-and-home-assistants` | In-car and home voice assistants stay safe, act only on authorized commands, and are open about what they hear. |
| `goals/government-service-agents` | Public-service agents give accurate, accessible, plain-language guidance and always leave a path to a person and an appeal. |
| `goals/travel-and-utility-agents` | Agents handling disruptions and outages quote the real rules, give specifics, and keep people informed. |
| `goals/banking-agents` | Banking agents contact customers in ways that cannot be mistaken for fraud, and capture disputes completely. |
| `goals/insurance-claims-agents` | Claims intake is humane, accurate about coverage, and clear about what evidence is needed. |
| `goals/health-scheduling-agents` | Scheduling and patient-message agents use the right wording, provider, and visit type, and never leave patients with unexplained results. |
| `goals/real-estate-agents` | Housing agents treat applicants fairly and route emergencies correctly. |
| `goals/outbound-messaging-agents` | Outbound texts and calls respect consent, quiet hours, and suppression lists. |

## Run schedule
Run N covers queue orders as shown. At one run every hour, 91 runs take about 91 hours between the first and last start, roughly 3.8 days. A run that marks a pattern *Needs review* doesn't delay the queue, but those patterns need a person.

| Run | Orders | Themes |
|---|---|---|
| 1 | 1-3 (3) | Flagship set |
| 2 | 4-6 (3) | Flagship set |
| 3 | 7-9 (3) | Flagship set |
| 4 | 10-12 (3) | Flagship set |
| 5 | 13-15 (3) | Flagship set |
| 6 | 16-18 (3) | Flagship set |
| 7 | 19-21 (3) | Flagship set |
| 8 | 22-24 (3) | Flagship set |
| 9 | 25-27 (3) | Flagship set |
| 10 | 28-30 (3) | Flagship set |
| 11 | 31-35 (5) | Understood, in context, and a real first reply |
| 12 | 36-40 (5) | Understood, in context, and a real first reply |
| 13 | 41-45 (5) | Reaching a person; Upselling and conflicts of interest |
| 14 | 46-50 (5) | Upselling and conflicts of interest; Following the conversation |
| 15 | 51-55 (5) | Following the conversation |
| 16 | 56-60 (5) | Following the conversation |
| 17 | 61-65 (5) | Following the conversation; Reply shape, length, and closers |
| 18 | 66-70 (5) | Reply shape, length, and closers |
| 19 | 71-75 (5) | Reply shape, length, and closers |
| 20 | 76-80 (5) | Reply shape, length, and closers; Errors, refusals, and recovery |
| 21 | 81-85 (5) | Errors, refusals, and recovery |
| 22 | 86-90 (5) | Errors, refusals, and recovery |
| 23 | 91-95 (5) | Errors, refusals, and recovery; Effort, completeness, and memory |
| 24 | 96-100 (5) | Effort, completeness, and memory |
| 25 | 101-105 (5) | Effort, completeness, and memory; Response time and waiting |
| 26 | 106-110 (5) | Response time and waiting |
| 27 | 111-115 (5) | Response time and waiting; Measurement and feedback |
| 28 | 116-120 (5) | Measurement and feedback |
| 29 | 121-125 (5) | Measurement and feedback; Accessibility |
| 30 | 126-130 (5) | Accessibility |
| 31 | 131-135 (5) | Accessibility; High-harm picks |
| 32 | 136-140 (5) | High-harm picks |
| 33 | 141-145 (5) | High-harm picks; Coding agents |
| 34 | 146-150 (5) | Coding agents; Research and data-analysis agents |
| 35 | 151-155 (5) | Research and data-analysis agents; Workflow-automation agents |
| 36 | 156-160 (5) | Workflow-automation agents; IT and security agents |
| 37 | 161-165 (5) | IT and security agents; Healthcare agents |
| 38 | 166-170 (5) | Healthcare agents; Transcription and listening |
| 39 | 171-175 (5) | Transcription and listening |
| 40 | 176-180 (5) | Transcription and listening |
| 41 | 181-185 (5) | Transcription and listening; Finance agents |
| 42 | 186-190 (5) | Chat and core, the rest |
| 43 | 191-195 (5) | Chat and core, the rest |
| 44 | 196-200 (5) | Chat and core, the rest; Persona and tone |
| 45 | 201-205 (5) | Persona and tone |
| 46 | 206-210 (5) | Persona and tone; Onboarding and the chat interface |
| 47 | 211-215 (5) | Onboarding and the chat interface |
| 48 | 216-220 (5) | Onboarding and the chat interface |
| 49 | 221-225 (5) | Onboarding and the chat interface; Selling and sales agents |
| 50 | 226-230 (5) | Selling and sales agents |
| 51 | 231-235 (5) | Selling and sales agents |
| 52 | 236-240 (5) | Selling and sales agents; Support and style frameworks |
| 53 | 241-245 (5) | Support and style frameworks |
| 54 | 246-250 (5) | Support and style frameworks |
| 55 | 251-255 (5) | Support and style frameworks |
| 56 | 256-260 (5) | Support and style frameworks; Privacy, governance, and access |
| 57 | 261-265 (5) | Privacy, governance, and access |
| 58 | 266-270 (5) | Privacy, governance, and access |
| 59 | 271-275 (5) | Privacy, governance, and access |
| 60 | 276-280 (5) | Privacy, governance, and access; Emerging surfaces, the rest |
| 61 | 281-285 (5) | Emerging surfaces, the rest |
| 62 | 286-290 (5) | Emerging surfaces, the rest |
| 63 | 291-295 (5) | Emerging surfaces, the rest |
| 64 | 296-300 (5) | Emerging surfaces, the rest; Voice |
| 65 | 301-305 (5) | Voice |
| 66 | 306-310 (5) | Voice |
| 67 | 311-315 (5) | Voice; Browser, shopping, and assistant agents |
| 68 | 316-320 (5) | Browser, shopping, and assistant agents |
| 69 | 321-325 (5) | Browser, shopping, and assistant agents; Multimodal input |
| 70 | 326-330 (5) | Multimodal input |
| 71 | 331-335 (5) | Multimodal input; Model and prompt changes |
| 72 | 336-340 (5) | Model and prompt changes; Language and locale |
| 73 | 341-345 (5) | Language and locale |
| 74 | 346-350 (5) | Language and locale |
| 75 | 351-355 (5) | Language and locale; Education, HR, legal, and multi-agent |
| 76 | 356-360 (5) | Education, HR, legal, and multi-agent |
| 77 | 361-365 (5) | Education, HR, legal, and multi-agent; Proactive agents and group chats |
| 78 | 366-370 (5) | Proactive agents and group chats |
| 79 | 371-375 (5) | Proactive agents and group chats; Service verticals and outbound rules |
| 80 | 376-380 (5) | Service verticals and outbound rules |
| 81 | 381-385 (5) | Service verticals and outbound rules |
| 82 | 386-390 (5) | Service verticals and outbound rules |
| 83 | 391-395 (5) | Service verticals and outbound rules |
| 84 | 396-400 (5) | Service verticals and outbound rules |
| 85 | 401-405 (5) | Service verticals and outbound rules |
| 86 | 406-410 (5) | Visual and oversight, the rest |
| 87 | 411-415 (5) | Visual and oversight, the rest |
| 88 | 416-420 (5) | Visual and oversight, the rest |
| 89 | 421-425 (5) | Visual and oversight, the rest |
| 90 | 426-430 (5) | Visual and oversight, the rest |
| 91 | 431-432 (2) | Visual and oversight, the rest |

## Queue
Status: *Queued*, *In progress*, *Done*, *Needs review*, or *Skipped*. The **Library** column is the status in the catalog when the queue was built (**New** or **Extends**).

| # | ID | Pattern | Library | Flags | Target file | Status | Run |
|---|---|---|---|---|---|---|---|
| 1 | HU-01 | 'Talk to a human' ignored or looped | Extends | - | `goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md` | Done | 10 (manual) |
| 2 | HU-02 | Escalates too early, or too late | Extends | - | `goals/human-handoff/failures/escalates-too-early-or-too-late.md` | Done | 10 (manual) |
| 3 | HU-03 | Cold transfer | Extends | - | `goals/human-handoff/failures/cold-transfer.md` | Done | 10 (manual) |
| 4 | CP-14 | Re-asks for known information | Extends | V | `goals/embedded-copilots/failures/re-asks-for-known-information.md` | Done | 11 |
| 5 | CP-15 | Forces a fresh login | New | E | `goals/embedded-copilots/failures/forces-a-fresh-login.md` | Done | 11 |
| 6 | CP-20 | Generic first response | New | R | `goals/embedded-copilots/failures/generic-first-response.md` | Done | 11 |
| 7 | CP-08 | Missing the obvious intent | Extends | - | `goals/embedded-copilots/failures/missing-the-obvious-intent.md` | Done | 12 |
| 8 | CP-12 | Doesn't say what it can do | New | R | `goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md` | Done | 12 |
| 9 | XA-01 | Dead-end 'I don't understand' replies | Extends | V, R | `goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md` | Done | 12 |
| 10 | CP-01 | Help that becomes a sales pitch | New | V, R, L | `goals/embedded-copilots/failures/help-that-becomes-a-sales-pitch.md` | Done | 13 |
| 11 | CP-06 | Obstructing cancellation, downgrade, or refund | Extends | V, L | `goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md` | Done | 13 |
| 12 | CP-03 | Answers withheld behind an upgrade, unsaid | New | L | `goals/embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md` | Done | 13 |
| 13 | RS-14 | No reply to acknowledgments and closers | Extends | - | `goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md` | Done | 14 |
| 14 | RS-01 | Answer buried | New | - | `goals/response-structure/failures/answer-buried.md` | Done | 14 |
| 15 | EM-02 | Deferring work to the user | New | - | `goals/effort-and-memory/failures/deferring-work-to-the-user.md` | Done | 14 |
| 16 | EM-11 | No warning of context loss | Extends | - | `goals/effort-and-memory/failures/no-warning-of-context-loss.md` | Done | 15 |
| 17 | EM-01 | Lazy completion | New | V | `goals/effort-and-memory/failures/lazy-completion.md` | Done | 15 |
| 18 | DM-03 | Corrections not applied | New | - | `goals/dialogue-management/failures/corrections-not-applied.md` | Done | 15 |
| 19 | DM-09 | Guessing instead of asking | Extends | - | `goals/dialogue-management/failures/guessing-instead-of-asking.md` | Done | 16 |
| 20 | RF-01 | Over-refusal of ordinary requests | Extends | V | `goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md` | Done | 16 |
| 21 | RF-02 | Refusal with no reason or next step | Extends | - | `goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md` | Done | 16 |
| 22 | TE-01 | Generic error messages | New | - | `goals/errors-and-recovery/failures/generic-error-messages.md` | Done | 17 |
| 23 | TE-06 | Confident wrong answer with no way to check | Extends | - | `goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md` | Done | 17 |
| 24 | GS-01 | Eligibility answers sound like decisions | New | L, E | `goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md` | Done | 17 |
| 25 | DT-01 | Order mix-ups at the speaker | New | V | `goals/drive-thru-agents/failures/order-mix-ups-at-the-speaker.md` | Done | 18 |
| 26 | VO-05 | Repair failure | Extends | - | `goals/voice/failures/repair-failure.md` | Done | 18 |
| 27 | RT-02 | Silent long-running work | Extends | V | `goals/response-time/failures/silent-long-running-work.md` | Done | 18 |
| 28 | RT-06 | Silent failure and timeout | Extends | - | `goals/response-time/failures/silent-failure-and-timeout.md` | Queued |  |
| 29 | CC-08 | Scam victim not interrupted | New | E, L | `goals/vulnerable-users/failures/scam-victim-not-interrupted.md` | Queued |  |
| 30 | CC-16 | Romantic or parasocial dependence | New | L, E | `goals/relational-and-boundaries/failures/romantic-or-parasocial-dependence.md` | Queued |  |
| 31 | CP-10 | Irrelevant or already-answered clarifying questions | Extends | - | `goals/embedded-copilots/failures/irrelevant-or-already-answered-clarifying-questions.md` | Queued |  |
| 32 | CP-13 | Ignores the page, selection, and form state | New | R | `goals/embedded-copilots/failures/ignores-the-page-selection-and-form-state.md` | Queued |  |
| 33 | CP-16 | Ignores role, plan, locale, and device | Extends | - | `goals/embedded-copilots/failures/ignores-role-plan-locale-and-device.md` | Queued |  |
| 34 | CP-17 | Ignores recent activity and history | Extends | - | `goals/embedded-copilots/failures/ignores-recent-activity-and-history.md` | Queued |  |
| 35 | CP-19 | Context lost across a multi-session task | Extends | - | `goals/embedded-copilots/failures/context-lost-across-a-multi-session-task.md` | Queued |  |
| 36 | CP-21 | Greeting-only first turn | New | - | `goals/embedded-copilots/failures/greeting-only-first-turn.md` | Queued |  |
| 37 | CP-22 | No likely-next-action suggestions | New | R | `goals/embedded-copilots/failures/no-likely-next-action-suggestions.md` | Queued |  |
| 38 | CP-23 | Boilerplate steps that don't match the user's setup | Extends | - | `goals/embedded-copilots/failures/boilerplate-steps-that-don-t-match-the-user-s.md` | Queued |  |
| 39 | CP-09 | Over-complicating simple tasks | Extends | - | `goals/embedded-copilots/failures/over-complicating-simple-tasks.md` | Queued |  |
| 40 | CP-11 | Keyword-matched documentation instead of an answer | Extends | - | `goals/embedded-copilots/failures/keyword-matched-documentation-instead-of-an-answer.md` | Queued |  |
| 41 | HU-04 | Handoff summary is wrong or misleading | New | - | `goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md` | Queued |  |
| 42 | HU-05 | Humans can't see what the bot said or promised | New | - | `goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md` | Queued |  |
| 43 | HU-06 | Bot keeps replying after a person joins | New | - | `goals/human-handoff/failures/bot-keeps-replying-after-a-person-joins.md` | Queued |  |
| 44 | HU-07 | Handoff outside staffed hours with no alternative | New | - | `goals/human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md` | Queued |  |
| 45 | CP-02 | Recommending features the user can't use | Extends | - | `goals/embedded-copilots/failures/recommending-features-the-user-can-t-use.md` | Queued |  |
| 46 | CP-04 | Self-preferencing | New | R, L | `goals/embedded-copilots/failures/self-preferencing.md` | Queued |  |
| 47 | CP-05 | Paid content blended into answers | New | V, R, L | `goals/embedded-copilots/failures/paid-content-blended-into-answers.md` | Queued |  |
| 48 | CP-07 | Helpfulness theatre | Extends | - | `goals/embedded-copilots/failures/helpfulness-theatre.md` | Queued |  |
| 49 | DM-01 | Reference resolution failures | New | R | `goals/dialogue-management/failures/reference-resolution-failures.md` | Queued |  |
| 50 | DM-02 | Tangents never closed | Extends | - | `goals/dialogue-management/failures/tangents-never-closed.md` | Queued |  |
| 51 | DM-04 | Multi-intent messages answered in part | Extends | - | `goals/dialogue-management/failures/multi-intent-messages-answered-in-part.md` | Queued |  |
| 52 | DM-05 | Negation and exceptions ignored | New | - | `goals/dialogue-management/failures/negation-and-exceptions-ignored.md` | Queued |  |
| 53 | DM-06 | Questions asked one at a time when the user already gave everything | Extends | - | `goals/dialogue-management/failures/questions-asked-one-at-a-time-when-the-user.md` | Queued |  |
| 54 | DM-07 | Over-confirmation | New | - | `goals/dialogue-management/failures/over-confirmation.md` | Queued |  |
| 55 | DM-08 | Under-confirmation of consequential details | Extends | - | `goals/dialogue-management/failures/under-confirmation-of-consequential-details.md` | Queued |  |
| 56 | DM-10 | Clarifying questions the user can't answer | Extends | - | `goals/dialogue-management/failures/clarifying-questions-the-user-can-t-answer.md` | Queued |  |
| 57 | DM-11 | No way back in a flow | New | - | `goals/dialogue-management/failures/no-way-back-in-a-flow.md` | Queued |  |
| 58 | DM-12 | Rigid flows break on off-script answers | Extends | - | `goals/dialogue-management/failures/rigid-flows-break-on-off-script-answers.md` | Queued |  |
| 59 | DM-13 | Small talk and off-topic messages handled badly | New | - | `goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md` | Queued |  |
| 60 | DM-14 | Same answer to a rephrased question | Extends | - | `goals/dialogue-management/failures/same-answer-to-a-rephrased-question.md` | Queued |  |
| 61 | DM-15 | False premises accepted | New | R | `goals/dialogue-management/failures/false-premises-accepted.md` | Queued |  |
| 62 | RS-02 | Wall of text | Extends | - | `goals/response-structure/failures/wall-of-text.md` | Queued |  |
| 63 | RS-03 | Over-long replies | Extends | V | `goals/response-structure/failures/over-long-replies.md` | Queued |  |
| 64 | RS-04 | Over-short replies | Extends | - | `goals/response-structure/failures/over-short-replies.md` | Queued |  |
| 65 | RS-05 | Message bursts | New | - | `goals/response-structure/failures/message-bursts.md` | Queued |  |
| 66 | RS-06 | Unstructured procedures | New | - | `goals/response-structure/failures/unstructured-procedures.md` | Queued |  |
| 67 | RS-07 | Key details buried | New | - | `goals/response-structure/failures/key-details-buried.md` | Queued |  |
| 68 | RS-08 | Bullet and heading overuse | New | R | `goals/response-structure/failures/bullet-and-heading-overuse.md` | Queued |  |
| 69 | RS-09 | Filler and padding | New | R | `goals/response-structure/failures/filler-and-padding.md` | Queued |  |
| 70 | RS-10 | Structure flips between turns | Extends | - | `goals/response-structure/failures/structure-flips-between-turns.md` | Queued |  |
| 71 | RS-11 | Formatting artifacts | Extends | - | `goals/response-structure/failures/formatting-artifacts.md` | Queued |  |
| 72 | RS-12 | Wrong format for the medium | Extends | - | `goals/response-structure/failures/wrong-format-for-the-medium.md` | Queued |  |
| 73 | RS-13 | Cut-off replies | Extends | - | `goals/response-structure/failures/cut-off-replies.md` | Queued |  |
| 74 | RS-15 | Over-reply to acknowledgments | New | - | `goals/response-structure/failures/over-reply-to-acknowledgments.md` | Queued |  |
| 75 | RS-16 | Misreading 'ok' and minimal replies | Extends | V, R | `goals/response-structure/failures/misreading-ok-and-minimal-replies.md` | Queued |  |
| 76 | RS-17 | Length mismatch with the user's effort | New | - | `goals/response-structure/failures/length-mismatch-with-the-user-s-effort.md` | Queued |  |
| 77 | RS-18 | Link and resource dumps | New | R | `goals/response-structure/failures/link-and-resource-dumps.md` | Queued |  |
| 78 | TE-02 | Apology without repair | Extends | - | `goals/errors-and-recovery/failures/apology-without-repair.md` | Queued |  |
| 79 | TE-03 | Blames the user | New | - | `goals/errors-and-recovery/failures/blames-the-user.md` | Queued |  |
| 80 | TE-04 | Contradicts an earlier answer without saying so | Extends | - | `goals/errors-and-recovery/failures/contradicts-an-earlier-answer-without-saying-so.md` | Queued |  |
| 81 | TE-05 | Different answers by session or regeneration | Extends | - | `goals/errors-and-recovery/failures/different-answers-by-session-or-regeneration.md` | Queued |  |
| 82 | TE-07 | Doesn't acknowledge its own mistake when it is pointed out | Extends | - | `goals/errors-and-recovery/failures/doesn-t-acknowledge-its-own-mistake-when-it-is.md` | Queued |  |
| 83 | TE-08 | Repeats a corrected mistake | Extends | - | `goals/errors-and-recovery/failures/repeats-a-corrected-mistake.md` | Queued |  |
| 84 | RF-03 | Preachy, moralizing replies | New | R | `goals/refusals-and-boundaries/failures/preachy-moralizing-replies.md` | Queued |  |
| 85 | RF-04 | Excess disclaimers and warnings | New | - | `goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md` | Queued |  |
| 86 | RF-05 | Boundaries that change between turns or sessions | Extends | - | `goals/refusals-and-boundaries/failures/boundaries-that-change-between-turns-or-sessions.md` | Queued |  |
| 87 | RF-06 | Refusals that reveal internal rules | New | - | `goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md` | Queued |  |
| 88 | RF-07 | Out-of-scope requests handled badly | Extends | - | `goals/refusals-and-boundaries/failures/out-of-scope-requests-handled-badly.md` | Queued |  |
| 89 | RF-08 | Silent sandbagging | New | - | `goals/refusals-and-boundaries/failures/silent-sandbagging.md` | Queued |  |
| 90 | RF-09 | Refusal depends on wording | Extends | - | `goals/refusals-and-boundaries/failures/refusal-depends-on-wording.md` | Queued |  |
| 91 | RF-10 | Accusatory or harsh refusals | New | - | `goals/refusals-and-boundaries/failures/accusatory-or-harsh-refusals.md` | Queued |  |
| 92 | EM-06 | Skipped steps with no receipt | Extends | - | `goals/effort-and-memory/failures/skipped-steps-with-no-receipt.md` | Queued |  |
| 93 | EM-09 | Early-assumption lock-in | Extends | V | `goals/effort-and-memory/failures/early-assumption-lock-in.md` | Queued |  |
| 94 | EM-12 | Critical facts not pinned | Extends | - | `goals/effort-and-memory/failures/critical-facts-not-pinned.md` | Queued |  |
| 95 | EM-03 | Underthinking | Extends | V | `goals/effort-and-memory/failures/underthinking.md` | Queued |  |
| 96 | EM-08 | Partial answers to multi-part questions | New | - | `goals/effort-and-memory/failures/partial-answers-to-multi-part-questions.md` | Queued |  |
| 97 | EM-13 | Fresh-session amnesia | New | - | `goals/effort-and-memory/failures/fresh-session-amnesia.md` | Queued |  |
| 98 | EM-14 | Silent capability downgrade | Extends | - | `goals/effort-and-memory/failures/silent-capability-downgrade.md` | Queued |  |
| 99 | EM-17 | Defensive over-deferral to professionals | Extends | R, E | `goals/effort-and-memory/failures/defensive-over-deferral-to-professionals.md` | Queued |  |
| 100 | EM-21 | Giving up too early on a tool error | Extends | - | `goals/effort-and-memory/failures/giving-up-too-early-on-a-tool-error.md` | Queued |  |
| 101 | EM-22 | Overclaiming effort | Extends | - | `goals/effort-and-memory/failures/overclaiming-effort.md` | Queued |  |
| 102 | EM-23 | Scope shrink on long tasks | New | - | `goals/effort-and-memory/failures/scope-shrink-on-long-tasks.md` | Queued |  |
| 103 | EM-25 | Handoff of incomplete work with no TODO list | Extends | - | `goals/effort-and-memory/failures/handoff-of-incomplete-work-with-no-todo-list.md` | Queued |  |
| 104 | RT-01 | Slow first response | Extends | V, R | `goals/response-time/failures/slow-first-response.md` | Queued |  |
| 105 | RT-03 | Unpredictable latency | Extends | V | `goals/response-time/failures/unpredictable-latency.md` | Queued |  |
| 106 | RT-07 | Queue wait with no ETA | Extends | - | `goals/response-time/failures/queue-wait-with-no-eta.md` | Queued |  |
| 107 | RT-14 | Fast replies, slow resolution | Extends | V | `goals/response-time/failures/fast-replies-slow-resolution.md` | Queued |  |
| 108 | RT-04 | Pacing mismatch | New | R | `goals/response-time/failures/pacing-mismatch.md` | Queued |  |
| 109 | RT-05 | Deceptive typing indicators | New | L | `goals/response-time/failures/deceptive-typing-indicators.md` | Queued |  |
| 110 | RT-08 | Missed async promises | Extends | - | `goals/response-time/failures/missed-async-promises.md` | Queued |  |
| 111 | RT-09 | Session timeout and lost context | New | - | `goals/response-time/failures/session-timeout-and-lost-context.md` | Queued |  |
| 112 | RT-10 | Impatient idle nudges | New | - | `goals/response-time/failures/impatient-idle-nudges.md` | Queued |  |
| 113 | RT-11 | Urgency-blind pacing | New | - | `goals/response-time/failures/urgency-blind-pacing.md` | Queued |  |
| 114 | RT-12 | Streaming that rewrites itself | Extends | - | `goals/response-time/failures/streaming-that-rewrites-itself.md` | Queued |  |
| 115 | XA-02 | Conversation-quality measurement gaps | Extends | V, R | `goals/measurement-and-feedback/failures/conversation-quality-measurement-gaps.md` | Queued |  |
| 116 | XA-03 | No way to report bad behaviour | New | R | `goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md` | Queued |  |
| 117 | ME-01 | Containment counted as success | Extends | - | `goals/measurement-and-feedback/failures/containment-counted-as-success.md` | Queued |  |
| 118 | ME-02 | Survey bias | New | - | `goals/measurement-and-feedback/failures/survey-bias.md` | Queued |  |
| 119 | ME-03 | Reviewing only failures | New | - | `goals/measurement-and-feedback/failures/reviewing-only-failures.md` | Queued |  |
| 120 | ME-04 | Tone changes shipped with no regression test | New | - | `goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md` | Queued |  |
| 121 | ME-05 | User simulators more cooperative than real people | Extends | - | `goals/measurement-and-feedback/failures/user-simulators-more-cooperative-than-real-people.md` | Queued |  |
| 122 | ME-06 | Clean-lab testing | New | - | `goals/measurement-and-feedback/failures/clean-lab-testing.md` | Queued |  |
| 123 | ME-07 | Averages hide group gaps | Extends | - | `goals/measurement-and-feedback/failures/averages-hide-group-gaps.md` | Queued |  |
| 124 | AX-01 | Streaming text read out token by token | New | V | `goals/accessibility/failures/streaming-text-read-out-token-by-token.md` | Queued |  |
| 125 | AX-02 | No accessible 'working' or 'done' signal | New | - | `goals/accessibility/failures/no-accessible-working-or-done-signal.md` | Queued |  |
| 126 | AX-03 | Controls unreachable by keyboard | New | - | `goals/accessibility/failures/controls-unreachable-by-keyboard.md` | Queued |  |
| 127 | AX-04 | Voice-only flows with no text alternative | New | L | `goals/accessibility/failures/voice-only-flows-with-no-text-alternative.md` | Queued |  |
| 128 | AX-05 | Timeouts too short for assistive technology | New | - | `goals/accessibility/failures/timeouts-too-short-for-assistive-technology.md` | Queued |  |
| 129 | AX-06 | Language that is hard for people with cognitive disabilities | New | E | `goals/accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md` | Queued |  |
| 130 | AX-07 | Identity checks that exclude disabled users | New | L | `goals/accessibility/failures/identity-checks-that-exclude-disabled-users.md` | Queued |  |
| 131 | AX-08 | Missing or wrong captions and transcripts | New | - | `goals/accessibility/failures/missing-or-wrong-captions-and-transcripts.md` | Queued |  |
| 132 | CC-11 | Teens: persuasion and dependence | Extends | L, E | `goals/age-adaptation/failures/teens-persuasion-and-dependence.md` | Queued |  |
| 133 | CC-09 | Older or cognitively impaired users | New | E | `goals/vulnerable-users/failures/older-or-cognitively-impaired-users.md` | Queued |  |
| 134 | CC-10 | Financial hardship mishandled | New | L, E | `goals/vulnerable-users/failures/financial-hardship-mishandled.md` | Queued |  |
| 135 | CC-07 | Mishandled abuse | New | - | `goals/difficult-customers/failures/mishandled-abuse.md` | Queued |  |
| 136 | VI-03 | Dark patterns | New | V, L | `goals/visual/failures/dark-patterns.md` | Queued |  |
| 137 | OV-01 | Approval fatigue | Extends | V | `goals/human-oversight/failures/approval-fatigue.md` | Queued |  |
| 138 | FW-S01 | Pitching before discovery | Extends | V | `goals/conversation-frameworks/failures/pitching-before-discovery.md` | Queued |  |
| 139 | EX-07 | Hidden instructions hijack a browsing agent | Extends | V | `goals/browser-agents/failures/hidden-instructions-hijack-a-browsing-agent.md` | Queued |  |
| 140 | EX-01 | Purchase without clear authorisation | Extends | V, R, L | `goals/shopping-agents/failures/purchase-without-clear-authorisation.md` | Queued |  |
| 141 | EX-22 | Per-resolution pricing rewards counting things as resolved | Extends | V, R | `goals/customer-support-agents/failures/per-resolution-pricing-rewards-counting-things-as-resolved.md` | Queued |  |
| 142 | CD-01 | Edits beyond the request | Extends | R | `goals/coding-agents/failures/edits-beyond-the-request.md` | Queued |  |
| 143 | CD-02 | Claims tests pass without running them, or edits tests to pass | Extends | V, R | `goals/coding-agents/failures/claims-tests-pass-without-running-them-or-edits-tests.md` | Queued |  |
| 144 | CD-03 | Invented packages and APIs | New | R | `goals/coding-agents/failures/invented-packages-and-apis.md` | Queued |  |
| 145 | CD-04 | Secrets and insecure code accepted by non-experts | Extends | - | `goals/coding-agents/failures/secrets-and-insecure-code-accepted-by-non-experts.md` | Queued |  |
| 146 | CD-05 | Destroys uncommitted work | Extends | - | `goals/coding-agents/failures/destroys-uncommitted-work.md` | Queued |  |
| 147 | CD-06 | Forgets project conventions in long sessions | Extends | - | `goals/coding-agents/failures/forgets-project-conventions-in-long-sessions.md` | Queued |  |
| 148 | DA-01 | Wrong joins and double counting | New | R | `goals/research-and-data-agents/failures/wrong-joins-and-double-counting.md` | Queued |  |
| 149 | DA-02 | Wrong business definitions | New | - | `goals/research-and-data-agents/failures/wrong-business-definitions.md` | Queued |  |
| 150 | DA-03 | One-sided or cherry-picked sources | New | R | `goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md` | Queued |  |
| 151 | DA-04 | Claims to have read inaccessible sources | Extends | - | `goals/research-and-data-agents/failures/claims-to-have-read-inaccessible-sources.md` | Queued |  |
| 152 | DA-05 | Method and query not shown | Extends | - | `goals/research-and-data-agents/failures/method-and-query-not-shown.md` | Queued |  |
| 153 | WA-01 | No dry-run before bulk changes | Extends | - | `goals/workflow-automation-agents/failures/no-dry-run-before-bulk-changes.md` | Queued |  |
| 154 | WA-02 | Overwrites a person's recent edit | Extends | - | `goals/workflow-automation-agents/failures/overwrites-a-person-s-recent-edit.md` | Queued |  |
| 155 | WA-03 | Partial batch reported as done | Extends | - | `goals/workflow-automation-agents/failures/partial-batch-reported-as-done.md` | Queued |  |
| 156 | WA-04 | Silent breakage after a UI or schema change | Extends | - | `goals/workflow-automation-agents/failures/silent-breakage-after-a-ui-or-schema-change.md` | Queued |  |
| 157 | IT-01 | Credential reset for a manipulated caller | Extends | - | `goals/it-and-security-agents/failures/credential-reset-for-a-manipulated-caller.md` | Queued |  |
| 158 | IT-02 | True alerts closed as false positives | New | - | `goals/it-and-security-agents/failures/true-alerts-closed-as-false-positives.md` | Queued |  |
| 159 | IT-03 | Containment without human sign-off | Extends | - | `goals/it-and-security-agents/failures/containment-without-human-sign-off.md` | Queued |  |
| 160 | IT-04 | Outdated runbook followed with confidence | Extends | - | `goals/it-and-security-agents/failures/outdated-runbook-followed-with-confidence.md` | Queued |  |
| 161 | IT-05 | Fabricated indicators or vulnerability details | Extends | - | `goals/it-and-security-agents/failures/fabricated-indicators-or-vulnerability-details.md` | Queued |  |
| 162 | HC-01 | Scribe omissions and invented content | Extends | V, E, L | `goals/healthcare-agents/failures/scribe-omissions-and-invented-content.md` | Queued |  |
| 163 | HC-02 | Notes approved without being read | New | E | `goals/healthcare-agents/failures/notes-approved-without-being-read.md` | Queued |  |
| 164 | HC-03 | Recording consent not captured | New | L | `goals/healthcare-agents/failures/recording-consent-not-captured.md` | Queued |  |
| 165 | HC-04 | Fabricated clinical justification in appeals | New | R, L, E | `goals/healthcare-agents/failures/fabricated-clinical-justification-in-appeals.md` | Queued |  |
| 166 | HC-05 | Patient summaries too simple to be safe | New | E | `goals/healthcare-agents/failures/patient-summaries-too-simple-to-be-safe.md` | Queued |  |
| 167 | TR-04 | Transcription hallucination | New | V | `goals/voice/failures/transcription-hallucination.md` | Queued |  |
| 168 | TR-03 | Non-speech heard as speech | Extends | - | `goals/voice/failures/non-speech-heard-as-speech.md` | Queued |  |
| 169 | TR-01 | Names with no repair path | Extends | - | `goals/voice/failures/names-with-no-repair-path.md` | Queued |  |
| 170 | TR-02 | Proper nouns beyond names | Extends | V, R | `goals/voice/failures/proper-nouns-beyond-names.md` | Queued |  |
| 171 | TR-15 | Transcript treated as ground truth | Extends | V | `goals/voice/failures/transcript-treated-as-ground-truth.md` | Queued |  |
| 172 | TR-16 | Word-error-rate-only evaluation | New | R | `goals/voice/failures/word-error-rate-only-evaluation.md` | Queued |  |
| 173 | TR-09 | Dropped negations and small words | New | R, E | `goals/voice/failures/dropped-negations-and-small-words.md` | Queued |  |
| 174 | TR-08 | Punctuation and segmentation errors | New | R | `goals/voice/failures/punctuation-and-segmentation-errors.md` | Queued |  |
| 175 | TR-10 | Spelled-out strings | Extends | - | `goals/voice/failures/spelled-out-strings.md` | Queued |  |
| 176 | TR-05 | Voice-activity-detection misfires | Extends | - | `goals/voice/failures/voice-activity-detection-misfires.md` | Queued |  |
| 177 | TR-07 | Speaker attribution errors | Extends | - | `goals/voice/failures/speaker-attribution-errors.md` | Queued |  |
| 178 | TR-17 | Spoken PII persists in transcripts and audio | Extends | L | `goals/voice/failures/spoken-pii-persists-in-transcripts-and-audio.md` | Queued |  |
| 179 | TR-18 | Children's and atypical speech | Extends | V, E | `goals/voice/failures/children-s-and-atypical-speech.md` | Queued |  |
| 180 | TR-19 | Wrong recognition model for the speaker | Extends | - | `goals/voice/failures/wrong-recognition-model-for-the-speaker.md` | Queued |  |
| 181 | TR-20 | Machine audio treated as a person | Extends | - | `goals/voice/failures/machine-audio-treated-as-a-person.md` | Queued |  |
| 182 | FN-01 | Posting to the wrong period or account | New | - | `goals/finance-agents/failures/posting-to-the-wrong-period-or-account.md` | Queued |  |
| 183 | FN-02 | Inventing reconciling items | New | R | `goals/finance-agents/failures/inventing-reconciling-items.md` | Queued |  |
| 184 | FN-03 | Splitting payments under approval limits | New | - | `goals/finance-agents/failures/splitting-payments-under-approval-limits.md` | Queued |  |
| 185 | FN-04 | Payment approved by a deepfake or spoofed email | Extends | - | `goals/finance-agents/failures/payment-approved-by-a-deepfake-or-spoofed-email.md` | Queued |  |
| 186 | CC-01 | Closing without confirmation | Extends | - | `goals/conversation-leadership/failures/closing-without-confirmation.md` | Queued |  |
| 187 | CC-02 | Over-solemn handling of low-stakes requests | New | - | `goals/stakes-calibration/failures/over-solemn-handling-of-low-stakes-requests.md` | Queued |  |
| 188 | CC-03 | Missed subtext | Extends | - | `goals/emotional-intelligence/failures/missed-subtext.md` | Queued |  |
| 189 | CC-04 | Fixing before listening | New | - | `goals/emotional-intelligence/failures/fixing-before-listening.md` | Queued |  |
| 190 | CC-05 | No follow-through | New | - | `goals/trust-and-rapport/failures/no-follow-through.md` | Queued |  |
| 191 | CC-06 | Over-hedging | Extends | - | `goals/trust-and-rapport/failures/over-hedging.md` | Queued |  |
| 192 | CC-12 | Technology-literacy mismatch | New | - | `goals/cultural-adaptation/failures/technology-literacy-mismatch.md` | Queued |  |
| 193 | CC-13 | Regional and community styles | New | R | `goals/cultural-adaptation/failures/regional-and-community-styles.md` | Queued |  |
| 194 | CC-14 | Accessibility in chat | New | E, L | `goals/fairness-and-identity/failures/accessibility-in-chat.md` | Queued |  |
| 195 | CC-15 | Over-correcting for identity | New | - | `goals/fairness-and-identity/failures/over-correcting-for-identity.md` | Queued |  |
| 196 | CC-18 | Channel chosen for organisational convenience | New | - | `goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md` | Queued |  |
| 197 | CC-19 | User-context channel mismatch | New | E | `goals/channel-selection/failures/user-context-channel-mismatch.md` | Queued |  |
| 198 | CC-22 | Creepy personalisation and memory | Extends | L | `goals/trust-and-rapport/failures/creepy-personalisation-and-memory.md` | Queued |  |
| 199 | CC-23 | Proactive outreach overreach | New | L | `goals/relational-and-boundaries/failures/proactive-outreach-overreach.md` | Queued |  |
| 200 | PV-01 | Persona drift within a conversation | Extends | - | `goals/persona-and-tone/failures/persona-drift-within-a-conversation.md` | Queued |  |
| 201 | PV-02 | Persona changes after a model or prompt update | Extends | - | `goals/persona-and-tone/failures/persona-changes-after-a-model-or-prompt-update.md` | Queued |  |
| 202 | PV-03 | Condescending or patronizing tone | New | - | `goals/persona-and-tone/failures/condescending-or-patronizing-tone.md` | Queued |  |
| 203 | PV-04 | Forced cheerfulness | Extends | - | `goals/persona-and-tone/failures/forced-cheerfulness.md` | Queued |  |
| 204 | PV-05 | Stock phrases | New | - | `goals/persona-and-tone/failures/stock-phrases.md` | Queued |  |
| 205 | PV-06 | Humor and sarcasm misused | Extends | - | `goals/persona-and-tone/failures/humor-and-sarcasm-misused.md` | Queued |  |
| 206 | PV-07 | Emoji and slang that don't fit the audience | Extends | - | `goals/persona-and-tone/failures/emoji-and-slang-that-don-t-fit-the-audience.md` | Queued |  |
| 207 | PV-08 | Over-familiar address | New | - | `goals/persona-and-tone/failures/over-familiar-address.md` | Queued |  |
| 208 | PV-09 | Scripted lines at the wrong moment | Extends | - | `goals/persona-and-tone/failures/scripted-lines-at-the-wrong-moment.md` | Queued |  |
| 209 | OB-01 | Blank box: no hint what to ask | New | V | `goals/onboarding-and-discoverability/failures/blank-box-no-hint-what-to-ask.md` | Queued |  |
| 210 | OB-02 | Starter suggestions that fail | New | - | `goals/onboarding-and-discoverability/failures/starter-suggestions-that-fail.md` | Queued |  |
| 211 | OB-03 | Hidden commands and features | New | - | `goals/onboarding-and-discoverability/failures/hidden-commands-and-features.md` | Queued |  |
| 212 | OB-04 | Users must engineer prompts to get good results | New | - | `goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md` | Queued |  |
| 213 | OB-05 | First-run tours that block use | New | - | `goals/onboarding-and-discoverability/failures/first-run-tours-that-block-use.md` | Queued |  |
| 214 | OB-06 | Chat widget hard to find, or intrusive | New | V | `goals/onboarding-and-discoverability/failures/chat-widget-hard-to-find-or-intrusive.md` | Queued |  |
| 215 | CM-01 | Auto-scroll fights the reader | New | - | `goals/chat-interface/failures/auto-scroll-fights-the-reader.md` | Queued |  |
| 216 | CM-02 | Lost drafts and failed sends | New | - | `goals/chat-interface/failures/lost-drafts-and-failed-sends.md` | Queued |  |
| 217 | CM-03 | Silent attachment failures | New | - | `goals/chat-interface/failures/silent-attachment-failures.md` | Queued |  |
| 218 | CM-04 | Long threads can't be searched | New | - | `goals/chat-interface/failures/long-threads-can-t-be-searched.md` | Queued |  |
| 219 | CM-05 | No editing or branching of a sent message | New | - | `goals/chat-interface/failures/no-editing-or-branching-of-a-sent-message.md` | Queued |  |
| 220 | CM-06 | Copy, share, and export lose content | New | - | `goals/chat-interface/failures/copy-share-and-export-lose-content.md` | Queued |  |
| 221 | CM-07 | Quick-reply buttons that don't match what was typed | New | - | `goals/chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md` | Queued |  |
| 222 | CM-08 | Crossed messages | New | - | `goals/chat-interface/failures/crossed-messages.md` | Queued |  |
| 223 | CM-09 | Mobile keyboard or screen hides the reply | New | - | `goals/chat-interface/failures/mobile-keyboard-or-screen-hides-the-reply.md` | Queued |  |
| 224 | CM-10 | Shared devices show someone else's chat | Extends | L | `goals/chat-interface/failures/shared-devices-show-someone-else-s-chat.md` | Queued |  |
| 225 | SA-01 | Invented personalisation | Extends | - | `goals/sales-agents/failures/invented-personalisation.md` | Queued |  |
| 226 | SA-02 | Unsubscribe requests not honoured | New | L | `goals/sales-agents/failures/unsubscribe-requests-not-honoured.md` | Queued |  |
| 227 | SA-03 | Wrong contact merged in the CRM | Extends | - | `goals/sales-agents/failures/wrong-contact-merged-in-the-crm.md` | Queued |  |
| 228 | SA-04 | Double-booked meetings | Extends | - | `goals/sales-agents/failures/double-booked-meetings.md` | Queued |  |
| 229 | FW-S02 | No qualification | Extends | R | `goals/conversation-frameworks/failures/no-qualification.md` | Queued |  |
| 230 | FW-S03 | Feature dump instead of insight | New | V | `goals/conversation-frameworks/failures/feature-dump-instead-of-insight.md` | Queued |  |
| 231 | FW-S04 | Mishandled objections | New | R | `goals/conversation-frameworks/failures/mishandled-objections.md` | Queued |  |
| 232 | FW-S05 | No ask | New | - | `goals/conversation-frameworks/failures/no-ask.md` | Queued |  |
| 233 | FW-S06 | Manipulative closing | Extends | L, R | `goals/conversation-frameworks/failures/manipulative-closing.md` | Queued |  |
| 234 | FW-S07 | Discount-first selling | Extends | - | `goals/conversation-frameworks/failures/discount-first-selling.md` | Queued |  |
| 235 | FW-S08 | No follow-up | New | L | `goals/conversation-frameworks/failures/no-follow-up.md` | Queued |  |
| 236 | FW-S09 | Buying-committee blindness (B2B) | New | R | `goals/conversation-frameworks/failures/buying-committee-blindness-b2b.md` | Queued |  |
| 237 | FW-S10 | Wrong-fit recommendation | New | - | `goals/conversation-frameworks/failures/wrong-fit-recommendation.md` | Queued |  |
| 238 | FW-S11 | Upsell at the wrong moment | New | - | `goals/conversation-frameworks/failures/upsell-at-the-wrong-moment.md` | Queued |  |
| 239 | FW-S12 | Lead handoff without qualification | Extends | - | `goals/conversation-frameworks/failures/lead-handoff-without-qualification.md` | Queued |  |
| 240 | FW-C01 | No triage or severity check | Extends | - | `goals/conversation-frameworks/failures/no-triage-or-severity-check.md` | Queued |  |
| 241 | FW-C02 | Unstructured troubleshooting | New | - | `goals/conversation-frameworks/failures/unstructured-troubleshooting.md` | Queued |  |
| 242 | FW-C03 | Symptom fixed, root cause missed | New | - | `goals/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md` | Queued |  |
| 243 | FW-C04 | High customer effort | Extends | V | `goals/conversation-frameworks/failures/high-customer-effort.md` | Queued |  |
| 244 | FW-C05 | No proactive updates | New | - | `goals/conversation-frameworks/failures/no-proactive-updates.md` | Queued |  |
| 245 | FW-C06 | No learning loop | Extends | - | `goals/conversation-frameworks/failures/no-learning-loop.md` | Queued |  |
| 246 | FW-C07 | Service recovery failure | New | R | `goals/conversation-frameworks/failures/service-recovery-failure.md` | Queued |  |
| 247 | FW-C08 | Bad news without structure | New | V, E | `goals/conversation-frameworks/failures/bad-news-without-structure.md` | Queued |  |
| 248 | FW-C09 | Instructions without comprehension checks | New | R | `goals/conversation-frameworks/failures/instructions-without-comprehension-checks.md` | Queued |  |
| 249 | FW-C10 | Behaviour-change talk without listening skills | New | V, E | `goals/conversation-frameworks/failures/behaviour-change-talk-without-listening-skills.md` | Queued |  |
| 250 | FW-M01 | No style matching | Extends | V, R | `goals/conversation-frameworks/failures/no-style-matching.md` | Queued |  |
| 251 | FW-M02 | Over-mirroring | New | - | `goals/conversation-frameworks/failures/over-mirroring.md` | Queued |  |
| 252 | FW-M03 | Mirroring hostility | New | - | `goals/conversation-frameworks/failures/mirroring-hostility.md` | Queued |  |
| 253 | FW-M04 | Imitating dialect or errors | New | E | `goals/conversation-frameworks/failures/imitating-dialect-or-errors.md` | Queued |  |
| 254 | FW-M06 | Style whiplash | Extends | - | `goals/conversation-frameworks/failures/style-whiplash.md` | Queued |  |
| 255 | FW-M07 | No reflective listening | New | V | `goals/conversation-frameworks/failures/no-reflective-listening.md` | Queued |  |
| 256 | FW-M08 | Misused tactical empathy | New | V, R | `goals/conversation-frameworks/failures/misused-tactical-empathy.md` | Queued |  |
| 257 | FW-O01 | Cooperation violations | Extends | R | `goals/conversation-frameworks/failures/cooperation-violations.md` | Queued |  |
| 258 | FW-O02 | Bad endings | Extends | R | `goals/conversation-frameworks/failures/bad-endings.md` | Queued |  |
| 259 | GV-01 | Over-collection of personal data | Extends | - | `goals/privacy-and-governance/failures/over-collection-of-personal-data.md` | Queued |  |
| 260 | GV-02 | Sensitive data echoed or read aloud | Extends | - | `goals/privacy-and-governance/failures/sensitive-data-echoed-or-read-aloud.md` | Queued |  |
| 261 | GV-03 | Third-party data shared by users | New | R, L | `goals/privacy-and-governance/failures/third-party-data-shared-by-users.md` | Queued |  |
| 262 | GV-05 | Sensitive-category inference | New | R, L, E | `goals/privacy-and-governance/failures/sensitive-category-inference.md` | Queued |  |
| 263 | GV-07 | Memory the user can't see or control | Extends | L | `goals/privacy-and-governance/failures/memory-the-user-can-t-see-or-control.md` | Queued |  |
| 264 | GV-08 | Privacy-rights requests not recognised | New | V, L, R | `goals/privacy-and-governance/failures/privacy-rights-requests-not-recognised.md` | Queued |  |
| 265 | GV-09 | Weak or excessive identity verification | Extends | - | `goals/privacy-and-governance/failures/weak-or-excessive-identity-verification.md` | Queued |  |
| 266 | GV-10 | No notice or consent at the moment of collection | Extends | L | `goals/privacy-and-governance/failures/no-notice-or-consent-at-the-moment-of-collection.md` | Queued |  |
| 267 | GV-12 | Recording, transcription, and training-use notice | Extends | L | `goals/privacy-and-governance/failures/recording-transcription-and-training-use-notice.md` | Queued |  |
| 268 | GV-14 | Role claims accepted from the conversation | Extends | - | `goals/privacy-and-governance/failures/role-claims-accepted-from-the-conversation.md` | Queued |  |
| 269 | GV-23 | Denial messages that leak or dead-end | Extends | - | `goals/privacy-and-governance/failures/denial-messages-that-leak-or-dead-end.md` | Queued |  |
| 270 | GV-34 | Rules not explainable to users | Extends | - | `goals/privacy-and-governance/failures/rules-not-explainable-to-users.md` | Queued |  |
| 271 | GV-36 | No user-facing record of what the bot said or promised | New | L | `goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md` | Queued |  |
| 272 | GV-37 | Consequential automated decisions with no explanation or review | Extends | R, L | `goals/privacy-and-governance/failures/consequential-automated-decisions-with-no-explanation-or-review.md` | Queued |  |
| 273 | GV-38 | Manipulative persuasion | Extends | L, E | `goals/privacy-and-governance/failures/manipulative-persuasion.md` | Queued |  |
| 274 | GV-39 | Deceptive anthropomorphism | Extends | - | `goals/privacy-and-governance/failures/deceptive-anthropomorphism.md` | Queued |  |
| 275 | GV-40 | Engagement-maximising design that harms | New | L, E | `goals/privacy-and-governance/failures/engagement-maximising-design-that-harms.md` | Queued |  |
| 276 | GV-41 | Exploiting vulnerable circumstances | New | L, E | `goals/privacy-and-governance/failures/exploiting-vulnerable-circumstances.md` | Queued |  |
| 277 | GV-42 | Calibration between helping with wrongdoing and over-blocking | Extends | E | `goals/privacy-and-governance/failures/calibration-between-helping-with-wrongdoing-and-over-blocking.md` | Queued |  |
| 278 | EX-02 | Wrong item or variant bought | Extends | - | `goals/shopping-agents/failures/wrong-item-or-variant-bought.md` | Queued |  |
| 279 | EX-03 | Merchant content steers the shopping agent | Extends | V | `goals/shopping-agents/failures/merchant-content-steers-the-shopping-agent.md` | Queued |  |
| 280 | EX-04 | Spend and category limits not enforced | Extends | - | `goals/shopping-agents/failures/spend-and-category-limits-not-enforced.md` | Queued |  |
| 281 | EX-05 | No clear route when an agent buys wrongly | New | R, L | `goals/shopping-agents/failures/no-clear-route-when-an-agent-buys-wrongly.md` | Queued |  |
| 282 | EX-06 | Sponsored ranking inside agent recommendations | New | L | `goals/shopping-agents/failures/sponsored-ranking-inside-agent-recommendations.md` | Queued |  |
| 283 | EX-08 | Agent uses the user's logged-in sessions with full reach | Extends | - | `goals/browser-agents/failures/agent-uses-the-user-s-logged-in-sessions-with.md` | Queued |  |
| 284 | EX-09 | Misreading the screen | New | R | `goals/browser-agents/failures/misreading-the-screen.md` | Queued |  |
| 285 | EX-11 | Tool-name collisions | Extends | V | `goals/tool-ecosystems/failures/tool-name-collisions.md` | Queued |  |
| 286 | EX-12 | Unauthenticated tool servers | Extends | V | `goals/tool-ecosystems/failures/unauthenticated-tool-servers.md` | Queued |  |
| 287 | EX-14 | Consent fatigue from tool sprawl | Extends | - | `goals/tool-ecosystems/failures/consent-fatigue-from-tool-sprawl.md` | Queued |  |
| 288 | EX-16 | Recorders that join without everyone's consent | New | V, L | `goals/meeting-agents/failures/recorders-that-join-without-everyone-s-consent.md` | Queued |  |
| 289 | EX-17 | Summaries that misattribute or invent action items | Extends | R | `goals/meeting-agents/failures/summaries-that-misattribute-or-invent-action-items.md` | Queued |  |
| 290 | EX-18 | Voiceprints captured without consent | New | R, L | `goals/meeting-agents/failures/voiceprints-captured-without-consent.md` | Queued |  |
| 291 | EX-19 | Emotional pressure when users try to leave | New | R, L, E | `goals/companion-and-wellbeing-agents/failures/emotional-pressure-when-users-try-to-leave.md` | Queued |  |
| 292 | EX-20 | AI offering therapy where the law restricts it | New | V, L, E | `goals/companion-and-wellbeing-agents/failures/ai-offering-therapy-where-the-law-restricts-it.md` | Queued |  |
| 293 | EX-21 | Hiring and screening tools with unequal impact | Extends | V, L | `goals/hr-agents/failures/hiring-and-screening-tools-with-unequal-impact.md` | Queued |  |
| 294 | EX-23 | Agent-to-agent negotiation without clear authority | Extends | R | `goals/multi-agent-platforms/failures/agent-to-agent-negotiation-without-clear-authority.md` | Queued |  |
| 295 | EX-24 | AI-voice outbound calls without consent | Extends | V, L | `goals/voice-receptionist-agents/failures/ai-voice-outbound-calls-without-consent.md` | Queued |  |
| 296 | EX-25 | Cloned voices defeat voice authentication | Extends | L, R | `goals/voice/failures/cloned-voices-defeat-voice-authentication.md` | Queued |  |
| 297 | VO-06 | No repeat or recap controls | New | - | `goals/voice/failures/no-repeat-or-recap-controls.md` | Queued |  |
| 298 | VO-08 | Atypical speech mishandled | New | E | `goals/voice/failures/atypical-speech-mishandled.md` | Queued |  |
| 299 | VO-11 | Spoken-language misidentification | Extends | - | `goals/voice/failures/spoken-language-misidentification.md` | Queued |  |
| 300 | VO-12 | Dense information read aloud | Extends | R | `goals/voice/failures/dense-information-read-aloud.md` | Queued |  |
| 301 | VO-15 | Fixed speaking rate and volume | New | - | `goals/voice/failures/fixed-speaking-rate-and-volume.md` | Queued |  |
| 302 | VO-16 | IVR-style menu maze | New | - | `goals/voice/failures/ivr-style-menu-maze.md` | Queued |  |
| 303 | VO-17 | Spoken sensitive data | Extends | L | `goals/voice/failures/spoken-sensitive-data.md` | Queued |  |
| 304 | VO-18 | Missing disclosure and recording notice | Extends | L | `goals/voice/failures/missing-disclosure-and-recording-notice.md` | Queued |  |
| 305 | VO-19 | Voice cloning and spoofing | Extends | L, R | `goals/voice/failures/voice-cloning-and-spoofing.md` | Queued |  |
| 306 | VO-20 | Answering-machine and voicemail errors | Extends | L, R | `goals/voice/failures/answering-machine-and-voicemail-errors.md` | Queued |  |
| 307 | VO-21 | Wake-word false activation | New | L | `goals/voice/failures/wake-word-false-activation.md` | Queued |  |
| 308 | VO-22 | Emotion inferred from voice | New | L, R, E | `goals/voice/failures/emotion-inferred-from-voice.md` | Queued |  |
| 309 | VO-23 | Voice-to-visual handoff failure | New | - | `goals/voice/failures/voice-to-visual-handoff-failure.md` | Queued |  |
| 310 | VO-24 | Hold and wait handling | Extends | - | `goals/voice/failures/hold-and-wait-handling.md` | Queued |  |
| 311 | VA-01 | Bookings without confirming details | New | - | `goals/voice-receptionist-agents/failures/bookings-without-confirming-details.md` | Queued |  |
| 312 | VA-02 | Emergency phrases missed in routine calls | Extends | E | `goals/voice-receptionist-agents/failures/emergency-phrases-missed-in-routine-calls.md` | Queued |  |
| 313 | VA-03 | Collections calls without required disclosures | New | L, R | `goals/voice-receptionist-agents/failures/collections-calls-without-required-disclosures.md` | Queued |  |
| 314 | BA-01 | Bypasses CAPTCHAs or site terms | New | L | `goals/browser-agents/failures/bypasses-captchas-or-site-terms.md` | Queued |  |
| 315 | BA-02 | Accepts consent pop-ups for the user | New | L | `goals/browser-agents/failures/accepts-consent-pop-ups-for-the-user.md` | Queued |  |
| 316 | BA-03 | Navigation loops and cost blow-ups | Extends | - | `goals/browser-agents/failures/navigation-loops-and-cost-blow-ups.md` | Queued |  |
| 317 | BA-04 | Asks for credentials at login walls | Extends | - | `goals/browser-agents/failures/asks-for-credentials-at-login-walls.md` | Queued |  |
| 318 | SH-01 | Stale price or stock at checkout | New | - | `goals/shopping-agents/failures/stale-price-or-stock-at-checkout.md` | Queued |  |
| 319 | SH-02 | Free trials that become paid subscriptions | New | L | `goals/shopping-agents/failures/free-trials-that-become-paid-subscriptions.md` | Queued |  |
| 320 | SH-03 | Return policy ignored | New | - | `goals/shopping-agents/failures/return-policy-ignored.md` | Queued |  |
| 321 | SH-04 | Shared accounts reveal gifts | New | - | `goals/shopping-agents/failures/shared-accounts-reveal-gifts.md` | Queued |  |
| 322 | PA-01 | Sends in the wrong tone or to the wrong person | Extends | - | `goals/personal-assistants/failures/sends-in-the-wrong-tone-or-to-the-wrong.md` | Queued |  |
| 323 | PA-02 | Books non-refundable travel on a guess | Extends | - | `goals/personal-assistants/failures/books-non-refundable-travel-on-a-guess.md` | Queued |  |
| 324 | PA-03 | Time-zone and double-booking errors | Extends | - | `goals/personal-assistants/failures/time-zone-and-double-booking-errors.md` | Queued |  |
| 325 | MI-01 | Screenshot ignored or misread | Extends | - | `goals/multimodal-input/failures/screenshot-ignored-or-misread.md` | Queued |  |
| 326 | MI-02 | Long upload silently cut | Extends | - | `goals/multimodal-input/failures/long-upload-silently-cut.md` | Queued |  |
| 327 | MI-03 | Voice notes and audio attachments ignored | New | - | `goals/multimodal-input/failures/voice-notes-and-audio-attachments-ignored.md` | Queued |  |
| 328 | MI-04 | Confident judgment of a photo | Extends | E | `goals/multimodal-input/failures/confident-judgment-of-a-photo.md` | Queued |  |
| 329 | MI-05 | Live camera guidance too slow or wrong | New | R | `goals/multimodal-input/failures/live-camera-guidance-too-slow-or-wrong.md` | Queued |  |
| 330 | MI-06 | Conflicting inputs resolved silently | New | - | `goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md` | Queued |  |
| 331 | MI-07 | Images of IDs and documents kept without need | Extends | L | `goals/multimodal-input/failures/images-of-ids-and-documents-kept-without-need.md` | Queued |  |
| 332 | MI-08 | No warning about input limits | New | - | `goals/multimodal-input/failures/no-warning-about-input-limits.md` | Queued |  |
| 333 | MO-01 | A model change shifts personality, length, or refusals | Extends | - | `goals/model-and-prompt-changes/failures/a-model-change-shifts-personality-length-or-refusals.md` | Queued |  |
| 334 | MO-02 | Fallback model gives a visibly different experience | Extends | - | `goals/model-and-prompt-changes/failures/fallback-model-gives-a-visibly-different-experience.md` | Queued |  |
| 335 | MO-03 | Prompt edits by non-engineers break other behavior | New | - | `goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md` | Queued |  |
| 336 | MO-04 | Quiet degradation under peak load | Extends | - | `goals/model-and-prompt-changes/failures/quiet-degradation-under-peak-load.md` | Queued |  |
| 337 | MO-05 | Memory contaminates conversation experiments | New | - | `goals/model-and-prompt-changes/failures/memory-contaminates-conversation-experiments.md` | Queued |  |
| 338 | LG-01 | Wrong-language reply | Extends | - | `goals/language-and-locale/failures/wrong-language-reply.md` | Queued |  |
| 339 | LG-03 | Language switch ignored | Extends | - | `goals/language-and-locale/failures/language-switch-ignored.md` | Queued |  |
| 340 | LG-04 | Unchecked translation in high-stakes text | New | E | `goals/language-and-locale/failures/unchecked-translation-in-high-stakes-text.md` | Queued |  |
| 341 | LG-05 | Politeness and formality errors | New | R, E | `goals/language-and-locale/failures/politeness-and-formality-errors.md` | Queued |  |
| 342 | LG-06 | Reading-level mismatch | New | R | `goals/language-and-locale/failures/reading-level-mismatch.md` | Queued |  |
| 343 | LG-07 | Jargon, acronyms, and idioms | Extends | - | `goals/language-and-locale/failures/jargon-acronyms-and-idioms.md` | Queued |  |
| 344 | LG-08 | Locale format errors | Extends | - | `goals/language-and-locale/failures/locale-format-errors.md` | Queued |  |
| 345 | LG-09 | Name and transliteration errors | Extends | - | `goals/language-and-locale/failures/name-and-transliteration-errors.md` | Queued |  |
| 346 | LG-10 | Gender and pronoun errors | New | E | `goals/language-and-locale/failures/gender-and-pronoun-errors.md` | Queued |  |
| 347 | LG-11 | Dialect and slang misreading | Extends | - | `goals/language-and-locale/failures/dialect-and-slang-misreading.md` | Queued |  |
| 348 | LG-12 | Typos, shorthand, and noisy input | New | - | `goals/language-and-locale/failures/typos-shorthand-and-noisy-input.md` | Queued |  |
| 349 | LG-13 | Emoji and punctuation tone misreads | Extends | R | `goals/language-and-locale/failures/emoji-and-punctuation-tone-misreads.md` | Queued |  |
| 350 | LG-14 | Profanity and slang handling | New | - | `goals/language-and-locale/failures/profanity-and-slang-handling.md` | Queued |  |
| 351 | LG-15 | Mixed-language experience | New | - | `goals/language-and-locale/failures/mixed-language-experience.md` | Queued |  |
| 352 | LG-16 | Right-to-left and mixed-script rendering | New | - | `goals/language-and-locale/failures/right-to-left-and-mixed-script-rendering.md` | Queued |  |
| 353 | ED-01 | Gives answers instead of teaching | New | - | `goals/education-agents/failures/gives-answers-instead-of-teaching.md` | Queued |  |
| 354 | ED-02 | Wrong explanations taught as fact | New | R | `goals/education-agents/failures/wrong-explanations-taught-as-fact.md` | Queued |  |
| 355 | ED-03 | Unfair or inconsistent grading | Extends | R | `goals/education-agents/failures/unfair-or-inconsistent-grading.md` | Queued |  |
| 356 | ED-04 | Student data and surveillance | Extends | L | `goals/education-agents/failures/student-data-and-surveillance.md` | Queued |  |
| 357 | HR-01 | Employee-relations complaints routed wrongly | New | L | `goals/hr-agents/failures/employee-relations-complaints-routed-wrongly.md` | Queued |  |
| 358 | HR-02 | Pay or leave answers that leak confidential data | Extends | - | `goals/hr-agents/failures/pay-or-leave-answers-that-leak-confidential-data.md` | Queued |  |
| 359 | HR-03 | Manager and employee views mixed up | Extends | - | `goals/hr-agents/failures/manager-and-employee-views-mixed-up.md` | Queued |  |
| 360 | LA-01 | Crossing into practising law | New | L, E | `goals/legal-agents/failures/crossing-into-practising-law.md` | Queued |  |
| 361 | MA-01 | Agents contradict each other | Extends | - | `goals/multi-agent-platforms/failures/agents-contradict-each-other.md` | Queued |  |
| 362 | MA-02 | Internal coordination leaks into replies | Extends | - | `goals/multi-agent-platforms/failures/internal-coordination-leaks-into-replies.md` | Queued |  |
| 363 | AM-01 | Interrupts at a bad moment | New | - | `goals/proactive-and-ambient/failures/interrupts-at-a-bad-moment.md` | Queued |  |
| 364 | AM-02 | Dismissed suggestions come back | New | - | `goals/proactive-and-ambient/failures/dismissed-suggestions-come-back.md` | Queued |  |
| 365 | AM-03 | Summaries and digests too long to read | New | - | `goals/proactive-and-ambient/failures/summaries-and-digests-too-long-to-read.md` | Queued |  |
| 366 | AM-04 | Ambient assistants act on overheard conversation | New | L | `goals/proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md` | Queued |  |
| 367 | AM-05 | Proactive action surprises the user | Extends | - | `goals/proactive-and-ambient/failures/proactive-action-surprises-the-user.md` | Queued |  |
| 368 | GC-01 | Answers the wrong person in a group | New | - | `goals/group-and-shared-chats/failures/answers-the-wrong-person-in-a-group.md` | Queued |  |
| 369 | GC-02 | One member's private information shown to the group | Extends | L | `goals/group-and-shared-chats/failures/one-member-s-private-information-shown-to-the-group.md` | Queued |  |
| 370 | GC-03 | Conflicting instructions from different members | Extends | - | `goals/group-and-shared-chats/failures/conflicting-instructions-from-different-members.md` | Queued |  |
| 371 | GC-04 | The bot talks over people | New | - | `goals/group-and-shared-chats/failures/the-bot-talks-over-people.md` | Queued |  |
| 372 | DT-02 | Modifiers and customizations misparsed | New | R | `goals/drive-thru-agents/failures/modifiers-and-customizations-misparsed.md` | Queued |  |
| 373 | DT-03 | Upsell pressure at the speaker | New | - | `goals/drive-thru-agents/failures/upsell-pressure-at-the-speaker.md` | Queued |  |
| 374 | DT-04 | Screen and spoken order disagree | New | - | `goals/drive-thru-agents/failures/screen-and-spoken-order-disagree.md` | Queued |  |
| 375 | DT-05 | Allergy and dietary requests handled loosely | New | E, L | `goals/drive-thru-agents/failures/allergy-and-dietary-requests-handled-loosely.md` | Queued |  |
| 376 | IC-01 | Replies too long or visual for a driver | New | E, L | `goals/in-car-and-home-assistants/failures/replies-too-long-or-visual-for-a-driver.md` | Queued |  |
| 377 | IC-02 | Smart-home commands go to the wrong device or room | New | - | `goals/in-car-and-home-assistants/failures/smart-home-commands-go-to-the-wrong-device-or.md` | Queued |  |
| 378 | IC-03 | Anyone can issue a sensitive voice command | New | L | `goals/in-car-and-home-assistants/failures/anyone-can-issue-a-sensitive-voice-command.md` | Queued |  |
| 379 | IC-04 | Always-listening surprises | New | L | `goals/in-car-and-home-assistants/failures/always-listening-surprises.md` | Queued |  |
| 380 | IC-05 | Purchases by children or the TV | New | L | `goals/in-car-and-home-assistants/failures/purchases-by-children-or-the-tv.md` | Queued |  |
| 381 | GS-02 | Plain-language and language access gaps | New | L | `goals/government-service-agents/failures/plain-language-and-language-access-gaps.md` | Queued |  |
| 382 | GS-03 | Deadlines and document lists wrong or stale | Extends | - | `goals/government-service-agents/failures/deadlines-and-document-lists-wrong-or-stale.md` | Queued |  |
| 383 | GS-04 | Identity checks exclude people without standard IDs | New | L | `goals/government-service-agents/failures/identity-checks-exclude-people-without-standard-ids.md` | Queued |  |
| 384 | GS-05 | No appeal or human path for denials | New | L | `goals/government-service-agents/failures/no-appeal-or-human-path-for-denials.md` | Queued |  |
| 385 | TV-01 | Disruption rebooking with wrong rules and no human path | New | R | `goals/travel-and-utility-agents/failures/disruption-rebooking-with-wrong-rules-and-no-human-path.md` | Queued |  |
| 386 | TV-02 | Outage updates generic or late | New | - | `goals/travel-and-utility-agents/failures/outage-updates-generic-or-late.md` | Queued |  |
| 387 | TV-03 | Refund and credit rules misquoted | Extends | - | `goals/travel-and-utility-agents/failures/refund-and-credit-rules-misquoted.md` | Queued |  |
| 388 | TV-04 | Group bookings mix up travelers | New | - | `goals/travel-and-utility-agents/failures/group-bookings-mix-up-travelers.md` | Queued |  |
| 389 | BK-01 | Fraud-alert conversations that look like phishing | New | L, E | `goals/banking-agents/failures/fraud-alert-conversations-that-look-like-phishing.md` | Queued |  |
| 390 | BK-02 | Unusual activity explained too vaguely | New | E | `goals/banking-agents/failures/unusual-activity-explained-too-vaguely.md` | Queued |  |
| 391 | BK-03 | Disputed-transaction intake loses details | Extends | - | `goals/banking-agents/failures/disputed-transaction-intake-loses-details.md` | Queued |  |
| 392 | CI-01 | Cold handling of a loss | Extends | - | `goals/insurance-claims-agents/failures/cold-handling-of-a-loss.md` | Queued |  |
| 393 | CI-02 | Coverage answers sound like guarantees | New | L | `goals/insurance-claims-agents/failures/coverage-answers-sound-like-guarantees.md` | Queued |  |
| 394 | CI-03 | Photo-evidence guidance fails | Extends | - | `goals/insurance-claims-agents/failures/photo-evidence-guidance-fails.md` | Queued |  |
| 395 | HS-01 | Triage wording understates or overstates urgency | New | E, L | `goals/health-scheduling-agents/failures/triage-wording-understates-or-overstates-urgency.md` | Queued |  |
| 396 | HS-02 | Medication instructions misunderstood | New | E | `goals/health-scheduling-agents/failures/medication-instructions-misunderstood.md` | Queued |  |
| 397 | HS-03 | Scheduling picks the wrong provider or visit type | New | - | `goals/health-scheduling-agents/failures/scheduling-picks-the-wrong-provider-or-visit-type.md` | Queued |  |
| 398 | HS-04 | Results delivered without context | New | E, L | `goals/health-scheduling-agents/failures/results-delivered-without-context.md` | Queued |  |
| 399 | RE-01 | Steering by protected class in recommendations | New | L, E | `goals/real-estate-agents/failures/steering-by-protected-class-in-recommendations.md` | Queued |  |
| 400 | RE-02 | Maintenance emergencies not recognized | New | E, L | `goals/real-estate-agents/failures/maintenance-emergencies-not-recognized.md` | Queued |  |
| 401 | LC-01 | Marketing texts without consent | New | L | `goals/outbound-messaging-agents/failures/marketing-texts-without-consent.md` | Queued |  |
| 402 | LC-02 | Quiet hours and time zones ignored | New | L | `goals/outbound-messaging-agents/failures/quiet-hours-and-time-zones-ignored.md` | Queued |  |
| 403 | LC-03 | Do-not-call lists not checked | New | L | `goals/outbound-messaging-agents/failures/do-not-call-lists-not-checked.md` | Queued |  |
| 404 | RP-01 | Role-play drifts into harmful or unwanted territory | New | L, E | `goals/companion-and-wellbeing-agents/failures/role-play-drifts-into-harmful-or-unwanted-territory.md` | Queued |  |
| 405 | RP-02 | Bereavement handled with scripts | Extends | E | `goals/companion-and-wellbeing-agents/failures/bereavement-handled-with-scripts.md` | Queued |  |
| 406 | VI-01 | Cognitive overload | New | R | `goals/visual/failures/cognitive-overload.md` | Queued |  |
| 407 | VI-02 | No clear primary action | New | - | `goals/visual/failures/no-clear-primary-action.md` | Queued |  |
| 408 | VI-04 | Accessibility gaps | New | V, L, E | `goals/visual/failures/accessibility-gaps.md` | Queued |  |
| 409 | VI-05 | Motion and flashing harm | New | E, R | `goals/visual/failures/motion-and-flashing-harm.md` | Queued |  |
| 410 | VI-06 | Colour-only encoding | New | E | `goals/visual/failures/colour-only-encoding.md` | Queued |  |
| 411 | VI-07 | Small targets and small screens | New | V | `goals/visual/failures/small-targets-and-small-screens.md` | Queued |  |
| 412 | VI-08 | Misleading generated visuals | New | L | `goals/visual/failures/misleading-generated-visuals.md` | Queued |  |
| 413 | VI-09 | Unlabelled synthetic faces and avatars | Extends | L | `goals/visual/failures/unlabelled-synthetic-faces-and-avatars.md` | Queued |  |
| 414 | VI-10 | Avatar overpromising | New | R | `goals/visual/failures/avatar-overpromising.md` | Queued |  |
| 415 | VI-11 | Rich-card misuse | New | - | `goals/visual/failures/rich-card-misuse.md` | Queued |  |
| 416 | VI-12 | Sensitive-data forms | Extends | L | `goals/visual/failures/sensitive-data-forms.md` | Queued |  |
| 417 | VI-13 | Stakes-blind visual style | Extends | - | `goals/visual/failures/stakes-blind-visual-style.md` | Queued |  |
| 418 | VI-14 | Misleading charts | New | - | `goals/visual/failures/misleading-charts.md` | Queued |  |
| 419 | VI-15 | Missing loading, empty, and error states | New | V | `goals/visual/failures/missing-loading-empty-and-error-states.md` | Queued |  |
| 420 | VI-16 | Generative UI instability | New | R | `goals/visual/failures/generative-ui-instability.md` | Queued |  |
| 421 | VI-17 | Visuals that don't localise | New | R | `goals/visual/failures/visuals-that-don-t-localise.md` | Queued |  |
| 422 | VI-18 | Notification overload | New | L | `goals/visual/failures/notification-overload.md` | Queued |  |
| 423 | VI-19 | Manipulated consent UI | New | L | `goals/visual/failures/manipulated-consent-ui.md` | Queued |  |
| 424 | VI-20 | Fake urgency and trust cues | New | L | `goals/visual/failures/fake-urgency-and-trust-cues.md` | Queued |  |
| 425 | OV-02 | Hidden agent actions | Extends | - | `goals/human-oversight/failures/hidden-agent-actions.md` | Queued |  |
| 426 | OV-04 | Poor action previews | Extends | - | `goals/human-oversight/failures/poor-action-previews.md` | Queued |  |
| 427 | OV-05 | Miscalibrated confidence display | Extends | R | `goals/human-oversight/failures/miscalibrated-confidence-display.md` | Queued |  |
| 428 | OV-07 | Invisible long-running status | Extends | V | `goals/human-oversight/failures/invisible-long-running-status.md` | Queued |  |
| 429 | OV-08 | No stop or takeover | Extends | - | `goals/human-oversight/failures/no-stop-or-takeover.md` | Queued |  |
| 430 | OV-09 | Permission fatigue or under-asking | Extends | - | `goals/human-oversight/failures/permission-fatigue-or-under-asking.md` | Queued |  |
| 431 | OV-10 | Misleading explanations | Extends | R | `goals/human-oversight/failures/misleading-explanations.md` | Queued |  |
| 432 | OV-12 | Confusion over who is acting | Extends | - | `goals/human-oversight/failures/confusion-over-who-is-acting.md` | Queued |  |

## Run log
*(Each run appends an entry here.)*

### Run 1: 2026-10-18 19:16 UTC (first scheduled run): Blocked
- **Patterns:** none written. HU-01, HU-02 and HU-03 stay *Queued*.
- **Why:** the session's network policy refuses every source host tried: `files.consumerfinance.gov`, `www.consumerfinance.gov`, `www.gartner.com`, `www.ftc.gov`, `www.lawcommentary.com`, `en.wikipedia.org` and `www.techradar.com` (proxy returned 403, `connect_rejected`). Web search works but returns only summaries, which the Definition of done does not accept as opened sources.
- **Read through summaries only, not used in any file:** the CFPB 2023 chatbot issue spotlight (doom loops); a Gartner July 2024 survey (64% prefer no AI in customer service; 53% would consider switching); reports of a proposed California bill on human customer service. None was opened, so none was written down as a fact.
- **Needs from a person:** allow outbound access to source sites in the environment's Network access settings (a broader level, or add the hosts under Allowed domains). Until then each run stops at step 0.
- **Content-program task and SEO review:** not done. The SEO review needs Search Console, which needs Chrome or an export; neither is available.

### Runs 2 to 5: 2026-10-18 20:16 to 23:16 UTC (hourly): Blocked
- *(Repeat blocked runs update this one entry instead of adding a new one each hour.)*
- Step 0 failed again: `www.consumerfinance.gov` is still unreachable (no HTTP response through the proxy). Nothing written; queue unchanged (checked `consumerfinance.gov`, `gartner.com`, `ftc.gov`; all unreachable at 21:17 UTC). Same fix needed as run 1: allow source sites in the environment's Network access settings.

### Run 10 (manual, run now): 2026-10-19 03:55 UTC onward
- **HU-01 'Talk to a human' ignored or looped: Done.** File: `goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md`, plus a new family README, `tests/talk-to-a-human-ignored-or-looped.md` (12 conversations, results "Not yet run") and `incidents/cfpb-bank-chatbot-doom-loops.md`.
- **Sources opened (3 of 5 cited):** the CFPB report PDF (full text read: sections 1, 3.1.3, and 5) and the CFPB landing page. **Read through a search summary only:** the Gartner July 2024 press release (page returned 403) and the 64% / 53% figures, shown in the pattern as unverified. **Not used:** a "68% abandon" claim (traces to a blog), the HBS anxiety paper (403, cited by the CFPB), a California bill on human customer service (403 on the statute site; status unverified), a Klarna reversal (only summaries; Bloomberg original not opened).
- **Claims left unverified:** the 37% of US population figure (CFPB's own estimate from a source not opened); the Gartner figures.
- **Review pass changed:** softened the family README's claim about customers' top complaint; marked the "why it happens" causes as our reading; added the incident link to the Maturity row.
- **Incident:** the site's incidents folder has no similar page; new page written in the site's format as a draft for a person to copy.
- **HU-02 Escalates too early, or too late: Done.** File: `goals/human-handoff/failures/escalates-too-early-or-too-late.md`, plus `tests/escalates-too-early-or-too-late.md` (12 conversations, "Not yet run"). Incident: links the CFPB page for the too-late side; states "No public incident found" for the too-early side with the searches run.
- **Sources opened (2):** Liu et al., *Time to Transfer*, AAAI-21 (full text; the early/late trade-off quote, the labeling rules, and dataset sizes were checked against the text) and the CFPB report. **Read through search summaries only, not used as facts:** vendor blogs on containment rate (a deployment example of 72.6% containment vs 35.2% AI-resolved was not opened), the EMNLP 2022 handoff paper (downloaded but not read), a practitioner write-up on lateness.
- **Claims left unverified:** none stated as fact beyond the opened sources.
- **Review pass changed:** marked causes as our reading; replaced a vendor figure with the opened paper's own statement of the trade-off.
- **HU-03 Cold transfer: Done.** File: `goals/human-handoff/failures/cold-transfer.md`, plus `tests/cold-transfer.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Sources opened (2 articles):** CMSWire's report on Five9's 2026 CX report and the Liveops blog post on its 2026 Resolution Gap Report. **Original reports not opened.** Both are vendor surveys; the pattern says so and uses them only as evidence the complaint is common. **Not used:** a Zendesk figure and a UJET agent survey (seen only in search summaries); cold/warm transfer definitions from vendor glossaries (summaries).
- **Claims left unverified:** the original Five9 and Liveops question wording.
- **Review pass changed:** added the "vendor survey of perceptions" caveat to each row, marked causes as our reading, and kept the primary metric aligned with the channel-selection family (re-ask under 5%).
- **Part B (daily SEO review):** Blocked: no Chrome tools and no export in `seo/inbox/`; logged in `seo/log.md`.

### Run 11 (scheduled): 2026-10-19 04:17 UTC onward
- **CP-14 Re-asks for known information: Done.** File: `goals/embedded-copilots/failures/re-asks-for-known-information.md`, a new family README, and `tests/re-asks-for-known-information.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Sources opened (3):** the B&T article on Salesforce's connected-customer report (ANZ edition), the Salesforce 2019 news story, and the Digital Applied agent-clarification guide. **Not opened:** the Salesforce reports themselves, ServiceNow's conversation-design page (403).
- **Claims left unverified:** the catalog row's 56% global figure could not be verified and was not used; only the 66% ANZ figure from the B&T article is shown, with its caveats. The edition year of that article is unknown.
- **Review pass changed:** removed a link to a pattern that did not exist yet and replaced it with plain text; added a note that the global repeat figure was not verified.
- **CP-15 Forces a fresh login: Done, flagged E (expert review needed).** File: `goals/embedded-copilots/failures/forces-a-fresh-login.md` with a "Read this first" security note, plus `tests/forces-a-fresh-login.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Sources opened (2):** NIST SP 800-63B-4 AAL page (the reauthentication timeout values were checked against the text) and the Open.cx widget documentation. **Not used:** secondary pages with older NIST values (12 hours / 30 minutes), forum threads.
- **Claims left unverified:** how often the failure occurs (no study found). The risk table and policy are design guidance for a security team to set.
- **Review pass changed:** removed the pre-existing planned-link text from CP-14 now that this page exists; added the NIST caveat that the values are a federal benchmark, not a rule for every product.
- **CP-20 Generic first response: Done.** File: `goals/embedded-copilots/failures/generic-first-response.md`, plus `tests/generic-first-response.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Sources opened (1):** the IceBreaker preprint (arXiv 2604.18375; the ~20% and the per-mille lifts were checked against the text). **Not opened or not usable:** Google's welcome-message guidance (the page redirected to a landing page; only a search summary), vendor blogs with engagement claims (one 40% figure not traceable to a study).
- **Claims left unverified:** none stated as fact beyond the opened paper; the paper is about suggested starters, which the page says.
- **Review pass changed:** replaced a placeholder link with the roadmap link; added the caveat that the preprint is not about support greetings.
- **Part C (content-program task):** not done in this run. The first ready task is 13 (redo the gap analysis); it stays Queued for the next run.

### Run 12 (scheduled): 2026-10-19 05:16 UTC onward
- **CP-08 Missing the obvious intent: Done.** File: `goals/embedded-copilots/failures/missing-the-obvious-intent.md`, plus `tests/missing-the-obvious-intent.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Searches run: 3** (intent-detection benchmarks; clarify-versus-answer research; chatbot misunderstanding surveys). **Sources opened (3):** the Verint 2022 press release, and the abstracts of Zhang et al. (arXiv 2410.13788) and Su and Cardie (arXiv 2605.25284). **Search summaries only, not used as facts:** BANKING77 benchmark figures; a Five9 "46% abandon because the bot misunderstood" figure (the article I opened did not contain it); Cyara and Tidio survey figures.
- **Claims left unverified:** how often plain requests are misread (no study found).
- **Review pass changed:** added the note that the two research rows concern truly ambiguous requests, and a "don't over-correct" line on keeping clarification for those.
- **CP-12 Doesn't say what it can do: Done.** File: `goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md`, plus `tests/doesn-t-say-what-it-can-do.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Searches run: 3** (discoverability and suggested prompts; the Microsoft human-AI guidelines; capability mental models and blank-box research). **Sources opened (3):** NN/g's March 2024 study of new AI users, Amplitude's blog on its chat-box tests, and the abstract of arXiv 2402.08030. **Search summaries only, not used as facts:** the Microsoft human-AI guideline wording (the page I opened did not contain it), the VU capability-communication study, practitioner blogs on onboarding levels.
- **Claims left unverified:** the Amplitude test design and statistics (company's own claims, stated as such).
- **Review pass changed:** added a caveat that one academic study found prompt hints alone made little difference; kept the 2x and retention figures labelled as the company's account.
- **XA-01 Dead-end 'I don't understand' replies: Done.** File: `goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md`, plus `tests/dead-end-i-don-t-understand-replies.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Searches run: 3** (fallback design guidance; repair strategies; banking-chatbot abandonment). **Sources opened (4):** Li et al. CHI 2020 (full text; the 1,685 users, 12 NP types, and three-consecutive-NP sign were checked against the text), Yang et al. CUI 2021 (abstract), Ashktorab et al. CHI 2019 (abstract), and the Mensch und Computer 2024 short paper (abstract). **Not opened, not used:** the 2024 IJHCI abandonment study (1,373 users) and the roadmap row's vendor poll (25.9%); practitioner fallback blogs (summaries).
- **Claims left unverified:** effect sizes of the MuC 2024 study.
- **Review pass changed:** removed the 1,373-user figure and the vendor poll figure, which I had not opened; added the caveat that "three" comes from an observational study.
- **Part B (daily SEO review):** an entry for today already exists in `seo/log.md`; no Search Console data available.
- **Part C (content-program task):** not done in this run; task 13 (redo the gap analysis) stays Queued.

### Run 13 (scheduled): 2026-10-19 06:25 UTC onward
- **CP-01 Help that becomes a sales pitch: Done, flagged L (legal review needed).** File: `goals/embedded-copilots/failures/help-that-becomes-a-sales-pitch.md` with a "Read this first" note, plus `tests/help-that-becomes-a-sales-pitch.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Searches run: 3** (FTC dark-patterns report; ads and sponsored answers in chatbots; upselling in support chats). **Sources opened (3):** arXiv 2409.15436 (abstract and results text), arXiv 2604.08525 (abstract), and a ZwillGen summary of the FTC report. **Not opened:** the FTC staff report itself (403) and three other law-firm summaries (403); only the ZwillGen summary, which is secondary, is used and labelled as such. Vendor upsell guides (summaries only) were not used.
- **Claims left unverified:** nothing is stated about what the law requires.
- **Review pass changed:** removed an author attribution I had guessed for the first paper; replaced a fragile anchor link; added the point that banning all offers hides legitimate options.
- **CP-06 Obstructing cancellation, downgrade, or refund: Done, flagged L (legal review needed).** File: `goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md` with a "Read this first" note, plus `tests/obstructing-cancellation-downgrade-or-refund.md` (12 scenarios, "Not yet run") and the incident page `incidents/ftc-v-amazon-prime-cancellation-settlement.md` (FTC v. Amazon, settled Sept 25, 2025).
- **Searches run: 3** (the Eighth Circuit and the FTC rule; the Amazon settlement; California's renewal law). **Sources opened (4):** the Claims Journal / Bloomberg report on the settlement, the legislative digest of California AB 2863, the Latham & Watkins client alert on the Eighth Circuit ruling, and the ZwillGen summary of the FTC dark-patterns report. **Not opened:** the FTC report, FTC press releases, statute text, Fenwick (403), McGuireWoods (404), eMarketer (403).
- **Claims left unverified:** the AB 2863 effective date (only in a search summary); any development after July 2025 on the click-to-cancel rule. The page states no legal requirement as fact beyond what those sources say, and labels them as summaries.
- **Review pass changed:** removed the "Iliad" nickname and the page counts, which I had seen only in summaries; kept the Amazon figures to what the opened report states; fixed a link to the sales-pitch pattern.
- **CP-03 Answers withheld behind an upgrade, unsaid: Done, flagged L (legal review needed); evidence is thin and says so.** File: `goals/embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md` with a "Read this first" note, plus `tests/answers-withheld-behind-an-upgrade-unsaid.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Searches run: 3** (paywalled or degraded AI answers; FTC deception and disclosure for AI products; Microsoft human-AI guidelines). **Sources opened (3):** the McDonald Hopkins update and the Paubox summary of the FTC's July 2026 proposed policy statement, and the NN/g study (already opened in run 11). **Not opened:** the FTC proposal itself, the Federal Register notice, Mondaq (403), the Microsoft guideline pages (rendered by script, no text).
- **Claims left unverified:** nothing is stated about what the law requires; the FTC material is about a different kind of steering and is cited only for its disclosure principle. No measurement of how common the failure is.
- **Review pass changed:** reworded the comment-period statement to what the source says; replaced a link to an unwritten pattern with a roadmap reference.
- **Flagship patterns written so far: 12 of 30** (HU-01 to HU-03, CP-14, CP-15, CP-20, CP-08, CP-12, XA-01, CP-01, CP-06, CP-03).
- **Deploy (run 13):** content repo merged to `main` as `b12d203` (PR 7). Site repo `main` at `4084a40`, pushed after a clean build: 1,567 sitemap URLs, 0 URLs lost against the live sitemap, 3 added (the three patterns above), and 1 refreshed goal page. **Live check: not deployed.** `/talk-to-a-human-ignored-or-looped/` still returns 404 about 3 hours after the first publish (site commit `99d2fa6`) and 5 minutes after this one; the live sitemap still has 1,553 URLs. No deploy hook variable is set. Not pushed again beyond this commit, per deploy.md. Needs the owner to check Vercel (see the Known gap in deploy.md).
- **Part B (SEO review):** an entry for today exists in `seo/log.md`; Search Console not available.
- **Part C (content-program task):** not done in this run. Task 13 (redo the gap analysis) remains Queued; it has now been skipped in runs 10 to 13 because the pattern work used the time.

### Run 14 (scheduled): 2026-10-19 07:21 UTC onward
- **RS-14 No reply to acknowledgments and closers: Done.** File: `goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md`, `tests/no-reply-to-acknowledgments-and-closers.md` (12 scenarios, "Not yet run"), and the new family README `goals/response-structure/README.md`. Incident: "No public incident found" with the searches run.
- **Searches run: 4** (closing and acknowledgment research; closing sequences and backchannels; "anything else" loops; a targeted search for the robot closings paper). **Sources opened (4):** Uchida, Kameo and Ishiguro, *Scientific Reports* 2024 (abstract and results: 27 participants, likeability p = 0.04); the OpenDialog closing pattern; the Edesy voice-agent post (vendor); and the Microsoft Copilot Studio page, which turned out to be a different page and is not used. **Not opened:** the eScholarship gratitude study (202, no content) and the DOAJ page (403). The roadmap's "ok" conversation-analysis references (Beach 1993; Oloff 2019) were not opened and are not used.
- **Claims left unverified:** nothing about how often chat bots fail on closers. The one experiment is a robot study.
- **Review pass changed:** dropped a Microsoft claim that the opened page did not support; limited the Scientific Reports finding to the likeability result I read in detail.
- **RS-01 Answer buried: Done.** File: `goals/response-structure/failures/answer-buried.md`, `tests/answer-buried.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Searches run: 4** (inverted pyramid and scanning; verbosity and preamble research; answer-first chat design; incident search). **Sources opened (3):** NN/g *Inverted Pyramid* (2018), Nielsen *How Users Read on the Web* (1997; 79% scanned, 16% read word by word; 58%, 47%, 27%, 124% usability), and the YapBench abstract (arXiv 2601.00624). **Not opened:** the length-reward study named in the roadmap (leads only, labeled as such in the page); several vendor UX blogs (not used).
- **Claims left unverified:** no chat study of answer ordering exists in what I found; the NN/g evidence is for web pages.
- **Review pass changed:** checked that the three-change combination in the 1997 test was "concise, scannable, objective"; fixed a relative link to the depth-mismatch pattern.
- **EM-02 Deferring work to the user: Done; evidence is thin and says so.** File: `goals/effort-and-memory/failures/deferring-work-to-the-user.md`, `tests/deferring-work-to-the-user.md` (12 scenarios, "Not yet run"), the new family README `goals/effort-and-memory/README.md`, and the incident page `incidents/openai-gpt-4-turbo-laziness-reports.md` (adjacent case, labeled as such).
- **Searches run: 4** (laziness and placeholders; OpenAI's acknowledgment; customer-service redirection; agents offloading work to users, extended). **Sources opened (2):** CIO Dive, Jan. 25, 2024, and the OpenAI Developer Community thread of Dec. 7, 2023. **Not opened:** OpenAI's own post and X post (403 and not reachable); the 8x8 page quoting Gartner effort figures (429), so no figure from it is used.
- **Claims left unverified:** how often assistants with tools defer work; any root cause for the 2023 and 2024 reports (the source gives none).
- **Review pass changed:** replaced an unsupported statement about OpenAI having "no single explanation" with what the source says; kept the incident labeled adjacent, not a direct match.
- **Part C: Task 13 Done.** `gap-analysis.md` redone: 14 listed sources fetched; 12 read at least at abstract level, 1 not opened (vectara list: no repository access), and 2 added from a second search (GRASP, abstract opened; QiscusCS, summary only). Six first-pass claims corrected or dropped (MAST counts, AdaMAST "fixed catalogs", DGM misalignment warning, governance-paper claim, Hyper-τ-bench figures, vectara star count). Two "nothing found" claims got a second search and both narrowed. The guide (WS-11) is recommended against in generic form, for a person to confirm.
- **Part B (SEO review):** an entry for today exists in `seo/log.md`; Search Console not available.
- **Deploy (run 14):** content repo merged to `main` as `b0c25e9` (PR 8). Site repo `main` at `e85c258`, pushed after a clean build: 1,572 sitemap URLs, 0 URLs lost against the live sitemap (1,553), 19 added (the three new patterns, the 11 earlier unpublished patterns, and the goal pages for effort-and-memory, response-structure, embedded-copilots, and human-handoff, among others). One H1 per page checked; no visible SEO comment. **Live check: not deployed** (the new pages return 404 a few minutes after the push; the live sitemap still has 1,553 URLs; no deploy hook variable is set). Same known gap as run 13; not pushed again. Needs the owner to check Vercel.
- **Flagship patterns written so far: 15 of 30** (HU-01 to HU-03, CP-14, CP-15, CP-20, CP-08, CP-12, XA-01, CP-01, CP-06, CP-03, RS-14, RS-01, EM-02).

### Run 15 (scheduled): 2026-10-19 08:16 UTC onward
- **EM-11 No warning of context loss: Done.** File: `goals/effort-and-memory/failures/no-warning-of-context-loss.md`, `tests/no-warning-of-context-loss.md` (12 scenarios, "Not yet run"), and the incident page `incidents/chatgpt-memory-missing-memories-november-2025.md` (adjacent case, labeled so).
- **Searches run: 3** (ChatGPT memory loss reports; "conversation too long" notices; lost-in-the-middle and multi-turn research). **Sources opened (6):** the OpenAI status page incident (Nov. 6 to 7, 2025), an OpenAI Developer Community thread (Feb. 3, 2025), a Microsoft Community Hub thread (May 2024, first post), and the abstracts of Liu et al. (arXiv 2307.03172) and Laban et al. (arXiv 2505.06120); also TechRadar (says there is no official OpenAI confirmation of a memory-wipe problem; not cited). **Not opened:** the Tom's Guide and Logicc pages; search-summary claims of a February 2025 wipe acknowledged by OpenAI were not supported and are not used.
- **Claims left unverified:** how often products fail to warn; what users were told inside the product during the November 2025 incident.
- **Review pass changed:** dropped a February 2025 "memory wipe" framing that no source supported; labeled the status-page incident adjacent; used only the first post of the Microsoft thread.
- **EM-01 Lazy completion: Done.** File: `goals/effort-and-memory/failures/lazy-completion.md`, `tests/lazy-completion.md` (12 scenarios, "Not yet run"). Incident: the existing page `incidents/openai-gpt-4-turbo-laziness-reports.md`, now also matched to this pattern, with OpenAI's Dec. 8, 2023 post added through Semafor and Gigazine.
- **Searches run: 4** (placeholder code; the winter break hypothesis; partial lists, which returned nothing relevant; LongWriter). **Sources opened (4):** Semafor, Gigazine, CIO Dive (opened in run 14), and the LongWriter abstract (arXiv 2408.07055). **Not opened:** OpenAI's post itself and the Ars Technica article (relayed by the two I opened); a practitioner "full output enforcement" page (connection failed).
- **Claims left unverified:** how often it happens; any cause for the 2023 reports. The winter break effect is stated as contested, and cost as a motive is attributed to Semafor commentary only.
- **Review pass changed:** merged a duplicated related-pattern bullet; reworded the cost explanation to what the source says.
- **DM-03 Corrections not applied: Done.** File: `goals/dialogue-management/failures/corrections-not-applied.md`, `tests/corrections-not-applied.md` (12 scenarios, "Not yet run"), and the new family README `goals/dialogue-management/README.md`. Incident: "No public incident found" with the searches run.
- **Searches run: 3** (dialogue state tracking and corrections; sycophancy under challenge; voice or booking bots using a wrong date). **Sources opened (4):** abstracts of Sun et al. (IJCAI 2022), Kim et al. (ACL 2020, SOM-DST), Laban et al. (FlipFlop, arXiv 2311.08596), and TRUTH DECAY (arXiv 2503.11656; no figures used). **Not opened:** two Vapi forum threads (script-rendered page; security checkpoint).
- **Claims left unverified:** how often live products fail corrections.
- **Review pass changed:** checked every author attribution against the arXiv pages; bounded the fix with the FlipFlop result so it does not teach the bot to accept every challenge.
- **Part C: Task 13b Done.** New file `agent-type-gap-analysis.md` for six agent types: 6 searches and the abstract pages (or PDF text for τ-bench) of 16 papers plus the OWASP press release opened. Summary-only items are marked, and the Hyper-τ-bench and GPT-4o figures from blog write-ups are not used.
- **Part B (SEO review):** an entry for today exists in `seo/log.md`; Search Console not available.
- **Deploy (run 15):** content repo merged to `main` as `26e345d` (PR 9). Site repo `main` at `ebcb2b2`, pushed after a clean build: 1,576 sitemap URLs, 0 URLs lost against the live sitemap (1,553), 23 added (the three new patterns, the pages from runs 13 and 14 still unpublished live, and goal pages including dialogue-management). One H1 per page checked; no visible SEO comment. **Live check: not deployed** (`/answer-buried/` and `/lazy-completion/` return 404; the live sitemap still has 1,553 URLs; no deploy hook variable is set). Same known gap as runs 13 and 14. Needs the owner to check Vercel.
- **Flagship patterns written so far: 18 of 30** (HU-01 to HU-03, CP-14, CP-15, CP-20, CP-08, CP-12, XA-01, CP-01, CP-06, CP-03, RS-14, RS-01, EM-02, EM-11, EM-01, DM-03).

### Run 16 (scheduled): 2026-10-19 09:16 UTC onward
- **DM-09 Guessing instead of asking: Done.** File: `goals/dialogue-management/failures/guessing-instead-of-asking.md`, `tests/guessing-instead-of-asking.md` (12 scenarios, "Not yet run"). Incident: "No public incident found" with the searches run.
- **Searches run: 3** (LLMs and clarifying questions; user studies on how many questions are too many; wrong-intent guesses in customer service). **Sources opened (5):** abstracts of CLAMBER (ACL 2024), Zou et al. (CIKM 2020), Zou et al. (ACM TOIS 2023), the *Ask or Recommend* study (CIKM '24), and Lautraite et al. (arXiv 2110.15235; opened, not cited). **Not opened:** vendor and practitioner pages on intent thresholds (not used).
- **Claims left unverified:** no study of ask versus guess in live support; the studies are search and shopping tasks and are labeled that way.
- **Review pass changed:** kept the 11 to 21 question figure as a different-task outer limit, not a target; named only authors and venues I had read.
- **RF-01 Over-refusal of ordinary requests: Done.** File: `goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md`, `tests/over-refusal-of-ordinary-requests.md`, new family README `goals/refusals-and-boundaries/README.md`, and the incident page `incidents/virgin-money-chatbot-flags-own-brand-name.md`.
- **Searches run: 4** (XSTest; OR-Bench; bank chatbot refusals; the Virgin Money case). **Sources opened (5):** the XSTest and OR-Bench abstracts, Fortune (Jan. 30, 2025), CX Today, and a Vibe Graveyard summary (not cited). **Not opened:** the benchmark papers' result tables; a safety-over-refusal correlation figure seen only in a search summary is not used.
- **Claims left unverified:** how often live products over-refuse; the cause of the Virgin Money reply (the bank says it was more than a single-word block).
- **Review pass changed:** relabeled the incident as an older basic filter, not an LLM; replaced a health-dosage test scenario with a neutral security one so no expert review is needed.
- **RF-02 Refusal with no reason or next step: Done.** File: `goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md`, `tests/refusal-with-no-reason-or-next-step.md`. Incident: the Virgin Money page, now also matched to this pattern.
- **Searches run: 3** (user perceptions of refusal styles; OpenAI Model Spec refusal wording; Anthropic guidance on declining), the last two returning only secondary material. **Sources opened (3):** abstracts of *Let Them Down Easy!* (EMNLP 2025), Nahar et al. (arXiv 2609.16191), and *The Art of Saying No* (NeurIPS 2024). **Not opened:** the Model Spec and Anthropic's published guidance (not reached; none used).
- **Claims left unverified:** no live-product test of refusal templates. Per-strategy figures from a search summary (including satisfaction scores) are not used.
- **Review pass changed:** limited the explanation finding to the abstract's wording (helps infrequent refusals, not frequent ones); added a cause-specific rule.
- **Part C: Task 13c Done.** `roadmap/l1-harness-decision.md`: a proposed decision (framework-neutral spec, borrowing the τ-bench evaluation shape and the cookbook and GRASP designs), from abstracts and pages I opened; marked for a person to confirm.
- **Part B (SEO review):** an entry for today exists in `seo/log.md`; Search Console not available.
- **Deploy (run 16):** content repo merged to `main` as `f5c7780` (PR 10). Site repo `main` pushed after a clean build: 1,580 sitemap URLs, 0 URLs lost against the live sitemap (1,553), 27 added (the three new patterns, earlier unpublished ones, and goal pages including refusals-and-boundaries). One H1 per page checked; no visible SEO comment. **Live check: not deployed** (pages return 404; the live sitemap still has 1,553 URLs; no deploy hook variable is set). Same known gap as runs 13 to 15. Needs the owner to check Vercel.
- **Flagship patterns written so far: 21 of 30** (the 18 from run 15, plus DM-09, RF-01, RF-02).

### Run 17 (scheduled): 2026-10-19 10:16 UTC onward
- **TE-01 Generic error messages: Done.** File: `goals/errors-and-recovery/failures/generic-error-messages.md`, `tests/generic-error-messages.md` (12 scenarios, "Not yet run"), new family README `goals/errors-and-recovery/README.md`. Incident: "No public incident found" with the searches run.
- **Searches run: 3** (NN/g error-message guidelines; generic versus specific error studies; chatbot "something went wrong" incidents). **Sources opened (4):** NN/g *Error-Message Guidelines* (2023), Baymard (Dec. 2023, first part), the German UPA guideline (contents and foreword), and an OpenAI Developer Community thread (Aug. 2024). **Not opened:** the 2000 Rimmer and Ozchi web-error-page paper (bot check) and outage news pieces (read through a search summary only; not used).
- **Claims left unverified:** how often chat products show generic errors; any controlled comparison in chat.
- **Review pass changed:** stated the Baymard 98% finding as it appears (messages not targeted at the exact problem); dropped the claim that any outage was a sourced incident about message text.
- **TE-06 Confident wrong answer with no way to check: Done.** File: `goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md`, `tests/confident-wrong-answer-with-no-way-to-check.md`. Incident: the site's existing Air Canada page, linked by URL.
- **Searches run: 3** (uncertainty expression and reliance; the Air Canada ruling; citations and trust). **Sources opened (4):** abstracts of Kim et al. (FAccT 2024), Ding et al. (AAAI 2025), and Liu et al. (EMNLP Findings 2023), and the site's Air Canada incident page (plus the CTV headline and date). **Not opened:** the CanLII ruling (403); a blog claim about hedging and internal confidence, not used.
- **Claims left unverified:** how often live support bots are confidently wrong; whether any confidence display reduces wrong actions in production.
- **Review pass changed:** noted that a citation raised trust even when random, so the fix requires checking support; labeled the tribunal case as a small-claims decision and added no legal statement.
- **GS-01 Eligibility answers sound like decisions: Done, flagged L and E (legal and expert review needed).** File: `goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md` with a "Read this first" note, `tests/eligibility-answers-sound-like-decisions.md` (12 scenarios, "Not yet run"), and the new family README `goals/government-service-agents/README.md`. Incident: the site's NYC MyCity page, labeled adjacent.
- **Searches run: 3** (benefits chatbot accuracy and disclaimers; the NYC MyCity coverage; GOV.UK Chat findings). **Sources opened (4):** the GDS blog on the first GOV.UK Chat experiment, the abstract of Gosciak et al. (arXiv 2603.11213), the Beeck Center Policy2Code summary, and The Markup article (partly). **Not opened:** later GOV.UK Chat pilot reports (press only), Services Australia and Canadian guidance (not found), and any statute or agency rule.
- **Claims left unverified:** how applicants act after a chatbot "no"; any program rule, deadline, or appeal right (none is stated; the page links agency pages instead).
- **Review pass changed:** removed a statement that income limits update each year; reworded the NYC bot description to what the article text I read supports; kept all legal rights out of the fix.
- **Part C: Task 13d Done.** `roadmap/l0-base-spec.md`: a draft table of 24 behaviors with their patterns, tests, and metrics, built from the pattern pages' principle lines, with five tensions for a person to decide. Untested, for review.
- **Part B (SEO review):** an entry for today exists in `seo/log.md`; Search Console not available.
- **Deploy (run 17):** content repo merged to `main` as `1682d61` (PR 11). Site repo `main` pushed after a clean build: 1,585 sitemap URLs, 0 URLs lost against the live sitemap (1,553), 32 added (the three new patterns, earlier unpublished ones, and goal pages including errors-and-recovery and government-service-agents). One H1 per page checked; no visible SEO comment. **Live check: not deployed** (pages return 404; the live sitemap still has 1,553 URLs; no deploy hook variable is set). Same known gap as runs 13 to 16. Needs the owner to check Vercel.
- **Flagship patterns written so far: 24 of 30** (the 21 from run 16, plus TE-01, TE-06, GS-01).

## Backlog (not scheduled)
Ideas from earlier lists that were never chosen. They stay out of the queue until someone adds them.

AI-written help content in knowledge bases · agents using other agents' tools (user-facing side) · email and calendar agents (now partly PA) · document and spreadsheet copilots · workplace monitoring through copilots · shopping honesty (stale prices, affiliate bias) · outbound AI sales at scale · elder-care assistants · household and family assistants · digital twins and cloned voices of real people · video and avatar service agents · "know your agent" identity · AI-generated reviews · scammers impersonating your support · assistant marketplaces · invisible model routing · memory shared across products · apps inside assistants · jurisdiction-aware behaviour (state-by-state rules) · transcript mining and privacy · smart glasses and AR overlays · robots and embodied assistants · live camera and screen sharing · game characters and creative companions

## Schedule
| Item | Value |
|---|---|
| Status | **Active** from 2026-10-18 (credits reset). Merged to main in PR #4. Runs append to the Run log below. |
| Scheduled task name | `HMI roadmap: patterns and content program every hour` |
| Task id | `trig_01J1rwvuKcpXBGmKkkRfihF7` |
| Created | 2026-10-14 19:05 UTC |
| Cron (UTC) | `16 * * * *`, so runs start at minute 16 of every hour (changed from every 5 hours on 2026-10-18) |
| First run | 2026-10-18 19:16 UTC (hourly schedule) |
| Where it fires | Into the same session that created it, so the run has the repository checkout and tools |
| To pause or stop | Ask the session to disable the task, or call the scheduled-task update tool with `enabled=false` for the id above. The queue keeps its place, so re-enabling resumes where it stopped. |
