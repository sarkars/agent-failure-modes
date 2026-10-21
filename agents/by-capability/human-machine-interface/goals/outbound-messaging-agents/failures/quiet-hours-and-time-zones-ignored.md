# AI Agent Texting Customers at Night: Quiet Hours and Time Zones Ignored

<!-- SEO
title: AI Agent Texting at Night: Quiet Hours and Time Zones
description: An AI agent that schedules texts and calls in its own time zone reaches people at night. Schedule by the recipient's local time, and hold what is early or late.
search phrases:
- tcpa quiet hours text messages 8am 9pm
- ai agent sent text at night wrong time zone
- can i text customers after 9 pm
- area code time zone wrong number porting text
- sms quiet hours by state
- outbound ai calling hours time zone compliance
-->

**Frequency**: Common

## Issue: An AI agent that schedules texts and calls in the sender's time zone, or guesses the recipient's zone from an area code, reaches people at night; schedule by the recipient's local time and hold what falls outside the window.

> **One line:** The agent decides "send at 8 p.m." using the company clock or the phone number's area code, and the message lands at 11 p.m. or 6 a.m. for a person who moved, ported their number, or lives in another zone.

> **Read this first.** This pattern is design guidance, not legal advice. Calling and texting hours depend on who you are, whether the message is marketing, collections or service, the channel, the recipient's state and your carrier rules. Have your legal and compliance team review every send window, time zone source and hold rule before launch. Law text is stated here only as far as the sources marked "opened" in section 4 say. Items found only in search summaries are marked as unverified and kept out of the fix.

| | |
|---|---|
| **Channel** | Written for **text (SMS) and chat-style outbound messages**. **Voice** (outbound calls) is PLANNED, not written, measured or tested. |
| **Stakes** | High (regulatory exposure, consumer complaints, lost goodwill) |
| **Who is affected** | People who receive texts or calls from a company's AI agent; the teams that build and schedule those agents |
| **Frequency** | Common in outbound scheduling generally. No prevalence data found for AI agents. |
| **Pattern ID** | quiet-hours-and-time-zones-ignored |
| **Family** | [Outbound messaging agents](../README.md) |
| **Goal** | Outbound texts and calls respect consent, quiet hours, and suppression lists. |
| **Primary metric** | Contacts outside permitted hours. Target: 0 (starting point, tune). |
| **Maturity** | Researched (sources opened; no tests written or run) |
| **Will a better model fix this?** | No. The model does not know the recipient's clock; the scheduler and the contact record do, so the check must live in the product. (Our judgment, not tested.) |
| **Also searched as** | text message quiet hours · wrong time zone text · area code time zone mistake · AI agent texting at night · TCPA calling hours · sending hours by state |

## 1. In plain words
Rules and carrier norms set hours when a person may be texted or called, and those hours are counted on the recipient's clock, not the sender's. An AI agent that picks "7 p.m." in the company's zone, or reads the zone off an area code, can reach someone at 10 p.m. or 5 a.m. The fix is to compute the send time from the recipient's own time zone, taken from a record, and to hold the message until the window opens.

## 2. What it looks like
**Without the fix** (appointment reminder from a home-services company in Los Angeles)
```
Scheduler: send reminders at 8:30 p.m. Pacific (company time)
Bot (to a 212 number, customer now lives in New York): 11:30 p.m. - Hi Dana, this is BrightHome. Want to
        confirm tomorrow's 9 a.m. visit? Reply YES or call us to move it.
Dana: It's 11:30 at night. Who is this?
Bot:  Sorry about that! Reply YES to confirm your visit.
Dana: Stop texting me.
```
**With the fix**
```
Scheduler: contact record says time zone America/New_York (from the booking address, confirmed 2 months ago)
           window 8 a.m.-9 p.m. local; now 11:30 p.m. there -> HOLD until 8:00 a.m. Eastern
Bot (8:00 a.m. Eastern next day): Hi Dana, this is BrightHome. Your visit is today at 9 a.m. Reply YES to
        confirm or RESCHEDULE to change it. Reply STOP to opt out.
Dana: YES
```
The fixed version computes the window from a stored time zone, holds the message instead of sending at the company's clock time, and logs why it waited.

## 3. Why it happens
- **The scheduler runs on the sender's clock.** "Send at 8 p.m." is stored without a time zone, or in the server's zone, so a campaign launched in one zone fans out across the country.
- **The zone is guessed from the area code.** An area code shows where a number was first assigned. People move and port numbers, so the guess drifts from where the person is. One search summary also reports that area code lookups are the usual shortcut (see section 4, unverified).
- **Nothing blocks the send at the last step.** The agent writes the message and a queue delivers it. No check compares the actual send time with the recipient's window, and delayed queues can push a message past the cutoff after it was approved.

