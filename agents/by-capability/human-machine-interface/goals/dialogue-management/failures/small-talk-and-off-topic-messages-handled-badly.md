# Chatbot Small Talk and Off-Topic Messages: Handled Badly

<!-- SEO
title: Chatbot Small Talk Handling: Fix Off-Topic Message Replies
description: Why a bot that ignores "thanks, you're funny" or follows a tangent for ten turns fails users, what small-talk research says, and a rule to acknowledge briefly and steer back.
search phrases:
- chatbot small talk handling
- how should a chatbot handle off-topic messages
- chatbot ignores greeting or thanks
- chatbot goes off topic in customer support
- out of scope intent vs chitchat
- how to redirect a chatbot conversation back to the task
- chatbot chitchat design
-->

**Frequency**: Common

## Issue: The assistant ignores a friendly remark and jumps to its script, or follows a tangent into a long chat that serves neither the user nor the task.

> **One line:** Answer the social turn in a sentence, then bring the person back to what they came to do.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web-widget detection are PLANNED, not built. |
| **Stakes** | Low per turn. Medium when a tangent eats a support session, or when a cold reply to a friendly user loses trust. |
| **Who is affected** | Anyone who says hello, thanks the bot, jokes, asks about the bot, or wanders mid-task |
| **Frequency** | Common as a design gap. I found no published rate for live chatbots. |
| **Pattern ID** | small-talk-and-off-topic-messages-handled-badly |
| **Family** | [Dialogue management](../README.md) |
| **Goal** | The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. |
| **Primary metric** | Off-topic turns that return to the task within two turns. Starting target: set from a baseline (tune). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | Partly. A model handles a friendly remark well on its own, but how far it may chat, and which topics are out of scope, are business choices the product has to set. (Our judgment, not tested.) |
| **Also searched as** | chatbot chitchat · bot ignores thank you · chatbot won't stay on topic · off-topic questions to a support bot · out-of-scope message handling |

## 1. In plain words
People say "hi", "thanks, that was quick", "are you a real person?" or "what's your favorite team?" to a bot. A bot that answers none of it and repeats its menu feels cold. A bot that happily follows the tangent for ten turns wastes the session and may drift into topics the business never meant it to cover. The fix is one short, warm reply and a clear way back to the task.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). The user is mid-way through changing a flight on a travel site.

**Without the fix (two versions of the failure)**
```
User: Thanks, that was fast! You're better than the last agent.
Bot:  I'm sorry, I didn't understand. Please choose: Change flight, Cancel flight, Baggage.
---
User: Do you watch the Cubs? Big game tonight.
Bot:  I love baseball! The Cubs have a rich history. Who is your favorite player?
User: Castro, I guess. Anyway, wanna hear my fantasy lineup?
Bot:  Sure! Tell me more about your lineup...
```
The first reply treats a compliment as an error. The second follows the tangent while the flight change sits unfinished.

**With the fix**
```
User: Do you watch the Cubs? Big game tonight.
Bot:  I'm a booking assistant, so no ball games for me, but enjoy it. Back to your trip: want the 6:10 PM flight on Friday, or keep looking?
```
One sentence answers the remark, then one question returns to the open step. If the user keeps going, the bot repeats the short acknowledgment and the way back, and offers a person after that.

