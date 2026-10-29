# "Delve" Frequency Over Time: ChatGPT Overused-Word Lists Go Stale With Each Model Version

<!-- SEO
title: "Delve" Frequency Over Time: AI Word Lists Go Stale
description: Each model version overuses different words, and people adopt them too, so a ChatGPT word list must be measured per model and re-measured.
search phrases:
- does chatgpt still say delve
- delve frequency over time
- chatgpt overused words 2026
- gpt-5 overused words list
- ai words list outdated
- why does my ai word list flag human writing
- claude vs chatgpt overused words
- how to update list of ai words
-->

**Frequency**: Common

## Issue: Each model version overuses different words, and people adopt them too, so a ChatGPT word list must be measured per model and re-measured.

> **One line:** A team checks AI drafts against a "ChatGPT words" list ("delve", "tapestry", "testament") copied from a 2024 blog post; the drafting model has since moved on to other words, and human writers now use the old ones, so the list misses new AI drafts and flags people; the fix is to keep every word as a measured row (which model, how much more often than human text, measured when) and re-measure each word, and the human baseline, on every model change.

| | |
|---|---|
| **Channel** | Written for **word-level checks on published text**: phrase lists in Vale, CMS plugins, editor macros and review checklists used on drafts from ChatGPT, Claude, Gemini, Grok or Copilot. |
| **Stakes** | Medium. Missed AI drafts reach readers, and stale words flag human writers, which can feed false accusations. |
| **Who is affected** | Editors and reviewers who trust the list; writers whose own text is flagged; readers of what slips through |
| **Frequency** | Common, in our judgment. Wikipedia's editor guide now lists different AI words for each model era (section 4). I found no count of teams using outdated lists. |
| **Pattern ID** | text-word-list-drift |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Measured-word rate: words on the active list whose excess ratio was measured on the current drafting model, divided by all active words. Proposed starting target: 100% within 7 days of a model change. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Newer models drop old favorites and pick up new ones, so a better model makes a fixed list stale faster. (Our judgment, not tested.) |
| **Also searched as** | ChatGPT words list 2026 · delve no longer AI · new AI words GPT-5 · AI vocabulary by model · humans saying delve · AI word list false positives |

## 1. In plain words
"Delve" was the famous ChatGPT word of 2023. One study found GPT-5 uses it less often than people do. Each model version has its own favorite words, and people pick up the old ones from reading AI text. A word list is a measurement of one model against one set of human writing at one time. Keep the measurement with each word, and take it again when either side changes.

## 2. What it looks like
**Without the fix** (illustrative: a marketing team in Phoenix that checks freelance and AI-drafted blog posts)
```
Editor:  Run the AI-word check on this week's 30 posts.
Checker: 2 posts flagged. Post 7 (Maria, staff writer): "delve", "tapestry". Post 19: "testament".
         28 posts clean. List: "50 ChatGPT words" (copied from a blog post, 2024).
Editor:  Maria, did you use ChatGPT on post 7?
Maria:   No. I wrote it myself. I say "delve" all the time now.
(Posts 3, 11 and 24 came straight from the drafting tool's current model. They pass.)
```
**With the fix**
```
Editor:  Run the AI-word check on this week's 30 posts.
Checker: Drafts from writer-2026-10 are scored with 23 words measured on that model (Oct 12).
         Posts 3, 11, 24: 4-6 measured words each, e.g. "leverage" (6x the human rate on this model).
         Post 7: "delve" is retired; it now runs at or below the 2026 human rate. No count.
         These are weak signals, not proof. Choose: "Send 3, 11, 24 for rewrite", "Show the word table", "Something else".
Editor:  Send 3, 11, 24 for rewrite.
```
The fixed checker scores each draft only with words measured on the model that made it, shows each word's ratio and date, and has retired "delve" because people now use it as often as the model.

