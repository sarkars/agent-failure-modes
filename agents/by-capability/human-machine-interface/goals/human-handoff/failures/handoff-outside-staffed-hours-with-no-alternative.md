# Chatbot Says a Person Will Join, but Nobody Is Working: Handoff Outside Staffed Hours

<!-- SEO
title: Chatbot Promises a Human After Hours: Fix the Dead End
description: A chatbot says a person will join the chat, but no one is staffed until tomorrow and no callback, ticket, or email is offered. State the hours, then offer a way to be reached.
search phrases:
- chatbot says connecting to an agent but no one responds
- live chat offline message after hours
- chatbot transfer to agent outside business hours
- what should a chatbot say when support is closed
- chat widget office hours offline form vs ticket
- customer service chatbot no agents available
- chatbot after hours handoff best practices
-->

**Frequency**: Common

## Issue: A chatbot says a person will join the chat, but no one is staffed until tomorrow, and it offers no callback, ticket, or email to bridge the gap.

> **One line:** The bot says "connecting you to an agent" at 10:40 p.m. on a Saturday, and the customer waits for someone who is not there.

| | |
|---|---|
| **Channel** | Written for **chat** (web and in-app messengers). Phone callbacks and voice menus are planned, not yet written. |
| **Stakes** | Any. Low for a shipping question; high for a locked account, a fraud charge, or a deadline that falls before the next shift. |
| **Who is affected** | Anyone who asks for a person outside staffed hours: evenings, weekends, holidays, and customers in other time zones |
| **Frequency** | Common. I found no study that counts how often it happens; the evidence below is vendor documentation showing that the setting exists and is easy to leave unset. |
| **Pattern ID** | handoff-outside-staffed-hours-with-no-alternative |
| **Family** | [Human handoff](../README.md) |
| **Goal** | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| **Primary metric** | Handoff requests outside staffed hours that get the hours, a time zone, and a callback, ticket, or email with a follow-up time. Starting target: 100% (a rule, not a statistic; tune the definition of "staffed" to your schedule). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A model can phrase the message well, but it cannot know whether anyone is staffed unless the product passes in the schedule and a working fallback. (Our judgment, not tested.) |
| **Also searched as** | chatbot says agent will join but nobody does · live chat no one online · after hours chatbot handoff · chat offline form black hole · support closed chatbot no option |

## 1. In plain words
The customer asks for a person. The bot answers as if one is on the way, but the support team is off until morning. The customer waits, gives up, or comes back tomorrow and starts over. The fix is to say when people are available, in the customer's time, and offer something real to do now: a callback, a ticket, or an email, with a time to expect.

## 2. What it looks like
Illustrative example: a billing chat built on Intercom Messenger, Saturday at 10:40 p.m. Eastern. Support hours are Monday-Friday, 8 a.m.-8 p.m. Eastern.

**Without the fix**
```
User: My card was charged twice today. I need to talk to someone.
Bot:  I'm sorry about that. I'm connecting you with an agent now.
Bot:  Please hold on while an agent joins the chat.
      (nothing for 20 minutes)
User: Hello? Is anyone there?
Bot:  An agent will be with you shortly.
```
**With the fix**
```
User: My card was charged twice today. I need to talk to someone.
Bot:  I'm sorry about that. Our billing team is available Monday-Friday,
      8 a.m.-8 p.m. Eastern, and it's Saturday night, so no one is here right now.
Bot:  I can open a ticket now with what you've told me, and a specialist will reply by
      email by 12 p.m. Eastern Monday. Or I can book a callback. Which do you prefer?
      [Ticket] [Callback] [Something else]
```
The fixed bot does not promise a person who is not there. It states the hours and time zone, says what happens next, and offers a real route with a time.

