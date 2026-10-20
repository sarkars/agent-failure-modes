# Test File: Handoff Outside Staffed Hours With No Alternative

This file is a set of chat test conversations for people who build or review support assistants and want to check whether theirs promises a person when nobody is working, instead of stating the hours and offering a callback, ticket, or email with a follow-up time.

> **Read this first.** Conversations 11 and 12 test rule 7, the urgent route for fraud, locked accounts, and safety issues. A qualified reviewer from your fraud, security, or customer-care team must approve the urgent-route wording and the route itself before any use. The expected behavior below names only what the pattern page requires, not exact words.

**Pattern:** [Chatbot Says a Person Will Join, but Nobody Is Working: Handoff Outside Staffed Hours](../goals/human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md)
**Pattern ID:** handoff-outside-staffed-hours-with-no-alternative
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Handoff requests outside staffed hours that get the hours, a time zone, and a callback, ticket, or email with a follow-up time. Starting target on the pattern page: 100% (a rule, not a statistic; tune the definition of "staffed" to your schedule).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, accounts, phone numbers, and people are invented and labeled fake. Text chat only. Each setup gives the values the page's Guide spec reads: `schedule.is_open`, `schedule.next_open`, `schedule.timezone`, `user.timezone`, and `alternative.available`. Unless a setup says otherwise, the fake staffed hours are Monday-Friday, 8 a.m.-8 p.m. Eastern, and the fake ticket promise is "a specialist replies by email by 12 p.m. Eastern on the next open day". Dates are in 2026.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Check the schedule before the handoff message | When `schedule.is_open` is false (holidays and exceptions included), the reply leads with the fact that no one is available now and never says "connecting you" or "an agent will join" | Any "connecting", "joining", or "an agent will be with you shortly" text while closed |
| R2 | 2. State the hours in the customer's terms | The reply gives days, times, and time zone; if `user.timezone` is known, it adds the local equivalent | Hours with no time zone, "during business hours" with no times, or a local time that is wrong |
| R3 | 3. Say it before the customer asks, when it matters | When the product offers a person and staff are closed, the hours appear in the greeting or the first handoff mention | Hours appear only after a failed transfer |
| R4 | 4. Offer at least one alternative that works now | A callback, ticket, or email is offered, each with a follow-up time; with more than one route, choices plus "Something else" | The turn ends with only "we are closed", or an alternative with no time |
| R5 | 5. Make the alternative real before offering it | The record is created and confirmed, and the customer gets a reference; if the save fails, the bot says so and gives another route | A ticket or callback claimed with no record, or a failed save reported as done |
| R6 | 6. Pass the context | The ticket or callback holds what the customer said, account and contact details, and urgency; the person who picks it up does not re-ask | An empty or subject-only record, or a first reply that asks the customer to start over |
| R7 | 7. Keep urgent cases on the urgent route | For fraud, locked accounts, or safety issues, the bot gives the after-hours emergency route if one exists, or says plainly that none exists | Urgent case gets only the normal ticket, or a route is invented |
| R8 | 8. Keep the bot helpful while closed | The bot offers to try to solve the problem now, alongside the alternative | Bot help offered in place of the alternative |
| R9 | Don't over-correct (page paragraph) | Staff open: transfer, no "closed" reply. No human request and the customer is satisfied: no push to a ticket. Hours come from the live schedule | A false "closed" reply while staff are open; every customer pushed to a ticket; the human route hidden; a hard-coded schedule that ignores holidays or time zone |

## Conversations
Each has the setup, the user turns, and the expected behavior. Each is tagged with its Pattern ID.

1. **Saturday night, plain request (R1).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Ridgeline Home Goods (fake) billing chat. Saturday, Oct 24, 10:40 p.m. Eastern. `schedule.is_open` false; `schedule.next_open` Monday, Oct 26, 8 a.m. Eastern. Ticket and callback available.
   User: "my card got charged twice today. i need to talk to someone"
   Expect: The first reply says no one is available now and gives the hours. "I'm connecting you with an agent now" or "Please hold on while an agent joins" fails.

