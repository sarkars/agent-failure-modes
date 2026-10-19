# Voice Assistant Can't Take a Correction: "No, the Other One" and "Say That Again" Fail

<!-- SEO
title: Voice Assistant Won't Take a Correction: How to Fix Voice Repair Failures
description: Why voice agents fail on "no, the other one" and "say that again", what studies of spoken corrections and smart-speaker breakdowns found, and a repair design with targeted questions, a stop word, and a switch to a screen or a person.
search phrases:
- voice assistant ignores my correction
- alexa doesn't understand when i correct it
- voice bot keeps mishearing me after i repeat
- how to design error recovery for voice assistants
- phone bot won't let me correct my answer
- speech recognition corrections misrecognized
- voice agent repeat that please design
-->

**Frequency**: Very Common

## Issue: In a voice conversation, the user corrects a detail ("no, the other one") or asks for a repeat ("say that again"), and the agent does not understand, ignores it, or keeps the old value.

> **One line:** The caller fixes it out loud, and the agent carries on as if they had not.

| | |
|---|---|
| **Channel** | Written for **voice** (phone agents, smart speakers, in-car and kiosk voice). Chat corrections are in [corrections not applied](../../dialogue-management/failures/corrections-not-applied.md). |
| **Stakes** | Low to high. A wrong date, name, or number on a booking, a payment, or a medical call can matter. |
| **Who is affected** | Everyone, most of all people with accents, speech differences, or noisy settings, who correct most often |
| **Frequency** | Common. Studies below observe corrections being misrecognized and abandoned requests in field use; I found no rate for production agents. |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | Correction-success rate: user corrections that end with the right value in the final state. Starting target: set from a baseline (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/repair-failure.md); not yet run) |
| **Will a better model fix this?** | Partly. Recognition improves, but spoken corrections are harder, and the repair design (targeted questions, a channel switch) is a product choice. (Our judgment, not tested.) |
| **Also searched as** | voice bot won't let me fix it · repeat that · mishears twice · bot ignores no · speech repair |

## 1. In plain words
On a screen, a person edits the wrong field. In voice, the only tool is to say it again, usually louder and slower. Studies of spoken systems found that those repeats are themselves often misrecognized. If the agent has no plan for repair, the caller loops.

## 2. What it looks like

**Without the fix**
```
Agent:  I have you booked for Thursday at 3. Is that right?
Caller: No, Tuesday.
Agent:  Great, Thursday at 3 it is. Anything else?
Caller: No! TUES-day.
Agent:  I'm sorry, I didn't catch that. Thursday at 3?
```

**With the fix**
```
Agent:  I have you booked for Thursday at 3. Is that right?
Caller: No, Tuesday.
Agent:  Tuesday at 3, is that right?
Caller: Yes.
Agent:  Done: Tuesday at 3. I've texted you the confirmation.
```
The fixed agent changes only the day, reads the new value back, and gets a clear yes.

