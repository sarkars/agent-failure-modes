# Chat Session Timed Out and I Lost My Conversation: Session Timeout and Lost Context

<!-- SEO
title: Chatbot Session Timed Out: Lost Context and How to Resume
description: A chat that expires on a timer, or greets a returning user as a stranger, forces a restart. Warn before expiry, keep the state, and resume where they left off.
search phrases:
- chatbot session timed out
- chat session expired lost my conversation
- chatbot timeout after inactivity
- how long should a chatbot session last
- chatbot resume conversation after inactivity
- dialogflow session timeout 30 minutes
- zendesk messaging conversation expires after inactivity
- chatbot makes me start over after I come back
-->

**Frequency**: Common

## Issue: A chat session expires on a timer the user was never told about, or a user who comes back after a gap is treated as new, so the work done so far has to be repeated.

> **One line:** You step away, come back, and the chat has closed or reset, with no warning and nothing carried over.

| | |
|---|---|
| **Channel** | Written for **chat** (web widget, in-app, messaging). Voice and web-form timeouts are PLANNED, not written. |
| **Stakes** | Low to high. Losing a chat about store hours is a nuisance; losing a half-finished claim, return, or dispute costs time and can lose the user's place in line. |
| **Who is affected** | Anyone who pauses mid-task: looking for a document, switching apps, taking a call, or using a slow connection. People who need more time to finish are hit hardest. |
| **Frequency** | Common. Every chat product with a session limit has the gap; I found no count of how often users hit it. |
| **Pattern ID** | session-timeout-and-lost-context |
| **Family** | [Response time](../README.md) |
| **Goal** | Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. For this pattern: a user returning after a gap resumes where they left off. |
| **Primary metric** | Context-resume success rate: returning sessions where the user continues without restating what they already gave. Starting target: over 90% (tune). Timeout-related complaints are the second metric. |
| **Maturity** | Researched (no tests written; see Section 6) |
| **Will a better model fix this?** | No. The timer, the retention rule, and the resume screen are product decisions. A model cannot recall a session its product closed. (Our judgment, not tested.) |
| **Also searched as** | chat session expired · chatbot closed while I was away · chatbot starts over when I return · chat timed out lost my place · conversation reset after inactivity |

## 1. In plain words
Chat products close or reset a conversation after a quiet period. That is reasonable. The failure is that the user is not told the limit, gets no warning before it hits, and finds either a dead chat or a blank one on return. The fix is to say the limit, warn once before it, keep the state for a stated time, and show where things stood when the user comes back.

## 2. What it looks like
The scenario is illustrative: a health insurer's help chat, a user disputing a $240 emergency-room bill.

**Without the fix**
```
User: I'm disputing a $240 ER charge from March 14. Claim number is on my explanation of benefits.
Bot:  I can help. Can you read me the claim number?
User: One sec, it's in my mail. (steps away for 45 minutes)
User: Okay, it's 8841-27.
Bot:  Hi! I'm the virtual assistant. How can I help you today?
User: I was just disputing a $240 ER charge! You already asked me for this.
```

**With the fix**
```
Bot:  (after the first quiet stretch) Still there? This chat closes in 5 minutes. I'll keep your place for 24 hours.
User: (returns 45 minutes later)
Bot:  Welcome back. You were disputing a $240 ER charge from March 14 and had the claim number ready.
      I kept that. I did not keep your identity check, so I need to confirm it again before I open the claim.
      [Continue the dispute] [Start something new] [Something else]
```
The fixed bot warned before expiry, said what it kept and what it did not, and asked only for the step that had to be repeated.

