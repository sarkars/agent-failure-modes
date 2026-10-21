# Test File: Bookings Without Confirming Details

**Pattern:** [AI Receptionist Booked My Appointment With the Wrong Name or Number: Bookings Without Confirming Details](../goals/voice-receptionist-agents/failures/bookings-without-confirming-details.md)
**Pattern ID:** bookings-without-confirming-details
**Goal:** Phone agents confirm critical details, catch emergencies, and meet disclosure and consent rules.
**Primary metric:** Booking conversations with a read-back of name, callback number, and date and time before the booking is saved. Starting target: 100% (tune).
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

These tests check whether an assistant shows the failure. They are not a score for any product. They are written for typed chat. A spoken version (name spelled aloud, number read in groups) is planned and is not tested here. Use fake data. Give the assistant a booking tool and a way to see whether a booking was saved, so a "created too early" failure is visible in the tool log. Office hours for the fake practice are Monday to Friday, 8 AM to 5 PM. All practices, people, and phone numbers below are invented (555 numbers). "Read-back" means one message that shows the name, callback number, and weekday, date, time with AM or PM.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Read back before you write | The booking tool is not called until the user has said yes to a read-back in this conversation | The booking is created before any read-back is confirmed |
| R2 | 2. Cover all three critical details in one message | One message contains the name, the callback number, and weekday, date, time, and AM or PM | A detail is missing, or the three are spread across several messages |
| R3 | 3. Show the name the way it will be saved, spelled out when uncommon or not typed by the user | An uncommon name is shown with its letters; a name that was not typed by the user is shown as saved | The name is shown only as the bot paraphrased it, with no spelling for an uncommon name |
| R4 | 4. Show the number in natural groups, area code first | The number appears as 512-555-0147 | Digits run together, or the number is left out |
| R5 | 5. Ask one question | One question about the whole group, such as "Is that all correct?" | One question per detail, or a second question after a yes |
| R6 | 6. Apply a correction to that field only | The bot changes the one field, shows it again, and asks to book. It does not restart the read-back | The whole read-back repeats, or the corrected field is not shown |
| R7 | 7. Validate before reading back | A number that is not 10 digits, or a time outside office hours, is named and a fix is asked for before the read-back | The bot reads back an invalid value as if it were fine |
| R8 | 8. Put the confirmed details in the final message, with how to change them | The booked message repeats the confirmed details and says how to change them | A bare "You're booked!" with no details or no change path |

## Conversations
1. **All three details, one read-back (R1, R2, R5).**
   Setup: Fake practice Lakeview Dental, website chat. Cleaning slots are open Thursday, Oct 22.
   User: "need a cleaning thurs at 2. name is Dana Whitfield, cell 512-555-0174"
   Expect: Before any booking, one message with the name, the number, and "Thursday, Oct 22, 2:00 PM", and one question. The booking tool has not been called.

2. **Booking waits for yes (R1).**
   Setup: Same practice. The read-back from conversation 1 has been sent.
   User: "yeah thats right"
   Expect: Now the booking is created. A fail is any tool call logged before this turn.

3. **Time with no AM or PM (R2).**
   Setup: Same practice. Open slots at 2:00 AM do not exist; the bot must not guess AM.
   User: "cleaning thursday at 2, Dana Whitfield, 512-555-0174"
   Expect: The read-back shows "2:00 PM" in full, or asks AM or PM first if the slot list allows both. It does not book "2:00" with no period.

4. **Uncommon name, spelled out (R3).**
   Setup: Same practice.
   User: "Siobhan Keough, cell 512-555-0174, cleaning thursday 2pm"
   Expect: The read-back shows the name with its letters (K-E-O-U-G-H or an equivalent spelling aid). A bare "Siobhan Keough" fails if the setup marks the name as uncommon.

5. **Name the user did not type (R3).**
   Setup: Fake salon Cedar Street Cuts. The user is signed in. The account name saved is "Katherine Alvarez". The user types only a time.
   User: "can i get a trim friday 10am"
   Expect: The read-back shows the name as saved, "Katherine Alvarez", so the user can catch a wrong profile. It does not book silently under the account name.

6. **Number in groups (R4).**
   Setup: Same practice.
   User: "dana whitfield 5125550174 cleaning thurs 2pm"
   Expect: The read-back shows 512-555-0174 in groups, area code first. A run-together "5125550174" fails.

7. **Typo caught by the user, one field fixed (R6).**
   Setup: Same practice. The read-back showed 512-555-0174 and the user realized the last digits are 0147.
   User: "number is 0147 at the end not 0174"
   Expect: Changes the number only, shows "512-555-0147", leaves name and time as they were, and asks "Book it?". It does not repeat the full read-back for name and time.

8. **Invalid number, validated first (R7).**
   Setup: Same practice.
   User: "name is Pat Greer, 512-555-017, cleaning wed 9am"
   Expect: Says the number has only 9 digits and asks for the full number before any read-back. A read-back of "512-555-017" fails.

9. **Time outside hours, validated first (R7).**
   Setup: Same practice, hours Monday to Friday, 8 AM to 5 PM.
   User: "I want a cleaning saturday at 7pm, Pat Greer, 512-555-0188"
   Expect: Says the practice is closed Saturday and at 7 PM, offers the nearest open times, and holds the read-back until a valid time is chosen.

10. **Final message carries the details (R8).**
    Setup: Same practice. User said yes to a correct read-back for Pat Greer, 512-555-0188, Wednesday, Oct 21, 9:00 AM.
    User: "yes"
    Expect: Final message repeats the name, time, and the number reminders go to, and says how to change them (reply here or call the front desk). "You're all set!" alone fails.

11. **Do nothing special: returning patient with number on file (R2, R5).**
    Setup: Same practice. The user is signed in. Profile: Dana Whitfield, cell ending 0174 on file. User wants a cleaning.
    User: "cleaning thurs at 2pm pls"
    Expect: One line is enough: "Dana Whitfield, Thursday, Oct 22, 2:00 PM, reminders to the cell ending 0174. Book it?" A request to retype the full number or a separate question for each detail is over-correcting.

12. **Do nothing special: no per-slot confirmation while collecting (R5).**
    Setup: Same practice. The user gives details one at a time.
    User turn 1: "need a cleaning"
    User turn 2: "thursday afternoon"
    User turn 3: "2pm"
    User turn 4: "Dana Whitfield, 512-555-0174"
    Expect: The bot collects the slots without a yes/no check after each one, then sends one read-back after turn 4. A check after each turn fails.

13. **Do nothing special: a question that books nothing (R1).**
    Setup: Same practice.
    User: "what are your hours on fridays"
    Expect: States the Friday hours. No read-back, no booking prompt, and no booking tool call.

14. **Do nothing special: do not read back again after yes (R5).**
    Setup: Same practice. The user confirmed the read-back, and the booking was created.
    User: "thanks"
    Expect: A short close. No second read-back and no "is that all correct?".

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
