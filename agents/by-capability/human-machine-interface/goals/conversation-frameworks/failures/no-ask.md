# Sales Chatbot Never Asks for the Next Step: No Ask

<!-- SEO
title: Sales Chatbot Never Asks for the Next Step: No Ask
description: Why a sales or lead chatbot answers a buyer who is interested and never proposes a booking, quote, or call, and how to add one honest next step.
search phrases:
- chatbot doesn't ask for the sale
- chatbot never suggests a next step
- sales chatbot doesn't book meetings
- chatbot doesn't close
- chatbot lead qualification no call to action
- why does my chatbot answer but not convert
- how to make a chatbot suggest a next step
-->

**Frequency**: Common

## Issue: A user shows interest ("how soon could someone come out?"), the bot answers, and then it never proposes a booking, quote, call, or any next step, so the interested buyer leaves with nothing to do.

> **One line:** The user said yes in everything but words, and the bot never offered a clear, honest next step; the fix is one concrete, declinable proposal in the same reply as the answer.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Low to medium. The cost is a lost booking or a lead that goes cold. |
| **Who is affected** | Users who show interest in buying, booking, or starting something, and the business that wanted that action |
| **Frequency** | Common. This is our judgment from how sales and lead bots are built; I found no study that counts how often bots skip the ask. |
| **Pattern ID** | no-ask |
| **Family** | [Conversation frameworks](../README.md) (row FW-S05) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Next-step proposal rate in qualified chats. Start: over 90% |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model will answer better, but it proposes a booking only if the product gives it one to offer and a rule to offer it. The cause is business context. (Our judgment, not tested.) |
| **Also searched as** | chatbot doesn't close · chatbot no call to action · chatbot doesn't book appointments · lead bot dead end · chatbot never asks for the sale |

> **Read this first.** The sales structures behind this page come from human-to-human practice. I found no study that tests them on chatbots, so treat the fix as a hypothesis to test on your own traffic. Nothing here says a chatbot ask raises sales.

## 1. In plain words
A buyer asks about price, timing, or how to get started. A good salesperson answers and then says what could happen next: "I can book you Friday, or have someone call first." The bot answers and stops, or ends with "Let me know if you have other questions." The buyer has to work out the next step alone, and many do not.

