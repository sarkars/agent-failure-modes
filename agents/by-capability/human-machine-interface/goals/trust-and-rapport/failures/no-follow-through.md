# Chatbot Says "I'll Update You" and Never Does: No Follow-Through

<!-- SEO
title: Chatbot Promises to Follow Up but Never Does: How to Fix It
description: An AI agent says "I'll update you" or "I'll check back," but nothing is scheduled. Record every promise, keep it on time, or say what you can't do.
search phrases:
- chatbot says it will follow up but never does
- ai agent promises to get back to me
- how to make an ai agent follow up later
- chatbot "i'll update you" no notification
- ai agent scheduled follow-up reminder design
- llm agent can't message user later
- chatbot callback promise not kept
-->

**Frequency**: Occasional

## Issue: An AI agent says "I'll update you" or "I'll check back," but no promise is recorded, scheduled, or delivered, so the user waits for a message that never comes.

> **One line:** The bot promises a future action in words, but nothing in the system will ever perform it, and nobody notices.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and email promises are PLANNED, not written. |
| **Stakes** | Low to high. A missed "I'll tell you when the refund posts" is low; a missed "I'll alert you before the deadline" is high. |
| **Who is affected** | Any user who is told to wait: long tasks, pending orders, refunds, claims, tickets, reminders |
| **Frequency** | Occasional (our judgment). I found no study that measures how often chatbots break follow-up promises. |
| **Pattern ID** | no-follow-through |
| **Family** | [Trust and rapport](../README.md) |
| **Goal** | Users know what they are dealing with, what it can do, and can rely on what it says it did. In this pattern: every promise is recorded and kept. |
| **Primary metric** | Promise-kept rate: promises delivered by their stated time, divided by promises made. Starting target: 98% (tune on your own data). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Our judgment: a model can word a promise well, but keeping it needs a promise ledger, a scheduler and a delivery channel, which are engineering. |
| **Also searched as** | chatbot never follows up · ai agent says it will get back to me · chatbot promised a callback · agent can't send a message later · chatbot "I'll let you know" |

## 1. In plain words
The bot says "I'll let you know when it's ready." Then the turn ends. Nothing is saved, nothing is timed, and the bot has no way to message the user first. The fix is to make a promise a record: write it down with a time and a way to reach the user, send it, and mark it kept. If the bot can't do that, it should not make the promise.

## 2. What it looks like
**Without the fix**
```
User: My refund for order 48213 hasn't posted. Can you check?
Bot:  Checked. It's still pending at the bank. I'll update you as soon as it posts!
User: Great, thanks.
      (nothing is saved; no job is scheduled; the user never hears back)
User (3 days later): Hello? Did my refund post?
```
**With the fix**
```
User: My refund for order 48213 hasn't posted. Can you check?
Bot:  It's still pending at the bank. I can message you here or by email when it posts.
      I'll also check again on Friday, Oct 23, and tell you either way. Which do you prefer:
      here, email, or something else?
User: Email.
Bot:  Done. Reminder R-3391 is set: I'll email you by Fri, Oct 23, even if there's no change.
```
The fixed bot asked where to reach the user, made a record with an ID and a date, and promised an update even if nothing changed.

## 3. Why it happens
- **A promise is only text.** The model can write "I'll check back" with no tool behind it. One agent-framework doc says it directly: "A promise in chat is not a scheduled callback: creation must return a follow-up ID."
- **No way to reach the user first.** Many chat deployments can only reply inside an open session. With no outbound channel, nothing can deliver the update.
- **Nothing audits promises.** Teams log answers and errors, not commitments, so a broken promise leaves no trace until the user comes back.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| J.D. Power's analysis of unresolved customer service calls names "Broken Promises" ("Follow-up actions promised by the representative did not occur") as one of four drivers, and says it had the most detrimental effect on satisfaction, ahead of miscommunication and inaccurate information. It recommends being transparent about delays and next steps. | [J.D. Power, *What customers say about unresolved calls*, Aug 14, 2024](https://www.dev.jdpower.com/business/news/what-customers-say-about-unresolved-calls/) (opened) | Phone calls with human representatives, not chatbots. The page gives no percentages or sample size for this driver. A vendor's article, not a peer-reviewed study. |
| An agent framework's docs state: "A promise in chat is not a scheduled callback: creation must return a follow-up ID." | [Kylon docs, follow-ups](https://docs.kylon.io/concepts/followups.md) (opened) | One vendor's design rule. It is a useful test for a promise, not a measurement. |
| Cloudflare's Agents SDK persists scheduled tasks: "Scheduled tasks survive agent restarts and are persisted to SQLite," and Durable Object alarms wake the agent when a task is due. Delayed and one-time date tasks can pile up as duplicates after restarts unless marked idempotent. | [Cloudflare Agents docs, schedule tasks](https://developers.cloudflare.com/agents/runtime/execution/schedule-tasks/index.md) (opened) | Shows that a durable scheduler is available and what its pitfalls are. It is one vendor's product, not evidence of how often promises fail. |

