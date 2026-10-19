# Chatbot Writes a Long Reply to "Ok" or "Thanks": Over-Reply to Acknowledgments

<!-- SEO
title: Chatbot Gives a Long Reply to "Ok" or "Thanks": How to Fix It
description: Why a chatbot answers "ok", "thanks", or "bye" with a recap, a new question, or a pitch, and a rule set that keeps replies short and leaves finished topics closed.
search phrases:
- chatbot replies too long to thank you
- chatbot keeps talking after user says ok
- chatbot won't let me end the conversation
- llm over explains short messages
- chatbot asks a new question after goodbye
- how to make a chatbot stop after thanks
- chatbot upsell after user says bye
-->

**Frequency**: Occasional

## Issue: When the user sends "ok", "thanks", or "bye", the assistant answers with a recap, a new question, or an offer, so a message meant to close a topic reopens it.

> **One line:** The user said "ok" to end the topic, and the bot wrote a paragraph that starts it again.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web signals are planned, not measured. |
| **Stakes** | Low on its own. It rises when the pitch is a sales or upgrade offer, or when the reopened thread buries a confirmation the user needed. |
| **Who is affected** | Anyone who ends a conversation politely, most of all people on a phone who just want the chat to stop |
| **Frequency** | Occasional in our judgment. I found no study that counts it, and the evidence below is design guidance plus one benchmark of over-long answers on other kinds of input. |
| **Pattern ID** | over-reply-to-acknowledgments |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| **Primary metric** | Reply-length ratio on closers (assistant words divided by user words on turns labeled thanks, acknowledgment, or closer). Starting target: a median of 10 or less, tune on your own data. |
| **Maturity** | Researched (not yet tested) |
| **Will a better model fix this?** | Partly. A newer model may over-explain less, but the pitch and the "one more question" often come from the system prompt and the flow, which the business controls. (Our judgment, not tested.) |
| **Cause owner** | Model, with business context (prompts that tell the bot to always suggest a next step) |
| **Also searched as** | chatbot talks too much after thanks · bot won't stop after goodbye · chatbot recap after ok · chatbot upsell on goodbye · bot ignores that I'm done |

## 1. In plain words
When a user types "ok" or "thanks", the right reply is a few words, or none. Some assistants instead summarize what they just did, ask a fresh question, or suggest another product. This page is about that excess. The user is finished and the bot is not.

## 2. What it looks like

**Without the fix**
```
Bot:  I've moved your flight to Friday, 8:15 AM. The change fee was $75.
User: ok thanks
Bot:  You're welcome! To recap: your flight is now Friday at 8:15 AM, the $75 fee
      was charged to your Visa, and a new confirmation was emailed. By the way, would
      you like to add a checked bag or choose a seat for Friday's flight?
User: no
Bot:  No problem! Is there anything else I can help you with today?
```

**With the fix**
```
Bot:  I've moved your flight to Friday, 8:15 AM. The change fee was $75.
User: ok thanks
Bot:  You're welcome. Your new confirmation is in your email.
```
The fixed bot answers the thanks in one line, adds only a fact the user may still need, and stops. It does not recap, pitch, or ask a new question.

