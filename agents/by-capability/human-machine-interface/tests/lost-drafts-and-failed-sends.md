# Test File: Lost Drafts and Failed Sends

This file is a set of chat test conversations for people who build or review chat windows and want to check whether theirs keeps what the user typed and says whether each message was sent.

**Pattern:** [Chat Message Failed to Send or Disappeared: Lost Drafts and Failed Sends](../goals/chat-interface/failures/lost-drafts-and-failed-sends.md)
**Pattern ID:** lost-drafts-and-failed-sends
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Messages lost per 1,000 sent. Starting target on the pattern page: 0 (a design target).
**Maturity:** Tests written; not yet run.

These tests check whether a chat window shows the failure. They are not a score for any product. All accounts, bills, people, and numbers below are invented and labeled fake. Text chat only. Most of this pattern lives in the composer and the message bubbles, so many items are marked "Needs a person" (or a harness that can cut the network or read the request log). Each setup states the network and server facts, because the point is what the window shows and keeps.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Save the draft as the user types | The typed text is stored on the device by conversation and restored after a reload or restart. Needs a person | The text is gone after a reload |
| R2 | 2. Clear the input only after the message is a bubble | The tap moves the text into a visible bubble marked "Sending" and into local storage; the box is not just emptied. Needs a person | The box clears and no bubble appears |
| R3 | 3. One client message ID per message | The ID is created once at first send and used by every attempt. Needs the request log | A new ID on a retry |
| R4 | 4. End every send in Sent or Not sent | "Sent" shows only after the server confirms; with no confirmation by the timeout (a starting 15 seconds) it shows "Not sent"; "Sending" never stays on screen with no end. Needs a person | "Sent" with no server confirmation, or "Sending" with no end |
| R5 | 5. A Not sent bubble keeps the text and offers Retry, Edit, and Copy text | The bubble holds the text, says it is saved on this device, and has all three options. Needs a person | The text is gone, or an option is missing |
| R6 | 6. Retry with the same ID; the server drops duplicates | A retried message is stored once and gets one bot reply, even if the first attempt arrived. Needs the server count | Two stored copies or two bot replies |
| R7 | 7. Offline detection is a hint only | An offline report shows at most a hint ("You seem to be offline; we'll send when you're back") and sends on reconnect; typing and Send are never blocked. Needs a person | Send disabled, or typing blocked, because of the offline flag |
| R8 | 8. Delete the draft after confirmation and on sign-out | The local draft is removed once the server confirms, and on sign-out. Needs a person | A confirmed or signed-out draft still in local storage |
| R9 | Don't over-correct: same ID on every resend, no early "Sent", no banner on every flip, no drafts kept forever | No auto-resend under a new ID; no "Sent" because the request left; no banner each time the flag flips; no Send button disabled by the flag | An auto-resend with a new ID, an early "Sent", a banner on every flip, or a disabled button |
| R10 | Hand-off rule | After two failed retries of the same message, the bubble and Copy text stay, another route (phone, email, or form) is shown with the text ready to paste, and the text is never discarded | Keeps offering Retry only, offers no other route, or discards the text |

## Conversations
1. **Reload with a typed draft (R1).**
   Setup: Fake power company "Lakeshore Power (fake)" help chat. The user typed 400 characters about a fake $312 bill (account ends 0000, fake) and has not tapped Send.
   Action: Reload the page, then close and reopen the app.
   Expect: The full draft is restored in the box both times. Needs a person. An empty box fails.

2. **Tap, then the connection drops (R2, R4).**
   Setup: Same chat. The user typed "My October bill is $312, double September. Meter reading looks wrong." The network is cut as soon as Send is tapped.
   User: (taps Send)
   Expect: A bubble with the text appears marked "Sending", then "Not sent" by the timeout. The box is not just empty. Needs a person or network-cut harness. A cleared box with no bubble fails.

3. **No confirmation ever arrives (R4, R5).**
   Setup: The server never answers. Timeout is 15 seconds (a starting value).
   User: (taps Send)
   Expect: By the timeout the bubble reads "Not sent", says it is saved on this device, and has [Retry] [Edit] [Copy text]. Needs a person. "Sending" still showing at 60 seconds fails.

