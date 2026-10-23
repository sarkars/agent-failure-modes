---
title: "Google Search AI Overviews Say the Air India Flight 171 Crash Involved an Airbus, Not the Boeing 787, June 2025"
date: 2025-06-12
source: "https://arstechnica.com/ai/2025/06/google-ai-mistakenly-says-fatal-air-india-crash-involved-airbus-instead-of-boeing/"
summary: "On June 12, 2025, the day Air India Flight 171, a Boeing 787-8, crashed after takeoff from Ahmedabad, Ars Technica reported that Google's AI Overviews told at least one searcher the crash involved an Airbus A330. Ars got Boeing, Airbus, or a mix of both on repeat searches. Google said the response was no longer showing."
categories:
  - Search
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - one-sided-or-cherry-picked-sources
  - stakes-blind-register
---

**This page is a dated teardown of one public incident in which an AI search summary named the wrong plane maker in a deadly crash on the day it happened, for teams that let a model write a short answer at the top of search results about breaking news.**

**Status: Needs review.** Built from one original news report, one follow-up news report, a news wire item for the crash facts, and two incident database entries, all opened as raw page text. Not from a test of the feature. Google's statement is quoted as the outlets printed it.

> **Read this first.** This is a summary of public reports, not a finding of fact. It concerns a crash in which, per the news wire item we opened, 260 people died. The aircraft was a Boeing 787-8; nothing here says anything about the cause of the crash, which was still under investigation in the sources we read. Airbus had no part in this flight; we repeat the false answer only as far as needed to show what the feature produced. Nothing here is legal advice. Every fact below comes from a source we opened (listed at the end).

## What happened (as reported)

- **June 12, 2025: the crash.** Air India's Boeing 787-8, flying from Ahmedabad to London Gatwick, crashed into a building soon after takeoff, killing 260 people, including 19 on the ground; one of the 242 people on board survived (Deccan Herald, PTI wire, July 19, 2025). Ars Technica, writing the same day as the crash, said reports put the dead at "more than 200" passengers and crew.
- **The search.** Ars Technica (Ryan Whitwam, June 12, 2025) says a Reddit user, credited in an image caption as /u/stuckintrraffic, saw the error "when searching for crashes involving Airbus planes." Ars does not give the exact query.
- **The answer.** Per Ars, the AI Overview said, "confidently (and incorrectly)," that the plane was an Airbus A330 that went down shortly after takeoff. Ars published a screenshot with the caption that Google's AI "says the crash involved an Airbus A330 instead of a Boeing 787." We did not see the screenshot's full text.
- **It changed between searches.** Ars says it ran "a few similar searches" and that some answers said Boeing, some said Airbus, and some mixed both.
- **The notice.** Ars says a line at the bottom of every AI Overview reads "AI answers may include mistakes," and calls it "not very prominent."
- **Google's response, same day.** Ars says Google told it that it had "manually removed this response." The article is marked "Updated 6/12 with statement from Google." Storyboard18 (June 13, 2025) prints the same statement and says the error was "first flagged by Ars Technica."
- **Database entries.** The AI Incident Database lists it as Incident 1097, incident date 2025-06-12, report count 1 (the Ars article). The OECD AI Incidents Monitor lists it too, with nine further news articles dated June 12 to 14, 2025, including Italian-language outlets, NDTV and Yahoo; we did not open those articles.

## What Google said

The statement, as Ars Technica and Storyboard18 print it, in four parts:

- Google uses "examples like this to update our systems," as with all Search features.
- "This response is no longer showing."
- Google says it maintains a "high quality bar" for Search features.
- Google says the accuracy rate for AI Overviews is "on par with" features like Featured Snippets. Neither outlet says how that rate is measured, and we found no independent check of it.

The statement does not explain why the answer named Airbus, how many people saw it, or whether other wrong versions (the "mashup" answers Ars describes) were also removed.

## Where the sources disagree

