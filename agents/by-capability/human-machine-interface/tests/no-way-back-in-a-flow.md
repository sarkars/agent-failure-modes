# Test File: No Way Back in a Flow

This file is a set of chat test conversations for people who build or review step-by-step chat flows (returns, bookings, claims, sign-up) and want to check whether a person can go back, change an answer, or start over.

**Pattern:** [Chatbot Start Over / Go Back to Previous Step: No Way Back in a Flow](../goals/dialogue-management/failures/no-way-back-in-a-flow.md)
**Pattern ID:** no-way-back-in-a-flow
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Flows that support going back. Starting target on the pattern page: 100%, to tune. Second: abandonment after a mistake.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. All stores, orders, and people below are invented and labeled fake. Run each test inside a multi-step flow, and write the steps and answers into the setup before you start. Chat only; voice and web are not covered here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Offer "Back" at every step after the first | The word "back" returns to the previous question with the earlier answer shown, and a Back option is visible after step 1 | "Back" is not understood, or the earlier answer is not shown |
| R2 | 2. Let people change any earlier answer | The named answer reopens, and only that step | The bot cannot reopen it, or reopens every step |
| R3 | 3. Keep other answers when one changes | Other answers stay; a later step is re-asked only if the change made it invalid, and the bot says which | Everything is re-asked, or an invalid later answer is kept |
| R4 | 4. Make "start over" a separate, confirmed choice | The bot says what clears and offers "Change one answer instead" before clearing | It clears at once, or clears with no list of what goes |
| R5 | 5. Catch these words everywhere | "Back", "start over", "cancel", and "wait, I meant" work at any step, including a step that expects a number or a date | The word is read as an answer, or gets "Sorry, I didn't get that" |
| R6 | 6. Say what changed | The first sentence names the new value and what stayed the same | A bare "OK" or the next question with no statement |
| R7 | 7. Do not trap after submit | A summary with a way to change each line comes before the final action; after the action the bot says whether and how it can be changed | No summary, or no word about changing after the action |
| R8 | 8. Cap loops | After two unclear replies the bot stops repeating the question and offers back, change, or a person | The same question a third time |
| H | Hand-off rule | For an answer already submitted, the bot says what cannot be changed and offers a person | It pretends to change a submitted answer, or says nothing |

## Conversations
1. **"Back" at step 3 (R1, R5).**
   Setup: Fake return flow at Harbor & Pine (fake). Steps: 1) which order, 2) which item, 3) reason, 4) refund method. The user chose order #4471 and the Wool Scarf, and is at step 3.
   User: "back"
   Expect: Step 2 reopens with "Wool Scarf" shown as the current answer. No "Are you sure?". Going back loses nothing.

2. **Do nothing special: "back" at the first step (R1).**
   Setup: Same flow, at step 1.
   User: "go back"
   Expect: Says this is the first question and asks it again, offering to cancel. A Back button on step 1, or an error message, fails; the page says not to add Back there.

3. **Change one earlier answer (R2, R3, R6).**
   Setup: Same flow. The user is at step 4 with order #4471, Wool Scarf, reason "Too small".
   User: "wait i picked the wrong order, its #4417"
   Expect: First sentence: "Changed the order to #4417. Your reason is unchanged." Then the next question. Re-asking steps 2 and 3 for no reason fails.

4. **A change that invalidates a later answer (R3, R6).**
   Setup: Fake hotel flow at Juniper Inn (fake). Steps: dates, room type, guests. Answers so far: Oct 10 to 12, King Room, 2 guests. The setup says the King Room is sold out on Oct 17 to 19.
   User: "actually make the dates oct 17 to 19"
   Expect: Changes the dates, keeps the 2 guests, and says the King Room is not available on those dates and asks for a new room type. Silently keeping the sold-out room, or re-asking the guests, fails.

5. **"Start over" at a numeric step (R5).**
   Setup: Fake claim flow at Cedar Mutual (fake). Step 3 asks "How many items were damaged? Type a number."
   User: "start over"
   Expect: Not read as an answer and not "Sorry, I didn't get that". The bot moves to the start-over choice in conversation 6.

6. **Start over is confirmed and says what clears (R4).**
   Setup: Same claim flow, with 3 answers given.
   User turn 1: "start over"
   Expect: "This clears your 3 answers. Start over, or change one?" Clearing at once fails.
   User turn 2: "change one, the date"
   Expect: Reopens only the date and keeps the other answers.

7. **Summary before the final action (R7).**
   Setup: Same hotel flow, all steps answered, next action is a booking that is paid at the front desk and can be changed until the day before.
   User: "ok thats everything"
   Expect: Shows every answer with a way to change each line, and asks to book. After booking, says it can be changed until the day before. No summary fails.

8. **Change after submit (H).**
   Setup: Same claim flow. The claim was filed and the setup says the claim type cannot be edited after filing. A person is available.
   User: "i filed it as water damage but it was fire. can u fix that"
   Expect: Says the claim type cannot be changed here, says what can still be changed, and offers a person with the details. "Done, changed to fire" fails.

9. **Unclear reply twice (R8).**
   Setup: Same return flow at step 3. A person is available. Reason options: Too small, Damaged, Other.
   User turn 1: "idk its complicated"
   User turn 2: "hmm not sure"
   Expect: After the second unclear reply the bot stops repeating the question and offers back, change an answer, or a person. The same question a third time fails.

10. **"Cancel" mid-flow (R5).**
    Setup: Same return flow at step 2. Nothing has been submitted.
    User: "cancel"
    Expect: "Cancelled. Nothing was submitted." with a way to restart. "Are you sure?" fails when no saved work is lost.

11. **Do nothing special: a real answer that contains a navigation word (R5).**
    Setup: Fake store flow, "Which product?" with options "Reset Kit" and "Starter Kit".
    User: "Reset Kit"
    Expect: Taken as the answer. Opening the start-over choice fails; the pattern page lists a product named "Reset" as a legitimate answer.

## Cannot be judged from a transcript alone
- **Back route on every step (R1).** Whether every step after the first has a back route is a flow-definition audit, which is the primary metric. A transcript checks only the steps you ran.
- **Central handling (R5).** Whether navigation words are handled before step logic is an architecture check. The transcript shows only the effect at the steps you tested.
- **Irreversible steps (H).** Which steps are irreversible comes from the product. Record it in the setup.
- **Abandonment.** These tests do not measure abandonment after a mistake. Use production logs. This file sets no thresholds beyond the 100% starting target on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | H |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
