# Developer Search Plan

> **Decision, 2026-10-19:** the audience is **developers** (people building or running chatbots and AI agents). This plan replaces the earlier consumer-oriented alignment in [content-alignment.md](content-alignment.md); that file and [queries.md](queries.md) stay as a record. The plan uses two real sources: the site's own Search Console export for the last three months (exported 2026-10-19), and Google autocomplete suggestions for developer phrases (pulled 2026-10-19). Neither source gives search volume for new pages; autocomplete shows only that a phrase is common enough to be suggested.

## 1. What Search Console says about the site today
Source: the Performance report for agent-kb-autopublish.vercel.app, search type Web, last three months (July 23 to October 17, 2026).

| Measure | Value |
|---|---|
| Impressions | 8,838 |
| Clicks | 21 (a click-through rate of about 0.24%) |
| Average position | about 16 (daily averages ranged from about 6 to 55) |
| Devices | desktop 7,954 impressions and 17 clicks; mobile 848 and 4 |
| Top countries by impressions | United States 4,019; India 772; United Kingdom 305; Brazil 296; Philippines 208 |
| Trend | impressions ran about 40 to 140 a day in July and August, then 150 to 290 a day from late September; the last few days fell |

What this tells us:
- **The site gets impressions, almost no clicks.** The pages that already show up rank at positions 5 to 12 yet draw about zero clicks, so the first lever is what searchers see (title, description, opening), not new pages.
- **The audience already looks like developers:** desktop-heavy, and the pages that appear are engineering failure topics, not consumer questions.
- **None of the new human-machine-interface pages appear yet.** They have not been published to the live site (the build has not deployed), so nothing here measures them.
- **The query table is partial.** It lists 293 queries covering about 1,224 of the 8,838 impressions; Search Console withholds rare queries. No listed query has a click.
- **Many listed queries are long, exam-style questions** (for example "which context failure detection strategy involves running the same query twice with slightly different phrasing…"). I do not know who or what sends them; I note it and draw no conclusion.

### Pages already earning impressions (older library pages, outside the human-machine-interface folder)
| Page | Impressions | Clicks | Position |
|---|---|---|---|
| /patterns/ (the index) | 2,048 | 1 | 6.8 |
| /handoff-timing-mismatch/ | 235 | 0 | 6.0 |
| /approval-timeout-mishandling/ | 193 | 0 | 11.0 |
| /webhook-delivery-guarantee-not-enforced/ | 152 | 0 | 11.7 |
| /goals/voice-synthesis/ | 112 | 0 | 18.3 |
| /atypical-presentation-blindness/ | 111 | 0 | 8.9 |
| /multi-agent-handoff-drops-override-flag-between-deploy-and-rollback-agent/ | 99 | 0 | 5.0 |
| /conflicting-instructions/ | 88 | 1 | 5.4 |
| /state-machine-violation/, /circuit-breaker-false-positive/, /stale-state-use/, /rolling-window-quota-misunderstanding/ | 50 to 77 each | 0 | 6.6 to 8.8 |

## 2. Developer queries and the content that answers them
All quoted queries are Google autocomplete suggestions as returned. "Fit" rates how well our existing content answers the likely intent (Strong: we hold researched material; Partial: we hold part; none rated Weak here).

