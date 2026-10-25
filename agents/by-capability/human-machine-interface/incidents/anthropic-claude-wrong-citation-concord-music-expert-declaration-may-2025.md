---
title: "Claude Wrong Citation in Concord v. Anthropic Expert Filing"
date: 2025-05-23
source: "https://storage.courtlistener.com/recap/gov.uscourts.cand.431519/gov.uscourts.cand.431519.377.0.pdf"
description: "Anthropic's lawyers asked Claude to format a citation for an expert declaration; it returned a wrong title and authors, and a judge struck the paragraph."
summary: "In Concord Music Group v. Anthropic (N.D. Cal.), an April 30, 2025 declaration by Anthropic data scientist Olivia Chen cited a journal article under a title and authors that did not match the linked article. On May 15, 2025, Latham & Watkins associate Ivana Dukanovic told the court she had asked Claude.ai to format the citation from the correct link, that the returned citation had an inaccurate title and incorrect authors, and that a manual cite check missed it. On May 23, 2025, Magistrate Judge Susan van Keulen called it a plain and simple AI hallucination, struck paragraph 9 of the declaration, and said the issue undermines the declaration's overall credibility. Status: Needs review."
categories:
  - Legal and professional advice
  - Accuracy
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - unchecked-translation-in-high-stakes-text
  - notes-approved-without-being-read
  - conflicting-inputs-resolved-silently
---

**This page is a dated teardown of one public case, a Claude-formatted citation that changed an article's title and authors in a court filing, for teams that build or deploy a chatbot that reformats or cleans up text people will sign or file.** Claude.ai is Anthropic's text chatbot. The user here was a lawyer at Latham & Watkins, the firm defending Anthropic. The task was small: turn a link to a real article into a formatted legal citation. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Seven sources were downloaded on 2026-10-25 and read as text: four court filings from the CourtListener docket (PDFs, converted to text), and TechCrunch, The Register and The Volokh Conspiracy (raw HTML). Each quote below was checked word for word against that text with a script, with line breaks, line numbers and curly and straight quote marks treated as the same. We did not open the May 13, 2025 hearing transcript; hearing words appear only as the publishers' filing quotes them.

> **Read this first.** This is a summary of court filings and public reporting, not legal advice and not a finding of fact about Anthropic, Latham & Watkins, Ms. Chen or the publishers. Statements by the parties are their own positions, as filed. The case was still going on when these filings were made. Do not treat anything here as a statement about how the case ended.

## What happened (as filed and reported)

- **The case.** Music publishers led by Concord Music Group sued Anthropic over song lyrics and Claude. Case No. 5:24-cv-03811-EKL-SVK, Northern District of California, San Jose. The district judge is Eumi K. Lee; discovery went to Magistrate Judge Susan van Keulen.
- **The declaration, April 30, 2025.** Anthropic filed a declaration by Olivia Chen, an Anthropic data scientist, to back its proposed sample size for Claude prompt-output records (Dkt. 341-2). Paragraph 9 says a 25% relative margin of error is "widely accepted by statisticians" for rare events. Footnote 3 supports that. Its first citation names Julien Dutant and Julia Staffel and the title "A Statistician's Guide to Making Sound Inferences from Noisy Data," in volume 78 of The American Statistician (2024), with a link to tandfonline.com.
- **The challenge, May 13, 2025.** At the hearing, the publishers asked the court to examine Ms. Chen and strike her declaration. The court's order says they argued the citation was to "an article that did not exist and whose purported authors had never worked together."
- **The firm's explanation, May 15, 2025.** In a sworn declaration (Dkt. 371), Ivana Dukanovic, a Latham & Watkins associate, said: "I asked Claude.ai to provide a properly formatted legal citation for that source using the link to the correct article." She said the link, publication, volume, page numbers and year were right, but "the returned citation included an inaccurate title and incorrect authors." She added: "Our manual citation check did not catch that error."
- **The real article.** Per the same declaration, the linked article is "Binomial Confidence Intervals for Rare Events: Importance of Defining Margin of Error Relative to Magnitude of Proportion" by Owen McGrath and Kevin Burke. A Latham associate had found it with a Google search.
- **Two more slips from the same step.** The declaration lists other wording errors "introduced in the citations during the formatting process using Claude.ai." Footnote 2's source is titled "Computing Necessary Sample Size," not "Sample Size Estimation." A footnote 3 author is "Windward Environmental LLC," not "Lower Windward Environmental LLC."
- **The review that missed it.** The team "corrected the volume and page numbers in the citation, but did not notice the incorrect title and authors, despite clicking on the link provided in the footnote and reviewing the article."
- **The firm's framing.** "This was an honest citation mistake and not a fabrication of authority." And: "This was an embarrassing and unintentional mistake." The firm said it had added procedures, "including multiple levels of additional review."
- **The publishers' reply, May 16, 2025.** The publishers (Dkt. 373) said Claude ended up "fabricating entirely the authors and title of an article that does not exist." They asked how, if counsel gave Claude the link, "Claude could have completely ignored those details and hallucinated something that does not exist at all." They quoted the judge at the hearing: "there is a world of difference between a missed citation and a hallucination generated by AI, and everyone on this call knows that." They also said the real article gives a 10% to 50% range, not 25% as a settled standard.
- **The ruling, May 23, 2025.** Judge van Keulen's order (Dkt. 377) found the issue serious, "if not quite so grave as it at first appeared." It said: "That is a plain and simple AI hallucination." It also said the article exists, was properly linked and was found by a person, so this was not lawyers handing their judgment to AI. Its "remaining serious concern" was the manual cite check: "It is not clear how such an error" escaped a human check. It noted Judge Lee's standing order requires a certification "that lead trial counsel has personally verified the content's accuracy," and said neither the certification nor the verification had happened. It struck paragraph 9 and said the issue "undermines the overall credibility of Ms. Chen's written declaration."
- **Coverage.** TechCrunch (Maxwell Zeff, May 15, 2025) and The Register (Thomas Claburn, May 15, 2025) reported the firm's declaration the day it was filed. TechCrunch says Bloomberg reported it first. The Volokh Conspiracy (Eugene Volokh, May 26, 2025) printed the order's passage on the citation.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Hallucination or mistake | The firm: "an honest citation mistake." The publishers: a fabricated non-existent article. The court: "a plain and simple AI hallucination," but the underlying article is real and was properly linked. |
| What Claude was given | The firm says it gave Claude "the link to the correct article." No opened source shows the prompt, the reply, or whether Claude opened the page or only saw the URL. |
| Which paragraph the court cited | The order cites "Dkt. 372, ¶ 6" for the cite-check statement. That wording is in the Dukanovic declaration, Dkt. 371, ¶ 6. We read it as a typo; we did not confirm. |
| Whether the source supports 25% | The firm says the article supports Ms. Chen. The publishers say it gives 10% to 50%. The order's later section records the experts' 10% to 50% and 5% to 25% ranges and set about 11.3%. |
| How many citations Claude touched | The court says Claude formatted "at least three citations." The firm's declaration lists errors in footnotes 2 and 3. |
| Sanctions | No opened source reports sanctions over the citation. The order struck one paragraph. |