## 3. Why it happens
These are our reading of the pattern.
- **A fixed idle timer, unrelated to the task.** The clock counts quiet minutes, not whether the user is mid-task, so a user fetching a document looks identical to one who left.
- **Expiry deletes the working state, not just the connection.** Closing the session also discards the goal, the facts given, and the step reached, and nothing saves them for the return.
- **The limit is invisible.** The product does not say how long the chat stays open or how long state is kept, so neither the user nor the support team can plan around it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Dialogflow CX keeps session data for 30 minutes by default, counted from the last request. Developers can raise it with `QueryParameters.session_ttl` (maximum 24 hours), or save `current_page` and `parameters` and send them back later. The docs' example is a user who stops for 50 minutes; the new request need not use the same session ID, and the handler call stack is not restored. | [Google Cloud, *Dialogflow CX sessions*](https://docs.cloud.google.com/dialogflow/cx/docs/concept/session). Opened and read. | Vendor documentation. It shows that a default expiry exists and how to work around it, not how often users lose work. |
| Zendesk's default reminders for an inactive messaging conversation: the first after five minutes (ticket moves to Pending), the second five minutes later, the third one minute after that (ticket moves to Solved). By default the messaging session itself does not end. | [Zendesk, *Sending conversation inactivity reminders to end users*](https://support.zendesk.com/hc/en-us/articles/9496171412378-Sending-conversation-inactivity-reminders-to-end-users). Opened and read. | Vendor documentation for one product, with defaults an admin can change. |
| Zendesk AI agents treat a conversation as expired after 72 hours of inactivity and delete its back-end metadata, not the messages. A user who returns after that gets a new ticket that includes the last ten earlier messages. | [Zendesk, *Why do messaging conversations contain old and previous messages*](https://support.zendesk.com/hc/en-us/articles/7463958274586-Why-do-messaging-conversations-contain-old-and-previous-messages). Opened and read. | Vendor documentation; it describes what the ticket contains, not whether the user could resume the task. |
| WCAG success criterion 2.2.5 (Level AAA): "When an authenticated session expires, the user can continue the activity without loss of data after re-authenticating." Its goal is that users do not lose information or context due to reauthentication. | [W3C, *Understanding SC 2.2.5: Re-authenticating*](https://www.w3.org/WAI/WCAG22/Understanding/re-authenticating.html). Opened and read. | A web-accessibility standard written for authenticated sessions and forms, not chat. Level AAA is the highest, optional level. |

I found no controlled study of how often chat users lose work to a timeout, or of whether warnings reduce it. I searched for Intercom's behavior when a visitor returns after auto-close; only community-forum answers appeared, and they disagreed on whether the visitor lands in the old conversation or a new one, so I leave Intercom out. I also found no NN/g article on session timeouts.

**Public incident.** No public incident found for session timeouts in a chat assistant. The sources above are documentation, not reports of harm.

## 5. The fix

**The principle:** Say how long the chat stays open, warn before it ends, keep the user's place for a stated time, and on return show where things stood before asking anything.

**Do this**
1. **State the limit up front.** Early in the session, or in the first reminder, say how long a quiet chat stays open and how long the user's place is kept, using your configured values.
2. **Warn once before expiry.** Send one message before the chat closes, with a one-tap way to keep it open. Do not send a second warning for the same quiet stretch.
3. **Do not expire mid-task.** While the bot is waiting on the user for a named item (a document, a code, a confirmation), count the wait as part of the task and use a longer limit.
4. **Save state at expiry.** Store the goal, facts the user gave, decisions made, and the step reached, keyed to the user or device, for the stated retention time.
5. **On return, show the place before asking.** The first reply to a returning user restates the goal and what is already given, and asks only for what is missing.
6. **Say what was kept and what was not.** Name items that expired by design, such as an identity check, and ask for those only.
7. **Re-check facts that can change.** If the saved state involves an order status, price, or appointment slot, confirm it is still current before continuing.
8. **Never imply memory that was not kept.** If nothing was saved, say so and ask for the goal in one line.

**Reference design: the return message**
| Part | Content |
|---|---|
| Welcome | "Welcome back." No "How can I help you today?" if state exists. |
| Place | Goal, facts given, and step reached, in one to three lines |
| Kept / not kept | "I kept [X]. I did not keep [Y], so I need [Z] again." |
| Choices | Continue, start something new, something else |

```
When a user returns after a gap and saved state exists, show the goal, what is already given, and the step reached before asking anything.
Name what expired by design and ask only for that. Offer to continue or start something new.
Before a chat closes for inactivity, warn once and offer one tap to keep it open.
If nothing was saved, say so and ask for the goal in one line.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A user returns to saved state: "Continue the dispute", "Start something new", "Something else". Do not offer them when the user's first message is clearly a new topic, or when the user is in the middle of a reply and only needs the next line answered. |
| Admit uncertainty and show how to check | The saved state may be stale or incomplete: say what was kept, what was not, and ask the user to confirm the key facts. |
| Hand off to a person | Resume failed and the matter is time-sensitive: pass the saved summary to a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not keep sessions open forever or keep state indefinitely: a shared device, a stale price, or a closed claim can make old state wrong or private. Do not warn so early or so often that the warning becomes the pestering. Do not show the resume screen after a short pause in an active chat. Keep sensitive steps, such as identity checks, subject to your own security policy.

**Hand-off rule.** If the saved state is missing or wrong and the matter is time-sensitive or involves money, offer a person and pass whatever summary exists ([cold transfer](../../human-handoff/failures/cold-transfer.md) covers what a good hand-off carries).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests: **Not yet run**, and no full test file has been written.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | The user goes quiet near the limit | One warning with a keep-open option is sent before closing (rules 1, 2) |
| 2 | The bot is waiting for a document the user is fetching | The chat does not close at the normal limit (rule 3) |
| 3 | The user returns inside the retention time | First reply restates goal and facts given, and does not ask for them again (rules 4, 5) |
| 4 | The user returns after an identity check expired | Reply names the check as not kept and asks only for it (rule 6) |
| 5 | The user returns, and the saved order status has changed | The bot re-checks and reports the change before continuing (rule 7) |
| 6 | The user returns after the retention time | The bot says nothing was kept and asks for the goal in one line (rule 8) |
| 7 | The user returns with an unrelated new topic | No resume prompt is pushed (Moves table) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Context-resume success rate** (primary) | Over 90% (tune) | Returning sessions inside the retention time where the user does not restate the goal in the first 3 turns, over all such returns; confirm by sampled review | Below 80% |
| Timeout-related complaints | Track; set from baseline | Count of tickets or messages tagged "chat closed", "lost my chat", "started over" | Rising two weeks in a row |
| Warning sent before expiry | 100% (tune) | Expiry events with a preceding warning event | Below 95% |
| Expiry while awaiting a named user item | Under 1% of expiries (tune) | Expiry events where the bot's last turn asked for an item | Over 3% |
| Return messages that show the place before asking | Over 95% (tune) | Sampled review of first replies after a gap | Below 85% |
| Stale state used without re-check (counter-metric) | 0 | Resumes with changed facts and no re-check event | Any |
| Resume prompts after short pauses (counter-metric) | Under 2% of active sessions (tune) | Resume prompts shown within a session that never expired | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Greeting template sent to a user who had an open task before the gap | Turn event with greeting template and a prior session with an unfinished step | The user deliberately started something new |
| User repeats the goal or a fact from the earlier session in the first 3 turns after a gap | Turn text plus per-user session history | A correction because the earlier fact changed |
| Session expiry event while the bot's last turn asked for an item | Expiry event plus the last bot turn | The user abandoned the chat on purpose |
| User writes "you already asked" or "I just told you" within 5 turns of a return | Turn text in the first turns after a gap | A repeat inside one session, which is a different pattern (re-asks) |
| User ends the session within 3 turns of returning after a gap | Session end event after a return | The task was already done |

**Starter rule:** before a chat closes for inactivity, warn once; when the user returns, show the saved place before asking anything.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: session-timeout-and-lost-context
runs: conversation
reads: [session.idle_time, session.expiry_event, session.saved_state, session.awaiting_item, turn.user_text]
trigger: a session nears expiry, or a user returns after a gap with saved state
moves: [offer_choices, admit_uncertainty, hand_off]
choices: ["Continue where I left off", "Start something new", "Something else"]
on_miss: ask
metric: context-resume success rate
counter_metric: stale state used without re-check
status: proposed
```

## 8. Related patterns
- [Fresh-session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md): the closest page. It covers a new chat that starts with nothing from the last one and the consent-based continuity summary (view, edit, delete). This page covers the clock: the timer that ends a session, the missing warning, the state saved at expiry, and the return message in the same thread. Use that page for how a summary is approved and stored; use this one for when and how the session ends and resumes.
- [No warning of context loss](../../effort-and-memory/failures/no-warning-of-context-loss.md): content dropped because the conversation outgrew its limit. Here the limit is time, not size.
- [Silent failure and timeout](silent-failure-and-timeout.md): a request that times out with no error. That is one reply failing; this is a whole session ending.
- [Forces a fresh login](../../embedded-copilots/failures/forces-a-fresh-login.md): asks a signed-in user to log in again. Here the re-check is justified for some steps; the failure is losing the work around it.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): asking again within a live session for facts already given.

## 9. Common questions
### Why did my chat session time out?
Chat products usually close or reset a conversation after a quiet period. Dialogflow CX keeps session data 30 minutes by default; Zendesk's bot conversations expire after 72 hours of inactivity (see Section 4). Your product's limit may differ.

### How long should a chatbot session last?
I found no sourced answer. Vendors differ, and the right limit depends on the task. State your limit to the user, and extend it while the bot is waiting on something the user is fetching.

### Can a chatbot resume a conversation after a long gap?
Yes, if the product saves the state. Dialogflow CX's docs describe saving the current page and parameters and sending them with a new request, even in a new session ID. The bot still has to show the user where things stood.

### Is a timeout warning the same as "Are you still there?"
Not quite. A warning says the chat will close and keeps the user's place. A nudge that pushes the user to reply fast is a separate problem, listed in the roadmap but not yet written.

---
## Technical section

### T1. Solution architecture
```
idle timer -> awaiting-item check (extend if the bot asked for something)
           -> warn once -> expire
expire     -> save {goal, facts, decisions, step, awaiting} with retention time and owner
return     -> load state -> stale check on changeable facts -> return message (kept / not kept / choices)
```
The Dialogflow CX docs describe the same shape: record the current page and parameters from each response, and send them with the next input after a gap.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| State is deleted after the stated retention time | State store | Retention test in each release |
| State belongs to one user or device | Storage keys | Cross-user isolation test |
| Sensitive checks are not carried over unless policy allows | Resume logic | Test 4 |
| Changeable facts are re-checked before use | Resume logic | Test 5 |

### T3. Evals
- **Dataset:** a few dozen scripts that pause for different lengths (inside the warning window, inside retention, past retention) and resume, plus scripts that start a new topic.
- **Judge rubric:** does the return message restate the goal and facts correctly, name what was not kept, and avoid re-asking?
- **Metrics and starting thresholds:** resume success over 90%, warning sent 100%, stale-state use 0. Starting points to tune.
- **Release gate:** block a deploy if a session can expire without a warning event, or a resume skips the stale check.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Stale state used without re-check | Any | Any | Disable auto-resume for that fact type |
| Context-resume success rate | Below 80% | Below 60% | Check the state store and the expiry job |

### T5. Trade-offs
- Longer retention helps returning users but holds more personal data. Keep it short, stated, and deletable.
- Extending the limit while the bot awaits an item holds server resources longer.
- Saved state can go stale; the re-check costs a lookup.

---
### Deep dive
- **Open question.** I found no study of how often timeouts cost users their work in chat. The evidence here is vendor documentation and one accessibility standard.
- **Unverified.** Zendesk's default 10-minute inactivity definition and Intercom's re-open behavior appeared only in search summaries or forum posts; not used in the fix.
- **References.** [Dialogflow CX sessions](https://docs.cloud.google.com/dialogflow/cx/docs/concept/session) (opened); [Zendesk inactivity reminders](https://support.zendesk.com/hc/en-us/articles/9496171412378-Sending-conversation-inactivity-reminders-to-end-users) (opened); [Zendesk old and previous messages](https://support.zendesk.com/hc/en-us/articles/7463958274586-Why-do-messaging-conversations-contain-old-and-previous-messages) (opened); [W3C SC 2.2.5](https://www.w3.org/WAI/WCAG22/Understanding/re-authenticating.html) (opened).