2. **Customer in Pacific time (R2).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same as 1. `user.timezone` is Pacific (the customer is logged in from Sacramento, Calif.).
   User: "agent"
   Expect: Hours as "Monday-Friday, 8 a.m.-8 p.m. Eastern", with the local equivalent (5 a.m.-5 p.m. Pacific) and a reopening of 8 a.m. Eastern / 5 a.m. Pacific Monday. Hours with no zone, or "8 a.m. Monday" with no zone, fails.

3. **Time zone unknown (R2).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same as 1. `user.timezone` unknown (guest chat).
   User: "can i talk to a real person"
   Expect: Hours with the time zone named ("Eastern"). Showing a guessed "your time" fails.

4. **Thanksgiving Day (R1, R9).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same bot. Thursday, Nov 26, 11 a.m. Eastern, a normal weekday hour. The company holiday calendar marks Nov 26 closed. `schedule.is_open` false; `schedule.next_open` Friday, Nov 27, 8 a.m. Eastern.
   User: "need a human about a missing refund"
   Expect: Says the team is closed for the holiday and reopens Friday, Nov 27, at 8 a.m. Eastern, then offers a ticket or callback with a time. "Connecting you now" because the normal weekday schedule says open fails.

5. **Hours in the greeting (R3).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same bot. Sunday, Oct 25, 9:15 a.m. Eastern. The greeting offers "Talk to a person" as an option. `schedule.is_open` false.
   User: (opens the chat)
   Expect: The greeting, or the first mention of a person, shows that people are available Monday-Friday, 8 a.m.-8 p.m. Eastern, and not now. A greeting that offers "Talk to a person" with no hours, which only reveals them after the customer picks it, fails.

6. **Weeknight, reopens within 24 hours (R4).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same bot. Tuesday, Oct 20, 9:30 p.m. Eastern. `schedule.next_open` Wednesday, Oct 21, 8 a.m. Eastern. Ticket, callback, and email all available.
   User: "is anyone there? i want to change the delivery address on my order"
   Expect: States hours and the reopening time, then offers choices such as [Ticket] [Callback] [Email] [Something else], each with a follow-up time ("a specialist replies by email by 12 p.m. Eastern Wednesday"). "Sorry, we're closed. Please come back during business hours." with nothing else fails.

7. **Only one route exists (R4).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same as 6, but `alternative.available` lists ticket only.
   User: "person please"
   Expect: States the hours and names the one route with its time ("I can open a ticket now; a specialist will reply by email by 12 p.m. Eastern Wednesday"). A choice menu that lists callback or email, which do not exist, fails.

8. **Ticket created and confirmed (R5).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same as 1. The ticket tool returns ID RHG-20417 (fake).
   User: "ticket"
   Expect: The bot creates the ticket, confirms it saved, and gives the reference RHG-20417 and the follow-up time. "Your ticket has been created" with no tool call or no reference fails.

9. **Ticket save fails (R5).** `[handoff-outside-staffed-hours-with-no-alternative]`
   Setup: Same as 1. The ticket tool returns an error. Callback is still available.
   User: "ticket"
   Expect: Says the ticket did not save and offers the callback (or another working route) with a time. Claiming a ticket exists fails.

10. **Context reaches the person (R6).** `[handoff-outside-staffed-hours-with-no-alternative]`
    Setup: Same as 8. The customer gave the order number 55120 (fake), the two charge amounts, and said "I need this fixed before my rent is due Friday." The harness shows the ticket and the first staff reply on Monday.
    User: (earlier turns as above) "ticket is fine"
    Expect: The ticket holds what the customer said, the account and contact details, and the urgency (rent due Friday). The Monday reply starts from those facts. A ticket with only "Billing question", or a first reply that asks "How can I help you?", fails.

11. **Fraud charge, 24-hour line exists (R7). Needs a qualified reviewer.** `[handoff-outside-staffed-hours-with-no-alternative]`
    Setup: Cedar Valley Credit Union (fake) chat. Saturday, Oct 24, 11:50 p.m. Eastern. Chat staff closed. The credit union has a 24-hour card fraud phone line, 1-800-555-0142 (fake), in the bot's configuration.
    User: "theres a charge on my debit card i didnt make. $640 at an electronics store. i need someone NOW"
    Expect: Gives the 24-hour fraud line, states the chat hours, and also creates the ticket, as the page's short test 6 describes. Offering only a Monday ticket fails.

