# Prompt Change Broke Chatbot Tone: Tone Changes Shipped With No Regression Test

<!-- SEO
title: Prompt Change Broke Chatbot Tone: Add a Tone Regression Test
description: A prompt edit made your chatbot curt and nobody noticed. Run a fixed conversation set, score tone before and after each change, and block the release.
search phrases:
- prompt change broke chatbot tone
- chatbot suddenly sounds rude after prompt update
- LLM regression testing for prompts
- how to test chatbot tone before release
- system prompt update made the bot curt
- how to score chatbot tone with an LLM judge
- golden set for prompt changes
-->

**Frequency**: Common

## Issue: A prompt edit makes the chatbot curt or cold, and nobody notices because no fixed set of conversations is run before and after each change.

> **One line:** Someone edits the prompt to fix one problem, the bot's tone shifts, and the first people to find out are customers.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice (pace, pauses, tone of voice) and visual signals are PLANNED, not written or measured. |
| **Stakes** | Low to high. Curt replies to an angry or frightened user cost more than curt replies to a simple lookup. |
| **Who is affected** | Every user after the change, and most of all users who write in upset |
| **Frequency** | Common (our judgment). I found no study that counts how many teams ship prompt changes without a tone test. |
| **Pattern ID** | tone-changes-shipped-with-no-regression-test |
| **Family** | [Measurement and feedback](../README.md) |
| **Goal** | Teams can tell whether conversations really work, and users can tell the team when they don't. |
| **Primary metric** | Tone scores before and after each release. Starting target: mean tone score on the fixed set drops by no more than 0.2 points (1-5 scale), and no single conversation scores below 3 (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model still follows a changed prompt, and a new model version can shift tone too, so the check has to run on every change. (Our judgment, not tested.) |
| **Also searched as** | chatbot got rude after update · bot replies too short after prompt change · LLM prompt regression test · tone drift after model upgrade · golden dataset for chatbot prompts |

## 1. In plain words
Prompt edits have side effects. Adding "be concise" to stop rambling can also strip the warmth from a reply to someone whose power is out. If the team only reads a few test replies by hand, nothing flags it. Run the same fixed set of conversations before and after every change, score the tone, and block the release if it drops.

## 2. What it looks like
Example: an electric utility's outage chatbot. Last week the team added "Be concise. No filler." to the system prompt because replies were long.

**Without the fix** (the edit shipped after a spot check of three questions)
```
User: Power's been out since 6 and I have formula for my baby in the fridge. Any update?
Bot:  Outage 4471. Estimated restoration 11:00 PM.
User: That's it? Is someone coming?
Bot:  Crew assigned. ETA unchanged.
User: wow ok. thanks for nothing
Bot:  You're welcome.
```
**With the fix** (the fixed set scored this conversation 2.0, below the gate, so the edit was revised to "Be concise, and acknowledge a stated worry in one short sentence before the facts")
```
User: Power's been out since 6 and I have formula for my baby in the fridge. Any update?
Bot:  Restoration is estimated for 11:00 PM (outage 4471). A crew is assigned.
      That's a long time with formula to protect. Keep the fridge closed; I can text you when the estimate changes.
User: That's it? Is someone coming?
Bot:  Yes. A crew is assigned to your area. Want a text if the estimate moves, or the number for a person at the outage desk?
```
The fixed prompt stayed short, but the answer still comes first and the reply notices what the user said.

## 3. Why it happens
- **Prompt edits are tested by spot check.** Someone tries a few messages, sees the fix works, and ships. Nothing re-reads the cases the edit was not about.
- **Tone is not in the test suite.** Teams test facts, format, and tool calls, which can be matched by code. Tone needs a rubric or a judge, so it is skipped.
- **No stored "before" score.** Without the last release's scores on the same conversations, a drop has nothing to be compared against.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "A prompt tweak that fixes one complaint can quietly break ten other answers." The page gates prompt, model, retrieval and tool changes with a fixed dataset that fails CI when a score drops below a threshold. Size guidance: "tens to low hundreds of items" for a pull request gate; below roughly 20 items, one flaky output moves an average score by 5 percentage points or more. | [Langfuse, *LLM regression testing*](https://langfuse.com/resources/engineering/llm-regression-testing.md). Opened and read. | Vendor guide (Langfuse sells the tooling). Its examples are about correctness and format, not tone; it does not describe a tone evaluator. |
| Anthropic's docs describe an "LLM-based Likert scale" that rates tone from 1 to 5, "ideal for evaluating nuanced aspects like empathy, professionalism, or patience". The example test set is 100 customer inquiries with a target tone, including an angry customer. The docs advise using a different model to grade than the one that wrote the reply. | [Anthropic, *Develop tests*](https://platform.claude.com/docs/en/docs/build-with-claude/develop-tests). Opened; the first 100,000 of 153,035 characters read. | Vendor documentation for its own API. A recipe, not evidence that it catches regressions. |
| OpenAI's cookbook: "Model grading will have an error rate, so it is important to validate the performance with human evaluation". It also says it makes sense to use a different model to grade than the one that wrote the completion. | [OpenAI Cookbook, *Getting started with OpenAI Evals*](https://developers.openai.com/cookbook/examples/evaluation/getting_started_with_openai_evals). Opened and read. | Vendor documentation. The page I read gives no error-rate figure. |
| In April 2025 a GPT-4o update was reported as overly flattering. Per Simon Willison's summary of OpenAI's follow-up, offline evaluations and A/B tests looked good, some expert testers felt the model was slightly off before launch, and OpenAI said it would treat behavior problems as launch-blocking. | Our [teardown of the GPT-4o rollback](../../../incidents/openai-gpt-4o-sycophancy-rollback-april-2025.md), built from TechCrunch, The Register and Willison (all opened). | Secondary reports; OpenAI's own posts could not be opened (HTTP 403). It was a model update, not a prompt edit, and the shift was flattery, not curtness. |

**Public incident.** No public incident found of a prompt edit that made a bot curt, with a source I opened. Searches run on 2026-10-20: "chatbot tone changed after prompt update users complain curt rude"; "LLM prompt regression testing golden set before deploying prompt change"; "Anthropic OpenAI evals guide regression test prompts model-graded tone". One search result described 2026 user complaints that ChatGPT was curt; I read only the search summary, so I use nothing from it. The GPT-4o case above is the closest opened example of a behavior change shipped without catching it.

## 5. The fix

**The principle:** No prompt or model change ships until the same fixed conversations have been scored before and after, and tone has not dropped.

**Do this**
1. **Keep one fixed tone set, stored with a version number.** Start with 40 conversations (a starting point; Langfuse says below roughly 20 one flaky output swings the average, Anthropic's example uses 100). Cover at least five slices: angry user, worried user, plain lookup, bad news (a denial or a delay), and a thank-you or goodbye.
2. **Give every conversation a target tone.** For example "empathetic", "patient", "professional", "brief and neutral". A person writes it, not the model.
3. **Run old and new prompts on the same set, same grader, same settings.** Store both scores per conversation with the prompt version and model version.
4. **Score with a rubric grader and cheap code checks.** Grader: a 1-5 rating of how well the reply matches the target tone, run by a different model than the one that wrote the reply. Code checks: reply length in words, and presence of a stated-feeling acknowledgment where the case requires one.
5. **Validate the grader against people.** Two reviewers label 20 replies; the grader must agree within one point on at least 80% (starting point) before it can block a release.
6. **Gate on per-slice and per-case change, not only the average.** Block if any slice's mean drops by more than 0.3, or any conversation scores below 3 (starting points). Start the grader gate as a warning, and promote it to blocking once false alarms have stopped (Langfuse's advice for judge metrics).
7. **A person reads the biggest drops.** Before release, read the five conversations with the largest score decline and sign off or revise.
8. **Every tone complaint becomes a test case.** Within 14 days (starting point) the conversation, anonymized, joins the set with a target tone.
9. **Rerun on every change that can move tone:** prompt edits, model swaps, vendor model upgrades, and changes to the persona or style text.

**Reference design: the release check**
```
change proposed (prompt vN -> vN+1, or model swap)
  -> run tone set on vN and vN+1 (same grader, same settings)
  -> compare: per-case delta, per-slice mean, cases below 3
  -> any gate hit?  yes: block, show the cases and both replies side by side
                    no : release; log prompt_version, set_version, mean, per-slice scores
  -> after release: sample 50 live replies/week, grade them, compare with the gate score
```
Test-case format:
```
id: outage-formula-01   slice: worried   target_tone: empathetic
user: "Power's been out since 6 and I have formula for my baby in the fridge. Any update?"
must: answers the ETA in the first sentence; one-sentence acknowledgment
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | In every set case: a tone fix must not push the answer down. Do not add warmth before a plain lookup that needs none. |
| Offer choices: 2-4 options plus "Something else", free text open | After a user writes "that's it?", "rude", or "thanks for nothing": "Too short", "Too blunt", "Reply was fine", "Something else". Do not offer them after an ordinary thank-you or when the user already stated the problem in words. |
| Hand off to a person | When the user stays upset after that reply: offer a person and pass the conversation. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** A tone gate can push every prompt toward long, padded, apologetic replies. Keep a counter-check: reply length and the share of replies that open with filler must not rise past the previous release by more than the gate allows (see [filler and padding](../../response-structure/failures/filler-and-padding.md)). Keep "brief and neutral" cases in the set so a plain lookup does not get a paragraph of sympathy.

**Hand-off rule.** Live conversations are handed to a person under the normal hand-off patterns. For the release process: if the grader and human reviewers disagree on a blocked change, a named owner decides within one business day; the default is not to ship.

**Framework used:** none yet.

## 6. How to test it (short version)
There is no full test file for this pattern yet; the [tests folder](../../../tests/README.md) holds the format and the per-pattern fixed conversation sets. Results: **Not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Edit the prompt to add "Be concise. No filler." and run the set | The gate fires on the worried and angry slices (rule 6) |
| 2 | Run the same prompt twice | Scores differ by less than the gate margin, so the gate is not noise (rules 3, 4) |
| 3 | Grader versus two human reviewers on 20 replies | Agreement within one point on at least 80% (rule 5) |
| 4 | Release a change with a blocked case and no sign-off | The release is stopped (rules 6, 7) |
| 5 | Add a complaint conversation to the set | It appears in the next run with a target tone (rule 8) |
| 6 | Change only the model version | The set runs without a prompt edit (rule 9) |
| 7 | A change that does nothing to tone (a new opening-hours fact) | Gate passes; no spurious block |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Tone scores before and after each release** (primary) | Mean drop of 0.2 or less; no case below 3 | Release log: prompt version, set version, per-case and per-slice score for old and new | Mean drop over 0.2, or any slice drop over 0.3 |
| Releases that ran the tone set | 100% | Count prompt or model version changes in the deploy log with a matching eval run ID | Below 100% |
| Grader agreement with human labels | At least 80% within one point | Monthly: two reviewers label 20 replies; compare | Below 70% |
| Live tone score on sampled replies | Within 0.3 of the gate score | Grade 50 sampled live replies a week with the same grader | Gap over 0.5 |
| Tone complaints per 1,000 conversations (counter-view) | Set from your own baseline | Reports tagged "rude", "curt" or "cold" (see [no way to report bad behaviour](no-way-to-report-bad-behaviour.md)) | Doubles within 7 days of a release |
| Complaints added to the set within 14 days | 100% | Match complaint IDs to set case IDs | Any older than 14 days |
| Mean reply length versus last release (over-correction) | Within 25% | Words per reply on the set and on live samples | Over 25% longer or shorter |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Say "proposed" until they are checked against human-labeled conversations. Written for text; voice signals are PLANNED. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt or model version changed with no eval run ID attached | Deploy event against eval log | An emergency rollback to a version that was already tested |
| Mean words per bot reply drops over 25% within a day of a version change | Turn-level reply length grouped by prompt version | A change in the mix of questions, such as a spike in yes/no lookups |
| User reply with "rude", "that's it?", "thanks for nothing" or similar right after a short bot reply | User turn text after a bot turn under 15 words | Sarcasm about a policy, not about the tone |
| Thumbs-down or report reasons tagged tone rise after a release | Report event by prompt version | A known outage or price change the same day |

**Starter rule:** no prompt or model change is released until the fixed tone set has been scored for the old and new version and no slice has dropped past the gate.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: tone-changes-shipped-with-no-regression-test
runs: conversation
reads: [deploy.prompt_version, deploy.model_version, eval_run.id, eval_run.case_scores, user_turn.text, bot_turn.word_count]
trigger: a user says the reply was too short or rude, or a release changes the prompt or model
moves: [lead_with_the_answer, offer_choices, hand_off]
choices: ["Too short", "Too blunt", "Reply was fine", "Something else"]
on_miss: handoff
metric: tone scores before and after each release
counter_metric: mean reply length versus last release
status: proposed
```

## 8. Related patterns
- [No way to report bad behaviour](no-way-to-report-bad-behaviour.md): the user half of this family. That page is about users telling the team; this one is about the team checking tone itself before release. Reports are one input to this set (rule 8), not a substitute for it.
- Persona changes after a model or prompt update (planned page PV-02, not yet written). It will cover brand voice drift. The closest existing pages are [voice drift after a model version upgrade](../../../../../by-use-case/content-marketing/goals/brand-consistency/failures/voice-drift-after-model-version-upgrade.md) and [silent model update](../../../../reasoning-and-thought/goals/model-updates-and-versioning/failures/silent-model-update.md). This page is the measurement side: how to catch the shift, whatever caused it.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): the opposite miss, warm words with no substance. A tone set should catch both.
- [Filler and padding](../../response-structure/failures/filler-and-padding.md): the over-correction when a tone fix adds words.
- [GPT-4o sycophancy rollback teardown](../../../incidents/openai-gpt-4o-sycophancy-rollback-april-2025.md): a behavior change that evaluations did not catch before launch.

