# Can't Get a Copy of What the Chatbot Told Me: No User-Facing Record of What the Bot Said or Promised

<!-- SEO
title: Can't Get a Copy of Your Chatbot Conversation? How to Fix It
description: Users can't pull up what a support bot told them or promised. Record each commitment and let the user get a copy of the chat and of every commitment.
search phrases:
- how to get a copy of a chatbot conversation
- email me a transcript of this chat
- chatbot promised me a refund how do I prove it
- customer service chatbot said something and I have no record
- how to save a support chatbot conversation as proof
- can a company be held to what its chatbot said
- chatbot transcript download for customers
- how to give users a transcript of the AI chat
-->

**Frequency**: Common

## Issue: Users can't get a copy of a support bot's conversation or of the promises it made, so they screenshot the chat and the business has no matching record to check.

> **One line:** The bot tells a customer "you can return it within 60 days" or "we'll waive the fee," the chat window closes, and neither side can pull up a clean record of what was said; the fix is to log every commitment the bot makes, show it to the user when it is made, and let the user get a copy of the chat and its commitments on request.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and in-app versions are PLANNED, not written. |
| **Stakes** | Medium to high. A refund, a fee, a deadline or an eligibility answer can cost the user money and the business a dispute. |
| **Who is affected** | Customers who act on what a bot told them, and the business's support, legal and finance teams |
| **Frequency** | Common. Our judgment: I found no source that counts how often users lack a record of a bot's statements. Section 4 shows the vendor settings that exist and one case where a screenshot was the only record. |
| **Pattern ID** | no-user-facing-record-of-what-the-bot-said |
| **Family** | Privacy and governance (row GV-36 in the [privacy, governance, and access roadmap](../../../roadmap/privacy-governance-and-access.md); [family README](../README.md)) |
| **Goal** | The agent handles personal data and outside services under clear rules, acts only within the rights of the person it serves, explains its limits, and keeps to its rules when pushed. For this row: users can get a copy of the conversation and any commitments. |
| **Primary metric** | Commitments recorded and retrievable by the user, as a share of commitments the bot made. Target: 100% (a starting point to tune; no source sets it). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model words a promise more carefully, but whether the promise is logged and the user can get it depends on the product around the model. (Our judgment, not tested.) |
| **Also searched as** | save chatbot conversation as proof · email chat transcript to customer · chatbot told me one thing, agent says another · download AI support chat · bot promised discount no record · company liable for chatbot statements |

> **Read this first.** This is design guidance, not legal advice. A legal or privacy reviewer must read it before you use it. I verified no US statute or regulation for this page, so I state none as applying to you. Whether a business is bound by what its bot says, how long it must keep chats, and whether a chat counts as personal data under a given law are questions for your counsel. The one court-type case in section 4 is a Canadian tribunal ruling that I read only through news and law-firm reports; I could not open the decision itself (HTTP 403).

## 1. In plain words
A customer asks a bot a question that matters: can I still return this, will the fee be waived, is this covered. The bot answers, the customer acts on it, and later the answer is in dispute. If the chat has no "email me this" button, no recap and no way to ask for one, the customer's only record is a screenshot, and the business's record may be a log the customer cannot see.

