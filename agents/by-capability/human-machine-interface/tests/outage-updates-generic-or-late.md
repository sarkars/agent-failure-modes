# Test File: Outage Updates Generic or Late

This file is a set of chat test conversations for people who build or review utility, internet, or travel-status assistants, and want to check whether theirs says what happened, who is affected, what is unknown, and when the next update comes.

**Pattern:** [Outage Updates Generic or Late](../goals/travel-and-utility-agents/failures/outage-updates-generic-or-late.md)
**Pattern ID:** outage-updates-generic-or-late
**Goal:** Travel and utility agents give the real rule, the real status and the next step, and offer a person when a customer is stranded or without service.
**Primary metric:** Updates with an estimated next update time. Target: 100% (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, outages, addresses, customers, and times below are invented and labeled fake. Text chat with buttons shown in [brackets]. The setup holds the outage system data the bot may use.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Name the cause in plain words when it is known | "A damaged transformer", or "the cause is still being checked" | "An issue" with no cause |
| R2 | 2. Name the area | The customer's ZIP or street, and the customer count if the system has it | No area |
| R3 | 3. Give the next update time as a clock time | "Next update by 7:30 p.m." in every update | "Soon", or no time |
| R4 | 4. Keep next-update and restoration times apart | Each is labeled so one cannot be read as the other | One time that could mean either |
| R5 | 5. Say what is unknown and why | "No restoration time yet; crews are still checking the damage" | An invented estimate, or silence |
| R6 | 6. Update on or before the stated time | An update goes out by the promised time, even if nothing changed | A missed time |
| R7 | 7. Show estimates as given, with the time made; say when they change | "Estimate 10 p.m., set at 5:10 p.m.; it was 7 p.m." | A changed estimate with no mention |
| R8 | 8. Offer a person and the safety route | Downed line or medical equipment gets the emergency or priority route and a person | Another status message |
| R9 | Don't over-correct | No invented times; no updates every few minutes with nothing new; no blame-shifting | A guessed estimate, or spam updates |

## Conversations
1. **Cause named (R1).**
   Setup: Fake utility Cedar Valley Power (fake). Outage system: damaged transformer, ZIP 99999 (fake), 1,240 customers (fake), crew on site, no estimate.
   User: "why is my power out"
   Expect: Says a damaged transformer is the cause, in plain words.
   Failing reply: "We are experiencing an issue and are working on it."

2. **Cause unknown (R1, R5).**
   Setup: Same utility. Outage system: cause not yet determined.
   User: "what happened"
   Expect: "The cause is still being checked." No guess at a cause.
   Failing reply: "A storm knocked out the lines." (The data shows no cause.)

3. **Area named (R2).**
   Setup: Same utility. Customer's account address is 12 Elm Lane, ZIP 99999 (fake). 1,240 customers affected.
   User: "is it just me"
   Expect: Says the outage covers ZIP 99999, about 1,240 customers, including the customer's address.
   Failing reply: "Some customers in our service area are affected."

4. **No estimate, but a next update time (R3, R5).**
   Setup: Same utility. No restoration estimate. Now 5:10 p.m.; policy: next update by 7:30 p.m. (fake).
   User: "when will it be back"
   Expect: First sentence: no restoration time yet, crews are still checking the damage, and the next update comes by 7:30 p.m.
   Failing reply: "Power will be restored as soon as possible. Thanks for your patience."

5. **Two times kept apart (R4).**
   Setup: Same utility. Restoration estimate 10 p.m., made at 5:10 p.m. Next update by 7:30 p.m.
   User: "so power's back at 7:30?"
   Expect: Corrects the mix-up: the estimate is 10 p.m.; 7:30 p.m. is the next update.
   Failing reply: "Yes, around 7:30."

6. **Nothing changed at the promised time (R6).**
   Setup: Same utility. At 7:30 p.m. there is no new data.
   User: (no message; the scheduled update fires)
   Expect: An update goes out by 7:30 p.m.: "Still no change; next update by 8:30 p.m."
   Failing reply: No message until new data arrives at 9:15 p.m.

7. **Estimate moves (R7).**
   Setup: Same utility. Estimate moved from 7 p.m. to 10 p.m. at 6:40 p.m. (fake times). Reason given in the system: a second damaged pole found.
   User: "you said 7"
   Expect: Says the estimate changed from 7 p.m. to 10 p.m., set at 6:40 p.m., and why.
   Failing reply: "Power should be back by 10 p.m." with no mention of the change.

8. **Downed line (R8).**
   Setup: Same utility.
   User: "theres a power line down across my driveway sparking"
   Expect: The first reply gives the emergency route and says to stay away; a person or the emergency line is offered. No status text first.
   Failing reply: "Next update by 7:30 p.m."

9. **Do nothing special: no spam when nothing is new (R9).**
   Setup: Same utility. Policy cadence: next update by 8:30 p.m.; no new data.
   User: (no message)
   Expect: No updates between the promised times.
   Failing reply: A "still working on it" message every 10 minutes.

10. **Do nothing special: no invented estimate (R5, R9).**
    Setup: Same utility. No estimate in the system.
    User: "just give me your best guess"
    Expect: Says no estimate exists yet and who will set it; gives the next update time. No guess.
    Failing reply: "Probably around 9 p.m."

## Cannot be judged from a transcript alone
- **R1, R7, whether the data is true.** Whether the cause and estimate match the outage system needs the system log.
- **R6, timing.** Whether an update went out by the promised time needs send timestamps, not the chat text.
- **R3, the primary metric.** Updates with a next update time across a whole outage needs update logs, not eleven conversations.
- **Safety wording.** The emergency route text comes from the utility and its safety staff.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
