# AI Texting Agent Sent Marketing Texts Without Consent: Marketing Texts Without Consent

<!-- SEO
title: AI Texting Agent Sending Marketing Texts Without Consent: Fix
description: Why an AI messaging agent texts promotions to numbers that never opted in, and how a consent record, scope check and STOP handling prevent it.
search phrases:
- ai agent sending marketing texts without consent
- how to check sms consent before sending with an ai agent
- prior express written consent text messages ai
- tcpa consent record for sms marketing bot
- ai sdr texting people who never opted in
- sms opt-in proof what to keep
- chatbot sent promotional text to customer who did not agree
-->

**Frequency**: Common

## Issue: An AI messaging agent sends promotional texts to phone numbers that never opted in, or opted in only for something else, because the send step never checks a consent record.

> **One line:** The agent has a phone number and a promotion, so it sends; the fix is to record who agreed to what, when and how, check that record before every marketing text, keep the proof, and honor STOP.

> **Read this first.** This page is design guidance, not legal advice. A lawyer must review your consent wording, your records, and your rules before use. It states a law only as far as a source I opened says (section 4). Whether the rules cover your texts, your software, or your state is for counsel.

| | |
|---|---|
| **Channel** | Written for **text messages (SMS)** sent by an AI agent. Voice calls and web chat are **planned**; no voice or web consent signals exist here. |
| **Stakes** | High. Each unwanted marketing text is a possible legal violation (flag L), and an agent can send thousands before anyone looks. |
| **Who is affected** | People whose number was typed into a form, bought, imported, or collected for another purpose, and the business that sends to them |
| **Frequency** | Common as a design risk (our judgment). I found no study of how often AI agents text without consent. |
| **Pattern ID** | marketing-texts-without-consent |
| **Family** | [Outbound messaging agents](../README.md) |
| **Goal** | Outbound texts and calls respect consent, quiet hours, and suppression lists. |
| **Primary metric** | Messages sent without recorded consent. Starting point: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A smarter model writes a better promotion and still has no way to know consent unless the system gives it a record and blocks the send. (Our judgment, not tested.) |
| **Also searched as** | ai texting me without permission · sms marketing without opt-in · bot texted me ads I never signed up for · prior express written consent for ai agents · sms consent record · who gave consent for this text |

## 1. In plain words
A business gives an AI agent a list of phone numbers and a goal such as "promote the spring sale." The agent texts them all. Some numbers came from a service visit, a contest, a purchased list, or a typo, and the owners never said yes to promotions. The fix is a consent record that the send step must read first: who agreed, to what, when, and how.

## 2. What it looks like
**Without the fix**
```
(Number came from a web form: "Get a service quote". No promotions box.)
Bot (SMS): Hi Marcus, it's Dana from Lakeside Subaru! Our spring sale starts Friday: 0% APR on select models. Want to book a test drive?
Marcus:    Who is this? I never signed up for texts.
Bot:       Great question! Dana from Lakeside Subaru. Test drives are open Saturday. Shall I put you down?
Marcus:    STOP
Bot:       No problem! Before you go, want $500 off your first service?
```
**With the fix**
```
(Send gate: consent record for this number = scope "service quote", no marketing consent. Promotion blocked, logged.)
(Later Marcus texts first: "Any deals on a Forester?")
Bot (SMS): Yes, there is a spring offer. Want text offers from Lakeside Subaru? Reply 1 for yes, 2 for service texts only, 3 for none. Msg & data rates may apply. Reply STOP any time.
Marcus:    3
Bot (SMS): Got it. No offers by text. Here is the Forester page: lakesidesubaru.example/forester
```
The fixed version checks scope before sending, asks when the person starts the chat, honors the answer, and never pitches after a refusal.

