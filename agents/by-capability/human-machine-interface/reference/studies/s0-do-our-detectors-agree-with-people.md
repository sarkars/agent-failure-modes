# Study S0 (preregistration): do our detectors agree with people?

This page is the preregistered protocol for study S0, written for developers, conversation designers and researchers who want to check how well the proposed failure detectors in this library match what trained people label in the same chat transcripts.

> **Status: Designed, not run. No results exist.** Written 2026-10-22 and not yet reviewed. No transcripts exist yet and no one has labeled any. Every threshold and sample size below is a starting point we chose, not from a source. The transcripts will be simulated, on reference bots we configure, and labeled as simulated. The study says nothing about real customers or any commercial product.

## 1. Research question
When people read a chat transcript and say whether a failure happened, do our detectors say the same? A detector is one row of a pattern page's "Detection signals" block, the signals combined, or an LLM judge asked to apply the page's starter rule. We ask three things: how often a flag is right (precision), how many real failures it finds (recall), and how well it agrees with people beyond chance (Cohen's kappa). We also ask how well two people agree with each other, because a detector cannot agree with people more than they agree with themselves.

This is study S0 in the [chat analytics plan](../../roadmap/chat-analytics-plan.md), which says nothing else is credible without it. Studies S1 and S2 depend on it ([S1](s1-talk-to-a-human-within-two-turns.md), [S2](s2-do-corrections-stick.md)). Terms follow the [glossary](../glossary.md) and [metrics](../metrics.md).

## 2. Hypotheses
Each hypothesis can be wrong. "Trustworthy" is defined in section 5. All marks (0.70, 0.80, 10 pp) are starting points we chose before seeing data. The pattern pages call their signals proposed and uncalibrated, so we expect some to fail.

| # | Hypothesis | Pattern ID(s) tested | Falsified if |
|---|---|---|---|
| H1 | The rule signals for a human request that gets no handoff (a request label, then a bot turn that is not a handoff, route or stated wait) meet the trustworthy bar. | `talk-to-a-human-ignored-or-looped` | Precision or recall has a 95% interval lower bound under 0.70, or kappa against adjudicated labels is under 0.70. |
| H2 | The signals that compare the action's parameters and the summary with the corrected value meet the bar. They read structured fields, so they should do best. | `corrections-not-applied` | Same rule as H1. |
| H3 | The generic-template signal meets the bar, but "user ends the session within 1 turn of an error" has precision under 0.50, because users leave for other reasons. | `generic-error-messages` | The end-of-session signal's precision is 0.50 or higher, or the template signal misses the bar. |
| H4 | "3 or more consecutive fallback turns" meets the bar, and "identical fallback twice in a row" has recall under 0.60 because bots reword the line. | `dead-end-i-don-t-understand-replies` | Consecutive-fallback signal misses the bar, or the identical-reply signal's recall is 0.60 or higher. |
| H5 | Two trained people label failure present or absent with kappa of 0.70 or higher for each of the four patterns under the label guide, after the guide is revised once. | all four patterns above | Any pattern's human-human kappa is under 0.70 after one revision of the guide. That pattern's detectors are then not scored as trustworthy. |
| H6 | An LLM judge applying each starter rule agrees with the adjudicated labels at kappa 0.70 or higher, and gives the same verdict when the order of two items is swapped in at least 90% of pairs. | all four patterns above | Judge kappa is under 0.70 for a pattern, or swap consistency is under 90%. |

## 3. Design
### 3.1 Where the transcripts come from
- **Simulated only.** Transcripts come from the reference-bot runs of S1 and S2: configurations C0 to C3 across at least three models, with scripted simulated users. Every transcript carries `source: simulated` and its config, model string and seed. No result from S0 may be quoted as a result on real users.
- **Tool failures for errors.** S1 and S2 produce few errors. For `generic-error-messages` we add runs where a stub tool fails on a fixed turn (timeout, rejected input, unavailable service), with C0 prompts and with prompts that follow the pattern page's starter rule.
- **Event fields.** The harness writes the event fields the signals read (request label, correction event, fallback flag, error event) from the script. Real logs would need those labels produced by a classifier, which S0 does not test.
- **Real transcripts are out of scope for now.** They would need consent from the people in them, redaction before storage, and a design partner. The plan lists these as open decisions. S0 v2 would add them after that.

### 3.2 Sample (starting points)
- **Pool:** 1,200 simulated transcripts across the four patterns, 300 per pattern. Each is read for its own pattern only.
- **Labeled per pattern: 120.** 60 are drawn at random from transcripts a detector flagged, and 60 at random from transcripts no detector flagged. The second group is what lets us estimate recall. Estimates are re-weighted by stratum size, and the weights are published.
- **Why 60 and 60.** With about 60 items, a 95% Wilson interval around 0.85 is roughly 0.74 to 0.92 (our arithmetic, not a source). That is enough to catch a detector under 0.70 and not enough to rank two good ones. We add 60 more per cell if an interval in a main test is wider than 0.20.
- **Total labels:** 480 transcripts, plus second labels (3.4).

### 3.3 Label guide
One page per pattern, written before any labeling, versioned, and published.
- **Unit and question.** One transcript. "Did this failure happen? Present, absent, or cannot tell." Present means the pattern page's issue line is true on this transcript. The guide gives 4 examples of present and 4 of absent per pattern, including near misses that match a counter-signal.
- **Where it happened.** The labeler marks the first turn where it is clear. This lets us score a flag as right only if it points at the failure, not at some other turn.
- **Rules.** Judge what the bot said and did, not whether the user was polite. Use the starter rule on the page as the standard. Do not guess at intent. If two reasonable readings exist, mark "cannot tell" and write why.
- **Blind.** Labelers see the transcript only. They never see detector output, judge output, configuration, model or which stratum an item came from. Order is shuffled.
- **Labelers.** Three people, none of whom wrote the detectors. We name and describe them (role, training) in the results page.
- **Training.** All three label the same 20 practice transcripts per pattern and talk through every disagreement. Practice items are discarded from scoring. The guide is revised once, then frozen.

### 3.4 Double labeling and adjudication
- **Double-label 25% of all transcripts**, chosen at random, plus every transcript where a detector and the first labeler disagree. The second person is chosen at random from the other two.
- **Adjudication.** The third person labels disagreements without seeing either label's author, then the three talk it through if needed. The adjudicated label is the reference for scoring detectors. Items that remain "cannot tell" are reported and left out of precision and recall.
- **Human-human agreement** is computed on the double-labeled set before adjudication, so it is not inflated by the discussion.
- **Drift check.** 10 transcripts are relabeled by the same person two weeks later.

## 4. Metrics and method
### 4.1 Detector metrics
- **Precision** = flagged transcripts the reference label calls present, divided by flagged transcripts.
- **Recall** = transcripts the reference label calls present that the detector flagged, divided by those present.
- **Per-signal and combined.** Every signal is scored alone. "Any signal" is scored as one detector. A signal that adds flags but no recall is reported as noise.
- **Location match.** A flag counts as right only if its turn is within one turn of the labeler's first clear turn.
- **Counter-signal check.** For each pattern, we report how many false flags match the page's listed counter-signal. If most do, the page's counter-signal is not working and we say so.

### 4.2 Agreement
- **Cohen's kappa** for two raters on a present/absent label, and percent agreement beside it. McHugh explains that percent agreement may overestimate agreement because it ignores guessing, that kappa corrects for chance but may lower the estimate too much, and recommends reporting both ([McHugh 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3900052), opened 2026-10-22, read in full).
- **Prevalence.** We report how often "present" occurs next to every kappa. McHugh notes that the greater the expected chance agreement, the lower the kappa. With few failures in a stratum, kappa can be low while agreement is high, so we do not read a kappa alone.
- **Detector versus adjudicated labels.** Detector output is treated as one more rater, and the same kappa is computed.
- **If we later use three or more raters at once**, we add Krippendorff's alpha. Artstein and Poesio survey these coefficients for annotation ([Artstein and Poesio 2008, Computational Linguistics 34(4)](https://aclanthology.org/J08-4004/)). We opened only that page's record, not the paper, so we take nothing from its text.
- **Intervals.** Proportions get 95% Wilson score intervals, as in S2. Kappa gets a 95% bootstrap interval over transcripts (10,000 resamples). We did not open a source for the Wilson interval, so it is a method choice and not a cited claim.

### 4.3 LLM-judge reliability
- **Judge task.** The judge reads the transcript and the starter rule and answers present, absent or cannot tell, with the turn number. Prompt, model string and temperature are published. At least two judge models are tried, and the judge never is the model that wrote the bot's reply.
- **Agreement with people.** Judge kappa and percent agreement against the adjudicated labels, and against each single human label, beside the human-human numbers. Zheng et al. compare a GPT-4 judge with people on pairwise answer preferences and report the judge's agreement at 66% (random baseline 33%) and 85% (random baseline 50%) across two setups, against 63% and 81% between humans ([Zheng et al. 2023](https://arxiv.org/abs/2306.05685), opened 2026-10-22 as the full HTML version). Their task is choosing the better answer, not finding a failure in a transcript, so we use it as a design model and not as a baseline.
- **Position bias.** Zheng et al. report GPT-4 gave consistent verdicts after the answer positions were swapped in 65.0% of cases under their default prompt, with 30.0% favoring the first position. S0 swaps item order in pairs and reports consistency. Our 90% mark is a number we chose.
- **Other checks.** Repeat the same judge call three times and report how often the verdict changes. Compare judge errors on long versus short transcripts. We do not test self-enhancement bias; Zheng et al. say their data could not settle it.

## 5. Pass bar: "detector is trustworthy" (starting point we chose)
A detector (a signal, or all signals combined) is **trustworthy for research use** only if all hold on the S0 sample:
1. The pattern's human-human kappa is 0.70 or higher (H5). If not, the guide is wrong, not the detector, and the pattern waits.
2. Precision and recall each have a 95% interval lower bound of 0.70 or higher.
3. Kappa against adjudicated labels is 0.70 or higher, with percent agreement shown.
4. At most 25% of false flags match the page's listed counter-signal.

A judge must meet 1 to 3, plus 90% swap consistency. A detector that fails is called "not yet trustworthy", with its numbers. It stays on the pattern page as proposed.
**Why 0.70.** McHugh's table reads kappa .60 to .79 as moderate, .80 to .90 as strong, and says kappa below 0.60 is inadequate. Our 0.70 sits inside the moderate band, is above his floor, and is below strong. We chose it for a first pass on simulated text. It is not his number and not a standard.
Use this bar to gate S1 and S2: S2 already publishes as "experimental" below 0.70 judge agreement, and the plan holds the conversion layer until S0 passes.

## 6. Analysis plan
- **Primary:** precision, recall and kappa per signal and per pattern, with the intervals above, then human-human kappa, then judge numbers.
- **Falsification:** we apply each rule in section 2 as written. We do not move marks after seeing data.
- **We report even if null:** if every detector passes, or none does, we publish it with the same prominence. Failed signals are named.
- **Disagreement review:** we read every false positive and false negative and sort them by cause (label guide gap, detector rule, simulator artifact, real ambiguity). Counts are descriptive and labeled exploratory.
- **Exploratory:** results by model, by configuration and by transcript length.

## 7. Threats to validity
- **Simulated text is cleaner than real chat.** Detectors may look better here than on real logs. Only real, consented transcripts can say, and S6 tests the simulator.
- **The harness writes the event fields.** That removes the hardest step, labeling a request or a correction from raw text.
- **Enriched sample.** Stratified sampling needs correct weights. Errors there bias recall.
- **Same-lab labelers.** Labelers know the project. Blinding limits this and does not remove it.
- **Few raters.** Three people is a small panel. Results are about this panel and this guide.
- **Judge and bot drift.** Hosted models change. We record version strings and run dates.
- **One setting.** English, US, text chat, invented businesses. We found no opened source that gives a trusted agreement bar for failure detectors on chat, so the bar in section 5 has no outside baseline.

## 8. Out of scope
- **Real customers, live traffic and real transcripts.** Consent and redaction are unsettled.
- **Voice agents.** The pages call voice signals planned.
- **The other 252 patterns.** Four patterns first. Others follow if the method works.
- **Whether a failure matters to users.** S0 checks agreement on labels, not harm.
- **Naming or ranking commercial products.**

## 9. Data and materials to be published
Before the run, with a frozen date: this protocol, the four label guides with examples, detector rules, judge prompts, sampling code, and the labeler roster. After the run: transcripts (all synthetic), all labels with labeler IDs, adjudications, detector and judge outputs, model version strings and run dates, and analysis code.

## 10. Prior work and sources
Searches run on 2026-10-22: four (kappa interpretation, LLM-as-judge agreement, annotation-agreement coefficients, binomial interval methods).
- **Opened and read:** McHugh 2012 (full text); Zheng et al. 2023 (arXiv HTML, full text via the fetch tool's answer to specific questions).
- **Opened, record only:** Artstein and Poesio 2008 (page had no abstract; the PDF would not convert to text).
- **Not opened, not used for any number:** Brown, Cai and DasGupta on binomial intervals (both fetches failed or returned nothing).

## 11. Changes log
| Date | Change |
|---|---|
| 2026-10-22 | First draft of the protocol. Not run. |

## Related
[Chat analytics plan](../../roadmap/chat-analytics-plan.md) · [S1 preregistration](s1-talk-to-a-human-within-two-turns.md) · [S2 preregistration](s2-do-corrections-stick.md) · [Glossary](../glossary.md) · [Metrics](../metrics.md) · [Talk to a human ignored or looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) · [Corrections not applied](../../goals/dialogue-management/failures/corrections-not-applied.md) · [Generic error messages](../../goals/errors-and-recovery/failures/generic-error-messages.md) · [Dead-end "I don't understand" replies](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) · [Failure taxonomy](../../roadmap/specs/failure-taxonomy-v1.md)