I found no study that measures how often chatbots or AI agents fail to follow up, or how that affects trust. Some forum posts (an Adobe community thread about missed callbacks, a Zoho community post) turned up in search summaries. I did not open them, and I kept them out of the fix and the numbers.

## 5. The fix
**The principle:** A promise is a record with an owner, a time and a delivery route; if the bot can't make that record, it doesn't make the promise.

**Do this**
1. **Promise only what a tool recorded.** Say "I'll update you" only after a scheduling or ticket call returned an ID. Otherwise use rule 4.
2. **Record every promise in a ledger** with: what, due time, delivery channel, owner, and status (open, kept, late, broken, canceled).
3. **Say it in the reply:** what you will do, by when, and where the user will hear it. Include the ID.
4. **If you can't follow up, say so and give the user a way to check.** "I can't message you later. You can check order status at [link], or ask me here."
5. **Keep it on time.** At the due time, send the result. If the result isn't ready, send "still pending" with a new time, before the old time passes.
6. **Promise an update even if nothing changes,** when the user is waiting on a result.
7. **If a promise can't be kept, tell the user and offer a person.** Mark it broken in the ledger.
8. **Let the user cancel or change it** ("stop updates," "text me instead"). Honor it in the next send.
9. **Make the ledger durable.** It must survive a restart or deploy, and a retry must not send the update twice.

**Reference design: promise ledger record**
```
promise_id:     R-3391
conversation:   c_8f21
text_said:      "I'll email you by Fri, Oct 23, even if there's no change."
action:         recheck refund status for order 48213, then notify
due_at:         2026-10-23T17:00:00-05:00
channel:        email (user consented in this chat)
status:         open | kept | late | broken | canceled
created_by:     tool call schedule_followup -> returned R-3391
```
```
Before you tell a user you will do something later, call schedule_followup. Say you will follow up only if it returns an ID.
Put what, when and where in the reply. If there is no follow-up tool or channel, say you can't message them later and give a way to check.
At the due time, send the result or a new time. Never leave a promise open past its due time with no message.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The bot has no scheduler or no outbound channel: say it can't message later and give the user one way to check. Do not promise a follow-up you can't send. |
| Offer choices: 2-4 options plus "Something else", free text open | The bot can follow up and more than one channel is possible: "Here", "Email", "Text", "Something else". Do not offer a channel the product can't send on. |
| Hand off to a person | A promise is about to be late or can't be kept: tell the user, and offer a person. Do not hand off if the user asked to wait for the bot. |

**Don't over-correct.** Don't stop saying "I'll" for work done in the same turn ("I'll look that up now" is fine). Don't promise nothing: a plain "I can't message you later" beats a silent gap. Don't send a message every hour to prove you're alive; one update at the promised time, plus one on a delay, is enough.

**Hand-off rule.** If a promised update is overdue, or the bot can't deliver on the channel the user chose, tell the user and offer a person, with the promise ID and what was promised ([cold transfer](../../human-handoff/failures/cold-transfer.md) covers what to pass on).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md). The ledger and the follow-up ID rule come from agent scheduler designs (see sources in section 4), not from a published human-factors framework.

## 6. How to test it (short version)
Results: **Not yet run.**

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | The user waits on a pending refund and the bot says "I'll update you" | A ledger record with an ID exists before the words are sent (rules 1, 2) |
| 2 | The same, with the follow-up tool disabled | The bot says it can't message later and gives a way to check (rule 4) |
| 3 | A promise comes due and the result is ready | The update arrives on the chosen channel by the due time (rule 5) |
| 4 | A promise comes due and the result isn't ready | A "still pending" message with a new time goes out before the old time passes (rules 5, 6) |
| 5 | The scheduler restarts before the due time | The update still fires, once (rule 9) |
| 6 | The user says "stop updates" | No further sends; the record is marked canceled (rule 8) |
| 7 | The channel fails (bounced email) | The promise is marked broken, and the user is told or offered a person (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Promise-kept rate** (primary) | 98% | Ledger: promises with status kept by `due_at`, divided by promises made | Below 95% |
| Untracked promises | 0 | Scan bot turns for promise phrases ("I'll update you," "I'll check back") with no ledger ID in the same turn | Any |
| Overdue open promises | 0 | Ledger rows still open past `due_at` | Any older than 1 hour |
| Late promises with notice | Over 95% of late ones | Late rows with a "new time" message sent before `due_at` | Below 90% |
| Duplicate or post-cancel sends (counter-metric) | 0 | Sends per promise above 1, and sends after a cancel event | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All signals are for text chat events. Voice and web signals are PLANNED only: never detected or measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot turn contains a promise phrase and no ledger ID | Bot message text matched against promise phrases, versus a `schedule_followup` event in the same turn | "I'll look that up now," where the work finishes in the same turn |
| Ledger row open past `due_at` | Ledger status and due time | A promise the user postponed in chat |
| Update sent after the due time with no earlier delay notice | Send event time versus `due_at` and any delay message | A delay the user asked for |
| User asks "any update?" or "did you forget?" about an earlier promise | User turn classified as a status check, with an open or overdue ledger row | A user checking before the promised time, out of habit |
| Promise made while the session has no outbound channel or no follow-up tool | Session capability flags versus a promise phrase in a bot turn | A channel the user is about to set up in the next turn |

**Starter rule:** say "I'll update you" only after a scheduling call returned an ID; otherwise say you can't message them later and give a way to check.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-follow-through
runs: pre_send
reads: [bot_draft.text, session.followup_tool_available, session.delivery_channels, ledger.promise_id, ledger.due_at, ledger.status]
trigger: the bot is about to promise a later update, or a promise reaches its due time
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Here in chat", "Email me", "Text me", "Something else"]
on_miss: rewrite
metric: promise-kept rate
counter_metric: duplicate or post-cancel sends
status: proposed
```