## 4. Why it matters
Rule text was read from pages I opened. Confirm each point against the current official text and with counsel.

| Finding | Source | Caveat |
|---|---|---|
| Federal rule text: no telephone solicitation to "any residential telephone subscriber before the hour of 8 a.m. or after 9 p.m." with the clock stated as "local time at the called party's location". Paragraph (e) says paragraphs (c) and (d) apply to "making telephone solicitations or telemarketing calls or text messages to wireless telephone numbers" to the extent described in FCC 03-153. | [47 CFR 64.1200](https://www.law.cornell.edu/cfr/text/47/64.1200) (opened; page reader returned quoted excerpts, not the full section) | Scope depends on "telephone solicitation" and exemptions I did not read. Service messages and other message types may fall outside this paragraph; counsel decides. |
| Debt collection rule: a time before 8:00 a.m. and after 9:00 p.m. "local time at the consumer's location" is inconvenient absent knowledge to the contrary. For an email or text, the communication "occurs when the debt collector sends it", not when it is received or viewed. With conflicting location information, contacting at a time convenient "in all of the locations" the information indicates is compliance. | [12 CFR 1006.6 and commentary, CFPB](https://www.consumerfinance.gov/rules-policy/regulations/1006/6/) (opened; page reader excerpts) | Applies to debt collectors as the rule defines them. It shows one way a rule treats send time and unclear location; it does not set the rule for other message types. |
| Florida Telemarketing Act: "A commercial telephone solicitation phone call before 8 a.m. or after 8 p.m. local time in the called person's time zone" is among the listed violations (subsection 6(a)). Subsection 6(b) lists "more than three" such calls "from any number to a person over a 24-hour period". | [Fla. Stat. 501.616](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.616.html) (opened; page reader excerpts) | I did not open the definitions or exemptions, so I do not say whether it reaches texts or your messages. It shows a state window narrower than the federal one. |

**Read through search summaries only, kept out of the fix (unverified):**
- Compliance-vendor and law-firm blogs say the federal window also covers marketing texts, that area codes are an unreliable proxy for location, that send time (not read time) controls, and that a text queued at 8:55 p.m. but delivered after 9 p.m. may be a violation. I did not open a court decision or FCC order for any of these.
- Blogs mention many time-of-day TCPA lawsuits over texts filed in 2024-2025 and state windows in Oklahoma, Washington and Texas. I opened none of the underlying laws or dockets.
- One blog summary says CTIA's messaging best practices advise avoiding quiet hours in the recipient's time zone, generally 9 p.m. to 8 a.m. I tried the CTIA site and could not open the Principles document, so I do not rely on CTIA wording.
- I did not find a mini-TCPA text-hours statute other than Florida's section above in a source I opened.

**Public incident.** I found no documented, dated incident of an AI agent texting people at night. I do not claim one.

## 5. The fix

**The principle:** Every outbound text or call is scheduled and sent against the recipient's own local clock, from a time zone stored in their record, and anything outside the window is held, never sent.

**Do this**
1. **Store a time zone per contact, as an IANA name** such as America/Chicago, with its source and date (billing or service address, consent form, or the person told you). Check the record at send time.
2. **Do not use the area code alone.** Treat an area-code guess as "low confidence", not a zone. If the only evidence is the area code, use rule 4.
3. **Compute the send decision at the moment of sending**, not at scheduling: convert now to the recipient's zone and compare it with the window.
4. **If the zone is missing or conflicts, send only at a time that is inside the window in every zone the evidence allows**, or hold and ask the person. (This is the approach the debt-collection commentary above describes for unclear location.)
5. **Use the strictest window that applies**: the narrowest of your company policy, the federal rule your counsel says applies, the recipient's state rule, and any carrier or platform rule. Counsel sets the window table; the default below is a placeholder to replace.
6. **Hold and queue.** A message outside the window goes to a hold queue with a release time at the next window open in the recipient's zone. Re-check just before release, and drop it if the window closes first.
7. **Re-check after delay.** If a send is retried or delayed, compare the actual dispatch time, not the approved time, with the window.
8. **Log every decision**: recipient zone, zone source, window used, send or hold, and the dispatch time in the recipient's clock.
9. **Honor replies at any hour**: a person writing "stop" at night gets the opt-out confirmation, which answers their message and is not new outreach. Counsel confirms this exception.

**Reference design: send-time check (the window values are placeholders for counsel's table)**
```
input:  contact.tz, contact.tz_source, now_utc, message.type, contact.state
step 1: if contact.tz missing or source == "area_code": zones = all zones the evidence allows; else zones = [contact.tz]
step 2: window = strictest(company_policy, federal[message.type], state[contact.state], carrier)   # counsel table
step 3: ok = for every zone in zones: window.start <= local_time(now_utc, zone) < window.end
step 4: ok -> send; not ok -> hold until next time every zone is inside window; log reason
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The zone is unknown or conflicts and the person is already in a chat: "What time zone are you in?" |
| Offer choices: 2-4 options plus "Something else", free text open | When a person asks about timing: "Morning (8-11)", "Afternoon (12-4)", "Evening (5-8)", "Something else". Do not offer choices as an unprompted menu in a one-way notice. |
| Lead with the answer | The person replies "why are you texting me now?": say the time you wrongly sent, apologize in one line, and say what happens next |
| Hand off to a person | A complaint about contact hours, or any mention of a lawyer or regulator |

**Don't over-correct.** Holding everything until noon makes time-sensitive messages useless (a code that expires, a reminder for tomorrow's 8 a.m. visit). Keep a counsel-reviewed list of message types that may go inside the window early, and send the rest at the next opening. Do not drop messages silently: show the hold in the log and tell the person when a message was delayed if it matters.

**Hand-off rule.** Route to a person when someone complains about the time of contact, says the zone on file is wrong, or two holds in a row expire unsent. Pass the zone on file, its source, and the send log.

**Framework used:** none yet.

## 6. How to test it (short version)
No tests have been written or run. Proposed scenarios:

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Company in Los Angeles queues 8:30 p.m. Pacific text to a New York contact | Held until the next window opens in New York (rules 1, 3, 6) |
| 2 | Number with a 212 area code; stored zone America/Los_Angeles from the booking address | Zone on file is used, not the area code (rules 1, 2) |
| 3 | Zone missing; only the area code is known | Sent only when inside the window in every zone allowed, else held (rule 4) |
| 4 | Message approved at 8:55 p.m., dispatched at 9:03 p.m. recipient time after a queue delay | Blocked at dispatch (rule 7) |
| 5 | Florida contact, marketing type, 8:30 p.m. local | Blocked if counsel's table sets an 8 p.m. state limit (rule 5) |
| 6 | Hold released, but the window closes before dispatch | Dropped or re-held, not sent (rule 6) |
| 7 | Person texts "stop" at 11 p.m. | Opt-out confirmation sent; no further outreach (rule 9) |
| 8 | Expiring code (message type marked time-sensitive by counsel) at 10 p.m. | Handled per the counsel list, logged (rule 5, over-correction check) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Contacts outside permitted hours** (primary) | 0 | Dispatch timestamp converted to the contact's stored zone, compared with the window used; count sends outside it | Any |
| Sends with zone from a record (not area code alone) | 100% | `tz_source` field on each send, share not equal to `area_code` or missing | Below 98% |
| Sends held then released in window | Track | Count of hold events and release times | Hold queue older than one window |
| Contacts with a zone on file | 95% or more | Share of active contacts with `contact.tz` set | Below 90% |
| Complaints citing time of contact | Track | Stop or complaint replies mentioning "night", "late", "early", "time" | Rising for two weeks |
| Time-sensitive messages delayed past usefulness (counter-metric) | Track | Held messages whose purpose expired before release | Any for a type counsel marked time-sensitive |

### Detection signals (proposed, not yet calibrated)
Written for text event logs. None is measured; voice signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Dispatch time falls outside 8 a.m.-9 p.m. in the contact's stored zone | Send event timestamp, `contact.tz` | A reply to the person's own message, or a stored zone that is wrong |
| `tz_source` is `area_code` or empty on a send | Send event field | A contact with a sparse record where rule 4 was applied correctly |
| Reply within 30 minutes containing "who is this", "it's late" or "stop" after a night send | Reply text after a send outside the window | A neutral reply to a message sent inside the window |
| Send time in company zone equals approval time, with no recipient-zone conversion logged | Scheduler log missing `window_check` | Internal-only test messages |
| Hold released, then dispatched after window close | Hold release time vs dispatch time | A resend the person asked for |

**Starter rule:** before every outbound text, compare the dispatch time in the contact's stored time zone with the permitted window, and hold the message if it is outside or if the zone cannot be confirmed.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: quiet-hours-and-time-zones-ignored
runs: pre_send
reads: [contact.tz, contact.tz_source, contact.state, message.type, send.dispatch_time_utc, policy.window]
trigger: an outbound text or call is about to be sent
moves: [ask_one_question, offer_choices, lead_with_answer, hand_off]
choices: ["Morning (8-11)", "Afternoon (12-4)", "Evening (5-8)", "Something else"]
on_miss: rewrite
metric: contacts outside permitted hours
counter_metric: time-sensitive messages delayed past usefulness
status: proposed
```

## 8. Related patterns
- [Marketing texts without consent](marketing-texts-without-consent.md): whether you may contact the person at all; this page is about the hour.
- [Do-not-call lists not checked](do-not-call-lists-not-checked.md): who is on a suppression list; this page is the clock on people who are not.
- [Collections calls without required disclosures](../../voice-receptionist-agents/failures/collections-calls-without-required-disclosures.md): the closest existing page. It lists a local-time check as one of nine rules for collections contacts; this page covers the time zone data, the hold queue and the dispatch-time check for any outbound message type.
- [Interrupts at a bad moment](../../proactive-and-ambient/failures/interrupts-at-a-bad-moment.md): an assistant breaks into a task; this page is about the hour the contact arrives.

## 9. Common questions
### What hours can an AI agent text or call customers?
The federal rule text I opened says 8 a.m. to 9 p.m. local time at the called party's location for telephone solicitations to residential subscribers ([47 CFR 64.1200(c)(1)](https://www.law.cornell.edu/cfr/text/47/64.1200)). Other rules are narrower, such as Florida's 8 p.m. limit for commercial solicitation calls ([Fla. Stat. 501.616](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.616.html)). Which rule covers your messages is for counsel.

### Whose time zone counts, mine or the recipient's?
In the rule text I opened, it is the recipient's: "local time at the called party's location" and "local time in the called person's time zone." Schedule by their clock.

### Can I use the area code to find the time zone?
Not alone. Search summaries say people move and port numbers, but I did not open a source on this. Take the zone from a record you can date (address, consent form, what the person said) and treat the area code as a weak hint.

### What if I do not know the recipient's time zone?
One rule I opened (the debt collection commentary) accepts contact at a time convenient in all locations the information indicates ([12 CFR 1006.6](https://www.consumerfinance.gov/rules-policy/regulations/1006/6/)). Use the same idea: send only when it is inside the window everywhere the evidence allows, or hold and ask.

### Does a text count as sent when it is queued or when it arrives?
The debt collection commentary says an electronic message "occurs when the debt collector sends it." For other message types I opened no source, so use dispatch time as the safe check.

---
## Technical section

### T1. Solution architecture
```
agent draft -> message type classifier -> contact lookup (tz, tz_source, state)
            -> window resolver (counsel table: company, federal, state, carrier)
            -> check at dispatch: now in window for every candidate zone?
            -> yes: send + log | no: hold queue (release = next window open) + log
hold release -> re-check -> send or re-hold or drop
```
The window table is data owned by counsel, not text in the prompt.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Zone from a record, area code alone is low confidence | Contact service | Tests 2-3 |
| Check at dispatch, not at approval | Sender / queue worker | Test 4 |
| Strictest window wins | Window resolver | Test 5 |
| Re-check after hold | Hold queue | Test 6 |

### T3. Evals
- **Dataset:** 200 synthetic sends across zones (include Hawaii, Arizona with no daylight saving shift, Florida's two zones, daylight saving change days), missing zones, delayed queues and replies. Starting size, tune.
- **Judge rubric:** Is the dispatch time inside the window in the contact's zone? Was a hold logged with a reason? Was an opt-out reply honored?
- **Metrics and starting thresholds:** sends outside window 0, zone from record 100% of known contacts. Starting points.
- **Release gate:** block a deploy if any synthetic send lands outside the window.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Sends outside window | Any | More than one in a day | Pause the sender; check zone data and the clock source |
| Hold queue age | Over one window | Over two | Check the release job |

### T5. Trade-offs
- Holding delays time-sensitive messages; keep a counsel-reviewed exception list.
- Zone data needs collecting and upkeep; asking costs one question for chat contacts.
- Using the strictest window across states shortens the sending day for some contacts.

---
### Deep dive
- **Voice (PLANNED).** Outbound calls would need the same window check before dialing and a callback hold. No voice behavior is written or measured here.
- **Open questions.** I found no study of AI agents sending at night, no opened source on carrier quiet-hour rules, and no opened court ruling on which clock controls for texts.
- **References.** [47 CFR 64.1200 (Cornell LII)](https://www.law.cornell.edu/cfr/text/47/64.1200), [12 CFR 1006.6 (CFPB)](https://www.consumerfinance.gov/rules-policy/regulations/1006/6/), [Fla. Stat. 501.616](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.616.html) (all opened, read as page-reader excerpts).
