# Study S2 (preregistration): do corrections stick for the next two to five turns?

This page is the preregistered protocol for study S2, written for developers, conversation designers and researchers who want to check or reproduce how often a booking or order chatbot still uses the old value, in its summary or its action, after a simulated customer corrected it.

> **Status: Designed, not run. No results exist.** Written 2026-10-22 and not yet reviewed. Thresholds are starting points we chose, not from sources. The study uses simulated users on reference bots we configure; it says nothing about real customers or any commercial product.

## 1. Research question
After a simulated customer corrects one detail ("sorry, I meant Tuesday"), and then talks about other things for 2 to 5 more turns, does the reference bot's final summary and final action hold the corrected value and not the old one? How does that rate change with the bot's configuration, the underlying model, the number of turns since the correction, and the kind of correction?

This is study S2 in the [chat analytics plan](../../roadmap/chat-analytics-plan.md). Its metric is the primary metric of [corrections-not-applied](../../goals/dialogue-management/failures/corrections-not-applied.md), corrections still wrong two turns later, extended to 2 to 5 turns and scored on the end state, not on how the bot sounds. Terms follow the [glossary](../glossary.md) and [metrics](../metrics.md). The test conversations in the [test file](../../tests/corrections-not-applied.md) are the starting point for the scenarios.

## 2. Hypotheses
Each hypothesis can be wrong. "End-state correct" is defined in section 4. Differences are in percentage points (pp). All marks (90%, 10 pp, 5 pp) are starting points we chose before seeing data.

| # | Hypothesis | Pattern ID(s) tested | Falsified if |
|---|---|---|---|
| H1 | With a generic booking prompt and no instruction about corrections (C0), the pooled end-state-correct rate is below 90%. | `corrections-not-applied` | The pooled C0 rate is 90% or higher, with a 95% interval lower bound of 85% or higher. |
| H2 | Adding the pattern page's prompt block (C2) raises the pooled rate over C0 by 10 pp or more. | `corrections-not-applied` | The C2 minus C0 difference is under 10 pp, or its 95% interval includes 0. |
| H3 | Distance hurts: under C0, the rate at 5 turns after the correction is at least 5 pp lower than at 2 turns. | `corrections-not-applied` | The 2-turn minus 5-turn gap is under 5 pp, or its interval includes 0. |
| H4 | A read-back is not enough. Under C0, at least 5% of conversations whose first reply after the correction states the new value still end with the old value in the summary or the action. | `corrections-not-applied` | Under 5% of those conversations end wrong, with an interval upper bound under 5%. |
| H5 | Corrections that change a dependent detail (a price, a total) are fixed fully at least 10 pp less often than plain corrections under C0, because the total stays stale. | `corrections-not-applied` | The plain minus cascade gap is under 10 pp, or its interval includes 0. |
| H6 | Counter-effect: C2 does not raise false overwrites (a preference such as "no window seat" treated as a change to a slot) or needless re-confirmations by more than 5 pp over C0. | `over-confirmation`, `negation-and-exceptions-ignored` | C2 raises the combined decoy rate by more than 5 pp over C0, with an interval excluding 0. |

