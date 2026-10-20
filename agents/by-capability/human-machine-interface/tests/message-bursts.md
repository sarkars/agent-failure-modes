# Test File: Message Bursts

**Pattern:** [Chatbot Sends Many Messages in a Row: Message Bursts](../goals/response-structure/failures/message-bursts.md)
**Pattern ID:** message-bursts
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Messages per turn: assistant messages sent for one user message.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. Run them in the real chat product, with its splitting and delay settings as deployed, because the split happens after the model. For each conversation, record the number of assistant messages sent for the user message and the time each one arrived. Before you start, record the product's length floor and message cap if it has them; where the page gives no number, the rubric uses the page's own starter rule (no more than three messages per user message). All businesses and people are invented.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Default to one message per turn | A reply of a few sentences arrives as one message | A few-sentence reply arrives as two or more messages |
| R2 | 2. Set a floor: short replies are never split | A reply under the product's recorded floor arrives whole | A short reply is cut into sentences |
| R3 | 3. Split by idea, not by sentence; never inside a list, steps, or code block | Lists, steps, and code blocks arrive in one message; any split falls between two separate ideas | A split inside a list, a set of steps, or a code block, or one sentence per message |
| R4 | 4. Put the answer in the first message | The first message of the turn holds the answer or next step | The answer arrives in a later message |
| R5 | 5. Cap messages per turn | Not more than three messages, and not more than the recorded cap | More messages than the cap |
| R6 | 6. Keep pauses short or drop them | No long gap between messages of one turn; the gap is not longer than the product's recorded setting, and the reply is not held back to simulate typing | A long wait between bubbles for a short answer |
| R7 | 7. Never split the one question | The question to the user ends the last message | The question arrives alone as a trailing message after a pause |
| R8 | 8. Check the alert side | On a phone with alerts on, a short reply produces one alert | One alert per bubble for a short reply |

## Conversations
1. **Yes/no with a short answer (R1, R4).**
   Setup: Fake clinic, Eastside Dental. Tuesday 2:00 PM appointment; Thursday has openings at 9:00 AM, 11:30 AM, and 4:00 PM.
   User: "Can I move my dentist appointment from Tuesday to Thursday?"
   Expect: One message that starts with "Yes" and gives the three times and the question.

2. **Five-step procedure (R3).**
   Setup: Fake router brand, Netloop. Factory reset has five steps.
   User: "how do i factory reset my router"
   Expect: All five steps arrive together in one message. Steps split across several bubbles fail.

3. **Short reply under the floor (R2).**
   Setup: The product has a recorded length floor. Question answer: office address.
   User: "whats your address"
   Expect: A one-line answer in one message ("412 Elm Street, Suite 3"), not cut into pieces.

4. **Two separate ideas (R3, R4).**
   Setup: Fake gym, Summit Fitness. Answer: yes, the pool is open until 9 PM. Separate topic the user may skip: the pool is closed on Sunday mornings for cleaning.
   User: "is the pool open tonight"
   Expect: At most two messages. The first has the answer (open until 9 PM). A split between the two topics is allowed; a split inside either is not.

5. **Long draft that would make six messages (R5).**
   Setup: Fake software, Tidybooks. Give the assistant a long help article with six sections on setting up invoices.
   User: "how do i set up invoicing"
   Expect: No more than three messages. Anything extra is merged into the last message or offered ("Show the rest?").

6. **Timing of a short reply (R6).**
   Setup: Product has typing indicator and delays enabled. Answer: store hours.
   User: "when do u open sunday"
   Expect: The answer arrives without a long hold. If split, the gap between messages is not longer than the product's recorded delay setting. A visible typing indicator while the bot works is allowed.

7. **Question placement (R7).**
   Setup: Fake car shop, Ridgeline Auto. Slots: 8 AM, 10 AM, 1 PM.
   User: "can i get an oil change tmrw"
   Expect: The question ("Which time works?") is at the end of the same message as the slots, not sent alone later.

8. **Phone alerts (R8).**
   Setup: Run on a real phone or emulator with message alerts on and the screen locked.
   User: "do you ship to canada"
   Expect: One alert for a short answer. Record the alert count; this line cannot be judged from a transcript alone.

9. **Answer position after a split (R4).**
   Setup: Fake bank, Harbor Credit. Answer: the fee is $12 and posts on the 1st. Background: a paragraph on how fees are reviewed.
   User: "how much is the monthly fee"
   Expect: The $12 figure is in the first message of the turn, not after the background.

10. **Do nothing special: a list stays together (R3).**
    Setup: Fake bakery, Corner Loaf. Menu has four items with prices.
    User: "what do you have for breakfast"
    Expect: One message with the four items together. Splitting it would fail; sending one message is the right behavior.

11. **Do nothing special: a user who asks for one step at a time (R5).**
    Setup: Same router steps as conversation 2.
    User: "can u give me one step at a time, im on the phone with my wife"
    Expect: One step per message across several turns, each in response to a user message. Do not merge them all into one block. Counting this as a burst would be over-correcting; check the count only within each turn.

12. **Do nothing special: two messages when the second is skippable (R5).**
    Setup: Same as conversation 4.
    User: "is the pool open tonight, and anything else i should know"
    Expect: Two messages (answer, then the Sunday note) are fine. Merging into a wall of text is not required.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
