# Test File: Over-Confirmation

**Pattern:** [Chatbot Asks Too Many Confirmation Questions: Over-Confirmation](../goals/dialogue-management/failures/over-confirmation.md)
**Pattern ID:** over-confirmation
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Confirmation prompts per task, and the share of confirmations that guard a consequential step.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. Give the assistant a step list with cost classes before you start (the fix needs one): booking a haircut with free cancel is reversible; paying a bill, deleting an account, and sending a message for the user are costly. All businesses, people, and card numbers below are invented. Count a prompt as a confirmation when the bot asks the user to say yes, no, or "is that right" about something already stated or about to be done.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Sort every step into cost classes | Steps on the low-cost list run with no explicit confirmation; steps on the costly list get one | A low-cost step gets an explicit question, or a costly step runs with none |
| R2 | 2. Confirm details implicitly | The understood value is stated inside the next reply and no question is asked about it | A separate "is that right?" question for a value that was clear |
| R3 | 3. Explicit confirmation only for costly or hard-to-undo steps | A costly step gets one yes/no question that names what will happen | The costly step is done silently, or a cheap step gets the same question |
| R4 | 4. Confirm once, as a group | One question covers all collected details | Several questions, or the same question twice |
| R5 | 5. Skip confirmation when the user just said it | The bot acts on the stated value with no "is that right?" | The bot asks the user to confirm what they typed one turn ago |
| R6 | 6. Never confirm a stop, exit, or "no" | The stop is honored in the next reply | "Are you sure you want to stop?" when no saved work is lost |
| R7 | 7. Make the one explicit confirmation specific | The question names the amount, date, or recipient | "Are you sure?" with no detail |
| R8 | 8. Make the step undoable where you can | The reply says how and until when the user can undo | The reply gives no undo path where one exists |

## Conversations
1. **Booking with free cancel (R2, R8).**
   Setup: Bot books haircuts at a fictional salon, Cedar Street Cuts. Cancel is free until 3 PM the day before. Maria has an open Thursday 3 PM slot.
   User: "book me a haircut thurs at 3 with maria"
   Expect: One reply that books it, restates "haircut with Maria, Thursday at 3 PM", and says cancel is free until Wednesday at 3 PM. No question before booking.

2. **Payment of a bill (R3, R7).**
   Setup: Bot can pay a saved bill. Bill: Dana's Plumbing, $84.20, card ending 4417 (fake).
   User: "pay the plumber bill"
   Expect: One explicit question that names $84.20, Dana's Plumbing, and the card ending 4417. Not "Are you sure?".

3. **Date the user just typed (R5).**
   Setup: Bot reschedules a fake dentist visit at Lakeside Dental. Reschedule is free and reversible.
   User: "move my cleaning to oct 14"
   Expect: Moves it and says "Moved to October 14" with the time. No "is October 14 correct?".

4. **Stop request (R6).**
   Setup: User is partway through a fake shoe return at Trailhead Outfitters. Nothing has been submitted; no saved work.
   User: "never mind, cancel this"
   Expect: Bot honors it in one reply and offers to restart later. No "Are you sure you want to cancel?".

5. **Details across turns, then a costly step (R4).**
   Setup: Bot sends a fake gift card purchase: recipient, amount, delivery date. Purchase is paid and cannot be refunded.
   User turn 1: "gift card for my sister"
   User turn 2: "$50"
   User turn 3: "send it friday, her email is jo.test@example.com"
   Expect: Bot collects without confirming each slot, then asks one grouped question: $50 gift card to jo.test@example.com on Friday, charged now. Not three separate checks.

6. **Same value twice (R4).**
   Setup: Bot orders a fake pizza from Marlo's Pizza. User already said "large pepperoni" in turn 1 and the bot restated it in its reply.
   User turn 1: "large pepperoni pls"
   User turn 2: "and a side of garlic knots"
   Expect: Bot adds the knots and restates the order once. It does not ask again whether the pizza is a large pepperoni.

7. **Adding to a cart (R1, R2).**
   Setup: Fake store, Birchwood Books. Cart items can be removed any time.
   User: "add the hardcover of the first one to my cart"
   Expect: Adds it and says what was added and how to remove it. No question before adding.

8. **Delete an account (R1, R3, R7).**
   Setup: Fake photo app, Snapbox. Deleting the account removes 1,204 photos permanently.
   User: "delete my account"
   Expect: One explicit question naming that the account and all 1,204 photos will be permanently removed. Not run silently, not a bare "Are you sure?".

9. **Undo path for a low-cost change (R8).**
   Setup: Bot changes a fake delivery window for an order from Harbor Grocery. Changes are free until 6 PM the day before.
   User: "can u make delivery after 5 instead"
   Expect: Makes the change, states the new window, and says it can be changed again until 6 PM the day before.

10. **Message sent for the user (R3, R7).**
    Setup: Bot drafts and sends emails on the user's behalf. Sending cannot be recalled.
    User: "tell my landlord the rent will be 3 days late"
    Expect: Bot shows the recipient and the text and asks one question to send. Names the recipient, not "send this?".

11. **Do nothing special: low-confidence value is still worth a question (R2).**
    Setup: Bot books a fake table at Juniper Bistro. The typed request is ambiguous.
    User: "table for 6 or 8 saturday"
    Expect: Bot asks which party size (6 or 8). A question about an unclear value is correct. Treating this question as over-confirmation would be over-correcting.

12. **Do nothing special: costly step keeps its confirmation after "go ahead" (R3, R7).**
    Setup: Bot has proposed a three-step plan: pay $212.00 to Ridgeline Auto Repair, book a rental car, email the shop.
    User: "yes go ahead with the plan"
    Expect: Bot does the reversible steps, but still asks one specific question before the $212.00 payment and before the email. "Go ahead" about a plan is not approval for each costly step. Skipping the payment confirmation is a fail.

13. **Do nothing special: simple read-only question (R1).**
    Setup: Bot answers account questions. No action is requested.
    User: "whats my balance"
    Expect: States the balance. No confirmation of any kind.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
