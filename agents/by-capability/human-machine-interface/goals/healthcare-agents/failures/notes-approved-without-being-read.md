# AI Scribe Notes Signed Without Review: Notes Approved Without Being Read

<!-- SEO
title: AI Scribe Notes Signed Without Review: How to Fix It
description: Clinicians sign AI-drafted visit notes without reading them. Make review effortful where risk is high: flag uncertain items and link each to the visit.
search phrases:
- ai scribe notes signed without review
- ambient ai scribe automation bias
- clinicians not reviewing ai generated notes
- how to make clinicians review ai scribe notes
- ai scribe note review interface design
- ai scribe errors missed by physicians
- ambient documentation rubber stamp sign button
- ai scribe seeded error test
-->

**Frequency**: Common

## Issue: Clinicians sign AI-drafted visit notes without reading them; the fix is to make review effortful where the risk is high, with changes and uncertain items marked and each one tied to what was said in the visit.

> **One line:** The scribe delivers a clean, finished-looking note with one Sign button, so the allergy or dose that is wrong gets the same two seconds of attention as the template line above it.

> **Read this first.** This page is design guidance, not clinical or legal advice. It states clinical findings only as far as the sources I opened say them, and I did not verify how any law, accreditation rule, or payer policy applies to your product. Clinical informatics, patient safety, and compliance staff need to review any design here before use with real patients.

| | |
|---|---|
| **Channel** | Written for the **visual** note-review screen of an ambient scribe (a draft note plus a side panel of messages). Voice and chat-only versions are not written. |
| **Stakes** | High. A signed note becomes part of the medical record that later clinicians read as fact. |
| **Who is affected** | Clinicians who sign AI-drafted notes, and patients whose records carry an error nobody caught |
| **Frequency** | Common (our judgment). One pilot found 14.9% of notes left entirely unedited, but unedited is not the same as unread. I found no measured rate of unread approvals. |
| **Pattern ID** | notes-approved-without-being-read |
| **Family** | [Healthcare agents](../README.md) |
| **Goal** | Healthcare agents capture what happened accurately, flag what they're unsure of, and keep clinicians genuinely in the loop. |
| **Primary metric** | Seeded-error catch rate in drills on synthetic notes. Starting target: 90% or higher on high-risk items (tune with clinical leads). Its production pair, approvals under a minimum read time, is in section 7. |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. A better scribe makes fewer errors, and the Medical Economics commentary in section 4 argues that this lowers scrutiny of each note. The review step has to be designed. (Our judgment, not tested.) |
| **Also searched as** | ai scribe automation bias · clinicians rubber stamp ai notes · ambient ai scribe review burden · ai scribe errors physicians miss · sign without reading ai note · ai scribe seeded errors |
| **Flag** | E (expert review needed) |

## 1. In plain words
An ambient AI scribe listens to a visit and drafts the note. The clinician is supposed to check it and sign. When the draft is mostly right and the only control is one Sign button, checking becomes a glance, and a wrong dose, an invented finding, or a left-out symptom goes into the chart. The fix is to spend the clinician's attention where the risk is: mark the items that matter, show what was actually said next to each one, list what was heard but left out, and require a deliberate act on those items only.

## 2. What it looks like
The scenario is made up for this page: a primary care follow-up at a US clinic.

**Without the fix**
```
Scribe:  Marcus T., 58, follow-up. Your note is ready.            [Sign note]
Note:    Plan: Continue lisinopril 20 mg daily. No known drug allergies. Return in 3 months.
Dr. Lee: [Sign note]    (note open for 6 seconds)
(In the visit audio the patient said "I'm on the 10 milligram," "penicillin gave me hives,"
 and "I get tight in my chest on the stairs." The note says none of these.)
```

**With the fix**
```
Scribe:  Marcus T. Note ready. 3 items need your check before you sign. 1 thing I heard is not in the note.
         1. Lisinopril dose. Heard: "I'm on the 10 milligram." Chart lists 20 mg. I left it blank: [dose unconfirmed]
            [10 mg] [20 mg] [Something else]
         2. Allergy. Heard: "penicillin gave me hives." Added: penicillin (hives). [Confirm] [Edit] [Remove]
         3. Plan line "Return in 3 months" was not stated in the visit. I inferred it. [Confirm] [Edit] [Remove]
         Heard but not in the note: "tight in my chest on the stairs." [Add to note] [Not relevant] [Something else]
         The rest of the note is routine text and signs with one click once items 1 to 3 are resolved.
```
The fixed scribe marks what it could not settle, puts the spoken words beside each item, lists the omission, and lets the clinician sign routine text in one step.

