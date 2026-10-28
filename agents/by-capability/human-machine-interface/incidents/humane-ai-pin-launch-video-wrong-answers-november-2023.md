---
title: "Humane's AI Pin launch video shows the device naming the wrong places to see the next solar eclipse and overstating the protein in a handful of almonds, November 2023"
date: 2023-11-09
source: "https://www.shacknews.com/article/137771/humane-ai-pin-demo-false-results"
description: "How Humane's AI Pin launch video showed the device naming wrong eclipse viewing spots and overstating almond protein, and how Humane explained it."
summary: "In early November 2023 Humane posted a ten-minute launch video for its screenless, voice-first AI Pin. In it, co-founder Imran Chaudhri asks where to see the next solar eclipse, and the Pin names Exmouth, Australia and East Timor; the April 8, 2024 eclipse crossed North America. He also holds up a handful of almonds, and the Pin says they contain 15 grams of protein, which outlets called two to three times too high. Bloggers flagged both errors within days. Humane's Sam Sheffer said on the company's Discord that the video used pre-release software, that a bug reported a previous eclipse's viewing location, and that the protein figure was for a half cup of almonds. He said the issues were resolved and the video would be updated. Futurism, citing Business Insider, reported Humane was reshooting the video."
categories:
  - Governance
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - guessing-instead-of-asking
---

**This page is a dated teardown of two wrong answers in Humane's AI Pin launch video, for teams that show a voice or chat assistant answering factual questions in a demo, an ad or launch material.** The product was the Humane AI Pin, a screenless wearable. The "user" was co-founder Imran Chaudhri, speaking to the Pin on camera. The moments were two plain questions: where to see the next solar eclipse, and how much protein was in the almonds in his hand. Every fact below comes from a source we opened (listed at the end). Where we have only a second-hand account, we say so.

**Status: Needs review.** Shacknews, Futurism, 512 Pixels, Hackster.io and Cult of Mac were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. We did not watch the launch video, open Humane's Discord, or open the Business Insider report that Futurism cites (see "What we could not verify").

> **Read this first.** This is a summary of public reporting, not a finding of fact. It is not nutrition, health or legal advice. We do not say what model the Pin used or why it gave these answers; no opened source shows that. Check any nutrition figure against a primary source such as a food label or a government nutrient database.

**Channel note.** Voice first. Per Hackster.io, the Pin's primary mode of interaction is voice, with a laser projector that can show menus on the user's palm; there is no screen. In the video, Chaudhri spoke his questions and the Pin answered aloud, and for the almonds it used its camera. This phase of the knowledge base is chat-first: voice signals and voice checks are planned and not covered here. The signals and checks below are the proposed text-chat equivalents (a typed question, or a photo attached to a chat).

## What happened (as reported)

- **The launch.** 512 Pixels (Stephen Hackett, November 9, 2023) says Humane had launched its first product, the AI Pin, and points readers to a roughly ten-minute introductory video. Shacknews (Asif Khan, November 13, 2023) says Humane posted the 10-minute video to Vimeo and Twitter "last week." Shacknews and Hackster.io (Gareth Halfacree, November 10, 2023) give the price as $699 plus a $24-a-month plan.
- **The eclipse question.** Per Futurism (Maggie Harrison Dupré, November 15, 2023), citing Business Insider, about three minutes and 40 seconds into the video Chaudhri asks where to best view the next solar eclipse. 512 Pixels quotes blogger Nick Heer: the Pin said the eclipse would be on April 8, 2024, and the "best places to see it are Exmouth, Australia and East Timor". Heer and 512 Pixels say that eclipse would be visible almost only across North America, not near Australia. Futurism calls it a "Great American Eclipse."
- **The almond question.** Per Futurism, a little after the six-minute mark, Chaudhri asks how many grams of protein are in a handful of almonds, and the Pin says 15 grams. Cult of Mac (D. Griffin Jones, November 11, 2023) says he held the almonds up before the Pin's camera. Hackster.io says the Pin recognizes the almonds and "confidently overstates their protein content almost threefold."
- **Who caught it.** 512 Pixels credits Nick Heer. Hackster.io says it was spotted by David Friedman and others. Futurism says an X user pointed out you would need about 60 almonds for 15 grams of protein. All of this was within about a week of the video, by the dates on the opened pages.
- **What critics said.** 512 Pixels asks whether anyone at Humane fact-checked the answers. Shacknews: "Perhaps some basic fact-checking could have prevented this from happening?" Cult of Mac and Hackster.io both say that with no screen and no cited source, a user has no easy way to check what the Pin says.

