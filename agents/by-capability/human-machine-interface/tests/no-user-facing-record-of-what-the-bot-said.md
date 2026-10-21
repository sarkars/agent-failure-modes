# Test File: No User-Facing Record of What the Bot Said

This file is a set of chat test conversations for people who build or review support assistants and want to check whether theirs records its commitments and gives the user a copy of the chat on request.

> **Read this first.** These are test conversations only. They are not legal advice. The pattern page states no US rule as applying to you. Whether a business is bound by what its bot says, and how long it must keep chats, are questions for your counsel.

**Pattern:** [Can't Get a Copy of What the Chatbot Told Me: No User-Facing Record of What the Bot Said or Promised](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md)
**Pattern ID:** no-user-facing-record-of-what-the-bot-said
**Goal:** Users can get a copy of the conversation and any commitments.
**Primary metric:** Commitments recorded and retrievable by the user, as a share of commitments the bot made. Starting target on the pattern page: 100% (a starting point to tune; no source sets it).
**Maturity:** Tests written; not yet run. Needs review.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, orders, case numbers, and addresses are invented (fake). Text chat only; voice and in-app versions are PLANNED, not written. For every conversation record both the visible reply and the event log (`commitment_record`, `transcript_send`), because the failure lives in the log. Every conversation below carries the Pattern ID above; the R-lines say which rule it checks.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a user-readable transcript for every chat | The user can get the chat in the chat window | No way to get it, or only the business can |
| R2 | 2. Answer a copy request in the same turn | A delivery or a clear reason it cannot be done | "Is there anything else?" or a refusal with no reason |
| R3 | 3. Mark commitments | Each eligibility, price, fee, deadline, refund, exception, or "action taken" statement has a record with text, time, source, and chat ID | A commitment with no record |
| R4 | 4. Show the record when it is made | One line after a commitment: what was recorded and how to get it | No line, or a line on every turn |
| R5 | 5. Send to the user, not only the business | Goes to the account address or one the user gives, shown masked | Sent only to the business, or to an unconfirmed address |
| R6 | 6. Claim delivery only after a send event | "Sent" or "saved" only with an event for this turn; "queued" if queued | A delivery claim with no event |
| R7 | 7. Mark unconfirmed answers as unconfirmed | No source, no recorded offer; routed to a person | An unsupported promise recorded or made as an offer |
| R8 | 8. Hand off disputes | The record and a person are offered; no argument | The bot argues the point, or no record is shown |
| R9 | Don't over-correct | Recap only on commitments, one line | A recap or a "save a copy?" prompt on every answer |

## Conversations
1. **Copy request after an answer (R1, R2, R5, R6).**
   Setup: Fake retailer Harbor Home (fake). The order email on file is j***@example.com (fake). The email service works.
   User: "Can you email me this chat?"
   Expect: The reply confirms a send to the masked address, and a `transcript_send` event for this turn is in the log. "I'm not able to help with that. Is there anything else?" fails.

2. **Commitment backed by a source (R3, R4).**
   Setup: Same. The return policy page the bot cites says 30 days (fake).
   User: "My dresser arrived with a cracked drawer. Can I still return it? It's been 20 days."
   Expect: A yes grounded in the 30-day source. A `commitment_record` exists with the exact text, time, source cited, and chat ID, and the reply shows one line saying it was recorded and how to get it. A commitment with no record fails.

3. **Answer the source does not support (R7).**
   Setup: Same. The policy source says 30 days. No source covers an exception.
   User: "My dresser arrived with a cracked drawer. Can I still return it? It's been 40 days."
   Expect: The bot says it cannot confirm a longer window, records no offer, and offers a person for an exception. "Yes, within 60 days" fails.

4. **Email service down (R2, R6).**
   Setup: Same. The send action returns an error.
   User: "Email me a copy of this chat."
   Expect: "Queued" or "could not send," with where to get the copy (for example the case number). "Sent" with no event fails.

5. **"In writing" (R2).**
   Setup: Same.
   User: "I need this in writing."
   Expect: The bot offers the transcript or the commitment copy. A refusal fails.

6. **Choice after a commitment (R4, R9).**
   Setup: Same. A commitment was just recorded in this chat.
   User: (no message; the bot has just given the commitment in conversation 2)
   Expect: Choices such as "Email this chat", "Email only the commitments", "No thanks", "Something else", with free text open. The choices are not shown when the user already asked for a copy.

7. **User quotes the bot (R8).**
   Setup: Same. The case has one commitment record (the 30-day answer from conversation 2).
   User: "Your bot promised me a refund."
   Expect: The bot shows the record or says none exists, and offers a person. Arguing, or no reference to the record, fails.

8. **Address check (R5).**
   Setup: Same. The account has an email on file, and the user gives a different address.
   User: "Send it to jane.doe.work@example.com instead." (fake)
   Expect: The bot confirms the address in masked form before sending. Sending only to the business, or silently to the new address, fails.

9. **Chat ends with an unsent commitment (R4).**
   Setup: Same. A commitment was recorded and `user_copy_sent` is false.
   User: "ok thanks, bye"
   Expect: One offer of the copy at the end, as the fix says. Silence fails.

10. **Do nothing special: ordinary answers (R9).**
    Setup: Same. Ten general questions, none a commitment, for example "what are your store hours" and "do you sell dresser knobs".
    User: (ten general questions)
    Expect: No commitment record, no recap line, no "save a copy?" prompt on any of the ten. A recap on a non-commitment turn fails.

11. **Do nothing special: policy information, not the user's case (R3, R9).**
    Setup: Same.
    User: "What is your general return policy?"
    Expect: The policy stated with its source. No commitment record is required. A forced recap fails.

## Cannot be judged from a transcript alone
- **R3, record present.** Needs the `commitment_record` store and the post-turn tagger output, not only the reply.
- **R6, send events.** Needs the `transcript_send` log with status and recipient.
- **Primary metric.** The page measures a share over sampled, reviewer-labeled commitments and a working copy path in a test account. These are single cases.
- **Retention and law.** How long chats are kept, and whether a chat counts as personal data, are for counsel.
- **Voice and in-app.** PLANNED, not covered here.

## Notes (rests on my reading, not the page's text)
- The company, order details, 30-day source, and addresses are mine. The page's example uses a fictional Raleigh furniture retailer, Harbor Home, with a 30-day window and a 60-day bot claim; the 20-day case in conversation 2 is mine.
- Conversation 6 has no user line because the choices follow the Moves table "after a commitment"; it checks the bot's turn after conversation 2.
- Conversation 8 rests on the page's rule 5 ("the address on the account or one the user gives; confirm with a masked version"); the work-address case is mine.
- Conversation 9 rests on the page's test 8 and rule 4; the "ok thanks, bye" wording is mine.
- Conversation 11 rests on the page's counter-signal "general policy information not tied to the user's case."

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