## 3. Why it happens
- **A good first draft lowers scrutiny.** The Medical Economics commentary in section 4 argues that the better the scribe, the less attention each note gets. This is one commentator's argument, not a measured result.
- **One Sign button treats every line the same.** An allergy and a boilerplate sentence look alike, nothing marks which sentences the scribe was unsure about, and the note reads as finished prose. (Our reading.)
- **Omissions leave nothing to see.** A reviewer checks what is written. The most frequent error in the UC Davis pilot was an accidental omission, and a missing symptom shows up only if the reviewer remembers it or can compare against the visit.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a UC Davis Health pilot, 31 physicians used an ambient scribe for 7,545 clinic notes (July to August 2024). Physicians rated 356 notes (4.7%): omissions in 64 (18%), hallucinations in 41 (11.5%), accidental inclusions in 33 (9.3%). 19 notes (5.3%) had an error rated as serious or imminent risk. The authors write that "careful clinician review of notes remains imperative." | [Taylor et al., JMIR Medical Informatics 2026;14:e86474](https://escholarship.org/uc/item/9r89g3sp). Opened (PDF text). | One health system, volunteer early adopters, physicians rated their own notes, severity ratings were subjective, and only 4.7% of notes were rated. The authors list these limits. |
| In the same pilot, 14.9% (143/960) of AI notes were not edited at all, and the median share of words changed was 9.0%. Average edits per physician ranged from 1.9% to 69.3%. | Same paper. Opened. | The edit metric came from the vendor and was available for only 960 notes (12.7%). Editing measures effort, not reading: a note can be read and correct. |
| A preprint audited three commercial scribes on 142 consultations (565 notes) and reports that 31.3% of notes (interval 27.0 to 35.6) contain at least one verified failure, concentrated in allergy and medication information, invented patient identity, and examinations written up for telephone visits. The authors say the review instruction alone moved the share of candidates verified from 9.3% to 79.0%. | [Fox et al., arXiv 2608.31017, Aug 31, 2026](https://arxiv.org/abs/2608.31017). Opened (abstract page and PDF text). | Preprint, not shown to be peer reviewed. Notes came from recorded consultations run through the products, and errors were found by AI panels with clinician spot checks. It is not a measure of what clinicians catch, and the authors say failure rates depend on the instrument that counted them. |
| The Australian Commission on Safety and Quality in Health Care warns that clinicians are "susceptible to automation bias when they accept ambient AI scribe outputs as being accurate and complete." | [Bala, Medical Economics, Jun 23, 2026](https://www.medicaleconomics.com/view/is-ai-turning-you-from-physician-to-proofreader-). Opened. | A commentary. The commission's guidance is quoted second hand; I did not open it. It is Australian. |
| A systematic review of automation bias in decision support kept 74 of 13,821 papers. It reports mitigators that include training and emphasizing user accountability, and that prominent wrong advice is more likely to be followed. | [Goddard, Roudsari, Wyatt, JAMIA 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751). Opened (read through the fetch tool). | Decision support, not scribes, and from 2011-era studies. The review notes that automation bias is often found incidentally and that only four studies were pooled. |

**Public incident.** I did not find a public incident traced to an unread scribe note. I ran 4 searches (scribe sign-off and automation bias, seeded-error studies, omission and hallucination rates, review-interface designs and automation bias). A blog post about a Lancet seeded-error simulation and a JMIR viewpoint on the limits of review appeared only in search summaries; I did not open them and do not use their claims. I found no controlled study of highlighted or transcript-linked review screens. That is a search result, not proof none exists.

## 5. The fix

**The principle:** Spend the clinician's attention where an error would do harm, and make it impossible to sign those items without a deliberate act.

**Do this**
1. **Sort the note into high-risk and routine items before showing it.** High-risk means allergies, medications and doses, diagnoses added or changed, orders, negative statements ("denies," "no known allergies"), and any sentence the scribe inferred. Show the count at the top: "3 items need your check."
2. **Show what was said beside each high-risk item.** Put the spoken words (or "not stated in the visit") next to the written item, with a link to the audio or transcript passage.
3. **Do not fill a gap with a plausible value.** If the dose, side, or date was not stated or the audio was unclear, leave a visible marker such as `[dose unconfirmed]`.
4. **List what was heard and left out.** Below the note, show clinically relevant statements from the visit that did not reach the note, with Add and Not relevant buttons.
5. **Require one deliberate act per high-risk item.** Confirm, Edit, or Remove, each separately. No "Confirm all" for high-risk items. Sign stays disabled until each is resolved.
6. **Keep routine text to one step.** A note with no high-risk items signs with one click and no extra prompts.
7. **Log what the clinician actually did.** Record, per item, the action and time, and the time the note was open. Do not record "reviewed" for a note signed with unresolved items.
8. **Test with seeded errors on synthetic notes only.** Plant known errors, including omissions, in practice notes made from synthetic encounters and measure how many get caught. Never plant an error in a real chart.

**Reference design: note-review panel**
```
Header:   <n> items need your check · <m> heard but not in the note
Item:     <section> · Heard: "<quote>" [play] · Note says: <text> · [Confirm] [Edit] [Remove]
Gap:      Not stated in the visit: <field>. Left as [<field> unconfirmed].
Omission: Heard but not in the note: "<quote>" · [Add to note] [Not relevant] [Something else]
Sign:     disabled until every item above is resolved; enabled with one click if there are none.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The scribe inferred an item or could not hear a value: say so, show the heard words, and mark the gap. Do not use it for a sentence copied directly from the clinician's dictation. |
| Offer choices: 2-4 options plus "Something else", free text open | At each flagged item: Confirm, Edit, Remove, Something else. Do not offer choices for routine template text. |
| Ask one clarifying question | One missing fact changes the entry, such as which dose. Ask it beside the item, not as a pop-up after Sign. |
| Hand off to a person | The audio is missing or unusable for a high-risk section, or the same clinician signs over unresolved items repeatedly. Do not hand off an ordinary routine note. |

**Don't over-correct.** If every line is flagged, the clinician stops reading the flags, which is the original failure again. Flag only the high-risk categories and the scribe's own inferences, and keep the count small. Do not add a pop-up on top of Sign for routine notes. Do not lock the chart so long that clinicians copy the note out and sign elsewhere. Do not treat time-on-screen alone as proof of reading.

**Hand-off rule.** If audio is unavailable or unclear for a high-risk section, tell the clinician to write that section themselves. If the log shows repeated sign-offs with unresolved items, route it to clinical informatics or the practice's patient safety lead, not to the clinician alone. Who acts on that log is a policy decision for your clinical and compliance leads.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **Not yet run.** These are designed drills on synthetic encounters.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Draft with a wrong dose, an added allergy, and an inferred plan line | All three appear in the "needs your check" list with the heard words beside them | 1, 2 |
| 2 | Visit audio where the dose is mumbled | The note shows `[dose unconfirmed]`, not a guessed value | 3 |
| 3 | A symptom said in the visit that the draft leaves out | It appears under "heard but not in the note" | 4 |
| 4 | Clinician clicks Sign with two unresolved items | Sign is blocked and names the two items; no "Confirm all" exists for them | 5 |
| 5 | Routine follow-up with no high-risk items | One click signs it; no extra prompt | 6 |
| 6 | Note signed with one item removed and one confirmed | The log holds each action and the open time, and no "reviewed" flag for a note signed with unresolved items | 7 |
| 7 | Seeded-error drill with planted commission and omission errors | Catch rate is computed per error type; no seeded error enters a real chart | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data and with clinical leads. I found no source that sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Seeded-error catch rate** (primary) | 90% or higher on high-risk items | Quarterly drills: planted errors in synthetic notes, share found or corrected, split by commission and omission | Below 80%, or a drop of 5 points from the last drill |
| Approvals under a minimum read time | Under 5% of notes with high-risk items | Share of signs where note-open time is below a floor set from timing a careful read of your own note types | Above 10%, or a rise for two weeks |
| High-risk items resolved individually | 100% | Item actions logged over flagged items at sign time | Below 100% (a path skips the gate) |
| Flags per note (counter-metric) | Track; set from baseline | Mean flagged items per note; also share of flags dismissed with no change | Rising for two weeks, which suggests flag overload |
| Added sign time on routine notes (counter-metric) | Near zero | Median seconds from open to sign for notes with no flags, before and after | Rises more than your baseline allows |

### Detection signals (proposed, not yet calibrated)
Signals in a note-review event log that suggest this failure. Proposed until checked against clinician-labeled reviews.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Note signed within a few seconds of opening, when it has flagged items | `note_opened` and `note_signed` timestamps | A short routine note, or the clinician watched the draft build live |
| Zero edits and zero item actions on a note with flagged items | Edit and item-action counts | Every flag was correct |
| Several high-risk items resolved in under a second each | Item-action timestamps | A scripted bulk action in the UI |
| Sign clicked with items still open (where the gate is not yet enforced) | `sign_attempt` with unresolved count above 0 | Clinician then went back and resolved them |
| Allergy or medication line in a signed note amended soon after | Amendment event on that field | The patient gave new information |

**Starter rule:** a note with high-risk items cannot be signed until each one is confirmed, edited, or removed by the clinician, with the words from the visit shown beside it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: notes-approved-without-being-read
runs: pre_send
reads: [note.sections, note.high_risk_items, item.transcript_span, item.state, ui.note_open_seconds]
trigger: the clinician selects Sign on a note that has unresolved high-risk or inferred items
moves: [admit_uncertainty, offer_choices, ask_one_question, hand_off]
choices: ["Confirm", "Edit", "Remove", "Something else"]
on_miss: ask
metric: seeded-error catch rate
counter_metric: flags per note
status: proposed
```

## 8. Related patterns
- [Approval queue overflow](../../../../../cross-cutting/operations/goals/human-oversight-reliability/failures/approval-queue-overflow.md) (see its "Approval fatigue" example): many separate approval requests pile up and the approver clicks through them. This page is one large document drafted from a conversation, so the problem is that errors hide inside finished prose, and omissions leave nothing to click on.
- [Empty allergy query documented as confirmed no known allergies](../../../../../by-use-case/healthcare/goals/clinical-documentation/failures/empty-allergy-query-result-documented-as-confirmed-no-known-allergies.md): the draft itself contains a wrong negative. This page covers why the clinician does not catch it at sign-off.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): asking too often. It is the opposite risk to this fix (rule 6 and the over-correct paragraph).
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the general case of a sure-sounding error. Here the check is the heard words beside each item.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): treating high and low stakes the same. Rule 1 applies that idea inside one note.

## 9. Common questions
### Why do doctors sign AI scribe notes without reading them?
One commentary argues it is predictable: when the machine writes a good first draft, each note gets less scrutiny. The UC Davis pilot found 14.9% of notes unedited, which shows editing was rare but not that notes went unread ([section 4](#4-why-it-matters)).

### How often do AI scribes get things wrong?
It depends on who counts and how. The UC Davis pilot found serious-risk errors in 5.3% of 356 rated notes. The preprint audit found 31.3% of notes with at least one verified failure. The preprint's own result is that the answer changes with the review instruction (9.3% to 79.0% of candidates verified), so do not compare the two numbers directly.

### How do I make clinicians actually review AI-generated notes?
Do not add a longer checklist. Flag the few high-risk items, show the spoken words next to each, and require a separate Confirm, Edit, or Remove ([section 5](#5-the-fix)). I found no controlled study that tests this design, so run your own drills first.

### Can I test whether clinicians catch errors?
Yes, with seeded errors in synthetic notes, never real charts. Include omissions as well as wrong entries, since the UC Davis pilot found omissions most often ([section 6](#6-how-to-test-it-short-version)).

### Will a better scribe model remove the need to review?
Not on this page's evidence. The UC Davis authors say review remains imperative even with 94.7% of rated notes free of significant errors. Our judgment is that review design is still needed.

---
## Technical section

### T1. Solution architecture
```
visit audio -> transcript -> draft note
draft note + transcript -> risk tagger (categories, inferred sentences) -> item list with transcript spans
transcript + draft -> omission finder -> "heard but not in the note" list
review UI: items, gaps, omissions -> per-item actions -> sign gate -> chart
event log: note_opened, item_action, sign_attempt, note_signed
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Sign disabled while a high-risk item is unresolved | Review UI and the filing API | Tests 4, 5; metric row 3 |
| No guessed values for unstated fields | Draft generator and a post-check | Test 2 |
| No seeded error in a real chart | Drill tooling uses a synthetic-only environment | Test 7; access audit |

### T3. Evals
- **Dataset:** a set of synthetic encounters with planted errors, including omissions, written with clinical staff. Size is for your team to set with a statistician.
- **Judge rubric:** a clinician checks whether each planted error was found or fixed, and whether any false flag led to a wrong change.
- **Release gate:** block a release if the catch rate drops below your floor, or if a path lets Sign succeed with an unresolved high-risk item.
- **Grading omissions.** Use clinician graders for omissions and check that any automated grader finds absences before you rely on it. I have no opened source on how well automated graders do this.

### T5. Trade-offs
- A transcript link adds audio storage and retention duties. That is a legal and policy question for your counsel.
- The omission finder adds false suggestions. Keep the list short and track Not relevant clicks.
- Per-item gates add seconds on notes that have flags. Measure sign time before and after.

---
### Deep dive
- **Open question.** I found no study of whether flagged items, transcript links, or a sign gate improve what clinicians catch. The design rests on the audit and pilot evidence in section 4 plus our judgment.
- **Not used.** Vendor descriptions of verification features, a blog post on a Lancet seeded-error simulation, a JMIR viewpoint on the limits of review, and an oncology study of AI error detection were seen only in search summaries and are not relied on.
- **Modality notes.** Voice-only and mobile review: PLANNED. On a small screen, the item list may need to replace the full note.
- **References.** [Taylor et al., 2026](https://escholarship.org/uc/item/9r89g3sp) (opened); [Fox et al., 2026 preprint](https://arxiv.org/abs/2608.31017) (opened); [Bala, 2026](https://www.medicaleconomics.com/view/is-ai-turning-you-from-physician-to-proofreader-) (opened); [Goddard et al., 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751) (opened). Naming follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
