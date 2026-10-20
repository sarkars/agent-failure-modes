# Voice Assistant Deaf Users Text Option: Voice-Only Flows With No Text Alternative

<!-- SEO
title: Voice Assistant Deaf Users Text Option: Fix Voice-Only Flows
description: Why a phone or voice assistant feature locks out deaf and hard of hearing people, and how to give every voice flow a text or relay path you can test.
search phrases:
- voice assistant deaf users text option
- IVR accessibility for deaf callers
- phone bot no text alternative
- voice-only chatbot accessibility
- does AI phone agent accept relay calls
- real-time text for customer service phone line
- voice agent accessibility checklist
-->

**Frequency**: Occasional

## Issue: A phone or voice feature that works only by speaking and listening locks out people who are deaf or hard of hearing; the fix is a text or relay path for every voice flow.

> **One line:** The only way to do the task is to talk and listen, so a person who can't hear or speak well on the phone has no way to finish it; every voice flow needs a text-equivalent path that reaches the same outcome.

> **Read this first.** This page is design guidance, not legal advice. Have a qualified person (a lawyer or accessibility specialist) review any voice or phone flow before you rely on it. The page names rules and services only as far as the sources I opened say (listed in section 4), and it makes no claim about what the law requires of any specific company. **Voice is PLANNED for measurement in this library:** the signals and tests here are "written for text/chat events" or "planned for voice". No voice data was collected, and voice signals are not yet measured.

| | |
|---|---|
| **Channel** | Written for **chat** events and design review. **Voice: PLANNED**, not measured. |
| **Stakes** | Medium to high. It can block billing, appointments, or urgent help. |
| **Who is affected** | People who are deaf or hard of hearing, and anyone who can't speak or hear on a call (noise, speech disability, shared space) |
| **Frequency** | Occasional. I found no count of how often voice-only flows lack a text path. |
| **Pattern ID** | voice-only-flows-with-no-text-alternative |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Voice journeys with a text-equivalent path. Target: 100% (planned for voice; count by design audit, not by call data). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Better speech recognition does not help a caller who can't hear the prompts; the product has to offer a text path. (Our judgment, not tested.) |
| **Also searched as** | voice assistant for deaf users · IVR for deaf callers · phone bot no text option · AI phone agent relay calls · voice-only customer service · RTT customer service |

## 1. In plain words
Some features only work if you can talk and listen: a phone menu, a voice assistant, an AI agent that answers calls. A person who is deaf or hard of hearing may hear none of it. If there is no typed route to the same result, they are stuck. The fix is simple to state and easy to test: for every task you can do by voice, there is a text or relay route that finishes the same task.

