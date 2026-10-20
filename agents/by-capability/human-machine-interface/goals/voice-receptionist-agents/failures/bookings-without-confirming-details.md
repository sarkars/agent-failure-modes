# AI Receptionist Booked My Appointment With the Wrong Name or Number: Bookings Without Confirming Details

<!-- SEO
title: AI Receptionist Booking Mistakes: Read Back Name, Number, Time
description: Why a booking bot that never reads back the name, callback number, or time books wrong appointments, and a read-back step to add before the booking is saved.
search phrases:
- ai receptionist got my name wrong
- ai appointment booking wrong phone number
- chatbot booked wrong time
- ai receptionist confirm appointment details
- how to confirm details in a booking chatbot
- voice agent read back phone number
- ai receptionist misspelled name
- ai appointment scheduler no confirmation
-->

**Frequency**: Common

## Issue: A booking assistant saves the appointment on details it read or heard once, and never reads the name, callback number, and time back, so a wrong detail surfaces only when a reminder fails or the patient shows up at the wrong time.

> **One line:** The booking is saved before anyone checks the three details the office will depend on.

| | |
|---|---|
| **Channel** | Written for **chat** (typed booking requests on a practice or salon website). The spoken name-spelling and phone-number case is described as **planned** for voice; no voice detection or voice data exists yet. |
| **Stakes** | Medium. A wrong time or callback number costs a missed visit and an unused slot; a wrong name can attach the booking to the wrong chart. |
| **Who is affected** | Patients and clients who book through an assistant, and front-desk staff who find the error later |
| **Frequency** | Common as a design gap (our judgment). I found no published measure of how often booking assistants skip read-back. |
| **Pattern ID** | bookings-without-confirming-details |
| **Family** | [Voice receptionist agents](../README.md) |
| **Goal** | Phone agents confirm critical details, catch emergencies, and meet disclosure and consent rules. |
| **Primary metric** | Booking conversations with a read-back of name, callback number, and date and time before the booking is saved. Starting target: 100% (tune). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | No. A stronger model hears or reads more accurately, but whether the flow stops to read details back is a product decision. (Our judgment, not tested.) |
| **Also searched as** | AI receptionist wrong phone number · bot misspelled my name · chatbot booked wrong day · AI scheduler no confirmation · read back appointment details |

## 1. In plain words
A booking has three details the office relies on later: who the patient is, how to reach them, and when they are coming. If the assistant saves the booking the moment it has them, one typo, one misheard letter, or one "2" that was meant as 2 PM goes unnoticed. The fix is one short read-back before the booking is saved.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "Lakeview Dental" is an invented practice with a website chat assistant.

**Without the fix**
```
User: Need a cleaning Thursday at 2. Name's Siobhan Keough, cell is 512-555-0174.
Bot:  You're all set! I've booked a cleaning for Siobhan Keogh on Thursday at 2:00.
User: (closes the chat)
      (saved: the name is misspelled; the number has the typo the user meant
       to type as 0147, so the reminder text goes to a stranger; "2:00" was saved as 2:00 AM)
```

**With the fix**
```
User: Need a cleaning Thursday at 2. Name's Siobhan Keough, cell is 512-555-0174.
Bot:  Before I book it, please check:
      Siobhan Keough (K-E-O-U-G-H)
      Cleaning, Thursday, Oct 22, 2:00 PM
      Reminders go to 512-555-0174
      Is that all correct?
User: The number is 0147, I typed it wrong.
Bot:  Thanks. Reminders go to 512-555-0147. Everything else stays the same. Book it?
User: Yes.
Bot:  Booked. You'll get a text at 512-555-0147 the day before.
```
The bot kept the read-back to one message, and the user caught their own typo before it cost a missed visit.

**Planned for voice (not built or tested).** A caller says "Keough" on the phone and the transcript may say "Keogh". The same read-back would spell the name letter by letter ("K, E, O, U, G, H") and read the number in its natural groups, digit by digit. See [number and date errors](../../../../speech-and-audio/goals/speech-recognition/failures/number-date-errors.md) (it holds the spelled-out strings example, TR-10) for the listening side.

