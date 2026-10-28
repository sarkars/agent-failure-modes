# AI Made Up Citations and Fake Quotes: How to Check Every Source Before You Publish

<!-- SEO
title: AI Made Up Citations: Check Every Source Before Publishing
description: AI-drafted briefs, reports and articles ship with cases, papers, links and quotes that do not exist; resolve every citation before you publish.
search phrases:
- chatgpt made up citations
- how to check if a citation is real
- ai fake case citations lawyer sanctioned
- chatgpt fake references doi
- verify ai generated sources before publishing
- ai invented quote in article
- how to spot hallucinated references
-->

**Frequency**: Common

## Issue: AI-drafted briefs, reports and articles ship with cases, papers, links and quotes that do not exist; resolve every citation before you publish.

> **Read this first.** This page is design guidance, not legal advice. It states what court orders and studies say only as far as I read them in the sources I opened. Court rules, sanctions and duties differ by court and state. Have a qualified person, such as a lawyer or your court's rules, review any check before you rely on it for a filing.

> **One line:** A writer asks ChatGPT, Claude or another assistant for supporting sources, pastes the answer into a brief, report or post, and publishes a case name, paper, DOI, URL or quotation that nobody opened; the fix is a pre-publish gate that resolves every citation to a real record and matches every quote against the opened source text.

| | |
|---|---|
| **Channel** | Written text: court filings, reports, news articles, blog posts, newsletters. Slides and spoken scripts are PLANNED, not written. |
| **Stakes** | High. Courts have sanctioned lawyers for fake cases; a publisher has run a list of books that do not exist. |
| **Who is affected** | Lawyers, reporters, analysts, students and marketers who publish AI-assisted text; readers, judges and the real people a fake quote is pinned on |
| **Frequency** | Common, in our judgment. Controlled studies find high fabrication rates in generated references (section 4); I found no count of how often fake citations reach print. |
| **Pattern ID** | text-invented-citations |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Unresolved citations at publish: citations and quotes in the final text with no resolved record and no matched source passage. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Newer models invent fewer references in one study (55% vs. 18%, section 4), but any rate above zero still needs a lookup outside the model before publishing. (Our judgment, not tested.) |
| **Also searched as** | fake references from chatgpt · hallucinated case law · ai cited a study that doesn't exist · made up quote ai · check citations before filing |

## 1. In plain words
An AI assistant writes text that looks researched: a case with a reporter cite, a paper with authors and a DOI, a link, a quotation in marks. Some of these were never real. They look exactly like real ones, so a reader who does not open each one cannot tell. The fix is boring and reliable: before anything is published or filed, every citation is looked up and every quote is found word for word in the source.

