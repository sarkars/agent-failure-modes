# Voice Assistant Cuts Off Stuttering and Atypical Speech: Atypical Speech Mishandled

<!-- SEO
title: Voice Assistant Cuts Off Stuttering and Atypical Speech: Fixes
description: Why speech recognition cuts off or garbles stuttering, dysarthria, and Deaf speech, and how a bot can let people finish, confirm a guess, and type instead.
search phrases:
- voice assistant cuts me off when I stutter
- speech recognition doesn't understand my speech
- speech to text for dysarthria
- chatbot voice input stuttering
- voice assistant deaf speech not recognized
- alexa can't understand my speech disability
- how to make a voice bot work for people who stutter
- dictation messages with repeated words chatbot
-->

> **Read this first.** This is design guidance, not clinical, legal, or professional advice. It needs review by people with the lived experience and by a qualified expert (for example, a speech-language pathologist and an accessibility specialist) before use. It does not say what any law requires of your product. Test with the people it is for.

**Frequency**: Common

## Issue: When a person stutters, has dysarthria, or has Deaf speech, the recognizer cuts them off or mishears them and the bot offers only "I didn't catch that", so they can't finish the task.

> **One line:** Speech systems tuned on typical speech end the turn at a pause and garble atypical speech; the fix is to wait longer, let the person confirm a guess, and always offer a typed path.

