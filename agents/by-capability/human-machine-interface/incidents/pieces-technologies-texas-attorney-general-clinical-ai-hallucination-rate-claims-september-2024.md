---
title: "Texas attorney general says Pieces Technologies' hospital AI summary tool advertised a hallucination rate that was likely inaccurate; Pieces denies it and signs a five-year disclosure agreement, September 2024"
date: 2024-09-18
source: "https://www.texasattorneygeneral.gov/news/releases/attorney-general-ken-paxton-reaches-settlement-first-its-kind-healthcare-generative-ai-investigation"
description: "Texas said a vendor's claim of under one severe AI error per 100,000 hospital summaries was likely wrong. The vendor denies it but must define its metrics."
summary: "On September 18, 2024, Texas Attorney General Ken Paxton announced an Assurance of Voluntary Compliance with Pieces Technologies, a Texas company whose generative AI drafts clinical summaries and notes for hospital staff inside the electronic health record. The agreement, filed in Dallas County district court on August 21, 2024, says Pieces advertised a 'critical hallucination rate' and 'severe hallucination rate' of '<.001%' and '<1 per 100,000.' The attorney general said these metrics were likely inaccurate and may have deceived at least four major Texas hospitals. Pieces denied wrongdoing, said it had accurately represented its hallucination rate, and said the attorney general's press release misrepresented the agreement. There was no money penalty; for five years Pieces must define and explain any accuracy metric it advertises and tell customers about known limits and risky uses. Status: Needs review."
categories:
  - Health care
  - Accuracy
  - Trust
patterns:
  - notes-approved-without-being-read
  - confident-wrong-answer-with-no-way-to-check
  - word-error-rate-only-evaluation
---

**This page is a dated teardown of the 2024 Texas attorney general agreement with Pieces Technologies over the accuracy claims for its hospital AI summary tool, for teams that build, buy or deploy a generative AI assistant whose text clinicians read while treating patients.** The product was Pieces' generative AI, which, per the agreement, "summarizes, charts, and drafts clinical notes" for doctors and nurses in the electronic health record. The users were hospital staff at, per the attorney general, at least four major Texas hospitals. The moment that matters is the sales pitch, not a single bad reply: a vendor told hospitals its AI almost never made a serious error, and the state said that number was likely wrong. No opened source shows a specific wrong summary, a patient harmed, or the data behind the advertised rate. The date above is the day of the attorney general's announcement; the agreement was filed on August 21, 2024.

**Status: Needs review.** Four sources were downloaded on 2026-10-28 and read as plain text: the Texas Attorney General's press release (September 18, 2024), the filed Petition and Assurance of Voluntary Compliance (State of Texas and Pieces Technologies, Dallas County cause DC-24-13476, filed August 21, 2024; PDF converted to text), Fierce Healthcare (Dave Muoio, September 19, 2024) and Healthcare Dive (Rebecca Pifer Parduhn, September 23, 2024). Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. Pieces' own press release was not opened; its words appear here only as Fierce Healthcare and Healthcare Dive quote them.

> **Read this first.** This is a summary of public reporting and a public court filing, not a finding of fact, not legal advice and not clinical advice. The agreement is not an admission: Pieces "expressly denies" any violation, and no court or agency found that its rate was false. Nothing here says a Pieces summary was wrong or that any patient was harmed; no opened source reports either. We name only public officials and company leaders named in the opened sources.

**Channel note.** This is a text incident: generated summaries and draft notes shown to clinicians inside the health record, not a back-and-forth chat. This phase of the knowledge base is chat-first, and the signals and checks below are written for generated text. Voice and web signals, such as an ambient scribe that drafts notes from a recorded visit, or a vendor's web page that publishes accuracy figures, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The product.** The agreement quotes Pieces' website: "Pieces summarizes, charts, and drafts clinical notes for your doctors and nurses in the [Electronic Health Record] – so they don't have to." Healthcare Dive says Pieces offers tools that "generate summaries of patient care, draft progress notes within electronic health records and track barriers to discharge."
- **The hospitals.** The attorney general: "At least four major Texas hospitals have been providing their patients' healthcare data in real time to Pieces so that its generative AI product can 'summarize' patients' condition and treatment for hospital staff." No opened source names the hospitals.
- **The advertised numbers.** Per the agreement, Pieces marketed its products "by claiming that they have a 'critical hallucination rate' and 'severe hallucination rate' of '<.001%' and '<1 per 100,000.'" The agreement calls hallucination "a term commonly used to describe the phenomena of generative AI products creating an output that is incorrect or misleading."
- **The state's view.** The attorney general's investigation "found that these metrics were likely inaccurate and may have deceived hospitals about the accuracy and safety of the company's products." The agreement itself states this as an allegation: the representations "may have violated the DTPA," the Texas Deceptive Trade Practices-Consumer Protection Act.
- **August 21, 2024: filed.** The petition and agreement were filed in Dallas County district court. The Pieces CEO's signature is dated August 5, 2024.
- **September 18, 2024: announced.** Paxton called it a "first-of-its-kind settlement." Healthcare Dive and Fierce Healthcare report it is not a financial settlement and carries no money penalty.
- **What Pieces must do, for five years.** If it advertises any accuracy metric, it must "clearly and conspicuously disclose" what the metric means and how it was calculated, or have an independent auditor back its claims. It must give customers documentation of known limits, "including risks to patients and healthcare providers," and of known misuses that "increase the risk of inaccurate outputs." It must not misrepresent accuracy, testing or monitoring methods. Pieces may ask to end the agreement after one year.
- **How Pieces says it measures.** A Pieces spokesperson told Healthcare Dive that its system picks random summaries for review, an "adversarial AI" flags any that may hold a severe hallucination using evidence from the medical record, and a physician reviews, assesses and corrects the flagged ones. This is Healthcare Dive's paraphrase, not the agreement's text.