## 8. Related patterns
- [False completion claim](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md): the closest pattern. That one claims a task is done when it is not. This one promises a future action and never does it. The first is a false report about the past; the second is a broken commitment about the future. A bot can have both.
- [Undisclosed bot identity](undisclosed-bot-identity.md): hides what the bot is and what it can't do. Rule 4 here is the same honesty about limits, applied to follow-up.
- [Chatbot says a person will join, but nobody is working](../../human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md): a broken promise of a human, with no route offered. This page covers any promised follow-up.
- [Silent long-running work](../../response-time/failures/silent-long-running-work.md): no status while working in the same session. This page is about promises that span sessions.
- [Fresh session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md): the bot forgets earlier sessions, so even a sincere promise can be lost.

## 9. Common questions
### Why does my chatbot say it will follow up and then never does?
Usually the promise is only words. No tool recorded it, and no job or channel exists to deliver it. See section 3 and rule 1.

### How do I make an AI agent follow up later?
Give it a scheduling tool that returns an ID, store each promise in a durable ledger, and send the update at the due time. Persisted schedulers exist, such as the one in the [Cloudflare Agents docs](https://developers.cloudflare.com/agents/runtime/execution/schedule-tasks/index.md). Check retries so an update isn't sent twice.

### What should a chatbot say if it can't message me later?
Say so plainly and give a way to check: "I can't message you later. You can see the status at [link], or ask me here." That beats a promise that won't be kept.

### Is this the same as the chatbot claiming it finished something it didn't?
No. That is the [false completion claim](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md): a wrong report about work already done. This is a promise about work to come.

---
## Technical section

### T1. Solution architecture
```
bot draft -> promise detector -> has ledger ID? -- no -> rewrite (rule 1 or 4)
                                      | yes
user reply  <- delivery channel <- scheduler (due_at) <- promise ledger (durable)
                                      |
                  result ready? -- yes -> send, mark kept
                                 -- no  -> send "still pending, new time", update due_at
                  send failed   -> mark broken, tell user or hand off
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No promise phrase without a ledger ID | Pre-send check | Test 1, untracked-promise scan |
| The ledger is durable and idempotent | Scheduler and storage | Test 5; duplicate-send count |
| Delivery channel confirmed with the user | Promise creation | Ledger row has a consented channel |
| Cancel is honored | Send step | Test 6 |

### T3. Evals
- **Dataset:** 40 conversations where a wait is natural (pending refund, claim review, long job, reminder), half with the follow-up tool disabled; seven scenarios from section 6.
- **Judge rubric:** does a promise phrase appear only with a ledger ID? When there is no tool, does the bot say so?
- **Metrics (starting points to tune):** untracked promises 0; promise-kept rate 98% in simulation; duplicate sends 0.
- **Release gate:** block a deploy if any untracked promise appears in the test set or test 5 fails.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Overdue open promises | 1 over 15 minutes | Any over 1 hour | Check scheduler health and the delivery channel |

### T5. Trade-offs
- A ledger and scheduler add storage, a worker and a delivery path to run. For a bot that only answers in-session, the cheaper fix is rule 4: never promise.
- Proactive messages need consent and a channel; each added channel adds rules to follow.

---
### Deep dive
- **Not scanning for intent.** One open-source follow-up tool is reported (in a search summary I did not open) to make the agent call the tool on purpose instead of detecting promise phrases. The detector here is a safety net, not the main path.
- **Modality notes (PLANNED):** *Voice:* a promised callback needs a number and a time window read back to the caller. *Email:* the bot may send the update outside the chat; consent rules differ.
