# Drive-Thru Screen Shows a Different Order Than the Voice Said: Screen and Spoken Order Disagree

<!-- SEO
title: Drive-Thru Screen and Voice Order Don't Match: How to Fix It
description: The order board shows one order and the voice agent reads back another. Build both from one order record, so what the customer sees is what is spoken.
search phrases:
- drive thru screen doesn't match what the AI said
- ai drive thru order screen shows different items
- chatbot says one cart but cart shows another
- ai ordering readback doesn't match screen
- voice ordering confirmation screen mismatch
- single source of truth for voice and screen ordering
- chatbot order summary different from checkout
-->

**Frequency**: Occasional

## Issue: A drive-thru, kiosk, or ordering assistant shows one order on the screen and says another in its readback, so the customer cannot tell which one is real.

> **One line:** The order board shows one thing and the speaker says another.

| | |
|---|---|
| **Channel** | Written for **text chat** (the chat reply says one cart, the cart panel shows another) and for the **order screen plus readback** at drive-thru, kiosk and app ordering. The spoken form is described from reports and design reasoning; voice-only signals are PLANNED. |
| **Stakes** | Medium. A wrong item is a remake; a wrong allergy note, or a total that differs from what was agreed, is worse. |
| **Who is affected** | Anyone who checks an order by ear and by eye, especially drivers who glance at the board while talking, and crew who fill the order from the screen |
| **Frequency** | Occasional (our judgment). I found no count of display-versus-speech mismatches; the public reports I opened describe related errors, not this one directly. |
| **Pattern ID** | screen-and-spoken-order-disagree |
| **Family** | [Drive-thru agents](../README.md) |
| **Goal** | Voice ordering gets the order right, shows it, and never pressures or risks someone's health. |
| **Primary metric** | Mismatches between display and spoken readback. Target: 0 (starting target to tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Two outputs built from different state is an engineering fault, not a language fault. (Our judgment, not tested.) |
| **Also searched as** | ai drive thru screen wrong · order board doesn't match readback · bot says different order than screen · cart panel differs from chat · confirmation doesn't match checkout |

## 1. In plain words
The customer is given two views of the same order: what the board shows and what the voice says. If they differ, the customer has no way to know which will reach the window. Both views must come from one order record, so the voice reads what the board shows.

## 2. What it looks like
A drive-thru lane at a burger chain with an on-screen order board.

**Without the fix**
```
Customer: Two cheeseburgers, no onions, and a large fries.
Board:    2 Cheeseburger | 1 Large Fries            $11.48
Agent:    So that's two cheeseburgers, a large fries and a large Coke. Anything else?
Customer: I didn't ask for a Coke. The board doesn't show one.
Agent:    Sorry about that. Your total is $13.47. Pull forward.
(The board still says $11.48 and shows no "no onions" note.)
```
**With the fix**
```
Customer: Two cheeseburgers, no onions, and a large fries.
Board:    2 Cheeseburger (no onions) | 1 Large Fries     $11.48
Agent:    Here's what's on the screen: two cheeseburgers, no onions, and a large fries. Total $11.48. Is that right?
Customer: Yes.
Agent:    Thanks. Pull forward to pay.
```
The fixed agent says only what the board shows, including the note and the total, because it speaks from the same order record.

The text-chat form is the same fault:
```
Bot:   Added: 1 Margherita pizza, 1 garlic bread. Your cart is $18.50.
Cart panel (right side): 1 Margherita pizza  $14.00
```
The fixed bot builds its reply from the cart record, so the panel and the reply cannot differ.

## 3. Why it happens
These are our reading of the pattern.
- **Two code paths build two outputs.** The speech reply is generated from the model's running idea of the order, while the board is drawn from the point-of-sale record. Each can be right about its own state and still disagree.
- **The sync is the weak link.** Screens that mirror the register depend on the link between them. Toast describes its confirmation screen as showing items "as they are entered into the POS in real-time", and says the connected POS must be the one the order was placed on. When that link or the menu configuration lags, the views drift apart.
- **Changes land on one side.** A correction ("actually, no onions"), a limited-time item, or a price change is applied to one record and not the other, so the readback and the board carry different versions.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Nielsen's first heuristic says a design "should always keep users informed about what is going on". His fourth says users "should not have to wonder whether different words, situations, or actions mean the same thing". Two conflicting descriptions of one order break both. | [Nielsen, *10 Usability Heuristics*, NN/g, 1994, reviewed Jan. 2024](https://www.nngroup.com/articles/ten-usability-heuristics/). Opened and read. | General interface guidance, not drive-thru research. It does not test voice plus screen. |
| A drive-thru operator guide says AI ordering works when "the order is confirmed on screen before the pay window," calls the screen "the contract with the guest," and names "menu drift" (a limited-time item that reached the menu boards but not the AI setup) as a failure mode. | [TSourcing, *Drive-thru AI ordering: what operators should know*, listed Sept. 28, 2026](https://www.tsourcing.com/resources/drive-thru-ai-ordering-what-operators-should-know). Opened and read. | A vendor-side guide with no data on mismatch rates. |
| A mystery-shop study of 120 orders at AI lanes of three chains (June and July 2025) scored AI lanes 83% accurate against 87% across all lanes visited. | [Maple, *AI drive-thru accuracy: what the published numbers measure*](https://maple.inc/blog/ai-drive-thru-accuracy). Opened and read; the study is relayed secondhand (Intouch Insight). | Written by a vendor of a competing product. It does not say why orders were wrong, so it does not isolate screen-versus-voice mismatch. |
| In an open-source shop's issue tracker (Oct. 17, 2026), the checkout showed a total from the price saved in the cart while the server booked the current database price, so a customer could pay a different amount than the page showed. The proposed fix: pay exactly what was shown, or be told of the change. | [kartalbas/coder-shop issue #12](https://github.com/kartalbas/coder-shop/issues/12). Opened and read. | One small project's bug report, closed the day it was opened. It is a cart-versus-charge mismatch, not a chatbot. It shows the engineering shape of the fault. |
| Toast's confirmation screen is built to show items as they are entered in the POS, with modifiers, total and discounts. | [Toast support, Delphi order confirmation screen](https://support.toasttab.com/en/article/Getting-Started-Delphi-Order-Confirmation-Screen). Opened and read. | Product documentation, not evidence of how often the screen and speech differ. |

I found no study that measures display-versus-readback mismatches, and no public report that describes one. The [Taco Bell teardown](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md) says the sources did not describe a readback or on-screen order at all, so I do not claim it as an example of this pattern.

**Public incident.** No public incident found for a drive-thru or chat agent whose readback contradicted its own order screen. Searches run: "drive-thru order confirmation screen does not match what was said AI", "voice and visual feedback consistency single source of truth ordering UX", "chatbot cart summary differs from checkout wrong items in cart".

## 5. The fix
**The principle:** The visible order is the single source of truth, and every readback is generated from it.

**Do this**
1. **Keep one order record.** Items, modifiers, quantities, prices and total live in one store. The board, the speech and the chat reply all read from it. Check: no component holds its own copy of the order.
2. **Generate the readback from the record, not from the model's memory.** The model may choose the wording, but not the items. Check: every item and modifier in the spoken or chat readback appears in the record at that moment.
3. **Write to the record first, then speak.** An item or correction is saved, shown, and only then said. Check: no spoken item has an earlier timestamp than its record entry.
4. **Compare before you speak.** Before a readback, diff the rendered screen state against the record. If they differ, do not read it back; fix the screen first. Check: a forced mismatch blocks the readback.
5. **Say what the screen shows, and point to it.** "Here's what's on the screen: ..." Check: the readback names the total shown.
6. **Re-read the record before checkout.** A chat or app cart summary is fetched from the cart system right before it is shown or sent to payment. Check: the total paid equals the total last shown.
7. **On a detected mismatch, stop and say so.** Show the record, read it, and ask which is right if the customer disagrees. Check: no "Pull forward" after a mismatch flag.
8. **Hand off when the screen cannot be trusted.** After a second mismatch, give the lane to a person with the record on the screen.

**Reference design: one order record, three views**
| Part | Rule |
|---|---|
| Order record | Single store of items, modifiers, quantities, prices, total, version number |
| Board / cart panel | Renders the record; shows the version it drew |
| Speech / chat reply | Template filled from the record; carries the version it read |
| Gate | Spoken version must equal displayed version, or no readback |
| Checkout | Re-fetches the record; pays the total last shown |

```
Never state an item, modifier, quantity or price that is not in the order record.
Read the order back from the record, and say what the screen shows.
If the screen's version differs from the record's, fix the screen, then read it back.
If the customer says the screen and your words disagree, show the record and ask which is wrong.
After two mismatches, hand the order to a person with the record on the screen.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The customer says the screen and the voice differ, or the gate flags it: say that the two disagree, show the record, and read from it. Do not use it on every order. |
| Ask one clarifying question | The customer's correction conflicts with the record: "The screen shows no onions. Do you want onions back?" Skip it when the record already matches what they said. |
| Hand off to a person | After two mismatches in one order, or on request: pass the record to a crew member. |

Offer choices is not used here: at a speaker a menu of options slows the line, and the screen already carries the order.

**Don't over-correct.** Do not add a second confirmation round on every order. One readback from the record is enough when the gate passes. Do not block the lane for a harmless difference in wording (for example "fries" versus "large fries" when the record has the full name); compare items, not phrasing.

**Hand-off rule.** Give the crew member the record, its version, and what the customer said was wrong. Keep the record on the screen for both of them ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **Not yet run**. Replay orders through the speech, screen and chat outputs and diff them.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Simple order, then readback | Every spoken item matches the screen (1, 2) |
| 2 | "No onions" correction | Screen and readback both show it (3) |
| 3 | Force the screen to lag the record by one item | Readback is blocked until the screen catches up (4) |
| 4 | Menu item added to the record but not the model's list | Readback shows it, not the model's version (2) |
| 5 | Chat: bot adds an item, cart panel shows a stale cart | Reply is built from the cart record, panel refreshes (1, 6) |
| 6 | Price changes between cart and checkout | Customer pays the last-shown total, or is told (6) |
| 7 | Customer says "the screen says something else" | Record is shown and read; no "pull forward" until resolved (7) |
| 8 | Second mismatch in one order | Hand-off with the record on the screen (8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Mismatches between display and spoken readback** (primary) | 0 | Diff the readback's item list against the record's item list at the moment of speech | Any |
| Readbacks generated from the record | 100% | Log the record version on every readback and every render | Below 99% |
| Total paid differs from total last shown | 0 | Compare the last displayed total with the charged total | Any |
| Orders where the customer disputes the screen or the voice | Track; set from baseline | Transcript flag for "the screen says...", plus crew notes | Rising |
| Readback time added (counter-metric) | Track; set from baseline | Median seconds from last item to payment | Rising by more than a set margin |

### Detection signals (proposed, not yet calibrated)
Written for the order log and chat transcript. Signals that need audio (the agent said something the recognizer scored low) are PLANNED for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Spoken or chat readback contains an item not in the record | Readback event item list vs. record items | A recorded add that landed a moment after the diff |
| Displayed version differs from spoken version | Version number on render and on readback | A render that was a few hundred milliseconds behind and caught up before the customer looked |
| Customer says "that's not what the screen says" or similar | Transcript phrase match | The customer is describing their own earlier request, not the screen |
| Charged total differs from last displayed total | Payment event vs. last render event | A promo or tax applied at payment that the screen said it would |
| Crew edits items right after a readback with a yes | Crew edit event after confirm | The customer changed their mind at the window |

**Starter rule:** every readback is generated from the order record the screen shows, and is blocked if the two differ.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: screen-and-spoken-order-disagree
runs: pre_send
reads: [order.record_version, order.items, display.rendered_version, display.rendered_items, readback.items, order.total, display.total]
trigger: a readback or order summary is about to be spoken or sent, or the customer says the screen and the voice differ
moves: [admit_uncertainty, ask_clarifying_question, hand_off]
choices: none
on_miss: rewrite
metric: mismatches between display and spoken readback
counter_metric: readback time added
status: proposed
```

## 8. Related patterns
- [Order mix-ups at the speaker](order-mix-ups-at-the-speaker.md): the closest page. It covers an order that is wrong with no readback or screen to check it. This page covers a readback and a screen that both exist but disagree.
- [Voice to visual handoff failure](../../voice/failures/voice-to-visual-handoff-failure.md): moving the user from voice to a screen. This page is about the two staying equal while both are in use. (Matched by name; I did not re-read it.)
- [Conflicting inputs resolved silently](../../multimodal-input/failures/conflicting-inputs-resolved-silently.md): the user's own inputs conflict. Here the system's two outputs conflict. (Matched by name; I did not re-read it.)
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): a correction lands in one place and not another, a common route to this mismatch.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the guardrail here is one readback, not many.
- [Taco Bell teardown](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md): a drive-thru incident page; its sources do not describe this fault.

## 9. Common questions
### Why does the drive-thru screen show something different from what the AI said?
I found no source that explains a specific case. The likely causes are in section 3: the speech and the screen are built from different state, the register link lags, or a correction reached only one side. This is our reading.

### Which should I trust, the screen or the voice?
Trust the screen, and say so out loud if they differ. A well-built system reads from the screen's record, so the voice cannot be the better source. Ask the crew to confirm before you pay.

### Can a chatbot's cart summary differ from checkout?
Yes, when the bot summarizes from its own memory or an old copy of the cart. The fix is to re-read the cart from the cart system right before showing a summary or sending the user to pay (rule 6).

### Should the readback be generated by the language model?
The model can choose wording, but the items, modifiers, quantities and prices should be filled in from the order record. Otherwise the readback can invent or drop items the screen does not have (rule 2).

---
## Technical section

### T1. Solution architecture
```
speech / chat input -> intent + slots -> order service (single record, version N)
order service -> board / cart panel (renders version N)
              -> readback template (fills from version N) -> speech / chat reply
gate: readback.version == display.version, else re-render then read
checkout: re-fetch record -> charge last-shown total
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Readback fields come from the record only | Readback renderer | Test 4, log scan |
| Readback blocked on version mismatch | Gate before speech | Test 3 |
| Pay the last-shown total | Checkout | Test 6 |

### T3. Evals
- **Dataset:** 200 scripted orders with corrections, menu changes and forced sync lag (chat and speech).
- **Judge rubric:** does every spoken or written item and price match the displayed record at the time of speaking?
- **Metrics and starting thresholds:** mismatches 0; readbacks from record 100%. Starting points to tune.
- **Release gate:** block a deploy if any scripted order produces a mismatch.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Display-versus-readback mismatches | Any in a day | More than 1 per site per day | Check the POS sync and the readback renderer |

### T5. Trade-offs
- A version check adds a small delay before the readback; skip it only if the record and the render are the same code path.
- Strict templates make the voice less flexible; the customer still hears natural wording around the filled fields.

---
### Deep dive
- **Open question.** I found no public data on how often a screen and a readback differ. The evidence is general design guidance, operator guidance and one cart-versus-charge bug report.
- **References.** [NN/g, 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/) (opened); [TSourcing](https://www.tsourcing.com/resources/drive-thru-ai-ordering-what-operators-should-know) (opened); [Maple](https://maple.inc/blog/ai-drive-thru-accuracy) (opened); [coder-shop issue #12](https://github.com/kartalbas/coder-shop/issues/12) (opened); [Toast support](https://support.toasttab.com/en/article/Getting-Started-Delphi-Order-Confirmation-Screen) (opened). Read through search summaries only and not used in the fix: other vendor pages on confirmation screens, and an architecture guide that says the cart must remain authoritative.
