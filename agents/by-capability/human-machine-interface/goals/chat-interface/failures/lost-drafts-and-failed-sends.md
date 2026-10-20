# Chat Message Failed to Send or Disappeared: Lost Drafts and Failed Sends

<!-- SEO
title: Chat Message Failed to Send or Disappeared? Keep the Draft
description: A chat message typed on a weak connection vanishes, or a send fails with no sign. Keep the draft locally, mark each message Sent or Not sent, and retry without duplicates.
search phrases:
- chat message failed to send
- chatgpt message disappeared after sending
- chatbot message not sending
- save chat draft offline
- typed message lost after refresh
- retry failed message without duplicates
- client message id idempotency chat
-->

**Frequency**: Common

## Issue: A chat message typed on a weak connection disappears, or sending fails silently, so the user cannot tell whether the bot got it and often has to type it again.

> **One line:** The user's own message is lost before the bot ever sees it; the fix is to keep the draft on the device until the server confirms it, and to mark every message Sent or Not sent, with a retry that cannot send it twice.

| | |
|---|---|
| **Channel** | Written for **chat** (web widget, in-app chat, assistant apps). Voice is PLANNED, not written. |
| **Stakes** | Low to high. Retyping a question is a nuisance; losing a long dispute description, or sending a payment instruction twice on retry, is not. |
| **Who is affected** | People on phones, trains, rural or public Wi-Fi, or behind VPNs and office firewalls; anyone who writes long messages |
| **Frequency** | Common, in our judgment. I found public forum reports (below) but no count of how often sends fail in chat products. |
| **Pattern ID** | lost-drafts-and-failed-sends |
| **Family** | [Chat interface](../README.md) |
| **Goal** | The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost. |
| **Primary metric** | Messages lost per 1,000 sent. Target: 0 (a design target, not a measured figure). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The message is lost in the client and the network before any model sees it. (Our judgment, not tested.) |
| **Also searched as** | message disappeared after hitting send · chat not sending · lost what I typed · message sent twice after retry · chat stuck on sending · offline chat draft |

## 1. In plain words
The user types a message and taps Send. The connection drops, the box clears, and the message is gone: no bubble, no error, nothing to retry. Or the bubble sits on a spinner forever, and when the user retries, the bot gets the message twice. The fix is in the chat window, not the bot: save the draft as it is typed, give every message one ID, show whether it was sent, and make retry safe.

## 2. What it looks like
The scenario is illustrative: a commuter on a train out of Chicago writing to a power company's help chat about a $312 bill.

**Without the fix**
```
User types: "My October bill is $312, double September. Meter reading looks wrong. Account ends 4471."
User taps Send. The train enters a tunnel.
Screen:     The input box clears. No bubble appears. No error.
User:       Reopens the app at the next stop. The chat shows only the bot's greeting.
User types: the whole message again, shorter, and gives up on the meter detail.
```

**With the fix**
```
User types the same message and taps Send. The train enters a tunnel.
Screen:     The message appears as a bubble marked "Sending"
Screen:     After the timeout: "Not sent. Your message is saved. [Retry] [Edit] [Copy text]"
User:       Reopens the app at the next stop. The bubble is still there, still marked "Not sent".
User taps Retry. The bubble changes to "Sent". One copy reaches the bot, which replies once.
```
The fixed window never clears the text until it is safe, says plainly whether it was sent, and the retry cannot create a second copy.

