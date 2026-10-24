---
title: "Los Angeles Times Insights: an AI 'different views' note softened the 1920s Klan on a column about Anaheim's KKK past, March 2025"
date: 2025-03-03
source: "https://www.latimes.com/california/story/2025-03-03/a-letter-to-readers"
description: "How the LA Times AI Insights feature added a counterpoint that played down the 1920s Klan on a column about Anaheim's KKK recall, and was pulled in a day."
summary: "On March 3, 2025, Los Angeles Times owner Patrick Soon-Shiong launched Voices labels and Insights, an AI feature that adds a political-spectrum label and 'different views on the topic' to some point-of-view pieces, with no editorial review. On Gustavo Arellano's February 25, 2025 column about Anaheim's 1925 recall of four Klan city council members, Insights added bullets saying some accounts frame the 1920s Klan as a cultural reaction rather than a hate-driven movement. TheWrap and The Daily Beast reported on March 4, 2025 that the paper removed Insights from that column. Both said Insights stayed on other Voices pieces; B&T later said the whole tool went offline. Sources disagree on that point."
categories:
  - Accuracy
patterns:
  - one-sided-or-cherry-picked-sources
  - stakes-blind-register
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public incident with the Los Angeles Times' AI "Insights" feature, for teams that attach AI-generated summaries, labels or counterpoints to articles, posts or other content written by people.** Every fact below comes from a source we opened (listed at the end). The paper's own launch letter and the column itself were opened; the removed Insights text is known only from news reports.

**Status: Needs review.** The LA Times letter to readers, Gustavo Arellano's column, TheWrap, The Daily Beast, GIGAZINE and B&T were downloaded as raw HTML and read as text on 2026-10-24. Each quote below was checked word for word against that text. The sources disagree on whether Insights was pulled from one column or from the whole site (see "What we could not verify").

> **Read this first.** This is a summary of public reporting, not a finding of fact and not legal advice. We did not see the Insights output ourselves; the quoted AI text comes from news outlets that saw it before removal. We take no side on the history; we describe what the feature showed and how outlets and the columnist reacted.

## What happened (as reported)

- **The launch.** On March 3, 2025, the LA Times posted a letter to readers from owner Patrick Soon-Shiong. It said point-of-view content "may be labeled Voices," including opinion, news commentary, criticism and reviews. It announced Insights, "an AI-driven feature that will appear on some Voices content."
- **What Insights does, per the paper.** The note under the letter says Insights identifies where a piece's views "may fall on the political spectrum." It offers a summary of the piece's ideas "along with different views on the topic from a variety of sources."
- **No editor in the loop.** The same note says Insights "is not created by the editorial staff." It "makes no judgment on the quality of any piece of journalism." The Daily Beast says each summary carried a disclaimer beginning "The following content is AI-generated and was not created by the editorial staff."
- **The vendors.** Per TheWrap, the political grades came from Particle.news, and Perplexity AI was used to identify a piece's ideas. The Daily Beast calls the perspectives feature one "produced by AI company Perplexity." The live letter page does not name either company today.
- **The column.** On February 25, 2025, Gustavo Arellano wrote that 100 years earlier, on Feb. 3, 1925, Anaheim voters recalled four Klan council members. He called the Klan's rule "a stain" on the city. He said the recall teaches "how to combat tyranny and white supremacy."
- **The AI counterpoint.** TheWrap and The Daily Beast quote an Insights bullet under "different views on the topic." It said some local accounts frame the 1920s Klan as a cultural response "rather than an explicitly hate-driven movement, minimizing its ideological threat."
- **A second bullet.** Per TheWrap, Insights also said critics argue the Klan focus "distracts from Anaheim’s modern identity as a diverse city."
- **Who spotted it.** B&T says New York Times reporter Ryan Mac noticed it. GIGAZINE quotes a social post saying the AI "'well, actually'-ed the KKK."
- **The columnist's reply.** Per B&T, Arellano posted "Um, AI actually got that right." B&T quotes him saying Orange County people have long minimized the 1920s Klan. So the bullet may have described a real local framing; the problem outlets raised was presenting it as one of the "different views."
- **Another output.** B&T says Insights labeled a separate op-ed on AI in historical documentaries as having a "Centre Left point of view."

