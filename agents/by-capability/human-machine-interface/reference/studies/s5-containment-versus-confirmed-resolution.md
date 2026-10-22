# Study S5 (preregistration): containment versus confirmed resolution

This page is the preregistered protocol for study S5, written for developers, support analysts and researchers who want to check how far a "no handoff" containment rate sits from a confirmed-resolution floor when both are read from the same simulated support conversations, and which kinds of conversation make the gap.

> **Status: Designed, not run. No results exist.** Written 2026-10-22 and not yet reviewed. Thresholds and windows are starting points we chose, not from sources. S5 uses simulated users with scripted ground truth on reference bots we configure. It says nothing about real customers or any commercial product, and the check of simulated against human behavior belongs to S6, not here.

## 1. Research question
On the same conversations, how far apart are the containment rate (no handoff event) and the confirmed-resolution floor (the user said it worked, or did not come back about the same issue)? Which conversation types put the gap there: abandonment, wrong answers, blocked handoffs, or a fix that only treated the symptom? Does a repeat-contact window or a transcript reader close the gap, and at what cost in extra confirmation turns?

This is study S5 in the [chat analytics plan](../../roadmap/chat-analytics-plan.md). Terms follow the [glossary](../glossary.md), [metrics](../metrics.md) and [conversation outcome metrics](../conversation-outcome-metrics.md). In those pages containment counts abandonment, wrong answers and hidden exits as contained, and confirmed resolution is a floor, not a rate. Every S5 result carries the simulation caveat in section 6.

## 2. Hypotheses
Each hypothesis can be wrong. Differences are in percentage points (pp). All marks (15 pp, 10 pp, 5 pp, 0.70, 7 days) are starting points we chose before seeing data. Bots B0 to B4 and readings M0 to M3 are defined in section 3, end states in section 4.

| # | Hypothesis | Pattern ID(s) tested | Falsified if |
|---|---|---|---|
| H1 | Containment (M0) overstates scripted truth by 15 pp or more, pooled over all non-decoy scripts and bots. | `confident-wrong-answer-with-no-way-to-check`, `answer-and-go-conversation` | The M0 minus truth difference is under 15 pp, or its 95% interval includes 0. |
| H2 | Containment cannot tell the bot that answers wrongly (B2) from the bot that answers correctly and checks (B0): their M0 rates differ by under 5 pp while their truth rates differ by 40 pp or more. | `confident-wrong-answer-with-no-way-to-check` | The B0 minus B2 difference in M0 is 5 pp or more, or the truth difference is under 40 pp. |
| H3 | The bot that blocks a request for a person (B3) is read as contained in at least 90% of its person-only conversations while truth is under 30%. | `talk-to-a-human-ignored-or-looped` | M0 is under 90% on B3, or truth is 30% or higher. |
| H4 | Confirmed resolution (M1) is a floor: M1 never exceeds scripted truth by more than 2 pp in any bot cell, and on the bot that never asks (B1) it sits 10 pp or more below truth because users leave without saying. | `answer-and-go-conversation`, `survey-bias` | M1 exceeds truth by more than 2 pp in any cell, or the B1 gap is under 10 pp. |
| H5 | A 7-day repeat-contact window (M2) reads within 5 pp of truth for scripted returning users, and a 24-hour window misses at least 10 pp more of the failures than the 7-day window. | `symptom-fixed-root-cause-missed` | M2 at 7 days is more than 5 pp from truth, or the 24-hour window misses under 10 pp more failures. |
| H6 | A transcript reader (M3, an LLM judge) agrees with scripted truth at Cohen's kappa 0.70 or higher and is not further from truth than M2. | `confident-wrong-answer-with-no-way-to-check` | Kappa is under 0.70, or M3 is further from truth than M2 with an interval excluding 0. |
| H7 | Counter-effect: the checking bot (B0) does not raise handoffs on solvable scripts by more than 5 pp, or median turns by more than 1, over the bot that never asks (B1). | `over-confirmation`, `escalates-too-early-or-too-late` | The B0 minus B1 handoff difference is over 5 pp with an interval excluding 0, or median turns differ by more than 1. |
| H8 | Counter-effect: the silent-failure bot (B4, no reply after a timeout) is read as contained in at least 80% of its conversations, and its truth is under 20%. | `silent-failure-and-timeout` | M0 is under 80% on B4, or truth is 20% or higher. |

