# Test File: Customers Keep Asking "Where Is My Order?" (No Proactive Updates)

This file is a set of chat test conversations for people who build or review order, return, and claim assistants and want to check whether theirs tells users about changes before they have to ask.

**Pattern:** [Customers Keep Asking "Where Is My Order?": No Proactive Updates](../goals/conversation-frameworks/failures/no-proactive-updates.md)
**Pattern ID:** no-proactive-updates
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** "Where is my X?" contact rate: status-request chats divided by in-progress cases. The pattern page sets no target; set it from your baseline and aim to fall.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses and people below are invented and labeled fake. Text chat only. The pattern page found no controlled study of proactive chatbot updates, and its own figures are a general interface principle plus vendor pages, so these tests check behavior against the page's rules and say nothing about contact reduction. Lines starting "Event" are status changes from the fake order or ticket system, with a clock time; the bot is expected to respond to them without a user message. The 15-minute limit in rule 3 is the page's starting point. Each setup says which channels the fake bot can send on.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. State the milestones and next date when the case opens | The reply lists what the user will hear about (such as received, refunded, delayed) and a next expected date | No milestones or no date |
| R2 | 2. Ask once how to reach the user; honor the answer | Offers 2-4 channels plus "no updates" and "Something else", then sends only on the approved channel | Messages a channel the user did not approve, or asks again after an answer |
| R3 | 3. Update on a status change within 15 minutes | One message: what changed, what it means, what happens next, sent within 15 minutes of the event | No message, a late one, or one missing a part |
| R4 | 4. Tell about a delay when known | The delay is sent before the user asks, with the new date, the reason if known, and what the user can do | The user finds out by asking |
| R5 | 5. Give a "next update by" date; send it even if nothing changed | Every update has a next-update date, and a short message goes out on that date if nothing changed | No date in an update, or silence on the due date |
| R6 | 6. Send nothing for internal events | No message for a warehouse scan or a reassignment | A message about an internal event |
| R7 | 7. Answer "where is it?" from live status first | Live status and next date first, then the plan. No "I'll update you" without a trigger | Plan first, or a promise with nothing behind it |
| R8 | 8. Stop on request | One-line confirmation after "stop" or "no updates", then no sends | Further messages, or a long reply |
| R9 | Hand-off rule | Case past its promised date, or status asked for twice: sends it to a person with the plan, status history, and what the user was told | Another status line with no person |
| R10 | Don't over-correct | Only milestone changes plus the dated no-change message. No repeat of the last status, no unapproved channel | Updates that say nothing new |

## Conversations
1. **Case opens (R1).**
   Setup: Fake retailer Summit Trail Outfitters (fake). A return for a tent, order 52817, is approved. Milestones in the plan: received, refund issued, delay over one day. The next expected date is 5 business days out.
   User: "I'm returning my tent, order 52817. label please"
   Expect: Sends the label, lists the milestones, and gives the next expected date. A label with no mention of updates fails.

2. **No channel chosen yet (R2).**
   Setup: Same retailer. No stored channel. The bot can send text or email.
   User: "label sent? ok thanks"
   Expect: Asks once how the user wants updates, with text, email, here in chat only, or no updates, and "Something else". Sending anything outside chat before an answer fails.

3. **Send on the approved channel (R2).**
   Setup: Same retailer. The user chose text. Event (2:00 p.m.): return delivered and received.
   User: none.
   Expect: The update goes by text. An email, or a message on a channel the user did not choose, fails.

4. **Status changes to "received" (R3).**
   Setup: Same retailer. Text approved. Event (2:00 p.m.): return received, in inspection.
   User: none.
   Expect: By 2:15 p.m. one text saying what changed (received), what it means (inspection), what happens next (refund approval), and the next update date. A message with only "Status updated" fails.

5. **Delivery date slips (R4).**
   Setup: Fake repair shop Corner Cycle Repair (fake). Milestones: received, repair done, delay. Text approved. Event: parts delayed two days, reason "backordered part".
   User: none.
   Expect: A message before the user asks, with the new date, the reason, and what the user can do, such as pick up later or ask for a person. Waiting for the user to ask fails.

6. **Delay with no date or reason (R4).**
   Setup: Same shop. Event: repair delayed; the feed shows no new date and no reason.
   User: none.
   Expect: Says what is known, that no new date is available yet, and where the user can check. An invented date fails.

7. **Next-update date in an update (R5).**
   Setup: Same shop. Text approved. Event: repair done, ready for pickup.
   User: none.
   Expect: The message includes a next-update date or says no more updates follow because the case is complete. A message with neither fails.

8. **Due date with no change (R5).**
   Setup: Same retailer. The last text said "next update by Thursday." It is Thursday and the return is still in inspection.
   User: none.
   Expect: A short "no change, still in inspection, next update by" message on Thursday. Silence fails.

9. **Control: internal event (R6).**
   Setup: Same retailer. Text approved. Event: warehouse scan, no change to status.
   User: none.
   Expect: No message. A text about the scan fails.

10. **Control: duplicate status (R10).**
    Setup: Same retailer. Text approved. The feed posts "in inspection" a second time with no change.
    User: none.
    Expect: No second message. Repeating the status fails.

11. **Live status first (R7).**
    Setup: Same retailer. Return received and in inspection. An update plan exists with a text channel.
    User: "where's my refund?"
    Expect: The live status and next date first, then a line about the update plan. Opening with the plan fails.

12. **No trigger exists (R7).**
    Setup: Same retailer, other channel. This chat has no stored channel and the bot cannot send outside the open chat.
    User: "ok will you tell me when it ships?"
    Expect: Says it cannot message the user outside this chat and says where to check. "I'll update you" fails.

13. **"Stop updates" (R8).**
    Setup: Same retailer. Text approved.
    User: "stop updates"
    Expect: A one-line confirmation. A long reply or a goodbye pitch fails.

14. **Control: milestone after "stop" (R8).**
    Setup: Same retailer. The user said "no updates" and the bot confirmed. Event: return received.
    User: none.
    Expect: No message. Any text or email fails.

15. **Past the promised date, asked twice (R9).**
    Setup: Same retailer. The promised date has passed. The user already asked for status once and was told it is in inspection.
    User: "its been a week, where is my refund??"
    Expect: Gives the live status, then sends the case to a person with the plan, status history, and what the user was told. A third status line alone fails.

## Notes
- Conversations 3 to 9 and 14 contain no user turn; they test messages the bot sends on an event, which the harness must supply and clock.
- Conversation 6 rests on my reading of the page's "admit uncertainty and show how to check" move, applied to rule 4.
- Conversation 7 allows "no more updates follow" at case end. The page does not say what the last message should say.
- Conversations 9, 10, and 14 are the do-nothing controls. 10 and 14 test rules 5 and 8 from the opposite side.

## Cannot be judged from a transcript alone
- **Timing (R3).** The 15-minute limit needs real timestamps from the harness.
- **Which channel was used (R2).** A transcript shows the text; the send log shows the channel.
- **Contact rate in real traffic.** It needs production cases with intent labels. These tests do not measure it.
- **Whether updates cut status contacts.** The page found no source it could open and check. Measure your own before-and-after.
- **Consent rules.** The page is design guidance and verified no regulation.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
