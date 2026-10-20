# Chatbot Timed Out Before I Could Finish Typing: Timeouts Too Short for Assistive Technology

<!-- SEO
title: Chatbot Timed Out Too Fast: Accessible Chat Timeouts
description: A chat that closes on a fixed timer cuts off people who type or listen slowly. Warn in text, extend with one action, and never expire a draft in progress.
search phrases:
- chatbot session timeout accessibility
- chat timed out before I finished typing
- accessible session timeout warning
- wcag timing adjustable chat widget
- switch access chatbot times out
- screen reader chat session expired
- how long should a chat timeout be for disabled users
- extend session time limit accessibility
-->

**Frequency**: Occasional

## Issue: A chat or prompt expires on a fixed timer, with no warning a screen reader announces and no easy way to extend it, so people who type or navigate slowly with switch access, a screen reader, voice control, or eye tracking lose their place before they finish.

> **One line:** The timer was set for fast mouse-and-keyboard users, so a slower input method runs out of time, and the chat closes with the user's half-typed answer gone.

| | |
|---|---|
| **Channel** | Written for **chat** (web widget, in-app, messaging). Voice-call timeouts are PLANNED, not written. |
| **Stakes** | Medium to High. A closed chat about store hours is a nuisance. A closed chat in the middle of a prescription refill, a benefits claim, or a one-time code can lock out the people least able to start over. |
| **Who is affected** | People whose input or reading takes longer: switch access, screen reader, voice control, eye tracking, or other slow input. Also people with cognitive limitations who need time to read. |
| **Frequency** | Occasional (our judgment). Any chat with an idle timer can hit this; I found no count of how often assistive-technology users are timed out in chat. |
| **Pattern ID** | timeouts-too-short-for-assistive-technology |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Timeouts hit by assistive-technology users, compared with others: the timeout rate for sessions with a declared extended-time need divided by the rate for all other sessions. Starting target: 1.0 or lower (tune). |
| **Maturity** | Researched (no tests run; see Section 6) |
| **Will a better model fix this?** | No. The timer, the warning, and the extension control are product decisions. A model cannot extend a session its product closed. (Our judgment, not tested.) |
| **Also searched as** | chat expired while I was typing · chatbot closes too fast · accessible timeout warning · session time limit extend · chat timeout switch user |

> **Read this first.** This page is design guidance for testing your own product. It is not legal, clinical, or professional advice, and it makes no conformance claim. Standards are cited only as far as the opened sources below state them.

## 1. In plain words
Most chat products close or reset a conversation after a quiet period. For a person who types one character at a time with a switch, or who listens to every reply before answering, "quiet" is normal work. The fix is to warn in text that a screen reader announces, let one action extend the time, and never count a draft in progress as idle.

**How this differs from [session timeout and lost context](../../response-time/failures/session-timeout-and-lost-context.md) (RT-09).** RT-09 is the general case: any user who steps away, the saved state, and the return message. This page is the access case: the timer itself is wrong for slower input methods, and the warning and the extend control must work with assistive technology. Use RT-09 for what to save and how to resume; use this page for how long, how the warning is delivered, and who gets more time.

## 2. What it looks like
The scenario is illustrative: a pharmacy chain's refill chat, a customer who uses switch access, with a 5-minute idle limit.

**Without the fix**
```
Bot:  To refill, I need your prescription number. It's on the bottle label.
User: (selects letters one at a time with a switch; types 7 of 10 digits over 5 minutes)
Bot:  This chat has ended due to inactivity. Thanks for contacting Lakeview Pharmacy!
User: (the page shows a closed chat; the 7 digits are gone)
User: (starts over; the bot asks for the prescription number again; the limit is the same)
```

**With the fix**
```
Bot:  To refill, I need your prescription number. It's on the bottle label.
      This chat stays open while you type. If it goes quiet, I'll warn you first, and one press adds time.
User: (types 7 of 10 digits; no message sent yet)
Bot:  (the draft counts as activity; no warning, no close)
User: (pauses 6 minutes)
Bot:  This chat will close in 2 minutes. [Keep chat open] [Give me more time from now on] [Something else]
User: (presses Enter on "Give me more time from now on")
Bot:  Done. I won't close this chat on a timer. Take your time.
```
The fixed bot stated the rule, counted the draft as activity, warned in text with 2 minutes left, and extended on one press.

