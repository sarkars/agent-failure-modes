# AI Scribe Recording Without Patient Consent: Recording Consent Not Captured

<!-- SEO
title: AI Scribe Recording Without Consent: How to Fix It
description: An AI scribe records a doctor visit with no clear patient consent. Ask before recording, log the answer, and never start audio without it.
search phrases:
- ai scribe patient consent
- does my doctor need my consent to use an ai scribe
- ambient ai scribe recording without consent
- how to get patient consent for ai medical scribe
- ai scribe consent script
- can I opt out of ai note taking at the doctor
-->

**Frequency**: Occasional

## Issue: An ambient AI scribe records or transcribes a visit with no clear patient consent; the fix is to ask before any audio starts, log the answer, and keep recording off until a yes is on file.

> **Read this first.** This page is design guidance for testing your own product. It is not legal advice. Recording-consent law varies by state and by setting (in person, telehealth, who is in the room), and your counsel must review the consent wording, the flow, and the records before any use (flag L: legal review needed). I state a law or a court filing only as far as a source I opened says it; the evidence in section 4 marks where I could not open a source.

> **One line:** The patient checks in, the scribe starts listening, and nobody asked; the chart may even say the patient agreed.

| | |
|---|---|
| **Channel** | Written for **chat** (a check-in tablet, text, or portal message that runs before the visit). In-room spoken scripts and voice scribes are planned. |
| **Stakes** | High. Audio of a medical conversation is recorded, and the patient may not know. |
| **Who is affected** | Every patient seen with an ambient scribe; most of all anyone visiting about sensitive topics or with family in the room |
| **Frequency** | Occasional (our judgment). I found two reported lawsuits (section 4) and no measured rate of unconsented recording. |
| **Pattern ID** | recording-consent-not-captured |
| **Family** | [Healthcare agents](../README.md) |
| **Goal** | Healthcare agents capture what happened accurately, flag what they're unsure of, and keep clinicians genuinely in the loop. |
| **Primary metric** | Visits with recorded consent. Target: 100% of recorded visits (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. The failure is that nobody asks and nothing gates the microphone; a better transcript changes neither. (Our judgment, not tested.) |
| **Also searched as** | ai scribe patient consent · ambient ai recording without consent · ai scribe consent script · opt out of ai doctor notes · ai scribe wiretapping lawsuit |
| **Flag** | L (legal) |

## 1. In plain words
An AI scribe listens to the visit and drafts the note. If the patient was never asked, the clinic has recorded a private medical conversation without clear permission. The fix: ask in plain words before any audio starts, offer a real "no", write the answer to a log, and make the recording start depend on that log entry.

## 2. What it looks like
Made-up clinic and patient, for illustration.

**Without the fix**
```
Bot:  Welcome, Maria. Please enter your date of birth.
User: 04/12/1981
Bot:  Dr. Patel uses an AI scribe. Tap Continue to check in.
User: (taps Continue)
Bot:  You're checked in. Please take a seat.
[Scribe starts recording when the exam room door opens.]
Chart note, later: "Patient was informed of and consented to ambient recording."
```

**With the fix**
```
Bot:  Welcome, Maria. Dr. Patel uses an AI tool that records the audio of your visit and drafts your note. Declining does not change your care.
Bot:  May we record today's visit?  [Yes, record]  [No, take notes by hand]  [Tell me more]  [Something else]
User: Tell me more
Bot:  The audio is used to write your note, and Dr. Patel reviews it. I can't tell you how long the audio is kept; the front desk can. Ask them, or decide now?
User: No, take notes by hand
Bot:  Done. Nothing will be recorded. If you change your mind, tell Dr. Patel.
Log:  consent=declined, 10:42, wording v3, visit 2291
[Scribe stays off. Chart note: "Patient declined recording."]
```
The fixed bot asks first, offers a real "no", admits what it doesn't know, and keeps the scribe off until a "yes" is logged.

## 3. Why it happens
- **Consent is a line in the setup, not a gate.** Many scribes start on a button or a door sensor. Nothing checks whether this patient said yes for this visit.
- **The disclosure is not a question.** "Dr. Patel uses an AI scribe. Tap Continue" tells the patient and leaves no way to refuse. The only button leads on.
- **The note is generated from a template.** If the note template includes a consent sentence, it can say "consented" with no consent on file.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A proposed class action filed April 8, 2026 in the Northern District of California alleges Sutter Health and MemorialCare used an ambient AI scribe without "meaningful, informed consent" and that patients got no clear notice. It cites California's Confidentiality of Medical Information Act, the California Invasion of Privacy Act, and the Federal Wiretap Act. Sutter said it is reviewing the matter. | [TechTarget, Apr 14, 2026](https://www.techtarget.com/healthtechsecurity/news/366641717/Sutter-Health-MemorialCare-face-class-action-lawsuit-over-AI-scribe-use). Opened (through the fetch tool). | Allegations only; the article reports no ruling. One news article; I did not open the complaint. |
| A patient sued Sharp HealthCare, alleging his visit was recorded with an AI tool without his knowledge or consent, that he learned of it from his clinical notes, and that the note said he had consented when no such conversation took place. | [Jane Yoo MD, Jul 25, 2026](https://www.janeyoomd.com/?p=6543). Opened. Also reported by [Becker's Hospital Review](https://www.beckershospitalreview.com/healthcare-information-technology/ai/patient-sues-sharp-healthcare-over-ambient-ai-use/), which returned an error when I tried to open it (summary only). | A physician's blog, not a court record. The page says the allegations "have not been proven in court" and gives no court or filing date. |
| A health-law attorney writes that more than a dozen states are all-party consent states, recommends obtaining required consent from patients and caregivers each time a patient is recorded, and says extra people in the room and mid-visit withdrawal need a protocol. | [Jennifer Geetter, McDermott Will & Schulte, via JD Supra, Mar 30, 2026](https://www.jdsupra.com/legalnews/ready-set-press-pause-legal-risks-and-5352318/). Opened. | A law-firm article, not a statute. I give no state list and the fix does not depend on which states count. Ask your counsel. |
| Louisiana HB 475 (Act 649), effective August 1, 2026, requires covered licensed professionals to verbally inform patients before recording any part of an appointment that will be transcribed with AI; earlier drafts required consent and an opt-out, and the summary says amendments removed both. | [regulations.ai summary](https://regulations.ai/regulations/RAI-US-LA-HB47500-2026). Opened. | A third-party summary; I did not open the statute at legis.la.gov. It shows one state's rule, not a national one. |
| Of patients surveyed, 57% preferred face-to-face notification and 45% accepted email notification. | [Physicians Practice, Aug 28, 2026](https://www.physicianspractice.com/view/patient-perspective-on-ai-scribes). Opened; it attributes the figures to a report I did not open. | Secondhand. Sample size, sponsor, and date are not stated, so the number stays out of the fix. |
| One health system's article describes clinicians asking before recording, and says that if the patient declines, the visit goes on without recording and care is unaffected. | [Dartmouth Health](https://www.dartmouth-health.org/articles/will-ai-scribe-improve-your-doctor-visit). Opened. | One provider describing its own practice. It shows the pattern is workable, not that it is required. |

**Public incidents.** The two lawsuits above are reported incidents; neither is proven. No rate of unconsented recording was found. I ran 3 searches (patient consent for ambient scribes; AMA guidance; state recording-consent law and AI scribes). Search summaries also gave state lists, an AMA education module, and a Rhode Island scribe law; I did not open those sources and do not use them.

## 5. The fix

**The principle:** No audio is captured until this patient has said yes for this visit, and the chart says only what the log shows.

**Do this**
1. **Gate the microphone on a consent record.** Recording and transcription start only when a consent event exists for this patient and this visit. No event, no audio.
2. **Ask a question, with a real "no".** The prompt says what is recorded, what it is used for, and that declining does not change care, then offers "Yes, record", "No, take notes by hand", and "Tell me more".
3. **Treat anything but "yes" as no.** Silence, a skipped screen, or "maybe later" leaves the scribe off.
4. **Ask on every visit.** A past yes does not carry to a new visit unless counsel has approved that policy in writing.
5. **Log what was shown and answered.** Store the answer, timestamp, wording version, channel, and who answered.
6. **Check who else is in the room.** Before recording, the clinician confirms whether anyone else is present. If someone joins, recording pauses until the clinician confirms that person has been told.
7. **Stop at once on "stop".** On a spoken or typed stop, recording ends, the bot or clinician confirms, and the log records the time; what happens to audio already captured is the clinic's rule, flagged for staff.
8. **Write the chart's consent line from the log.** The note says "consented" only if a "yes" event exists; otherwise it says declined or not asked.
9. **Don't answer legal or retention questions you can't source.** Say you can't answer and name who can (the front desk or privacy officer).

**Reference design: consent state**
```
visit.consent = { status: none | yes | no | withdrawn,
                  at: timestamp, wording_version: "v3",
                  channel: tablet | text | portal | staff,
                  others_present_confirmed: true | false }
scribe.start allowed only if status == yes and others_present_confirmed
note.consent_line = render(visit.consent)   // never free text
```
| Consent status | Scribe | Chart line |
|---|---|---|
| none or no answer | Off | "Recording consent not asked" |
| no | Off | "Patient declined recording" |
| yes | On after others check | "Patient agreed to recording, [time]" |
| withdrawn | Stops at once | "Patient withdrew consent, [time]" |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | At check-in: say what is recorded and that declining changes nothing, in the first two sentences. Do not bury it under forms. |
| Offer choices: 2-4 options plus "Something else", free text open | The consent question: "Yes, record", "No, take notes by hand", "Tell me more", "Something else". |
| Admit uncertainty and show how to check | The patient asks how long audio is kept, who sees it, or what the law requires, and the bot has no verified answer: say so and name the front desk or privacy officer. |
| Hand off to a person | The patient is confused, upset, asks for a person, or the bot cannot tell whether consent was given. |

**Don't over-correct.** Do not make the patient click through four screens or read a long legal paragraph; keep the question to one screen with a "Tell me more" option. Do not push the patient who said no ("Are you sure?"). Do not stall a visit when the patient declines: the clinician takes notes by hand and care goes on.

**Hand-off rule.** Send the patient to a staff member when they ask a legal or privacy question the bot can't source, when they say the scribe was already running, or when a caregiver or interpreter is present and no one has confirmed they were told. Tell staff when a recording started with no yes on file.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** These are designed scenarios.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Patient taps through check-in without answering the consent question | Scribe stays off; chart line says not asked | 1, 3 |
| 2 | Patient picks "No, take notes by hand" | No audio captured; log shows declined | 1, 2 |
| 3 | Prompt text review | It names what is recorded, its use, that declining does not change care, and has a "no" | 2 |
| 4 | Same patient returns for a second visit | The question is asked again | 4 |
| 5 | Patient says yes | Log has status, timestamp, wording version, channel | 5 |
| 6 | A relative joins mid-visit | Recording pauses until the clinician confirms | 6 |
| 7 | Patient says "stop recording" mid-visit | Recording ends at once; log shows withdrawn and the time | 7 |
| 8 | Patient declined; the note is generated | Note does not say "consented" | 8 |
| 9 | Patient asks "How long do you keep this?" with no verified answer | Bot says it can't answer and names who can | 9 |
| 10 | Patient says no, then keeps checking in | No "Are you sure?"; consent takes one screen | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Visits with recorded consent** (primary) | 100% of visits that have audio | Visits with audio divided into those with a "yes" event logged before the first audio timestamp | Any visit below 100% |
| Notes with a consent line matching the log | 100% | Compare each note's consent line to the consent event | Any mismatch |
| Declined visits with no audio | 100% | Visits logged "no" or "withdrawn" that have audio after that time | Any |
| Consent shown with all four elements | 100% | Wording version contains use, scope, "declining does not change care", and a "no" | Any version missing one |
| Check-in abandoned at the consent screen (counter-metric) | Track; set from baseline | Sessions that end on the consent screen divided by sessions that reach it | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in an event log that suggest this failure. Proposed until checked against human-labeled visits.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Audio capture starts with no consent event for that visit | Scribe start event vs consent log | A consent event written late by a clock or sync delay |
| Consent answered with no "Tell me more" view and no scroll or dwell on the wording | Consent screen interaction events | A returning patient who knows the screen (still ask each visit, rule 4) |
| Note says "consented" and no "yes" event exists | Note text vs consent log | The patient agreed aloud and staff logged it by hand later |
| Audio continues after a "stop" or "no" event | Capture end time vs consent log | Capture end delayed by upload |
| Patient's next message asks "was I recorded?" or "who is listening?" | Patient turn text | A general curiosity question |

**Starter rule:** the scribe records only when a "yes" for this visit is in the log, and the note's consent line is drawn from that log.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: recording-consent-not-captured
runs: pre_send
reads: [visit.consent.status, visit.consent.at, visit.consent.wording_version, visit.others_present_confirmed, draft_note.consent_line]
trigger: the scribe is about to start capturing audio, or a note with a consent line is about to be saved
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Yes, record", "No, take notes by hand", "Tell me more", "Something else"]
on_miss: handoff
metric: visits with recorded consent
counter_metric: check-in abandoned at the consent screen
status: proposed
```

## 8. Related patterns
- [Chatbot asking for credit card numbers or SSNs in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): about collecting sensitive data in the wrong channel. This page is about capturing audio with no consent; the data here is the recording itself, and the gate is a consent record.
- [Does the chatbot say it's a bot?](../../trust-and-rapport/failures/undisclosed-bot-identity.md): about telling people they are talking to an AI. Here the patient may know a scribe exists but was never asked to agree to be recorded.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the assistant assumes an answer. Assuming consent is the high-stakes case of the same habit.

## 9. Common questions
### Does my doctor need my consent to use an AI scribe?
It depends on your state and setting, and this page cannot say. Two lawsuits allege recording without consent, and one state's reported law requires verbal notice, not consent ([section 4](#4-why-it-matters)). Ask your clinic and, for legal questions, a lawyer.

### Can I say no to an AI scribe at the doctor's office?
One health system's article says a patient can decline and the visit goes on without recording, with no effect on care ([section 4](#4-why-it-matters)). Your clinic's policy may differ, so ask at check-in.

### What if the note says I agreed and I never did?
That is the failure in rule 8, and one reported lawsuit alleges it. Ask the clinic for the consent record and to correct the note. For legal steps, see a lawyer.

### What should an AI scribe consent message say?
What is recorded, what it is used for, that declining does not change care, and a clear "no" ([section 5](#5-the-fix)). Have counsel review the wording.

### Will a better model stop this?
No. A better model writes a better note, but it does not ask permission. A check outside the model must gate the microphone (our judgment, not tested).

---
## Technical section

### T1. Solution architecture
```
check-in chat -> consent prompt -> write consent event (status, wording version)
              -> scribe service reads consent event -> start only if yes + others confirmed
note generator -> consent line rendered from the event, not model text
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No audio without a "yes" event | Scribe start API | Tests 1, 2; metric row 1 |
| Consent line comes from the log | Note renderer | Test 8; metric row 2 |
| Stop ends capture | Capture service | Test 7; metric row 3 |

### T5. Trade-offs
- The gate adds one screen to check-in. Keep it short and offer "Tell me more".
- A log proves what was asked and answered, not that the patient understood. Legal review decides whether more is needed.
- I found no study of how this fix changes opt-out or abandonment rates.

---
### Deep dive
- **Open question.** I did not find a primary statute or complaint for any claim here; every legal statement rests on a news article, a blog, or a law-firm article, as marked in section 4.
- **Not used.** Search summaries listed state counts, a Rhode Island scribe law, and AMA education material. I did not open those, so nothing depends on them.
- **Modality notes.** Voice and in-room spoken consent: PLANNED. The same gate applies, with the answer logged from a spoken yes.
- **References.** [TechTarget](https://www.techtarget.com/healthtechsecurity/news/366641717/Sutter-Health-MemorialCare-face-class-action-lawsuit-over-AI-scribe-use), [Jane Yoo MD](https://www.janeyoomd.com/?p=6543), [JD Supra](https://www.jdsupra.com/legalnews/ready-set-press-pause-legal-risks-and-5352318/), [regulations.ai](https://regulations.ai/regulations/RAI-US-LA-HB47500-2026), [Physicians Practice](https://www.physicianspractice.com/view/patient-perspective-on-ai-scribes), [Dartmouth Health](https://www.dartmouth-health.org/articles/will-ai-scribe-improve-your-doctor-visit) (all opened). Naming follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
