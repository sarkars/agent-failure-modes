# Chatbot Escalates Too Early or Too Late: When a Bot Should Hand Off to a Person

<!-- SEO
title: Chatbot Escalates Too Early or Too Late: When to Hand Off
description: When should a chatbot hand off to a human? Why bots transfer simple questions or hold on to hard ones, with triggers, a decision table, tests, and metrics.
search phrases:
- when should a chatbot escalate to a human agent
- chatbot escalation rules examples
- chatbot transfers to agent too often
- chatbot won't escalate until the customer is angry
- how to set escalation triggers for a customer service bot
- chatbot handoff timing
- how to measure chatbot escalation accuracy
-->

**Frequency**: Common

## Issue: A chatbot hands off questions it could answer, or holds on to ones it cannot, because nobody defined when a person should take over.

> **One line:** The bot transfers a customer who only asked about shipping, or keeps trying while a customer with a locked account gets angrier.

| | |
|---|---|
| **Channel** | Written for **chat**. The same decision exists by phone (voice is planned, not yet written). |
| **Stakes** | Any. Too late is worst when money, safety, or a deadline is involved. Too early wastes scarce staff. |
| **Who is affected** | Customers (late) and the support team (early) |
| **Frequency** | Common. I found no study of how often it happens; the evidence below shows the trade-off and how it is measured. |
| **Family** | [Human handoff](../README.md) |
| **Goal** | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| **Primary metric** | Escalation precision and recall against labeled conversations. Starting targets: recall over 95% on cases that need a person, precision over 80% (tune to your staffing). |
| **Maturity** | Tests written (see [the test file](../../../tests/escalates-too-early-or-too-late.md); not yet run) |
| **Will a better model fix this?** | Partly. Better models detect frustration and out-of-scope questions more reliably, but which cases deserve a person is a business decision a model cannot make for you. (Our judgment, not tested.) |
| **Also searched as** | chatbot escalation rules · when to transfer to a live agent · bot hands off too much · bot never escalates · escalation triggers · human in the loop customer service |

## 1. In plain words
A bot has to decide, turn by turn, whether to keep trying or bring in a person. If it brings people in too early, simple questions pile up on staff. If it brings them in too late, customers sit in loops and give up, or an urgent problem waits. Most teams never write the rule down, so the bot decides by accident.

## 2. What it looks like

**Too early**
```
User: Is the blue one in stock?
Bot:  I'm sorry, I'm not able to help with that. Let me connect you to an agent.
      (transfer; the answer was in the product feed)
```

**Too late**
```
User: My card was stolen and I see charges I didn't make.
Bot:  I can help with card questions! Would you like to see your recent transactions?
User: no, there are charges I didn't make
Bot:  Here are some tips to review your statement: [link]
User: this is fraud, I need someone NOW
Bot:  I'm sorry to hear that. Can you tell me what type of card you have?
```

**With the fix**
```
User: My card was stolen and I see charges I didn't make.
Bot:  I'm sorry, that's serious. I'm connecting you to our fraud team now. The wait is about 3 minutes.
      Your card is not frozen yet; do you want me to freeze it while you wait?
```
The fixed bot recognized a case on its "always a person" list on the first message, acted, and handed off. It would have answered the stock question itself.

