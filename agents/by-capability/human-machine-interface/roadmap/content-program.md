# Content Program: Fifteen Workstreams Run Alongside the Pattern Queue

> **What this is.** Besides writing patterns, each scheduled run does **one** task from this file. The tasks turn a catalog into something people cite and use: tiered quality, real incidents, runnable tests, an honest "will a better model fix this?" answer, and entry points by symptom and by role. Everything stays inside `agents/by-capability/human-machine-interface/`. The [execution plan](execution-plan.md) says how a run works.

## Site compatibility
**Two repositories.** This repo holds content only; the Astro site and its importers live in `sarkars/agent-kb-autopublish`. Anything that needs a change there goes to `roadmap/merge-proposals.md`. See [REPOSITORIES.md](../../../../REPOSITORIES.md).

The published site is Astro, fed by an importer that reads this repo. Keep these true or pages vanish or lose their goal and category:
- Written patterns live at `goals/<family>/failures/<name>.md`, with `goals/<family>/README.md` present.
- Line 1 of a pattern is its H1. It also has a `**Frequency**: Very Common|Common|Occasional|Rare` line and a `## Issue: <one sentence>` line.
- Run `python3 -I agents/by-capability/human-machine-interface/roadmap/tools/check_site_compat.py` with the other checks. It must pass before every commit.
- **Existing public URLs must not change** (Google has indexed them). Never move, rename, or delete a pattern file, or a goal or category folder, outside the HMI folder. `check_public_urls.py` compares against `roadmap/tools/public-urls.tsv`, a frozen list of the 1,267 patterns, goals, and categories on the live site, and fails on any change. HMI pages are exempt and may change, but keep their URLs stable too unless there is a reason.
- Incident pages use the site's incident front matter.

## Rules for every task
- **No invented evidence.** Cite only what you opened. Never write test results, incidents, quotations, or mappings you did not verify. If you can't, write "Not yet run", "No public incident found", or leave the task *Blocked* with the reason.
- **Link only to what exists.** Entry pages (symptoms, roles, glossary) link only to patterns marked **Written**. A page with fewer than three links to written patterns waits.
- **Nothing outside this folder.** Merges, redirects, or edits to older patterns go into `roadmap/merge-proposals.md` as proposals. A person approves them.
- **Human review is required** for mappings to outside frameworks and for any statement about law. These stay *Needs review*.
- Run `rebuild_summary.py` and `check_links.py` and fix every problem before committing.

## Maturity labels (workstream 1)
| Label | Meaning | Who or what can set it |
|---|---|---|
| Researched | Passed the plan's Definition of done | A scheduled run |
| Tests written | Flagship only: the test file exists; results say "Not yet run" | A scheduled run |
| Tested | The tests were run against named models and versions; results recorded with the date | A person or an automated harness, with the run recorded |
| Verified | A named subject-matter reviewer checked it | A person |

## The 30 flagship patterns
These come first in the queue, at 3 per run. They were picked for customer demand, legal or reputational weight, and the chance of a real public incident, not for queue order. Flagships carry the extra items in the Definition of done: an incident, a test file, and a maturity label.

| # | ID | Pattern |
|---|---|---|
| 1 | HU-01 | 'Talk to a human' ignored or looped |
| 2 | HU-02 | Escalates too early, or too late |
| 3 | HU-03 | Cold transfer |
| 4 | CP-14 | Re-asks for known information |
| 5 | CP-15 | Forces a fresh login |
| 6 | CP-20 | Generic first response |
| 7 | CP-08 | Missing the obvious intent |
| 8 | CP-12 | Doesn't say what it can do |
| 9 | XA-01 | Dead-end 'I don't understand' replies |
| 10 | CP-01 | Help that becomes a sales pitch |
| 11 | CP-06 | Obstructing cancellation, downgrade, or refund |
| 12 | CP-03 | Answers withheld behind an upgrade, unsaid |
| 13 | RS-14 | No reply to acknowledgments and closers |
| 14 | RS-01 | Answer buried |
| 15 | EM-02 | Deferring work to the user |
| 16 | EM-11 | No warning of context loss |
| 17 | EM-01 | Lazy completion |
| 18 | DM-03 | Corrections not applied |
| 19 | DM-09 | Guessing instead of asking |
| 20 | RF-01 | Over-refusal of ordinary requests |
| 21 | RF-02 | Refusal with no reason or next step |
| 22 | TE-01 | Generic error messages |
| 23 | TE-06 | Confident wrong answer with no way to check |
| 24 | GS-01 | Eligibility answers sound like decisions |
| 25 | DT-01 | Order mix-ups at the speaker |
| 26 | VO-05 | Repair failure |
| 27 | RT-02 | Silent long-running work |
| 28 | RT-06 | Silent failure and timeout |
| 29 | CC-08 | Scam victim not interrupted |
| 30 | CC-16 | Romantic or parasocial dependence |

