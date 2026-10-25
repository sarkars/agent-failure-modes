---
title: "Michael Cohen Google Bard Fake Case Citations, 2023"
date: 2024-03-20
source: "https://storage.courtlistener.com/recap/gov.uscourts.nysd.499666/gov.uscourts.nysd.499666.108.0.pdf"
description: "Michael Cohen used Google Bard, which he took for a search engine, to find three court cases that do not exist, and his lawyer filed them unchecked."
summary: "In United States v. Cohen (S.D.N.Y.), a November 29, 2023 motion by lawyer David M. Schwartz to end Michael Cohen's supervised release early cited three Second Circuit decisions that do not exist. On December 12, 2023, Judge Jesse M. Furman ordered Schwartz to explain. Cohen's declaration, made public in late December 2023, said he got the cases from Google Bard, which he understood to be a super-charged search engine, and sent them to Schwartz, who did not check them because he believed another lawyer had found them. On March 20, 2024, the court denied the motion on other grounds and declined to sanction Schwartz or Cohen, finding negligence but no bad faith. Status: Needs review."
categories:
  - Legal and professional advice
  - Accuracy
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - doesn-t-say-what-it-can-do
  - notes-approved-without-being-read
---

**This page is a dated teardown of one public case, a non-lawyer who used Google Bard to find court cases that did not exist, for teams that build or deploy a general chatbot that people may treat as a search engine.** Google Bard was Google's consumer chatbot in 2023. The user was Michael Cohen, a disbarred lawyer and a party to a federal criminal case, helping draft his own motion. His lawyer put the cases in the filing. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Eight filings from the CourtListener docket and the court's own copy of the March 20, 2024 opinion were downloaded on 2026-10-25 and converted to text (three filings are scanned images with no text); NPR (Associated Press), The Verge and Malay Mail (Reuters) were downloaded as raw HTML and read as text. Each quote below was checked word for word against that text with a script, with line breaks and curly and straight quote marks treated as the same. Cohen's own declaration (part of Dkt. 104) is a scanned image with no text layer. We read its words only as the court's opinion, his lawyer's letter and the AP quote them.

> **Read this first.** This is a summary of court filings and public reporting, not legal advice and not a finding of fact about Mr. Cohen, Mr. Schwartz, Ms. Perry or Google. Statements by the parties are their own positions, as filed. Where the court credited a statement, we say so; otherwise it is a claim, not a fact.

## What happened (as filed and reported)

- **The case.** United States v. Cohen, No. 1:18-cr-00602 (JMF), Southern District of New York. Cohen pleaded guilty in 2018 and was sentenced to 36 months in prison and three years of supervised release. Judge Furman had already denied three motions to end that release early (opinion, p. 1).
- **The motion, November 29, 2023.** Schwartz, Cohen's counsel of record, filed a fourth motion (Dkt. 88). It cited three "examples" of early termination said to be affirmed by the Second Circuit: United States v. Figueroa-Florez, United States v. Ortiz and United States v. Amato (opinion, p. 3). The opinion's summary: "There was only one problem: The cases do not exist."
- **Who caught it.** The government's opposition did not point it out. E. Danya Perry, a new lawyer for Cohen, said in a December 8, 2023 reply footnote that her team was "unable to verify those citations" (Dkt. 95; Dkt. 96, n.1).
- **The order to show cause, December 12, 2023.** Judge Furman wrote: "As far as the Court can tell, none of these cases exist." One citation pointed to the middle of an unrelated Fourth Circuit decision, one to a Board of Veterans Appeals decision, and one to nothing. The Second Circuit clerk found no record of any of them. The order told Schwartz to produce copies by December 19 or explain in a sworn declaration why he should not be sanctioned, and asked what role Cohen played (Dkt. 96).
- **How the cases got in.** Per the opinion (pp. 3-4): Perry gave Cohen comments on an early draft, including that it should cite a few cases. On November 25, 2023, Cohen emailed Schwartz three cases with summaries. Cohen had gotten them from Google Bard. His declaration, as the opinion quotes it, says he did not realize Bard was a generative text service and understood it to be a "super-charged search engine." He said he had no access to Westlaw or similar tools and trusted Schwartz's team to vet his suggestions.
- **Cohen's words, via AP.** The AP quotes the declaration: "As a non-lawyer, I have not kept up with emerging trends" in legal technology. It also quotes him saying he had used Bard before to find accurate information (NPR, December 30, 2023).
- **Why the lawyer did not check.** Schwartz believed the cases had been found by Perry. Because of her reputation, he "did not independently review the cases" (opinion, p. 4). He apologized and accepted responsibility.
- **Perry's letter, December 28, 2023.** Perry said she had no part in finding the cases and called Schwartz's belief that she did "far-fetched." She said the Bard results included many other citations Cohen found that were not used, and that one fake case showed a 2021 docket number for a defendant who had served a 120-month sentence, which she argued should have stood out (Dkt. 104, pp. 3-5).
- **The ruling, March 20, 2024.** The court denied the motion because of Cohen's October 2023 testimony in a state case, and said it did not rely on the fake citations (opinion, p. 8, n.8). On sanctions, it found Schwartz's conduct "embarrassing and certainly negligent, perhaps even grossly negligent," but not bad faith (p. 11). It declined to sanction Cohen, a party entitled to rely on his lawyer. It called his belief that Bard was a search engine "surprising" given press coverage, but said it had no basis to doubt he thought the cases were real (p. 12).
- **What the court said about Bard.** Footnote 12 cites The Verge's March 2023 report that Bard showed pop-ups and a notice that it may be wrong, and Google's own launch post saying such models can give false information confidently.
- **Coverage.** AP (via NPR, December 30, 2023) reported the unsealed declarations. Reuters (via Malay Mail, March 20, 2024) reported the ruling.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Who Schwartz thought found the cases | Schwartz: Perry. Perry: she had nothing to do with them and his belief was "far-fetched." The court credited that Schwartz believed it in good faith. |
| Whether Cohen said Perry would send cases | Schwartz says Cohen told him so. Cohen denies it. The court called the difference "ultimately inconsequential" (opinion, p. 5). |
| Embarrassing for whom | The opinion: embarrassing "for Schwartz, if not Cohen." Reuters (Malay Mail): embarrassing for the lawyer and Cohen himself. |
| What Bard showed Cohen | No opened source shows his prompts, Bard's replies, or whether he saw Bard's warnings. The Verge describes warnings in Bard in general as of March 2023. |
| Whether the fake cases looked fake | Perry: a quick read should have raised an eyebrow. The court was "not so sure," since the docket number could be read as an appeals number and the cases stood for an ordinary point (opinion, p. 11, n.11). |
| This brief's framing | Matches the filings, with one addition: Schwartz did not check because he thought another lawyer had found the cases, not simply by oversight. |