## 3. Why it happens
These are our reading of the pattern, with the sourced causes marked.
- **Corrections are harder to recognize.** In a spoken dialogue study, corrections were misrecognized more often than ordinary turns, and corrections differed from other speech in ways consistent with hyperarticulation.
- **People change how they speak when repairing.** Another study found users lengthen speech and pauses and alternate wording over repeated correction attempts.
- **No repair plan.** The agent treats "no" as a new turn instead of a pointer to the last thing it said.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In the TOOT spoken dialogue system, corrections differed prosodically from other turns in ways consistent with hyperarticulation, and corrections were misrecognized more frequently than non-corrections though no more likely to be rejected; corrections farther from the error were recognized more poorly; strategies with longer tasks but fewer misrecognitions were preferred by users. | [Swerts, Litman and Hirschberg, *Corrections in spoken dialogue systems*, ICSLP 2000](https://doi.org/10.21437/ICSLP.2000-344). Opened and read. | A 2000 research system. Speech recognition has changed; the user-behavior finding is the useful part. |
| In a simulated error-resolution study, when correcting persistent errors users adapted in three ways: increasing linguistic contrast by alternating input modes and wording, hyperarticulating (lengthening speech and pauses, more final falling contours) with verbatim speech, and suppressing variability in amplitude and pitch when hyperarticulating. | [Oviatt, Bernard and Levow, *Linguistic adaptations during spoken and multimodal error resolution*, Language and Speech, 1998](https://research.monash.edu/en/publications/linguistic-adaptations-during-spoken-and-multimodal-error-resolut/). Opened; abstract read. | A simulation with a 1990s setup. It describes what users do, not what current systems handle. |
| In a five-week field study of nine families using Alexa, the number of abandoned failed requests had a significant negative effect on satisfaction while successfully repaired requests had no influence on it; users were more inclined to reformulate when they did not see the breakdown as their fault. | [*"Alexa, You're Really Stupid"*, Frontiers in Computer Science, Jan. 2022](https://www.frontiersin.org/articles/10.3389/fcomp.2022.791704/full). Opened; abstract read. | Nine families, one device, five weeks. The authors call their statistical picture mixed. |

I also saw a CHI 2018 study of 12 participants and a calendar voice assistant, known to me only through a search summary (the page I opened held only the title), so I do not use its findings. I found no study of repair in production phone agents.

**Public incident.** A related, dated case: [McDonald's pulled its AI drive-thru after viral order chaos (June 2024)](https://agent-kb-autopublish.vercel.app/incidents/mcdonalds-ai-drive-thru-shutdown/), which the site reports included an agent that kept adding items after the customer said "stop". It is adjacent, not a direct match.

## 5. The fix

**The principle:** Treat a correction as a pointer to the last thing said, fix only that, confirm it, and have a second way out when speech keeps failing.

**Do this**
1. **Recognize correction turns.** "No", "not that", "the other one", "I said", and a repeat of a slot with a different value all point to the last prompt.
2. **Repair the slot, not the whole turn.** Change only the value in question and keep the rest.
3. **Ask a targeted question when unsure.** "Tuesday or Thursday?" beats "Sorry, I didn't catch that".
4. **Read the new value back and wait for a yes.** Do not move on until it is confirmed.
5. **Expect harder audio on corrections.** Allow for slower, louder, more pause-heavy repeats; do not drop them for low confidence without a targeted question.
6. **Vary the repair.** After one failed repair, change method: spell it, use digits, send a text or link, or switch to a screen.
7. **Honor "say that again" and "stop" at once.** Repeat the last prompt in a shorter form, and stop any action in progress ([order mix-ups at the speaker](../../drive-thru-agents/failures/order-mix-ups-at-the-speaker.md)).
8. **Hand off after two failed repairs** to a person or a channel that shows the value ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Reference design: repair ladder**
| Attempt | Agent does |
|---|---|
| 1 | Targeted question with the two likely values, then readback |
| 2 | Change method: spell or digits, or send a text or link |
| 3 | Hand off to a person or a screen with the details so far |

```
When the caller says no, not that, or the other one, treat it as a correction to the last thing you said. Change only that detail and read the new value back.
If unsure, ask a short either-or question. Do not say only "I didn't catch that".
After one failed repair, change method (spelling, digits, a text link). After two, hand off to a person or a screen.
If the caller says stop, stop what you are doing at once.
```

**Don't over-correct.** Do not read back every detail of every turn, which slows calls. Do not ask the caller to repeat when you already have a confident, corrected value. Do not treat every "no" as a correction ("No, that's all" ends the call).

**Hand-off rule.** Pass the person the corrected and uncorrected values and what was tried ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/repair-failure.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "No, Tuesday" | The day changes and is read back |
| 2 | "Say that again" | The last prompt is repeated, shorter |
| 3 | A correction in noise | A targeted question, not a generic apology |
| 4 | Two failed repairs | A new method or a hand-off |
| 5 | "Stop" mid-action | The action stops |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Correction-success rate** (primary) | Set from baseline; higher is better | User corrections that end with the right value in the final state, from a labeled sample | Falling |
| Abandoned failed requests | Track; lower is better | Calls or requests ending in a failure with no fix | Rising |
| Generic "didn't catch that" replies | Under 5% of repair turns | Log | Over 10% |
| Repair method changes after one failure | Over 95% | Log: second repair uses a different method | Below 85% |
| Added call time from readbacks (counter-metric) | Track | Median call time | Rising by more than a set margin |

## 8. Related patterns
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): the same failure in chat.
- [Override signal failures](../../../../speech-and-audio/goals/conversation-flow/failures/override-signal-failures.md): stop and override signals in voice.
- [Slot extraction errors](../../../../speech-and-audio/goals/conversation-flow/failures/slot-extraction-errors.md): wrong values captured from speech.
- [Incremental capture failures](../../../../speech-and-audio/goals/conversation-flow/failures/incremental-capture-failures.md): building values over several turns.
- [Order mix-ups at the speaker](../../drive-thru-agents/failures/order-mix-ups-at-the-speaker.md): a voice setting where this failure costs money.

## 9. Common questions
### Why does a voice assistant mishear me even more when I repeat myself?
Studies I opened found corrections were misrecognized more often than ordinary turns and that people change how they speak when repairing. A design that expects this asks a targeted question.

### How should a voice agent handle "no, the other one"?
Treat it as a pointer to the last thing said, change only that detail, and read the new value back.

### What should a voice bot do after two failed repairs?
Change method (spell it, digits, a text link) or hand off to a person or a screen.

### Does repairing a request successfully make users satisfied?
In one five-family Alexa study, successful repairs had no measured effect on satisfaction, while abandoned failures lowered it. Avoid the failures first.

---
## Technical section

### T1. Solution architecture
```
audio -> speech recognition (n-best, confidence) -> correction detector (cue words + slot match)
      -> slot repair (overwrite one slot) -> targeted question (n-best values) -> readback + confirm
      -> repair counter -> method switch (spell / digits / text link) -> hand-off
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| A correction changes one slot, not the whole state | Dialogue manager | Test 1 |
| Repair method changes after a failure | Dialogue manager | Log check |
| Stop halts any action | Action layer | Test 5 |

### T3. Evals
- **Dataset:** 150 recorded or synthetic calls with corrections (including hyperarticulated repeats, noise, and accents) and 30 "stop" cases.
- **Judge rubric:** is the final value right, was it read back, was the method varied after a failure?
- **Metrics and starting thresholds:** correction success set from baseline; stop honored 100%. Starting points to tune.
- **Release gate:** block a deploy if correction success falls or a stop is ignored.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Correction success | Falls 5 points | Falls 10 points | Check recognition and the correction detector |

### T5. Trade-offs
- Readbacks lengthen calls; keep them to corrected values and risky fields.
- A text link is a good fallback only where the caller has a phone that can receive it.

---
### Deep dive
- **Open question.** The correction studies are old systems and small samples. I found no study of repair in production LLM phone agents.
- **References.** [Swerts et al., ICSLP 2000](https://doi.org/10.21437/ICSLP.2000-344) (opened); [Oviatt et al., 1998](https://research.monash.edu/en/publications/linguistic-adaptations-during-spoken-and-multimodal-error-resolut/) (abstract opened); [Frontiers in Computer Science, 2022](https://www.frontiersin.org/articles/10.3389/fcomp.2022.791704/full) (abstract opened).
