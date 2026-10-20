# Chatbot Treats a Fraud Alert Like a Casual Question: Urgency-Blind Pacing

<!-- SEO
title: Chatbot Treats Fraud and Outages Like Casual Questions
description: A chatbot gives a stolen card or an outage the same menus, questions, and queue as a store-hours question. Fix it with an urgent fast path to action or a person.
search phrases:
- chatbot stolen card report no human
- chatbot fraud report takes too long
- how should a chatbot handle urgent requests
- chatbot priority routing urgent issues
- chatbot detect urgency and escalate
- support bot outage report same queue
- bank chatbot lost card freeze card fast
- ai agent urgent intent fast path
-->

**Frequency**: Occasional

## Issue: A chatbot answers a fraud alert, a lost card, or an outage report with the same greeting, menus, questions, and queue as a casual question, so the urgent user waits as long as everyone else.

> **One line:** The user writes "someone is using my card" and the bot opens with a menu, because nothing told it that minutes matter here.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web-form signals (hold time, IVR menus) are planned, not yet written. |
| **Stakes** | High. Money, access, or a business running down while the user waits. |
| **Who is affected** | Users reporting fraud, a lost or stolen card, an account takeover, a payment due today, or an outage |
| **Frequency** | Occasional. I found no study that counts how often bots miss urgency; the evidence below is regulator and vendor material. |
| **Pattern ID** | urgency-blind-pacing |
| **Family** | [Response time](../README.md) |
| **Goal** | Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. |
| **Primary metric** | Time to action or human for urgent intents. Start: under 2 min (tune). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | Partly. A better model recognizes urgent wording more often, but the fast path (a freeze tool, a staffed queue, a priority flag) is product work. (Our judgment, not tested.) |
| **Also searched as** | chatbot urgent request · stolen card chatbot · bot won't escalate fraud · priority routing chatbot · support bot outage same queue |

## 1. In plain words
Some messages cannot wait: "my card was stolen", "the site is down", "my payment is due today". A bot with one pace treats these like "what are your hours?". It greets, shows a menu, asks for details it does not need yet, and sends the user to the same queue. The fix is a short, written list of urgent intents that skips the slow path and goes straight to the action or a person.

## 2. What it looks like
*(Illustrative. The bank and bot are invented, modeled on the time-sensitive complaints in section 4.)*

**Without the fix**
```
User: Someone is using my debit card. I just got 3 texts for charges I didn't make.
Bot:  Hi, I'm Penny, your Harbor Credit Union assistant! I can help with balances, transfers, branch hours, and more.
      What would you like to do today?  [Balances] [Transfers] [Branch hours] [Other]
User: other. my card is being used right now
Bot:  Thanks! To get started, can you tell me which type of account you have?
User: I NEED SOMEONE NOW
Bot:  I understand you're looking for help. Here are some tips to protect your card: [link]
```

**With the fix**
```
User: Someone is using my debit card. I just got 3 texts for charges I didn't make.
Bot:  That sounds like fraud, so I'm moving this to the front. I can freeze the card ending in 4417 right now.
      The fraud team can also join; the wait is about 3 minutes. What do you want first?
      [Freeze the card now] [Connect me to the fraud team] [Something else]
User: Freeze the card now
Bot:  Done: the card ending in 4417 is frozen. Charges made before now are not undone. The fraud team will pick this up from here; I've passed on what you told me, so you won't need to repeat it.
```
The fixed bot spotted the intent in the first message, led with an action it could take, offered a person with a stated wait, and passed the context on.

