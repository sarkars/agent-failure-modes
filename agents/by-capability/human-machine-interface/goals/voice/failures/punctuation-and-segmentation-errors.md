# Speech to Text Punctuation Errors: Punctuation and Segmentation Errors

<!-- SEO
title: Speech to Text Punctuation Errors: Fix Meaning Changes
description: Wrong sentence breaks or commas in a speech transcript can change who or what an instruction covers. See the evidence and a read-back design for risky sentences.
search phrases:
- speech to text punctuation errors
- asr punctuation restoration errors change meaning
- sentence segmentation errors speech recognition
- voice transcript missing commas wrong meaning
- dictation puts period in the wrong place
- automatic punctuation speech to text wrong commas
(Phrases come from result titles and wording seen during research and from the source papers, not from volume data.)
-->

**Frequency**: Common

## Issue: Wrong sentence breaks or missing commas in a speech transcript can change what an instruction covers; the fix is to read back risky sentences with their scope spelled out before acting.

> **One line:** A dictated message comes back with a period or comma in the wrong place, and the agent acts on a different meaning than the user spoke.

| | |
|---|---|
| **Channel** | Written for **chat**: transcripts logged as text events, and chat input that arrives as run-on dictated text. Pause and prosody signals for live voice and web dictation are **PLANNED**; nothing here was measured on voice or web traffic. |
| **Stakes** | Low to high. A list, an address, a dose, or a cancel instruction can change meaning with one mark. |
| **Who is affected** | Anyone who dictates lists, addresses, or multi-part instructions; spontaneous speakers with false starts and corrections |
| **Frequency** | Common (our judgment). The sources below show punctuation is hard in spontaneous speech; I found no rate of meaning changes in production agents. |
| **Pattern ID** | punctuation-and-segmentation-errors |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | Meaning-change rate on a labelled punctuation set. Starting target: under 2% on sentences that carry an action or a list (a starting point to tune, not sourced). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Yes, mostly: placement accuracy tends to improve with better models. But some spoken sentences are ambiguous even with perfect words, so a read-back is still needed for actions. (Our judgment, not tested.) |
| **Also searched as** | speech to text wrong commas · asr sentence boundary errors · voice dictation punctuation changes meaning · transcript run-on sentences · automatic punctuation mistakes |
| **Flag** | R (needs research) |

## 1. In plain words
Speech has no commas. The system guesses where they go from the words and, in some setups, from pauses. When it guesses wrong, the words are right but the meaning is not. The fix is to spot sentences where a different break would change an action, and read the agent's understanding back before acting.

## 2. What it looks like
The transcripts below are made up for this page and are shown as text.

**Without the fix**
```
User:  [dictated] Cancel the Austin order, Dallas and Houston stay on hold.
Bot:   Transcript: "Cancel the Austin order Dallas and Houston stay on hold."
Bot:   Done. Your Austin, Dallas, and Houston orders are canceled.
User:  No, I only wanted Austin canceled.
Bot:   I'm sorry. The three orders were canceled as you requested. Reopening takes 2 business days.
```

**With the fix**
```
User:  [dictated] Cancel the Austin order, Dallas and Houston stay on hold.
Bot:   Transcript: "Cancel the Austin order Dallas and Houston stay on hold."
Bot:   That can be read two ways. Which do you mean?
       [Cancel Austin only, hold Dallas and Houston] [Cancel all three] [Something else]
User:  Cancel Austin only
Bot:   Canceling the Austin order only. Dallas and Houston stay on hold. Confirm?
User:  Yes
```
The fixed bot noticed that one missing comma changes the scope of "cancel", asked, and acted only on the confirmed reading.

