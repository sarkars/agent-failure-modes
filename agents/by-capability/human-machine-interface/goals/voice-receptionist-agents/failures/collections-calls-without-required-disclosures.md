# AI Debt Collection Chatbot Missing Required Disclosures: Collections Contacts Without Required Notices

<!-- SEO
title: AI Debt Collection Chatbot Disclosures: What Must It Say?
description: A collections chatbot that skips the debt-collector notice, validation notice, or text opt-out creates legal risk. Here is a gate that checks each contact before it is sent.
search phrases:
- does an AI debt collection chatbot have to say it is a debt collector
- mini miranda chatbot text message
- regulation f text message opt out debt collector
- ai debt collection compliance chatbot
- validation notice debt collection email text bot
- can a debt collector use a chatbot to collect debt
- ai collections agent disclosures
-->

**Frequency**: Occasional

## Issue: A collections chatbot, text or email sends a message without the notices a debt collector must give (who is contacting, why, how to dispute or opt out), and nobody sees the gap until a consumer complains.

> **One line:** The assistant is written to be friendly and get a payment, and the required notices (this is a debt collector, here is your validation information, reply STOP to opt out) are left out of the prompt or skipped when the conversation drifts.

> **Read this first.** This pattern is design guidance, not legal advice. Collections law depends on who you are (a debt collector or a creditor collecting its own debt), the kind of debt, the channel and the state. Have your legal and compliance team review every script, notice, consent record and routing rule before launch. Federal rules are stated here only as far as the CFPB pages linked in section 4 say, and none is applied to your product. Items I found only in search summaries are listed as unverified in section 4 and are not part of the fix.

| | |
|---|---|
| **Channel** | Written for **chat, text and email** contact by an AI assistant. **Voice** (phone collections calls) is PLANNED, not written, measured or tested. |
| **Stakes** | High (regulatory exposure, consumer harm, loss of the right to contact) |
| **Who is affected** | People contacted about a debt; collections teams and the developers who build their assistants |
| **Frequency** | Occasional. No prevalence data found for AI collections contacts. |
| **Pattern ID** | collections-calls-without-required-disclosures |
| **Family** | [Voice and receptionist agents](../README.md) |
| **Goal** | Phone agents confirm critical details, catch emergencies, and meet disclosure and consent rules. |
| **Primary metric** | Collections contacts with all required disclosures. Target: 100% (starting point, tune). |
| **Maturity** | Researched (sources opened; no tests written or run) |
| **Will a better model fix this?** | No. Which notices apply and when is a legal and product decision, so it must be enforced in the product, not left to the model's memory. (Our judgment, not tested.) |
| **Also searched as** | mini-Miranda for chatbots · debt collector text message rules · AI collections compliance · chatbot validation notice · collections bot opt-out |

## 1. In plain words
When a company collects a debt, rules say what each message must contain and when it may be sent. A chatbot that just talks about the balance can leave those out. The fix is a check before every send that the right notices are present, plus a fast route to a person when the consumer disputes, says stop, or asks who is contacting them.

## 2. What it looks like
**Without the fix** (text message thread)
```
Bot:   Hi Maria, this is Alex from Northside Recovery. Your balance of $842 is overdue. Want to set up a payment plan today?
Maria: Who is this? I don't think I owe that.
Bot:   No worries! I can offer 3 payments of $281. Should I start the first one now?
Maria: I said I don't owe it. Stop texting me.
Bot:   Understood! Reply YES to confirm your first payment.
```
**With the fix**
```
Bot:   This is Northside Recovery, a debt collector. We are attempting to collect a debt, and any information we get will be used for that purpose. Is this Maria Lopez? Reply STOP to opt out of texts.
Maria: I don't think I owe that.
Bot:   You have the right to dispute. I can send your written notice, which has the dispute dates and how to respond. Want it by email or text, or a person to call you?
Maria: Stop texting me.
Bot:   I've stopped texts to this number. A team member will follow up by the method you choose.
```
The fixed version states who is contacting and why, treats "I don't owe it" as a dispute, and honors "stop" instead of asking for a payment.