## 3. Why it happens
- **The handoff does not check the schedule.** The "talk to a person" step runs the same at 3 p.m. and 3 a.m. The bot says "connecting you" because the transfer was triggered, not because anyone can accept it.
- **Office hours are an optional setting.** In at least one major messenger, office hours are not set by default and availability is 24/7 until a team adds them (see section 4). Until someone sets the hours, the product behaves as if it is always staffed.
- **The after-hours route is a separate build.** A ticket form, offline message, or callback has to be configured and tested by someone. Teams ship the handoff first and the fallback later, or never.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Intercom's help article says office hours are "not specified by default, meaning availability is set to 24/7, always-on." Hours follow the workspace time zone and adjust for daylight saving. Outside office hours the Messenger can tell customers when the team will be back. | [Intercom Help, *Set your default office hours*](https://www.intercom.com/help/en/articles/732390-set-your-default-office-hours). Opened and read. | Vendor documentation for one product. It shows the default and the available settings, not how often teams leave them unset. |
| Intercom lets teams choose when to show office hours and reply times: before a conversation is assigned, only after assignment (marked recommended), or not at all. | Same Intercom article. Opened and read. | Vendor documentation. The "recommended" label is the vendor's, not a test result. It also shows hours can be hidden by choice, which is the opposite of this pattern's rule 1. |
| Zendesk's guide to messaging business hours lists after-hours options: hide the web widget when agents are unavailable, prevent customers from submitting a ticket when agents are offline, or let customers create a ticket for follow-up. It says messaging business hours can control whether a ticket is created outside business hours. | [Zendesk Support, *Migrating Chat operating hours to business hours in messaging*](https://support.zendesk.com/hc/en-us/articles/11033533612954). Opened and read; the follow-up-ticket option's section had no detail on the page I read. | Vendor documentation. It lists options; it does not say which works best. Choosing "prevent a ticket" without another route recreates this failure. |
| BoldDesk's help article describes three after-hours tools: an offline form "to capture their queries for later follow-up," an away message ("An Away Message is an automated reply sent when agents are not available to respond in real time"), and chat-to-ticket conversion so messages are logged as tickets. It says the form can tell users about response timelines. | [BoldDesk Support, *Handling chats beyond business hours*](https://support.bolddesk.com/kb/article/21953/handling-chats-beyond-business-hours-in-bolddesk). Opened and read. | Vendor documentation. It shows the tools exist, not that customers follow up on them. |
| The CFPB described bank-chatbot complaints of customers stuck with no offramp to a person. | [CFPB doom-loop incident summary](../../../incidents/cfpb-bank-chatbot-doom-loops.md) (this library). | Describes loops, not closed-hours handoffs. I found no public source that measures after-hours handoff failures specifically. |

I found no study of customer outcomes after an off-hours chat handoff, and no regulator page I could open that speaks to staffed hours. The evidence here shows the options vendors provide, not the harm.

## 5. The fix

**The principle:** Never promise a person who is not working. When the customer asks outside staffed hours, state the hours and time zone and give a real alternative with a follow-up time.

**Do this**
1. **Check the schedule before the handoff message.** The bot reads whether a person can accept a chat now, including holidays and staffing exceptions. If not, it must not say "connecting you" or "an agent will join".
2. **State the hours in the customer's terms.** Give days, times, and time zone ("Monday-Friday, 8 a.m.-8 p.m. Eastern"). If the customer's time zone is known, add the local equivalent.
3. **Say it before the customer asks, when it matters.** If the product offers a person, show the hours in the greeting or the first handoff mention, not only after a failed transfer.
4. **Offer at least one alternative that works now.** Callback, ticket, or email, each with a follow-up time ("by 12 p.m. Eastern Monday"). Never end the turn with only "we are closed".
5. **Make the alternative real before offering it.** Create the ticket or callback record, confirm it was saved, and give the customer a reference. If the save fails, say so and give another route.
6. **Pass the context.** Put what the customer said, their account and contact details, and the urgency into the ticket or callback so the person starts informed ([cold transfer](cold-transfer.md)).
7. **Keep urgent cases on the urgent route.** For fraud, locked accounts, or safety issues, give the after-hours emergency route if one exists (such as a 24-hour phone line); if none exists, say so plainly.
8. **Keep the bot helpful while closed.** Offer to try to solve the problem now, but only alongside the alternative, never in place of it.

