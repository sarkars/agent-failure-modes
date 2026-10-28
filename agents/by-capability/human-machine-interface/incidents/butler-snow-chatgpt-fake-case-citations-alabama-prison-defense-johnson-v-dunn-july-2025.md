---
title: "A Butler Snow partner defending Alabama's prison system filed ChatGPT case citations that did not exist, and a federal judge removed three lawyers from the case, July 2025"
date: 2025-07-23
source: "https://www.law.berkeley.edu/wp-content/uploads/archive/2025/12/Johnson-v-Dunn.pdf"
description: "A lawyer for Alabama's prison system put ChatGPT case citations in two motions without checking them. Five were false, and a judge removed three lawyers."
summary: "In May 2025, lawyers at the firm Butler Snow, defending former Alabama Department of Corrections Commissioner Jefferson Dunn in a suit by incarcerated plaintiff Frankie Johnson, filed two motions with five false case citations. Partner Matthew B. Reeves admitted he used ChatGPT to find supporting case law and did not verify what it returned. The colleague who signed and filed both motions checked only grammar and typos; the group leader scanned one motion briefly. On July 23, 2025, U.S. District Judge Anna M. Manasco publicly reprimanded Reeves, William J. Cranford and William R. Lunsford, disqualified them from the case, ordered them to share the order with clients, opposing counsel and judges in their other pending cases, and referred them to the Alabama State Bar. She released the firm and two other lawyers without sanction. Status: Needs review."
categories:
  - Government
  - Legal and professional advice
  - Accuracy
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - notes-approved-without-being-read
  - false-premises-accepted
  - fabricated-clinical-justification-in-appeals
---

**This page is a dated teardown of one federal sanctions order, for teams that build or govern chat assistants used by professionals who work for a government client, and for anyone who writes the AI-use policy those professionals are meant to follow.** The product was ChatGPT, OpenAI's general chat assistant. The user was Matthew B. Reeves, a partner at Butler Snow, a law firm the State of Alabama hires to defend its prison system. The moment is a search he ran in ChatGPT for case law to support a point he already believed, and then pasted into two motions without checking. The client, in the judge's words, was "an Alabama government agency." The date above is the day the sanctions order was signed.

**Status: Needs review.** Built from two court documents and three news reports, downloaded on 2026-10-28. The sanctions order, Johnson v. Dunn, No. 2:21-cv-1701-AMM (N.D. Ala. July 23, 2025), reported at 792 F. Supp. 3d 1241, was read as a Westlaw PDF hosted by UC Berkeley School of Law and converted to text with pdftotext. Butler Snow LLP's Response to Order to Show Cause (Doc. 195, filed May 19, 2025) was read as a PDF copy hosted on a third-party Amazon S3 site; its pages carry the court's filing header. The news reports, read as raw HTML converted to text, are the Associated Press (Kim Chandler, May 22, 2025, as republished by Corrections1), the Associated Press (July 24, 2025, via Yahoo News; no byline shown) and the ABA Journal (Debra Cassens Weiss, July 30, 2025). Each quote below was checked word for word against that text with a script, with line breaks, curly and straight quote marks treated as the same.

> **Read this first.** This is a summary of a public court record and news reports. It is not legal advice and does not say what any court rule or ethics rule requires beyond quoting the judge's order. The lawyers' accounts come from their own declarations and hearing statements as the order quotes them. We did not see the ChatGPT chats. The State Bar referral had no outcome in any source we opened. We name only the lawyers, judge and officials named in the order or on record with reporters. The underlying suit involves allegations of prison violence; we describe it only as the sources do and judge none of it.

**Channel note.** This is a text incident: a lawyer typed a search into the ChatGPT chat and copied typed answers into a court filing. This phase of the knowledge base is chat-first, and the signals and checks below are written for chat logs and the documents built from them. Voice and web signals, such as a dictated research query or a citation pasted from an AI search page, are PLANNED only: never detected or measured here.

## What happened (from the court record)

