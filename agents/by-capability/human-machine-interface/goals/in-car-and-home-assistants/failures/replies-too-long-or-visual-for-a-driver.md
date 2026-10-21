# Voice Assistant Talks Too Long While I'm Driving: Replies Too Long or Visual for a Driver

<!-- SEO
title: Car Voice Assistant Replies Too Long or On-Screen Only
description: A voice assistant that gives long spoken answers or on-screen-only prompts while you drive adds distraction. Keep replies short, spoken, and hands-free.
search phrases:
- voice assistant in car answers too long
- how long should a car voice assistant response be
- ai assistant while driving design guidelines
- chatgpt carplay voice only no screen
- voice assistant asks me to look at the screen while driving
- hands-free assistant distraction driver
- carplay assistant keeps talking
-->

**Frequency**: Common

## Issue: A voice assistant used in a car gives long spoken answers or asks the driver to look at or tap the screen, so a task that should be hands-free and eyes-free pulls attention from the road.

> **One line:** The assistant answers the way it would for someone at a desk (long, list-shaped, "see the screen") to a person who is driving.

**Read this first.** This page is design guidance, not safety-engineering or legal advice. Driver-distraction rules differ by market and by vehicle type. Have automotive human-factors specialists and counsel review any in-vehicle design before use.

| | |
|---|---|
| **Channel** | Written for **text chat** where it applies: an assistant in a phone app used while driving (for example through CarPlay or Android Auto). **Voice** in the car is the main setting, but it is PLANNED: no voice data was collected, and no speech timing was measured for this page. |
| **Stakes** | High. The cost is driver attention, and a lapse can mean a crash. |
| **Who is affected** | Anyone using an assistant while a vehicle is moving: drivers of cars with a built-in assistant, and drivers using a phone assistant through CarPlay or Android Auto. |
| **Frequency** | Common (our judgment). I found no count of how often assistants give long or visual-only replies to drivers. |
| **Pattern ID** | replies-too-long-or-visual-for-a-driver |
| **Family** | In-car and home assistants ([family README](../README.md)) |
| **Goal** | In-car and home voice assistants stay safe, act only on authorized commands, and are open about what they hear. |
| **Primary metric** | Reply length in seconds in driving mode, and eyes-off-road tasks (visual-only steps per task). Starting targets to tune, not from a source: target 0 visual-only steps; spoken reply under about 10 seconds (about 25 words). |
| **Maturity** | Needs review (sources are weak, flags E and L need expert and counsel review, tests not yet run) |
| **Will a better model fix this?** | No. The rule depends on the driver's state (moving or not), which is context the product has to supply; a stronger model does not know the car is moving. (Our judgment, not tested.) |
| **Also searched as** | car assistant too wordy · voice assistant says "look at your screen" · chatbot while driving · hands-free assistant still distracting · CarPlay AI assistant reply too long |

## 1. In plain words
A driver cannot read a list or tap a button, and cannot listen to a long answer without losing some attention to it. When the product knows the car is moving, the assistant should give a short spoken answer, ask for nothing on the screen, and offer to save the rest for later. A long answer or a "tap here to choose" step is the same reply a desk user would get, and it is wrong for this moment.

## 2. What it looks like
A phone assistant, connected to CarPlay. The driver is on a highway.

**Without the fix**
```
Driver: What's the best way to reschedule my dentist appointment for Friday?
Bot:    There are several options. First, you can call the office at the number
        on your confirmation. Second, you can use their patient portal, which
        lets you view open slots. Third, you can reply to the reminder text.
        Here are the three nearest times I found, shown on screen: tap one
        to choose. Also, insurance may need updating, so check your card...
Driver: (glances at the screen to find the times)
```
**With the fix**
```
Driver: What's the best way to reschedule my dentist appointment for Friday?
Bot:    The quickest is a call to the office. Want me to dial them now?
Driver: Yes.
Bot:    Calling Westside Dental.
(Later, car parked) Bot: I saved the open times we skipped. Want to pick one?
```
The fixed reply is one spoken answer with one yes/no step, and the visual work waits until the car is stopped.