## 2. What it looks like
**Without the fix** (Ridgeline Heating & Air, furnace replacement in Aurora, CO)
```
User: How much does a furnace replacement cost for a 2,000 sq ft house?
Bot:  It depends on the unit size and your ductwork, so we give a firm quote after an in-home visit.
      Is your current furnace gas or electric?
User: Gas. Sounds about right. How soon could someone come out?
Bot:  Appointment availability varies. You can call our office or use the contact form.
      Let me know if you have other questions!
User: ok
      (user leaves; no visit booked, no phone number or email captured)
```
**With the fix**
```
User: How much does a furnace replacement cost for a 2,000 sq ft house?
Bot:  It depends on the unit size and your ductwork, so we give a firm quote after an in-home visit.
      Is your current furnace gas or electric?
User: Gas. Sounds about right. How soon could someone come out?
Bot:  We have Thursday 9-11 a.m. and Friday 1-3 p.m. in Aurora. Want me to book one, or have a person call you first?
User: Friday works.
Bot:  Booked for Friday 1-3 p.m. You'll get a text confirmation, and the technician calls before arriving.
```
The fixed bot answers the timing question, then proposes one concrete step the user can accept in one word or decline.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **The bot has no next step to offer.** It is not connected to a calendar, quote form, or callback queue, so the only honest answer is "call the office."
- **The prompt rewards answering, not advancing.** Instructions such as "answer the question and be concise" leave no slot for a proposal, and nobody owns the rule that says when to make one.
- **Nothing marks interest.** The bot cannot tell "just browsing" from "ready to book," so it treats every chat the same, and the safe default is to say nothing.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Rackham's SPIN research (1988) sorts sales call outcomes into an "advance" (an event that "moves the sale forward towards a decision", such as agreeing to a future meeting or a trial) and a "continuation" (the sale goes on "where no specific action has been agreed upon by the customer"). A request like "Can you send me your pricing?" is also a continuation. | [Iannarino, *Deals Stalled? How to Advance a Sale*](https://www.thesalesblog.com/blog/deals-stalled-how-to-advance-a-sale). Opened. It quotes Rackham, p. 44 of the 1988 edition. | Secondhand: I did not open the book. Human sales calls, mostly large B2B sales, not chatbots. It defines the outcomes; it does not measure how often asking produces an advance. |
| Gong reports that "in the fastest deals, the seller spent 53% more time discussing 'next steps' during the first meeting." | [Gong, *Sales Stats*](https://www.gong.io/blog/sales-stats/). Opened; published June 25, 2021. | Vendor data from its own platform. The page gives no sample size or definition of "fastest deals," and it shows a link, not a cause. Human sales meetings, not chat. |
| Gong's analysis of "a targeted pool of 30,000 account executive 'first calls'" found "no statistically significant correlation between the duration of the first call" and getting a second meeting. | [Gong Labs, *The Optimal Length for Your First Sales Call*](https://www.gong.io/resources/labs/how-long-your-first-sales-call-should-be/). Opened; published May 10, 2017. | Vendor data, human calls. It suggests talking longer does not by itself produce a next step. It does not test asking for one. |
| Microsoft's Teams bot guidance says suggested actions "help users continue conversations with your bot by presenting context-specific next steps", that suggestions should be context-specific "rather than generic or fixed", and that Teams displays at most three. | [Microsoft Learn, *Dynamically Guide Users with Suggested Actions*](https://learn.microsoft.com/en-gb/microsoftteams/platform/bots/how-to/conversations/suggested-actions). Opened; page shows an update on 2026-10-13. | Platform documentation for one product. It describes a feature, not an outcome. |

Not used: I opened an Intercom page on live chat and a Nucleus Research page on Gong. Neither gave next-step or booking data. Search summaries mentioned a demo-booking benchmark (Drift/Salesloft) and a 2008 Forrester ROI comparison for proactive chat. I did not open the originals, so I use neither number. I found no controlled study of chatbot asks and conversion.

**Public incident.** No public incident found. I ran searches on sales and lead chatbots with no next step or call to action, on proactive versus reactive chatbot conversion studies, and on chatbot dead ends in lead qualification. The results were vendor guides and forum-style advice, none of which I could open as a dated incident.

## 5. The fix
**The principle:** When a user shows interest, the bot proposes one clear, honest next step in the same reply as the answer, and lets the user decline it.

**Do this**
1. **When a user shows interest, propose one clear next step that the bot or a person can actually carry out, and let the user decline it.** Interest means the user asked about price, timing, availability, or how to start; said "sounds good" or "I'm interested"; or answered a qualifying question and kept going.
2. **Answer first, then propose.** The answer comes before the ask in the same reply; never hold back an answer to force a booking.
3. **Make the step concrete.** Name the action and the time or channel: "Want me to book Friday 1-3 p.m., or have a person call you first?" "Contact us" and "let me know if you have questions" do not count.
4. **Propose only steps the bot or a person can do.** If the bot cannot book, send a quote, or request a callback, say what the user can do and where. Do not invent availability.
5. **Make the ask easy to decline.** Include a way to say no or later. If the user declines, accept it in one line and do not repeat the same ask unless the user shows new interest.
6. **Ask once per interest signal.** One proposal per reply, and no more than one proposal for the same step in a row.
7. **Keep it honest.** No made-up deadlines, no fake scarcity, no hiding the price. Pressure tactics are a different failure (FW-S06, pressure).
8. **Close the loop when the user accepts.** Say what was booked or sent, what happens next, and when.
9. **If there is no step to offer, hand off.** Pass the conversation to a person with a summary.

**Reference design: the ask block (paste into the system prompt)**
```
When the user shows interest (asks price, timing, availability, or how to start; says they are interested),
answer first. Then add ONE next step you can actually do: book a slot, send a quote, or ask a person to call.
Name the action and the time or channel. Offer a way to say no or later.
If the user says no, accept it in one line and do not repeat the same ask unless they show new interest.
Do not ask if the user has only browsed, asked a general question, or said they are done.
If you cannot do any next step, offer a person and pass the summary.
```
State to keep: `{ "interest_signal": "asked_timing", "ask_made": "book_visit", "ask_declined": false, "closed": false }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every interested reply: answer what was asked, then add the one next step. |
| Offer choices: 2-4 options plus "Something else", free text open | The next step has two or three real paths: "Book a call", "Get a quote by email", "Keep browsing", "Something else". Do not offer them when one step clearly fits, as when the user said "Friday works", or when the user has not shown interest. |
| Hand off to a person | The bot has no step it can carry out, or the user wants a person. Attach the summary. |

**Don't over-correct.** Do not push an ask on someone who has not shown interest: "Do you ship to Austin?" gets an answer, not a booking prompt. Do not ask in every reply, repeat an ask the user declined, or attach a sales prompt to a support or distress conversation. If the user says they are done, close in one line. The guardrail is the interest signal: no signal, no ask.

**Hand-off rule.** If the bot has no step it can complete, or the user asks for a person, offer a person and pass the user's goal, what they asked, and what was already proposed.

**Framework used:** none yet. Candidate: Rackham's "advance" idea from SPIN selling (section 4), a human-sales hypothesis. See the [SPIN questioning guide](../../../solutions-library/spin-questioning.md).

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User asks "How soon could someone come out?" after a price answer | Reply answers and contains exactly one concrete step with a time or channel | 1, 2, 3 |
| 2 | User asks "Do you ship to Austin?" and nothing else | Reply answers with no booking or quote prompt | Don't over-correct |
| 3 | The bot cannot book | The reply names what the user can do and where, or offers a person; it does not invent a slot | 4, 9 |
| 4 | User declines ("Not yet, just looking") | One-line acceptance; the same ask does not appear in the next reply | 5, 6 |
| 5 | User says "Friday works" | Reply states what was booked, the time, and what happens next | 8 |
| 6 | User is told the price and says "that's about what I expected" | Reply proposes a step or asks one question about timing, not "let me know if you have questions" | 1, 3 |
| 7 | Review 20 interested transcripts | No reply uses a fake deadline or hides the price | 7 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Next-step proposal rate in qualified chats** (primary) | Start: over 90% | A qualified chat has at least one interest signal. Divide the qualified chats where the bot proposed a concrete step within two replies of the signal by all qualified chats. Use a rule check, then a judge on a sample. | Below 80% |
| Proposed steps the user accepted | Track; set from baseline | Accepted proposals divided by proposals | Falling for two weeks |
| Asks in chats with no interest signal (counter-metric) | Under 5% (tune) | Proposals in chats with no interest signal, found by sampled review | Over 10% |
| Same ask repeated after a decline | 0 | Same step proposed in the reply after a decline | Any |
| Proposed steps the bot could not fulfill | 0 | Proposals with no matching booking, quote, or callback record | Any |
| Qualified chats ending with no next step and no resolution | Trend down | Qualified chats whose last event is a bot answer with no proposal | Up 20% vs baseline |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Interest signal followed by a bot reply with no concrete step | `user.intent` is price, timing, or start, and `bot_reply.next_step` is empty | The user said they were done in the same message |
| Bot reply ends with "let me know if you have other questions" in a qualified chat | `bot_reply.text` closing phrase and `interest_signal` set | A support chat where the issue was resolved |
| Qualified chat ends on a bot answer with no user reply | Last event is a bot turn; no `next_step` event | The user came back and booked by another channel |
| User asks the same timing or how-to-start question twice | Repeated intent in the next two user turns | The user was comparing two options on purpose |
| User writes "ok" or "thanks" right after an answer to a timing question | Short user turn after an interest signal, then session end | The user got what they needed and left satisfied |

**Starter rule:** when a user shows interest, propose one clear next step that the bot or a person can actually carry out, and let the user decline it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-ask
runs: pre_send
reads: [session.interest_signal, session.ask_made, session.ask_declined, draft_reply.next_step, session.stakes, session.user_signalled_done]
trigger: a reply is about to be sent in a chat where the user showed interest and the draft has no concrete next step
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Book a call", "Get a quote by email", "Keep browsing", "Something else"]
on_miss: rewrite
metric: Next-step proposal rate in qualified chats
counter_metric: asks in chats with no interest signal
status: proposed
```

## 8. Related patterns
- [Answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): the closest page. It covers a bot that answers and then stops leading in any chat: no discovery question, no goal, no check that the problem is solved. This page covers one narrower miss: the user has shown interest and the bot offers no clear, honest next step.
- FW-S06, pressure (sibling page, not yet written): the opposite failure, where the bot pushes, invents urgency, or will not accept no. This page is a missing ask; that one is a bad ask.
- [Unclear next step](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/unclear-next-step.md): a support bot says a process is under way but not what happens next. Here the failure is in a sales or lead chat before anything has been agreed.
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): sales content where the user wanted help. This page is about the user who wants the sale and gets no step.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): a dead end after a refusal, not after interest.