- **The case.** Per the AP (July 24), the suit was filed by "an inmate who was stabbed on multiple occasions at the William E. Donaldson Correctional Facility." The defendant was former Corrections Commissioner Jefferson Dunn. Per the AP (May 22), Alabama's attorney general appointed Lunsford a deputy attorney general to represent the state.
- **Two motions, May 7 and May 12, 2025.** Per the order, Dunn's lawyers filed a motion for leave to depose Johnson (Doc. 174) and a motion to compel (Doc. 182). Four Butler Snow lawyers were on each signature block. Cranford filed both under his own credentials.
- **How the citations got in.** Cranford drafted both motions and sent them to Reeves and Lunsford. Reeves sent back revisions with the citations. Reeves's declaration says he "performed a search [on ChatGPT] to identify supporting case law" and "failed to verify the case citations returned by ChatGPT through independent review in Westlaw or PACER." Butler Snow's response says he used ChatGPT "to obtain legal authority to support what Mr. Reeves already understood to be a well-established legal proposition."
- **What came back.** The order lists five problem citations. Some did not exist. Others pointed to real cases on other subjects: one Westlaw number led to "a maritime personal injury case that does not discuss discovery," and one case name matched only a 1939 traffic-offense appeal.
- **Who caught it.** Johnson's lawyers flagged the citations in a response (Doc. 186), "possibly through the use of generative artificial intelligence." On May 16, the judge wrote that she "ha[d] conducted independent searches for each allegedly fabricated citation, to no avail," and ordered the signers and the firm to show cause.
- **The signer's check.** Cranford said he reviewed the edits "for grammatical and typographical issues" and "did not conduct an independent review of the legal authorities added." At the hearing: "In my normal practice, I do not typically check citations that are added from Mr. Lunsford or Mr. Reeves." He did not know ChatGPT had been used.
- **The supervisor's check.** Lunsford did not review the first motion. On the second: "I did not conduct any detailed or substantive review of the legal authorities."
- **The policy already in place.** Per the order, a June 2023 firm email warned of "significant risks that LLM [Large Language Model] output can appear perfectly researched and logical while in fact it is wholly inaccurate." Lunsford: "Under firm policy, the use of ChatGPT for legal research requires written approval from a practice group leader." Reeves admitted he "did not comply with the [firm's] policy." Per the order, firm counsel confirmed that practice group leaders "did not have to seek permission to utilize artificial intelligence" under the policy then in force; Reeves was an assistant practice group leader.
- **The firm's review.** "In all, Morgan Lewis reviewed more than 2,400 separate legal citations across 330 filings," the order says, quoting Butler Snow; a Morgan Lewis partner found no other fabricated citations.

## What the people and organizations said

- **Butler Snow, May 19 (Doc. 195).** "What happened here is unacceptable." And: "Butler Snow is embarrassed by what happened here, which was against good judgment and firm policy." It promised a prefiling protocol "confirming the existence, accuracy, and relevance of each citation," per the Watson declaration quoted in the order.
- **Reeves, at the May 21 hearing**, per the AP: "I would hope your honor would not punish my colleagues."
- **The Alabama Attorney General's Office.** Brad Chynoweth told the court "there is no generative AI platform that is authorized for use" by the office, and that Lunsford "remains the [A]ttorney [G]eneral's counsel of choice."
- **Judge Manasco, July 23.** "In simpler terms, the citations were completely made up." "Fabricating legal authority is serious misconduct that demands a serious sanction." On Reeves: "This is recklessness in the extreme, and it is tantamount to bad faith." On the firm: it "acted reasonably in its efforts to prevent this misconduct and doubled down on its precautionary and responsive measures when its nightmare scenario unfolded."
- **The outcome.** Public reprimand, publication, disqualification and State Bar referral for Reeves, Cranford and Lunsford; Chism, Potter and Butler Snow released without sanction. Dunn "was unaware of his attorney's conduct," so the court declined to sanction him, and stayed the case thirty days for his new counsel.
- **OpenAI.** No opened source reports a comment from OpenAI.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| How many signers | The order and AP (May 22): four lawyers on each signature block, with Potter added to the motion to compel by mistake. ABA Journal: "three out of five lawyers who signed the motion." |
| The ChatGPT prompt | The order paraphrases Reeves's purpose. No opened source shows his typed words or ChatGPT's reply. |
| State payments | AP (July 24): "Alabama has paid Lunsford and his firm more than $40 million since 2020, according to state spending records." Not checked against those records. |
| What happened next | No opened source reports the State Bar's action or the case's later course. |

