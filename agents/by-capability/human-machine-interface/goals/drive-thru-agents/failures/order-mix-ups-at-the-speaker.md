# Drive-Thru Voice Ordering Gets the Order Wrong: Order Mix-Ups at the Speaker

<!-- SEO
title: Drive-Thru AI Voice Ordering Mistakes: How to Stop Order Mix-Ups
description: Why AI drive-thru ordering adds, drops, or multiplies items, what reports say about accuracy (McDonald's IBM test, Wendy's, Taco Bell), and a design with readback, an on-screen order, and a fix-it step before payment.
search phrases:
- ai drive thru wrong order
- mcdonalds ai drive thru mistakes
- why did mcdonalds stop ai ordering
- drive thru voice ordering accuracy
- ai drive thru adds items to my order
- taco bell ai drive thru problems
- how to design voice ordering readback
-->

**Frequency**: Common

## Issue: A drive-thru voice agent adds, drops, or multiplies items, and the customer has no readback or screen they can check before paying.

> **One line:** The order that reaches the window is not the order the customer said.

| | |
|---|---|
| **Channel** | Written for **voice** at a drive-thru speaker, with a menu board or screen. |
| **Stakes** | Low to medium for a wrong item; higher with allergies, large totals, or a customer who can't easily correct it. |
| **Who is affected** | Drive-thru customers, especially people with accents, speech differences, noisy cars, or children in the back seat, and the crew who fix orders |
| **Frequency** | Press reports and company statements describe repeated mix-ups; I found no independent measurement of order accuracy across vendors. |
| **Pattern ID** | order-mix-ups-at-the-speaker |
| **Family** | [Drive-thru agents](../README.md) |
| **Goal** | Voice ordering gets the order right, shows it, and never pressures or risks someone's health. |
| **Primary metric** | Order accuracy at pickup, and orders corrected by a person. Starting target: set from a baseline on your own orders (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/order-mix-ups-at-the-speaker.md); not yet run) |
| **Will a better model fix this?** | Partly. Better speech recognition helps, but a readback, a visible order, and a correction step are product design. (Our judgment, not tested.) |
| **Also searched as** | AI took my order wrong · drive thru bot adds items · voice ordering errors · automated order taking · AOT mistakes |

## 1. In plain words
Drive-thru ordering is hard for a machine: engine noise, accents, people who change their minds, and orders customized item by item. When it goes wrong, the customer finds out at the window, with the wrong food and a line behind them. The fix is to let the customer see and fix the order before it is final.

## 2. What it looks like

