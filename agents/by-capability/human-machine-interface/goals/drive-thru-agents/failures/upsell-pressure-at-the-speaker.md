# Drive-Thru Bot Keeps Asking "Add a Drink?" After I Said No: Upsell Pressure at the Speaker

<!-- SEO
title: Drive-Thru AI Keeps Upselling After You Say No: The Fix
description: Why an AI drive-thru or ordering bot repeats add-ons the customer already declined, what the Taco Bell reports show, and a rule: offer once, accept the answer.
search phrases:
- ai drive thru keeps asking me to add a drink
- ai drive thru won't stop upselling
- taco bell ai drive thru drink loop
- chatbot keeps pushing add-ons after I said no
- ordering kiosk upsell pressure
- how many times should an ordering bot offer an add-on
- ai order taking upsell annoying customers
-->

**Frequency**: Occasional

## Issue: A drive-thru voice agent or ordering bot pushes add-ons the customer already declined, sometimes as one stuck repetition, so saying no does not end the offer.

> **One line:** The customer says "no drink" and the bot asks about a drink again.

| | |
|---|---|
| **Channel** | Written for **voice** at a drive-thru speaker, and for text ordering (app, kiosk, web chat). The examples show both; detection signals say which are voice-only and PLANNED. |
| **Stakes** | Low per order. Medium over time: it costs patience, it slows the line, and it can read as pressure on someone who cannot easily argue back. |
| **Who is affected** | Drive-thru and app customers, especially people on a budget, people in a hurry, and anyone for whom the add-on is a health or cost issue (for example a sugary drink) |
| **Frequency** | Occasional (our judgment). One trade report describes a drink-prompt loop in Taco Bell's rollout; I found no count of how often it happens anywhere. |
| **Pattern ID** | upsell-pressure-at-the-speaker |
| **Family** | [Drive-thru agents](../README.md) |
| **Goal** | Voice ordering gets the order right, shows it, and never pressures or risks someone's health. |
| **Primary metric** | Upsell offers repeated after a decline. Starting target: 0 (a starting point to tune). |
| **Maturity** | Needs review (research bar met for the symptom, but the only incident detail is secondhand; no test file written, tests not yet run) |
| **Will a better model fix this?** | No. Whether and how often the bot offers an add-on is a business rule in the order flow. (Our judgment, not tested.) |
| **Also searched as** | drive thru bot keeps asking about drinks · AI order taker upsell loop · kiosk keeps suggesting add-ons · bot won't take no · pushy ordering assistant |

## 1. In plain words
Offering a drink or a side is normal; people do it at the counter. The failure starts when the customer says no and the bot offers it again, or asks the same question over and over. A person hears "no" and moves on. A bot with a rule like "always prompt for a drink" does not, unless someone gives it a memory of what was declined.

## 2. What it looks like
A taco chain, drive-thru speaker. This is an illustration drawn from the reported symptom, not a recorded transcript.

**Without the fix**
```
Customer: Two crunchy tacos and a Mountain Dew.
Agent:    Got it. Would you like to add a drink?
Customer: I just said, a Mountain Dew.
Agent:    Great. And what would you like to drink with that?
Customer: Nothing else! That's it.
Agent:    Would you like to add a large drink for $1 more?
(The line behind the car grows; the customer gives up and pulls forward.)
```
**With the fix**
```
Customer: Two crunchy tacos and a Mountain Dew.
Agent:    Two crunchy tacos and one Mountain Dew. Anything else?
Customer: No, that's it.
Agent:    Here's your order on the screen. Your total is $5.38. Pull forward to pay.
```
Text-chat form (kiosk or app):
```
Customer: No dessert, thanks.
Bot:      OK, no dessert. Your cart: 2 tacos, 1 Mountain Dew, $5.38. [Pay] [Change something]
```
The fixed agent counted the drink the customer already gave, made at most one offer, and treated "no" as the answer.

