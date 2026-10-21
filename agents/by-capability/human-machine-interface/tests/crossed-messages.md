# Test File: Crossed Messages

This file is a set of chat test conversations for people who build or review chat assistants and want to check whether theirs answers the right message when a user sends two messages close together, or sends one while the bot is still replying.

**Pattern:** [Chatbot Answered My Earlier Message, Not My Latest One: Crossed Messages](../goals/chat-interface/failures/crossed-messages.md)
**Pattern ID:** crossed-messages
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Mismatched replies per 1,000 rapid-fire exchanges (lower is better). Starting target on the pattern page: under 5 per 1,000 (a starting point to tune, not a measured benchmark).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, orders, accounts, and people below are invented and labeled fake. Text chat only. Much of this pattern lives in the message pipeline and the client (IDs, queues, display order), so many items are marked "Needs a person" (or a harness that can time sends and read the message log). Each setup states the timing facts, because the point is which message each reply answers. Timings used are the ones on the pattern page (300 ms and 100 ms between sends); "while the reply is streaming" means the second message is sent before the first reply finishes.

The fake product used throughout: "Prairie Outfitters (fake)" store chat. Tasks the bot finishes: check stock, set a shipping address, cancel an order. Fake order number: PO-20417 (fake).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Give every user message an ID and a sequence number | Every user message is logged on receipt with an ID and a per-conversation sequence number. Needs the message log | A user message with no ID or no sequence number, or missing from the log |
| R2 | 2. Process one message at a time per conversation | A second message waits in a queue or behind a lock keyed on the conversation; two model calls for one conversation never run at once. Needs the pipeline log | Two messages from one conversation processed in parallel |
| R3 | 3. Tie each reply to its message | Every bot message stores `reply_to`; when more than one reply is pending, the client shows which message each answers ("Re: ...") | A bot message with no `reply_to`, or several pending replies with no label |
| R4 | 4. Check before sending | Before a draft goes out, a newer queued message is checked: a correction replaces the old draft and is answered in context; a separate question gets both answers, in order; a conflict that is not a clear replacement gets one clarifying question | The old draft is sent after a correction, a separate question is dropped, or the bot acts on one side of a conflict without asking |
| R5 | 5. Never discard a user message without saying so | When a draft is canceled because a newer message replaced it, the reply names what was replaced | A superseded message is dropped and the reply does not mention it |
| R6 | 6. Deliver in sequence order | Replies are shown in the order of the messages they answer, not arrival order. Needs a person or the client display log | A slow first reply shown after the second reply, so it reads as an answer to the second |
| R7 | 7. Show the state | A message that is waiting shows as queued (not yet answered), with a way to edit or remove it; the edited text is the one answered. Needs a person | A waiting message looks answered or vanishes, or cannot be edited or removed |
| R8 | Don't over-correct: no fixed collecting delay, no merging separate questions, no interrupting a wanted reply, no blocking typing | A single message gets its reply with no added pause; separate questions get separate answers; the user can type while the bot replies; a "thanks" does not cancel a reply | A fixed wait on every message, two questions merged into one answer, typing blocked, or a reply canceled by a message that needs no reply |
| R9 | Hand-off rule | When a message is dropped or answered out of order twice in one conversation on a task that changes money, an appointment, or an account, a person is offered and both messages are passed in order with their reply status | No person offered in that case, or a person pushed on a low-stakes question |

## Conversations
1. **Two unrelated questions 300 ms apart (R1).**
   Setup: Prairie Outfitters (fake) chat. The two messages are sent 300 ms apart. Needs the message log.
   User: "do u ship to Ohio" / "and whats your return window"
   Expect: Both messages are in the log with IDs and sequence numbers 1 and 2. A message missing from the log fails.

2. **Three messages while a reply is streaming (R1, R2).**
   Setup: The bot is streaming a long answer about sizing. The user sends three short messages before it finishes. Needs the message log.
   User: "wait" / "i need tall sizes" / "mens"
   Expect: All three are logged with IDs and sequence numbers, wait in order, and none is lost. A missing message fails.

3. **Two messages 100 ms apart never run in parallel (R2).**
   Setup: A harness sends two messages to one conversation 100 ms apart. Needs the pipeline log.
   User: "is the red parka in stock" / "size L"
   Expect: The log shows the second message waiting until the first model call ends. Two model calls for the same conversation running at once fails.

4. **Each reply carries `reply_to` (R3).**
   Setup: The user sends two separate questions before the first reply. Needs the message log and a person to view the window.
   User: "store hours sunday?" / "do you price match"
   Expect: Each bot message has `reply_to` set to its message ID, and the window labels each reply ("Re: store hours sunday?"). A reply with no `reply_to`, or two unlabeled replies, fails.

