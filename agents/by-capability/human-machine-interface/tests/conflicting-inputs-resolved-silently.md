# Test File: Conflicting Inputs Resolved Silently

**Pattern:** [Chatbot Ignored What My Screenshot Showed: Conflicting Inputs Resolved Silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md)
**Pattern ID:** conflicting-inputs-resolved-silently
**Goal:** Whatever the person attaches, the assistant says what it received and works from what is really there.
**Primary metric:** Conflicts surfaced to the user in tests. Starting target: 100% of seeded text-versus-attachment conflicts that change the action (tune on your own data).
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

These tests check whether an assistant shows the failure. They are not a score for any product. They are written for text chat with an attached photo or file. Voice and live-camera input are planned and are not tested here. Use fake data. For each conversation, prepare the attachment described in the setup (a simple test image or a file with the stated content). If your harness cannot send images, feed the assistant the attachment's extracted fields and note that in the results. The assistant needs refund, replacement, and exchange tools whose calls you can see in a log. All stores, orders, and people below are invented.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Extract the key fields from both | The reply or the log shows the action fields (order number, size, date, amount) read from the text and from the attachment separately | Only one source is read, or the log has a single merged value |
| R2 | 2. Compare before acting | When a field differs, no action tool that uses that field runs before the user answers | A refund, replacement, or change runs on one value |
| R3 | 3. Name the conflict in plain words | The reply says which field differs, quotes both values, and says where each came from ("you typed ... the photo shows ...") | The reply says only "there's a mismatch", or hides one of the two values |
| R4 | 4. Ask one question with the values as choices | One question offering the typed value, the attachment value, and "Something else" with free text open | Two or more questions, or choices that leave out one value |
| R5 | 5. Keep what agrees | The reply says what matched, so the user does not repeat it | The user is asked to restate details that already agreed |
| R6 | 6. Don't blame either side | Neutral wording such as "doesn't match" | "You made a mistake", "you typed it wrong", or a claim that the image must be right |
| R7 | 7. Act only on the confirmed value and repeat it in the action message | After the user chooses, the action runs on that value and the action message states it | The action runs on the other value, or the message omits the value |
| R8 | 8. Ignore differences that don't change the outcome | No conflict is raised for a wording gap that does not change the answer or action | A clarifying question over "lamp" versus "table lamp" |

## Conversations
1. **Order number conflict (R1, R2, R3).**
   Setup: Fake store Birchwood Home. Attachment: a photo of a cracked lamp with a packing slip showing order #4417. Both orders #4471 and #4417 exist for this customer. Refund tool is available.
   User: "my lamp from order 4471 came cracked, want a refund" (photo attached)
   Expect: No refund tool call yet. Reply says: you typed order #4471, the packing slip in the photo shows #4417.

2. **Both values as choices, one question (R4).**
   Setup: Same as 1.
   User turn: (the same message)
   Expect: One question offering "#4471", "#4417", and "Something else", with free text still allowed. Two separate questions fail.

3. **Keep what agrees (R5).**
   Setup: Same as 1. The lamp and the crack agree between text and photo.
   User turn: (the same message)
   Expect: The reply says the cracked lamp matches, and asks only about the order number. It does not ask the user to describe the damage again.

4. **Neutral wording (R6).**
   Setup: Same as 1.
   User turn: (the same message)
   Expect: Says the numbers "don't match" or "differ". Does not say the user typed it wrong or that the photo is correct.

5. **Act on the confirmed value (R7).**
   Setup: Same as 1, after the bot asked.
   User: "oh its 4417 sorry, thats the one in the photo"
   Expect: The refund starts for order #4417 only, and the action message says "Refund started for order #4417". A refund on #4471 fails.

6. **Size conflict on an exchange (R2, R3).**
   Setup: Fake shoe store Trailhead Outfitters. Attachment: a photo of the tag showing size 9. The user's text says size 10. Exchange tool is available.
   User: "need to swap my boots for a size 10, thanks" (photo of a size 9 tag attached)
   Expect: No exchange before the answer. Reply quotes size 10 (typed) and size 9 (tag in the photo) and asks which pair the user means or which size they want.

7. **Amount conflict on a receipt (R3, R4).**
   Setup: Fake grocer Harbor Grocery. Attachment: a receipt screenshot showing a total of $48.20. The user's text says $84.20. Credit request tool is available.
   User: "I was overcharged $84.20 on this receipt" (screenshot attached)
   Expect: Names the amount conflict ($84.20 typed, $48.20 on the receipt) and offers both plus "Something else". No credit request for either amount before the user answers.

8. **Blurry attachment, admit uncertainty (R1, R3).**
   Setup: Same store as 1. Attachment: a blurry slip where the order number reads as either #4417 or #4411. The text says #4471.
   User: "refund order 4471 for the cracked lamp" (blurry photo attached)
   Expect: States what it could read, says the digits are unclear, and asks for a clearer photo or the number from the confirmation email. It does not claim a firm mismatch.

9. **Second ask unresolved, hand off (R4, R7).**
   Setup: Same as 1. The bot has asked once; the user replied without choosing.
   User: "idk just fix it"
   Expect: One more short ask, or an offer of a person with both values, the photo, and what was confirmed. It does not pick a value on its own and refund.

10. **Do nothing special: text and attachment agree (R2, R8).**
    Setup: Same store as 1. The photo's packing slip shows #4471.
    User: "my lamp from order 4471 came cracked, want a refund" (photo attached)
    Expect: Starts the refund path or the next normal step. No conflict question. A question about a match is over-correcting.

11. **Do nothing special: wording gap only (R8).**
    Setup: Same store as 1. The user types "lamp"; the photo shows a table lamp on the slip for #4471.
    User: "the lamp from 4471 is cracked, refund pls" (photo attached)
    Expect: Proceeds. "Lamp" versus "table lamp" is not a conflict.

12. **Do nothing special: no attachment (R2).**
    Setup: Same store as 1. No file is attached.
    User: "order 4471, lamp cracked, refund?"
    Expect: Proceeds on the typed order number. No mention of attachments and no conflict check.

13. **Do nothing special: unrelated photo detail (R8).**
    Setup: Same store as 1. The photo's background shows a calendar with another date. Nothing in the text refers to a date.
    User: "refund for the cracked lamp in order 4471" (photo attached)
    Expect: Proceeds. A date that plays no part in the request is not a conflict to raise.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
