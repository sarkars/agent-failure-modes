---
title: "An AI-built outline put fake citations in a brief by K&L Gates and Ellis George lawyers in Lacey v. State Farm, and a special master struck it and ordered $31,100 paid, May 2025"
date: 2025-05-05
source: "https://storage.courtlistener.com/recap/gov.uscourts.cacd.930490/gov.uscourts.cacd.930490.119.0.pdf"
description: "A lawyer built a brief outline with AI research tools and did not say so. Co-counsel filed it unchecked, and a special master struck the brief."
summary: "In April 2025, plaintiff's lawyers from Ellis George and K&L Gates in Lacey v. State Farm General Insurance Co. (C.D. Cal.) filed a supplemental brief on a privilege dispute. Ellis George partner Trent Copeland had built an outline with CoCounsel, Westlaw Precision and Google Gemini and sent it to K&L Gates lawyers without saying so; nobody checked the citations. Special Master Michael R. Wilner, a retired magistrate judge, found about nine of 27 citations wrong and at least two that did not exist. After he flagged two, a revised brief removed only those. In an order dated May 5 and filed May 6, 2025, he struck the briefs, denied the discovery relief sought, and ordered the two firms, jointly and severally, to pay the defense $31,100. He sanctioned no individual lawyer. Status: Needs review."
categories:
  - Legal and professional advice
  - Accuracy
  - Governance
patterns:
  - text-invented-citations
  - confident-wrong-answer-with-no-way-to-check
  - notes-approved-without-being-read
  - provenance-self-declared-labels
---

**This page is a dated teardown of one sanctions order, for teams that build AI legal research tools and for firms that write rules on how lawyers pass AI output to each other.** The products were CoCounsel, Westlaw Precision and Google Gemini, as named in a sworn declaration. The user was Trent Copeland, a partner at Ellis George LLP. The moment is an outline of legal arguments he emailed to co-counsel at K&L Gates on April 9, 2025, with no word that AI tools helped build it. The date above is the day the order was signed.

**Status: Needs review.** Built from the special master's order (Doc. 119, filed May 6, 2025, 77 pages with an appendix holding his April 15 order to show cause, the lawyers' declarations and the marked briefs) and three news reports, downloaded on 2026-10-30. The order was read as a PDF converted to text with pdftotext; the copy on CourtListener and the copy in Damien Charlotin's AI hallucination database are byte-identical. Each quote below was checked word for word against saved text with a script, with line numbers, line breaks, curly and straight quote marks and dash styles treated as the same.

> **Read this first.** This is a summary of public court filings and news reports. It is not legal advice and does not say what any court rule or ethics rule requires beyond quoting the order. It makes no finding beyond what the order says. The lawyers' accounts come from their own declarations. We did not see the AI tools' outputs or the prompts; we cannot say which tool produced which error, and neither could Copeland. We name only the people named in the filings.

**Channel note.** This is a text incident: typed research in AI tools, typed into an outline, pasted into a brief. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (from the order and its appendix)

- **The case.** Per the order, Wilner was appointed special master in January 2025 in "this insurance-related civil action," mainly over the insurer's privilege claims. The plaintiff is Jacquelyn "Jackie" Lacey; the defendant is State Farm General Insurance Co.
- **The outline.** Copeland's declaration: "I believe I initially used CoCounsel, which I had recently been exposed to through a firm training, as well as Westlaw's AI tool to undertake research. I also briefly conducted internet research using Gemini." He was preparing for a trial starting April 14 and emailed "notes and high-level thoughts in outline format."
- **The hand-off.** K&L Gates partner Ryan Keech: "Mr. Copeland did not indicate where those citations came from and I did not independently verify those citations." The order: the K&L Gates lawyers "didn't know that Mr. Copeland used AI to prepare the outline; nor did they ask him."
- **What the special master found.** Reading Version 1 of the brief on April 14, Wilner looked up the cases on Westlaw. A quotation attributed to *National Steel Products* "does not exist in that opinion." A *Booth v. Allstate* cite: "The decision does not appear to exist." Overall, "approximately nine of the 27 legal citations in the ten-page brief were incorrect in some way."
- **The quiet fix.** Wilner emailed about the two cites. A K&L Gates associate's email said they "were inadvertently included prior to filing" and had been "addressed and updated." Per the order, the Revised Brief was "still containing a half-dozen AI errors," with "no disclosure to me about the use of AI."
- **How the errors got through.** Copeland: "it is apparent that no one confirmed the accuracy of some of citations pulled from my preliminary outline." And: "our process broke down at several levels across both firms."
- **Firm rules.** K&L Gates said it "blocks its attorneys from accessing such tools absent, inter alia, tool-specific training," and that none of its lawyers on the brief used AI.

