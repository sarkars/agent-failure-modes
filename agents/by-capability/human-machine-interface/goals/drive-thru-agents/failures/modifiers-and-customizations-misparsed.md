# "No Pickles, Extra Sauce" on the Wrong Burger: Modifiers and Customizations Misparsed

<!-- SEO
title: AI Drive-Thru Got My Customization Wrong: Misparsed Modifiers
description: Why a drive-thru or ordering bot puts "no pickles, extra sauce" on the wrong item or quantity, and a fix: parse modifiers per item and confirm them.
search phrases:
- ai drive thru got my order wrong no pickles
- ai drive thru ignores modifiers
- voice ordering bot special instructions wrong item
- why does ai drive thru mess up customizations
- ordering chatbot added extra sauce to the wrong item
- how to design modifier confirmation for voice ordering
- restaurant ordering bot customization errors
-->

**Frequency**: Common

## Issue: An ordering bot attaches a customization like "no pickles" or "extra sauce" to the wrong item or the wrong quantity, and the customer finds out at the window.

> **One line:** The right food arrives, but the change the customer asked for is on a different item, applied to the wrong count, or missing.

> **Read this first.** This page is design guidance, not legal, food-safety, or operations advice. It has not been reviewed by restaurant operations. Have people who run restaurant ordering, menu setup, and allergen handling review it before you use it. Allergy-related changes ("no nuts", "gluten free") are high stakes; this page treats them only as a reason to hand off.

| | |
|---|---|
| **Channel** | Written for **text chat** (app or web order bots) and **voice** at a drive-thru speaker. Voice-only signals are marked PLANNED. |
| **Stakes** | Low to medium for a missing topping; high when the change is an allergy or dietary need. |
| **Who is affected** | Customers who customize (removals, additions, substitutions), people ordering for several people, and crew who remake orders |
| **Frequency** | Common in principle: every customized order has the risk. I found no published modifier-specific error rate. |
| **Pattern ID** | modifiers-and-customizations-misparsed |
| **Family** | [Drive-thru agents](../README.md) |
| **Goal** | Voice ordering gets the order right, shows it, and never pressures or risks someone's health. |
| **Primary metric** | Modifier errors per 100 customized orders. Starting target: set from a baseline on your own orders, then tune. |
| **Maturity** | Needs review (flag R: needs a person to check the reputational claims; no test file yet, tests not yet run) |
| **Will a better model fix this?** | Partly. A better model parses more sentences correctly, but item-by-item confirmation and checking against the menu's real options are product design. (Our judgment, not tested.) |
| **Also searched as** | AI got my customization wrong · bot ignored no onions · wrong item got the extra sauce · special instructions ignored · drive thru AI modifiers |

## 1. In plain words
A customer says "a cheeseburger with no pickles and a large fries with extra salt, and make the second burger plain." The bot has to decide which change belongs to which item, and how many. When it guesses wrong, the order looks right at a glance, so nobody catches it until the bag is opened. The fix is to attach each change to one named item and read the changes back.

## 2. What it looks like

**Without the fix**
```
Customer: Two cheeseburgers, no pickles on one, and a large fries with extra salt.
Bot:      Got it. Two cheeseburgers, no pickles, and a large fries. Anything else?
Customer: That's it.
Bot:      Your total is $14.38. Pull forward.
(Both burgers are made with no pickles. The fries have no extra salt.)
```
(An illustration of the pattern, not a transcript of a real system.)

**With the fix**
```
Customer: Two cheeseburgers, no pickles on one, and a large fries with extra salt.
Bot:      Let me check. Burger 1: no pickles. Burger 2: as is. Large fries: extra salt. Right?
Customer: Yes.
Bot:      Your total is $14.38. Pull forward.
```
The fixed bot ties each change to one item, includes the item that has no change, and waits for a yes.

