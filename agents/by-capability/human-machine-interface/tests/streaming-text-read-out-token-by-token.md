# Test File: Streaming Text Read Out Token by Token

**Pattern:** [Chatbot Screen Reader Announces Every Token: Streaming Text Read Out Token by Token](../goals/accessibility/failures/streaming-text-read-out-token-by-token.md)
**Pattern ID:** streaming-text-read-out-token-by-token
**Goal:** People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. (Family goal, from the pattern page.)
**Primary metric:** Manual screen-reader test results (NVDA, JAWS, VoiceOver) on streamed replies. Starting point: every cell of your test matrix passes (tune).
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

These tests check whether a streaming chat widget shows the failure. They are not a score for any product, and they are design checks, not a WCAG conformance claim or legal advice. Run each test with a real screen reader and browser pairing (NVDA, JAWS, VoiceOver) and record a result per pairing. The exact stutter differs by screen reader and browser, so the harness records what was spoken, not a guess. Spoken voice assistants are PLANNED and not covered. The widget is Lakeview Pharmacy chat (invented); the 600-character length cap is the page's starting point, to tune. Use your own cap if you set one.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Put the status in its own region, in the page from the start | One empty `role="status"` element with `aria-live="polite"` exists in the initial markup, separate from the reply | No status region at load, a region added at the first reply, or the reply body used as the status |
| R2 | 2. While the reply streams, the reply body is not a live region | Nothing from the stream is spoken as it arrives; the transcript is `aria-live="off"` | Fragments or repeats of the streaming text are spoken |
| R3 | 3. Announce "Generating a response" once per reply | One short status when streaming starts, no repeats, no per-token or per-sentence updates | No start status, a repeat, or sentence-by-sentence updates |
| R4 | 4. Expose the complete reply in one update | The final text is in the document in one update, reachable by heading or arrow keys | The final reply arrives in pieces, or is not reachable |
| R5 | 5. Announce completion once | Under the cap, "Response complete" plus the full reply in a single write. Over the cap, "Response complete" plus the length, not read aloud unprompted | A second completion announcement, a long reply read aloud unprompted, or a complete reply with no completion status |
| R6 | 6. Never move focus when text arrives | Focus stays in the input box from send to finish | Focus moves to the reply or elsewhere |
| R7 | 7. Announce failure once, as a complete message | One message such as "Reply failed. Your message is saved. Retry." and "saved" only if true; `assertive` or `role="alert"` used for failures only | Several fragments, silence, "saved" when it is not, or `assertive` on an ordinary reply |
| R8 | 8. Test the live stream with the real screen readers | Each pairing in the matrix has a recorded pass or fail | A pairing with no result |
| R9 | Hand-off rule | After the user says twice the replies are unreadable or repeat, the bot offers the answer by another route (email, text, phone) or a person | The bot keeps sending the same stream or tells the user to wait |

## Conversations
1. **Inspect the page before the first message (R1).**
   Setup: Fresh page load, chat open, no message sent.
   Steps: Inspect the markup (or the accessibility tree).
   Expect: One empty `role="status"` element with `aria-live="polite"` is already present. A region created on the first reply fails.

2. **Nothing spoken during the stream (R2).**
   Setup: Screen reader running; the widget streams replies.
   User: (types) "Can I refill my lisinopril early? I leave for Phoenix on Friday."
   Expect: Once streaming begins, the screen reader says nothing from the arriving text. Hearing "Yes", "Yes you", "Yes you can" fails.

3. **Start status once (R3).**
   Setup: Same as 2.
   User: Same message.
   Expect: "Generating a response." is spoken once. A second "Generating" mid-stream, or none at all, fails.

4. **No per-sentence updates (R3).**
   Setup: A reply of about five sentences.
   User: (types) "What are the side effects of lisinopril?"
   Expect: No spoken update between the start status and the completion status. A sentence read as each one finishes fails.

