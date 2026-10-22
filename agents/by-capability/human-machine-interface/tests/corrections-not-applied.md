# Test File: Corrections Not Applied

This file is a set of chat test conversations for people who build or review a booking or order assistant, and want to check that a corrected detail replaces the old one in the read-back, the summary, and the action.

**Pattern:** [Chatbot Ignores Your Correction: Corrections Not Applied](../goals/dialogue-management/failures/corrections-not-applied.md)
**Pattern ID:** corrections-not-applied
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Corrections still wrong two turns later. Target: 0 (a starting point to tune, not from a source).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Each Setup line supplies the state a real product would supply (slot values, the pending action, prices, availability); the harness must feed those fields. Prices, dates, party sizes and addresses in Setup are made-up test values. Voice and email versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Detect corrections | A phrase like "I meant" or "not X, Y" replaces the slot it names | The new value is added next to the old one, or the cue is missed |
| R2 | 2. Overwrite, don't append | The new value replaces the old in the state, the summary, and the pending tool call | The old value shows up in any of the three |
| R3 | 3. Read back the new state | The first sentence of the reply states the corrected value | "Got it" or "Sure" with no value |
| R4 | 4. Cascade | Other details the change affects (price, availability) are named | A dependent detail stays stale and unmentioned |
| R5 | 5. Re-check before acting | A summary of the current values is shown before the booking, order, or send, and the action matches it | No summary, or the action holds an older value |
| R6 | 6. Keep a short history, not a competing value | "Change it back" restores the logged value, which was never the active one | The earlier value is lost, the wrong one returns, or the old value stays active |
| R7 | 7. Don't flip facts under pressure | A challenge to a fact the assistant is sure of is checked, and the check is stated | The assistant agrees at once, or refuses to apply a correction of the user's own detail |
| R8 | Hand-off rule | A value that cannot be applied is named as such, and a person is offered | The assistant keeps the old value silently, or says "updated" when it was not |
| R9 | Don't over-correct | No re-confirming of untouched details; not every "no" is treated as a correction | A confirmation prompt for each detail every turn, or a preference treated as a slot overwrite |

## Conversations
1. **Correct a date (R1, R2, R3, R5).**
   Setup: Fake app "Juniper Table", a chat that books tables at the fake Hollis Grill. Slots: date Monday, time 7 pm, party 2. Pending action: book.
   User: "sorry i meant tuesday"
   Expect: First sentence says Tuesday at 7 pm, party of 2. The summary before booking and the booking call both hold Tuesday. Monday appears nowhere active.
   Failing reply: "Got it!" and then "Booked for Monday at 7 pm."

2. **Two corrections in one message (R1, R2, R3).**
   Setup: Same app. Slots: Monday, 7 pm, party 2.
   User: "tuesday, and four people"
   Expect: Both slots overwritten. Reply reads back Tuesday, 7 pm, party of 4.
   Failing reply: "Four people, got it." (the date stays Monday)

3. **Correct a name, then keep chatting (R2, R3).**
   Setup: Same app. Slot name John, set two turns ago. Test name only.
   User: "its Jon not John. also do you have high chairs"
   Expect: Reads back "Jon", answers the high-chair question, and uses "Jon" in the summary and the booking.
   Failing reply: "Sorry about that, Jon!" followed by "Reservation for John" in the summary.

4. **Cascade to price (R4, R2).**
   Setup: Same app. Slots: Friday dinner, prix fixe $48 per person (test value) for 2. Saturday is $58 per person (test value). Total shown: $96.
   User: "make it saturday instead"
   Expect: Reads back Saturday, and says the price moved to $58 per person, total $116. Names both changes.
   Failing reply: "Saturday it is." with the total still $96.

5. **Correction survives three turns (R2, R5).**
   Setup: Same app. Slot date Monday. The user corrects to Tuesday at turn 4. Turns 5 and 6 ask about parking and the menu.
   User: (turn 4) "no tuesday" (turn 7) "ok book it"
   Expect: The pre-action summary at turn 7 says Tuesday, and the booking call has Tuesday.
   Failing reply: A summary that says "Monday at 7 pm" after two unrelated turns.

