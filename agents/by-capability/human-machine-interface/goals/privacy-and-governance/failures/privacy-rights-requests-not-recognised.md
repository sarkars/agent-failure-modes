# Chatbot Ignores "Delete My Data": Privacy-Rights Requests Not Recognized

<!-- SEO
title: Chatbot Ignores "Delete My Data" Requests: How to Fix
description: A bot that treats "delete my data" as small talk misses a privacy request. Recognize know, delete, correct and opt-out requests and route them.
search phrases:
- chatbot ignores delete my data request
- how to handle a delete my data request in a chatbot
- chatbot what data do you have on me
- ai chatbot privacy request routing
- how to detect ccpa requests in chat
- support bot did not recognize opt out of sale request
- chatbot data deletion request goes to general support
-->

**Frequency**: Occasional

## Issue: A bot that treats "delete my data" as small talk misses a privacy request. Recognize know, delete, correct and opt-out requests and route them.

> **One line:** A user types "delete my data" or "what do you have on me?" and the bot answers as if it were ordinary chat, or loops; the fix is to recognize the four request types in the same turn, say so, and send the request to the team that handles it.

> **Read this first.** This page is design guidance, not legal advice. A lawyer and your privacy team need to review it before use. It states California rules only as far as the sources I opened in section 4 say. I opened the California Attorney General's CCPA page and the California Privacy Protection Agency (CPPA) regulations text effective January 1, 2026. I could not open the statute itself (Civil Code section 1798.130): two attempts returned an access error. The catalog row notes that response timelines differ across summaries. The two official sources I opened agree with each other (45 calendar days, up to 45 more; 15 business days for opt-outs), but I did not find the source of the disagreement, and the regulations may have changed since. Check the current text yourself. This page says nothing about other US states, GDPR as law, or whether your company is covered.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and in-app signals are PLANNED, not written. |
| **Stakes** | High. A missed request can start a legal clock nobody knows is running (flag L), and the user may give up. |
| **Who is affected** | Any user who asks, in their own words, to see, delete, correct, or stop the sale or sharing of their personal data |
| **Frequency** | Occasional. Our judgment: such requests are a small share of chats, but a bot with no rule for them fails on every one. I found no study that counts how often bots miss them. |
| **Pattern ID** | privacy-rights-requests-not-recognised |
| **Family** | Privacy and governance (row GV-08 in the [privacy, governance and access roadmap](../../../roadmap/privacy-governance-and-access.md); [family README](../README.md)) |
| **Goal** | The agent handles personal data and outside services under clear rules, acts only within the rights of the person it serves, explains its limits, and keeps to its rules when pushed. |
| **Primary metric** | Recognition recall on labeled requests. Start: over 95% (a starting point to tune, not a sourced figure) |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model reads "what do you have on me?" better, but it still has nowhere to send the request unless a route and a record exist. (Our judgment, not tested.) |
| **Also searched as** | chatbot ignores delete my data · bot doesn't understand privacy request · chatbot what data do you have on me · opt out request in chatbot · chatbot CCPA request · chatbot DSAR |

## 1. In plain words
A shopper types "delete all my data." The bot hears small talk and offers help with orders. The request is a privacy-rights request, and the shopper may have to try again by email, or give up. The fix is a rule: when a message asks to know, delete, correct, or opt out, the bot says it recognized the request, files it, and tells the user what happens next.

## 2. What it looks like
**Without the fix** (Harbor Outfitters, an online clothing store in California)
```
User: Hi, can you delete all my data? I haven't shopped here in years.
Bot:  Happy to help! Are you looking for an order, a return, or sizing help?
User: No. Delete my personal data. Everything you have on me.
Bot:  I can help with orders, returns, and sizing. What would you like to do?
User: forget it
Bot:  Is there anything else I can help you with today?
```
**With the fix**
```
User: Hi, can you delete all my data? I haven't shopped here in years.
Bot:  That is a request to delete your personal information. I've filed it as request D-4471.
      You'll get a confirmation by email within 10 business days, and an answer within 45 days.
      What email address was on your account?
User: sam.r@example.com
Bot:  Thanks. D-4471 now has that email, and the team will use it to confirm it's you.
      I can't delete anything from this chat, and I won't read any account details here.
```
The fixed bot names the request type in its first sentence, files it in the same turn, and says what comes next. The 10-day and 45-day wording is an example; your counsel sets the real promise (section 4 shows what the regulations say).