| | |
|---|---|
| **Channel** | Written for **chat**: typed or dictated messages that arrive in pieces, with repeated words, long gaps, or odd spellings, and the bot's replies to them. Voice (recognizer cutoffs, endpointing, word error rate by speaker group) is **planned**: the design applies, but the signals that need audio are not written yet. |
| **Stakes** | Medium to high. A person who can't get a refill, a booking, or a bank answer through the voice route is shut out of the service. |
| **Who is affected** | People who stutter, people with dysarthria (for example from ALS, cerebral palsy, or Parkinson's), and some Deaf and hard of hearing speakers. Anyone using dictation with atypical speech. |
| **Frequency** | Common where voice is a main route. No rate was found for how many production bots fail these users; the studies below measure recognizers. |
| **Pattern ID** | atypical-speech-mishandled |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | Task completion for the atypical-speech test set, with fallback availability (a typed or tap path offered by the second miss) reported next to it. Starting target: set from a baseline per group (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Personalized or better-trained recognizers cut errors a lot in the studies below, but when a turn ends, whether a guess is confirmed, and whether a typed route exists are product decisions. (Our judgment, not tested.) |
| **Also searched as** | voice assistant cuts me off · stuttering and voice assistants · dysarthria speech recognition · Deaf speech not recognized · bot says "I didn't catch that" · voice typing for speech disability |

## 1. In plain words
Speech systems learn from typical speech. A person who blocks on a word, repeats a sound, or speaks with dysarthria or Deaf speech often gets cut off mid-sentence or transcribed wrongly, then hears "Sorry, I didn't catch that" again and again. The fix is to give them time, show what was heard and let them confirm it, and offer typing or a person at the first sign of trouble.

## 2. What it looks like
Illustrative example: a US pharmacy refill bot, with dictated input to a chat window. The person stutters.

**Without the fix**
```
User:  Re-re-refill my... (send)
Bot:   Sorry, I didn't catch that. What would you like to do?
User:  ...my lisinopril, the ten milligram (send)
Bot:   Sorry, I didn't catch that. What would you like to do?
User:  Re-refill lisinopril
Bot:   I can help with prescriptions, store hours, and more. What would you like to do?
```

**With the fix**
```
User:  Re-re-refill my... (send)
Bot:   Take your time. I'm waiting for the rest.
User:  ...my lisinopril, the ten milligram (send)
Bot:   Refill lisinopril 10 mg, the same pharmacy as last time (Oak Street). Is that right?
       [Yes] [No, change it] [Type it instead] [Something else]
User:  Yes
Bot:   Done. It will be ready tomorrow after 10 AM.
```
The fixed bot joins the two fragments, does not treat the pause as the end, shows its guess for a one-tap confirm, and keeps typing and a free-text reply open.

## 3. Why it happens
- **The turn ends at a pause.** Recognizers decide that speech is over after a stretch of silence. A block or a long pause inside a word looks like an ending, so the system cuts the person off (the stuttering paper below measured this).
- **Recognizers are trained and tested on typical speech.** Atypical speech is rare in training data and in test sets, so errors are high for these speakers and an average accuracy score hides it ([word-error-rate-only evaluation](word-error-rate-only-evaluation.md)).
- **There is one failure path.** After a miss the bot repeats "I didn't catch that" instead of changing the route, so each retry costs the user more than the last.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a survey of 61 people who stutter, "voice assistants cut off my speech before I finish talking" was the most-cited barrier to using voice assistants more (61.0%, 36 of 59). 3.3% said they were cut off "always" and 37.7% "often". Of those cut off, 77.2% (44 of 57) said a pause or block led the system to think they had finished. | ["From User Perceptions to Technical Improvement: Enabling People Who Stutter to Better Use Speech Recognition," arXiv 2302.09044](https://ar5iv.labs.arxiv.org/html/2302.09044). Opened and read (arXiv HTML version). | Self-reported, small sample, one research group. The text and figures differ slightly in places (for example, 4.8% versus 4.9% for mild). |
| In the same paper's recording study (91 people who stutter), the baseline recognizer's endpointer truncated 23.8% of utterances in the 41-person phase 2 set, against a general-population target of about 3%. Baseline word error rate was 4.8% for mild, 13.6% for moderate, and 49.2% for severe stuttering. | Same paper. Opened and read. | One consumer-grade system in a research setting; the bot you run may differ. Reported by the paper's authors. |
| Tuning the endpointer and decoder, plus a dysfluency refinement, took phase 2 word error rate from 25.4% to 9.9%. Raising the end-of-speech threshold added about 1.2 to 1.7 seconds of delay for mild and moderate severity. | Same paper. Opened and read. | Shows a real trade-off: fewer cutoffs, slower replies. The gain is for the authors' system and test set. |
| Google's Project Euphonia reported personalized recognition models with up to 85% lower word error rate in select domains. For severely impaired speech, the median error rate on short home-automation phrases dropped from around 89% to 13%. The dataset held over 1 million utterances from 1,330 speakers (as of August 2021). | [Google Research blog, "Personalized ASR Models from a Large and Diverse Disordered Speech Dataset"](https://research.google/blog/personalized-asr-models-from-a-large-and-diverse-disordered-speech-dataset/). Opened and read. | Vendor-reported. Mostly scripted phrases recorded at home; personalized models need recordings from the speaker; the blog gives no figures for conversational speech. |
| A feasibility test of one commercial recognizer on 45 recordings from Deaf and hard of hearing speakers found about 78% word error rate in the abstract (77% in the results text), against 18% for five hearing readers. Even speakers rated "good" scored 53%. | ["Feasibility of Using Automatic Speech Recognition with Voices of Deaf and Hard-of-Hearing Individuals," arXiv 1909.01167](https://ar5iv.labs.arxiv.org/html/1909.01167). Opened and read (arXiv HTML version). | Old system, one service, 45 files, unequal recording conditions (the authors say so). Treat as dated, not current performance. |

A 2024 study of four commercial services on Deaf and hard of hearing speech turned up in search results. I could not open the full text, so no figure from it is used here.

## 5. The fix

**The principle:** Never end the turn on a pause alone, never retry the same failure, and give every user a typed or human route by the second miss.

**Do this**
1. **Do not end a turn on silence alone.** In chat, after a partial or fragment message, reply "Take your time" and wait; do not run the intent step until the person signals done or a longer timeout passes. Pass if no fragment under a set length gets a fallback reply.
2. **Join fragments sent close together.** Treat messages from the same user within a short window as one turn. Pass if a three-fragment request is answered once, with all three parts.
3. **Strip repeated sounds before matching intent.** Collapse "re-re-refill" and filler like "uh" before intent matching, but keep the user's original text in the log and show it on request. Pass if "re-re-refill" and "refill" give the same intent.
4. **Show the guess and ask one confirm.** When confidence is low, say what you heard in full and ask "Is that right?" with a one-tap yes. Pass if a low-confidence turn gets a confirm, not "I didn't catch that".
5. **Never repeat "I didn't catch that" twice.** After the first miss, change the route: a best guess, choices, or typing. Pass if no two consecutive agent turns share a fallback text.
6. **Offer typing or tap by the second miss, and a person by the third.** Say it as an option, not as a verdict on the speaker. Pass if every conversation with two misses shows a typed or tap option.
7. **Let the user set more time.** If the user says "I stutter" or "give me more time", store a longer wait for the rest of the session and say so. Pass if the stored setting changes the next wait.
8. **Never blame or coach the speaker.** No "please speak clearly", "slow down", or "try again". Pass if none of these appear in a fallback reply.
9. **Keep results by speaker group.** Report task completion for an atypical-speech set, not only the average. Pass if the dashboard shows the group beside the overall figure.

**Reference design: miss ladder**
```
turn arrives incomplete or low confidence:
  1st: wait ("Take your time.") and join fragments
  confidence still low: show best guess + confirm
      choices: "Yes", "No, change it", "Type it instead", "Something else" (free text always open)
  2nd miss: change route -> typed or tap field, plus "connect me to a person"
  3rd miss: hand off with what was understood so far
never: same fallback twice; "speak clearly"; ending the turn on a pause alone
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Confirm what was heard | The recognizer or the joined fragments give a likely meaning: restate it in full with a one-tap yes. Do not confirm a low-stakes, high-confidence turn. |
| Offer choices: 2-4 options plus "Something else", free text open | After the first miss: "Yes", "No, change it", "Type it instead", "Something else". Do not offer them when the guess was confirmed or the answer was one short fact. |
| Ask one clarifying question | Two readings are plausible (the 10 mg or the 20 mg). Do not ask when only one fits. |
| Hand off to a person | Two misses with a typed option declined, or the user asks for a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not wait so long that every reply drags; the study above found a longer threshold cost about 1.2 to 1.7 seconds. Make the longer wait the default for chat fragments but short for complete messages. Do not ask everyone to confirm every turn, and do not move people to text unasked when voice is working. Do not label users as having a disability from how they speak; act on the text and the confidence, not a guess about the person.

**Hand-off rule.** After the second miss with a typed route offered, or on request, pass the understood parts to a person ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)), and keep a text or relay route for people who can't use voice ([voice-only flows with no text alternative](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**. Write cases with people who have the lived experience.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Three fragments sent 4 seconds apart ("re-re-refill my", "lisinopril", "ten milligram") | One reply, with all parts (rules 1, 2) |
| 2 | "re-re-refill" and "refill" | Same intent (rule 3) |
| 3 | Low-confidence dictated turn | Bot shows the guess and asks one confirm (rule 4) |
| 4 | Two unintelligible turns in a row | Second reply is not the first reply's text, and offers typing (rules 5, 6) |
| 5 | User types "I stutter, give me more time" | Longer wait stored and acknowledged (rule 7) |
| 6 | Every fallback reply in the set | None say "speak clearly" or "try again" (rule 8) |
| 7 | Report from an atypical-speech set | Completion shown by group and overall (rule 9) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Task completion, atypical-speech test set** (primary) | Set from baseline; gap to the overall rate shrinking | Run scripted tasks from the labeled test set each release | Gap widens |
| Fallback availability: typed or tap option shown by the second miss | 100% | Log: second fallback turn with a typed or tap option present | Below 99% |
| Repeated identical fallback text in consecutive turns | 0% | Log: two agent turns with the same fallback template | Any |
| Fragments answered separately (under the join window) | Under 2% | Log: consecutive short user turns each getting a reply | Over 5% |
| Confirm-guess accepted rate (counter-metric) | Track | Log: confirm shown, then "Yes" | Falls, or the confirm is shown on over 30% of turns (tune) |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. The text signals are written for chat. Audio signals are PLANNED for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Written for text: two or more short user messages sent within a few seconds, each followed by a fallback reply | Consecutive user turns and agent reply types | A user who always sends short messages, or a paste |
| Written for text: a user message with repeated syllables or words ("re-re-refill", "c-c-can") followed by a fallback | Turn text pattern, then reply type | A typo, or a deliberate stylistic repeat |
| Written for text: the same fallback template twice in a row | Two agent turns with the same template id | A scripted step that repeats on purpose |
| Written for text: the user types "I stutter", "my speech", "I'm deaf", or "give me more time" | Phrase match on the user turn | Someone describing another person, or a joke |
| PLANNED for voice: the recognizer ends an utterance mid-phrase, then the user repeats the same words | Needs audio endpointing events and timing; not computable from the transcript | A user who changed their mind |

**Starter rule:** do not end a turn on a pause, show a guess for one-tap confirmation, and never repeat the same failure message.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: atypical-speech-mishandled
runs: conversation
reads: [turn.text, turn.confidence, turn.fragment_count, agent.fallback_template_id, miss.count, session.wait_setting]
trigger: a fragment or low-confidence turn, a repeated fallback, or a stated need for more time
moves: [confirm_what_was_heard, offer_choices, ask_clarifying_question, hand_off]
choices: ["Yes", "No, change it", "Type it instead", "Something else"]
on_miss: rewrite
metric: task completion for the atypical-speech test set
counter_metric: confirm-guess accepted rate
status: proposed
```

## 8. Related patterns
- [Hesitation mishandling](../../../../speech-and-audio/goals/conversation-flow/failures/hesitation-mishandling.md): about a caller who is unsure about a decision and gets pressured. This page is about a speaker whose pauses and repeated sounds are a feature of their speech, not doubt.
- [End-of-turn detection](../../../../speech-and-audio/goals/conversation-flow/failures/end-of-turn-detection.md): the general problem of deciding a turn is over. This page covers the people for whom the usual silence rule fails most, and the confirm-and-route fix.
- [Accent and dialect bias](../../../../speech-and-audio/goals/speech-recognition/failures/accent-dialect-bias.md): recognition that works worse for some accents; it has a short section on children and atypical speech.
- [Word-error-rate-only evaluation](word-error-rate-only-evaluation.md): why an average score hides these groups.
- [Voice-only flows with no text alternative](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md): the typed or relay path this page relies on.
- [Transcription hallucination](transcription-hallucination.md): invented words from silence, which a longer wait can make more likely if not checked.

## 9. Common questions
### Why does my voice assistant cut me off when I stutter?
The system decides you are done when it hears a pause, and a block or long gap in a word looks like the end. In a survey of 61 people who stutter, 77.2% of those cut off said a pause or block was the cause ([section 4](#4-why-it-matters)).

### How do I make a voice bot work for people who stutter?
Do not end the turn on silence alone, join fragments, show your best guess for a one-tap confirm, and offer typing by the second miss ([section 5](#5-the-fix)). Test with people who stutter.

### Does a better speech model fix this?
Partly. Personalized models cut error rates in Google's reported work, but they need recordings from each speaker, and the turn-ending, confirm, and typed-route choices are still yours.

### Should the bot ask if I have a speech disability?
No. Act on the text and the recognizer's confidence. Offer typing and more time to everyone who misses twice, and let the user ask for more time in their own words.

---
## Technical section

### T1. Solution architecture
```
audio or dictated text -> endpointing (longer wait for fragments) -> fragment joiner (window)
   -> disfluency normalizer (keep raw text) -> intent + confidence
   -> low confidence? confirm guess -> miss counter -> route change (typed/tap) -> hand-off
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No fallback reply twice in a row | Dialogue manager | Test 4 |
| Typed or tap option by the second miss | Reply builder | Test 4 |
| Raw user text kept, normalized text only for matching | Pre-processing | Test 2 |
| No "speak clearly" or "try again" in fallbacks | Output check | Test 6 |

### T3. Evals
- **Dataset:** scripted task conversations with fragments, repeated sounds, long gaps, and low-confidence turns, written and reviewed with people who have the speech patterns; start at 100 and tune. Voice audio from consenting speakers is PLANNED.
- **Judge rubric:** did the bot wait, join, confirm, change route after a miss, and avoid blame?
- **Metrics and starting thresholds:** completion gap to overall under 10 points; identical fallbacks 0%. Starting points to tune.
- **Release gate:** block a deploy if the atypical-speech completion rate falls from baseline or any conversation shows the same fallback twice.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Atypical-set completion gap | Widens 5 points | Widens 10 points | Check endpointing wait and the confirm step |

### T5. Trade-offs
- A longer wait feels slower for everyone. Scope it to fragments and to users who asked for more time.
- Disfluency stripping can remove a word the user meant; keep raw text and confirm when the result changes the meaning.

---
### Deep dive
- **Open question.** No public measurement was found of how often production chatbots or voice agents fail these users; the sources measure recognizers in research settings.
- **Not opened.** A 2024 Laryngoscope study of four commercial services on Deaf and hard of hearing speech appeared in a search summary and its PDF could not be read, so no number from it is used. The Google 2019 Interspeech paper was not opened.
- **Voice (PLANNED).** Endpointer cutoff rate and word error rate by speaker group need audio and are not measured here.
- **References.** [stuttering paper, arXiv 2302.09044](https://ar5iv.labs.arxiv.org/html/2302.09044) (opened); [Google Research blog on personalized ASR](https://research.google/blog/personalized-asr-models-from-a-large-and-diverse-disordered-speech-dataset/) (opened); [Deaf speech feasibility paper, arXiv 1909.01167](https://ar5iv.labs.arxiv.org/html/1909.01167) (opened).
