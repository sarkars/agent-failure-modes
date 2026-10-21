---
title: "Deloitte Australia's Welfare Review for DEWR Had Nonexistent References and a Wrong Court Quote"
date: 2025-10-08
source: "https://www.cyberdaily.au/government/12737-deloitte-to-refund-government-after-using-ai-in-440-000-report"
summary: "A July 2025 Deloitte review for Australia's Department of Employment and Workplace Relations contained invented references and a misattributed court quote. A revised version disclosed use of Azure OpenAI GPT-4o, and Deloitte agreed to repay the final installment. Read through three fetch summaries; Status: Needs review."
categories:
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public incident, for teams that use an LLM to help draft reports that a client or regulator will rely on.** It describes what the sources report and what the parties said. It makes no claim about why the model erred. Every fact below comes from a page we opened (listed at the end), and each was read through a fetch summary only.

**Read this first.** This is design analysis, not legal, audit or financial advice. Review your own process with qualified people. Status: Needs review.

## What happened (as reported)

- **The report.** Deloitte wrote an independent review for the Department of Employment and Workplace Relations (DEWR) on the Targeted Compliance Framework, the welfare penalty system. Cyber Daily says it was first published in July 2025.
- **The value.** The Australian Financial Review (AFR), via the AI Incident Database, and the Greens release both give the contract as $440,000 (the sources do not name the currency; the outlets are Australian).
- **The discovery.** The AFR piece says Chris Rudge, an academic at the University of Sydney, flagged errors in August 2025, and that Deloitte then began an investigation. Cyber Daily says he found more than a dozen fabricated points attributed to his colleagues.
- **Invented references.** AFR reports three nonexistent academic references. Cyber Daily names two: a paper titled *The Rule of Law and Administrative Justice in the Australian Social Security System*, and a 2012 UNSW Law Journal article credited to Carolyn Adams, which it calls fake.
- **The court quote.** Cyber Daily says a quote was attributed to Justice Jennifer Davies in *Deanna Amato v Commonwealth*, with her name misspelled. It says the cited paragraphs 25 and 26 do not exist in the consent orders, and a quote cited to paragraph 30 appears in paragraph 9. AFR calls it a made-up quote from a Federal Court judgment.
- **The fix.** AFR says the revised version removed more than a dozen nonexistent references and footnotes. A corrected version was uploaded quietly before a long weekend in early October 2025.
- **The disclosure.** The revised methodology says a generative AI tool, Azure OpenAI GPT-4o, was used for "traceability and documentation gaps" (AFR). Cyber Daily says the tool chain was licensed by DEWR and hosted on DEWR's Azure tenancy.
- **Context.** AFR says Deloitte Australia has held contracts worth almost $25 million with DEWR since 2021.
- **The refund.** Both articles say Deloitte agreed to repay the final installment; AFR says the amount was not disclosed. The Greens release, dated October 9, 2025, says Finance told a Senate estimates hearing that Deloitte refunded $97,587.

## What the parties said

- **Deloitte** (via Cyber Daily): the mistakes did not affect the findings; the revision made "a small number of corrections to references and footnotes"; it has not confirmed that AI caused the errors; "the matter has been resolved directly with the client."
- **AFR (summary):** an internal Deloitte review attributed the problems to human error and did not conclude that AI misuse caused them.
- **DEWR** (via Cyber Daily): an independent assurance review confirmed some footnotes and references were incorrect. The substance is retained and the recommendations are unchanged.
- **Finance Department** (via the Greens release, a political party's account): it learned of the errors from media reports and called Deloitte's conduct "troubling." The Greens want a full refund and an apology.

## Where in the flow it broke

The reader expected every footnote in an independent review to point to something real. The break sits between drafting and publication: nothing the sources describe caught a reference that could not be found. An outside academic found it after publication. A second break is disclosure. The first version did not mention an AI tool (AFR says the revision "now" states it), so the client could not weigh the risk. The sources do not say what checks Deloitte or DEWR ran before July, or who wrote which parts.

## Pattern match

Pattern files were checked with `Glob` in this library. There is no page for fabricated citations or for undisclosed AI use in deliverables, so we did not invent one.

- [`confident-wrong-answer-with-no-way-to-check`](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) is the closest fit. Fake references looked like real ones, and a reader had to search outside the report to find out. **The match is partial:** that page is about assistants answering users, and here the output went through a consulting firm's report. Breaks at: the footnote and court-quote check before release.

The Mata v. Avianca teardown in this folder uses the same pattern for a similar failure in a court filing.

## What to measure

Proposed checks for a team that lets an LLM touch a deliverable. None come from Deloitte or DEWR. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Unresolved references | Share of citations in a draft that cannot be matched to a real document, author and year |
| Quote mismatches | Share of quotes whose text and paragraph number differ from the cited source |
| Unreviewed AI-touched sections | Sections where AI was used and no named human has checked every citation |
| Time to correct | Days from an outside error report to a corrected, labeled version |

## What a team can change

Proposed rules, each a pass/fail check. Status: Not yet run.

1. **Resolve every citation before release.** Check: each reference has a link, DOI or document ID that a second person opened.
2. **Check quotes against the source text.** Check: quote wording and paragraph number match the primary document.
3. **Disclose AI use in the first version.** Check: the methodology section names the tool and what it did, before delivery.
4. **Log which sections an AI tool touched.** Check: the log exists and every logged section has a named human sign-off.
5. **Label corrections.** Check: a revised report carries a visible change note, not a silent swap.

## What stays unknown

- Whether the model produced the errors. Deloitte has not said so, and AFR relays an internal finding of human error.
- What Deloitte's and DEWR's review steps were before July 2025.
- Whether any amount beyond $97,587 was repaid, and the currency.
- Exact dates of the revised uploads. The sources give no day.
- The exact count of faulty references; the sources say "three" and "more than a dozen" for different things.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.cyberdaily.au/government/12737-deloitte-to-refund-government-after-using-ai-in-440-000-report | Cyber Daily (Daniel Croft) | 2025-10-08 | Yes, 2026-10-21, via fetch summary |
| https://incidentdatabase.ai/reports/6247 | AI Incident Database, summarizing the AFR article by Paul Karp | AFR URL suggests 2025-10-05 | Yes, 2026-10-21, via fetch summary |
| https://greens.org.au/news/media-release/greens-slam-deloittes-unethical-behaviour-and-measly-refund-over-ai-report | Australian Greens (media release) | 2025-10-09 | Yes, 2026-10-21, via fetch summary |

No page was read in full. Not opened: https://yourstory.com/ai-story/deloitte-repay-australia-ai-report-errors (HTTP 403) and the AFR article itself. Seen only in search results and kept out of the text above: City AM, TechRadar, Malay Mail, InnovationAus, Cornell Catherwood Library, and a claim in a search snippet that the review cost about $435,000.

## Caveats

- The sources disagree on the refund. Cyber Daily's summary says Deloitte will refund "$440,000" in part; AFR says the final installment, amount undisclosed; the Greens say $97,587. We carry all three.
- The Greens release is a party's framing. We use it for the figure and Senate hearing facts only.
- The `date` is the Cyber Daily article date, not the July 2025 publication.

- AFR's own text was not opened. Its details reach us only through the AI Incident Database's summary of it.
- The currency is not stated in any opened page.

## Corrections

If you have the original report, DEWR's statement, the AFR article or a better date, tell us and we will fix this page.