## What the company and the state said

- **The attorney general.** "AI companies offering products used in high-risk settings owe it to the public and to their clients to be transparent about their risks, limitations, and appropriate use." And: "Hospitals and other healthcare entities must consider whether AI products are appropriate and train their employees accordingly."
- **In the agreement.** Pieces "contends that it has not engaged in conduct that violates Texas law, including the DTPA, and that it has accurately set forth and represented its hallucination rate."
- **In Pieces' statement, per Fierce Healthcare.** The press release "misrepresents" and is "wholly inconsistent with" the agreement. Pieces also said: "Pieces strongly supports the need for additional oversight and regulation of clinical generative AI."
- **Per Healthcare Dive.** Pieces said there is no industrywide standard for classifying the risk of hallucination in AI clinical summaries, and that the order does not mention the safety of its products. Healthcare Dive says the attorney general's office did not respond to its question on how it ran the investigation.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Was the rate wrong | Attorney general: "likely inaccurate." Pieces, in the agreement: it "accurately set forth and represented its hallucination rate." No opened source shows the data, the state's analysis, or an independent test. |
| Which number is which | The agreement pairs the two names with the two figures without saying which goes with which. Fierce Healthcare: critical "less than 0.001%," severe "less than 1 per 100,000." The press release ties "<1 per 100,000" to the severe rate. As arithmetic, 0.001% and 1 per 100,000 are the same number. |
| Safety | The press release speaks of "accuracy and safety" and the public interest. Pieces, per Healthcare Dive, says the order does not mention the safety of its products. The agreement's state allegations concern accuracy claims. |
| What a "hallucination" counted as | The agreement gives a general meaning. No opened source gives Pieces' definitions of "critical" or "severe," or the count of summaries behind the rate. |
| Where Pieces is based | The press release says Dallas-based; the agreement lists an Irving, Texas address. |

## Where in the workflow it broke

Based on the sources above, and only as far as they go. No step below is shown to have caused a wrong summary.

1. **One headline number.** A vendor sold a clinical text tool with a single tiny error rate. Per the agreement, the definition and method were not required to be shown until this order.
2. **Undefined severity.** "Critical" and "severe" are the vendor's labels. A buyer could not tell from the number what kind of wrong summary was counted, or left out.
3. **The vendor graded its own work.** Per Healthcare Dive, Pieces' own process sampled summaries, used another AI to flag problems, and had physicians review the flags. Summaries the flagging AI missed may not reach a physician; no opened source says how that was handled.
4. **Staff reliance.** The press release says Pieces agreed to make sure hospital staff "understand the extent to which they should or should not rely on its products." A near-zero error claim pushes the other way, toward reading a summary as fact.
5. **The fix is disclosure.** The order requires definitions, methods and known limits, not a new test or a lower error rate.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on an agreement that admits nothing and on press reports; no opened source shows a Pieces summary, its review screen, or its metric data.

- [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`). **Partial fit.** The entry covers clinicians signing AI-drafted notes without reading them. Pieces drafts clinical notes, and the order requires telling staff how far to rely on its output. But no opened source reports any clinician signing a Pieces note unread; the fit is the risk that an advertised near-zero error rate creates.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Weak fit.** A summary that reads as fact, sold with a claim that serious errors almost never happen, is the setting this entry warns about. But no opened source shows a wrong summary, and the reported problem is the claim, not a reply.
- [Word-error-rate-only evaluation](../goals/voice/failures/word-error-rate-only-evaluation.md) (`word-error-rate-only-evaluation`). **Weak fit, by analogy.** That entry warns that one average error number hides the errors that matter. The Pieces dispute is about one headline rate whose meaning a buyer could not see. But that entry is about speech recognition, and nothing here involves voice.
- **Considered, not a fit.** [Patient summaries too simple to be safe](../goals/healthcare-agents/failures/patient-summaries-too-simple-to-be-safe.md) (`patient-summaries-too-simple-to-be-safe`): that entry is about plain-language rewrites for patients; Pieces' summaries are for staff, and no dropped caveat is reported. [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md) (`handoff-summary-is-wrong-or-misleading`): close in shape, but it covers a chatbot handing a customer chat to a person, and no wrong summary is reported. [Transcription hallucination](../goals/voice/failures/transcription-hallucination.md) (`transcription-hallucination`): no speech input is described. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`): about testing on tidy input; no opened source describes Pieces' test inputs. [Fabricated clinical justification in appeals](../goals/healthcare-agents/failures/fabricated-clinical-justification-in-appeals.md) (`fabricated-clinical-justification-in-appeals`): about insurance appeals, not hospital summaries.
- **Possible gaps for a person to judge.** (1) No pattern covers a vendor's published accuracy or hallucination rate that has no stated definition or method, so buyers and staff over-trust the tool. (2) No pattern covers staff-facing generated summaries inside a health record, where the reader is a clinician, not the patient or a customer. These are proposals, not decisions.

