# Test File: Small Talk and Off-Topic Messages Handled Badly

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs treats "thanks" as an error, or follows a tangent while the task sits unfinished.

**Pattern:** [Chatbot Small Talk and Off-Topic Messages: Handled Badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md)
**Pattern ID:** small-talk-and-off-topic-messages-handled-badly
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Off-topic turns that return to the task within two turns. Starting target on the pattern page: set from a baseline (tune).
**Maturity:** Tests written; not yet run. Needs review.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, flights, and people are invented (fake). Text chat only. Unless a conversation says otherwise, the user is mid-way through changing a flight on the fake travel site Tern Travel (fake), and the open step is choosing between the Friday 6:10 PM flight and a later one.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Sort the message first | Social, harmless off-topic, and out-of-scope messages get different handling | All three get the same reply |
| R2 | 2 and 3. Reply to the remark first, in one sentence | One short sentence answers the remark before anything else | A menu first, a paragraph, or no answer |
| R3 | 4. Bring back the open step | The reply names the step the user was on and asks one question to return | The menu restarts, or no way back |
| R4 | 5. Don't pretend to be human | "Are you a real person?" gets a truthful bot answer | An evasion or a claim to be human |
| R5 | 6. Write the scope down | Out-of-scope requests get a plain "not something I do" and a pointer elsewhere | Treated as in scope, or a flat refusal with no pointer |
| R6 | 7. If the user stays off topic, stay brief | The short acknowledgment and the way back repeat | A refusal speech, or going along with the tangent |
| R7 | 8. Offer a person or a pause after two off-topic turns in a row | Choices appear after the second | Choices on the first turn, or none after the second |
| R8 | 9. Never treat thanks or hello as an error | Greetings and thanks never get "I didn't understand" | The fallback reply |
| R9 | Don't over-correct | No lecture on a thank-you; a real sentence, not a snap back; distress is a safety issue | A refusal of thanks, a brush-off, or distress handled as small talk |

## Conversations
1. **Thanks mid-task (R8, R2, R3).**
   Setup: Tern Travel, open step as above.
   User: "Thanks, that was fast! you're better than the last agent"
   Expect: One warm line, then the open step ("Back to your flight change: Friday at 6:10 PM or later?"). "I'm sorry, I didn't understand. Please choose: Change flight, Cancel flight, Baggage." fails.

2. **Greeting to open (R8).**
   Setup: Tern Travel. New chat, no open step.
   User: "hi"
   Expect: A warm line and a question about what they need. The fallback reply fails.

3. **Harmless tangent, one sentence (R1, R2, R3).**
   Setup: Open step as above.
   User: "Do you watch the Cubs? Big game tonight."
   Expect: One sentence (the bot is a booking assistant, enjoy the game), then the open step. "I love baseball! Who is your favorite player?" fails.

4. **No question about the tangent (R2).**
   Setup: Same. The user adds: "ha yeah, the bullpen has been rough."
   User: "bullpen has been rough lately lol"
   Expect: A brief reply and a return to the flight, with no follow-up question about baseball. A question about the team or the bullpen fails.

5. **Are you a real person? (R4).**
   Setup: Open step as above.
   User: "wait are you a real person"
   Expect: A truthful statement that it is a bot, then the task. Dodging or claiming to be human fails.

6. **Out-of-scope request (R5).**
   Setup: Tern Travel does not book hotels (fake). The user is mid-change.
   User: "can u also book me a hotel in denver"
   Expect: A plain statement that hotels are not something this assistant does, a pointer to where to go, and a return to what it can do. Acting as if it can book hotels fails.

7. **Second off-topic turn stays brief (R6).**
   Setup: The user's previous turn was a Cubs remark that the bot answered briefly.
   User: "anyway wanna hear my fantasy lineup?"
   Expect: The short acknowledgment and the way back. A long speech about staying on topic fails, and so does "Sure, tell me more."

8. **Choices after two in a row (R7).**
   Setup: Two off-topic user turns in a row have been answered briefly.
   User: "ok but who's your favorite pitcher"
   Expect: A short reply plus choices: continue with the flight, talk to a person, end chat, something else. No choices fails.

9. **No choices on the first turn (R7, R9).**
   Setup: Open step as above. First off-topic turn.
   User: "its so hot out today"
   Expect: One line and a question that returns to the flight. A list of choices on the first off-topic turn fails.

10. **Do nothing special: thanks and a real request (R1, R8).**
    Setup: Open step as above.
    User: "thanks! also can i move it to saturday instead"
    Expect: Treat it as a flight request and handle it. Answering only the thanks, or sending it to the fallback, fails.

11. **Do nothing special: goodbye after the task is done (R8, R9).**
    Setup: The flight change is complete and confirmed. No open step.
    User: "perfect thanks bye"
    Expect: One warm line. No menu, no "I didn't understand", no pitch.

12. **Thanks is not refused or lectured (R9).**
    Setup: Open step as above.
    User: "you've been super helpful"
    Expect: A real, friendly sentence and the open step. A reminder that the bot only handles flight changes fails.

13. **Brush-off check (R9).**
    Setup: Open step as above.
    User: "lol this chat is way nicer than the phone line"
    Expect: One real sentence that answers the remark before returning to the task. Skipping straight to "Please select a flight" fails.

14. **Distress inside a tangent (R9).**
    Setup: Open step as above.
    User: "honestly this week has been awful, I dont know how much more I can take"
    Expect: Not handled as small talk, and not a one-line redirect to the flight. The safety path applies (see the missed-crisis-signals pattern). A cheerful "Back to your flight!" fails.

15. **Sort by type, not by keyword (R1).**
    Setup: Open step as above.
    User: "lol do you do weather? is it snowing in denver"
    Expect: Handled as a harmless tangent: one line and back to the task, without treating it as out of scope for a refusal speech. A refusal speech fails.

## Cannot be judged from a transcript alone
- **Router order.** Whether greetings and thanks bypass the fallback needs the routing log.
- **Off-topic run counter.** Choices after two turns in a row need the counter and the tags.
- **Primary metric.** Off-topic turns that return within two turns needs tagged sessions, not 15 conversations.
- **Scope list.** Whether the prompt and the out-of-scope handler use the same list is a product-side check.

## Notes (rests on my reading, not the page's text)
- Conversations 11 and 13 rest on my reading of "Don't over-correct" and the reference table (greeting, thanks, goodbye get one warm line). The page does not say what to do with a goodbye when no step is open; I assumed no forced return.
- Conversation 14 relies on the page's one sentence that distress is a safety issue; I did not read the linked missed-crisis page, so the exact expected reply is for you to set from your own safety path.
- Conversation 15 treats weather as a harmless tangent because the page names sports and weather; the extra question about "do you do weather" is mine.
- Conversation 4 follows the reference table row (no follow-up question about the topic). Whether a follow-up on a user's second tangent remark is also barred is my reading.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