## 3. Why it happens
These are our reading of the pattern.
- **A tool call that succeeds looks like done.** Once the calendar API returns a booking, the flow says "booked", with no step for the user to check what was saved.
- **Confirmation was cut to avoid over-confirming.** A team that fixed [over-confirmation](../../dialogue-management/failures/over-confirmation.md) can remove the one check that matters here.
- **Details are captured once and trusted.** Typed text can hold typos, "Thursday at 2" has no AM or PM, and spoken names and digits can be transcribed wrong. Nothing compares what was saved with what the person meant.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google's conversation design guide says to double-check before an action that is difficult to undo, and keeps explicit confirmation of parameters for cases where misunderstanding is costly, such as names, addresses, or messages sent for the user. | [Google, *Confirmations*](https://developers.google.com/assistant/conversation-design/confirmations). Opened and read. | Design guidance for Google Assistant, not an experiment. It does not mention appointment booking. |
| Avaya's speech-application guide says to have callers give long digit strings in segments and "confirm each group before going to the next", and to use the natural groups of a telephone number. | [Avaya, digit sequences](https://support.avaya.com/elmodocs2/ir/15535.htm). Opened and read. | Vendor documentation for phone speech systems; undated in what I read. Not a measurement. |
| LiveKit's phone-number task reads the number back in groups, and its `require_confirmation` setting defaults to true for audio sessions and false for text. | [LiveKit docs, GetPhoneNumberTask](https://docs.livekit.io/agents/prebuilt/tasks/get-phone-number.md). Opened and read. | A developer toolkit's defaults. It shows a common design, not that text needs no read-back. |
| Henry Schein's dental tips say to keep contact information current because reminders sent to a wrong number "are no good to anyone", and to verify contact details and preferred contact method at each appointment. | [Henry Schein, *20 Tips to Reduce Dental Patient No Shows*](https://henryschein.com/us-en/dental/business-solutions/practice-services-knowledge-center-articles/20-tips-to-reduce-dental-patient-no-shows.aspx). Opened and read. | Vendor practice advice. It gives no dental no-show rate; its statistics come from medical no-show research I did not open. |

A Vapi support forum thread about an AI agent that misspells customer information turned up in search. The page returned an access error when I opened it, so I know it only from a search summary; it is unverified and not used in the fix. I found no study of how often booking assistants save wrong names, numbers, or times.

**Public incident.** No public incident found. I searched for reports of AI receptionists booking with wrong details and found vendor pages and forum posts, not a dated, sourced case.

## 5. The fix

**The principle:** Before saving a booking, read back the name, the callback number, and the date and time in one message, and save only after the user says yes.

**Do this**
1. **Read back before you write.** Do not create the booking until the user has confirmed the read-back in this conversation.
2. **Cover all three critical details in one message.** Name, callback number, and weekday, date, time, and AM or PM.
3. **Show the name the way it will be saved,** spelled out letter by letter when it is uncommon or was not typed by the user.
4. **Show the number in natural groups,** area code first, so a typo is easy to see ("512-555-0147").
5. **Ask one question.** "Is that all correct?" or "Tell me what to change." Never one question per detail.
6. **Apply a correction to that field only,** then show the corrected field and ask to book. Do not restart the read-back ([corrections not applied](../../dialogue-management/failures/corrections-not-applied.md)).
7. **Validate before reading back.** If the number is not 10 digits or the time is outside office hours, say so first and ask for a fix.
8. **Put the confirmed details in the final message,** with how to change them.

**Reference design: what to read back**
| Detail | Why it is critical | Read back as |
|---|---|---|
| Name | Attaches the booking to a chart | Spelled out: "Siobhan Keough (K-E-O-U-G-H)" |
| Callback number | Reminders and "we need to move you" calls go here | Natural groups: "512-555-0147" |
| Date and time | The visit itself | "Thursday, Oct 22, 2:00 PM" |
| Service, provider | Sets the slot length | Include, but one clause is enough |

