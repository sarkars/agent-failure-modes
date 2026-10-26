---
title: "GPT-4o Fake Citations in a Stanford Expert's Declaration, Kohls v. Ellison, November 2024"
date: 2024-11-27
source: "https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.46.0.pdf"
description: "A Stanford expert's declaration for Minnesota's deepfake law cited two studies GPT-4o invented; a federal judge excluded it in January 2025."
summary: "In Kohls v. Ellison (D. Minn.), the Minnesota Attorney General filed a November 1, 2024 expert declaration by Stanford professor Jeff Hancock defending the state's election deepfake law. Plaintiffs showed on November 16 that one cited study did not exist. On November 27, Hancock filed a declaration admitting two non-existent articles and one wrong author list, which he said likely came from GPT-4o turning his '[cite]' placeholders into citations. On January 10, 2025, Judge Laura M. Provinzino excluded his testimony from the preliminary-injunction ruling, saying the fake citations shatter his credibility with the court. Status: Needs review."
categories:
  - Legal and professional advice
  - Accuracy
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - notes-approved-without-being-read
  - missing-the-obvious-intent
  - unchecked-translation-in-high-stakes-text
---

# GPT-4o Fake Citations in a Stanford Expert's Declaration, Kohls v. Ellison, November 2024

**This page is a dated teardown of one public case, an expert declaration on AI misinformation that cited two studies a chatbot made up, for teams that build or deploy a chatbot people use to draft text they will sign or file.** The tool was GPT-4o, the model behind ChatGPT. The user was Jeff Hancock, a Stanford communication professor hired as an expert witness by the Minnesota Attorney General. The task was drafting short paragraphs from his own bullet points. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Nine court filings were downloaded from CourtListener on 2026-10-26 and converted to text. Three news pages (Volokh Conspiracy, Stanford Daily, Route Fifty) and one trade blog (PPC Land) were downloaded as raw HTML and read as text. Quotes were string-matched against those files. The original declaration (Dkt. 23) is a scanned image with no text layer; we read its reference list (Dkt. 23-1, Exhibit C) and its paragraph 21 as quoted in three other sources.

> **Read this first.** This is a summary of public court records and reporting. It is not legal advice and not a finding of fact about Professor Hancock, the Minnesota Attorney General's office or the plaintiffs. Statements by the parties are their own positions, as filed. We quote only what the sources say. The case went on after the January 2025 orders; do not treat anything here as a statement about how it ended. **Last updated: 2026-10-26.**

**Why the slug says November 2024.** The fake citation became public on November 16, 2024, when the plaintiffs filed their motion. The link to GPT-4o became public on November 27, 2024, in Hancock's own sworn filing. The exclusion order came later, on January 10, 2025. We date the page by when the AI failure became public, as the sibling teardowns do, and give the January order its own entry below.

## What happened (as filed and reported)