| # | Topic | Real suggestions | Our content | What the page would be, and what is missing | Fit |
|---|---|---|---|---|---|
| 1 | Chatbot-to-human handoff | "chatbot human handoff", "chatbot to human handoff", "ai agent escalation" | [Talk to a human ignored or looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md), [When a bot should hand off](../../goals/human-handoff/failures/escalates-too-early-or-too-late.md), [Cold transfer](../../goals/human-handoff/failures/cold-transfer.md) | Guide with the trigger table, the handoff summary schema, and test scenarios; the older site page /handoff-timing-mismatch/ already has 235 impressions at position 6.0 and no clicks | **Strong** |
| 2 | Chatbot fallback message | "chatbot fallback message", "chatbot fallback rate" | [Dead-end "I don't understand" replies](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | Reference page: fallback ladder, example messages, the metric, and 12 test scenarios | **Strong** |
| 3 | Chatbot error handling and error messages | "chatbot error handling", "chatbot error message" | [Generic error messages](../../goals/errors-and-recovery/failures/generic-error-messages.md), [Silent long-running work](../../goals/response-time/failures/silent-long-running-work.md) | Guide: error classes, message template, what to say about saved state | **Strong** |
| 4 | Human in the loop for AI agents (approval and escalation) | "ai agent human in the loop", "ai agent human approval", "agentic human in the loop" | [When a bot should hand off](../../goals/human-handoff/failures/escalates-too-early-or-too-late.md), [Confident wrong answer with no way to check](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md); site page /approval-timeout-mishandling/ (193 impressions, position 11.0) | The approval half is covered by the older site page; our added angle is when to ask a person and what to show them | **Partial** |
| 5 | LLM clarifying questions | "llm clarifying questions", "llm ask clarifying questions" | [Guessing instead of asking](../../goals/dialogue-management/failures/guessing-instead-of-asking.md) | Guide with the ask-or-answer rule and CLAMBER and user-study evidence | **Strong** |
| 6 | LLM confidence score and calibration | "llm confidence score", "llm confidence calibration", "agentic confidence calibration" | [Confident wrong answer with no way to check](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) | Our angle is what the user sees; calibration methods themselves are not covered and are well served elsewhere | **Partial** |
| 7 | Chatbot testing checklist and scenarios | "chatbot testing checklist", "chatbot testing scenarios", "chatbot testing framework" | The 27 test files (12 scenarios each, rubrics) and the [L1 base agent test cases](../l1-base-agent-design.md) | A single checklist page built from the test files; unique to this library; scenarios are untested designs and must say so | **Strong** |
| 8 | LLM and AI agent timeouts | "llm timeout", "ai agent timeout", "llm request timeout" | [Silent long-running work](../../goals/response-time/failures/silent-long-running-work.md), [Generic error messages](../../goals/errors-and-recovery/failures/generic-error-messages.md); site page /integration-timeout-mismatch/ (50 impressions, position 15.1) | We cover what the user sees during a wait; engineering timeout settings per framework are not covered | **Partial** |
| 9 | LLM context window degradation and chatbot memory | "llm context window degradation", "chatbot memory management", "chatbot context window" | [No warning of context loss](../../goals/effort-and-memory/failures/no-warning-of-context-loss.md) | Research is cited (lost in the middle); notice design is ours; memory architecture is not covered | **Partial** |
| 10 | AI agent failure modes | "ai agent failure modes", "llm agent failure modes", "agentic ai failure modes" | [Gap analysis](../gap-analysis.md), [agent-type gap analysis](../agent-type-gap-analysis.md), the library's patterns | Competitive (MAST and others); our angle is human-facing failures plus tests; a hub page linking the pattern families | **Partial** |
| 11 | How to test an AI agent | "how to test an ai agent", "how to evaluate an ai agent", "ai agent testing framework" | [L1 base agent design](../l1-base-agent-design.md), [L0 base spec](../l0-base-spec.md), the test files | Hub page on behavior tests; competitive; our test scenarios are designs, not results | **Partial** |

## 3. What to do, in order
1. **Fix what searchers see on pages that already rank.** Rewrite title, meta description, and the first two sentences of the older pages in section 1, so each answers its likely query directly. Expected effect: more clicks at the same position. **These pages are outside the human-machine-interface folder, so I need your go-ahead to edit them** (or I write the proposed text into the merge-proposals file for you to apply). The /patterns/ index alone has 2,048 impressions.
2. **Retitle the written human-machine-interface patterns for developer phrases** (no address changes). For example, "Dead-End Replies" becomes a page about the chatbot fallback message. Rows 1 to 9 above name the target phrase for each.
3. **Build three or four developer guides from existing material** instead of more patterns: the chatbot handoff guide (row 1), the chatbot testing checklist (row 7), chatbot error handling (row 3), and the AI agent failure-modes hub (row 10). Each carries its query evidence.
4. **Get the pages live.** Nothing from this library can rank until the site builds and deploys; every publish so far has built cleanly but not deployed.
5. **Measure.** Re-export Search Console after two weeks and compare impressions, position, and clicks on the changed pages. Log the result in the SEO log.

## 4. What this plan does not claim
- Volumes: the suggestions are not search counts, and Search Console shows impressions only for pages that already exist.
- That any change will raise rankings or clicks.
- Anything about queries Search Console withheld.

## Related
- [Search queries (consumer-oriented, set aside)](queries.md) · [Content alignment (consumer, set aside)](content-alignment.md) · [SEO README](README.md) · [SEO log](log.md)
