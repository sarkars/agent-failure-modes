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


## 2b. Second pull: more developer queries (1,394 suggestion requests, 76 seeds)
Pulled 2026-10-19 from the same suggestion endpoint, with seeds covering testing, metrics, handoff, fallback, errors, timeouts, context, memory, hallucination, citations, confidence, refusals, voice, and agent failures. Many phrasings I tried returned nothing (for example "how to hand off chatbot to human agent", "when to escalate chatbot to human", "chatbot user correction", "llm forgets earlier messages"), which means searchers use shorter, topic-style phrases. Some seeds also returned unrelated meanings ("llm" as a law degree), which I dropped. The rows below quote suggestions exactly as returned.

### A. Testing and evaluation
*Highest fit: our 27 test files and rubrics.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| chatbot test cases, test scenarios, how to evaluate a chatbot | "chatbot test cases", "chatbot test scenarios", "test scenarios for chatbot", "how to evaluate a chatbot", "chatbot testing strategy" | The 27 test files (12 scenarios each, with a rubric and a results table) | **Strong** | One checklist page: scenarios by behavior (handoff, fallback, corrections, errors, refusals, waits). Say plainly the scenarios are untested designs |
| How to evaluate a RAG chatbot | "how to evaluate a rag chatbot" | Citation and wrong-answer tests in the confident-wrong-answer pattern | **Partial** | Retrieval metrics are not ours; cover answer-side checks only |
| Voice agent testing | "ai voice agent testing", "automated voice agent testing", "voice agent testing framework" | [Repair failure](../../goals/voice/failures/repair-failure.md) and the order and wait tests | **Partial** | Our scenarios are behavior checks; platform and audio-pipeline testing are not covered |

### B. Metrics and measurement
*Fit: the primary metrics and counter-metrics on every pattern.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| Chatbot containment rate | "chatbot containment rate benchmark", "what is chatbot containment rate", "bot containment rate" | [The answer-and-go conversation](../../goals/conversation-leadership/failures/answer-and-go-conversation.md) (confirmed resolution versus containment); handoff measurement notes | **Strong** | Page: what containment measures, why it misleads, and what to track beside it; benchmark figures from vendors would need sources I have not opened |
| Chatbot KPIs and evaluation metrics | "chatbot kpi metrics", "chatbot evaluation metrics", "ai chatbot success metrics", "chatbot csat benchmark" | Every pattern's metrics table (metric, target, how to measure, alert at) | **Strong** | A metrics catalog page that points from each metric to its pattern; targets stay labeled as starting points |

### C. Human in the loop and escalation in code
*Partial: our rules are framework-neutral; searchers want framework steps.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| Human in the loop in LangGraph and LangChain | "human in the loop with langgraph", "how to add human in the loop langgraph", "human in the loop langgraph python", "human in the loop in langchain", "langchain agents middleware human_in_the_loop" | [When a bot should hand off](../../goals/human-handoff/failures/escalates-too-early-or-too-late.md), the approval and handoff rules | **Partial** | The decision of when to pause for a person is ours; framework code is not. A page would need tested code from a person, so it stays a design page until then |
| n8n AI agent human in the loop, timeout, retry | "n8n ai agent human in the loop", "n8n ai agent timeout", "n8n ai agent infinite loop" | [Silent long-running work](../../goals/response-time/failures/silent-long-running-work.md) | **Weak** | Tool-specific how-to; we have no tested workflow to offer |

### D. Errors, timeouts, and retries
*Partial: we cover what the user sees, not engineering settings.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| LangChain tool and agent error handling | "langchain tool error handling", "langchain agent error handling", "langchain tool call error handling" | [Generic error messages](../../goals/errors-and-recovery/failures/generic-error-messages.md) | **Partial** | Add the user-facing half to a page whose engineering half is someone else's |
| OpenAI API timeout and 504 errors | "openai api timeout", "openai api connection timeout", "openai api 504 gateway time out" | Same | **Weak** | Pure troubleshooting; we have no verified fix |
| AI agent stuck in a loop | "ai agent stuck in loop", "ai agent feedback loop", "ai agent control loop" | [Dead-end replies](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) (repeat limits), [Corrections not applied](../../goals/dialogue-management/failures/corrections-not-applied.md), the McDonald's incident | **Partial** | Loop detection rules could be a short page; needs a named source for loop statistics |

### E. Context, memory, and long conversations
*Partial to Strong: we cite the research.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| Lost in the middle | "llm lost in the middle problem", "llm lost in the middle paper", "lost in the middle in llm", "llm lost in the middle effect" | [No warning of context loss](../../goals/effort-and-memory/failures/no-warning-of-context-loss.md) (cites Liu et al.) | **Strong** | A short explainer from the paper's abstract and what a product should do about it; the paper is well covered elsewhere |
| Chatbot memory management | "chatbot memory management", "chatbot memory architecture", "ai chatbot memory and privacy" | Same, and the memory-full incident | **Partial** | We cover notices and pinned facts, not storage architecture |

### F. Hallucination, citations, and confidence
*Partial: we cover the user-facing design.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| How to prevent LLM hallucinations | "how to prevent llm hallucinations", "how to reduce hallucinations in llm", "chatbot hallucination rate" | [Confident wrong answer with no way to check](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) | **Partial** | Very competitive; our angle is show-the-source and say-when-unsure, with the experiments we opened |
| RAG citation accuracy | "rag citation accuracy", "llm citation accuracy", "citations in rag" | Same (Liu et al. audit: 51.5% and 74.5%; Ding et al. on trust) | **Strong** | A page on whether the citation supports the claim; has a real audit number from an opened abstract |
| LLM confidence score | "confidence score from llm", "asking llm for confidence score", "confidence score for llm output" | Same | **Partial** | We say when to show uncertainty; the technique itself is someone else's topic |