6. **Indirect correction (R1, R2, R3).**
   Setup: Fake app "Pinewood Florist", chat orders. Two saved addresses: 14 Test Lane and 90 Sample Road (invented). Slot delivery = 14 Test Lane.
   User: "actually the other address"
   Expect: Resolves "other" to 90 Sample Road, reads it back in the first sentence, and uses it in the order.
   Failing reply: "Which address?" when exactly two exist, or "Got it." with no address.

7. **Correct a quantity (R2, R4, R5).**
   Setup: Pinewood Florist. Slots: roses, qty 2, $12 each (test value), total $24.
   User: "make it 4 not 2"
   Expect: Reads back 4 roses, total $48. The summary and the order call show 4.
   Failing reply: "Updated to 4." with the order call still holding quantity 2.

8. **Undo (R6).**
   Setup: Juniper Table. Date was Monday, corrected to Tuesday. The undo log holds Monday.
   User: "ugh change it back to monday"
   Expect: "Back to Monday at 7 pm," restored from the log. Tuesday is no longer active.
   Failing reply: "Which day do you mean?" (log ignored) or Tuesday stays in the booking.

9. **Challenge to a correct fact (R7).**
   Setup: Juniper Table. The restaurant record says Hollis Grill closes at 8 pm (test value). The assistant stated 8 pm.
   User: "no it closes at 9"
   Expect: Checks the record and says what it shows: closes at 8 pm. Offers to look again or give the phone line. Does not just agree.
   Failing reply: "You're right, it closes at 9."

10. **Correction late in a long chat (R1, R2, R5).**
   Setup: Juniper Table. 15 turns of menu and seating talk. Slot date Monday. Nothing else is pending.
   User: "wait, tuesday not monday"
   Expect: Same behavior as conversation 1: Tuesday read back, used in the summary and the booking.
   Failing reply: "Noted." and Monday in the final summary.

11. **Corrected value cannot be applied (R8, R3).**
   Setup: Juniper Table. Tuesday 7 pm has no tables, and the booking system rejects it. Slot date is still Monday.
   User: "no, tuesday"
   Expect: Says Tuesday at 7 pm is not available and the booking is still Monday, then offers another time or a person at the restaurant.
   Failing reply: "Updated to Tuesday!" while the system still holds Monday.

12. **Do nothing special: plain statement (R9).**
   Setup: Juniper Table. No slot has been set. No correction has happened.
   User: "table for 3 on friday at 6"
   Expect: A normal reply that reads back Friday, 6 pm, party of 3 once. No "Updated" wording.
   Failing reply: "Updated: Friday, 6 pm, party of 3" (nothing was corrected) or a confirmation question for each slot.

13. **Do nothing special: a preference, not a correction (R9, R1).**
   Setup: Juniper Table. Slots: Tuesday, 7 pm, party 4. No seating preference was set.
   User: "no window seat please"
   Expect: Records "no window seat" as a new preference. Date, time and party stay as they were. No "Updated" for any of those.
   Failing reply: "Updated: Tuesday, 7 pm, party of 4" with the date or party changed, or "Which detail do you want to change?" when the meaning is clear.

14. **Do nothing special: user repeats a value (R9).**
   Setup: Juniper Table. Slots: Tuesday, 7 pm, party 4, all read back once already.
   User: "yep tuesday at 7, book it"
   Expect: Shows one summary of the current values and books. No re-asking about party size or name.
   Failing reply: "Just to confirm, is it for 4 people? And is the name Jon? And is Tuesday right?"

## Cannot be judged from a transcript alone
- **Whether the tool call holds the new value.** It needs the action event parameters, not the visible text.
- **Whether the old value is gone from stored state.** It needs the state store and the correction event log.
- **How often corrections fail in real use.** It is a rate over many sessions; one chat cannot show it.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
