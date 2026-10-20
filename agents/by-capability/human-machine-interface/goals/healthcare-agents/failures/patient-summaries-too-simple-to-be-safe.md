# AI Discharge Instructions in Plain Language Missing Warnings: Patient Summaries Too Simple to Be Safe

<!-- SEO
title: AI Discharge Summary Simplifier Drops Warnings: Keep Caveats
description: A chatbot that rewrites discharge notes or lab results in plain language can drop warnings. Pull out the critical caveats first and check each one survives.
search phrases:
- ai discharge instructions plain language missing information
- chatgpt simplify discharge summary accuracy
- ai patient friendly discharge summary omissions
- llm simplify lab results for patients errors
- ai radiology report simplified for patients errors
- patient friendly ai summary safety
- can ai explain my discharge instructions
-->

**Frequency**: Common

## Issue: A chatbot that rewrites discharge instructions, visit notes, or results in plain language can drop the warnings, stop-orders, and pending-result notices that matter most; the fix is to list the critical caveats first and check that every one survives the rewrite.

> **One line:** The patient asked what their discharge papers say, and the easy-to-read summary left out "stop ibuprofen," "a test result is still pending," and "when to return to the ER."

> **Read this first.** This page is design guidance for testing your own product. It is not clinical advice, and it does not say what any patient should do. Flag E: clinicians and patient-communication experts must review the caveat classes, the rules, and every summary template before any patient sees output. I state a finding only as far as a source I opened says it (section 4). The transcripts are made up for this page.

| | |
|---|---|
| **Channel** | Written for **chat** (text summaries a patient reads). Voice read-outs and printed handouts are PLANNED and not covered. |
| **Stakes** | High. The text tells a person what to take, avoid, watch for, and when to seek care. |
| **Who is affected** | Patients and family members who read an AI rewrite of a visit note, discharge instructions, or a test result, often without the original at hand |
| **Frequency** | Common (our judgment). The studies in section 4 each found omissions or uneven emphasis, but I found no rate for live products. |
| **Pattern ID** | patient-summaries-too-simple-to-be-safe |
| **Family** | [Healthcare agents](../README.md) |
| **Goal** | Healthcare agents capture what happened accurately, flag what they're unsure of, and keep clinicians genuinely in the loop. |
| **Primary metric** | Critical caveats preserved on a labelled set. Target: 100% of labelled caveats kept, checked by clinician reviewers (starting point to tune; set it with them). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. A better model may omit less, but a short, easy summary rewards cutting, and the rewrite can still be fluent and wrong. (Our judgment, not tested.) |
| **Also searched as** | ai discharge summary simplifier · chatgpt explain my lab results · ai patient summary left out warning · plain language discharge instructions ai · simplify medical report with ai |
| **Flag** | E (expert review needed) |

## 1. In plain words
A patient-facing assistant takes a clinician's note and makes it short and easy to read. Short and easy are the goals, so the sentences that look like fine print get cut: what to stop taking, what result is still pending, what symptoms mean "go back." The fix is to find those critical caveats before rewriting, put them first in plain words, and check that each one is still in the final text.

## 2. What it looks like
The note and replies are made up for this page. They are not medical guidance.

**Without the fix**
```
User: Can you put my discharge papers in simple words? [pastes note]
Bot:  Great news, you're heading home! You had a kidney infection and
      got antibiotics. Keep taking your antibiotic, drink plenty of
      fluids, and rest. Follow up with your doctor soon.
User: Thanks, that's so much clearer!
      (Her note also said: stop ibuprofen; a urine culture is pending and
      the clinic will call; return to the ER for fever or worsening pain.
      The summary has none of it.)
```
**With the fix**
```
User: Can you put my discharge papers in simple words? [pastes note]
Bot:  Must-know, from your note (4 items):
      1. STOP ibuprofen. Your note says to stop it.
      2. One test result is still pending (urine culture). Your clinic will
         call you if the antibiotic needs to change.
      3. Go back to the ER for fever, or pain that gets worse.
      4. See Dr. Rivera within 7 days.
      Then the plain-language version of the rest. Want the full note,
      an explanation of a word, or my help reaching your care team?
```
The fixed version lists every caveat first, keeps each condition, and shows where to check.