## What Humane said

- **The Discord statement.** Shacknews reproduces a statement it says Sam Sheffer posted to Humane's official Discord server. Futurism, citing Business Insider, names Sheffer as Humane's head of new media. Per the text Shacknews reproduces:
  - The video "was created using pre-release software."
  - The eclipse error was "a bug that incorrectly reported a viewing location of a previous eclipse" rather than the upcoming one.
  - On the almonds, Humane stated "the amount of protein for a half cup of almonds" rather than the amount in Chaudhri's hand.
  - Humane had resolved the issues and "will be updating the video on our website shortly."
  - Issues found before customers get devices would be fixed as they are found, through over-the-air updates.
- **Reshoot.** Futurism, citing Business Insider, says Humane is "reshooting the video." We did not see a new video or an edit note, so we cannot say whether or when it changed.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Size of the almond error | 512 Pixels (quoting Heer): "off by at least a factor of two." Hackster.io: almost threefold. Cult of Mac: about three times. Futurism: about 60 almonds needed for 15 grams. None states how many almonds were in his hand. |
| Humane's almond explanation | The statement says the figure was for a half cup. It then says "the former is the correct and current behaviour," which does not make clear which behavior it means. |
| Who spotted the errors | 512 Pixels: Nick Heer. Hackster.io: David Friedman and others. Futurism: an X user, for the almonds. |
| Video updated | Sheffer: the video would be updated. Futurism via Business Insider: being reshot. No opened source confirms a new version. |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The date was right, the place was wrong.** Per Heer's quote, the Pin gave the right date for the next eclipse but named places that, per Humane, belonged to a previous one. Two facts in one answer came from different events, and nothing in the reply flagged that.
2. **The portion was guessed.** "A handful" has no fixed size. Per Humane, the Pin answered for a half cup instead of what the camera showed, and it did not say which amount it used.
3. **The tone was sure.** The sources describe both answers as given plainly, with no hedge and no source named. On a screenless device, the user hears one number and has nothing to check it against.
4. **The video was edited and published.** This was a recorded launch video, not a live demo. Both answers passed every step of production and went out to the public.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Core fit.** Both answers were wrong, stated in a sure tone, with no source the listener could check. The screenless, voice-first design makes the "no way to check" half stronger than in a text chat. **Where it does not match:** that pattern is about a live chat with a real user; here the company chose and published the answers itself, so the missing check was a publishing check.
- [Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md) (`guessing-instead-of-asking`). **Partial fit, almonds only.** Per Humane, the Pin used a half-cup serving instead of the amount shown. That is a guess about portion size. The pattern's fix is to ask one short question; for a camera answer, a better fix may be to say the amount assumed so the user can correct it. No source says the Pin should have asked.
- **Considered, not a fit.** `clean-lab-testing`: about messy typed input, and these questions were clean. `allergy-and-dietary-requests-handled-loosely`: about ordering bots and allergy safety, not nutrient counts. `voice-only-flows-with-no-text-alternative`: an accessibility pattern about people who cannot use voice; the Pin had a projector, and no source raised access. `live-camera-guidance-too-slow-or-wrong`: about step-by-step guidance from photos, not one identification. `conflicting-inputs-resolved-silently`: the almond photo and the spoken question did not conflict; the answer ignored the photo's amount, which is closer to a guess. `wrong-explanations-taught-as-fact`: written for tutors and students.
- **Possible gap for a person to judge.** The eclipse answer mixed a correct date with another event's places. No pattern in this taxonomy names an answer whose parts come from different events or time periods. This is a proposal, not a decision.

## How it differs from close cases

