# Chatbot Won't Let Me Talk to a Human: "Talk to a Human" Ignored or Looped

<!-- SEO
title: Chatbot Won't Let Me Talk to a Human: Why and How to Fix It
description: Why customers say "agent" and the chatbot keeps looping, what the CFPB found, and a copyable rule set so a clear request for a person always gets a real route.
search phrases:
- chatbot won't let me talk to a human
- how to talk to a real person instead of a chatbot
- chatbot keeps looping and won't transfer to an agent
- chatbot ignores "speak to a representative"
- how to add a talk to a human button to a chatbot
- chatbot human handoff best practices
- customers stuck in chatbot doom loop
-->

**Frequency**: Common

## Issue: A customer asks for a person, and the chatbot answers with the same menu, asks the same question again, or sends them in circles instead of connecting them or saying how.

> **One line:** The customer types "agent", "representative", or "human", and the bot keeps going as if they had asked something else.

| | |
|---|---|
| **Channel** | Written for **chat**. The same failure happens by phone with voice menus (notes in the Deep dive; voice is planned, not yet written). |
| **Stakes** | Any. At low stakes it costs time; with a bill due, a frozen account, or a fraud claim it costs money. |
| **Who is affected** | Anyone whose problem falls outside what the bot can do, which is usually the customers who most need help |
| **Frequency** | Common. I found no study that measures how often it happens; the evidence below is regulator and survey material. |
| **Pattern ID** | talk-to-a-human-ignored-or-looped |
| **Family** | [Human handoff](../README.md) |
| **Goal** | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| **Primary metric** | Human-request fulfillment rate: requests for a person that end in a transfer, a scheduled callback, or a stated route within 2 bot turns. Starting target: 100% (this is a rule, not a statistic). |
| **Maturity** | Tests written (see [the test file](../../../tests/talk-to-a-human-ignored-or-looped.md); not yet run). Incident: [CFPB report on bank chatbot doom loops](../../../incidents/cfpb-bank-chatbot-doom-loops.md) |
| **Will a better model fix this?** | No. Models already recognize "let me talk to a person". Whether the product honors it is a routing and policy choice. (Our judgment, not tested.) |
| **Also searched as** | chatbot dead end · chatbot loop no agent · "I want to speak to a human" bot ignores · bot won't transfer to live agent · customer service chatbot doom loop |

## 1. In plain words
The customer has tried the bot, it did not work, and they ask for a person. The bot either pretends not to hear, answers a different question, or hands back the same menu. Some products hide the person behind a login the customer does not have, or a wait nobody mentions. The customer ends up with a worse problem than the one they started with.

## 2. What it looks like

**Without the fix**
```
User: I was charged twice for the same order.
Bot:  I can help with billing! Here are our billing FAQs: [link]
User: that doesn't answer it. I need to talk to a person
Bot:  I understand you have a billing question. Can you tell me your order number?
User: AGENT
Bot:  Sorry, I didn't get that. You can ask me about orders, returns, or billing.
User: human please
Bot:  I can help with billing! Here are our billing FAQs: [link]
```

**With the fix**
```
User: I was charged twice for the same order.
Bot:  I'm sorry about that. Send me the order number and I'll check right now.
User: that's not going to work, I need to talk to a person
Bot:  Of course. I'm connecting you to a billing specialist. The wait is about 6 minutes.
      I'm sending them what you've told me, so you won't need to repeat it.
      If you'd rather not wait, I can have them call you back; tell me a number.
```
The fixed bot honors the request on the first clear ask, says what happens and when, and passes the details along.

