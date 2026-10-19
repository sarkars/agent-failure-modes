# Chatbot Sends Many Messages in a Row: Message Bursts

<!-- SEO
title: Chatbot Sends Multiple Messages in a Row: Fix Message Bursts
description: Why a chatbot splits one reply into many rapid messages that flood the chat, what product docs say about splitting, and rules for splitting only when it helps reading.
search phrases:
- chatbot multiple messages in a row
- chatbot message splitting
- chatbot sends too many messages at once
- how to split chatbot replies into bubbles
- chatbot typing indicator delay between messages
- chatbot floods the chat
- one reply split into several messages
-->

**Frequency**: Occasional

## Issue: One reply is split into many rapid messages, one per sentence or line, so the chat floods, the thread is hard to scan, and a phone buzzes once for each piece.

> **One line:** The user asked one question and got eight messages, and has to read them in order to find the answer.

| | |
|---|---|
| **Channel** | Written for **chat** (web widget, in-app, messaging apps). Voice and email are different cases. |
| **Stakes** | Low to medium. It rises when the answer, a deadline, or a fee lands in the middle of a burst, or when the user is on a phone with alerts on. |
| **Who is affected** | Anyone who chats with a bot that splits replies, most of all people reading on a phone and people whose device alerts on every message |
| **Frequency** | Occasional. Several chatbot products offer reply splitting as a setting (see section 4), so it appears where teams turn it on. I found no count of how often it happens. |
| **Pattern ID** | message-bursts |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| **Primary metric** | Messages per turn: assistant messages sent for one user message. Starting target: 1 for most replies, with a team-set cap for the rest (tune). |
| **Maturity** | Researched (not yet tested) |
| **Will a better model fix this?** | No. The split happens in the product or channel layer, after the model has written the reply, and it is controlled by settings the business chooses. (Our judgment, not tested.) |
| **Cause owner** | Business context (the product's splitting, delay, and notification settings) |
| **Also searched as** | bot sends text after text · chatbot double texting · chatbot spams me with messages · reply split into bubbles · too many chat bubbles |

## 1. In plain words
Some chat products take a finished reply, cut it into sentences, and send each one as its own message, with a typing indicator and a pause between them. Done well, that can make a long reply easier to read. Done by default, on every reply, it makes a short answer arrive slowly in pieces, buries the answer in the thread, and can trigger one notification per piece.

## 2. What it looks like

**Without the fix**
```
User: Can I move my dentist appointment from Tuesday to Thursday?
Bot:  Sure, I can help with that!                                (message 1)
Bot:  I see your appointment on Tuesday at 2:00 PM.              (message 2)
Bot:  Thursday has openings.                                     (message 3)
Bot:  The times are 9:00 AM, 11:30 AM, and 4:00 PM.              (message 4)
Bot:  Which one works for you?                                   (message 5)
Phone: five alerts in about ten seconds
```

**With the fix**
```
User: Can I move my dentist appointment from Tuesday to Thursday?
Bot:  Yes. Thursday has openings at 9:00 AM, 11:30 AM, and 4:00 PM. Which one works for you?
      [9:00 AM] [11:30 AM] [4:00 PM] [Something else]
```
The fixed reply is one message, with the answer first and the choice at the end. The user reads once and answers once.

## 3. Why it happens
These are our reading of the pattern.
- **Splitting is a product switch.** Platforms offer it as a setting, so one toggle applies to every reply, short or long.
- **It is meant to feel human.** Teams add bubbles and typing pauses so the bot "sounds like a person", and do not test whether the pauses help or only delay.
- **Splitting runs after the model.** The reply is cut by sentence or line, so the cut ignores which part is the answer.
- **No cap on messages per turn.** Nothing counts the bubbles a single turn produces, so a long draft becomes a long burst.
- **Alerts are per message.** The channel decides how alerts work, and the bot team often does not look at what a burst does on a locked phone. I found no source that measures this (see section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| ChatLab's documented behavior: the bot writes the full answer, splits it into sentences, and shows each sentence as its own bubble after a typing indicator. The default delay between bubbles is 5 seconds; it suggests 2-3 seconds for support bots and says to disable splitting for support bots, high-volume bots, and bots that usually give single-sentence answers. | [ChatLab, *Chat Features: human-like messaging*](https://www.chatlab.com/help/human-like-messaging/). Opened and read. | A vendor's documentation, not a study. It shows that sentence-level splitting with long default pauses exists and that the vendor itself says to switch it off for fast-answer bots. |
| SleekFlow's "Semantic Message Splitting" breaks longer replies into shorter bubbles with typing pauses, always sends replies under 150 characters as one bubble, keeps lists together in one bubble, and finishes its current bubble sequence before answering a new customer message. | [SleekFlow changelog, *chat bubble replies*](https://feedback.sleekflow.io/changelog/make-your-ai-agent-feel-more-human-with-chat-bubble-replies). Opened and read; the page shows no date. | A vendor changelog. The 150-character figure is that product's setting, not research. It shows one product's design choices (short replies stay whole, lists stay whole), which are the same rules this page proposes. |
| Toyota Europe's chat design guidance says to "break long explanations into separate bubbles" and to "Front-load the most important information or the answer at the beginning of the message." | [Toyota Europe DX Playbook, *Chat messages*](https://dx-playbook-prev.toyota-europe.com/cds/components/chat-messages/). Opened and read; the page shows "last updated Oct 16, 2026". | A design system's guidance for one company's chat component. It supports splitting long content, so splitting is not the failure; unneeded splitting is. |
| Khoros's flow guide describes a different burst: a user who sends several messages in a row can make a bot move on too early. Its options are to ask for one message, to wait for the user to type "Done", or to wait a set time (5 seconds in its example) after the last message. | [Khoros, *Flow Designs: Handle multiple user or customer messages*](https://developer.khoros.com/khoros-flow/docs/flow-designs-handle-multiple-user-or-customer-messages). Opened and read. | About bursts from the user, not from the bot. It is cited only to mark that boundary. It says nothing about bots sending many messages. |

I found no study that measures reading time, comprehension, or notification annoyance for bot-side message splitting, and no sourced count of notification complaints about it. Two other pages from my searches (a UX Collective article on bot design and a CloseBot help article) came back as errors when I tried to open them, so I use nothing from them.

**Public incident.** No public incident found. Searches for chatbot message floods turned up vendor docs and forum threads about duplicate notifications and stuck interfaces, which are different problems.

## 5. The fix

**The principle:** Send one message by default. Split only when the split helps reading, and keep the answer in the first message.

**Do this**
1. **Default to one message per turn.** A reply of a few sentences goes out as one message.
2. **Set a floor.** Short replies are never split. SleekFlow's 150-character floor is one product's example; set your own and test it.
3. **Split by idea, not by sentence.** A split is allowed between two separate ideas, never inside a list, a set of steps, a code block, or a sentence pair that only makes sense together.
4. **Put the answer in the first message.** Anything that follows is support, and the user can skip it.
5. **Cap messages per turn.** Choose a maximum (for example 2 or 3) and merge anything past it into the last message. Treat the number as a starting point.
6. **Keep pauses short or drop them.** A long delay between bubbles adds waiting without adding reading help. ChatLab's own guidance puts 2-3 seconds as the fast end and says to turn splitting off when speed matters.
7. **Never split the one question.** The question to the user ends the last message; do not send it alone as a trailing bubble that arrives after a delay.
8. **Check the alert side.** Test what a burst does on a phone with alerts on. If each bubble alerts, send fewer, or group them into one message.

**Reference design: when to split**
| Case | Send |
|---|---|
| Short answer (a few sentences) | One message |
| Answer plus one separate topic the user may skip | Two messages: answer first, extra second |
| Steps, list, or table | One message, kept together |
| Long reply with several ideas | A short first message with the answer, then an offer: "Show the rest?" |

```
Send one message per reply. Do not split short replies, lists, or steps.
If a reply has two separate ideas, you may send at most two messages, and the first holds the answer.
Never send more than three messages for one user message. End the last message with the one question, if there is one.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reply: the first (or only) message holds the answer or the next step, so a burst never hides it. |
| Offer choices: 2-4 options plus "Something else", free text open | The reply is long and has an optional second part: send the answer, then offer "Show the rest", "Next step", "Something else". Do not offer them when the whole reply fits in one short message, or when the options would be sent as a separate trailing bubble. |

**Don't over-correct.** Do not merge a long reply into one block of text; that is the wall of text problem (a planned pattern in the [family README](../README.md)), and a split between two real ideas can help. Do not drop typing indicators if the bot is slow; the user needs to know it is working.

**Hand-off rule.** Not applicable. This is a formatting and channel-settings fix, so no person is needed.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file is written for this pattern yet. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A yes/no question with a two-sentence answer | One message, answer first |
| 2 | A reply with a five-step procedure | One message, steps kept together |
| 3 | A reply with two separate ideas | At most two messages; the answer is in the first |
| 4 | A long draft that would make six messages | No more than the cap; the rest is merged or offered |
| 5 | A phone with alerts on | One alert for a short reply |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Messages per turn** (primary) | 1 for most replies; a cap for the rest | Count assistant messages between two user messages in the event log | Over the cap on any turn |
| Replies split that were under the length floor | 0 | Split events where the draft was shorter than the floor | Any |
| Time from user message to last bubble | Track; set from baseline | Timestamps of the user message and the last assistant message in the turn | Rising two weeks in a row |
| Notification complaints | Track; set from baseline | Support tickets and feedback tagged "too many notifications" or "spam" | Rising two weeks in a row |
| Answer in first message (counter-metric) | Over 90% (tune) | Sampled review: is the answer in the first message of the turn? | Below 80% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat. Voice and web-push signals are PLANNED, not detected.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Three or more assistant messages follow one user message | Message count per turn in the event log | A deliberate multi-part reply that the user asked for, such as "send me each step one at a time" |
| Several assistant messages sent within a few seconds of each other | Timestamps of consecutive assistant messages | Streaming of one reply that the client shows as one message |
| A message under the length floor sent right after another assistant message | Message lengths and order within a turn | A short last message that holds the question |
| User sends "wait", "slow down", or "stop sending so many" during or after a burst | Next-turn text match | A user asking the bot to pause for another reason |
| User asks again for something that was in the middle of a burst | Same intent repeated in the next user turn | A user who wants a different detail |

**Starter rule:** one user message gets one assistant message, except when a reply has two separate ideas, and then the first message holds the answer and no more than three messages are sent.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: message-bursts
runs: pre_send
reads: [draft_reply.length, draft_reply.parts, draft_reply.has_list_or_steps, turn.message_count]
trigger: a reply is about to be split into more than one message
moves: [lead_with_answer, offer_choices]
choices: ["Show the rest", "Next step", "Something else"]
on_miss: rewrite
metric: messages per turn
counter_metric: answer in first message
status: proposed
```

## 8. Related patterns
- [Answer buried](answer-buried.md): the answer sits late in one long reply. In a message burst the answer can sit late in the thread. Answer buried is about order inside a reply; this page is about how many messages the reply is cut into.
- [No reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md): the short-message end of the same family. This page covers the opposite case, too many replies.
- [Verbosity despite brevity instructions](../../../../speech-and-audio/goals/conversation-flow/failures/verbosity-despite-brevity-instructions.md): length, not message count, and in voice.
- [Interruption mishandling](../../../../speech-and-audio/goals/conversation-flow/failures/interruption-mishandling.md): what happens when the user talks over the bot, a related timing problem in voice.

## 9. Common questions
### Why does my chatbot send multiple messages in a row?
Often a setting splits the finished reply into sentences and sends each as its own bubble. ChatLab and SleekFlow, two products I read, both offer it. Check the splitting and delay settings first.

### Is it ever right to split a chatbot reply into several messages?
Yes, between separate ideas, when each part is short. Toyota's chat guidance says to break long explanations into separate bubbles. Keep the answer in the first message and keep lists and steps together.

### How many messages should a bot send at once?
I found no published limit. A cap of two or three per user message is a reasonable starting point to test, not a researched figure.

### Do typing indicators between messages help?
They show the bot is working, but long pauses add waiting. ChatLab's docs say 2-3 seconds suits support bots and to turn splitting off when speed matters. I found no study of the effect.

### Is this the same as a user sending many messages in a row?
No. That is a user-side burst, covered in the Khoros guide I read. This page is about the bot sending many messages for one user message.

---
## Technical section

### T1. Solution architecture
```
model draft -> splitter policy (length floor | list/steps check | idea boundary | cap)
            -> render as 1..N messages (N <= cap) -> send -> log (messages per turn, timestamps)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Drafts under the floor are sent whole | Splitter | Log scan, test 1 |
| Lists, steps, and code blocks are never split | Splitter | Test 2 |
| Messages per turn never exceed the cap | Send layer | Log scan, test 4 |
| The answer is in the first message | Judge check on a sample | Test 3 |

### T3. Evals
- **Dataset:** 100 real drafts from logs (short answers, lists, procedures, long multi-idea replies) with a label for the expected message count.
- **Judge rubric:** is the answer in the first message, is the count within the cap, and are lists and steps intact?
- **Metrics and starting thresholds:** messages per turn within cap 100%; answer in first message over 90%. Starting points to tune.
- **Release gate:** block a splitter or prompt change if any eval draft exceeds the cap.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Turns over the cap | Any | Over 1% of turns | Check the splitter setting and recent prompt changes |

### T5. Trade-offs
- Fewer, larger messages can look less lively than a typing-bubble flow. Test with users before removing the pauses completely.
- A cap can merge two ideas that read better apart. Allow two messages when the second can be skipped.

---
### Deep dive
- **Open question.** I found no study of reading, comprehension, or notification annoyance for bot-side splitting. The evidence is vendor documentation and one design system, so the target numbers here are starting points.
- **References.** [ChatLab](https://www.chatlab.com/help/human-like-messaging/) (opened); [SleekFlow](https://feedback.sleekflow.io/changelog/make-your-ai-agent-feel-more-human-with-chat-bubble-replies) (opened); [Toyota Europe DX Playbook](https://dx-playbook-prev.toyota-europe.com/cds/components/chat-messages/) (opened); [Khoros](https://developer.khoros.com/khoros-flow/docs/flow-designs-handle-multiple-user-or-customer-messages) (opened).
