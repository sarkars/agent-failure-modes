---
title: "Google's Bard Launch Example Says the Webb Telescope Took the First Exoplanet Pictures"
date: 2023-02-08
source: "https://blog.google/technology/ai/bard-google-ai-search-updates/"
summary: "In February 2023 Google's announcement of its Bard chatbot used an example answer about the James Webb Space Telescope. Press reports say the answer gave a wrong claim, and Alphabet shares fell that week. Read from Google's post and four news and science pages; the reports disagree on the size of the drop."
categories:
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public launch incident, for teams that show an AI assistant's answers in a demo, an ad or a launch post.** Every fact below comes from a page we opened (listed at the end). Where we only have a second-hand account, we say so.

**Note on money.** This page repeats share-price and market-value figures only as the opened sources state them, with the source named. It does not explain why the stock moved. The sources do not tie the move to this error alone, and nothing here is financial advice.

## What happened (as reported)

- **February 6, 2023.** Google published "Introducing Bard," signed by Sundar Pichai (CEO of Google and Alphabet). It describes Bard as an experimental conversational AI service powered by LaMDA, opened first to "trusted testers" with wider release planned "in the coming weeks." The post says Bard can help you "explain new discoveries from NASA's James Webb Space Telescope to a 9-year-old." We did not see the example answer's own text on that page; the page we read through a fetch summary shows only the sentence and a caption repeating it.
- **February 7, 2023.** Business Today (February 10) dates the tweet of astrophysicist Grant Tremblay, who flagged the error, to this day. It says he noted the first exoplanet image came from Chauvin et al. (2004), using the VLT/NACO instrument, and later showed that a Google Search for a similar question returned the correct answer. The article also says unnamed "prominent astronomers" pointed out the error. We did not open the tweet itself.
- **February 8, 2023.** 9to5Google (9:51 a.m. PT) calls the JWST line Google's single explicit Bard example. It says Bard answered that JWST "took the very first pictures of a planet outside of our own solar system," that Reuters, citing NASA, said the European Southern Observatory's Very Large Telescope took the first exoplanet pictures in 2004, and that the error "highlights the importance of a rigorous testing process." It reports, citing Bloomberg, that Alphabet fell 9% to $98.40 at 11:26 a.m. New York time, on track for its biggest drop since October 26.
- **February 8, 2023 (evening, UTC).** The Register (22:30 UTC) says about 10 percent of Alphabet's market value, "some $120 billion," was wiped out "this week," and quotes Google as saying it was starting its Trusted Tester program that week and would combine external feedback with internal testing.

## What the user saw

The "user" here was anyone reading Google's launch post. The sources describe a prompt of the form "What new discoveries from the James Webb Space Telescope can I tell my 9 year old about?" (we read the sentence "explain new discoveries from NASA's James Webb Space Telescope to a 9-year-old" on Google's page; the longer prompt wording is in the sources only as a paraphrase) and an answer containing the claim in quotes above. The sources do not show a hedge, a source link or a "check this" note beside the claim. We did not see the original image or video, so we cannot say what the screen showed beyond what the articles describe.

## What was wrong with the claim

- NASA, as relayed by 9to5Google (via Reuters) and The Register, credits the European Southern Observatory's Very Large Telescope with the first image of an exoplanet, in 2004.
- **A wrinkle we found in the primary source.** ESO's own press release (September 10, 2004, "Is This Speck of Light an Exoplanet?") calls the object a "Giant Planet Candidate Companion" and says "the definitive answer is now awaiting further observations." So the 2004 claim was itself cautious at the time. The press coverage we opened states the 2004 image as the first, and we cannot say from these pages how that status was settled later. We do not rest the teardown on that point: all opened news pages treat Bard's claim as wrong.
- We did not open any page about Webb's own exoplanet imaging, so we make no claim about what Webb did or when.

## What Google said

Per The Register and 9to5Google, Google said the error "highlights the importance of a rigorous testing process" and tied it to the Trusted Tester program starting that week. Business Today attributes a statement about combining external feedback with internal testing to a spokesperson speaking to The Verge, and it says the aim is a high bar for "quality, safety, and real-world information." The wording differs between outlets; we did not open the statement itself. The sources we opened do not say whether the launch post or its example was changed afterward. 9to5Google shows no edit note, and Google's page shows none in the text we read.

## What the sources do not say

