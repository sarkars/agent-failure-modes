# Voice Assistant Can't Repeat That or Go Back: No Repeat or Recap Controls

<!-- SEO
title: Voice Assistant Can't Repeat or Go Back: Add Repeat Controls
description: Why a voice bot or chatbot that can't repeat, slow down, or go back strands the user after "what?", and a design with a stored last answer and a recap.
search phrases:
- voice assistant won't repeat what it said
- chatbot ignores "say that again"
- how to add a repeat command to a voice bot
- ivr go back and repeat commands
- alexa can't repeat the last answer
- chatbot response too long, how to summarize again
- voice bot talks too fast, can't slow down
-->

**Frequency**: Common

## Issue: The user missed or didn't follow what the agent said and can't get it again: "what?", "say that again", or "go back" gets a new answer, a vague apology, or nothing.

> **One line:** Spoken words are gone as soon as they are said, and an agent with no repeat, slow-down, or go-back control leaves the user to guess what they missed.

| | |
|---|---|
| **Channel** | Written for **chat** (the user types "what?", "say that again", "go back", "summarize that"). Voice (spoken "repeat", "slower", "go back" on a phone or speaker) is **planned**: the design below applies, but the signals that need audio are not written yet. |
| **Stakes** | Low to high. Missing a pharmacy hour is minor; missing a confirmation number, a dose, or a deadline is not. |
| **Who is affected** | Everyone in noisy or distracted settings; people who process speech more slowly, including some older adults; people listening in a second language |
| **Frequency** | Common. Voice-design guides treat repeat and go back as standard controls, but no rate was found for how often production agents lack them. |
| **Pattern ID** | no-repeat-or-recap-controls |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | Recovery-success rate after "what?": share of repeat or "go back" requests where the user's next turn moves on without asking again. Starting target: set from a baseline (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model understands "say that again" better, but whether the last answer is stored, replayable, and restatable at any point is a product decision. (Our judgment, not tested.) |
| **Also searched as** | bot won't repeat itself · say that again · go back a step · talks too fast · summarize what you just said · can you repeat that |

## 1. In plain words
Heard once, spoken information is easy to lose: a phone number, a time, a step in a list. A person asks "sorry, what was that?" and gets it again. An agent with no repeat control either answers "what?" as a brand-new question or says "I'm not sure what you mean." The fix is to treat repeat, slower, shorter, and go back as controls that work at any point.

## 2. What it looks like

**Without the fix**
```
Bot:   Your prescription is ready at the Oak Street pharmacy. Pickup closes at 7 PM, you'll need photo ID, and the order number is 4 8 1 7 2 0.
User:  What was the order number?
Bot:   I can help with prescriptions, refills, and store hours. What would you like to do?
User:  The order number, say it again.
Bot:   Sorry, I didn't understand. Could you rephrase?
```

**With the fix**
```
Bot:   Your prescription is ready at the Oak Street pharmacy. Pickup closes at 7 PM, you'll need photo ID, and the order number is 4 8 1 7 2 0.
User:  What was the order number?
Bot:   The order number is 4 8 1 7 2 0. Pickup closes at 7 PM. Want me to go through all of it again, slower?
User:  Yes, slower.
Bot:   Pharmacy: Oak Street. Closes: 7 PM. Bring: photo ID. Order number: 4 8 1 7 2 0.
```
The fixed bot answers the question about the earlier turn from what it already said, offers a full replay, and changes pace and shape on request.