**How this differs from the closest pages.** [AI agent cites sources that don't exist](../../../../knowledge-retrieval/goals/citation-accuracy/failures/fabricated-citations.md) and [confident fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) cover a retrieval or chat system producing false citations at answer time; this page covers the person or pipeline that publishes AI-assisted text, and the resolve-every-citation check that catches the fakes before the text goes out.

## 2. What it looks like
**Without the fix** (illustrative: a paralegal at a fictional Denver firm drafting a response brief)
```
Paralegal: Find me 10th Circuit cases where an airline's notice of a claim deadline was too vague.
Assistant: Here are three: Harmon v. Frontier Air Lines, 912 F.3d 1104 (10th Cir. 2019),
           which held that "a deadline buried in fine print is no deadline at all"; ...
Paralegal: (pastes all three, with the quote, into the brief)
Partner:   Signs and files. Nobody opened the cases.
(Three weeks later the other side's reply says none of the three cases can be found.)
```
**With the fix**
```
Paralegal: Find me 10th Circuit cases where an airline's notice of a claim deadline was too vague.
Assistant: I suggested 3 cites. Citation check: 0 of 3 resolved in the case database.
           "Harmon v. Frontier Air Lines, 912 F.3d 1104": no case at that volume and page.
           I removed the quote, because I could not find it in any opened opinion.
           Search the database for this issue instead, or paste opinions you have?
Paralegal: (runs a Westlaw search, pastes two real opinions)
Assistant: Both resolve. Quotes copied from the pasted text, with pin cites. Check log saved.
```
The fixed flow looks up each cite, says which ones failed, drops the unmatched quote, and keeps a log a partner can sign off on.

## 3. Why it happens
- **A citation is just more text to the model.** It writes a case name, volume, page and DOI in the right format the same way it writes any sentence, with no lookup behind it unless a tool runs one.
- **The model vouches for itself.** In Mata v. Avianca the lawyer asked ChatGPT "Is Varghese a real case", and the order says ChatGPT responded that it had supplied "real" authorities (section 4). Asking the same model is not a check.
- **The publishing step trusts the draft.** Signing, editing and posting workflows check spelling and style, not whether each source opens. Format looks right, so the citation passes.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Judge P. Kevin Castel wrote that "there is nothing inherently improper about using a reliable artificial intelligence tool for assistance. But existing rules impose a gatekeeping role on attorneys to ensure the accuracy of their filings." | [Mata v. Avianca, Opinion and Order on Sanctions, S.D.N.Y. 22-cv-1461 (PKC), ECF 54, June 22, 2023](https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0.pdf). Opened and read. | **Needs review.** One district court's order under federal Rule 11. Not a rule for other courts. |
| The order says the respondents acknowledged the "Varghese", "Miller", "Petersen", "Shaboon", "Martinez" and "Durden" decisions "were generated by ChatGPT and do not exist," and that the filing contained "fake quotes and citations." | Same order, paragraph 36 and page 1. Opened. | Six fake decisions in one brief; a single incident, not a rate. |
| The court ordered a $5,000 penalty, plus letters to the client and to each judge "falsely identified as the author" of a fake opinion. | Same order, Conclusion, page 34. Opened. | **Needs review.** Sanctions depend on the court and the facts, including conduct after the fakes were questioned. |
| The order says the lawyer asked ChatGPT "Is Varghese a real case" and "Are the other cases you provided fake", and it answered that its authorities were "real". | Same order, paragraph 45. Opened. | Shows self-checking with the same model failed in this case. |
| GPT-3.5 and GPT-4 wrote short papers on 42 topics (636 citations): "55% of the GPT-3.5 citations but just 18% of the GPT-4 citations are fabricated"; 43% and 24% of the real ones had substantive errors. | [Walters & Wilder, Scientific Reports, 2023 (PMC copy)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/). Opened through a fetch tool that quoted the text. | 2023 models, no retrieval, one prompt style. Rates for current tools will differ. Single study. |
| The Chicago Sun-Times ran a syndicated summer book list with titles that do not exist, such as "Tidewater Dreams" credited to Isabel Allende. Its CEO said the section "was inserted into our paper without review from our editorial team." | [NBC News, May 21, 2025](https://www.nbcnews.com/tech/tech-news/chicago-sun-admits-summer-book-guide-included-fake-ai-generated-titles-rcna208325). Opened. | Secondary news report. The article says "several" titles were fake and gives no exact count. |

Other incidents are written up in this library: a [Butler Snow brief with fake cites, July 2025](../../../incidents/butler-snow-chatgpt-fake-case-citations-alabama-prison-defense-johnson-v-dunn-july-2025.md), a [Stanford expert declaration, November 2024](../../../incidents/chatgpt-fake-citations-stanford-expert-declaration-kohls-v-ellison-november-2024.md), and the [Sun-Times list](../../../incidents/chicago-sun-times-ai-summer-reading-list-fake-books-may-2025.md). I did not re-open their sources for this page.

## 5. The fix
**The principle:** Nothing cited ships until it resolves to a real record, and nothing in quotation marks ships until it is found word for word in the opened source.

**Do this**
1. **Extract every citation** from the final text: case cites, DOIs, paper titles with authors, URLs, book titles, and every passage in quotation marks.
2. **Resolve each one in a source of record**, never in the drafting model: case cites in a case database (CourtListener, Westlaw, Lexis), DOIs in Crossref or doi.org, URLs by fetching them, books in a library catalog.
3. **Match the record, not just the format.** The resolved case name, court, year, authors or title must match what the text says. A real DOI that points to a different paper fails.
4. **Match every quote** as an exact string in the opened source text, with a pin cite or page. No match means the quotation marks come off or the sentence goes.
5. **Never ask the drafting model whether its own cite is real.** Its answer is not a check (section 4).
6. **Block publish or filing** while any citation is unresolved, mismatched or unquoted-but-quoted, and list each failure by location in the text.
7. **Save a check log** per document: each citation, where it resolved, who opened it, and when. A human signs the log for court filings.
8. **The assistant reports what failed.** When a check fails, it names the cite and offers to search a source of record; it does not offer a replacement cite from memory.

**Reference design: pre-publish citation gate**
| Item in text | Resolve with | Pass if | Else |
|---|---|---|---|
| Case cite (e.g. 925 F.3d 1339) | [CourtListener citation lookup API](https://wiki.free.law/c/courtlistener/help/api/rest/v4/citation-lookup), or Westlaw/Lexis | Cite resolves and the case name matches | Block; list the cite |
| DOI | [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) `/works/{doi}` | Record exists; title and first author match | Block |
| Paper with no DOI | Crossref search or library database | One record matches title, authors, year | Send to human review |
| URL | HTTP fetch | Page loads and contains the cited claim | Block |
| Quotation | Opened source text | Exact string match, with page or pin cite | Remove the marks or the sentence |
| Statute, regulation | Official code site | Section exists and text matches | Send to human review |

The CourtListener page says its lookup "can be useful as a guardrail to help prevent hallucinated citations." It skips statutes, law journals, "id." and "supra" cites and checks at most 250 citations per request, so those rows go to human review.

**Prompt block (paste into the drafting assistant's instructions)**
```
Never write a citation, DOI, URL, case name or quotation from memory. Cite only sources
I paste or a lookup tool returned in this session, and copy quotes exactly. If you have
no source, write [NEEDS SOURCE: <claim>] and tell me in your reply.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the "conversation" is the writer and the drafting assistant, or the gate reporting)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A cite fails to resolve: the assistant says so, names it, and points to the source of record. |
| Ask one clarifying question | A cite resolves to two possible records, or the writer may have the source on hand: "Do you have the opinion?" |
| Offer choices: 2-4 options plus "Something else", free text open | After a failure: "Search the database", "Paste the source", "Cut the claim", "Something else". |
| Hand off to a person | Court filings, statutes, and any cite the gate cannot check: a named reviewer signs the log. |

**Don't over-correct.** Do not strip real citations because they were found with AI help; the Mata order itself says using a reliable AI tool is not improper. Do not block a paraphrase that carries no quotation marks, and do not flag a real cite only because the database lags behind a new decision; send it to human review instead.

**Hand-off rule.** Any court filing, any cite the gate cannot check by machine (statutes, unpublished orders, paywalled papers), and any quote attributed to a living person goes to a named human reviewer, who opens the source and signs the check log before filing or publishing.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **not yet run**.

| # | Scenario | Maps to rule | Pass if |
|---|---|---|---|
| 1 | Draft cites a case with a real format but no record | 2, 6 | Gate blocks and names the cite |
| 2 | Real DOI attached to the wrong paper title | 3 | Mismatch flagged |
| 3 | Quote that appears nowhere in the opened source | 4 | Marks removed or sentence cut |
| 4 | Writer asks the assistant "is this case real?" | 5, 8 | Assistant runs a lookup or says it cannot vouch; no "yes" from memory |
| 5 | Court filing with all cites resolved | 7, hand-off | Log saved; filing waits for a human sign-off |
| 6 | Real cite found with AI help, paraphrased, no quotes | Don't over-correct | Passes without a flag |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unresolved citations at publish** (primary) | 0 | Gate log: citations and quotes with status not "resolved" in the final version | Any |
| Quote exact-match rate | 100% | Gate log: quotes with a string match in opened source text | Below 100% |
| Documents published with a check log | 100% | Count published documents with a saved log | Below 100% |
| Fakes caught before publish vs. after | All before | Compare gate failures with corrections issued after publish | Any post-publish correction for a fake cite |
| Real citations wrongly blocked (counter-metric) | Under 5% of blocks | Sampled human review of 20 blocked cites per month | Above 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Cite resolves to nothing in the database | Gate log status "not found" | A very new decision or a database gap |
| Resolved record's name differs from the name in the text | Gate log name mismatch | A party name abbreviation or a later caption change |
| Quote has no exact match in the source | Gate log quote status | Text from a different edition or an OCR error |
| URL returns 404 or a different page | Fetch status and page title | Link rot on a real page; check an archive |
| Citations added in the same edit as AI-drafted text, with no lookup event | Document history and tool log | Writer typed real cites from a source they had open |

**Starter rule:** block publishing or filing when any citation in the text does not resolve to a matching record or any quotation has no exact match in its opened source.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-invented-citations
runs: pre_send
reads: [document.text, citations.extracted, lookup.results, source.text, check_log]
trigger: a document with citations or quotations is about to be published or filed
moves: [admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["Search the database", "Paste the source", "Cut the claim", "Something else"]
on_miss: handoff
metric: unresolved citations at publish
counter_metric: real citations wrongly blocked
status: proposed
```

## 8. Related patterns
- [AI agent cites sources that don't exist](../../../../knowledge-retrieval/goals/citation-accuracy/failures/fabricated-citations.md) - the retrieval system invents citations at answer time; this page is the check before publishing.
- [Confident fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) - false facts stated with confidence in general, not only citations.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) - the chat reply gives the user nothing to verify.
- [One-sided or cherry-picked sources](../../research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) - the sources are real but chosen to support one side.
- [Fabricated social proof](./ui-fabricated-social-proof.md) - the same invent-then-ship failure for testimonials and stats on web pages.

## 9. Common questions
### How do I check if a citation from ChatGPT is real?
Look it up outside ChatGPT. Put a DOI into Crossref or doi.org, a case cite into CourtListener, Westlaw or Lexis, and open every URL. Then check that the title, authors or case name match, and find any quote word for word in the source ([section 5](#5-the-fix)).

### Can I just ask the AI if the case is real?
No. In Mata v. Avianca the lawyer asked ChatGPT whether a case was real and, per the court's order, it said its authorities were "real". They were not.

### Do lawyers get sanctioned for AI fake citations?
In Mata v. Avianca a federal court in New York ordered a $5,000 penalty and letters to the judges named on the fake opinions. Outcomes depend on the court and the facts; this is not legal advice ([section 4](#4-why-it-matters)).

### Is a fake reference with a real DOI possible?
Yes, a real DOI can sit next to the wrong title or authors. Rule 3 checks that the resolved record matches the text, not only that the DOI exists.

### Is it wrong to use AI to find sources at all?
No. The Mata order says using a reliable AI tool is not inherently improper. The duty is to open and check what you cite before you publish or file.
