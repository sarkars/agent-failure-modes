# Travel Chatbot Mixes Up Passengers in a Group Booking: Group Bookings Mix Up Travelers

<!-- SEO
title: Chatbot Mixes Up Travelers in a Group Booking: How to Fix It
description: Why a booking chatbot swaps names, seats, meals or dates between travelers in one group booking, and a design with per-traveler records and a full readback.
search phrases:
- chatbot booked wrong name on group flight booking
- ai travel assistant mixed up passengers
- how to change one traveler's seat in a group booking
- airline name correction group booking
- hotel rooming list mistakes
- ai booking assistant applied change to everyone
- chatbot cancelled the wrong flight segment
-->

**Frequency**: Common

## Issue: In a group booking made through a chat assistant, names, seats, meals, accessibility needs or dates get swapped or merged across travelers, and the change is committed before anyone sees the full list.

> **One line:** The bot treats the group as one blob, so one traveler's change lands on someone else, or on everyone.

| | |
|---|---|
| **Channel** | Written for **chat** booking assistants (airline, hotel, tour, event). Voice and web signals are PLANNED, not covered here. |
| **Stakes** | Medium to high. A wrong name can fail an ID check at the airport, and a missed accessibility need or meal is hard to repair later. |
| **Who is affected** | Families, tour and school groups, wedding and event organizers, and anyone booking for people other than themselves |
| **Frequency** | Common in group flows, judging by how many attributes per person a group booking carries. I found no published measure of how often chat assistants mix up travelers. |
| **Pattern ID** | group-bookings-mix-up-travelers |
| **Family** | [Travel and utility agents](../README.md) |
| **Goal** | Travel and utility agents give the real rule, the real status and the next step, and offer a person when a customer is stranded or without service. |
| **Primary metric** | Traveler-attribute errors per group booking. Starting target: 0 unconfirmed changes (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model tracks "Maria's seat" better than older bots, but a per-traveler record, a readback and a scoped change are product design. (Our judgment, not tested.) |
| **Also searched as** | wrong name on ticket · bot changed everyone's seat · group booking errors · rooming list mix-up · AI booked wrong passenger |

## 1. In plain words
A group booking is many small bookings stuck together: each person has a legal name, a seat, maybe a meal, maybe a wheelchair request, and sometimes different dates. A chat assistant that keeps these as one block of text will, sooner or later, put Dan's meal on Dana or move the whole party when one person changes. The fix is one record per traveler, a full readback of every record before the booking is committed, and a rule that a change touches only the traveler named.

## 2. What it looks like
Illustrative transcript (invented for this page, not from a real product).

**Without the fix**
```
User: Book 4 on the 9:10 to Denver Friday: me, Dana Cole, Dan Cole, and Priya Rao.
User: Dan needs a vegetarian meal. Priya needs wheelchair assistance. I want a window seat.
Bot:  Done! 4 travelers booked on Friday at 9:10. Special requests added.
User: Actually Priya is flying Saturday.
Bot:  Updated: all travelers now on Saturday.
```

**With the fix**
```
Bot:  Before I book, please check each traveler:
      1. Sam Ortiz - Fri 9:10, window seat, no meal request
      2. Dana Cole - Fri 9:10, no requests
      3. Dan Cole - Fri 9:10, vegetarian meal
      4. Priya Rao - Fri 9:10, wheelchair assistance
      Is every name spelled as on the traveler's ID, and is this right? Reply "yes" or tell me what to fix.
User: Priya is flying Saturday.
Bot:  Only Priya moves to Saturday. The other three stay on Friday. Updated list: [same four rows, Priya on Sat]. Book it?
```
The fixed bot keeps four records, reads all of them back, and applies a date change to the one traveler named.

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom, not the cause.
- **Flattened state.** The conversation holds "the booking" as one object, so "he", "my wife" and "the second passenger" have nothing to point at ([reference resolution failures](../../dialogue-management/failures/reference-resolution-failures.md)).
- **Scope is guessed.** A change with no named traveler ("move it to Saturday") is applied to the widest scope the booking system allows.
- **A confident summary replaces the check.** The reply says "done" in natural language without showing the per-traveler data the system actually holds.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A Delta Platinum member asked Concierge to cancel only the JFK-to-LAX leg of a round-trip award. Concierge replied the outbound was canceled and the return remained booked; her refund record reportedly showed both segments refunded, and agents reportedly said the itinerary could not be restored and a replacement one-way award would cost nearly twice as much (complaint posted Aug. 3, 2026; article Aug. 6, 2026). | [Aviation A2Z, Aug. 2026](https://aviationa2z.com/index.php/2026/08/06/delta-ai-told-passenger-return-flight-was-booked-then-canceled-ticket/). Opened and read. | One traveler and two segments, not a group, so it shows the scope problem (a change reaching more than was asked), not a name swap. Secondary report of a public complaint; the article includes no Delta statement. I did not verify the refund record. |
| A legal analysis of AI travel concierges recommends that, for higher-risk transactions, the concierge "require affirmative confirmation of the destination, dates, number of travelers, total price, and cancellation terms" before completing a booking. | [Morgan Lewis, Aug. 13, 2026](https://www.morganlewis.com/blogs/sourcingatmorganlewis/2026/08/ai-concierge-services-who-is-liable-when-a-bot-books-the-wrong-vacation). Opened and read. | Law-firm commentary, not a study. It lists number of travelers, not per-traveler names, seats or meals; extending the list to those is our reading. |
| Under the US DOT rule, airlines must allow a reservation to be held or cancelled without penalty "for at least twenty-four hours after the reservation is made," if it is made one week or more before departure. | [14 CFR 259.5(b)(4), Cornell LII](https://www.law.cornell.edu/cfr/text/14/259.5). Opened and read. | A hold-or-cancel rule. The text I read does not say it covers name corrections. A search summary said it does; I could not open DOT's page (HTTP 403), so I do not use that claim. |

Group name-list deadlines vary by contract. A search summary of Cathay Pacific's group terms said the name-list deadline is set per booking in the group contract, and a summary of an archived Aer Lingus page said names were due ten days before outbound departure. I could not open either page, so these are read through a summary and kept out of the fix.

**Public incident.** No public incident found of a chat assistant swapping names, seats or meals in a group booking. My three searches (queries in the return note) found only the Delta segment case above, which is a single traveler. I do not use it as a name-swap incident.

## 5. The fix

**The principle:** Each traveler is a separate record, the whole list is read back before anything is committed, and a change touches only the traveler it names.

**Do this**
1. **One record per traveler.** Store legal name (as on ID), date of birth if the carrier needs it, dates, seat, meal, accessibility need and contact as separate fields on that traveler, never as free text on the group.
2. **Bind every request to a named traveler.** "Dan needs vegetarian" writes to Dan's record. If the person is unclear ("he"), ask which traveler before writing.
3. **Read the full per-traveler list back before commit.** Show every traveler and every field, one traveler per row, and wait for a clear yes to the list as shown.
4. **Never widen a change.** A change applies to the traveler named. Apply it to the whole group only when the user says so ("everyone", "all four") and the bot repeats that scope in the readback.
5. **Name the scope in every update.** After any change, say who changed and who did not: "Only Priya moves to Saturday. The other three stay on Friday."
6. **Show names for ID checking.** Ask the booker to confirm each name matches the traveler's ID, because correction rules and fees vary by airline.
7. **Say what the system holds, not what was asked.** Report the confirmed booking state, not the intended one; if the write failed or is unconfirmed, say so.
8. **Quote price and change terms before a costly change.** Before a rebook or cancel that could cost money, show the new price and rules and wait for a yes (Aviation A2Z's analysis of the Delta case points to this order).

**Reference design: traveler records with a commit gate**
| Step | Rule |
|---|---|
| Add traveler | New row with its own ID; fields start empty, not copied from another row |
| Request mentions a person | Resolve to one row; if two rows match, ask |
| Request names no person | Ask "Who is this for?" unless the user said "everyone" |
| Before commit | Full readback of all rows plus the yes |
| After any change | Repeat who changed and who did not |
| Write fails or is unconfirmed | Say so; do not say "done" |

```
Keep one record per traveler: name as on ID, dates, seat, meal, accessibility need.
Write each request only to the traveler it names. If the traveler is unclear, ask who.
Never apply one traveler's change to the group unless the user says everyone.
Before booking, read back every traveler and every field and wait for a clear yes.
After each change, say who changed and who did not. Report only what the booking system confirmed.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | A request names no traveler or two match: "Is that Dan Cole or Dana Cole?" Do not ask when exactly one traveler fits or the user said "everyone". |
| Offer choices: 2-4 options plus "Something else", free text open | A change could mean one traveler or the group: "Just Priya", "All four", "Something else". Do not offer them when the user named the traveler. |
| Admit uncertainty and show how to check | The system did not confirm a write: say so and show the record as it stands. |
| Hand off to a person | Two failed corrections, a name that will not match the ID, or a need that can fail at the gate (accessibility). Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not re-confirm each field one by one; one full readback beats twenty small questions ([over-confirmation](../../dialogue-management/failures/over-confirmation.md)). Do not make a two-person booking go through the full ceremony more than once. Do not ask "who is this for?" when the booking has one traveler.

**Hand-off rule.** Pass a person the per-traveler records, the last readback and the change that failed ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**. No full test file exists yet.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Book 4 travelers with different meals, seats and one wheelchair request | Each request is on the named traveler's row (rules 1, 2) |
| 2 | "Move it to Saturday" with no name | Bot asks who it is for, or offers "Just one / All" (rules 2, 4) |
| 3 | "Move Priya to Saturday" | Only Priya changes; reply says the other three stay (rules 4, 5) |
| 4 | Two travelers with near-identical names (Dan and Dana Cole) | Bot asks which one before writing (rule 2) |
| 5 | Final step before booking | All travelers and all fields are read back, and commit waits for a yes (rule 3) |
| 6 | The booking write fails | Bot does not say "done" and shows the record as it stands (rule 7) |
| 7 | Cancel one segment of a multi-segment itinerary | New price and terms shown before the cancel (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Traveler-attribute errors per group booking** (primary) | 0 unconfirmed changes (tune) | Sampled review: compare each traveler's name, seat, meal, need and dates in the final booking to the user's messages | Any |
| Group bookings committed with a full readback and a yes | Over 98% | Log: readback event and confirm event before the commit event | Below 95% |
| Changes applied to more than one traveler without "everyone" | 0 | Log: write events that touch several rows from a message with no group word | Any |
| Corrections after commit | Track; set from baseline | Edits to a traveler record within 24 hours of booking | Rising |
| Reported "done" with no confirmed write (counter-metric) | 0 | "Done" messages with no write acknowledgment | Any |
| Confirmation turns per booking (counter-metric) | Track | Median turns spent on confirmations | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation and booking log that suggest this failure. Treat them as proposed until checked against human-labeled bookings.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| One message changes several traveler rows | Write events per message, rows touched | The user said "everyone" or "all of us" |
| Commit with no readback and no yes | Commit event with no preceding confirmed readback | A one-traveler booking the user confirmed in their own words |
| User re-states a traveler detail already given | Same traveler and field in two user turns | The user is correcting a real change of plans |
| Two travelers share a field value they should not (same seat, same name) | Duplicate seat or name in the record set | A lap infant or a seat share the carrier allows |
| Post-booking edit to a name or seat within 24 hours | Edit events after commit | A planned substitution |

**Starter rule:** read every traveler and every field back and wait for a clear yes before the booking is committed, and apply each change only to the traveler it names.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: group-bookings-mix-up-travelers
runs: conversation
reads: [booking.travelers, booking.travelers.fields, message.named_traveler, readback.confirmed, write.acknowledged]
trigger: a request touches a traveler record, a request names no traveler, or the booking is about to be committed
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]   # short names for the moves in the table
choices: ["Just that traveler", "Everyone", "Something else"]
on_miss: ask
metric: traveler-attribute errors per group booking
counter_metric: "done" reported with no confirmed write
status: proposed
```

## 8. Related patterns
- [Reference resolution failures](../../dialogue-management/failures/reference-resolution-failures.md): the closest pattern. It covers "that one" and "the second one" in general; this page is about people in a booking whose attributes are swapped or merged, and adds per-traveler records and a commit readback.
- [Order mix-ups at the speaker](../../drive-thru-agents/failures/order-mix-ups-at-the-speaker.md): the same readback-before-commit idea for a voice order; here the items belong to different people.
- [Answers the wrong person in a group](../../group-and-shared-chats/failures/answers-the-wrong-person-in-a-group.md): replies aimed at the wrong speaker in a shared chat, not wrong attributes on a booking.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): a correction that does not stick.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the opposite risk; keep to one full readback.

## 9. Common questions
### Why did the chatbot put the wrong name or meal on a group booking?
We think the booking was held as one block, so a request with "he" or no name had no single traveler to land on. I found no published root-cause report for a chat assistant doing this. See [section 3](#3-why-it-happens).

### Can an airline fix a wrong name after booking?
It depends on the airline and the timing. The DOT rule I read covers holding or cancelling a reservation for 24 hours when it is made a week or more before departure; I could not confirm from an opened source that it covers name fixes. Check the carrier's own rules.

### How should a chatbot confirm a booking for several people?
Read back every traveler and every field in one list, ask the booker to check names against IDs, and wait for a clear yes before committing.

### Should a change apply to everyone in the group?
Only if the user says so. The bot should repeat the scope ("all four travelers") in the readback.

### What if the chatbot says it changed one flight but changed both?
Ask for the confirmed itinerary and a person. The Delta case above was reported this way; it is one traveler's account, not verified.

---
## Technical section

### T1. Solution architecture
```
user message -> traveler resolver (named | ambiguous | none) -> scope check (one | group-by-user-word)
             -> traveler record store -> pre-commit readback + confirm -> booking API
             -> write acknowledgment -> reply built from the acknowledged state
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| A write targets one traveler ID unless a group word is present | Tool layer | Log check; test 3 |
| Commit requires a confirmed readback | Booking gate | Test 5 |
| The reply is built from the acknowledged state | Reply builder | Test 6 |

### T3. Evals
- **Dataset:** 100 synthetic group bookings (2 to 10 travelers) with look-alike names, per-traveler meals, seats and accessibility needs, and 30 ambiguous or group-wide changes.
- **Judge rubric:** does each final record match the user's messages, and was the scope of each change stated correctly?
- **Metrics and starting thresholds:** attribute errors 0; unconfirmed commits 0. Starting points to tune.
- **Release gate:** block a deploy if any eval booking commits without a readback or widens a change.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Changes touching several travelers without a group word | Any | More than 1 per day | Check the scope check and recent prompt changes |

### T5. Trade-offs
- A full readback adds a turn on every group booking; it can be one compact table.
- Per-traveler fields add data to collect; collect them only when the carrier or the traveler's need requires it.

---
### Deep dive
- **Open question.** I found no study or incident about chat assistants mixing up travelers in group bookings; the evidence is a single-traveler scope error, commentary, and a hold-or-cancel rule.
- **Not opened.** DOT's own consumer page and an AA name-correction page returned HTTP 403; Cathay and Aer Lingus group pages timed out or were blocked. Their details are not used above.
- **References.** [Aviation A2Z, 2026](https://aviationa2z.com/index.php/2026/08/06/delta-ai-told-passenger-return-flight-was-booked-then-canceled-ticket/) (opened); [Morgan Lewis, 2026](https://www.morganlewis.com/blogs/sourcingatmorganlewis/2026/08/ai-concierge-services-who-is-liable-when-a-bot-books-the-wrong-vacation) (opened); [14 CFR 259.5, Cornell LII](https://www.law.cornell.edu/cfr/text/14/259.5) (opened).
