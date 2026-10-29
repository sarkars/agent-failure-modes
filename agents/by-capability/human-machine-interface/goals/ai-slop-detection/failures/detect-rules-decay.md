# AI Detection Rules Stop Working After a Model Update: Phrase Lists, Regex and Classifiers That Decay

<!-- SEO
title: AI Detection Rules Stop Working After a Model Update
description: Phrase lists, regex rules and AI-text or AI-image classifiers built on last quarter's model miss the new one; version rules and re-test on each release.
search phrases:
- ai detector stopped working after model update
- chatgpt doesn't say delve anymore
- ai phrase list outdated new model
- ai text detector fails on new models
- ai image detector doesn't work on midjourney
- how often to update ai detection rules
- detector drift new llm release
- regression test for ai content checks
-->

**Frequency**: Common

## Issue: Phrase lists, regex rules and AI-text or AI-image classifiers built on last quarter's model miss the new one; version rules and re-test on each release.

> **One line:** A content team's check for AI-written text, code or images was tuned on one model ("delve", em dashes, a classifier trained on last year's images); the drafting tool moves to a new model, the hit rate falls to near zero, and the check reports "all clear" while catching nothing; the fix is to version every rule with the model it was tested on, re-test it on a fixed set of fresh samples whenever a generating model changes, and alert when its hit rate drops.

| | |
|---|---|
| **Channel** | Written for **pre-publish and pre-merge checks** on text, code and images: Vale or regex phrase lists, CI lint rules, and AI-text or AI-image classifiers that a builder runs on output from ChatGPT, Claude, Gemini, Copilot, Midjourney or similar tools. |
| **Stakes** | Medium. Nothing visibly breaks: the check keeps passing, so the team stops looking, and slop reaches readers until someone outside notices. |
| **Who is affected** | Editors, reviewers and platform teams who rely on the check; readers who get the unchecked output |
| **Frequency** | Common, in our judgment. Every study opened for section 4 found detectors or word signals that shift when the generator changes; I found no count of teams whose rules decayed. |
| **Pattern ID** | detect-rules-decay |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Re-tested rule rate: detection rules in use whose latest canary re-test ran against the current generating model version, divided by all detection rules in use. Proposed starting point: 100% within 7 days of any model change. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Each new model shifts its tells, and people edit around known ones, so a better generator makes a fixed rule decay faster, not slower. (Our judgment, not tested.) |
| **Also searched as** | AI detector outdated · delve no longer works · AI tells change with each model · detector generalization new generator · re-test AI checks after upgrade · AI writing check false negatives |

## 1. In plain words
A rule that catches AI output is a snapshot of one model's habits. When the model changes, or when people learn the rule and edit around it, the habit fades and the rule goes quiet. A quiet rule looks the same as a clean draft, so nobody notices. The fix is to treat each rule like a test with a date on it: record which model it was checked against, check it again on fresh samples when the model changes, and watch its hit rate week by week.

## 2. What it looks like
**Without the fix** (illustrative numbers: a content agency in Chicago that drafts client blog posts with an AI tool)
```
Editor:  Run the AI-tell check on this week's 40 client posts.
Checker: 40 of 40 passed. 0 phrase-list hits. Classifier: 40 "likely human".
Editor:  Great. Publishing all 40.
(The drafting tool moved to a new model on Monday. Last month the same check flagged 12 of 40.
 A client replies Friday: "These all read the same. Did a bot write them?")
```
**With the fix**
```
Editor:  Run the AI-tell check on this week's 40 client posts.
Checker: Not run as a pass. Drafts came from model writer-2026-10; phrase list v14 and classifier c3
         were last re-tested on writer-2026-06. On the canary set they catch 2 of 50 new-model drafts.
         Choose: "Re-test and update now", "Hold the batch", "Publish, logged as unchecked", "Something else".
Editor:  Re-test and update now.
Checker: 9 candidate phrases found in new-model drafts, sent to Dana (list owner) for review. Batch on hold.
```
The fixed checker knows which model each rule was tested on, refuses to call a stale rule a pass, and shows the measured drop instead of "all clear".