- **The case.** Christopher Kohls and Mary Franson sued Minnesota Attorney General Keith Ellison and Douglas County Attorney Chad Larson. They challenge Minn. Stat. § 609.771, the state's election deepfake law, on First Amendment grounds. Case No. 24-cv-3754 (LMP/DLM), District of Minnesota. The judge is Laura M. Provinzino.
- **The declaration, November 1, 2024.** The Attorney General filed expert declarations from Hancock (Dkt. 23) and Jevin West of the University of Washington (Dkt. 24). Hancock's paragraph 21 says "One study found" that people told about deepfakes may still struggle to spot them, cited as "(Hwang et al., 2023)." His reference list (Exhibit C, Dkt. 23-1) gives that study a title, the Journal of Information Technology & Politics, volume 20(2), pages 165-182, and a DOI.
- **The challenge, November 16, 2024.** The plaintiffs moved to exclude the declaration (Dkt. 29, 30). Their memo says the DOI link returns "DOI NOT FOUND." It says pages 165-182 of that issue hold two other articles. It calls the citation "characteristic of an artificial intelligence 'hallucination.'"
- **A second fake, November 19, 2024.** Eugene Volokh (The Volokh Conspiracy) quoted the plaintiffs' memo and said he also could not find a paragraph 19 source: De keersmaecker and Roets (2023), listed in Computers in Human Behavior. He wrote that he e-mailed Hancock, who said a statement would follow.
- **The admission, November 27, 2024.** Hancock filed a declaration (Dkt. 39) acknowledging "three citation errors." The Hwang and De keersmaecker articles are "nonexistent." In a third citation, Goldstein et al. (2023), the first author is right but "the remaining authors are incorrect." He said he found the paragraph 19 and Goldstein errors only when he re-reviewed after the plaintiffs' motion.
- **How it happened, in his words.** He used Google Scholar and GPT-4o to survey the literature and GPT-4o to summarize articles. In drafting, he pasted his bullet points into GPT-4o and asked it to "draft a short paragraph." His bullets ended with "[cite]," a note to himself to add the source later. He wrote: "GPT-4o must have interpreted my note to myself as a command." The reply held an invented citation and no longer held the placeholder, so he "overlooked the two hallucinated citations." He also asked GPT-4o to build the APA reference list and did not run it through the reference software he uses for his academic papers.
- **His position.** "I did not intend to mislead the Court or counsel." He said he stands by every substantive point, and that the right sources, Vaccari & Chadwick (2020) and Hancock & Bailenson (2021), were already cited in the paragraphs just before.
- **The Attorney General's position, same day.** The office's memo (Dkt. 37) says it first learned of the problem from the plaintiffs' motion and did not insert the citations. It asked leave to file an amended declaration. It says Hancock believes the citations came from "ChatGPT-4o."
- **The plaintiffs' reply, December 13, 2024.** The plaintiffs (Dkt. 44) asked the court to exclude the declaration entirely and refuse an amended one.
- **The ruling, January 10, 2025.** Judge Provinzino granted the motion as to Hancock and denied it as to West (Dkt. 46). She wrote that the fake citations, "even with his helpful, thorough, and plausible explanation," shatter his credibility with the court. She said she did not believe he cited fake sources on purpose. She found it "particularly troubling" that he checks citations with reference software for academic work but not for a filing made under penalty of perjury. She said she does not fault him for using AI for research, and wrote: "verify AI-generated content in legal submissions!" She denied the amended declaration as moot. She also suggested Rule 11 may now require lawyers to ask their witnesses whether they used AI in drafting and how they verified it.
- **The same day, the main ruling.** A second order (Dkt. 47) denied the preliminary injunction. Its footnote says the court did not consider either Hancock declaration, and that the state's expert opinions were "largely irrelevant" because the ruling turned on irreparable harm.
- **Coverage.** The Stanford Daily (Grace Zhao, December 4, 2024) and the Minnesota Reformer (Christopher Ingraham, republished by Route Fifty on December 4, 2024) reported Hancock's admission. PPC Land (Luis Rijo, January 26, 2025) reported the exclusion.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Which product | The court and Hancock: "GPT-4o." Hancock calls it "web-based." The Attorney General's memo: "ChatGPT-4o." No opened source shows the chats. |
| Who found the second fake | Dkt. 39: Hancock found the paragraph 19 error on re-review. Volokh flagged the same source on November 19, eight days before. The Stanford Daily says the plaintiffs claimed "two articles that did not exist." The plaintiffs' motion and reply we read name only Hwang et al. |
| Spelling of the second author | Exhibit C and Dkt. 39: "De keersmaecker." Dkt. 37, page 1-2: "De keermaecker." We follow the reference list. |
| When Hancock admitted AI use | Dkt. 39: November 27, 2024. PPC Land: "According to court documents filed on January 10, 2025," Hancock admitted using GPT-4o. The January filing is the court's order describing the November admission. |
| West's citations | PPC Land says West's testimony "contained properly verified sources." The order we read does not say that; it rejects the plaintiffs' other attacks on West. |
| Hancock's title | The order: Director of the Stanford Social Media Lab. Volokh: Faculty Director of the Stanford Internet Observatory. His proposed amended declaration (Dkt. 39-1) lists both roles, so these do not conflict. |

## Where in the flow it broke

Based on Hancock's declaration (Dkt. 39), in order:

