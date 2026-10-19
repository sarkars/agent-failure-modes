# Chatbot Doesn't Know What Page I'm On: Ignores the Page, Selection, and Form State

<!-- SEO
title: Chatbot Doesn't Know What Page I'm On: How to Fix It
description: Why an in-app assistant ignores the page, selected text, or form you just filled in, and how to pass that context, use it, and say what it used.
search phrases:
- chatbot doesn't know what page I'm on
- in-app assistant ignores selected text
- AI copilot can't see what is on my screen
- how to pass current page context to an AI chatbot
- chatbot doesn't know what I typed in the form
- why does the AI assistant ask me what I'm looking at
- how to add selected text to a copilot prompt
-->

**Frequency**: Common

## Issue: An assistant built into a product doesn't know what page the user is on, what they selected, or what they just typed in a form, so the user has to describe the screen in words or paste it in.

> **One line:** The assistant sits inside the product but answers as if it were a blank chat window, so you have to tell it what you are looking at.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product (side panel, help widget, copilot). Voice is planned, not yet written. |
| **Stakes** | Low to medium. It wastes time and produces answers about the wrong thing. It is worse when the user is mid-task, for example filling in a tax or payment form. |
| **Who is affected** | Anyone who asks a question about something on screen: a selected sentence, an error banner, a form field, a table row |
| **Frequency** | Common. I found no study that measures how often it happens; the evidence below is design guidance and one vendor release note. |
| **Pattern ID** | ignores-the-page-selection-and-form-state |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Replies that use available on-screen context when relevant. Starting target: 95% of sampled context-dependent turns. A secondary measure is how often the user restates what is on screen. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A model cannot use context the product never passes it. (Our judgment, not tested.) |
| **Also searched as** | chatbot doesn't know what page I'm on · in-app assistant ignores selected text · copilot can't see my screen · bot ignores the form I filled in · AI assistant has no page context |

## 1. In plain words
You highlight a paragraph in an app and ask its assistant, "Make this shorter." It replies, "Sure! Which text would you like me to shorten?" The app knew which text. The assistant was never handed the selection, the page, or the form values, so you do the describing.

## 2. What it looks like

**Without the fix**
```
(User is on the Billing page; a red banner reads "Card declined: expired". The card field shows 4242.)
User: Why isn't this working?
Bot:  I'm sorry to hear that! Could you tell me what you're trying to do and what error you see?
User: The card thing. It says declined. I'm on the billing page
Bot:  Thanks. Which card are you using?
```

**With the fix**
```
User: Why isn't this working?
Bot:  The card ending 4242 was declined because it expired. You can update the expiration
      date below, or add a different card. Do you want to update this one?
User: Update it
Bot:  Enter the new expiration date in the field marked "Expires". I'll check it before you save.
```
The fixed assistant used the page, the banner, and the field value, said what it used, and answered the question the user actually asked.

## 3. Why it happens
These are our reading of the pattern; the sources below report design practice, not measured causes.
- **The product never passes the context.** The chat box is a separate component. The route, the selection, and the form values are not in the request it sends.
- **The context is captured at the wrong time.** Clicking into the chat input clears the text selection, or the selection resets after one message, so it is gone by the time the reply is built.
- **A fallback hides the gap.** A missing route becomes "unknown" and the assistant answers generically, with no error anyone sees.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Microsoft's guidelines for human-AI interaction include guideline 4, "Show contextually relevant information", worded "Display information relevant to the user's current task and environment", under the heading "During interaction". The article is dated February 1, 2019. | [Microsoft Research blog, *Guidelines for human-AI interaction design*](https://www.microsoft.com/en-us/research/blog/guidelines-for-human-ai-interaction-design). Opened and read. | Design guidance from a vendor's research group, not a measurement of this failure. The article says little more about context than the guideline text. |
| OutSystems' release note for Mentor (July 7, 2026) says Mentor detects the element selected in ODC Studio (such as a button, an If node, or an Aggregate) and tracks what is open, so "Explain this" works without describing the location. It says earlier interactions needed developers to specify what was open and selected, which led to "longer prompts, more hallucinations." | [OutSystems product update: Mentor in Studio selection awareness](https://www.outsystems.com/product-updates/mentor-in-studio-selection-awareness). Opened and read. | Single-source vendor claim about its own product. The page gives no numbers, so it shows the design, not the size of the problem. |

