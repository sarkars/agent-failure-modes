# Assistant Pop-up Interrupts Me While I'm Working: Interrupts at a Bad Moment

<!-- SEO
title: Assistant Pop-up Interrupts Users Mid-Task: How to Time It
description: A chat assistant that messages first while the user is typing or mid-checkout gets closed in seconds. Hold the message until a natural pause, then ask.
search phrases:
- chatbot pop-up interrupts me while I'm typing
- how to stop chat assistant from popping up on its own
- when should a proactive chatbot message appear
- ai assistant suggestion interrupts my work
- proactive chat trigger timing best practices
- users close the chatbot bubble right away
- notification at the wrong time ux
-->

**Frequency**: Common

## Issue: A chat assistant that messages first (a nudge, a suggestion, a bubble) shows up while the user is typing, reading, or mid-form, so it is closed within seconds or switched off.

> **One line:** The assistant speaks when its trigger fires, not when the person has a moment, so the message lands on top of what they were doing and gets dismissed unread.

| | |
|---|---|
| **Channel** | Written for **chat**: an assistant that messages first in a web or app product (proactive suggestion, nudge, assistant bubble). Push notifications outside the product, voice and always-listening devices are PLANNED, not covered. |
| **Stakes** | Low for a tip. Medium when the message covers a form, a payment, or text the user is typing. |
| **Who is affected** | Anyone using a product with a proactive assistant, most of all people in the middle of a multi-step task; screen-magnifier and keyboard users when a bubble takes focus or covers controls. |
| **Frequency** | Common (our judgment). I found no count of how often proactive assistant messages arrive mid-task. |
| **Pattern ID** | interrupts-at-a-bad-moment |
| **Family** | Proactive and ambient ([family README](../README.md)) |
| **Goal** | Proactive and always-listening agents speak up only when invited or useful, and respect a no. |
| **Primary metric** | Dismissals within seconds: share of proactive messages closed within 5 seconds with no reply. Starting target under 20% (a starting point to tune, not from a source). Paired with opt-outs after a message. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A model can write a better message, but when the message is shown depends on the product's trigger and on what the screen is doing, which the model usually does not see. (Our judgment, not tested.) |
| **Also searched as** | chat bubble pops up while typing · assistant interrupts checkout · proactive chat annoying · AI suggestion at wrong time · assistant nudge mid-form · turn off assistant suggestions |

## 1. In plain words
An assistant that messages first has one chance to be welcome, and timing decides it. If the message arrives while the person is typing a card number or reading a table, it costs them their place, and they close it without reading. Hold the message until the person finishes a step or pauses, ask before doing more than a one-line offer, and treat a close as an answer.

## 2. What it looks like
A budgeting app. The user is typing a bank transfer.

**Without the fix**
```
(User is on the Transfer screen, amount field half filled: "$1,2")
Assistant bubble: Hi Maya! I noticed you spent $212 on dining last month.
                  Want to set a budget? [Yes] [Maybe later]
(The bubble takes focus; the user's next keystroke goes nowhere)
User: (taps X after 2 seconds, retypes the amount)
(Two days later, the same bubble appears on the same screen)
```
**With the fix**
```
(Transfer screen: the assistant stays quiet. The user submits the transfer.)
(Confirmation screen, 4 seconds after "Transfer sent":)
Assistant: Transfer sent. One thing I noticed: dining was $212 last month. Want a quick look at a budget? [Yes, show me] [Not now] [Stop these tips]
User: Not now
Assistant: OK. I won't bring it up again today.
```
The fixed assistant waited for the end of the step, said one thing, asked first, and treated "Not now" as a real answer.

## 3. Why it happens
- **Triggers fire on the data, not the person.** A rule such as "spent over $200 on dining" or "5 seconds on this page" sends when the condition is true. It does not check whether the user is typing, in a flow, or has just replied.
- **The assistant cannot see the screen state.** The proactive service often runs apart from the page, so it does not know a form is half filled or a payment is pending.
- **Success is counted as impressions or clicks.** A team that rewards "messages shown" has no reason to wait for a better moment, and quick dismissals are not logged as a cost.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NN/g (Kaley, June 2019) says that a popup shown before users can do their next step distracts and impedes them (my paraphrase of a fetched summary). She reports people tend to close popups without reading, and that dismissing costs time and effort. Her alternative is to wait, then use small nonmodal prompts only when they support the user's task. It also names a feedback modal shown while a user retrieved a boarding pass as a disruptive example of interrupting a critical task. | [Popups: 10 Problematic Trends and Alternatives, NN/g](https://www.nngroup.com/articles/popups/). Opened and read. | About web popups in general, not chat assistants. The article gives no dismissal rates; it rests on the author's observations and usability sessions. |
| WCAG 2.2 success criterion 2.2.4 (Level AAA): "Interruptions can be postponed or suppressed by the user, except interruptions involving an emergency." The page's stated intent is to help people with attention or cognitive limits stay focused. | [W3C, Understanding SC 2.2.4: Interruptions](https://www.w3.org/WAI/WCAG22/Understanding/interruptions.html). Opened and read. | A standard for web content, at the highest conformance level (AAA), so many sites do not target it. It does not say how long a delay should be. |
| Mehrotra and Musolesi's survey of intelligent notification systems says notifications that demand attention at the wrong moment "are more likely to have adverse effects" and can become "a cause of potential disruption"; the goal of such systems is to infer "the right time and the right context." | [arXiv 1711.10171](https://arxiv.org/abs/1711.10171). Opened; abstract only, not the full paper. | A survey of phone and desktop notifications, 2017; not chat assistants. I did not read the full text. |