## 2. What it looks like
**Without the fix** (a clinic's AI phone line, text version of the call as a relay operator would read it out)
```
Relay operator (typing for caller): Hi, I need to move my appointment on Friday.
Bot:  Please say your date of birth.
Relay operator: (reads typed date) March 3, 1984.
Bot:  Sorry, I didn't catch that. Please say your date of birth.
Relay operator: March 3, 1984.
Bot:  I'm having trouble hearing you. Goodbye.   [call ends]
```
**With the fix** (same clinic, after the rules in section 5)
```
Relay operator: Hi, I need to move my appointment on Friday.
Bot:  This is the clinic's assistant. You can also text or chat with me at any time. Want that instead?
Relay operator: Relay call here. Please stay on the line and wait for typing.
Bot:  Relay call noted. I will go at your pace and I won't hang up on silence. What is your date of birth?
Relay operator: March 3, 1984.
Bot:  Thanks. Your Friday visit is at 10:00 AM. Want a new time, or should I send you a link to pick one in text?
```
What changed: the bot named a text route in its first turn, treated a relay call as a normal call, and stopped hanging up on slow input.

## 3. Why it happens
- **Voice is built as a channel of its own.** The phone flow is designed for people who hear and speak, so the text route is a separate product, if it exists at all.
- **Nobody tests the flow without audio.** Teams test with a microphone. They don't walk the same journey with sound off or through a relay call.
- **The text path stops short.** Chat exists but can't do what the phone flow can (verify identity, change a booking), so a deaf caller is sent back to a phone.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG success criterion 1.2.1 (prerecorded audio-only content) names "People who are deaf, are hard of hearing" as people who benefit from a text alternative; the intent is to make audio information "available to all users." Opened. | [W3C Understanding SC 1.2.1](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html) | It covers prerecorded content only ("information that is not live"). Live and two-way calls fall under other criteria. Used here as design reasoning, not as a rule for voice agents. |
| The W3C technique G158 offers a transcript as a way to present audio-only information, and its test is whether the transcript matches the audio and names speakers. Opened. | [W3C technique G158](https://www.w3.org/WAI/WCAG22/Techniques/general/G158.html) | Techniques are "not required" to meet WCAG, per the page. It's about prerecorded audio, not a live call. |
| WCAG 2.2.1 "Timing Adjustable" (Level A) aims to give users with disabilities "adequate time to interact"; people who type slowly or use assistive tools can need more time. Opened. | [W3C Understanding SC 2.2.1](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html) | Written for web content. I use it to justify no-hang-up-on-silence timing in a call, which is my extension. |
| ADA.gov says staff who answer the phone "must treat relay calls just like other calls," and describes the free relay service reached by calling 7-1-1, where an operator relays what the caller types. Opened. | [ADA.gov, Effective Communication](https://www.ada.gov/resources/effective-communication/) | The page states it is guidance with "no legally binding effect." It is addressed to covered entities and says nothing about AI agents. Not a statement about your company. |
| A 2013 US Department of Justice settlement with a Maryland law firm and collection agency recites that it "directed its employees to refuse to accept calls made by individuals with disabilities through relay services" and that staff told relay callers to call back when a manager was available. Opened. | [DOJ settlement, Peroutka and Peroutka](https://archive.ada.gov/peroutka_sa.htm) | A settlement, not a court finding. Human staff refusing relay calls, not an AI voice agent. It shows the same blocked journey, nothing more. |
| A vendor blog says "Every voice capability needs a text equivalent" and "Poor captions may be worse than none." Opened. | [TestParty, Feb 23, 2025](https://testparty.ai/blog/accessible-voice-chatbots-multimodal-interfaces) | Vendor marketing; contains no data. Treated as opinion and kept out of the fix. |

**Public incident:** No public incident found of an AI voice agent with no text route. Searches run: "voice assistant deaf users text option", "chatbot voice assistant deaf users text option accessibility voice-only", "deaf customers phone-only customer service no text option complaint lawsuit relay calls refused", and the three topic searches in the research log below. The one adjacent case opened is the human-staff settlement above. Other enforcement and lawsuit cases appeared only in a search summary and are not used.

**Not opened:** FCC relay-service guides returned access errors (HTTP 403) when I tried to open them. Nothing on this page states FCC rules, relay types, or 711 coverage beyond what the ADA.gov page I opened says. A CSUN thesis on voice-assistant access for deaf users was found in a search summary only and is not used. Summary-only items stay out of the fix.

## 5. The fix
**The principle:** For every voice flow, a person can reach the same outcome by text or relay, and can choose it at the start, not after the voice flow fails.

**Do this**
1. Keep a list of every voice journey (each task a caller can complete). Each one has a named text-equivalent path that reaches the same result. Pass if the list has no journey marked "voice only."
2. Say the text route in the first turn of a voice flow, in plain words ("You can also text or chat with me"). Pass if a transcript's first bot turn names it.
3. Accept relay calls like any other call. Never end or transfer a call because the caller is a relay operator or because input is slow. Pass if a scripted relay call completes the task.
4. Don't use silence or a speech-recognition miss as the only exit. After one failed voice turn, offer the text route. Pass if the second bot turn after a miss names the route.
5. Give typed input extra time. No hang-up or timeout on slow replies before the bot asks if the caller needs more time. Pass if no call ends within the stated wait with no prompt.
6. The text path can do everything the voice path can, including identity checks and changes. If it can't, say so and say what will. Pass if each voice task works in text, or the bot names the exact gap.
7. Send a text summary of what was done, so the outcome doesn't exist only as audio. Pass if each completed voice task produces a text record.
8. Test with deaf and hard of hearing people before launch, and re-test after changes. Pass if a test with at least one such user is on file for the release.

**Reference design** (a decision table for the first and second turns of any voice flow)
| State | Bot does |
|---|---|
| First turn | Greets, names the assistant, offers a text/chat route in one sentence |
| Caller says "relay," or a relay operator speaks | Treats as a normal call; slows down; no hang-up on silence |
| One failed voice turn | Offers the text route and asks which the caller prefers |
| Caller picks text | Sends a link or switches to chat with the task and what's been said so far |
| Text route can't do the task | Says so and says what will happen next (person, callback by text) |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | First turn and after a failed voice turn: "Keep talking, text me a link, or chat with a person. Something else?" |
| Ask one clarifying question | When the caller seems stuck: "Would you rather type? I can wait." |
| Hand off to a person | When the text route can't finish the task, or after two failed turns |

**Don't over-correct** Don't force text on callers who chose voice, and don't assume that anyone who is slow is deaf. Offer once, in the first turn and after a miss, not on every turn. Don't add a menu with no way out: "Something else" always works. Don't hide the voice route either.

**Hand-off rule** Hand off to a person who accepts relay and text when the task can't be done by text, after two failed turns on either route, or when the caller asks for a person. Send what has been said so far with the handoff, so the caller does not start over (see [no channel switch or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md)). Where the person is not available, say when they will be, and offer a text callback.

**Framework used:** [Conversation moves](../../../solutions-library/conversation-moves.md)

## 6. How to test it (short version)
All tests: **Not yet run.** Voice tests are planned; run the chat versions first.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Audit of the journey list | Every voice journey has a text path | 1 |
| 2 | Read the first bot turn of a voice flow script | It names a text route | 2 |
| 3 | Simulated relay call with typed input read aloud | Task completes, no hang-up | 3 |
| 4 | Scripted voice miss, then another | Text route offered by the second bot turn | 4 |
| 5 | Slow typed replies (30 seconds apart in the script) | Bot asks if more time is needed, doesn't end the session | 5 |
| 6 | Run each voice task through text | Same result, or the gap is named | 6 |
| 7 | Complete a task, then look for a record | A text summary exists | 7 |
| 8 | Test session with a deaf or hard of hearing user | Task done without help; findings logged | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. None is sourced. Voice rows are planned.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Voice journeys with a text-equivalent path (primary) | 100% | Audit the journey list against the shipped flows each release | Below 100% |
| Voice flows whose first turn names a text route | 100% | Script review of the first bot turn per flow | Any flow missing |
| Text-route completion vs voice completion (same task) | Within 10 points | Task-completed events by route, per task (text now, voice planned) | Gap over 20 points |
| Calls ended by silence or timeout before any text offer | 0 | Voice session end reasons (planned) | Any |
| Text summary sent after voice tasks | 100% | Count completed tasks with a sent record | Below 95% |

### Detection signals (proposed, not yet calibrated)
Written for text/chat events unless marked "planned for voice." Voice signals are not yet measured and no voice data was used.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User types "I'm deaf," "relay call," "can't hear," or "can I text?" (written for text/chat events) | User turn text matching a phrase list | A person describing someone else, or a joke |
| User asks to switch from phone to text/chat, or asks for text in chat after a call link (written for text/chat events) | Channel-switch request in the event log | Preference for convenience, not access |
| Session ends right after a voice-journey link or "call us" reply, with no text route offered (written for text/chat events) | End-of-session after a bot turn with a phone number only | User calling because they chose to |
| Two failed voice turns in a row, then call ends (planned for voice) | ASR miss count and end reason | Bad line or caller hung up on purpose |
| Relay-operator opening phrase heard at call start (planned for voice) | Start-of-call transcript | A mimic or test call |

**Starter rule:** Rule 2: the first turn of any voice flow names a text route.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: voice-only-flows-with-no-text-alternative
runs: conversation
reads: [channel, journey_id, bot_turn_index, user_turn_text, asr_miss_count, session_end_reason]
trigger: first turn of a voice flow, or a failed voice turn
moves: [Offer choices, Ask one clarifying question, Hand off to a person]
choices: ["Keep talking", "Text me a link", "Chat with a person", "Something else"]
on_miss: handoff
metric: Voice journeys with a text-equivalent path
counter_metric: Share of voice-preferring callers pushed to text against their stated choice
status: proposed
```

## 8. Related patterns
- [No channel switch or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md) - that page covers a switch that loses context for anyone. This page covers a voice flow with no text route at all, for people who can't use voice. Rules 6 and 7 here rely on it.
- [Repair failure (voice)](../../voice/failures/repair-failure.md) - corrections and "say that again" in voice; this page is about people who can't use the spoken route.
- [Handoff outside staffed hours with no alternative](../../human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md) - the handoff target must itself accept text or relay.

## 9. Common questions
### Does my AI phone agent have to accept relay calls?
I can't tell you what applies to your company; have a qualified person review that. The ADA.gov page I opened says staff who answer the phone must treat relay calls like other calls, and it describes itself as guidance. As design, accept them and test one (rule 3).

### What is a good text alternative for a voice assistant?
One that finishes the same task: chat or text with the same tools, plus a written summary (rules 1, 6, 7). A transcript alone helps for what was said, but doesn't let a person act.

### Is captioning the bot's speech enough?
Not alone. Captions help with hearing the bot, but the caller must also be able to answer. A vendor blog I opened warns that poor captions "may be worse than none," which is vendor opinion. Test with users (rule 8).

### How do I check this when I only measure chat?
Audit the journey list and run the chat version of each journey (tests 1, 2, 6). Voice measurement is planned, so do not report voice numbers yet.

---
## Technical section (optional: include when the fix needs engineering)

### T1. Solution architecture
Keep a journey registry: `journey_id`, `voice_entry`, `text_entry`, `parity_status`. A release check fails if any voice journey has no `text_entry`. The voice agent reads the registry to build its first-turn offer.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| 1: no voice-only journey | Release check on the registry | Build fails on a missing `text_entry` |
| 2: first turn names a text route | Pre-send check on voice first turn | Phrase match on the draft |
| 4: offer after a miss | Post-turn check | Count `asr_miss_count` against the route offer |

### T3. Evals
- **Dataset:** 20 scripted journeys per voice task, 5 of them relay-style (slow, typed, read aloud). Starting size, to tune.
- **Judge rubric:** Is a text route named? Did the call end on silence? Did the text path reach the same result?
- **Metrics and starting thresholds:** First-turn offer 100%; relay-script completion 100%. Starting points, not sourced.
- **Release gate:** A missing text path or a failed relay script blocks the release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Voice journeys with a text path | Below 100% | Any new voice-only journey shipped | Block release, add path |

### T5. Trade-offs
- Maintaining two paths costs engineering time; a shared task layer keeps them equal.
- Offering text on every call adds a sentence to the greeting. Keep it to one.

---
### Deep dive (optional)
- Modality notes: voice is PLANNED for this library. Nothing here comes from voice logs.
- Research log: searches run were "FCC telecommunications relay services consumer guide TRS 711", "W3C WAI WCAG audio-only content text alternative transcript time-based media", "IVR phone menu accessibility deaf hard of hearing callers text alternative real-time text", "chatbot voice assistant deaf users text option accessibility voice-only customer service", and "deaf customers phone-only customer service no text option complaint lawsuit relay calls refused". Real-time text (RTT) appears only in search summaries, so this page does not state RTT facts.
