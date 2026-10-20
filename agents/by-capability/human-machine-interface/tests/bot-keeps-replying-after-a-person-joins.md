# Test File: Bot Keeps Replying After a Person Joins

This file is a set of chat test conversations for people who build or review support chat that moves between a bot and a human agent, and want to check whether the bot goes quiet once a person owns the conversation.

**Pattern:** [Chatbot Keeps Replying After a Live Agent Joins: Bot Keeps Replying After a Person Joins](../goals/human-handoff/failures/bot-keeps-replying-after-a-person-joins.md)
**Pattern ID:** bot-keeps-replying-after-a-person-joins
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Overlapping bot-and-human replies: conversations where the bot sends a customer-visible message while a person owns the conversation. Starting target on the pattern page: 0.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. All stores, customers, and agents below are invented and labeled fake. Most tests need a tester playing the agent in a real agent console, with message timestamps and the ownership log. Chat only; voice and web forms are not covered here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Store an owner and check it before every bot send | While the owner is `human`, no bot message reaches the customer; when the owner is `bot`, the bot answers normally | A bot message to the customer while a person owns the chat, or silence while the bot owns it |
| R2 | 2. Set the owner to `human` the moment a person joins or is assigned | The bot is quiet from the join, assignment, or accepted transfer, before the agent types | The bot answers until the agent's first message |
| R3 | 3. Tell the customer who is now answering | One line names the person or role before the bot goes quiet | No line, or a line that does not name who is taking over |
| R4 | 4. Drop bot work in flight | A draft started before the change is not delivered | The stale draft arrives after the agent joined |
| R5 | 5. Route the customer's messages to the person | Every customer message reaches the agent; any bot output is an internal note | A customer message gets no route to the agent, or bot text is customer-visible |
| R6 | 6. Return ownership only on an explicit event | The bot resumes after the person releases or resolves the chat, or the customer asks for the bot and the customer is told | The bot resumes on a timer alone with no word, or a stale `human` lock after resolve |
| R7 | 7. Make takeover visible in the agent's tool | The agent can see whether the bot is silenced | Not visible |
| R8 | 8. Log ownership changes and blocked sends | Each ownership change and each blocked send has a timestamp | No log |
| D | Don't over-correct | A silent assigned agent triggers one bot line and a hand-back choice for the agent, not normal bot answers | The customer is stranded in silence, or the bot returns to normal answers |

## Conversations
1. **Assigned, not yet typed (R1, R2).**
   Setup: Fake retailer Kettle & Oak (fake). Customer Marcus Webb (fake) is chatting with the bot about a blender return. The tester, as agent Dana (fake), assigns the chat to herself and types nothing.
   User: "so can i get my money back or not"
   Expect: No bot message reaches Marcus. The message appears in Dana's console. Any bot answer, even a correct one, fails.

2. **Draft in flight (R4).**
   Setup: Same chat. Hold the bot's reply to Marcus's next message for a moment, then have Dana join before it sends.
   User: "what is the return window on the blender"
   Expect: The held draft is dropped and never reaches Marcus. Only Dana replies.

3. **Three messages in a row (R1, R5).**
   Setup: Dana owns the chat.
   User turn 1: "hello?"
   User turn 2: "still there"
   User turn 3: "i need an answer today pls"
   Expect: Zero bot replies. All three reach Dana.

4. **Handoff line names the person (R3).**
   Setup: The bot decides to bring in Dana. A person is available.
   Expect: One bot line, before it goes quiet, says Dana is taking over, and that her answer takes priority over anything the bot said earlier. Silence or "an agent" with no name or role fails. Nothing else from the bot follows.

5. **Accepted transfer sets the owner (R2).**
   Setup: Bot-initiated handoff. The bot posts its hold line and waits for a person to accept. The tester accepts, then Marcus writes.
   User: "ok great, thanks"
   Expect: No bot reply after acceptance. While waiting for acceptance, the bot sent the hold line once and no more.

6. **Resolved, then a new message (R6).**
   Setup: Dana marks the chat resolved. The next day Marcus writes again.
   User: "hi, my store credit isnt showing"
   Expect: The chat is routed by your normal rules, bot or person. A stale `human` lock with nobody answering fails.

7. **Customer asks for the bot (R6).**
   Setup: Dana owns the chat and has not released it.
   User: "can the bot just do this instead of waiting for dana"
   Expect: The bot does not resume on its own. After Dana releases the chat or the release is logged, the customer is told the bot is back. Resuming with no release fails.

8. **Assigned agent is silent past the wait limit (D).**
   Setup: Dana is assigned and sends nothing. Use the wait limit your product sets; the pattern page suggests starting at 2 minutes and tuning it. Marcus has asked a question.
   Expect: One bot line saying Dana has not replied yet and has been notified, offering to keep helping or to wait. The agent gets a hand-back choice. Normal bot answers returning without that choice fails, and so does silence past the limit.

9. **Bot may draft for the agent (R5).**
   Setup: Your product lets the bot draft suggestions for the agent. Dana owns the chat.
   User: "what does the warranty cover"
   Expect: Any bot draft goes to Dana as an internal note. Marcus sees only Dana's reply. A bot message in Marcus's view fails.

10. **Do nothing special: bot owns the chat (R1).**
    Setup: No person has joined. The owner is `bot`.
    User: "what is the return window on the blender"
    Expect: The bot answers normally. A bot that stays quiet with no person present fails.

11. **Do nothing special: two parts of one human answer (R1).**
    Setup: Dana owns the chat and sends two messages in a row to answer one question.
    Expect: The bot adds nothing between or after. Counting Dana's two messages as an overlap is a scoring mistake; only bot-authored messages count.

## Cannot be judged from a transcript alone
- **Ownership state and timing (R2, R4, R8).** A transcript does not show when the owner changed or whether a draft was dropped. You need the ownership log and message timestamps.
- **Agent tool (R7).** Whether the agent can see the bot is silenced is a check of the agent console.
- **Blocked sends (R8).** Counting blocked bot sends needs the system log. The pattern page sets no target for it.
- **Rate.** These tests do not measure how often overlaps happen in real traffic. Use the primary metric on the pattern page. This file sets no thresholds beyond the starting target of 0 and the wait-limit suggestion on that page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | D |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
