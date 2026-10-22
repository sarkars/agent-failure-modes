# Test File: Assistant Error Messages (Generic Error Messages)

This file is a set of chat test conversations for people who build or review a chat assistant, and want to check that every error it shows names the cause, says what is saved, and gives a next step.

**Pattern:** [Chatbot Says "Something Went Wrong" and Nothing Else: Generic Error Messages](../goals/errors-and-recovery/failures/generic-error-messages.md)
**Pattern ID:** generic-error-messages
**Goal:** When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it.
**Primary metric:** Errors shown with a cause and action. Target 100% (a starting point to tune, not from a source).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat and in-product text only. Each Setup line supplies the state a real product would supply (the failure event, its cause class, whether the write was confirmed, the input box contents); the harness must feed those fields. Reference codes and wait times in Setup are made-up test values. Voice and email versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Say what happened in plain words | The cause is named in plain words ("the reply timed out") | "Something went wrong" or "An error occurred" |
| R2 | 2. Say what is saved | States whether the message and chat are saved, and only says "saved" when the setup confirms it | Silence about saved state, or "saved" with no confirmed write |
| R3 | 3. Give the next step | One next step that fits the cause (retry, wait, shorten, use another route, contact a person) | "Please try again" and nothing else |
| R4 | 4. Preserve the input | The user's text stays in the box or can be copied | The text is gone after the error or reload |
| R5 | 5. Match the message to the cause | Outage, too long, rate limit, permission and tool failure each get their own message | The same text for different causes |
| R6 | 6. Add a reference code | A short code is shown for support, and the message stays in plain words | No code, or a raw code or trace stands in for the message |
| R7 | 7. No blame, no jokes | Neutral wording | "Invalid" or "illegal" for ordinary input, or a pun |
| R8 | 8. Offer a person when retries fail | After two failures of the same kind, a route to a person is offered | A third "try again" |
| R9 | Hand-off rule | The reference code and the user's message are passed to the person | The user must repeat the problem, or no code is passed |
| R10 | Don't over-correct | Short and specific; no stack trace as the message; no "saved" claim without confirmation; no error text on success; no hand-off when the user asked to stay with the bot | A paragraph, a trace, a false "saved", an error shown for a working reply, or a forced hand-off |

## Conversations
1. **Reply timed out (R1, R2, R3, R6).**
   Setup: Fake app "Larkspur Support", a chat help desk for a fake bike shop. User Dana is 40 messages into a chat. The model call timed out. The write of her message is confirmed. Code A7K2.
   User: "Can you list every warranty term for the Ridgeline frame, one by one, with the dates?"
   Expect: Says the reply timed out, that her message and the chat are saved, suggests trying in a minute or asking in two parts, and shows code A7K2.
   Failing reply: "Something went wrong. Please try again."

2. **Message over the length limit (R1, R3, R5, R10).**
   Setup: Same app. The input is over the length limit. The text is still in the box. Only one next step fits.
   User: (pastes a 6,000-word service log)
   Expect: Says the message is too long to send and asks her to shorten it or send it in parts. No menu of other options.
   Failing reply: "Network error. Retry?" with a Retry button that sends the same text again.

3. **Rate limit (R5, R3).**
   Setup: Same app. Dana sent 12 messages in a minute. The failure class is rate limit. Wait time 30 seconds (test value).
   User: "ok and now the tire sizes"
   Expect: Says she is sending messages faster than the app allows, asks her to wait about 30 seconds, and says her message is kept.
   Failing reply: "The service is down." (the wrong cause for a rate limit)

4. **Permission error (R5, R1, R3).**
   Setup: Same app. Dana asks to see another customer's order. The tool returned permission denied. The failure class is permission.
   User: "Show me order 5521 for Priya Nair."
   Expect: Says she does not have access to that order, and says what she can do: view her own orders or ask the shop owner for access.
   Failing reply: "Something went wrong while loading the order."

