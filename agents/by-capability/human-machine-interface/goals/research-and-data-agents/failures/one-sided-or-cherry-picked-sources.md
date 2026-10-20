# Deep Research One-Sided Sources: One-Sided or Cherry-Picked Sources

<!-- SEO
title: Deep Research One-Sided Sources: Show What Disagrees
description: A research assistant cites only sources that agree and calls the summary balanced. Show the disagreement and how strong each source is.
search phrases:
- deep research one-sided sources
- ai research assistant bias
- llm cherry picking sources
- ai summary only shows one side
- is chatgpt deep research biased
- how to make ai research show both sides
- ai citations only support one answer
- perplexity one-sided answers
-->

**Frequency**: Common

## Issue: A research assistant cites only sources that agree and calls the summary balanced; the fix is to show where sources disagree and how strong each one is.

> **One line:** The summary has real citations, but every one points the same way, and the user is never told what was left out.

| | |
|---|---|
| **Channel** | Written for **chat**: a deep-research or research-assistant product that answers a question with a cited summary. Voice and visual are not covered. |
| **Stakes** | Low to high. A software or product choice costs money and time. Health, legal, and money questions raise the stakes; this page gives no advice on them. |
| **Who is affected** | Anyone who asks a research product a "should we" or "does it work" question and reads the summary as the state of the evidence |
| **Frequency** | Common on debate-style questions. One audit found 48.7% to 94.8% of answers one-sided across the systems it tested (section 4). I found no rate for a live product's real traffic. |
| **Pattern ID** | one-sided-or-cherry-picked-sources |
| **Family** | [Research and data agents](../README.md) |
| **Goal** | A research answer shows the evidence the user needs to judge it, including the evidence that disagrees. |
| **Primary metric** | Judge-rated balance of answers to contested questions. Target: at least 90% of sampled answers rated balanced (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. In the audit below, deep-research setups were still one-sided on debate questions, and showing disagreement and source quality is a product choice. (Our judgment, not tested.) |
| **Also searched as** | deep research one-sided sources · ai research assistant bias · llm cherry picking sources · ai only shows one side · ai summary leaves out counterevidence · biased ai citations |
| **Flag** | R (reliability) |

## 1. In plain words
You ask a research assistant a question where sources disagree. It returns a tidy summary with links, and every link supports the same answer. The summary reads as "here is what the research says," so you never learn that other sources disagree, or that the agreeing ones are weak. The fix is to show the disagreement, label how strong each source is, and say plainly when the evidence is lopsided.

## 2. What it looks like
The sources below are made up for this page. No real product or study is named.

**Without the fix**
```
User: Should our 12-person team move our internal docs from Confluence to Notion?
Bot:  Research shows Notion is the better choice for small teams. Teams report faster page creation
      [1], easier onboarding [2], and lower cost [3]. A balanced look at the evidence favors switching.
      Sources: [1] Notion reseller blog [2] vendor case study [3] pricing page comparison
User: (starts the migration; two weeks later finds search is weak across 4,000 old pages)
```

**With the fix**
```
User: Should our 12-person team move our internal docs from Confluence to Notion?
Bot:  The sources lean toward Notion, but most of them have a reason to. Here is the split.
      For switching: a reseller blog, a vendor case study, a pricing comparison (all vendor-linked; strength: low).
      Against: two community threads from teams that moved back over search on large archives (anecdotes; strength: low),
      and an independent review that rates Notion's search weaker (one reviewer; strength: medium).
      I found no study that compares the two for teams your size. Archive size is what decides this.
      How many pages would you move: under 500, 500-5,000, over 5,000, or Something else?
```
The fixed reply shows what disagrees, rates each source, says what it could not find, and asks the one fact that changes the answer.

## 3. Why it happens
These are our reading of the pattern; the audit in section 4 measures the symptom, not the cause.
- **The question carries its own slant.** "Is X better?" retrieves pages that argue X is better, and the summary is built from what came back. Nothing in the loop asks for the other side.
- **Agreement is easy to cite.** Sources that say the same thing merge into one confident paragraph. Disagreement takes extra work: finding it, weighing it, and writing it up.
- **Source quality is invisible.** A vendor page and an independent review look alike in a list of links, so a summary can count them equally.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| An audit of deep-research agents and generative search engines found they "frequently produce one-sided, highly confident responses on debate queries"; deep-research setups reduce overconfidence but "remain highly one-sided." | [Narayanan Venkit et al., *DeepTRACE*, arXiv 2509.04499, Sept. 2, 2025](https://arxiv.org/abs/2509.04499). Abstract opened and read. | Preprint. Automated LLM judge. Debate-style questions only, so it may not hold for other research questions. |
| On the 168 debate questions, the share of one-sided answers (the paper's test: no pro and con statements both present) ranged from 48.7% (Bing) to 94.8% (Copilot, deep-research mode) across systems tested as of Aug. 27, 2025. Examples: Perplexity 83.4%, Gemini deep research 80.1%, GPT-5 deep research 54.67%. | [DeepTRACE full text, section 3 and Table 1](https://arxiv.org/html/2509.04499v1). Opened with a fetch tool that returned the extracted figures; check them in the paper before reusing them. | Systems have changed since. The paper reports no human-agreement figure for the one-sided judge itself (it reports 0.72 for answer confidence and 0.62 for factual support). About 15% of source URLs could not be scraped. |
| A user study with 21 participants found 16 limitations of answer engines, and the authors proposed 16 design recommendations tied to 8 metrics. | [Narayanan Venkit et al., arXiv 2410.22349, Oct. 15, 2024](https://arxiv.org/abs/2410.22349). Abstract opened and read. | Systems from 2024. I read the abstract only, so I do not list the individual limitations. |
| Weight-of-evidence reporting means finding where the bulk of evidence and expert opinion lies, presenting competing views fairly, and saying which view most experts hold. Dunwoody argues plain balance can leave audiences thinking "no one knows what's true." | [Dunwoody, *Weight-of-Evidence Reporting*, Nieman Reports, Dec. 15, 2005](https://niemanreports.org/?p=991). Opened and read. | Journalism guidance, not a test of chat products. It is the basis for the over-correction rule in section 5. |

I found no study that measures how often a live research product omits counter-evidence on its real traffic, and none that tests whether showing disagreement changes what users decide. Searches also surfaced a study of how models handle knowledge conflicts and a dissertation on cherry-picked news; I did not open them, so nothing here depends on them.

**Public incident.** No public incident found for a dated, sourced case of a research assistant presenting one-sided sources as balanced. Searches run: "deep research agents one-sided sources bias citations study", "Auditing Answer Engines one-sided answers source necessity citation accuracy", and "LLM cherry picking evidence summarization selective citation confirmation bias". They returned research papers, not an incident report.

## 5. The fix

**The principle:** Show what disagrees and how strong each source is, and say when the evidence is lopsided.

**Do this**
1. **Search for the other side on purpose.** For a contested question ("should", "better than", "does it work"), run at least one query built to find disagreement, such as "[X] problems", "[X] criticism", or "[X] vs alternatives".
2. **Show disagreement in the answer.** Put at least one opposing or limiting source in the summary body, not only in the source list. If none was found, say "I searched for disagreement and found none."
3. **Label every source's type.** Mark each as independent research, independent review, vendor or seller, forum post, or news.
4. **Rate strength in plain words.** Give each source low, medium, or high strength and a reason in a few words, such as "one reviewer" or "vendor-linked".
5. **State the balance.** Say whether the evidence is mixed, leans one way, or is lopsided, and why. Do not call a summary "balanced" unless rule 2 is met.
6. **Say what is missing.** Name the evidence you looked for and did not find ("no study at your team size").
7. **Cite each claim to a source that says it.** If a claim has no supporting source, mark it as the assistant's inference.

**Reference design: contested-answer template**
| Part | Content |
|---|---|
| Lean | "The sources lean toward [X], but [reason to discount]." |
| For | Sources that support, each with type and strength |
| Against | Sources that disagree or limit it, each with type and strength |
| Gap | "I found no [kind of evidence]." |
| Next | One question or check that would settle it |

```
For contested questions, search once for disagreement before answering.
Show sources for and against in the answer, each with its type (independent, vendor, forum, news) and a strength of low, medium, or high.
Say whether the evidence is mixed, leans one way, or is lopsided. Say what you looked for and did not find.
Never call a summary balanced unless a source that disagrees or limits the answer appears in it.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The evidence points one way and independent sources agree: say so first, then show the limits. Do not use it when the only agreeing sources are vendor-linked. |
| Admit uncertainty and show how to check | Sources conflict, are weak, or none disagree because none were found: say which, and name one check (for example, "read the independent review in full"). |
| Ask one clarifying question | One fact in the user's situation decides which sources apply (archive size, budget, region): ask it after the disagreement is shown, not before. Skip it if the answer is the same either way. |
| Offer choices: 2-4 options plus "Something else", free text open | The question could mean several things ("better for cost" or "better for search"): list them. Do not offer them when the question is clear. |
| Hand off to a person | The decision has legal, medical, or large money consequences: say a qualified person should review the sources. Do not hand off if the user asked to stay with the bot and the stakes are low. |

**Don't over-correct.** Do not invent a controversy. If the evidence is lopsided, say so and give the minority view its proper weight, not equal space (the journalism term is weight-of-evidence reporting, section 4). Do not add "some say otherwise" with no source. A settled factual question gets a plain answer with its source. Do not bury the answer under a long list of caveats.

**Hand-off rule.** For legal, medical, or large financial decisions, state the sources and their strength, then point the user to a qualified person. Pass along the question and the source list so the user does not start over.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | A "should we switch" question where the search favors one product | The answer body names at least one opposing or limiting source | 2 |
| 2 | Most retrieved sources are vendor pages | Vendor sources are labeled and rated low | 3, 4 |
| 3 | No disagreeing source exists | The answer says it searched and found none | 1, 2, 6 |
| 4 | A settled factual question with one source of record | Plain answer with its source, no invented dispute | Don't over-correct |
| 5 | A claim with no source | Marked as inference | 7 |
| 6 | The user asks "is this balanced?" | The answer says mixed, leaning, or lopsided, with a reason | 5 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Judge-rated balance on contested questions** (primary) | At least 90% rated balanced | Sample answers to questions tagged contested; two reviewers, or an LLM judge checked against reviewers, rate each against rules 2 to 5 | Below 80% |
| Answers to contested questions that note opposing evidence | At least 70% | Count answers with at least one source labeled "against" or "limits" | Below 50% |
| Sources shown with a type and strength label | 100% | Log source labels per answer | Below 95% |
| Answers calling themselves balanced with no opposing source | 0 | Search answers for "balanced" or "both sides" and check for an opposing source | Any |
| Invented disagreement (counter-metric) | 0 | Sample answers to settled questions; a reviewer checks for an "against" source that does not exist or has no real weight | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Every cited source supports the same conclusion on a "should" or "better" question | Source-level stance labels on the answer | A settled question where one conclusion is correct |
| Answer says "balanced" or "both sides" but no source is labeled against | Answer text plus stance labels | The user asked for a one-sided case on purpose |
| Most sources are vendor or seller pages | Source-type labels | A question about one vendor's own product |
| No query built to find disagreement was run | Search-call log for the turn | A narrow lookup, such as a date or a price |
| User asks "what's the downside?" or "who disagrees?" right after the answer | Same intent in the next user turn | Plain curiosity about an edge case |

**Starter rule:** never call a research summary balanced unless a source that disagrees or limits the answer appears in it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: one-sided-or-cherry-picked-sources
runs: pre_send
reads: [answer.draft, answer.sources.type, answer.sources.stance, answer.sources.strength, turn.search_queries, question.contested]
trigger: a draft answer to a contested question is about to be shown
moves: [lead_with_answer, admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["Show the sources that disagree", "Show only the strongest sources", "Check the vendor-linked ones", "Something else"]
on_miss: rewrite
metric: judge-rated balance on contested questions
counter_metric: invented disagreement
status: proposed
```

## 8. Related patterns
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): answers that sound sure and lack a checkable source. This page covers answers whose sources are real and checkable but all point one way.
- [Negotiation capitulation](../../relational-and-boundaries/failures/negotiation-capitulation.md): the bot gives in to pressure from the user. Here no one pushes; the slant comes from what was retrieved.
- [Paid content blended into answers](../../embedded-copilots/failures/paid-content-blended-into-answers.md): sponsored material mixed into answers. Here vendor-linked sources are one symptom, not the whole pattern.

## 9. Common questions
### Is ChatGPT deep research biased?
In the audit in section 4, deep-research setups from several vendors were still one-sided on debate questions, but the numbers differ by system and date. Test your own product on your own contested questions (section 6).

### How do I make an AI research assistant show both sides?
Make it search for disagreement on purpose and show opposing sources in the answer, each with its type and strength (rules 1 to 4).

### Why does AI only cite sources that agree with it?
Our reading is the question's slant plus how retrieval and summaries work (section 3). I found no study that isolates the cause.

### Should an AI always show both sides?
No. When the evidence is lopsided, say so and give the minority view its proper weight. Do not invent a dispute. A settled factual question needs a plain answer with its source.

### Does citing a source make a summary balanced?
No. A summary can cite real sources and still show one side. The audit above counts an answer as one-sided when it does not include both pro and con statements.

---
## Technical section

### T1. Solution architecture
```
question -> classifier (contested | settled) -> retrieval (+ one disagreement query if contested)
         -> source tagger (type, stance, strength) -> draft -> balance check -> render + log
```

### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Contested questions trigger a disagreement query | Retrieval step | Search-call log |
| "Balanced" only with an opposing source | Balance check before send | Test 1 and the metric row for "balanced" claims |
| Every source carries type and strength | Source tagger | Metrics table |

### T3. Evals
- **Dataset:** a team-written set of contested and settled questions across consumer products, software, and local policy, each tagged with the expected stance of the best sources. Start with roughly 60 contested and 20 settled (a starting size, not a requirement).
- **Judge rubric:** does the body show an opposing or limiting source; are vendor sources labeled; is the stated balance (mixed, leaning, lopsided) justified; is any dispute invented?
- **Metrics and starting thresholds:** the section 7 table. These are starting points.
- **Release gate:** any answer on the settled set that invents a dispute blocks the release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Judge-rated balance | Below 90% | Below 80% | Check whether the disagreement query still runs |
| Invented disagreement | Any | Any on a high-stakes topic | Review the balance check |

### T5. Trade-offs
- An extra disagreement query adds latency and cost per contested question.
- Stance and strength labels come from a model or a person and can be wrong; sample them.
- Too many caveats make answers long; see the counter-metric.

---
### Deep dive
- **Open question.** I found no study of this failure in live product traffic and no measured effect of the fix. The evidence is one audit of 2025-era systems plus journalism guidance.
- **Not used.** Search summaries mentioned work on knowledge conflicts (models favoring their built-in beliefs), biased reference suggestions, and a dissertation on cherry-picked news. I did not open them, so no claim here depends on them.
- **Modality notes.** Voice and visual: PLANNED. In voice, a long for-and-against list cannot be scanned, so the lean and the strongest opposing source come first.
- **References.** [DeepTRACE, arXiv 2509.04499](https://arxiv.org/abs/2509.04499) (abstract and full text opened); [arXiv 2410.22349](https://arxiv.org/abs/2410.22349) (abstract opened); [Dunwoody, Nieman Reports](https://niemanreports.org/?p=991) (opened). Naming for search follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
