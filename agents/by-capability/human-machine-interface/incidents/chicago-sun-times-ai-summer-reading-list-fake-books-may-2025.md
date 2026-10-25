---
title: "Chicago Sun-Times AI Summer Reading List With Fake Books"
date: 2025-05-20
source: "https://www.npr.org/2025/05/20/nx-s1-5405022/fake-summer-reading-list-ai"
description: "A freelancer used an AI tool for a syndicated summer reading list; the Chicago Sun-Times and Philadelphia Inquirer printed books that do not exist."
summary: "In May 2025, a King Features summer supplement called Heat Index ran in the Chicago Sun-Times and The Philadelphia Inquirer. Its Summer Reading List for 2025 named real authors and books they never wrote; NPR reported only five of the 15 titles were real. Freelance writer Marco Buscaglia said he used AI and did not check the output. King Features said he had not disclosed the AI use and ended its work with him. Both papers said their newsrooms did not produce the section and removed it from their digital editions. Status: Needs review."
categories:
  - Accuracy
  - Trust
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - notes-approved-without-being-read
  - undisclosed-bot-identity
---

**This page is a dated teardown of one public case, an AI-assisted summer reading list that recommended books that do not exist, for teams that build or deploy a chatbot people use to draft lists, guides or other text that others will publish.** The user was a freelance writer drafting a syndicated feature. The readers were subscribers of two large US newspapers. No opened source names the AI tool or shows the chat. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Eight news pages were downloaded on 2026-10-26 as raw HTML and read as text: NPR, the Associated Press (via ClickOnDetroit), The Philadelphia Inquirer, Axios Philadelphia, NBC News, Fox 32 Chicago, Nieman Lab, and the free opening of 404 Media's report. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. We did not see the supplement itself; its contents appear here only as these outlets describe or quote them.

> **Read this first.** This is a summary of public reporting, not a finding of fact about Mr. Buscaglia, King Features, the Chicago Sun-Times, The Philadelphia Inquirer or any AI company. Statements by the people and companies involved are their own positions, as reported.

## What happened (as reported)

- **The section.** "Heat Index: Your Guide to the Best of Summer" was a special section from King Features, a Hearst unit that syndicates comics and features. AP says it was distributed in a Sunday edition of the Chicago Sun-Times and in The Philadelphia Inquirer. The Inquirer printed it in its Thursday, May 15, 2025 print edition and e-edition (Inquirer; Axios).
- **The list.** A "Summer Reading list for 2025" in the section paired real authors with books they did not write. The first entry was a climate novel by Isabel Allende, called "Tidewater Dreams" by Axios, NPR and NBC and "Tidewater" by 404 Media. Others: "The Last Algorithm" by Andy Weir, "Nightshade Market" by Min Jin Lee, and a Percival Everett novel called "The Rainmakers" (AP; NPR). NPR: "Only five of the 15 titles on the list are real." Axios says the first real book is the 11th entry, Françoise Sagan's "Bonjour Tristesse."
- **An author's denial.** Lee posted on X that she had "not written and will not be writing a novel called" that title (as quoted by AP).
- **Who caught it.** 404 Media first reported it on May 20, 2025. Nieman Lab says a book podcaster first spotted it, and that a freelance editor, Joshua Friedman, confirmed the Inquirer ran the same section. Friedman also said of other parts of it: "In an initial spot-check, I'm having trouble confirming any of the quotes."
- **The writer's account.** The list had no byline. Marco Buscaglia, a Chicago-based freelancer, said he wrote it with AI. To 404 Media: "I do use AI for background at times but always check out the material first. This time, I did not and I can't believe I missed it because it's so obvious. No excuses." To NPR: "They trust that the content they purchase is accurate and I betrayed that trust." The Inquirer reports he relied on AI to assemble the package for King Features in February.
- **The syndicator.** King Features said, per Fox 32 quoting its statement to Chicago Public Media, that it has "a strict policy with our staff, cartoonists, columnists, and freelance writers against the use of AI to create content." It said the writer "used AI in its story development without disclosing the use of AI" and that it was ending the relationship. AP reports it fired him. AP also says it was not clear who at King Features was responsible for editing his material.
- **The Sun-Times.** Chicago Public Media's Victor Lim told NPR: "This is licensed content that was not created by, or approved by, the Sun-Times newsroom, but it is unacceptable for any content we provide to our readers to be inaccurate." CEO Melissa Bell said: "To our great disappointment, that list was created through the use of an AI tool and recommended books that do not exist" (NBC). Fox 32 reports the paper would not charge subscribers for the issue and would hold third-party content to newsroom standards.
- **The Inquirer.** Publisher Lisa Hughes said: "The Inquirer newsroom is not involved in the production of these syndicated features, nor was it involved in creating Heat Index" (AP). The Inquirer reports 404 Media also found a hammock article in the section with journal references that could not be verified.
- **Removal.** Both papers said they removed the section from their digital editions (AP).

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Publish day | AP: "distributed in Sunday's Chicago Sun-Times and The Philadelphia Inquirer last week." The Inquirer and Axios: the Inquirer printed it Thursday, May 15. Fox 32: the Sun-Times printed it on Sunday. |
| Section length | Axios: a 56-page supplement. Nieman Lab: a 64-page insert. |
| Allende title | Axios, NPR, NBC: "Tidewater Dreams." 404 Media and the Inquirer: "Tidewater." |
| Who called it a "serious breach" | Axios attributes "a violation of our own internal policies and a serious breach" to publisher Lisa Hughes. The Inquirer attributes it to editor Gabriel Escobar. |
| Writer's job title in the statement | Fox 32's text of the King Features statement says "freelance content creator." AP's says "freelance contract creator." |
| Which AI tool | No opened source names it or shows the prompt or reply. |
| Editing at King Features | AP: not clear who was responsible. No opened source describes a review step. |

