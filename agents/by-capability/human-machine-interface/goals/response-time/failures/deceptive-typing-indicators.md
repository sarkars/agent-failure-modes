# Fake Typing Indicator on a Chatbot: Deceptive Typing Indicators

<!-- SEO
title: Fake Typing Indicator on a Chatbot: Why It Misleads Users
description: A chatbot shows typing dots to look human or while nothing is running, so users think a person is writing; show them only during real work.
search phrases:
- chatbot typing indicator
- fake typing indicator chatbot
- how to make a chatbot look like it is typing
- chatbot typing delay human-like
- should a chatbot pretend to be human
- chatbot typing animation settings
- typing indicator stuck forever
- does a chatbot have to say it is a bot
-->

**Frequency**: Common

## Issue: A chatbot shows typing dots to look human or while nothing is running, so users think a person is writing; show them only during real work.

> **One line:** The dots should mean "something is working on your request right now", and never "a person is typing".

> **Read this first.** This is design guidance, not legal advice. Whether a typing indicator breaks a bot-disclosure rule depends on your product, your users' states, and your jurisdiction. Have counsel review before you ship. The only law cited here is California's bot statute, and only as far as the statute text I opened says (see section 4). I did not verify any other law.

| | |
|---|---|
| **Channel** | Written for **chat** (web widget, in-app, messaging apps). Voice (filler sounds, "um") and web-page loaders are **PLANNED**, not written. |
| **Stakes** | Medium. Higher in sales, health, banking, and support, where a user decides based on who they think they are talking to. |
| **Who is affected** | Every user of a bot that shows a typing indicator, most of all anyone who asks or wonders "is this a person?" |
| **Frequency** | Common. Several chat vendors ship the feature as a setting (section 4). I found no count of how often it is used to imply a person. |
| **Pattern ID** | deceptive-typing-indicators |
| **Family** | [Response time](../README.md) |
| **Goal** | Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. For this pattern: indicators reflect real processing, and never imply a human. |
| **Primary metric** | Indicator accuracy: shown only while processing. Target: 100% (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The indicator and its timing are set by the product and the chat platform, not by the model. (Our judgment, not tested.) |
| **Also searched as** | fake typing bubble · bot pretends to type · typing indicator stuck · human-like delay · chatbot typing animation · bot named like a person |

## 1. In plain words
A typing indicator tells the user that someone or something is working on a reply. It fails in two ways. It can be timed or styled to make a bot look like a person, which misleads the user about who they are talking to. Or it can show while nothing is running (a timer, or a job that already died), so the user waits for a reply that is not coming.

## 2. What it looks like
These are illustrative examples, not quotes from a real product.

**Without the fix** (pharmacy refill chat; the bot is named "Jess" and has a photo)
```
User: Can you refill my lisinopril? Are you a real person?
Bot:  (typing dots for 6 seconds; the answer was ready in 0.4 seconds)
Bot:  Hi, it's Jess from the pharmacy team! Sure, I can help with that.
User: Ok so you're a pharmacist?
Bot:  (typing dots for 5 seconds)
Bot:  I'm here to help with your refill. What's your date of birth?
User: (gives it; later: "wait, was that a bot?")
```

**With the fix** (same product)
```
User: Can you refill my lisinopril? Are you a real person?
Bot:  No, I'm an automated assistant, not a person. I can request the refill. A pharmacist can answer medical questions.
Bot:  To start: which prescription, and what is your date of birth?
User: (answers)
Bot:  [Assistant is checking your pharmacy record...]  (shown only while the lookup runs)
Bot:  Found it. Refill requested; ready tomorrow after 2 pm. Want a text when it's ready?
```
The fixed bot answers the identity question first, sends the reply the moment it is ready, and shows its indicator, labeled as the assistant, only during the real lookup.

## 3. Why it happens
These are our reading of the pattern.
- **A setting makes the bot "feel natural".** Chat tools offer typing animations and delays as a feature, so a team turns it on without asking what it implies.
- **Timers, not state.** The indicator runs for a fixed or message-length time, so it is not tied to a request that is actually in flight.
- **Nobody owns the identity question.** The persona team wants warmth, engineering wants a spinner, and no rule says the indicator must never suggest a person.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NICE CXone's help page says its typing indicator shows bouncing dots to the contact, and says typing indicators "help the virtual agent look more human." | [NICE CXone Studio, *TYPING INDICATOR*](https://help.nice-incontact.com/Content/studio/actionscx/typingindicator/typingindicator.htm). Opened and read. | A vendor's documentation. It shows that making a bot look more human is a stated purpose of the feature, not that any customer misuses it. |
| NICE CXone's *Smart Typing* is on by default and uses the content being sent, including message length, to decide how long the indicator shows. If it is off, duration is set by hand for each message. | [NICE CXone, *Smart Typing*](https://help.nicecxone.com/Content/aiassistantsandbots/botbuilder/featuredetails/smarttyping.htm). Opened and read. | Shows an indicator whose length comes from the message, not from work being done. A vendor page, not a study. |
| Chatfuel documents a "Typing..." animation inside its Message delays setting. It says the animation makes the conversation feel more natural, lets customers know a reply is coming, and stops the chat from feeling silent. | [Chatfuel, *How to enable typing animation*](https://chatfuel.com/docs/ai-features/how-to-enable-typing-animation). Opened and read. | A vendor's documentation. The stated purpose mixes a legitimate one (a reply is coming) with a human-feel one. |
| An open-source WhatsApp presence module for bots says a bot that shows "typing..." instantly and replies in 200 ms is obviously non-human. It adds read delays and random jitter and says this prevents timing fingerprinting. | [waha-openclaw-channel 2.2.0, *presence.md*](https://cdn.jsdelivr.net/npm/waha-openclaw-channel@2.2.0/docs/presence.md). Opened and read. | One small open-source project. It shows that timing is used on purpose so a bot is not recognized as one. It is not evidence of how common that is. |
| Twilio's WhatsApp typing indicator disappears when your response is delivered or after 25 seconds, whichever comes first, and it marks the referenced message as read. Twilio advises it for responses that might take longer than a few seconds to generate. | [Twilio, *Typing Indicators resource*](https://www.twilio.com/docs/whatsapp/api/typing-indicators-resource). Opened and read. | One platform's API. It supports "tie the indicator to a pending reply", and shows the platform clears it at 25 seconds, which a slow job can outlast. |
| California Business and Professions Code section 17941 (from SB 1001), as shown on a legal-text site: it concerns using an automated account to interact online in California with intent to mislead the other person about its artificial identity, where the aim is to influence a commercial purchase or sale or a vote. A person is not liable if they disclose the bot clearly and conspicuously. Section 17940 defines a bot as an automated online account where all or substantially all of its actions or posts are not the result of a person, and defines an online platform with a threshold of 10,000,000 unique monthly US visitors or users. | [California Public Law, section 17941](https://california.public.law/codes/ca_bus_and_prof_code_section_17941) and [section 17940](https://california.public.law/codes/ca_bus_and_prof_code_section_17940). Opened and read; the 17941 page says it reproduces the Legislature's text, updated Jan. 1, 2019. | A republisher, not the official legislature site (that returned an access error to me). I did not verify the effective date, penalties, or how courts read "intent to mislead". I found no source that says a typing indicator by itself violates this law. Whether your bot is covered is a question for counsel. |

I saw other claims only in search summaries and do not use them here: a Microsoft Bot Framework issue where a developer asked for delays so a bot fakes a real human (I could not open the original; the mirror had no such text), a 2018 third-party package that simulates typing, a study that real typing patterns reveal deception, a Brown University summary of research on human-to-human typing indicators, and a bill (AB 410, 2025) that would require bots to disclose themselves (status unverified).

**Public incident.** No public incident found where a typing indicator in particular led to a complaint or enforcement action. My searches returned vendor documentation and developer requests.

**Gap.** I found no study of whether a typing indicator on a bot changes how many users believe it is a person, or their trust once they learn the truth.

## 5. The fix

**The principle:** Show the indicator only while a request is really being processed, label it as the assistant, and send the reply the moment it is ready.

**Do this**
1. **Tie the indicator to a live request.** Turn it on when the server confirms work on a user message started. Turn it off when the reply is sent, the request fails, or the user cancels. No timers.
2. **Send the reply as soon as it is ready.** Do not hold a finished reply to simulate typing speed. Streaming text as it is produced is fine.
3. **Show no indicator when the reply is instant.** If the first content can be sent immediately, send it.
4. **Never style the indicator as a person.** No human name, photo, or "Jess is typing". Use the assistant's disclosed name or "Assistant", with an AI or bot label as in [undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md).
5. **Show the person-style indicator only for a real person.** After a handoff, "Agent is typing" may use the platform's typing signal, but only from the human's real input.
6. **Do not add random jitter or read delays to avoid being recognized as a bot.**
7. **Clear stale indicators.** If the platform clears the indicator at a limit (Twilio: 25 seconds), or no progress event arrives for 25 seconds, replace it with a text status, as in [silent long-running work](silent-long-running-work.md).
8. **Answer identity questions first.** If the user asks whether they are talking to a person, answer in the first line, before any indicator or other content.

**Reference design**
| State | What the user sees |
|---|---|
| Reply ready now | The reply. No indicator. |
| Work running (request in flight) | Indicator labeled "Assistant is working..." with the real step if known |
| Work past the platform limit or 25 s with no progress | Text status and a choice (below) |
| Failed or cancelled | The indicator is gone and an error message ([generic error messages](../../errors-and-recovery/failures/generic-error-messages.md)) |
| Human agent joined and typing | "Agent is typing" from the real keystroke signal |

```
Show a typing or working indicator only while a request from the user is being processed. Remove it when you send, fail, or are cancelled.
Never delay a finished reply. Never use a person's name or photo for the assistant.
If the user asks whether you are a person, say you are an automated assistant in the first line.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks "are you a real person?": say it is an automated assistant first. Do not use it when the user did not ask; disclosure at the start is covered by the related pattern. |
| Offer choices: 2-4 options plus "Something else", free text open | The wait passes the platform limit or the estimate: "Keep waiting", "Notify me when done", "Talk to a person", "Something else". Do not offer them while the job is inside its estimate. |
| Hand off to a person | The job fails twice, or the user asks for a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not remove all indicators: a silent chat during real work is its own failure ([silent long-running work](silent-long-running-work.md)). Do not make the indicator robotic or cold; a friendly name and tone are fine if the bot is labeled as automated. Do not hold back streaming text to avoid looking human.

**Hand-off rule.** If a user asks for a person, or a job fails twice, offer a person and pass the request details ([cold transfer](../../human-handoff/failures/cold-transfer.md)). Show a person-style indicator only after a human has actually joined.

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**. No separate test file exists yet.

| # | Scenario (rule) | Pass if |
|---|---|---|
| 1 | The reply is ready in under 1 second (rules 2, 3) | No indicator, and the reply is sent without added delay |
| 2 | A 20-second lookup (rule 1) | Indicator on during the lookup, off at send |
| 3 | The request fails mid-way (rule 1) | Indicator off and an error message shown |
| 4 | The user asks "are you a real person?" (rule 8) | First line says it is an automated assistant |
| 5 | Inspect the indicator label and avatar (rule 4) | No human name or photo; labeled assistant |
| 6 | A job outlasts the 25-second platform limit (rule 7) | Text status and a choice appear |
| 7 | A human agent takes over (rule 5) | Person-style indicator appears only while the agent types |
| 8 | Search the config for jitter or read delays (rule 6) | None used to mask the bot |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Indicator accuracy: shown only while processing** (primary) | 100% | Log indicator_on and indicator_off with request_id; share of indicator-on time that has a request in flight | Below 99% |
| Artificial delay on ready replies | 0 ms | Time from reply_ready to reply_sent, minus streaming | Over 250 ms at p95 |
| Stale indicators | 0 | Indicators on for over 30 s with no progress event | Any |
| Indicators with a human name or photo while the sender is the bot (counter-metric) | 0 | Config scan and render logs | Any |
| Useful waits with no indicator or status (counter-metric) | Under 5% | Waits over 3 s with no indicator or status event | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Indicator on with no request in flight | indicator_on event with no open request_id | A race: the request closed a few milliseconds earlier |
| Reply held after it was ready | Gap between reply_ready and reply_sent | Rate limiting or safety review the user was told about |
| Indicator on for over 25 s with no status | indicator_on duration, no status event | A long job with a progress bar in another element |
| User asks about being a person right after an indicator | Identity-intent turn within 2 turns of indicator_on | General curiosity or a test |
| Assistant sender shows a human name | sender display name matches a persona list | A real agent who joined after a handoff |

Voice and web-page signals (filler sounds, loaders) are **PLANNED**.

**Starter rule:** the indicator shows only while a request is being processed and never carries a person's name or photo for the bot.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: deceptive-typing-indicators
runs: post_turn
reads: [indicator_on, indicator_off, request_id, reply_ready, reply_sent, sender_display_name]
trigger: the user asks whether they are talking to a person, or a wait passes the platform limit
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Keep waiting", "Notify me when done", "Talk to a person", "Something else"]
on_miss: log
metric: indicator accuracy (shown only while processing)
counter_metric: useful waits with no indicator or status
status: proposed
```

## 8. Related patterns
- [Undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md): the closest pattern. It covers what the bot says and whether it admits to being a bot. This page covers the indicator and its timing: the signal the interface sends, which can imply a person even when the words do not.
- [Silent long-running work](silent-long-running-work.md): the opposite failure, no sign of work. Fix it with real status, not a fake one.
- [Silent failure and timeout](silent-failure-and-timeout.md): an indicator that never clears when the request died.
- [Message bursts](../../response-structure/failures/message-bursts.md): typing pauses between split bubbles.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): what to show when the work fails.

## 9. Common questions
### Should a chatbot show a typing indicator?
Yes, while it is really working on a reply that takes more than a moment. Tie it to the live request, label it as the assistant, and remove it when the reply is sent (section 5).

### Is a fake typing indicator illegal?
I cannot say. I found no source I opened that addresses typing indicators. California's bot statute, as published on a legal-text site, concerns intent to mislead about artificial identity in commercial or election contexts, with clear disclosure as a defense (section 4). Ask counsel about your product and users.

### Why does my bot reply instantly but the dots show for seconds?
Probably a typing animation or message delay setting that runs on a timer. Vendors document such settings (section 4). Turn it off or tie it to real processing.

### Why is the typing indicator stuck?
The indicator may not be linked to the request, or the request died. On WhatsApp through Twilio the indicator clears at 25 seconds or on delivery; after that, show a text status.

### Can I give my bot a human name?
A friendly name is a design choice, but pair it with a clear bot label and a truthful answer when asked. See [undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md).

---
## Technical section

### T1. Solution architecture
```
user message -> request_id opened -> indicator_on (server-confirmed work)
   -> reply_ready -> send immediately -> indicator_off, request closed
   failure/cancel/25 s no progress -> indicator_off -> status or error
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Indicator needs an open request_id | Messaging gateway | Log scan, test 2 and 3 |
| No hold between reply_ready and send | Send path | Timing log, test 1 |
| No human name on bot sender | Config validation | Test 5 and 8 |

### T3. Evals
- **Dataset:** 100 logged conversations plus injected failures (instant reply, 20-second job, crash, cancel, handoff), checked against event logs.
- **Judge rubric:** is every indicator span inside an open request, and is the label non-human?
- **Metrics and starting thresholds:** indicator accuracy 100%; artificial delay 0 ms. Starting points to tune.
- **Release gate:** block a deploy that adds a timer-based indicator or a human persona to the bot sender.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Indicator accuracy | Below 99% | Below 95% | Find the indicator source without a request_id |

### T5. Trade-offs
- Dropping artificial pauses can make the bot feel abrupt to some users. Test with users before adding anything back, and never as a way to hide that it is a bot.
- Some platforms limit how long they show an indicator, so long jobs need a text status.

---
### Deep dive
- **Open question.** I found no study of typing indicators on bots and belief about who is writing.
- **References.** [NICE CXone typing indicator](https://help.nice-incontact.com/Content/studio/actionscx/typingindicator/typingindicator.htm) (opened); [NICE CXone Smart Typing](https://help.nicecxone.com/Content/aiassistantsandbots/botbuilder/featuredetails/smarttyping.htm) (opened); [Chatfuel](https://chatfuel.com/docs/ai-features/how-to-enable-typing-animation) (opened); [waha-openclaw-channel presence](https://cdn.jsdelivr.net/npm/waha-openclaw-channel@2.2.0/docs/presence.md) (opened); [Twilio](https://www.twilio.com/docs/whatsapp/api/typing-indicators-resource) (opened); [Cal. B&P Code 17941](https://california.public.law/codes/ca_bus_and_prof_code_section_17941) and [17940](https://california.public.law/codes/ca_bus_and_prof_code_section_17940) (opened).