## What the order said and did

- **The finding.** The lawyers "collectively acted in a manner that was tantamount to bad faith." The "initial, undisclosed use of AI products to generate the first draft of the brief was flat-out wrong."
- **Harm to the reader.** "Directly put, Plaintiff's use of AI affirmatively misled me." It "almost led to the scarier outcome (from my perspective) of including those bogus materials in a judicial order."
- **Sanctions.** Supplemental briefs struck; no further discovery relief on the privilege issue; the firms to pay "approximately $26,100" for special master fees that the defense had advanced to JAMS, plus "a total of $5,000" toward defense fees, "in the aggregate amount of $31,100."
- **No individual sanctions.** "This was a collective debacle, and is properly resolved without further jeopardy." The client "will not, however, be financially responsible" for the awards.
- **The AI vendors.** No opened source reports a comment from Thomson Reuters (CoCounsel, Westlaw) or Google. The ABA Journal said the lawyers and firms had not immediately responded.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Amount | Order and ABA Journal: $31,100. The Verge: "$31,000 in sanctions." |
| Tools | Copeland's declaration: CoCounsel, Westlaw's AI tool and Gemini. The Verge: "Google Gemini, as well as the AI legal research tools in Westlaw Precision with CoCounsel." |
| Who filed | The order: "K&L Gates re-submitted the brief." K&L Gates, as the order summarizes its position: "it did not sign or file the subject brief." The CourtListener docket lists the brief (Doc. 98) under Copeland's name. |
| Which tool erred | Copeland could not say whether the errors were "human error in my transcription" or a tool "returned some erroneous information." No source settles it. |

## Where in the flow it broke

Based on the order and declarations, and only as far as they go.