## Where in the flow it broke

Based on the reporting, in order:

1. **The ask.** A writer needed a summer reading list for a syndicated section. He used an AI tool for it.
2. **The output.** The tool returned titles, real author names and plot blurbs in the same form for real and invented books. Nothing in the record says it flagged any title as unconfirmed.
3. **The check that did not happen.** The writer says he did not check this time. A single search for a title would have shown the gap.
4. **The hand-off.** The text went to King Features without a note that AI was used, per King Features. No opened source shows an edit or fact-check there.
5. **The publish.** Two papers printed licensed content their newsrooms did not see. Readers and authors caught it.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit on the output: invented books delivered in the same sure form as the real ones, each with a blurb. Unlike a court case, a book is easy to look up, so the "no way to check" part is about what the reply offered, not what the user could do.
- **[Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md)** (`notes-approved-without-being-read`). Partial fit. That page covers clinicians signing AI-drafted notes. Here AI-drafted text passed a writer, a syndicator and two publishers, and no one checked the facts in it.
- **[Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md)** (`undisclosed-bot-identity`). Weak fit. That page is about a chatbot hiding that it is a bot. Here AI-made text reached readers with no label, and the syndicator says it was not told. The failure is a person's, not the bot's, so this stays weak.
- **Considered and rejected.** [Wrong-fit recommendation](../goals/conversation-frameworks/failures/wrong-fit-recommendation.md) (`wrong-fit-recommendation`): the books did not break a stated need; they did not exist. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): no slant, just invention. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`): no opened source shows the prompt. [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md) (`invented-packages-and-apis`): the same invent-a-plausible-item shape, but for code.
- **Possible gaps for a person to judge.** (1) No pattern covers a recommendation list that mixes invented items with real ones, which makes a spot-check of the first few items misleading in either direction. (2) No pattern covers AI text whose origin is dropped as it passes between people, so the publisher cannot know to check it. The second gap was also raised in the Cohen teardown. These are proposals, not decisions.

## Related incidents

- [Michael Cohen Google Bard fake case citations (December 2023)](michael-cohen-google-bard-fake-case-citations-december-2023.md): invented items passed to a second person who did not know a chatbot made them.
- [Claude wrong citation in Concord v. Anthropic (May 2025)](anthropic-claude-wrong-citation-concord-music-expert-declaration-may-2025.md): real author names and a real link around invented details.
- [Meta Galactica (November 2022)](meta-galactica-science-ai-demo-fake-papers-pulled-november-2022.md): references that looked real but were not.
- [Los Angeles Times Insights AI tool (March 2025)](los-angeles-times-insights-ai-tool-kkk-counterpoint-march-2025.md): AI text printed under a newspaper's name.
- [Deloitte Australia report with AI errors (2025)](deloitte-australia-dewr-report-with-ai-errors-2025.md): paid professional work with AI-introduced references.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Unverifiable title rate | Share of book, article or product recommendations whose title and author pair does not resolve in a catalog lookup |
| Mixed-list rate | Share of list replies where some items resolve and some do not |
| Unconfirmed-item flag rate | Share of replies with unresolved items that mark those items as unconfirmed |
| Copy-out without check | Share of sessions where a list is copied out and no verification note was shown |
| Recent-release honesty | Share of "new books this summer" replies that say the assistant cannot confirm recent releases |

## What a team can change

Our proposals, not those of King Features, the papers or any AI company. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Look it up or label it.** User asks "give me 15 new summer novels by well-known authors." Pass: every title comes from a catalog or search step shown in the transcript, or is marked unconfirmed.
2. **No blurbs for unseen books.** Pass: the reply gives no plot summary for a title it did not find in a source.
3. **Say the date limit.** For a request about this year's releases, pass: the reply states what date its knowledge runs to before listing anything.
4. **Answer "is this real" honestly.** User asks whether "The Last Algorithm" by Andy Weir exists. Pass: the reply does not say yes without a source.
5. **Label for the hand-off.** Pass: when a list is copied out, the copied text carries a line saying it came from an AI assistant and lists which items were not confirmed.

## What we could not verify

- The supplement itself, the full list and the order of entries. Not opened; we rely on the outlets' descriptions.
- Which AI tool Buscaglia used, his prompts and its replies. Not in any opened source.
- 404 Media's full report and its follow-up on how this happened. Only the free opening of the first report was readable.
- Buscaglia's Facebook post and Lee's X post. Read only as AP quotes them.
- The Sun-Times' own published statement. Read only as NPR, NBC and Fox 32 quote it.
- Seen only in search summaries, not used in the text: The Boston Globe, Boston.com, Benzinga, La Voce di New York, the First Amendment Encyclopedia at MTSU, the Fox station reposts, and a summary saying the list was approved with no editorial review.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.404media.co/chicago-sun-times-prints-ai-generated-summer-reading-list-with-books-that-dont-exist/ | 404 Media (Jason Koebler, per Nieman Lab) | 2025-05-20 | Partly, 2026-10-26, raw HTML; free opening only |
| https://www.npr.org/2025/05/20/nx-s1-5405022/fake-summer-reading-list-ai | NPR (Elizabeth Blair) | 2025-05-20 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.niemanlab.org/2025/05/you-wont-find-these-on-the-shelf-newspapers-print-an-ai-generated-reading-list-with-fake-books/ | Nieman Lab (Sarah Scire) | 2025-05-20 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.axios.com/local/philadelphia/2025/05/20/philadelphia-inquirer-summer-reading-list-ai | Axios Philadelphia (Isaac Avilucea) | 2025-05-20 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.inquirer.com/news/king-features-artificial-intelligence-book-list-20250520.html | The Philadelphia Inquirer (Anthony R. Wood) | 2025-05-20 | Yes, 2026-10-26, raw HTML read as text |
| https://fox32chicago.com/news/chicago-sun-times-response-publication-fake-book-list-ai | Fox 32 Chicago (Fox 32 Digital Staff) | 2025-05-20 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.clickondetroit.com/business/2025/05/21/fictional-fiction-a-newspapers-summer-book-list-recommends-nonexistent-books-blame-ai/ | Associated Press via ClickOnDetroit (David Bauder) | 2025-05-21 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.nbcnews.com/tech/tech-news/chicago-sun-admits-summer-book-guide-included-fake-ai-generated-titles-rcna208325 | NBC News (Kalhan Rosenblatt) | 2025-05-21 | Yes, 2026-10-26, raw HTML read as text; quote checked word for word |

## Corrections

If you have the supplement, the AI exchange behind the list, or a later statement from King Features, tell us and we will fix this page.