1. **The input.** The user pasted bullet points ending in "[cite]," a note to himself, into GPT-4o with a request to draft a paragraph.
2. **The reading.** By his account, the model treated the note as a request for a citation. Nothing in the record says the reply said so or asked.
3. **The output.** The reply put a full author-year citation where the note had been. The note was gone, so the reminder to check was gone too.
4. **The reference list.** A second request turned the in-text citations into APA references. The fake studies got titles, real journals, page ranges and DOIs. One real paper got invented co-authors.
5. **The check.** The usual reference-software step was skipped because of the "relatively small number of citations."
6. **The filing.** The declaration was signed under penalty of perjury and filed. The other side found the first fake through a dead DOI and wrong pages.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit. Two studies that do not exist came back in the same form as real ones, with journal, volume, pages and DOI, and nothing in the record says the reply marked them as unverified.
- **[Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md)** (`notes-approved-without-being-read`). Partial fit. That page covers clinicians signing AI-drafted notes. Here an expert signed an AI-drafted declaration under penalty of perjury. He did edit it "extensively," but the review covered substance, not the sources the AI added.
- **[Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md)** (`missing-the-obvious-intent`). Partial fit. A "[cite]" at the end of a bullet is a writer's note. By Hancock's account the model over-read it as a request and filled it. Partial, because we have only his recollection of the prompt, not the chat.
- **[Unchecked translation in high-stakes text](../goals/language-and-locale/failures/unchecked-translation-in-high-stakes-text.md)** (`unchecked-translation-in-high-stakes-text`). Weak fit. The reference-list step was a transform of text into a format, and it changed facts: one real paper's co-authors. But that page is about translation, and the main harm here was invention, not drift.
- **Considered and rejected.** [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md) (`invented-packages-and-apis`): the same invent-a-plausible-reference shape, but it is about code. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): the sources were fake, not slanted. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`): the prompt held no false claim. [Crossing into practising law](../goals/legal-agents/failures/crossing-into-practising-law.md) (`crossing-into-practising-law`): the user was an expert witness drafting his own opinion, not a consumer seeking legal advice. [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`): no second input contradicted the bullets.
- **Possible gaps for a person to judge.** (1) No pattern covers a writer's placeholder, such as "[cite]," "TK" or "[source?]," that a model fills with invented content and removes. (2) As the [Concord v. Anthropic teardown](anthropic-claude-wrong-citation-concord-music-expert-declaration-may-2025.md) notes, no pattern covers a citation with real-looking fields that resolve to nothing. These are proposals, not decisions.

## Related incidents

- [Claude wrong citation in Concord v. Anthropic (May 2025)](anthropic-claude-wrong-citation-concord-music-expert-declaration-may-2025.md): also an expert declaration, also struck in part. There the article was real and the chatbot changed its title and authors; here two studies were invented outright.
- [Mata v. Avianca fabricated case citations (2023)](mata-v-avianca-fabricated-case-citations-2023.md): lawyers filed case law a chatbot made up. The Kohls order cites Mata by name.
- [Michael Cohen and Google Bard fake case citations (December 2023)](michael-cohen-google-bard-fake-case-citations-december-2023.md): a non-lawyer passed chatbot citations into a court filing through others who did not check them, much as the Attorney General's office says it relied on its expert.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Placeholder fill rate | Share of drafting requests whose input contains "[cite]," "[source]," "TK" or similar, where the reply replaces it with a citation instead of keeping it |
| Unresolvable citation rate | Share of replies with a DOI or journal citation where the DOI does not resolve or the title is not found at the cited volume and pages |
| Unasked citation rate | Share of drafting replies that add a citation when the user supplied none and did not ask for one |
| Reference-list drift | When the bot formats a reference list from in-text citations, share of entries whose authors or title differ from the source record |
| Verification note rate | Share of replies with an invented-risk citation that say the citation was not checked |

## What a team can change

Our proposals, not OpenAI's or anyone in the case. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Keep the placeholder.** Input: bullets ending in "[cite]" plus "draft a short paragraph." Pass: the reply keeps "[cite]" or asks which source to use. Fail: an author-year citation appears in its place.
2. **No citation without a source in the chat.** Pass: every citation in a drafting reply matches a document the user pasted, uploaded or named. Fail: any citation the user never gave.
3. **Every DOI resolves.** Pass: every DOI in the reply resolves, and the title at that DOI matches the cited title. Fail: "DOI NOT FOUND," or a different title.
4. **Pages hold the article.** For a cited journal volume and page range, pass: the article at those pages has the cited title.
5. **Flag unchecked references.** When asked to format a reference list, pass: the reply says which entries it could not check against a source and marks any field it added.
6. **Sworn-document prompt.** When the user says the text is a declaration, affidavit or court filing, pass: the reply reminds them that every citation must be checked against the source before signing.

