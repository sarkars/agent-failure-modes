# Model Collapse from AI-Generated Training Data: Filtering AI-Written Web Pages Before You Fine-Tune

<!-- SEO
title: Model Collapse From AI-Generated Training Data
description: Teams that train on scraped web or user data now ingest AI-written text; tag provenance, keep a dated human set and add synthetic data, never swap it in.
search phrases:
- model collapse ai generated training data
- training llm on ai generated text
- how to filter ai generated content from training data
- is common crawl contaminated with ai text
- pre-2022 data for training ai
- synthetic data model collapse accumulate vs replace
- fine-tuning on scraped web data ai content
-->

**Frequency**: Common

## Issue: Teams that train on scraped web or user data now ingest AI-written text; tag provenance, keep a dated human set and add synthetic data, never swap it in.

> **One line:** A team refreshes its fine-tuning set from a new web crawl, support tickets or crowd labels, and a growing share of that "human" data was written by AI, sometimes by the team's own model; each retrain loses rare cases and drifts toward bland, average output. The fix is to tag every training record with its source and collection date, keep a frozen human reference set that is never replaced, add synthetic data on top instead of swapping it in, and block a retrain when rare-case quality drops.

| | |
|---|---|
| **Channel** | Written for the **builder's data pipeline**: web scrapes, crawl snapshots, user-submitted text, crowd-labeled data and an assistant's own logged outputs used for fine-tuning or pretraining. It affects every channel the trained model later serves. |
| **Stakes** | High. The harm is slow and hard to undo: rare customer cases, minority dialects and edge-case answers fade first, and the damage carries into every later model trained on the same pool. |
| **Who is affected** | ML and data engineers who build training sets; users whose questions are rare or unusual; teams that later inherit the dataset |
| **Frequency** | Common, in our judgment. A press summary of an August 2026 Pew study puts AI-written pages at about 10% of a Common Crawl sample, and one 2023 study estimated 33-46% of crowd workers used LLMs on a summarization task (section 4). I found no count of teams whose models degraded from it. |
| **Pattern ID** | data-model-collapse-contamination |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Provenance-tagged record rate: training records with a source, a collection date and an origin label (human, synthetic, unknown), divided by all records in a training run. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The loss comes from what the training data contains, not from model strength; a stronger model trained on its own outputs still learns from a narrower copy of the world. (Our judgment, not tested.) |
| **Also searched as** | ai inbreeding · model autophagy disorder · training on synthetic data degradation · llm trained on its own output · ai pollution of training data · low-background steel data |

## 1. In plain words
More of the web is now written by AI. If you scrape it, or collect text from users or crowd workers who paste AI output, your training set quietly fills with machine text. Models trained this way keep the common patterns and lose the rare ones, and each new round makes it worse. The fix is bookkeeping: know where every record came from and when, keep a fixed set of real human data that you never throw out, and test for the rare cases before you ship a retrain.

## 2. What it looks like
**Without the fix** (illustrative: a tax-help startup in Austin, Texas, retraining its support model)
```
Engineer:  Refresh the fine-tune set. Pull the 2026 forum crawl plus last quarter's tickets.
Data tool: Done. 410,000 records, dedup applied. Old 2021 forum set dropped as stale.
           Train/eval split from the same pool. Eval loss improved 4%.
Engineer:  Ship it.
(Two weeks later: answers on rare cases, such as farm income or a part-year
 resident of two states, come back as generic "consult a tax professional" text.
 A third of the new forum posts were drafts written by the old support bot.)
```
**With the fix**
```
Engineer:  Refresh the fine-tune set. Pull the 2026 forum crawl plus last quarter's tickets.
Data tool: 410,000 records tagged. Origin: 61% human-verified or pre-Dec-2022,
           27% unknown, 12% matched our own bot's logged outputs (excluded).
           The 2021 human reference set is kept, not replaced.
           Rare-case eval (farm income, multi-state): 3 of 40 answers got worse. Retrain blocked.
           Options: drop the unknown slice, cap it at its current share, or send the 40 to review.
Engineer:  Drop the unknown slice and rerun.
```
The fixed tool reports origin by source, removes the team's own bot text, keeps the old human data, and checks rare cases instead of trusting a pooled eval loss.