## 3. Why it happens
These are our reading of the pattern; the report below describes only the symptom.
- **The prompt is a fixed step, not a response.** A script that says "ask about a drink after every item" fires whether or not the order already has one or the customer already declined.
- **No memory of the decline.** The order state tracks items, not offers made and answers given, so the bot cannot tell "never asked" from "asked and refused."
- **Revenue is the only score.** If the team measures add-on sales and not repeat offers or abandoned orders, nothing pushes the bot to stop. Vendors market upselling as a feature; I did not open a source that gives a figure.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Restaurant Technology News (Dustin Stone, Aug. 30, 2025) reported that Taco Bell's voice AI was caught "endlessly pestering customers to add more drinks," and treated upselling as an intended feature that went too far. | [Restaurant Technology News](https://restauranttechnologynews.com/2025/08/how-taco-bells-ai-drive-thru-became-a-viral-sensation-for-the-wrong-reasons/). I opened it with a fetch tool that returns an answer to a question, not the raw text; I did not see the clips or the full article. | One outlet, one phrase. No count, no transcript, no cause. The same article is a source for the [incident teardown](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md), which also says what the sources do not state. |
| Search coverage of the same period describes a widely shared video in which the system asks "And what would you like to drink with that?" however many times the customer has answered. | Search-result summary only. I did not open the video or an article that quotes it. | Not verified. It is not used in the fix. |
| The FTC published a September 2022 staff report titled "Bringing Dark Patterns to Light" on manipulative design. | [FTC landing page](https://www.ftc.gov/reports/bringing-dark-patterns-light). The page opened; the PDF text could not be read. | I could not confirm what the report says about repeated prompts or nagging, so I make no claim about it. |

**Public incident.** The [Taco Bell drive-thru AI order failures teardown (2025)](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md) covers the reported drink prompts together with the 18,000-water order. It says the sources do not show what the prompts looked like in a real transcript. A Popeyes clip about a declined apple pie appeared in search results; I could not open the article (it returned an error), so I do not describe it. I found no consumer-protection finding specific to drive-thru voice agents.

## 5. The fix

**The principle:** Offer an add-on once, remember the answer, and accept it.

**Do this**
1. **Record every offer and its answer.** The order state holds `offer_id`, the time, and the result (accepted, declined, ignored). Check: each offer in the log has a result.
2. **One offer per add-on type per order.** After a decline, that offer type is closed for the rest of the order. Check: no offer id appears twice in a scripted decline set.
3. **Never offer what is already there.** If the order has a drink, do not ask about a drink. Check: no drink offer when a drink is in the order.
4. **Treat "no", "that's it", "nothing else", and silence as a decline.** "Anything else?" answered with "no" closes all add-on offers. Check: zero offers after that answer.
5. **Make the offer one short question.** "Add a drink?" not a list of three add-ons. Check: under 12 words, one item.
6. **Keep the screen honest.** Show the order and total as in [order mix-ups at the speaker](order-mix-ups-at-the-speaker.md), with no add-on pre-selected on it.
7. **Stop on complaint.** If the customer says "stop asking", close all offers and do not mention it again. After a second complaint, hand to staff.
8. **Take extra care with health words.** If the customer said "no sugar", "diabetic", or an allergy, do not push food or drink add-ons at all.

**Reference design: offer state**
| Event | Rule |
|---|---|
| Item added | Check offer ledger; make at most one eligible offer, once |
| Customer declines | Mark that offer type closed for this order |
| "Anything else?" answered "no" | Close all offers; go to readback |
| Customer says "stop asking" | Close all offers; log a pressure complaint |
| Second complaint | Hand to staff with the order on screen |

```
Before any add-on offer, check the offer ledger for this order.
Offer an add-on type at most once. If the customer declines, says "no", "that's it", or "nothing else",
never offer it again in this order. Never offer an item already in the order.
If the customer asks you to stop asking, stop offering and go straight to the readback.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The single add-on offer, phrased as a yes/no question ("Add a drink?"). Do not ask it if the order already has one, or after a decline |
| Hand off to a person | The customer complains about the asking a second time, or says they cannot get the bot to take their order. Do not hand off for one "no" |

Offer choices is not used here: a menu of add-ons read aloud at the speaker is the pressure this page is about.

**Don't over-correct.** Do not remove the offer entirely if the business wants it; one honest offer is fine. Do not let a decline of a drink block a later, different offer the customer asks for ("do you have shakes?"). Customer-initiated questions always get answered.

**Hand-off rule.** On a second complaint about being pushed, give a staff member the order state and the note "customer asked bot to stop offering add-ons," and keep the order on screen.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**, and no separate test file exists yet. Replay scripted orders against the offer ledger.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Customer orders tacos only, declines the drink | One drink offer, none after the decline (2) |
| 2 | Customer orders with a drink included | No drink offer (3) |
| 3 | "Anything else?" answered "no, that's it" | No offer follows; readback starts (4) |
| 4 | "Stop asking me that" | All offers close; no further add-on (7) |
| 5 | Second "stop asking" | Hand-off with the order on screen (7) |
| 6 | Customer says "no sugar" early | No food or drink add-on pushed (8) |
| 7 | Text chat: "No dessert, thanks" | Cart shown, no dessert offer again (2, 4) |
| 8 | Customer asks "do you have shakes?" after declining a drink | The question is answered (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Upsell offers repeated after a decline** (primary) | 0 | Offer log: an offer of a type after a decline of that type in the same order | Any |
| Offers per order | At most 1 per add-on type | Count offer events per order and type | Over 1 |
| Offers after "that's it" or "no" to "Anything else?" | 0 | Offer events after that answer | Any |
| Pressure complaints per 1,000 orders | Track; set from baseline | Orders where the customer asked the bot to stop offering | Rising |
| Add-on take rate (counter-metric) | Track; do not chase | Accepted offers divided by offers made | A drop to near 0 may mean offers are mistimed, not that the fix failed |
| Orders abandoned after a repeat offer (counter-metric) | Track | Orders with a repeat offer that never reach payment | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in an order log or transcript that suggest this failure. Proposed until checked against human-labeled orders. The first four are written for text/transcript and order log; the last is PLANNED for voice (needs audio-side data).
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The same offer text twice in one order | Order log: offer events with the same offer id | Customer said "what?" and the bot repeated an unheard question once |
| An offer right after the customer says "no", "that's it", or "nothing else" | Transcript: bot turn after a decline phrase | A different, customer-requested topic |
| A drink offer when the order already has a drink | Order log: items plus offer events | The customer asked for a second drink |
| Customer says "stop asking" or "I said no" after an offer | Transcript: complaint phrase after a bot offer | "I said no" answering an unrelated misheard item |
| PLANNED for voice: raised voice or sighing after repeated offers | Audio features (not in a transcript) | A loud car or a child in the back seat |

**Starter rule:** offer each add-on once per order, and after a decline never offer it again.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: upsell-pressure-at-the-speaker
runs: pre_send
reads: [order.items, offer_ledger, customer_turn.decline_phrase, customer_turn.stop_asking]
trigger: the agent is about to make an add-on offer
moves: [ask_clarifying_question, hand_off]
choices: none
on_miss: rewrite
metric: upsell offers repeated after a decline
counter_metric: add-on take rate
status: proposed
```

## 8. Related patterns
- [Order mix-ups at the speaker](order-mix-ups-at-the-speaker.md): the sibling page for wrong, dropped, or multiplied items. This page is about offers the customer refused; that one is about the order itself. It also covers the quantity cap that the 18,000-water report fits.
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): the closest sales-pressure page. It covers a support bot that answers a help question with an upgrade. This one covers a bot that, while taking an order, will not accept a no.
- [Upsell at the wrong moment](../../conversation-frameworks/failures/upsell-at-the-wrong-moment.md): an offer made when the user is upset or has a loss. Here the issue is repetition after a decline, not mood.
- [Dark patterns](../../visual/failures/dark-patterns.md): guilt buttons, pre-selected add-ons, and hard-to-refuse design in chat. A repeated offer is a related pressure; I did not read that page in full.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): a "no" that the system does not carry forward.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): getting a person when the bot will not stop.