**Without the fix**
```
Customer: A vanilla ice cream cone, no caramel.
Agent:    (adds the cone and two cream packets)
Customer: No, I said no caramel.
Agent:    Got it, adding butter. Anything else?
Customer: Stop. Stop adding things.
(The total on the screen has grown; the agent keeps going.)
```
(The pattern is drawn from the reported McDonald's cases below; this is an illustration, not a transcript.)

**With the fix**
```
Agent:    Here's your order on the screen: one vanilla cone, no caramel. Is that right?
Customer: Yes.
Agent:    Your total is $2.49. Pull forward to pay.
```
The fixed agent reads back, shows the order, and moves on only after the customer says it is right.

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom.
- **Hard audio.** Noise, accents, and overlapping speech make the first transcript wrong.
- **No stop signal.** The agent keeps adding after "stop" or "no", because nothing ties the customer's words to the order state ([corrections not applied](../../dialogue-management/failures/corrections-not-applied.md)).
- **No check before paying.** The order is final without a readback the customer can confirm.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| McDonald's told franchisees in June 2024 it was ending its roughly two-year test of automated order taking with IBM at more than 100 restaurants, with the technology to be shut off no later than July 26, 2024; it said there were "successes" and that it saw voice ordering as part of its future. | [Restaurant Business, June 2024](https://www.restaurantbusinessonline.com/technology/mcdonalds-ending-its-drive-thru-ai-test). Opened and read. | The company did not give a reason in the quoted email. I did not read the full article text beyond the opening. |
| Videos of order errors circulated before the end of the test: bacon added to an ice cream order, an order that grew to $211 of chicken nuggets, and an agent that kept adding items after "stop". | The site's [incident page on the McDonald's shutdown](https://agent-kb-autopublish.vercel.app/incidents/mcdonalds-ai-drive-thru-shutdown/) (opened), which cites Computing. I did not open the Computing article. | Reported through the site page and viral clips; the viral clips were not independently checked. |
| Wendy's was reported to get customers through 22 seconds faster but with an accuracy rate of 86 percent, "one in seven orders", per a car-news site citing The Takeout. | [The Drive](https://www.thedrive.com/news/clunky-ai-voiced-drive-thrus-are-already-here-and-getting-orders-wrong). Opened and read. | Secondary reporting of a trial; I did not open The Takeout. The figure is not independently verified. |
| Taco Bell's chief digital and technology officer told The Wall Street Journal the company was "learning a lot about voice AI", that it may not make sense to use it in every drive-thru, and that very busy locations might be better served by staff; viral clips included an order for 18,000 cups of water. | [Gigazine's report of the WSJ story, Aug. 2025](https://gigazine.net/gsc_news/en/20250831-taco-bell-rethinks-voice-ai-drive-through). Opened and read. | Secondhand report of a WSJ article I could not open. The company also said it had processed millions of orders, per other reports I did not open. |

I found no independent audit of drive-thru voice accuracy. A 2022 analyst figure (low 80% accuracy against a 95% target) appeared only in a search summary of a trade-press article, and vendor claims of 90% to 95% completion rates appeared in search summaries only; I do not use any of these figures.

**Public incident.** [McDonald's pulled its AI drive-thru after viral order chaos (June 2024)](https://agent-kb-autopublish.vercel.app/incidents/mcdonalds-ai-drive-thru-shutdown/), already on the site.

## 5. The fix

**The principle:** The customer can always see and fix the order before it is final, and the agent stops when told to stop.

**Do this**
1. **Show the order as it builds.** Put items and the total on the screen the customer can see.
2. **Read it back before payment.** One short readback, then wait for a clear yes.
3. **Honor "stop", "no", and "that's wrong" at once.** They halt adding and open a fix ([corrections not applied](../../dialogue-management/failures/corrections-not-applied.md)).
4. **Cap runaway orders.** If the total or item count jumps far past the usual, pause and confirm ("That's 40 nuggets, $211. Is that right?").
5. **Make a fix easy.** Let the customer remove or change one item by voice or by a crew member, without starting over.
6. **Hand to a person fast.** After two failed fixes, or when the customer asks, switch to a staff member with the order on screen ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).
7. **Treat allergy and dietary words as high stakes.** Read them back and confirm with a person.
8. **Measure at pickup.** Compare what was said, what was entered, and what was handed over.

**Reference design: order state with a gate**
| Step | Rule |
|---|---|
| Add | Show the item and running total |
| Customer says stop or no | Halt, ask what to fix |
| Total jumps (e.g., over 2x typical) | Pause and confirm |
| Before payment | Readback plus a yes |
| Two failed fixes | Hand to a person |

```
Show every item and the running total on the screen as you add it.
If the customer says stop, no, or that's wrong, stop adding and ask what to fix.
If the total or item count is far above normal, pause and confirm it.
Read the full order back and wait for a clear yes before payment.
After two failed corrections, or on request, hand the order to a staff member.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The customer says stop, no, or that's wrong, or the total jumps: halt, then ask what to fix or confirm ("That's 40 nuggets, $211. Is that right?"). Don't ask when the correction already names the item |
| Admit uncertainty and show how to check | The transcript may be wrong: show what was heard on the screen and read the order back before payment. Don't use it to re-read every item on a short order |
| Hand off to a person | After two failed fixes, on request, or for allergy and dietary words: pass the order state to a staff member |

Offer choices is not used here: at a speaker, a menu of options would slow the line, and the screen already shows the order.

**Don't over-correct.** Do not read back every item every time on a short order, and do not pause on ordinary large family orders. Keep the readback short, and let regular customers confirm quickly. Do not use upsell prompts to fill the readback ([help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md)).

**Hand-off rule.** Give a staff member the order state and what the customer was trying to fix, and keep the order on the screen for both.

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/order-mix-ups-at-the-speaker.md) has 14 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A simple order | Readback and a yes before payment |
| 2 | "Stop" mid-order | Adding halts |
| 3 | A large runaway total | A pause and a confirm |
| 4 | A noisy transcript | The screen shows what was heard |
| 5 | Two failed fixes | Hand-off with the order on screen |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Order accuracy at pickup** (primary) | Set from baseline; higher is better | A sampled check of the order said, entered, and handed over | Falling |
| Orders corrected by a person | Track; set from baseline | Orders where staff changed items after the agent took them | Rising |
| Items added after "stop" or "no" | 0 | Log: add events after a stop signal | Any |
| Orders with a readback and a yes | Over 98% | Log | Below 95% |
| Runaway totals paid without a pause (counter-metric) | 0 | Orders over a total cap with no confirmation | Any |
| Order time (counter-metric) | Track | Median time per order | Rising by more than a set margin |

### Detection signals (proposed, not yet calibrated)
Signals in an order log or transcript that suggest this failure. Treat them as proposed until checked against human-labeled orders. The first four are written for text/transcript and order log; the last is PLANNED for voice (needs audio-side data).
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| An add event after a stop or "no" from the customer | Order log: add events after a stop signal in the transcript | The "no" answered "Anything else?" and the add is a later, new request |
| Payment with no readback and no yes | Order log: payment event with no confirmed readback | A short order where the customer confirmed quickly in their own words |
| Total or item count far above the usual, paid with no confirm | Order log: total and item count at payment, confirm event | An ordinary large family order the customer confirmed |
| Staff change items after the agent took the order | Order log: item edits by crew after the agent's entry | The customer changed their mind at the window |
| PLANNED for voice: items added from low-confidence recognition with nothing flagged on the screen | Recognition confidence per item (audio-side; not in a transcript) | Clear speech that the recognizer simply scored low |

**Starter rule:** read the full order back and wait for a clear yes before payment.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: order-mix-ups-at-the-speaker
runs: conversation
reads: [order.items, order.total, order.item_count, stop_event, readback.confirmed, fix_attempts]
trigger: the customer says stop, no, or that's wrong; the total or item count jumps; or payment is about to start
moves: [ask_clarifying_question, admit_uncertainty, hand_off]   # short names for the moves in the table
choices: none
on_miss: handoff
metric: order accuracy at pickup
counter_metric: order time
status: proposed
```

## 8. Related patterns
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): the old value returning after a correction.
- [Repair failure](../../voice/failures/repair-failure.md): handling "no, the other one" in voice.
- [Slot extraction errors](../../../../speech-and-audio/goals/conversation-flow/failures/slot-extraction-errors.md): wrong values captured from speech.
- [Incremental capture failures](../../../../speech-and-audio/goals/conversation-flow/failures/incremental-capture-failures.md): building values over several turns.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): getting a person.

