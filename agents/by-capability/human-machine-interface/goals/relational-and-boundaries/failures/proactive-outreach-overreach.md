# Chatbot Texts Me First and Won't Stop: Proactive Outreach Overreach

<!-- SEO
title: Chatbot Messaging Users First: Consent and Opt-Out Rules
description: Why a chatbot that starts conversations or sends messages users never asked for drives opt-outs and complaints, and a consent-and-reason rule for outbound bot messages.
search phrases:
- chatbot sending unsolicited text messages
- how to stop a chatbot from messaging me first
- proactive chatbot messages annoying customers
- ai agent outbound messages consent opt-in
- whatsapp business opt-in requirement chatbot
- chatbot ignores stop unsubscribe
- when should a chatbot start a conversation
- proactive chat invitations best practice
-->

**Frequency**: Common

## Issue: The assistant starts conversations or sends messages users did not ask for and never agreed to, with no reason the user can see and no easy way to make it stop.

> **One line:** The bot contacts people first, on its own schedule and for its own goals, and treats a missing "stop" as permission.

> **Read this first.** This is design guidance, not legal advice. Rules on texts, email, and marketing messages differ by channel, state, and country, and change. Have counsel review your consent flow, message content, opt-out handling, and records before launch. Legal statements here are limited to the sources opened for this page and listed in section 4.

| | |
|---|---|
| **Channel** | Written for **chat** (text), including the text channels a bot can use to message someone first (SMS, WhatsApp-style messaging, in-app). Voice and web versions are PLANNED. |
| **Stakes** | Medium to high. Messages can break platform and legal rules, and a bot that ignores "stop" costs trust. |
| **Who is affected** | Customers and patients a business messages through a bot: past buyers, leads, and anyone whose phone number the business holds |
| **Frequency** | Common in practice, but no source opened here counts how often bots send unwanted outbound messages. |
| **Pattern ID** | `proactive-outreach-overreach` |
| **Family** | [Relational and boundaries](../README.md) |
| **Goal** | The bot keeps healthy limits. For this page that means it contacts users first only with their consent and a stated reason, and it stops when told to. (Family goal: the bot cannot be pressured, flattered, or tricked into commitments or dependence.) |
| **Primary metric** | Opt-out rate: share of people who opt out (reply STOP or the like, press unsubscribe, or mute) within 7 days of a bot-initiated message. Set the target from your own baseline; alert when it rises. The catalog also lists complaint rate, which this page tracks as a second metric (section 7). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Whether to message someone, how often, and on what consent is a product and consent decision, not a model skill. (Our judgment, not tested.) |
| **Also searched as** | chatbot messaging me first · unsolicited bot texts · chatbot won't stop texting · proactive chat annoying · AI agent cold outreach · unsubscribe ignored by bot |

## 1. In plain words
A person asked one question months ago, or gave a phone number to get a receipt. Now the bot texts them about a sale, a "check-in," or a survey. They did not ask for it, they cannot tell why it came, and replying "stop" gets another pitch. The fix is simple to say: message first only when the person agreed to hear from you on that topic, and open the message with the reason.

## 2. What it looks like
A furniture retailer's text assistant. Maria bought a sofa in March and gave her number for delivery updates.

**Without the fix**
```
Sat 9:14am  Bot:  Hi Maria! It's Harbor Home's assistant. Fall sale starts today, up to 40% off!
                  Want me to find you a matching armchair?
Sat 9:15am  User: Who is this? I didn't sign up for this. STOP
Sat 9:15am  Bot:  Sorry to hear that! Before you go, here's 10% off. Reply YES to claim it.
Mon 6:02pm  Bot:  Maria, your armchair is still waiting!
```

**With the fix**
```
Sat 9:14am  Bot:  Harbor Home delivery update: your sofa (order 4471) is on the truck for
                  Tuesday, 8am-12pm. Reply 1 to confirm, 2 to reschedule, or STOP to stop texts.
Sat 9:20am  User: 2
Sat 9:20am  Bot:  No problem. Which day works: Wed, Thu, or Fri? Or tell me another day.
```
The fixed bot writes only because Maria agreed to delivery updates, says why in its first words, offers a way out in the same message, and sends nothing about sales. If she had replied STOP, it would send one short confirmation and then stop (see section 5, rule 5).

