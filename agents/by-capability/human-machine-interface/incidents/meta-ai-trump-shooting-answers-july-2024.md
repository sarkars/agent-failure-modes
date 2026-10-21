---
title: "Meta AI Declines or Denies Questions About the July 2024 Trump Shooting"
date: 2024-07-30
source: "https://about.fb.com/news/2024/07/review-of-fact-checking-label-and-meta-ai-responses/"
summary: "In July 2024 Meta AI was reported to give a generic non-answer, and in some cases to say the July 13 shooting at a Trump rally did not happen. Meta's July 30 post says it had set the assistant not to answer and that the wrong denials were hallucinations. Read from Meta's post and four news or aggregator pages."
categories:
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - refusal-with-no-reason-or-next-step
---

**This page is a dated teardown of one public chatbot incident, for teams whose assistant gets questions about breaking news.** It describes what the sources report the assistant said and what Meta said about why. It takes no political side and makes no claim about anyone's intent. Every fact below comes from a page we opened (listed at the end).

**Read this first.** This is design analysis, not legal, political or editorial advice. Whether and how an assistant should answer questions on live political events is a policy decision for your own legal and trust teams.

## What happened (as reported)

- **July 13, 2024.** The shooting at a campaign event in Pennsylvania, per bluewin (published July 31). GIGAZINE says July 14, which it gives in Japan time; we treat the gap as a time-zone difference, not a disagreement we can confirm.
- **July 22, 2024.** Futurism (July 31) cites a Washington Post report of this date on the chatbot's responses. We did not open the Washington Post report.
- **July 30, 2024.** Meta published "Review of Fact-Checking Label and Meta AI Responses," signed by Joel Kaplan, VP Global Policy. The same post covers a separate issue, a fact-check label placed on a photo. This page does not cover the label.
- **July 30-31, 2024.** Coverage followed: The Verge (July 30, per its URL; the page itself could not be fetched), Nieman Lab's link to it (July 31), Futurism, bluewin and GIGAZINE (all July 31 or August 1), and ppc.land (August 1).

## What the assistant did (as reported)

- **Generic reply or silence on the event.** Meta's post says Meta AI had been set to give a generic reply, "rather than" answer questions about the attempt. ppc.land and bluewin say some users reported that it refused to discuss the event.
- **Denial of the event.** Meta's post says that "in a small number of cases" Meta AI "continued to provide incorrect answers," sometimes saying the event did not happen. Futurism and the OECD page describe the assistant as denying the shooting.
- **What we do not have.** We did not open a transcript or screenshot. The exact wording, the prompts, the number of users and the share of answers that were wrong are not in any page we opened.

## What Meta said about the cause

All of this is Meta's statement, as read in its post and as relayed by the outlets. We cannot check it.

- The assistant was set not to answer questions about the attempt and to give a generic reply instead. Meta presents this as the reason some people saw refusals.
- Meta calls the incorrect answers "hallucinations" and says they are "an industry-wide issue." It says chatbots are "not always reliable when it comes to breaking news or returning information in real time."
- Meta says it updated the responses and "should have done this sooner."
- bluewin reports that Meta described the denials as "unfortunate" and not intentional, and that they continued in some cases even after the assistant was given information about the attack. We did not see those words in the Meta post as fetched.

## Where in the flow it broke

The user asked a factual question about a news event that had already happened. Two things went wrong in the conversation, whatever the cause:

1. **A refusal with no stated reason and no pointer.** Per the sources, the generic reply did not say why the assistant would not answer. We have no evidence it pointed to a news site or any other source.
2. **A confident denial.** When the assistant did answer, some answers told users the event had not occurred. The sources show no hedge such as "I may be out of date" and no source link beside those answers.

Both are the same moment seen from two sides: the assistant had no way to say "this is recent, I may not have reliable information, check a news source." A refusal covered the cases it was set to catch. A wrong denial came out of the cases it missed.

## Pattern match

