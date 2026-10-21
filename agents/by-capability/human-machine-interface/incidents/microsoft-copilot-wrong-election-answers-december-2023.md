---
title: "Microsoft Copilot (Bing Chat) Gives Wrong Answers About Swiss and German Elections"
date: 2023-12-15
source: "https://algorithmwatch.org/en/microsofts-bing-source-misinformation-elections/"
summary: "In December 2023, AlgorithmWatch and AI Forensics reported that Microsoft's Bing Chat, now Copilot, gave factually wrong answers to election questions ahead of the Swiss and German state elections of autumn 2023. Microsoft said it had improved the tool and fixed some answers; the researchers said little changed. Read from four pages through fetch summaries."
categories:
  - Search
patterns:
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public research report on a search chatbot, for teams that ship an assistant that answers questions about elections, voting or other civic facts.** It describes what the sources report and what Microsoft said as relayed by them. It makes no claim about why the model erred. Every fact below comes from a page we opened (listed at the end), and each was read through a fetch summary only.

**Read this first.** This is design analysis, not safety, legal or election-law advice. Review your own setup with qualified people. The studies did not claim the answers changed any vote.

## What happened (as reported)

- **October 5, 2023.** AlgorithmWatch published early findings from a joint project with AI Forensics and the Swiss broadcasters SRF and RTS. It covered the state elections in Bavaria and Hesse and Swiss votes.
- **Wrong poll figure.** On September 12, Bing Chat said the Freie Wahler party was at 4 percent in the latest Bavarian polls. AlgorithmWatch says forecasts that day ranged from 12 to 17 percent.
- **Wrong candidates.** For Hesse, the top-candidates question was never answered correctly in the tests. The CDU frontrunner was repeatedly named as Volker Bouffier, who the article says had already retired.
- **Invented link to a real story.** Asked about the latest scandal of Hubert Aiwanger, Bing cited a COVID-vaccination flyer. AlgorithmWatch says the real story, public since August 2023, concerned antisemitic statements allegedly made when he was at school.
- **December 15, 2023.** AlgorithmWatch's press release on the final study says nearly 30% of the chatbot's answers contained factual errors, such as false polling numbers, outdated candidates and wrong election dates. The AI Forensics page says one third.
- **Evasion.** The AI Forensics page says the chatbot evaded questions 40% of the time, often on simple election details. The IANS wire story (DT Next, updated December 16, 2023) repeats the one-third and 40 percent figures.
- **Follow-up.** The press release says a follow-up assessment found little progress: the chatbot still made up controversies about candidates and gave wrong information about Swiss candidates and their cantons.

## What Microsoft said

All of this is Microsoft's position as relayed by AlgorithmWatch. We did not open a Microsoft statement, so we cannot check it.

- In the October article: accurate election information is essential, it had improved accuracy, and answers now rest on search results and top-ranked content. It said it corrected some answers cited in the report and offers an "Exact" mode.
- Microsoft encouraged users to click the source links and to rate answers with thumbs up or down.
- The press release says Microsoft Deutschland received a set of failing prompts before the October report, and that Microsoft said it had improved Bing Chat to base answers on top search results.
- AlgorithmWatch replied that Microsoft fixed only the specific answers tested and did not address structural problems. It also said Microsoft's announced election measures fall short.
- The October article says Microsoft did not say whether it sees wrong election answers as a systemic risk under the EU Digital Services Act.

## What the interface did (as reported)

- **Plain answers, not refusals.** In the examples above, Bing Chat gave a specific number, name or story. The summaries do not describe a warning on those answers.
- **Sources were shown but did not guarantee the answer.** The researchers recorded source links and suggested searches. The AI Forensics page says the chatbot attributed false information to credible sources. Microsoft pointed users to those links.
- **Uneven refusals.** The 40% evasion figure means many election questions got no direct answer. The summaries do not say which rule triggered an evasion.
- **Feedback buttons.** Microsoft pointed to thumbs up and down. The sources do not say what happened to that feedback.
- **Fix by example.** Microsoft corrected some cited answers, which AlgorithmWatch calls a fix of the tested cases only.

## Where in the flow it broke

The user asks a plain factual question: who is running, when is the vote, what do the polls say. The break is in the answer. It states a wrong fact in the same form as a right one. The user is then expected to catch it by opening the source links, which the sources say can themselves be misattributed. The October article says some answers were correct but users cannot tell which, so the check falls entirely on the reader. After the researchers reported failing prompts, the reported fix covered those prompts, and the follow-up found similar errors elsewhere.