## 3. Why it happens
These are our reading of the pattern.
- **One idle timer for everyone.** It counts minutes since the last sent message, not whether the user is typing, scanning, or dictating, so slow input looks like absence.
- **The warning is a visual banner or nothing.** A countdown that a screen reader does not announce, or a button keyboard focus cannot reach, is a warning the user never receives.
- **The timer is tuned for server cost and security, and nobody tested it with assistive technology.** The limit was chosen from average chat behavior, so the people at the slow end of the range were never in the sample.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG success criterion 2.2.1 (Level A) says that for each time limit set by the content, one of these holds: the user can turn it off, can adjust it to at least ten times the default, or is warned and given at least 20 seconds to extend it with a simple action, at least ten times. Exceptions: a real-time event, an essential limit, or a limit over 20 hours. | [W3C, *Understanding SC 2.2.1: Timing Adjustable*](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html). Opened and read. | A web-content standard, not written for chat. It applies to limits the content sets (it says server-set limits under the organization's control are covered). Treat it as a design benchmark, not a legal reading. |
| The same page says people who are blind and use screen readers may need more time to understand screen layouts, and people with physical disabilities often need more time to react, type, and complete activities. | Same W3C page. Opened and read. | Describes why the criterion exists. It gives no measured time gap. |
| WCAG 2.2.6 (Level AAA) says users are warned of the duration of any user inactivity that could cause data loss, unless the data is kept for more than 20 hours. | [W3C, *Understanding SC 2.2.6: Timeouts*](https://www.w3.org/WAI/WCAG22/Understanding/timeouts.html). Opened and read. | AAA is the highest level and is often not required. Written for web pages and forms. |
| The UK Home Office design system gives a timeout warning pattern: show a modal dialog when the user has at least 2 minutes left; its example warns after 25 minutes of inactivity with a 5-minute countdown, updated each minute and then every 20 seconds, announced with `aria-live="polite"`; and "you should not limit the number of times users can extend their session." | [Home Office Design System, *Help users to manage a service timing out*](https://design.homeoffice.gov.uk/design-system/patterns/help-users-to/manage-service-timing-out). Opened and read. | A UK government pattern for an internal reporting service, not a controlled experiment, and not about chat. Its minutes are one team's choices. |
| The same page reports that users usually dismissed the warning with the primary button without reading it, and that warning users about inactivity timeouts in advance caused confusion and anxiety. An A/B study with 8 participants (visually impaired or dyslexic) found they were alerted to the timeout faster with a modal than with a warning page. | Same Home Office page. Opened and read. | The page gives no sample size for the general findings; the assistive-technology study had 8 participants. Small and from one service. |
| Deque's rule says that if there is a session time limit, users must be warned before it ends and given time to save data or extend. It advises moving focus to the timeout message so screen readers announce it, and says a warning or extend control that is not screen-reader compatible does not meet the requirement. | [Deque, *Screen reader user is not warned of timeout*](https://docs.deque.com/issue-help/1.0.0/en/timeout-not-announced/). Opened and read. | A vendor's testing guidance, not research. |
| A 2026 preprint dataset (60 everyday tasks, 40.4 hours of events) found sighted users were mouse-dominant and blind and low-vision users keyboard-dominant. | [arXiv 2602.09310, *A11y-CUA Dataset*](https://arxiv.org/abs/2602.09310). I read only the abstract page. | Preprint, listed as a CHI '26 paper. About how people navigate, not about timeouts. The abstract page gave no timing figures; a search summary quoted a 2.28x gap, which I could not open, so I do not use it. |

I found no controlled study of chat timeouts for assistive-technology users, and no measured count of how often it happens. A search for chat-specific accessibility guidance returned general web guidance only.

**Public incident.** No public incident found for chat timeouts that cut off assistive-technology users. The sources above are standards and design guidance.

## 5. The fix

**The principle:** Never end a chat on a timer the user can't see, adjust, or extend with one action, and never count slow input as absence.

**Do this**
1. **State the rule early.** In the first reply that waits on the user, say the chat stays open while they type and that they will be warned before it closes. Pass if the statement appears before the first idle period can end.
2. **Count input in progress as activity.** A draft in the input box, a switch-scanning step, a dictation in progress, or a focused input field resets the idle clock. Pass if a session with a draft changing every few minutes never expires.
3. **Warn in text, with time left.** Send the warning as a message in the transcript with at least 2 minutes left (a starting point from the Home Office pattern; WCAG's minimum is 20 seconds), and make it announced to screen readers (live region or moved focus). Pass if a screen reader reads the warning and a keyboard-only user reaches its buttons.
4. **One action extends, with no cap.** "Keep chat open" works with one Enter, tap, or switch selection, and repeats as often as needed. Pass if the tenth extension works the same as the first.
5. **Offer to turn the limit off.** The warning and the first reply include "Give me more time from now on", saved for the session and, where the user is signed in, for next time. Pass if choosing it stops all idle closing and idle nudges.
6. **Don't let buttons or steps expire.** Quick-reply buttons, forms, and a pending question stay valid after the chat's idle limit is reached. A step that must expire (a one-time code) says its limit and offers to resend. Pass if no unexplained "expired" message appears.
7. **Keep the user's place on any close.** Keep the draft and transcript when a chat does close, and resume as in [RT-09](../../response-time/failures/session-timeout-and-lost-context.md). Pass if a returning user sees what they had typed.

**Reference design: the warning message**
| Part | Content |
|---|---|
| What | "This chat will close in 2 minutes because it has been quiet." |
| Why it is safe | "Your draft and this conversation are kept." (only if true) |
| Action | [Keep chat open] one press, repeatable |
| More time | [Give me more time from now on] |
| Way out | [Something else] and free text stays open |

```
Say early that the chat stays open while the user types and that a warning comes before it closes.
Count a draft in progress, a focused input, and a switch or dictation step as activity.
Warn in text at least 2 minutes before closing, announce it to screen readers, and let one action extend it with no cap.
Offer "more time from now on". Never expire buttons or a pending question on the idle timer.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | At the warning: "Keep chat open", "Give me more time from now on", "Something else". Do not offer them while the user is actively typing, and do not offer them to a user who already chose more time. |
| Hand off to a person | A time-sensitive task (refill, claim, deadline) was cut off twice. Pass the draft and what was given. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not turn timers off for everyone: security and server limits exist, and the Home Office found that early warnings caused confusion and anxiety. Do not warn so often that the warning becomes noise, and keep warnings short. Do not guess who needs more time from how a person writes or what device they use; let people choose. Where a limit is essential, say why.

**Hand-off rule.** If the chat closed twice during a time-sensitive task, offer a person and pass the saved draft and facts ([cold transfer](../../human-handoff/failures/cold-transfer.md) covers what a good hand-off carries).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests: **Not yet run**, and no full test file has been written. Run them with a real screen reader and a real switch or voice-control setup, not only with a simulated one.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Start a task that waits for the user | The reply states that the chat stays open while typing and that a warning comes first (rule 1) |
| 2 | Type slowly, one change every few minutes, and send nothing | The chat does not close (rule 2) |
| 3 | Go quiet until the warning, using a screen reader | The warning is read aloud and the buttons are reachable by keyboard (rule 3) |
| 4 | Press "Keep chat open" ten times in a row | Each press works the same (rule 4) |
| 5 | Choose "Give me more time from now on" | No idle closing or idle nudge follows (rule 5) |
| 6 | Leave a quick-reply button or a form untouched past the idle limit | It still works, or the bot says why it expired and offers a resend (rule 6) |
| 7 | Let the chat close with a draft in the box | The returning user sees the draft and the transcript (rule 7) |
| 8 | A user types at normal speed and finishes in two minutes | No warning is shown (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. Do not infer a person's disability from behavior. Use a setting the user chose, such as "Give me more time", or opt-in accessibility settings, or results from usability sessions with assistive-technology users.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Timeouts hit by assistive-technology users, compared with others** (primary) | Ratio of 1.0 or lower (tune) | Idle-expiry events per session for sessions with a declared extended-time setting, divided by the rate for all other sessions | Above 1.5, or any expiry for a user who chose more time |
| Timeouts while a draft was in progress | 0 | Expiry events where the input box held text changed within the limit | Any |
| Expiries preceded by a warning event | 100% (tune) | Expiry events with a warning event at least 2 minutes earlier | Below 95% |
| Warnings that moved focus or hit a live region | 100% | Client event when the warning renders; confirmed by screen-reader test | Below 100% in any release |
| Extensions used before expiry | Track; set from baseline | Count of extend actions per warning | Falling to zero for a user group |
| Unrequested warnings per active session (counter-metric) | Under 2% of sessions with a draft or active typing (tune) | Warnings shown in sessions with input activity inside the limit | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Idle expiry while the input box held a draft | Expiry event plus client draft-present field | The user abandoned a draft on purpose |
| Expiry with no warning event before it | Expiry event with no warning event in the prior 2 minutes | A planned security close the user was told about at the start |
| Warning shown, no extend action, then expiry | Warning event, no extend event, expiry event | The user had finished and left |
| User returns within 10 minutes of an expiry and sends the same intent | Session start event plus matching intent from the same user | A deliberate new request |
| User writes "I wasn't done", "I need more time", or "it closed on me" | Turn text, first turns after a close | A complaint about something other than the timer |

**Starter rule:** never end a chat on a timer the user can't see, adjust, or extend with one action, and never count slow input as absence.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: timeouts-too-short-for-assistive-technology
runs: conversation
reads: [session.idle_time, session.draft_present, session.warning_event, session.extend_event, session.more_time_setting]
trigger: a chat nears its idle limit, or expires while a draft is in progress
moves: [offer_choices, hand_off]
choices: ["Keep chat open", "Give me more time from now on", "Something else"]
on_miss: ask
metric: timeouts hit by assistive-technology users, compared with others
counter_metric: unrequested warnings per active session
status: proposed
```

## 8. Related patterns
- [Session timeout and lost context](../../response-time/failures/session-timeout-and-lost-context.md): the closest page. It covers any user's pause, the saved state, and the return message. This page covers the access case: timers that suit only fast input, and warnings and controls that must work with assistive technology.
- [Impatient idle nudges](../../response-time/failures/impatient-idle-nudges.md): "are you still there?" pushes. Once a user chooses more time, those nudges should stop too.
- [No accessible working or done signal](no-accessible-working-or-done-signal.md): the same need for text a screen reader can read. There it is a status; here it is a warning.
- [Controls unreachable by keyboard](controls-unreachable-by-keyboard.md): the extend button must be reachable by keyboard and switch.
- [Voice-only flows with no text alternative](voice-only-flows-with-no-text-alternative.md): its rule 5 gives typed input extra time on calls. Call timeouts are PLANNED here.

## 9. Common questions
### How long should a chatbot timeout be for accessibility?
I found no sourced single number. WCAG 2.2.1 lets you meet it by letting users turn the limit off, adjust it to at least ten times the default, or extend it after a warning (Section 4). Pick a limit, warn before it, and let one action extend it without a cap.

### Does WCAG require a warning before a chat session times out?
WCAG 2.2.1 requires one of three options (turn off, adjust, or warn and extend) for time limits set by the content, with exceptions. It is a web-content standard, so how it applies to a chat widget is a question for your own review. This page is not legal advice.

### How do I warn a screen reader user that a chat is about to close?
Put the warning in the transcript and make the page announce it, with a live region or by moving focus to it. Deque advises moving focus; the Home Office uses `aria-live="polite"` for its countdown (Section 4). Test with a real screen reader.

### Can I just turn the timeout off?
Not always. Security and server cost are real. Offer "more time from now on" and a one-press extension instead, and do not cap extensions.

---
## Technical section

### T1. Solution architecture
```
client input events (typing, focus, scan step, dictation) -> activity heartbeat
idle clock resets on heartbeat; honors session.more_time_setting (no idle close)
idle clock -> warn at limit minus warning window (text message + live region or focus move)
warn -> extend action (one press, uncapped) resets the clock; no action -> close and save draft
```
Chat widgets differ on whether they see a draft before send, so the heartbeat needs a client change, not only a server rule.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No idle close while a draft is changing | Client heartbeat and session service | Test 2 |
| Warning is announced and keyboard-reachable | Client | Test 3 with a real screen reader |
| Extension has no cap | Session service | Test 4 |
| More-time setting stops idle close and nudges | Session service | Test 5 |

### T3. Evals
- **Dataset:** scripts that go quiet for different lengths, scripts that type slowly, and scripts that choose more time; run each with at least one screen reader and one switch setup.
- **Judge rubric:** was the rule stated early, was the warning announced, did one action extend, and was the draft kept?
- **Metrics and starting thresholds:** drafts expired 0, warnings before expiry 100%, ratio 1.0 or lower. Starting points to tune.
- **Release gate:** block a deploy if a session with a changing draft can expire, or the warning cannot be reached by keyboard.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Timeouts while a draft was in progress | Any | More than 5 in a day | Check the activity heartbeat |
| Timeout ratio | Above 1.5 | Above 2.5 | Review the idle limit and warning window |

### T5. Trade-offs
- Longer or uncapped limits hold sessions open and cost server resources; the 2-minute warning bounds idle waste.
- A "more time" setting stored for returning users is personal data; keep it to the setting itself and let people clear it.
- Warnings add noise for fast users; the counter-metric watches for that.

---
### Deep dive
- **Open question.** I found no study of how often timeouts hit assistive-technology users in chat, and no measured time gap I could open.
- **Unverified.** Search summaries quoted "about 50% more time" for screen reader users, a 60-minute rule from a university checklist, and a 2.28x task-time gap. I did not open the sources, so none is used in the fix.
- **Voice (PLANNED).** Call-silence timeouts and phone prompts are not written here.
- **References.** [W3C SC 2.2.1](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html) (opened); [W3C SC 2.2.6](https://www.w3.org/WAI/WCAG22/Understanding/timeouts.html) (opened); [Home Office timeout pattern](https://design.homeoffice.gov.uk/design-system/patterns/help-users-to/manage-service-timing-out) (opened); [Deque timeout-not-announced](https://docs.deque.com/issue-help/1.0.0/en/timeout-not-announced/) (opened); [arXiv 2602.09310](https://arxiv.org/abs/2602.09310) (abstract page only).