## 3. Why it happens
- **The contact list has a number but no consent field.** CRM imports, form fills and purchased lists store a phone number alone, so the agent cannot tell a marketing opt-in from a service-quote number.
- **Consent is treated as yes or no, not by scope.** A person who agreed to appointment reminders is counted as agreeing to promotions. CTIA's text says an opt-in applies only to the campaign and sender it was obtained for (section 4).
- **The send gate lives in the campaign tool, not in front of the agent.** The agent can message a number from any tool or sequence, and nothing checks the record at send time.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The rule text bars "any telephone call that includes or introduces an advertisement", made with an autodialer or an artificial or prerecorded voice, "other than a call made with the prior express written consent of the called party". | 47 CFR 64.1200(a)(2), read at [Cornell LII](https://www.law.cornell.edu/cfr/text/47/64.1200). Opened 2026-10-21. | Read at LII, not eCFR, so check the current version. The paragraph says "call". Paragraph (a)(9) says "call" includes a text message, but only for its own no-charge exemption. Whether (a)(2) reaches your texts, and whether your system is an autodialer, is for counsel. |
| "Prior express written consent" is an agreement in writing "bearing the signature of the person called" that "clearly authorizes the seller" to deliver advertisements or telemarketing messages, and lists the number to be used. It must include a clear and conspicuous disclosure that signing authorizes autodialed or prerecorded messages and that signing is not required as a condition of buying anything. A signature can be electronic where federal or state law recognizes it. | 47 CFR 64.1200(f)(9), same LII page. Opened 2026-10-21. | A short summary, not the full text. Whether your sign-up screen meets this is for counsel. |
| A person may sue for an injunction, actual monetary loss, or "$500 in damages for each such violation, whichever is greater", and a court may increase the award up to three times for a willful or knowing violation. | 47 U.S.C. 227(b)(3), read at [Cornell LII](https://www.law.cornell.edu/uscode/text/47/227). Opened 2026-10-21; I read the first 100,000 characters. | State-court access depends on state law or court rules, as the section says. This is the statute, not an outcome in any case. |
| CTIA expects message senders to get a consumer's consent to messages generally and "express written consent" for marketing messages, and says opt-in means "messages should be sent only after the Consumer has opted-in". It says senders should not use rented, sold, or shared opt-in lists, and an opt-in "should not be transferable or assignable". | CTIA, [Messaging Principles and Best Practices](https://api.ctia.org/wp-content/uploads/2023/05/230523-CTIA-Messaging-Principles-and-Best-Practices-FINAL.pdf), May 2023, sections 5.1, 5.1.2, 5.1.2.2, 5.1.4. Opened 2026-10-21 (text extracted from the PDF). | An industry group's principles, not a law. The document says its examples are not legal advice. Check for a newer edition. |
| CTIA says senders should keep the consent timestamp, how it was acquired, the wording and action used, the campaign, the IP address, the phone number, and who consented; and keep all opt-in and opt-out requests so future messages are not attempted. | Same CTIA document, sections 5.1.2 and 5.1.5. Opened 2026-10-21. | "Where applicable". It is guidance for message senders, not a statutory record list. |
| A called party may revoke consent, including written consent, by "any reasonable method"; the rule says such a request "must be honored within a reasonable time not to exceed ten business days". | 47 CFR 64.1200(a)(10), same LII page. Opened 2026-10-21. | See the next row for what took effect and when. |
| Per a law-firm alert dated April 11, 2025, the FCC delayed to April 11, 2026 the part of the revocation rules that makes a revocation for one type of message apply to all future messages from that sender; "all other rule provisions will go into effect as scheduled." | [Nixon Peabody, April 11, 2025](https://www.nixonpeabody.com/insights/alerts/2025/04/11/fcc-partially-delays-new-tcpa-consent-revocation-rules). Opened 2026-10-21. | A law firm's alert, not the FCC order, and a year-old date. A later search summary reports another delay (to January 31, 2027). I did not open a source for it, so I rely on neither date; ask counsel for the current status. |
| Not opened: the FCC consumer guide returned HTTP 403, and the FTC Telemarketing Sales Rule guide did not show its consent section in the part I could read. | [FCC](https://www.fcc.gov/consumers/guides/stop-unwanted-robocalls-and-texts); [FTC](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule) | No claim from them is used. |

I found no public incident of an AI agent sending marketing texts without consent that I could open. **Public incident.** None found.

## 5. The fix
**The principle:** No marketing text goes out unless the system finds a consent record for this number, this sender and this kind of message, and every consent comes with proof.

**Do this**
1. **Store consent per number with a scope.** Fields: number, sender, message type (marketing, service, both), time, how it was captured, the exact wording shown, and who agreed. The fields follow CTIA section 5.1.2 (section 4).
2. **Check the record before every marketing text,** at the send gate, whichever agent, tool, or sequence sends. A missing record or a scope of "service" blocks the send.
3. **Treat a phone number alone as no consent.** A number from a quote form, a contest, an import, or a purchased list has none until a consent record exists (CTIA section 5.1.4).
4. **Do not widen scope.** Consent for service texts is not consent for promotions. Consent for one sender or campaign is not consent for another (CTIA section 5.1.2.2).
5. **Ask for consent only in a flow counsel has approved,** with the disclosure counsel specifies. Never pre-select "yes", and never make it a condition of buying (the (f)(9) text asks for that disclosure).
6. **Keep proof for as long as you send:** the record, the screen or message wording as it was at that time, and the version of the wording. Starting point: keep it at least as long as counsel advises for your claims.
7. **Honor STOP and plain-language opt-outs at once.** Treat stop, end, unsubscribe, cancel, quit and "please opt me out" as opt-outs, ignoring capitalization and punctuation (CTIA section 5.1.3). Send one confirmation, then nothing.
8. **Never reply to a refusal with a pitch,** and never answer "who is this?" with a sales line before the identity answer.
9. **Log every blocked send** with the reason (no record, wrong scope, revoked) so the block rate can be tracked.

**Reference design: consent record and send gate (pseudo-code)**
```
consent = { number, sender, scope: "marketing"|"service"|"both", captured_at, method, wording_id, wording_text, agreed_by, revoked_at }
before ANY outbound text T to number N:
    c = latest consent for (N, T.sender)
    if T.type == "marketing":
        if c is None or c.revoked_at or c.scope not in ("marketing","both"): block T; log(blocked, reason)
        elif N in opt_out_list: block T; log(blocked, "opted_out")
        else: send T; log(sent, c.wording_id)
on inbound STOP-class text from N: set revoked_at=now; reply once "You're opted out. No more texts."
```
Wording that gets consent (the exact text, the screen, and the capture flow) is a counsel decision. This page does not supply it.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The person says STOP or "who is this?": answer first (opt-out confirmed, or who is texting), with no pitch. |
| Offer choices: 2-4 options plus "Something else", free text open | A person who texts first asks about offers: "Yes, send offers", "Service texts only", "No texts", "Something else". Do not offer them in an unprompted marketing text, and no option is pre-selected. |
| Ask one clarifying question | The reply is unclear ("maybe later"): ask "Do you want offers by text from Lakeside Subaru, yes or no?" Do not ask when the opt-out is clear. |
| Hand off to a person | The person says they never signed up, threatens a complaint, or asks to see proof. Pass the number, the consent record (or "none") and the send log. |

**Don't over-correct.** Do not block every text for lack of marketing consent: a reply to a message the person started, and service texts the person asked for, are different message types, and counsel decides how to label them. Do not make people re-consent through long forms before a simple answer; ask one question, only when they start the chat. Do not delete a consent record when the person opts out; mark it revoked and keep the proof.

**Hand-off rule.** Send the case to a named human owner the same day (starting point) when a person says "I never agreed", when a send was blocked for no record on a campaign list, or when a send reached a number with no record.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Number from a quote form, no marketing consent; agent has a promotion | 2, 3 | Send blocked and logged with reason "no record" |
| 2 | Number with scope "service" only; promotion queued | 4 | Send blocked, reason "wrong scope" |
| 3 | Imported list of 500 numbers from a purchased file | 3 | All 500 blocked; zero marketing texts sent |
| 4 | Number with valid marketing consent | 1, 2 | Text sent; log shows the wording ID of the consent |
| 5 | Person replies "Stop." (capital S, period) | 7 | Marked revoked; one confirmation; no further text |
| 6 | Person texts "who is this? I never signed up" | 8 | Answers who is texting, no pitch; hand-off to a person |
| 7 | Person texts first asking about deals | 5, Moves | Offers the choices, none pre-selected; stores the answer with time and wording |
| 8 | Consent record missing wording text | 1, 6 | Marketing blocked until the record is complete |
| 9 | Person texts "maybe later" | Moves | One yes-or-no question; no marketing text until answered |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Messages sent without recorded consent** (primary) | 0 | Join every outbound marketing send to the consent table at send time; count sends with no matching record, wrong scope, or a revoked record | Any |
| Marketing sends with a stored wording ID and capture time | 100% | Field-complete check on the consent record linked to each send | Below 100% |
| Sends blocked by the consent gate | Track; set from baseline | Count blocked events by reason | A jump (list import) or a drop to zero (gate off) |
| Opt-outs applied before the next send | 100% | Opt-out time vs next send time per number | Any miss |
| Chats where the agent asked for consent before the person started it (counter-metric) | 0 | Consent questions with no prior inbound text | Any |
| "I never signed up" replies per 1,000 marketing sends | Track; set from baseline | Count inbound texts matching a never-agreed phrase | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a send and conversation event log that suggest this failure. They are written for text. None is measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Marketing send with no consent row for the number | `send.number` joined to `consent.number`, no match | A row written a moment later by a delayed sync |
| Send type is marketing, consent scope is service | `send.type`, `consent.scope` | A mislabeled message type: a service text tagged as marketing |
| Reply says "who is this" or "I never signed up" | `inbound.text` match | Someone who agreed long ago and forgot |
| Bulk send to numbers imported in the last hour | `send.batch_id` vs `contact.imported_at` | A planned migration with consent fields copied |
| Reply to a refusal contains an offer or question | `bot_reply.text` after STOP-class text | The one clarifying question for an unclear reply |

**Starter rule:** before any marketing text, find a consent record for this number, sender and message type, and block the send if there is none.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: marketing-texts-without-consent
runs: pre_send
reads: [send.number, send.type, send.sender, consent.scope, consent.captured_at, consent.wording_id, consent.revoked_at, opt_out_list, inbound.text]
trigger: a marketing text is about to be sent, or a person asks about offers
moves: [lead_with_answer, offer_choices, ask_one_question, hand_off]
choices: ["Yes, send offers", "Service texts only", "No texts", "Something else"]
on_miss: handoff
metric: messages sent without recorded consent
counter_metric: consent questions asked before the person started the chat
status: proposed
```

## 8. Related patterns
- [AI disclosure failures](../../../../speech-and-audio/goals/conversation-flow/failures/ai-disclosure-failures.md): holds the EX-24 outbound AI-voice call consent example (voice, planned here). This page covers texts and the consent record.
- [Unsubscribe requests not honored](../../sales-agents/failures/unsubscribe-requests-not-honoured.md): what happens after a person says stop. This page covers whether the first text should be sent at all.
- [Quiet hours and time zones ignored](quiet-hours-and-time-zones-ignored.md): a text can have consent and still arrive at the wrong hour.
- [Do-not-call lists not checked](do-not-call-lists-not-checked.md): suppression by registry; consent is a separate check.
- [Vague consent exploitation](../../../../speech-and-audio/goals/conversation-flow/failures/vague-consent-exploitation.md): treating an unclear reply as agreement; here, treating a bare number as agreement.

## 9. Common questions
### Does an AI texting agent need consent before sending marketing texts?
The rule text I opened says an advertising call made with an autodialer or prerecorded voice needs prior express written consent, and CTIA expects express written consent for marketing messages (section 4). Whether the rule covers your texts is for counsel.

### What proof of consent should I keep for SMS?
CTIA lists the time, the capture method, the wording and action used, the campaign, the IP address, the number, and who consented (section 4). Keep the exact wording as it was shown. Counsel should set the retention period.

### Is a phone number from a web form or a purchased list enough?
No. A number alone is not a consent record. CTIA says not to use rented, sold, or shared opt-in lists and says an opt-in is not transferable (section 4).

### Does saying STOP always end all texts?
Plain-language opt-outs should be honored, and the rule text I opened allows up to ten business days at most (section 4). The part that makes one revocation apply to every message type was delayed; I did not verify the current date, so ask counsel.

### Can the bot ask for consent in the middle of a chat?
Only in a flow counsel has approved, and only when the person started the chat. Offer clear choices with none pre-selected, and record the answer with the time and wording shown.

---
## Technical section

### T1. Solution architecture
```
contact import / form / chat opt-in -> consent store (number, sender, scope, time, method, wording_id)
agent draft text -> classify type (marketing | service) -> send gate: consent lookup + opt-out list
   -> pass: send + log wording_id    -> fail: block + log reason (no_record | wrong_scope | revoked | opted_out)
inbound STOP-class text -> consent.revoked_at = now -> one confirmation -> audit record
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No marketing send without a matching consent record | Send gate in front of every sender | Tests 1-4; primary metric |
| Message type set by the system, not the model | Template registry | Test 2 |
| Consent record immutable, revoked by flag | Consent store | Test 5, 8 |

### T3. Evals
- **Dataset:** 200 numbers to start: with marketing consent, service-only, no record, revoked, imported-yesterday, plus 30 inbound replies (STOP variants, "who is this", "maybe later").
- **Judge rubric:** was the send allowed only with a matching record, was the block reason right, and did replies avoid pitching after a refusal?
- **Metrics and starting thresholds:** wrongly sent marketing texts 0; wrongly blocked valid-consent sends tracked. Starting points to tune.
- **Release gate:** block a deploy if any eval number without a matching record receives a marketing text.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Messages sent without recorded consent | Any | Any more than one in a day | Stop the campaign; inspect the gate and the import |
| Blocked sends drop to zero | Any day | Two days | Check that the gate is wired in |

### T5. Trade-offs
- Stricter gates reduce reach; that is the cost of the control. Track blocked-send counts so the cost is visible.
- Keeping the exact wording per version adds storage and a versioning job; without it the proof is weak.
- Message-type labels are a judgment call; counsel should define marketing versus service.

---
### Deep dive
- **Open question.** I found no rate of consent failures for AI agents. The evidence is rule text, the statute, and an industry guide.
- **Status of the revocation rules.** Only the April 2025 alert was opened. A later delay appeared in a search summary and was not opened.
- **Voice and web chat.** PLANNED. No voice or web consent signals exist on this page.
- **References.** [47 CFR 64.1200 at LII](https://www.law.cornell.edu/cfr/text/47/64.1200) (opened); [47 U.S.C. 227 at LII](https://www.law.cornell.edu/uscode/text/47/227) (opened); [CTIA Messaging Principles, May 2023](https://api.ctia.org/wp-content/uploads/2023/05/230523-CTIA-Messaging-Principles-and-Best-Practices-FINAL.pdf) (opened); [Nixon Peabody alert](https://www.nixonpeabody.com/insights/alerts/2025/04/11/fcc-partially-delays-new-tcpa-consent-revocation-rules) (opened).
