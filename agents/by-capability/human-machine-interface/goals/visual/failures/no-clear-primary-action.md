# Chatbot Buttons: No Clear Primary Action or Next Step

<!-- SEO
title: Chatbot Buttons: No Clear Primary Action or Next Step
description: Why a chatbot reply or card leaves users unsure what to do next, with three equal buttons or "Anything else?", and rules for one primary action and a way out.
search phrases:
- chatbot buttons too many options
- chatbot dead end anything else
- how many buttons should a chatbot message have
- chatbot primary action vs secondary action
- chatbot card design one call to action
- chatbot doesn't tell me what to do next
- quick reply buttons best practices
- chatbot response ends with no next step
-->

**Frequency**: Common

## Issue: A chatbot reply or card ends with no obvious next step, or with several equal buttons and links, so the user does not know what to do next.

> **One line:** The bot shows three buttons that look the same, or ends with "Is there anything else?"; the fix is one clearly primary action per message, secondary actions that look and read as secondary, and a way out.

| | |
|---|---|
| **Channel** | Written for **chat** (text replies, buttons, quick replies and cards). Voice and web-page variants are PLANNED, not written. |
| **Stakes** | Low to medium. A missed step on a payment, claim, or booking can cost the user money or a deadline. |
| **Who is affected** | Anyone who finishes a task or reaches a decision point, and especially first-time users who do not know what the assistant can do |
| **Frequency** | Common as a design default. I found no study that counts how often chat products ship competing buttons or dead-end closers. |
| **Pattern ID** | no-clear-primary-action |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Share of decision messages and cards that have exactly one primary action. Starting target: 100% (a starting point; tune it). Read it next to the dead-end rate. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The buttons, card layout and closing line come from the product's templates and flow, not the model's answer. A better model can still be handed three equal buttons. (Our judgment, not tested.) |
| **Also searched as** | chatbot too many buttons · bot doesn't say what to do next · "is there anything else" chatbot · equal-weight buttons · chatbot dead end · which button do I press |

## 1. In plain words
After a bot answers, the user needs to know the next move. Often the message gives none ("Is there anything else I can help with?") or gives several that look alike, so the user stares at three buttons and picks at random or leaves. The fix is one obvious main step in every message, other options that clearly rank below it, and always a way to say "something else" or reach a person.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Northfield Bank" assistant)
```
User: My debit card was declined at the pharmacy.
Bot:  I found 2 recent declined payments on your card ending 4821.
      [View transactions] [Replace card] [Freeze card] [Dispute a charge] [Learn about card security]
      (all five buttons are the same size and color)
User: ok
Bot:  Is there anything else I can help you with?
```
**With the fix**
```
User: My debit card was declined at the pharmacy.
Bot:  Your card ending 4821 was declined twice today because the daily limit of $500 was reached.
      [Raise my limit for today]            (primary: solid, first)
      [See the two payments]  [Something else]  [Talk to a person]    (secondary: plain text)
User: ok
Bot:  Do you want me to raise the limit for today? It takes effect right away.
```
The fixed version names the cause, leads with one main action in plain verb words, shows the other options as clearly lesser, and still gives a way out. When the user answers "ok", the bot asks the one question that moves things forward, not "anything else?".