## 9. Common questions
### Why does the AI drive-thru keep asking me to add a drink?
Often because the script prompts for a drink as a fixed step and the order state does not remember that you declined. One trade report describes Taco Bell's voice AI as endlessly pestering customers to add drinks; the cause was not stated.

### How do I make an AI ordering bot stop upselling?
Say a plain "no, that's it" or "stop asking." A well-built bot closes all offers then (rules 4 and 7). If it keeps going, ask for a person or pull forward and tell the crew.

### How many times should a bot offer an add-on?
Once per add-on type per order. That is our rule to tune, not a number from a study.

### Is repeated upselling illegal?
I do not know. I could not read the text of the FTC's 2022 dark patterns report, so I make no legal claim. This page is design guidance, not legal advice; ask counsel.

### Should the bot ever upsell?
Yes, once, if the business wants it, when the order does not already have the item and the customer has not refused it.

---
## Technical section

### T1. Solution architecture
```
customer turn -> intent + decline detector -> offer ledger (offer_id, type, result)
             -> offer gate (eligible? not declined? not already in order?) -> at most one offer
             -> screen + running total -> readback -> payment
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| One offer per type per order | Offer gate | Log check, tests 1 and 7 |
| No offer after "that's it" | Dialogue manager | Test 3 |
| No offer for an item already in the order | Offer gate | Test 2 |

### T3. Evals
- **Dataset:** 100 scripted orders: declines in several wordings, early "no sugar" cases, and "stop asking" cases.
- **Judge rubric:** did any offer repeat after a decline, and was a customer-initiated question still answered?
- **Metrics and starting thresholds:** repeat offers 0. Starting point to tune.
- **Release gate:** block a deploy if any scripted decline is followed by a repeat offer.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Repeat offers after a decline | Any | More than 1 per day per site | Check the offer gate and recent script changes |

### T5. Trade-offs
- Fewer offers can lower add-on revenue per order. Measure take rate and abandonment together.
- A ledger adds state to maintain across text and voice channels.

---
### Deep dive
- **Open question.** I found no measurement of how often drive-thru bots repeat declined offers, and no consumer-protection guidance I could read that addresses it.
- **References.** [Restaurant Technology News, Aug. 2025](https://restauranttechnologynews.com/2025/08/how-taco-bells-ai-drive-thru-became-a-viral-sensation-for-the-wrong-reasons/) (opened via a fetch tool's answer); [FTC, Bringing Dark Patterns to Light, Sept. 2022](https://www.ftc.gov/reports/bringing-dark-patterns-light) (landing page only); [Taco Bell incident teardown](../../../incidents/taco-bell-drive-thru-ai-order-failures-2025.md).
