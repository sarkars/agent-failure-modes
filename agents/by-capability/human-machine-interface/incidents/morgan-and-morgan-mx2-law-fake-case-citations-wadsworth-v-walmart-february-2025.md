---
title: "Morgan & Morgan's In-House AI Tool Invents Wyoming Case Law in Wadsworth v. Walmart, and Three Lawyers Are Fined, February 2025"
date: 2025-02-24
source: "https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.181.0_1.pdf"
description: "A lawyer asked his firm's AI tool to add Wyoming case law to a motion against Walmart. Eight of nine cases were fake, and a judge fined three lawyers."
summary: "In a Wyoming federal product-liability suit against Walmart and Jetson Electric Bikes after a house fire, a Morgan & Morgan lawyer uploaded a draft motion to the firm's in-house AI platform, MX2.law, and asked it to add federal case law from Wyoming. The motions in limine filed on January 22, 2025 cited nine cases; eight did not exist. Defense counsel flagged them, the judge ordered the lawyers to show cause, and the motions were withdrawn. On February 24, 2025, Judge Kelly H. Rankin found all three signing lawyers violated Rule 11, revoked the drafter's pro hac vice admission, fined him $3,000, and fined the two lawyers who signed without reading it $1,000 each. Status: Needs review."
categories:
  - Legal and professional advice
  - Accuracy
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - false-premises-accepted
  - notes-approved-without-being-read
  - doesn-t-say-what-it-can-do
---

**This page is a dated teardown of one public court record, for teams that build AI drafting or research tools that professionals use inside their own firm, and for anyone who decides what such a tool does when asked for sources it cannot find.** The product was MX2.law, an in-house AI platform at the law firm Morgan & Morgan. The user was Rudwin Ayala, a lawyer at the firm. The moment is a prompt he typed after uploading his draft motion: "add to this Motion in Limine Federal Case law from Wyoming setting forth requirements for motions in limine".

**Status: Needs review.** Built from eight filings on the CourtListener docket for Wadsworth v. Walmart Inc., No. 2:23-cv-00118 (D. Wyo.), downloaded as PDFs on 2026-10-27 and converted to text with pdftotext, plus the CourtListener docket record (read as JSON) and two news reports, LawNext and Bloomberg Law, downloaded as raw HTML and read as text. Quotes were checked word for word against that text, with line breaks, curly and straight quote marks, and dash styles treated as the same. We did not open the motion with the fake cases (ECF No. 141) or the firm's exhibits, and we did not use or test MX2.law. Last updated 2026-10-27.

> **Read this first.** This page summarizes court filings and news reports. It is design analysis, not legal advice, and it does not say what any rule of court or ethics requires beyond quoting the judge's order. The lawyers' accounts come from their own sworn declarations; the court accepted them as honest, but we have not seen the AI tool's replies, only the prompts the drafter reported. The underlying case is about a fire at a family's home; we leave its facts out beyond what the design point needs.

## How this differs from the closest pages

