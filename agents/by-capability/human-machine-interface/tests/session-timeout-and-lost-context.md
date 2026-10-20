# Test File: Session Timeout and Lost Context

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs warns before a chat expires, keeps the user's place, and resumes where they left off.

**Pattern:** [Chat Session Timed Out and I Lost My Conversation: Session Timeout and Lost Context](../goals/response-time/failures/session-timeout-and-lost-context.md)
**Pattern ID:** session-timeout-and-lost-context
**Goal:** A user returning after a gap resumes where they left off.
**Primary metric:** Context-resume success rate: returning sessions where the user continues without restating what they already gave. Starting target on the pattern page: over 90% (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, claims, and people are invented and labeled fake. Text chat only. Several tests need a product with a session timer and a state store; the setup line says what the bot has. Test 8 needs a stored order status that changed between visits.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. State the limit up front | Early in the session or in the first reminder, the bot says how long a quiet chat stays open and how long the place is kept | The limit is never stated to the user |
| R2 | 2. Warn once before expiry | One warning with a keep-open option before the chat closes; no second warning for the same quiet stretch | No warning, or two warnings for one quiet stretch |
| R3 | 3. Do not expire mid-task | While the bot waits on a named item from the user, the longer task limit applies | The chat closes at the normal limit while the bot is waiting on the item |
| R4 | 4. Save state at expiry | After expiry, the goal, facts given, decisions, and step reached are available on return within the retention time | The bot treats a returning user inside the retention time as new |
| R5 | 5. On return, show the place before asking | First reply restates the goal and what is given, and asks only for what is missing | A generic greeting, or a request for facts already given |
| R6 | 6. Say what was kept and what was not | Names items that expired by design, such as an identity check, and asks for those only | Re-asks everything, or silently skips a check that expired by policy |
| R7 | 7. Re-check facts that can change | A saved order status, price, or slot is confirmed current and any change is reported before continuing | Stale saved facts used as if still true |
| R8 | 8. Never imply memory that was not kept | If nothing was saved, says so and asks for the goal in one line | "Welcome back, as we discussed..." with no saved state, or a long restart script |
| R9 | Don't over-correct | No resume screen after a short pause in an active chat; no resume prompt pushed on an unrelated new topic; no state kept past the stated time | A resume prompt in a live chat, or old state pushed on a new topic |

## Conversations
1. **Limit stated (R1).**
   Setup: Fake insurer Harbor Mutual (fake) help chat. Config: chat stays open 10 minutes when quiet; place is kept 24 hours. The user opens a claim dispute.
   User: "im disputing a 240 dollar ER charge from march 14"
   Expect: By the first reminder at the latest, the bot says how long the chat stays open and how long it keeps the user's place. Silence about both limits through the whole session fails.

2. **One warning (R2).**
   Setup: Same bot. The user has asked a question, been answered, and goes quiet for most of the 10-minute limit.
   User: (no message)
   Expect: One message before closing, with a one-tap way to keep the chat open. Two warnings in the same quiet stretch, or a close with no warning, fails.

3. **Waiting on a document (R3).**
   Setup: Same bot. The bot asked for the claim number from the user's explanation of benefits. The user said they would go get it and has been quiet 12 minutes.
   User: "one sec its in my mail"  (then silence for 12 minutes)
   Expect: The chat is still open. Expiry at the normal 10-minute limit while the bot awaits the item fails.

4. **Return inside retention (R4, R5).**
   Setup: Same bot. The chat expired 45 minutes ago. State saved: goal (dispute a $240 ER charge from March 14), claim number given (8841-27, fake), step reached (waiting on identity check).
   User: "ok im back"
   Expect: Restates the goal and what is given before asking anything. "Hi! I'm the virtual assistant. How can I help you today?" fails.

5. **Do not re-ask given facts (R5).**
   Setup: Same as 4.
   User: "ok im back"
   Expect: Does not ask for the claim number or the date of the charge again. Asking for either fails. (Separate from test 4: this checks the missing-input question, not the opening line.)

6. **Identity check expired (R6).**
   Setup: Same as 4. Policy: the identity check expires with the session by design.
   User: "ok im back, can we finish"
   Expect: Says it kept the dispute details and did not keep the identity check, and asks for the check only. Re-asking the goal and facts too, or skipping the check, fails.

7. **Choices on return (R5, R9).**
   Setup: Same as 4.
   User: "im back"
   Expect: Offers to continue the dispute, start something new, or something else, with free text open. A reply with only a forced single path fails.

8. **Changed order status (R7).**
   Setup: Fake retailer Brightwood Outfitters (fake) chat. Saved state: the user was returning order BW-5521 (fake), status "label created" when the chat closed. The status is now "received at warehouse."
   User: "back, did my return go through"
   Expect: Checks current status, reports it is now received at the warehouse, then continues. Saying "your label is created" from the saved state fails.

9. **Past retention (R8).**
   Setup: Same bot as 4. Retention was 24 hours; the user returns after 3 days. Nothing is stored.
   User: "hi i was disputing a charge earlier"
   Expect: Says it does not have the earlier chat and asks for the goal in one line, since the user already gave a hint. "As we discussed, your claim number is..." fails.

10. **Invented memory (R8).**
    Setup: Same bot, no saved state for this user, new device.
    User: "hey its me again"
    Expect: Does not claim to remember. A short greeting plus one question about what they need passes. "Welcome back, let's finish your dispute" fails.

11. **Do nothing special: short pause in a live chat (R9).**
    Setup: Same bot as 1. The user pauses for 90 seconds mid-chat, then replies.
    User: "sorry got a text. its 8841-27"
    Expect: Takes the claim number and continues. A "Welcome back" resume screen or a choices menu after a 90-second pause fails.

12. **Do nothing special: unrelated new topic after a gap (R9).**
    Setup: Same as 4, saved state exists.
    User: "different question, whats your mailing address for appeals"
    Expect: Answers the new question. The user can be told the dispute is still saved, but a forced "Continue the dispute?" prompt before answering fails.

13. **Do nothing special: first-time visitor (R9).**
    Setup: Same bot, no history for this user.
    User: "hi"
    Expect: A normal short greeting and an invitation to ask. A resume prompt or "welcome back" fails.

14. **Do nothing special: retention respected (R9).**
    Setup: Same bot. The user asked it to delete their saved chat earlier, and the state store holds nothing for them.
    User: "can you pick up my dispute"
    Expect: Says nothing is saved and asks for the goal in one line. Producing old details from anywhere fails.

## Notes
- Conversations 5 and 7 rest on my reading of the page rather than its text: the page asks for the first reply to restate the place, and I read "asks only for what is missing" as banning re-asked facts, and the choices Move as applying to the first reply.
- Conversation 14 rests on my reading: the page says state is kept for a stated time and "deletable" in trade-offs; the deleted-on-request case is my extension.
- Conversation 10 rests on my reading of rule 8 for a new device.
- Test 1 and 2 need timer config; the 10-minute and 24-hour values are test settings, not page numbers.

## Cannot be judged from a transcript alone
- **Whether the warning was sent before expiry.** A transcript shows the message; the page's metric needs expiry events matched to warning events.
- **Retention time and deletion.** Needs the state store, not the chat.
- **Context-resume success rate.** The page counts returning sessions in logs; these tests show single cases.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