### G. Refusals
*Partial.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| LLM over-refusal benchmark | "llm over refusal", "llm refusal benchmark", "llm refusal dataset", "llm refusal detection" | [Over-refusal of ordinary requests](../../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (XSTest, OR-Bench) | **Strong** | A page on how to measure over-refusal in your own product with the two-sided test; benchmarks are named from opened abstracts |

### H. Agent failures and observability
*Partial; competitive.*

| Topic | Real suggestions | Our content | Fit | What the page would be, and what is missing |
|---|---|---|---|---|
| Diagnosing AI agent failures | "diagnosing ai agent failures from execution trajectories", "ai agent failure rate", "ai agent mistakes" | [Agent-type gap analysis](../agent-type-gap-analysis.md) (trajectory studies I opened) | **Partial** | A hub linking trajectory research to our human-facing failures |
| Customer support AI agent architecture | "customer support ai agent architecture", "customer service ai agent", "customer support ai agent github" | [L1 base agent design](../l1-base-agent-design.md), [L0 base spec](../l0-base-spec.md) | **Partial** | The design is untested; a page must say so |

**Reading the second pull**
- **The best fits are testing and metrics** ("chatbot test cases", "chatbot test scenarios", "chatbot containment rate", "chatbot kpi metrics", "chatbot evaluation metrics"). Developers search these, and we hold a distinctive asset for them: scenario lists and metric definitions on every pattern. These should be the first assets.
- **Framework-specific queries** (LangGraph, LangChain, n8n) show real developer demand, but our content is framework-neutral and we have no tested code. Treat these as design pages until a person supplies tested snippets.
- **Pure troubleshooting queries** (OpenAI API timeouts, 504 errors) are out of our reach without verified fixes.
- **Competition is unmeasured.** I have not checked who ranks for any of these. Before writing, check the top results for each target, and prefer queries where the leading pages are thin.


## 2c. Competition check for the four lead queries
I searched each phrase once with the web search tool and read who appears. This is **not a rankings report**: it shows which kinds of pages the tool returned, not where they rank on Google, and I opened none of them beyond the result summaries.

| Query | Who appears | What they offer | The gap for us |
|---|---|---|---|
| chatbot test cases | Botium and Rasa documentation, a research paper on a test generator (Chatbot Test Generator, arXiv 2503.05561), a student project, short guides | Tool-specific test syntax, intent and paraphrase coverage, regression testing | A behavior checklist with pass and fail rubrics (handoff, corrections, errors, refusals, waits) that is not tied to one tool. Our scenarios are untested designs and must say so |
| what is chatbot containment rate | At least ten vendor glossary and blog pages (Decagon, Botpress, Kommunicate, Fini, Kodif, and others) | A definition, the formula, a 70% to 90% benchmark range, and a caveat that contained does not mean resolved | The space is crowded and vendor-written. Our angle is narrower: why containment misleads, and confirmed resolution as the companion metric. Benchmark ranges quoted by vendors would need sources I have not opened |
| chatbot fallback message | Platform help pages (WATI, Chatfuel, Chatway, Hexabot) and a Kommunicate glossary | How to set the message text and the number of attempts | Design rules: the fallback ladder, what to say on the second miss, when to hand off, and the metric. Platform pages stop at configuration |
| chatbot human handoff | Vendor blogs and docs (Landbot, Macha, eesel, Kommunicate, Tiledesk), plus a research paper on predicting handoff (arXiv 2012.07610) | Triggers, continuity, queueing, "the goal is the right handoffs" | A trigger table with test scenarios and a handoff summary schema, built on sources I opened; vendors mostly give advice without tests |

**What this means:** the four lead queries are contested by vendors with larger sites. Our edge is evidence and tests (opened sources, rubrics, metrics with counter-metrics), not coverage. Prefer the query where our asset is clearly different (test cases, handoff with tests, fallback ladder) over the one with the most vendor pages (containment rate), and measure with Search Console rather than assume a win.

## 3. What to do, in order
1. **Fix what searchers see on pages that already rank.** Rewrite title, meta description, and the first two sentences of the older pages in section 1, so each answers its likely query directly. Expected effect: more clicks at the same position. **These pages are outside the human-machine-interface folder, so I need your go-ahead to edit them** (or I write the proposed text into the merge-proposals file for you to apply). The /patterns/ index alone has 2,048 impressions.
2. **Retitle the written human-machine-interface patterns for developer phrases** (no address changes). For example, "Dead-End Replies" becomes a page about the chatbot fallback message. Rows 1 to 9 above name the target phrase for each.
3. **Build developer assets from existing material** instead of more patterns, in this order: the chatbot test cases and scenarios checklist (section 2b A, row 7), chatbot containment rate and KPIs (2b B), the chatbot handoff guide (row 1), chatbot fallback message (row 2), RAG citation accuracy (2b F), chatbot error handling (row 3), and the AI agent failure-modes hub (row 10). Each carries its query evidence.
4. **Get the pages live.** Nothing from this library can rank until the site builds and deploys; every publish so far has built cleanly but not deployed.
5. **Measure.** Re-export Search Console after two weeks and compare impressions, position, and clicks on the changed pages. Log the result in the SEO log.

## 4. What this plan does not claim
- Volumes: the suggestions are not search counts, and Search Console shows impressions only for pages that already exist.
- That any change will raise rankings or clicks.
- Anything about queries Search Console withheld.

## Related
- [Search queries (consumer-oriented, set aside)](queries.md) · [Content alignment (consumer, set aside)](content-alignment.md) · [SEO README](README.md) · [SEO log](log.md)
