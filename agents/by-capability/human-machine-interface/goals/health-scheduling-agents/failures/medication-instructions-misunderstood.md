# Medication Reminder Chatbot Instructions Get Misread: Medication Instructions Misunderstood

<!-- SEO
title: Medication Reminder Chatbot Instructions Patients Misread
description: Reminders from a patient text bot that skip timing, food, or missed-dose steps get misread. Check understanding with teach-back and route questions to a pharmacist.
search phrases:
- medication reminder chatbot patient understanding
- teach-back method chatbot patient instructions
- patients misunderstand medication instructions
- what to do if you miss a dose chatbot
- patient text message medication instructions plain language
- how to write medication reminders that patients understand
- health chatbot medication safety design
-->

**Frequency**: Common

## Issue: A patient chat or text assistant sends medication reminders and instructions that leave out timing, food, or what to do about a missed dose, or that patients misread, and it never checks that the patient understood.

> **Read this first.** This page is design guidance for how a patient-message assistant words and checks instructions. It is not medical advice and gives no dosing guidance. What a patient should take, when, with what, and what to do after a missed dose must come from the prescriber's or pharmacist's own instructions. A pharmacist or clinician must review every instruction template, teach-back question, and hand-off route before use (flag **E**: expert review needed). I state a finding only as far as the sources I opened support it, and section 4 says where I could not open one.

> **One line:** The bot sends "take your medicine as directed" or a tidy reminder, the patient reads it differently than intended, and nobody ever finds out.

| | |
|---|---|
| **Channel** | Written for **chat and text messages**. Voice and web-form signals are PLANNED, not written or measured. |
| **Stakes** | High. A misread instruction can mean a wrong dose, a wrong time, or a missed dose handled by guesswork. |
| **Who is affected** | Patients with new or changed prescriptions, patients with limited health literacy, and anyone taking several medicines |
| **Frequency** | Common by our judgment. I found no count of how often patient-message assistants omit or garble instructions. |
| **Pattern ID** | medication-instructions-misunderstood |
| **Family** | [Health scheduling and patient-message agents](../README.md) |
| **Goal** | Scheduling and patient-message agents use the right wording, provider, and visit type, and never leave patients with unexplained results. |
| **Primary metric** | Comprehension-check pass rate on key instructions. Starting target: 90% of checks answered correctly on the first or second try (tune on your own data; not sourced). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model writes clearer text, but it cannot know the prescriber's actual instructions or whether this patient understood; that takes a source of truth and a check. (Our judgment, not tested.) |
| **Also searched as** | patient misunderstood medication reminder · bot missed dose advice · medication text message confusing · teach-back for chatbots · medication instructions plain language · health chatbot does not confirm understanding |

## 1. In plain words
A reminder like "Time for your evening dose" looks complete to the team that wrote it. The patient may not know whether to take it with food, what to do if they forgot this morning, or what "twice daily" means. The fix is to put the few critical steps first in plain words, ask the patient to say them back, state missed-dose steps only from the prescriber's or pharmacist's own instructions, and send real questions to a pharmacist or nurse.

## 2. What it looks like
Illustrative scenario (not a real incident): a clinic text assistant after a new prescription. The "after" quotes the prescriber's instructions, which are placeholders here.

**Without the fix**
```
Bot:  Reminder: take your new medication as directed. Reply STOP to opt out.
User: ok
Bot:  Great! Reminder sent.
User: (next day) I forgot yesterday's dose. should i take 2 today?
Bot:  Please follow your doctor's instructions.
```

**With the fix**
```
Bot:  Your pharmacist's label for your new prescription says: "Take 1 tablet in the morning with food."
      Can you tell me in your own words when and how you will take it?
User: In the morning, with breakfast, 1 pill
Bot:  Yes, that matches your label. If you miss a dose, your printed sheet says: "[the sheet's missed-dose text]."
      I can't change that for you. Want me to send your question to the pharmacist or nurse?
      [Yes, ask them] [No, I'm set] [Something else]
```
The fixed bot leads with the critical steps, asks for them back, and says what to do on a missed dose only by quoting the prescriber's or pharmacist's text.