## 3. Why it happens
These are our reading of the pattern; no source measures the causes.
- **One path for every intent.** The flow starts with a greeting and a menu, and every intent follows the same steps, so a stolen card gets the same route as a branch-hours question.
- **Urgency is left for the user to declare.** Rule-based routing waits for a priority field or a keyword. The OpenCX guide says rule-based systems need the customer to state urgency, which most customers do not do (section 4). Capital letters and "now" are not read as signals.
- **The fast path does not exist.** Even if the bot spots the problem, it has no freeze or lock tool and no priority queue to hand off to, so the best it can do is a help article.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The CFPB report says chatbots may fail to flag a complaint because "only specific words or syntax may trigger the recognition of a dispute". | [CFPB, *Chatbots in consumer finance*, June 6, 2023](https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/). Opened and read. | Consumer complaints and regulator analysis, not a measured miss rate. Disputes, not stolen-card reports. |
| The same report says: "If a broken chatbot is a customer's only option to receive time sensitive help from their financial institution, it may leave people stranded". It quotes a cardholder: "my payment is due today". | Same report, "Time-sensitive matters" section. Opened and read. | The report states it does not address lost or stolen cards specifically. US consumer finance only. |
| Under Regulation E, a consumer's liability for unauthorized electronic fund transfers depends on how fast they report the loss or theft of an access device. Reporting within two business days of learning of it caps liability at the lesser of $50 or the transfers before notice; later notice raises the cap. | [CFPB, 12 CFR 1005.6, *Liability of consumer for unauthorized transfers*](https://www.consumerfinance.gov/rules-policy/regulations/1005/6/). Opened; I read paragraph (b) only. | Describes the rule, is not legal advice, and covers electronic fund transfers such as debit cards. Other products follow other rules that I did not open. The bot should not state a liability figure to a user. |
| Zendesk's help center shows SLA targets set per ticket priority, with an example of "respond to urgent tickets in 10 minutes and resolve them within 2 hours", and says "the ticket must have a value in the system Priority field" for a target to apply. | [Zendesk, *Defining SLA policies*](https://support.zendesk.com/hc/en-us/articles/4408829459866-Defining-SLA-policies). Opened and read. | The 10-minute figure is a documentation example, not a recommendation. It shows that a blank priority gets no urgent target. |
| A vendor routing guide says an AI classifier should infer urgency from "time-sensitivity cues like "outage" or "production"", and routes a high-urgency outage to engineering on-call. | [OpenCX, *Intercom ticket routing with AI*](https://www.open.cx/blog/intercom-ticket-routing-ai). Opened and read. | Vendor blog. It also quotes accuracy figures that are vendor-reported or cited to other vendor blogs; I do not use them. |

**Public incident.** I found no public, dated incident where a bot's slow pacing of an urgent request was the documented cause of harm. The nearest sourced case is the [CFPB report on bank chatbot doom loops](../../../incidents/cfpb-bank-chatbot-doom-loops.md), which is about missing human access, not pace.

## 5. The fix

**The principle:** When the intent is on the urgent list, the first reply is the action or the route to a person, not a menu or a question.

**Do this**
1. **Keep a written urgent list.** Name the intents (for example: card fraud, lost or stolen card, account takeover, outage, payment due today) and the action or queue for each. An intent not on the list is not urgent.
2. **Classify on the first user turn.** Read the wording and context ("charges I didn't make", "production is down", "due today"), not only a keyword or a priority field the user must fill in.
3. **Lead with the action or the route.** The first reply to an urgent intent offers the fast action or a person. It has no greeting menu, no feature list, and no unrelated question.
4. **Ask only what the action needs.** One question, and only if the action cannot start without it. Identity checks stay; do the safe step first where policy allows.
5. **State the wait for a person, or say there is none.** Give the wait or callback time. If no one is staffed, say so and give the fastest alternative ([handoff outside staffed hours](../../human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md)).
6. **Say what the action did and did not do.** "The card is frozen. Earlier charges are not undone." Never imply it fixed more than it did.
7. **Hand off with the urgency flag and the context.** The person sees the intent, what was done, and what the user said, so the user does not repeat it ([cold transfer](../../human-handoff/failures/cold-transfer.md)).
8. **Drop the slow extras.** No upsell, survey, or long disclaimer before the action on an urgent intent.
9. **If the action takes longer than expected, say so.** Show a status message, as in [silent long-running work](silent-long-running-work.md).

**Reference design: urgent intent table**
| Intent | First-reply action | Person route | Flag passed on |
|---|---|---|---|
| Card fraud, card lost or stolen | Offer to freeze the card | Fraud team, wait stated | `urgency=high`, intent, card last 4, what was done |
| Account takeover | Offer to lock the account and reset access | Security team | `urgency=high`, intent, last login seen |
| Product outage | Confirm status page link and a report path | On-call or incident desk | `urgency=high`, product, error text |
| Payment due today | Show the fastest payment route | Billing team if the route fails | `urgency=high`, due date, amount |

```
Check the user's first message against the urgent list. If it matches, do not greet with a menu.
Reply with the action you can take now and a path to a person with the wait stated. Ask at most one question, only if the action needs it.
After the action, say what it did and what it did not do, and pass the intent and context to the person. Do not give legal or liability advice.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The intent is on the urgent list and the bot has a safe action: state the action first. Do not use it if the bot has no action; then go to the hand-off. |
| Offer choices: 2-4 options plus "Something else", free text open | The first reply has more than one valid fast route (freeze the card, talk to the fraud team). Do not offer choices when only one route fits, or when the user already said which one they want. |
| Hand off to a person | The bot has no action, the action failed, or the user asks. Pass the urgency flag and the context. |

**Don't over-correct.** Do not treat every angry or capitalized message as urgent: that floods the priority queue and slows the real cases. Do not run an action (freezing a card) without the user's choice or the identity checks policy requires. Track the share of urgent flags a reviewer judges not urgent.

**Hand-off rule.** Hand off at once when the bot has no safe action for an urgent intent, when an action fails, or when the user asks for a person ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. These are designs and have **not been run**.

| # | Scenario (rule tested) | Pass if |
|---|---|---|
| 1 | First message: "someone is using my card" (rules 2, 3) | First reply offers the freeze or a person; no menu or greeting list |
| 2 | Same message, no one staffed (rule 5) | The bot says no one is available and gives the fastest alternative |
| 3 | Urgent intent with a vague word choice: "weird charges, I didn't make them" (rule 2) | Treated as urgent, same fast path |
| 4 | "What are your hours?" typed in capitals (don't over-correct) | Answered normally; no urgent flag |
| 5 | Freeze action succeeds (rule 6) | The reply says what changed and what did not |
| 6 | Hand-off after the action (rule 7) | The handoff record holds intent, urgency flag, action taken |
| 7 | Freeze tool is slow (rule 9) | A status message appears; no silent wait |
| 8 | Outage report from a business user (rules 1, 3) | Status link and report path or on-call route in the first reply |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Time to action or human for urgent intents** (primary) | Under 2 min (tune) | From the first urgent message to the action completed or a person's first message, per conversation tagged with an urgent intent | Median over 2 min, or any case over 10 min |
| Urgent intents recognized on the first user turn | Over 95% (tune) | Sampled review against human labels | Below 90% |
| First reply is an action or route, not a menu | Over 95% (tune) | Check the first bot message for urgent conversations | Below 90% |
| Urgent conversations that end with no action or person | 0 | Sessions with an urgent tag and neither event | Any |
| Share of urgent flags judged not urgent (counter-metric) | Under 10% (tune) | Sampled review of flagged conversations | Over 20% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Say "proposed" until they are checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Urgent-list wording in turn 1, first bot reply is a menu or greeting | Turn 1 text match plus bot message type | A question that only mentions the word, such as "how does card fraud protection work?" |
| User repeats the request with capitals or "now" after a bot reply | Second user turn with the same intent and an emphasis marker | A user who types in capitals as habit |
| More than 2 bot turns before any action or handoff event | Turn count between intent tag and first action event | A required identity check that was explained |
| Urgent intent reaches the general queue | Handoff event with no priority field, or the default queue | An urgent case with no staffed priority queue, where the bot said so |

**Starter rule:** the first reply to a message on the urgent list offers the fast action or a person, and has no menu or unrelated question.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: urgency-blind-pacing
runs: pre_send
reads: [user_turn.text, intent.label, intent.urgent_flag, tools.available, queue.priority_wait]
trigger: the first user message matches an intent on the urgent list
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Freeze the card now", "Connect me to the fraud team", "Something else"]
on_miss: rewrite
metric: time to action or human for urgent intents
counter_metric: share of urgent flags judged not urgent
status: proposed
```

## 8. Related patterns
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the closest. There the user asks for a person and the bot ignores it. Here the user never asks; the intent itself is urgent, and the failure is the slow path (menus, questions, same queue), including the actions the bot could take.
- [Escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md): whether to hand off at all. This page is about the speed and route for a known urgent intent.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): tone and care with facts. This page is about pace and path.
- [Missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md): safety crises. This page covers urgent, non-crisis intents such as fraud and outages.
- [Handoff outside staffed hours with no alternative](../../human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md): what to offer when no one is there.
- [Silent long-running work](silent-long-running-work.md): the status message when the fast action itself is slow.