## 3. Why it happens
- **Scrapes and user data carry no origin label.** A forum post, ticket or crowd label written with a chatbot looks like any other text, and most pipelines store only the text and a URL, not who or what wrote it or when.
- **Refreshes replace old data instead of adding to it.** Teams drop "stale" sets to save compute or to reflect current topics. In one study, replacing real data with each generation's synthetic output tended toward collapse, while keeping it did not (section 4).
- **The eval set comes from the same polluted pool.** If the test split is drawn from the new crawl, it rewards the model for matching AI-average text, and a pooled loss hides losses on rare cases, which are the first to go.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Training on data produced by earlier models causes "irreversible defects" in which the tails of the original distribution disappear; the authors call it model collapse and report it in LLMs, variational autoencoders and Gaussian mixture models. | [Shumailov et al., *AI models collapse when trained on recursively generated data*, Nature 631, July 24, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11269175/). Opened and read (PubMed Central copy). | Lab setting: each generation is trained only on the previous model's output, which is harsher than a real web scrape. |
| In the same paper, OPT-125m fine-tuned on wikitext2 lost performance when no original data was kept ("from 20 to 28 perplexity points"); keeping a random 10% of the original data each generation gave "only minor degradation". | Same paper, LLM experiments. Opened and read. | Small model, one dataset. Supports rule 2, not a recommended ratio. |
| The authors say "access to the original data distribution is crucial" and that telling LLM-generated data apart "raises questions about the provenance of content"; they suggest community-wide coordination. | Same paper, discussion. Opened and read. | A recommendation, not a tested method. |
| Replacing real data with each generation's synthetic data "does indeed tend towards model collapse"; accumulating synthetic data alongside the original real data "avoids model collapse", across language models, diffusion models and VAEs. | [Gerstgrasser et al., *Is Model Collapse Inevitable?*, arXiv 2404.01413, April 2024](https://arxiv.org/abs/2404.01413). Opened (abstract page). | Preprint; I read the abstract, not the full paper. Basis for rule 2. |
| Without "enough fresh real data in each generation" of a self-consuming loop, models lose quality or diversity; the authors call it Model Autophagy Disorder. | [Alemohammad et al., *Self-Consuming Generative Models Go MAD*, arXiv 2307.01850, July 2023](https://arxiv.org/abs/2307.01850). Opened (abstract page). | Image models mainly; abstract only. |
| An estimated 33-46% of Amazon Mechanical Turk workers used LLMs on an abstract summarization task. | [Veselovsky, Ribeiro and West, arXiv 2306.07899, June 2023](https://arxiv.org/abs/2306.07899). Opened (abstract page). | One task that suits LLMs well; the authors say other tasks are unclear. Basis for rule 5. |
| Pew analyzed nearly half a million English pages from Common Crawl with the Open Pangram detector: about 10% showed clear signs of AI authorship, more than a third of pages published after late 2022 did, and .edu and .gov pages were about 1%. | [The Decoder, Aug. 24, 2026, summarizing Pew Research Center, Aug. 20, 2026](https://the-decoder.com/pew-study-shows-ai-written-text-has-surged-across-the-web-since-late-2022/). Opened. | Secondhand: the Pew page returned an error when I tried to open it. Detector-based, so a rough estimate with per-page errors. |
| A researcher quoted in the press says data collected before 2022 can be assumed to have "minimal, if any, contamination"; the same article reports doubt about how big a problem model collapse will be. | [The Register, Thomas Claburn, June 15, 2025](https://www.theregister.com/2025/06/15/ai_model_collapse_pollution). Opened and read. | Press article; the cutoff is an approximation, not a measured line. |

**Seen only in a search summary, kept out of the fix:** a Harvard JOLT digest reportedly says date metadata cannot reliably separate pre- and post-2022 data. I did not open it.

## 5. The fix
**The principle:** Know where every training record came from and when, keep real human data in every run, and prove rare cases did not get worse before a retrain ships.

**Do this**
1. **Tag every record.** Each training record carries `source`, `collected_at`, `first_seen_at` (crawl or archive date) and `origin` (`human_verified`, `pre_cutoff`, `synthetic`, `own_model`, `unknown`). Records without a tag do not enter a training run.
2. **Accumulate, never replace.** A frozen human reference set (verified human text, or text first seen before your chosen cutoff, such as December 2022) is included in every training run. A refresh adds data; it never drops the reference set.
3. **Exclude your own model's output.** Log a hash of every output your assistant sends. Scraped or user-submitted records that match a logged output are tagged `own_model` and excluded unless a person adds them on purpose as labeled synthetic data.
4. **Report AI share as an estimate per source.** Run a detector over each source and crawl date and report the share with its known error rate. Use it to set source-level caps and to choose sources, never to delete or label single documents as AI.
5. **Check crowd and user labels.** For paid labeling, record paste events and time-on-task, and keep a slice labeled by checked in-house reviewers. Compare the two before using the crowd set.
6. **Evaluate on held-out human data and rare cases.** The eval set comes from the reference set, not the new pool, and includes a named rare-case slice. A retrain that is worse on the rare slice is blocked, even if pooled loss improved.
7. **Label synthetic data you add on purpose.** Synthetic records are tagged `synthetic` with the generator and date, and their share of each run is recorded.

**Reference design: training-set gate**
| Check | What it looks at | Action on hit |
|---|---|---|
| Untagged records | Records missing `source`, `collected_at` or `origin` | Block run |
| Reference set missing | Frozen human set not fully in the run manifest | Block run |
| Own-model match | Record hash or near-duplicate matches the assistant's output log | Exclude record |
| Unknown-origin share rising | `unknown` share by source vs. the last run (proposed flag: up more than 10 points) | Human review |
| Rare-case regression | Any rare-slice item scored worse than the current model (proposed: 2 or more of 40) | Block run |
| Diversity drop | Distinct n-gram ratio or embedding spread of sampled outputs vs. the current model | Human review |
| Eval leak | Eval records drawn from the new pool instead of the reference set | Block run |

**Run manifest (one per training run)**
```yaml
run_id: support-ft-2026-10
reference_set: human-ref-2021-v3   # frozen, never removed
cutoff_date: 2022-12-01
origin_share: {human_verified: 0.31, pre_cutoff: 0.30, synthetic: 0.00, unknown: 0.27, own_model_excluded: 0.12}
detector: {name: <tool>, version: <v>, false_positive_rate_on_our_sample: <measured>}
rare_slice: {items: 40, worse_than_current: 3}
decision: blocked
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the data tool reporting to the engineer)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The tool reports AI share: it gives the estimate, the detector's error rate and the sampled records so a person can read them. |
| Offer choices: 2-4 options plus "Something else", free text open | A gate blocks a run: "Drop the unknown slice", "Cap it at its current share", "Send the rare cases to review", "Something else". |
| Ask one clarifying question | A source has no collection date: the tool asks once for the archive date or crawl ID before tagging it `unknown`. |
| Hand off to a person | The rare-case slice gets worse twice in a row: the data owner reviews the sources before any further retrain. |

**Don't over-correct.** Do not throw out all post-2022 data: it holds new products, laws and slang your users ask about, and a frozen 2021 set alone goes stale. Do not delete single documents because a detector flagged them; detectors misfire, and English learners' writing is flagged more often (see the detector page in section 8). Do not ban synthetic data: the accumulation study shows it can be added safely when real data stays in the mix.

**Hand-off rule.** When a retrain is blocked by a rare-case regression twice in a row, or when no source can supply a collection date for more than a quarter of the records, the named data owner decides before any further run, and the current model stays in production.

**Framework used:** none yet. The rules draw on the accumulate-not-replace result (Gerstgrasser et al.) and the "preserve the original data" finding (Shumailov et al.), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | New crawl records arrive with URL only, no date | Gate blocks the run until records are tagged or marked `unknown` | 1 |
| 2 | Refresh job config drops the 2021 human set as stale | Gate blocks: reference set missing | 2 |
| 3 | 5,000 forum posts match hashes in the assistant's output log | All 5,000 excluded and counted in the manifest | 3 |
| 4 | Detector flags 18% of one source | Report shows share, error rate and samples; no single record deleted | 4 |
| 5 | Crowd labels show heavy paste events | Crowd set compared with the in-house slice before use | 5 |
| 6 | Pooled eval loss improves, rare slice gets worse on 3 of 40 | Run blocked | 6 |
| 7 | Eval split drawn from the new crawl | Gate blocks: eval leak | 6 |
| 8 | Team adds 20,000 generated Q&A pairs on purpose | Tagged `synthetic`, share recorded, reference set still present | 2, 7 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Provenance-tagged record rate** (primary) | 100% | Run manifest: tagged records / all records | Below 100% on any run |
| Reference-set inclusion | 100% of runs | Manifest lists the frozen set in full | Any run without it |
| Own-model records in training | 0 | Hash and near-duplicate match against the output log | Any |
| Rare-slice regressions shipped | 0 | Rare-slice eval per run vs. the model in production | Any |
| Unknown-origin share | Flat or falling run to run | Manifest `origin_share.unknown` | Rise of more than 10 points |
| Over-filtering rate (counter-metric) | Under 20% | Monthly review of 30 records removed by caps or filters, labeled human or AI by a person | Over 40% human |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Estimated AI share in a source rises from one crawl date to the next | Per-source detector report in the run manifest | Detector update or a change in which pages were crawled |
| Scraped or user records match the assistant's own logged outputs | Hash or near-duplicate join against the output log | Users quoting the bot on purpose in a complaint ticket |
| Sampled outputs from the new model use fewer distinct phrases than the current model on the same prompts | Diversity eval on a fixed prompt set | A deliberate style tightening in the fine-tune |
| Rare-slice scores fall while pooled loss improves | Eval report per run | A rare-slice item whose correct answer changed (a new tax rule) |
| Crowd labels arrive with paste events and very short time-on-task | Labeling platform event log | Workers pasting from the provided source text |

**Starter rule:** block a training run when any record lacks a source, collection date and origin tag, or when the frozen human reference set is missing.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: data-model-collapse-contamination
runs: pre_send
reads: [run_manifest.records, run_manifest.origin_share, run_manifest.reference_set, output_log.hashes, eval.rare_slice, eval.source]
trigger: a training or fine-tuning run is about to start, or a retrained model is about to replace the one in production
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Drop the unknown slice", "Cap it at its current share", "Send the rare cases to review", "Something else"]
on_miss: ask
metric: provenance-tagged record rate
counter_metric: over-filtering rate
status: proposed
```

## 8. Related patterns
- [Model collapse in generation](../../../../vision-and-images/goals/generation-artifacts/failures/model-collapse.md) - the closest page by name. It covers mode collapse in an image generator fine-tuned on narrow data, fixed with diversity losses. This page covers the data-pipeline cause: AI-written text entering scraped and user data, fixed with provenance tags, a kept human set and a rare-case gate.
- [Provenance metadata stripped](./provenance-metadata-stripped.md) - labels removed from files on the way to users. Here, the same missing labels make it impossible to tell AI text from human text in a training scrape.
- [AI detector false positives](./detect-detector-false-positives.md) - why rule 4 uses detector scores only as source-level estimates, never as per-document verdicts.
- [Unverified detector accuracy claims](./detect-unverified-accuracy-claims.md) - measure a detector's error rate on your own sample before you use its share estimate.
- [AI made-up numbers in reports](./data-too-clean.md) - invented figures in one report. This page is about invented text at training-set scale.
- [AI generated reviews that all sound the same](./data-templated-reviews.md) - templated review text is one common source of AI-written records in a scrape.

## 9. Common questions
### What is model collapse in simple terms?
It is what happens when models are trained on text or images made by earlier models instead of by people. Rare cases drop out first, and over rounds the model drifts toward a narrow, average version of the data. Shumailov et al. showed it in language and image models (section 4).

### Is it safe to fine-tune on data scraped from the web in 2026?
It can be, if you know where each record came from and keep real human data in the mix. Tag every record, keep a frozen human set, exclude your own bot's text, and test rare cases before shipping (section 5).

### Does adding synthetic data always cause model collapse?
No. In one study, swapping real data out for synthetic data led toward collapse, but adding synthetic data on top of the original real data did not. Keep the real data and label what is synthetic.

### Should I only train on data from before 2022?
No. Pre-2022 data is a useful reference set, but it misses everything that happened since. Use it as the anchor that is always included, and add newer data with origin tags.

### Can an AI detector clean my training data?
Not record by record. Detectors make errors on single documents, so use them to estimate the AI share of a source and to set caps, and check their error rate on your own sample first.
