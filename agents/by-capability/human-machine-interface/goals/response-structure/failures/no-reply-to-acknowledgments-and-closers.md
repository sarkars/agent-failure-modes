# Chatbot Goes Silent or Loops After "Thanks", "Ok", or "Bye": No Reply to Acknowledgments and Closers

<!-- SEO
title: Chatbot Ignores "Thanks", "Ok" and "Bye": How to Handle Acknowledgments and Closers
description: Why chatbots go silent, restart, or keep asking "anything else?" when a user says thanks, ok, or goodbye, what the evidence says about conversation closings, and a rule set for replying and ending cleanly.
search phrases:
- chatbot doesn't respond to thank you
- how should a chatbot respond to thanks
- chatbot keeps asking is there anything else
- chatbot response to ok
- how to end a chatbot conversation gracefully
- chatbot closing message best practices
- chatbot restarts after user says bye
-->

**Frequency**: Common

## Issue: When the user sends "ok", "thanks", "got it", or "bye", the assistant says nothing, restarts the menu, or repeats its last question, so the user cannot tell whether the conversation is over.

> **One line:** The user closes the loop, and the bot either leaves it hanging or reopens it.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice call endings are covered by [graceless call ending](../../../../speech-and-audio/goals/conversation-flow/failures/graceless-call-ending.md) and [premature call ending](../../../../speech-and-audio/goals/conversation-flow/failures/premature-call-ending.md). |
| **Stakes** | Low on its own. It matters more when the "ok" is an agreement to a charge, a booking, or a handoff the bot then treats as unanswered. |
| **Who is affected** | Everyone who ends a conversation politely, which is most users |
| **Frequency** | Common in practice, but I found no study that counts it. The evidence below is design guidance and small experiments. |
| **Pattern ID** | no-reply-to-acknowledgments-and-closers |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| **Primary metric** | Handling correctness on labelled acknowledgment and closer turns. Starting target: over 95% (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/no-reply-to-acknowledgments-and-closers.md); not yet run) |
| **Will a better model fix this?** | Partly. A strong model usually replies to "thanks" on its own, but the "ok" that means "go ahead" and the end-of-session rules are product decisions. (Our judgment, not tested.) |
| **Also searched as** | bot doesn't say you're welcome · chatbot stuck after goodbye · is there anything else loop · end chat politely · acknowledgment tokens in chat |

## 1. In plain words
People end conversations in small steps: "ok", "thanks", "bye". A person answers each with something short. A bot often does one of three things instead: nothing, a restart ("Hi! How can I help you today?"), or the same "Is there anything else?" again.

## 2. What it looks like

**Without the fix**
```
Bot:  Your return label is in your email. Anything else?
User: no that's all, thanks
Bot:  Is there anything else I can help you with?
User: no
Bot:  Hi! I'm Ava. What can I help you with today?
User: bye
(no reply; the chat window stays open)
```

