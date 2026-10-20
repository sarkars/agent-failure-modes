# Customers Keep Asking "Where Is My Order?": No Proactive Updates

<!-- SEO
title: "Where Is My Order?" Chatbot Contacts: No Proactive Updates
description: Why users must ask a chatbot "where is my order?" or "any update?", and how to tell them status, delays, and next steps before they ask.
search phrases:
- chatbot customers keep asking where is my order
- how to reduce where is my order contacts chatbot
- chatbot proactive status updates
- chatbot doesn't tell me what's happening with my request
- how to send proactive updates from an ai agent
- chatbot "any update" asking for status again
- proactive customer notifications chatbot design
-->

**Frequency**: Common

## Issue: A user's order, claim, or request is in progress, and the bot says nothing until the user comes back and asks "any update?", so every status check is a chase.

> **One line:** The bot tells the user the status only when asked; the fix is to decide at the start which changes the user will hear about, and to say them before the user has to ask.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and email-only flows are PLANNED, not written. |
| **Stakes** | Low to medium. A late "your package slipped a day" is low; a claim or refund that stalls for weeks is medium. |
| **Who is affected** | Users with something in progress: orders, returns, refunds, claims, tickets, applications |
| **Frequency** | Common. This is our judgment from how status bots are built (they answer lookups, they do not volunteer). I found no study that counts how often bots fail to update. |
| **Pattern ID** | no-proactive-updates |
| **Family** | [Conversation frameworks](../README.md) (row FW-C05) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | "Where is my X?" contact rate: status-request chats divided by in-progress cases. Start: set from your baseline, then aim to fall (tune) |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model words an update well, but sending one needs a status event, a user-approved channel and a trigger, which are product and engineering. (Our judgment, not tested.) |
| **Also searched as** | where is my order chatbot · chatbot never updates me · chatbot "any update" · WISMO · proactive notifications chatbot · have to ask for status every time |

## 1. In plain words
A user starts a return, a claim, or a repair. Nothing is said until the user comes back and asks, "Where is my refund?" A good support agent calls first: "Your refund is delayed two days; here is why." The bot only answers questions, so the user has to chase, and silence reads as "nothing is happening."

## 2. What it looks like
**Without the fix** (Harbor Outdoor Gear, a return for order 70418)
```
User: I'm returning my tent, order 70418. Label please.
Bot:  Return approved. Label sent to your email. Refunds post after we receive the item.
User: Thanks.
      (carrier scans delivery on Oct 12; refund is held for inspection; bot sends nothing)
User (Oct 19): Where's my refund? It's been a week.
Bot:  Your return was received Oct 12 and is under inspection. Refund pending.
User: Nobody told me that. How long does inspection take?
```
**With the fix**
```
User: I'm returning my tent, order 70418. Label please.
Bot:  Return approved. Label sent to your email. Refunds post after we receive and inspect the item.
      I can message you at each change: received, refunded, or any delay. How do you want updates?
      Text, email, or something else? (Or say "no updates".)
User: Text.
Bot:  Text it is. You'll hear from me when it's received, and I'll tell you if it stalls.
      (Oct 12, text) Your tent arrived and is in inspection. Typical next change: refund approved.
      I'll text you again by Oct 16 either way.
```
The fixed bot asks once how to reach the user, then tells them each change and gives a date for the next update, so nothing needs chasing.