## Pattern match

Pattern files below were checked with `ls` in this library, and the ID was checked in the failure taxonomy.

- [`confident-wrong-answer-with-no-way-to-check`](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) is the closest page. **The match is partial.** That page is about a wrong answer with no source and no uncertainty cue. Here source links were shown, so the "no source" half does not fit; the sources instead describe links that did not back the claim. The match holds for the lack of any cue telling the user which answers are right. Breaks at: the answer text and the cited source.
- [`one-sided-or-cherry-picked-sources`](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) is adjacent only through source handling. Nothing in the sources says the answers were one-sided. Not a direct match.

## What to measure

Proposed checks for a team that answers election or other civic questions. None come from Microsoft or the researchers. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Factual error rate on a fixed election set | Share of answers to a fixed list of questions (dates, candidates, polls) that a reviewer marks wrong against an official source |
| Source support rate | Of answers that cite a link, share where the linked page actually says what the answer says |
| Fix generalization | After fixing the reported prompts, error rate on a fresh set of similar prompts |
| Evasion rate on simple facts | Share of plain election-date or voting-how-to questions that get no direct answer |

## What a team can change

Proposed rules, each a pass/fail check on a transcript or screen. Status: Not yet run.

1. **Send time-sensitive civic facts to an official source.** Check: a question about an election date or voting method links to the election authority, not a summary.
2. **Do not give poll numbers without a dated, named poll.** Check: any poll figure shows its pollster and date, or the bot declines.
3. **Check that cited pages support the claim.** Check: for a test set, a reviewer opens each link and confirms the claim appears there.
4. **Re-test a family of prompts, not only the reported ones.** Check: after a fix, a paraphrased version of each failing prompt passes; see [`tone-changes-shipped-with-no-regression-test`](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) for the same habit applied to tone.
5. **Show uncertainty when the topic is an election.** Check: answers about candidates or polls carry a visible note that the user should confirm with an official source.

## What stays unknown

- Why the tool gave wrong answers. The sources give no cause, and we offer none.
- The number of questions and conversations. The October article and the press release do not state them. A search summary gave counts, but we could not open the PDF report to confirm them, so we leave them out.
- Who coded the answers and by what rubric. The AI Forensics page says local experts, without naming them or the criteria.
- Why the figures differ: nearly 30% on the press release, one third on the AI Forensics page.
- Whether current Copilot behaves this way. The tests ran on Bing Chat in 2023.
- Microsoft's own wording. We have it only through AlgorithmWatch.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://algorithmwatch.org/en/bing-chat-election-2023/ | AlgorithmWatch | 2023-10-05 | Yes, 2026-10-21, via fetch summary |
| https://algorithmwatch.org/en/microsofts-bing-source-misinformation-elections/ | AlgorithmWatch (press release) | 2023-12-15 | Yes, 2026-10-21, via fetch summary |
| https://aiforensics.org/work/bing-chat-elections | AI Forensics | Listed as 2023-11-12 | Yes, 2026-10-21, via fetch summary |
| https://www.dtnext.in/technology/microsofts-bing-chat-made-up-false-scandals-about-eu-elections-researchers-754865 | DT Next (IANS wire) | Updated 2023-12-16 | Yes, 2026-10-21, via fetch summary |

All four were read through the fetch tool, which returns a summary, not the raw page. Needs review: the full text of each was not seen.

Opened but unusable: the full PDF report (AlgorithmWatch_AIForensics_Bing_Chat_Report.pdf) returned a 404 error. Seen only in search summaries and kept out of the text above: the counts of 867 questions and 5,759 conversations, the language list on the AI Forensics page, a WIRED follow-up about Microsoft's reply on the 2024 US election, and the claim that the study ran from late August to early October.

## Caveats

- The date on the AI Forensics page (November 12) is earlier than the December 15 press release; the summary does not explain it. We use December 15 for the page `date`.
- The October article itself says its results were not final and that a fuller evaluation was planned after the elections.
- The press release has no limitations section and gives no sample size. It says testing was done at scale.
- The researchers say the findings concern Bing Chat as tested, not all AI search tools.
- The headline error rate differs by source (nearly 30% versus one third); we report both.

## Corrections

If you have the full PDF report, Microsoft's own statement, or a better date, tell us and we will fix this page.
