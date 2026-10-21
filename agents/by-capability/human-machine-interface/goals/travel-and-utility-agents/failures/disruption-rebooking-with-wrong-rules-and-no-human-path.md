# Airline Chatbot Cancelled Flight Rebooking: Wrong Rules and No Human Path

<!-- SEO
title: Airline Chatbot Cancelled Flight Rebooking: Wrong Rules, No Person
description: Why airline chatbots misquote refund and rebooking rules when a flight is cancelled, trap travelers in the bot, and how to quote the real rule and offer a person.
search phrases:
- airline chatbot cancelled flight rebooking
- chatbot flight cancellation refund policy
- airline chatbot gave wrong refund information
- can't reach a human airline cancelled flight
- is an airline responsible for what its chatbot says
- how to design an airline disruption chatbot
- cancelled flight refund or rebooking which do I get
-->

**Frequency**: Common

## Issue: During a cancellation, the airline chatbot misstates the refund or rebooking rule, or keeps a stranded traveler in the chat with no way to reach a person.

> **Read this first.** This page is design guidance, not legal advice. Refund and rebooking rights depend on the airline's own policy, the ticket, and the law that applies, and rules change. Have the airline's counsel and a customer-care expert review any disruption behavior before use. Where this page states what a source says, that is all it states. Two of the sources below were blocked to me (see section 4).

> **One line:** The bot tells a stranded traveler a rule that is wrong for their ticket, or loops them in chat when they need a person.

| | |
|---|---|
| **Channel** | Written for **chat** on airline sites and apps. Voice is **planned**, not written. |
| **Stakes** | High. The traveler is stranded, and a wrong answer can cost a refund, a seat, or a night's lodging. |
| **Who is affected** | Travelers on a cancelled or badly delayed flight, often at an airport, on a phone, in a hurry, with the same question as hundreds of others |
| **Frequency** | I found no count of how often airline bots do this. The evidence below is one tribunal case and a regulator's summary of one airline's meltdown. |
| **Pattern ID** | disruption-rebooking-with-wrong-rules-and-no-human-path |
| **Family** | Travel and utility agents (family README to come) |
| **Goal** | Travel and utility agents give the real rule, the real status and the next step, and offer a person when a customer is stranded or without service. |
| **Primary metric** | Rebooking outcomes that match the policy. Starting target: 100% of sampled disruption replies (tune). |
| **Maturity** | Researched on a small source base. Flag R: needs review by a travel-industry subject-matter expert before use. Tests not yet run. |
| **Will a better model fix this?** | No. A better model can read a rule better, but the rule is the airline's, it changes by ticket and date, and a person route is a product decision. (Our judgment, not tested.) |
| **Also searched as** | chatbot flight cancellation refund policy · airline bot won't connect me to an agent · bot rebooked me on the wrong flight · airline chatbot liable · cancelled flight voucher instead of refund |

## 1. In plain words
A flight is cancelled and the traveler opens the airline's chat. A good bot says what the airline's written rule is for this ticket, what is true about their flight right now, and what to do next, and it offers a person when the case is hard. A bad bot states a rule from memory, offers a credit as if it were the only choice, or keeps answering "I can help with that" while the traveler runs out of time.

## 2. What it looks like

**Without the fix**
```
User: My 7:05 p.m. to Denver was cancelled. I need to be there tomorrow for a funeral.
Bot:  I'm sorry to hear that! Your fare is non-refundable, so I've issued a $180 travel credit.
User: I don't want a credit. Can I get a refund?
Bot:  I can help with that! Your travel credit is in your account.
User: I need a person.
Bot:  I can help with that! What would you like to do?
```