- [Google Bard launch demo, February 2023](google-bard-launch-demo-wrong-jwst-claim-february-2023.md): a single wrong "first" in a launch post, caught by an astronomer. Here two answers in one video were wrong, and the device had no screen to show a source.
- [Google Gemini Super Bowl ad, February 2025](google-gemini-super-bowl-ad-wrong-gouda-cheese-statistic-february-2025.md): a wrong share-of-consumption figure that Google said came from the web, and the ad was quietly edited. Here Humane blamed pre-release software bugs and said the video would be updated.
- Futurism counts this as the third such launch that year, after Google's and Microsoft's in February 2023. We did not open a source on the Microsoft case for this page.

## What to measure

Proposed text-chat signals, not results. Status: Not yet run. Voice signals are planned only.

- Share of demo and launch answers with a named reviewer and a primary source for each date, place and number, signed off before release.
- Share of answers to "where/when is the next X" questions where every place, date and time refers to the same event (checked against the source).
- Share of nutrition answers to a photo or a vague amount ("a handful," "a bowl") that state the amount assumed.
- Share of nutrition answers that name a source the user can check.
- Count of public corrections to a published demo answer, and hours from first public report to a visible fix.

## What a team can change

Our proposals, not Humane's. Each is a pass/fail check on a transcript, a review sheet or a test run. Status: Not yet run.

1. **Fact-check every demo answer.** Pass: the review sheet lists a primary source and a reviewer name for each date, place and number spoken or shown in the video.
2. **One event per answer.** Pass: for "next eclipse" style questions, the place, date and time in the reply all match the same source entry.
3. **Say the amount you assumed.** Pass: a reply to "how much protein is in this handful" states the count or weight it used, such as a count of almonds or a weight in grams.
4. **Name the source out loud or in text.** Pass: a nutrition or event answer includes a source name the user can look up.
5. **Re-run demo prompts on the shipping build.** Pass: each prompt in the launch video gives the same checked answer on the release build, in two runs.
6. **Have a correction path ready.** Pass: before launch, a named owner, a way to post a correction note and a target time to fix are written down.
7. **Don't over-correct.** Pass: a clear question with one answer, such as "when is the next eclipse," gets a short direct answer with its source, not a stack of caveats or a follow-up question.

## What we could not verify

- The launch video itself. We did not watch it, so the exact spoken words, timestamps and what the camera showed come from the articles.
- Humane's Discord post. We read only the text Shacknews reproduces from a screenshot.
- Business Insider's report that Humane was reshooting the video, and Sheffer's job title. Both are seen only through Futurism.
- Nick Heer's original post. We read only the lines 512 Pixels quotes.
- Whether the video was ever updated, and what changed.
- How many almonds were in Chaudhri's hand, and the correct protein figure. No opened source gives a primary nutrition source.
- Which model or service the Pin used. Hackster.io and Cult of Mac describe links to large language models such as OpenAI's ChatGPT, but we do not rely on that.
- Seen only in search summaries / unverified: a beehiiv repost of the Futurism story (AIPressRoom), a Yahoo UK story headlined as a "major mistake," WinFuture.de, the ACS Information Age article, a Substack post by Eliot C., and a hyperquest.digitalpress.blog post. None is used for facts here.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.shacknews.com/article/137771/humane-ai-pin-demo-false-results | Shacknews (Asif Khan) | 2023-11-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://futurism.com/the-byte/ai-pin-mistakes-launch-video | Futurism (Maggie Harrison Dupré) | 2023-11-15 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://512pixels.net/2023/11/the-humane-ai-pin/ | 512 Pixels (Stephen Hackett, quoting Nick Heer) | 2023-11-09 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://hackster.io/news/humane-unveils-the-ai-pin-its-large-language-model-linked-wearable-with-some-embarrassing-errors-fe424a998c36 | Hackster.io (Gareth Halfacree) | 2023-11-10 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://www.cultofmac.com/?p=836839 | Cult of Mac (D. Griffin Jones), "Even more reasons Humane's Ai Pin is a total bust" | 2023-11-11 | Yes, 2026-10-28, raw HTML read as text; paraphrased only |

## Corrections

If you have the original or updated launch video, Humane's Discord post, or the Business Insider report, tell us and we will fix this page.