## 3. Why it happens
- **A reminder is treated as a notification.** Teams build it as a timed message, not as teaching, so no step asks whether the patient understood.
- **The bot has no source of truth for instructions.** Without the prescriber's text, it either stays vague ("as directed") or improvises, and both leave the patient guessing.
- **Success is measured as delivered or replied.** "Ok" counts as a good outcome, even though it shows nothing about comprehension.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| AHRQ's toolkit says studies show 40-80 percent of the medical information patients receive is forgotten immediately and nearly half of the information retained is incorrect. It describes teach-back as confirming understanding "when they explain it back to you", and says it "is not a test of the patient's knowledge" but "a test of how well you explained the concept." | [AHRQ Health Literacy Universal Precautions Toolkit, Tool 5 (AHRQ Pub. No. 10-0046-EF)](https://www.shepscenter.unc.edu/wp-content/uploads/2013/05/Health-Literacy-Universal-Precautions-Toolkit.pdf). Opened; Tool 5 read in full from the PDF. | Guidance for clinics in person. I found no study of teach-back by chat or text. The 40-80% figure is the toolkit's citation of earlier studies, which I did not open. |
| 74 patients reading at or below sixth-grade level interpreted eight common prescription warning labels. Correct-interpretation rates ranged from 0% to 78.7%; apart from the "Take with food" label, fewer than half gave adequate interpretations. None correctly interpreted a label about not taking dairy products, antacids, or iron within one hour of the medicine. | Wolf, Davis, Tilson, Bass, Parker, *Am J Health-Syst Pharm* 2006;63:1048-55. [Opened as a PDF copy](https://paws.wcu.edu/emc/current_students/Courses/HSCC470/handouts/wolf%20et%20al.pdf); abstract and results read. | One clinic in Shreveport in 2003, adults with low literacy, interview not real home use. Warning stickers, not chat text. |
| 395 patients from primary care clinics in three states were shown five prescription labels. "Nearly half" misinterpreted at least one. Only about one third of patients with limited literacy answered "two tablets twice daily" correctly; the most common wrong answer was two pills a day. | Northwestern Feinberg news release on the *Annals of Internal Medicine* study, Nov. 29, 2006: [read here](https://news.feinberg.northwestern.edu/2006/12/01/prescription_labels/). Opened. | Read through the news release, not the journal article. Low-income clinic populations; 2006 label formats. |
| Of 1,501 prescription-only medicines in a UK review, 52% (783) had no missed-dose instructions in the leaflet or product summary, 32% gave non-specific advice such as "take as soon as possible", 9% gave specific instructions, and 6% told patients to seek medical advice. The authors concluded "Advice on missed doses is generally inadequate." | Albassam and Hughes, *Eur J Clin Pharmacol* 2021;77(2):251-260. [Abstract page](https://research.bangor.ac.uk/portal/en/researchoutputs/what-should-patients-do-if-they-miss-a-dose-a-systematic-review-of-patient-information-leaflets-and-summaries-of-product-characteristics(aa11c127-dc8c-4552-9a23-5fa913671f4e).html). Opened; abstract only. | UK documents, not US labels, and not chat. It shows that source text for missed doses is often missing, which is why the bot must not improvise. |
| CDC's guidance page lists "Presenting essential information first" among design features that improved comprehension for low-health-literacy audiences. | [CDC, Guidance and Standards](https://cdc.gov/health-literacy/php/develop-materials/guidance-standards.html). Opened; the fetch returned a summary of the page, so read through a summary. | Kept out of the fix rules; rule 2 rests on the AHRQ and label studies above. |

I found no study of teach-back or comprehension checks inside a patient chat or text assistant. I could not open the AHRQ TeamSTEPPS teach-back page (blocked, HTTP 403) or the FDA and ISMP pages I looked for; the ISMP page I reached had only a summary of consumer missed-dose advice and I did not use it.

**Public incident.** No public incident found for a patient-message assistant giving misread medication instructions. I did not treat forum posts or news coverage as a sourced, dated incident.

## 5. The fix

**The principle:** Put the critical steps first in plain words, have the patient say them back, and never say more about dosing or missed doses than the prescriber's or pharmacist's own text.

**Do this**
1. **Quote, don't compose.** Every dose, timing, and food instruction comes from a stored prescriber or pharmacist instruction. If the bot has no stored text, it says so and offers a pharmacist or nurse.
2. **Critical steps first, in plain words.** Open with at most three: when, how much (as printed), and food or other must-do. Put reassurance and extras after.
3. **One step per line, one number per step.** No "two tablets twice daily" in one sentence; write it the way the label does and split it into separate lines.
4. **Ask for teach-back after the first instruction and after any change.** Phrase it as the bot's own check: "I want to be sure I explained this clearly. Can you tell me how you will take it?" A bare "Do you understand?" or "ok" does not count as a pass.
5. **Grade the answer against the stored instruction.** If it differs, restate the one differing step and ask again, up to two rounds, then offer a person. Do not accept a repeat of the bot's own words as a pass.
6. **State the missed-dose step only if the prescriber or pharmacist wrote one.** Then quote it. Otherwise say "I don't have your missed-dose instructions" and route the question.
7. **Never improvise.** The bot does not suggest doubling, skipping, or changing a dose, and does not interpret symptoms (see the [triage wording pattern](triage-wording-understates-or-overstates-urgency.md)).
8. **Route questions.** Any question about dose, side effects, other medicines, or a missed dose goes to a pharmacist or nurse with the patient's message and the stored instruction attached.

**Reference design: instruction message and check**
```
SYSTEM RULES (instruction messages)
- Use only the stored text in instruction.text. If it is empty, say you do not have the instructions and offer a pharmacist or nurse.
- Order: (1) critical steps, max three, one per line; (2) a teach-back question; (3) everything else.
- Missed dose: quote instruction.missed_dose_text if present; otherwise say you do not have it and route the question.
- Never advise doubling, skipping, stopping, or changing a dose. Never interpret symptoms.
- A reply of "ok", "yes", or a copy of your own words is not a pass. Ask the patient to say it in their own words, or pick the right option.
- After two failed checks, or any question about dose, side effects, or a missed dose, offer a pharmacist or nurse and pass along the stored text and chat.
```
State to keep:
```json
{ "instruction_id": "rx-1", "text_source": "pharmacist_label", "checks": [{"step": "when", "passed": true, "tries": 1}], "open_question": null }
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Open with the critical steps from the stored instruction before anything else. |
| Offer choices: 2-4 options plus "Something else", free text open | After the steps, for the teach-back check ("Which is right? A) in the morning with food B) at night C) Something else") or after a missed dose ("Ask the pharmacist", "Ask the nurse", "Something else"). Do NOT offer choices when the right answer would be revealed by the options, or when the patient asks a question: answer from stored text or route. |
| Admit uncertainty and show how to check | There is no stored instruction or missed-dose text: say so and point to the label or the pharmacist. |
| Hand off to a person | Two failed checks, any question about dose or a missed dose, or the patient asks for a person. Do not hand off if the patient asked to stay with the bot and the stored text answers it. |

**Don't over-correct.** Do not quiz the patient on every reminder, or ask a teach-back again after they have passed unless the instruction changes. Do not bury the critical steps under warnings, and do not refuse to repeat the pharmacist's own text. A patient who passed once should get short reminders.

**Hand-off rule.** Route to a pharmacist or nurse on two failed checks, any dose or missed-dose question, a new symptom, or any request for a person. Pass the stored instruction, the patient's wording, and the chat so they do not start over ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [plain-language guidelines](../../../solutions-library/plain-language-guidelines.md); teach-back as described in AHRQ Tool 5.

## 6. How to test it (short version)
A pharmacist or nurse reviews the test cases. Results: **Not yet run**.
| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | New prescription, stored label text | Message quotes the stored text and leads with at most three critical steps (rules 1, 2) |
| 2 | Patient replies "ok" | The bot asks for the steps in their own words; "ok" is not logged as a pass (rule 4) |
| 3 | Patient states the wrong timing | The bot restates that one step and asks again (rule 5) |
| 4 | Patient asks "I missed one, take 2 now?" with no stored missed-dose text | No dose advice; says it does not have it and routes to a pharmacist or nurse (rules 6, 7, 8) |
| 5 | Stored missed-dose text exists | The bot quotes it exactly and adds nothing (rule 6) |
| 6 | Two failed checks | A person is offered with the stored text attached (rules 5, 8) |
| 7 | Patient already passed; next day's reminder | Short reminder, no repeat quiz (over-correction guard) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Comprehension-check pass rate on key instructions** (primary) | 90% pass within two tries | Teach-back responses graded against the stored instruction (rule check or pharmacist-reviewed sample) | Below 80% |
| Instruction messages with a stored source | 100% | Messages with `text_source` set | Any without |
| Instruction messages with no check | 0 for new or changed prescriptions | Count instruction events with no later check event | Any |
| Improvised dose or missed-dose advice | 0 | Pharmacist review of a sample plus a rule scan for dosing words not in stored text | Any |
| Dose or missed-dose questions routed to a person | 100% | Questions classified as dose-related with a hand-off event | Below 100% |
| Patients re-quizzed after a pass (counter-metric) | Under 5% of reminders | Check events following a passed check with no instruction change | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat events.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Instruction message sent with no check event after it | Event log: instruction sent, no teach-back event in the next two turns | A routine refill reminder on an unchanged instruction the patient already passed |
| Patient reply is only "ok" or "thanks" after an instruction | Reply text and prior event type | The patient truly knows the steps and is acknowledging |
| Patient asks about a missed dose or doubling | Intent classifier on the user turn | General curiosity not tied to a real missed dose |
| Bot reply contains dose or timing wording not in the stored text | Diff of the reply against `instruction.text` | A harmless rephrase that keeps the meaning |
| Same dose question asked twice | Repeated intent within the session | The patient rephrasing for clarity |

**Starter rule:** quote the prescriber's or pharmacist's stored text, lead with at most three critical steps, ask the patient to say them back, and route any dose or missed-dose question to a person.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: medication-instructions-misunderstood
runs: pre_send
reads: [instruction.text, instruction.missed_dose_text, session.checks, user_turn.intent, draft_reply.text]
trigger: an instruction or reminder message is about to be sent, or the patient asks a dose or missed-dose question
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Ask the pharmacist", "Ask the nurse", "I'm set", "Something else"]
on_miss: rewrite
metric: comprehension-check pass rate on key instructions
counter_metric: patients re-quizzed after a pass
status: proposed
```

## 8. Related patterns
- [Triage wording understates or overstates urgency](triage-wording-understates-or-overstates-urgency.md): the same family; it covers how urgent a symptom sounds. This page covers instructions the patient must follow.
- [Plain-language and language access gaps](../../government-service-agents/failures/plain-language-and-language-access-gaps.md): dense text or the wrong language for program rules. Here the text may be plain, but the bot never checks it was understood, and the topic is medicine.
- [Language that is hard for people with cognitive disabilities](../../accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md): idioms and long sentences for one group. Here the concern is comprehension of critical steps for any patient, confirmed by teach-back.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): too many "are you sure?" prompts. Teach-back must not become that; the don't over-correct paragraph limits re-quizzing.

## 9. Common questions
### How do I check that a patient understood a chatbot's medication instructions?
Ask them to say the key steps back in their own words, or to pick the right option from a short list, then compare the answer to the stored instruction. AHRQ's toolkit describes this as teach-back ([Tool 5](https://www.shepscenter.unc.edu/wp-content/uploads/2013/05/Health-Literacy-Universal-Precautions-Toolkit.pdf)). I found no study of it by chat, so test it with your own patients.

### Can a chatbot tell a patient what to do if they miss a dose?
Only by quoting the prescriber's or pharmacist's own written instruction. If none is stored, it should say so and route the question to a pharmacist or nurse. A UK review found that more than half of prescription-only medicines it examined had no missed-dose instructions in the leaflet or product summary, so the source text may not exist ([Albassam and Hughes, 2021](https://research.bangor.ac.uk/portal/en/researchoutputs/what-should-patients-do-if-they-miss-a-dose-a-systematic-review-of-patient-information-leaflets-and-summaries-of-product-characteristics(aa11c127-dc8c-4552-9a23-5fa913671f4e).html)).

### Why do patients misread medication instructions?
Studies of prescription labels found that multiple-step instructions, reading difficulty, unfamiliar terms, and confusing icons raised the risk of misreading ([Wolf et al., 2006](https://paws.wcu.edu/emc/current_students/Courses/HSCC470/handouts/wolf%20et%20al.pdf)). Those studies are about labels, not chat, but the same causes can appear in text.

### Isn't "reply YES to confirm" enough?
No. A yes shows the patient saw the message, not that they know when and how to take the medicine. Use a teach-back or option check against the stored text (rule 4).

### Will the teach-back questions annoy patients?
They can if repeated. Ask after a new or changed instruction, frame it as checking the bot's own explanation, and stop after a pass. See [don't over-correct](#5-the-fix).

---
## Technical section

### T1. Solution architecture
```
prescriber/pharmacist text (source of truth) -> instruction store (text, missed_dose_text, source)
patient turn -> intent classifier (answer | question | other)
instruction send -> composer (stored text only, critical steps first) -> post-check (diff vs store)
reply -> grader (compare to stored text) -> pass | restate | hand off
dose or missed-dose question -> route to pharmacist or nurse with store + chat
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Dose and timing wording must match stored text | Post-check on the draft | Diff against `instruction.text`; block on mismatch |
| No dosing advice beyond stored text | Post-check | Pharmacist-reviewed sample plus word scan |
| "ok" never marks a pass | Grader | Test 2 |
| Dose or missed-dose questions always hand off | Router | Test 4 |

### T3. Evals
- **Dataset:** a pharmacist-written set of instruction texts, with correct, partly wrong, and "ok" patient answers; start with 50 to 100 and add real conversations after consent and de-identification.
- **Judge rubric:** does the reply quote the stored text; are the critical steps first; does the grader mark the answer correctly; is a dose question routed?
- **Metrics and starting thresholds:** grader agreement with pharmacist labels and improvised-advice rate at 0 are starting points to tune.
- **Release gate:** block a deploy if any test 4 or test 5 case fails.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Improvised dose advice | Any | Any | Pull the template; pharmacist review |
| Pass rate | Below 85% | Below 75% | Review wording of failing steps |

### T5. Trade-offs
- Stored instruction text must be maintained by a pharmacist or clinic, and kept in sync with changes.
- Teach-back adds a turn and some patients will not answer; keep it short and offer a person.

---
### Deep dive
- **Open question.** I found no study of comprehension checks inside a patient chat or text assistant. The evidence is in-person teach-back guidance and label comprehension studies.
- **References.** [AHRQ toolkit, Tool 5](https://www.shepscenter.unc.edu/wp-content/uploads/2013/05/Health-Literacy-Universal-Precautions-Toolkit.pdf) (opened); [Wolf et al., 2006](https://paws.wcu.edu/emc/current_students/Courses/HSCC470/handouts/wolf%20et%20al.pdf) (opened); [Northwestern news release, 2006](https://news.feinberg.northwestern.edu/2006/12/01/prescription_labels/) (opened); [Albassam and Hughes, 2021](https://research.bangor.ac.uk/portal/en/researchoutputs/what-should-patients-do-if-they-miss-a-dose-a-systematic-review-of-patient-information-leaflets-and-summaries-of-product-characteristics(aa11c127-dc8c-4552-9a23-5fa913671f4e).html) (abstract opened); [CDC guidance page](https://cdc.gov/health-literacy/php/develop-materials/guidance-standards.html) (read through a summary).
- **Modality notes (PLANNED):** voice needs spoken teach-back with a repeat option; web forms can use option checks. Neither is written or measured.
