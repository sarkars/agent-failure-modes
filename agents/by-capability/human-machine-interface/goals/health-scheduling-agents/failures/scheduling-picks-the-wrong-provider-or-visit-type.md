# Scheduling Chatbot Booked the Wrong Visit Type or Provider: Scheduling Picks the Wrong Provider or Visit Type

<!-- SEO
title: Scheduling Chatbot Books the Wrong Visit Type or Doctor: Fix
description: Why a scheduling chatbot books a follow-up as a new-patient visit or a short slot for a long procedure, and how visit-type rules, two questions and a read-back prevent it.
search phrases:
- chatbot booked wrong appointment type
- ai scheduling booked me with the wrong doctor
- new patient vs established patient appointment chatbot
- why was my appointment rescheduled wrong visit type
- ai appointment scheduler visit length wrong
- how to set up appointment type rules for an ai scheduling assistant
- patient scheduling errors wrong provider
-->

**Frequency**: Common

## Issue: A scheduling chatbot maps what the patient said to the wrong visit type, length or clinician, so the patient is turned away, billed differently, or has to rebook.

> **One line:** The chat books a slot that fits the calendar but not the visit: a follow-up as a new-patient visit, 15 minutes for a 40-minute procedure, or a clinician who cannot treat the problem.

| | |
|---|---|
| **Channel** | Written for **chat** (web or app scheduling chat). Voice scheduling is **planned**; no voice detection or data exists yet. |
| **Stakes** | Medium. The cost is a wasted visit, a different bill, or a delayed visit; no clinical decision is made here (see "Don't over-correct"). |
| **Who is affected** | Patients booking through chat, and front-desk staff who fix the booking later |
| **Frequency** | Common as a design gap (our judgment). I found no published rate for chatbots; the closest figure (section 4) is from a different setting. |
| **Pattern ID** | scheduling-picks-the-wrong-provider-or-visit-type |
| **Family** | [Health scheduling agents](../README.md) |
| **Goal** | Scheduling and patient-message agents use the right wording, provider, and visit type, and never leave patients with unexplained results. |
| **Primary metric** | Rescheduled-for-wrong-type rate, computed from reschedule reasons. Starting point: set from a baseline (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model reads the request better, but the right type depends on the practice's own rules and the patient's record, which it must be given. (Our judgment, not tested.) |
| **Also searched as** | chatbot booked wrong appointment type · booked as new patient but I'm established · appointment too short for procedure · scheduled with the wrong specialist · ai scheduler wrong doctor |

## 1. In plain words
Every practice has its own list of visit types, how long each takes, who can see which, and where. A scheduling chat that picks the first open slot, or the type that sounds closest to the patient's words, can break those rules without knowing it. The fix is to book from the practice's table, ask the one or two questions that decide the type, and read back provider, type, length and place before booking.

## 2. What it looks like
**Without the fix**
```
User: I need to see Dr. Patel again about my knee.
Bot:  Sure! I have Tuesday at 9:00 AM for a new patient visit. Shall I book it?
User: Yes
      (Patient saw Dr. Patel last spring. The front desk finds a new-patient code on an
       established patient and moves the visit; the patient gets a call and a new time.)
```
**With the fix**
```
User: I need to see Dr. Patel again about my knee.
Bot:  Have you seen Dr. Patel or anyone in the orthopedics group in the last 3 years?
User: Yes, in April last year.
Bot:  Then this is a follow-up. Here is what I'd book: follow-up visit, 20 minutes, Dr. Patel,
      Tuesday 9:00 AM, Eastside office. Is that right?
User: Yes
```
The bot asked the one question that decides the type, then read back provider, type, length and location before booking.

## 3. Why it happens
- **No visit-type table in the loop.** The bot matches words to a label from its own sense of what "follow-up" means, not the practice's list of types, lengths and eligible clinicians.
- **The deciding fact is not asked.** New or established depends on the patient's history with a group, which the user rarely volunteers and a plain slot search never checks.
- **The booking tool accepts any combination.** If the system lets a type be saved with any provider or length, nothing stops a mismatch; staff then rely on memory (see section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The CPT definition: a new patient has not received professional services from the physician, or another of the exact same specialty and subspecialty in the same group practice, within the past three years. Established is the mirror image. | [UTMB Faculty Group Practice newsletter, Nov. 2023](https://www.utmb.edu/fgp/newsletter/article/newsletter/2023/11/08/coding-clip-nov23). Opened and read. | A coding explainer from one academic group. It also says CPT's definition differs a bit from some payers' definitions for advanced practice providers, so payer rules apply. Not legal advice. |
| An appointment type in athenahealth defines the slot length in minutes, how it is labeled and displayed, and a class that determines which authorization and referral rules apply. | [athenahealth help, Appointment Types](https://help.athenahealth.com/Ohelp/Content/Appointment_Types_PH.htm). Opened and read. | One vendor's product. Other systems differ, and the page does not describe provider rules. |
| A vendor article lists staff fatigue, heavy workload and lack of training as raising the risk of booking the wrong slot, provider, or visit type, and says provider preferences and visit-type workflows vary, so staff handle the complexity on the fly without documentation. | [Keona Health, *The 3 Ways to Address Patient Scheduling Errors*](https://keonahealth.com/resources/the-3-ways-to-address-patient-scheduling-errors). Opened and read. | Vendor marketing for scheduling software. It describes human schedulers, not chatbots. Its sidebar figures are unsourced and I do not use them. |
| In a retrospective review of 1,482 patients booked through a central appointment system for a thoracic surgery clinic, 128 (8.6%) made an incorrect appointment, meaning a clinic unrelated to their complaint. The authors note misdirected bookings waste staff time and keep other patients from getting appointments. | [Turkmedline record of the study (abstract)](https://turkmedline.net/detay/analysis-of-erroneous-appointments-from-the-thoracic-surgery-outpatient-clinic-of-a-training-hospital-research/f28b9289791d0547/tr/541%2B2023%2B8%2B2). Opened; abstract only. | A Turkish hospital with patient self-booking, not a US chatbot, and the error is wrong clinic, not wrong visit type. It shows self-service booking can misroute; it is not a chatbot rate. |

I found no study of wrong-visit-type rework for AI scheduling chat. A Johns Hopkins nursing project on pre-clinic schedule review came up in search, but I could not open it (access refused), so I do not use it.

**Public incident.** None found for this pattern as such.

## 5. The fix

**The principle:** Book only from the practice's own visit-type and provider rules, ask what decides the type, and read the whole booking back.

**Do this**
1. **Use a rules table the practice owns.** Each visit type has a name, length, eligible providers, locations, and the question that decides it. The bot reads it; it does not invent types or lengths.
2. **Never offer a type, provider, length or location that is not a row in the table.** If the request fits no row, hand off (see hand-off rule).
3. **Ask the one or two questions that decide the type**, and only those: for example "Have you seen this provider or their group in the last 3 years?" or "Is this a check-up on something we treated, or a new problem?" Skip a question the record already answers.
4. **Use the practice's definition of new and established.** If the table says three years, ask about three years, and about the same group or specialty as the practice defines it. Do not reword the rule.
5. **Match the provider to the reason, from the table.** If no listed provider treats the stated reason, say so and offer the options the table allows.
6. **Read back provider, visit type, length and location before booking**, in one message, and book only after the patient says yes.
7. **Say what a type means in plain words**, such as "a follow-up is shorter and for something we already treated", so the patient can correct a wrong guess.
8. **After booking, say how to change it.** Mention cost or billing differences only if the practice's table says so; never quote prices the bot was not given.
9. **Log the type, the answers that chose it, and the table version** so a later reschedule reason can be tied back.

**Reference design: visit-type decision table (the practice fills this in)**
| Stated need | Deciding question | Visit type | Length | Eligible providers | Location |
|---|---|---|---|---|---|
| Back for an ongoing problem | Seen this group in the past 3 years? | Yes: follow-up; No: new patient | per table | per table | per table |
| A procedure | Which procedure? (pick from list) | Procedure visit | per table | per table | per table |
| A new problem | Seen this provider before? | New problem or new patient | per table | per table | per table |
| Anything else or unclear | none | Hand off to scheduling staff | n/a | n/a | n/a |

```
Book only a visit type, length, provider and location that is a row in the practice's visit-type table.
Ask only the questions the table lists for the stated need; skip any the record already answers.
Before booking, read back provider, visit type, length and location in one message and wait for a yes.
If the request matches no row, or the answers conflict with the record, offer the front desk; never choose a nearest type.
Do not judge how urgent or serious the problem is, and do not give medical advice.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The answer decides the type, such as "seen this group in 3 years?". Do not ask it when the record already shows the answer. |
| Offer choices: 2-4 options plus "Something else", free text open | The need could map to a few rows: "Follow-up", "New problem", "Procedure", "Something else". Do not offer them when the patient named a row exactly. |
| Admit uncertainty and show how to check | The record and the patient disagree: say what the bot sees and offer to have staff confirm. |
| Hand off to a person | No row fits, the table and record conflict, or the patient says the type is wrong. |

**Don't over-correct.** Do not ask five questions before showing a slot; ask only the one or two the table needs. Do not give clinical advice or decide who "needs" a certain provider; the table decides eligibility and staff decide anything clinical. If the patient describes symptoms that may be urgent, follow your triage rules and see [triage wording understates or overstates urgency](triage-wording-understates-or-overstates-urgency.md); this pattern is only about matching a stated need to a visit type. Do not repeat the read-back as a separate "are you sure?" step after the patient said yes (see [over-confirmation](../../dialogue-management/failures/over-confirmation.md)).

**Hand-off rule.** Offer scheduling staff when no table row fits, the patient disagrees with the type, or the record and the answers conflict. Pass on the stated need, the answers given, the type the bot would have chosen, and the table version, so the patient does not repeat themselves.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | "See Dr. Patel again" with a visit 14 months ago | 3, 4 | Asks the 3-year question or uses the record, books follow-up |
| 2 | A procedure that needs a longer slot than a check-up | 1, 2 | Books the length in the table, not a default slot |
| 3 | Reason that no listed provider treats | 5 | Says so and offers table options or staff; books none |
| 4 | Any booking | 6 | One message with provider, type, length, location before saving |
| 5 | Patient answer contradicts the record | 3, hand-off | Names the conflict and offers staff; does not pick a type |
| 6 | Request fitting no row | 2, hand-off | Offers the front desk; no invented type |
| 7 | Patient mentions chest pain while booking | Don't over-correct | Follows triage rules; gives no advice about the visit type |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Rescheduled-for-wrong-type rate** (primary) | Set from a baseline | Reschedules tagged "wrong visit type, provider or length" divided by bookings made in chat | Rising two weeks in a row |
| Bookings with a read-back of provider, type, length, location | 100% | Log the read-back turn before the booking write | Below 95% |
| Bookings with a type that is a row in the table | 100% | Compare booked type, provider, length to the table version | Any miss |
| Hand-offs where no row fit | Track; set from baseline | Count hand-offs with reason "no matching row" | Sudden jump (table gap or wrong tagging) |
| Questions asked before the first slot (counter-metric) | 2 or fewer | Count bot questions before slots shown | Over 3 |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Booking saved with no read-back turn | Booking write event with no preceding read-back message | Patient rebooking the same details after a cancellation |
| Booked type or length is not in the table | Booking event vs table version | A table update after the booking |
| Reschedule reason is wrong type, provider or length | Reschedule event reason field | Patient changed their mind about the date |
| Patient says "I'm not new" or "that's too short" after booking | Post-booking user turn | Patient testing the bot |
| Staff changes type on a chat booking | Change event by staff user | A change for a clinical reason the bot could not know |

**Starter rule:** before booking, read back provider, visit type, length and location from the practice's visit-type table and wait for a yes.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: scheduling-picks-the-wrong-provider-or-visit-type
runs: pre_send
reads: [visit_type_table.version, patient_record.last_visit_with_group, booking_draft.type, booking_draft.provider, booking_draft.length, booking_draft.location]
trigger: a booking is about to be saved
moves: [ask_one_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Follow-up", "New problem", "Procedure", "Something else"]
on_miss: ask
metric: rescheduled-for-wrong-type rate
counter_metric: questions asked before the first slot
status: proposed
```

## 8. Related patterns
- [Bookings without confirming details](../../voice-receptionist-agents/failures/bookings-without-confirming-details.md): the read-back of name, number and time. This pattern reads back the visit itself (type, provider, length, place) and fixes how the type is chosen.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the general rule for asking versus guessing. This page applies it to the two or three facts that decide a visit type.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the opposite risk. One read-back is the confirmation; do not add more.
- [Triage wording understates or overstates urgency](triage-wording-understates-or-overstates-urgency.md): how urgent a problem sounds. This page is only about visit type and provider.
- [Medication instructions misunderstood](medication-instructions-misunderstood.md): another place patient-facing wording can mislead.

## 9. Common questions
### Why did the chatbot book me as a new patient when I have been there before?
It likely never asked, or never checked your record. Many practices define new versus established by whether anyone in the same specialty and group saw you in the past three years (see section 4); the bot needs that question or the record.

### How do I set up visit types for an AI scheduling assistant?
Give it a table the practice owns: visit type, length, eligible providers, locations, and the question that decides it. Many scheduling systems already store length and type (see section 4); the bot should read that source, not guess.

### Should the chatbot decide which doctor I need?
It should match your stated reason to the practice's rules and offer what the table allows. It should not judge what is medically right for you; staff and clinicians do that.

### How many questions is too many before booking?
Ask the one or two that decide the type, and skip any the record answers. More than that and patients leave; the starting limit in section 7 is a number to tune, not a sourced one.

### Is the read-back an extra confirmation step?
It is the one confirmation. It lists provider, type, length and location once, and the booking is saved after the patient says yes.

---
## Technical section

### T1. Solution architecture
```
patient message -> intent (need) -> rules table lookup (rows for need)
   -> record check (last visit with group) -> 0-2 deciding questions
   -> draft booking (type, length, provider, location) -> validator (is every field in the table?)
   -> read-back message -> patient yes -> booking write + log (answers, table version)
no row / conflict -> hand off to staff with context
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Booking fields must come from the table | Booking validator before write | Tests 2, 6 |
| No write before a read-back and a yes | Orchestration layer | Test 4 |
| No triage or clinical judgment in scheduling replies | Prompt and output check | Test 7 |

### T3. Evals
- **Dataset:** 100 scheduling requests built from your own table and de-identified past reschedules, covering each row, near-misses, new vs established edge cases, and no-match requests.
- **Judge rubric:** did the bot pick a row from the table, ask only the deciding questions, read back all four fields, and hand off when no row fit?
- **Metrics and starting thresholds:** table-valid bookings 100%; read-back 100%. Starting points to tune.
- **Release gate:** block a deploy if any eval booking has a type, provider or length not in the table.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Bookings with a type not in the table | Any | Several in a day | Check the validator and table version |

### T5. Trade-offs
- The table needs an owner and updates; a stale table books confidently wrong.
- More questions improve accuracy but cost completion; keep to the deciding ones.
- Payer rules can differ from the practice's own definition of new and established (UTMB note, section 4); the practice must decide which governs.

---
### Deep dive
- **Open question.** I found no rate for wrong-visit-type errors in AI scheduling chat. The evidence is coding definitions, vendor documentation, and one misrouted-booking study from another setting.
- **References.** [UTMB newsletter, 2023](https://www.utmb.edu/fgp/newsletter/article/newsletter/2023/11/08/coding-clip-nov23) (opened); [athenahealth Appointment Types](https://help.athenahealth.com/Ohelp/Content/Appointment_Types_PH.htm) (opened); [Keona Health](https://keonahealth.com/resources/the-3-ways-to-address-patient-scheduling-errors) (opened); [Turkmedline abstract](https://turkmedline.net/detay/analysis-of-erroneous-appointments-from-the-thoracic-surgery-outpatient-clinic-of-a-training-hospital-research/f28b9289791d0547/tr/541%2B2023%2B8%2B2) (opened).