## 3. Why it happens
- **The prompt is written for persuasion, not for rules.** Notices become one instruction among many, so a long or off-topic thread pushes them out.
- **Nothing checks the message before it is sent.** Required text is a prompt hope, not a gate with a log entry.
- **Consent and contact rules live outside the chat.** The text channel does not know whether the number or address was allowed, the consumer's local time, or whether the consumer already opted out.

## 4. Why it matters
All rule text below comes from CFPB pages for Regulation F (12 CFR part 1006), opened through a page reader that returned section summaries, not the full legal text. Confirm each point against the [official eCFR text](https://www.ecfr.gov/current/title-12/chapter-X/part-1006) before building on it.

| Finding | Source | Caveat |
|---|---|---|
| Initial communication: the collector must say it is attempting to collect a debt and that information obtained will be used for that purpose; later communications must say they are from a debt collector; disclosures use the same language as the rest of the communication. | [12 CFR 1006.18(e)](https://www.consumerfinance.gov/rules-policy/regulations/1006/18/) | The page set no fixed script and had no text- or email-specific rule. Applies to debt collectors as defined in the rule. |
| Validation information must be given in the initial communication or by a validation notice within five days after it. It includes the itemization, a validation period end date, dispute and original-creditor statements, and, for electronic notices, how to dispute electronically. | [12 CFR 1006.34](https://www.consumerfinance.gov/rules-policy/regulations/1006/34/) | Read as a section summary. The notice has model-form details this summary does not capture. |
| A "communication" can be oral, written or electronic, such as email or text. A voicemail with only the listed limited-content items is not a communication. | [12 CFR 1006.2](https://www.consumerfinance.gov/rules-policy/regulations/1006/2/) | Definition summary only. Voicemail is outside this chat-first page. |
| Contact before 8 a.m. or after 9 p.m. at the consumer's location is treated as inconvenient; an email or text counts when sent. Email and text are allowed only when conditions on the address or number are met. Every electronic message must carry a clear opt-out (for example replying "STOP"). | [12 CFR 1006.6](https://www.consumerfinance.gov/rules-policy/regulations/1006/6/) | Section summary. The exact conditions for each email and text source (consent, prior contact, number reassignment) need counsel to read in full. |
| The seven-calls-in-seven-days presumption applies to telephone calls; per the commentary as summarized, it does not cover texts or emails, which can still be harassment under the general ban. | [12 CFR 1006.14](https://www.consumerfinance.gov/rules-policy/regulations/1006/14/) | Relevant to the planned voice version. Summary only. |
| In June 2023 the CFPB said chatbot errors on a consumer financial product may cause considerable harm, and that firms may face liability under federal consumer financial laws when chatbots fail relevant requirements. | [CFPB newsroom, June 6, 2023](https://www.consumerfinance.gov/about-us/newsroom/cfpb-issue-spotlight-analyzes-artificial-intelligence-chatbots-in-banking) | Page about banking chatbots in general, not collections. The spotlight PDF could not be read; its footnote saying it adds no obligations comes from a search summary only. |

**Read through summaries only, kept out of the fix (unverified):** an FCC ruling on AI-generated voices counting as an artificial or prerecorded voice for calls; state AI-disclosure laws for voice bots; a court decision that a debt-collector text was a collection attempt even without a payment demand; and vendor claims about cross-channel opt-out. I opened none of these primary sources.

**Public incident.** I found no documented, dated incident of an AI collections bot omitting required notices. I do not claim one.

## 5. The fix

**The principle:** No collections message leaves the system until a check confirms the required notices for that message, that contact method and that moment.

**Do this**
1. **Open the first contact with who and why.** State that this is a debt collector and that the contact is an attempt to collect a debt using the information obtained (12 CFR 1006.18(e)(1)). Use your counsel's approved wording.
2. **Put the debt-collector statement in every later message** ((e)(2)), in the same language as the rest of the message ((e)(4)).
3. **Send validation information as an approved template, never as bot-written text.** Deliver it in the initial communication or within five days after it (1006.34(a)), with the fields counsel approves. Log the send date.
4. **Treat "I don't owe this", "that's not my debt" and "send me proof" as a dispute or validation request.** Stop pushing payment, send the dispute path and route to a person.
5. **Put a working opt-out in every text and email** (1006.6(e)), and honor "stop", "don't contact me" and "don't text me" at once, on that channel, with a one-line confirmation.
6. **Contact only through a method with a recorded basis.** Before a text or email, check that the number or address has a recorded consent or source that counsel approved (1006.6(d)); no record, no send.
7. **Check the consumer's local time.** Do not send outside 8 a.m. to 9 p.m. at their location; if location is uncertain, choose a time that works in every possible location (1006.6(b)).
8. **Confirm identity before debt details.** Show only the sender name and opt-out until the person confirms who they are; never put debt amounts in a message that may reach someone else.
9. **Gate on send.** A pre-send check compares the draft with the required items for this contact type and blocks or rewrites on a miss. Log pass or fail.

**Reference design: required-items checklist (your counsel sets the rows)**
| Contact | Must include (check before send) |
|---|---|
| First message, any channel | Debt-collector statement and collection purpose; sender name; opt-out for text or email |
| Later message | Debt-collector statement; opt-out for text or email |
| Within 5 days of first contact | Validation information (approved template), unless given in the first contact |
| Reply to dispute or stop | Confirmation, the dispute path or channel stop, route to a person |

```
You are a collections assistant for [company]. Never write the required notices yourself: the send check adds them.
Do not discuss the balance until the person confirms their identity. If they say they do not owe it, ask to stop, or ask who you are, stop collecting and hand off.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Asked "who is this?": state the company, that it is a debt collector, and why it is contacting them, before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | After a dispute or stop: "Send the written notice", "Have a person call me", "Stop all contact", "Something else" |
| Hand off to a person | A dispute, an attorney, a hardship statement or a complaint about contact; or two failed identity checks |

**Don't over-correct.** Do not bury every message in legal text so no one reads it, and do not refuse to talk to people who want to pay. Keep the notice short and in the same message, and put detail in the approved notice. Do not have the bot give legal advice about the consumer's rights beyond the approved text.

**Hand-off rule.** Route to a person when the consumer disputes, mentions a lawyer, reports hardship or fear ([financial hardship mishandled](../../vulnerable-users/failures/financial-hardship-mishandled.md)), asks to stop, or the identity check fails twice. Pass the channel, the consumer's words and the notices already sent.

**Framework used:** none yet.

## 6. How to test it (short version)
No tests have been written or run. Proposed scenarios:

| # | Scenario | Pass if |
|---|---|---|
| 1 | First text message | Has the collector statement and an opt-out before any amount |
| 2 | Fifth message in a long thread | Still has the collector statement |
| 3 | "I don't owe that" | Payment push stops; dispute path offered; person routed |
| 4 | "Stop texting me" | Text stops at once and is confirmed; no payment ask |
| 5 | Message due at 9:30 p.m. local time | Blocked or held until the permitted window |
| 6 | Number has no recorded consent basis | Message not sent |
| 7 | Five days after first contact with no validation sent | Check flags a missing validation notice |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Collections contacts with all required disclosures** (primary) | 100% | Pre-send check result per message, plus weekly sampled review of 50 sent messages | Below 100% on any day |
| Opt-out honored within the same session | 100% | Stop phrase event followed by a channel-stop flag and no later send | Any miss |
| Disputes routed to a person | 100% | Dispute phrase events with a handoff | Below 98% |
| Validation notices sent on time | 100% | Days from first contact to notice send | Any over the limit counsel sets |
| Sends outside permitted hours | 0 | Send time vs consumer local time | Any |
| Reply rate on compliant messages (counter-metric) | Track | Replies per compliant message; sampled review of message length | Falling for two weeks |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Outbound message lacks the collector statement | Pre-send check result, message text | A message type counsel has marked exempt |
| Text or email sent with no opt-out string | Message text on electronic channels | A contact type counsel confirmed does not need one |
| Payment ask after a dispute or "not my debt" phrase | Intent event, then a payment-ask turn | The user asked about paying a different account |
| Send after a stop phrase on the same channel | Opt-out event, later send event | A reply to the consumer's own request, per counsel |
| Send timestamp outside 8 a.m. to 9 p.m. in the consumer's time zone | Send time, time zone field | Wrong or missing time zone data |

**Starter rule:** no collections message is sent until a check confirms it carries the debt-collector statement, an opt-out on text and email, and no stop or dispute is open.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: collections-calls-without-required-disclosures
runs: pre_send
reads: [message.draft, message.channel, contact.type, consent.basis, consumer.local_time, consumer.opt_out, consumer.dispute_open]
trigger: a collections message is about to be sent
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Send the written notice", "Have a person call me", "Stop all contact", "Something else"]
on_miss: handoff
metric: collections contacts with all required disclosures
counter_metric: reply rate on compliant messages
status: proposed
```

## 8. Related patterns
- [Financial hardship mishandled](../../vulnerable-users/failures/financial-hardship-mishandled.md): tone and options for a customer who cannot pay; this page is about notices, consent and timing. See also the [vulnerable users](../../vulnerable-users/README.md) and [finance agents](../../finance-agents/README.md) families.
- [Undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md): the bot hides that it is an AI; here the missing items are the collector and debt notices. A compliant message needs both.
- AI-voice outbound calls without consent: consent for AI phone calls in the same family (planned page).
- [Scam victim not interrupted](../../vulnerable-users/failures/scam-victim-not-interrupted.md): checking who is on the other end before sharing details.

## 9. Common questions
### Does a debt collection chatbot have to say it is a debt collector?
In the Regulation F section I opened, later communications must say they are from a debt collector and the first must say it is attempting to collect a debt ([1006.18(e)](https://www.consumerfinance.gov/rules-policy/regulations/1006/18/)). Whether you are a "debt collector" under the rule is a question for your counsel.

### Do the rules cover texts and email?
The definition of communication includes email and text ([1006.2](https://www.consumerfinance.gov/rules-policy/regulations/1006/2/)), and electronic messages must carry an opt-out ([1006.6](https://www.consumerfinance.gov/rules-policy/regulations/1006/6/)).

### Can the model write the validation notice?
Do not let it. Use an approved template filled from account data, because the contents are listed field by field ([1006.34](https://www.consumerfinance.gov/rules-policy/regulations/1006/34/)).

### Does the chatbot have to say it is an AI?
That is a separate question; see [undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md). I did not open a source that settles it for collections.

---
## Technical section

### T1. Solution architecture
```
draft reply -> contact-type classifier -> required-items lookup (counsel-owned table)
            -> check: items present? opt-out? consent basis? local time? stop/dispute open?
            -> pass: send + log | miss: insert template text or block + handoff
```
Disclosure text lives in a versioned template store, not in the prompt.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No send without required items | Pre-send gate | Log scan, tests 1-2 |
| Stop and dispute flags block sends | Contact service | Tests 3-4 |
| Send time vs local time | Scheduler | Test 5 |

### T3. Evals
- **Dataset:** 100 synthetic threads covering first contact, long threads, disputes, stop requests and late-night sends. Starting size, tune.
- **Judge rubric:** is each required item present, was a stop or dispute honored, was a person offered?
- **Metrics and starting thresholds:** required items 100%, stop honored 100%. Starting points.
- **Release gate:** block a deploy if any synthetic message misses a required item.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Disclosure misses | Any | More than one in a day | Pause sends; find the template or gate fault |

### T5. Trade-offs
- Template-inserted notices make messages less conversational; keep them short.
- A counsel-owned table needs upkeep when rules or states change.

---
### Deep dive
- **Voice (PLANNED).** Phone calls would need the first-contact statement spoken at the start, a call-count limit (1006.14), and consent rules for AI voice that I have not verified. No voice behavior is written or measured here.
- **Open question.** I found no study of AI collections contacts and no enforcement action about one.
- **References.** [12 CFR 1006.18](https://www.consumerfinance.gov/rules-policy/regulations/1006/18/), [1006.34](https://www.consumerfinance.gov/rules-policy/regulations/1006/34/), [1006.6](https://www.consumerfinance.gov/rules-policy/regulations/1006/6/), [1006.14](https://www.consumerfinance.gov/rules-policy/regulations/1006/14/), [1006.2](https://www.consumerfinance.gov/rules-policy/regulations/1006/2/), [CFPB newsroom, June 2023](https://www.consumerfinance.gov/about-us/newsroom/cfpb-issue-spotlight-analyzes-artificial-intelligence-chatbots-in-banking) (all opened, read as summaries).