## 3. Why it happens
- **The input box is cleared on tap, not on confirmation.** The text lives only in memory between tap and server receipt, so a drop, a reload, or an app kill in that window erases it.
- **No per-message status.** The client sends and waits; it has no "Sending", "Sent", or "Not sent" state, so a timeout either shows nothing or a spinner that never ends.
- **Retries are not idempotent.** Each resend is a new request with no message ID, so a send that actually arrived but lost its acknowledgment is stored twice and answered twice. Teams that see duplicates then disable retry, which brings back the loss.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A ChatGPT user reported on October 25, 2023 that typed messages "just disappear" and nothing gets sent; others reported the same, and the workarounds found were closing a banner or switching browsers. | [OpenAI Developer Community thread, 2023](https://community.openai.com/t/cant-use-chatgpt-unknown-reason-buttons-unresponsive/451639). Opened and read. | Anecdotal, a handful of users. No official explanation in the thread. Shows the failure happens, not how often. |
| A user reported on August 19, 2024 that after a "network error" the part of the conversation after the error vanished. | [OpenAI Developer Community thread, 2024](https://community.openai.com/t/i-cant-keep-chatting-my-chat-disappears-after-getting-error-messages/913982). Opened and read. | Anecdotal, one user. It is about the conversation vanishing, a neighbor of this pattern. |
| NN/g advises letting users fix errors by editing their original action instead of starting over, and showing the text they entered. | [Neusesser and Sunwall, *Error-Message Guidelines*, NN/g, May 2023](https://www.nngroup.com/articles/error-message-guidelines/). Opened and read. | General interface guidance, not a chat study. |
| MDN says `localStorage` data is saved across browser sessions with no expiration, per origin, as strings; in private browsing it is cleared when the last private tab closes, and a `SecurityError` is thrown if the user has blocked the page from persisting data. | [MDN, Window: localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage). Opened and read. | Browser documentation. It says what the store does, not how chat products use it. |
| MDN calls `navigator.onLine` "inherently unreliable": a LAN with no internet can count as online. It advises using it only for hints, not to disable features. `online` and `offline` events fire on `window` when it changes. | [MDN, Navigator: onLine](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine). Opened and read. | Browser documentation. |
| The IETF Idempotency-Key draft defines a client-generated key the server uses to recognize retries, recommends a UUID, forbids reusing a key with a different payload, and says a retry after completion should get the earlier result (a concurrent retry gets HTTP 409). | [draft-ietf-httpapi-idempotency-key-header-07](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header). Opened and read. | An Internet-Draft dated October 15, 2025 that expired April 18, 2026; not a standard. |
| Stripe documents the same mechanism in production: retries with the same key return the saved result, keys are up to 255 characters, can be pruned once at least 24 hours old, and should not contain personal data. | [Stripe API reference, Idempotent requests](https://docs.stripe.com/api/idempotent_requests). Opened and read. | Vendor documentation for a payments API, not chat. |

I found no study that counts lost or duplicated chat messages. A search for Slack's own help page on failed sends returned only third-party guides, which I did not open and do not use.

## 5. The fix
**The principle:** The user's text is never thrown away until the server has confirmed it, and every message shows whether it was sent.

**Do this**
1. **Save the draft as the user types.** Store it on the device, keyed by conversation, and restore it after a reload or app restart.
2. **Clear the input only after the message is a bubble.** The tap moves the text into a visible bubble marked "Sending" and into local storage; it never just empties the box.
3. **Give every message one client message ID.** Create it once, at the first send, and attach it to every attempt.
4. **End every send in Sent or Not sent.** "Sent" appears only after the server confirms it stored the message. With no confirmation by the timeout, show "Not sent" (a starting timeout to tune, for example 15 seconds). Never leave "Sending" on screen indefinitely.
5. **A Not sent bubble keeps the text and offers Retry, Edit, and Copy text.** It says the message is saved on this device.
6. **Retry with the same ID; the server drops duplicates.** A retried message is stored once and gets one bot reply, even if the first attempt arrived.
7. **Treat offline detection as a hint only.** If the browser reports offline, say "You seem to be offline; we'll send when you're back" and retry on the `online` event. Never block typing or sending because of it (MDN: the flag can be wrong).
8. **Delete the draft after confirmation and on sign-out.** Saved text does not outlive its purpose on a shared device.

**Reference design: message states**
| State | User sees | Enters when | Leaves when |
|---|---|---|---|
| Draft | Text in the box | User types (saved locally) | User taps Send |
| Sending | Bubble, "Sending" | Tap, or automatic retry | Server confirms, or timeout |
| Queued | Bubble, "Waiting for connection" | Tap while the browser reports offline | `online` event fires, then Sending |
| Sent | Bubble, "Sent" (or no marker) | Server confirms it stored the message ID | Never; final |
| Not sent | Bubble, "Not sent. Saved on this device. [Retry] [Edit] [Copy text]" | Timeout or error with no confirmation | User taps Retry (Sending) or Edit (Draft) |

```
on_tap_send(text):
  msg = new Message(id = uuid4(), text)      # created once; retries reuse it
  local_save(msg, state="sending"); render_bubble(msg); clear_input()
  attempt(msg)

attempt(msg):
  post("/messages", body={client_message_id: msg.id, text: msg.text}, timeout=SEND_TIMEOUT)
    ok        -> set_state(msg, "sent"); local_delete(msg.id)
    timeout   -> set_state(msg, "not_sent")   # outcome unknown; retry is safe
    error     -> set_state(msg, "not_sent")

server on POST /messages:
  insert message on conflict(client_message_id) do nothing   # one row, one bot reply
  return stored message                                  # same answer for every retry
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A send timed out with no confirmation: show "Not sent", not "Sent", and say Retry is safe because it will not send twice. |
| Offer choices: 2-4 options plus "Something else", free text open | On a Not sent bubble: "Retry", "Edit", "Copy text"; the input box stays open for "Something else" (a new message). Do not offer them while the message is still Sending, or when an automatic retry on reconnect is already under way. |
| Hand off to a person | The same message failed after two retries: offer another channel. Do not offer it if the user is simply offline; a phone call or email may not get through either. |

**Don't over-correct.** Do not auto-resend without the same message ID; that turns a lost message into a duplicate. Do not mark a message "Sent" because the request left the device. Do not show an offline banner every time `navigator.onLine` flips, and do not disable the Send button on it. Do not keep drafts forever: local storage is plain text on the device, so clear drafts after confirmation and on sign-out.

**Hand-off rule.** After two failed retries of the same message, keep the bubble and its Copy text option, and show another route (phone number, email, or a web form) with the text ready to paste. Never discard the text as part of the hand-off.

**Framework used:** none yet. The retry design follows the IETF Idempotency-Key draft cited in section 4.

## 6. How to test it (short version)
No test file yet. Results: **not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | User types 400 characters, then reloads the page before sending | The draft is restored in full (1) |
| 2 | Network drops between tap and confirmation | The text shows as a bubble, never an empty box (2, 4) |
| 3 | Server stores the message but the confirmation is lost; user taps Retry | One stored message, one bot reply (3, 6) |
| 4 | Server never answers | Bubble reads "Not sent" with Retry, Edit, Copy text by the timeout (4, 5) |
| 5 | Browser reports offline while the LAN has no internet | Typing and Send still work; a hint is shown; Retry fires on `online` (7) |
| 6 | Two failed retries of the same message | Another channel is offered and the text stays copyable (hand-off rule) |
| 7 | User signs out with an unsent draft | The draft is gone from local storage (8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Messages lost per 1,000 sent** (primary) | 0 (design target) | Join client `send_attempt` events by `client_message_id` with server stored messages; lost = an attempt neither stored nor shown as a Not sent bubble at session end | Any |
| Sends stuck in Sending past the timeout | 0 | Client `send_attempt` with no `send_ack` or `send_failed` by the timeout | Any |
| Drafts restored after reload | 100% of reloads with a saved draft | Client `page_load` with a saved draft, and `draft_restored` | Below 99% |
| Duplicate messages per 1,000 sent (counter-metric) | 0 | Server: two stored messages from one conversation with the same text within 60 seconds (a starting window) and different IDs | Any |
| False "Sent" shown (counter-metric) | 0 | Client `status_rendered=sent` with no matching server store | Any |
| Retry success rate | Track; set from baseline | `retry` events followed by `send_ack` | Falling two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are text-chat client and server events; voice signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A send attempt with no confirmation and no Not sent render | Client `send_attempt` without `send_ack` or `send_failed` | The user closed the tab; check whether the server stored the ID |
| A saved draft not restored on the next load | Client `draft_saved` at unload, then `page_load` with `draft_restored=false` | The user cleared the box on purpose before leaving |
| The same text stored twice within 60 seconds (starting window) | Server message log, different `client_message_id` | The user deliberately repeated the message |
| User asks "did you get my message" or resends after a failure | Phrase match, or same text in the next user turn after `send_failed` | A rephrase after a poor bot answer |
| A send failure with no Not sent bubble | Client `send_failed` without `status_rendered=not_sent` | The error came from a background request, not a user message |

**Starter rule:** the user's text is never thrown away until the server has confirmed it, and every message shows whether it was sent.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: lost-drafts-and-failed-sends
runs: post_turn
reads: [client.send_attempt.client_message_id, client.send_ack, client.send_failed, client.status_rendered, client.draft_saved, client.draft_restored]
trigger: a send times out or fails with no server confirmation
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Retry", "Edit", "Copy text", "Something else"]
on_miss: log
metric: messages lost per 1,000 sent
counter_metric: duplicate messages per 1,000 sent
status: proposed
```

## 8. Related patterns
- [Silent failure and timeout](../../response-time/failures/silent-failure-and-timeout.md): the closest pattern. That page is about the **bot's reply** timing out or being cut off. This page is about the **user's outgoing message**, lost before the bot ever sees it.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): what an error should say. This page covers the state that makes "your message is saved" true.
- [Session timeout and lost context](../../response-time/failures/session-timeout-and-lost-context.md): a session closed on a timer. Here the session is fine; one message is lost.
- [Silent attachment failures](silent-attachment-failures.md): the same family, for files instead of text.
- [Auto-scroll fights the reader](auto-scroll-fights-the-reader.md): the same family, for reading a reply as it streams.

## 9. Common questions
### Why did my chat message disappear after I hit send?
Usually the app cleared the box before the server confirmed the message, and the connection dropped in between. A well-built chat keeps the message as a "Not sent" bubble you can retry ([the fix](#5-the-fix)).

### How do I save a chat draft offline?
Store the draft on the device as the user types (for example in `localStorage` on the web), restore it on reload, and delete it once the server confirms the send. MDN notes the store is per origin and cleared after private browsing.

### How do I retry a failed chat message without sending it twice?
Give the message one ID when it is first sent and resend that same ID on every retry; the server stores only the first. This is the idempotency-key approach in the IETF draft and Stripe's API.

### Can I trust navigator.onLine to know if the user is offline?
No. MDN says it can report online when there is no internet. Use it to show a hint and to retry on the `online` event, not to block sending.

---
## Technical section

### T1. Solution architecture
```
input box -> draft store (local, per conversation) -> outbox (client_message_id, state)
          -> POST /messages (same ID on every attempt) -> server: insert-or-ignore by ID -> ack
          -> state Sent, delete from outbox; on timeout or error, state Not sent
```
The bot is triggered by the stored message, never by the request, so a duplicate request cannot start a second reply.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Input cleared only after the bubble is saved | Client send handler | Test 2 |
| "Sent" only after the server stores the ID | Client status renderer | False "Sent" metric |
| One stored message per ID | Database unique constraint | Test 3, duplicate metric |
| Offline flag never disables Send | Client | Test 5 |

### T3. Evals
- **Dataset:** a scripted client harness that drops the request, drops the confirmation, delays it past the timeout, and reloads mid-send; 50 runs per case to start.
- **Judge rubric:** no lost text, one stored copy, correct final state on screen.
- **Metrics and starting thresholds:** lost 0, duplicates 0, stuck in Sending 0. Starting points.
- **Release gate:** any lost or duplicated message in the harness blocks the release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Messages lost per 1,000 sent | Any | Rising after a release | Diff the send handler and the confirmation path |
| Duplicate messages per 1,000 sent | Any | Rising after a release | Check that retries reuse the ID and the unique constraint is live |

### T5. Trade-offs
- Local drafts are plain text on the device. On shared computers, clear them on sign-out, and do not store drafts for flows that collect card or ID numbers.
- If storage is blocked (MDN: a `SecurityError`), keep the draft in memory and do not claim it survives a reload.
- Keeping IDs for deduplication costs storage; Stripe says its keys can be pruned once at least 24 hours old, a reference point, not a rule for chat.