## 3. Design
### 3.1 Reference bots and simulated users
- **One company, five behaviors.** The "Brightwater Internet" support bot (an invented company) handles four intents: billing question, cancel or change plan, outage, moving service. All bots share the intents, the knowledge stub and the handoff stub. Only the behavior at the end of a task differs. We name behaviors, not vendors, and publish no ranking of commercial products.

| Bot | Behavior |
|---|---|
| B0 | Answers correctly, then asks "Did that fix it?" and accepts yes, no or silence. |
| B1 | Answers correctly, then says nothing more (the answer-and-go pattern). |
| B2 | Gives a confident wrong answer with no way to check it. |
| B3 | Ignores or loops on an explicit request for a person; no handoff event is ever logged. |
| B4 | Stops replying after a scripted timeout, with no message. |

- **Scripts with a planted truth.** 12 non-decoy scripts (3 per intent) and 4 decoys. Each script fixes the goal, the correct fix, whether only a person can solve it, and the truth label: **solved** or **not solved**. Truth is set by the script, never by the bot's own words.
- **Scripted simulator, versioned.** A rule-based simulator plays the customer with a confirm propensity c (0.3, 0.6 or 0.9: the chance it answers "yes, fixed" when the fix worked and a check is shown) and a return propensity q (0.5 or 1.0: the chance it contacts again within 7 days about the same issue when truth is not solved). It leaves without a word when it is not asked, when its patience of 3 turns runs out, or after B4 goes quiet. These values are our modeling choices, varied but not measured.
- **Why scripted.** [Davidson et al. (2023)](https://arxiv.org/abs/2309.13233) say their LLM simulator works well "especially on single-intent conversational goals", so each script has one goal. A secondary run with an LLM simulator is labeled exploratory (5 seeds per cell). Temperature, seed, simulator version and prompt are recorded.

### 3.2 Readings (the metrics under test)
| Reading | Definition |
|---|---|
| M0 | Containment: share of conversations with no handoff event. |
| M1 | Confirmed resolution: share where the user said it worked. A floor. |
| M2 | Floor with repeat contact: confirmed, or finished with no repeat contact about the same issue within W. W = 7 days is the main setting; 24 hours and 30 days are sensitivity checks. |
| M3 | Transcript reader: an LLM judge labels each transcript solved, not solved or cannot tell. Prompt and model published. |

### 3.3 Variables
- **Independent:** bot (B0 to B4), script, c, q, window W, seed.
- **Controlled:** intents, knowledge and handoff stubs, user key (stable per simulated user), conversation cap of 12 bot turns, "same issue" rule (same intent and same account in the log).
- **Dependent:** M0 to M3 against truth, the exit split in 4.2, the counter-metrics in 4.4.

## 4. What counts as correct
### 4.1 Definitions (exact)
1. **Contained:** no handoff event in the log. Abandonment, wrong answers and a blocked request for a person all count as contained.
2. **Confirmed:** the simulator sent an explicit yes to a bot check, or a thanks that names the fix.
3. **Repeat contact:** a new conversation by the same user key, about the same issue, inside W after the end. The window and the same-issue rule are ours to set. Changing either changes the reading, so both are fixed before the run.
4. **Truth:** the script's planted label. Every metric is scored against it.

### 4.2 Exit split (each conversation gets one, first rule that applies)
1. **Confirmed:** per 4.1. 2. **Finished without confirmation:** the bot gave its final answer and the user left with no signal. 3. **Handed off:** a handoff event. 4. **Dropped:** the user left before a final answer, or the bot went silent. The split is the reading aid from [metrics](../metrics.md), applied to every bot.

### 4.3 Scoring rules
- **Containment gap (H1)** = M0 minus truth, in pp, per bot, script and pooled.
- **Confirmed floor gap (H4)** = truth minus M1, in pp.
- **Window miss (H5)** = scripted not-solved conversations that M2 calls resolved, per window.
- **Judge agreement (H6)** = Cohen's kappa of M3 against truth on solved and not solved. "Cannot tell" is reported separately and counted as disagreement.
- Errors and missing runs count as not solved and contained. They are reported, never dropped.

### 4.4 Counter-metrics
- **Extra turns and handoffs (H7):** median turns, and handoffs on solvable scripts, per bot.
- **Over-confirmation:** B0 checks after a decoy where nothing needed checking, per [over-confirmation](../../goals/dialogue-management/failures/over-confirmation.md).
- **Early handoff:** handoffs on scripts the bot could solve, per [escalates-too-early-or-too-late](../../goals/human-handoff/failures/escalates-too-early-or-too-late.md).
- **Cold handoff:** handoffs with no summary, per [handoff-summary-is-wrong-or-misleading](../../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md).
- **Obstruction:** cancel scripts that end with no cancellation and no handoff, per [obstructing-cancellation-downgrade-or-refund](../../goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md).

### 4.5 Human-label check
Truth is planted, so it needs no judge. M3 is checked by two people who label a random 10% of transcripts plus every M3 disagreement with truth; a third settles disagreements. Judge agreement comes from study S0. If agreement is below 0.70 (our starting point), S5 is published labeled "experimental" and H6 is reported without a conclusion.

## 5. Analysis plan
- **Primary:** M0, M1, M2 and M3 against truth per bot, pooled with equal weights over c and q, and the exit split per bot.
- **Counter-metrics:** section 4.4 beside every headline. A bot that raises confirmed resolution by asking more, and also raises turns or handoffs past the H7 marks, is reported as a trade.
- **Sample size (starting point):** 12 non-decoy and 4 decoy scripts, 5 bots, 3 values of c, 2 of q, 10 seeds per cell. That is 4,800 conversations. If a main interval is wider than 15 pp, we add seeds from a pre-listed range and say so.
- **Intervals:** each proportion carries a 95% Wilson score interval. Seeds within a script are not independent, so differences also carry a 95% bootstrap interval that resamples scripts, then seeds (10,000 resamples). A difference is never shown without its interval.
- **Falsification:** each rule in section 2 is applied as written. We do not move thresholds after seeing data.
- **We report even if null:** if containment lands near truth (H1), if M3 beats M2 (H6), or if the 24-hour window works as well as 7 days (H5), we publish that with the same prominence.
- **Exploratory** results (the LLM-simulator run, the 30-day window, per-script rankings, any comparison not in section 2) are labeled exploratory and kept out of the headline.

## 6. Limits and threats to validity
- **The gap is built in.** Containment ignores abandonment and wrong answers by definition, so scripts that plant them will show a gap. S5 measures how large the gap is under chosen mixes of scripts, not how large it is at any real company.
- **Truth is planted.** Real "solved" is fuzzy and often disputed. Real users also answer surveys and bot checks in biased ways, as [survey-bias](../../goals/measurement-and-feedback/failures/survey-bias.md) describes; c and q are our assumptions.
- **Mixes are ours.** The share of each bot behavior and script type sets the pooled numbers. We report per-bot results first and the pooled number second.
- **Single company, English, US text chat.** Voice, email and multi-intent goals are outside S5.
- **Author bias.** The authors defined the readings under test. All scripts, wordings and code are published so others can check.
- **Judge error** is limited in section 4.5, not removed.

## 7. What would change our mind
- If M0 stays within 15 pp of truth on a realistic mix, containment is a usable first look on that mix, and we soften the warning in [metrics](../metrics.md).
- If M2 at 24 hours matches M2 at 7 days, the longer window adds waiting without value in this setup.
- If M3 beats every rule-based reading, we say the library should recommend a validated transcript reader beside the floor.
- If B0's extra turns or handoffs cross the H7 marks, asking "Did that fix it?" has a cost the metrics page should state.

## 8. Prior work and how it shapes the design
We counted four web searches (containment versus resolution definitions; repeat-contact windows; human labeling practice; survey CSAT versus conversation-scored resolution) and opened the pages below on 2026-10-22. Numbers below come from pages we opened.
- **Kaizo, containment versus resolution.** Opened. It separates the two measures, which is the split S5 tests. We use no number from it, because its figures are vendor reported.
- **Kustomer, repeat-contact window.** Opened. It supports setting a window for repeat contact. It does not fix one window for us, so W is our choice.
- **Retell AI, first contact resolution.** Opened. It says to set the window per reason and keep it fixed across periods, gives "such as 7 days" as an example, and says the window length and the "same issue" rule both move the result. It also says a repeat-contact number is not directly comparable to survey benchmarks. The page shows no publication date. This is why section 4.1 fixes both before the run.
- **Dialpad, CSAT surveys.** Opened. It reports a 3% survey response rate, that customers with a negative experience took the survey at a higher rate, and that survey CSAT averaged 24% lower than AI-scored CSAT in one contact center. A vendor page with no publication date, so we treat it as an example of survey skew, not a benchmark.
- **Arize, human labeling for evaluations.** Opened. It informs the two-person label check in section 4.5.
- **Davidson et al., [User Simulation with Large Language Models](https://arxiv.org/abs/2309.13233) (2023).** Opened the abstract page. It is why scripts are single-goal and why a human check (S6) is planned.
- **Not opened, not used:** the insertchat resolution-rate glossary (HTTP 404), and every figure seen only in search summaries: a Parloa report of adoption and resolution shares, repeat-rate and window figures from other vendors, and an inter-rater alpha attributed to customer-service transcripts. We could not confirm that alpha in arXiv 2605.12922, whose PDF text was unreadable to us. Unverified, so excluded. We found no opened independent study comparing AI-judged resolution with survey CSAT on abandoned chats, so H1 to H6 have no sourced baseline.

## 9. Out of scope
- **Real customers, live traffic and the human panel** (study S6).
- **Whether a person asks for a human and gets one.** That is [talk-to-a-human-ignored-or-looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) and study S1. In S5 only B3 ignores the request, to test the reading.
- **Survey design and satisfaction scores.** S5 does not test CSAT.
- **Handoff quality after pickup**, beyond the summary check in 4.4.
- Naming or ranking commercial chatbots or metric vendors.

## 10. Data and materials to be published
Before the run, with a frozen date: this protocol, scripts and truth labels, personas, simulator rules and prompt, all bot reply text, the stubs, the window and same-issue rules, scoring code, seed list and judge prompt. After the run: transcripts (all synthetic), event logs, scores, human labels, version strings, run dates and analysis code. License and repository are open decisions for the owner.

## 11. Changes log
| Date | Change |
|---|---|
| 2026-10-22 | First draft of the protocol. Not run. Pages opened: Kaizo, Kustomer, Retell AI, Dialpad, Arize and Davidson et al. 2023 (abstract page). |

## Related
[Chat analytics plan](../../roadmap/chat-analytics-plan.md) · [S1 preregistration](s1-talk-to-a-human-within-two-turns.md) · [S2 preregistration](s2-do-corrections-stick.md) · [S3 preregistration](s3-fallback-designs-compared.md) · [Glossary](../glossary.md) · [Metrics](../metrics.md) · [Conversation outcome metrics](../conversation-outcome-metrics.md) · [Answer-and-go conversation](../../goals/conversation-leadership/failures/answer-and-go-conversation.md) · [Confident wrong answer](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) · [Symptom fixed, root cause missed](../../goals/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md) · [Silent failure and timeout](../../goals/response-time/failures/silent-failure-and-timeout.md) · [Failure taxonomy](../../roadmap/specs/failure-taxonomy-v1.md)