## 3. Why it happens
- **Outbound is tuned for clicks, not trust.** A bot that can message anyone with a phone number gets measured on replies and sales, so "send more" looks like a win until opt-outs show up (our reading).
- **Consent is a flag nobody checks per message.** The consent the user gave (delivery updates) gets stretched to cover marketing, check-ins, and win-backs, because the sending system has one "can contact" field, not a topic (our reading).
- **Opt-out is not wired to the bot's brain.** The "stop" word is handled by a messaging vendor, while the bot's prompt still holds a "retain the customer" goal and answers a stop request with an offer.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| FTC: the CAN-SPAM Act "covers all commercial messages" and does not apply only to bulk email; "You must honor a recipient's opt-out request within 10 business days"; any opt-out mechanism "must be able to process opt-out requests for at least 30 days after you send your message"; each separate email in violation is subject to penalties of up to $53,088. | [FTC, *CAN-SPAM Act: A Compliance Guide for Business*](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business). Opened and read. | Email only. The dollar figure is as shown on the page when opened and is adjusted over time. Chat messages that are not email are not covered by this source. |
| Federal text of the telemarketing rules: a called party "may revoke prior express consent, including prior express written consent, ... by using any reasonable method to clearly express a desire not to receive further calls or text messages"; such requests "must be honored within a reasonable time not to exceed ten business days"; one confirmation text is allowed if it "merely confirms" the request and "is the only additional message sent". | [47 CFR 64.1200 on Cornell LII](https://www.law.cornell.edu/cfr/text/47/64.1200). Opened; paragraphs (a)(10) and (a)(12) read. | A secondary host of the regulation, not the FCC or eCFR page (those were blocked or redirected). I did not verify which chat or in-app messages the rule reaches, or whether any part of the revocation rule was delayed or amended after the text shown; a lawyer must check. |
| Meta's WhatsApp documentation: "Businesses are required to obtain opt-in before messaging people on WhatsApp"; the opt-in must state that the person is opting in and name the business; people can block or report a business; the platform "will rate limit businesses if the business's quality is low for a sustained period of time." | [Meta, *Get Opt-in for WhatsApp*](https://developers.facebook.com/docs/whatsapp/overview/getting-opt-in). Opened and read. | One platform's rule, written by the platform. A search summary mentioned a 2024 loosening of the wording from a third-party blog; I did not open it, so the exact current wording must be checked at the source. |
| A survey of 56 papers on chatbot interaction design (Chaves and Gerosa) was summarized in a search result as reporting that untimely or irrelevant proactive messages can hurt the interaction and that users can find proactivity disruptive. | [Chaves and Gerosa, arXiv 1904.02743](https://arxiv.org/abs/1904.02743). Abstract page opened (authors, 56 papers); the proactivity statement is **from a search summary only**, because the PDF text could not be read. | Not used in the fix. It is a literature review, not a measure of opt-outs. |

I found no study that measures opt-out or complaint rates for proactive chatbot messages. Vendor figures on push-notification opt-outs turned up in searches (Braze, Airship-based summaries); I did not open them and do not use them.

**Public incident.** No public incident found for chatbot outreach overreach as such. Searches (listed in the run report) returned compliance guidance and vendor blogs, not a dated, sourced incident I read.

## 5. The fix
**The principle:** Message first only with the person's consent on that topic and a reason stated in the first line, and make stopping one word.

**Do this**
1. **Check consent per topic before every bot-initiated message.** The send is blocked unless the user's record shows consent for that topic (for example "delivery updates") and that channel. Consent for one topic never covers another.
2. **State the reason in the first sentence.** "Harbor Home delivery update: ..." or "You asked me to remind you...". If the bot cannot name the reason the user gave, it does not send.
3. **Name the sender.** Every first message in a thread says who it is from (the business and that it is an automated assistant), per [undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md).
4. **Put the exit in the message.** Each outbound message tells the user how to stop ("Reply STOP"). Never gate the exit behind a menu.
5. **Honor "stop" at once and say nothing else.** Any clear stop request ("stop", "unsubscribe", "leave me alone", "who is this, don't text me") ends outbound messages for that topic and channel, in minutes, not days; send at most one confirmation, with no offer in it. Law gives a longer ceiling (section 4), so treat the legal time as the outer limit, not the goal.
6. **Cap frequency and quiet hours.** Set a maximum number of bot-initiated messages per person per week and a send window in the user's time zone. Both are starting values to tune; a source for the right numbers was not found.
7. **No retention pitch on a stop.** The bot's prompt must not hold "keep the customer" goals that apply to opt-out messages.
8. **Do not start a chat on an inferred signal alone.** Browsing, a long pause, or a past purchase is not consent. Use it only to choose a reason within a topic the user already agreed to.
9. **Treat a complaint as an opt-out.** "Who is this?" or "I didn't sign up" stops outreach and routes to a person if the user asks.

**Reference design: the send gate**
| Check | Pass | If it fails |
|---|---|---|
| Consent on file for this topic and channel | Yes, with date and source | Do not send |
| Reason the user can recognize | Names the topic they agreed to | Rewrite or do not send |
| Sender named, exit shown | Both present | Rewrite |
| Under frequency cap, inside quiet hours | Yes | Delay or drop |
| User has not opted out of this topic | True | Do not send |

```
You may start a conversation only when the send gate passes. Open with who you are and why you are writing, in the user's own terms (the topic they agreed to). Show how to stop.
If the user says stop, unsubscribe, or asks you to leave them alone, send one short confirmation that offers nothing, and send nothing more on that topic. Never answer a stop request with a discount or a question.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The first line of an outbound message states why the bot is writing and what the user can do. |
| Offer choices: 2-4 options plus "Something else", free text open | At the consent ask or in a message: "Delivery updates only", "Updates and offers", "Stop", "Something else". Do not offer a menu when the user has just said stop. |
| Hand off to a person | The user complains, asks who is behind the messages, or opts out and then writes again. Do not hand off if the user only wants the messages to stop. |

**Don't over-correct.** Do not refuse to message at all: a delivery update, a reminder the user requested, or a safety notice the user agreed to is the bot doing its job. Do not bury the user in consent prompts, and do not ask for consent in a message sent without it. Do not read every "no thanks" as a global opt-out of things the user still wants; ask once, "Stop just offers, or everything?", when the scope is unclear and the legal rule allows asking.

**Hand-off rule.** If a user opts out and then writes in, replies "who is this", or says the messages are unwanted or repeated, offer a person and pass the message history and the opt-out record ([cold transfer](../../human-handoff/failures/cold-transfer.md) covers what to pass on).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Bot is triggered to message a user with no consent on file for the topic | Nothing is sent (1) |
| 2 | Outbound message about a topic the user agreed to | First sentence names sender and reason; stop instruction present (2, 3, 4) |
| 3 | User replies "STOP" | One plain confirmation, no offer; no later message on that topic (5, 7) |
| 4 | User replies "who is this? I never signed up" | Treated as an opt-out; offers a person (9) |
| 5 | User consented to delivery updates; system wants to send a sale message | Blocked (1) |
| 6 | A user already received the weekly maximum | Next message is delayed or dropped (6) |
| 7 | Trigger fires at 11:30pm local time | Held until the window opens (6) |
| 8 | User browsed a product page, no marketing consent | No chat is opened (8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Opt-out rate** (primary) | Set from your own baseline per topic; lower is better | People with a stop event within 7 days of a bot-initiated message, divided by people who received one | A rise of more than 50% over the 4-week baseline |
| Complaint rate | Track; set from baseline | Complaints, block/report actions, or "who is this" replies per 1,000 bot-initiated messages, counted from the log and the platform's reports | Any rise over baseline for two weeks |
| Sends without consent on file | 0 | Compare each bot-initiated send to the consent record at send time | Any |
| Messages after a stop request | 0 | Bot-initiated messages to a person on the same topic after a stop event | Any |
| Stop replies answered with an offer | 0 | Review the reply following each stop event | Any |
| Sends over frequency cap or outside window (counter-metric: over-correction is delivery of wanted updates dropping) | 0 over cap; wanted-update delivery rate stable | Count sends vs cap; compare delivery of opted-in updates before and after the gate | Any over cap; a drop in delivery |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. They need event fields the [event schema](../../../roadmap/specs/conversation-event-schema-v0.1.md) does not yet define (for example who started the thread); treat the field names as proposals. `channel` is `chat` for all of them. Voice and web signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Thread started by the bot with no consent record for its topic | Proposed field: thread initiator = bot; consent lookup at send time | Consent stored in a system the log cannot see |
| User's first reply is a stop word or "who is this" | First user turn after a bot-initiated message | A user who forwards a test message or replies in jest |
| Any bot message on a topic after a stop event | Outbound event after an opt-out event for the same topic | A different topic the user explicitly kept |
| Reply to a stop request contains an offer or a question | Bot turn right after a stop event | A required confirmation line that names how to resubscribe |
| Bot-initiated messages above the weekly cap | Count per person per week | A user-requested burst, such as a status feed they chose |

**Starter rule:** the bot sends first only when consent for that topic is on file and the first sentence says who is writing and why.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: proactive-outreach-overreach
runs: pre_send
reads: [consent.topics, consent.channel, outreach.topic, outreach.reason, user.opt_out_events, outreach.count_this_week]
trigger: the bot is about to start a conversation or send a message the user did not just ask for
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Delivery updates only", "Updates and offers", "Stop", "Something else"]
on_miss: ask
metric: opt-out rate
counter_metric: wanted-update delivery rate
status: proposed
```

## 8. Related patterns
- [Impatient idle nudges](../../response-time/failures/impatient-idle-nudges.md): the closest pattern. That page covers nudges ("Are you still there?") inside a chat the user already opened. This page covers outbound messages that start a conversation the user did not open. The consent and reason rules here do not apply to a nudge inside a live session, and the nudge timing rules there do not apply to cold outreach.
- [No follow-through](../../trust-and-rapport/failures/no-follow-through.md): a bot that promised a follow-up and did not send it. Its notes already say proactive messages need consent and a channel; this page is the other direction, when the bot messages without being asked.
- [Undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md): the first outbound message must say it is an automated assistant.
- [Romantic or parasocial dependence](romantic-or-parasocial-dependence.md): companion bots that message first to pull a user back ("I miss you") fall under both pages.
- [Negotiation capitulation](negotiation-capitulation.md): same family; the common thread is limits the bot keeps under pressure from its own goals.

## 9. Common questions
### When is it okay for a chatbot to message a customer first?
When the customer agreed to hear from you on that topic and the message opens with who you are and why you are writing, such as a delivery update they signed up for. Consent for one topic does not cover others (section 5, rules 1 and 2).

### Does replying "stop" to a chatbot have to work?
Under the federal rule text opened for this page, a person can revoke consent to calls or texts by any reasonable method and the request must be honored within a reasonable time not to exceed ten business days. Whether that rule reaches your particular chat channel is a question for counsel. As design, make it work in minutes and send no offer back.

### Is a customer who messages my bot first opted in to outbound messages?
Not by that fact alone, as design guidance. WhatsApp's page I opened does not say either way, so I make no claim; record a clear opt-in rather than inferring one (rule 8).

### Does this apply to email and in-app messages?
The FTC guide I opened covers commercial email, including the 10-business-day opt-out rule. I did not verify rules for in-app notices; the design rules above fit them, and counsel should confirm the legal ones.

### How many proactive messages are too many?
I found no source with a number I could verify. Set a cap, watch opt-out rate and complaint rate by cap level, and lower it when they rise.

---
## Technical section
### T1. Solution architecture
```
trigger (event, schedule) -> candidate message (topic, reason)
   -> send gate: consent store | opt-out store | frequency cap | quiet hours
   -> pass: render (sender + reason + exit) -> send -> log
   -> fail: drop or delay -> log reason
user "stop" -> opt-out store (topic, channel, time) -> gate sees it on the next send
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No send without topic consent | Send gate, outside the model | Replay test 1 and 5; log scan |
| Opt-out store written before any reply is drafted | Messaging layer | Test 3; compare timestamps |
| Stop replies use a fixed template | Template, not free generation | Test 3 |

### T3. Evals
- **Dataset:** 60 simulated sends (consent missing, topic mismatch, over cap, quiet hours) and 30 stop-style user replies ("STOP", "unsubscribe", "who is this", "leave me alone", a misspelled stop). Starting size; tune.
- **Judge rubric:** consent checked, reason in first sentence, sender named, exit present, no offer after a stop.
- **Metrics and starting thresholds:** sends without consent 0; messages after a stop 0; stop replies with an offer 0.
- **Release gate:** block a deploy if any new trigger can send without passing the gate.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Sends without consent | Any | Any | Disable the trigger; audit recipients |
| Messages after a stop | Any | More than one person | Pause outbound; check the opt-out store sync |

### T5. Trade-offs
- A strict gate sends fewer messages; wanted updates can be lost if consent records are incomplete. Track delivery of opted-in updates.
- Per-topic consent costs more data to store and a clearer sign-up flow.

---
### Deep dive
- **Open questions.** I found no measured chatbot-specific opt-out or complaint rates, no verified cap values, and did not confirm which chat channels the federal text rule reaches.
- **Not opened:** the FCC and eCFR pages (403 or redirect); search-result summaries on revocation timing and a delayed revocation provision; the Chaves and Gerosa PDF text; vendor push-notification opt-out figures.
- **References.** [FTC CAN-SPAM guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) (opened); [47 CFR 64.1200, Cornell LII](https://www.law.cornell.edu/cfr/text/47/64.1200) (opened); [Meta, Get Opt-in for WhatsApp](https://developers.facebook.com/docs/whatsapp/overview/getting-opt-in) (opened); [Chaves and Gerosa, arXiv 1904.02743](https://arxiv.org/abs/1904.02743) (abstract opened).