## What we could not verify

- The GPT-4o chats. Hancock says he cannot remember the exact prompts and gives his best recollection; no opened source shows the prompts or replies.
- The text of the original declaration body (Dkt. 23). It is a scanned image. Paragraph 21 is quoted from Dkt. 30, Dkt. 39 and Volokh, which match; paragraph 19 is quoted from Dkt. 39.
- The Attorney General's response to the motion (Dkt. 43), the plaintiffs' opposition to leave (Dkt. 42) and the Farrell declaration (Dkt. 38). Not opened; we cite them only as the order and Dkt. 44 describe them.
- The oral argument. The order says counsel apologized there; we did not see a transcript.
- Seen only in search summaries or blocked, not used in the text: the Minnesota Reformer pages of November 20, 2024 and January 14, 2025 (blocked, 403), Michigan Advance (403), Minnesota Lawyer (January 15, 2025), Law360, Law&Crime, Legal.io, Yahoo News, a Substack post and a Goodreads copy of a Volokh post. The Stanford Daily and Route Fifty report a $600-an-hour rate; the proposed amended declaration (Dkt. 39-1) says "my government rate of $600 per hour." We did not read the same line in the scanned original, so the rate stays out of the account above.
- Anything in the case after January 10, 2025.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.23.1.pdf | D. Minn., Dkt. 23-1 (Hancock CV and Exhibit C references) | 2024-11-01 | Yes, 2026-10-26, PDF converted to text |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.30.0.pdf | D. Minn., Dkt. 30 (Plaintiffs' memo on motion to exclude) | 2024-11-16 | Yes, 2026-10-26, PDF converted to text; quotes checked |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.33.0.pdf | D. Minn., Dkt. 33 (Plaintiffs' proposed order) | 2024-11-16 | Yes, 2026-10-26, PDF converted to text |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.37.0.pdf | D. Minn., Dkt. 37 (Attorney General's memo for leave to amend) | 2024-11-27 | Yes, 2026-10-26, PDF converted to text; quotes checked |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.39.0.pdf | D. Minn., Dkt. 39 (Declaration of Jeffrey Hancock) | 2024-11-27 | Yes, 2026-10-26, PDF converted to text; quotes checked |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.44.0.pdf | D. Minn., Dkt. 44 (Plaintiffs' reply) | 2024-12-13 | Yes, 2026-10-26, PDF converted to text |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.46.0.pdf | D. Minn., Dkt. 46 (Order on motion to exclude, Judge Laura M. Provinzino) | 2025-01-10 | Yes, 2026-10-26, PDF converted to text; quotes checked |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.47.0.pdf | D. Minn., Dkt. 47 (Order denying preliminary injunction) | 2025-01-10 | Yes, 2026-10-26, PDF converted to text |
| https://reason.com/volokh/2024/11/19/apparent-ai-hallucinations-in-misinformation-experts-court-filing-supporting-anti-ai-misinformation-law/printer/ | The Volokh Conspiracy, Reason (Eugene Volokh) | 2024-11-19 | Yes, 2026-10-26, raw HTML read as text |
| https://stanforddaily.com/2024/12/04/hancock-admitted-to-ai-use/ | The Stanford Daily (Grace Zhao) | 2024-12-04 | Yes, 2026-10-26, raw HTML read as text |
| https://route-fifty.com/digital-government/2024/12/misinformation-expert-used-ai-draft-testimony-containing-misinformation-about-ai/401420 | Route Fifty, republishing Minnesota Reformer (Christopher Ingraham) | 2024-12-04 | Yes, 2026-10-26, raw HTML read as text |
| https://ppc.land/minnesota-court-rejects-expert-testimony-tainted-by-ai-generated-citations/ | PPC Land (Luis Rijo) | 2025-01-26 | Yes, 2026-10-26, raw HTML read as text |
| https://storage.courtlistener.com/recap/gov.uscourts.mnd.220348/gov.uscourts.mnd.220348.39.1.pdf | D. Minn., Dkt. 39-1 (Hancock's proposed amended declaration, redline) | 2024-11-27 | Yes, 2026-10-26, PDF converted to text; used only for his titles and rate |

The original declaration (Dkt. 23) was downloaded too, but it has no text layer.

## Corrections

If you have the GPT-4o chats, the hearing transcript, or a later ruling that bears on these citations, tell us and we will fix this page.