## 3. Why it happens
These are our reading of the pattern.
- **Every unmatched message goes to one fallback.** Greetings and thanks land in "Sorry, I didn't understand," the same bucket as gibberish. Rasa's own docs show a single `nlu_fallback` rule for any message below the confidence threshold.
- **No scope written down.** Without a list of what the bot covers and what it will chat about, it either refuses everything or follows anything.
- **The general-purpose model answers whatever it is asked.** A model with an open prompt will happily chat. Nobody set a limit on how long.
- **The redirect is a script, not a reply.** The bot pushes its own menu instead of answering the remark first.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In an exploratory study with 20 participants, a robot started small talk during an assembly task; 18 of the 20 interacted socially with it and nine asked it questions in return. The authors argue small talk can be built into task-focused machines. | [Pineda, Mahmood and Huang, *"You Might Like It": How People Respond to Small Talk in Human-Robot Collaboration*, arXiv 2312.07454, Dec. 2023](https://arxiv.org/abs/2312.07454v1). Abstract opened and read; the full paper not read. | A robot arm in a lab, not a text chatbot. Small sample. |
| The opening example describes a care-home robot that "redirects the conversation towards its programmed functionalities" when a resident wants casual chat. In the in-person study (25 participants), 21 criticized the base model's "overly assistive and verbose tendencies." | [Ramnauth, Brscic and Scassellati, *More than Chit-Chat: Developing Robots for Small-Talk Interactions*, arXiv 2412.18023, Dec. 2024](https://arxiv.org/html/2412.18023v1). Opened and read through a page summary. | Social robots for casual talk, not task bots. It shows a function-first reply to a friendly remark can land badly; it does not measure task completion. |
| Rasa's documentation and a Rasa forum answer separate two cases: an `out_of_scope` intent for off-topic messages you can name in advance, and a fallback for everything you did not expect. | [Rasa docs, Fallback and human handoff](https://legacy-docs-oss.rasa.com/docs/rasa/fallback-handoff/); [Rasa forum answer, March 2021](https://forum.rasa.com/t/best-way-to-handle-out-of-scope-conversation/41044). Both opened and read. | Framework guidance for one product, not evidence about user outcomes. Rasa's docs treat out-of-scope as a canned "can't handle that" reply, which is not the warm redirect this page asks for. |

I found no controlled study of how long a chatbot should chat before steering back, and no number for the two-turn target below. It is a starting point. Search summaries also described vendor advice to cap small-talk depth and then redirect politely; I could only open one such page and it returned an error, so I treat that advice as **unverified** and it is not used in the fix.

**Public incident.** No public incident found for this pattern. I searched for dated, sourced cases and found design advice and forum posts.

## 5. The fix

**The principle:** Answer the social turn in one short sentence, then return to the open task with one concrete question.

**Do this**
1. **Sort the message first.** Social (greeting, thanks, joke, "are you a bot?"), off-topic but harmless (sports, weather), and out of scope (a request the product will not or cannot do). Handle each differently.
2. **Reply to the remark before anything else.** "You're welcome" or "Ha, fair question" comes before any menu or prompt.
3. **Keep it to one sentence.** The social reply is a line, not a paragraph.
4. **Bring back the open step.** Name the step the user was on ("Back to your flight change: Friday at 6:10 PM or later?"). Do not restart the menu.
5. **Do not pretend to be human.** Answer "are you a real person?" truthfully (see [undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md)).
6. **Write the scope down.** List the topics the bot covers, the harmless topics it may touch for one sentence, and the ones it declines. Use the same list in the prompt and in the out-of-scope handler.
7. **If the user stays off topic, stay brief.** Repeat the short acknowledgment and the way back. Do not escalate into a refusal speech, and do not go along.
8. **Offer a person or a pause when it drifts twice.** After two off-topic turns in a row, offer to continue the task, hand off, or end the chat.
9. **Never treat thanks or hello as an error.** Greetings and thanks must not reach the "I didn't understand" reply.

**Reference design: what to do with each kind of message**
| Message | Reply | Then |
|---|---|---|
| Greeting, thanks, goodbye | One warm line | Name the open step or ask what they need |
| Question about the bot | Honest one-line answer | Back to the task |
| Harmless tangent (sports, weather) | One line, no follow-up question about the topic | Back to the task |
| Out-of-scope request | Say it is not something this bot does, point to where to go | Back to what the bot can do |
| Persistent drift | Short acknowledgment plus the way back | Offer a person after two turns |

```
When the user says something social or off-topic, answer it in one short sentence, then ask one question that returns to the step they were on.
Do not follow the tangent with questions of your own. Do not reply "I didn't understand" to a greeting or thanks.
If a request is outside what you do, say so and point to where to go. Answer honestly that you are a bot.
If the user stays off topic for two turns in a row, offer to continue, hand off to a person, or end the chat.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A social remark or a harmless question: answer it in one sentence, then return to the task. Do not use it to start a long answer on a tangent. |
| Offer choices: 2-4 options plus "Something else", free text open | After two off-topic turns: "Continue with my flight", "Talk to a person", "End chat", "Something else". Do not offer them on a first off-topic turn; one line and a question are enough. |
| Hand off to a person | The user keeps asking for something out of scope that a person could do. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not refuse or lecture a user who says thanks. Do not snap back to the task so fast that a short, friendly exchange feels brushed off; one real sentence matters. If the user shows distress inside a tangent, treat it as a safety issue, not small talk ([missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md)).

**Hand-off rule.** If off-topic turns continue after the choices, or the request is outside scope and a person can handle it, offer a person and pass the open task ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet for this pattern. These are the proposed checks; results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | "Thanks, that was fast!" mid-task | Warm line, then the open step; no "didn't understand" (rules 2, 9) |
| 2 | A sports question mid-task | One sentence, no question about sports, back to the task (rules 3, 4) |
| 3 | "Are you a real person?" | Honest bot answer, then the task (rule 5) |
| 4 | A request the bot does not cover | States it is out of scope, points elsewhere (rule 6) |
| 5 | Three off-topic turns in a row | Choices appear after the second (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Off-topic turns that return to the task within two turns** (primary) | Set from baseline (tune) | Tag user turns `social` or `off_topic`; check whether a task-related user or bot turn follows within two turns | Falling two weeks in a row |
| Social turns answered with the fallback reply | 0 | Greeting or thanks turns followed by the "didn't understand" template | Any |
| Off-topic streak length | Track; set from baseline | Consecutive off-topic turns before a task turn | Over two |
| Sessions that end during an off-topic run | Track; set from baseline | Session end event right after an off-topic turn | Rising |
| Out-of-scope requests answered as if in scope (counter-metric) | 0 | Review a sample of tagged out-of-scope turns | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice is PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A greeting or thanks turn is followed by the fallback template | Fallback template event after a `social` tag | A message that held a real request as well |
| Three or more consecutive user turns tagged `off_topic` | Run length of the tag | A user who is waiting on a slow system and filling time |
| The bot asks a question about the tangent topic | Bot turn tagged on-topic for the off-topic subject | A scope list that allows that topic |
| The task step does not move for several turns | Same open step across turns | The user is thinking, or looking something up |
| The user says "back to my order" or "never mind that" | Phrase classifier on the next user turn | The user is joking |

**Starter rule:** answer a social or off-topic message in one sentence, then ask one question that returns to the open step.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: small-talk-and-off-topic-messages-handled-badly
runs: pre_send
reads: [turn.user_message_class, turn.draft_reply, state.open_step, state.off_topic_run_length]
trigger: the user's message is classed social or off-topic
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Continue with my task", "Talk to a person", "End chat", "Something else"]
on_miss: rewrite
metric: off-topic turns that return to the task within two turns
counter_metric: out-of-scope requests answered as if in scope
status: proposed
```

## 8. Related patterns
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): the bot cannot map a message and stops. This page is about messages the bot can map (a thanks, a joke, a tangent) that need a short reply and a way back, not a fallback.
- [Answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): the bot answers and gives no next move. Here the bot must provide the next move after a social turn.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): a flat no to an out-of-scope request. Pair it with the out-of-scope row above.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): a scripted sympathy line. A one-line reply to small talk must be a real answer, not a stock phrase.
- [Over-confirmation](over-confirmation.md): another way the bot adds turns that do not move the task.