## 9. Common questions
### How should a chatbot handle urgent requests like a stolen card?
Recognize the intent in the first message, offer the fast action (freeze the card) or a person with the wait stated, and skip menus. See the [fix](#5-the-fix).

### How does a chatbot know a message is urgent?
Use a written list of urgent intents and classify the wording and context, not only a keyword or a field the user must fill in. A vendor guide describes inferring urgency from cues such as "outage", but I did not find an independent accuracy figure.

### Should the bot tell users their legal liability for fraud?
No. Regulation E sets time-based limits on debit-card liability, but explaining how they apply to a case is advice the bot should not give. It should act quickly and hand off.

### Won't an urgent path flood my fraud team?
It can if the list is loose. Keep the list short, review flagged cases, and watch the share judged not urgent (section 7).

---
## Technical section

### T1. Solution architecture
```
user turn 1 -> urgent-intent classifier (list + context) -> urgent? 
   yes -> action tool available? -> offer action + person route (wait from queue) -> log timestamps
                          no  -> priority handoff with flag and summary
   no  -> normal flow
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Urgent intent first reply has no menu | Pre-send check | Test 1; log scan |
| Action runs only after user choice and required checks | Tool layer | Test 5 |
| Handoff carries the urgency flag and summary | Handoff service | Test 6 |

### T3. Evals
- **Dataset:** a labeled set of urgent and non-urgent messages per intent, including vague phrasings and look-alikes ("how does fraud protection work?"). Start with a few dozen per intent and grow from production samples.
- **Judge rubric:** is the intent recognized on turn 1; is the first reply an action or route; is the outcome stated truthfully?
- **Metrics and starting thresholds:** recognition over 95%, first-reply compliance over 95%, false-urgent under 10%. Starting points to tune.
- **Release gate:** block a deploy if an urgent test case gets a menu first.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Median time to action or human | Over 2 min | Over 10 min | Check queue staffing and the action tool |

### T5. Trade-offs
- A fast path needs a staffed priority queue and an action tool; the bot alone cannot supply them.
- Wider urgent lists catch more cases but raise false flags and staff load.

---
### Deep dive
- **Open question.** I found no study of how often chatbots miss urgency or how much a delay costs in chat. The evidence is regulator reports, rule text, and vendor documentation.
- **Not used.** Search summaries described Zendesk escalation guides, other Intercom integration docs, and consumer-advice pages on card liability. I did not open them, so the page does not rely on them.
- **Voice (PLANNED).** Phone IVR menus and hold times add the same delay; not yet written.
- **References.** [CFPB, *Chatbots in consumer finance*, 2023](https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/) (opened); [12 CFR 1005.6](https://www.consumerfinance.gov/rules-policy/regulations/1005/6/) (opened, paragraph (b)); [Zendesk SLA policies](https://support.zendesk.com/hc/en-us/articles/4408829459866-Defining-SLA-policies) (opened); [OpenCX routing guide](https://www.open.cx/blog/intercom-ticket-routing-ai) (opened).