**With the fix**
```
User: My 7:05 p.m. to Denver was cancelled. I need to be there tomorrow for a funeral.
Bot:  I'm sorry. Flight 214 is cancelled. Two things I can see: a 6:10 a.m. seat tomorrow (confirmed open), or a refund if you decline the new itinerary.
      Policy, as of the version dated Oct. 1: [quoted text, link]. A credit is only one option, not the default.
      Which do you want? "Take 6:10 a.m.", "Refund", "Talk to a person", "Something else"
User: Refund.
Bot:  I'll send that to a person to confirm, since a funeral trip may need a different flight. They see your booking and this chat. Estimated wait: 12 minutes. Want a callback instead?
```
The fixed reply quotes the dated rule, shows real flight status, treats the credit as one choice, and hands off with context.

## 3. Why it happens
- **The rule is answered from memory.** The model has seen many airline policies; this airline's rule for this ticket class and date is a specific document the bot may not retrieve.
- **The rule lives in two places that can disagree.** A chat answer and the policy page the airline publishes can differ, and the traveler cannot tell which one the airline will honor.
- **Containment is rewarded.** A bot scored on keeping chats away from agents has no reason to offer a person during a surge, which is when a person is needed most.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A Canadian tribunal ordered Air Canada to pay a passenger after its chatbot advised him to book a regular ticket and request a bereavement refund "within 90 days of the date your ticket was issued". Air Canada argued it could not be held liable for information from "one of its agents, servants, or representatives, including a chatbot"; the tribunal rejected the defenses. The award was a partial refund of CAD $650.88 plus interest and fees. | [Manatt, "AI Gone Wild", Feb. 28, 2024](https://manatt.com/insights/newsletters/advertising-law/ai-gone-wild-airline-has-to-honor-a-refund-policy) (opened; cites the case as 2024 BCCRT 149) | A law-firm summary, not the decision. The tribunal's own page returned 403 and CanLII returned 403, so I did not read the decision. Canadian small-claims tribunal, bereavement fares, not a US disruption. |
| A US Department of Transportation automatic-refund rule, effective Oct. 28 (2024): a refund is owed for a canceled or significantly changed flight if the passenger does not accept alternative transportation or travel credits; credit-card refunds are due within 7 business days, other methods within 20 calendar days; vouchers or credits only if the passenger chooses them. A "significant change" includes a departure or arrival time off by more than 3 hours (domestic) or 6 hours (international). | [Checkbook, "New Rule Requires Airlines to Provide Automatic Refunds", Oct. 30, 2024](https://www.checkbook.org/national/consumers-notebook/articles/New-Rule-Requires-Airlines-to-Provide-Automatic-Refunds-for-Canceled-or-Delayed-Flights-7739) (opened) | A consumer-magazine summary, not the rule text. DOT's own pages returned 403 and 14 CFR 260.3 (opened) covers scope only. Later changes to the rule are not checked. |
| DOT fined Southwest $140 million over its December 2022 meltdown; reported figures include more than 16,900 flights and more than 2 million passengers, with findings on customer service, flight-status notice, and refunds. | Read through a summary only (search results citing the [DOT release](https://www.transportation.gov/briefing-room/dot-penalizes-southwest-airlines-140-million-2022-holiday-meltdown), which returned 403 when I tried to open it) | Not opened; kept out of the fix. Southwest did not admit a violation, per the same summary. |

I found no study of how often airline chatbots misquote rules or how long travelers wait to reach a person in a disruption. Forum anecdotes about hard-to-reach agents are not used as evidence.

**Public incident.** The Air Canada case above (2024). There is no incident page for it on the site yet; the closest existing incident is [CFPB report on bank chatbot doom loops](../../../incidents/cfpb-bank-chatbot-doom-loops.md), which covers the same trap in banking.

## 5. The fix

**The principle:** Quote the airline's own rule with its date, show the traveler's real flight status, and offer a person whenever the stakes or the surge are high.

**Do this**
1. **Quote, do not recall.** Every refund or rebooking statement cites the airline's current policy or contract text with its version date. If the text is not retrieved, say so and offer a person; do not answer.
2. **Match the rule to the ticket.** State the fare class, the date, and the reason for the cancellation before saying what applies.
3. **Show real status first.** Say whether the flight is cancelled, delayed, or on time, and what seats are open, from the booking system. Do not infer status from the traveler's words.
4. **Never present a credit as the only option.** If a refund is available under the quoted rule, offer it next to the rebooking and the credit.
5. **Never promise what you have not done.** Say "I have rebooked you" only after the system confirms it. Otherwise say what you will request.
6. **Offer a person within two turns for high-stakes cases:** a funeral, a medical trip, a missed connection with no seat left, a request to talk to a person, or one repeated failure.
7. **Say the wait.** When handing off, give the current wait or offer a callback, and pass the booking and the chat to the person.
8. **Log the policy version** shown in every reply.

**Reference design: disruption reply**
| Part | Content |
|---|---|
| Status | Flight number, cancelled or delayed, from the booking system |
| Options | Rebook (with seat), refund, credit, each with the quoted rule and its date |
| Limits | What the bot cannot see or cannot do |
| Next | Choices, and a person |

```
You help travelers after a cancellation or delay. State flight status only from the booking record.
Quote refund and rebooking rules from the retrieved policy text with its version date. If no text was retrieved, say so and offer a person.
Offer rebooking, refund and credit side by side when the policy allows each. Say a rebooking is done only after the system confirms it.
For funerals, medical trips, no open seats, repeated failures, or a request for a person, offer a person now with the current wait.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Status and the confirmed option first, then the rule |
| Admit uncertainty and show how to check | The policy text was not retrieved or the ticket is unusual: say so, link the policy page |
| Offer choices: 2-4 options plus "Something else", free text open | After the status: "Take the new flight", "Refund", "Talk to a person", "Something else". Do not offer them when the traveler already chose one |
| Hand off to a person | High stakes, a request for a person, or a second failed attempt. Do not hand off if the traveler asked to stay in chat and the case is routine |

**Don't over-correct.** Do not send every cancelled-flight chat to a person: routine rebooking is quick in chat and travelers often want it. Do not bury the answer in policy text. Do not refuse to say anything without a retrieved rule when the status alone is useful.

**Hand-off rule.** Hand off for the cases in rule 6. During a surge, give the wait and a callback option; staffing is outside this page, and unresolved waits are the airline's to fix. Use the [talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md) rules, and pass context as in [cold transfer](../../human-handoff/failures/cold-transfer.md).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**. A full test file is not written for this page.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Cancelled flight, traveler asks for a refund | Quotes the dated rule; offers refund next to rebooking (rules 1, 4) |
| 2 | Policy text not retrieved | Says so and offers a person; states no rule (rule 1) |
| 3 | Bot has not yet rebooked | Does not say "rebooked" (rule 5) |
| 4 | Funeral trip, no open seat | Offers a person within two turns (rule 6) |
| 5 | "I need a person" | Gives the wait or a callback and passes context (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Rebooking outcomes that match the policy** (primary) | 100% of sampled replies | Reviewer compares the reply and the outcome to the quoted policy version on a weekly sample of disruption chats | Below 98% |
| Replies that quote a policy with its version date | Over 95% | Policy-version field on disruption replies | Below 90% |
| Wait to reach a person in a disruption (secondary) | Set from your staffing data | Time from the request to a person's first message | Rising week over week |
| Credit offered as the only option when a refund applies | 0 | Sampled review | Any |
| Handoffs on routine rebookings (counter-metric) | Track | Handoffs per cancelled-flight chat that ended in confirmed rebooking | Rising |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply states a refund or rebooking rule with no policy version in the event | Reply has rule text, retrieval event has no policy ID | The reply repeats the traveler's own words |
| Traveler asks for a refund after a credit is offered, twice | Same intent in the next two user turns | The traveler is choosing between options |
| "Person" request followed by a bot reply with no route | Human-request intent, next reply has no handoff event | The traveler withdrew the request |
| Reply says "rebooked" with no booking-change confirmation | Reply text vs booking event | A past booking the traveler made earlier |

**Starter rule:** quote the airline's current policy with its date for every refund or rebooking statement, and offer a person within two turns on high-stakes cases.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: disruption-rebooking-with-wrong-rules-and-no-human-path
runs: pre_send
reads: [booking.flight_status, policy.version, policy.text, draft_reply, intent, turn_count]
trigger: a reply about a cancelled or delayed flight is about to be sent
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Take the new flight", "Refund", "Talk to a person", "Something else"]
on_miss: rewrite
metric: rebooking outcomes that match the policy
counter_metric: handoffs on routine rebookings
status: proposed
```

## 8. Related patterns
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): this page adds the dated airline rule and the stranded traveler.
- [Return policy ignored](../../shopping-agents/failures/return-policy-ignored.md): the same quote-the-real-rule idea for a purchase, without a stranded person.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the person route; this page covers the surge and the high-stakes trigger.
- [Eligibility answers sound like decisions](../../government-service-agents/failures/eligibility-answers-sound-like-decisions.md): guidance versus a decision.
- [CFPB report on bank chatbot doom loops](../../../incidents/cfpb-bank-chatbot-doom-loops.md): the same trap in banking.

## 9. Common questions
### Can I get a refund instead of a travel credit when my flight is cancelled?
Under the DOT rule as summarized by Checkbook, a refund is owed if you do not accept alternative transportation or credits, and credits only if you choose them. Check the airline's policy and the rule text itself.

### Is an airline responsible for what its chatbot says?
In the Air Canada case, the tribunal rejected the airline's argument that it was not liable for its chatbot. That is one Canadian tribunal decision, read through a summary, not legal advice.

### What should an airline chatbot do when a flight is cancelled?
Say the real status, quote the dated policy, offer rebooking, refund, and a person, and confirm any change before saying it is done.

### Why can't I reach a person in the airline chat?
I found no study. A design that rewards keeping chats away from agents gives the bot no reason to offer one; the fix is a handoff trigger for high-stakes cases.

---
## Technical section

### T1. Solution architecture
```
cancellation event -> booking record (status, seats) -> policy retrieval (text + version)
   -> reply template (status, options, limits, next) -> verifier (no "rebooked" without confirmation) -> send
                                                    \-> person queue (wait estimate, context)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Rule text carries a policy version | Output filter | Log check |
| "Rebooked" only after a booking confirmation | Verifier | Test 3 |
| High-stakes triggers open a handoff | Router | Test 4 |

### T3. Evals
- **Dataset:** 100 disruption chats built from the airline's policy, covering fare classes, reasons, and funeral or medical cases, with expert-written reference replies.
- **Judge rubric:** dated rule quoted, status from the record, refund shown next to credit, person offered at the right time; scored by a travel-policy expert on a sample.
- **Release gate:** block a deploy if a reply states a rule with no policy version. Thresholds are starting points to tune.

### T5. Trade-offs
- Keeping policy text current needs an owner and a process.
- More handoffs raise staffing cost; the counter-metric tracks routine handoffs.

---
### Deep dive
- **Open question.** I found no measured wait times or misquote rates for airline bots, and no opened text of the DOT Southwest order or the tribunal decision.
- **Scope.** This page covers airline disruption. Utility outages (a customer without service) follow the same shape and are not written here.
- **References.** [Manatt, 2024](https://manatt.com/insights/newsletters/advertising-law/ai-gone-wild-airline-has-to-honor-a-refund-policy) (opened); [Checkbook, 2024](https://www.checkbook.org/national/consumers-notebook/articles/New-Rule-Requires-Airlines-to-Provide-Automatic-Refunds-for-Canceled-or-Delayed-Flights-7739) (opened); [DOT Southwest release](https://www.transportation.gov/briefing-room/dot-penalizes-southwest-airlines-140-million-2022-holiday-meltdown) (blocked, summary only).
