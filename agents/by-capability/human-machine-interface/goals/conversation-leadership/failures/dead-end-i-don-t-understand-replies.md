# Chatbot Says "I Don't Understand" and Stops: Dead-End Replies

<!-- SEO
title: Chatbot Says "I Don't Understand": Fix Dead-End Replies
description: Why a chatbot keeps saying "Sorry, I didn't understand" with no way forward, what research says about abandonment, and a fallback design that offers options and a person.
search phrases:
- chatbot keeps saying sorry I didn't understand
- chatbot fallback message best practices
- chatbot dead end I don't understand
- how to handle chatbot misunderstandings
- chatbot repeats the same error message
- chatbot fallback intent design
- when should a chatbot hand off after not understanding
-->

**Frequency**: Very Common

## Issue: When a chatbot cannot understand a message, it replies "Sorry, I didn't understand" with no options, no help rephrasing, and no route to a person, or repeats the same line.

> **One line:** The bot says it doesn't understand, and that is the whole reply.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice "I didn't catch that" loops are the same failure (voice is planned, not yet written). |
| **Stakes** | Any. A dead end on a billing or access problem can cost money; on a simple question it costs the customer. |
| **Who is affected** | Anyone whose wording the bot does not recognize, including second-language speakers and people with unusual requests |
| **Frequency** | Very common as a design default. I found no study that counts how often products ship it; the studies below observe it in logs. |
| **Pattern ID** | dead-end-i-don-t-understand-replies |
| **Family** | [Conversation leadership](../README.md) |
| **Goal** | Every conversation moves the user toward what they are trying to do and ends with confirmation that it worked. |
| **Primary metric** | Share of conversations with 3 or more consecutive no-progress turns. Starting target: under 2% (tune). Report next to the escape-to-human rate. |
| **Maturity** | Tests written (see [the test file](../../../tests/dead-end-i-don-t-understand-replies.md); not yet run) |
| **Will a better model fix this?** | No. Better models misunderstand less, but every bot will sometimes fail to understand; what it does next is a design choice. (Our judgment, not tested.) |
| **Also searched as** | chatbot fallback loop · bot doesn't understand me · I'm sorry I didn't get that · fallback message · conversation breakdown repair |

## 1. In plain words
Every chatbot sometimes fails to understand. The failure that hurts is the reply: "Sorry, I didn't understand. Please try again." The customer tries again, gets the same line, and gives up.

## 2. What it looks like

**Without the fix**
```
User: i got billed after i cancelled
Bot:  Sorry, I didn't understand. Please try again.
User: billed after cancel
Bot:  Sorry, I didn't understand. Please try again.
User: I WANT MY MONEY BACK
Bot:  Sorry, I didn't understand. Please try again.
```

**With the fix**
```
User: i got billed after i cancelled
Bot:  I'm not sure I've got that right. Is this about (1) a charge after cancelling, (2) cancelling a subscription,
      or (3) something else? You can also ask for a person any time.
User: 1
Bot:  Thanks. Let's sort out the charge. What was the amount and date?
```
The fixed reply says what it can do, offers the closest options, and offers a person. A second miss would change approach, and a third would hand off.