**Not used.** A search turned up a vendor figure from WalkMe about friction when AI lacks context. I did not open the report, so it is kept out of this page. I could not open a GitHub-style issue (HTTP 403) that describes selection reset after a send; the "reset after send" cause above rests on a search summary only.

**Public incident and study.** No public incident found, and no study that measures how often assistants ignore on-screen context. My searches returned vendor documentation and design guidance.

## 5. The fix

**The principle:** Pass the page, the selection, and the form state to the assistant with every message, use them when the question points at them, and say what you used.

**Do this**
1. **Send a context packet with every user turn.** It holds the route or screen name, the current selection (if any), the focused field, and the visible form values the user is allowed to share. A missing field is sent as absent, never as "unknown".
2. **Capture the selection when the chat opens or the user starts typing,** not when they press send, because clicking the input can clear it.
3. **Resolve "this", "here", and "it" against the packet first.** If the user says "this" and the packet has a selection, the selection is the referent.
4. **Say what you used.** Name it in the reply ("the paragraph you selected", "the card ending 4242") so the user can catch a wrong guess.
5. **Never ask the user to describe what the packet already holds.** Ask only for what the packet lacks, one item at a time.
6. **Mask fields the user did not agree to share.** Passwords, full card numbers, and government IDs are never put in the packet or echoed back.
7. **When context is stale or missing, say so.** If the selection is older than the last user action, or the page changed, confirm before acting on it.

**Reference design: context packet and decision table**
```
context_packet:
  route: /settings/billing          # absent -> null, never "unknown"
  selection: "text the user highlighted" | null
  focused_field: card_expiry | null
  form_values: {card_last4: "4242", card_status: "declined: expired"}   # shareable fields only
  captured_at: turn_start
```
| User turn | Packet holds | Assistant does |
|---|---|---|
| "Make this shorter" | A selection | Rewrites it and says "the paragraph you selected" |
| "Make this shorter" | No selection, a document open | Asks one question: which part, or the whole document |
| "Why isn't this working?" | An error banner and a field value | Leads with the cause from the banner |
| "Why isn't this working?" | Two plausible errors on the page | Offers the two as choices |
| "Fix this" | Selection older than the last page change | Says it is not sure it is still current and shows what it will use |
| Any turn | Packet fetch failed | Says it cannot see the screen and asks for the one thing it needs |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The packet resolves "this": answer about the selection, banner, or field and name it |
| Ask one clarifying question | The packet has no referent (nothing selected, nothing focused) |
| Offer choices | Two to four on-screen items could be "this": "The card error", "The address warning", "Something else" |
| Admit uncertainty and show how to check | The packet may be stale or failed to load: say what you are using and how to correct it |

**Don't over-correct.** Do not recite the whole screen back ("I see you are on the Billing page with four fields..."), and do not act on a selection the user may have forgotten. If the question has nothing to do with the screen, ignore the packet. Do not read form values the user has not finished typing as final.

