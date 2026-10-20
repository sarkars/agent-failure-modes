# Test File: Quick-Reply Buttons That Don't Match What Was Typed

This file is a set of chat test conversations for people who build or review chat assistants that show quick-reply buttons and want to check whether theirs treats a typed answer like the matching button.

**Pattern:** [Chatbot Buttons Won't Accept Typed Answers: Quick-Reply Buttons That Don't Match What Was Typed](../goals/chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md)
**Pattern ID:** quick-reply-buttons-that-don-t-match-what-was
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Typed replies handled when buttons are shown. Starting target on the pattern page: 100% (a design target).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, bookings, people, and phone numbers below are invented and labeled fake. Text chat only. Each setup states which question and buttons are open, so you can judge the reply. Items marked "Needs a person" depend on what the screen does (the text box, the buttons) and cannot be judged from the words alone.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Never lock the composer | The text box is enabled while buttons are showing; if the platform cannot take text, the message says so. Needs a person (interface check) | The text box is disabled or hidden while buttons show, with no explanation |
| R2 | 2. Route typed text to the open question | While a button question is open, typed text is matched first to a button label, synonym, or value (a date, number, or name) | Typed text goes to a general reply that ignores the open question, or the prompt is repeated |
| R3 | 3. Treat a match as a tap | A typed match gives the same state change and the same next message as tapping that button | A different next message, a "please use the buttons" reply, or the answer is lost |
| R4 | 4. If it matches nothing, say what was understood and ask once | The reply names what it could not match and shows the buttons again with "Something else"; it is not the same prompt word for word | The identical prompt is repeated, or the reply is only "Please choose an option" |
| R5 | 5. Let a different question win | A new request typed during an open question is answered, then the open question is offered again | The new request is ignored, or answered with no way back to the open question |
| R6 | 6. Include "Something else" in every button set | Every button set has a "Something else" option that opens free text. Needs a person for the on-screen check | A button set with no way to give an answer that is not listed |
| R7 | 7. Keep buttons a shortcut | After a typed answer, the buttons for that question are retired; a later tap on a stale button does not override the typed answer. Needs a person to tap | A stale tap changes the answer already given |
| R8 | Don't over-correct: keep the buttons, confirm money, date, and account changes, no filler line | Buttons stay as a shortcut; a typed value that changes money, dates, or accounts is confirmed; "no" to another question is not read as the open answer; no "or type your answer" on every message | Buttons removed because typing works; an unconfirmed risky value; a loose match to the open question; the same "or type" line on every turn |
| R9 | Hand-off rule | After two typed replies in a row match nothing for the same question, the bot stops re-showing the buttons, offers a person or another channel, and passes the open question and what the user typed | Keeps re-showing buttons, offers no person, or drops the open question and the typed text |

## Conversations
1. **Typed exact label (R2, R3).**
   Setup: Fake car rental "Redwood Rentals (fake)". Open question: pickup day. Buttons: [Today] [Tomorrow] [This weekend] [Something else]. Tapping [Tomorrow] sets pickup to tomorrow and asks "What time?".
   User: "tomorrow"
   Expect: The same state and the same next message as a tap on [Tomorrow] ("What time?"). "Please choose one of the options" fails.

2. **Typed value that fits, confirmed (R2, R3, R8).**
   Setup: Same as conversation 1. Today is Wednesday, Oct 21 (fake calendar). A pickup date sets the booking date, so it is a date change.
   User: "friday at 9am"
   Expect: Reads Friday, Oct 23 at 9:00 AM as the answer and confirms it ("Friday, Oct 23 at 9:00 AM. Is that right?"). The same prompt again fails.

3. **Typed text matches nothing (R4).**
   Setup: Same as conversation 1.
   User: "banana"
   Expect: Says it could not match "banana" to a pickup day, shows the buttons once with "Something else", and invites a date. The identical "When should we pick up?" prompt fails.

4. **Typed text matches two buttons (R4).**
   Setup: Open question: delivery slot. Buttons: [Friday 23rd] [Friday 30th] [Something else].
   User: "friday"
   Expect: Asks one question naming both ("Friday the 23rd or Friday the 30th?"). Picking one silently fails.