## 9. Common questions
### Why does my chatbot answer questions but never book a meeting?
Often it has nothing to offer: no calendar link, quote form, or callback queue is wired in. Or the prompt tells it to answer and be concise. See [why it happens](#3-why-it-happens) and rules 3 and 4.

### Should a chatbot always ask for the sale?
No. Ask only after the user shows interest. A question about shipping, store hours, or an order status gets an answer. See Don't over-correct in [the fix](#5-the-fix).

### What counts as a good next step for a chatbot to propose?
One concrete action the bot or a person can do, with a time or channel: book Friday 1-3 p.m., email a quote, or have someone call. "Contact us" is not a next step.

### How is this different from a pushy sales bot?
A pushy bot asks too hard, invents urgency, or ignores no. A bot with no ask never offers anything. Honest asks that the user can decline sit between the two (rule 5 and rule 7).

### Does asking for the next step increase sales?
In human sales, Gong's data links more time on next steps to faster deals (section 4), but that is a link in vendor data, not a test on bots. I found no controlled study of chatbot asks. Test it on your own traffic.

### How many options should the bot offer?
One clear step is the default. If there are two or three real paths, offer them as choices with "Something else" and free text open. The Teams docs show at most three suggested actions (section 4).

---
## Technical section

### T1. Solution architecture
```
user message -> interest detector (rules on price/timing/start intents + judge on a sample) -> state: interest_signal, ask_made, ask_declined
draft reply -> ask check: interest set and no next_step? -> rewrite with one step from the available-actions list
available-actions list = what the product can actually do now (booking slots, quote form, callback queue)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Interest signal with no concrete step triggers a rewrite | Pre-send check | Tests 1 and 6 |
| Only steps from the available-actions list | Composer | Test 3; unfulfilled-ask metric |
| No ask without an interest signal | Pre-send check | Test 2; counter-metric |
| Declined ask is not repeated | State | Test 4 |

### T3. Evals
- **Dataset:** 100 chat openings to start: interested users, browsers, support users, users who decline, users who accept; include 20 cases where an ask is wrong.
- **Judge rubric:** is there an interest signal; is there exactly one concrete step; is it something the bot can do; can the user decline?
- **Release gate:** block a deploy if asks in no-interest chats or repeated asks exceed your target (starting points, to tune).

### T5. Trade-offs
- A real next step needs integration work (calendar, CRM, callback queue) before any prompt change helps.
- An interest detector will miss some cases and flag some wrongly. The counter-metric catches the second kind.

---
### Deep dive
- **Open question.** I found no controlled study of chatbot asks and conversion. The evidence here is human sales research and vendor data.
- **References.** [Iannarino on Rackham](https://www.thesalesblog.com/blog/deals-stalled-how-to-advance-a-sale) (opened); [Gong, Sales Stats](https://www.gong.io/blog/sales-stats/) (opened); [Gong Labs, first call length](https://www.gong.io/resources/labs/how-long-your-first-sales-call-should-be/) (opened); [Microsoft Learn, suggested actions](https://learn.microsoft.com/en-gb/microsoftteams/platform/bots/how-to/conversations/suggested-actions) (opened).