## Where in the flow it broke

Based on the filings, in order:

1. **The source.** A person found a real article with a Google search. This step was right.
2. **The ask.** The lawyer asked Claude.ai for "a properly formatted legal citation" from the link. To the user, this is a formatting job, not a research job.
3. **The output.** Claude returned a full citation. The link and journal were right; the title and authors belonged to no matching article. Nothing in the record says the reply flagged doubt. The wrong part looked like the right part.
4. **The check.** Reviewers clicked the link, read the article and fixed the volume and pages. They did not compare the title and authors on the page with the footnote.
5. **The filing.** The citation went into a sworn declaration. The other side found it, and the court struck the paragraph it supported.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit on the core: invented title and authors delivered in the same sure form as the real link and volume. The twist is that a way to check did exist, the link, and the reviewers used it but did not compare the right fields.
- **[Unchecked translation in high-stakes text](../goals/language-and-locale/failures/unchecked-translation-in-high-stakes-text.md)** (`unchecked-translation-in-high-stakes-text`). Partial fit. That page is about translation, but the shape is the same: a chatbot transforms text that will be relied on, changes facts in the process, and nobody is told the output is unverified. The formatting step changed a title, two authors and two other names.
- **[Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md)** (`notes-approved-without-being-read`). Partial fit. That page covers clinicians signing AI-drafted notes. Here lawyers and a witness signed off on an AI-formatted footnote. They did read, but the review checked substance and pages, not the fields the AI wrote.
- **[Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md)** (`conflicting-inputs-resolved-silently`). Weak fit. If Claude saw the linked page, its output disagreed with its input and it did not say so. No opened source says what Claude could see, so this stays weak.
- **Considered and rejected.** [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md) (`invented-packages-and-apis`): the same invent-a-plausible-reference shape, but it is about code. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): a person chose the source, not the bot. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`): the request held no false premise. [Crossing into practising law](../goals/legal-agents/failures/crossing-into-practising-law.md) (`crossing-into-practising-law`): the user was a lawyer and the task was formatting, not legal advice to a consumer.
- **Possible gaps for a person to judge.** (1) No pattern covers a format-only or clean-up task that silently changes facts, such as names, titles, numbers or dates, outside translation. (2) No pattern covers a citation whose link is right but whose title and authors are invented, which a check of the link alone will pass. (3) No pattern covers a review step that checks the parts the person wrote but not the parts the AI wrote. These are proposals, not decisions.

## Related incidents

- [Mata v. Avianca fabricated case citations (2023)](mata-v-avianca-fabricated-case-citations-2023.md): lawyers filed citations a chatbot invented outright; here the source was real and only its details were invented.
- [Deloitte Australia report with AI errors (2025)](deloitte-australia-dewr-report-with-ai-errors-2025.md): professional work product with AI-introduced reference errors.
- [Meta Galactica (November 2022)](meta-galactica-science-ai-demo-fake-papers-pulled-november-2022.md): references that looked real but were not.
- [ChatGPT Search misattributes news quotes (November 2024)](chatgpt-search-misattributes-news-quotes-tow-center-study-november-2024.md): a citation that names the wrong source in a sure tone.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Field drift rate | Share of citation-formatting replies where title, authors, year, volume or pages differ from the source metadata |
| Invented-field rate | Share of replies with a title or author that does not appear on the linked page or in its metadata |
| Unseen-source honesty | Share of replies where the bot could not open the link and says so instead of filling fields |
| Flag rate on changed fields | Share of replies that changed a field from the input and marked the change |
| Reviewer catch rate | In a seeded test, share of planted title or author errors that human reviewers catch |

## What a team can change

Our proposals, not Anthropic's or the firm's. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Format, do not fill.** Give a link plus a pasted title and authors. Pass: the reply's title and authors match the input exactly.
2. **Say when the source was not read.** Give only a URL the bot cannot open. Pass: the reply says it could not read the page and leaves title and authors blank or marked as unknown.
3. **Mark every field you supplied.** Pass: any title, author, volume or page the user did not provide is marked as filled in by the assistant.
4. **Show a diff.** When a user pastes a citation to reformat, pass: the reply lists every word that changed besides punctuation and order.
5. **Match the page.** For a source the bot did open, pass: the cited title appears on that page.
6. **Seeded review drill.** Plant a wrong title in one of 20 citations. Pass: the review checklist names title and authors as fields to compare against the source, and the reviewer flags the planted error.

## What we could not verify

- The May 13, 2025 hearing transcript (Dkt. 372). The PDF was not on CourtListener when we tried; hearing words appear only as the publishers quote them.
- The court's May 13 order for a statement (Dkt. 365). Not opened.
- The Claude prompt and reply. Not in any opened source.
- Whether Claude opened the linked page. Not stated in any opened source.
- Seen only in search summaries, not used in the text: Fortune and AOL reports from May 18, 2025; a Law360 Pulse article; two Music Business Worldwide articles (blocked when downloaded); two ChatGPT Is Eating the World posts (rate-limited when downloaded); a Bloomberg report TechCrunch credits; RouteNote; Slashdot; the AI Incident Database entry. The summaries attributed further statements to plaintiffs' counsel Matthew Oppenheim and Latham partner Sy Damle; we did not verify them.
- Anything after the May 23, 2025 order about this citation.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://storage.courtlistener.com/recap/gov.uscourts.cand.431519/gov.uscourts.cand.431519.341.2_2.pdf | U.S. District Court, N.D. Cal., Dkt. 341-2 (Declaration of Olivia Chen) | 2025-04-30 | Yes, 2026-10-25, PDF converted to text |
| https://storage.courtlistener.com/recap/gov.uscourts.cand.431519/gov.uscourts.cand.431519.371.0.pdf | U.S. District Court, N.D. Cal., Dkt. 371 (Declaration of Ivana Dukanovic) | 2025-05-15 | Yes, 2026-10-25, PDF converted to text; quotes checked word for word |
| https://storage.courtlistener.com/recap/gov.uscourts.cand.431519/gov.uscourts.cand.431519.373.0.pdf | U.S. District Court, N.D. Cal., Dkt. 373 (Publishers' response, Oppenheim + Zebrak) | 2025-05-16 | Yes, 2026-10-25, PDF converted to text; quotes checked word for word |
| https://storage.courtlistener.com/recap/gov.uscourts.cand.431519/gov.uscourts.cand.431519.377.0.pdf | U.S. District Court, N.D. Cal., Dkt. 377 (Order on Joint Discovery Submissions, Magistrate Judge Susan van Keulen) | 2025-05-23 | Yes, 2026-10-25, PDF converted to text; quotes checked word for word |
| https://techcrunch.com/2025/05/15/anthropics-lawyer-was-forced-to-apologize-after-claude-hallucinated-a-legal-citation/ | TechCrunch (Maxwell Zeff) | 2025-05-15 | Yes, 2026-10-25, live raw HTML read as text |
| https://www.theregister.com/2025/05/15/anthopics_law_firm_blames_claude_hallucinations/ | The Register (Thomas Claburn) | 2025-05-15 | Yes, 2026-10-25, live raw HTML read as text |
| https://reason.com/volokh/2025/05/26/judge-strikes-part-of-anthropic-claude-ai-experts-declaration-because-of-uncaught-ai-hallucination-in-part-of-citation/printer/ | The Volokh Conspiracy, Reason (Eugene Volokh) | 2025-05-26 | Yes, 2026-10-25, live raw HTML read as text |

## Corrections

If you have the hearing transcript, the Claude exchange itself, or a later filing about this citation, tell us and we will fix this page.