## The fifteen workstreams
| ID | Workstream | Deliverable | When a run does it |
|---|---|---|---|
| WS-01 | Two tiers, labeled | Maturity label and tier on every written pattern; this file's flagship list | Set up now. Each run labels its own patterns |
| WS-02 | Incident anchoring | `incidents/<slug>.md` in the site's incident format ([README](../incidents/)); check the site's existing incidents first and link to them | Alongside each flagship, plus one standalone task per week when ready |
| WS-03 | Tested fixes | `tests/<pattern>.md` per flagship in the `tests/README.md` format | Alongside each flagship |
| WS-04 | "Will a better model fix this?" | A header row on every pattern, from the catalog column, marked "our judgment" or "tested" | Every pattern |
| WS-05 | Symptom-first entry pages | `symptoms/<slug>.md`: a three-question diagnosis ending at written patterns | When three or more written patterns share a symptom |
| WS-06 | Fewer, stronger pages | `roadmap/merge-proposals.md`: duplicate or overlapping pages and what to keep | One proposal task per ten patterns written |
| WS-07 | Original data | `data/` process and template; accepted anonymized submissions summarized in the Run log | Set up once; check for submissions each run |
| WS-08 | Role-based starting points | `start-here/<role>.md` for product leads, engineers, CX leaders, and compliance | When each role has at least five written patterns, then refresh every ten |
| WS-09 | Definition pages | `glossary/<term>.md`: short, sourced definitions linking to patterns | One term per run when a term is used by three or more written patterns |
| WS-12 | Base agent and learning loop | The end state in [learning-agent.md](learning-agent.md): L0 base spec, L1 base agent design, and the gated learning loop's policy, all labeled untested until a person runs them. Built on the [gap analysis](gap-analysis.md) | Gap analysis redo first; then one level at a time |
| WS-13 | Use-case agent specs | One page per specific agent in `agents/by-agent/use-cases/`: scope, business goals with measure, failure definition, severity, hand-over triggers, and linked failures to test. Eight exist as first drafts | Add a spec when a use case has at least three documented failures; revise each with a practitioner's input |
| WS-14 | Solutions: chat use cases | One independent Markdown page, [agents/solutions/chat-use-cases.md](../../../solutions/chat-use-cases.md), that explains 32 narrow chat use cases end to end: goals, instructions, guardrails, evals, and the existing failure patterns to test against, each with a metric and a counter-metric. Markdown only; no interactive pages | Verify usage evidence first, then deepen one use case per task in priority-wave order |
| WS-10 | Cross-framework mappings | `mappings/proposals.md`: OWASP, NIST, and MITRE entries for flagships, each with a source you opened and a confidence label | Flagships only, after the pattern is Done; always *Needs review* |
| WS-15 | SEO from search data | Daily review of Search Console queries and pages (Chrome, or an export in `seo/inbox/`), logged in [seo/log.md](seo/log.md); title, summary, and internal-link fixes; queries with no page become queue rows. Rules in [seo/README.md](seo/README.md) | Once per UTC day, before the other content task |
| WS-11 | Build guide | `guide/`: a failure-first guide to building a customer-facing agent that doesn't fail people. A gap analysis first, then one step per task, each linking only written patterns | Gap analysis first; then one step when its condition is met |

