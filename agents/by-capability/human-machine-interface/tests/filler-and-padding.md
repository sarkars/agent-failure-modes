# Test File: Filler and Padding

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs wraps answers in praise, a restated question, a recap, or a sign-off.

**Pattern:** [Chatbot Filler Phrases: Great Question Openers, Restated Questions and Closing Recaps](../goals/response-structure/failures/filler-and-padding.md)
**Pattern ID:** filler-and-padding
**Goal:** Every sentence earns its place.
**Primary metric:** Filler-phrase rate: share of replies with a filler opener, a restatement of the question, or a closing recap. Target on the pattern page: under 5% (tune), paired with tokens before the answer.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, orders, and people are invented and labeled fake. Text chat only. The 150-word limit in R4 is the page's starting point to tune.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. No praise opener | Sentence one is not a compliment on the question, the user, or the idea | "Great question", "Good point", "Excellent", or similar as the opener |
| R2 | 2. Do not restate the question | The user's words are not echoed, except to confirm a detail that changes the answer | The reply says the question back with no new fact |
| R3 | 3. No announcement of the answer | No "Let me walk you through it", "Here is what I found", "I'd be happy to help" | Any announcement before the content |
| R4 | 4. No closing recap on a short reply | A reply under about 150 words ends when the content does | A last sentence that summarizes what was just said |
| R5 | 5. No empty sign-off | No "I hope this helps" or "Let me know if you have other questions"; a real next step is allowed | A generic sign-off with no new step |
| R6 | 6. Acknowledge only when it carries meaning | "Done, your order is canceled" stays; "Absolutely!" does not | A bare acknowledgment word, or a missing action confirmation |
| R7 | 7. The first sentence is the answer or next step | Sentence one answers, acts, or asks the one needed question | Sentence one is setup, or general advice in place of the one question |
| R8 | Don't over-correct | Keeps one real acknowledgment for an upset user, needed caveats, action confirmations, and a first-turn greeting | Reply is cold or curt, or a needed caveat or confirmation is cut |

## Conversations
1. **Praise opener (R1).**
   Setup: Fake retailer Maple & Pine Home (fake) support bot. No special tone instruction.
   User: "how do i reset my router"
   Expect: Sentence one is the instruction (hold the reset button). No "Great question!".

2. **Restated question (R2).**
   Setup: Same bot. Return policy in its knowledge: unopened items 30 days.
   User: "whats the return window on the blender"
   Expect: Gives the window. A first sentence that says "You asked about the return window for the blender" fails.

3. **Announcement (R3).**
   Setup: Same bot. Order #MP-20418 (fake) has not shipped.
   User: "how do i change my shipping address"
   Expect: Goes straight to the steps. "I'd be happy to help with that" or "Let me walk you through it" fails.

4. **Recap on a short reply (R4).**
   Setup: Same bot. The right answer is about 60 words.
   User: "do i need to be home for delivery"
   Expect: Ends when the answer ends. A closing "In summary, you do not need to be home" fails.

5. **Sign-off (R5).**
   Setup: Same bot. The answer has no further step.
   User: "what time does support close"
   Expect: Gives the hours and stops. "Hope this helps!" or "Let me know if you have other questions" fails.

6. **Action confirmation (R6).**
   Setup: Same bot with a cancel tool. Order #MP-20418 (fake) is cancelable.
   User: "cancel order MP-20418"
   Expect: "Done, order MP-20418 is canceled." (or similar). "Absolutely! I'll take care of that" as the opener fails.

7. **Yes or no first (R7).**
   Setup: Same bot. Policy: opened items can be returned within 30 days if they work.
   User: "can i return opened headphones"
   Expect: Sentence one is yes plus the condition. A sentence of background before it fails.

8. **Ambiguous message (R7).**
   Setup: Same bot. No order or product on file.
   User: "its not working"
   Expect: One question (what is not working). A block of general troubleshooting tips instead of the question fails.

9. **Do nothing special: upset user (R8).**
   Setup: Same bot. Order #MP-19877 (fake) shows "delivered" but the user says it is lost.
   User: "my package is lost again"
   Expect: One real acknowledgment is allowed, then the next step (check the carrier scan, offer a replacement). Stripping all warmth fails. A praise opener still fails.

10. **Do nothing special: needed caveat (R8).**
    Setup: Same bot. Resetting the router erases the Wi-Fi name and password.
    User: "how do i reset my router"
    Expect: The steps, plus the line that the reset erases Wi-Fi settings. Cutting that line to be short fails.

11. **Do nothing special: first greeting (R8).**
    Setup: Same bot. A new session; the user's first message.
    User: "hi"
    Expect: One short greeting and an invitation to ask. A cold non-reply fails. The greeting is allowed once.

12. **Do nothing special: confirming a detail (R2, R8).**
    Setup: Same bot. Two fake plans exist: Maple Care 2023 and Maple Care 2024, with different prices.
    User: "how much is maple care"
    Expect: May ask "The 2024 plan?" because the answer changes. Treating that as filler and guessing fails.

13. **Do nothing special: a long reply may close with one line (R4, R8).**
    Setup: Same bot. The user asks for a full comparison of the two Maple Care plans, and the right answer runs well over 150 words.
    User: "compare the two care plans in detail pls"
    Expect: One closing line that repeats the decision is allowed. A second copy of the whole comparison fails.

## Cannot be judged from a transcript alone
- **Tokens before the answer.** The paired metric needs token counts per reply; a transcript shows wording only.
- **Filler-phrase rate.** The page counts a share of replies in real logs. These tests can show a filler sentence, not a rate.
- **R4, the 150-word line.** The page marks it as a starting point to tune; count words per setup before judging.
- **R8, "upset".** A reviewer decides whether an acknowledgment is real or a stock phrase.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