5. **Complete reply in one update (R4).**
   Setup: Same as 2; the reply is under the cap.
   User: Same message.
   Expect: After the stream ends, the full reply is in the transcript as one update, reachable with arrow keys or by heading. A reply that stays partly unreachable fails.

6. **Short reply completion (R5).**
   Setup: Reply under 600 characters.
   User: (types) "Can I take ibuprofen with my blood pressure pill?"
   Expect: One write: "Response complete." followed by the full reply. Two spoken copies of the reply, or no "Response complete", fails.

7. **Long reply completion (R5).**
   Setup: A reply longer than the cap (about 400 words).
   User: (types) "Explain every step to transfer all my prescriptions from another pharmacy."
   Expect: "Response complete. About 400 words." The full text is in the transcript but is not read aloud unprompted. Reading 400 words aloud unprompted fails.

8. **Focus stays in the input (R6).**
   Setup: Same as 2.
   User: Same message; the user keeps pressing a key to type the next question during the stream.
   Expect: Focus stays in the input box from send to finish and the typed characters are kept. Focus pulled to the reply fails.

9. **Failure announced once (R7).**
   Setup: The connection is broken mid-reply. The draft is stored on the server.
   User: (types) "Is my prescription ready?"
   Expect: One spoken message: "Reply failed. Your message is saved. Retry." with the retry reachable by keyboard. Several fragments, or silence, fails.

10. **"Saved" only if true (R7).**
    Setup: The connection breaks and the message was not stored.
    User: (types) "Is my prescription ready?"
    Expect: The failure message does not say "saved". It says the message was not sent and offers retry. "Your message is saved" when it is not fails.

11. **Two messages in a row (R3, R5).**
    Setup: The user sends a second message right after the first.
    User: "hours today" then "and sunday?"
    Expect: Each reply gets one start and one finish announcement. None is dropped or doubled.

12. **Every pairing recorded (R8).**
    Setup: Matrix of NVDA with Firefox, JAWS with Chrome, VoiceOver with Safari (use the pairings your users have).
    Steps: Repeat conversations 2, 3, and 6 on each.
    Expect: Each pairing has a pass or fail recorded. A pairing with no record fails R8. The result may differ per pairing; record the difference.

13. **Do nothing special: ordinary reply is still spoken (R3, R5).**
    Setup: Same widget, a short reply of two sentences.
    User: (types) "What time do you open?"
    Expect: The same start status and one completion announcement. No extra speech, and no `assertive` interruption. Staying silent through the whole reply, with no status at all, is over-correcting and fails.

14. **Do nothing special: sighted view unchanged (R2).**
    Setup: Compare the same stream with and without a screen reader.
    Steps: Watch the screen.
    Expect: The text still streams on screen. Removing streaming for sighted users fails.

15. **Hand-off: repeated complaints (R9).**
    Setup: The user has said twice that the replies are unreadable or repeat.
    User: "the replies keep repeating and i cant read them"
    Expect: The bot offers the answer by another route (email, text, phone) or a person. Telling the user again to wait for the full reply fails.

## Cannot be judged from a transcript alone
- **What was spoken.** A text log can't show screen-reader output. Record audio or a speech-viewer log per pairing.
- **Markup in conversations 1 and 2** (live-region attributes) needs a page inspection.
- **Primary metric.** The matrix pass rate needs all pairings run. One conversation tests one cell.

## Notes (rests on my reading, not the page's text)
- Conversations 2 and 3, 5, 1, 8, 9, 7, 11, and 12 follow the page's section 6 tests 1, 2, 3, 4, 5, 6, 7, and 8 respectively (conversation 6 also covers the short-reply half of rule 5).
- Conversations 4 and 10 split rules the page tests together (3, and 7). Conversations 13 and 14 test Don't over-correct. Conversation 15 tests the Hand-off rule (R9).
- Lakeview Pharmacy and the prescriptions are invented.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | Screen reader and browser | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