## Task queue
**Order:** flagship patterns come first (Part A of every run). Among tasks, roadmap tasks (13 to 17) come first, then tasks tied to written flagships (5 to 12 and 24), then the chat use-case tasks (14a to 14j). **Daily SEO review (WS-15):** the first run of each UTC day does it before the queue task, if `seo/log.md` has no entry for today. It is not a queue row.

Status values: *Queued*, *In progress*, *Done*, *Blocked*, *Needs review*. A run takes the first row that is *Queued* or *In progress* and whose condition is met.

| # | Task | Workstream | Condition | Status |
|---|---|---|---|---|
| 1 | Write `tests/README.md`: the test-file format (conversation, expected behavior, pass/fail rubric, results table) | WS-03 | None | Done |
| 2 | Write `incidents/README.md`: the incident-page format and the source rules | WS-02 | None | Done |
| 3 | Write `data/README.md` and `data/failure-report-template.md`: consent, anonymization, what never to submit | WS-07 | None | Done |
| 4 | Add Maturity and "Will a better model fix this?" rows to the pattern template | WS-01, WS-04 | None | Done |
| 13 | Redo `roadmap/gap-analysis.md` properly: open every source it lists, correct any claim the source doesn't support, mark each row opened or summary-only, and add a second search for each "nothing found" claim. Decide whether a guide (WS-11) is still worth writing | WS-11, WS-12 | None | Done (run 14); see the second-pass status line in the file |
| 13b | Per-agent-type gap analysis for the six most-built agent types: customer service, coding, research and data, workflow automation, IT and security, and copilots. For each, open the main failure and benchmark references and record what they cover, what they leave out, and what the library adds | WS-12 | Task 13 Done | Done (run 15); see [agent-type-gap-analysis.md](agent-type-gap-analysis.md) |
| 13c | Decision record: build the L1 base agent on an existing harness (tau2-bench, the OpenAI cookbook loop) or from scratch, with reasons from opened sources | WS-12 | Task 13b Done | Queued |
| 13d | L0 base spec from the Done flagships' fixes | WS-12 | 10 flagships Done | Queued |
| 13e | L1 base agent design: prompt, tool contracts, handoff and refusal rules, test cases; label everything untested | WS-12 | Task 13d Done | Queued |
| 13f | Learning-loop policy (L2 to L4) with each rule checked against an opened source, and the candidate-registry format | WS-12 | Task 13c Done | Queued |
| 14 | Guide outline: the steps, what each decides, and the patterns each links; no prose beyond a sentence per step | WS-11 | Task 13 Done and says a guide is worth writing | Queued |
| 15 | Write one guide step: what to decide, the minimal fix, the patterns it prevents, the tests, and when you can skip it | WS-11 | Outline Done and the step has at least two written patterns it can link; repeat per step | Queued |
| 16 | Review the eight use-case specs in `agents/by-agent/use-cases/`: open sources for every metric name and definition, remove anything unsupported, and list which definitions need a practitioner's review | WS-13 | None | Queued |
| 17 | Add the next use-case agent specs (candidates: candidate screening, voice appointment scheduling, e-commerce order support, internal knowledge assistant), each with at least three documented failures behind it | WS-13 | Task 16 Done | Queued |
| 5 | Incident page: pick the best-sourced public case for the first flagship that has one | WS-02 | A flagship is Done | Queued |
| 6 | Seed `glossary/`: "containment rate" and "cold transfer" | WS-09 | HU-01 and HU-03 Done | Queued |
| 7 | First symptom page: "The bot keeps asking what I already told it" | WS-05 | CP-14 Done and two more related patterns Done | Queued |
| 8 | First merge proposal covering the written HMI patterns and their older-library neighbors | WS-06 | 10 patterns written | Queued |
| 9 | First role page: `start-here/cx-leaders.md` | WS-08 | 5 written patterns relevant to CX leaders | Queued |
| 10 | First mapping proposal for the first Done flagship | WS-10 | A flagship is Done | Queued |
| 11 | Seed `symptoms/` with the next 3 pages | WS-05 | 9 patterns written | Queued |
| 12 | Add terms to `glossary/` until 10 exist | WS-09 | Repeat as terms qualify | Queued |
| 24 | Repeat: merge proposals, role pages, mapping proposals as their conditions are met | WS-06, WS-08, WS-10 | As conditions are met | Queued |
| 14a | **Verify market usage.** Open every source in section 1 of [chat-use-cases.md](../../../solutions/chat-use-cases.md): confirm each figure and its grade, replace grade C claims with better sources where they exist, and record use cases with no evidence. Correct the page | WS-14 | None | Queued |
| 14b | **Deepen CU-27 (information-seeking assistant)** in place: research it, then write its full end-to-end section (use-case-specific instructions, guardrails, evals, each with a metric and counter-metric). Link only to existing failure patterns. Mark everything untested | WS-14 | Task 14a Done | Queued |
| 14c | **Deepen CU-02 (e-commerce order support)** the same way | WS-14 | Task 14b Done | Queued |
| 14d | **Adversarial review of 14b and 14c:** is each metric measurable from logs, an eval, or sampled review? Does each item have a counter-metric? Is anything claimed that is not sourced? Fix the page structure if it fails | WS-14 | Task 14c Done | Queued |
| 14e | **Deepen wave 1**, one use case per task: CU-26, CU-28, CU-32, CU-30 (CU-30 carries legal and expert flags and stays *Needs review*) | WS-14 | Task 14d Done | Queued |
| 14f | **Deepen wave 2**, one per task: CU-29, CU-31, CU-07, CU-15, CU-16, CU-17, CU-05, CU-04, CU-01 | WS-14 | Three wave 1 use cases Done | Queued |
| 14g | **Deepen wave 3**, one per task, as *Needs review*, with instruction text withheld: CU-21, CU-20, CU-22, CU-23, CU-24, CU-25 | WS-14 | Task 14d Done and two wave 2 use cases Done | Queued |
| 14h | **Wave 4:** for each use case with no usage evidence, look for evidence; keep it only if some is found or a judgment reason is written. Add use cases the evidence shows are missing | WS-14 | Task 14a Done | Queued |
| 14i | **Link new patterns:** when a failure pattern is written that a use case needs, link it and remove the "none documented yet" note | WS-14 | A pattern is Done | Queued |
| 14j | **Refresh market usage** every 20 runs: search for new usage studies, update section 1, and record what changed | WS-14 | Task 14a Done | Queued |