- **The death toll.** Ars (June 12) says "more than 200" passengers and crew. Storyboard18 (June 13) says the crash "killed 241 people on board." The PTI wire item (July 19) says 260 died, including 19 on the ground, with one survivor of 242 on board. These fit together as figures that firmed up over time; we use the PTI numbers.
- **Who found it.** Storyboard18 says Ars "first flagged" the error. Ars itself credits a Reddit user. We use Ars's account.
- **The cause.** Ars calls its explanation a "best guess": many crash articles mention Airbus as Boeing's main competitor, and the summary went "down the wrong path." The AI Incident Database description says the error "was traced to" summaries that conflated those Airbus mentions. No source we opened shows Google confirming any cause.
- **How widely it showed.** The OECD entry says the error was "widely displayed to users." That text is marked "[AI generated]" on the OECD page, and no source we opened gives a number, so we do not use it.

## What we could not verify

- **The exact answer text and query.** We did not open the Reddit post or see a full copy of any wrong answer. We rely on Ars's description and image caption.
- **Reach.** No source gives how many people saw a wrong answer, in which countries, or for how long.
- **The fix.** Google says "this response" is no longer showing. No source says whether the Boeing-and-Airbus mashup answers were also removed, or whether Google changed how AI Overviews handle breaking news.
- **Why it happened.** Google has not explained it in any source we opened. The competitor-mention theory is Ars's guess.
- **Any response from Airbus, Boeing or Air India.** None appears in the sources we opened.
- **Search-only claims.** Search summaries mentioned coverage by The Register, NDTV, Cybernews, Free Press Journal, Yahoo and several Italian outlets, and reposts of the Ars article on other sites. We opened none of these articles; we did not find a Register article in four searches. Nothing above relies on them.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All three Pattern IDs below appear in it.

- [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Ars says the answer named the wrong plane maker "confidently," at the top of the page, with only a small general notice. It differs from the pattern page in one way: AI Overviews show links, so a reader could in principle open the source articles. The sources do not say which links were shown or whether any of them said Airbus.
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Weak fit.** If Ars's guess is right, the summary took a side mention (Airbus as Boeing's rival) from source articles and made it the main fact. That is a source-handling failure, but the pattern is about leaving out sources that disagree. We list it because the fix overlaps (show which source each claim rests on); we do not claim it is the same failure.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Partial fit.** The pattern covers calibrating tone and accuracy to the stakes. Here the stakes were a deadly crash on the day it happened, and the feature answered the same way it answers anything else. It is partial because the sources report wrong content, not a wrong tone.
- **Considered, not a fit.**
  - [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md): the reported query asked about Airbus crashes in general. It did not assume Air India's plane was an Airbus; the summary added that.
- **Possible gaps for a person to judge.** (1) No pattern covers an answer engine that gives different facts to the same question on repeat searches. (2) No pattern covers summaries of breaking news, where sources are few, early and changing. These are proposals, not decisions.

## Where in the flow it broke

This reconstruction uses the reports only. Google has not published how this answer was made.

1. **Trigger.** A search about Airbus crashes, hours after a Boeing crash, gets an AI Overview. No source shows a rule that held back summaries on a breaking, deadly event.
2. **Source choice.** Per Ars's guess, the newest, most-linked results were Air India crash articles, many of which mention Airbus only as Boeing's competitor.
3. **Writing.** The summary attaches "Airbus A330" to the crash. Repeat searches give different plane makers, per Ars.
4. **Display.** The answer appears at the top of results with a general "may include mistakes" line, not a claim-level source.
5. **Correction.** A Reddit user notices; Ars reports it; Google says the response is no longer showing, the same day. The sources do not say how long it was live before that.

The reported cost is a false fact about a deadly crash, shown to an unknown number of searchers. No source reports a further harm.

## Related incidents

- [Google AI Overviews odd and unsafe answers, May 2024](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): the same feature, a year earlier. Google's statement then and now both compare accuracy to Featured Snippets.
- [Apple Intelligence notification summaries misreport news headlines, December 2024](apple-intelligence-notification-summaries-misreport-news-headlines-december-2024.md): an AI summary of news told people something false under a trusted label.
- [Google Bard launch demo wrong JWST claim, February 2023](google-bard-launch-demo-wrong-jwst-claim-february-2023.md) and [Google Gemini Super Bowl ad wrong Gouda statistic, February 2025](google-gemini-super-bowl-ad-wrong-gouda-cheese-statistic-february-2025.md): other public Google AI answers that stated a wrong fact plainly.