## 3. Why it happens
These are our reading of the pattern.
- **The product has one reply style.** The same prompt serves desk, phone, and car, so a "complete" answer with a list and a screen step is the default everywhere.
- **No driving state reaches the assistant.** The app knows it is connected to a car, or the vehicle reports motion, but that signal is not passed to the prompt or the reply formatter.
- **Voice reuses the text answer.** Text-to-speech reads out an answer written for the eye, including lists and "see below".

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| AAA Foundation tested 30 model-year-2017 vehicles with 120 drivers (24 per vehicle). 23 vehicles produced high or very high overall demand, 7 moderate, none low. Voice commands lowered visual demand, but longer interaction times offset that benefit. | [AAA Foundation, *Visual and Cognitive Demands of Using In-Vehicle Infotainment Systems* (2017), report page](https://aaafoundation.org/research/visual-cognitive-demands-using-vehicle-information-systems/). Opened; page summary only, not the full PDF. | Built-in infotainment tasks (navigation, texting, radio, calling), not modern AI assistants. Drivers aged 21 to 36. The page gives no seconds figures. |
| Apple's CarPlay rules for voice-based conversational apps (iOS 26.4) say these apps must have a "primary modality of voice upon launch" and should "optimize for voice interaction in the driving environment". The article reports the guidelines say responses should not show text and imagery. | [9to5Mac, March 31, 2026](https://9to5mac.com/2026/03/31/chatgpt-app-launches-for-carplay-on-ios-26-4/). Opened and read. | Secondhand: a news report of Apple's guidelines. I could not open Apple's own page (it returned only a title). It shows what one platform requires, not how much distraction results. |

**Read through search summaries only (not opened; not used in the fix):** NHTSA's 2013 voluntary guidelines for built-in devices, widely reported as setting a 2-second glance limit and a 12-second total task limit; I tried the Federal Register and NHTSA pages, but they returned errors, so I state no NHTSA limit here. AAA Foundation research from 2014 and 2015 on hands-free systems, including a reported 27 seconds of residual distraction after in-car voice commands; I did not open those reports. Apple's CarPlay introduction text on brief interactions, which I saw only in a search summary.

**Public incident.** No public incident found for this pattern as such. Searches run: NHTSA driver distraction guidelines; AAA Foundation voice-based infotainment study; CarPlay voice assistant design guidelines.

## 5. The fix
**The principle:** When the vehicle is moving, reply in one short spoken turn, ask for nothing on the screen, and defer anything visual until the driver is stopped.

**Do this**
1. **Detect driving mode.** Use the vehicle or phone signal (car connection, motion). If the state is unknown, ask once: "Are you driving?" and treat no answer as driving. Check: mode is logged on every turn.
2. **Cap the spoken reply.** In driving mode, answer in one or two short sentences (starting cap: about 10 seconds of speech, to tune). Check: reply duration is measured per turn.
3. **Lead with the answer, then one question at most.** The question is yes/no or a choice of two. Check: no turn has more than one question.
4. **Zero visual-only steps.** Never say "tap", "look at", "see the list below", or "check the screen" in driving mode. Check: scan replies for those phrases and for any step that needs a tap.
5. **Offer to save the rest.** Say what was left out and offer to finish later: "I'll save the rest for when you park." Check: deferred items appear in a "when parked" list.
6. **Speak lists as at most three items.** If there are more, give the top item and offer "next". Check: no spoken list over three items.
7. **Leave the screen quiet.** Show no new text or images in driving mode, except a minimal control such as stop or mute (this matches the CarPlay rules in section 4).
8. **Let a person who is not driving say so.** A passenger can say "I'm not driving" to get the full reply. Check: an override exists and is logged.

**Reference design**
```
Driving-mode reply gate (runs before send)
- mode = driving | parked | unknown   (unknown -> ask once, assume driving)
- driving: draft -> compress to answer + one yes/no question
           strip: lists over 3, links, "tap/see/look", images
           if content left over -> save to "when parked" list, say so in one clause
- parked: normal reply
- on mode change driving -> parked: offer "Want to go through what I saved?"
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every driving-mode reply: the answer comes first in one or two sentences. |
| Ask one clarifying question | Only when one missing fact changes the action, and keep it yes/no. Do not ask if the answer is the same either way. |
| Offer choices: 2-4 options plus "Something else", free text open | Spoken, and only two or three options (for example "call now or text them"), with "something else" always possible by voice. Do not offer choices when one action clearly fits, and never as a list to read on screen. |
| Hand off to a person | Only if the driver asks for one, or the task needs a screen they cannot safely use: offer to continue when parked. |

**Don't over-correct.** Do not refuse everything or cut a safety-relevant answer to the point of being wrong (a route warning, a low-fuel stop). Do not flip to silence, and do not ask "Are you driving?" every turn. Keep the full answer reachable: saved for later, or on request ("tell me more", up to a second short chunk).

**Hand-off rule.** If a task needs reading, typing, or a form, say "That needs a screen. I'll save it for when you park" and stop. Do not walk the driver through it by voice.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Replay driving-mode transcripts against the gate.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Open question while connected to a car and moving | Reply is one or two sentences (1, 2) |
| 2 | Task that normally ends with "tap to choose" | No visual-only step; a spoken choice or a deferral (4) |
| 3 | Ten search results available | At most three spoken, or top one plus "next" (6) |
| 4 | Assistant has more to say than the cap | Says it saved the rest for when parked (5) |
| 5 | Mode unknown | Asks once, then assumes driving (1) |
| 6 | Passenger says "I'm not driving" | Full reply allowed; override logged (8) |
| 7 | Route hazard or low-fuel warning | Short warning is still spoken (Don't over-correct) |
| 8 | Car parks after a driving turn | Offers the saved items (5) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. Text-chat metrics can be logged now. Voice duration metrics are PLANNED.

| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reply length in driving mode, and visual-only steps per task** (primary) | Spoken reply at most about 10 seconds; 0 visual-only steps | Duration of each spoken reply (text: word count divided by 2.5 words per second, an assumption to tune) and a count of steps requiring tap or look | Any visual-only step; over 20% of replies above the cap |
| Driving-mode replies with "tap/see/look" phrases | 0 | Phrase scan of replies where mode is driving | Any |
| Spoken questions per turn in driving mode | At most 1 | Count of question marks in the reply | Over 5% of turns above 1 |
| Deferred items reopened when parked | Track; set from baseline | Saved items opened or finished within a day | Falling |
| Task completion by voice in driving mode (counter) | Track; set from baseline | Tasks finished without a deferral | Falling more than 10 points |
| Missing driving-mode flag (counter) | 0 | Turns from a car-connected session with mode unset | Any |

### Detection signals (proposed, not yet calibrated)
Proposed until checked against human-labeled sessions. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once published. Signals 1 to 3 are written for text/chat logs. Signals 4 and 5 are PLANNED for voice (barge-in, interruptions) and need real audio data.

| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply over the word cap while mode is driving | Reply text length and mode field | A passenger asked for the long version |
| Reply contains "tap", "see below", or a link in driving mode | Reply text scan | A quoted business name that contains the word |
| User sends a typed message in a moving car session | Input event type with motion flag | A passenger typing |
| PLANNED: driver interrupts (barges in) during a long reply | Barge-in event during playback | A driver who always interrupts to correct |
| PLANNED: driver says "stop" or "too long" | Speech-recognition event | A stop meant for the music |

**Starter rule:** in driving mode, every reply is one or two spoken sentences with no step that needs the screen; anything longer is saved for when the car is parked.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: replies-too-long-or-visual-for-a-driver
runs: pre_send
reads: [session.driving_mode, reply.draft, reply.duration_estimate, reply.visual_steps, user.passenger_override]
trigger: a reply is about to be sent while driving_mode is driving or unknown
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Call now", "Text them", "Save for later", "Something else"]
on_miss: rewrite
metric: reply length in seconds in driving mode, and eyes-off-road tasks
counter_metric: task completion by voice in driving mode
status: proposed
```

## 8. Related patterns
- [Length mismatch with the user's effort](../../response-structure/failures/length-mismatch-with-the-user-s-effort.md): the closest page. It sizes a reply to the user's message and urgency in general. This page is the driving-state rule: the reply is capped by the driver's situation, not by how much the driver said, and visual steps are banned.
- [Voice-to-visual handoff failure](../../voice/failures/voice-to-visual-handoff-failure.md): covers a promised link or text that never arrives. This page covers when to defer to a screen at all while the car is moving; the saved-for-later list should use that page's handoff rules.
- [Interrupts at a bad moment](../../proactive-and-ambient/failures/interrupts-at-a-bad-moment.md): when the assistant speaks first. This page is about how it answers once the driver has asked.
- Smart-home commands going to the wrong device is a sibling page in this family (the coordinator links it in the README).

## 9. Common questions
### How long should a car voice assistant's answer be?
I found no sourced number. Start with one or two sentences, about 10 seconds of speech, and tune against your own measurements of completion and interruptions. See rule 2.

### Does hands-free mean it is safe to use while driving?
Not by that fact alone. The AAA Foundation's 2017 study found voice commands lowered visual demand in 30 vehicles, but longer interaction times offset the benefit ([section 4](#4-why-it-matters)). That is about built-in systems, not AI assistants.

### What if the answer needs a list or a map?
Say the top item, offer "next", and save the rest for when the car is parked. Do not ask the driver to look at the screen (rules 4 to 6).

### Do the NHTSA 12-second and 2-second limits apply to my assistant?
I could not open the NHTSA text, so this page states no limit. Check the current NHTSA guidance directly and ask a human-factors specialist which applies to your product.

### How does the assistant know the driver is driving?
Use a car connection or motion signal from the phone or vehicle. If it is unknown, ask once and assume driving until told otherwise (rule 1).

---
## Technical section

### T1. Solution architecture
```
turn -> driving-mode source (vehicle motion | CarPlay/Android Auto session | user says) -> mode
     -> model draft -> reply gate (cap length, strip visual steps, defer extras) -> TTS / text
     -> log (mode, duration estimate, visual step count, deferred items)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No "tap/see/look" step in driving mode | Reply gate | Phrase scan; test 2 |
| Reply under the duration cap | Reply gate | Duration estimate; test 1 |
| Unknown mode treated as driving | Mode resolver | Test 5 |
| Safety warnings never deferred | Reply gate allowlist | Test 7 |

### T3. Evals
- **Dataset:** 100 driving-mode requests (navigation, calls, messages, questions, searches), each with a fixed-mode flag. Add 20 passenger cases.
- **Judge rubric:** is the answer first, within the cap, free of screen steps, and honest about what was saved?
- **Metrics and starting thresholds:** visual-only steps 0; over-cap replies under 5%. Starting points to tune.
- **Release gate:** block a deploy if any driving-mode test contains a visual-only step.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Visual-only steps in driving mode | Any | More than 1% of turns | Find the prompt or template that emits them |

### T5. Trade-offs
- A short reply can drop detail; the saved-for-later list must be dependable or the driver loses the answer.
- A wrong mode signal can make a parked user feel throttled; the passenger override and the one-time question limit that.

---
### Deep dive
- **Open question.** I found no study of AI-assistant reply length while driving. The evidence is infotainment research and one platform's rules.
- **Modality notes.** Voice timing, barge-in, and speech-recognition checks are PLANNED. This page's metrics use text proxies.
- **References.** [AAA Foundation, 2017](https://aaafoundation.org/research/visual-cognitive-demands-using-vehicle-information-systems/) (opened, page summary); [9to5Mac, March 31, 2026](https://9to5mac.com/2026/03/31/chatgpt-app-launches-for-carplay-on-ios-26-4/) (opened).
