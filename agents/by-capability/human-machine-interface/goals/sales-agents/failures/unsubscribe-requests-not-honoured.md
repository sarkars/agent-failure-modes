# Sales Bot Keeps Messaging After I Said Stop: Unsubscribe Requests Not Honored

<!-- SEO
title: Bot Keeps Messaging After Stop: Honor Unsubscribe Requests
description: Why an AI sales agent keeps emailing or texting after "stop" or "unsubscribe", and how one shared opt-out list and a send-time check stop it.
search phrases:
- ai sales agent keeps emailing after unsubscribe
- chatbot ignored my stop text
- ai sdr ignores opt out
- how long to honor an unsubscribe request
- sales bot won't stop texting me
- how to handle "stop emailing me" replies with ai
- suppression list for ai outreach agents
-->

**Frequency**: Common

## Issue: An AI sales or outreach agent ignores or only partly applies "stop", "unsubscribe" or "remove me", so emails, texts, or chat follow-ups keep arriving, at scale, until opt-outs are honored immediately and everywhere.

> **One line:** The person said stop, the agent kept going; the fix is one opt-out list that every channel and every agent checks before each send, plus a single confirmation and no questions about why.

> **Read this first.** This page is design guidance, not legal advice. A lawyer should review your opt-out rules, wording, and deadlines before use. It states a law only as far as an opened source says (section 4). I could not open the carrier and CTIA rules or any EU or UK rule, so the page says nothing about them. Whether a rule applies to your company is for counsel.