## What the company did

- **Removed it from the column.** TheWrap (March 4, 2025) says the paper removed Insights from the column "on Tuesday," a day after launch. The Daily Beast says "Within hours of its debut, the feature was removed from the column."
- **Scope of removal.** TheWrap says "Insights remains active on other Voices stories." The Daily Beast and GIGAZINE say the same. B&T (March 7, 2025) says "soon after, the LA Times took the entire tool offline." No opened LA Times page confirms either version.
- **No comment.** TheWrap and The Daily Beast say the paper did not respond to requests for comment. GIGAZINE says the same of its communications team.
- **The paper's error path.** The launch note says "If you see an error, please report it on the Insights page." TheWrap quotes the paper saying reader feedback would bring "better, more accurate results over time."
- **The union.** The Daily Beast quotes the newsroom union saying the tool "risks further eroding confidence in the news." B&T names it as the Media Guild of the West.

## Where in the conversation flow it broke

The "conversation" here is one-way: a reader opens a column, and the page adds AI text under it. Based on the reports, and only as far as they go:

1. **The input.** A column marking a recall of Klan officials, written from a clear point of view.
2. **The task.** Insights was built to find "different views on the topic" for any Voices piece. Per the paper's note, it makes no judgment on viewpoints.
3. **The mix-up.** The model treated a minimizing frame of a hate group as a peer counterpoint. It gave it the same bullet format it gives any rival argument.
4. **No weight.** The bullet said "local historical accounts" without, in any opened report, saying how many, which ones, or what most historians hold.
5. **No stakes check.** The same treatment applied to a tech op-ed and to Klan history. Nothing in the reports shows a rule for topics like hate groups.
6. **No review.** Per the paper, no editor saw the text before readers did. Readers and reporters found it, and removal followed within about a day.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). Strong fit, via its over-correction rule. That page says "Do not invent a controversy" and to give a minority view "its proper weight, not equal space." It also tracks "Invented disagreement" as a counter-metric. Insights was built to always produce a different view, so it gave a minimizing frame equal standing.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). Partial fit. The same "different views" format ran on a Klan history column and a tech op-ed. That page is about tone in service chats, not editorial topics, but its rule (let treatment follow the stakes) maps here.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). Weak fit. The bullet cited unnamed "local historical accounts." No opened report says whether Insights linked its sources, and Arellano said the framing exists, so we cannot call the bullet false.
- **Considered, not a fit.** [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`): the paper did offer an error report path. [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`): there was no approval step at all, by design. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`): no opened source says how Insights was tested. [Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) (`missing-the-obvious-intent`): Insights did what it was asked; the ask was the problem.
- **Possible gaps for a person to judge.** This taxonomy has no pattern for AI text a publisher attaches to someone else's work, where the reader may read it as the outlet's view. It also has none for a feature that must always produce a counterpoint, whatever the topic. A pattern such as "mandatory counterpoint creates false balance" could cover this case and the counterpoint side of [Google Gemini image generation](google-gemini-image-generation-paused-february-2024.md). These are proposals, not decisions.

## Related incidents

- [Apple Intelligence notification summaries misreport news headlines (December 2024)](apple-intelligence-notification-summaries-misreport-news-headlines-december-2024.md): AI text placed on top of a news outlet's work changed what readers took from it.
- [Google Gemini image generation paused (February 2024)](google-gemini-image-generation-paused-february-2024.md): a rule meant to add balance gave wrong results on history.
- [Amazon Alexa different answers for Harris and Trump (September 2024)](amazon-alexa-different-answers-for-harris-and-trump-voting-question-september-2024.md): an assistant's handling of political views drew public charges of bias.
- [xAI Grok white genocide replies (May 2025)](xai-grok-white-genocide-replies-unauthorized-prompt-change-may-2025.md): an AI pushed a fringe racial frame into unrelated answers.
- [Google AI Overviews odd and unsafe answers (May 2024)](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): AI text published above human-written content with no review before readers saw it.

## What to measure

Proposed signals, not results. Status: Not yet run.

- Share of AI counterpoints that minimize a group a reviewer tags as a hate group, sampled from pieces on such topics.
- Share of counterpoints that name no source a reader can open.
- Share of pieces where the tool produced a counterpoint at all, split by topic tag (to see if it ever declines).
- Time from first reader error report to removal of a flagged output.

## What a team can change

Our proposals, not the LA Times'. Each is a pass/fail check on a sample of outputs. Status: Not yet run.

1. **Allow "no counterpoint."** Pass: on a test piece about a recognized hate group's history, the tool either shows no counterpoint or shows only a sourced dispute among historians.
2. **Give weight, not just a view.** Pass: every counterpoint says whether it is a majority, minority or fringe view, with a source.
3. **Name the source.** Pass: no bullet says "some accounts" or "critics argue" without a link a reader can open.
4. **Route sensitive topics to a person.** Pass: outputs on pieces tagged hate groups, violence or race wait for an editor before they go live.
5. **Label it clearly.** Pass: the AI block starts with a plain label that it is AI text, not the author's or editors' view.
6. **Don't over-correct.** Pass: an ordinary review or tech op-ed still gets a counterpoint, with no added warning.

## What we could not verify

- Whether Insights was removed site-wide, and when. TheWrap, The Daily Beast and GIGAZINE say it stayed on other pieces; B&T says the whole tool went offline. No opened LA Times page says.
- The full Insights text on the column. We saw only the bullets quoted in reports.
- Whether Insights showed source links for its "different views." No opened report says.
- Which model produced the bullet. TheWrap and The Daily Beast name Perplexity; neither names a model.
- Who first flagged it. B&T names Ryan Mac; GIGAZINE spells it "Ryan Mack." TheWrap and The Daily Beast say a reporter spotted it first, but the name did not survive in our text copies.
- The union officer's title. The Daily Beast calls Matt Hamilton vice chair; GIGAZINE says vice president.
- Coverage by AsAmNews, KTLA, CTV/AP, The Jakarta Post, Raw Story, SAN, Denver Gazette, the AI Incident Database, Portside and Electoral-Vote, and a Hollywood Reporter interview. Seen only in search results, or opened with no readable article text; not used.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.latimes.com/california/story/2025-03-03/a-letter-to-readers | Los Angeles Times (Patrick Soon-Shiong) | 2025-03-03 (modified 2025-03-07) | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.latimes.com/california/story/2025-02-25/anaheim-ku-klux-klan-council-recall-1925 | Los Angeles Times (Gustavo Arellano) | 2025-02-25 | Yes, 2026-10-24, live raw HTML read as text, plus an Internet Archive copy captured 2025-03-05; quotes checked word for word |
| https://www.thewrap.com/la-times-pulls-ai-tool-for-kkk-gaffe/ | TheWrap (Sean Burch) | 2025-03-04 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.thedailybeast.com/maga-newspaper-owners-ai-bot-defends-kkk/ | The Daily Beast (Corbin Bolies) | 2025-03-04 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://gigazine.net/gsc_news/en/20250305-la-times-ai-insights-kkk | GIGAZINE | 2025-03-05 | Yes, 2026-10-24, live raw HTML read as text; quote checked word for word |
| https://www.bandt.com.au/la-times-ai-tool-pulled-just-one-day-after-it-downplayed-the-kkk/ | B&T (Aimee Edwards) | 2025-03-07 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |

## Corrections

If you have an LA Times statement on when and how widely Insights was pulled, the full removed output, or how Insights chose its "different views," tell us and we will fix this page.
