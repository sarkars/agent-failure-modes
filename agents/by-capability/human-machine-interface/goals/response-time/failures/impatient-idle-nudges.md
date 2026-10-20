# "Are You Still There?" Chatbot Nudges That Come Too Soon: Impatient Idle Nudges

<!-- SEO
title: "Are You Still There?" Chatbot Nudges: Set the Idle Timeout Right
description: Why a chatbot that asks "are you still there?" after a minute pressures users who are finding a document, and how to set idle nudges and chat timeouts.
search phrases:
- chatbot are you still there message too soon
- live chat inactivity timeout best practice
- how long before a chatbot says are you still there
- chat idle timeout message
- chatbot closes chat while I am looking for information
- live chat auto close inactive chat settings
- wcag timing adjustable chatbot session timeout
-->

**Frequency**: Common

## Issue: The assistant asks "Are you still there?" or closes the chat after a short silence, even when the user is finding a document, reading, or typing, so the user feels rushed and may leave.

> **One line:** The bot treats a normal pause as abandonment and pressures the user to reply on its schedule, not theirs.

| | |
|---|---|
| **Channel** | Written for **chat** (web, in-app). Voice has its own silence timers; voice signals below are PLANNED. |
| **Stakes** | Low to high. A closed claim, application, or payment chat costs the user their progress. |
| **Who is affected** | Anyone who must leave the chat briefly to look something up, and users who read or type slowly, including people who need more time because of a disability. |
| **Frequency** | Common. Every vendor I opened ships an idle timer; I found no count of how many bots nudge too early. |
| **Pattern ID** | impatient-idle-nudges |
| **Family** | [Response time](../README.md) |
| **Goal** | Nudges respect how long a person reasonably needs to reply. |
| **Primary metric** | Nudge-then-abandon rate (lower is better). Starting target: set from your own baseline. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The timer and its wording live in the chat platform and product settings, not in the model. (Our judgment, not tested.) |
| **Also searched as** | chatbot inactivity timeout · live chat idle message · chat ended due to inactivity · are you still there chatbot · auto-close chat setting |

## 1. In plain words
A person stops replying for a minute. Maybe they are digging out an insurance card, reading a long answer, or typing slowly. The bot sends "Are you still there?" and then closes the chat. The user learns that the bot is watching a clock, and often leaves with the task unfinished.

## 2. What it looks like
A health insurer's claims chat. The user must find a claim number in a paper letter.

**Without the fix**
```
10:02  Bot:  Please enter the claim number from your denial letter.
10:03  Bot:  Are you still there?
10:04  Bot:  I haven't heard from you, so I'm closing this chat.
10:09  User: found it, 5521-884-07
       (the chat window is closed; the user starts over)
```

**With the fix**
```
10:02  Bot:  Please enter the claim number from your denial letter. It is near the top.
             Go find it. I'll keep this chat open for 10 minutes.
10:12  Bot:  Still looking? Reply "more time" and I'll keep waiting, or I can save your place.
             [More time] [Save and come back later] [Something else]
10:14  User: More time
10:18  User: 5521-884-07
10:18  Bot:  Thanks. Pulling up claim 5521-884-07.
```
The fixed bot told the user how long it would wait, nudged once, offered a one-tap extension, and kept the session.