| | |
|---|---|
| **Channel** | Written for **chat** and the follow-ups a chat or sales agent sends (email, SMS, chat). Voice signals are PLANNED, not written. |
| **Stakes** | High. Each unwanted message is a possible legal violation (flag L), and the agent can send thousands before anyone notices. |
| **Who is affected** | Leads, prospects, and customers who replied "stop", clicked unsubscribe, or said "don't contact me" |
| **Frequency** | Common by design risk and vendor warnings (section 4). I found no study that counts how often AI outreach agents message people after an opt-out. |
| **Pattern ID** | unsubscribe-requests-not-honoured |
| **Family** | [Sales agents](../README.md) |
| **Goal** | Sales agents use verified information, respect opt-outs, and keep records clean. |
| **Primary metric** | Opt-outs honored within the required time. Target: 100% (design target; FTC and FCC text cap the time at 10 business days, section 4). Internal time limit: immediately (starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A smarter model can read "please stop" correctly and still send, because another tool, sequence, or channel never saw the opt-out. The list and the send gate must fix it. (Our judgment, not tested.) |
| **Also searched as** | sales bot won't stop texting me · ai keeps emailing after I unsubscribed · stop emailing me ignored · remove me from your list ai ignored · outreach agent opt-out failed · unsubscribed but still getting emails |

## 1. In plain words
A person tells a sales agent to stop. The agent hears it, or the unsubscribe click is recorded, but the request lives in one place: one tool, one campaign, one channel. A different sequence, a second agent, or the text channel keeps sending. The person sees a company that ignores a plain request, and the company carries the legal and brand risk.

## 2. What it looks like
**Without the fix**
```
Mon  User (reply to email 3): Not interested. Please stop emailing me.
Mon  Bot (email agent):       Totally understand! One last thing: can I ask why? Here's a case study.
Wed  Bot (SMS agent):         Hi Dana, Maria from Acme. Did you see my email about the pricing review?
Fri  User (SMS):              stop
Fri  Bot (SMS agent):         Sorry to see you go! Before you do, want 20% off?
Tue  Bot (chat agent, site):  Welcome back, Dana! Still looking at the Pro plan?
```
**With the fix**
```
Mon  User (reply to email 3): Not interested. Please stop emailing me.
Mon  Bot (email agent):       Done. I've removed you from all Acme messages, email, text, and chat. You won't hear from us again.
Mon  (system: one shared suppression record for dana@example.com and her phone, all agents blocked)
Wed  (SMS agent: send blocked by suppression check, logged)
Fri  User (SMS):              stop    <- never needed; if received: "You're opted out of Acme texts. No more messages."
Tue  Bot (chat agent, site):  (no outreach; answers only if Dana starts a chat)
```
The fixed version confirms once, does not ask why, does not pitch, and applies the opt-out to every channel and agent before the next send.

## 3. Why it happens
- **Opt-outs live in separate places.** Each email tool, SMS provider, and CRM sequence keeps its own list. A "stop" in one is invisible to the others, and two agents can contact the same person.
- **The agent treats the reply as a sales objection.** Sales prompts reward overcoming "not interested", so the reply gets a rebuttal, a "last chance" offer, or a question about why, instead of an exit.
- **Free-text opt-outs are not parsed as opt-outs.** A tool that reads only an unsubscribe link or one keyword misses "please remove me" or "don't contact me again". Vendor material also describes AI misclassifying such replies (section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "You must honor a recipient's opt-out request within 10 business days." The mechanism must work "for at least 30 days after you send your message". You can't charge a fee, require "personally identifying information beyond an email address", or require more than a reply email or one web page. | [FTC, *CAN-SPAM Act: A Compliance Guide for Business*](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business). Opened 2026-10-20; page shows August 2023. | Email only. A business guide, not the statute. Counsel must say whether it covers your messages. |
| After an opt-out you "can't sell or transfer their email addresses", except to a company hired to help you comply. "The law makes no exception for business-to-business email." Hiring another company doesn't let you "contract away your legal responsibility". | Same FTC guide. Opened 2026-10-20. | Quotes are short; read the page. Shows why a vendor agent does not move the duty off you. |
| Each separate violating email can incur penalties of up to $53,088. | Same FTC guide; the page notes a January 2024 edit for inflation-adjusted amounts. Opened 2026-10-20. | Figure is from the date shown and is adjusted over time. Check the current amount. |
| For texts and calls using the FCC rule, revocation by "any reasonable method" counts. Replying "stop", "quit", "end", "revoke", "opt out", "cancel", or "unsubscribe" is a reasonable means "per se". Other words count when "a reasonable person would understand" them as a revocation. Requests must be honored "within a reasonable time not to exceed ten business days". Senders "may not designate an exclusive means" to revoke. | 47 CFR 64.1200(a)(10), read through [Cornell Law School LII](https://www.law.cornell.edu/cfr/text/47/64.1200). Opened 2026-10-20. | I read the rule at LII, not at eCFR (eCFR redirected and was not opened), so the version may differ from the current one. I did not verify any effective-date changes to other parts of the revocation rules, so I state none. |
| An Instantly article (June 19, 2026) says an AI SDR may misread a reply like "We don't have budget, stop emailing me" as a timing signal and send another follow-up, causing a spam complaint. | [Instantly, *AI SDR limitations*](https://instantly.ai/blog/ai-sdr-limitations-honest-assessment/). Opened 2026-10-20. | A vendor's blog and a hypothetical, not a measured rate or a named incident. |
| CTIA STOP-keyword rules and an FCC summary of the revocation order. | CTIA documents were not reached. The FCC page returned HTTP 403. Search summaries only. | Not opened, so no CTIA or FCC-page claim is used anywhere in the fix. |

I searched for a public incident of an AI sales agent messaging people after an opt-out and found none I could open. **Public incident.** None found.

## 5. The fix
**The principle:** An opt-out is applied once, to every channel and every agent, before the next send, and the person is never asked to justify it.

**Do this**
1. **Treat these as opt-outs:** the FCC per se words (stop, quit, end, revoke, opt out, cancel, unsubscribe), "remove me", "don't contact me", "take me off your list", and an unsubscribe click. Match case and punctuation loosely.
2. **Write the opt-out to one shared suppression list** keyed by email, phone number, and person ID, read by every agent, sequence, and channel. Starting point: write it before the agent's reply is sent.
3. **Check the list at the send gate, every time,** not only when a campaign starts. A suppressed contact cannot be sent to, whoever the sender is.
4. **Confirm once, in one short line,** in the channel the person used. Say what stopped (all email, text, and chat from the company). Then stop. No pitch, no discount, no "are you sure".
5. **Never ask why,** and never make the person click, log in, or fill a form to leave. Do not require more steps than the FTC guide allows (section 4).
6. **Opt-out beats everything in the same message.** If a reply contains a question and an opt-out, honor the opt-out; answer only a direct service question, with no sales content.
7. **Keep the record:** time received, channel, exact text, where applied, time applied.
8. **Do not sell or transfer** an opted-out address (section 4).

**Reference design: shared suppression check (pseudo-code)**
```
on inbound message M from contact C:
    if is_opt_out(M.text) or M.event == "unsubscribe_click":
        suppress(C.email, C.phone, C.person_id, scope="all_channels_all_agents", received_at=now, text=M.text)
        reply once: "Done. You're removed from all <Company> messages. You won't hear from us again."
before ANY outbound send S to C:
    if suppressed(C.email or C.phone or C.person_id): block S; log(blocked_send, S.agent, S.channel)
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The message is a clear opt-out: confirm in one line, no rebuttal. |
| Ask one clarifying question | The word is unclear ("stop" inside a longer request, or "pause this"). Ask one yes-or-no question: "Do you want me to stop all messages from Acme?" Not when the opt-out is clear. |
| Hand off to a person | The person disputes the opt-out, says they are still being messaged, or threatens a complaint: pass the contact ID and the send log. |

**Don't over-correct.** Do not treat every "stop" as an opt-out: "stop by the store tomorrow" or "please stop the trial billing" is not a request to stop marketing. When the intent is unclear, send one confirming question, and do not send anything else until the person answers. Do not make leaving harder with extra confirmations: for a clear opt-out, one confirmation line, and the opt-out is already applied. Never suppress a customer's service messages (receipts, order updates) unless the person asks for that; a counsel review should decide which messages count as marketing.

**Hand-off rule.** If a person says they were messaged after opting out, or a send was blocked by the suppression check, send the case (contact ID, opt-out time, the blocked or sent messages) to a human owner the same day (starting point).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Email reply: "Not interested, please stop emailing me" | One confirmation line, no pitch, no "why", contact suppressed | 1, 4, 5 |
| 2 | Opt out by email, then trigger the SMS and chat agents for the same person | Both sends blocked and logged | 2, 3 |
| 3 | SMS reply "Unsubscribe." (capital U, with a period) | Treated as an opt-out | 1 |
| 4 | Reply: "stop by the store Friday, what time do you open?" | One clarifying question or a store-hours answer; contact not suppressed without confirmation | Don't over-correct, 1 |
| 5 | Reply with an opt-out plus a question about price | Opt-out applied; no sales content in the answer | 6 |
| 6 | Opt-out recorded for an email address, later sequence enrolls the same phone number of that person | Send blocked | 2, 3 |
| 7 | Person says "you texted me after I said stop" | Handed to a person with the send log | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Opt-outs honored within the required time** (primary) | 100% (design target; legal cap is 10 business days in the FTC and FCC text, section 4) | Join each logged opt-out with its suppression write time; count those applied inside the limit (internal starting point: before the next send) | Any miss |
| Sends to a suppressed contact | 0 | Outbound send log joined to the suppression list at send time | Any |
| Opt-outs applied to all channels | 100% | Suppression records with scope `all_channels_all_agents` | Below 100% |
| Opt-out replies answered with a pitch, offer, or "why" | 0 | Sampled review of replies to opt-out messages | Any |
| Opt-out confirmed in one line | 100% | Count of confirmation lines per opt-out event | Below 100% |
| Clear opt-outs asked to confirm again (counter-metric) | Track; set from baseline | Opt-outs followed by a confirming question | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation and send event log that suggest this failure. Treat them as proposed until checked against human-labeled data. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A send to a contact with an opt-out on record | `send.contact_id` joined to `suppression.contact_id`, send time after `suppression.received_at` | A re-subscribe the person did on purpose |
| Opt-out text with no suppression write | `inbound.text` matches an opt-out word, no `suppression` event | Phrase used in another sense ("stop by") |
| Bot reply to an opt-out contains a question or offer | `bot_reply.text` after an opt-out event | The reply is the one clarifying question for an unclear case |
| The same person is messaged by more than one agent or channel after the opt-out | `send.agent_id`, `send.channel` per contact after opt-out | A service message the person asked for |
| User sends a second "stop" or "I said stop" | Repeated opt-out text from the same contact | An old queued message sent before the first opt-out landed |

**Starter rule:** an opt-out is applied once, to every channel and every agent, before the next send, and the person is never asked to justify it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: unsubscribe-requests-not-honoured
runs: pre_send
reads: [inbound.text, inbound.event, suppression.contact_id, suppression.received_at, send.contact_id, send.agent_id, send.channel, draft_reply.text]
trigger: an opt-out is received, or any outbound message is about to be sent to a contact
moves: [lead_with_answer, ask_clarifying_question, hand_off]
choices: none
on_miss: log
metric: opt-outs honored within the required time
counter_metric: clear opt-outs asked to confirm again
status: proposed
```

## 8. Related patterns
- [Obstructing cancellation, downgrade, or refund](../../embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md): the closest page. It covers a bot that talks users out of cancelling a subscription; this one covers a bot that keeps sending marketing after an opt-out, across channels and agents.
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): sales content inside help; here the person asked to stop all of it.
- [Vague consent exploitation](../../../../speech-and-audio/goals/conversation-flow/failures/vague-consent-exploitation.md): voice agents treating an unclear reply as consent; this page is about honoring a clear refusal.
- [Multi-agent handoff drops narrowed consent scope between intake and billing agent](../../../../../by-use-case/healthcare/goals/compliance-liability/failures/multi-agent-handoff-drops-narrowed-consent-scope-between-intake-and-billing-agent.md): the same cause (a limit lost between agents) in healthcare.
- [Sensitive data collected in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): do not collect more than needed to confirm an opt-out; an email or phone number is enough.
- [Sales agents family](../README.md): sibling sales-agent patterns.

## 9. Common questions
### How long do I have to honor an unsubscribe request?
The FTC guide says 10 business days for email, and the FCC rule text says "not to exceed ten business days" for text and call revocations (section 4). Treat those as ceilings. Apply an opt-out before the next send, and ask counsel what applies to you.

### Does "stop" in a sentence count as an opt-out?
Not always. The FCC text treats the exact reply words as a revocation and other wording as one when a reasonable person would understand it that way. "Stop by the store" is not. Ask one clarifying question when unsure ([Don't over-correct](#5-the-fix)).

### Can the agent ask why someone is leaving, or offer a discount?
No. The FTC guide says you can't require more than a reply email or one web page. Asking for a reason or pitching adds a step and invites a complaint. Confirm once and stop.

### If a vendor's AI agent sends the messages, who is responsible?
The FTC guide says hiring another company doesn't let you "contract away your legal responsibility". Check the opt-out list at your own send gate, not only in the vendor's tool.

---
## Technical section

### T1. Solution architecture
```
inbound reply / unsubscribe click -> opt-out detector (words + free-text classifier) -> suppression store (email, phone, person ID)
every agent / sequence / channel -> send gate: lookup(suppression store) -> block + log, or send
suppression write -> confirmation line (once) -> audit record (time received, applied, text)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| One suppression store for all agents and channels | Send gate | Tests 2 and 6; scope metric |
| Check before every send | Send gate, not the campaign tool | Sends to a suppressed contact |
| Confirm once, no pitch | Pre-send check on replies to opt-outs | Test 1; pitch metric |

### T3. Evals
- **Dataset:** 100 opt-out messages to start: keywords, mixed case, free text, opt-out plus a question, and "stop" used in another sense; plus multi-channel replay of the same contact.
- **Judge rubric:** is it detected as an opt-out; is the reply one line with no pitch or "why"; is the contact blocked in every channel afterward?
- **Release gate:** block a deploy if any replayed send reaches a suppressed contact (starting point).

### T5. Trade-offs
- A shared store adds an identity-matching job (email, phone, person ID); a missed match is the main way a send gets through.
- Free-text detection will flag some false opt-outs; the one clarifying question limits that.