**With the fix**
```
Bot:  Your return label is in your email. Anything else?
User: no that's all, thanks
Bot:  You're welcome. If the label doesn't arrive, message us here any time. Bye for now.
User: bye
(chat ends; a transcript option is shown)
```
The fixed bot treats "no, that's all" as the end, answers the thanks once, offers a way back, and stops. It does not ask the question a second time.

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom and the design remedy.
- **Closers are not in the flow.** The bot's intents cover requests, so "thanks" and "ok" fall through to fallback or a restart.
- **A loop without an exit rule.** A flow that ends only on exact phrasing keeps replaying its last message when the user says something slightly different.
- **One word, several meanings.** "Ok" can mean "I agree", "I understand", "go ahead", or "I'm leaving", and the bot has one response for all.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a within-participants experiment with 27 Japanese participants and an android robot, a dialogue closing system (extra turns before exit) scored higher on likeability (p = 0.04) than a version without it. The abstract also reports better politeness and dialogue satisfaction than the control. | [Uchida, Kameo and Ishiguro, *Scientific Reports*, 2024](https://www.nature.com/articles/s41598-024-81353-7). Opened; abstract and results read. | A physical robot, a sightseeing conversation, young Japanese participants, a short lab session. I read only the likeability result in detail. It is not a chatbot study. |
| A conversation-design pattern library describes a closing as a sequence: a last topic check, then pleasantries such as thanks and an offer of future contact, then "goodbye" answered by "goodbye". | [OpenDialog, *Closing: example dialog*](https://patterns.opendialog.ai/the-pattern-library/closing/example-dialog). Opened; the page is short and read in full. | A vendor's design guidance with one sample dialog and no outcome data. |
| An AI voice-agent vendor reports a real B2B sales deployment where the agent ended calls when callers said "thank you" or "no" mid-call. Its fix was a checklist: end only after a closing question, an explicit "no", and a spoken goodbye. | [Edesy, *Why Your AI Voice Agent Hangs Up Too Early*, 2026](https://edesy.in/blog/why-ai-voice-agent-hangs-up-too-early-fix-2026). Opened and read. | A vendor blog about voice, not chat. It gives no counts. It shows the mirror-image failure (ending too early). |

I did not find a study that measures what chat users do when a bot ignores "thanks", or that compares replies to a bare "ok". Material from the roadmap on "ok" as a topic transition (conversation analysis) is not used here because I did not open it.

**Public incident.** No public incident found. I searched for dated reports of chatbots failing on thanks, ok, or goodbye and found forum threads and vendor posts, which are not incident reports.

## 5. The fix

**The principle:** Treat acknowledgments and closers as real turns. Reply in proportion, end only when the user has ended, and never restart or re-ask.

**Do this**
1. **Classify the short turn.** Separate at least four: thanks, acknowledgment ("ok", "got it"), agreement to a pending proposal ("ok" after "Shall I proceed?"), and closer ("bye", "that's all").
2. **Thanks:** reply once, briefly ("You're welcome."), then end or offer a way back. Do not start a new topic.
3. **Acknowledgment with nothing pending:** no reply is needed in a live chat. If you reply, keep it to a few words and do not ask a new question.
4. **"Ok" with a pending proposal:** treat it as agreement only if the proposal was explicit, and confirm what you are doing ("Done: I've scheduled it for 3 pm.").
5. **Closer:** say a short goodbye with a way back, then close the session. Never restart the greeting.
6. **Ask "anything else?" at most once per conversation.** An explicit "no" or "that's all" ends it.
7. **Never end on "thanks" or "ok" alone when the task is unfinished.** Those words are not goodbyes (the voice-agent vendor above saw this failure in calls).
8. **Keep the way back visible**: chat history, a transcript option, or a reopen link.

**Reference design: closer handling**
| User turn | Pending question or action? | Reply |
|---|---|---|
| "thanks" | No | "You're welcome." plus a way back; end |
| "ok" / "got it" | No | No reply, or "Great."; do not ask a new question |
| "ok" | Yes (explicit proposal) | Do it and confirm |
| "no, that's all" (after "anything else?") | n/a | Short goodbye plus way back; close |
| "bye" | Any | Goodbye; if a task is pending, say what is saved |

```
Short user messages are real turns. Classify them: thanks, acknowledgment, agreement to a pending proposal, or closer.
Reply to thanks once, briefly, and stop. Do not restart the greeting or open a new topic.
Treat "ok" as agreement only if you just made an explicit proposal; then confirm what you did.
Ask "anything else?" at most once. If the user says no or that's all, say goodbye with a way back and end the conversation.
Do not end the conversation on "thanks" or "ok" if the task is unfinished.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The short turn is clear: reply to "thanks" once, confirm the action after an "ok" to an explicit proposal, or say goodbye with a way back after a closer (and what is saved if a task is pending) |
| Hand off to a person | "ok" or "bye" comes right after the user asked for a person and none has arrived: keep the handoff alive and do not close |

Offering choices is not used here: the user is closing the conversation, and a menu after "bye" is the restart this page warns against.

**Don't over-correct.** Do not answer every "ok" with a paragraph, and do not add "Is there anything else?" to every reply. Do not close a session on a word that was only a pause.

**Hand-off rule.** If "ok" or "bye" comes right after the user asked for a person and none has arrived, do not close: keep the handoff alive (see [talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/no-reply-to-acknowledgments-and-closers.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "thanks" after a finished task | One short reply, no new topic |
| 2 | "no, that's all" after "anything else?" | Goodbye and close, no second question |
| 3 | "ok" after an explicit proposal | The action is done and confirmed |
| 4 | "ok" with nothing pending | No restart, no new question |
| 5 | "thanks" mid-task | The task continues, no goodbye |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Handling correctness on labelled acknowledgment and closer turns** (primary) | Over 95% | Label a sample of short turns against the table above | Below 90% |
| Restart after a closer (greeting or menu shown after "bye" or "thanks") | 0 | Log check | Any |
| "Anything else?" asked twice in one conversation | 0 | Log check | Any |
| Sessions closed on an unfinished task (counter-metric) | Under 1% | Closed sessions with a pending step | Over 3% |
| Conversations reopened within 5 minutes of a close (counter-metric) | Track; set from baseline | Same user, new session | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Chat only.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A greeting or menu is sent right after a user turn labeled thanks or closer (restart after a closer) | Bot turn template or intent field ("greeting", "menu") on the turn after a turn labeled closer | The user sent a new request in that turn |
| "Anything else?" is sent a second time in one conversation | Count of bot turns using the "anything else" template per conversation id | A different question that only resembles the template |
| The session ends while a step is still pending | Session end event with an open pending-state flag | The user said "bye" and the bot stated what is saved |
| A user turn labeled closer gets no bot reply and the session stays open | Closer-labeled user turn with no following bot turn and no session end event | A bare "ok" with nothing pending, where no reply is fine |
| The same user starts a new session within 5 minutes of a close | Session start event, same user id, within 5 minutes of the last session end event | An unrelated new request |

**Starter rule:** ask "anything else?" at most once per conversation, and let an explicit "no" or "that's all" end it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-reply-to-acknowledgments-and-closers
runs: pre_send
reads: [user_turn.short_turn_label, session.pending_state, session.anything_else_count, session.handoff_requested]
trigger: a short user turn labeled thanks, acknowledgment, agreement or closer is about to get a reply
moves: [lead_with_answer, hand_off]   # short names for the moves in the table
choices: none
on_miss: rewrite
metric: handling correctness on labelled acknowledgment and closer turns
counter_metric: sessions closed on an unfinished task
status: proposed
```

## 8. Related patterns
- [Graceless call ending](../../../../speech-and-audio/goals/conversation-flow/failures/graceless-call-ending.md): the voice version of this failure. This page covers chat.
- [Premature call ending](../../../../speech-and-audio/goals/conversation-flow/failures/premature-call-ending.md): ending before the task is done.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): when the fallback fires on a closer.
- [The answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): the bot ends its own turn with no next step.

## 9. Common questions
### How should a chatbot respond to "thanks"?
Reply once, briefly ("You're welcome"), offer a way back, and stop. Do not ask a new question.

### Should a chatbot answer "ok"?
Only if something is pending. After an explicit proposal, confirm the action. Otherwise a short acknowledgment or no reply is fine.

### How many times should a chatbot ask "is there anything else?"
Once. The design guidance I opened treats it as a last topic check, and an explicit "no" ends it.

### Does it matter how a bot ends a conversation?
In one robot experiment with 27 people, a closing sequence raised likeability. It is a small, non-chat study, so test it on your own users.

---
## Technical section

### T1. Solution architecture
```
user turn -> short-turn classifier (thanks | ack | agree | closer | other)
          -> pending-state check (open proposal? unfinished task? handoff waiting?)
          -> reply policy -> close or continue
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No greeting or menu after a closer | Reply policy | Log check |
| "Anything else?" once per conversation | Conversation state | Log check |
| No session close with a pending step | Close handler | Test 5 |

### T3. Evals
- **Dataset:** 200 labelled short turns from logs (thanks, ack, agree, closer) with the pending state at the time.
- **Judge rubric:** is the reply proportionate, free of restarts and repeated questions, and consistent with the pending state?
- **Metrics and starting thresholds:** handling correctness over 95%; restarts 0. Starting points to tune.
- **Release gate:** block a deploy if any labelled closer in the eval set gets a greeting or menu.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Restart after closer | Any | Over 1% of closers | Check classifier and recent flow changes |

### T5. Trade-offs
- Replying to every "ok" adds noise; skipping every reply can feel cold. Start with no reply to a bare "ok" and a short reply to "thanks".

---
### Deep dive
- **Voice.** A spoken goodbye has to be said before the call ends, and "thank you" mid-call is not a goodbye (see the linked voice patterns).
- **Open question.** I found no controlled study of chat closers. The one experiment I opened used a robot.
- **References.** [Uchida et al., *Scientific Reports*, 2024](https://www.nature.com/articles/s41598-024-81353-7) (opened); [OpenDialog closing pattern](https://patterns.opendialog.ai/the-pattern-library/closing/example-dialog) (opened); [Edesy, 2026](https://edesy.in/blog/why-ai-voice-agent-hangs-up-too-early-fix-2026) (opened, vendor).
