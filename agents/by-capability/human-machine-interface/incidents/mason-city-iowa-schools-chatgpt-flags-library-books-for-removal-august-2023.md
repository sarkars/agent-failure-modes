---
title: "An Iowa school district asked ChatGPT which library books described sex acts and pulled the 19 it flagged, August 2023"
date: 2023-08-14
source: "https://www.popsci.com/technology/iowa-chatgpt-book-ban/"
description: "Mason City schools typed book titles into ChatGPT to comply with a new Iowa law. Reporters who asked again got different answers about the same books."
summary: "In August 2023, the Mason City Community School District in Iowa removed 19 books from its grade 7-12 school libraries to comply with Senate File 496, a new state law that bars school library books with descriptions or visual depictions of a sex act. Assistant Superintendent Bridgette Exman told reporters she typed each title from a list of commonly challenged books into ChatGPT with a yes-or-no question taken from the law, and books that got a yes were removed and stored. Popular Science, asking a differently worded question, got a different sorting of the 19 books and contradictory answers about one title. The Des Moines Register reported that when Exman reran one flagged title during a call, ChatGPT did not flag it. No opened source shows the chats themselves. Status: Needs review."
categories:
  - Government
  - Education
  - Accuracy
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - users-must-engineer-prompts-to-get-good-results
---

**This page is a dated teardown of an Iowa school district's use of ChatGPT to decide which library books to remove in August 2023, for teams that build, buy or set rules for a chat assistant whose yes-or-no answers can become an official public decision.** The product was ChatGPT, OpenAI's general chat assistant. The user was a school administrator working against a legal deadline. The moment that matters is a single typed question per book, in the words of the law: does this book describe a sex act? A yes meant the book left the shelf. The answer came with no page, passage or source, and reporters who asked again got different answers. The date above is the first original report we opened (Popular Science, August 14, 2023).