- Why Bard produced the claim. No opened source explains it.
- Whether anyone at Google checked the example before publishing, or whether a person was asked to.
- How the stock moved after the first day, or whether the error caused the move.

## Pattern match

- [Chatbot is confidently wrong and you can't check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) is the core fit. The claim was given in a plain, sure tone, and the sources show no source link or hedge next to it. The pattern's fix has seven rules. Rules 1 and 2 (answer from a shown source, check it supports the claim) were not met in what was shown. Rule 3 (say when you are not sure) was not shown. Rules 5 and 6 (easy checking, a person for high stakes) do not apply cleanly: this was a public demo, not a live chat with a user.
- **Where it does not match.** The pattern is written for an assistant answering a real user in a live chat. Here the answer was chosen and published by the company itself in a launch post. That makes the failure a publishing check, not a chat-time check: someone could have verified one line before it went out. The error was caught in public by an astronomer within about a day (per Business Today's dates), which is the "way to check" the pattern asks for, but it came from outside the company.

## What to measure

Proposed checks for a team that publishes example answers. None come from Google. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Example answers published with a named fact-check | Share of demo or ad answers that a named reviewer signed off against a primary source before release |
| Checkable claims per example | Count of dates, firsts, numbers and names in each example that a source could confirm |
| Wrong claims found after publishing | Public or internal corrections to a published example, divided by examples published |
| Time to correction | Hours from first public report to a visible fix or note |

## What a team can change

Proposed rules, each a pass/fail check. Status: Not yet run.

1. **Check every factual claim in a published example against a primary source.** A claim like "first," "only" or "largest" gets a named source. Check: the review sheet lists a source for each.
2. **Pick demo prompts the product has been tested on, and run them twice.** Check: the same prompt gives a source-backed answer in two runs.
3. **Ask a subject expert for science, medical, legal and financial examples.** Check: reviewer name on the sheet.
4. **Have a correction path ready before launch.** Check: who edits the page, how a note is added, and how fast, written down.
5. **Don't over-correct.** Not every demo line needs a footnote. Limit mandatory source checks to specific factual claims, not tone or summaries.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://blog.google/technology/ai/bard-google-ai-search-updates/ | Google (Sundar Pichai) | 2023-02-06 | Yes, 2026-10-21, via fetch summary |
| https://www.theregister.com/2023/02/08/alphabet_bard_mistake/ | The Register | 2023-02-08 | Yes, 2026-10-21, via fetch summary |
| https://9to5google.com/2023/02/08/google-bard-mistake/ | 9to5Google | 2023-02-08 | Yes, 2026-10-21, via fetch summary |
| https://businesstoday.in/technology/news/story/google-bard-ai-gets-fact-checked-the-story-behind-the-100-billion-mistake-369743-2023-02-10 | Business Today | 2023-02-10 | Yes, 2026-10-21, via fetch summary |
| https://www.eso.org/public/news/eso0428/ | European Southern Observatory | 2004-09-10 | Yes, 2026-10-21, via fetch summary |

All five were read through the fetch tool, which returns a summary of the page rather than the raw page. Direct quotes above are as that tool returned them.

Not opened: Reuters (fetch refused), Tom's Guide and TechRadar (only headlines returned), NBC Palm Springs (403), a NASA page (404), Grant Tremblay's tweets, Bloomberg and The Verge originals, CNN. Headlines seen in search results that we did not open give figures such as "$100 billion," "$120 billion," "$140 billion" and "7%" or "7.7%"; we use none of those except where an opened page states it.

## Where sources disagree

- **Size of the loss.** The Register (written February 8, 22:30 UTC) says about 10 percent, some $120 billion, "this week." 9to5Google, citing Bloomberg, says a 9% fall to $98.40 at 11:26 a.m. New York time that day. Business Today says as much as 9% in regular trading and puts "$100 billion" in its headline without a figure in the body. These measure different times and bases, and we cannot reconcile them.
- **Who made the statement.** The Register and 9to5Google attribute the "rigorous testing process" line to Google; Business Today attributes related wording to a spokesperson speaking to The Verge.
- **First exoplanet image.** News pages say 2004; ESO's 2004 release calls the object a candidate (see above).

## Caveats

- Everything is through fetch summaries, not the raw pages or the original post image.
- The date field is the day of the stock fall and the Register and 9to5Google coverage; the launch post is February 6.
- We do not know what Google changed afterward, if anything.

## Corrections

If you have the original post, Google's full statement or a better date, tell us and we will fix this page.