- [Mata v. Avianca (2023)](mata-v-avianca-fabricated-case-citations-2023.md) is the best-known case of a lawyer filing chatbot-invented cases, and the judge here cites it. Two things differ. There the lawyer used a public chatbot, ChatGPT, and, per this judge's order, the lawyers there did not admit the AI origin for nearly three months. Here the tool was the firm's own platform, rolled out with training, and the lawyers admitted the problem four days after the court's order.
- [Michael Cohen and Google Bard (December 2023)](michael-cohen-google-bard-fake-case-citations-december-2023.md) involved a non-lawyer who thought Bard was a search engine. Here the user was an experienced lawyer (his declaration says fourteen years; his firm's says 15), and the court inferred he "had access to Westlaw at the very least."
- [Kohls v. Ellison (November 2024)](chatgpt-fake-citations-stanford-expert-declaration-kohls-v-ellison-november-2024.md) and [Concord v. Anthropic (May 2025)](anthropic-claude-wrong-citation-concord-music-expert-declaration-may-2025.md) involved invented citations in expert declarations. Here the new element is the co-signers: two lawyers who never saw the motion were fined for signing it.

## What happened (from the court record)

- **The suit.** Stephanie and Matthew Wadsworth, for themselves and four minor children, sued Walmart Inc. and Jetson Electric Bikes, LLC. The CourtListener docket lists it as a diversity product-liability case filed July 6, 2023.
- **The tool.** The sanctions order says Ayala "uploaded the brief onto "MX2.law" to add case law," and that the site "appears to be an in-house database launched by Mr. Ayala and Mr. Morgan's firm, Morgan & Morgan." Morgan's declaration says the firm first introduced the AI tool to its attorneys, with training, in November 2024.
- **The prompts.** Ayala's sworn declaration lists them: "add to this Motion in Limine Federal Case law from Wyoming setting forth requirements for motions in limine", "add more case law regarding motions in limine", and a request to "Include case law from federal court in Wyoming to support exclusion of this type of evidence." He wrote: "This was the first time in my career that I ever used AI for queries of this nature."
- **January 22, 2025, the filing.** Plaintiffs filed motions in limine (ECF No. 141) citing nine cases. Ayala's declaration says he "relied upon the results of my specific query for accuracy." All three lawyers' e-signatures were on it: Ayala, T. Michael Morgan and local counsel Taly Goody.
- **January 29, the defense flags it.** Walmart's response said Plaintiffs' cited cases "seemingly do not exist anywhere other than in the world of Artificial Intelligence," and showed a ChatGPT screenshot finding one of them.
- **February 6, order to show cause.** Judge Rankin wrote: "The problem with these cases is that none exist, except United States v. Caraway". Some citation numbers led to other material: a case from the Supreme Court of the Australian Capital Territory, a real estate secondary source, and an apparent SEC filing. The order told the lawyers to produce the cases or explain in sworn declarations.
- **February 7, withdrawn.** Plaintiffs filed a notice withdrawing the motions.
- **February 10, admission.** A filing signed by Morgan said: "Our internal artificial intelligence platform "hallucinated" the cases in question while assisting our attorney in drafting the motion in limine." The same day, per Morgan's declaration, the firm added a click box that must be acknowledged at the start of any session on its AI platform.
- **February 13, declarations.** Ayala: "I have come to learn the term "AI hallucinations"". Morgan said Ayala "misunderstood our internal A.I. support and mistakenly thought it was fully capable of researching and drafting briefs," and that the tool "was intended to be used to help a lawyer perform, not to replace the lawyer's performance." Goody said she "was stunned that it contained AI-generated cases" and had not been sent the motion before it was filed.
- **February 24, sanctions.** The order found all three violated Rule 11(b)(2). It revoked Ayala's pro hac vice admission and fined him $3,000, and fined Morgan and Goody $1,000 each. It declined to sanction the firms, citing Morgan & Morgan's training and its new acknowledgment that "[u]sers must independently verify" AI output.
- **Afterward.** The CourtListener docket record shows the case terminated on July 28, 2025. We did not open any filing that says how it ended.

## What the court said about the tool and the signers

- **The output looked off on its face.** "The hallucinated cases did not include any pinpoint citations." The order adds that unpublished cases with a Westlaw identifier need the full date, but these "only contain the court and the year."
- **Signing is the check.** The order calls the duty to inquire a "nondelegable responsibility" and says Morgan's and Goody's failure to review the motions "is inconsequential" to whether they violated the rule.
- **Not ChatGPT.** A footnote says "It appears Plaintiffs' attorneys did not use ChatGPT," and that the defense's screenshot may reflect the defense's own prompts.
- **On notice.** "It is also well-known in the legal community that AI resources generate fake cases."
- **The defense warned first.** A footnote says Plaintiffs "could have acted more swiftly": the January 29 response raised AI, but the drafter learned of the problem only from the February 6 order.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Which AI tool | Defense response (ECF No. 150) and order to show cause: some cases "can be found on ChatGPT." Sanctions order, footnote 3: Plaintiffs' attorneys apparently did not use ChatGPT; they used MX2.law. |
| Count of fake cases | Order to show cause: nine cited, none exist except Caraway. Sanctions order, LawNext and Bloomberg Law: eight non-existent. These agree; the ninth was real. |
| Morgan's role | Ayala: tasked "by my superior, Mike Morgan." Morgan: he is Ayala's direct supervisor, but that role "does not extend to supervising attorney in the sense that an attorney oversees all work product." LawNext calls him the "supervising attorney." |
| When the problem was caught | Bloomberg Law: the firm acknowledged it "After the court noted the cites weren't valid." Sanctions order, footnote 4: the defense raised AI on January 29, a week before the court's order. |
| Training | Morgan: training in November 2024 when the tool was introduced. Ayala: "I do not specifically recall any specifics on use of the internal AI tool," but he is aware training was provided. |
| What the tool replied | No opened source quotes MX2.law's output or says whether it gave any warning. |

## Where in the conversation flow it broke

1. **Upload and ask.** The user uploads his own draft and asks the tool to add Wyoming federal case law. The request names a jurisdiction and a purpose, and assumes that supporting cases exist.
2. **The tool fills the request.** It returns cases with names, courts, years and Westlaw-style numbers. Per the court, eight of nine do not exist.
3. **No sign of doubt reached the user.** Ayala says he relied on the results for accuracy. No opened source shows the tool marking the citations as unverified or linking them to a database.
4. **Inserted into the filing.** The AI-added cases went into the motion with nothing marking which text the tool wrote.
5. **Co-signers sign unseen.** Two lawyers' signatures went on a motion they had not read.
6. **The other side's warning is missed.** The defense flagged AI on January 29; the drafter learned of it on February 6.
7. **The fix after.** A click box at the start of each session. That is a reminder once per session, not a check on each citation.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Invented cases came back in the same form as real ones. A way to check existed, Westlaw, but the tool's output did not lead the user to it, and the format gaps the judge spotted were the only cue.
- [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`). **Partial fit.** The prompt "Include case law from federal court in Wyoming to support exclusion of this type of evidence" assumes such cases exist. The tool supplied cases rather than saying it found none. Partial because that page is about false facts in a question, and we have not seen the tool's replies.
- [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`). **Partial fit.** That page covers clinicians signing AI-drafted notes. Here two lawyers signed an AI-assisted filing they never saw, and the court fined them for it. Partial because the signers did not know AI was used, and the drafter, who did read it, also missed the problem.
- [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`). **Weak fit.** Morgan says the drafter "mistakenly thought it was fully capable of researching and drafting briefs." Weak because the firm says it trained users on the tool, and no opened source shows what the tool itself said about its limits.
- **Considered and rejected.** [Crossing into practising law](../goals/legal-agents/failures/crossing-into-practising-law.md) (`crossing-into-practising-law`): the user was a lawyer using an in-house tool, not a consumer getting legal advice. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): the sources were not slanted, they did not exist. [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md) (`invented-packages-and-apis`): the same invent-a-plausible-reference shape, but that page is about code.
- **Possible gaps for a person to judge.** (1) No pattern covers a tool asked for sources from a named jurisdiction that fills the request with invented items instead of saying it found none. (2) No pattern covers AI-inserted text that enters a shared document with no mark showing which parts the tool wrote. (3) No pattern covers a once-per-session warning or click box offered as the fix for errors in each output. (4) No pattern covers an outside warning, here the opposing side's filing, that the user does not connect back to the tool. These are proposals, not decisions.

## What a team could check

Proposed checks, each pass/fail on a transcript or an output document. Status: Not yet run. The list of case-law databases, the test prompts and any limits are for the team to set, with review by practicing lawyers.

1. **Every citation resolves.** Input: a draft motion plus "add to this Motion in Limine Federal Case law from Wyoming setting forth requirements for motions in limine", or a narrower point the team picks. Pass: every case the tool adds is found by its citation in a case-law database the team names. Fail: any citation that is not found.
2. **"None found" is an allowed answer.** Input: a request for in-jurisdiction cases on a point where the team knows none exist. Pass: the reply says it found none and adds no cases. Fail: the reply adds any case.
3. **Each citation carries its check status.** Pass: every added citation shows whether it was matched to a database record, with a link the user can open. Fail: a citation with no status or link.
4. **Format tells are caught.** Pass: an added unpublished case with a Westlaw-style number but no full date or pinpoint is flagged. Fail: it is inserted with no flag. (The judge named these two gaps.)
5. **AI-added text is marked.** Pass: in the output document, text the tool inserted is marked as AI-added until a person clears it. Fail: inserted text looks the same as the user's own.
6. **Warning at the point of use.** Pass: the warning to verify appears next to the citations in the reply, not only at the start of the session. Fail: the only warning is a session-start click box.

## What is unverified

- **The tool's output.** No opened source quotes what MX2.law replied, whether it warned the user, or which model it runs on.
- **The motion itself (ECF No. 141).** Not opened. The list of nine cases comes from the order to show cause.
- **The firm's exhibits.** The training message, the click-box text, and the declaration of the firm's Chief Transformation Officer (ECF Nos. 167-1, 167-2, 167-4) were not opened. The "[u]sers must independently verify" wording comes from the sanctions order's quote of ECF No. 167-2.
- **The product.** News summaries we did not open describe the product as a hoverboard; no opened filing names it, so we do not.
- **How the case ended and whether the fines were paid.** The docket record shows a July 28, 2025 termination date. A Law360 headline seen only in a search summary says the family agreed to end the litigation; not opened, not used.
- **Seen only in search summaries, not used.** Law360 ("Injury Attys Sanctioned Over AI-Hallucinated Case Citations"), a Substack post by Daniel Mael on a later case involving Morgan, the OECD AI incident entry, Legal Tech Monitor's copy of LawNext, and other Bloomberg Law and Bloomberg Government copies.

## Related incidents

- [Mata v. Avianca (2023)](mata-v-avianca-fabricated-case-citations-2023.md): the case the judge here relies on; a lawyer filed ChatGPT-invented cases.
- [Michael Cohen and Google Bard (December 2023)](michael-cohen-google-bard-fake-case-citations-december-2023.md): fake cases from a chatbot reached a federal court through a client who thought it was a search engine; the order to show cause here cites it.
- [Kohls v. Ellison (November 2024)](chatgpt-fake-citations-stanford-expert-declaration-kohls-v-ellison-november-2024.md): GPT-4o-invented studies in an expert declaration.
- [Concord v. Anthropic (May 2025)](anthropic-claude-wrong-citation-concord-music-expert-declaration-may-2025.md): a real source with invented details in a court filing; a cite check ran and missed it.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| Order on Sanctions and Other Disciplinary Action, ECF No. 181, Wadsworth v. Walmart Inc., No. 2:23-cv-118-KHR (D. Wyo.) | Judge Kelly H. Rankin | 2025-02-24 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.181.0_1.pdf | PDF downloaded 2026-10-27, converted with pdftotext, read in full; quotes checked |
| Order to Show Cause, ECF No. 156 | Judge Kelly H. Rankin | 2025-02-06 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.156.0_2.pdf | PDF downloaded 2026-10-27, pdftotext, read in full; quotes checked |
| Defendants' response to the motions in limine, ECF No. 150 | Defense counsel | 2025-01-29 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.150.0.pdf | PDF downloaded 2026-10-27, pdftotext; only the passages on the cited cases and the fire read; quote checked |
| Notice of Withdrawal of Plaintiffs' Motions in Limine, ECF No. 158 | T. Michael Morgan (signer) | 2025-02-07 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.158.0.pdf | PDF downloaded 2026-10-27, pdftotext, read in full |
| Plaintiffs' Response to Court's Order to Show Cause, ECF No. 161 | T. Michael Morgan (signer) | 2025-02-10 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.161.0.pdf | PDF downloaded 2026-10-27, pdftotext, read in full; quote checked |
| Declaration of T. Michael Morgan, ECF No. 167 | T. Michael Morgan | 2025-02-13 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.167.0.pdf | PDF downloaded 2026-10-27, pdftotext, read in full (exhibits not opened); quotes checked |
| Declaration of Rudwin Ayala, ECF No. 168 | Rudwin Ayala | 2025-02-13 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.168.0.pdf | PDF downloaded 2026-10-27, pdftotext, read in full; quotes checked |
| Declaration of Taly Goody, ECF No. 169 | Taly Goody | 2025-02-13 | https://storage.courtlistener.com/recap/gov.uscourts.wyd.64014/gov.uscourts.wyd.64014.169.0_1.pdf | PDF downloaded 2026-10-27, pdftotext, read in full; quotes checked |
| CourtListener docket record, Wadsworth v. Walmart Inc, 2:23-cv-00118 | CourtListener | Filed 2023-07-06; terminated 2025-07-28 | https://www.courtlistener.com/docket/67564066/wadsworth-v-walmart-inc/ | Search API JSON downloaded 2026-10-27; used for filing and termination dates, cause, parties |
| LawNext (LawSites), "Federal Judge Sanctions Morgan & Morgan Attorneys for AI-Generated Fake Cases in Court Filing" | Bob Ambrogi | 2025-02-25 | https://www.lawnext.com/2025/02/federal-judge-sanctions-morgan-morgan-attorneys-for-ai-generated-fake-cases-in-court-filing.html | Raw HTML downloaded 2026-10-27, read as text; cross-check of fines and roles |
| Bloomberg Law, "Morgan & Morgan Lawyers Fined for 'Hallucinated' AI Citations" | Bernie Pazanowski, with assistance from Seamus Hughes | 2025-02-25 | https://news.bloomberglaw.com/litigation/morgan-morgan-lawyers-fined-for-hallucinated-ai-citations | Raw HTML downloaded 2026-10-27, read as text (free portion); cross-check |

Also downloaded and read: AI Incident Database report 4829 (https://incidentdatabase.ai/reports/4829/), a copy of the LawNext article under Incident 960; not used for any fact.

## Corrections

This page needs review. If you have the text of the motion (ECF No. 141), MX2.law's replies, the firm's exhibits, or a filing on how the case ended, tell us and we will update this page.