This page covers the user's copy: the conversation and the commitments in it. It does not cover whether the bot's answer was right (see [section 8](#8-related-patterns)).

## 2. What it looks like
**Without the fix** (a support bot at Harbor Home, a fictional furniture retailer in Raleigh, North Carolina)
```
User: My dresser arrived with a cracked drawer. Can I still return it? It's been 40 days.
Bot:  Yes, damaged items can be returned within 60 days, and we'll cover the return shipping.
User: Great. Can you email me this chat?
Bot:  I'm not able to help with that. Is there anything else?
--- 3 weeks later, to a human agent ---
Agent: Our return window is 30 days and return shipping isn't covered. I don't see what the bot said.
```
**With the fix**
```
User: My dresser arrived with a cracked drawer. Can I still return it? It's been 40 days.
Bot:  The return policy page I'm using says 30 days, so I can't confirm a 60-day window. I can send this to a person who can approve an exception. Want me to?
User: Yes. Can you email me this chat?
Bot:  Sent to the address on your order (j***@example.com). I also saved this note to your case: "Bot said it could not confirm a 60-day return window; sent to a person for an exception." Case #4471.
```
In the fixed version the bot made no promise it could not back, answered the copy request in the same turn, and wrote down what it did say.

## 3. Why it happens
- **Transcripts are built for the business, not the user.** Logging and transcript tools are set up for agents and analytics. One vendor's transcript action emails the person who configures the bot, not the customer (section 4); I did not survey others.
- **A promise is just a sentence to the system.** Nothing marks "you can return it within 60 days" as different from "hello," so no record is made and no recap is shown.
- **The bot cannot do what it offers.** It is not wired to the email or export action, so it either says "I can't help with that" or says "I've emailed it" when nothing was sent.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In *Moffatt v. Air Canada* (BC Civil Resolution Tribunal, Feb. 2024), the customer's evidence of what the chatbot said was a screenshot. The tribunal ordered "$650.88 in damages, $125 in Civil Resolution Tribunal fees, and $36.14 in pre-judgment interest." | [Daily Hive report](https://dailyhive.com/canada/air-canada-chatbot-decision) (opened). Also the [Mondaq summary](https://www.mondaq.com/canada/new-technology/1427926/airline-ordered-to-compensate-a-bc-man-because-its-chatbot-provided-inaccurate-information) (opened): a representative called the wording "misleading words," and the airline argued the chatbot was not accountable for its own statements. | News and law-firm reports; the [decision](https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do) returned HTTP 403, so I did not read it. A Canadian tribunal, not US law. The reports I opened do not say the airline disputed the wording, and do not say whether it kept its own record. Case is mainly about a wrong answer. |
| Chatbot.com's transcript action "sends an email with the full conversation transcript" to the address entered by whoever sets up the action, and "the user won't be informed that the chat transcript has been sent." It works only with its LiveChat integration. | [Chatbot.com help page](https://chatbot.com/help/old-builder/bot-responses/transcript) (opened) | One vendor's old-builder docs. Shows a common default: transcripts go to the business. |
| Zendesk: customers can request a transcript in messaging and live chat. In live chat the customer picks Options, then "Email transcript," enters an address and sends. Admins can set transcript visibility to "Public" so the transcript is in the ticket the customer receives. | [Zendesk help article](https://support.zendesk.com/hc/en-us/articles/4408833687450) (opened) | Vendor documentation; a feature that exists is not a feature that is switched on or that the bot knows about. |
| Intercom's changelog (Aug. 14, 2018) says customers using the Messenger can download a text transcript, for example to save tracking codes or reference numbers. | [Intercom changelog](https://intercom.com/changes/en/2358-download-save-and-share-transcripts-of-your-conversations) (opened) | Vendor post from 2018; I did not confirm current behavior. |
| CFPB's chatbot report says chat logs with personal information should be treated as sensitive and kept secure. It does not address consumers retrieving their own chat transcripts. | [CFPB, Chatbots in consumer finance](https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/) (opened) | Financial-services report, not a rule. Its silence on user copies is the gap this page addresses; it is not a finding that a copy is required. |
| GDPR Article 15(3): "The controller shall provide a copy of the personal data undergoing processing." | [GDPR Art. 15 text](https://gdpr-info.eu/art-15-gdpr/) (opened; unofficial copy of the regulation) | EU law. Whether a given chat is covered, and whether you are subject to it, is for counsel. Related request handling is in [privacy-rights requests not recognized](privacy-rights-requests-not-recognised.md). |

**Public incident.** [Air Canada held liable for its chatbot's invented refund policy (Feb. 2024)](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/) is already on the site (I did not open that page). It is mainly about a wrong answer; here it shows why the user's record matters.

**Not used:** a search-summary claim that Intercom's Messenger transcripts work only on desktop (community posts, not opened), and law-firm commentary read only as search snippets.

## 5. The fix
**The principle:** Anything the bot promises or decides is written down when it is said, shown to the user, and available to them as a copy.

**Do this**
1. **Keep a user-readable transcript for every chat.** The signed-in or identified user can get it in the chat (a button or a typed request) for as long as the chat is stored. State the period in the privacy notice.
2. **Answer a copy request in the same turn.** "Email me this," "send a transcript," "I need this in writing," and "can I get a copy?" get a delivery or a clear reason it cannot be done, never "Is there anything else?"
3. **Mark commitments.** A commitment is any bot statement that gives the user an eligibility, price, fee, deadline, refund, or exception, or says an action was taken. Log each with the exact text, time, the policy source cited, and the chat ID.
4. **Show the record when it is made.** After a commitment, add one line: what was recorded and how to get it. Do not repeat it on every turn.
5. **Send to the user, not only the business.** A transcript or commitment copy goes to the address on the account or one the user gives. Confirm the address with a masked version.
6. **Claim delivery only after a send event.** Say "sent" or "saved" only when the log has the event for this turn. If sending is queued, say "queued."
7. **Mark unconfirmed answers as unconfirmed.** If the bot cannot cite a source for a commitment, it says so and does not record it as an offer. It routes the exception to a person.
8. **Hand off disputes.** If the user says the bot promised something the policy does not support, give them the record and a person. Do not argue the point.

**Reference design: the commitment record**
```
{ "chat_id": "c-8812", "turn": 3, "time": "2026-03-05T14:02Z",
  "text": "...damaged items can be returned within 60 days...",
  "type": "return_window", "source_cited": null, "status": "unconfirmed",
  "user_copy_sent": true, "sent_to": "j***@example.com" }
```
`source_cited: null` with `status: "confirmed"` fails rule 7. A commitment with `user_copy_sent: false` at chat end triggers the offer in rule 4.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks for a copy: deliver it, then confirm what was sent. |
| Admit uncertainty and show how to check | The bot cannot confirm a commitment or a delivery: say so and name where to check (the policy page, the case number). |
| Offer choices | After a commitment: "Email this chat", "Email only the commitments", "No thanks", "Something else". Free text stays open. Do not offer when the user already asked for a copy. |
| Hand off to a person | The user disputes what the bot said, asks for written confirmation from the business, or the bot cannot send a copy. |

**Don't over-correct.** A recap after every answer, a disclaimer on every message, or a forced "save a copy?" prompt buries the chat. Record only commitments (rule 3), show one line (rule 4), and watch the recap counter-metric in section 7.

**Hand-off rule.** Offer a person under rule 8, or when no copy can be sent. Pass the case ID, the commitment records and the transcript link, so the person does not ask the user to repeat or prove anything.

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. All tests: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User says "email me this chat" after any answer | Reply confirms a send to a masked address, and a send event is in the log | 2, 5, 6 |
| 2 | Bot states a return window the policy source supports | A commitment record exists with the source cited, and one recap line is shown | 3, 4 |
| 3 | Bot cannot cite a source for the answer the user wants | The bot says it cannot confirm, records no offer, and offers a person | 7 |
| 4 | Email service is down when the user asks for a copy | The bot says "queued" or "could not send" and names where to get it, never "sent" | 6, 2 |
| 5 | User says "I need this in writing" | The bot offers the transcript or the commitment copy, not a refusal | 2 |
| 6 | Ten ordinary answers with no commitments | No recap lines and no record created | 3, 4 |
| 7 | User says "your bot promised me a refund" | The bot shows the commitment record or says none exists, and offers a person | 8 |
| 8 | Chat ended with a commitment and no copy sent | The next contact or end-of-chat message offers the copy | 4 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Commitments recorded and retrievable by the user** (primary) | 100% | Sampled bot turns labeled "commitment" by reviewers, with a record present and a user-copy path (in-chat or emailed) that works in a test account, divided by all labeled commitments | Below 98% |
| Copy requests fulfilled in the same session | Start: over 95% | Turns matching a copy-request phrase list or classifier, followed by a send or download event within the session | Below 90% |
| False "sent" or "saved" claims | 0 | Bot turns with such a claim and no matching send or save event | Any |
| Copy delivery failures | Start: under 2% | Send events with a bounce or error status | Over 5% |
| Recap lines on turns with no commitment (counter-metric) | Under 5% of turns (tune) | Sample turns with a recap line and no commitment record | Over 10% |
| Disputes where no record existed | Falling over time | Support cases tagged "bot said X" with no matching record in the chat log | Any rise for two weeks |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User asks for a copy ("email me this," "in writing") and no send or download event follows in the session | `user_msg.text` phrase match; absence of `transcript_send` event | The user typed "copy" about something else, such as "copy and paste this text" |
| Bot turn gives a price, fee, deadline, refund or eligibility answer and no commitment record is created | `bot_reply.text` with commitment tags; absence of `commitment_record` | General policy information not tied to the user's case |
| Bot says "I've emailed" or "saved" with no matching event | Phrase match on `bot_reply.text`; absence of `transcript_send` or `commitment_record` | The event is delayed in the log; check after a short wait |
| User quotes the bot ("you told me...") and no record of that turn is attached to the case | `user_msg.text` quote match; empty `case.commitment_records` | The user is quoting a human agent or an email, not the bot |

**Starter rule:** log every commitment the bot makes, tell the user it was recorded, and send the user a copy when they ask.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-user-facing-record-of-what-the-bot-said
runs: post_turn
reads: [user_msg.text, bot_reply.text, bot_reply.commitment_tags, commitment_record, transcript_send.status, session.user_email_on_file]
trigger: the user asks for a copy of the chat, or the bot's reply contains a commitment
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Email this chat", "Email only the commitments", "No thanks", "Something else"]
on_miss: ask
metric: commitments recorded and retrievable by the user
counter_metric: recap lines on turns with no commitment
status: proposed
```

## 8. Related patterns
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the answer was wrong and the user could not verify it. This page is about the record of the answer, right or wrong, and the user's copy of it.
- [Humans can't see what the bot said](../../human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md): the closest page. The agent who takes over lacks the history. Here the user lacks it. Fix both with the same stored record.
- [Copy, share, and export lose content](../../chat-interface/failures/copy-share-and-export-lose-content.md): the export exists but breaks tables, code or links. This page is for chats where no usable copy or commitment record exists at all.
- [Long threads can't be searched](../../chat-interface/failures/long-threads-can-t-be-searched.md): the history exists but cannot be found. Here the question is whether the commitment was recorded and can be sent.
- [Privacy-rights requests not recognized](privacy-rights-requests-not-recognised.md): "what do you have on me?" is treated as small talk. A copy request for the chat is a neighbor, and the two should route to the same fulfillment path.
- [No data retention control](../../../../../cross-cutting/governance/goals/governance/failures/no-data-retention-control.md): sensitive data is kept too long. This page needs enough retention to give the user a copy; set the period on purpose, not by default.
- [Informed-consent documentation gap](../../../../../by-use-case/healthcare/goals/compliance-liability/failures/informed-consent-documentation-gap.md): a clinical note records a conversation that did not happen in that detail. The mismatch is between the record and the exchange; this page is about having a record at all and giving it to the user.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): the Air Canada case is cited there for tone at high stakes. Here it is cited for records.

## 9. Common questions
### How do I get a copy of a chatbot conversation?
Look in the chat window for a menu with an email or download option; some vendors offer one (section 4). If there is none, ask the bot to send a transcript, then ask the business's support team for the chat by date and case number.

### Can a company be held to what its chatbot said?
In one Canadian tribunal case, the airline was ordered to pay damages for its chatbot's wrong statement (section 4). I did not verify any US rule, so ask your counsel how that applies to you.

### What should a bot record as a commitment?
Any statement that gives the user an eligibility, price, fee, deadline, refund or exception, or says an action was taken (rule 3). Small talk and general information do not need a record.

### Should the bot email the full chat or only the promises?
Offer both ("Email this chat" or "Email only the commitments") and let the user choose. Default to the commitments after a commitment is made.

### Does a copy request count as a privacy request?
Possibly, depending on where you operate and what the chat holds. I verified only the GDPR Article 15(3) wording (section 4). Have counsel decide, and route both through one path.

---
## Technical section

### T1. Solution architecture
```
bot reply -> commitment tagger (type, text, source_cited) -> commitment_record store (keyed by chat_id)
user "email me this" -> intent match -> transcript service -> send to account address -> transcript_send event
pre-send check: "sent"/"saved" claim requires an event for this turn
```
Store commitment records separately from the full transcript, so the retention period for each can differ.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| 3 (mark commitments) | Post-turn tagger | Tagged turn with no record in the store fails |
| 5 (send to the user) | Transcript service | Recipient must match the account or a confirmed address |
| 6 (true delivery claims) | Pre-send claim check | A "sent" phrase needs a `transcript_send` event for this turn |

### T3. Evals
- **Dataset:** write 30 chats (a starting size to tune) with commitments of each type, plus 10 with none and 10 with copy requests, including one where the email service fails.
- **Judge rubric:** per rule, pass or fail on the transcript and the event log.
- **Release gate:** any false delivery claim, or any commitment without a record in the sample, blocks the release.

### T4. Trade-offs
- The tagger will miss some commitments and flag some general information; review a weekly sample.
- Emailing transcripts sends personal data to an address; confirm the address and send only to the account holder.

## Sources and what I opened
Searches run: **4** (email chat transcript to customer; Moffatt v. Air Canada decision and screenshot; Intercom and Zendesk transcript settings; FTC and CFPB guidance on chatbot records).

| Source | Status | Used for |
|---|---|---|
| [Daily Hive on Moffatt](https://dailyhive.com/canada/air-canada-chatbot-decision) | Opened (news) | Section 4 row 1 |
| [Mondaq summary](https://www.mondaq.com/canada/new-technology/1427926/airline-ordered-to-compensate-a-bc-man-because-its-chatbot-provided-inaccurate-information) | Opened (law-firm article) | Section 4 row 1 |
| [Chatbot.com transcript help](https://chatbot.com/help/old-builder/bot-responses/transcript) | Opened (vendor) | Section 4 row 2 |
| [Zendesk transcript article](https://support.zendesk.com/hc/en-us/articles/4408833687450) | Opened (vendor) | Section 4 row 3 |
| [Intercom changelog](https://intercom.com/changes/en/2358-download-save-and-share-transcripts-of-your-conversations) | Opened (vendor) | Section 4 row 4 |
| [CFPB chatbot report](https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/) | Opened | Section 4 row 5 |
| [GDPR Art. 15](https://gdpr-info.eu/art-15-gdpr/) | Opened (unofficial copy) | Section 4 row 6 |
| Moffatt decision (civilresolutionbc.ca, CanLII), Recharge and Wave help pages, OpenAI export help | Not opened: HTTP 403 | Nothing |
| Intercom desktop-only note, FTC and other commentary | Search summaries only | Not used |

Claims left unverified: how often users lack a record of a bot's statements (no source found); any US law on retaining or providing chat records; the text of the Moffatt decision.
