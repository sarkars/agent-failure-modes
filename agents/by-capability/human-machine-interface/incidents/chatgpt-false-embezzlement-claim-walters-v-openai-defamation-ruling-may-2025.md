---
title: "ChatGPT Says a Radio Host Was Accused of Embezzlement; Court Rules for OpenAI in Walters v. OpenAI, May 2025"
date: 2025-05-19
source: "https://reason.com/wp-content/uploads/2025/05/WaltersvOpenAISJOrder.pdf"
summary: "On May 3, 2023, journalist Frederick Riehl asked ChatGPT to summarize a lawsuit complaint, SAF v. Ferguson. After he gave it a link it could not open, ChatGPT said the complaint accused radio host Mark Walters of embezzling from the Second Amendment Foundation. That was false. Walters sued OpenAI for defamation in Georgia state court. On May 19, 2025, Judge Tracie Cason of the Gwinnett County Superior Court granted summary judgment to OpenAI on three independent grounds. Read from the court's order (pages 1-6 and 22 read directly from the scanned PDF, the rest through long quotes in Eugene Volokh's post), plus raw text of Volokh, Eric Goldman, Bloomberg Law and the CourtListener federal docket. Status: Needs review."
categories:
  - Governance
  - General-Purpose Assistants
patterns:
  - silent-attachment-failures
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one US court case about a chatbot stating a false accusation against a real, named person while summarizing a document, for teams building assistants that summarize documents or answer questions about real people.** Every fact below comes from a source we opened (listed at the end).

**Read this first.** This is design analysis, not legal advice. It does not say what the law requires of your product, and it does not predict how another court would rule. It describes only what the opened sources say. The order is a state trial court ruling. Volokh notes the decision largely adopts a proposed order submitted by the prevailing party (OpenAI), which he says is common in some states' courts. **Status: Needs review.**

## What happened (as reported)

From the court's order (pages 1-4), unless another source is named:

- **The people.** Mark Walters is a nationally syndicated radio host. He is the East Coast media spokesperson for the Second Amendment Foundation (SAF). Frederick Riehl is the editor of AmmoLand.com. In 2023 he was on the SAF's board of directors.
- **The lawsuit being summarized.** On May 3, 2023, the SAF sued the Washington State Attorney General in federal court, in a case captioned *SAF v. Ferguson*. Riehl got a press release and a link to a public copy of the complaint.
- **The chat, step by step.** Also on May 3, Riehl asked ChatGPT to summarize the complaint for a possible article.
  1. He pasted sections of the complaint. ChatGPT summarized them accurately.
  2. He gave ChatGPT a link to the complaint and asked it to summarize what was there. ChatGPT said it did "not have access to the internet and cannot read or retrieve any documents."
  3. He gave the same link again. ChatGPT gave "a different, inaccurate summary" that said the complaint alleged embezzlement by an unnamed SAF treasurer and chief financial officer.
  4. He gave the link again and asked if ChatGPT could read it. ChatGPT said "yes." It again described embezzlement claims, and this time named Mark Walters as the accused treasurer and CFO.
  5. Later, asked for news reports on the case, ChatGPT cited a "knowledge cutoff date of September 2021," before the complaint was filed.
- **The correction to the common telling.** ChatGPT did not say Walters embezzled. It said the complaint *accused* him of embezzlement. Walters was not a party to *Ferguson*, and the order says Riehl knew Walters had never been SAF's treasurer or CFO.
- **What the user knew.** Riehl testified that "within about an hour and a half" he had established the output "was not true." He had seen ChatGPT give "flat-out fictional responses" before.
- **Warnings on screen.** The order says an on-screen notice read "ChatGPT may produce inaccurate information about people, places, or facts." The Terms of Use Riehl accepted told users to evaluate output accuracy, "including by using human review of the Output."
- **Reach and harm.** Walters testified he "is not claiming here that [he has] been harmed." He did not ask OpenAI for a correction or retraction. Volokh's summary of the order says Riehl was the only person who saw the statement.
- **Procedure.** The state case number is 23-A-04860-2. CourtListener shows OpenAI removed the case to federal court (N.D. Ga.) on July 14, 2023; that docket closed December 31, 2024. Bloomberg Law says Walters sued in 2023.