## Guide rules (workstream 11)
- **Failure-first, not architecture-first.** The guide covers what to decide so the failures in this library don't happen. It does not re-teach general agent architecture; it links to the original sources for that.
- **Primary sources for every recommendation that isn't a pattern.** Open them. Where practice is only our judgment, say so.
- **Every step links to written patterns and test files,** and each step says when it can be skipped.
- **Short.** A step is a page a team can act on in an afternoon. If a step needs more, it becomes a pattern.
- **Maintained.** Each step has a last-reviewed date. Frameworks change fast, so avoid framework-specific code unless it is tested.
- **No claim that following the guide guarantees good behavior.** The guide reduces known failures; only testing shows whether a given agent has them.

## Chat use-case solution rules (workstream 14)
- **Markdown only.** No interactive pages, data files, or build scripts. Everything is a Markdown file.
- **Solution pages are independent and link only to existing failure patterns,** other solution pages, or the solutions README. `check_solutions.py` enforces this.
- **Every instruction, guardrail, and eval has a metric, how it is measured, and a counter-metric.** No invented thresholds: write "set from your baseline" unless a law or published benchmark gives a number, and cite it.
- **Usage first.** Do not deepen a use case until its usage evidence in section 1 has been verified by opening the source, or is labeled as judgment. Waves weigh usage evidence with stakes.
- **Untested means untested.** Instructions, guardrails, and evals are drafts until a recorded run exists. Never write results you did not obtain.
- **Tier C is gated.** Instruction text for emotional support, companions, children, older adults, grief, and role-play stays withheld until a qualified reviewer has checked it.

## What these runs cannot do
- **Run the tests.** The scheduled run has no model-evaluation harness. It writes the tests and leaves "Not yet run". Someone has to run them and record results before any pattern can be *Tested*.
- **Collect original data.** Submissions have to come from readers. Without them, WS-07 produces a process and nothing else.
- **Approve mappings, law, or merges.** A person does.
- **Change the website.** This file covers content only. Site features are separate work.