## 3. Why it happens
- **Every team adds one more button.** Each button was requested by a different owner (support, sales, compliance). No one owns the message as a whole, so no one picks the primary action.
- **Templates are filled by rule, not ranked.** A card template lists the actions the account allows. Nothing sorts them by what the user most likely needs next, so they render in equal weight.
- **A closer is cheaper than a next step.** "Is there anything else?" needs no account data. A real next step needs the state of the task, which the reply template often does not receive.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The GOV.UK Design System says: "Use a default button for the main call to action on a page" and "Use secondary buttons for secondary calls to action on a page." It adds: "Avoid using multiple default buttons on a single page" and "Pages with too many calls to action make it hard for users to know what to do next." | [GOV.UK Design System, Button](https://design-system.service.gov.uk/components/button/). Opened and read. | Guidance for government web pages, not chat. It states no numeric limit. |
| The same page gives the reason as: "Having more than one main call to action reduces their impact." It advises: "Before adding lots of secondary buttons, try to simplify the page or break the content down across multiple pages." | Same GOV.UK page. | Design guidance, not a measured result. |
| Nielsen Norman Group describes button styles by importance: primary buttons "have the most visual emphasis to grab user attention" and are typically solid and filled; secondary buttons have "a medium visual emphasis" for actions "less important or commonly used" and are typically outline; tertiary buttons have "the least amount of visual emphasis" for optional or supplementary actions. | [NN/g, Button States: Communicate Interaction](https://www.nngroup.com/articles/button-states-communicate-interaction/). Opened and read. | The article is about button states; the style hierarchy is a side point in it. No test data in the part I read. |
| Google's conversation design guidance on chips says they help users refine topics, discover related topics and next steps, and take action. It sets a maximum of 8 chips per turn and 25 characters per chip, says to "Move the conversation forward, but don't put words in the user's mouth", to lead action chips with a verb, and not to repeat options already shown in a list or carousel. | [Google for Developers, Conversation Design: Chips](https://developers.google.com/assistant/conversation-design/chips). Opened and read. | A platform limit, not a target. The page is for Google Assistant, which Google has marked legacy in related pages (I did not confirm the current status). |
| Microsoft's Bot Framework guidance says buttons are "a great way to present the user with a simple choice", and advises: "Start by using the minimum UI controls that enable the bot to solve the user's problem, and add other elements later if those controls are no longer sufficient." It also says each channel controls how its clients render cards and buttons. | [Microsoft Learn, Design the user experience (Bot Service)](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-design-user-experience?view=azure-bot-service-4.0). Opened and read. | Guidance for one framework. It does not rank buttons. Rendering can differ by channel, so test on each. |

**How this differs from the closest pages.** [Cognitive overload](cognitive-overload.md) is about too much information in one reply; this page is about a reply whose next step is missing or unranked, even when the reply is short. [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) covers the fallback after a misunderstanding; this page covers dead ends after a successful answer and on cards. [No likely next-action suggestions](../../embedded-copilots/failures/no-likely-next-action-suggestions.md) covers which next steps to pick from product state; this page covers how to present them (one primary, rest secondary, a way out). [No way back in a flow](../../dialogue-management/failures/no-way-back-in-a-flow.md) covers back, change and start over inside a multi-step flow.

**Public incident.** I found no public incident of a chatbot that failed only through competing buttons. The nearest library item is the [CFPB report on bank chatbot "doom loops"](../../../incidents/cfpb-bank-chatbot-doom-loops.md), which is about having no route to a person, one part of this page's "way out" rule.

## 5. The fix

**The principle:** Every message that asks the user to decide has exactly one primary action, every other option is plainly secondary, and no message leaves the user without a next step or a way out.

**Do this**
1. **One primary action per decision message or card.** It comes first, is styled as the strongest option (solid, not outline), and is worded as a verb plus outcome ("Raise my limit for today"). A message that is only a statement is not a decision message; it still follows rule 4.
2. **Rank the rest as secondary.** Secondary actions use a lighter style or plain text and plain labels. Show at most 3 secondary actions plus "Something else" (a starting point). If more options exist, show the likeliest and keep free text open.
3. **For truly equal options, ask a question, not a card.** A yes/no or A/B choice is asked in words ("Which do you want, a replacement card or a limit increase?") with options of identical style. Label such messages as equal-choice so the primary-action check skips them.
4. **Never end on a bare closer.** A reply may not end with only "Is there anything else?", "Let me know if you need anything", or "Hope that helps". End with one next step drawn from the task state, or say the task is done and what happens next ("Your replacement card ships Friday. I'll message you when it does.").
5. **Always include a way out.** Every card and choice set carries "Something else" and a route to a person where one exists. Free text stays open next to buttons ([see typed answers next to buttons](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md)).
6. **Don't repeat what is already shown.** If a list or card already presents options, the buttons below it narrow or decline the list; they do not repeat it.
7. **Say what a button does.** Labels state the result in plain words; none says only "Continue", "Learn more", or "Click here" when other buttons are nearby.

**Reference design: decision message**
| Part | Content |
|---|---|
| Lead | What happened, in one sentence, with the cause if known |
| Primary action | One solid button, verb plus outcome, first |
| Secondary | Up to 3 plain-text options, lower in the visual order |
| Exit | "Something else" and, where available, "Talk to a person" |
| Free text | Open at all times |

```
Each message that asks the user to decide must have exactly one primary action, placed first and worded as a verb plus outcome.
Other actions are secondary: lighter style, at most 3, plus "Something else".
Never end a reply with only "Is there anything else?"; end with one next step or a clear statement that the task is done.
Always keep free text open and offer a route to a person where one exists.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply states the result or cause first, then the one action that follows from it |
| Offer choices | The next step has 2-4 likely meanings: one primary, the others secondary, plus "Something else", free text open. Do NOT offer buttons when the next step is obvious from the answer; ask the one question in words |
| Ask one clarifying question | The user replies "ok" or "?" to a card: ask the single question that picks the primary action |
| Hand off to a person | The user ignores two cards in a row or asks for a person: offer the route with a summary |

**Don't over-correct.** One primary action does not mean one choice. Do not strip secondary options users need, such as "See the two payments", and do not force a single path when the user's need is unclear. If the next step is genuinely unknown, ask one question in words. Do not make the primary action a sales push; it should be what the user most likely needs next, and for a destructive or irreversible step, confirm before running it.

**Hand-off rule.** When the user ignores two consecutive cards, types "?" or "what now" twice, or asks for a person, stop showing buttons and offer a route to a person with a one-line summary ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet. Rules 1, 2 and 7 follow the button-hierarchy guidance in section 4; rule 5 follows the library's [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No test file yet. The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Trigger a reply that asks the user to decide | Exactly one button is styled primary, listed first, with a verb-plus-outcome label | 1, 7 |
| 2 | Trigger a card with 5 possible actions | At most 3 secondary actions plus "Something else"; the rest are dropped or moved behind free text | 2 |
| 3 | Trigger a true A/B choice | The options are asked in words with identical style, and the message is tagged equal-choice | 3 |
| 4 | Finish a task (refund filed, form sent) | The reply ends with a next step or a "done, and here is what happens next" line, not a bare closer | 4 |
| 5 | Read every card and choice set in the flow | Each has "Something else"; a route to a person exists where staffed; free text still works | 5 |
| 6 | Show a list, then the buttons under it | The buttons do not repeat the listed items | 6 |
| 7 | Reply "ok" to a card | The bot asks one question that selects the primary action, not "anything else?" | 4 |
| 8 | Ignore two cards in a row | The bot stops showing buttons and offers a person | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Decision messages and cards with exactly one primary action** (primary) | 100% (starting point) | Log each outgoing message with its `actions[]` and a `style` field; count messages tagged `decision` with exactly one `style = primary` | Below 98% |
| Dead-end rate: bot messages with no action, no question, and no stated outcome | Under 2% (starting point) | Sample or classify final lines for closers with no next step; count per 100 bot messages | Above 5% |
| Cards and choice sets with an exit ("Something else" or a person) | 100% | Check each `actions[]` set for an exit label | Any card without one |
| Secondary actions per message | 3 or fewer plus the exit (starting point) | Count non-primary actions per message | Above 4 |
| Reply to a card is "ok", "?" or "what now" | Track; set from your baseline | Count user turns matching those strings right after a card | Rising |
| Free-text fallback rate after cards (counter-metric) | Track; do not chase | User types instead of tapping | Falling sharply after a fix: the buttons may now hide needed options |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat** text and button events only; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A decision message has zero or two or more actions with `style = primary` (rules 1, 3) | `message.actions[].style` count | A message tagged equal-choice (rule 3) |
| A bot message ends with a bare closer phrase and has no actions (rule 4) | Final sentence matches a closer list; `actions` empty | The user just said goodbye and the bot is replying to it |
| A card carries 4 or more actions of the same style (rule 2) | Count by style per message | A carousel where each card has one button |
| A card or choice set has no exit label (rule 5) | `actions[].label` lacks an "exit" tag | A step where leaving is blocked by law or by the flow (log it as a reason) |
| The user's next turn after a card is "ok", "?" or "what now" (rules 1, 4) | Short user turn after a card render | An acknowledgment of a finished task |

**Starter rule:** every message that asks the user to decide has exactly one primary action, other options are lighter and capped, and no reply ends without a next step or a way out.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-clear-primary-action
runs: pre_send
reads: [message.type, message.actions, action.style, action.label, task.state, session.free_text_open]
trigger: a reply with buttons, a card, or a closing line is about to be sent
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Raise my limit for today", "See the two payments", "Something else", "Talk to a person"]
on_miss: rewrite
metric: decision messages and cards with exactly one primary action
counter_metric: free-text fallback rate after cards
status: proposed
```

## 8. Related patterns
- [Cognitive overload](cognitive-overload.md): too much information in a reply; this page covers an unranked or missing next step.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): the dead end after a misunderstanding.
- [Answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): the bot answers and stops without moving the user toward the goal.
- [No likely next-action suggestions](../../embedded-copilots/failures/no-likely-next-action-suggestions.md): which next steps to pick from product state.
- [No way back in a flow](../../dialogue-management/failures/no-way-back-in-a-flow.md): back, change and start over.
- [Quick-reply buttons that don't match what was typed](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md): free text next to buttons.
- [Dark patterns](dark-patterns.md): rigged choices; this page is about unclear ones.

## 9. Common questions
### How many buttons should a chatbot message have?
There is no source-backed ideal. The GOV.UK guidance says to avoid multiple default buttons and warns that too many calls to action make it hard to know what to do next. Google sets a platform maximum of 8 chips, which is a ceiling, not advice. This page's starting point is one primary action, up to 3 secondary actions, and an exit (rule 2). Tune it on your own data.

### Should I always end with "Is there anything else I can help with?"
No. As the only ending it gives the user no next step. Name the next step from the task state, or state that the task is done and what happens next (rule 4). A short closer is fine after a next step, not in place of one.

### What is the difference between a primary and a secondary action?
Nielsen Norman Group describes primary buttons as carrying the most visual emphasis, usually solid and filled, and secondary buttons as medium emphasis, usually outlined, for less important actions. In chat, add the wording: the primary action states the likeliest result as a verb plus outcome, and it comes first.

### What if all the options really are equal?
Ask the question in words and give the options the same style (rule 3). Tag the message as equal-choice so the check for one primary action skips it. If you cannot tell which option is likeliest, ask one clarifying question before showing buttons.

### Does one primary action mean I can't give users choices?
No. It means one option is clearly the main step and the others are visibly lesser. Keep "Something else", a route to a person, and open free text so the user is never boxed in ([typed answers next to buttons](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md)).