**Status: Needs review.** Five sources were downloaded on 2026-10-28 as raw HTML and read as plain text: Popular Science (Andrew Paul, August 14, 2023), Education Week (Eesha Pendharkar, August 21, 2023), the Des Moines Register as republished on Yahoo News (Samantha Hernandez, with Tim Webber; the page shows "Updated" October 8, 2023 and no first publication date), Fortune (Paige Hagy, August 17, 2023) and Smithsonian Magazine (Sarah Kuta, August 21, 2023; byline from the page's author metadata). Popular Science, Education Week and the Register are original reporting: each spoke with district officials and the first two ran their own ChatGPT queries. Fortune and Smithsonian are mostly secondary. Each quote below was checked word for word against the downloaded text with a script, with curly and straight quote marks treated as the same. The Gazette's August 11, 2023 article, which first reported the removals, was not opened; we quote it only as Popular Science and Smithsonian quote it.

> **Read this first.** This is a summary of public reporting, not legal advice and not a finding of fact. It does not say what Iowa's law requires, whether any book meets its terms, or whether any removal was right or wrong. We did not see the ChatGPT chats, the full list of titles the district checked, or any district record. We name only people who spoke on record or acted in an official role: Assistant Superintendent Bridgette Exman, Superintendent Pat Hamilton, Iowa Department of Education spokesperson Heather Doe, Deborah Caldwell-Stone of the American Library Association, Courtney Pentland of the American Association of School Librarians, and Gov. Kim Reynolds.

**Channel note.** This is a text incident: an administrator typed questions into the ChatGPT web chat and read typed answers. This phase of the knowledge base is chat-first, and the signals and checks below are written for chat logs and the decisions made from them. Voice and web signals, such as an assistant that reads a verdict aloud or a public catalog page updated from a chat answer, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **May 26, 2023: the law.** Gov. Kim Reynolds signed Senate File 496 on May 26, per Education Week, which quotes the law: "'age-appropriate' does not include any material with descriptions or visual depictions of a sex act." Education Week says it took effect July 1 and that consequences would be enforced from January 1, 2024.
- **The district's reason.** Per Popular Science, quoting the Gazette, Exman said it was "simply not feasible to read every book and filter for these new requirements." A district statement, per Fortune, added: "Therefore, we are using what we believe is a defensible process to identify books that should be removed from collections at the start of the 23-24 school year."
- **The list.** Per Popular Science, administrators compiled "a master list of commonly challenged books," then dropped titles challenged for reasons other than sexual content. The Register says the list had 42 titles; Education Week says "about 50" and "almost 50."
- **The question.** Per Popular Science, administrators asked ChatGPT the law's own language: "Does [book] contain a description or depiction of a sex act?" Exman wrote: "If the answer was yes, the book will be removed from circulation and stored." The Register gives her wording as "Does [book] describe a sex act?"
- **The result.** "Nineteen times the system responded with a yes," per the Register. Per Popular Science, quoting the Gazette, flagged books were removed from grade 7-12 libraries and "stored in the Administrative Center." Titles included The Color Purple, The Handmaid's Tale, Beloved and Friday Night Lights.
- **The checks the district describes.** Exman told Popular Science: "I was also able to verify ChatGPT responses with my own knowledge of some of the texts," and that the teacher librarian found "no books on the final list of 19 that were surprising to her." Hamilton told Education Week he cross-checked the 19 against BookLooks.org, a website run by parents who review books. Per the Register, Exman first queried books she had taught, "to make sure the system was flagging the right books."
- **A different question, a different answer.** Popular Science asked, "Do any of the following books or book series contain explicit or sexual scenes?" Of the 19 removed titles, ChatGPT put only four under "Explicit or Sexual Content," six under "Mature Themes but not Necessary Explicit Content," and nine under "Primarily Mature Themes, Little to No Explicit Sexual Content."
- **The same book, two answers.** Per Popular Science, one response said The Kite Runner has "little to no explicit sexual content"; a follow-up said it "does contain a description of a sexual assault."
- **A rerun on the phone.** During a call with the Register, Exman ran The Absolutely True Diary of a Part-Time Indian through ChatGPT and, "unlike in early August, the system did not flag the book as describing a sex scene." The Register wrote: "It got at least one wrong, however." Exman: "It's not a perfect process." She said she would likely reread the book to decide.
- **What the bot said about itself.** When Education Week ran the titles, ChatGPT sometimes added: "If you have concerns about the content, it's recommended to read reviews or consult with educators or parents before deciding if it's appropriate for a particular reader."

## What the organizations said

- **Assistant Superintendent Exman.** "Frankly, we have more important things to do than spend a lot of time trying to figure out how to protect kids from books," and "Our goal here really is a defensible process" (Popular Science). "We used Chat GPT [sic] to help answer that question" (Popular Science). "I'll be really blunt and say we absolutely would not have done this if we weren't required by law to do so" (Register). She also noted: "We already have a system in place that allows parents to request that we reconsider a book" (Register).
- **Superintendent Hamilton.** "We don't want to ban any books, but we have to comply with Iowa state law," and "And we have received no guidance from the state" (Education Week). He said the removals were meant to protect teachers from violating the law.
- **The district, earlier.** "We have searched back 20 years and can't find a single formal challenge to a book by a parent of a student here in the Mason City School District," per Smithsonian, citing the Gazette.
- **Iowa Department of Education.** "As always, each school district is required to create their own policies and procedures for book selection and reconsideration that comply with Iowa law," Heather Doe told Education Week.
- **Librarians' groups.** Caldwell-Stone, to Education Week: "We can't rely on AI as a definitive tool, or maybe even a great tool, until it's better developed," and the district was "using the crudest tools." Pentland, to the Register: "I would recommend that school districts rely on school librarians, who are specifically trained experts, to provide insight into materials selection and review."
- **OpenAI.** No opened source reports a comment from OpenAI.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| How many titles were checked | Register: 42 (its original headline, shown at the foot of the Yahoo copy, says 41). Education Week: "about 50" and "almost 50." Popular Science gives no count. |
| The exact question | Popular Science: "contain a description or depiction of a sex act." Education Week: "contain a description of a sex act." Register: "describe a sex act." No opened source shows the typed chats. |
| How results were checked | Popular Science: Exman's own knowledge of "some of the texts" and the teacher librarian. Education Week: Hamilton's cross-check with BookLooks.org. No source says any of the 19 was read in full before removal. |
| Whether ChatGPT was right | The Register says it got "at least one wrong." Popular Science and Education Week show varying answers but do not judge any book. We do not judge any book either. |
| What happened to the books later | Not reported in any opened source. |

## Where in the flow it broke

Based on the sources above, and only as far as they go.

1. **A legal test turned into a chat prompt.** The law's wording became a yes-or-no question typed once per title.
2. **An answer with nothing to check.** No opened source says ChatGPT quoted a passage or page; the yes or no stood alone.
3. **One run counted as the answer.** Asked again, or asked in other words, ChatGPT gave different verdicts (Popular Science, Register).
4. **The tool's own caution was not part of the process.** Education Week saw ChatGPT advise consulting educators or parents; no source says the district's process acted on such advice.
5. **The yes became the decision.** Flagged books left the shelves; partial checks came from memory, a librarian and a parent review site.
6. **Outsiders found the instability.** Reporters, not the district's process, surfaced the contradictory answers.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on what reporters describe; no opened source shows the chats.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Each verdict was a bare yes or no with no passage cited, and the Register reports it "got at least one wrong." The user could not check an answer without reading the book, which was the work the tool was meant to save.
- [Users must engineer prompts to get good results](../goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md) (`users-must-engineer-prompts-to-get-good-results`). **Partial fit.** Popular Science's differently worded question sorted the same 19 books differently. That entry is about users who cannot get a good answer without prompt skill; here the deeper problem is that answers changed even for the same question.
- [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) (`eligibility-answers-sound-like-decisions`). **Partial fit.** A general chat answer became a public body's decision. That entry is about a public-service bot answering residents; here a public official used a general tool on the agency's side.
- [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`). **Weak fit.** AI output became an official action with light review. That entry is about clinicians signing AI-drafted visit notes.
- [No appeal or human path for denials](../goals/government-service-agents/failures/no-appeal-or-human-path-for-denials.md) (`no-appeal-or-human-path-for-denials`). **Weak fit.** Exman points to an existing reconsideration process, and Hamilton says keeping a book a committee cleared would still risk violating the law; no source says how a removal could be reversed.
- **Considered, not a fit.** [Wrong explanations taught as fact](../goals/education-agents/failures/wrong-explanations-taught-as-fact.md) (`wrong-explanations-taught-as-fact`): about tutors teaching students; no student used the tool here. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): ChatGPT cited no sources at all. [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`): no opened source says whether ChatGPT stated that it could not see the books' text.
- **Possible gaps for a person to judge.** (1) No pattern covers an assistant giving different verdicts to the same question across runs, with nothing in any single reply to show it. (2) No pattern covers a general chat tool used as a bulk yes-or-no classifier for an official decision. These are proposals, not decisions.

## How it differs from close cases

- [Texas A&M-Commerce instructor relies on ChatGPT's claim it wrote student essays (May 2023)](texas-a-m-commerce-chatgpt-falsely-claims-it-wrote-student-essays-may-2023.md): an educator also took ChatGPT's yes as a decision about people; there the question was authorship, here book content under a law.
- [Two federal judges' staff AI drafts docketed (October 2025)](federal-judges-wingate-and-neals-staff-ai-drafts-docketed-error-filled-orders-october-2025.md): a public body's official act also rested on chat output with skipped review; there the output was drafted text, here a verdict.
- [NYC MyCity chatbot gives businesses illegal advice (2024)](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a government bot answering the public; here a government user asked a public bot.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each can be computed from chat logs and a labeled review set; each has a counter-signal.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Run-to-run flip rate | Ask each yes-or-no question 3 or more times in fresh chats; share of items where the verdicts differ | Share of items forced to one answer by fixing the output, which hides real doubt |
| Wording flip rate | Ask the same item in 2 or more phrasings of the same test; share whose verdict changes | Share of phrasings that are not truly the same test |
| Unsupported verdicts | Share of yes-or-no verdicts with no quoted passage or page from the item itself | Share of quoted passages that do not appear in the item |
| Advice-to-consult ignored | Share of chats where the reply advises human review and the logged decision has no review entry | Share of replies that add the advice to every answer, so it means nothing |
| Decisions without a reader | Share of official actions based on a chat verdict with no logged full human review | Time to decision, so the review does not stall all action |

## What a team can change

Our proposals, not the district's or the state's. Each is a pass/fail check on a chat log or a decision record. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **Show the evidence or say you cannot.** Pass: a verdict on a document quotes the passage and page it rests on, or says the assistant has not seen the text. Fail: a bare yes or no about a book it was not given.
2. **Repeat before you rely.** Pass: a yes-or-no used for an official action is run at least twice, and any disagreement is logged and sent to a person. Fail: one run decides.
3. **Keep the tool's own warning in the record.** Pass: when the reply advises human review, the decision log shows that review. Fail: the advice is in the chat and missing from the record.
4. **A person reads before the action.** Pass: each item removed or denied has a named reviewer who checked the cited passage. Fail: removal based on the chat verdict alone.
5. **Keep the chats.** Pass: the prompts and replies behind each decision are saved with it. Fail: no record of what was asked or answered.
6. **Say how to challenge it.** Pass: the public notice says the tool used and how to ask for a review of one item. Fail: "AI software" with no name and no path.

## What we could not verify

- The Gazette's August 11, 2023 article and the district's original statement. Not opened; quoted only through Popular Science, Fortune and Smithsonian.
- The ChatGPT chats, the model version, the full list of titles and the district's records. No opened source shows them.
- Which, if any, of the 19 verdicts were wrong under the law. Only the Register's "at least one wrong" is reported, and we do not judge any book.
- The Register article's first publication date. The Yahoo copy shows only an update date.
- Fortune reports that Insider tested the same question and that ChatGPT "contradicted itself when asked the same question three times." We could not read Insider's test (the downloaded page held no article text), so this is not used as fact.
- Unverified, seen only in search summaries and not used as fact: a PEN America statement criticizing the decision; that some removed books were later returned to shelves after an author's challenge; that the district used Common Sense Media for 13 of the 19 books; and coverage by LGBTQ Nation, the Daily Beast and Book Riot.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.popsci.com/technology/iowa-chatgpt-book-ban/ | Popular Science (Andrew Paul), original reporting and own test | 2023-08-14 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.edweek.org/teaching-learning/an-iowa-district-used-ai-to-figure-out-which-books-to-ban/2023/08 | Education Week (Eesha Pendharkar), original reporting and own test | 2023-08-21 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://news.yahoo.com/iowa-school-official-needed-know-171817437.html | Des Moines Register (Samantha Hernandez; Tim Webber contributed), via Yahoo News | Updated 2023-10-08; first date not shown | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://fortune.com/2023/08/17/mason-city-iowa-schools-ban-books-using-chatgpt-education-dont-say-gay-censorship/ | Fortune (Paige Hagy), mostly secondary | 2023-08-17 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.smithsonianmag.com/smart-news/why-this-school-district-used-ai-to-help-remove-library-books-180982762/ | Smithsonian Magazine (Sarah Kuta), secondary (cites Popular Science and the Gazette) | 2023-08-21 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |

## Corrections

If you have the district's records, the ChatGPT chats, the Gazette's original article, or a later account of what happened to the 19 books, from a source we can open, tell us and we will fix this page.