## 3. Why it happens
These are our reading of the pattern, with the sourced parts marked.
- **Speech carries no punctuation.** Boundaries must be inferred. The Interspeech 2020 abstract says word errors from recognition "often confuse punctuation prediction models", so wrong words and wrong marks compound.
- **Spontaneous speech is hard to segment.** False starts and backtracking break the cues models rely on; a 2025 preprint says current models often struggle here.
- **Nothing flags the risky sentence.** The agent treats the punctuated text as exactly what was meant, so a list, a scope, or a "no, wait" correction is acted on without a check.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In long-form speech translation, an error analysis found that "sentence boundary segmentation has the largest impact on quality" among ASR error types (phoneme substitutions, grammar, boundaries). The authors propose a data augmentation fix. | [Li et al., *Sentence Boundary Augmentation For Neural Machine Translation Robustness*, arXiv 2010.11132](https://arxiv.org/abs/2010.11132). Abstract page opened and read; the PDF text could not be read. | Machine translation of speech transcripts, not an agent taking actions. No numbers in the abstract. |
| "ASR systems introduce word errors, which often confuse punctuation prediction models." The authors' method improved punctuation prediction accuracy by 6.2% (question marks) to 9% (periods) in absolute terms over the prior state of the art. | [Augustyniak et al., Interspeech 2020](https://www.isca-archive.org/interspeech_2020/augustyniak20_interspeech.html). Abstract opened and read. | Results of their method on their own data. It shows errors compound; it does not give a baseline error rate for your system. |
| Current models "often struggle" to restore punctuation in transcripts of spontaneous speech; the authors say this limits downstream tasks such as translation, text-to-speech, and summarization. | [Pulipaka et al., *Mark My Words*, arXiv 2506.03793](https://arxiv.org/abs/2506.03793) (submitted June 2025, marked work in progress). Abstract opened and read. | Preprint, not peer reviewed. The abstract gives no error rates for the weaker models. |
| Lab tests of pause-based models: periods identified about 87% of the time, commas 55%. "Real-world noise pushes both numbers lower." The page calls commas the hardest mark to place. | [Deepgram, speech to text automatic punctuation guide](https://deepgram.com/learn/speech-to-text-automatic-punctuation-guide). Opened and read. | **Vendor marketing page.** No method, dataset, or sample size on the page, and no size for the noise drop. Not used in the fix. |
| Subjective tests showed that "humans understand quite well" ASR-generated captions despite word and punctuation errors. | [Tündik, Kaszás and Szaszák, *Periodica Polytechnica EECS* 63(4), 2019](https://www.pp.bme.hu/eecs/article/view/14052). Abstract opened and read. | Hungarian, 2019, captions read by people. It suggests readers repair marks that software cannot, which is why an agent acting on text is at more risk than a person reading it. |

**Not used.** The PunKtuator system paper (EACL 2021): only its title and metadata could be read, so I use none of its claims. Papers on an end-to-end punctuated recognizer (Nozaki, Interspeech 2022), on medical ASR punctuation, and on punctuation and unpunctuated-output readability were seen **only in search summaries**. I found no study that measures how often a punctuation error changes the action an agent takes.

## 5. The fix
**The principle:** When a different break would change what an action covers, say how you read it and get a yes before acting.

**Do this**
1. **Mark risky sentences.** A sentence is risky when it has an action verb (cancel, send, pay, delete, refill) plus a list of 2 or more items, names, or numbers, or a correction cue ("no, wait", "I mean").
2. **Check for a second reading.** For a risky sentence, test whether moving or removing one comma or period changes which items the action covers. If yes, do not act yet.
3. **Spell out the scope.** Restate the instruction with explicit items ("Cancel Austin only; Dallas and Houston stay on hold"), never by repeating the same punctuated string.
4. **Offer the readings as choices.** Show 2-4 readings plus "Something else", with free text open.
5. **Act only on a confirmed reading** for any change to a record, an order, or money. Log the choice.
6. **Keep the user's words.** Show the transcript as heard, and do not silently "fix" marks in a record the user may rely on.
7. **Do not ask when the reading is the same either way.** If every reasonable break gives the same action, proceed.

**Reference design: scope check**
| Sentence | Readings that change the action? | Bot does |
|---|---|---|
| "Cancel the Austin order Dallas and Houston stay on hold." | Yes: cancel one order or three | Offers the readings, confirms the chosen scope |
| "Cancel order 4417." | No | Reads back the order number only |
| "Send it to Dana, not Dan." | Possible: who gets it | Reads back the recipient, then sends after a yes |

```
Before acting on dictated text, check for a list or a correction next to an action verb.
If moving one comma or period would change which items the action covers, ask which reading is meant.
State the scope in words and wait for a yes. Do not act on the punctuated string alone.
If every reading gives the same action, do not ask.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A risky sentence has two readings: show each reading in words. Do not offer them when every reading gives the same action. |
| Ask one clarifying question | Only one scope question matters ("Only Austin, or all three?"). Do not ask about marks that do not change the action. |
| Hand off to a person | The same instruction is misread twice, or the action cannot be undone and is still unconfirmed. Do not hand off if the user wants to keep typing with the bot. |

**Don't over-correct.** Do not ask about every comma. Most punctuation differences do not change an action, and a question on each message trains users to click "yes" without reading. Limit checks to action sentences with a list, a name choice, or a correction, and track how many checks the user answers with the same reading the bot first picked.

**Hand-off rule.** After two misread attempts, or an unconfirmed irreversible action, pass a person the transcript as heard, the readings offered, and what was chosen ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "Cancel the Austin order Dallas and Houston stay on hold." | Flagged as risky; the bot does not cancel yet (1, 2) |
| 2 | Same sentence | The reply states the scope in words, not the same string (3) |
| 3 | The user picks "Cancel Austin only" | Only Austin changes; the choice is logged (4, 5) |
| 4 | "Cancel order 4417." | No question; the number is read back (7) |
| 5 | An address dictated as one run-on line | The recipient and street are restated; no record changes before a yes (1, 5) |
| 6 | A correction: "Send it to Dana, no wait, Dan." | The final recipient is read back as Dan (1, 3) |
| 7 | Transcript marks differ from what the user typed in a record | The record shows the words as heard (6) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Meaning-change rate on a labelled punctuation set** (primary) | Under 2% on action and list sentences | Build a set of dictated sentences with 2 or more plausible breaks; people label whether the agent's reading matches the speaker's; count mismatches | Over 5%; any rise after a model change |
| Risky action sentences acted on without a scope read-back | 0 | Log each action with the risky flag and the confirmation flag | Any |
| Scope read-backs where the user then changes the scope | Track; lower is better | Next user turn after a read-back | Rising |
| Checks on sentences with one reading (counter-metric) | Under 10% of checks | Sampled review of checks | Over 20% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published. Signals 1 to 4 can be computed from text; the voice and web signals are PLANNED and nothing has been measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Written for text: an action verb followed by 2 or more items and no list punctuation in the same sentence | Transcript text | A user who really meant every item |
| Written for text: the user's next message after an action starts "no, I meant" or "only the" | Next user turn after the action | A change of mind, not a misread |
| Written for text: a dictated chat message of 40 or more words with no sentence-ending mark (the 40 is a starting point) | Chat input text | A pasted list or a code snippet |
| Written for text: a read-back shows a scope that differs from the first action the bot proposed | Draft action vs. read-back | A scope the user widened on purpose |
| PLANNED for voice and web dictation: a long pause inside a clause that the transcript joined, or a missing pause where it split | Needs word timings from the recognizer; none are recorded here | A speaker who pauses to think |

**Starter rule:** for an action sentence with a list or a correction, state the scope in words and wait for a yes.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds beyond the starting points above)
```yaml
pattern_id: punctuation-and-segmentation-errors
runs: pre_send
reads: [transcript.text, action.pending, action.items, action.confirmed, turn.risky_flag]
trigger: a pending action rests on dictated text with a list, a name choice, or a correction, and a different break would change its scope
moves: [offer_choices, ask_clarifying_question, hand_off]
choices: ["Cancel Austin only", "Cancel all three", "Talk to a person", "Something else"]
on_miss: ask
metric: meaning-change rate on a labelled punctuation set
counter_metric: checks on sentences with one reading
status: proposed
```

## 8. Related patterns
- [Transcription hallucination](transcription-hallucination.md): the recognizer invents words. Here the words are right and the marks between them are wrong.
- [Repair failure](repair-failure.md): the agent mishandles a spoken "no, the other one". Here a correction is also at risk because a missing mark hides where it starts.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): the same failure to apply a correction in chat.
- [Homophones confusion](../../../../speech-and-audio/goals/speech-recognition/failures/homophones-confusion.md): a wrong word that sounds right. This page covers the right word in the wrong place.
- [Number and date errors](../../../../speech-and-audio/goals/speech-recognition/failures/number-date-errors.md): spoken values captured wrongly, which also benefit from a read-back.
- [Streaming ASR instability](../../../../speech-and-audio/goals/speech-recognition/failures/streaming-asr-instability.md): interim text changes, including its marks.

## 9. Common questions
### Why does speech to text put commas and periods in the wrong place?
Speech has no written marks, so the system infers them from the words and sometimes from pauses. One Interspeech 2020 paper says word errors "often confuse" punctuation models. See [section 4](#4-why-it-matters).

### Can a missing comma really change what an AI agent does?
Yes, when an action sits next to a list. In the example, one missing comma turns "cancel one order" into "cancel three". The sources I opened show punctuation is hard in spontaneous speech, but none measures how often it changes an agent's action.

### Is automatic punctuation in speech to text accurate?
One vendor page reports lab figures of about 87% for periods and 55% for commas, and says noise lowers both. It is marketing material with no method, so test your own system on a labelled set.

### Should a voice bot ask the user to confirm every sentence?
No. Check only action sentences with a list, a name choice, or a correction, and only when a different break would change the action. See "Don't over-correct" in [section 5](#5-the-fix).

### Will a better speech model fix this?
It should help with placement, in our judgment, but spoken sentences can stay ambiguous with perfect words. Keep the read-back for actions.

---
## Technical section

### T1. Solution architecture
```
dictated text -> punctuation / segmentation -> risk check (action verb + list or correction)
              -> alternate-break test (does one move change the item scope?)
              -> reply (scope in words, choices) -> confirmation -> action
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No change to a record from a risky sentence without a confirmed scope | Action layer | Test 1, 3 |
| Scope restated in words, not the same string | Reply builder | Test 2 |
| Transcript stored as heard | Storage | Test 7 |

### T3. Evals
- **Dataset:** a labelled set of dictated sentences, each with 2 or more plausible breaks that change an action scope, plus a matched set with one reading. Start with 100 of each (starting point). Label by two people and settle disagreements.
- **Judge rubric:** does the agent's reading match the speaker's? Was a second reading offered when one existed? Was a check asked when none was needed?
- **Metrics and starting thresholds:** meaning-change rate under 2% on the risky set; unneeded checks under 10%. Starting points to tune.
- **Release gate:** block a deploy if the risky-set meaning-change rate rises or a risky action runs unconfirmed.

### T5. Trade-offs
- A read-back adds one turn; keep it to risky action sentences.
- The alternate-break test can be done by rules or a model; a model adds cost and its own errors, so test it on the same labelled set.

---
### Deep dive
- **Open question.** The sources I opened measure punctuation accuracy or translation quality. None measures meaning change in an agent that acts. The labelled set in T3 is the way to get your own number.
- **Modality notes.** Live voice and web dictation (PLANNED): word timings and pause lengths could mark clause boundaries before the text is punctuated.
- **References.** [Li et al., arXiv 2010.11132](https://arxiv.org/abs/2010.11132) (abstract opened); [Augustyniak et al., Interspeech 2020](https://www.isca-archive.org/interspeech_2020/augustyniak20_interspeech.html) (abstract opened); [Pulipaka et al., arXiv 2506.03793](https://arxiv.org/abs/2506.03793) (abstract opened); [Deepgram guide](https://deepgram.com/learn/speech-to-text-automatic-punctuation-guide) (vendor, opened); [Tündik et al. 2019](https://www.pp.bme.hu/eecs/article/view/14052) (abstract opened).
