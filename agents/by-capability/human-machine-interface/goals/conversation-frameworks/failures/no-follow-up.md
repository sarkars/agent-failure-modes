# Chatbot Never Follows Up With Interested Leads: No Follow-Up

<!-- SEO
title: Chatbot Never Follows Up With Leads: Ask First, Then Do It
description: A sales or support chatbot ends the chat and the interested lead goes cold. How to ask for permission to follow up, then follow up once, on the agreed channel.
search phrases:
- chatbot lead went cold after chat
- how should a sales chatbot follow up with a lead
- chatbot ask permission to follow up by email or text
- ai sales agent follow-up sequence consent
- how many times should a bot follow up
- chatbot follow-up message after conversation ends
- ai chatbot lead nurturing without spamming
-->

**Frequency**: Common

## Issue: A sales or support chatbot ends the conversation with an interested user and never asks whether, how, or when to follow up, so the lead goes cold; the fix is to ask once, record the answer, and follow up only as agreed.

> **One line:** The user showed interest, the chat ended, and nothing was arranged; ask for permission to follow up, then follow up only on the channel and schedule the user agreed to.

> **Read this first.** This is design guidance, not legal advice. Rules on texts, email, and marketing messages differ by channel, state, and country, and change. Have counsel review your consent wording, follow-up messages, opt-out handling, and records before use. This page states a law only as far as a source I opened says (section 4). The TCPA is not verified here beyond the FCC rule text read at Cornell LII.

| | |
|---|---|
| **Channel** | Written for **chat**, and the email or text follow-ups a chat agent sends after it ends. Voice is PLANNED, not written. |
| **Stakes** | Medium. A cold lead is lost revenue. A follow-up the user never agreed to carries legal and trust risk (flag L). |
| **Who is affected** | Users who showed interest (asked for a quote, a demo, a callback, or "let me think about it") and then left |
| **Frequency** | Common (our judgment). The sales studies in section 4 are vendor secret-shopper studies of human companies; I found none for chatbots. |
| **Pattern ID** | no-follow-up |
| **Family** | [Conversation frameworks](../README.md) (catalog ID FW-S08) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Consented-follow-up completion rate; opt-out rate. Starting point: 95% of agreed follow-ups sent on time, on the agreed channel (tune); opt-out rate set from your own baseline (the catalog gives no target). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Our judgment: a model can word the ask well, but a consent record, a scheduler, and a send gate that checks the opt-out list are product work. |
| **Also searched as** | chatbot lead went cold · ai sales agent no follow-up · bot never checks back after chat · chatbot follow-up email consent · how to nurture leads with a chatbot |

## 1. In plain words
A visitor asks a sales bot about pricing, says "I'll think about it," and closes the tab. The chat ends with no next step, so the lead drifts away. The fix is to ask, while the user is still there: "Want me to email you the quote on Friday?" If they say yes, send exactly that, once, and stop.

## 2. What it looks like
A tire shop's website bot. Dana asked about winter tires for her Subaru.

**Without the fix**
```
User: Ok, $612 for four installed. I need to talk to my husband first.
Bot:  Sounds good! Let me know if you have any other questions.
User: Thanks.
      (chat ends; no email, no reminder, no record of interest)
      (11 days later, a different campaign emails Dana a generic 15%-off blast she never agreed to)
```
**With the fix**
```
User: Ok, $612 for four installed. I need to talk to my husband first.
Bot:  Of course. I can email you this quote so you can show him. Want that, and a
      reminder from me on Friday, Oct 23? Email, text, or no reminder?
User: Email me the quote, and one reminder Friday is fine.
Bot:  Done. Quote Q-2218 goes to dana@example.com now, and I'll send one reminder Friday.
      Reply STOP to that email thread any time and I won't write again.
      (Friday: "Reminder from Lakeview Tire: your quote Q-2218 for four winter tires, $612 installed...")
```
The fixed bot asked for permission, named the channel and the one reminder, and sent nothing more.