## 3. Why it happens
- **Each model version learns a different set of favorite words.** One study found the "delve" odds ratio in GPT-revised abstracts fell from about 380:1 (GPT-3.5-turbo) to 40:1 (GPT-4o) and below 1:1 (GPT-5). Another links word overuse to human-feedback tuning. Each new tuning run can change which words win (section 4).
- **People adopt the AI words, so the human baseline moves.** Words ChatGPT favors rose in unscripted human speech after its release. A list measured against 2022 human text will flag 2026 human writers.
- **Lists get copied, not measured.** Public "ChatGPT words" lists are snapshots of one model era. They rarely say which model or date they came from, so the team can't tell when a word went stale. (Our reading.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| For "delve", "the odds ratio in revised arXiv abstracts declines from approximately 380:1 under GPT-3.5-turbo", to "100:1 for GPT-4-turbo and 40:1 for GPT-4o". With GPT-5, "most of the signature words are no longer over-used, and *delve* itself falls below its human baseline" (about 0.7:1 on arXiv). The same appendix says word preference patterns were stable across GPT-family models in general. | [Yakura et al., *Empirical evidence of Large Language Model's influence on human spoken communication*, arXiv 2409.01754 v4, July 2026](https://arxiv.org/abs/2409.01754), Appendix A, read in the [HTML full text](https://arxiv.org/html/2409.01754v4) (first 100,000 of about 225,000 characters). | Preprint, single source. Measured on abstracts revised by GPT models, OpenAI models only. The paper notes both stability across most words and a steep decline for "delve". |
| The same study found an abrupt rise in words ChatGPT prefers, such as "delve", "showcase", "boast", "intricacies" and "meticulous", in unscripted human speech after its release. It analyzed 737,083 hours from 824,634 podcast episodes plus 360,445 academic YouTube talks. A preregistered experiment (N = 496) found brief chatbot use led people to adopt its words. | Same paper: abstract page and HTML full text opened. | Speech, not writing. Synthetic-control design, so the link to ChatGPT is inferred from timing and control words. |
| Wikipedia's guide says "The words that LLMs overuse have changed over time" and that "delve" "dropped off sharply in 2025". It lists different words per era: GPT-4 (2023 to mid-2024: "delve", "tapestry", "testament"), GPT-4o (mid-2024 to mid-2025: "align with", "fostering", "showcasing"), GPT-5 (mid-2025 to mid-2026: "emphasizing", "enhance", "highlighting") and GPT-6 (mid-2026 on: "leverage", "quietly", "steady"). It says AI vocabulary is "somewhat different depending on the chatbot" and that Grok "continues to overuse *underscore* as of 2026". | [Wikipedia, *Wikipedia:Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Opened; first 100,000 of about 250,000 characters read. | Editor guidance, not a study. The page says the eras are "not hard cutoffs". Lists are short excerpts here, not the full lists. |
| A classifier told apart ChatGPT, Claude, Grok, Gemini and DeepSeek output with 97.1% accuracy on held-out data. The authors find the differences are "rooted in word-level distributions". | [Sun, Yin, Xu, Kolter and Liu, *Idiosyncrasies in Large Language Models*, ICML 2025, arXiv 2502.12150](https://arxiv.org/abs/2502.12150). Abstract page opened. | Controlled task, five models, abstract only. Shows that model families use different words, so one merged list fits none of them well. |
| In an experiment emulating learning from human feedback on Meta's Llama, "participants systematically prefer text variants that include certain words"; the authors argue this tuning step contributes to word overuse. | [Juzek and Ward, *Word Overuse and Alignment in Large Language Models*, arXiv 2508.01930, Aug. 2025](https://arxiv.org/abs/2508.01930). Abstract page opened. | Workshop paper, one model family. That a new tuning run changes the word set is our reading, not their claim. |
| A pipeline "profiles model-specific slop against human baselines" and finds some patterns "over 1,000x more frequently in LLM output than human text". It reports that plain token banning "becomes unusable at just 2,000" patterns. | [Paech, Roush, Goldfeder and Shwartz-Ziv, *Antislop*, arXiv 2510.15061, Oct. 2025](https://arxiv.org/abs/2510.15061). Abstract page opened. | Preprint on creative writing. A search summary said it appeared at ICLR 2026; the arXiv page names no venue, so I did not use that. |

A separate study of arXiv abstracts found "delve" and similar words falling from April 2024 and credits authors editing around them; it is covered in [detection rules decay](./detect-rules-decay.md#4-why-it-matters). I found no study that measured how fast a team's own word list loses hits.

## 5. The fix
**The principle:** Every word on an AI-word list is a measurement (one model, one human baseline, one date), and a word scores drafts only while that measurement is current.

**Do this**
1. **Each word is a measured row.** Record the word, the model version it was measured on, its excess ratio against the human baseline, both sample sizes, the date and where the candidate came from.
2. **Measure before you use.** A word enters the active list only when it appears at least 3 times as often in your drafting model's output as in your human baseline, across at least 200 drafts from at least 3 different prompts (proposed starting thresholds).
3. **Score by model.** A draft is scored only with words measured on the model that made it. If the model is unknown, use all active words, mark the result "model unknown" and treat it as weak.
4. **Re-measure on every model change.** When a drafting model version changes, re-measure every active word on fresh drafts. Words below the threshold move to "retired"; they are kept with their history, not deleted.
5. **Re-measure the human side too.** At least twice a year (proposed), rebuild the human baseline from writing dated after the last baseline, such as your staff's signed-off posts. Retire words whose ratio fell because people now use them.
6. **Show the number, not a verdict.** Each hit is reported with its word, ratio, model and date. Never report a bare "AI word found".
7. **Public lists are candidates, not rules.** A word from a blog post, Wikipedia era list or another team stays in the candidate list, tagged with its source and era, until your own measurement passes rule 2.

**Reference design: the word table** (one row per word and model; it feeds the rule-level manifest in [detection rules decay](./detect-rules-decay.md#5-the-fix))
```yaml
- word: leverage
  model: writer-2026-10
  model_rate_per_10k: 4.8      # in 312 drafts, 9 prompts
  human_rate_per_10k: 0.8      # baseline: staff posts, Apr-Sep 2026
  excess_ratio: 6.0
  measured: 2026-10-12
  source: wikipedia-era-list   # own-drafts | public-list | wikipedia-era-list
  status: active               # candidate | active | retired
- word: delve
  model: writer-2026-10
  excess_ratio: 0.9
  measured: 2026-10-12
  status: retired
  retired_reason: below human rate on current model and 2026 baseline
```
Excess ratio = (word count / total words in model drafts) divided by (word count / total words in the human baseline). Add one to both counts so a word missing from the baseline does not divide by zero.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the checker reporting to the editor)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Every report: each hit carries its ratio, model and date and is called a weak signal, not proof of AI use. |
| Offer choices: 2-4 options plus "Something else", free text open | After a scored batch: "Send flagged posts for rewrite", "Show the word table", "Something else". |
| Ask one clarifying question | A batch has no model record: the checker asks once which tool and model made it, before using model-specific words. |
| Hand off to a person | Re-measurement turns up new candidate words or retires many at once: the list owner decides before the active list changes. |

**Don't over-correct.** Do not add every word with a high ratio; a long list flags ordinary writing, and Antislop found plain token banning breaks down past about 2,000 patterns. Do not re-measure on so few drafts that one prompt's topic words ("furnace", "Phoenix") pass the threshold; rule 2's prompt spread guards against this. Do not use a word hit to accuse a writer; see [folk tells are not evidence](./text-folk-tells-unreliable.md).

**Hand-off rule.** Moving a word from candidate to active, or retiring more than a quarter of the active list in one re-measure (proposed), needs the named list owner's sign-off. If a writer disputes a flag, a person reviews the post; the word table is shown as context only.

**Framework used:** none yet. The per-word ratio against a human baseline follows the Antislop profiling idea and the odds ratios in Yakura et al. (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Word added to the active list with no model or date | List build rejects it | 1 |
| 2 | Candidate word at 2x the human rate on the current model | Stays a candidate | 2 |
| 3 | Draft from model A scored while model B's words are also active | Only model A's words count | 3 |
| 4 | Drafting model changes from writer-2026-06 to writer-2026-10 | All active words re-measured within 7 days; those below 3x retired with history | 4 |
| 5 | Staff writer's own post uses "delve", now at the human rate in the new baseline | "delve" retired; post not flagged | 5 |
| 6 | Post with 4 active-word hits | Report shows each word's ratio, model and date, and the words "not proof" | 6 |
| 7 | Team pastes a 2024 "ChatGPT words" blog list | Words land as candidates tagged "public-list", none active | 7 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Measured-word rate** (primary) | 100% within 7 days of a model change | Word table: active words with a row for the current model / all active words | Below 95% after 7 days |
| Hits per 10,000 words on fresh drafts from the current model | Within half of the last re-measure | Weekly scan of a fixed sample of new model drafts | Below half |
| Active words with no own measurement | 0 | Word table: active rows whose `source` is a public list and have no `excess_ratio` | Any |
| Days since the human baseline was rebuilt | 183 or fewer (proposed) | Baseline build log | Over 183 |
| Human-baseline flag rate (counter-metric) | Track; set from baseline | Share of recent signed-off human posts with 3 or more active-word hits | Rising after a list update |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The list's newest `measured` date is older than the drafting model's release date | Word table vs. model change log | The model change was a pinned alias for the same model |
| Hits on human-written posts rise while hits on AI drafts fall | Scan log split by known author type | Writers started pasting AI drafts into their own posts |
| Most hits come from words tagged to an older model era ("delve", "tapestry") | Hit log joined to the word table | The team really is using an older model on purpose |
| Writers dispute flags and say the word is their own | Review comments, flag disputes | One writer's habit, not a list-wide drift |

**Starter rule:** score a draft only with words whose excess ratio was measured on the model that produced it, and show each hit with its ratio and date.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-word-list-drift
runs: pre_send
reads: [draft.body, draft.generating_model, word_table.word, word_table.model, word_table.excess_ratio, word_table.measured, word_table.status, human_baseline.built]
trigger: a draft is scored against the AI-word list, or the drafting model version changes
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Send flagged posts for rewrite", "Show the word table", "Something else"]
on_miss: log
metric: measured-word rate
counter_metric: human-baseline flag rate
status: proposed
```

## 8. Related patterns
- [Stock phrases in AI-written text ("delve")](./text-stock-phrases.md) - gives the starting phrase list and the pre-publish block. This page is about keeping each word on such a list measured against a named model and a current human baseline.
- [AI detection rules stop working after a model update](./detect-rules-decay.md) - the closest pattern. It versions whole rules and classifiers and re-tests them on a canary set. This page works one level down: per-word ratios, per-model columns, and the human baseline that drifts as people adopt AI words.
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - why a single word hit is never evidence about a person.
- [AI detector false positives](./detect-detector-false-positives.md) - the cost of flagging human writing, which a stale baseline makes worse.

## 9. Common questions
### Does ChatGPT still say "delve"?
Much less. One study measured "delve" at about 380 times the human odds in GPT-3.5-turbo revisions, 40 times in GPT-4o, and below the human rate in GPT-5. A "delve" check now mostly catches older models and people.

### What words does GPT-5 or the newest ChatGPT overuse?
Wikipedia's guide lists "emphasizing", "enhance", "highlighting" and "showcasing" for the GPT-5 era, and words such as "leverage", "quietly" and "steady" from mid-2026. Treat these as candidates and measure them on your own drafts (rule 7).

### Do Claude and ChatGPT overuse the same words?
No. A 2025 study told five chatbots apart with 97.1% accuracy, mostly from word choice, and Wikipedia notes Grok's own habits. Keep words per model family (rule 3).

### Why does my AI word list flag human writing now?
People have picked up AI words. One study found "delve" and similar words rose in unscripted podcasts and talks after ChatGPT. Rebuild your human baseline from recent writing (rule 5).

### How often should I update a ChatGPT words list?
Re-measure every word when the drafting model changes, and rebuild the human baseline at least twice a year (our starting point). See [the fix](#5-the-fix).