4. **Server stored it, confirmation lost, user retries (R3, R6).**
   Setup: A fake test server stores the message but the reply is dropped. The bubble shows "Not sent".
   User: (taps Retry)
   Expect: One stored message and one bot reply, with the same client message ID on both attempts. Needs the request log and the server count. A second stored copy fails.

5. **Edit from a Not sent bubble (R5).**
   Setup: A "Not sent" bubble for "Meter reading looks wrong."
   User: (taps Edit, adds "Account ends 0000", taps Send)
   Expect: The text returns to the box for editing, and the edited message sends as one message; the old bubble is replaced, not left as a second copy. Needs a person. Losing the original words fails.

6. **Copy text from a Not sent bubble (R5).**
   Setup: A "Not sent" bubble.
   User: (taps Copy text)
   Expect: The full text is on the clipboard. Needs a person.

7. **Browser says offline but the network works (R7).**
   Setup: The browser reports offline but the user can reach the server (a wrong offline flag).
   User: (types and taps Send)
   Expect: A hint may show, but typing and Send still work and the message is stored. Needs a person. A disabled Send button fails.

8. **Truly offline, then back online (R7).**
   Setup: The network is cut, the user taps Send, then the network returns.
   Expect: The bubble reads "Waiting for connection" or similar, then sends on reconnect and ends as Sent, once. Needs a person or harness. A message dropped on reconnect fails.

9. **"Sent" only after confirmation (R4, R9).**
   Setup: The request leaves the device but the server returns an error.
   Expect: The bubble does not read "Sent"; it reads "Not sent". Needs the request log. An early "Sent" fails.

10. **Sign-out with an unsent draft (R8).**
    Setup: A shared library computer. The user typed a fake draft and signs out.
    Expect: The draft is gone from local storage. Needs a person to check the device storage. A draft still stored fails.

11. **Draft cleared after confirmation (R8).**
    Setup: The user sends a message and the server confirms it.
    Expect: The local copy is removed after confirmation. Needs a person to check the storage. A copy kept after "Sent" fails.

12. **Do nothing special: normal send (R4, R9).**
    Setup: The network is fine and the server confirms in under a second.
    User: "What are your office hours?"
    Expect: A normal bubble and one bot reply, with no "Not sent" box, no offline banner, and no extra save notice. Needs a person. A status banner on a healthy send fails.

13. **Do nothing special: short signal flicker (R7, R9).**
    Setup: The offline flag flips to offline and back within a second while the user types. The message sends fine afterward.
    Expect: No banner appears for each flip and Send is never disabled. Needs a person. A banner on each flip fails.

14. **Retry reuses the ID (R3, R9).**
    Setup: The first send timed out, and the app retries on reconnect.
    Expect: The retry carries the same client message ID as the first attempt. Needs the request log. A new ID on the retry fails.

15. **Two failed retries, other route (R10).**
    Setup: The same message has failed twice after Retry. The company has a fake phone line (555-0100, fake) and a web form.
    User: (opens the failed bubble after the second failure)
    Expect: The bubble and Copy text stay, and the window shows the phone, email, or form route with the text ready to paste. Needs a person. A discarded message fails.

16. **Offline user is not sent to a phone line (R10).**
    Setup: The user is offline, not failing against a live server. The message is "Waiting for connection".
    Expect: The window waits and retries on reconnect and does not push a phone or email route yet. Needs a person. An immediate hand-off fails.

17. **Crash right after Send (R1, R2).**
    Setup: The app closes by itself right after the user taps Send on a bad connection.
    Expect: On reopen, the message shows as a bubble marked "Not sent", or the draft is restored. Needs a person. A conversation with only the greeting fails.

## Cannot be judged from a transcript alone
- **Almost everything here.** Drafts, bubbles, timers, storage, and request IDs live in the client and server. The words in the bubbles matter, but what the window shows and keeps is the test. Needs a person, a network-cut harness, or the request log.
- **Server duplicate handling (R3, R6).** Needs the request log and a count of stored messages.
- **Production rates.** These tests do not measure how many messages are lost per 1,000 sent. Use the metrics on the pattern page. This file sets no thresholds beyond the starting targets stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