## Where in the flow it broke

Based on the order and filings above, and only as far as they go.

1. **The request assumed the answer.** Reeves sought support for a point he already believed. The chat returned cases shaped to fit.
2. **Output looked like real research.** Citations came back in standard form, with reporter and Westlaw numbers, some pointing to real but unrelated cases.
3. **No check against a database.** Reeves had Westlaw and PACER and did not use them.
4. **The AI's role was invisible downstream.** Cranford got edits in redline or plain text with no sign that a chatbot wrote any part.
5. **Signers trusted the hierarchy.** The filer checked grammar; the supervisor checked facts and headings. Nobody owned the citations.
6. **The policy had a gap at the top.** Approval was required from a practice group leader; per firm counsel, leaders themselves did not need permission.
7. **The other side caught it.** Opposing counsel, then the judge, found the false citations.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on the order and filings; no opened source shows the chats.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** ChatGPT returned citations in the form of real ones, some with numbers that resolve to unrelated real cases. Nothing in the reply, as described, told the user they were unverified.
- [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`). **Partial fit.** Two lawyers signed AI-assisted filings without checking the AI-added parts, and were sanctioned for it. Partial because that entry covers clinicians signing AI-drafted notes, and here the signers did not know AI was involved.
- [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`). **Weak fit.** The search asked for cases supporting a proposition, and the tool supplied cases rather than saying it found none. Weak because the exact prompt is not public, and the proposition itself may be sound.
- [Fabricated clinical justification in appeals](../goals/healthcare-agents/failures/fabricated-clinical-justification-in-appeals.md) (`fabricated-clinical-justification-in-appeals`). **Weak fit.** The same shape, invented support placed into a formal argument to an authority, in a health-insurance setting. Named only as a cross-domain analog.
- **Considered, not a fit.** [Crossing into practising law](../goals/legal-agents/failures/crossing-into-practising-law.md) (`crossing-into-practising-law`): the user was a licensed lawyer, not a consumer seeking advice. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): the sources were invented, not selectively chosen. [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`): no opened source shows what ChatGPT said about its limits. [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) (`eligibility-answers-sound-like-decisions`): the client was a government agency, but no resident used the tool.
- **Possible gaps for a person to judge.** (1) No pattern covers AI-written text that reaches a co-signer through a supervisor's edit with no mark of where it came from. (2) No pattern covers an AI-use policy whose approvers are exempt from it. (3) No pattern covers invented citations whose ID numbers resolve to real, unrelated records, which can pass a quick lookup. These are proposals, not decisions.

## How it differs from close cases

- [Mata v. Avianca (2023)](mata-v-avianca-fabricated-case-citations-2023.md): also ChatGPT-invented cases in federal court, which this order cites. There a fine; here disqualification and a State Bar referral.
- [Morgan & Morgan MX2.law in Wadsworth v. Walmart (February 2025)](morgan-and-morgan-mx2-law-fake-case-citations-wadsworth-v-walmart-february-2025.md): co-signers also skipped the citations. There the tool was in-house; here a public chatbot used against firm policy.
- [Kohls v. Ellison (November 2024)](chatgpt-fake-citations-stanford-expert-declaration-kohls-v-ellison-november-2024.md): fake citations filed on behalf of a state, there in an expert declaration for Minnesota's attorney general.
- [Two federal judges' staff AI drafts docketed (October 2025)](federal-judges-wingate-and-neals-staff-ai-drafts-docketed-error-filled-orders-october-2025.md): AI errors from the bench, not from counsel.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each can be computed from chat logs, document history and a citation database; each has a counter-signal.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Unresolved citations | Share of citations in a chat reply that do not resolve in a case-law database | Real citations wrongly flagged because of format differences |
| Mismatched resolutions | Share of citations whose number resolves to a case with a different name or subject | Share flagged for minor name variants of the same case |
| Paste without lookup | Share of chat-sourced citations pasted into a draft with no database lookup logged between | Lookups done outside the logged tool |
| Unmarked AI text | Share of AI-sourced passages in a shared draft with no provenance mark | Share of marks so common that readers ignore them |
| Signer citation coverage | Share of citations in a filed document that each signer's review log shows as checked | Time to file, so review does not stall urgent filings |

## What a team can change

Our proposals, not Butler Snow's or the court's. Each is a pass/fail check on a chat log or a document. Status: Not yet run. Test sets and thresholds are for the team to set, with review by practicing lawyers.

1. **Say when a case is unverified.** Pass: a chat reply that lists case citations states, for each, that it has not been checked against a database, or links the database record. Fail: a bare citation list.
2. **Say when nothing fits.** Pass: asked for cases supporting a proposition, the assistant says it found none when it cannot point to one. Fail: invented cases.
3. **Mark pasted AI text.** Pass: text copied from a chat assistant into a shared draft carries a visible source mark until a person clears it. Fail: no mark.
4. **Every signer checks every citation, or says who did.** Pass: before filing, the document shows a named person who resolved each citation. Fail: no record.
5. **No exemptions for approvers.** Pass: the AI-use rule applies to the people who approve its use. Fail: leaders exempt.

## What we could not verify

- The ChatGPT chats, the model version and Reeves's typed prompts. No opened source shows them.
- The CourtListener and Justia docket pages, including Doc. 204 as filed; our copy of the order is the Westlaw version.
- The Alabama State Bar's action, the case's later course, and whether Reeves's planned law-school program happened.
- The AP's figure that Alabama paid the firm "more than $40 million since 2020."
- Seen only in search summaries and not used as fact: Law360 reports, one said to describe the firm calling the episode an isolated event; Reuters coverage; EDRM commentary; and entries in the AI Incident Database and OECD.AI.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.law.berkeley.edu/wp-content/uploads/archive/2025/12/Johnson-v-Dunn.pdf | U.S. District Court, N.D. Ala. (Judge Anna M. Manasco), sanctions order, 792 F. Supp. 3d 1241, Westlaw copy | 2025-07-23 | Yes, 2026-10-28, PDF read as text; quotes checked word for word |
| https://websitedc.s3.amazonaws.com/documents/Johnson_v._Dunn_N._Alabama_USA_May_19_2025.pdf | Butler Snow LLP, Response to Order to Show Cause (Doc. 195), third-party copy | 2025-05-19 | Yes, 2026-10-28, PDF read as text; quotes checked word for word |
| https://www.corrections1.com/legal/sanctions-possible-for-ala-prison-defense-attorneys-over-fake-ai-generated-legal-citations | Associated Press (Kim Chandler), via Corrections1 | 2025-05-22 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.yahoo.com/news/articles/judge-sanctions-lawyers-defending-alabama-221155007.html | Associated Press, via Yahoo News; no byline shown | 2025-07-24 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.abajournal.com/news/article/5-fabricated-cases-lead-federal-judge-to-kick-3-butler-snow-lawyers-off-case | ABA Journal (Debra Cassens Weiss) | 2025-07-30 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.courthousenews.com/attorney-sanctions-in-alabama-demonstrate-perils-of-ai/ | Courthouse News Service | Not confirmed | No: returned a bot check on 2026-10-28; not used |

## Corrections

If you have the ChatGPT chats, the filed docket entries, the State Bar's decision or a later account of the case, from a source we can open, tell us and we will fix this page.