## What to measure

Proposed metrics; none come from Google or the sources. Status: Not yet run. Thresholds are for the team to set; we propose none.

| Metric | How to compute from logs |
|---|---|
| Entity mismatch rate | Sampled answers whose named company, model or person differs from the one in the top-cited source, divided by all sampled answers |
| Repeat-answer disagreement | For a fixed query run 10 times, the share of runs whose key fact (here, the plane maker) differs from the most common answer |
| Breaking-news answer rate | Answers shown for queries a classifier links to an event less than 48 hours old, divided by all such queries |
| Unsupported key fact | Answers whose key fact appears in no cited source as the subject, only as a side mention, divided by answers checked |
| Time to removal | For answers later marked false, time from first display to removal |

## What a team can change

Proposed rules, each a pass/fail check on a test set or a log sample. Status: Not yet run.

1. **Slow down on fresh disasters.** Pass: for a query tied to a deadly event less than a set number of hours old, the page shows news results and no generated summary, or a summary that only quotes named official sources.
2. **Check the key fact against the source's subject.** Pass: a named maker, model or person in the answer is the subject of at least one cited source, not only a side mention such as "rival to."
3. **Test for stable answers.** Pass: a test set of crash and disaster queries run 10 times each gives the same key fact every time, or gives no summary.
4. **Put the source next to the claim.** Pass: the sentence naming the plane maker shows its source inline, so a reader can see where "Airbus" came from.
5. **Make removal cover variants.** Pass: when one wrong answer is removed, a rerun of close variants of the query (like the "mashup" answers Ars saw) shows none of the same false fact.
6. **Don't over-correct.** Pass: ordinary aircraft queries ("what plane is a 787") still get a summary.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| Ars Technica, "AI Overviews hallucinates that Airbus, not Boeing, involved in fatal Air India crash" | Ryan Whitwam | 2025-06-12, updated 2025-06-12 | https://arstechnica.com/ai/2025/06/google-ai-mistakenly-says-fatal-air-india-crash-involved-airbus-instead-of-boeing/ | Live page returned a human-verification check, not bypassed; read the Internet Archive copy of 2025-12-19 as raw text, fetched 2026-10-24; answer, query, notice, statement and update note checked |
| Storyboard18, "Google's AI Overviews falsely link Airbus to Air India crash; company responds" | Storyboard18 (no byline) | 2025-06-13 | https://www.storyboard18.com/digital/googles-ai-overviews-falsely-link-airbus-to-air-india-crash-company-responds-70236.htm | Raw HTML read as text, fetched 2026-10-24; statement, "241 people on board" and "first flagged" checked |
| Deccan Herald, "Reports on AI plane crash premature, speculative: US probe agency NTSB says it fully supports AAIB probe" | PTI | 2025-07-19 | https://www.deccanherald.com/india/reports-on-ai-plane-crash-premature-speculative-us-probe-agency-ntsb-says-it-fully-supports-aaib-probe-3638457 | Raw HTML read as text, fetched 2026-10-24; aircraft type, route, death toll and survivor count checked |
| AI Incident Database, Incident 1097 | Editor: Daniel Atherton | Incident date 2025-06-12 | https://incidentdatabase.ai/cite/1097/ | Raw HTML read as text, fetched 2026-10-24; description, date and report count checked |
| OECD AI Incidents Monitor, "Google AI Overview Spreads Misinformation About Deadly Air India Crash" | OECD.AI (automated monitor) | Articles dated 2025-06-12 to 2025-06-14 | https://oecd.ai/en/incidents/2025-06-13-eb48 | Raw HTML read as text, fetched 2026-10-24; article list checked; summary text is marked AI generated and not used |

Not opened: the Reddit post, The Register, NDTV, Cybernews, Free Press Journal, Yahoo, the Italian articles listed by OECD, and reposts of the Ars article. These appeared only as search results or links and are not used above.

## Corrections

This page needs review. If you have the original Reddit screenshot, Google's account of how long the answer showed, or a record of other wrong versions, tell us and we will fix this page.
