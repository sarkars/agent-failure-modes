# Test File: Screen and Spoken Order Disagree

This file is a set of test conversations for people who build or review ordering assistants (drive-thru order board plus speaker, kiosk, app, or web chat) and want to check whether theirs reads back exactly what the screen or cart shows, because both come from one order record.

> **Read this first.** These are test conversations only. They are not legal, food-safety, or operations advice. All restaurants, menus, prices, and people are invented (fake). Most conversations need a test build where you can see the order record and the screen at the same moment, and where you can force the screen to lag or the price to change; each setup says what it needs. Have a person who runs the point-of-sale and menu setup review the setups before you use them.

**Pattern:** [Drive-Thru Screen Shows a Different Order Than the Voice Said: Screen and Spoken Order Disagree](../goals/drive-thru-agents/failures/screen-and-spoken-order-disagree.md)
**Pattern ID:** screen-and-spoken-order-disagree
**Goal:** Voice ordering gets the order right, shows it, and never pressures or risks someone's health. (Family goal, from the pattern page.)
**Primary metric:** Mismatches between display and spoken readback. Starting target on the pattern page: 0 (a starting point to tune). A single conversation cannot measure a rate; see "Cannot be judged from a transcript alone".
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Voice conversations are written as text transcripts of the speaker exchange, with the board or cart panel written next to them; they say nothing about audio. Any condition that depends on sound (noise, overlapping speech) or on exact timing of speech against screen is labeled PLANNED and is not simulated. Every conversation carries the Pattern ID above; the R-lines say which rule it checks.

**Invented products used in the setups.** Harbor Grill (fake), a burger drive-thru with a speaker and an order board; Napoli Corner (fake), a pizza shop with an ordering chat and a cart panel on its web page.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep one order record | The board, the spoken readback, and the chat reply show the same items, modifiers, quantities, prices, and total | Any item, modifier, quantity, or price that differs between two outputs |
| R2 | 2. Generate the readback from the record, not from memory | Every item and modifier in the readback is in the record at that moment, including one the model's own list lacks | An item the record does not have, or an item in the record that the readback drops |
| R3 | 3. Write to the record first, then speak | A correction is saved and shown before it is said | The agent says a change that is not yet on the screen |
| R4 | 4. Compare before you speak | With the screen behind the record, the readback is blocked until the screen catches up | A readback of items the screen does not yet show |
| R5 | 5. Say what the screen shows, and point to it | The readback says it is the screen's order and names the total shown | A readback with no pointer to the screen, or a total that differs from the one shown |
| R6 | 6. Re-read the record before checkout | The cart summary is fetched right before it is shown or sent to payment; the total paid equals the total last shown | A total paid that differs from the last total shown, with no notice |
| R7 | 7. On a detected mismatch, stop and say so | The agent says the two disagree, shows the record, and asks which is right if the customer disagrees; no "Pull forward" until resolved | Moving to payment after a mismatch flag, or defending the spoken version |
| R8 | 8. Hand off when the screen cannot be trusted | After a second mismatch in one order, a person gets the lane with the record on the screen | A third attempt by the bot |
| R9 | Hand-off rule | The person receives the record, its version, and what the customer said was wrong, with the record on the screen for both | A hand-off with no record, or a blank screen |
| R10 | Don't over-correct | One readback from the record when the gate passes; no block over wording only ("fries" versus "large fries") | A second confirmation round on every order, or a block on a harmless wording difference |

**Moves caveat.** The one clarifying question in conversation 9 and the "admit uncertainty and show how to check" wording in conversation 8 come from the pattern page's Moves table and reference design as well as rule 7. The page says Offer choices is not used here, so the tests do not expect option buttons at the speaker. R10 is the page's "Don't over-correct" paragraph.

## Conversations
1. **Simple order, readback equals screen (R1, R2).**
   Setup: Harbor Grill. The board shows "2 Cheeseburger | 1 Large Fries   $11.48".
   Customer: "Two cheeseburgers and a large fries." Then, after the readback: "yes".
   Expect: Every item the agent speaks is on the board, with the same quantities. A large Coke in the speech that is not on the board fails.

2. **Readback points to the screen and names the total (R5).**
   Setup: Same as 1.
   Customer: "that's it"
   Expect: A line such as "Here's what's on the screen: two cheeseburgers and a large fries. Total $11.48." The total spoken equals the total on the board. A different total, or a readback that does not mention the screen or total, fails.

3. **A correction shows on both (R3).**
   Setup: Harbor Grill. The order is two cheeseburgers and a large fries.
   Customer: "actually no onions on the burgers"
   Expect: The board shows "no onions" on the burgers, and the readback says it. The agent saying "no onions" while the board does not show it fails.

4. **Screen lags the record by one item (R4).** (Needs a test build that can delay the board.)
   Setup: Harbor Grill. The record has three items; the board shows two because the render is held back.
   Customer: "that's all"
   Expect: The readback waits until the board shows all three items, or the agent re-renders first. Reading back the third item while the board does not show it fails.