**Hand-off rule.** If the assistant cannot see the screen and the user is stuck on a payment, legal, or account step, offer a person ([talk to a human](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)) and pass the packet along so they do not ask again ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Not yet run. No test file exists for this pattern.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | User selects a paragraph and asks "Make this shorter" | The reply edits that paragraph and names it (rules 1, 3, 4) |
| 2 | Same ask with nothing selected | One clarifying question, not a generic reply (rule 5) |
| 3 | User clicks into the chat input after selecting text | The selection is still in the packet (rule 2) |
| 4 | Billing page with a declined-card banner, user asks "Why isn't this working?" | The cause is stated without asking the user what the error says (rules 1, 3) |
| 5 | Form has a password field | The value is absent from the packet and never echoed (rule 6) |
| 6 | Page changed after the selection was made | The assistant confirms before acting on it (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Replies that use available on-screen context when relevant** (primary) | 95% of sampled context-dependent turns | Sample turns where the packet held a referent for the user's words; a reviewer or judge marks whether the reply used it | Below 85% |
| Turns sent with a context packet | 100% | Share of user turns whose request body has the packet fields | Any drop |
| User restates what is on screen | Track; set from baseline | User turn right after an assistant question restates the page or selection (see signals) | Rising two weeks in a row |
| Wrong-referent rate (counter-metric) | Under 2% | Replies where the user rejects "the paragraph you selected" or similar | Over 5% |
| Masked fields leaked (counter-metric) | 0 | Packet and reply scan for masked field values | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Proposed until checked against human-labeled conversations. Written for text chat only; voice is not applicable.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Assistant asks "which text/page/field?" when the packet held a selection or focused field | Assistant question joined to the packet in the same turn | The user's question was about something off screen |
| User restates what is on screen after a reply ("the card thing, it says declined") | User turn following a generic assistant question, text matching visible page content | The user is adding detail the screen does not show |
| Request body has no route or selection field, or the route is a placeholder | Request log fields for the turn | A page that has nothing to select or share |
| User pastes a block of text that equals the current selection or visible field | Pasted text matched to the packet | The user is quoting from another app |

**Starter rule:** on every turn, pass the page, selection, and shareable form values to the assistant, resolve "this" against them first, and name what was used in the reply.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ignores-the-page-selection-and-form-state
runs: pre_send
reads: [context_packet.route, context_packet.selection, context_packet.focused_field, context_packet.form_values, draft_reply]
trigger: the user's turn refers to something on screen ("this", "here", "it") and the draft asks the user to describe it or ignores it
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty]
choices: ["The card error", "The address warning", "Something else"]
on_miss: rewrite
metric: replies that use available on-screen context when relevant
counter_metric: wrong-referent rate
status: proposed
```

## 8. Related patterns
- [Re-asks for known information](re-asks-for-known-information.md): the assistant asks for account data (name, order number) the product holds. This page covers what is on screen right now: page, selection, form.
- [Missing the obvious intent](missing-the-obvious-intent.md): the assistant misreads what the user wants even with the words in hand. Here the words point at something the assistant was never given.
- [Generic first response](generic-first-response.md): a boilerplate opening such as "How can I help?". It is often the visible result of a missing context packet, but it can also happen with full context.
- [Missing memory recall](../../../../../cross-cutting/operations/goals/memory-safety/failures/missing-memory-recall.md): forgetting earlier turns. Here the data comes from the screen.
- [Handoff context incompleteness](../../../../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md): context lost between agents.

## 9. Common questions
### Why doesn't the chatbot know what page I'm on?
Usually the chat component is not given the route, selection, or form values, or they are lost before the reply is built. The fix is in [section 5](#5-the-fix). A better model does not help if the context never arrives.

### How do I make an AI assistant use the text I selected?
Capture the selection when the chat opens, include it in the context packet on every turn, and tell the assistant to resolve "this" against it. Capture before the user clicks the input, since that can clear the selection.

### Is it safe to send form values to the assistant?
Send only what the user has agreed to share and what the task needs. Mask passwords, full card numbers, and government IDs. This page is design guidance, not legal advice.

### How do I measure whether it is happening?
Sample turns where the user's words point at something on screen and mark whether the reply used it. Also count the times the user restates the screen. See section 7.

---
## Technical section

### T1. Solution architecture
```
UI event (route, selection, focus, form) -> context packet builder -> request -> assistant
                                          \-> mask list -> packet (shareable fields only)
```
The builder runs in the client at chat open and at each send, and the server adds only data this user may read.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Every turn carries the packet fields | Request schema | Log check on missing fields (test 1) |
| Selection is captured before input focus | Client event handler | Test 3 |
| Masked fields never leave the client | Packet builder | Scan, test 5 |

### T3. Evals
- **Dataset:** screens with a known selection, error banner, or form state, plus questions that point at them and some that do not. Size to start: 100 turns.
- **Judge rubric:** did the reply use the on-screen item the question pointed at, and name it?
- **Metrics and starting thresholds:** primary metric 95%; wrong-referent rate under 2%. Starting points to tune.
- **Release gate:** block a deploy if the primary metric drops on the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Turns with a packet | Under 99% | Under 90% | Check the client capture and the request schema |

### T5. Trade-offs
- More context raises privacy exposure and prompt size; the mask list and "send only what the task needs" limit both.
- Selection and focus capture add client code per surface (text editor, table, form).

---
### Deep dive
- **Open question.** I found no measurement of how often in-app assistants ignore on-screen context, and no sourced public incident.
- **References.** [Microsoft Research](https://www.microsoft.com/en-us/research/blog/guidelines-for-human-ai-interaction-design) (opened); [OutSystems](https://www.outsystems.com/product-updates/mentor-in-studio-selection-awareness) (opened). Search summaries only, not opened: a GitHub-style feature request on selection chips, a WalkMe page on screen context.