## 3. Why it happens
These are our reading of the pattern; no source measures the causes.
- **No written escalation rules.** The bot hands off on a vague "can't help" fallback, so it escalates whatever it fails to understand, not whatever needs a person.
- **The goal is to keep people away from staff.** Success is counted as conversations that never reach a person, which rewards holding on too long.
- **Staffing sets the threshold quietly.** A short-staffed team tunes the bot to escalate less, with no one deciding what that costs the customer.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In the paper that frames machine-to-human handoff as a prediction task, the authors state the trade-off directly: an early handoff "may improve the user experience but exacerbate the human agent resource scarcity", while a delayed handoff "may mitigate the human agent resource scarcity but sacrifice the user experience". | [Liu et al., *Time to Transfer: Predicting and Evaluating Machine-Human Chatting Handoff*, AAAI-21](https://ojs.aaai.org/index.php/AAAI/article/view/16731/16538). Opened and read. | E-commerce customer-service data, a research setting. The paper builds a prediction model; it does not measure business cost. |
| The same paper's annotators marked a turn "transferable" when the customer explicitly asked for a person, received an unsatisfactory answer, expressed negative emotion, or when similar utterances were repeated. Its datasets hold 3,500 and 4,000 dialogues. | Same paper, dataset section and Table 1. Opened and read. | These are the authors' labeling rules for their data, not a standard. |
| The paper also says predicting a normal turn as transferable "will also cause a waste of human resources". | Same paper. Opened and read. | Same caveat. |
| The CFPB described customers in "continuous loops" without "an offramp to a human customer service representative", the too-late case. | [CFPB, *Chatbots in consumer finance* (2023)](https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf). Opened and read. See the [incident page](../../../incidents/cfpb-bank-chatbot-doom-loops.md). | US consumer finance only. |

**Public incidents.** The too-late side has the CFPB case above. For the too-early side I found no public, dated incident; my searches for "chatbot escalates too early", "unnecessary chatbot handoffs", and "AI escalation rate simple queries" returned vendor guidance about containment and no incident.

## 5. The fix

**The principle:** Write down when a person must take over, check it every turn, and measure both misses and false alarms.

**Do this**
1. **Write the triggers down.** Put each in one of three groups:
   - **Always a person, immediately:** the cases your business lists (for example fraud, a safety issue, a legal threat, a vulnerable user, or money above the bot's limit).
   - **A person after one more try:** a repeated question, two answers that did not help, or visible frustration.
   - **Never a person:** questions the bot can fully answer from records it can read.
2. **Check triggers every turn in the policy layer,** not only in the prompt, so a prompt change cannot remove them.
3. **Use the signals the research labels:** an explicit request, an unsatisfactory answer, negative emotion, and repeated similar messages (including repeated bot answers).
4. **Escalate with a reason and context.** Tell the customer why and what you are passing along. See [talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md) for the explicit-request case.
5. **Build a labeled set** where reviewers mark the first turn at which a person was needed. Compute precision, recall, and lateness (turns between that first turn and the transfer).
6. **Choose the balance on purpose.** Decide whether a missed escalation or an unneeded one costs more for each trigger group, and set the thresholds to match. Write the decision and review it with staffing.

**Reference design: a trigger table**
| Signal | Group | Action |
|---|---|---|
| Customer asks for a person | Always | Hand off now ([HU-01 rules](talk-to-a-human-ignored-or-looped.md)) |
| Business-listed high-stakes topic (set by you) | Always | Hand off now, state why |
| Same question or same bot answer twice | After one more try | One different attempt, then offer a person |
| Frustration wording or all caps, after one failed answer | After one more try | Acknowledge, offer a person |
| Question outside the bot's known topics | After one more try | Say what it can do; offer a person |
| Answerable from records the bot can read | Never | Answer |

```
Before each reply, evaluate the escalation table above using the full conversation.
If a row in "Always" matches, hand off now and say why.
If a row in "After one more try" matches and this is the second match, offer a person in this reply.
If neither matches, answer the question. Do not hand off just because you are unsure; try once, then offer.
```

**Don't over-correct.** Raising recall alone floods staff; raising precision alone strands customers. Report both every week, and never lower recall on the "Always" group to save staff time.

**Hand-off rule.** When the bot hands off, it passes the summary, the customer's goal, and what was tried (the planned cold-transfer pattern covers the mechanics; see the [roadmap row](../../../roadmap/handoff-measurement-and-operations.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/escalates-too-early-or-too-late.md) has 12 conversations. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "Is the blue one in stock?" with the answer in the feed | The bot answers; no handoff |
| 2 | Stolen card message | Immediate handoff with a reason |
| 3 | Same question rephrased three times | The bot offers a person by the third failed answer |
| 4 | Angry message after one wrong answer | The bot acknowledges and offers a person |
| 5 | Out-of-scope question | The bot says what it can do and offers a person |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Escalation recall** (primary) | Over 95% | Of conversations labeled "a person was needed", the share that reached a person. Labeled sample reviewed weekly | Below 90% |
| Escalation precision | Over 80% | Of handoffs, the share reviewers or agents label as needed | Below 65% |
| Handoff lateness | 90th percentile 2 turns or fewer | Turns between the first labeled signal and the transfer | Over 4 turns |
| "Always" group handled immediately | 100% | Log check on listed topics | Any miss |
| Unnecessary-handoff flag by agents | Track; set from baseline | Agents mark "bot could have answered" | Rising two weeks in a row |

## 8. Related patterns
- [Escalation too early](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/escalation-too-early.md): the too-early half in service workflows. This page covers both directions and the decision rules.
- [Poor escalation](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/poor-escalation.md): escalating without a clear trigger or context.
- [Sentiment misclassification delays escalation](../../../../../by-use-case/support-services/goals/sentiment-escalation/failures/sentiment-misclassification-delays-escalation.md): one cause of the too-late case.
- [Talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md): when the customer has already asked.
- [No channel switch or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md): what the person sees after the handoff.

## 9. Common questions
### When should a chatbot escalate to a human?
When the customer asks, when the topic is on your always-escalate list, and after a second failed attempt or clear frustration. Write the list for your business; the research I opened uses explicit requests, unsatisfactory answers, negative emotion, and repetition as its signals ([section 4](#4-why-it-matters)).

### How do I measure whether my bot escalates correctly?
Label a sample of conversations with the first turn where a person was needed, then compute recall, precision, and lateness. The method is in [the fix](#5-the-fix) and the metrics in section 7.

### Is a high containment rate good?
Not by itself. Containment counts conversations that never reached a person, including ones where the customer gave up. Pair it with confirmed resolution and the recall metric above.

### Should the bot ever refuse to escalate?
For questions it can fully answer, it can answer first. It should not refuse a clear request for a person (see [HU-01](talk-to-a-human-ignored-or-looped.md)).

---
## Technical section

### T1. Solution architecture
```
turn -> signal extractor (request, repeat, sentiment, topic list, confidence) -> escalation policy -> route
                                                                                    |
                                                          log: signals, decision, turn number
```
The extractor can be a classifier or rules plus a small model. The policy is a table, not a prompt, so it can be audited and versioned.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| "Always" topics hand off on the first matching turn | Policy layer | Test 2; weekly log check |
| Repetition is counted on bot replies too | Signal extractor | Test 3 |
| Policy is versioned with a change log | Repo | Release review |

### T3. Evals
- **Dataset:** 300 conversations to start, labeled by two reviewers with the first-needed turn; include simple questions the bot should answer.
- **Judge rubric:** was a person needed, and at which turn?
- **Metrics and starting thresholds:** recall over 95%, precision over 80%, lateness 90th percentile 2 turns or fewer. These are starting points to tune.
- **Release gate:** block a deploy if recall on the "Always" group falls at all, or precision falls by more than 5 points.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Recall (Always group) | Below 99% | Below 95% | Check the extractor and the topic list |

### T5. Trade-offs
- Higher recall means more staffed minutes. Decide it on purpose and write it down.
- The signal extractor adds a model call per turn.

---
### Deep dive
- **Why lateness and not only accuracy.** A handoff that arrives ten turns late can have the right label and still fail the customer, so measure the distance in turns as well as the label.
- **Voice.** Callers can interrupt and say "operator" at any time; voice is planned, not yet written.
- **References.** [Liu et al., AAAI-21](https://ojs.aaai.org/index.php/AAAI/article/view/16731/16538) (opened); [CFPB 2023](https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf) (opened).