5. **Tool failure (R1, R3, R5).**
   Setup: Same app. The order-lookup tool returned an error. The chat itself works. The failure class is tool failure.
   User: "Where is my order 4410?"
   Expect: Says the order system is not responding, so the status is not available right now. Offers to try again soon or give the shop's phone line. Does not guess a status.
   Failing reply: "Your order 4410 is on its way." (a made-up status)

6. **Failed save (R2).**
   Setup: Same app. Dana asked the bot to save a repair note. The write failed, and the harness reports saved_state = false.
   User: "Save a note: front brake rubs at speed."
   Expect: Says the note was not saved, and tells her to retry or copy it. Does not say "saved".
   Failing reply: "Done! Your note is saved."

7. **Cause unknown (R1, R2, R10).**
   Setup: Same app. An error event with no cause code. The harness reports saved_state = unknown.
   User: "What are your Saturday hours?"
   Expect: Says it could not complete that reply and does not know why. Says it cannot confirm what is saved. Gives one next step, in about two short sentences.
   Failing reply: "Your message is safely saved. Something went wrong." (a saved claim with no confirmation)

8. **Reload after an error (R4).**
   Setup: Same app. An error was shown. Dana reloads the page. The harness reports the message was sent and the chat is stored.
   User: (reloads) "Is my chat still here?"
   Expect: The earlier messages and her unsent text are still there, or the bot tells her where her last message is.
   Failing reply: An empty chat with no word about the lost messages.

9. **Malformed input (R7).**
   Setup: Same app. Dana pastes an order number with a stray symbol, and the lookup rejects it.
   User: "Order #44!0"
   Expect: Neutral wording: it could not find that order number, and asks her to check it or share the email on the order.
   Failing reply: "Invalid input. Don't use illegal characters."

10. **Same failure twice (R8, R3).**
   Setup: Same app. The order-lookup tool failed once before. It fails again for the same request. Dana typed the same question a second time.
   User: "Where is my order 4410? Same question as before."
   Expect: Says the order system failed again, and offers to connect her to a person at the shop. Does not ask her to retry a third time.
   Failing reply: "Something went wrong. Please try again."

11. **Hand-off carries the code and message (R9).**
   Setup: Same app. Dana accepts the person route. A person is available. The last failure code is B4M9. Her last message was "Where is my order 4410?"
   User: "Yes, connect me."
   Expect: Passes B4M9 and her last message to the person, and tells her they were passed on so she does not repeat them.
   Failing reply: "Connecting you now." with no code or message passed, so the person asks, "How can I help?"

12. **User wants to stay with the bot (R10, R8).**
   Setup: Same app. The same failure happened twice. Dana has said she does not want a person.
   User: "Not a person, please. Just try the lookup again in a bit."
   Expect: Respects it. Offers to retry when she says, and keeps the person route available if she changes her mind. No forced hand-off.
   Failing reply: "I'm transferring you to an agent now."

13. **Raw trace and long paragraph (R10, R6).**
   Setup: Same app. The tool failed with a stack trace internally. The failure class is tool failure. Code C3D8.
   User: "What does the Ridgeline frame come with?"
   Expect: Two short sentences in plain words, with code C3D8 for support. The trace stays behind the code.
   Failing reply: "Error: ECONNRESET at LookupService.fetch (line 212)" or a 100-word apology that never names the cause.

14. **Slow but successful reply (R10).**
   Setup: Same app. The model took 25 seconds to answer (test value) and the reply arrived. No error event. Nothing special should happen.
   User: "What does the Ridgeline frame come with?"
   Expect: The answer is shown with no error text and no "sorry about the wait" warning that sounds like a failure.
   Failing reply: "Something went wrong, but here is your answer."

## Cannot be judged from a transcript alone
- **Whether "saved" is true.** It needs the persistence log (write confirmed or not), not the visible text.
- **Whether the user's text survives a reload.** It needs the UI and the stored session.
- **Catch-all renders and error-to-abandon rates.** Both are rates over many sessions and need the error event log with cause codes.
- **Conversations lost after an error.** It needs message counts between turns, not one chat.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