## How it differs from close cases

- [DoNotPay and the FTC robot lawyer claims](donotpay-ftc-robot-lawyer-claims-september-2024-and-january-2025.md): another regulator acting on what an AI product was claimed to do, in the same month. There the claims were made to consumers about legal help; here they were made to hospitals about error rates, and there was no money penalty.
- [AP reports Whisper invents text, including in hospital visit tools (October 2024)](openai-whisper-invents-text-in-hospital-transcription-ap-investigation-october-2024.md): reporters showed invented text in clinical transcripts. Here no wrong output is shown; the dispute is over the advertised rate.
- [Babylon Health symptom checker triage concerns (February 2020)](babylon-health-symptom-checker-chatbot-triage-safety-concerns-february-2020.md): a doctor publicly tested a patient-facing health bot. Pieces' text is for clinicians, and the challenge came from a state attorney general, not a tester.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each signal can be computed from generated summaries, clinician edits, and a clinician-labeled review set.

| Signal | How to compute from logs |
|---|---|
| Metric definition coverage | Share of advertised or internal accuracy figures that ship with a written definition of what counts as an error, its severity levels, and the sample it came from |
| Independent error rate | Share of a random sample of summaries that a clinician not tied to the vendor marks as holding a wrong or missing clinically important fact |
| Flagger miss rate | Share of errors found in a full clinician review of a random sample that the automated flagger did not flag |
| Unsupported statement rate | Share of summary sentences with no matching entry in the source record |
| Unread sign-off rate | Share of AI-drafted notes signed with no edit and an open time below a threshold the team sets |
| Edit rate by section | Share of summaries in which clinicians change medications, allergies or pending results, the parts where a miss costs most |

## What a team can change

Our proposals, not Pieces' or the state's. Each is a pass/fail check on a summary, a test run or a marketing claim. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **No number without its meaning.** Pass: every accuracy or hallucination figure in a sales deck, website or contract names its error definition, severity levels, sample size, time window and who did the review. A figure without them fails.
2. **Count misses the flagger missed.** Pass: the reported error rate comes from a random sample reviewed in full by clinicians, not only from summaries an automated checker flagged.
3. **Tie every sentence to the record.** Pass: in a test set, each statement in a summary links to a source entry in the record; any statement with no source is marked for the reader.
4. **Say how far to rely on it, where it is read.** Pass: the summary view itself tells staff it is AI-drafted and must be checked against the record, as the order's reliance language points to.
5. **Make review real for high-risk parts.** Pass: a draft that changes medications, allergies or pending results cannot be signed until the reader opens those changed items.
6. **List known misuses for buyers.** Pass: customer documentation names the uses that raise the risk of wrong output, as the order's paragraph 19 requires of Pieces, before go-live.

## What we could not verify

- Whether any Pieces summary was wrong, and whether any patient was harmed. No opened source reports either.
- The names of the four hospitals and the data behind the advertised rates. Not in the opened text.
- Pieces' own press release. Not opened; a search summary attributed to Pieces the line that the agreement makes no mention of the safety of its products. We use only Healthcare Dive's paraphrase of that point.
- Law firm summaries from Orrick, Hogan Lovells, Manatt, Nelson Mullins and Sidley. Seen only in search results; not used.
- Healthcare IT News coverage. The download was blocked; not used.
- Whether Pieces later asked to rescind or modify the agreement. No opened source reports it.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.texasattorneygeneral.gov/news/releases/attorney-general-ken-paxton-reaches-settlement-first-its-kind-healthcare-generative-ai-investigation | Office of the Texas Attorney General (press release) | 2024-09-18 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.texasattorneygeneral.gov/sites/default/files/images/press/Petition%20for%20Approval%20of%20AVC%20Pieces%20File%20Stamped.pdf | State of Texas and Pieces Technologies, Petition and Assurance of Voluntary Compliance, Dallas County cause DC-24-13476 | 2024-08-21 (filed) | Yes, 2026-10-28, PDF converted to text; quotes checked word for word |
| https://www.fiercehealthcare.com/ai-and-machine-learning/texas-ag-pieces-technologies-settle-allegations-inaccurate-generative-ai | Fierce Healthcare (Dave Muoio) | 2024-09-19 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.healthcaredive.com/news/texas-attorney-general-ken-paxton-settles-pieces-technologies-generative-ai-accuracy/727699/ | Healthcare Dive (Rebecca Pifer Parduhn) | 2024-09-23 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |

## Corrections

If you have Pieces' definitions of its critical and severe hallucination rates, an independent test of its summaries, or a dated filing that modifies or ends the agreement, from a source we can open, tell us and we will fix this page.
