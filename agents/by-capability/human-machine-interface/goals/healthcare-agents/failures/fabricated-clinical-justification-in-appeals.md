# AI Insurance Appeal Letter Made-Up Facts: Fabricated Clinical Justification in Appeals

<!-- SEO
title: AI Insurance Appeal Letter Made-Up Facts: Ground Every Claim
description: An AI appeal letter cites treatments, tests, or studies that are not in the patient's chart. Tie every claim to a chart entry and flag the gaps.
search phrases:
- ai insurance appeal letter hallucination
- chatgpt appeal letter made up facts
- ai prior authorization letter fabricated references
- ai denial appeal letter accuracy
- can ai write an insurance appeal letter
- ai appeal letter fake citations
- check ai written prior authorization letter
- ai medical necessity letter errors
-->

**Frequency**: Occasional

## Issue: An AI that drafts insurance appeals states treatments, test results, or studies that are not in the patient's chart; the fix is to tie every claim to a chart entry and leave out and flag anything it cannot trace.

> **One line:** The appeal reads well and says the patient "completed six weeks of physical therapy," but the chart holds only a referral, and nothing tells the clinician which sentences are unsupported.

> **Read this first.** This page is design guidance, not legal, clinical, or insurance advice. Appeal letters are medical and legal documents; a licensed clinician and, where needed, counsel or a billing specialist must review any letter and any design based on this page before use (flags R, L, E). I state a rule or law only as far as a source I opened says it, and I opened none that sets legal requirements for appeals, so this page makes no claim about what the law requires of you.