## What the court said

The order grants summary judgment "for three independent reasons" (order page 5):

1. **No defamatory meaning.** The court held that "a reasonable reader in Riehl's position" could not have read the output as "actual facts" (page 6). The court said disclaimers weigh in that test, and pointed to ChatGPT's own warnings in the chat, the Terms of Use, and Riehl's quick check against the real complaint. Per Volokh's excerpt, the court also found Riehl did not believe it.
2. **No fault.** Per Volokh's excerpt, Walters offered no evidence of what a reasonable publisher in OpenAI's place would do. OpenAI's expert evidence on its efforts to reduce hallucinations and its warnings went unrebutted. The court rejected the argument that releasing a system known to make mistakes is itself negligent, calling that strict liability. It also found Walters a public figure who showed no "actual malice."
3. **No damages.** Walters could not recover actual, presumed, or punitive damages (page 22).

Bloomberg Law (May 19, 2025) called it what "appears to be the first ever lawsuit alleging a chatbot produced defamatory content." Volokh wrote the ruling is "tied closely to its facts," and could differ with a user who had fewer signs of falsity, wider spread, a private-figure plaintiff, or a company that ignored a reported error.

## How this differs from the noyb complaint

The closest page here is [noyb's complaint over ChatGPT's false murder claim](chatgpt-false-claims-about-a-person-noyb-complaint-march-2025.md). Both involve ChatGPT stating a false crime about a named person. The differences:

- **Forum and law.** Walters was a US defamation suit for damages, decided by a court. noyb filed a GDPR accuracy complaint with Norway's data regulator; no decision is reported there.
- **Who asked.** Here a journalist asked for a document summary and named no one; the model inserted Walters. There, the man asked about himself.
- **Outcome logic.** This ruling turned on what this one reader knew and believed, on fault, and on damages. The GDPR complaint argues accuracy is required regardless of disclaimers. Neither result tells a product team the output was acceptable.

## Where in the flow it broke

1. **Input type changed.** Pasted text worked. A link the model could not fetch did not.
2. **Correct refusal.** The first reply to the link said plainly it could not read documents.
3. **Refusal dropped on repeat.** The same link, sent again, got a confident summary instead of the same refusal.
4. **Invented content.** The summary described claims not in the complaint.
5. **Named a real person.** On the third try, the invented claim named Walters.
6. **False capability claim.** Asked directly if it could read the link, it said "yes."
7. **Caught by the user.** The safeguard that worked was the user, who had the real complaint and checked it.