```
Before you create any booking, send one message that reads back the patient's name (spelled), callback number (in groups), and weekday, date, and time with AM or PM.
Ask once whether it is all correct. Create the booking only after a yes.
If the user fixes one detail, change only that detail and show it again. Never read back details the user already confirmed.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The read-back itself: one question about the whole group, right before the booking is written. Do not ask it again after a "yes". |
| Offer choices: 2-4 options plus "Something else", free text open | After a read-back, when buttons help on a small screen: "Yes, book it", "Change a detail", "Something else". Skip them when the user already answered in words. |
| Hand off to a person | The user fails two corrections in a row or the number will not validate. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Read back once, as a group, and only the critical details. Do not confirm each slot as it is filled, do not repeat details the user just confirmed, and do not add confirmation to steps that cost nothing to undo. That is the [over-confirmation](../../dialogue-management/failures/over-confirmation.md) failure. For a returning patient with a number on file, one line ("reminders go to the cell ending 0147") is a read-back.

**Hand-off rule.** After two failed corrections, or a number that will not validate, offer the front desk and pass the details collected so far ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. These are proposed checks; results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | Typed request with name, number, and "Thursday at 2" | One read-back with name, number in groups, weekday, date, and PM, before any booking (rules 1, 2, 4) |
| 2 | The user says the number is wrong | Only the number changes; it is shown again before booking (rule 6) |
| 3 | A 9-digit number | The bot asks for a fix before reading back (rule 7) |
| 4 | An uncommon name | The name is spelled out in the read-back (rule 3) |
| 5 | The user says "yes" to the read-back | Booking created; no second read-back (rules 1, 5) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Booking conversations with a read-back of name, number, and date and time before the booking is saved** (primary) | 100% | Log a `readback` turn tagged with the fields it covered; compare with the booking write time | Below 95% |
| Bookings changed within 24 hours for name, number, or time | Track; set from baseline | Edits to those fields after the booking event | Rising |
| Reminders that fail to deliver to the stored number | Track; set from baseline | Delivery-failure events by booking | Rising two weeks in a row |
| Read-backs per booking (counter-metric) | 1 | Count read-back turns per booking | Over 1 on average |
| Corrections made during a read-back | Track only | Field changes after a read-back turn; each is a caught error | None; a rate near 0 for months may mean users skim |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice is PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Booking write with no read-back turn before it | Booking event with no prior `readback` turn in the session | A returning patient whose details were confirmed earlier in the session |
| The user corrects name, number, or time right after "booked" | Field-change message after the booking event | The user changed plans and is not fixing an error |
| Reminder to the stored number is undeliverable | Delivery-failure event for the booking | A landline or a carrier problem |
| Read-back omits one of the three fields | `readback` turn covering fewer than three fields | A field the user declined to give |
| The same detail read back twice in a row (counter) | Two `readback` turns with the same value | The user changed it in between |

**Starter rule:** before saving a booking, read back the name, callback number, and date and time in one message, and save only after a yes.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: bookings-without-confirming-details
runs: pre_send
reads: [booking.name, booking.callback_number, booking.datetime, session.confirmed_fields, turn.draft_reply]
trigger: the assistant is about to create or finalize a booking
moves: [ask_clarifying_question, offer_choices, hand_off]
choices: ["Yes, book it", "Change a detail", "Something else"]
on_miss: ask
metric: booking conversations with a read-back of name, number, and date and time
counter_metric: read-backs per booking
status: proposed
```