## 3. Why it happens
- **The last answer is not kept as something to replay.** The agent treats "say that again" as a new request and re-generates, or fails to match any intent.
- **Repeat has no defined behavior.** Nobody decided whether it means the last sentence, the last turn, or the last item in a list, so it is not built or tested.
- **No short form exists.** The only version of the answer is the long one, so a slower or recap request has nothing to switch to.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The authors list "[repeat]" (repeat the most recently played prompt) and "[go back]" (back up to the preceding step) among recommended universal commands, and advise one set for all applications, drawn from two standards bodies (the Telephone Speech Standards Committee and ETSI) and their own deployment experience. They state that successful use of universals "should improve" completion, automation, and satisfaction. | [Balogh, Cohen and Giangola, InformIT chapter on universals](https://www.informit.com/articles/article.aspx?p=170792). Opened and read. | A design recommendation for phone IVR, not a measured result. The article gives no separate evidence for repeat or go back alone. |
| Google's Assistant implementation tips advise a repeat intent that matches phrases like "say that again" and replays a stored last prompt, with a short lead-in such as "Let me repeat that." | [Google Assistant best practices (Dialogflow)](https://developers.google.com/actions/assistant/best-practices). Opened and read. | A developer tip for a platform, not a study. The page is part of older Assistant developer docs, so check it is current before relying on it. |
| In a study where 48 people booked appointments with nine spoken dialogue systems, recall of appointment details was lower for users with slower information processing; working memory span did not affect recall. Systems with more options per turn and no explicit confirmations were faster without lowering task success. | [Wolters et al., *Interacting with Computers*, 2009](https://research.tees.ac.uk/en/publications/reducing-working-memory-load-in-spoken-dialogue-systems/). Opened; abstract read. | One 2009 task with simulated systems. It shows recall varies across listeners; it does not measure repeat requests. |
| A voice-interface columnist argues that repetition is under-valued and that endless varied re-prompts can leave callers feeling stuck in a loop. | [Rolandi, "Repeat or Not Repeat," *Speech Technology*, March 2003](https://www.speechtechmag.com/Articles/Editorial/Features/Repeat-or-Not-Repeat-29689.aspx). Opened and read. | An opinion column. It cites no data. |

No study was found that measures how often users ask a voice assistant to repeat, or how often agents fail them. Treat the frequency as unmeasured.

## 5. The fix

**The principle:** Keep the last answer and its structure, so "repeat", "slower", "shorter", "go back", and "recap" can each be answered from what the agent already said, at any point in the conversation.

**Do this**
1. **Store the last agent turn and its items.** Keep the turn text and any list, number, or time as separate fields so they can be replayed.
2. **Treat "what?", "say that again", "repeat", "huh" as a repeat of the last agent turn.** Do not treat them as a new topic or an unrecognized request.
3. **Answer a question about an earlier turn from that turn.** "What was the order number?" returns the stored number, not a fresh generation.
4. **Make "slower", "shorter", and "recap" change the form, not only the content.** Slower means smaller chunks with the key detail alone; shorter means the key detail first; recap means the decisions and next step so far.
5. **Make "go back" return to the previous step and say where the user is.** "Back to the pickup time" and then re-ask that step ([no way back in a flow](../../dialogue-management/failures/no-way-back-in-a-flow.md)).
6. **Never answer a repeat request with "I didn't understand" twice.** After one miss, offer the last answer in full.
7. **Name the controls once and early.** The first time a long answer is given: "You can say repeat, slower, or go back at any time."
8. **Keep the controls working in every state**, including mid-list, mid-form, and after an error.

**Reference design: replay store**
```
last_turn:   { text, items: [{label, value}], step_id }
on "repeat" / "what?":      say last_turn.text (same words, no new facts)
on "slower":                say last_turn.items one at a time, key value first
on "shorter" / "recap":     say the decision so far and the next step, under two sentences
on "go back":               restore the previous step_id and re-ask it
on a second miss:           offer: "Repeat it", "Say it slower", "Send it as text", "Something else"
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks "what was...?": give the stored value first, then the offer to replay. Do not lead with a menu. |
| Ask one clarifying question | The user says "go back" and there are two earlier steps it could mean: "To the pickup time, or to your address?" Do not ask when only one step is possible. |
| Offer choices: 2-4 options plus "Something else", free text open | After a second miss, or when a long answer is likely to be lost: "Repeat it", "Say it slower", "Send it as text", "Something else". Do not offer them after a clean first repeat, or when the answer was one short fact. |
| Hand off to a person | The user has asked for a repeat three times and still can't use the answer. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not recap after every turn, which is the filler this page does not want ([filler and padding](../../response-structure/failures/filler-and-padding.md)). Do not read the whole conversation back when the user asked for one number. Do not add new facts to a repeat; a replay says the same thing. Do not open every answer with "say repeat to hear it again".

**Hand-off rule.** If the user can't take in the answer after a slower replay and a text option, pass the details so far to a person ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | User types "what?" after a three-item answer | The same three items are repeated, no new request handled |
| 2 | "What was the order number?" | The stored number is returned, unchanged |
| 3 | "Slower" after a long answer | Items come in smaller chunks, key value first |
| 4 | "Go back" in a four-step flow | The previous step is restored and named |
| 5 | Two repeat requests in a row | The second offers a new form (slower, text), not the same words or an apology |
| 6 | "Recap" after five turns | Decisions and next step in under two sentences, no new facts |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Recovery-success rate after "what?"** (primary) | Set from baseline; higher is better | Repeat or go-back requests where the next user turn moves forward without asking again, from logs | Falling |
| Repeat requests answered with "didn't understand" | Under 2% | Log: repeat cue followed by a fallback reply | Over 5% |
| Repeat replies that change facts | 0% | Compare replay text with the stored turn on a sampled set | Any |
| Second repeat request within 2 turns | Track; lower is better | Count of consecutive repeat cues | Rising |
| Recap length, in sentences (counter-metric) | Under 3 | Log | Over 4 |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. The text signals are written for chat. Audio signals are PLANNED for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Written for text: a user turn matches a repeat cue ("what?", "say that again", "repeat that", "huh") and the next agent turn is a fallback or a new topic | User turn text, then agent reply type | The cue was a joke, or an unrelated "what?" such as "what time is it" |
| Written for text: the user asks the same question again within two turns of the agent's answer | Two similar user turns with an agent answer between | A deliberate second request, such as a different product |
| Written for text: a "go back" or "previous" cue is followed by an agent reply that does not restore an earlier step | Cue turn, then step id before and after | The user was already on the first step |
| Written for text: a user asks for a summary ("summarize", "tl;dr", "recap") right after a long agent turn | User cue after an agent turn over a set length | The user wanted a summary of a document, not of the bot's reply |
| PLANNED for voice: a caller says "what?" or goes silent, then repeats the question louder or slower | Needs audio and speech rate; not computable from the transcript | A caller who always speaks that way, or a noisy line |

**Starter rule:** treat "what?", "say that again", and "go back" as controls on the last agent turn, answer them from what was already said, and name them once.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-repeat-or-recap-controls
runs: conversation
reads: [turn.text, last_agent_turn.text, last_agent_turn.items, flow.step_id, repeat.count]
trigger: the user sends a repeat, slower, shorter, recap, or go-back cue
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Repeat it", "Say it slower", "Send it as text", "Something else"]
on_miss: rewrite
metric: recovery-success rate after "what?"
counter_metric: recap length
status: proposed
```

## 8. Related patterns
- [Repair failure](repair-failure.md): the closest page. It covers a spoken correction ("no, the other one") that is not applied; this page covers a missed or unclear agent turn that the user wants again, slower, or recapped, with no correction involved.
- [No way back in a flow](../../dialogue-management/failures/no-way-back-in-a-flow.md): the chat version of "go back".
- [Spoken form failures](../../../../speech-and-audio/goals/conversation-flow/failures/spoken-form-failures.md): numbers and dates read in a form that is hard to follow.
- [Monologue without engagement](../../../../speech-and-audio/goals/conversation-flow/failures/monologue-without-engagement.md): long turns that make a repeat more likely.
- [Voice-only flows with no text alternative](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md): when the fallback is a text copy.

## 9. Common questions
### Why won't my chatbot repeat what it just said?
Most often it treats "say that again" as a new request. Store the last agent turn and answer repeat cues from it.

### What commands should a voice bot always understand?
Voice-design guidance that was opened lists repeat and go back among a small set of universal commands. Help, start over, and transfer to an agent appear in the same guidance. Keep them the same in every state.

### Should "repeat" say the same words or rephrase?
The same facts. A plain replay can use the same words; after a second request, change the form (slower, shorter, or text) and do not add new facts.

### How is this different from the bot ignoring a correction?
A correction changes a value the bot got wrong ([repair failure](repair-failure.md)). A repeat or recap request changes nothing; the user wants to hear it again.

---
## Technical section

### T1. Solution architecture
```
user turn -> control-cue classifier (repeat | slower | shorter | recap | go back)
          -> replay store (last turn, items, step id) -> formatter (same | chunked | summary)
          -> reply; repeat counter -> options (text copy) -> hand-off
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| A replay contains no facts absent from the stored turn | Output check | Test 2, test 6 |
| Controls work in every flow state | Dialogue manager | Tests 1 and 4 |
| A second repeat changes the form | Dialogue manager | Test 5 |

### T3. Evals
- **Dataset:** 100 labeled conversations with control cues placed after short answers, long lists, errors, and mid-flow steps (starting point to tune).
- **Judge rubric:** did the reply answer from the stored turn, add no new facts, and change form on a second request?
- **Metrics and starting thresholds:** replay with new facts 0%; recovery success set from baseline. Starting points to tune.
- **Release gate:** block a deploy if a control cue falls through to a fallback reply on the test set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Recovery-success rate | Falls 5 points | Falls 10 points | Check the cue classifier and the replay store |

### T5. Trade-offs
- Storing every turn adds state; storing only the last turn and its items covers the common case.
- Recaps risk new errors if regenerated; build them from stored fields.

---
### Deep dive
- **Open question.** No measurement was found of repeat-request rates or recall of spoken agent output in production assistants. The sources are design guidance and a 2009 lab study.
- **Not opened.** A search summary mentioned a 2022 study of auditory word recall in older adults with vision loss and a month-long in-home study of older adults and voice assistants; neither was opened, so neither is used above.
- **References.** [Balogh, Cohen and Giangola](https://www.informit.com/articles/article.aspx?p=170792) (opened); [Google Assistant best practices](https://developers.google.com/actions/assistant/best-practices) (opened); [Wolters et al., 2009](https://research.tees.ac.uk/en/publications/reducing-working-memory-load-in-spoken-dialogue-systems/) (abstract opened); [Rolandi, 2003](https://www.speechtechmag.com/Articles/Editorial/Features/Repeat-or-Not-Repeat-29689.aspx) (opened).