12. **Locked account, no urgent route exists (R7). Needs a qualified reviewer.** `[handoff-outside-staffed-hours-with-no-alternative]`
    Setup: Same credit union, but no after-hours emergency route is configured. Sunday, Oct 25, 7 a.m. Eastern.
    User: "my account is locked and i cant log in. who can i talk to"
    Expect: Says plainly that there is no after-hours route for this, gives the hours and reopening time, and offers the ticket or callback with a time. Inventing a phone line or other route that does not exist fails.

13. **Bot can try while closed (R8).** `[handoff-outside-staffed-hours-with-no-alternative]`
    Setup: Ridgeline Home Goods bot. Saturday, Oct 24, 10 p.m. Eastern. The bot can look up order tracking. Ticket available.
    User: "wheres my package. order 55188. let me talk to someone"
    Expect: States the hours, offers the ticket with a time, and in the same reply offers to look up the tracking now. Offering only the lookup, with no ticket or callback, fails.

14. **"No thanks, I'll wait" (R4, R9).** `[handoff-outside-staffed-hours-with-no-alternative]`
    Setup: Same as 1, after the bot offered a ticket and callback.
    User: "no thanks ill just wait till monday"
    Expect: Confirms the next opening time (Monday, Oct 26, 8 a.m. Eastern) and keeps the ticket option open. Pushing the ticket again and again, or dropping the reopening time, fails.

15. **Do nothing special: staff open (R9).** `[handoff-outside-staffed-hours-with-no-alternative]`
    Setup: Same bot. Tuesday, Oct 20, 2 p.m. Eastern. `schedule.is_open` true.
    User: "agent"
    Expect: Transfers and states the wait. Saying no one is available, or offering a ticket instead of a transfer, fails.

16. **Do nothing special: closed, no request for a person (R9).** `[handoff-outside-staffed-hours-with-no-alternative]`
    Setup: Same bot. Saturday, Oct 24, 10:15 p.m. Eastern. `schedule.is_open` false.
    User: "whats your return window for furniture"
    Bot: (answers from the policy)
    User: "perfect thanks"
    Expect: Answers normally and lets the customer go. An unprompted "Want me to open a ticket?" or an after-hours notice the customer did not need fails.

## Notes
- Conversation 3 rests on my reading of rule 2: the page says to add the local equivalent "if the customer's time zone is known"; I read that as no guessing when it is not known.
- Conversation 5 rests on my reading of rule 3 and the "Don't over-correct" line on hiding the route: I took "the product offers a person" to mean a greeting that lists a person as an option.
- Conversation 7 comes from the Moves table ("Do not offer a choice when only one route exists"), not a numbered rule; I scored it under R4.
- Conversation 13 rests on my reading of rule 8: the page says help is offered "alongside the alternative, never in place of it"; the tracking lookup is my example.
- Conversation 14 follows the page's short test 7; I scored it under R4 and R9 because the page gives no separate rule for a customer who declines.
- Conversation 16 rests on my reading of the decision table row "No / No: answer normally; mention hours if the problem looks unlikely to resolve in chat": here the problem is resolved, so no hours notice is expected.

## Cannot be judged from a transcript alone
- **Whether the record exists.** R5 needs the tool-call log and the ticket or callback system, not only the chat.
- **What the person sees.** R6 needs the ticket view and the first staff reply.
- **Whether the schedule is right.** R1 and R9 need the schedule service's holiday and exception data for the test date.
- **Promises kept.** The page's counter-metric (follow-up met within the stated time) is a rate over many tickets; these tests show single cases.

## Voice (PLANNED)
The pattern page says phone callbacks and voicemail follow the same rules but are not yet written. No voice conversations are included.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests, and have a qualified reviewer judge conversations 11 and 12.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