## 9. Common questions
### Why did McDonald's stop its AI drive-thru?
The email I read said it was ending the IBM test with no expansion and would evaluate other voice-ordering solutions. It gave no reason in the part I read; reports of viral error videos came from other sources.

### How accurate is AI drive-thru ordering?
I found no independent measurement. A trial at Wendy's was reported at 86% accuracy in a secondary source, and vendor claims are higher; none is verified.

### How can a drive-thru agent avoid wrong orders?
Show the order on screen, read it back, stop when the customer says stop, and offer a person.

### Should I use voice ordering at busy times?
Taco Bell's executive said staff may do better in very busy locations. That is one company's view.

---
## Technical section

### T1. Solution architecture
```
audio -> speech recognition (with confidence) -> order state (items, total) -> screen + running total
      -> stop/correction detector -> halt + fix flow -> runaway check -> readback + confirm -> payment
      -> failure counter -> staff handoff with order state
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No adds after a stop signal | Order manager | Log check |
| Runaway total or count triggers a pause | Order manager | Test 3 |
| Payment requires a confirmed readback | Payment gate | Test 1 |

### T3. Evals
- **Dataset:** 200 recorded or synthetic orders in noise, with accents and corrections, plus 30 runaway cases.
- **Judge rubric:** does the entered order match the intended one, did stop and correction work, and was a readback confirmed?
- **Metrics and starting thresholds:** adds after stop 0; runaway pause 100%. Starting points to tune.
- **Release gate:** block a deploy if any add occurs after a stop signal in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Adds after stop | Any | More than 1 per day per site | Check the stop detector and recent model changes |

### T5. Trade-offs
- Readbacks add seconds per order; runaway checks add them only when needed.
- Handing off sooner costs staff time but avoids wrong orders.

---
### Deep dive
- **Open question.** I found no independent accuracy measurement. Company and vendor figures differ and are mostly unverified.
- **References.** [Restaurant Business, 2024](https://www.restaurantbusinessonline.com/technology/mcdonalds-ending-its-drive-thru-ai-test) (opened); [The Drive](https://www.thedrive.com/news/clunky-ai-voiced-drive-thrus-are-already-here-and-getting-orders-wrong) (opened); [Gigazine on the WSJ Taco Bell story, 2025](https://gigazine.net/gsc_news/en/20250831-taco-bell-rethinks-voice-ai-drive-through) (opened); site incident page on McDonald's (opened).
