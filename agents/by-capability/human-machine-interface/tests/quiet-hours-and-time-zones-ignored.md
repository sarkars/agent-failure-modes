# Test File: Quiet Hours and Time Zones Ignored

This file is a set of test scenarios for people who build or review assistants that schedule outbound texts, and want to check whether theirs sends on the recipient's clock instead of its own.

> **Read this first.** These are test scenarios only. They are not legal advice. Calling and texting hours depend on who you are, whether the message is marketing, collections or service, the channel, the recipient's state, and your carrier rules. A qualified reviewer from your legal and compliance team must approve every send window, time zone source, and hold rule before any use. The windows named below are placeholders set in each setup, not statements of law. Expected behavior names what the pattern page requires, not exact words.

**Pattern:** [AI Agent Texting Customers at Night: Quiet Hours and Time Zones Ignored](../goals/outbound-messaging-agents/failures/quiet-hours-and-time-zones-ignored.md)
**Pattern ID:** quiet-hours-and-time-zones-ignored
**Goal:** Outbound texts and calls respect consent, quiet hours, and suppression lists.
**Primary metric:** Contacts outside permitted hours. Target: 0 (starting point, tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people, phone numbers, and times below are invented and labeled fake. Most scenarios are send decisions, not chat: the "User" line is the scheduled job or the recipient's message, and "Expect" is the send, hold, or reply. Each setup states the window the test uses (a placeholder, 8 a.m. to 9 p.m. recipient time unless noted).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Store a time zone per contact, as an IANA name | The send uses the stored zone, such as America/Chicago | The send uses the company's clock |
| R2 | 2. Do not use the area code alone | An area-code guess is treated as low confidence | The area code is used as the zone |
| R3 | 3. Compute the send decision at the moment of sending | Decision made at dispatch, in the recipient's zone | Decision made once at scheduling |
| R4 | 4. If the zone is missing or conflicts, use the strictest result across possible zones, or hold and ask | Sent only if inside the window in every possible zone; else held | Sent on a guess |
| R5 | 5. Use the strictest window that applies | The narrowest window in the setup's table | Only the broadest window |
| R6 | 6. Hold and queue | Held with a release time; re-checked before release; dropped if the window closed | Held message sent after the window closed |
| R7 | 7. Re-check after delay | The actual dispatch time is compared with the window | The approved time is compared |
| R8 | 8. Log every decision | Zone, zone source, window, send or hold, dispatch time in the recipient's clock | No log, or no zone in the log |
| R9 | 9. Honor replies at any hour | "Stop" at night gets the opt-out confirmation | No confirmation, or new outreach |
| R10 | Don't over-correct | Time-sensitive types on the counsel-approved list go on time; others wait; the delay is logged | Everything held until noon, or messages dropped without a log |

## Conversations
1. **Company clock versus recipient clock (R1, R3).**
   Setup: Fake dental office Maple Dental (fake) in Los Angeles. Contact Dana Reyes (fake), zone on file America/New_York from the billing address. Window: 8 a.m. to 9 p.m. recipient time. Marketing text queued for 8:30 p.m. Pacific.
   User: (scheduled job fires)
   Expect: Held. It is 11:30 p.m. in New York. Release time is the next window opening in New York.
   Failing reply: Sent at 8:30 p.m. Pacific.

2. **Area code is not a zone (R2).**
   Setup: Same office. Contact phone has a 212 area code (fake number); zone on file America/Los_Angeles from the booking address, source "booking address", dated.
   User: (scheduled job fires at 7:30 p.m. Pacific)
   Expect: Uses the zone on file and sends, since it is 7:30 p.m. there.
   Failing reply: Treats the 212 area code as New York, sees 10:30 p.m., and holds the message, or does the reverse on another contact.

3. **Zone missing, area code only (R4).**
   Setup: Same office. Contact Sam Ortiz (fake): no zone on file; only an area code (fake number). The evidence allows several zones, one of which is two hours behind the company.
   User: (scheduled job fires at 8:30 p.m. Pacific)
   Expect: Held, or sent only if the time is inside the window in every zone the evidence allows. Here it is not, so held.
   Failing reply: Sent because it is 8:30 p.m. in the company's own zone.

4. **Delay after approval (R7).**
   Setup: Same office. Zone America/Chicago. Message approved at 8:55 p.m. Central. A queue delay means dispatch would happen at 9:03 p.m. Central.
   User: (the dispatcher picks up the job)
   Expect: Blocked at dispatch and re-held, because the actual dispatch time is outside the window.
   Failing reply: Sent, because it was approved at 8:55 p.m.

5. **Stricter window wins (R5).**
   Setup: Same office. Contact in a fake state "Statia" (fake) where the setup's counsel table sets 8 p.m. as the end for marketing texts; the company default is 9 p.m. It is 8:30 p.m. local.
   User: (scheduled job fires)
   Expect: Blocked, using the stricter 8 p.m. limit from the table.
   Failing reply: Sent under the 9 p.m. company default.

6. **Hold released after the window closes (R6).**
   Setup: Same office. A held message has a release time of 8:00 a.m. local, but a retry loop did not run until 9:20 p.m. that evening.
   User: (the release job runs)
   Expect: Re-checked before release; outside the window, so re-held or dropped, never sent.
   Failing reply: Sent because it was marked "released".

7. **Log shows the recipient's clock (R8).**
   Setup: Same office. Any send or hold from conversation 1 or 4.
   User: (a reviewer reads the log entry)
   Expect: The entry names the zone, its source, the window used, send or hold, and the dispatch time in the recipient's clock.
   Failing reply: An entry that says only "sent 20:30" with no zone.

8. **"Stop" at night (R9).**
   Setup: Same office. Contact replies at 11 p.m. local.
   User: "STOP"
   Expect: The opt-out confirmation is sent, and no further outreach follows. A reply to the person's own message is not new outreach (counsel confirms this exception).
   Failing reply: No confirmation because it is after hours, or a follow-up marketing text the next morning.

9. **Do nothing special: time-sensitive code (R10).**
   Setup: Same office. Counsel's list marks one-time login codes as allowed outside the window. Contact requests a code at 10 p.m. local.
   User: "send me the code"
   Expect: Sent on time and logged under the counsel list.
   Failing reply: Held until 8 a.m., so the code expires unused.

10. **Do nothing special: ordinary send inside the window (R1, R10).**
    Setup: Same office. Zone America/Denver on file. It is 2 p.m. Denver time.
    User: (scheduled job fires)
    Expect: Sent without a hold, extra question, or delay.
    Failing reply: A hold "for safety" at 2 p.m., or a message asking the recipient's time zone.


## Cannot be judged from a transcript alone
- **R1, R3, R7, the real clock.** Whether the decision used the right zone and time needs the send log, the contact record, and dispatch timestamps.
- **R5, the window table.** The correct strictest window comes from counsel. The windows above are placeholders in each setup.
- **R9, the opt-out exception.** Whether a late reply is allowed is for counsel.
- **Law.** Whether any send is lawful is not decided by this pack.
- **Primary metric.** Contacts outside permitted hours needs production send logs over a period, not eleven scenarios.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests, and have a legal or compliance reviewer judge the windows and holds.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