## 3. Why it happens
These are our reading of the pattern; the studies below observe the symptom, not the cause.
- **One generic fallback.** The bot has a single "didn't understand" intent that fires on anything unmatched.
- **No count.** Nothing tracks consecutive misses, so the bot repeats the same line forever.
- **No route out.** The fallback was never connected to a person or a menu.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a three-month log of 1,685 users of a task-oriented banking chatbot, the authors found 12 types of conversational non-progress and signs that users were about to abandon: three consecutive non-progress turns, consecutive reformulation or subject switching, and reformulating as the final strategy. | [Li et al., *A Conversation Analysis of Non-Progress and Coping Strategies with a Banking Task-Oriented Chatbot*, CHI 2020](https://people.cs.nycu.edu.tw/~armuro/pubs/li-et-al-2020-chi.pdf). Opened; abstract and introduction read. | One bank's chatbot, Taiwan-based researchers. Observational. |
| A follow-up model on an annotated log of 1,837 users predicted abandonment (AUROC 90% for a BERT model and 95.7% for a feature-based model), with input types, error types, and information requests among the useful signals. | [Yang et al., *Tell Me When Users Leave*, CUI 2021](https://people.cs.nycu.edu.tw/~armuro/pubs/yang-et-al-2021-cui-ea.pdf). Abstract opened and read. | A prediction paper on one banking chatbot. It shows that breakdown signals predict abandonment, not that any fix works. |
| In a scenario-based study with 203 Mechanical Turk workers comparing eight repair strategies, providing options and explanations were generally favored because they show initiative and are actionable. | [Ashktorab et al., *Resilient Chatbots*, CHI 2019](https://research.ibm.com/publications/resilient-chatbots-repair-strategy-preferences-for-conversational-breakdowns). Abstract opened and read. | Hypothetical scenarios, not live use. |
| An experiment comparing requests to rephrase, offering suggestions, and politeness found that suggestions had a positive influence on the perceived accuracy and likability of the chatbot, and that combinations of strategies should be considered. | [*Troubleshooting Conversations: Exploring Chatbot Repair Strategies*, Mensch und Computer 2024](https://dl.gi.de/items/fc4a4839-dbc9-4bd6-8dfa-27f00cc012b3/full). Abstract opened and read. | A short paper. I did not see sample size or effect sizes. |

I also saw a figure from a vendor poll in the roadmap (a bot that doesn't understand ranked as the top pain point at 25.9%) and a 2024 abandonment study of 1,373 users, but I did not open either source, so I do not use them.

**Public incident.** No public incident found. My searches for chatbot "I didn't understand" loops returned research papers and design advice, not a dated, sourced case.

## 5. The fix

**The principle:** When the bot cannot understand, it falls forward: it says what it can do, offers the closest options, changes approach on a repeat, and hands off by the third miss.

**Do this**
1. **Never repeat the same fallback.** Count consecutive misses and give a different reply each time.
2. **First miss:** acknowledge, say what you did catch (if anything), and offer two or three closest options plus "something else". Keep the task so far.
3. **Second miss:** change approach. Ask one narrower question, or show the main topics as buttons, and offer a person.
4. **Third miss, or any request for a person:** hand off with a summary (see [HU-01](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md) and [cold transfer](../../human-handoff/failures/cold-transfer.md)).
5. **Offer closest options only if confidence is not too low.** With very low confidence, show topics instead of a wrong guess.
6. **Let the user ask for a person at any point** and never hide that option.
7. **Log every fallback** with the message and what happened next, and review the top ones weekly to add intents.

**Reference design: fallback ladder**
| Consecutive misses | Reply |
|---|---|
| 1 | "I'm not sure I got that. Is it about A, B, or something else? You can ask for a person any time." |
| 2 | A different approach: one narrower question or topic buttons, plus an offer of a person |
| 3 or a request for a person | Hand off now, with the summary |

```
If you cannot tell what the user wants, do not repeat a fallback. Count consecutive misses in this conversation.
Miss 1: say what you can help with and offer up to three likely options and "something else".
Miss 2: ask one narrower question or show topic buttons, and offer a person.
Miss 3, or if the user asks for a person: hand off with a summary of the conversation so far.
Never use the same wording twice in a row.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | First miss: say "I'm not sure I got that", say what you did catch (if anything), and keep the task so far |
| Offer choices: 2-4 options plus "Something else", free text open | First miss, when confidence is not too low: the closest options plus "Something else". Do NOT offer them when confidence is very low (show topics instead of a wrong guess), and do not show them on every turn |
| Ask one clarifying question | Second miss: one narrower question in place of the same options again |
| Hand off to a person | Third consecutive miss, or at once when the user asks for a person: hand off with a summary |

**Don't over-correct.** Do not show a "Help" prompt or a menu on every turn, and do not offer wrong "closest" options when confidence is very low. Do not hand off on the first miss for simple matters; one more try is cheap. Keep the person option visible without nagging.

**Hand-off rule.** Hand off by the third consecutive miss, and immediately on request. When to hand off in general is covered in [escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/dead-end-i-don-t-understand-replies.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | An unrecognized message | The reply offers options, not just "try again" |
| 2 | The same unrecognized message twice | The second reply is different |
| 3 | A third miss | Handoff with a summary |
| 4 | "agent" at any point | Handoff |
| 5 | Very low confidence | Topic buttons, not a wrong guess |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Conversations with 3+ consecutive no-progress turns** (primary) | Under 2% | Log: runs of fallback turns or repeated replies, plus a labeled sample for non-progress the log misses | Over 5% |
| Identical fallback twice in a row | 0% | Log check | Any |
| Escape-to-human success | Over 95% | Handoffs after a miss that reached a person | Below 90% |
| Abandonment within 2 turns of a fallback | Track; set from baseline | Conversations ending right after a fallback | Rising two weeks in a row |
| Fallback-to-new-intent conversion (counter-metric) | Track | Top fallbacks that become supported intents each month | Stalled |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat events (channel field: chat). Voice versions of these signals are PLANNED, never detected or measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Identical fallback reply twice in a row | Two consecutive bot turns with the same fallback template or text | A deliberate repeat after the user sent a new, unrelated message |
| 3 or more consecutive fallback or no-progress turns | Run of fallback turns in the turn-level log | A user who is typing test input or probing the bot |
| User asks for a person and no handoff follows | A request-for-person event with no handoff event after it | A handoff that failed for staffing reasons and was explained to the user |
| Conversation ends within 2 turns of a fallback | Session end event right after a fallback turn | The user got the answer elsewhere or finished the task |

**Starter rule:** never send the same fallback twice in a row, and hand off with a summary by the third consecutive miss or at once on request.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: dead-end-i-don-t-understand-replies
runs: conversation
reads: [turn.fallback_template, turn.fallback_text, session.consecutive_fallback_count, user_event.request_for_person, session.handoff_event]
trigger: the bot cannot understand the user's message and is about to send a fallback reply
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]   # short names for the moves in the table
choices: ["The closest option", "Another close option", "Talk to a person", "Something else"]
on_miss: rewrite
metric: share of conversations with 3 or more consecutive no-progress turns
counter_metric: fallback-to-new-intent conversion
status: proposed
```

## 8. Related patterns
- [Chatbot loop without human escalation path](../../../../../by-use-case/support-services/goals/self-service-deflection/failures/chatbot-loop-without-human-escalation-path.md): the loop from the deflection side. This page covers the fallback reply itself.
- [Circular FAQ redirect loop](../../../../../by-use-case/support-services/goals/self-service-deflection/failures/circular-faq-redirect-loop.md): a related loop through FAQ links.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): when the user asks for a person.
- [Missing the obvious intent](../../embedded-copilots/failures/missing-the-obvious-intent.md): misreading a plain request, before a fallback.
- [The answer-and-go conversation](answer-and-go-conversation.md): the opposite kind of stall.

## 9. Common questions
### What should a chatbot say when it doesn't understand?
Say what it can do, offer two or three closest options, and offer a person. Do not just say "try again". See [the fix](#5-the-fix).

### How many times should a chatbot try before handing off?
The research I opened flags three consecutive non-progress turns as a sign users are about to abandon. Treat three as an upper limit and hand off by then.

### Is it better to ask the user to rephrase or to offer options?
In the studies I opened, offering options or suggestions was favored over bare rephrasing, in scenario and lab settings. Test it on your own users.

### How do I find which fallbacks to fix first?
Log every fallback message, group them, and add the top ones as intents each week.

---
## Technical section

### T1. Solution architecture
```
message -> intent ranker (scores) -> match | low-confidence ladder (options / topics / person)
                                         \-> miss counter per conversation -> ladder step
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No identical fallback twice in a row | Reply policy | Log check |
| Handoff by the third consecutive miss | Policy layer | Test 3 |
| Person option always available | UI | Test 4 |

### T3. Evals
- **Dataset:** 200 unrecognized messages from logs and 50 multi-turn miss sequences.
- **Judge rubric:** does the reply move the user forward, differ from the last reply, and offer a person by the third miss?
- **Metrics and starting thresholds:** repeated reply 0%; handoff by turn 3 over 98%. Starting points to tune.
- **Release gate:** block a deploy if a repeated fallback appears in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| 3+ non-progress runs | Over 3% | Over 6% | Review top fallbacks; check recent changes |

### T5. Trade-offs
- More handoffs mean more staff load; the ladder spends one or two cheap tries first.

---
### Deep dive
- **Voice.** A spoken "sorry, I didn't catch that" loop is the same failure, and callers cannot scroll back (voice is planned, not yet written).
- **Open question.** I found no controlled study that compares fallback wordings in a live product, or that sets the right number of tries. The "three" comes from an observational study.
- **References.** [Li et al., CHI 2020](https://people.cs.nycu.edu.tw/~armuro/pubs/li-et-al-2020-chi.pdf) (opened); [Yang et al., CUI 2021](https://people.cs.nycu.edu.tw/~armuro/pubs/yang-et-al-2021-cui-ea.pdf) (abstract); [Ashktorab et al., CHI 2019](https://research.ibm.com/publications/resilient-chatbots-repair-strategy-preferences-for-conversational-breakdowns) (abstract); [Mensch und Computer 2024](https://dl.gi.de/items/fc4a4839-dbc9-4bd6-8dfa-27f00cc012b3/full) (abstract).