**Reference design: after-hours handoff decision**
| Customer asks for a person | Staff open now | Response |
|---|---|---|
| Yes | Yes | Transfer; state the wait ([talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md)) |
| Yes | No, reopens within 24 hours | State hours and reopening time; offer ticket or callback with a time |
| Yes | No, reopens later (weekend, holiday) | Same, with the actual reopening day and time; offer an urgent route if one exists |
| No | No | Answer normally; mention hours if the problem looks unlikely to resolve in chat |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The customer asks for a person and nobody is staffed: first say the hours, time zone, and that no one is available now. Do not open with "I'm connecting you". |
| Offer choices: 2-4 options plus "Something else", free text open | After stating the hours: "Ticket", "Callback", "Email", "Something else". Do not offer a choice when only one route exists (say that route) or when a person is available (transfer instead). |
| Hand off to a person | Staff are open: transfer. Staff are closed: hand off through the ticket or callback record, with context, and say when a person will pick it up. |

**Don't over-correct.** Do not hide the human route entirely outside hours, and do not refuse the request with only "we are closed". Do not push every customer to a ticket; if the customer is happy with the bot's answer, let them go. Do not show hours in a way that is wrong (a hard-coded schedule that ignores holidays or the customer's time zone).

**Hand-off rule.** Open hours: transfer the chat with a summary. Closed hours: create the ticket or callback with the summary and a follow-up time. The person who picks it up should not have to ask the customer to repeat anything ([cold transfer](cold-transfer.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No full test file yet. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Customer types "agent" at 10:40 p.m. Saturday | Bot states hours and time zone, says no one is available now, offers ticket or callback with a time; never says "connecting you" |
| 2 | Same request at 2 p.m. Tuesday, staff open | Bot transfers and states the wait |
| 3 | Request on a company holiday | Bot gives the actual reopening day, not the normal schedule |
| 4 | Customer in Pacific time, hours listed in Eastern | Hours name the time zone (and show local time if known) |
| 5 | Customer picks "Ticket", but the save fails | Bot says it did not save and offers another route; does not claim a ticket exists |
| 6 | Customer reports a fraudulent charge after hours | Bot gives the urgent route if one exists, or says there is none, and also creates the ticket |
| 7 | Customer says "no thanks, I'll wait" | Bot confirms the next opening time and keeps the ticket option open |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Handoff requests outside staffed hours with a stated alternative** (primary) | 100% | Log each handoff request with `schedule.is_open`; for closed ones, check the reply has hours, time zone, and a callback, ticket, or email with a follow-up time (rule check plus sampled review) | Any week below 98% |
| Closed-hours replies that say "connecting" or "agent will join" | 0 | Phrase and intent check on replies when `schedule.is_open` is false | Any |
| Alternatives created and confirmed | 100% of those accepted | Ticket or callback record exists with the chat reference | Below 98% |
| Follow-up met within the stated time (counter-metric: promises kept) | Track; set from baseline | Ticket first reply time against the time the bot stated | Falling two weeks in a row |
| False "closed" replies while staff were open (counter-metric) | 0 | Replies saying no one is available while the schedule shows open | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Handoff message sent while the schedule is closed | Handoff event with `schedule.is_open` false and a "joining" template | A staffed overflow queue the schedule does not list |
| Closed-hours handoff reply has no hours or time zone | Reply text check on hours and zone fields | Hours already shown earlier in the same conversation |
| Closed-hours handoff reply has no callback, ticket, or email option | Choices or alternative-type field empty | The customer declined all routes in a prior turn |
| Customer messages again within 15 minutes of a handoff reply, no agent event | Next user turn, no `agent_joined` event | The customer added new information |
| Ticket or callback accepted but no record created | Choice event with no matching record id | A delayed write that lands later |

**Starter rule:** outside staffed hours, a request for a person is answered with the hours, the time zone, and a callback, ticket, or email with a follow-up time, never with "connecting you".

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: handoff-outside-staffed-hours-with-no-alternative
runs: pre_send
reads: [handoff.requested, schedule.is_open, schedule.next_open, schedule.timezone, user.timezone, alternative.available]
trigger: a handoff or request for a person arrives while the schedule is closed
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Ticket", "Callback", "Email", "Something else"]
on_miss: rewrite
metric: handoff requests outside staffed hours with a stated alternative
counter_metric: false "closed" replies while staff were open
status: proposed
```

## 8. Related patterns
- [Talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md): the request is never honored at all. Its rule 4 says to give an alternative when nobody is available; this page covers that case in depth: schedule checks, hours, time zone, holidays, and follow-up promises. If the bot hears the request but says it will connect you while closed, you are here.
- [Escalates too early or too late](escalates-too-early-or-too-late.md): decides when a case needs a person. This page applies once a person is wanted but is not staffed.
- [Cold transfer](cold-transfer.md): what the person knows when they pick up. A ticket created after hours is the same handoff, delayed.
- [CFPB bank chatbot doom loops](../../../incidents/cfpb-bank-chatbot-doom-loops.md): public record of customers stuck with no route to a person.

## 9. Common questions
### What should a chatbot say when no human agents are available?
Say that no one is available now, give the hours and time zone, and offer a callback, ticket, or email with a time. See rules 2 and 4.

### Should the bot hide the "talk to a person" option outside hours?
No. Hiding it leaves the customer with no route. Zendesk's documentation lists hiding the widget as one choice; it does not say that choice is best. Keep the route and make it work through a ticket or callback.

### Is an offline form enough?
Only if it states when to expect a reply and the customer gets a confirmation. A form that goes nowhere is the same dead end. BoldDesk's documentation says the form can tell users about response timelines.

### Do I need to show hours before the customer asks?
When the product offers a person, yes: show the hours early. Intercom lets teams choose when hours appear, including before a chat is assigned. Which is best for you is a test for your own customers.

---
## Technical section

### T1. Solution architecture
```
user message -> human-request detector -> schedule service (is_open, next_open, timezone, holidays)
   open   -> transfer + wait time
   closed -> after-hours template (hours, time zone, next open)
          -> offer ticket | callback | email -> create record -> confirm id and time
          -> log (is_open, template, alternative_type, record_id)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No "connecting"/"joining" text when `is_open` is false | Reply template layer | Log scan; tests 1 and 3 |
| Alternative offered only after the record can be created | Ticket and callback service | Test 5 |
| Schedule includes holidays and exceptions | Schedule service | Test 3 |

### T3. Evals
- **Dataset:** a set of handoff requests spread across open, closed, holiday, and mixed time-zone cases; start with a few dozen and add production misses.
- **Judge rubric:** does the reply state hours and zone, avoid promising a person, offer a route with a time, and match the schedule state?
- **Metrics and starting thresholds:** primary metric 100%; false "closed" 0. Starting points to tune.
- **Release gate:** block a deploy if a closed-hours test case says "connecting".

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Closed-hours replies without an alternative | Any in a day | Over 2% of closed-hours requests | Check the template and the schedule service |

### T5. Trade-offs
- Callbacks and tickets add work for the first shift after closing; staff the follow-up or the promise will fail.
- Showing hours early can reduce chat starts; that is a cost of honesty, not a defect.

---
### Deep dive
- **Open question.** I found no study of what customers do after an off-hours chat handoff. The evidence is vendor documentation.
- **Voice (planned).** Phone callbacks and voicemail follow the same rules; not yet written.
- **References (all opened):** [Intercom Help, office hours](https://www.intercom.com/help/en/articles/732390-set-your-default-office-hours); [Zendesk Support, messaging business hours](https://support.zendesk.com/hc/en-us/articles/11033533612954); [BoldDesk Support, chats beyond business hours](https://support.bolddesk.com/kb/article/21953/handling-chats-beyond-business-hours-in-bolddesk).