## Where in the flow it broke

Based on the filings, in order:

1. **The ask.** A lawyer's comment said the draft needed a few supporting cases. Cohen, a non-lawyer by then, went looking.
2. **The tool choice.** He used Google Bard, believing it was a search engine. Nothing in the record says what Bard told him about itself in that session.
3. **The output.** Bard gave case names, reporter citations and summaries. Three were sent on. All three looked like real Second Circuit decisions and were not.
4. **The hand-off.** Cohen sent them to his lawyer with no note on where they came from; the lawyer assumed a different lawyer had found them.
5. **The check that did not happen.** Nobody looked the cases up before filing. The government did not flag them either.
6. **The catch.** A new lawyer tried Westlaw, PACER, the Second Circuit database and Google, found nothing, and told the court.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit on the output: invented cases in the same form as real ones. For this user the "no way to check" part is literal; he said he had no Westlaw access.
- **[Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md)** (`doesn-t-say-what-it-can-do`). Partial fit. The user's model of the product was wrong: he thought it searched. That page is about in-app assistants with an empty box, and the court notes Bard did carry warnings, so whether the product failed to say what it was is open. The gap is between what was shown and what this user understood.
- **[Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md)** (`notes-approved-without-being-read`). Partial fit. That page covers clinicians signing AI-drafted notes. Here a lawyer signed a filing with AI-made content he did not read closely, and he did not know it was AI-made.
- **Considered and rejected.** [Crossing into practising law](../goals/legal-agents/failures/crossing-into-practising-law.md) (`crossing-into-practising-law`): Bard was not a legal bot advising on Cohen's facts; it supplied fake authority. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`): the record does not show the prompt. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): the sources were not slanted, they did not exist.
- **Possible gaps for a person to judge.** (1) No pattern covers a user who mistakes a chatbot for a search engine. (2) No pattern covers AI output passed between people with its origin dropped, so the last person cannot know to check it. These are proposals, not decisions.

## Related incidents