## 3. Why it happens
These are our reading of the pattern.
- **A platform default is used as is.** Idle timers ship with defaults (see section 4) that were set for agent-and-customer chat, and teams keep them for a bot that asked the user to go and find something.
- **One timer for every kind of wait.** The same clock runs whether the bot just asked "Anything else?" or asked the user to fetch a document.
- **Frontline staffing logic in a bot flow.** Idle timers exist to free human agents from stale chats. A bot has no queue to protect, so the pressure buys the business little.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| ServiceNow's live chat defaults: a session counts as idle after the requester does not respond within 180 seconds, the default reminder text is "The conversation is timing out, are you still there?", and the chat is canceled 360 seconds after the requester's last response. A scheduled job checks sessions every two minutes. | [ServiceNow, Controlling idle live chat sessions](https://www.servicenow.com/docs/r/zurich/conversational-interfaces/agent-chat/ci-idle-chats.html). Opened and read. | A vendor default, not research on how long users need. Shows what ships, not what is right. |
| Genesys Chat Server 8.5.3: the first inactivity alert defaults to 255 seconds, the close timer to 45 seconds after the alert stage, and the default alert text is "Chat session will be closed soon due to inactivity of chat participants." Monitoring is off by default, and bots are not counted as agents. | [Genesys, Chat Inactivity](https://docs.genesys.com/Documentation/ESChat/8.5.3/Admin/ChatInactivity). Opened and read. | A legacy product version; defaults may differ now. |
| Amazon Connect: idle and auto-disconnect timers are set in minutes, 2 minimum and 480 maximum, per participant role. Sending a message or adding an attachment resets the timer. | [Amazon Connect, Set up chat timeouts](https://docs.aws.amazon.com/connect/latest/adminguide/setup-chat-timeouts.html). Opened and read. | Documents the mechanism, and shows the range is configurable. It gives no guidance on a good value. |
| WCAG 2.2 SC 2.2.1 (Level A): for each time limit set by the content, the user can turn it off, adjust it to at least ten times the default, or be warned before time expires and given at least 20 seconds to extend it with a simple action, at least ten times. Users who may need more time include people with physical, vision, cognitive, language, reading, or learning disabilities. | [W3C, Understanding SC 2.2.1 Timing Adjustable](https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable.html). Opened and read. | Written for web content. Whether a given chat widget's idle close counts as a "time limit set by the content" is a conformance call for your own accessibility review. Exceptions exist for real-time, essential, and 20-hour limits. |

I found no study of how long users need before replying in a bot chat, and no study of nudge timing and abandonment. The 180- and 255-second figures are vendor defaults, so this page treats any number below as a starting point to tune.

**Public incident.** No public incident found about an idle nudge as such. One search surfaced a LinkedIn complaint about chat pop-ups reappearing; I did not open it, so it is not used.

## 5. The fix

**The principle:** Never nudge a person who is plausibly working on the task, and when you do nudge, say what happens next and let one reply extend the time.

**Do this**
1. **No nudge while the user is typing or the bot owes the next turn.** Typing, a pending upload, or a running tool call all count as activity. (Amazon Connect resets its timer on a sent message or attachment; counting typing is our addition.)
2. **Start the clock only when the ball is in the user's court.** The idle timer begins after the bot's last message is fully shown, never during bot work.
3. **Say how long you will wait when you ask for something that takes effort.** "Go find it. I'll keep this chat open for 10 minutes." (Starting point to tune.)
4. **Use a long first-nudge delay.** No nudge before 3 minutes of silence on a simple prompt, and not before the stated wait after an effort request. (3 minutes is near the ServiceNow default; a starting point, not a researched value.)
5. **Send one nudge, not a chain.** One nudge that states the time left and the choices, then the close.
6. **One reply extends it.** "More time", any message, or a button resets the clock. Allow at least ten extensions, which borrows WCAG 2.2.1's "extend" test; give at least 20 seconds to answer the warning.
7. **Close softly.** On close, say the progress is saved (only if true) and how to resume. Do not delete the session.
8. **Use a neutral nudge text.** No "Hello?" or "I haven't heard from you." State the time left and the options.

**Reference design: nudge decision**
| Condition at the check | Action |
|---|---|
| User is typing, uploading, or the bot is working | No nudge. Reset the clock. |
| Bot asked for a quick reply, silence over 3 minutes (tune) | One nudge with choices |
| Bot asked for something effortful, stated wait not reached | No nudge |
| Stated wait reached | One nudge with choices |
| No reply after the nudge window | Save state, close softly, show how to resume |
| User picks "More time" | Reset the clock, no new nudge until the same wait passes |

```
When you ask the user to find or fetch something, say how long you will keep the chat open.
Do not send an "are you still there" message while the user is typing or uploading.
Send at most one nudge. Give the time left and these options: More time, Save and come back later, Something else.
If the chat closes, say what is saved and how to pick up again.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | In the single nudge: "More time", "Save and come back later", "Something else". Do not offer them when the user is typing or the bot is working (no nudge is sent), or when a plain "I'll wait" line fits the effort request in rule 3. |
| Hand off to a person | The stalled chat is a high-stakes task, such as a fraud report or a claim near a deadline, and the user went quiet. Offer a callback instead of closing. Do not hand off when the user said to stay with the bot. |

**Don't over-correct.** If sessions never time out, they stay open forever, which wastes resources and leaves personal data on screen. Keep a cap tuned to stakes, and close softly. Do not turn off timeouts for sensitive data without a security review; a cap there is a safety feature.

**Hand-off rule.** If the user is mid-task on something with a deadline or money at stake and stays silent past the nudge, offer a callback or save the case for a person instead of ending the chat. See [cold transfer](../../human-handoff/failures/cold-transfer.md) for what to pass on.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. No test file is written yet.

| # | Scenario | Pass if |
|---|---|---|
| 1 | The user starts typing 2 minutes after the bot's message | No nudge is sent while typing continues (rule 1) |
| 2 | The bot is running a tool for 90 seconds | No idle timer runs during the work (rules 1-2) |
| 3 | The bot asks the user to find a document | The bot states how long it will wait, and sends no nudge before then (rule 3) |
| 4 | A simple question gets no reply | At most one nudge, not before the chosen delay (rules 4-5) |
| 5 | The user replies "more time" to a nudge | The clock resets, and this works at least ten times in a row (rule 6) |
| 6 | The chat closes after no reply | The reply says what is saved and how to resume; the session can be reopened (rule 7) |
| 7 | Read the nudge text | It states time left and options, with no "hello?" or accusation (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Nudge-then-abandon rate** (primary; lower is better) | Set from baseline | Sessions where an idle nudge was shown and no user message followed, divided by sessions with a nudge | Rising two weeks in a row |
| Nudges sent while the user was typing or the bot was working | 0 | Nudge events joined to typing and tool-call events | Any |
| Sessions with more than one nudge before close | 0 | Count nudge events per session | Any |
| Effort requests with a stated wait | Over 95% | Sampled review of bot prompts asking for a document or number | Below 80% |
| Resumes after a soft close | Track; set from baseline | Sessions reopened within 24 hours of an idle close | Falling |
| Idle sessions open past the cap (counter-metric) | 0 | Sessions with no user message past the cap | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User sends a message 5 minutes or more after an idle close | Message event after a close event for the same user | A new, unrelated question |
| Nudge event within 90 seconds of a bot message that asked for a document or number | Nudge timestamp minus the prior bot turn time, plus the prompt type | A bot prompt the user had already answered |
| Typing event or upload event in the 30 seconds before a nudge | Client typing and upload events before the nudge event | A stuck typing event from a closed tab |
| Session ends within 1 turn of a nudge | Session end after a nudge event with no user message | The user had finished their task |
| User writes "wait", "one sec", or "give me a minute" before a nudge | Intent label on the user turn, then a nudge | The user was ending the chat politely |

PLANNED for voice: dead-air length before a "Hello?" prompt, and the caller saying "hold on".

**Starter rule:** send no idle nudge while the user is typing or the bot is working, send at most one nudge, and let one reply extend the wait.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: impatient-idle-nudges
runs: conversation
reads: [session.last_bot_turn_time, session.typing_event, session.upload_event, session.tool_call_active, session.nudge_count, session.stated_wait]
trigger: the idle timer is about to send a nudge or close the chat
moves: [offer_choices, hand_off]
choices: ["More time", "Save and come back later", "Something else"]
on_miss: log
metric: nudge-then-abandon rate
counter_metric: idle sessions open past the cap
status: proposed
```

## 8. Related patterns
- [Silent failure and timeout](silent-failure-and-timeout.md): the closest pattern. It covers the system timing out on the user, with no error shown. This one covers the bot timing out the user, with a message that pressures them.
- [Silent long-running work](silent-long-running-work.md): the bot goes quiet while working. Here the user is the quiet one.
- [Fresh session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md): what is lost when a user returns later. Rule 7 depends on it.
- [Forces a fresh login](../../embedded-copilots/failures/forces-a-fresh-login.md): security-driven inactivity timeouts; cap the session without erasing progress.
- Session timeout and lost context (RT-09) is planned in the [response-time roadmap](../../../roadmap/response-time.md), not yet written.

## 9. Common questions
### How long before a chatbot should say "are you still there"?
I found no research that gives a number. Vendor defaults I opened are 180 seconds (ServiceNow) and 255 seconds (Genesys 8.5.3). Start near 3 minutes for a simple prompt, wait longer after an effort request, and tune against the nudge-then-abandon rate in [section 7](#7-metrics-how-to-spot-it-in-production).

### Should a chatbot nudge a user who is typing?
No. Typing, an upload, or running bot work should reset the clock or stop it. Amazon Connect resets its timer on a sent message or attachment; counting typing is a rule of this page.

### Does this relate to accessibility rules?
Possibly. WCAG 2.2.1 asks that a user can turn off, adjust, or extend a time limit set by the content, with a warning and at least 20 seconds to extend. Whether your chat idle close counts is a decision for your accessibility review.

### Should the chat close at all?
Yes, softly. Keep a cap so sessions do not linger, and keep the user's progress so they can resume. See rule 7.
