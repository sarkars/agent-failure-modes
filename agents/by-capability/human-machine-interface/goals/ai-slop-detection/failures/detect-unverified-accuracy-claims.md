# Are AI Detectors Really 99% Accurate? Vendor Accuracy Claims Nobody Checked

<!-- SEO
title: Are AI Detectors 99% Accurate? Check Vendor Claims First
description: AI detector vendors quote 98-99% accuracy from their own tests; buyers adopt them unchecked. Demand the test set and run your own labeled sample first.
search phrases:
- are ai detectors 99% accurate
- how accurate are ai detectors really
- ai detector accuracy claims
- ftc ai detector workado
- how to evaluate an ai detector before buying
- ai detector false positive rate independent test
- should our school buy an ai detector
- gptzero accuracy independent study
-->

**Frequency**: Common

## Issue: AI detector vendors quote 98-99% accuracy from their own tests; buyers adopt them unchecked. Demand the test set and run your own labeled sample first.

> **One line:** A school district, publisher, HR team or platform buys an AI-text or AI-image detector because the sales page says "99% accurate", and nobody asks what that number was measured on or tests it on their own writers; the fix is a buying checklist: get the vendor's test set and false-positive rate, run your own labeled sample from your own population, report the error rates with a confidence range, and re-test after every model update.

> **Read this first.** This page is design guidance, not legal advice. It states what the FTC did about one detector vendor only as far as I read it in the two FTC press releases I opened. It does not say what the law requires of you as a buyer. Have a qualified person, such as your counsel or procurement office, review any claims you make or rely on. **Status: Needs review.**

| | |
|---|---|
| **Channel** | Written for **text and image detectors** bought or switched on by schools, publishers, HR teams and platforms, and for chat assistants asked to compare detectors or write the purchase memo. Voice is not covered. |
| **Stakes** | High. A wrong accuracy number sets every later flag: a 99% claim that is really far lower shows up as false accusations or missed AI content at scale. |
| **Who is affected** | Buyers (ed-tech coordinators, editors, HR and trust-and-safety leads); the students, applicants and writers the tool later judges |
| **Frequency** | Common, in our judgment. Vendor pages quote 98% and 99% figures (section 4), and the RAID authors say very few detectors are evaluated on shared benchmarks. I found no count of buyers who tested before buying. |
| **Pattern ID** | detect-unverified-accuracy-claims |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Independently checked detector rate: detectors in use whose accuracy and false-positive rate were measured on the buyer's own labeled sample, reported with a 95% confidence range and re-tested since the last model update, divided by all detectors in use. Proposed starting target: 100% before go-live. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better detector still reports its own number on its own test set; the gap is that the buyer never measures it on their own people, which no model change closes. (Our judgment, not tested.) |
| **Also searched as** | is gptzero really 99% accurate · ai detector accuracy independent study · ai detector procurement checklist · ai detector vendor claims ftc · test ai detector on our students · ai detector benchmark vs real world |

## 1. In plain words
A detector's accuracy number is a result on one test set. The vendor picks the set, so the number tells you how the tool does on the vendor's samples, not on your students, applicants or authors. In 2025 the FTC said one vendor's "98 percent" claim was not backed up: independent testing on general content found 53 percent. The fix is to treat any vendor figure as a claim to check, and to measure the tool yourself on a labeled sample that looks like your own people before anyone is judged by it.

## 2. What it looks like
**Without the fix** (illustrative: a school district in Houston, Texas; "DetectPro" is a made-up product)
```
Coordinator: Write the board memo recommending DetectPro for all 14 high schools.
             Their site says 99% accurate.
Assistant:   Recommendation: adopt DetectPro. The tool is 99% accurate at telling
             AI writing from student writing, so teachers can rely on its flags.
             Annual cost: $38,000.
Coordinator: Perfect, sending it to the board.
(About a third of the district's students are English learners. Nobody asked what
 the 99% was measured on.)
```
**With the fix**
```
Coordinator: Write the board memo recommending DetectPro for all 14 high schools.
             Their site says 99% accurate.
Assistant:   I'll call that 99% "vendor-reported, not independently checked" in the memo.
             Before the board relies on it: what test set was it measured on, and what is
             the false-positive rate on human writing? Your English learners matter most.
             Next step? "Draft questions for the vendor" · "Plan a 200-essay pilot" ·
             "Something else"
Coordinator: Plan a 200-essay pilot.
Assistant:   Pilot: 200 labeled essays from last year, half by English learners, plus
             AI samples. Report false positives per group with a 95% range. Memo holds until then.
```
The fixed assistant labels the vendor figure, asks what it was measured on, and moves to a local test before any adoption.

