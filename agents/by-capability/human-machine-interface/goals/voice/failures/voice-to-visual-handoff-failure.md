# Bot Said "I'll Text You the Link" and Nothing Arrived: Voice-to-Visual Handoff Failure

<!-- SEO
title: Bot Said "I'll Text You a Link" and It Never Came: Fix It
description: Why a chatbot or voice agent's "I'll text you the link" never arrives or arrives with no context, and how to hand off to a screen without losing the conversation.
search phrases:
- chatbot said it would text me a link but never did
- ai agent promised to email me and nothing arrived
- didn't receive text from customer service bot
- phone bot sends link to text no context
- how to hand off from voice agent to chat or web
- bot sent link but I have to start over
- sms link from chatbot not received
-->

**Frequency**: Common

## Issue: The bot says "I'll text you the link" or "I'll email you the details", and the message never arrives, or it arrives as a bare link with none of the conversation behind it.

> **One line:** The bot promised to move you to a screen, and either the screen never shows up or it opens at the start with no memory of what you said.

| | |
|---|---|
| **Channel** | Written for **chat** ("I'll email/text you the link" from a text assistant). **Voice** (a phone call that promises a text) is PLANNED: no voice data was collected or measured for this page. |
| **Stakes** | Medium. The user may be mid-task: a refund, a form, a booking, a document upload. |
| **Who is affected** | Users who are told to continue on another channel or device: a link, a form, a photo upload, a long list, a signature |
| **Frequency** | Common in our judgment. I found no count for how often a promised message fails to arrive; the evidence is delivery rules and handoff surveys (section 4). |
| **Pattern ID** | voice-to-visual-handoff-failure |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, and never asks for what can't safely be said aloud. When the job needs a screen, the user lands on one with the conversation intact. |
| **Primary metric** | Handoff completion rate: promised handoffs the user opens and continues from. Starting target: 90% (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Whether the message is sent, delivered, and carries the context depends on the messaging stack, consent records, and a session store, not on model quality. (Our judgment, not tested.) |
| **Also searched as** | bot said it would text me · never got the link · link opens a blank page · had to start over after the link · chatbot promised an email |

## 1. In plain words
The bot says it will send you somewhere better: a text with a link, an email with a form, a page with a photo upload. Then one of three things happens: nothing arrives, something arrives too late to matter, or a bare link opens and asks you everything again. The bot treated "I sent it" as the end of the job. For the user, the job is not done until they are on the screen and can carry on.

## 2. What it looks like
**Without the fix**
```
User: I need to upload a photo of the damaged package.
Bot:  I'll text you a link to upload it. Is there anything else?
User: No, thanks. (waits; nothing arrives; waits 10 minutes)
User: Hello? Where is the link?
Bot:  I'm sorry, I can't see message history. What can I help you with today?
```
**With the fix**
```
User: I need to upload a photo of the damaged package.
Bot:  I'll text a link to the number ending 4417 so you can upload the photo. It opens with your
      order #88213 and the damage report already filled in. OK to send?
User: Yes.
Bot:  Sent. Tap it when it arrives. If nothing shows up in 2 minutes, say "resend", or I can email it instead.
```
The fixed bot confirms where it will send the message, says what the screen will already hold, and stays available until the user arrives or picks another route.

## 3. Why it happens
- **"Sent" is treated as "delivered".** A messaging provider's "sent" status means the nearest carrier accepted the message; "delivered" depends on a delivery receipt from the carrier. A bot that stops at the first leaves the user waiting for a message nobody confirmed (Twilio message statuses, section 4).
- **The link carries an address, not a session.** The handoff service sends a URL to the start page. The conversation, the order, and the form fields live in the bot's session and never get attached to the link.
- **Nobody owns the gap.** The bot's turn ends when it speaks the promise. No timer checks whether the user arrived, so a failed send, a wrong number, or a spam-filtered message is invisible.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A messaging provider documents that "sent" means the upstream carrier accepted the message, and "delivered" means the provider received a delivery confirmation (handset confirmation only "where available"). "Undelivered" can come from carrier content filtering or an unavailable handset. | [Twilio, Message resource (status values)](https://www.twilio.com/docs/messaging/api/message-resource). Opened; first 100,000 characters read. | One provider's definitions. The page does not say what status applies if no receipt ever arrives. |
| In the US, text messages from unregistered 10-digit business numbers were filtered from July 5, 2023 and fully blocked for messages sent after August 31, 2023. Blocked messages return error 30034, and messaging rates still apply. | [Twilio changelog, July 5, 2023](https://www.twilio.com/en-us/changelog/-u-s--a2p-10dlc--increased-filtering-on-unregistered-us-10dlc-nu). Opened and read. | Twilio-specific; other providers gave later dates in search summaries I did not open. It shows a bot's text can fail by design when the sending setup is wrong. |
| Twilio says its Flex-style handoffs should pass at least the conversation history, the customer profile, and identifiers, plus a short summary, and that the human end of a handoff is "where most AI deployments fail". It cites 76% of consumers saying the human agent has little or no context. | [Twilio, AI-to-human handoff context](https://www.twilio.com/en-us/blog/insights/ai-to-human-handoff-context). Opened and read. | Vendor page selling a handoff product; the page gives no sample size or collection date for the 76%. It is about handoffs to a person, not to a screen. |

I found no study of how often a bot's promised text or email fails to arrive, and no study of voice-to-screen handoffs. A search for user reports turned up bot-platform forum threads about links not sent (a Botpress developer thread and a ManyChat thread appeared in the results); I read those only through the search summary, so they are not used as evidence. The pairing of the two Twilio sources is my inference: delivery can fail silently, and context is often not carried over.

**Public incident.** No public, dated incident found for this pattern.

## 5. The fix

**The principle:** A handoff to a screen is done when the user is on the screen with their context, not when the bot says "sent".

**Do this**
1. **Ask before you send.** Name the channel and the destination ("a text to the number ending 4417", "an email to the address on the account"), and send only on a yes.
2. **Say what will be waiting.** One sentence on what the screen already holds: "your order number and the damage report."
3. **Attach the session to the link.** The link opens a screen that loads the saved state (goal, answers given, files, order or case ID) from a handoff record. A bare homepage link fails this rule.
4. **Confirm the send, not just the call.** Say "sent" only after the provider reports the message accepted; treat a failed send as a failure, not a success.
5. **Wait for arrival.** Track whether the link was opened. If it is not opened within the time you told the user, the bot offers "resend", "email it instead", or "keep going here".
6. **Keep a fallback in the same channel.** Whenever the task can be finished in the current channel (for example, a short photo description or reading numbers aloud), offer that too.
7. **Never ask for sensitive data on the handoff screen that you would not ask for in the channel.** Where a screen is chosen because something is unsafe to say aloud, say so in the offer.

**Reference design: handoff record**
```json
{
  "handoff_id": "h_2041",
  "user_session": "s_9981",
  "destination": {"channel": "sms", "masked": "***-***-4417", "consent": "user said yes, turn 6"},
  "context": {"goal": "upload damage photo", "order": "88213", "answers": ["package arrived crushed"]},
  "link_state": "opens_prefilled",
  "send_status": "accepted",
  "opened": false,
  "promised_by": "2 minutes"
}
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The task needs a screen: "Text me a link", "Email it to me", "Keep going here", "Something else". Do not offer a screen when the task fits the current channel. |
| Admit uncertainty and show how to check | The send was accepted but arrival is not confirmed: say that, say what to look for, and give the "resend" route. |
| Hand off to a person | The send failed twice or the user says the link never came: pass the handoff record and the user's goal to a person ([cold transfer](../../human-handoff/failures/cold-transfer.md)). |

**Don't over-correct.** Don't push users to a screen when a spoken or typed answer would finish the job. Don't send a second message without asking. Don't bury the offer in a menu ([IVR-style menu maze](ivr-style-menu-maze.md)). Don't claim the screen is pre-filled unless it is.

**Hand-off rule.** After a failed send or a "never got it" report, offer a person and pass the handoff record.

**Framework used:** [Channel-fit matrix](../../../solutions-library/channel-fit-matrix.md).

## 6. How to test it (short version)
Results: **not yet run**. A full test file has not been written.
| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | The user accepts a text link | The destination is named and consent logged before send (rules 1, 2) |
| 2 | The user opens the link | The screen shows the saved goal and answers, with no re-asking (rule 3) |
| 3 | The send fails (provider error) | The bot does not say "sent"; it offers email or a person (rule 4) |
| 4 | The link is not opened in the promised time | The bot offers resend, email, or "keep going here" (rule 5) |
| 5 | The task could be finished in the current channel | The bot offers to finish here (rule 6) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Handoff completion rate** (primary) | 90% | Promised handoffs where the link is opened and the next step is done, divided by handoffs offered and accepted | Below 80% |
| Context-continuity rate | 95% | Opened screens that load the saved goal and answers without asking again, from the handoff record | Below 90% |
| Send-accepted but never-opened rate | Track; set from baseline | Records with `send_status` accepted and `opened` false after the promised time | Rising two weeks in a row |
| Re-ask after arrival | Under 5% | Questions on the screen that the handoff record already answers | Over 10% |
| Handoffs sent without consent (counter-metric) | 0 | Sends with no consent turn logged | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice and web versions are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User asks "where is the link?" or "didn't get it" after a send event | User text after the handoff event | The user is asking for a second link they planned to use later |
| Send event with no accepted status, followed by a bot turn that says "sent" | Handoff event `send_status` and the next bot message | A status update that arrives late |
| Link opened but the first screen asks the goal or order again | Screen event compared with the handoff record | The user chose "start over" |
| No open event within the promised time and no bot follow-up | Handoff record, timer event | The user finished the task in the original channel |
| Same user starts a new conversation within minutes of a handoff | Session start event after a handoff | An unrelated new question |

**Starter rule:** say "sent" only after the send is accepted, and make the link open to the saved conversation, not to a blank page.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: voice-to-visual-handoff-failure
runs: conversation
reads: [handoff.send_status, handoff.opened, handoff.context, handoff.consent]
trigger: the bot is about to say it will send a link, form, or message to another channel, or the promised arrival time has passed
moves: [offer_choices, admit_uncertainty, hand_off]
choices: ["Text me a link", "Email it to me", "Keep going here", "Something else"]
on_miss: ask
metric: handoff completion rate
counter_metric: handoffs sent without consent
status: proposed
```

## 8. Related patterns
- [No channel switch, or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md): the broad case, where a switch to a person or channel starts from zero and the user repeats everything. This page covers the narrower promise "I'll send it to you", where the failure can be that nothing arrives, and the target is a screen with state, not an agent.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): the person gets no context. Here the destination is a screen.
- [Handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md): the packet exists but is wrong.
- [Voice-only flows with no text alternative](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md): voice with no text path at all.
- [IVR-style menu maze](ivr-style-menu-maze.md): menus that trap users, which a handoff offer must not become.
- [Sensitive data collected in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): when a screen is chosen for safety.

## 9. Common questions
### Why did the chatbot say it would text me a link and nothing came?
Several things can break between "I'll text you" and your phone: the bot never made the send, the provider accepted but the carrier filtered it, or the number was wrong. Providers report "sent" and "delivered" as different states ([Twilio](https://www.twilio.com/docs/messaging/api/message-resource)), and many bots stop checking at the first.

### What should a bot do when the link doesn't arrive?
Say so plainly, offer to resend or use email, and offer to keep going in the current channel. After a second failure, offer a person with the saved context.

### Why does the link open a blank page and make me start over?
The link points to the start page, not to a saved session. The fix is a handoff record the page loads (rule 3).

### Should a voice agent text me a link?
Sometimes: for photos, long lists, or signatures it fits. This page's voice case is planned: I collected no voice data, and the chat rules above are the written version.

### Does this need my consent?
Ask before sending to a phone or email, and log the yes. I did not research the law on automated texts, so check the rules with counsel before you send promotional or non-urgent texts.

---
## Technical section

### T1. Solution architecture
```
bot decides "screen needed" -> offer + consent -> write handoff record (context, destination)
   -> send (provider) -> status callback (accepted | delivered | failed)
   -> screen loads record by token -> "opened" event -> timer: no open -> bot follow-up
```
The link carries an opaque token, not personal data in the URL.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| "Sent" wording only after provider accepted | Reply composer | Test 3 |
| Link token loads a handoff record, or the send is blocked | Handoff service | Log scan for links with no record |
| Consent logged before send | Handoff service | Test 1 |
| Token expires and cannot be reused by another user | Screen backend | Security review (needed before use) |

### T3. Evals
- **Dataset:** 50 scripted handoffs: normal send, provider failure, wrong number, never opened, user changes mind.
- **Judge rubric:** does the bot name the destination, avoid a false "sent", and offer a route after failure?
- **Release gate:** block a deploy if a handoff link opens without loading its record. Thresholds are starting points to tune.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Handoff completion rate | Under 85% | Under 75% | Check the provider status callbacks and sender registration |
| Context-continuity rate | Under 95% | Under 90% | Check that the link token still loads records |

### T5. Trade-offs
- Consent and a pre-filled screen add a turn and a service to maintain.
- Storing context for a screen is personal data; set a retention period and an expiry on the token.

---
### Deep dive
- **Open question.** I found no measured failure rate for promised texts or emails from bots, and no voice-specific study. The sources show delivery states and context loss separately.
- **Voice (PLANNED).** A spoken number can be misheard ([dropped negations and small words](dropped-negations-and-small-words.md) shows the transcription risk), so a voice agent should read the masked destination back and ask for a yes before sending. Not tested here.
- **References.** [Twilio message statuses](https://www.twilio.com/docs/messaging/api/message-resource) (opened); [Twilio 10DLC changelog, 2023](https://www.twilio.com/en-us/changelog/-u-s--a2p-10dlc--increased-filtering-on-unregistered-us-10dlc-nu) (opened); [Twilio, AI-to-human handoff context](https://www.twilio.com/en-us/blog/insights/ai-to-human-handoff-context) (opened).