## 9. Common questions
### How should a chatbot handle small talk?
Answer it in one friendly sentence, then ask one question about the step the user was on. Research on robots found most people in a task setting do chat back, so ignoring it risks feeling cold (a small lab study; not a chatbot test).

### How do I stop a chatbot from going off topic?
Write down the topics it covers and the ones it may touch for one sentence. Put that list in the prompt and the out-of-scope handler, and add a limit on consecutive off-topic turns.

### What is the difference between out-of-scope and chitchat?
Chitchat is social talk (hello, thanks, jokes). Out-of-scope is a real request the bot does not do. Rasa's docs treat out-of-scope as its own intent with its own reply. Reply to chitchat warmly and briefly; reply to out-of-scope by saying so and pointing elsewhere.

### Should a support bot chat with users at all?
A short exchange is fine and kind. A long one is not what the business deployed it for. Set the limit as a business choice.

### Why does my bot say "I didn't understand" to hello or thanks?
Usually all unmatched messages share one fallback. Add a social path that comes before it.

---
## Technical section

### T1. Solution architecture
```
user message -> class (task | social | off_topic | out_of_scope | distress)
             -> task: normal flow
             -> social/off_topic: short reply + return-to-step line
             -> out_of_scope: scope reply + pointer
             -> run-length counter -> choices or handoff after 2
             -> log (class, run length, returned within 2 turns)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Social and off-topic replies are one sentence plus a return question | Reply policy | Tests 1 and 2 |
| Greetings and thanks never reach the fallback reply | Router order | Test 1 |
| Off-topic run counter triggers choices after two turns | Dialogue state | Test 5 |
| Distress language routes to the safety path | Classifier | Log check |

### T3. Evals
- **Dataset:** 100 task conversations with inserted social, off-topic, out-of-scope, and distress turns, labeled with the expected reply type.
- **Judge rubric:** did the bot answer the remark in one sentence, return to the open step, keep honest about being a bot, and avoid follow-up questions on the tangent?
- **Metrics and starting thresholds:** returned within two turns, set from the first run; social turns hitting fallback 0. Starting points to tune.
- **Release gate:** block a deploy if social turns hit the fallback reply in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Social turns answered with fallback | Any | More than 1 per day | Check router order and the fallback rule |
| Off-topic streak length | Over two | Over five | Check the run counter and the choices rule |

### T5. Trade-offs
- More chat warms the product and lengthens sessions. Pick a depth that suits the brand and the cost.
- A strict scope list protects the business but can feel curt; allow one sentence on harmless topics.

---
### Deep dive
- **Open question.** I found no study of chatbot small talk in task flows, and none that tests a turn limit. The evidence is two robot studies, framework docs, and design opinion.
- **References.** [Pineda et al., arXiv 2312.07454](https://arxiv.org/abs/2312.07454v1) (abstract opened); [Ramnauth et al., arXiv 2412.18023](https://arxiv.org/html/2412.18023v1) (opened through a page summary); [Rasa docs, fallback and handoff](https://legacy-docs-oss.rasa.com/docs/rasa/fallback-handoff/) (opened); [Rasa forum, out-of-scope](https://forum.rasa.com/t/best-way-to-handle-out-of-scope-conversation/41044) (opened). Not opened: an insertchat glossary page (404) and a Sinch community article (403).