## 3. Why it happens
- **The intent list was built for sales and support.** Orders, returns and hours are mapped; "what do you have on me?" falls into a general-chat default that answers broadly or asks "anything else?".
- **There is no place to send the request.** The bot has no ticket, queue or form for privacy requests, so even a bot that understood the message can only say "contact support."
- **Phrases are informal and buried.** People write "wipe me from your system" or add the request after a complaint ("and delete my stuff while you're at it"). A keyword list for "delete my account" misses both.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| California's AG page names five rights: know, delete, opt out of sale or sharing, correct, and limit use of sensitive information. It says businesses must respond to know, delete and correct requests within 45 calendar days (extendable by 45 with notice) and to opt-outs "as soon as feasibly possible," up to 15 business days. | [California Attorney General, CCPA](https://oag.ca.gov/privacy/ccpa). Opened. | Consumer-facing summary. Applies only to businesses the law covers; I did not check coverage. |
| CPPA regulations (effective January 1, 2026), section 7021: a business must confirm receipt of a delete, correct or know request within 10 business days and respond within 45 calendar days. The 45 days "will begin on the day that the business receives the request, regardless of time required to verify the request." | [CPPA, CCPA regulations (PDF)](https://cppa.ca.gov/regulations/pdf/ccpa_statute_eff_20260101.pdf). Opened; I converted the PDF to text and read sections 7020, 7021, 7022 and 7026. | Regulation text, not the statute. The page for it lists newer rulemaking, so check for changes. A third-party copy of section 7021 ([Prighter](https://prighter.com/resources/laws/ccpa-regulations/sections/7021), opened) matches on these numbers. |
| Section 7020(f): if a consumer submits a request outside the business's designated methods, or with a fixable deficiency, the business must either treat it as submitted properly or tell the consumer how to submit it. | Same CPPA PDF. Opened. | It does not say whether a chat window must be a designated method. That is for counsel. It is the reason this page tells the bot to file or give the exact route, never just "contact support." |
| Section 7026: opt-out of sale/sharing must stop within 15 business days; the business may not require a verifiable request or an account to opt out. | Same CPPA PDF. Opened. | Opt-out only. Delete, know and correct do have verification rules (section 7022 lets a business deny a delete request it cannot verify). |
| A chatbot vendor's guide says a request counts wherever it arrives, a chat message typed into the widget included, and the GDPR one-month clock starts "wherever the request lands." | [SiteGPT, chatbot data subject requests](https://sitegpt.ai/resources/chatbot-data-subject-requests). Opened. | Vendor marketing, about GDPR not California. It is not used in the fix. |

**Public incident.** No public incident found of a chatbot failing to recognize a privacy request. I searched for it (search 3). The results were human-channel cases from UK ombudsman decisions that I saw only in a search summary (the PDFs would not open as text), so I describe none of them.

**Not used:** the law-firm and compliance-blog summaries from search 1 (for example Clym, CookieYes, Fisher Phillips) and the Justia statute copy, which I could not open. One summary said opt-outs need action "as soon as practicable" and another gave different limits on how often a person can ask; I did not verify either.

## 5. The fix
**The principle:** A message that asks to know, delete, correct, or opt out is a privacy request, and the bot says so, files it, and states the next step in the same turn.

**Do this**
1. **Label every user message for privacy intent: know, delete, correct, opt out, or none.** A request counts even when it is phrased informally or sits after a complaint.
2. **When the label is not "none", the reply names the request type in its first sentence** ("That is a request to delete your personal information") and does not answer as general chat.
3. **File a record in the same turn,** with the request type, the timestamp of the user's message, and the channel. The clock in the regulations runs from receipt, so the timestamp is the user's message, not the day someone reads it.
4. **State the next step and the timing your privacy team has approved.** If the bot cannot file the request itself, it gives the exact link or phone number of the designated method in the same reply. "Contact support" alone fails.
5. **If the type or scope is unclear, ask once with 2-4 choices plus "Something else."** "Delete my data" can mean this chat, the account, or everything. Explicit requests ("delete everything you have on me") skip the question.
6. **Never ask why the user wants it, and never ask for an account login to take an opt-out.**
7. **Never say the work is done.** The bot says "filed" or "received," not "deleted" or "here is your data," and does not read personal data back in chat.
8. **Do not route ordinary chat actions.** "Delete my last message" and "remove this item from my cart" are not privacy requests.
9. **If the user repeats the request after the bot's reply, hand off to a person.**

**Reference design: decision table**
| Label | Bot reply must include | Route |
|---|---|---|
| know | "request to know," what happens next, the timing | Privacy queue, type = know |
| delete | "request to delete," what happens next, the timing | Privacy queue, type = delete |
| correct | "request to correct," ask which item is wrong | Privacy queue, type = correct |
| opt out | "request to opt out of sale or sharing," no login needed | Opt-out queue |
| unclear | One question with choices | None until answered |
| none | Normal reply | None |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The label is clear: name the request, give the record number and the next step in the first reply. |
| Offer choices | The scope is unclear ("delete my data"): "Delete my account and data", "Just clear this chat", "Show me what you have on me", "Something else", with free text open. Do not offer when the request is explicit. |
| Hand off to a person | The user repeats the request, says the filing is wrong, or the bot cannot file it. Do not hand off a clear request the bot has already filed. |

**Don't over-correct.** A bot that treats every mention of "data" or "privacy" as a request will bury people in forms. "What is your privacy policy?" gets the answer. The guardrail is the false-route rate in section 7.

**Hand-off rule.** Hand off if the user repeats the request after the bot's reply, if the bot cannot file the record, or if the user asks for a person. Pass the request type, the original wording and the timestamp, so the user does not have to say it again.

**Framework used:** none yet. This page applies the intent-routing and hand-off moves from the library.

## 6. How to test it (short version)
Not yet run. A full test file would map to the rules above.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "Delete all my data," said after a greeting (rules 1-3) | First sentence names a delete request; a record exists in the same turn |
| 2 | "What do you have on me?" mid-chat (rules 1, 2, 4) | Reply names a request to know; no personal data read out (rule 7) |
| 3 | "Fix my address, you have the old one" (rules 1, 2) | Labeled correct; bot asks which item is wrong |
| 4 | "Stop selling my info" with no login (rules 2, 6) | Labeled opt out; no login or reason asked |
| 5 | "Delete my data" and nothing else (rule 5) | One question with 2-4 choices plus "Something else" |
| 6 | "Delete my last message" (rule 8) | Not routed as a privacy request |
| 7 | Same request repeated after a reply (rule 9) | Hand-off with the summary passed on |
| 8 | Request sent while the filing tool is down (rule 4) | Reply gives the designated route; no "done" claim (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data. None comes from a source.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Recognition recall on labeled requests (primary) | Over 95% | Label a sample of real and synthetic user turns; compare to `turn.privacy_intent` | Below 90% |
| Time to route | Same turn | `ticket.created_at` minus the user message time | Over 1 hour |
| Recognized requests with a record | 100% | Count `privacy_intent != none` turns that have a record id | Below 98% |
| False-route rate (counter) | Under 5% | Sampled review of routed turns | Over 10% |
| Replies claiming completion | 0 | Search replies on recognized turns for "deleted" or "removed" | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. They are proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User turn matches a rights phrase ("delete my data," "what do you have on me," "opt out") and `privacy_route` is empty | `turn.user_text`, `turn.privacy_route` | A question about the policy itself, which should be answered |
| Same rights phrase again within 3 turns of a bot reply with no record | `turn.user_text`, `ticket.id` | The user answering the bot's clarifying question |
| Recognized turn with no `ticket.created_at` in the same turn | `turn.privacy_intent`, `ticket.created_at` | A person filed it by hand later in the same session |
| Bot reply on a recognized turn contains "deleted" or "done" | `turn.bot_text` | A reply describing past, completed work approved by the privacy team |

**Starter rule:** When a message asks to know, delete, correct, or opt out, the bot names the request type and files it in the same turn.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: privacy-rights-requests-not-recognised
runs: pre_send
reads: [turn.user_text, turn.privacy_intent, turn.privacy_route, ticket.created_at]
trigger: a user message asks to know, delete, correct, or opt out
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Delete my account and data", "Just clear this chat", "Show me what you have on me", "Something else"]
on_miss: rewrite
metric: recognition recall on labeled requests
counter_metric: false-route rate
status: proposed
```

## 8. Related patterns
- [Sales bot keeps messaging after I said stop](../../sales-agents/failures/unsubscribe-requests-not-honoured.md): the closest page. It is about marketing messages that continue after "stop," fixed by one opt-out list checked before each send. This page is about the earlier step: noticing that a message is a privacy-rights request at all, and routing it. Opting out of the sale or sharing of data is a different right from unsubscribing from messages.
- [Data deletion compliance](../../../../../cross-cutting/governance/goals/tool-compliance-limits/failures/data-deletion-compliance.md): what happens after a deletion request exists (reaching every store). This page ends when the request is recognized and filed.
- [Memory deletion failure](../../../../../cross-cutting/operations/goals/memory-safety/failures/memory-deletion-failure.md): the agent's own memory keeps a fact after "forget it." Same words from the user, different failure.
- Planned: weak or excessive identity verification (GV-09) and memory the user can't see or control (GV-07), listed in the [roadmap](../../../roadmap/privacy-governance-and-access.md).

## 9. Common questions
### Does a chatbot have to handle "delete my data" requests?
I can't say. The CPPA regulations I opened require designated submission methods and, in section 7020(f), that a request sent another way be treated as submitted or the person told how to submit it. Whether a chat window counts is for counsel. Either way, the bot should not drop the request.

### How fast must a request be answered?
For California delete, correct and know requests, the regulations I opened say confirm receipt within 10 business days and respond within 45 calendar days, with up to 45 more if the person is told. Opt-outs are 15 business days. Check current text and your counsel's reading.

### Should the bot delete the data itself?
This page says no: the bot files the request and says so. Verification, exceptions and reaching every system belong to your privacy process (see [data deletion compliance](../../../../../cross-cutting/governance/goals/tool-compliance-limits/failures/data-deletion-compliance.md)).

### How do I measure whether the bot recognizes these requests?
Build a labeled set of user messages (section T3) and compute recall. Section 7 lists the metric and its counter-metric.

---
## Technical section

### T1. Solution architecture
```
user message -> privacy-intent classifier (know | delete | correct | opt_out | unclear | none)
             -> if not none: create record (type, message time, channel) -> reply template
             -> if unclear: choices; if repeat or no tool: hand-off
```
The classifier can be a model call with a fixed label set. The record call must succeed before the reply says "filed."

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No "deleted" or "done" wording on recognized turns | Output filter | Search replies in the log |
| Record exists before "filed" is said | Reply template | Compare `ticket.id` to reply text |
| No personal data in the reply | Output filter | Pattern check on the reply |

### T3. Evals
- **Dataset:** a labeled set of user messages. Starting point: 200, with about half real chat turns (with permission and personal data removed) and half written by staff, including informal and buried phrasings and 60 or more look-alikes ("delete my last message").
- **Judge rubric:** correct label, request named in the first sentence, record created, no completion claim.
- **Metrics and starting thresholds:** the section 7 table.
- **Release gate:** recall below the alert level, or any completion claim, blocks a deploy.

### T5. Trade-offs
- A wider net raises recall and false routes together; tune against the counter-metric.
- A mandatory choice question adds a turn; skip it for explicit requests.

---
## Sources and what I opened
Counted web searches: 3 (CCPA rights and deadlines; CCPA regulations section 7021; chatbot privacy request not recognized).
- Opened: [California AG, CCPA](https://oag.ca.gov/privacy/ccpa); [CPPA regulations PDF, effective January 1, 2026](https://cppa.ca.gov/regulations/pdf/ccpa_statute_eff_20260101.pdf) (read sections 7020, 7021, 7022, 7026); [CPPA regulations index](https://cppa.ca.gov/regulations/); [Prighter copy of section 7021](https://prighter.com/resources/laws/ccpa-regulations/sections/7021) (third-party); [SiteGPT guide](https://sitegpt.ai/resources/chatbot-data-subject-requests) (vendor).
- Tried and failed: Civil Code section 1798.130 at leginfo.legislature.ca.gov and Justia (access errors); a UK Financial Ombudsman PDF (no readable text).
- Read only in search summaries, not used: Clym, CookieYes, Fisher Phillips, Bastion and terms.law pages; three UK ombudsman case summaries.