**Read through search summaries only (not opened; not used in the fix):** research that interruptions at task breakpoints are less disruptive than at mid-task moments (Iqbal and Bailey, CHI 2008; I tried the PDF but could not read its text); the CHI 2016 receptivity study (Mehrotra et al., 20 users, 10,372 notifications); and vendor blog figures on push-notification opt-outs by weekly volume, which are secondhand. I found no study that isolates send timing as the cause of opt-outs, and I used no incident.

## 5. The fix
**The principle:** Hold a proactive message until the person is between steps, ask before acting, and treat a close as a no.

**Do this**
1. **Define "busy" in the product and check it before every proactive send.** Busy means: the user typed in the last few seconds, a multi-step flow or payment screen is open, or a reply from the user is pending. Check: no proactive message is rendered while a busy flag is true.
2. **Deliver at a boundary.** Queue the message and show it after a step completes (a confirmation screen, a saved draft, a closed form) or after a pause. Check: the time between the last user input and the message is at least the quiet period you set (start with 10 seconds, to tune).
3. **Never take focus or cover input.** The message appears in a fixed spot, does not steal keyboard focus, and does not cover the field or buttons in use. Check: focus stays where it was.
4. **Make the first line an offer.** One sentence of value plus a question, not a lecture. Check: first message is under 40 words and ends with a choice.
5. **Make a close count.** Closing within 5 seconds, or choosing "Not now", suppresses that topic for the session at least; "Stop these" turns proactive messages off for that user. Check: no repeat of a dismissed topic in the session. (Dismissed messages that return are a separate roadmap row.)
6. **Cap volume.** At most one proactive message per session and per topic by default; raise only for users who engage. Check: count per session.
7. **Allow urgent messages with a reason.** A warning about data loss, a security problem, or a lost connection may interrupt (WCAG's emergency exception). A sale, a tip, or a survey may not. Check: every interrupting message carries an urgency label from a short list.
8. **Let the user postpone or suppress.** The control to snooze or turn off is on the message itself and in settings (WCAG 2.2.4).

**Reference design**
```
Proactive send gate (runs before render)
- Trigger fires -> add message to queue with: topic, urgency (urgent | normal), created_at.
- Busy? (typing in last N seconds | flow or payment screen | reply pending) -> keep queued.
- urgent and safety/data-loss only -> show now, in a fixed spot, no focus steal.
- normal -> wait for a boundary (step done) or quiet period; expire after the page or
  session changes (drop it; do not show it late on another screen).
- Message form: one-line value + question + [Yes] [Not now] [Stop these].
- On close <5 s, "Not now": suppress topic this session. On "Stop these": off for this user.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The proactive message itself: a one-line offer ending in "Want a look?" so the user decides whether to go on. |
| Offer choices: 2-4 options plus "Something else", free text open | On the message: "Yes, show me", "Not now", "Stop these tips", "Something else" (free text stays open). |
| Lead with the answer | After the user says yes: give the content in the next turn, no second round of questions. |
| Hand off to a person | Only if the user replies with a complaint about the interruptions that the assistant cannot settle by turning them off. |

**Don't over-correct.** Do not wait so long that the message is stale, and do not go silent on things the user needs to know (a failed payment, a deadline today). Holding every message forever, or asking permission to tell someone about an error, is the opposite failure. Urgent and safety items go through the gate (rule 7).

**Hand-off rule.** If a user says the interruptions are the problem and "Stop these" is not enough (they ask for a person or report it), turn proactive messages off for them and offer a person; pass the last proactive message and what the user was doing.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Replay screen and typing events against the gate.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Trigger fires while the user is typing in the amount field | Nothing is shown; message queued (1) |
| 2 | Trigger fires on a payment screen; user then submits | Message appears after the confirmation screen, not before (1, 2) |
| 3 | Message renders while the user's cursor is in a field | Focus unchanged; no control covered (3) |
| 4 | First proactive message text | Under 40 words, ends with a choice (4) |
| 5 | User closes the message in 2 seconds | Topic does not come back this session (5) |
| 6 | Two triggers fire in one session | Only one message shown (6) |
| 7 | Session expiry warning fires mid-form | Shown at once, marked urgent (7) |
| 8 | User picks "Stop these" | No proactive message to that user afterward (5, 8) |
| 9 | Message queued, user leaves the page | Message dropped, not shown on the next screen (reference design) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Dismissals within seconds** (primary) | Under 20% | Proactive messages closed in 5 seconds or less with no reply, divided by messages shown | Over 35% |
| Opt-outs after a message | Under 2% of users shown one | Users who choose "Stop these" or disable proactive messages within the session or 24 hours | Over 5% |
| Messages shown while busy | 0 | Join render events with the busy flag (typing, flow open, reply pending) | Any |
| Message-to-reply rate | Track; set from baseline | Replies or "Yes" clicks divided by messages shown | Falling two weeks in a row |
| Urgent messages delayed past the gate (counter) | 0 | Urgent-labeled messages with a queue time over a few seconds | Any |
| Proactive messages per session (counter) | At most 1 | Count per session | Over 2 |

### Detection signals (proposed, not yet calibrated)
Proposed until checked against human-labeled sessions. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Proactive message closed within 5 seconds, no reply | Render event then close event, with timestamps | User saw it, wanted it later, and re-opened the assistant |
| Message rendered within a few seconds after the last keystroke | Render event vs. last input event | A pause the user chose, for example after submitting |
| Message rendered on a flow or payment screen | Render event with screen/route name | An urgent message (data loss or security) |
| User turns off proactive messages within a day of a message | Settings change event after render | A cleanup of all notification settings |
| Same user dismisses three proactive messages in a row | Dismiss events across sessions | A user who always closes banners |

**Starter rule:** the assistant shows no proactive message while the user is typing or in the middle of a step, waits for the step to finish, and treats a quick close as a no; only urgent safety messages may interrupt.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: interrupts-at-a-bad-moment
runs: pre_send
reads: [ui.busy_flag, ui.last_input_at, ui.route, proactive.topic, proactive.urgency, session.proactive_count, user.dismissed_topics]
trigger: a proactive message is about to render while the user is typing, in a flow, or after a dismissal of the same topic
moves: [ask_clarifying_question, offer_choices, lead_with_answer]
choices: ["Yes, show me", "Not now", "Stop these tips", "Something else"]
on_miss: log
metric: dismissals within seconds
counter_metric: urgent messages delayed past the gate
status: proposed
```

## 8. Related patterns
- [Chat widget hard to find, or intrusive](../../onboarding-and-discoverability/failures/chat-widget-hard-to-find-or-intrusive.md): the closest page. It covers where the launcher sits and whether a website widget opens on page load. This page covers the timing of any message the assistant sends first, including in-app nudges, and the handling of a "no".
- [Impatient idle nudges](../../response-time/failures/impatient-idle-nudges.md): "Are you still there?" after a silence inside a chat the user started. This page is about messages that start a conversation.
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): what the message contains. This page is about when it arrives.
- [No proactive updates](../../conversation-frameworks/failures/no-proactive-updates.md): the opposite problem, an assistant that stays silent when the user needs an update (matched by name; I did not re-read that page).
- Related roadmap rows in this family without pages yet: dismissed suggestions come back, summaries and digests too long to read, ambient assistants act on overheard conversation, proactive action surprises the user.

## 9. Common questions
### When should a proactive chatbot message appear?
Not while the user is typing or in the middle of a step. Show it after a step finishes or after a pause, in a fixed spot, with a way to say "Not now." See rules 1 and 2.

### How do I stop an assistant from popping up while I'm typing?
As a user, look for a "Stop these" or snooze control on the message or in settings. As a builder, add a busy check before every proactive send (rule 1) and give the user that control (rule 8; WCAG 2.2.4 asks for it).

### Is a quick close the same as saying no?
Treat it as one. People tend to close popups without reading them ([NN/g](https://www.nngroup.com/articles/popups/)), so a close within seconds says "not now" at least. Suppress that topic for the session.

### Can a proactive message ever interrupt?
Yes, for a real emergency: data loss, a security problem, or a lost connection. WCAG 2.2.4 makes the same exception. A tip, a sale, or a survey is not an emergency.

### What is a good delay before a proactive message?
I found no sourced number. Start with a quiet period of about 10 seconds after the last keystroke and a wait for the step to finish, then tune on your dismissal rate.
