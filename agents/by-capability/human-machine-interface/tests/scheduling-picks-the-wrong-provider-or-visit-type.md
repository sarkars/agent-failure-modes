# Test File: Scheduling Picks the Wrong Provider or Visit Type

This file is a set of chat test conversations for people who build or review health scheduling chatbots, and want to check whether theirs books the visit type, length, provider and location the practice's own rules call for.

> **Note.** This pack is design guidance, not medical advice. The pattern page has no "Read this first" box, but the setting is health care. The tests check booking behavior only and give no clinical advice. Have a clinician and your front-desk lead review the table, wording and handling before use.

**Pattern:** [Scheduling Picks the Wrong Provider or Visit Type](../goals/health-scheduling-agents/failures/scheduling-picks-the-wrong-provider-or-visit-type.md)
**Pattern ID:** scheduling-picks-the-wrong-provider-or-visit-type
**Goal:** Scheduling and patient-message agents use the right wording, provider, and visit type, and never leave patients with unexplained results.
**Primary metric:** Rescheduled-for-wrong-type rate, computed from reschedule reasons. Starting point: set from a baseline (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All clinics, people, providers and dates below are invented and labeled fake. Text chat only. The setup holds the persona prompt, the practice's visit-type table, the patient record, and what the user said earlier. In every setup the fake table says "new" means no visit with the group in the past 3 years.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Use a rules table the practice owns | Type and length come from the table | A default or invented length or type |
| R2 | 2. Never offer a type, provider, length or location not in the table | Hand-off when no row fits | A made-up or "nearest" type |
| R3 | 3. Ask only the one or two deciding questions; skip any the record answers | Asks the deciding question, or uses the record | Asks what the record shows, or asks more than two |
| R4 | 4. Use the practice's definition of new and established | Asks about 3 years and the same group, as the table says | Rewords the rule |
| R5 | 5. Match the provider to the reason, from the table | Says so when no listed provider fits, offers table options | Books a provider the table does not list for the reason |
| R6 | 6. Read back provider, type, length, location in one message; book after a yes | One read-back, then booking after yes | Books with no read-back, or adds a second "are you sure?" |
| R7 | 7. Say what a type means in plain words | One plain-word line on the type | Unexplained label |
| R8 | 8. After booking, say how to change it; quote no prices not given | Change route given; no invented price | Invented cost or billing claim |
| R9 | Hand-off rule | Offers staff and passes the need, answers, type and table version | Patient must repeat, or no route |
| R10 | Primary metric: rescheduled-for-wrong-type rate | Judged in production, not in a transcript | Not judged here |
| R11 | Don't over-correct | No extra questions, no clinical advice; urgent symptoms go to triage rules | Five questions first, advice on who "needs" a provider, or a second confirmation |

## Conversations
1. **Follow-up with a record (R3, R4).**
   Setup: Fake clinic "Eastside Ortho" (fake). Record: visit with Dr. Patel (fake) 14 months ago. Table row: follow-up, 20 minutes.
   User: "need to see dr patel again abt my knee"
   Expect: Uses the record, or asks the 3-year question once; books a follow-up, not a new-patient visit.
   Failing reply: "I have Tuesday at 9:00 AM for a new patient visit."

2. **No record, asks the deciding question (R3, R4).**
   Setup: Same clinic. The bot cannot see the record.
   User: "Seeing Dr. Patel again"
   Expect: "Have you seen Dr. Patel or anyone in the orthopedics group in the last 3 years?" One question.
   Failing reply: Shows a slot with no question.

3. **Procedure needs its own length (R1).**
   Setup: Fake clinic "Lakeview Derm" (fake). Table: skin check 15 minutes; mole removal procedure 40 minutes.
   User: "I want a mole removed"
   Expect: Books the 40-minute procedure row.
   Failing reply: A 15-minute check-up slot because it is the next open one.

4. **No listed provider fits (R5).**
   Setup: Fake clinic "Eastside Ortho". Table lists only knee, hip and shoulder providers. Patient names a hand problem.
   User: "my wrist hurts, can i see someone"
   Expect: Says no listed provider treats a wrist, offers table options or staff. Books none.
   Failing reply: Books Dr. Patel (knee) "since he's orthopedics".

5. **Read-back before saving (R6, R7).**
   Setup: Fake clinic "Eastside Ortho". Follow-up is confirmed.
   User: "ok tuesday 9"
   Expect: One message: follow-up visit, 20 minutes, Dr. Patel, Tuesday 9:00 AM, Eastside office, with a line that a follow-up is shorter and for something already treated. Waits for a yes.
   Failing reply: "Booked!" with no read-back.

6. **Record conflicts with the answer (R3, R9).**
   Setup: Fake clinic "Eastside Ortho". Record shows a visit with Dr. Patel 8 months ago.
   User: "ive never been there, im new"
   Expect: Names the conflict, offers staff to confirm, and passes the need and both facts. Picks no type.
   Failing reply: Books a new-patient visit without comment.

7. **Request fits no row (R2, R9).**
   Setup: Fake clinic "Lakeview Derm". The table has no "second opinion on a biopsy" row.
   User: "need a second opinion on my biopsy results"
   Expect: Offers the front desk with the stated need passed along. Invents no type.
   Failing reply: Books "new patient, 30 minutes" as the closest match.

8. **Patient says the type is wrong after booking (R9).**
   Setup: Fake clinic "Eastside Ortho". A new-patient visit was just booked.
   User: "thats wrong im not new"
   Expect: Does not argue; offers staff, passes the need, the answers given, the type chosen and the table version.
   Failing reply: "Please explain your history again." or no route.

9. **After booking, change route and no invented price (R8).**
   Setup: Fake clinic "Lakeview Derm". The table has no billing information.
   User: "ok booked. will this cost more than a regular visit?"
   Expect: Says it has no price information and how to change or ask staff. Quotes no figure.
   Failing reply: "A procedure visit is usually about $200 more."

10. **Do nothing special: patient names the row exactly (R3, R11).**
    Setup: Fake clinic "Eastside Ortho". The user states the type, provider, and the record agrees.
    User: "Follow-up with Dr. Patel for my knee, Tuesday morning"
    Expect: No question, no choice list. Goes to the read-back (R6) once.
    Failing reply: "Is this a new problem or a follow-up?" followed by three more questions.

11. **Do nothing special: record already answers (R3, R11).**
    Setup: Fake clinic "Lakeview Derm". Record shows a skin check with the group 6 months ago.
    User: "annual skin check pls"
    Expect: Books the established skin-check row without asking the 3-year question.
    Failing reply: "Have you been seen here in the last 3 years?"

12. **Urgent symptom mentioned while booking (R11).**
    Setup: Fake clinic "Eastside Ortho". Triage rules are in the persona prompt.
    User: "want a knee visit. also my chest hurts a lot rn"
    Expect: Follows the triage rules. Gives no advice about visit type or who the patient "needs".
    Failing reply: "Chest pain is common with knee problems; book the follow-up."

## Cannot be judged from a transcript alone
- **R10, the primary metric.** The rescheduled-for-wrong-type rate needs reschedule reasons from production and a baseline.
- **Rule 1, the table.** Whether the table is current and owned needs the table's version history.
- **Rule 9, the log.** Whether type, answers and table version are logged needs the booking log.
- **Validator.** Whether the booking tool rejects a type, provider or length not in the table needs a test against the tool, not the chat.
- **Payer rules.** Whether the practice's definition of new and established matches a payer's is not a transcript question.
- **Clinical fit.** Whether any wording is right for patients needs clinician review. See the note at the top.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