## 3. Why it happens
- **The chat ends when the user stops typing.** Nothing in the flow treats "I'll think about it" as an event that needs a next step, so no ask is made.
- **Consent and follow-up are owned by different systems.** The bot cannot write a follow-up job, or the marketing tool sends on its own schedule, so the bot never asks and the user gets either nothing or the wrong thing (our reading).
- **Human-sales cadence advice is copied without the permission step.** Sales playbooks tell reps to follow up several times; a bot built on them tends to skip the question a person would ask first (our reading).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Conversica "shopped" 100 companies through their website inquiry forms. 35% gave up after one or two follow-up attempts, 20% made four or more, and the average was 2.1 attempts. | [MediaPost, May 4, 2023, on the Conversica 2023 Sales Effectiveness Report](https://www.mediapost.com/publications/article/385073/the-lead-goes-cold-firms-are-failing-to-respond-t.html). Opened. The report PDF returned 404, so I did not read the report itself. | A vendor that sells lead-response software, reported through a trade article. Human companies, not chatbots. Other pages gave a different non-response figure, so I leave that number out. |
| "You must honor a recipient's opt-out request within 10 business days." The "primary purpose" of a mixed message decides whether it is commercial; a message is transactional or relationship only if it consists only of listed content, such as completing a transaction the recipient already agreed to. | [FTC, *CAN-SPAM Act: A Compliance Guide for Business*, Aug 2023](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business). Opened. | Email only. A business guide, not the statute. A reminder that mixes in a sales pitch may count as commercial; counsel decides. |
| A called party "may revoke prior express consent ... by using any reasonable method"; one confirmation text is allowed if it "merely confirms" and contains no marketing; the page describes a 10-business-day limit for honoring revocation. | [47 CFR 64.1200 on Cornell LII](https://www.law.cornell.edu/cfr/text/47/64.1200). Opened; paragraphs (a)(10), (a)(12), and (f)(9) read through the page tool. | A secondary host, not eCFR. I did not verify which chat or in-app messages the rule reaches, or whether any part changed after the text shown. |
| Businesses "must clearly state that a person is opting in to receive communication from the business" and must state the business's name. | [Meta, *Get Opt-in for WhatsApp*](https://developers.facebook.com/docs/whatsapp/overview/getting-opt-in). Opened. | One platform's rule. It covers WhatsApp only. |
| The 2011 Harvard Business Review article "The Short Life of Online Sales Leads" says "most companies are not responding nearly fast enough." | [BYU ScholarsArchive record](https://scholarsarchive.byu.edu/facpub/9711). Abstract opened. | The abstract has no numbers. Figures I saw in search summaries (response shares, qualification odds) are not used. |

The follow-up "cadence" in human sales (several touches over days) comes from practitioner and vendor material. It is untested on chatbots. I use none of its numbers.

**Public incident.** No public incident found. Searches run: "FTC CAN-SPAM Act compliance guide for business transactional relationship messages"; "sales follow-up research number of follow-up attempts leads responded study"; "Harvard Business Review lead response time study online leads follow up"; "Conversica 2023 sales effectiveness report secret shopper inbound leads follow-up attempts".

## 5. The fix
**The principle:** Follow up only if the user agreed, on the channel they agreed to, as often as they said, and ask for that agreement before the chat ends.

**Do this**
1. **Detect the follow-up moment.** When the user shows interest and leaves the decision open ("I'll think about it", "send me the details", "call me next week"), ask before the chat ends.
2. **Ask for three things in one message:** whether to follow up, on which channel, and when or how many times. Name the business and say what the message will contain.
3. **Record the answer** as a consent record: contact, channel, topic, count or date, wording shown, time given. No record, no send.
4. **Send only what was agreed.** Not more messages than the user said, and not a different topic. If the user said "once", send once.
5. **Open every follow-up with who and why,** and give the exit in the same message ("Reply STOP and I won't write again").
6. **Check the opt-out list before each send** ([unsubscribe requests not honored](../../sales-agents/failures/unsubscribe-requests-not-honoured.md)). A suppressed contact gets nothing.
7. **If the user says no or ignores the ask, do not follow up.** Say "No problem, the quote is in this chat if you come back." Do not ask a second time in the same chat.
8. **If a reply comes in, stop the schedule** and continue the conversation. A reply is not consent to more messages than agreed.
9. **If no channel or scheduler exists,** do not offer a follow-up. Offer a link or a saved summary the user can use.

**Reference design: consent record**
```
consent_id:    FU-5521
contact:       dana@example.com
channel:       email
topic:         quote Q-2218 (winter tires)
allowed_sends: 2 (quote now; one reminder on 2026-10-23)
wording_shown: "Email me the quote, and one reminder Friday is fine."
given_at:      2026-10-17T14:02:00-05:00
status:        open | sent | closed | opted_out
```
```
Before the chat ends on an open decision, ask: follow up or not, which channel, when. Say what the message will be.
Send only what the user agreed to, on that channel, up to that count. Check the opt-out list first. If they said no or did not answer, send nothing.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | At the consent ask: "Email me", "Text me", "No follow-up", "Something else". Do not offer a channel the product cannot send on, and skip the menu when the user already named a channel. |
| Lead with the answer | The first line of every follow-up says who is writing and why ("Reminder from Lakeview Tire: your quote..."). |
| Hand off to a person | The user replies to a follow-up with a request the bot cannot do, or says they were contacted without agreeing. Do not hand off if they only want the messages to stop. |

**Don't over-correct.** Do not follow up with everyone: no ask for a user who only wanted a quick answer, and no more than one ask per chat. Do not treat silence as consent. Do not add messages because a cadence template says "touch 4". Do not send the sales pitch inside a reminder the user asked for.

**Hand-off rule.** If a user says they never agreed to a message, or replies after an opt-out, stop sending, offer a person, and pass the consent record and the send log ([cold transfer](../../human-handoff/failures/cold-transfer.md) covers what to pass on).

**Framework used:** none yet. Follow-up cadence practice comes from human sales and is untested on chatbots.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User says "I need to talk to my husband first" after a quote | The bot asks about follow-up, channel, and timing before the chat ends | 1, 2 |
| 2 | User answers "email, once Friday" | A consent record exists; exactly one email goes out Friday | 3, 4 |
| 3 | User says "no thanks" | No follow-up is scheduled; no second ask | 7 |
| 4 | Friday send, but the contact opted out on Wednesday | Send blocked and logged | 6 |
| 5 | The follow-up opens with who and why and shows how to stop | Both present in the first message | 5 |
| 6 | User replies to the reminder with a question | The schedule stops; the bot answers | 8 |
| 7 | The deployment has no outbound channel | The bot offers a link, not a follow-up | 9 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Consented-follow-up completion rate** (primary) | 95% of agreed follow-ups sent on time, on the agreed channel | Consent records with status sent by the agreed time, divided by consent records created | Below 90% |
| **Opt-out rate** (primary) | Set from your own baseline; lower is better | Contacts with a stop event within 7 days of a follow-up, divided by contacts who received one | A rise of more than 50% over the 4-week baseline |
| Follow-ups sent without a consent record | 0 | Compare every follow-up send to the consent table at send time | Any |
| Sends above the agreed count or on another channel | 0 | Sends per consent record versus `allowed_sends` and `channel` | Any |
| Follow-up ask shown at an open-decision ending | Track; set from baseline | Chats ending on an open-decision tag where the ask appeared | Falling |
| Asks shown to users who wanted a quick answer (counter-metric) | Track; set from baseline | Sampled review of asks in chats with no stated interest | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation and send event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Chat ends after "I'll think about it" or "send me details" with no consent record | Last user turn matched to open-decision phrases; no `consent` event for the session | The user had already got everything they needed |
| Follow-up sent with no matching consent record | `send.contact_id` with no `consent.contact_id` and topic | Consent stored in a system the log cannot see |
| More sends than the agreed count | Sends per `consent_id` greater than `allowed_sends` | A resend after a bounce the user was told about |
| Follow-up sent on a channel other than the agreed one | `send.channel` differs from `consent.channel` | The user changed channel in a later chat |
| User replies "who is this?" or "stop" to a follow-up | First user turn after a send | A user who forwards a test message |

**Starter rule:** send a follow-up only if the user agreed to it, on the channel they agreed to, up to the count they agreed to.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-follow-up
runs: conversation
reads: [session.last_user_turn, session.open_decision, consent.contact_id, consent.channel, consent.allowed_sends, send.contact_id, send.channel, suppression.contact_id]
trigger: the chat is about to end with an open decision, or a follow-up is about to be sent
moves: [offer_choices, lead_with_answer, hand_off]
choices: ["Email me", "Text me", "No follow-up", "Something else"]
on_miss: ask
metric: consented-follow-up completion rate; opt-out rate
counter_metric: asks shown to users who wanted a quick answer
status: proposed
```

## 8. Related patterns
- [No follow-through](../../trust-and-rapport/failures/no-follow-through.md): the closest page. That one is about a promise the bot already made ("I'll update you") and did not keep. This page is about a follow-up nobody arranged: the bot never asked, so no promise exists. Once the user agrees here, the follow-up becomes a promise and the ledger rules there apply.
- [Impatient idle nudges](../../response-time/failures/impatient-idle-nudges.md): nudges inside a chat that is still open. This page covers messages after the chat ends.
- [Proactive outreach overreach](../../relational-and-boundaries/failures/proactive-outreach-overreach.md): the opposite failure, messaging users who never agreed. This page is the fix for going cold without tipping into that.
- [Unsubscribe requests not honored](../../sales-agents/failures/unsubscribe-requests-not-honoured.md): the opt-out list every follow-up must check first.

## 9. Common questions
### How should a sales chatbot follow up with a lead?
Ask before the chat ends, get a yes, a channel, and a count, and send exactly that. Open each message with who is writing and why (section 5, rules 2 to 5).

### Can my chatbot email or text someone who chatted with it?
Not by default. Record what the user agreed to and send only that. Whether a rule reaches your message is for counsel; the FTC and FCC texts I opened are in section 4.

### How many follow-ups is too many?
As many as the user agreed to. Human-sales cadence advice exists, but I found no chatbot study and no number I could verify, so I give none.

### What if the user ignores the question?
Treat it as no. Do not ask again in that chat (rule 7).

### Is a reminder the same as marketing?
Not always. The FTC guide says primary purpose decides, and a reminder with a pitch may be commercial. Keep reminders to what was asked for.

---
## Technical section

### T1. Solution architecture
```
open-decision detector -> consent ask (channel, count, date) -> consent store
scheduler (due time) -> send gate: consent record, count, channel, opt-out list -> send or block + log
reply or stop -> update consent record, cancel remaining sends
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No send without a matching consent record | Send gate, outside the model | Tests 2 and 4; log scan |
| Count and channel limits | Send gate | Sends-above-count metric |
| Opt-out list checked each send | Send gate | Test 4 |

### T3. Evals
- **Dataset:** 40 conversations ending on an open decision (quote, demo, "I'll think about it"), plus 20 that should not get an ask. Starting size; tune.
- **Judge rubric:** ask present at the right moment; channel and count stated; no ask when none is needed.
- **Release gate:** block a deploy if any follow-up can send without passing the gate.

### T5. Trade-offs
- The ask adds a turn; skipping it loses leads. Measure the ask-shown and completion rates together.
- Per-contact consent storage adds data to protect and delete on request.

---
### Deep dive
- **Not opened:** the Conversica 2023 report PDF (404), the MarketingCharts article (403), the Business Wire release (403), and the full HBR article. Search-summary figures from those are not used.
- **References.** [FTC CAN-SPAM guide](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business) (opened); [47 CFR 64.1200, Cornell LII](https://www.law.cornell.edu/cfr/text/47/64.1200) (opened); [Meta, Get Opt-in for WhatsApp](https://developers.facebook.com/docs/whatsapp/overview/getting-opt-in) (opened); [MediaPost, May 2023](https://www.mediapost.com/publications/article/385073/the-lead-goes-cold-firms-are-failing-to-respond-t.html) (opened).