## 3. Design
### 3.1 Simulated users
- **One simulator prompt, versioned.** An LLM plays a customer with a persona, a goal (a table or a flower order) and a tone. The scored messages are scripted: the first request, the correction wording, the filler turns, and the closing "ok book it". The LLM only fills in answers to the bot's questions inside the script's limits.
- **The simulator always confirms a summary.** When the bot shows a summary, the simulated customer says "yes". Real customers may catch a wrong summary. S2 measures what the bot does, not whether a person would notice.
- **Why scripted.** Published LLM user simulators have limits. [Davidson et al. (2023)](https://arxiv.org/abs/2309.13233) say their simulator works well "especially on single-intent conversational goals", so each S2 scenario has one goal. Scripting the correction and the filler turns means every bot sees the same correction at the same moment.
- Temperature, seed, simulator model and prompt are recorded for every run.

### 3.2 Scenario set
Eleven families, adapted from the 14 conversations in the test file (not yet run). The settings are the test file's invented apps: a table-booking chat and a flower-order chat. Each family runs at 2, 3, 4 and 5 filler turns between the correction and the closing request. Filler turns are scripted questions that touch no slot (parking, the menu, a high chair).

| Family | Situation | In the primary metric? |
|---|---|---|
| A. Correct a date | "sorry i meant tuesday" | Yes |
| B. Correct a name | "its Jon not John" | Yes |
| C. Two corrections at once | "tuesday, and four people" | Yes |
| D. Cascade | "make it saturday instead" when Saturday costs more | Yes (stale total counts as wrong) |
| E. Quantity | "make it 4 not 2" | Yes |
| F. Indirect | "actually the other address" (two saved addresses) | Yes |
| G. Correct twice | The same slot is corrected, then corrected again | Yes (the latest value must win) |
| H. Undo | "change it back to monday" | Yes (the logged value must return) |
| I. Cannot apply | The corrected value is rejected by the booking system | No: scored on its own rule, section 4.4 |
| J. Decoy: preference | "no window seat please" (not a correction) | No: scored for false overwrite |
| K. Decoy: challenge | "no it closes at 9" when the record says 8 | No: scored for flipping a correct fact |

The scenario files, personas and wordings are published before the run.

### 3.3 Reference bots, by configuration
We name configurations, not vendors, and publish no ranking of commercial products. Models are listed by exact version string when the run is registered: at least three, from at least two providers, plus one run locally.

| Config | What it is |
|---|---|
| C0 | Generic booking system prompt, with a `book_table` or `place_order` tool and no instruction about corrections. |
| C1 | C0 plus one sentence: "If the customer changes a detail, use the new one." |
| C2 | C0 plus the prompt block from the pattern page's fix. |
| C3 | C2 plus an orchestrator that holds slot state, overwrites on correction, logs the old value, and fills tool parameters from the state, not from chat text. |
| C4 | A scripted slot-filling form bot with no LLM, as a deterministic baseline. Its correction keywords are published. |

### 3.4 Variables
- **Independent:** configuration (C0 to C4), model (C0 to C3), family, wording, filler turns after the correction (2 to 5).
- **Controlled:** simulator prompt and model, scripts, tool behavior, conversation cap (14 bot turns), seed list.
- **Dependent:** end-state correct, which place held the old value (summary, action, both), read-back present, false overwrite, flip on a correct fact.

## 4. What counts as correct
### 4.1 Turn counting (exact)
1. A **user turn** is one user message, or several sent with no bot message between them. A **bot turn** is all bot output between two user turns, tool calls included.
2. The **correction turn** is the user turn containing the correction. The script fixes it, so it is known in advance.
3. **Filler turns** are the next k user turns (k = 2, 3, 4 or 5), none of which touches a slot. The **closing turn** follows them: "ok book it".
4. Scoring uses the bot output after the closing turn. Each conversation is scored once.

### 4.2 End-state correct (primary)
A conversation is **end-state correct** only if all of these hold after the closing turn:
- **Action:** the logged tool call has the corrected value for every corrected slot, and no superseded value in any parameter.
- **Summary:** the last summary shown before the action has the corrected values. A bot that shows no summary before acting fails this line, because the pattern page says to show one.
- **Dependent details** (family D, E): totals and prices in the summary match the corrected state.

A bot that says "Updated!" and holds the old value in the action is not correct. This is the point of scoring the end state.

### 4.3 Scoring rule
- **End-state correct rate (primary)** = conversations in families A to H that are end-state correct, divided by conversations in A to H.
- **Where it failed:** old value in the action only, in the summary only, or both. Reported per cell.
- **Read-back rate** = conversations where the first sentence after the correction states the new value, divided by A to H. Used for H4.
- **False overwrite and needless re-confirmation (counter-metric)** = decoy conversations (J, and non-corrected slots in A to H) where the bot changes an untouched slot or asks the customer to confirm a detail they did not change.
- **Flip rate (counter-metric)** = family K conversations where the bot agrees with the wrong claim.
- A conversation that errors out or reaches the cap without an action counts as not correct. Missing runs are reported, never dropped.

### 4.4 Family I and the human-label check
- **Family I** is correct if the bot says the corrected value cannot be applied, keeps the value the system holds, and offers another time or a person. Saying "updated" when the system rejected it is a fail.
- Action and state checks are rule-based, from the event log. Read-back, cascade wording, family I wording and family K are judged by a rule first, then an LLM judge for text. The judge prompt and model are published.
- Before any result is published, two people independently label a random 10% of conversations plus every conversation where rule and judge disagree. A third person settles disagreements.
- Judge precision, recall and agreement come from study S0. If agreement with people is below 0.70 (our starting point), S2 is published labeled "experimental" and the human labels give the headline numbers. The primary metric does not depend on the judge, because it reads tool parameters and the logged summary.
- Study S6 compares simulated users with human participants. If S6 has not run when S2 publishes, S2 says so on its first line.

## 5. Analysis plan
- **Primary metric:** end-state correct rate, per configuration and model, pooled, per family and per number of filler turns. The pooled rate weights the four filler lengths equally.
- **Counter-metrics:** false overwrite and re-confirmation (H6) and the flip rate. A configuration that raises the primary rate and the counter-metrics together is reported as a trade, not a win.
- **Sample size (starting point):** 20 seeds per family, wording, filler length and cell. If an interval in a main comparison is wider than 15 pp, we add seeds from a pre-listed range and say so.
- **Intervals:** every proportion carries a 95% Wilson score interval. Seeds within a family are not independent, so pooled rates and all differences also carry a 95% interval from a bootstrap that resamples families, then seeds within them (10,000 resamples). Both are reported. A difference is never shown without its interval. P-values are not the headline.
- **Falsification:** each hypothesis has its rule in section 2. We apply it as written and do not move thresholds after seeing data.
- **We report even if null:** if C0 already scores 90% or more (H1), if distance does nothing (H3), if the prompt block does little (H2), or if a read-back always predicts a correct end state (H4), we publish that with the same prominence.
- **Exploratory results** (per-model rankings, any hypothesis not in section 2) are labeled exploratory and kept out of the headline.

## 6. Threats to validity
- **Simulator realism.** Scripted corrections are cleaner than real ones. Real people hedge, correct twice, or correct by implication. Only S6 can say how far results carry.
- **The simulator never objects.** It confirms every summary, so S2 cannot show whether people catch a wrong summary.
- **Prompt sensitivity.** We write C0 to C3. Another wording of "generic booking prompt" could change C0. We publish every prompt and run one alternate C0 wording as a check.
- **Harness shape.** Our tool and state design is simple. A real product with a form, a cart and a payment step has more places for an old value to hide.
- **Filler design.** Filler turns are short and touch no slot. Long or slot-related chat (see the 15-turn case in the test file) is outside S2.
- **Judge error.** Section 4.4 limits it and does not remove it.
- **Setting.** English, US, text chat, two invented businesses.
- **Models change.** Hosted models are updated. We record version strings and dates, and the result is a snapshot.
- **Author bias.** The authors wrote the pattern whose fix is tested in H2 and H6. Materials are published so others can check.
- **Scenario choice.** Families come from our own test file, chosen before any run. We publish all of them, including ones we expect bots to pass.

## 7. Prior work and how it shapes the design
We opened each page below on 2026-10-22. For every one we read the abstract page only, not the full paper. Numbers below are the abstract's numbers, and none sets a threshold in section 2.
- **Laban et al., [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) (2025).** Reports an average 39% drop for top open- and closed-weight models across six generation tasks, over 200,000 simulated conversations, and that models "get lost and do not recover" after a wrong turn. It does not test corrections, and the abstract does not name the tasks or the models. It is why we ask whether distance matters (H3). The size of the drop in S2 may be very different.
- **He et al., [Multi-IF](https://arxiv.org/abs/2410.15553) (2024).** Three-turn conversations, 14 models, and o1-preview's average accuracy falling from 0.877 at turn 1 to 0.707 at turn 3. It tests whether earlier instructions are still followed, not whether a changed value replaces an old one. It supports testing more than one turn after the event, nothing more.
- **Canaverde et al., [SEQUOR](https://arxiv.org/abs/2605.06353) (2026).** Reports accuracy falling by more than 9% when constraints are added or replaced mid-conversation, using simulated, persona-driven conversations. This is the closest design to S2. The abstract does not say how the drop is measured, which models were run, or whether the simulated users were checked against people, so we use it only as a reason to expect an effect and a reminder to validate the simulator (S6).
- **Laban et al., [Are You Sure? (FlipFlop)](https://arxiv.org/abs/2311.08596) (2023).** Ten models, seven classification tasks, answers flipped 46% of the time on average when asked "Are you sure?", with a 17% average accuracy drop. It is the reverse risk, models changing a right answer too easily. It is why family K exists and why H6 has a counter-metric.
- **Davidson et al., [User Simulation with Large Language Models for Evaluating Task-Oriented Dialogue](https://arxiv.org/abs/2309.13233) (2023).** Proposes an in-context-learning user simulator and a Human2Bot dataset to compare it with people. We took the single-goal scenarios and the idea of checking against people (S6).
- **Dialogue-state tracking.** The [pattern page](../../goals/dialogue-management/failures/corrections-not-applied.md) cites research that tracking models can "repeatedly inherit wrong slot values" (Sun et al., IJCAI 2022). We did not reopen it for this page, so it informs nothing here.
- **Search results seen but not opened** (a mechanism paper on attention and goals, simulator-reliability papers, a SIGDIAL 2026 slide deck) are not used in any design choice.
- We found no opened study that measures how often assistants keep a corrected-away value, so H1 has no sourced baseline.

## 8. Out of scope
- **Voice agents.** Speech errors and confirmations by voice are different.
- **Real customers, live traffic and real transcripts.**
- **Whether a person notices a wrong summary.** The simulator always confirms.
- **Long chats and slot-related filler.** Only 2 to 5 neutral filler turns.
- **Forgotten, not overridden, details** ([no-warning-of-context-loss](../../goals/effort-and-memory/failures/no-warning-of-context-loss.md)) and asking again for known facts ([re-asks-for-known-information](../../goals/embedded-copilots/failures/re-asks-for-known-information.md)). S2 scores replaced values only.
- **Ambiguous references beyond family F** ([reference-resolution-failures](../../goals/dialogue-management/failures/reference-resolution-failures.md)).
- Naming or ranking commercial chatbots. That needs a reproducible, permitted and fair design first, per the analytics plan.

## 9. Data and materials to be published
Before the run, with a frozen date: this protocol, scenarios and wordings, personas, simulator prompt, C0 to C4 prompts, tool definitions and orchestrator, scoring code, seed list and judge prompt. After the run: raw transcripts (all synthetic, no personal data), event logs with tool parameters and summaries, scores, human labels, model version strings and run dates, analysis code, and a results page that follows section 5. License and repository location are open decisions for the owner.

## 10. Changes log
| Date | Change |
|---|---|
| 2026-10-22 | First draft of the protocol. Not run. Sources opened for it (abstract pages only): Laban et al. 2025, He et al. 2024, Canaverde et al. 2026, Laban et al. 2023, Davidson et al. 2023. |

## Related
[Chat analytics plan](../../roadmap/chat-analytics-plan.md) · [S1 preregistration](s1-talk-to-a-human-within-two-turns.md) · [Glossary](../glossary.md) · [Metrics](../metrics.md) · [Corrections not applied](../../goals/dialogue-management/failures/corrections-not-applied.md) · [Test file](../../tests/corrections-not-applied.md) · [Over-confirmation](../../goals/dialogue-management/failures/over-confirmation.md) · [Negation and exceptions ignored](../../goals/dialogue-management/failures/negation-and-exceptions-ignored.md) · [Failure taxonomy](../../roadmap/specs/failure-taxonomy-v1.md)