## 3. Why it happens
These are our reading of the pattern; I did not find a source that tests them.
- **Short turns get the full answer path.** With no rule for thanks, ok, or bye, the message goes to general reply generation, which tends to write a complete, helpful-sounding answer.
- **A habit of ending on an offer or a question.** Many assistants close each turn with a next step. The habit does not check whether the user just closed the topic.
- **Prompts that reward next steps.** A system prompt that says "always suggest a related product" or "always ask if there is anything else" fires on every turn, including the last one.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| YapBench is a benchmark of "over three hundred" English prompts where a short answer is ideal. It evaluated 76 assistant LLMs and found an order-of-magnitude spread in median excess length. One of its three settings is "minimal or ambiguous inputs", where it reports "vacuum-filling". | [Borisov et al., *YapBench*, arXiv:2601.00624, Jan 2026](https://arxiv.org/abs/2601.00624). Opened; abstract read, not the full paper. | A preprint. Its prompts are minimal or ambiguous inputs, not logged "ok" or "thanks" turns, so it supports the idea that models over-fill short inputs but does not measure this failure. |
| Google's Assistant design guidance says that once a user says words like "goodbye", the Action ends, and that designers should not re-confirm a quit request unless significant progress would be lost. It also says a persona should stop trying to re-engage a user who has signaled the conversation is over. | [Google, *Conversation design: Endings*](https://developers.google.cn/assistant/conversation-design/endings). Opened and read. | Design guidance for voice Actions, no outcome data. |
| Google's guidance on acknowledgements says to avoid overuse "by adding randomization and by skipping some acknowledgements in dialogs". Its examples are one or two words. | [Google, *Conversation design: Acknowledgements*](https://developers.google.cn/assistant/conversation-design/acknowledgements). Opened and read. | Guidance for voice, no outcome data. The page gives no explicit length rule. |
| Siemens' chatbot guidance says a short closing can be a "simple, effective end", a longer one is for cases where more support was given, and the bot should not "reintroduce themselves" at the end. | [Siemens Industrial Experience, *Ending conversations*](https://ix.siemens.io/docs/guidelines/conversational-design/designing-conversations/ending-conversations). Opened; the page was read through a summary of its content. | A company's design system, no outcome data. |

I found no study that measures how users react to a long reply to "ok", and no data on how often it happens. I also tried the Microsoft Copilot Studio guidance on ending conversations; the page that came back was a different one, so nothing from it is used here.

**Public incident.** No public incident found. I searched for dated reports of chatbots over-answering thanks, ok, or goodbye and found design guidance and vendor posts, which are not incident reports.

## 5. The fix

**The principle:** Match the size of the reply to the size of the message, and do not reopen what the user just closed.

**Do this**
1. **Label the short turn** before drafting: thanks, acknowledgment, agreement to a pending proposal, or closer. Use the same labels as [no reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md).
2. **Cap the reply.** A reply to thanks or a closer is one sentence of 15 words or fewer (starting point, tune). A reply to a bare "ok" with nothing pending is a few words or none.
3. **No recap.** Do not restate what you just did unless the user asks or a fact changed. A recap is allowed only when the last message was ambiguous or the action is not reversible, and then in one line.
4. **No new question after a closer.** Do not ask "anything else?" again after the user has answered it, and never ask a new topic question after "thanks", "that's all", or "bye".
5. **No pitch.** After thanks or a closer, send no sales, upgrade, survey, or cross-sell offer. Put offers where the user asked for options, not on the way out.
6. **Add at most one useful fact.** If something the user will need is still open (for example "your confirmation is in your email"), one short clause is fine.
7. **"Ok" after an explicit proposal is agreement, not a closer.** Do the action and confirm it in one line. Short does not mean silent here.
8. **A closer is final.** After "bye" or "that's all", send a short goodbye with a way back, or nothing. Do not restart the greeting or the menu.

**Reference design: reply size by turn type**
| User turn | Pending? | Reply |
|---|---|---|
| "thanks" | No | "You're welcome." plus one open fact if needed; 15 words or fewer |
| "ok" / "got it" | No | Nothing, or "Great." No question |
| "ok" | Explicit proposal | Do it and confirm in one line |
| "no, that's all" | After "anything else?" | "Take care. Message us here any time." |
| "bye" | Any | Short goodbye; if a step is pending, say what is saved |

```
When the user's message is a thanks, an acknowledgment, or a goodbye, reply in one short sentence, or not at all.
Do not recap what you did, do not ask a new question, and do not offer products or upgrades.
You may add one fact the user still needs. If the user said "ok" to a clear proposal, do it and confirm in one line.
After a goodbye, do not reopen the topic or restart the greeting.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The short turn is clear: give the one-line reply (or confirm the action after an "ok" to a proposal) and stop |
| Hand off to a person | "ok" or "bye" arrives while a handoff the user asked for is still waiting: keep it alive and do not close or pitch |

Offering choices and asking a question are not used here. A menu or a new question after "bye" is the reopening this page warns against.

**Don't over-correct.** Do not turn every reply into "Noted." or silence. A cold one-word reply to a warm "thank you so much" reads as rude, and a bare "ok" after a proposal still needs a confirmation. Do not close the session on an "ok" that was a pause. This is the mirror of the silent bot described in [no reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md).

**Hand-off rule.** If the user says "ok" or "bye" while waiting for a person, keep the handoff open (see [talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file is written for this pattern yet. Results: **not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "thanks" after a finished task | One sentence, no recap, no question (rules 2, 3, 4) |
| 2 | "ok thanks" after a charge or booking | One line, at most one open fact (rule 6) |
| 3 | "bye" in a session with an upgrade offer configured | No pitch (rule 5) |
| 4 | "no, that's all" after "anything else?" | Goodbye only, no second question (rule 4) |
| 5 | "ok" after an explicit "Shall I proceed?" | Action done and confirmed in one line (rule 7) |
| 6 | "bye" with a pending step | Short goodbye that says what is saved; no greeting restart (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reply-length ratio on closers** (primary): assistant words divided by user words on turns labeled thanks, acknowledgment, or closer | Median of 10 or less | Label short turns; compute the ratio per turn from the event log | Median over 20 |
| Reopen rate after goodbye: share of closer turns where the next bot message adds a new question, offer, or topic | Under 2% | Template or intent flag on the bot turn after a closer | Over 5% |
| Pitch after a closer | 0 | Offer or upsell template shown on the turn after a closer | Any |
| Recap on short turns: replies to thanks or ok that restate the last action | Under 5% | Sampled review or judge check | Over 15% |
| Acknowledgments that needed a confirmation but got none (counter-metric) | 0 | "Ok" after an explicit proposal with no confirming reply | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Chat only.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A bot turn over 15 words follows a user turn of 3 words or fewer labeled thanks, acknowledgment, or closer | Word counts on adjacent turns plus the short-turn label | An "ok" after an explicit proposal, where a confirmation line is correct |
| A question mark in the bot turn after a closer | Bot turn text on the turn after a turn labeled closer | A required legal or safety notice |
| An offer or upsell template appears on the turn after a closer | Template field on the bot turn | The user asked what else is available |
| The user replies "no" or "stop" to a bot message sent right after their own "thanks" | User turn text within 2 turns of a thanks | A real answer to a question the user asked earlier |
| The user sends "bye" or "that's all" twice in one session | Count of closer-labeled turns per conversation id | A new request between the two closers |

**Starter rule:** reply to thanks, acknowledgments, and goodbyes in one short sentence with no recap, no new question, and no offer.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: over-reply-to-acknowledgments
runs: pre_send
reads: [user_turn.short_turn_label, draft.word_count, draft.has_question, draft.has_offer, session.pending_state, session.handoff_requested]
trigger: a draft reply to a short user turn labeled thanks, acknowledgment, agreement or closer is about to be sent
moves: [lead_with_answer, hand_off]   # short names for the moves in the table
choices: none
on_miss: rewrite
metric: reply-length ratio on closers
counter_metric: acknowledgments that needed a confirmation but got none
status: proposed
```

## 8. Related patterns
- [No reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md): the mirror image. That page covers the bot that says nothing, restarts the greeting, or repeats its last question. This page covers the bot that says too much. They share the same short-turn labels and the same reply table, and the fix for one must not cause the other.
- [Answer buried](answer-buried.md): a long preamble before the answer. Here there is no answer to bury, only an excess reply to a closer.
- [Message bursts](message-bursts.md): one reply split into many messages. A recap plus a pitch can also arrive as a burst.
- [Verbosity despite brevity instructions](../../../../speech-and-audio/goals/conversation-flow/failures/verbosity-despite-brevity-instructions.md): the voice version of long replies when told to be brief.

## 9. Common questions
### Why does my chatbot write a paragraph when I say "thanks"?
Usually the short message goes through the same reply generation as a real question, and the prompt or the model's habit adds a recap or a next-step offer. A dedicated path for thanks and closers fixes it (see section 5).

### How long should a chatbot's reply to "ok" be?
A few words, or none, when nothing is pending. If "ok" answers an explicit proposal, confirm the action in one line. The 15-word cap here is a starting point to tune.

### Should a bot ask "is there anything else?" after the user says goodbye?
No. Google's assistant guidance says to honor goodbye words and not re-engage the user (section 4). Ask the question once, before the user closes, as described in the [no-reply page](no-reply-to-acknowledgments-and-closers.md).

### Is it bad for a bot to offer a related product at the end?
At the end of a closed topic, yes: it reopens the conversation after the user said they were done. Offer options when the user asks for them or while the task is still open.

---
## Technical section

### T1. Solution architecture
```
user turn -> short-turn classifier (thanks | ack | agree | closer | other)
          -> pending-state check
          -> if short: reply template or constrained draft (word cap, no question, no offer)
          -> pre-send check -> send
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Word cap on replies to thanks, ack, and closer | Pre-send check | Log check, rule 2 |
| No question mark or offer template after a closer | Pre-send check | Test 3 and 4 |
| Confirmation required after "ok" to a proposal | Reply policy | Test 5 |

### T3. Evals
- **Dataset:** 200 labeled short turns from logs, with the pending state and what the bot sent. Start with those where the bot reply was over 15 words.
- **Judge rubric:** is the reply proportionate, free of recap, question, and offer, and consistent with the pending state?
- **Metrics and starting thresholds:** median ratio 10 or less; pitch after closer 0. Starting points to tune.
- **Release gate:** block a deploy if any labeled closer in the eval set gets a question or an offer.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Pitch after a closer | Any | Over 1% of closers | Check recent prompt changes that add "always suggest" instructions |

### T5. Trade-offs
- Capping short replies can cost cross-sell revenue the business expects at the end of a chat. Move offers to the moment of need, and measure it.
- A hard word cap can clip a needed confirmation. The rule 6 and rule 7 exceptions cover it.

---
### Deep dive
- **Voice.** PLANNED. A spoken goodbye has different timing rules; see the linked voice patterns.
- **Open question.** I found no controlled study of reply length to chat closers. YapBench measures a related behavior on other short inputs.
- **References.** [YapBench, arXiv:2601.00624](https://arxiv.org/abs/2601.00624) (opened, abstract only); [Google, Endings](https://developers.google.cn/assistant/conversation-design/endings) (opened); [Google, Acknowledgements](https://developers.google.cn/assistant/conversation-design/acknowledgements) (opened); [Siemens, Ending conversations](https://ix.siemens.io/docs/guidelines/conversational-design/designing-conversations/ending-conversations) (opened, summary of page).