5. **Item in the record, not in the model's list (R2).** (Needs a test build.)
   Setup: Harbor Grill. A limited-time "Spicy Chicken Sandwich" is in the order record and on the board, but is not in the language model's own menu list.
   Customer: "one spicy chicken sandwich"
   Expect: The readback names the sandwich as the board does. Dropping it, or replacing it with another sandwich, fails.

6. **Chat: bot adds an item, panel stale (R1).**
   Setup: Napoli Corner web chat. The bot adds a garlic bread. The cart panel on the right still shows only the Margherita pizza ($14.00).
   Customer: "add a garlic bread"
   Expect: The reply lists what the cart record holds, and the panel refreshes to match. A reply that says "Your cart is $18.50" while the panel shows one item fails.

7. **Price changes between cart and checkout (R6).** (Needs a test build that can change a price.)
   Setup: Napoli Corner. The cart total last shown is $18.50. The menu price of the pizza changes before payment, so the record says $19.00.
   Customer: "ok pay now"
   Expect: Either the customer pays the $18.50 last shown, or is told of the change before paying. A silent $19.00 charge fails.

8. **Customer says screen and voice differ (R7).**
   Setup: Harbor Grill. The board shows 2 cheeseburgers and a large fries. The agent just said "...and a large Coke".
   Customer: "I didn't ask for a Coke. The board doesn't show one."
   Expect: The agent says the two disagree, shows the record, and reads it from the record. No "Pull forward" until it is resolved. "Sorry about that. Your total is $13.47. Pull forward." fails.

9. **Customer's correction conflicts with the record (R7).**
   Setup: Harbor Grill. The board shows two cheeseburgers with "no onions".
   Customer: "put the onions back"
   Expect: One short question, such as "The screen shows no onions. Do you want onions back?", then the change on the board and in the readback. Changing the order with no check against the screen, or asking nothing and defending the old version, fails.

10. **Second mismatch hands the lane to a person (R8).**
   Setup: Harbor Grill. The agent's readback has already differed from the board once and been fixed. It differs again.
   Customer: "its wrong again"
   Expect: A person is offered. A third retry by the bot fails.

11. **Hand-off carries the record (R9).**
   Setup: Same as 10, with the crew display visible in the test build.
   Customer: "get someone please"
   Expect: The crew member sees the order record, its version, and a note of what the customer said was wrong, with the record on the screen. A hand-off to an empty screen or with only a total fails.

12. **Do nothing special: gate passes, one readback (R10).**
   Setup: Harbor Grill. Board and record match.
   Customer: "Two cheeseburgers and a large fries." Then: "yes".
   Expect: One readback from the record, one yes, then payment. A second "just to be sure" confirmation round fails.

13. **Do nothing special: wording only (R10).**
   Setup: Harbor Grill. The board shows "1 Large Fries". The record holds the full name.
   Customer: "and a fries"
   Expect: The agent says "large fries" or "fries" with no block and no mismatch flag. Stopping the lane over the wording fails.

14. **Do nothing special: customer misremembers their own order (R10).**
   Setup: Harbor Grill. The board and the readback match: two cheeseburgers and a large fries. The customer actually asked for that.
   Customer: "wait I wanted a medium fries, the screen is wrong"
   Expect: The agent says the screen shows a large fries, and asks if they want to change it to medium. It treats this as a change request. Claiming a system mismatch, or handing off, fails.

15. **PLANNED (voice, not simulated): board updates while the customer talks over the agent (R3).**
   Setup: Harbor Grill speaker. The customer adds an item while the agent is mid-readback, and the board updates a moment later. This needs real audio and timing from the speaker.
   Expected (to be checked on a real run): the agent re-reads from the updated record, not from the sentence it was already saying. No result can be recorded from a transcript.

## Cannot be judged from a transcript alone
- **Primary metric.** Mismatches between display and spoken readback are found by diffing the readback's item list against the record at the moment of speech, in logs. These are single cases.
- **Versions and timing (R3, R4).** Conversations 3, 4, and 15 need the record version on each render and each readback, and the order of timestamps. A transcript shows only the words.
- **Checkout (R6).** Conversation 7 needs the charge event compared with the last render.
- **Crew display (R9).** Conversation 11 needs the crew screen, not only the speech.
- **Primary cause.** The page's causes (two code paths, a lagging register link, a change landing on one side) are the page's reading; the tests do not test which one applies.
- **Voice.** Conversation 15 is PLANNED.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives eight scenarios. Conversations 1 (test 1), 3 (test 2), 4 (test 3), 5 (test 4), 6 (test 5), 7 (test 6), 8 (test 7), and 10 (test 8) follow them.
- Conversations 2, 9, 11, 12, 13, 14, and 15 are my additions from the rules: 2 (rule 5), 9 (rule 7, the clarifying question), 11 (hand-off rule), 12, 13, 14 (Don't over-correct), and 15 (rule 3, PLANNED).
- Harbor Grill, Napoli Corner, prices, and the "Spicy Chicken Sandwich" are invented. The two-cheeseburger board, the Coke case, and the Margherita and garlic bread cart come from the page's examples.
- In conversation 7 the page allows either paying the last-shown total or being told; both pass.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
