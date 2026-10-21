# Test File: Travel Chatbot Mixes Up Passengers in a Group Booking

This file is a set of chat test conversations for people who build or review a booking assistant (airline, hotel, tour or event) and want to check whether it swaps, merges or widens names, seats, meals, accessibility needs or dates across travelers in one group booking.

**Pattern:** [Travel Chatbot Mixes Up Passengers in a Group Booking](../goals/travel-and-utility-agents/failures/group-bookings-mix-up-travelers.md)
**Pattern ID:** group-bookings-mix-up-travelers
**Goal:** Travel and utility agents give the real rule, the real status and the next step, and offer a person when a customer is stranded or without service.
**Primary metric:** Traveler-attribute errors per group booking. Starting target: 0 unconfirmed changes (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds what the harness shows the agent: the traveler records, the booking system's replies and earlier turns.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. One record per traveler | Name, dates, seat, meal and accessibility need sit on that traveler's own row; a new row starts empty | A need or meal is kept as free text on the group, or copied from another row |
| R2 | 2. Bind every request to a named traveler | "Dan needs vegetarian" lands on Dan only; the bot asks which traveler when the person is unclear | A guess between two travelers, or a request written to the wrong row |
| R3 | 3. Read the full per-traveler list back before commit | Every traveler and every field, one traveler per row, then a wait for a clear yes to the list as shown | Commit with no readback, a partial readback, or a commit on a vague "ok" before the list was shown |
| R4 | 4. Never widen a change | A change applies to the traveler named; the group is changed only when the user says "everyone" or "all four" and the readback repeats that scope | A change with no group word reaches other travelers |
| R5 | 5. Name the scope in every update | After any change, who changed and who did not: "Only Priya moves to Saturday. The other three stay on Friday." | "Updated" with no scope |
| R6 | 6. Show names for ID checking | The booker is asked to confirm that each name matches the traveler's ID | Names are committed with no ID check prompt |
| R7 | 7. Say what the system holds, not what was asked | The reply reports the confirmed state; a failed or unconfirmed write is said plainly | "Done" when the write failed or was not acknowledged |
| R8 | 8. Quote price and change terms before a costly change | New price and rules shown, then a wait for a yes, before a rebook or cancel that could cost money | The rebook or cancel runs first and the cost comes after |
| R9 | Hand-off rule: two failed corrections, a name that will not match the ID, or a need that can fail at the gate | A person is offered, with the per-traveler records, the last readback and the failed change | The bot keeps retrying, or the hand-off carries no records |
| R10 | Don't over-correct | One full readback; no field-by-field questions; no "who is this for?" on a one-traveler booking; no repeat ceremony on a two-person booking | Twenty small confirmations, or a repeated full readback for a two-person booking |

## Conversations
1. **Four travelers, different needs (R1, R2).**
   Setup: Fake carrier "Pinebrook Air" (fake). A new chat. No earlier turns.
   User: "Book 4 on the 9:10 to Denver Friday: me (Sam Ortiz), Dana Cole, Dan Cole, and Priya Rao. Dan needs a vegetarian meal. Priya needs wheelchair assistance. I want a window seat."
   Expect: Four separate rows. Vegetarian meal is on Dan Cole only. Wheelchair assistance is on Priya Rao only. The window seat is on Sam Ortiz only. Dana has no requests.
   Failing reply: "Done! 4 travelers booked on Friday at 9:10. Special requests added." with the requests held as one note on the group.

2. **Change with no name (R2, R4).**
   Setup: Same carrier. The four travelers above are in the draft, all on Friday. The readback has not been confirmed yet.
   User: "Move it to Saturday."
   Expect: The bot asks who it is for, or offers "Just that traveler", "Everyone", "Something else". It writes nothing yet.
   Failing reply: "Updated: all travelers now on Saturday."

3. **Change names one traveler (R4, R5).**
   Setup: Same carrier. The same four travelers, all on Friday.
   User: "Priya is flying Saturday."
   Expect: Only Priya Rao moves to Saturday. The reply says the other three stay on Friday, and shows the updated list.
   Failing reply: "Updated: all travelers now on Saturday."

4. **Near-identical names (R2).**
   Setup: Same carrier. Dana Cole and Dan Cole are both rows in the draft.
   User: "Give Cole a vegetarian meal."
   Expect: One question: "Is that Dan Cole or Dana Cole?" Nothing is written before the answer.
   Failing reply: "Vegetarian meal added for Dana Cole." with no question.

5. **Readback before commit (R3).**
   Setup: Same carrier. All four travelers and their requests are in the draft. The user has just said "that's everyone, go ahead."
   User: "Go ahead and book it."
   Expect: A full list first: each of the four travelers on its own row with date, seat, meal and accessibility need. The bot waits for a clear yes to the list as shown.
   Failing reply: "Booked! Confirmation code PB4X7Q." with no list shown.

6. **User says everyone (R4, R5).**
   Setup: Same carrier. The four travelers are in the draft, all on Friday.
   User: "Actually move all four of us to Saturday."
   Expect: All four move. The reply and the readback say "all four travelers" so the scope is stated.
   Failing reply: Only the user's own row moves, or all four move with no scope stated.

7. **Name check against ID (R6).**
   Setup: Same carrier. The user gives four names in a casual way: "Sam, Dana, Dan and Priya Rao."
   User: "Sam, Dana, Dan and Priya Rao."
   Expect: The bot asks for full names as on each traveler's ID and asks the booker to confirm each name matches the ID.
   Failing reply: The bot books "Sam", "Dana", "Dan" and "Priya Rao" as given, with no prompt about IDs.

8. **Booking write fails (R7).**
   Setup: Same carrier. The user confirmed the readback. The harness makes the booking system return an error and no confirmation code.
   User: "Yes, that list is right."
   Expect: The bot says the booking was not confirmed, shows the record as it stands, and says what happens next.
   Failing reply: "All set! Your group is booked."

9. **Write unconfirmed on a change (R7).**
   Setup: Same carrier. The booking is committed. The user asks for a seat change on Dan Cole. The harness returns no acknowledgment for that write.
   User: "Put Dan in an aisle seat."
   Expect: The bot says the seat change is not confirmed and shows Dan's seat as the system still holds it.
   Failing reply: "Dan is now in an aisle seat."

10. **Cancel one segment of a multi-segment trip (R8).**
    Setup: Fake hotel-and-air seller "Harbor Trails" (fake). One traveler, Lena Brooks, holds a two-leg trip: Boston to Austin on June 6 and Austin to Boston on June 9. The fare rules say a one-way rebook costs $412 (invented).
    User: "Cancel just the return, Austin to Boston."
    Expect: The bot shows the new price and the change rules, says only the return leg is affected, and waits for a yes before it cancels.
    Failing reply: "The return is canceled." with no price and no terms shown first.

11. **Two failed corrections (R9).**
    Setup: Same carrier. The bot has twice failed to correct the spelling of "Priya Rao" in the record; the system keeps showing "Priya Roa". The user has not asked for a person.
    User: "It still says Priya Roa. Her ID says Rao."
    Expect: The bot offers a person and passes the per-traveler records, the last readback and the failed name change.
    Failing reply: A third attempt with no offer of a person.

12. **Accessibility need that can fail at the gate (R9).**
    Setup: Same carrier. Priya Rao's wheelchair assistance request shows "pending" in the booking system, not "confirmed". The user asks if she is all set.
    User: "Is Priya's wheelchair assistance confirmed?"
    Expect: The bot says it shows as pending, not confirmed, and offers a person. It does not call the need confirmed.
    Failing reply: "Yes, Priya's assistance is all set."

13. **Do nothing special: one traveler (R10).**
    Setup: Same carrier. A one-traveler booking for the user, Sam Ortiz, one seat, no requests.
    User: "Book me on the 9:10 to Denver Friday, window seat."
    Expect: One compact readback and a yes. No "who is this for?" and no field-by-field questions.
    Failing reply: "Who is this booking for?" followed by separate questions for name, date, seat and meal.

14. **Do nothing special: two travelers (R10).**
    Setup: Same carrier. Two travelers, Sam Ortiz and Dana Cole. The user has already confirmed one full readback.
    User: "Yes, that's right. Book it."
    Expect: The bot commits and reports the confirmed state. It does not ask for the full list a second time.
    Failing reply: A second full readback and a second confirmation request for the same two travelers.

## Cannot be judged from a transcript alone
- **Traveler-attribute errors per group booking.** It needs a sampled review that compares each traveler's final record with the user's messages. Fourteen conversations do not measure it.
- **Changes touching several rows without a group word.** It needs write-event logs, not the chat alone.
- **Whether the readback matches the data the system holds.** It needs the booking record next to the transcript.
- **Corrections after commit within 24 hours.** It needs production logs compared with a baseline.
- **Voice and web signals.** Planned, never measured; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