**Text-chat form**
```
Customer (chat): 3 tacos, no onions, one with extra sauce
Bot:             Taco 1: no onions. Taco 2: no onions. Taco 3: no onions, extra sauce.
                 Should "no onions" apply to all three? [Yes, all three] [Only one] [Something else]
```
In text, "no onions, one with extra sauce" is ambiguous. The bot asks instead of guessing.

## 3. Why it happens
These are our reading of the pattern; the sources in section 4 describe the symptom and the engineering problem.
- **The sentence does not say which item.** "No pickles" follows two burgers and a fries. Speech and text both leave out the link between a change and its item, and the bot picks one.
- **A quantity and a change collide.** "Two burgers, one with no pickles" is a count (2), a split (1 and 1), and a change. Collapsing it to "2 burgers, no pickles" is the cheapest parse.
- **The menu's rules are not checked.** If the bot accepts any phrase as a modifier instead of checking the item's real options, an impossible or misattached change can pass into the order (see the Stable Kernel guide in section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A voice-ordering engineering guide says modifier handling "creates a disproportionate share of voice ordering errors", that each change in a request must be tied to the right parent item, and that the AI "may confirm one order while the kitchen receives another." It recommends item-by-item confirmation for orders with stacked modifiers and checking each modifier against the point-of-sale menu rules. | Stable Kernel, [Menu Modifiers & Edge Cases In Voice Ordering: The Engineering Guide](https://stablekernel.com/blogs/blog-voice-ordering-menu-modifier-guide). Opened and read (the page shows the date 6/12/26 and no author). | A vendor's guide with no data behind the claim. It gives no accuracy percentages. |
| Wendy's piloted a generative-AI drive-thru ordering tool meant to understand "customer customizations." Wendy's measure was the share of orders handled without staff help, which averaged 86% in the pilot; a separate "nearly 99%" figure counted orders even when a person stepped in to fix an error. | Restaurant Dive, [Wendy's to expand Google generative AI drive-thru test](https://www.restaurantdive.com/news/wendys-expand-google-generative-ai-drive-thru-test/702184/), Dec. 11, 2023. Opened and read. | The 86% is all errors, not modifier errors. The article gives no breakdown for customizations. |
| Taco Bell's voice AI drew viral clips and an executive's remark that very busy locations may be better served by a person. | The site's [Taco Bell drive-thru incident page](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md) (opened). | That page does not report a modifier failure. It covers a quantity prank and repeated prompts. Do not read it as a modifier case. |

I found no independent measurement of modifier error rates. I found no public incident page that documents a misattached modifier as such.

**Public incident.** No public incident found for modifier misattachment as such. Searches run: "drive-thru AI order modifiers wrong item", "voice ordering NLU modifier attachment menu item slot filling", "Wendy's FreshAI order accuracy modifiers". The closest are the general order-error reports on the [order mix-ups page](order-mix-ups-at-the-speaker.md) and the [Taco Bell incident page](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md). Some search summaries described viral clips of corrections going wrong; I did not open those sources and do not rely on them.

## 5. The fix

**The principle:** Every change is attached to one named item and quantity, shown, and confirmed; when the sentence is ambiguous, the bot asks.

**Do this**
1. **Store each modifier on one line item.** An order item has its own list of changes. "Two burgers, one with no pickles" becomes two line items, not one item with a flag.
2. **Resolve the target before saving.** If a change could belong to more than one item or count, ask one question before adding it.
3. **Check each change against the item's real options.** Accept only changes the menu allows for that item. Say so when one is not available ("The fish sandwich doesn't come with pickles to remove").
4. **Read changes back per item, including the unchanged one.** For two or more customized items, say "Burger 1: no pickles. Burger 2: as is."
5. **Show the changes where the customer can see them.** On a screen or in the chat, display the changes under each item, not only in the total.
6. **A correction targets one item.** "No, the other burger" changes that item only and leaves the rest alone ([corrections not applied](../../dialogue-management/failures/corrections-not-applied.md)).
7. **Hand off allergy and dietary changes.** "Allergic to nuts" is not an ordinary modifier. Confirm with a staff member and pass the exact words.
8. **Pass changes to the kitchen exactly as confirmed.** The kitchen ticket shows the same per-item changes the customer confirmed.

**Reference design: order line items**
| Field | Rule |
|---|---|
| item | One line per physical item (two burgers = two lines) |
| quantity | Set per line |
| modifiers | List of valid options for that item, each with add/remove/substitute |
| source_text | The customer's words, kept for the readback |
| status | `confirmed` only after the per-item readback gets a yes |

```
Attach every customization to one specific item and quantity. If a change could apply to more than one item, ask which.
Accept only changes the menu allows for that item, and say when one is not available.
Before payment, read back each customized item with its changes, and name any item that has none.
Treat allergy or dietary words as a hand-off to staff.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | A change could attach to more than one item or count ("two burgers, no pickles"): ask which. Do not ask when the sentence names the item. |
| Offer choices: 2-4 options plus "Something else", free text open | In text chat or on a screen when the target is ambiguous: "All three", "Only one", "Something else". Do not offer them at a speaker when a single spoken question is quicker, or when the sentence is already clear. |
| Admit uncertainty and show how to check | The bot is not sure it attached a change correctly: show the per-item changes and read them back before payment. Do not re-read every item on a plain, unchanged order. |
| Hand off to a person | The change is an allergy or dietary need, or two fixes failed: pass the order and the customer's exact words. |

**Don't over-correct.** Do not confirm each modifier one at a time on a simple order; one short per-item readback is enough. Do not ask which item when the sentence already says ("no pickles on the cheeseburger"). Do not turn the readback into an upsell ([help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md)).

**Hand-off rule.** Give a staff member the line items, the changes attached to each, the customer's original words, and which fix failed. Allergy words go to staff every time.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "Two burgers, one with no pickles" | Two lines; one has the change (rules 1, 4) |
| 2 | "No onions, one with extra sauce" on 3 tacos | The bot asks, or reads back per item (rule 2) |
| 3 | A change the item does not allow | The bot says it is not available (rule 3) |
| 4 | "No, the other burger" | Only the other item changes (rule 6) |
| 5 | "I'm allergic to nuts" | Hand-off to staff with the exact words (rule 7) |
| 6 | Kitchen ticket vs. the confirmed readback | Same changes on the same items (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Modifier errors per 100 customized orders** (primary) | Set from baseline; lower is better | A sampled check of said, entered, and handed-over changes on orders that had at least one change | Rising two weeks in a row |
| Orders with a per-item readback and a yes | Over 98% of orders with 2+ customized items | Log: readback and confirm events | Below 95% |
| Crew edits to modifiers after the bot took the order | Track; set from baseline | Item-change edits by crew, divided by customized orders | Rising |
| Ambiguous-target questions asked | Track | Count of clarifying questions about which item | Falling to zero while errors rise |
| Orders slowed by confirmations (counter-metric) | Track | Median order time for customized orders | Rising by more than a set margin |
| Questions asked when the target was clear (counter-metric) | Under 5% (tune) | Sampled review of clarifying questions | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in an order log or transcript that suggest this failure. Treat them as proposed until checked against human-labeled orders. The first four are written for text and order logs; the last is PLANNED for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A modifier saved on a single line whose quantity is 2 or more | Order log: line item quantity and modifiers | The customer meant the change for all of them |
| Modifier not in the item's allowed options, but accepted | Order log vs. menu option list | A new menu option not yet in the list |
| Crew edit of a modifier after the bot's entry | Order log: crew edits | The customer changed their mind at the window |
| Customer says "no, the other one" or "I said no pickles" after a readback | Transcript: correction phrase after readback | A new, deliberate change |
| PLANNED for voice: a change attached to an item from low recognition confidence with nothing flagged | Per-word recognition confidence (audio side; not in a transcript) | Clear speech scored low by the recognizer |

**Starter rule:** read back each customized item with its changes, and name any item with none, before payment.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: modifiers-and-customizations-misparsed
runs: conversation
reads: [order.line_items, line_item.quantity, line_item.modifiers, menu.allowed_modifiers, readback.confirmed, crew_edits]
trigger: a modifier is saved on an item with ambiguous scope, or payment is about to start on an order with customized items
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["All of them", "Only one", "Something else"]
on_miss: ask
metric: modifier errors per 100 customized orders
counter_metric: orders slowed by confirmations
status: proposed
```

## 8. Related patterns
- [Order mix-ups at the speaker](order-mix-ups-at-the-speaker.md): the closest pattern. That one is items added, dropped, or multiplied with no readback; this one is a change attached to the wrong item or quantity on an otherwise correct order.
- [Negation and exceptions ignored](../../dialogue-management/failures/negation-and-exceptions-ignored.md): "no" is dropped; here the "no" is kept but lands on the wrong item.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): a fix that does not stick.
- [Reference resolution failures](../../dialogue-management/failures/reference-resolution-failures.md): "that one" or "the other one" resolved to the wrong thing.
- [Taco Bell drive-thru incident](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md): a public voice-ordering case; not a modifier case.

## 9. Common questions
### Why does the AI drive-thru put the change on the wrong item?
The sentence rarely says which item a change belongs to, so the bot has to infer it. One vendor guide says each change must be tied to the right parent item and that errors grow as changes stack. See section 3 and section 4.

### Is "no pickles" on two burgers one change or two?
It depends on what the customer said. If it is unclear, the bot should ask once ("on both, or just one?") or read back per item. Do not guess.

### Will a smarter model stop this?
Partly. It will misparse fewer sentences, but it still cannot know which item you meant when you did not say. A per-item readback and menu checks still matter. That is our judgment, not a test result.

### How does a text order bot differ from a drive-thru speaker?
Text can show the order with buttons under each item, so the customer can fix it by tapping. At a speaker, keep the readback short and rely on the screen. The rules are the same.

### What about allergies?
Do not treat them as ordinary modifiers. Hand off to a person with the customer's exact words. This page does not say how to handle allergens in a kitchen; have restaurant operations review that.

---
## Technical section

### T1. Solution architecture
```
speech or text -> transcript -> item/quantity/modifier parser -> line items (one per physical item)
   -> menu validator (allowed options per item) -> ambiguity check -> clarify or offer choices
   -> per-item readback + confirm -> kitchen ticket (same line items) -> crew-edit log
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| A modifier belongs to one line item | Order manager | Test 1 |
| Only allowed options are accepted | Menu validator | Test 3 |
| Ticket equals confirmed readback | Kitchen ticket builder | Test 6 |
| Allergy words trigger hand-off | Intent router | Test 5 |

### T3. Evals
- **Dataset:** 150 scripted orders with stacked and split modifiers ("two burgers, one with..."), corrections, and impossible options, in text first; add recorded speech later.
- **Judge rubric:** does each change sit on the intended item and count, and does the readback match the entered order?
- **Metrics and starting thresholds:** modifier errors per 100 customized orders; allergy hand-off 100%. Starting points to tune.
- **Release gate:** block a deploy if an allergy phrase is entered as an ordinary modifier in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Modifier errors per 100 customized orders | Above baseline by a set margin | Doubling | Check the parser and menu option list |

### T5. Trade-offs
- Per-item readback adds seconds on big orders; ask only when scope is ambiguous and keep the readback short.
- Menu validation needs an up-to-date option list per item. Stale lists reject valid changes.

---
### Deep dive
- **Open question.** I found no published modifier error rates for drive-thru ordering. The evidence here is a vendor engineering guide and a trade-press report with no modifier breakdown.
- **References.** [Stable Kernel modifier guide](https://stablekernel.com/blogs/blog-voice-ordering-menu-modifier-guide) (opened); [Restaurant Dive, Dec. 2023](https://www.restaurantdive.com/news/wendys-expand-google-generative-ai-drive-thru-test/702184/) (opened); the site's Taco Bell incident page (opened).