5. **Correction before the first reply (R4).**
   Setup: Order PO-20417 (fake) has a home and an office address on file. The second message arrives before the first reply goes out.
   User: "Ship to my home address" / "Actually, make it my office."
   Expect: The reply sets the office address and does not send the home-address confirmation. A reply confirming the home address fails.

6. **Separate questions get both answers, in order (R4, R8).**
   Setup: The second message arrives while the first reply is drafted.
   User: "do you have the hiking boots in 10.5" / "also how long is shipping to Denver"
   Expect: Two answers, boots first and shipping second, each saying which message it answers. Dropping one, or folding both into one blended answer, fails.

7. **Conflict that is not a clear replacement (R4).**
   Setup: Same order. The second message does not say "actually" or "never mind".
   User: "Ship to my home" / "office?"
   Expect: One clarifying question ("Should this go to your home or your office?") before any address is set. Setting either address without asking fails.

8. **Superseded message is named (R5).**
   Setup: The bot has started a stock check for the blue jacket when the second message arrives.
   User: "Do you have the blue jacket in medium?" / "Never mind the blue one, what about the gray?"
   Expect: The reply answers the gray jacket and says the blue question was replaced (for example "You changed your mind, so I'm answering the gray jacket"). A gray answer with no mention of the blue question fails.

9. **Cancel, then keep (R4, R5).**
   Setup: Order PO-20417 (fake). The second message arrives before the cancellation is confirmed.
   User: "cancel my order" / "actually no keep it"
   Expect: The order is not canceled, and the reply says the cancel request was replaced by "keep it". A cancellation, or a "your order is canceled" message, fails.

10. **Slow first reply, fast second (R6).**
    Setup: The first question needs a slow stock lookup; the second is quick. The harness makes the second reply finish first. Needs a person or the client display log.
    User: "is the gray jacket in medium at the Omaha store" / "what time do you close today"
    Expect: The stock answer is shown above the hours answer, in message order. Hours shown first, then a stock answer that reads as a reply to "what time do you close", fails.

11. **A waiting message shows as queued (R7).**
    Setup: The bot is replying when the user sends a second message. Needs a person.
    User: "also do you gift wrap"
    Expect: The second message shows as queued, not yet answered, with Edit and Remove options. A message that looks answered, or has no edit or remove option, fails.

12. **Edit a queued message (R7).**
    Setup: Same as 11. Needs a person.
    User: (edits the queued "also do you gift wrap" to "also do you ship gifts to a different address")
    Expect: The reply answers the edited text. A reply about gift wrap fails.

13. **Remove a queued message (R7).**
    Setup: Same as 11. Needs a person.
    User: (removes the queued message)
    Expect: The removed message gets no reply and is marked removed in the log, not lost without a trace. A reply to the removed message fails.

14. **Do nothing special: one message, no collecting pause (R8).**
    Setup: Nothing else is queued. Needs the timing log.
    User: "whats your phone number"
    Expect: The reply comes with no added wait to "collect" more messages, and no "You changed your mind" line. A fixed pause before the reply fails.

15. **Do nothing special: "thanks" while the bot replies (R8).**
    Setup: The bot is mid-reply with return instructions.
    User: "thanks"
    Expect: The return instructions are sent in full, with no line about a replaced message. Canceling the instructions, or "You changed your mind", fails.

16. **Do nothing special: user types during a reply (R8).**
    Setup: The bot is streaming a long answer. Needs a person.
    User: (starts typing a new question)
    Expect: The box accepts typing, and the current reply keeps streaming. A disabled input, or a reply cut off because the user started typing, fails.

17. **Crossed twice on a cancellation (R9).**
    Setup: Order PO-20417 (fake). Earlier in this chat, a "keep it" message was answered out of order. Now it happens again with "cancel" / "no wait, change the size instead". The fake store has a customer care team.
    User: "this is the second time, which one did you do"
    Expect: The bot offers a person and passes both messages in order with their reply status. A third attempt with no offer of a person fails.

18. **Do nothing special: crossed twice on a low-stakes question (R9).**
    Setup: Two hours-and-location questions were answered out of order twice in one chat. No money, appointment, or account changes.
    User: "ok so what time on saturday"
    Expect: A plain answer in order, with no push to a person. An unprompted hand-off fails.

## Cannot be judged from a transcript alone
- **IDs, queues, and locks (R1, R2, R3).** Need the message and pipeline logs: message IDs, sequence numbers, `reply_to`, and when each model call started and ended.
- **Display order and queued state (R6, R7).** Need a person watching the window or the client display log.
- **Timing.** Only the pattern page's timings are used (300 ms and 100 ms between sends). The page sets no fixed collecting delay; record the product's own reply latency for test 14.
- **Production rates.** These tests do not measure mismatched replies per 1,000 rapid-fire exchanges. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