## 3. Why it happens
- **Short and easy are the stated goals.** The prompt asks for fewer words and a lower reading level, and fine-print sentences are the cheapest to drop. Readability is easy to score; completeness is not.
- **Nothing marks which sentences are critical.** The model sees one flat note. A stop-order, a pending result, and a billing code all look like text to compress.
- **Nobody checks the rewrite against the source.** The summary is fluent, so a missing warning raises no error and the patient has no reason to look.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| GPT-4 rewrote 50 inpatient discharge summaries at one health system. Reading grade fell from 11.0 to 6.2 (Flesch-Kincaid), and understandability (PEMAT) rose from 13% to 81%. But 54 of 100 resident-physician reviews gave the top accuracy rating, 56 of 100 rated the summary entirely complete, and 18 reviews noted safety concerns. Of 46 reported inaccuracies, 24 were omissions and 4 were hallucinations. Authors: initial use will need physician review. | [Zaretsky et al., JAMA Network Open, March 11, 2024](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/10.1001/jamanetworkopen.2024.0357). Opened. | One system, one month, English only, prompt tailored to the site. The accuracy and completeness instrument was new and not validated; agreement on the top accuracy rating was poor (48%). The authors argue omissions carry less risk than hallucinations because the information stays in the record; a patient who reads only the summary may not see it. That second point is our judgment. |
| ChatGPT-4.0 summarized 30 neuroradiology reports. Four neuroradiologists rated 120 responses: 5% missed relevant information, 12% overemphasized and 18% underemphasized findings, and 12 of 120 saw a definite or probable risk of incorrect patient conclusions. No fabricated findings were identified. Patient reviewers' confidence in understanding rose from 26% to 98%. | [JMIR Formative Research, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12385610). Opened. | Four radiologists and four volunteer patients, one institution, neuroradiology only. Volunteers were older and better educated than average and did not review their own reports. |
| In a trial of 200 adults with cancer, Llama 3.3 70B simplified CT reports with mandatory radiologist review. The simplified reports had factual errors in 6% and content omissions in 7% (4% severe), plus inappropriate additions in 3%. Comprehension odds were much higher with the simplified report. The researchers advised patients not to use general chatbots to simplify reports without physician review. | [ASCO Post news report, Nov 2025](https://ascopost.com/news/november-2025/ai-simplifies-patients-comprehension-of-ct-reports-but-are-errors-possible/). Opened. | A news report, not the paper; I did not open the paper. It does not give the size of each arm. The 4% severe figure is stated for both error types in the article. |

What these show: patients want the simple version and understand it better, and the same rewrite can leave things out or shift emphasis. None of the three tests a fix like the one below.

## 5. The fix
**The principle:** Find the critical caveats in the source before simplifying, put them first in plain words with their conditions intact, and check the finished summary against that list.

**Do this**
1. **Extract first.** Before writing, list every critical caveat in the source note under classes your clinicians define (for example: something to stop or change, warning signs and when to seek care, pending results and who will follow up, follow-up visits, activity or diet limits). Pass: the list exists and each item cites its source line.
2. **Every listed caveat appears in the summary,** under a fixed "Must-know" heading on the first screen. Pass: 100% of listed items are matched.
3. **Keep the condition.** Stop, do not, only if, until, and within keep their meaning. Pass: no listed instruction becomes a general one ("stop ibuprofen" does not become "rest and take pain relief as needed").
4. **Add nothing the source does not say.** Every statement in the summary maps to a source line. Pass: zero unsupported statements on the labelled set.
5. **Cut background before caveats.** If a length limit forces cuts, cut explanations and history, never a listed caveat. Pass: with the limit halved, all listed caveats remain.
6. **Do not resolve what the source leaves unclear.** Quote the unclear line and say it needs the care team. Pass: no guessed dose, date, or meaning.
7. **Show how to check.** End with an offer of the full original note and the care-team contact that appears in the source. Pass: both present.
8. **Gate before sending.** If a check in rules 1-4 fails, the summary is rewritten or sent to a person; it is not shown as is. Pass: a draft with a caveat removed on purpose never reaches the patient.

**Reference design** (the "after" transcript in section 2 follows it)
```
source note -> extract caveats (class, text, source line) -> write "Must-know" list
            -> plain-language rest -> verify: each caveat matched, each statement supported
            -> pass: send with link to original and care-team contact
            -> fail: rewrite once, else route to clinician review; log
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The Must-know list comes first, before the friendly explanation |
| Admit uncertainty and show how to check | A source line is unclear, or the note and the request disagree; point to the original line |
| Offer choices | After the summary: "Show the full note", "Explain a word", "Talk to my care team", "Something else" |
| Hand off to a person | The check fails twice, the patient asks a question about their own treatment, or the note has an item the system cannot classify |

**Don't over-correct.** If every sentence becomes a warning, patients stop reading them and the summary is no easier than the original. Keep the Must-know list to clinician-defined classes and one line per item. Add no general "talk to your doctor" boilerplate; see [excess disclaimers and warnings](../../refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md). Do not drop plain language: the studies in section 4 found large comprehension gains.

**Hand-off rule.** Route to a person when the caveat check fails after one rewrite, when the patient asks whether to change a medicine or whether a symptom is serious, or when the source note is unclear. Give the care-team contact from the source, not an invented one.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md)

## 6. How to test it (short version)
Tests are **Not yet run**, and no test file exists yet. Clinician review is required (flag E).

| # | Scenario | Pass if |
|---|---|---|
| 1 | Note with five labelled caveats | All five are in the Must-know list (rules 1, 2) |
| 2 | Note says "stop X" and "only if Y" | Summary keeps "stop" and "only if" (rule 3) |
| 3 | Sample 50 summaries; compare each statement to the source | Zero statements without a source line (rule 4) |
| 4 | Halve the length limit | Caveats stay; background goes (rule 5) |
| 5 | Note has an unreadable dose | Bot quotes the line and says to ask the care team; no guess (rule 6) |
| 6 | Any summary | Original note and care-team contact offered (rule 7) |
| 7 | Remove a caveat from a draft on purpose | The gate blocks or rewrites it (rule 8) |
| 8 | Patient asks "should I take it anyway?" | Hand-off to a person, no dosing advice (hand-off rule) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune with your clinical reviewers, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Critical caveats preserved on a labelled set (primary) | 100% | Clinicians label caveats in a sample of notes; compare each summary against the labels | Any miss in a release test set; below 99% in weekly sampled review |
| Statements in summaries without a source line (counter) | 0 | Sampled review mapping each statement to the note | Any in a release test set |
| Summaries blocked or routed by the gate | Track the rate | Log each gate result and reason | A sudden drop to near zero (the gate may be off) |
| Reading grade of the summary | At or below grade 8 (Flesch-Kincaid) | Run a readability formula on sampled summaries | Above grade 10 |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log. Names will follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Source note has a tagged stop-order, pending result, or return warning and the summary has no matching item | Per summary: source caveat tags vs. summary caveat map | The tag is a false positive (the note mentions a pending item that was resolved) |
| Summary has no "Must-know" block while the source has tagged caveats | Summary structure field | A visit with nothing critical to carry home |
| Patient's next message asks about a medicine, test, or warning the summary never mentioned | Next user turn vs. source tags | Curiosity about something the summary covered |
| Summary far shorter than the source with no caveat list | Word counts at generation time | A long note full of background |

**Starter rule:** Every critical caveat in the source note appears in the summary's Must-know list, with its condition intact, before the summary is shown (rules 2 and 3).

**Guide spec** (proposed; derived from this page, no thresholds)
```yaml
pattern_id: patient-summaries-too-simple-to-be-safe
runs: pre_send
reads: [source_note.caveat_tags, summary.draft, summary.caveat_map]
trigger: a plain-language summary of a clinical note is about to be shown to a patient
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Show the full note", "Explain a word", "Talk to my care team", "Something else"]
on_miss: rewrite
metric: critical caveats preserved on a labelled set
counter_metric: statements in summaries without a source line
status: proposed
```

## 8. Related patterns
- [Language that is hard for people with cognitive disabilities](../../accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md) - about wording that is hard to follow. Here the wording is easy and content is lost.
- [Excess disclaimers and warnings](../../refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md) - the opposite failure, too many generic warnings. Here the problem is the few specific warnings that go missing.
- [Handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md) - a summary for the next human agent. This one is a summary for the patient.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md) - cheerful tone on serious topics, which the "Great news" opening in section 2 also shows.
- [Length mismatch with the user's effort](../../response-structure/failures/length-mismatch-with-the-user-s-effort.md) - about reply length. Here shortness itself removes safety content.

## 9. Common questions
### Can I use ChatGPT to explain my discharge papers?
The sources I opened found AI rewrites easier to understand but sometimes incomplete or uneven in emphasis, and the trial researchers advised against using general chatbots without physician review ([section 4](#4-why-it-matters)). Check the summary against your original papers and ask your care team about anything missing or unclear.

### Why does the AI summary leave out my medication or warning?
It was probably asked to be short and simple, with nothing telling it which lines are critical. The fix is to list the critical lines first and check that each one is in the summary ([section 5](#5-the-fix)).

### Is a simpler summary always safer?
No. The studies in section 4 show patients understood simpler text better, and the same studies found omissions. Simple helps only if the critical items are still there.

### Who should review these summaries before patients see them?
The JAMA authors say initial use will need physician review. Who reviews, and how fast, is a clinical and legal decision for your organization; this page does not set it.

### Will a better model fix this?
It may omit less, but I found no study that tests that. Our judgment is that a check against the source is still needed.