## 3. Why it happens
- **The bot is built to answer, not to speak first.** The product is a request-response chat. Status lives in the order system, and nothing turns a status change into a bot message.
- **No approved channel.** The bot has no stored consent or contact method for messaging the user outside the open chat, so even a wanted update cannot be sent.
- **Nobody owns the "what counts as news" rule.** Without a list of changes worth telling, teams either send nothing or send every internal event.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Nielsen Norman Group's first usability heuristic says "systems should always keep users informed about what is going on" through "appropriate feedback within reasonable time", and that "no action with consequences to users should be taken without informing them." | [NN/g, *Visibility of System Status* (Aurora Harley, June 3, 2018)](https://www.nngroup.com/articles/visibility-system-status/). Opened. | A general interface principle, not a chatbot study. It gives no time limit. It supports the fix idea; it does not measure how many contacts it prevents. |
| Moveworks' bot documentation recommends progress updates for "long-running or user-visible actions" to reduce perceived wait time, and says to skip them for "backend-only or fast operations" to avoid clutter. | [Moveworks docs, *Progress Updates*](https://docs.moveworks.com/agent-studio/actions/compound-actions/progress-updates). Opened. | Vendor documentation for one product. It covers waits inside a conversation, not status over days. It supports the "don't over-update" guardrail. |
| Descartes, a delivery-software vendor, attributes "where is my order" (WISMO) calls mainly to a lack of proactive tracking and communication, and lists five messages: order confirmation, scheduled delivery, in-transit, ETA update, delivery confirmation. It defines the WISMO rate as WISMO inquiries divided by total deliveries over a period. | [Descartes, *WISMO Calls: How to Reduce Them*](https://www.descartes.com/resources/knowledge-center/wismo-calls-how-reduce-them-and-boost-last-mile-efficiency). Opened; no publication date shown. | Vendor marketing for delivery logistics. It gives no data on how much each message reduces calls. Used here for the metric definition and the milestone list only. |

Not used: search summaries cited percentage reductions in status contacts from several shipping-software vendors (for example, ranges from 20% to 75%). I did not open the originals, and the figures disagree with each other, so I use none of them. I found no independent or controlled study of proactive updates in chatbots. Teams should measure their own before-and-after contact rate.

**Public incident.** No public incident found. I ran searches on proactive customer notifications and WISMO contacts, on chatbot long-running-task progress updates, and on WISMO study figures. The results were vendor guides, not dated incidents I could open.

## 5. The fix
**The principle:** Decide when the case opens which changes the user will hear about, then send each one on time, before the user asks.

**Do this**
1. **At the start of any in-progress case, state the milestones the user will hear about** (for example: received, refunded, delayed) and the next expected date.
2. **Ask once how to reach the user and honor the answer.** Offer text, email, or in-chat only, plus "no updates". Never message a channel the user did not approve.
3. **Send an update when a tracked status changes, within 15 minutes of the change** (starting point, tune). One message: what changed, what it means, what happens next.
4. **Tell the user about a delay when you know, not when they ask.** Say the new date, the reason if known, and what the user can do.
5. **Give a "next update by" date in every update, and send one on that date even if nothing changed.** "Still in inspection; next update Oct 16."
6. **Send nothing for internal events that change nothing for the user,** such as a warehouse scan or a ticket reassigned.
7. **Answer a direct "where is it?" from the live status first,** then confirm the update plan. Never reply "I'll update you" unless a trigger exists (see [no follow-through](../../trust-and-rapport/failures/no-follow-through.md)).
8. **Stop on request.** After "stop" or "no updates", send none, and confirm in one line.

**Reference design: the update plan (create it when the case opens)**
```
case_id: 70418-return
channel: sms            # approved by the user; "none" if declined
notify_on: [received, refund_issued, delay_over_1_day, stalled_past_next_update_by]
next_update_by: 2026-10-16
update_message: what changed + what it means + what happens next + next update date
suppress: [internal_scan, reassignment, duplicate_status]
last_sent: 2026-10-12T14:05
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | An update or a "where is it?" reply starts with the current status and the next date, before any apology or detail. |
| Offer choices: 2-4 options plus "Something else", free text open | When the case opens, asking how to reach the user: "Text", "Email", "Here in chat only", "Something else". Do not offer them if the user already chose, or if the update would go to the open chat. |
| Admit uncertainty and show how to check | The status feed is stale or has no estimate: say what is known, what is not, and where the user can check. |
| Hand off to a person | The case is stalled past its date, the user has asked twice, or the stakes are high. Attach the case summary. |

**Don't over-correct.** Do not message every internal scan, send updates that say nothing new, or message on a channel the user did not approve. A status text every hour is its own failure. The guardrail is the milestone list: if a change is not on it, the user hears nothing. The "next update by" message is the single allowed no-news message.

**Hand-off rule.** If a case has passed its promised date, or the user has asked for status twice in one case, send the case to a person with the plan, the status history, and what the user was told.

**Framework used:** none yet. The idea of keeping users informed comes from NN/g's visibility heuristic (section 4), a general interface principle, not tested on chatbots. See the [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | A user opens a return | Reply states the milestones and the next update date | 1 |
| 2 | User has not chosen a channel | Bot offers 2-4 channels plus "no updates" and "Something else", and sends nothing elsewhere | 2 |
| 3 | The refund status changes to "received" | A message with what changed, what it means, the next step, and the next date goes out within 15 minutes | 3, 5 |
| 4 | The delivery date slips two days | The user is told the new date before asking | 4 |
| 5 | The next-update date arrives with no change | A short "no change, next update by" message is sent | 5 |
| 6 | The carrier logs an internal scan only | No message is sent | 6 |
| 7 | User asks "where is my refund?" | Reply gives the live status first, then the plan; no "I'll update you" without a trigger | 7 |
| 8 | User says "stop updates" | One-line confirmation; no later messages | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **"Where is my X?" contact rate** (primary) | Set from your baseline; aim to fall (tune) | Chats classified as status requests (intent label, then a judge on a sample) divided by in-progress cases in the same period. Same definition as the WISMO rate in section 4. | Up 20% vs baseline |
| Proactive update rate | Over 95% of milestone changes (tune) | Milestone changes with a sent update within the time limit, divided by all milestone changes in the plan | Below 85% |
| Updates sent on a channel the user did not approve (counter-metric) | 0 | Sends where `channel` differs from the stored choice | Any |
| Updates after "stop" | 0 | Sends after an opt-out event | Any |
| Updates per case with no new information | Under 10% (tune) | Sampled review of updates that repeat the previous status, excluding the dated no-change message | Over 20% |
| Cases past their promised date with no update | 0 | Cases where `next_update_by` has passed and `last_sent` is earlier | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User asks for status on a case with no update sent | `user.intent` is status and `case.last_sent` is empty | The user asked within minutes of opening the case |
| User asks for status again after a status reply | Second status intent in the same case | The user wants a specific detail, such as the carrier name |
| Status changed but no message went out | `case.status_changed_at` is later than `case.last_sent` by over the time limit | The user opted out or the change is not on the milestone list |
| Promised date passes with no message | `case.next_update_by` earlier than now and `last_sent` earlier than it | The case was closed at the user's request |
| Bot says "I'll update you" with no trigger | Reply text phrase with an empty `case.notify_on` | The user asked the bot not to update them |

**Starter rule:** when a case opens, state the milestones the user will hear about and the next update date, and send each change before the user asks.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds beyond those marked as starting points)
```yaml
pattern_id: no-proactive-updates
runs: conversation
reads: [case.status, case.status_changed_at, case.notify_on, case.channel, case.next_update_by, case.last_sent, user.opted_out]
trigger: a tracked status changes, or a case reaches its next_update_by date without a message
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Text", "Email", "Here in chat only", "Something else"]
on_miss: log
metric: "Where is my X?" contact rate
counter_metric: updates sent on a channel the user did not approve
status: proposed
```

## 8. Related patterns
- [No follow-through](../../trust-and-rapport/failures/no-follow-through.md): the bot promises "I'll update you" and nothing is scheduled. This page is the next step: even with a working scheduler, the team has not decided which changes the user hears about, or when. Keep the promise there; choose and send the news here.
- [Silent long-running work](../../response-time/failures/silent-long-running-work.md): a wait inside one conversation with no progress message, measured in seconds. This page covers status that changes over hours or days, after the chat may have ended.
- [Silent failure and timeout](../../response-time/failures/silent-failure-and-timeout.md): a request ends with no reply or error. Here the case is running normally and the user is just not told.
- [No warning of context loss](../../effort-and-memory/failures/no-warning-of-context-loss.md): the bot forgets and does not say so. Different subject: that is about the bot's own memory, not the status of the user's case.
- [No follow-up](no-follow-up.md): a sales chat ends and the lead goes cold; follow up only as agreed. That is about re-engaging a lead; this is about status of work already in progress.

## 9. Common questions
### Why do customers keep asking my chatbot "where is my order?"
Often they were told nothing after the order or request was confirmed. The bot answers lookups but never speaks first. See [why it happens](#3-why-it-happens) and rules 1 to 3.

### Should a chatbot send an update when nothing has changed?
Only one kind: the dated "no change, next update by" message from rule 5, so the user knows the case is alive. Other no-news messages are noise (rule 6).

### Do I need the user's permission to send proactive updates?
Ask which channel they want and honor "no updates" (rules 2 and 8). This page is design guidance, not legal advice. Whether texts or emails need formal consent depends on your channel and jurisdiction; get that reviewed. I did not verify any regulation.

### How many updates is too many?
Send only the changes on the milestone list plus the dated no-change message. If sampled updates repeat the last status more than occasionally, cut them (section 7). The right number depends on how long your cases run.

### Will proactive updates cut my status contacts?
Vendor pages claim they do, but the numbers I saw varied widely and none came from a source I could open and check (section 4). Measure your contact rate before and after on a subset of cases.

### How is this different from a progress bar or a "working on it" message?
Those cover a wait of seconds inside one chat. This covers changes over hours or days, sent after the chat may be closed. See [silent long-running work](../../response-time/failures/silent-long-running-work.md).

---
## Technical section

### T1. Solution architecture
```
status event (order/claim system) -> plan lookup (notify_on, channel, opt-out) -> dedupe + milestone filter
  -> compose update (what changed, meaning, next step, next date) -> send on approved channel -> log last_sent
scheduler: at next_update_by, if no message since last_sent -> send the dated no-change message
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Update plan created when a case opens | Case creation | Test 1 |
| Send only on the approved channel | Sender | Test 2; counter-metric |
| Send within the time limit | Event consumer | Test 3; proactive update rate |
| Dated no-change message on the due date | Scheduler | Test 5; cases-past-date metric |
| Internal events suppressed | Milestone filter | Test 6 |
| No sends after opt-out | Sender | Test 8 |

### T3. Evals
- **Dataset:** 50 simulated cases to start: on-time, delayed, stalled, opt-out, no channel chosen, internal-only events.
- **Judge rubric:** did the user learn each milestone change before asking; does each update say what changed, what it means, what next, and when; was any update noise?
- **Release gate:** block a deploy on any send to an unapproved channel or after opt-out; other thresholds are starting points to tune.

### T5. Trade-offs
- Needs a status feed and a sender. Without them, only rules 1, 2 and 7 can be followed, in chat.
- More updates can reduce chases and raise opt-outs. Watch both; the counter-metrics catch the second.

---
### Deep dive
- **Open question.** I found no controlled study of proactive chatbot updates and status contacts. The evidence here is a general interface principle, one vendor's bot documentation, and a logistics vendor's page.
- **References.** [NN/g, Visibility of System Status](https://www.nngroup.com/articles/visibility-system-status/) (opened); [Moveworks docs, Progress Updates](https://docs.moveworks.com/agent-studio/actions/compound-actions/progress-updates) (opened); [Descartes, WISMO Calls](https://www.descartes.com/resources/knowledge-center/wismo-calls-how-reduce-them-and-boost-last-mile-efficiency) (opened). Not opened: the shipping-vendor pages that appeared in search results (ShippyPro, Ringly, ClaimLane and others); their figures are unverified and unused.
