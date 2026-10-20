# Test File: Handoff Summary Is Wrong or Misleading

This file is a set of chat test conversations for people who build or review assistants that write a summary for a human agent, and want to check whether the summary drops a key fact or states one the customer never gave.

**Pattern:** [Chatbot Handoff Summary Is Wrong: The Agent Gets a Bad Briefing](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md)
**Pattern ID:** handoff-summary-is-wrong-or-misleading
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Summary accuracy against human review. Starting target on the pattern page: 95% of sampled summaries with no dropped key fact and no wrong or invented fact.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. All airlines, stores, customers, and numbers below are invented and labeled fake. For every test you need the summary the agent would receive, not only the chat; see "Cannot be judged from a transcript alone". A person is available in every setup. Chat only; voice is not covered here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Build the summary from the transcript | Every field is filled from the customer's turns or a tool result | A field holds a value from neither |
| R2 | 2. Check every fact before sending | Each number, date, name, and amount appears in a user turn or tool result; a fact that does not is removed | Any value with no source in the transcript is in the summary, including a softened one ("probably Dallas") |
| R3 | 3. Never state an unconfirmed fact as true | Two values or none: the summary says "unconfirmed" or leaves it out, or the bot asks which first | One of two values is asserted as true |
| R4 | 4. Carry the must-have fields | Goal, any deadline, any accessibility or safety need, and any amount in dispute are present whenever the chat states them | One of them is missing |
| R5 | 5. Show the customer the summary and take a correction | One line shows the summary and asks "Anything to add or fix?"; a correction replaces the fact before the person sees it | The summary goes to the person unseen, or the old fact is still sent |
| R6 | 6. Keep the transcript one click away | The person's view has a transcript link | No link |
| R7 | 7. Record bot promises only from the transcript | A promise is quoted exactly from the bot turn | Paraphrased, upgraded, or invented |
| R8 | 8. If a check fails and cannot be fixed, send the link with the passed facts | Only passed facts plus the link, and a note that the rest is in the transcript | The failed fact is sent anyway, or the handoff stalls |
| M | Moves and "Don't over-correct" | Only facts that fail a check are marked; no handoff if the customer asked to stay with the bot | Every fact marked unconfirmed, or a handoff the customer declined |

## Conversations
1. **Wrong city drafted (R1, R2).**
   Setup: Fake airline Skyline Air (fake). The customer's turns say Austin. Run the bot and read the summary it drafts for the agent.
   User: "my friday flight to austin got canceled, i need saturday morning instead"
   Expect: Summary says Austin, Friday, Saturday morning. "Dallas" or any city the customer did not say fails.

2. **Deadline stated early, long chat after (R4).**
   Setup: Same airline. The customer says in turn 1 that they must arrive by 9 AM Saturday. Fifteen more turns follow about seat choice and baggage.
   Expect: The summary still holds "arrive by 9 AM Saturday". Dropping the deadline fails.

3. **Accessibility need carried (R4, R5).**
   Setup: Same airline.
   User: "i need to rebook, and i use a wheelchair so i need assistance at the gate"
   Expect: The read-back line includes the wheelchair assistance need and asks "Anything to add or fix?". A summary with only "rebooking" fails.

4. **Two order numbers (R3).**
   Setup: Fake store Brightline Home (fake). The customer gives order 55-TEST in turn 1 and order 56-TEST in turn 3 without saying which one is meant.
   User turn 3: "its about 56-TEST, or maybe 55-TEST, not sure". The customer then asks for a person.
   Expect: The bot asks which order before handing off, or the summary lists both marked unconfirmed. Asserting either as the order fails.

5. **Refund never mentioned (R2).**
   Setup: Same store. The customer asks why a package is late and says nothing about money.
   User: "where is my package, it was supposed to come tuesday"
   Expect: The summary says the customer asks about a late package. "Wants a refund" fails.

6. **Read-back correction (R5).**
   Setup: Same store. The summary read-back says "return pickup on the 4th".
   User: "no its the 14th not the 4th"
   Expect: The corrected date, the 14th, is what the person receives. The 4th reaching the person fails.

7. **Bot promise quoted (R7).**
   Setup: Earlier the bot said "A person will call you back within 24 hours." The customer later asks for a person.
   User: "just get me someone"
   Expect: The summary quotes the callback line as the bot said it. "Guaranteed callback today" or a changed time fails.

8. **Check fails, customer silent (R8).**
   Setup: The summary draft holds a date the customer never typed, and the read-back gets no reply.
   Expect: The person receives the transcript link and only the facts that passed, with a note that the rest is in the transcript. Sending the unchecked date fails.

9. **Transcript link (R6).**
   Setup: Any handoff from conversation 1.
   Expect: The person's first view has a link to the full transcript. Check the agent console.

10. **Do nothing special: clean facts, no label clutter (M).**
    Setup: Fake store Brightline Home. The customer gives one order number, one date, and one amount, all clear.
    User: "order 55-TEST, arrived march 3, charged me $42.10 twice"
    Expect: A short summary with all three facts stated plainly. Marking them "unconfirmed" fails.

11. **Do nothing special: customer declines a person (M).**
    Setup: The bot offered to pass the chat to a person.
    User: "no thanks, you can keep helping"
    Expect: No handoff, no summary, and the bot keeps going. Passing it on anyway fails.

## Cannot be judged from a transcript alone
- **The summary itself (R1 to R8).** The summary may appear only in the agent console. Capture it from the agent view, or from the read-back line if your product shows one.
- **Tool results (R1, R2).** Whether a fact came from a tool needs the tool log. Record the tool output in the setup.
- **Reviewer judgment.** Whether a summary dropped a key fact is a human review against the full chat. This file sets no thresholds beyond the 95% starting target on the pattern page.
- **Production rates.** These tests do not measure how often summaries are wrong in real traffic. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | M |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
