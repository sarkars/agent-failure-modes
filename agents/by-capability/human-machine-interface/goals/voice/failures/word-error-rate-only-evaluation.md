# Word Error Rate vs Entity Error Rate: Word-Error-Rate-Only Evaluation

<!-- SEO
title: Word Error Rate vs Entity Error Rate: Why WER Alone Misleads
description: A low average WER can hide wrong names, numbers, and dropped "not"s. Report entity and critical-slot error rates next to WER, and test the task.
search phrases:
- word error rate vs entity error rate
- speech to text evaluation metrics
- is WER a good metric for voice agents
- low WER but wrong phone numbers
- how to evaluate speech recognition for voice bots
- why word error rate is not enough
- asr evaluation negation errors
(Phrases come from result titles and wording seen during research, not from volume data.)
-->

**Frequency**: Common

## Issue: A voice agent is judged by average word error rate, which hides wrong names, numbers, and dropped "not"s; the fix is to report entity and critical-slot error rates next to WER and to test the task.

> **One line:** The dashboard says the speech recognizer is 97% accurate, and the caller's phone number, dose, or "do not" is still wrong.

| | |
|---|---|
| **Channel** | Written for **chat**: transcripts of voice calls kept as text events can be scored today. Audio-level checks for live voice are **PLANNED**. |
| **Stakes** | Medium to high. A wrong amount, name, or negation is acted on. |
| **Who is affected** | Callers whose key details are rare words: names, drug names, street names, digits. Teams that pick or tune a recognizer from one average score. |
| **Frequency** | Common (our judgment). Every source below is a vendor or trade article that says this is routine; I found no independent rate of how many teams use WER alone. |
| **Pattern ID** | word-error-rate-only-evaluation |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | Critical-slot error rate (names, numbers, negation) reported next to WER. Target: reported on every release; the value is set from your baseline (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. A better recognizer lowers errors, but the metric still weights every word the same, so the gap stays hidden. (Our judgment, not tested.) |
| **Also searched as** | speech to text evaluation metrics · low WER but wrong numbers · entity error rate · asr negation errors · wer vs semantic accuracy |
| **Flag** | R |

## 1. In plain words
Word error rate counts every wrong word the same. A caller's last name or the dose of a medicine is a few words in a long call, so getting it wrong barely moves the average. The fix is to score the words that matter on their own, next to WER, and to check whether the task came out right.

## 2. What it looks like
The transcripts below are made up for this page. A pharmacy phone assistant was chosen because its recognizer scored well on average WER.

**Without the fix**
```
Caller: Hi, I'm refilling my husband's prescription. Date of birth is one two, oh four, nineteen sixty.
Bot:    (heard) "one two, oh four, nineteen sixty-nine"  (heard) "Please refill his lisinopril."
Caller: He is not allergic to penicillin, just so you know.
Bot:    (heard) "He is allergic to penicillin."  Noted. Refill submitted for pickup at Walgreens on Maple.
Caller: Wait, no, he is not allergic.
Bot:    Your refill is on its way. Anything else?
```

**With the fix**
```
Caller: He is not allergic to penicillin, just so you know.
Bot:    I want to be sure I got that right. I heard: "not allergic to penicillin." Is that correct?
Caller: Yes.
Bot:    Thanks. Date of birth: December 4, 1960?  [Yes] [No, say it again] [Talk to the pharmacist] [Something else]
```
The test set now scores date, drug name, and "not" on their own, so the first bot's slips show up before release. The fixed bot reads back what the release gate flagged as high risk.

## 3. Why it happens
- **Every word weighs the same in WER.** A dropped "not" and a dropped "the" each cost one word. A 21-word transfer request with one wrong amount scores about 4.8% WER (see section 4).
- **Rare words are a small share of the text.** Phone numbers can be ten words in a thousand, so they barely move the average even when all are wrong.
- **Test audio is not call audio.** A leaderboard score on clean audio says little about noisy, accented calls full of names, and the reference transcript itself can be wrong.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "A transcript with 3% WER may nevertheless contain an incorrect dosage"; "A transcript can be 97 percent accurate overall and 0 percent accurate on phone numbers." It recommends measuring entities directly and "the task, not the transcript." Updated July 1, 2026. | [Soniox, *Speech recognition evaluation beyond WER*](https://soniox.com/wiki/beyond-wer). Opened and read. | Vendor reference page, no author. The 97%/0% figure is an illustration, not a measurement. |
| In a 21-word request ("transfer five hundred dollars...") the recognizer changes "five" to "nine": WER 0.0476, entity F1 recall on the amount tokens 0.5. "A comfortable 4.8% WER and a broken transaction." | [agwer README on PyPI](https://pypi.org/project/agwer/) (author Huck Yang, MIT license). Opened and read. | A worked example from a tool's documentation, one sentence, not real calls. |
| A dropped "not" turns "I do not want to upgrade" into "I do want to upgrade." "The transcript is 99 percent accurate... The interaction is 100 percent broken." Report entity accuracy per type; entity-weighted WER uses a multiplier "3x to 5x" that "is application-dependent." Slices: English/noisy 8.7% WER, 86% entity accuracy; Chinese/clean 12.3% WER, 78%. | [Cresta, *Evaluating Speech-to-Text Quality: Beyond Word Error Rate*](https://cresta.com/blog/evaluating-speech-to-text-quality-beyond-word-error-rate), May 29, 2026. Opened and read. | Vendor blog. The "99 percent" line is a rhetorical example. Slice figures are Cresta's own data, method not given. |
| On one AssemblyAI voice-agent benchmark, two models were under a point apart on WER (7.78% vs 8.64%) but more than 7 points apart on entity error (18.5% vs 26.1%). By category, one model: names 10.9%, dates 18.6%, emails 17.2%, phone numbers 2.4%. | [AssemblyAI, *Entity accuracy in speech-to-text*](https://assemblyai.com/blog/entity-accuracy-in-speech-to-text), Kelsey Foster, Sept 30, 2026. Opened and read. | Vendor selling the products compared. 12,460 scripted scenarios, not live calls; entity-error method not fully described. Not reproduced here as a ranking. |
| Expert clinicians labeled the impact of ASR discrepancies in two doctor-patient dialogue datasets as "No, Minimal, or Significant Impact." WER and many other metrics "correlate poorly" with those labels. An LLM judge reached 90% accuracy and Cohen's kappa 0.816. | [Ellis et al., *WER is Unaware*, IWSDS 2026](https://aclanthology.org/2026.iwsds-1.39/). Abstract opened; full text not read. | Peer-reviewed venue, but clinical dialogue only, and the abstract's numbers are the judge's. Not shown to hold for banking or retail calls. |

**Not used.** A 2018 JAMA Network Open study of dictated clinical notes (about 7% raw error, "17-year-old" heard as "70-year-old") appeared **only in search summaries**; the Becker's page I tried returned HTTP 403, so none of its numbers is on this page. A 1999 named-entity WER method and an ATENE metric were seen **only in a search summary** of a 2016 paper. I found no independent survey of how many teams ship on WER alone.

## 5. The fix
**The principle:** Report WER as a baseline, never as the only score; add entity and critical-slot error rates, and judge the task.

**Do this**
1. **Name the critical slots.** List the details the call cannot get wrong (names, digits, dates, amounts, drug names, yes/no and negation) before choosing a recognizer.
2. **Report entity error next to WER.** Every release report shows WER and a per-type slot error rate; a release report with WER alone is incomplete.
3. **Score negation on its own.** Keep test sentences where a missing "not" flips the meaning, and count a flipped polarity as a critical error, not one word.
4. **Test on your own audio.** Score on real or realistic calls (accents, noise, names), not only a public clean set.
5. **Measure the task.** Check whether the right action was taken or the right field was filled, on a sampled set of call transcripts.
6. **Read back critical slots in production.** Before acting on a name, number, or negation, the bot says what it heard and waits for a yes.
7. **Fix the rules before comparing.** Write the text normalization and scoring rules down, so two runs compare.

**Reference design: evaluation report**
| Layer | Example metric | Release rule |
|---|---|---|
| Words | WER | Reported; baseline only |
| Entities | Error rate per slot type (name, digits, date, amount, drug) | Reported per type; rising value blocks release |
| Meaning | Negation and intent preserved (reviewer or judge) | Any flipped polarity in the test set is listed |
| Task | Right action taken, right field filled | Reported on a sampled set |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A critical slot is weak or unconfirmed: "I heard 'not allergic to penicillin.' Is that right?" Do not use it for slots that tested clean and were confirmed. |
| Offer choices: 2-4 options plus "Something else", free text open | After a read-back that is wrong: "Yes", "No, say it again", "Talk to a person", "Something else". Do not offer them when the caller already said yes. |
| Hand off to a person | The same slot is wrong twice, or the slot is a dose, an amount, or an allergy and is still unconfirmed. Do not hand off if the caller asked to keep going with the bot. |

**Don't over-correct.** Do not drop WER, and do not make the caller confirm every word. WER still shows broad drift, and a read-back on every slot adds turns and wears people out. Confirm only the critical slots you listed, and track how many read-backs the caller accepts on the first try. Semantic or LLM-judge scores add cost and variability, so check them against human labels before trusting them.

**Hand-off rule.** After a critical slot fails twice, or any high-stakes slot stays unconfirmed, pass a person the audio or transcript, the slot, and what was tried ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | A recognizer test report | It lists critical slots and a per-type error rate, not only WER (1, 2) |
| 2 | A test sentence with a dropped "not" | Counted as a critical error, with polarity flagged (3) |
| 3 | A set with a wrong amount in a long request | WER looks small and the slot error rate flags it (2) |
| 4 | Scoring on a clean public set only | The report is marked incomplete until call-like audio is added (4) |
| 5 | A booking where the right action was not taken | The task metric catches it (5) |
| 6 | A caller says a name and a birth date | Both are read back before the record changes (6) |
| 7 | Two runs of the same audio | Scores match given the stored normalization rules (7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Critical-slot error rate reported next to WER** (primary) | Reported on every release; value set from a baseline | Score a labeled call sample per slot type; store with the WER of the same run | Any release with WER only |
| Share of critical slots confirmed before action | 100% | Log each slot with its confirmation flag | Below 95% |
| Negation flips found in the test set | 0 shipped | Count flipped polarity in labeled sentences each release | Any unlisted flip |
| Task success on a sampled call set | Set from baseline | Sampled review: right action, right field | Falling over two releases |
| Read-backs the caller accepts first try (counter-metric) | Track; set from baseline | Count "yes" after the first read-back | Falling sharply (too many needless read-backs) |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Written for text: the evaluation report has a WER field and no slot-level field | Release report fields | A model-selection note for a task with no critical slots |
| Written for text: the caller repeats a name, digits, or "no, not" right after a read-back or a confirmation | Next user turn after the bot's reply | A deliberate rephrase for clarity |
| Written for text: the transcript contains a changed value for a slot the caller later corrects | Slot value history in the event log | The caller really changed their mind |
| PLANNED for voice: per-slot recognizer confidence is below the slot threshold at action time | Needs recognizer confidence values; none are recorded here | A well-recognized rare word |

**Starter rule:** every evaluation report lists critical slots and their error rate next to WER, and the bot reads back a critical slot before acting on it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: word-error-rate-only-evaluation
runs: pre_send
reads: [slot.type, slot.value, slot.confirmed, slot.error_flag, eval.report_fields]
trigger: a critical slot (name, number, date, amount, negation) is about to be used for an action
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Yes", "No, say it again", "Talk to a person", "Something else"]
on_miss: rewrite
metric: critical-slot error rate reported next to WER
counter_metric: read-backs accepted on the first try
status: proposed
```

## 8. Related patterns
- [Transcription hallucination](transcription-hallucination.md): the recognizer invents words from silence or noise. Here it hears real speech and a good average score hides the wrong key words.
- [Repair failure](repair-failure.md): the agent mishandles a caller's spoken correction. This page covers how the recognizer is scored before any call happens.
- [Number and date errors](../../../../speech-and-audio/goals/speech-recognition/failures/number-date-errors.md): digits are misheard. This page is about the metric that fails to show it.
- [Name recognition failures](../../../../speech-and-audio/goals/speech-recognition/failures/name-recognition-failures.md): names are misheard. This page covers measuring that apart from WER.
- [Domain vocabulary gaps](../../../../speech-and-audio/goals/speech-recognition/failures/domain-vocabulary-gaps.md): terms of art are missed; entity scoring is how a team would see it.

## 9. Common questions
### Is word error rate a good metric for voice agents?
It is a fair baseline for overall drift. It is not enough alone, because it counts a wrong dose and a wrong filler word the same. See [section 4](#4-why-it-matters).

### What is entity error rate?
It is the error rate on the details that matter: names, numbers, dates, amounts. Sources define it in different ways (an error rate or precision and recall on those words), so write your own definition down. See [section 5](#5-the-fix).

### Why is my WER low but the bot still gets numbers wrong?
Numbers are a small share of the words, so they barely move the average. In the agwer example, one wrong amount in 21 words gave about 4.8% WER. Score digits and amounts on their own.

### How do I test speech to text on negation?
Keep sentences where a missing "not" flips the meaning and count each flip as a critical error. See tests 2 and 3 in [section 6](#6-how-to-test-it-short-version).

### Do I still need WER if I measure entities?
Yes, as a baseline. Report both, plus the task result. The sources above all say to add measures, not to remove WER.

---
## Technical section

### T1. Solution architecture
```
labeled call transcripts -> slot tagger (name, digits, date, amount, drug, negation)
  -> score per type + WER + task check -> release report -> gate
live call -> critical slot -> read-back -> action after yes
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Report lists slot error rates | CI report step | Test 1 |
| Critical slot read back before action | Action layer | Test 6 |
| Normalization rules stored with the score | Eval harness | Test 7 |

### T3. Evals
- **Dataset:** call-like audio with human-labeled critical slots and negation sentences. Start with 100 labeled calls (starting point).
- **Judge rubric:** is each slot value exactly right? Is meaning the same, including "not"?
- **Metrics and starting thresholds:** per-type slot error; flipped polarity 0 shipped; task success. Starting points to tune.
- **Release gate:** block if a slot error rate rises against baseline or a flipped polarity is unlisted.

### T5. Trade-offs
- Labeling slots costs time; start with the three or four slots that carry money, identity, or safety.
- LLM judges are cheaper than people but need checking against human labels.

---
### Deep dive
- **Open question.** The independent evidence here is one clinical paper's abstract. The rest are vendor materials, so check the effect on your own calls.
- **Modality notes.** Live voice (PLANNED): per-slot recognizer confidence could trigger the read-back; no values are recorded here.
- **References.** [Soniox](https://soniox.com/wiki/beyond-wer), [agwer](https://pypi.org/project/agwer/), [Cresta](https://cresta.com/blog/evaluating-speech-to-text-quality-beyond-word-error-rate), [AssemblyAI](https://assemblyai.com/blog/entity-accuracy-in-speech-to-text) (all opened); [Ellis et al.](https://aclanthology.org/2026.iwsds-1.39/) (abstract opened).