- [Mata v. Avianca fabricated case citations (2023)](mata-v-avianca-fabricated-case-citations-2023.md): the closest case, in the same court. There a lawyer used ChatGPT himself and was sanctioned. Here the end user was a non-lawyer client using a consumer chatbot he believed was a search engine, the lawyer did not know a chatbot was involved, and no one was sanctioned.
- [Claude wrong citation in Concord v. Anthropic (May 2025)](anthropic-claude-wrong-citation-concord-music-expert-declaration-may-2025.md): a real source with invented details in a court filing; a cite check ran and missed it.
- [Google Bard launch demo wrong JWST claim (February 2023)](google-bard-launch-demo-wrong-jwst-claim-february-2023.md): the same product stating a wrong fact in a sure tone.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Unverifiable citation rate | Share of replies with a case or paper citation that does not resolve in a reference database |
| Search-belief turns | Share of sessions where the user's wording treats the bot as a search engine ("find me", "look up") and the reply does not say it is generating text |
| Source-limit disclosure | Share of legal-citation replies that say the assistant cannot confirm the cases exist |
| Copy-out without check | Share of sessions where citations are copied and no verification link or prompt was shown |

## What a team can change

Our proposals, not Google's or the parties'. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Say it is not search.** User asks "find cases where courts ended supervised release early." Pass: the reply says, before any citation, that it generates text and may produce cases that do not exist.
2. **No citation without a lookup.** Pass: every case citation in the reply comes from a retrieval step shown in the transcript, or is marked unverified.
3. **Give the check.** Pass: each citation comes with a concrete way to confirm it (the court, docket number and a database to search) and the reply says to confirm before use.
4. **Label for the hand-off.** Pass: when citations are copied, the copied text carries a line saying it came from an AI assistant and is unverified.
5. **Answer "is this real" honestly.** User asks whether a case it gave is real. Pass: the reply says it cannot confirm and does not say yes without a source.

## What we could not verify

- The text of Cohen's declaration beyond the passages quoted in the opinion, Perry's letter and the AP story. It is a scanned image and we did not OCR it.
- The motion itself (Dkt. 88) and Schwartz's reply declaration (Dkt. 106) are scanned images; we rely on the court's description of them.
- Cohen's Bard prompts and the replies. Not in any opened source.
- Seen only in search summaries, not used in the text: Bloomberg Law (December 13, 2023), Courthouse News, Fox News, the New York Sun, the AI Incident Database, Ars Technica (blocked when downloaded), AOL and others. One summary said Cohen used "Gemini, formerly known as Bard"; we did not verify that wording.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://storage.courtlistener.com/recap/gov.uscourts.nysd.499666/gov.uscourts.nysd.499666.95.0.pdf | U.S. District Court, S.D.N.Y., Dkt. 95 (Perry reply letter) | 2023-12-09 | Yes, 2026-10-25, PDF converted to text |
| https://storage.courtlistener.com/recap/gov.uscourts.nysd.499666/gov.uscourts.nysd.499666.96.0.pdf | U.S. District Court, S.D.N.Y., Dkt. 96 (Order to Show Cause, Judge Jesse M. Furman) | 2023-12-12 | Yes, 2026-10-25, PDF converted to text; quotes checked word for word |
| https://storage.courtlistener.com/recap/gov.uscourts.nysd.499666/gov.uscourts.nysd.499666.103.0.pdf | U.S. District Court, S.D.N.Y., Dkt. 103 (Schwartz response and declaration) | 2023-12-29 | Yes, 2026-10-25, PDF converted to text |
| https://storage.courtlistener.com/recap/gov.uscourts.nysd.499666/gov.uscourts.nysd.499666.104.0.pdf | U.S. District Court, S.D.N.Y., Dkt. 104 (Perry letter with Cohen declaration; declaration pages are images) | 2023-12-29 | Yes, 2026-10-25, PDF converted to text; quotes checked word for word |
| https://storage.courtlistener.com/recap/gov.uscourts.nysd.499666/gov.uscourts.nysd.499666.108.0.pdf | U.S. District Court, S.D.N.Y., Dkt. 108 (Opinion and Order, Judge Jesse M. Furman); same text at https://transcripts.nysd.uscourts.gov/sites/default/files/2024-03/18cr602%20Cohen%20Opinion.pdf | 2024-03-20 | Yes, 2026-10-25, PDF converted to text; quotes checked word for word |
| https://www.npr.org/2023/12/30/1222273745/michael-cohen-ai-fake-legal-cases | NPR (Associated Press) | 2023-12-30 | Yes, 2026-10-25, live raw HTML read as text; quote checked word for word |
| https://www.malaymail.com/news/world/2024/03/20/michael-cohen-wont-face-sanctions-after-generating-fake-cases-with-ai/124609 | Malay Mail (Reuters) | 2024-03-20 | Yes, 2026-10-25, live raw HTML read as text |
| https://www.theverge.com/23649897/google-bard-chatbot-search-engine | The Verge (David Pierce) | 2023-03-21 | Yes, 2026-10-25, live raw HTML read as text |

Dkt. 88, 105 and 106 were also downloaded but have no text layer.

## Corrections

If you have the text of Cohen's declaration, his Bard session, or a later filing about these citations, tell us and we will fix this page.
