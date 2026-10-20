# Chatbot Buttons Won't Accept Typed Answers: Quick-Reply Buttons That Don't Match What Was Typed

<!-- SEO
title: Chatbot Buttons Won't Accept My Typed Answer: How to Fix It
description: Why a chatbot ignores a typed answer and only accepts a button tap, or keeps showing buttons after you typed, and how to treat typed text as a button.
search phrases:
- chatbot only lets me click buttons
- chatbot ignores what I type and shows the buttons again
- can't type in chatbot, only buttons
- quick reply buttons and free text input
- chatbot doesn't understand typed answer after quick reply
- should a chatbot accept typed text next to buttons
- chatbot buttons stay after I type
-->

**Frequency**: Occasional

## Issue: A person types an answer while quick-reply buttons are showing, and the bot ignores it, re-asks, or keeps the buttons blocking the flow, so only a button tap works.

> **One line:** The bot treats a button tap as the only valid answer; the fix is to accept free text next to the buttons and handle a typed answer the same way as the matching button.

| | |
|---|---|
| **Channel** | Written for **chat** (web, app, and messaging-app bots with buttons). Voice and web-analytics signals are PLANNED, not written. |
| **Stakes** | Low to medium. A stuck booking costs a retry; a stuck refund or payment step can send the person to a phone line. |
| **Who is affected** | Anyone who types before looking at the buttons, uses a keyboard, or whose answer isn't one of the options |
| **Frequency** | Occasional. I found no study that counts how often bots refuse typed answers (see section 4). |
| **Pattern ID** | quick-reply-buttons-that-don-t-match-what-was |
| **Family** | [Chat interface](../README.md) |
| **Goal** | The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost. |
| **Primary metric** | Typed replies handled when buttons are shown. Target: 100% (a design target and a starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The flow and the client decide whether typed text is read as an answer; a stronger model behind a button-only state machine still never sees the text. (Our judgment, not tested.) |
| **Also searched as** | chatbot only accepts button clicks · chatbot won't let me type · bot ignores my typed reply · quick reply buttons not working when typing · chatbot loops back to the menu · text input disabled chatbot |

## 1. In plain words
A bot shows buttons such as "Today" and "Tomorrow", and the person types "Friday morning" instead. Some bots then show the same buttons again, or say "Please choose an option", or leave the typing box locked. The buttons were meant as a shortcut for typing, not a replacement for it.

## 2. What it looks like

**Without the fix**
```
Bot:  When should we pick up your rental? [Today] [Tomorrow] [This weekend]
User: Friday at 9am
Bot:  Please choose one of the options below. [Today] [Tomorrow] [This weekend]
User: Friday
Bot:  Please choose one of the options below. [Today] [Tomorrow] [This weekend]
User: (closes the chat and calls the Denver branch)
```

**With the fix**
```
Bot:  When should we pick up your rental? [Today] [Tomorrow] [This weekend] [Something else]
      You can also type a day and time.
User: Friday at 9am
Bot:  Friday, Oct 23 at 9:00 AM at the Denver branch. Is that right? [Yes] [Change it]
User: Yes
Bot:  Booked. Your confirmation number is on its way by text.
```
The fixed bot reads the typed day and time as an answer, confirms what it understood, and keeps the buttons as a shortcut.

## 3. Why it happens
- **The flow only listens for the button value.** Buttons send a fixed value (a payload) to a step in a scripted flow. The step has no branch for text that matches no payload, so it repeats the prompt.
- **The client locks the composer.** Some widgets disable or hide the text box while buttons are shown, so typing is impossible, not just ignored.
- **Typed text goes to a different place than the tap.** The tap is routed to the flow step; typed text is routed to a general language model or an intent classifier that has no memory of the question just asked, so "Friday" has no meaning.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Microsoft's Bot Connector documentation describes suggested actions as buttons that let the user answer "with a simple tap" instead of typing with a keyboard, and says they disappear after the user makes a selection. A tap reaches the bot as a message containing the button's value. | [Microsoft Learn, *Add suggested actions to messages*](https://learn.microsoft.com/en-us/azure/bot-service/rest-api/bot-framework-rest-connector-add-suggested-actions) (page dated Oct 9, 2024). Opened 2026-10-20. | Vendor documentation. Shows buttons are designed as a tap shortcut; it does not say what a bot should do with typed text. |
| Meta's Messenger Platform lists quick replies with a maximum of 13 per message and a 20-character limit on a text quick reply's title. When a quick reply is tapped, the buttons are dismissed and the tapped title is posted to the conversation as a message. | [Meta for Developers, *Quick replies*](https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies/). Opened 2026-10-20. | Vendor documentation. The page does not say whether typing is allowed while quick replies show, so I do not use it for that. |
| Microsoft's Teams bot documentation says Teams displays only the first three suggested actions even if more are sent, and that in one-on-one chats only the actions from the last message appear. | [Microsoft Learn, *Dynamically guide users with suggested actions*](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/conversations/suggested-actions) (page dated Aug 19, 2026). Opened 2026-10-20. | Vendor documentation for one platform. Shows buttons are limited, so an answer outside them is common. |
| A WhatsApp bot-design guide says people type anyway, and that a flow accepting only a tap breaks when a customer answers in words. | [CodeWords, *WhatsApp bot UX: buttons, lists, free text*](https://codewords.ai/blog/whatsapp-bot-ux-buttons-lists-free-text). Opened 2026-10-20; no publication date on the page. | Vendor blog, no data behind the claim. It is a design opinion that supports the fix; it is not a measurement. |
| A secondhand summary attributes to Nielsen Norman Group the point that removing free text makes users feel constrained. | **Not opened.** I found only a search-result summary of a third-party guide and did not reach the NN/g page. | Unverified. I quote nothing from it and the fix does not rely on it. |

I searched for a study of how often bots reject typed answers while buttons are shown and found none. **Public incident:** None found.

## 5. The fix
**The principle:** A typed answer is as valid as the button it matches, and the composer stays open whenever buttons are shown.

**Do this**
1. **Never lock the composer.** Keep the text box enabled while buttons are showing. A button-only step is allowed only when the platform itself cannot take text; then say so in the message.
2. **Route typed text to the open question.** While a button question is open, run the user's text through the same step as the buttons first: match it to a button label, a synonym, or a value (a date, a number, a name).
3. **Treat a match as a tap.** If typed text matches a button, continue exactly as if the button had been tapped, with the same state change and the same next message.
4. **If it matches nothing, say what was understood and ask once.** Do not repeat the prompt word for word. Name what you could not match and show the buttons again with "Something else".
5. **Let a different question win.** If the text is a new request, not an answer ("What's your cancellation policy?"), answer it, then offer to return to the open question.
6. **Include "Something else" in every button set** so a person whose answer is not listed has a button that opens free text.
7. **Keep buttons a shortcut.** After a typed answer, retire the buttons for that question so a later tap on a stale button cannot override it.

**Reference design: one handler for tap and text**
```
open_question = {id: "pickup_day", buttons: ["Today","Tomorrow","This weekend","Something else"]}

on user_turn(text or button_value):
  answer = button_value or match(text, open_question)     # label, synonym, or parsed value
  if answer:           advance(open_question, answer); retire_buttons(open_question)
  elif is_new_request: reply(answer_it); then offer to return to open_question
  else:                reply("I couldn't match '" + text + "' to a pickup day. Pick one, or tell me a date.")
                       show open_question.buttons          # asks once, names what failed
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Typed text matches a button or a clear value: continue the flow with no "please use the buttons" reply. |
| Offer choices: 2-4 options plus "Something else", free text open | The question has a few likely answers: show the buttons, add "Something else", and keep the text box open. |
| Ask one clarifying question | Typed text matches nothing, or matches two buttons: say what was read and ask once which was meant. |
| Hand off to a person | Two typed answers in a row match nothing for the same question (see hand-off rule). |

**Don't over-correct.** Do not drop the buttons because people can type; buttons save typing on a phone. Do not accept text so loosely that "no" to a different question is read as "No" for the open one: confirm a typed value when the step changes money, dates, or accounts. Do not add the line "or type your answer" to every message when the composer is plainly open.

**Hand-off rule.** If two typed replies in a row match no option for the same question, stop re-showing the buttons. Offer a person or another channel (phone or email), and pass the open question and what the user typed.

**Framework used:** [Conversation moves](../../../solutions-library/conversation-moves.md) (offer choices with "Something else" and free text open).

## 6. How to test it (short version)
No full test file yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Buttons showing; open the page and check the composer | Text box is enabled | 1 |
| 2 | Type the exact label of a button ("Tomorrow") | Same state and next message as tapping it | 2, 3 |
| 3 | Type a value that fits ("Friday at 9am") | Parsed as the answer, then confirmed | 2, 3 |
| 4 | Type text that matches nothing ("banana") | Reply names what was not matched, shows buttons once with "Something else" | 4, 6 |
| 5 | Type a new question while a button question is open | Question is answered, then the open question is offered again | 5 |
| 6 | Type an answer, then tap an old button | The old tap does not change the answer | 7 |
| 7 | Type two unmatched answers in a row | Offer of a person or other channel appears | Hand-off rule |
| 8 | Type "yes" to an unrelated earlier question | Not read as a button answer without confirmation | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Typed replies handled when buttons are shown** (primary) | 100% (design target) | User text turns where `buttons_shown` is true and the next bot turn advances the flow, answers, or asks a specific question (not the same prompt again) | Below 95% |
| Composer enabled while buttons shown | 100% | Client event `composer.enabled` at each button render | Any miss |
| Identical prompt re-sent after a typed reply | 0 | Same bot text and `question_id` in the turn after a user text turn | Any |
| Button set without "Something else" | 0 | Button renders with no free-text option | Any |
| Typed answers confirmed wrongly (counter-metric) | Track; set from baseline | Sampled review of typed answers that advanced the flow and were later corrected | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot repeats the same prompt and buttons right after a user text turn | `bot_turn.question_id` equal to the previous turn, with `ui.buttons_shown` | The typed text was a real mismatch and the bot named what it could not read |
| User sends a second text turn before any button tap | Two user text turns with the same `question_id` open | User added detail to one answer |
| Composer disabled while buttons are shown | `composer.enabled` false at a button render | Deliberate lock during a short payment or verification step |
| User text turn is classified as fallback while a button question is open | `intent` is fallback and `question_id` is open | The user changed the subject |
| Session ends within 2 turns after a typed reply that got a repeat prompt | `session.end` after a repeated `question_id` | User got what they needed elsewhere |

**Starter rule:** a typed answer is as valid as the button it matches, and the composer stays open whenever buttons are shown.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: quick-reply-buttons-that-don-t-match-what-was
runs: post_turn
reads: [user_turn.text, user_turn.button_value, ui.buttons_shown, ui.composer_enabled, session.open_question_id, bot_turn.question_id]
trigger: a user text turn arrives while a button question is open
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Today", "Tomorrow", "This weekend", "Something else"]
on_miss: log
metric: typed replies handled when buttons are shown
counter_metric: typed answers confirmed wrongly
status: proposed
```

## 8. Related patterns
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): the closest page. It covers a bot that cannot understand a message and offers no way forward. This page is narrower: a button question is open, the typed text is a valid answer, and the failure is that it is not read as one.
- [Starter suggestions that fail](../../onboarding-and-discoverability/failures/starter-suggestions-that-fail.md): suggestion chips that lead to weak answers when tapped. Here the tap works and the typed route does not.
- [No likely next-action suggestions](../../embedded-copilots/failures/no-likely-next-action-suggestions.md): the opposite gap, where no choices are offered at all.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): a typed request for a person is ignored; this page covers typed answers in general and hands off after two misses.
- [Controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md): buttons that cannot be reached without a mouse. Free text is the fallback for those users too.
- [Lost drafts and failed sends](lost-drafts-and-failed-sends.md): sibling chat-interface page about typed text that disappears.

## 9. Common questions
### Why does the chatbot only accept the buttons and ignore what I type?
Usually the step is built to wait for a button value and has no branch for other text, or the chat widget turns the text box off. See [section 3](#3-why-it-happens). Try typing the exact button label; some bots accept that even when they reject other wording.

### Should a chatbot let people type when buttons are showing?
Yes. The platform docs I opened describe buttons as a way to avoid typing (Microsoft) and report a tap as a message (Meta and Microsoft), which fits treating typed text and taps as the same kind of answer. A design guide says people type anyway (section 4).

### How many quick-reply buttons can I show?
It depends on the platform. Meta's Messenger docs list a maximum of 13 quick replies and a 20-character title; Teams displays three suggested actions. Check the live documentation for your channel, because limits change.

### What if the typed answer matches two buttons?
Ask one question naming both ("Did you mean Friday the 23rd or Friday the 30th?"). Do not pick one silently. See the clarifying-question move in section 5.

---
## Technical section

### T1. Solution architecture
```
user turn (tap or text)
  -> if open_question: match(text, open_question.buttons, synonyms, slot parsers)    (rules 2-3)
       match    -> same handler as the tap -> retire buttons                          (rules 3, 7)
       no match -> new request?  answer, then re-offer question                       (rule 5)
                   else          name the mismatch, show buttons once, count a miss   (rule 4)
       2 misses on one question_id -> hand off                                        (hand-off rule)
client: composer stays enabled at every button render                                 (rule 1)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Composer enabled with buttons | Client component | Test 1, `composer.enabled` metric |
| Tap and text share one handler | Dialog manager | Tests 2-3 |
| "Something else" in every button set | Button builder lint | Test 4, metric row 4 |
| Two misses lead to hand-off | Dialog manager | Test 7 |

### T3. Evals
- **Dataset:** 40 open button questions from your own flows, each with 5 typed variants (exact label, synonym, a fitting value, a new question, nonsense); starting size.
- **Judge rubric:** did the flow advance exactly as the tap would; was the prompt repeated word for word; was a wrong option picked silently?
- **Release gate:** block a deploy if any exact-label typed reply fails to match its button (starting point).

### T5. Trade-offs
- Matching typed text needs synonyms and slot parsers per question; start with exact label plus a short synonym list.
- Confirming typed values adds a turn; do it only where a wrong match costs money, dates, or accounts.