## 3. Why it happens
- **The rule was fitted to one model's habits.** Phrase lists come from words one model overused; classifiers learn cues from the generators in their training set. Pu et al. found no text detector that generalized to every generator, and GenImage found an image detector trained on one generator dropped to near-chance on another (section 4).
- **The tells move from both sides.** New model versions change word choice, and people who know a tell edit it out. Geng and Trotta found "delve" and similar words fell in arXiv abstracts from April 2024; they disagree with an earlier study that tied the drop to a model release (section 4). Either cause breaks the same rule.
- **A silent rule looks like a passing check.** Most checks report hits, not coverage. A list that matches nothing gives the same green result as a clean draft, and few teams log the hit rate over time or which model the rule was last tested on.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A statistical analysis of arXiv abstracts reports "a marked drop" in words previously identified as ChatGPT-overused, such as "delve", starting soon after they were pointed out in early 2024; the authors write that "starting from April 2024" these words began to decrease, while "significant" kept rising. | [Geng and Trotta, *Human-LLM Coevolution: Evidence from Academic Writing*, arXiv 2502.09606, Feb. 2025](https://arxiv.org/abs/2502.09606). Abstract and HTML full text opened. | Academic abstracts, not marketing or code. The authors attribute the drop to authors adapting their LLM use, not to a model update. |
| The same paper says a December 2024 study (Leiter et al.) suggested the decline was likely due to GPT-4o's May 2024 release; Geng and Trotta disagree. They also report that the Binoculars detector score did not change significantly between original abstracts and the same abstracts revised by GPT-4o-mini. | Same paper, full text opened. | I did not open Leiter et al.; its claim is read through Geng and Trotta. The cause is disputed, but both readings make a "delve" rule decay. |
| A follow-up analysis says "variations across LLMs also result in evolving patterns of word usage in academic papers" and that real-world LLM usage is "heterogeneous and dynamic". | [Geng, Dong and Poibeau, *Beyond Via*, arXiv 2603.25638, Mar. 2026](https://arxiv.org/abs/2603.25638). Abstract page opened. | Preprint; abstract only, no per-model word lists read. |
| Detectors trained on one LLM's output and tested on held-out generators: "none of the detectors can generalize to all generators", though detectors trained on a medium-size model transferred to its larger version. | [Pu, Zhang, Han, Tsvetkov and He, Findings of EMNLP 2023](https://aclanthology.org/2023.findings-emnlp.318/). Abstract page opened. | Peer-reviewed; 2023 generators. Abstract only, so no accuracy numbers used here. |
| A detector study across recent OpenAI and Anthropic model generations reports that zero-shot detection (Binoculars) "fails on newer models", that supervised detectors transfer unevenly across generations, and concludes that detection needs "continually re-calibrated, model-aware pipelines". | [David, *On the Generalizability of AI-Generated Text Detection*, University of Waterloo thesis, Jan. 2026](https://uwspace.uwaterloo.ca/items/0a45a910-c13a-4323-9acf-806f9378591e). Record page and abstract opened. | Master's thesis, single source, not peer-reviewed; I did not read the full PDF or the model names. |
| In the GenImage benchmark, detectors trained and tested on the same generator scored above 98.5%, but a ResNet-50 trained on Stable Diffusion V1.4 and tested on Midjourney dropped to 54.9% accuracy; the authors observe "a substantial performance degradation" across generators. | [Zhu et al., *GenImage*, arXiv 2306.08571, June 2023](https://arxiv.org/abs/2306.08571). Full PDF opened. | Preprint from Huawei Noah's Ark Lab; 2023 generators; binary real-vs-fake, where 50% is chance. |
| OpenAI's CEO posted that if you tell ChatGPT not to use em dashes in custom instructions, "it finally does what it's supposed to do"; TechCrunch notes this "won't necessarily eliminate the em dash from its output by default." | [Perez, TechCrunch, Nov. 14, 2025](https://www.techcrunch.com/2025/11/14/openai-says-its-fixed-chatgpts-em-dash-problem/). Opened. | Shows a product change aimed at a known tell; no measured effect on em dash rates. |

**Seen only in search summaries, kept out of the fix:** a summary of the SciFigDetect preprint (arXiv 2604.08211) reported an image detector scoring 97.57% on its own generator and 28.40% on GPT-generated figures; and an opinion piece on Implicator argued the em dash setting may regress with future updates. I did not open either.

## 5. The fix
**The principle:** No detection rule counts as a pass unless it was re-tested against the model that produced the output, and its hit rate is tracked over time.

**Do this**
1. **Version every rule.** Each phrase list, regex set and classifier has a version and a `tested_on` field naming the generating model versions it was last re-tested against, with the date.
2. **Log the generating model with every sample.** Every checked draft, diff or image records which tool and model version made it. When unknown, the checker asks once.
3. **Re-test on each model change.** When any generating model in use changes, every rule runs on a canary set: at least 50 fresh samples from the new model (proposed starting size) plus the same human-written control set as last time.
4. **Stale rules don't pass.** If a rule's `tested_on` does not include the current model, the check result is "unchecked", never "pass".
5. **Alert on hit-rate drops.** Track each rule's weekly hit rate on known AI output. A drop of half or more against its baseline (proposed) opens a review, even with no model change logged.
6. **Mine the new model for new tells.** Each re-test lists phrases, patterns or image cues that appear in the new model's samples far more than in the control set; the list owner accepts or rejects each one.
7. **Retire rules that stop earning their keep.** A rule with near-zero hits on two re-tests in a row is retired or rewritten, with the reason logged, instead of kept for comfort.

**Reference design: rule manifest** (one entry per rule, kept next to the rules in version control)
```yaml
rule_id: stock-phrases-blog
kind: phrase_list            # phrase_list | regex | classifier
version: 14
owner: dana.lopez            # the list owner who accepts new tells
tested_on:
  - model: writer-2026-06
    date: 2026-06-18
    canary_hits: 27/50       # known AI samples caught
    control_hits: 1/50       # human-written samples flagged
baseline_hit_rate: 0.54
status: stale                # current | stale | retired; stale when the current model is not in tested_on
```

**Decision table for the checker**
| Situation | Result shown |
|---|---|
| Current model in `tested_on`, rule hit rate near baseline | Normal pass or fail |
| Current model not in `tested_on` | "Unchecked: rule last tested on <model>", with choices |
| Generating model unknown | Ask which tool and model made the batch |
| Weekly hit rate down by half or more, no model change logged | Pass or fail as normal, plus a review ticket to the rule owner |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the checker reporting to the editor or reviewer)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A rule is stale or its hit rate fell: the checker says "unchecked", names the model gap, and shows the canary numbers instead of "all clear". |
| Offer choices: 2-4 options plus "Something else", free text open | The batch hits a stale rule: "Re-test and update now", "Hold the batch", "Publish, logged as unchecked", "Something else". |
| Ask one clarifying question | The batch has no generating-model record: the checker asks which tool and model made it, once. |
| Hand off to a person | The re-test finds candidate tells: they go to the named list owner, not straight into the live rule. |

**Don't over-correct.** Do not add every new candidate phrase the moment it appears; a list that grows unchecked flags human writers too (false positives on human writing are a separate pattern). Do not freeze the generating model just to keep old rules working. Do not trust a vendor detector's "now supports the latest models" note without your own canary run (vendor accuracy claims are a separate pattern). Do not delete a decayed rule silently; retire it with a reason so the history explains past results.

**Hand-off rule.** New candidate tells, and any rule whose canary hit rate fell by half or more, go to the named rule owner before the live rule changes. If no owner is named, the batch is held and the platform team lead is notified.

**Framework used:** none yet. The re-test design follows the cross-generator test idea in Pu et al. and GenImage and the "re-calibrated, model-aware" conclusion in David (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Rule manifest entry with no `tested_on` field | CI rejects the rule file | 1 |
| 2 | Batch of drafts with no model version recorded | Checker asks which tool and model made them | 2 |
| 3 | Drafting model changes from writer-2026-06 to writer-2026-10 | Every rule's canary re-test is queued within 7 days | 3 |
| 4 | Batch from the new model, rule not yet re-tested | Result shows "unchecked", not "pass" | 4 |
| 5 | Phrase list hit rate falls from 54% to 8% with no logged model change | Review ticket opened to the rule owner | 5 |
| 6 | Re-test finds 9 phrases common in new-model drafts and rare in the control set | Phrases listed for the owner; live list unchanged until accepted | 6, hand-off |
| 7 | Image classifier catches 1 of 50 samples on two re-tests in a row | Rule retired or rewritten, reason logged | 7 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Re-tested rule rate** (primary) | 100% within 7 days of a model change | Rule manifests: rules whose `tested_on` includes the current model / all rules in use | Below 100% after 7 days |
| Canary hit rate per rule | Within half of its baseline | Weekly run of each rule on a fixed set of fresh known-AI samples | Below half of baseline |
| Batches published as "unchecked" | Track; set from baseline | Checker log of the "Publish, logged as unchecked" choice | Rising two weeks in a row |
| Samples with no generating-model record | 0 | Checker log: samples with an empty model field / all samples | Any in a week |
| Days from model change to first re-test | 7 or fewer | Model change log vs. earliest new `tested_on` date | Over 14 |
| Control-set flag rate (counter-metric) | Track; set from baseline | Same re-test, human-written control set flagged / control set size | Rising after a list update |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A rule's weekly hit rate falls by half or more | Checker hit log per rule | Writers really did stop pasting AI drafts, or the content mix changed |
| The generating model version in sample logs changed, but no rule's `tested_on` did | Sample log vs. rule manifests | The new version is a pinned alias for the same model |
| A rule matches zero items for 4 weeks while volume holds | Checker hit log | The rule targets a rare tell on purpose |
| Outside reports of "reads like AI" rise while check pass rates stay at or near 100% | Client replies, reader reports, review comments | A one-off complaint about a single piece |
| A rule file has no change in 6 months while two or more model changes were logged | Version control history vs. model change log | Rules re-tested with no change needed, if `tested_on` was updated |

**Starter rule:** show "unchecked", never "pass", for any detection rule whose `tested_on` list does not include the model that produced the output.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: detect-rules-decay
runs: pre_send
reads: [sample.generating_model, rule.version, rule.tested_on, rule.baseline_hit_rate, rule.weekly_hit_rate, model_change_log]
trigger: a check runs on output from a model not in the rule's tested_on list, or a rule's hit rate falls by half or more
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Re-test and update now", "Hold the batch", "Publish, logged as unchecked", "Something else"]
on_miss: ask
metric: re-tested rule rate
counter_metric: control-set flag rate
status: proposed
```

## 8. Related patterns
- [Stock phrases in AI-written text ("delve")](./text-stock-phrases.md) - the closest pattern. It gives the phrase list and the pre-publish block; this page covers what happens to that list, and to any regex or classifier, after the generating model changes, and how to version, re-test and watch it.
- [Em dashes, lists of three and "not X, it's Y"](./text-rhythm-tells.md) - rhythm tells that vendors are already tuning out; a rhythm check needs the same re-test.
- [Silent model update](../../../../reasoning-and-thought/goals/model-updates-and-versioning/failures/silent-model-update.md) - the provider changes the model without notice; that page covers the product's behavior, this one covers the checks that assumed the old model.
- [Tone changes shipped with no regression test](../../measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) - the same missing regression test, applied to the bot's own prompt instead of a detection rule.

## 9. Common questions
### Why did my AI detector stop catching ChatGPT text?
Most likely the rule or classifier was tuned on an older model, and the new one writes differently. Studies opened for this page found detectors that fail on generators they were not trained on. Re-test the rule on fresh samples from the current model (rule 3).

### Does ChatGPT still say "delve"?
One study of arXiv abstracts found "delve" and similar words dropped from April 2024, after they were widely pointed out. The authors credit people editing around it, not only a new model. Either way, a "delve" rule alone now catches less.

### How often should I update my AI writing phrase list?
At every change of the drafting model, and whenever a rule's weekly hit rate falls by half or more. Between changes, a monthly look at new candidate phrases is a reasonable starting point (our judgment).

### Do AI image detectors work on Midjourney or newer generators?
Not reliably unless they were tested on them. In GenImage, a detector trained on Stable Diffusion V1.4 scored 54.9% on Midjourney images, close to a coin flip. Run your own canary set from each generator you need to catch.

### Is a check that passes everything a good sign?
Not on its own. A rule that matches nothing looks the same as a clean draft. Check the rule's hit rate on known AI samples before trusting a 100% pass rate.