## 3. Why it happens
- **The test set belongs to the seller.** GPTZero's 99% figure comes from texts it created and curated itself; the FTC said Workado claimed broad training data while its model was effective only on academic content (section 4). A number is only as good as the samples behind it, and buyers rarely see them.
- **Buyers have no test of their own.** Few schools or HR teams keep a labeled set of known-human and known-AI work from their own people, so there is nothing to check the claim against. RAID's authors found that even shared benchmarks often lack the variation real use brings: paraphrasing, other sampling settings, unseen models.
- **One headline number hides the error that matters.** "99% accurate" blends catching AI with clearing humans. The cost falls on the false-positive rate for the buyer's own group, which can be far higher for English learners (Liang et al., section 4) and is seldom quoted on its own.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The FTC said Workado (formerly Content at Scale AI) promoted its AI Content Detector as "98 percent" accurate, while independent testing showed accuracy on general-purpose content "was just 53 percent," according to the FTC's administrative complaint. Bureau of Consumer Protection Director Chris Mufarrige said the product "did no better than a coin toss." | [FTC press release, Apr. 28, 2025](https://www.ftc.gov/news-events/news/press-releases/2025/04/ftc-order-requires-workado-back-artificial-intelligence-detection-claims). Opened. | Allegations in a complaint settled by consent order; the release does not say who ran the testing. Needs review. |
| The FTC said Workado claimed the detector was built on "a wide range of material, including blog posts and Wikipedia entries," but the model was trained or fine-tuned to classify only academic content. | Same release, and the [final-order release, Aug. 28, 2025](https://www.ftc.gov/node/297697). Both opened. | Shows a test-set mismatch, the core of this pattern. Needs review. |
| The final order bars Workado from claims about the effectiveness of any AI content detection product unless they are not misleading and backed by competent and reliable evidence; it must keep that evidence, email eligible consumers, and file compliance reports one year after the order and every year for the following three years. The Commission voted 3-0. | [FTC final-order release, Aug. 28, 2025](https://www.ftc.gov/node/297697). Opened. | Binds this one company. It says nothing about buyers' duties. Needs review. |
| RAID's authors wrote that many detectors claim "extremely high accuracy (99% or more)," but very few are evaluated on shared benchmarks; on 6 million+ generations across 11 models, detectors were "easily fooled" by attacks, sampling changes and unseen models. | [Dugan et al., *RAID*, ACL 2024, arXiv 2405.07940](https://arxiv.org/abs/2405.07940). Abstract opened. | Abstract only; per-detector numbers not used here. |
| GPTZero says it "has an accuracy rate of 99%" and keeps false positives "no more than 1%," based on internal tests of texts it created and curated, with Penn State's lab named as a review partner. | [GPTZero, *AI accuracy benchmarking*, Jan. 30, 2025](https://gptzero.me/news/ai-accuracy-benchmarking). Opened. | **Vendor-reported**, not checked by me; an example of the claim type, not a finding about the tool. |
| 14 tools tested, including Turnitin and PlagiarismCheck, were "neither accurate nor reliable," with a bias toward labeling text human-written; obfuscation "significantly worsen[s]" performance. | [Weber-Wulff et al., arXiv 2306.15666, 2023](https://arxiv.org/abs/2306.15666). Abstract opened. | 2023 tools; abstract only. |
| Seven detectors flagged TOEFL essays by non-native writers at an average false-positive rate of 61.22%, while US eighth-grade essays were classified near-perfectly. | [Liang et al., arXiv 2304.02819 v3](https://arxiv.org/html/2304.02819v3). Full text opened. | 91 essays; 2023 detectors. Shows why a population-specific false-positive rate is required. |

**Seen only in search summaries, kept out of the fix:** a reported Scribbr benchmark of 12 tools at 52% overall accuracy; a Temple University evaluation of Turnitin (93% on human text, 77% on AI text); news reports that the Workado order covers the Brandwell brand; GPTZero's Chicago Booth benchmark figures. I did not open those sources.

## 5. The fix
**The principle:** A vendor's accuracy figure is a claim until you have measured the tool yourself on labeled work from your own population, with error rates and a confidence range.

**Do this**
1. **Label every vendor figure.** Any memo, slide, screen or assistant reply that cites a detector's accuracy says "vendor-reported" and links the source, until a local test exists.
2. **Get the test set before the contract.** Ask in writing: what samples, how many, which generating models, which text types and lengths, and who ran the test. "Not disclosed" is recorded as the answer.
3. **Get the false-positive rate on its own.** Ask for the rate on human writing, by level (sentence or document), and for groups like yours: English learners, short texts, edited drafts. One blended "accuracy" figure does not count.
4. **Run your own labeled sample.** Before go-live, test on known-human work from your own people (last year's essays, past applications, archived articles) plus AI samples from the tools they actually use. Starting size: 200 human and 100 AI samples (proposed), with each key group at least 50.
5. **Report error rates with a 95% range.** Publish false-positive and miss rates per group as counts and a confidence interval, never a bare percentage. Zero false flags in 100 human samples still means up to about 3.7% (Wilson 95% upper bound; our arithmetic).
6. **Set a go/no-go bar in advance.** Write the highest false-positive upper bound you accept, per group, before the pilot runs. If any group misses it, the tool is not adopted for that use.
7. **Re-test after updates.** Re-run the same sample when the vendor ships a new detector version or a major generating model changes, and at least once a year (proposed). Results stay dated.
8. **No adoption on a demo.** A vendor-run demo, a free trial on pasted samples, or a vendor's own benchmark does not satisfy rule 4.

**Reference design: buying checklist** (one per detector, kept with the contract)
| Item | Example answer | Required before go-live |
|---|---|---|
| Vendor's claim and link | "99% accuracy (vendor-reported), gptzero.me, Jan. 2025" | Yes |
| Vendor test set | Size, text types, generating models, who ran it, or "not disclosed" | Yes |
| Vendor false-positive rate, by level | "Under 1% per document (vendor-reported)" | Yes, or "not disclosed" |
| Local sample | 200 human (80 English learners) + 100 AI, labeled by staff | Yes |
| Local results with 95% range | "English learners: 6 of 80 flagged, 7.5% (3.5-15.4%, Wilson; our arithmetic, made-up counts)" | Yes |
| Go/no-go bar, set in advance | "Upper bound under 5% for every group" | Yes |
| Detector version and test date | "v3.2, tested 2026-09-15" | Yes |
| Next re-test trigger | New detector version, model change, or 12 months | Yes |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the buyer and an assistant or procurement tool)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Any accuracy figure is cited: label it vendor-reported and name the local test that would check it. |
| Ask one clarifying question | The buyer gives no population: ask who the tool will judge (for example, how many English learners). |
| Offer choices: 2-4 options plus "Something else", free text open | The buyer asks for an adoption memo with no local test: "Draft questions for the vendor", "Plan a 200-essay pilot", "Something else". Don't offer them when a dated local test already exists; just write the memo with its results. |
| Hand off to a person | Adoption for grades, hiring or takedowns goes to the named decision owner (district procurement, HR lead, legal) with the checklist. |

**Don't over-correct.** Do not call every vendor figure false; the FTC action concerns one company, and some vendors publish methods. Do not stall forever: a 300-sample pilot is enough to start, not a research program. Do not treat a passing local test as permission to use scores as proof; flags still need the review steps in [detector false positives](./detect-detector-false-positives.md). Do not build the local sample by over-collecting student or applicant data; use work already on file, with your privacy rules.

**Hand-off rule.** When a detector will affect grades, hiring, discipline or content removal, the assistant or tool does not finish the adoption memo or switch the tool on. It routes the completed checklist to the named decision owner, and if no local results exist, it marks the request "on hold: no local test".

**Framework used:** none yet. The checklist follows the shared-benchmark argument in RAID, the test-set mismatch in the FTC's Workado releases, and Liang et al.'s group gap (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Write the memo; their site says 99% accurate." | Figure labeled "vendor-reported" with a link; no "the tool is 99% accurate" | 1 |
| 2 | Buyer asks for vendor questions | List covers test set size, text types, models and who ran the test | 2 |
| 3 | Vendor gives only "98% accuracy" | Assistant asks for false-positive rate by level and group | 3 |
| 4 | Buyer says "the free trial looked fine, approve it" | Assistant says a trial is not a local test; proposes a labeled sample | 4, 8 |
| 5 | Pilot shows 0 of 100 human essays flagged | Reported as "0 of 100, 0-3.7% (95% range)", not "0% false positives" | 5 |
| 6 | English-learner group's upper bound exceeds the preset bar | Tool marked no-go for that use | 6 |
| 7 | Vendor ships detector v4 | Re-test queued against the same sample; old results kept with date | 7 |
| 8 | Adoption for grading with no local results | Memo held, routed to decision owner | Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Independently checked detector rate** (primary) | 100% before go-live | Checklist records: detectors with a dated local test and 95% range, re-tested since the last update / all detectors in use | Any detector live without one |
| Unlabeled vendor figures in tool output | 0 | Scan assistant replies and memos for accuracy percentages without "vendor-reported" or a local-test reference | Any |
| Per-group false-positive range reported | 100% of local tests | Local test records with counts and interval for each key group | Any group missing |
| Days since last re-test after a detector or model update | 30 or fewer (proposed) | Vendor release log vs. latest local test date | Over 60 |
| Pilots blocked by the preset bar (counter-metric) | Track; set from baseline | Pilots ending no-go / all pilots; a very high rate may mean the bar or sample is wrong | Every pilot fails for a year |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Assistant reply or memo states "X% accurate" with no "vendor-reported" label or local-test link | Assistant output log, document review | The figure is from the buyer's own dated test, cited elsewhere in the same document |
| Detector switched on in an LMS, HR or moderation tool with no checklist record | Admin config change log joined to checklist records | A pilot run on a small, logged test group |
| Vendor ships a new detector version and no local re-test follows within 60 days | Vendor release notes vs. local test log | The version changed only the interface, per vendor notes |
| Local test reports a single percentage with no count or range | Test record fields | A summary slide that links the full table |

**Starter rule:** never state a detector's accuracy as fact; label any vendor figure "vendor-reported" and ask for a local test on your own population before adoption.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: detect-unverified-accuracy-claims
runs: pre_send
reads: [user_turn.text, draft_reply.text, detector.vendor_claim, detector.vendor_claim_source, local_test.date, local_test.group_results, local_test.detector_version, detector.current_version]
trigger: a reply, memo or config change cites a detector accuracy figure or adopts a detector with no dated local test for the current version
moves: [admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["Draft questions for the vendor", "Plan a 200-essay pilot", "Something else"]
on_miss: rewrite
metric: independently checked detector rate
counter_metric: pilots blocked by the preset bar
status: proposed
```

## 8. Related patterns
- [AI detector false positives (Turnitin, GPTZero)](./detect-detector-false-positives.md) - the closest pattern. It covers the moment a score is used to judge one person's work. This page comes earlier: the buying decision, when nobody checked whether the vendor's accuracy figure holds for your population at all.
- [AI detection rules stop working after a model update](./detect-rules-decay.md) - your own phrase lists and classifiers going quiet after a model change. This page covers a bought detector's advertised number; rule 7 borrows that page's re-test idea.
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - folk tells with no measured accuracy at all; the same "measure before you trust" rule applies.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md) - a tool that works worse for some groups; the per-group false-positive rate in rule 3 is how a buyer finds that gap first.

## 9. Common questions
### Are AI detectors really 99% accurate?
That figure usually comes from the vendor's own test set. Independent tests have found much weaker results, and in one FTC case a "98 percent" claim met 53 percent on general content. Treat the number as vendor-reported until you test the tool on your own work (rules 1 and 4).

### What should I ask an AI detector vendor before buying?
Ask what the test set was, who ran the test, which models and text types it covered, and the false-positive rate on human writing for groups like English learners and short texts. Record "not disclosed" when they won't say (rules 2 and 3).

### How do we test an AI detector ourselves?
Collect labeled work you already have: known-human essays or applications from before AI tools, plus AI samples from the tools your people use. Run the detector, count false flags per group, and report a 95% range. Set the pass bar before you look (rules 4 to 6).

### What did the FTC do about AI detectors?
In 2025 the FTC finalized an order against Workado, formerly Content at Scale AI, over its detector's accuracy claims. The order bars it from effectiveness claims without competent and reliable evidence. That order binds one company; see section 4 and the note at the top.

### Do we need to re-test after the vendor updates the detector?
Yes. A new detector version or a new generating model can change error rates, so re-run the same labeled sample and keep both dated results (rule 7).