## 9. Common questions
### How do I test a chatbot's tone before releasing a prompt change?
Keep a fixed set of conversations with a target tone for each, run the old and new prompt on it, and score both with the same grader. Block the release if any slice or case drops past your gate. See rules 1-6.

### Can an LLM judge score tone reliably?
It can rate tone on a 1-5 scale, and Anthropic's docs describe doing so. OpenAI's cookbook warns that model grading has an error rate and should be validated with human evaluation. Check yours against two human reviewers first (rule 5).

### How many test conversations do I need?
Langfuse says tens to low hundreds for a pull request gate and warns that below about 20 items one flaky output moves the average by 5 points or more. Forty across five slices is a starting point, not a standard.

### Does a spot check count as a regression test?
No. A spot check covers the cases the edit was about. The set is fixed so that it covers the ones it was not about.

---
## Technical section

### T1. Solution architecture
The tone set lives in a versioned dataset. A CI job runs both prompt versions through the same model settings, sends each reply to the grader, writes per-case scores to the release log, and fails the check when a gate is hit. A weekly job grades a live sample with the same grader.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No deploy of a changed prompt without an eval run ID | Deploy pipeline | Deploy log rows with no linked eval run |
| Grader differs from the generating model | Eval config | Config check |
| Set only grows or is versioned, never edited silently | Dataset store | Version history |

### T3. Evals
- **Dataset:** start with 40 anonymized conversations across five slices, each with a human-written target tone; add every tone complaint.
- **Judge rubric:** 1-5 match to target tone, "output only the number" (the Anthropic example format); add a second pass for "answers first".
- **Metrics and starting thresholds:** as in section 7; all are starting points.
- **Release gate:** block on slice drop over 0.3, any case below 3, or mean drop over 0.2; warn-only until false alarms stop.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Live tone score gap to gate score | Over 0.3 | Over 0.5 | Compare prompt and model versions; roll back if a release matches |
| Tone complaints per 1,000 | 1.5x baseline | 2x baseline within 7 days of a release | Read the reports, add them to the set |

### T5. Trade-offs
- Running the set twice per change costs grader calls and a few minutes of CI time.
- A strict gate slows prompt changes; a warn-only period lets the team tune thresholds first.
- A grader can be wrong or drift; that is why section 7 tracks agreement with people.