- [Chatbot is confidently wrong and you can't check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) fits the denials. They were stated as fact and, per the sources, offered no way to verify. Meta's own framing (the assistant was unreliable on breaking news) names the condition under which an uncertainty signal was needed.
- [Chatbot says "I can't help with that" and stops](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) fits the generic reply. It says what a good refusal gives: what the bot can't do, why in plain words, and what to do next.
- **Where the match is partial.** We do not know the exact refusal text, so we cannot say whether it gave a reason. We also do not know whether the denials came from the same configuration as the generic reply or from a separate failure. Meta's post describes them as two behaviors, and we cannot see inside.

## What to measure

Proposed checks for a team whose assistant fields news questions. None come from Meta. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Recent-event questions answered with a recency note | Share of answers to questions about events in the last N days that say the information may be incomplete or out of date. N is a starting point, tune on your own data |
| Recent-event questions answered with a source pointer | Share that name or link a news source or the user's next step |
| Denials of a documented event | Count of answers that say a documented event did not happen, found by replaying a list of dated, verifiable events |
| Refusals with a reason and a next step | Share of "can't answer" replies that say why and offer an alternative |
| Time from first public report to changed behavior | Days from the first external report to a deployed fix |

## What a team can change

Proposed rules, each a pass/fail check on a transcript. Status: Not yet run.

1. **Never state that a recent event did not happen unless you have a source that says so.** Check: replay a list of verifiable recent events; no answer says "did not happen."
2. **If you decline, say you are declining, say why in one plain sentence, and point to a place to look.** Check: every decline has all three.
3. **When recency matters, say so.** Check: answers about events inside your freshness window carry a recency note.
4. **Test the decline path and the answer path together.** A rule that blocks a topic can leave a gap where the model still answers wrongly. Check: the replay list covers phrasing that gets past the block.

## What stays unknown

- The exact text the assistant returned, and how many users saw each behavior.
- Why the denials occurred. Meta's explanation is the only one we read, and it is Meta's.
- Whether the denials happened because of the topic setting, despite it, or independent of it.
- What the assistant says today. We did not test it.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://about.fb.com/news/2024/07/review-of-fact-checking-label-and-meta-ai-responses/ | Meta (Joel Kaplan) | 2024-07-30 | Yes, 2026-10-21, via fetch summary |
| https://www.bluewin.ch/en/news/international/metas-chatbot-denies-trump-assassination-attempt-2306563.html | bluewin | 2024-07-31 | Yes, 2026-10-21, via fetch summary |
| https://ppc.land/meta-addresses-ai-missteps-in-handling-trump-assassination-attempt-news/ | ppc.land | 2024-08-01 | Yes, 2026-10-21, via fetch summary |
| https://gigazine.net/gsc_news/en/20240801-meta-ai-trunp-responses-hallucination | GIGAZINE | 2024-08-01 | Yes, 2026-10-21, via fetch summary |
| https://futurism.com/meta-ai-trump-wasnt-shot | Futurism | 2024-07-31 | Yes, 2026-10-21, via fetch summary |
| https://oecd.ai/en/incidents/2024-07-31-4a37 | OECD.AI incidents | 2024-07-31 | Yes, 2026-10-21, via fetch summary |
| https://www.niemanlab.org/reading/meta-blames-hallucinations-after-its-ai-said-trump-rally-shooting-didnt-happen/ | Nieman Lab | 2024-07-31 | Yes, 2026-10-21, via fetch summary (a link to The Verge; no article text) |

All were read through the fetch tool, which returns a summary rather than the raw page. Short quoted phrases are as that tool returned them.

Not opened: The Verge original (fetch refused), Business Insider (HTTP 522), the AOL page carrying a New York Post test (404), the Washington Post report, Reuters and AP (not found in searches), any transcript or screenshot, House committee letters mentioned in a search summary.

## Where sources disagree

- **Date of the shooting.** bluewin says July 13; GIGAZINE says July 14 (Japan time). We use July 13.
- **Mechanism.** ppc.land describes the assistant first giving generic answers, then some incorrect ones. bluewin says that after being given information it still denied the event in some cases. Meta's post as fetched says generic reply, plus a small number of incorrect answers. These are not clearly the same account of the order of events.

## Caveats

- Everything is through fetch summaries, not raw pages, and no Reuters or AP report was reached.
- The date field is Meta's post date, July 30, 2024.

## Corrections

If you have a transcript, Meta's full post text or a better date, tell us and we will fix this page.