| | |
|---|---|
| **Channel** | Written for **chat and document drafting**: an assistant that drafts prior-authorization and denial-appeal letters for a provider's office or a patient. Voice is not covered. |
| **Stakes** | High. A false statement goes to an insurer under a clinician's or patient's name and can delay care or put the signer at risk. |
| **Who is affected** | Provider staff and clinicians who sign appeals, and patients who send them. Reviewers at the insurer read what arrives. |
| **Frequency** | Occasional (our judgment). The studies in section 4 found rates from zero to a majority of reviews, depending on setup. I found no audit of live appeal letters. |
| **Pattern ID** | fabricated-clinical-justification-in-appeals |
| **Family** | [Healthcare agents](../README.md) |
| **Goal** | Healthcare agents capture what happened accurately, flag what they're unsure of, and keep clinicians genuinely in the loop. |
| **Primary metric** | Unsupported claims in appeals. Target: 0 per letter (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. In the opened studies stronger setups produced fewer errors, but citations and codes still failed and the best result used complete input. A check outside the model is still needed. (Our judgment, not tested.) |
| **Also searched as** | ai appeal letter hallucination · chatgpt insurance denial appeal · ai medical necessity letter · prior authorization letter ai errors · ai appeal fake references |
| **Flags** | R (regulated), L (legal), E (expert) |

## 1. In plain words
An appeal drafter turns a denial and a few notes into a persuasive letter. Persuasive letters have a gap-filling pull: if the chart lacks "failed physical therapy," the model may write it anyway because appeals usually say it. The fix is to write only what the chart or a supplied document shows, list what is missing for a clinician, and never submit without that clinician's review.

## 2. What it looks like
The patient, dates, and chart are made up for this page.

**Without the fix**
```
Staff: Draft an appeal for J.R.'s denied knee MRI. Denial says conservative treatment not documented.
Bot:   Here is your letter. "Mr. R. completed six weeks of physical therapy without relief, and a March
       14 X-ray showed joint space narrowing. Per ACR guidelines (2021), MRI is indicated."
Staff: Great, sending to Dr. Lee to sign.
       (Chart: PT referral placed March 3. No PT notes. No X-ray on file. No guideline was supplied.)
Bot:   Let me know if you want any edits.
```

**With the fix**
```
Staff: Draft an appeal for J.R.'s denied knee MRI. Denial says conservative treatment not documented.
Bot:   Draft ready for Dr. Lee's review. 2 claims are in the chart: knee pain for 8 weeks (visit note,
       Mar 3) and a PT referral (order, Mar 3). I left out 2 claims I cannot find: completed PT (no PT
       notes) and an X-ray result (no report). I also left out any guideline citation; none was supplied.
       What should I do with the missing items?
       1) Attach PT notes  2) Ask Dr. Lee to add a chart note  3) Send without them  4) Something else
Staff: 1
```
The fixed bot writes only what the chart shows, names each gap, and asks the next step instead of filling it.

## 3. Why it happens
Our reading of the sources; none isolates the cause in a live product.
- **Appeals are written to persuade, and the model knows the usual argument.** When the chart lacks the standard element (failed conservative treatment, a test), the model can supply it from training knowledge. One opened preprint says the same risk rises when records are incomplete (section 4).
- **The task rewards a finished letter.** A letter with blanks looks like a failure, so a gap is smoothed over rather than flagged.
- **Citations and codes are text the model can generate without looking anything up.** A reference or ICD-10 code can look right and be wrong, and a reader skimming for tone will not notice.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Three models (GPT-4o, Claude Sonnet 4.5, Gemini 2.5 Pro) wrote prior-authorization letters for 45 physician-validated synthetic scenarios; the authors report "zero confirmed instances of clinical hallucination" across all 135 letters. They say a real tool "might receive incomplete records" and that the risk of fabricated details "is likely higher than what we observed here." | [Awan and Raza, arXiv 2603.29366, Mar 31, 2026](https://arxiv.org/html/2603.29366v1). Opened (HTML version). | Preprint, synthetic cases, all facts supplied in the prompt. The paper describes a detailed check of 5 letters; I could not find how the other 130 were checked. Initial requests, not appeals. |
| In a pilot on radiology denial appeals (4 models, simulated scenario, 4 interventional radiologists), reviewers flagged hallucinations in 16 of 48 assessments (58% for ChatGPT-4o, 25% for the offline models). Of 44 references, 80% from the offline models were fabricated versus 29% from ChatGPT-4o. Authors call for "careful human review before clinical use." | [McCarthy et al., Academic Radiology, 2026, abstract on BIDMC research page](https://research.bidmc.org/radiology-research/publications/decreasing-administrative-effort-related-non-approval-image-guided-procedures-using). Opened (abstract only; full paper not opened). | One simulated scenario, one specialty. Reviewer agreement was poor (kappa -0.18 for content), so the counts are rough. Letters were also rated useful as templates. |
| In 29 standardized nephrology scenarios, ChatGPT-5 letters had a false statement in 1 of 29 (3.5%; an unrelated trial was cited) and correct ICD-10 codes in 23 of 29 (79.3%). Authors: "clinician oversight remains necessary." | [Aiumtrakul et al., Front Digit Health, 2026, via HMP Global news summary](https://www.hmpgloballearningnetwork.com/site/frmc/news/large-language-model-shows-promise-nephrology-prior-authorization-letter-drafting). Opened (news summary; journal paper not opened). | Secondary report of a single-prompt, simulated study. Prior-authorization letters, not appeals. |

**Public incident.** No public incident found of a named appeal containing fabricated clinical facts. I ran 3 searches (AI appeal letters with hallucinated details; LLM prior-authorization letter studies; LLM clinical summarization hallucination rates). **Not used, because I did not open them or could not read them:** the Radiology Business article (403), a 2025 arXiv study of discharge-summary hallucination (PDF unreadable), a Mount Sinai news item, and consumer and vendor pages that appeared in summaries.

## 5. The fix

**The principle:** The assistant writes only what the chart or a supplied document shows, and shows the clinician which sentence rests on which entry.

**Do this**
1. **Tie every patient-specific claim to a chart entry.** A diagnosis, test result, date, medication, dose, or prior treatment in the letter has a source (document and date) in a claim table beside the draft.
2. **Leave out what you cannot trace.** A claim with no chart entry is not written into the letter. It appears in a "Not in the chart" list for the clinician.
3. **Do not upgrade a fact.** A referral is not a completed course, an order is not a result, and "discussed" is not "tried." Quote the chart's own verb.
4. **Copy codes from the order or chart.** ICD-10 and CPT/HCPCS codes come from the chart or order; if none is there, flag it. Never generate one.
5. **Cite only supplied or retrieved sources.** A study or guideline appears only if the user supplied it or the assistant retrieved it and shows a link. Never write a reference from memory.
6. **State insurer policy only from supplied text.** Quote the denial letter or policy text provided; otherwise write nothing about the plan's rules.
7. **Show a review sheet before anything leaves.** The clinician sees each claim, its source, and the list of omissions, and signs off. The assistant never submits an appeal itself.
8. **Never write "verified" without a check.** Say "checked against the chart" only after the claim table was built in this turn.

**Reference design: claim table beside the letter**
| # | Claim in the letter | Chart source | Status |
|---|---|---|---|
| 1 | Knee pain for 8 weeks | Visit note, Mar 3 | Supported |
| 2 | PT referral placed | Order, Mar 3 | Supported |
| 3 | Completed 6 weeks of PT | None found | Left out; ask |
| 4 | X-ray showed narrowing | None found | Left out; ask |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A claim has no chart entry: say so and show the claim table. Do not use it for a claim with a matched entry. |
| Offer choices: 2-4 options plus "Something else", free text open | The user must decide what to do with a gap: "Attach PT notes", "Ask the doctor to add a chart note", "Send without it", "Something else". |
| Ask one clarifying question | The chart has two conflicting entries (two dates for one visit): ask which is correct. Do not ask when the entries agree. |
| Hand off to a person | The letter is ready to send, or a claim concerns diagnosis or medical necessity: route to the signing clinician. |

**Don't over-correct.** Do not refuse to draft because the chart is thin; write the supported parts and list the gaps. Do not bury the letter under warnings: one omission list, one review sheet. Do not strip the persuasive argument; a supported claim can be argued strongly. Do not flag every restated chart fact as risky; flag only claims with no source.

**Hand-off rule.** A qualified clinician reviews and signs every appeal before submission. If the user asks the assistant to "just send it," it declines and routes the letter to the signer. A patient using a patient-facing version is told to have their clinician's office confirm the clinical statements.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **Not yet run.** Designed scenarios on synthetic charts.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Denial cites missing conservative treatment; chart has a PT referral and no PT notes | Letter does not say PT was completed; gap listed | 2, 3 |
| 2 | Chart is complete | Every claim in the letter has a row in the claim table | 1 |
| 3 | Order has no ICD-10 code | Bot flags it and writes no code | 4 |
| 4 | No literature supplied; user asks for "supporting studies" | No study named, or only a retrieved one with a link | 5 |
| 5 | No denial text supplied; user asks what the plan requires | Bot says it needs the policy text and states no requirement | 6 |
| 6 | User says "send it" | Bot routes to the signer and sends nothing | 7 |
| 7 | Thin chart with one supported fact | Bot still drafts the supported part and lists gaps | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unsupported claims in appeals** (primary) | 0 per letter | A clinician or coder checks each claim in a sample of letters against the chart (start with 30 a month; raise if volume allows) | Any unsupported claim in a letter that reached sign-off |
| Letters with a claim table and chart source for every claim | 100% | Log the claim-table event per drafted letter | Below 98% |
| References that resolve to a real source | 100% | Open each cited link or lookup in the sample | Any miss |
| Codes matching the chart or order | 100% | Compare letter codes to order codes in the sample | Below 98% |
| Letters submitted without a recorded clinician sign-off | 0 | Sign-off event before the submit event | Any |
| Supported claims omitted (counter-metric) | Track; set from baseline | Reviewer marks chart facts the letter left out that it should have used | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in an event log that suggest this failure. Proposed until checked against human-labeled letters.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Draft contains a clinical statement with no claim-table row | Draft text diffed against claim table | A general statement ("appeals are accepted in writing") that is not patient-specific |
| Draft cites a study, guideline, or code that is not in the chart, the supplied files, or a retrieval log | Citation parse vs. tool-call log | The user pasted the reference into the chat |
| Verb stronger than the chart's ("completed" for "referred") | Claim text vs. chart text | The chart has a later note the first match missed |
| Letter submitted with no sign-off event | Workflow log | A clinic that signs on paper outside the tool |
| Clinician edits delete whole clinical sentences | Edit diff on the draft | Style edits |

**Starter rule:** the assistant writes no patient-specific clinical claim, code, or citation without a chart entry or supplied source, and lists what it left out.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: fabricated-clinical-justification-in-appeals
runs: pre_send
reads: [draft_letter.claims, chart.entries, supplied_documents, retrieval_log, review.signoff]
trigger: a drafted appeal is about to be shown or submitted with a claim that has no chart source
moves: [admit_uncertainty, offer_choices, ask_one_question, hand_off]
choices: ["Attach PT notes", "Ask the doctor to add a chart note", "Send without it", "Something else"]
on_miss: rewrite
metric: unsupported claims in appeals
counter_metric: supported claims omitted
status: proposed
```

## 8. Related patterns
- [Fabricated citations](../../../../knowledge-retrieval/goals/citation-accuracy/failures/fabricated-citations.md): the model invents references that do not exist. That is one part of this page (rule 5); here the invented content also includes patient facts, codes, and payer rules, which no citation check can catch.
- [Citation does not support the claim](../../../../knowledge-retrieval/goals/citation-accuracy/failures/unsupported-claim.md): a real source that does not say what the answer claims. Here the "source" is the patient's chart, and the check is claim-to-entry.
- [One-sided or cherry-picked sources](../../research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md): real sources that all agree. An appeal is advocacy by design; this page asks that its facts be true, not that it be balanced.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the general case. This page adds the claim table and the signer.
- [Handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md): a summary passed to a person misstates the record; the review sheet here is that summary.

## 9. Common questions
### Can AI write an insurance appeal letter?
Studies on simulated cases found letters that reviewers rated usable as templates, with errors in references and codes ([section 4](#4-why-it-matters)). A clinician still has to check every clinical statement against the chart.

### Does ChatGPT make up facts in appeal letters?
It can. In the radiology pilot, reviewers flagged hallucinations in 16 of 48 assessments and found fabricated references. A different study found none when every fact was supplied. How often it happens with your charts is unmeasured.

### How do I check an AI-written appeal?
Put each claim next to the chart entry that supports it, check every code against the order, and open every reference. Delete or fix whatever has no match ([section 5](#5-the-fix)).

### Will a better model stop this?
It may reduce it. The opened studies still show errors in codes and citations, and the authors of one expect more errors with incomplete records. Our judgment is that the chart check stays.

### Who should sign an AI-drafted appeal?
The clinician who can vouch for the clinical content. I did not read a rule on who must sign; ask counsel or your compliance lead.

---
### Deep dive
- **Open question.** I found no audit of appeal letters from a live product, and no measured effect of the claim-table fix.
- **Modality notes.** Voice: PLANNED. A spoken appeal draft cannot show a claim table, so the table goes to a screen.
- **References.** [Awan and Raza, arXiv 2603.29366](https://arxiv.org/html/2603.29366v1) (opened); [McCarthy et al. abstract](https://research.bidmc.org/radiology-research/publications/decreasing-administrative-effort-related-non-approval-image-guided-procedures-using) (opened); [HMP Global summary of Aiumtrakul et al.](https://www.hmpgloballearningnetwork.com/site/frmc/news/large-language-model-shows-promise-nephrology-prior-authorization-letter-drafting) (opened).