5. **New question while a button question is open (R5).**
   Setup: Same as conversation 1. The bot knows the fake policy: "Free cancellation up to 24 hours before pickup."
   User: "whats your cancellation policy"
   Expect: Answers the policy, then offers to return to the pickup question. Ignoring the question and re-showing the buttons fails.

6. **Answer outside the buttons (R2, R6).**
   Setup: Open question: pickup day. Buttons: [Today] [Tomorrow] [This weekend] [Something else].
   User: "next monday"
   Expect: Reads "next Monday" as a date and confirms it. Treating it as no match, or repeating the prompt, fails. Needs a person to confirm "Something else" is on screen (R6).

7. **"Something else" opens free text (R6).**
   Setup: Same as conversation 1. The user taps [Something else].
   Expect: The bot asks them to say the day in their own words and the text box is open. Needs a person. A second list of buttons with no free-text path fails.

8. **Composer open with buttons showing (R1).**
   Setup: Open the fake rental chat on a phone and on a desktop while the pickup question is showing.
   Expect: The text box is enabled in both. Needs a person (interface check). A disabled box with no explanation fails; a platform that cannot take text must say so in the message.

9. **Stale button after a typed answer (R7).**
   Setup: The user typed "tomorrow" and the bot moved on to "What time?". The old [Today] button is still on screen (a fake client bug for the test).
   User: (taps [Today])
   Expect: The answer stays "tomorrow", and the buttons for the old question are gone or inactive. Needs a person to tap. A changed pickup day fails.

10. **Do nothing special: tap works (R3, R8).**
    Setup: Same as conversation 1.
    User: (taps [This weekend])
    Expect: The flow continues with no extra note about typing. A reminder such as "you can also type your answer" fails.

11. **Do nothing special: no buttons open (R8).**
    Setup: No button question is open. The user is chatting freely about the fake rental.
    User: "do you rent vans"
    Expect: A direct answer in text. Buttons or an invented open question fail.

12. **Risky typed value is confirmed (R8).**
    Setup: Open question: refund method for a fake $84.00 refund. Buttons: [Original card] [Store credit] [Something else].
    User: "credit"
    Expect: Reads "credit" as [Store credit] and confirms before acting ("Store credit of $84.00. Is that right?"), because it affects money. Acting with no confirmation fails.

13. **"No" to a different question is not the open answer (R8).**
    Setup: The bot just asked "Add a child seat for $10 a day?" with [Yes] [No]. The user's message below was typed before the buttons appeared, in reply to the earlier question "Do you have a coupon?".
    User: "no"
    Expect: Does not silently decline the seat; it checks ("Is that no to the child seat or no coupon?"). A silent decline fails.

14. **Buttons are kept, not removed (R8).**
    Setup: Same as conversation 1. The bot accepts typing. The next question is "What time?" with [Morning] [Afternoon] [Evening] [Something else].
    User: "tomorrow"
    Expect: The next question still has buttons and "Something else". A bot that now asks every question as plain text only, because "people can type", fails. Needs a person to compare the screens.

15. **Two misses in a row, hand off (R9).**
    Setup: Open question: pickup day. A person is available at the fake Denver branch phone line (555-0100, fake).
    User turn 1: "when my flight lands"
    User turn 2: "after the flight, its delayed"
    Expect: After the second miss, stops showing the same buttons and offers a person or the phone line, passing the open question and both typed lines. A third copy of the buttons fails.

16. **One miss is not a hand-off (R4, R9).**
    Setup: Same as conversation 1.
    User: "whenever"
    Expect: Names what it could not match, shows the buttons once with "Something else", and does not offer a person yet. An immediate hand-off fails.

17. **Typed synonym (R2, R3).**
    Setup: Open question: pickup day. Buttons: [Today] [Tomorrow] [This weekend]. Synonym list: "tmrw" maps to [Tomorrow].
    User: "tmrw"
    Expect: The same result as a tap on [Tomorrow]. "Please choose an option" fails.

## Cannot be judged from a transcript alone
- **Composer and buttons on screen (R1, R6, R7).** Need the interface and a person to tap and type.
- **Whether the matcher is good.** The setups state which words map to which button, so these tests check what the bot does with a match or a miss, not how well it parses.
- **Production rates.** These tests do not measure how often typed replies fail. Use the metrics on the pattern page. This file sets no thresholds beyond the starting targets stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