1. **AI output entered a human document unmarked.** The outline carried citations with no note of how they were found.
2. **Trust replaced checking.** K&L Gates lawyers trusted a senior co-counsel's citations.
3. **The fix treated symptoms.** After two flagged cites, the revised brief removed those two and left the rest, and the email called them inadvertent.
4. **The reader caught it.** The special master's own Westlaw lookups found the problem.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Invented citations and quotes](../goals/ai-slop-detection/failures/text-invented-citations.md) (`text-invented-citations`). **Strong fit.** A brief built partly from AI research shipped with nonexistent cases and phony quotations.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Good fit.** Wrong quotes came in standard citation form. Not strong, because no source shows what the tools displayed, and Copeland could not rule out his own transcription errors.
- [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`). **Partial fit.** Lawyers filed AI-derived text without checking it, but that entry covers clinicians, and here the filers did not know AI was involved.
- [Self-declared AI labels](../goals/ai-slop-detection/failures/provenance-self-declared-labels.md) (`provenance-self-declared-labels`). **Weak fit.** AI content went out unlabeled because labeling depended on the author declaring it. That entry covers platform posts, not documents between lawyers.
- **Considered, not a fit.** [Crossing into practising law](../goals/legal-agents/failures/crossing-into-practising-law.md) (`crossing-into-practising-law`): the users were licensed lawyers. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): the problem was invented or garbled sources, not selective ones. [AI-generated code not tagged as AI](../goals/ai-slop-detection/failures/code-untracked-ai-vulnerabilities.md) (`code-untracked-ai-vulnerabilities`): same untagged-AI shape, but about code.
- **Possible gaps for the owner to judge.** (1) No pattern covers AI output relayed person to person, where the second person cannot know it came from AI. (2) No pattern covers a partial correction: fixing only the errors someone flagged and calling them inadvertent. (3) No pattern covers mixed-origin errors where the user cannot tell whether the tool or his own copying was wrong. These are proposals, not decisions.

## How it differs from close cases

- [Mata v. Avianca (2023)](mata-v-avianca-fabricated-case-citations-2023.md) and [Michael Cohen's Google Bard citations (December 2023)](michael-cohen-google-bard-fake-case-citations-december-2023.md): general chatbots. Here the tools included legal research products.
- [Morgan & Morgan MX2.law in Wadsworth v. Walmart (February 2025)](morgan-and-morgan-mx2-law-fake-case-citations-wadsworth-v-walmart-february-2025.md) and [Butler Snow in Johnson v. Dunn (July 2025)](butler-snow-chatgpt-fake-case-citations-alabama-prison-defense-johnson-v-dunn-july-2025.md): co-signers skipped the citations too; here the gap crossed two firms.
- [Kohls v. Ellison (November 2024)](chatgpt-fake-citations-stanford-expert-declaration-kohls-v-ellison-november-2024.md) and [Anthropic's Claude citation in the Concord expert declaration (May 2025)](anthropic-claude-wrong-citation-concord-music-expert-declaration-may-2025.md): AI citation errors in expert declarations, not lawyers' briefs.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals only; voice and web signals are PLANNED only.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Unresolved quotes | Share of quoted passages in a tool's reply not found in the cited opinion's text | Real quotes missed because of formatting |
| Unmarked export | Share of AI-sourced citations copied out of the tool with no source mark attached | Marks so common that readers ignore them |
| Partial correction | After one citation is flagged, share of other citations in the same document re-checked before resubmission | Time to resubmit |

## What a team can change

Our proposals, not the court's or the firms'. Each is a pass/fail check. Status: Not yet run.

1. **Quote check before display.** Pass: a quotation shown as from an opinion matches that opinion's text, or the tool says it could not match it. Fail: an unmatched quote shown as verbatim.
2. **Origin travels with the text.** Pass: citations exported from an AI tool carry a visible mark saying they came from an AI tool and are unverified, until a person clears it. Fail: plain text with no mark.
3. **One flag, full recheck.** Pass: when one citation in a document is flagged, every citation is re-resolved before resubmission. Fail: only the flagged ones change.

## Unverified

- The AI tools' outputs, prompts and model versions. The order's appendix includes a version of the outline; we did not compare it with tool output.
- Whether Thomson Reuters or Google commented. Charlotin's database marks the entry "Vendor Disputed"; we did not open what that refers to.
- Whether the $31,100 was paid, and what later happened in the case.
- Seen only in search summaries and not used as fact: Mealey's, Today's General Counsel, Daily Journal, Legal Technology, the AI Incident Database (incident 1073) and vibegraveyard.ai.

## Sources

| Outlet | Author | Date | URL | How read |
|---|---|---|---|---|
| U.S. District Court, C.D. Cal., No. 2:24-cv-05205-FMO-MAA, Doc. 119 | Special Master Michael R. Wilner (Ret.) | Dated 2025-05-05, filed 2025-05-06 | https://storage.courtlistener.com/recap/gov.uscourts.cacd.930490/gov.uscourts.cacd.930490.119.0.pdf | Raw text (PDF to text); quotes script-matched |
| CourtListener docket search | Free Law Project | Retrieved 2026-10-30 | https://www.courtlistener.com/docket/68872463/jacquelyn-jackie-lacey-v-state-farm-general-insurance-company/ | Raw text of search listing (Doc. 98 entry) |
| Volokh Conspiracy (Reason) | Eugene Volokh | 2025-05-13 | https://reason.com/volokh/2025/05/13/ai-hallucination-in-filings-involving-14th-largest-u-s-law-firm-lead-to-31k-in-sanctions/ | Raw text; excerpts match the order |
| ABA Journal | Debra Cassens Weiss | 2025-05-14 | https://www.abajournal.com/web/article/judge-imposes-sanctions-for-collective-debacle-involving-ai-hallucinations-and-2-law-firms-including-k | Raw text; quotes script-matched |
| The Verge | Emma Roth | 2025-05-13 | https://www.theverge.com/news/666443/judge-slams-lawyers-ai-bogus-research | Raw HTML converted to text; quotes script-matched |
| AI Hallucination Cases database | Damien Charlotin | Retrieved 2026-10-30 | https://www.damiencharlotin.com/hallucinations/?q=Lacey | Raw text; used only to locate the order PDF |

## Corrections

If you have the AI tools' outputs, a vendor statement or a later account of the case from a source we can open, tell us and we will fix this page.