## Which patterns it illustrates

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Silent attachment failures](../goals/chat-interface/failures/silent-attachment-failures.md) (`silent-attachment-failures`). **Strong fit on mechanism.** The bot answered as if it had read a source it never read. It is not a perfect match because that page is written for uploaded files, not links, and here the bot first said it could not read the source.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** The false summary came in the same tone as the accurate one, with nothing tying it to the document. Partial, because earlier turns did warn about access and the cutoff date, and the user could and did check.
- [Fabricated clinical justification in appeals](../goals/healthcare-agents/failures/fabricated-clinical-justification-in-appeals.md) (`fabricated-clinical-justification-in-appeals`). **Weak fit.** Different domain, but the same fix: every claim in a summary must trace to the source, or be flagged.
- [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`). **Weak fit.** The request assumed the bot could read the link. It corrected that once, then went along with it.
- **Considered, not a fit.** [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md): no handoff to a person happened. `doesn-t-say-what-it-can-do`: the bot did state its limit, then contradicted it. `lazy-completion`: the summary was invented, not partial.
- **Possible gaps for a person to judge.** (1) No pattern covers a bot that states a limit, then drops it when the user repeats the request. (2) As the noyb page also notes, no pattern covers false accusations about a named third party. These are proposals, not decisions.

## What to measure

Our proposals, not OpenAI's. Status: Not yet run. Thresholds are for the team to set.

| Metric | How to compute from logs |
|---|---|
| Unread-source summary rate | Summaries produced when the fetch or file log shows the source was not read, divided by all summary requests |
| Limit reversal on repeat | Conversations where the bot says it cannot read a source, the user resends it, and the bot then summarizes it, divided by conversations with that first refusal |
| Untraceable named-person claims | Statements in a summary that name a person and match no span in the source, divided by all named-person statements |
| Capability self-report accuracy | Answers to "can you read this?" that match the fetch log, divided by all such answers |

## What to change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run.

1. **No summary without a read.** Pass: if the source was not fetched or parsed, the reply says so and contains no summary.
2. **Same input, same limit.** Pass: resending a link the bot cannot open three times gets the same "I can't open this" answer each time.
3. **Answer "can you read it?" from the log.** Pass: the yes or no matches the fetch result for that turn.
4. **Trace every named-person claim.** Pass: each sentence in a summary that names a person or alleges wrongdoing quotes or points to a passage in the source; untraced sentences are removed or marked.
5. **Offer the working path.** Pass: when a link fails, the reply asks the user to paste the text, the path that worked here.
6. **Don't over-correct.** Pass: summaries of pasted or fetched text that name real parties still get answered.

## What is not known / Not verified

- **The full chat transcript.** The order cites it as an exhibit; we did not see it.
- **The state filing date.** Search summaries say June 2023; no opened source gives the exact date.
- **Remand.** Search summaries say the federal case was sent back to state court and that a January 2024 motion to dismiss was denied. We read only the federal docket header.
- **Appeal.** No opened source says whether Walters appealed.
- **Order pages 7-21.** Read only through Volokh's long excerpts, not directly.
- **Which model version** Riehl used. Not stated in what we read beyond the September 2021 cutoff the bot cited.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://reason.com/wp-content/uploads/2025/05/WaltersvOpenAISJOrder.pdf | Gwinnett County Superior Court order (Judge Tracie Cason), hosted by Reason | 2025-05-19 | Yes, 2026-10-23. Scanned PDF; pages 1-6 and 22 read directly from page images; quotes checked against them |
| https://reason.com/volokh/2025/05/19/openai-wins-libel-lawsuit-brought-by-gun-rights-activist-over-hallucinated-embezzlement-claims/ | Volokh Conspiracy (Eugene Volokh) | 2025-05-20 | Yes, 2026-10-23, raw HTML read as text; quotes checked |
| https://blog.ericgoldman.org/archives/2025/05/chatgpt-defeats-defamation-lawsuit-over-hallucination-walters-v-openai.htm | Technology & Marketing Law Blog (Eric Goldman) | 2025-05-27 | Yes, 2026-10-23, raw HTML read as text |
| https://news.bloomberglaw.com/litigation/openai-beats-defamation-lawsuit-over-chatgpt-hallucination | Bloomberg Law (Isaiah Poritz) | 2025-05-19 | Yes, 2026-10-23, raw HTML; only the free opening paragraphs; quote checked |
| https://www.courtlistener.com/docket/67617826/walters-v-openai-llc/ | CourtListener, N.D. Ga. docket 1:23-cv-03122 | 2023-07-14 (filed) | Yes, 2026-10-23, raw HTML; docket header and first entry read |
| https://www.gibsondunn.com/gibson-dunn-wins-significant-victory-for-client-openai-defending-against-defamation-claim-based-on-hallucinated-generative-ai-output/ | Gibson Dunn (OpenAI's counsel) | Not checked | Downloaded (HTTP 200), not read; not used for claims |
| https://arstechnica.com/tech-policy/2023/06/openai-sued-for-defamation-after-chatgpt-fabricated-yet-another-lawsuit/ | Ars Technica | 2023-06 | No; HTTP 405. Not used |
| https://www.courthousenews.com/?s=walters+openai | Courthouse News search | n/a | No; HTTP 403. Not used |

## Corrections

If you have the chat transcript exhibit, the state complaint, or news of an appeal, tell us and we will fix this page.