## 8. Related patterns
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the opposite failure, asking "is that right?" on every cheap step. Use its cost-class list; a booking's name, number, and time belong on the costly side.
- Under-confirmation of consequential details (DM-08 in the [catalog](../../../roadmap/conversation-design.md)): the general rule for amounts, dates, and recipients. Its chat example lives in [irreversible action without confirmation](../../../../external-actions/goals/action-execution/failures/irreversible-action-without-confirmation.md). This page is the receptionist case: the details are a name, a callback number, and a time.
- [Number and date errors](../../../../speech-and-audio/goals/speech-recognition/failures/number-date-errors.md): the listening problem for spelled-out letters and digits on a phone line (TR-10). This page covers the read-back step that catches those errors.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): what happens after the user says a detail is wrong.
- [Order mix-ups at the speaker](../../drive-thru-agents/failures/order-mix-ups-at-the-speaker.md): the same read-back idea for a drive-thru order.
- [Repair failure](../../voice/failures/repair-failure.md): recovering when a spoken detail keeps coming out wrong.

## 9. Common questions
### Why does my AI receptionist get names and phone numbers wrong?
Typed details can hold typos, and spoken ones can be transcribed wrong. Without a read-back, nothing catches either. Add one message that shows the name, number, and time before the booking is saved.

### Does a chat booking bot need a read-back if the user typed everything?
Yes, for the callback number and the time. LiveKit's toolkit turns confirmation off by default for text, but typos and a missing AM or PM still happen. A short read-back is cheap compared with a missed visit.

### How should a bot read back a phone number?
In its natural groups, digit by digit, then ask for a yes or a correction. Avaya's guide recommends natural groups and confirming each group on phone calls.

### Won't a read-back feel like over-confirming?
Not if it happens once, covers only the critical details, and replaces per-slot questions. See [over-confirmation](../../dialogue-management/failures/over-confirmation.md).

### What should I do with a patient whose number is already on file?
Show the last four digits in the read-back ("reminders go to the cell ending 0147") and offer a way to change it.

---
## Technical section

### T1. Solution architecture
```
collect name, phone, time -> validate (10 digits, office hours, free slot)
  -> render read-back (spelled name, grouped number, weekday date time AM/PM)
  -> wait for yes -> booking.create(confirmed_fields = [name, phone, datetime])
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Booking write refused unless all three fields are marked confirmed | Booking tool wrapper | Tests 1 and 5 |
| A correction updates one field and clears only that field's confirmed flag | Session state | Test 2 |
| Read-back text is built from the stored values, not the user's wording | Template | Log comparison |

### T3. Evals
- **Dataset:** 50 scripted booking requests with planted problems (a transposed digit, a 9-digit number, "at 2" with no AM or PM, an uncommon name spelling).
- **Judge rubric:** a read-back with all three fields before the write; one question; corrections limited to one field.
- **Metrics and starting thresholds:** read-back before write 100%; read-backs per booking 1. Starting points to tune.
- **Release gate:** block a deploy if any scripted booking writes before a confirmed read-back.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Read-back before write | Below 98% | Below 95% | Find the flow path that skips the wrapper |

### T5. Trade-offs
- One more turn per booking. Offset it by removing per-slot confirmations.
- A strict gate can block users who cannot confirm; keep the hand-off to the front desk.

---
### Deep dive
- **Open question.** I found no study of how often booking assistants save wrong details, or of read-back rates in appointment booking.
- **Voice (planned).** Spoken names and digits are less reliable than typed text, so the read-back matters more there. Code words for confusable letters belong in the voice version; nothing here was measured on voice.
- **References.** [Google, Confirmations](https://developers.google.com/assistant/conversation-design/confirmations) (opened); [Avaya, digit sequences](https://support.avaya.com/elmodocs2/ir/15535.htm) (opened); [LiveKit, GetPhoneNumberTask](https://docs.livekit.io/agents/prebuilt/tasks/get-phone-number.md) (opened); [Henry Schein, 20 tips](https://henryschein.com/us-en/dental/business-solutions/practice-services-knowledge-center-articles/20-tips-to-reduce-dental-patient-no-shows.aspx) (opened).