## 3. Why it happens
These are our reading of the pattern; no source measures the causes.
- **Deflection is the goal.** Bots are often measured on how many conversations they keep away from people. A request for a human counts against that number, so the product is tuned to avoid it.
- **"Human" is not recognized as a routing event.** The bot treats it as ordinary text and runs its normal intent matching, which has no matching intent. It falls back to the menu.
- **The route is gated.** The way to a person is behind a login, a form, or a queue the bot cannot see, so even a willing bot has nowhere to send the customer.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The CFPB reviewed consumer complaints about bank chatbots and described customers stuck in "continuous loops of repetitive, unhelpful jargon or legalese without an offramp to a human customer service representative". It called these "doom loops". | [CFPB, *Chatbots in consumer finance* (June 6, 2023)](https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf), section 3.1.3. Opened and read. | US consumer finance only. The report quotes individual complaints; it does not give a count of how many. |
| The same report says "deficient chatbots that prevent access to live, human support can lead to law violations, diminished service, and other harms." | CFPB report, conclusion. Opened and read. | A regulator's statement about financial institutions. It is not legal advice and does not apply to every business. |
| The CFPB reports that each of the 10 largest US commercial banks had deployed a chatbot, and estimates about 37% of the US population interacted with a bank chatbot in 2022. | CFPB report, key findings. Opened and read. | The 37% is the CFPB's estimate from a source I did not open. It is bank chatbots, not all chatbots. |
| The report notes that a chatbot's limits and the lack of access to a person "may not be apparent to customers when they are initially signing up", and that waits can also block the route to a person. | CFPB report, section 3.1.3. Opened and read. | Describes the problem; it is not a measurement. |
| A Gartner survey found 64% of customers would prefer companies not use AI in customer service, and 53% would consider switching. Difficulty reaching a person was reported as the top concern. n=5,728, fielded December 2023. | [Gartner press release (July 9, 2024)](https://www.gartner.com/en/newsroom/press-releases/2024-07-09-gartner-survey-finds-64-percent-of-customers-would-prefer-that-companies-didnt-use-ai-for-customer-service). **Read through a search summary; the page returned an access error and was not opened.** | Survey of attitudes, not behavior. Treat the figures as unverified until opened. |

A widely repeated claim that 68% of users abandon a chatbot with no human option traces to a blog, not a study. I did not use it.

## 5. The fix

**The principle:** A clear request for a person is a routing event. Honor it, or answer it with a real route, a time, and what happens next, within two bot turns.

**Do this**
1. **Treat "talk to a human" as a hard route.** Detect typed and spoken requests: "agent", "representative", "human", "person", "operator", "call me", "supervisor", and plain equivalents ("I want to talk to someone"). Detection runs before normal intent matching.
2. **At most one offer to help first.** The bot may say once that it can try to fix the problem, but only alongside the handoff offer, and only if the customer has not asked twice. On the second request, hand off. Never ask a diagnostic question in place of the answer.
3. **Say what happens next.** Give the wait time or when a person will reply, the channel (chat, callback, email), and what the bot is passing along.
4. **No person available right now?** Say so and give a real alternative with a time: callback, ticket, or email, with the follow-up window. Never leave the request unanswered.
5. **Never require a login to reach a person** for someone who cannot log in (new, locked out, or without an account). Offer a route that works without one.
6. **Offer a person without being asked** after two failed attempts on the same problem, or after the bot repeats an answer.
7. **Record every request and its outcome** so the metric in section 7 can be computed.

**Reference design: a prompt block (starting point; adapt to your product)**
```
If the user asks for a person in any wording (agent, human, representative, operator,
supervisor, "call me", "talk to someone"), do NOT answer the underlying question first.
Reply in this order:
1. Acknowledge in one short sentence.
2. Say how they will reach a person and when: [wait time or response window] by [channel].
3. Say what you are passing along: a summary of what they told you.
4. If no person is available now: offer [callback / ticket / email] with the time to expect.
Never ask the user to log in to reach a person. Never repeat a menu in response to this request.
If they ask a second time, hand off immediately.
```
Decision table the policy layer should follow:
| Request count | Person available | What the bot does |
|---|---|---|
| 1 | Yes | Offer the transfer now, with wait time and summary. May add one line offering to try first |
| 1 | No | Say when a person is available; offer callback or ticket; keep the conversation open |
| 2 or more | Yes | Transfer immediately |
| 2 or more | No | Confirm the callback or ticket is created and give the time |
| Any | Handoff fails | Say so, give another route, never go back to the menu |

**Don't over-correct.** Not every mention of "agent" is a request (for example "insurance agent" or "travel agent" inside a question). Use intent detection, not keyword matching alone. Do not transfer people who clearly want the bot's quick answer, and do not route trivial questions to scarce humans. The only thing the bot may not do is block a clear request.

**Hand-off rule.** When the handoff happens, pass a summary, the customer's goal, and what was tried, so the person does not start from zero. The mechanics belong to the planned [cold transfer](../../../roadmap/handoff-measurement-and-operations.md) pattern; the closest written one is [no channel switch or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md).

**Framework used:** none yet. The closest existing page is the [channel-fit matrix](../../../solutions-library/channel-fit-matrix.md).

## 6. How to test it (short version)
The [full test file](../../../tests/talk-to-a-human-ignored-or-looped.md) has 12 conversations. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Customer types "agent" at the start | Handoff or a real route with a time within 2 turns |
| 2 | Customer asks for a person twice, in different wording | Handoff on the second request, no menu in between |
| 3 | Request outside staffed hours | Bot states hours and gives a callback or ticket with a time |
| 4 | Customer cannot log in and asks for a person | Route offered does not require login |
| 5 | "I want to cancel my travel agent booking" | Bot does not treat "agent" as a request for a person |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Human-request fulfillment rate** (primary) | 100% | Share of conversations containing a request for a person that end in a transfer, scheduled callback, or stated route within 2 bot turns. Needs a request label from a classifier plus sampled review | Any week below 98% |
| Requests needing a second ask | Under 5% | Conversations where a second request for a person follows a bot reply | Over 10% |
| Repeated bot replies | Under 2% of turns | Identical or near-identical bot reply twice in a row after a request | Over 5% |
| Abandonment after a request | Track; set from baseline | Conversations that end within 3 turns of the request with no handoff | Rising two weeks in a row |
| Wait time stated | 100% of transfers | Transfers where the bot stated a wait or response window | Below 95% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice signals are planned.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User message asks for a person and the next bot turn is not a handoff, route, or stated wait | Request label on a user turn, bot turn type after it | A single offer to help alongside the handoff offer, which the fix allows once |
| A second request for a person after a bot reply | Two request-labeled user turns in one conversation | A user rephrasing because the first route was unclear |
| Identical or near-identical bot reply twice in a row after a request | Consecutive bot turns with high similarity | An intentional repeated confirmation |
| Conversation ends within 3 turns of a request with no transfer, callback, or stated route | Session end event after a request-labeled turn | The user found the answer elsewhere |
| Transfer with no wait time or response window stated | Handoff event with no stated window in the bot message | A channel with no queue |

**Starter rule:** a clear request for a person is a routing event, answered within two bot turns with a transfer, a callback, or a stated route and time.

## 8. Related patterns
- [Chatbot loop without human escalation path](../../../../../by-use-case/support-services/goals/self-service-deflection/failures/chatbot-loop-without-human-escalation-path.md): the same loop seen from the deflection side, in service workflows. This page is about honoring an explicit request.
- [Poor escalation](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/poor-escalation.md): escalating at the wrong moment or without context. Here the customer has already asked.
- [Escalation too early](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/escalation-too-early.md): the opposite problem.
- [No channel switch or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md): what happens after the handoff.
- [The answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): a bot that stops too early, the reverse of one that will not stop.

## 9. Common questions
### How do I make a chatbot hand off to a human?
Detect the request before normal intent matching, then route to a person or a callback and tell the customer the wait. The rules and a decision table are in [the fix](#5-the-fix).

### Should the bot try to solve the problem before transferring?
It may make one offer, in the same message as the handoff offer. If the customer asks again, transfer. Making the customer ask a third time is the failure this page describes.

### What if no human agent is available?
Say so, give the hours, and offer a callback, ticket, or email with a time. An unanswered request is the worst outcome. See rule 4.

### Does the CFPB require a human option?
The CFPB report says deficient chatbots that prevent access to live, human support can lead to law violations. It is a statement about consumer finance and is not a legal requirement for your product. Have counsel check your obligations.

### Won't offering a human raise costs?
It may increase transfers. The alternative is customers who leave or complain. Measure both: the fulfillment rate in section 7 and the cost per resolved conversation.

---
## Technical section

### T1. Solution architecture
```
user message -> human-request detector -> (hit) handoff policy -> transfer | callback | ticket
                    |                                   |
                (miss) -> normal bot flow          log: request, outcome, turns
```
The detector runs before intent matching. The policy layer, not the language model, decides the route, so a prompt change cannot disable it.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| A detected request always yields a route or a stated alternative | Policy layer | Log check: every `human_request` event has an outcome |
| No login required to reach a person | Routing configuration | Test 4 in the test file |
| Wait or response window stated | Reply template | Log check on transfer messages |

### T3. Evals
- **Dataset:** 200 conversations to start, with requests worded many ways, plus negatives such as "travel agent".
- **Judge rubric:** did a route, time, and next step appear within 2 turns?
- **Metrics and starting thresholds:** detection recall over 98% on the labeled set; false positives under 2%. These are starting points to tune.
- **Release gate:** block a deploy if recall drops by more than 1 point against the last release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Fulfillment rate | Below 99% | Below 95% | Check the detector and the routing service |

### T5. Trade-offs
- More transfers means more staffing cost.
- A strict detector may misfire on words like "agent". Keep a labeled negatives set.

---
### Deep dive
- **Voice.** Phone menus fail the same way ("press 0", then back to the menu). Voice is planned, not yet written.
- **Open question.** I found no controlled study that isolates the effect of a missing human option on abandonment. The only figures I found trace to vendor surveys or unsourced blogs.
- **References.** [CFPB, *Chatbots in consumer finance*](https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf) (opened, June 2023).
