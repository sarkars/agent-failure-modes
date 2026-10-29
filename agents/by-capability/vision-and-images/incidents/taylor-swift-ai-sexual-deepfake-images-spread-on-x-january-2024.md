# Taylor Swift AI Sexual Deepfake Images Spread on X, January 2024

<!-- SEO
title: Taylor Swift AI Deepfakes on X, January 2024: What Failed
description: In January 2024, AI sexual deepfakes of Taylor Swift spread on X. Reports tied them to Microsoft Designer, and X blocked searches for her name.
search phrases:
- taylor swift ai images x january 2024
- microsoft designer taylor swift deepfake loophole
- x blocks taylor swift search deepfakes
- why did x block searches for taylor swift
-->

**This page is a dated teardown of one public incident, for teams that run an AI image generator or a social platform where its output can be posted.** The products were Microsoft Designer, a free text-to-image tool, and X (formerly Twitter). The person shown was Taylor Swift, who did not consent. The moment was the week of January 22, 2024, when sexually explicit AI-generated images of her went viral on X. The date in the title is that week.

**Status: Needs review** (consent and law). Built from news reports downloaded on 2026-10-29 and read as text (listed at the end). The 404 Media articles are partly paywalled; we read only the free opening of each. We did not view the images and do not describe them or link to where they were posted. No opened source shows how the images were made, and Microsoft said it could not reproduce them, so the link to Designer is as reported, not proven.

> **Read this first.** This page summarizes news reports. It is not legal advice. Statements about laws, bills and platform rules are as reported and need review by a qualified person.

## What happened (as reported)

- **Before the spread.** Ben Decker of the threat intelligence group Memetica told the AP (Jan. 29) the images came from an ongoing campaign, begun the year before on fringe platforms, to make sexually explicit AI images of celebrity women, and that one of the viral images appeared online "as early as Jan. 6."
- **Jan. 25, 2024 (Thursday).** 404 Media (Emanuel Maiberg and Samantha Cole) reported the images "went viral on Twitter after jumping from 4chan and a specific Telegram group dedicated to abusive images of women," and that at least one tool the group uses is "a free Microsoft text-to-image AI generator." It cited The Verge: one of the most viral posts got 45 million views and 24,000 reposts and "was up for 17 hours prior to its removal," when the poster's account was deleted. It said other examples were still on Twitter as it wrote.
- **How the safeguards were beaten.** The AP reports Decker said "commenters on anonymous message boards discussed tactics for how to circumvent the moderation, especially on Microsoft Designer's text-to-image tool." No opened source gives the tactics.
- **Jan. 26, 2024 (Friday).** NBC News (Kat Tenbarge) reported the images posted on X "by Thursday had been viewed more than 27 million times," and the posting account was suspended after fans mass-reported it. X did not respond to NBC; Swift's representative declined to comment on the record. CBS (Jan. 29) reports X posted on its Safety account that day that "Posting Non-Consensual Nudity (NCN) images is strictly prohibited on X and we have a zero-tolerance policy towards such content."
- **Jan. 26, Microsoft's first statements.** To 404 Media: "We are investigating these reports and are taking appropriate action to address them," and its Code of Conduct "prohibits the use of our tools for the creation of adult or non-consensual intimate content." To GeekWire: "it's currently unclear where these images originated," and it had "strengthened our existing safety systems."
- **Jan. 26, Microsoft's CEO.** In an NBC interview with Lester Holt, Satya Nadella called the images "alarming and terrible" and said "we have to act." GeekWire notes the excerpt does not make clear whether he meant the Swift images specifically or deepfakes in general.
- **Microsoft's updated statement to NBC.** "We have investigated these reports and have not been able to reproduce the explicit images in these reports. Our content safety filters for explicit content were running and we have found no evidence that they were bypassed so far. Out of an abundance of caution, we have taken steps to strengthen our text filtering prompts and address the misuse of our services."
- **Other reactions.** Gizmodo (Jan. 29) reports White House press secretary Karine Jean-Pierre called the situation "alarming," and that the actors' union SAG-AFTRA said on Friday such content should be illegal if made without consent. Fans flooded X with positive posts under #ProtectTaylorSwift (AP).
- **Jan. 27-28 (weekend).** Gizmodo embeds a Jan. 27 post showing a search for "Taylor Swift" on X failing. CBS (Jan. 29) says searches had returned "Oops, something went wrong" since the Sunday before. Reuters (via SCMP) says Sunday afternoon searches showed "Something went wrong. Try reloading."
- **Jan. 29, 2024 (Monday).** The AP reports searches for her name without quote marks gave an error, while quoted searches still showed posts. X's head of business operations, Joe Benarroch: "This is a temporary action and done with an abundance of caution as we prioritize safety on this issue." CBS found some people got around the block by "adding words between the entertainer's first and last name." Microsoft told the AP it had "strengthened our existing safety systems to further prevent our services from being misused." 404 Media reported Microsoft "has introduced more protections to Designer"; SiliconANGLE says 404 Media reported this included strengthening text filtering prompts.
- **Jan. 29 evening.** Reuters (via SCMP) reports X lifted the search block; Benarroch said X "will continue to be vigilant for any attempt to spread this content and will remove it if we find it." Gizmodo (updated Jan. 30) says "Taylor Swift" searches worked by Tuesday morning but "Taylor Swift AI" still seemed blocked, and, citing Reuters, that X was hiring 100 content moderators in Austin.

## Timeline

| Date (2024) | Event | Source |
|---|---|---|
| Jan. 6 | One later-viral image online, per Memetica | AP |
| Jan. 25 | 404 Media traces images to 4chan and a Telegram group using a Microsoft tool | 404 Media |
| Jan. 26 | X Safety post; Microsoft statements; Nadella interview | CBS, 404 Media, GeekWire, NBC |
| Jan. 27-28 | Searches for "Taylor Swift" on X fail | Gizmodo, CBS, Reuters via SCMP |
| Jan. 29 | AP and CBS report the block; Microsoft adds protections to Designer; X lifts block that evening | AP, CBS, 404 Media, Reuters via SCMP |
| Jan. 30 | "Taylor Swift AI" searches still appear blocked | Gizmodo |

## Where the sources disagree or are silent

| Topic | What the sources say |
|---|---|
| Was Designer used? | 404 Media says the group used Designer and NBC says members of the group said so. NBC says it "has not independently verified that reporting." Microsoft said it could not reproduce the images and found "no evidence" its filters were bypassed "so far," yet strengthened its text filtering. SiliconANGLE says the Telegram claim was "not confirmed by others." |
| Reach | 45 million views on one post (The Verge via 404 Media; Gizmodo). More than 27 million by Thursday (NBC). CBS cites NBC for 27 million viewers and about 260,000 likes in 19 hours. These may count different posts or times. |
| Search block start | A Jan. 27 post, "Since last Sunday" (CBS) and "Sunday afternoon" (Reuters). The exact start is not stated by X. |

## Which failure patterns it shows

Pattern IDs below are the ones on each linked pattern page's header table. Taxonomy: [failure taxonomy v1](../../human-machine-interface/roadmap/specs/failure-taxonomy-v1.md); we did not find these two media IDs listed there, so a person should confirm them (Needs review). Goal: [AI deepfakes of real people](../goals/ai-deepfakes-of-real-people/README.md).

- [Nonconsensual sexual deepfakes of real people](../goals/ai-deepfakes-of-real-people/failures/nonconsensual-sexual-deepfakes-of-real-people.md) (`nonconsensual-sexual-deepfakes-of-real-people`). **Good fit.** Sexual images of a named real person were made with AI tools and spread on a large platform without her consent. That page already cites the 404 Media report on Designer in its section 4; this page adds the dated platform spread and response, so we link rather than repeat. It also matches the page's point that a policy against this content existed at both companies before the failure.
- [Real-person filters bypassed by rewording](../goals/ai-deepfakes-of-real-people/failures/deepfake-filters-bypassed-by-rewording.md) (`deepfake-filters-bypassed-by-rewording`). **Partial fit.** The AP reports people discussed tactics to circumvent Designer's moderation, and Microsoft responded by strengthening "text filtering prompts," which suggests a word-based check. Partial because no opened source says what the tactics were. That page already lists the misspelled-name claim as seen only in a summary; we also saw it only in search summaries and do not use it. A second, platform-side version of the same failure shows here: CBS found X's search block was beaten by adding words between her first and last name.
- **Possible gap for a person to judge.** No pattern in this goal covers the platform response: a search block that stops exact-name queries but not reworded ones, used because, in Decker's words to the AP, the platform could not "guarantee that everything has been taken down." This is a proposal, not a decision.

**Separate, later cases.** [Meta's celebrity chatbots that impersonated Taylor Swift, August 2025](../../human-machine-interface/incidents/meta-ai-celebrity-chatbots-impersonate-taylor-swift-without-permission-august-2025.md) is a different incident: chatbots using her name and likeness without permission, not generated sexual images. Common Dreams (Aug. 5, 2025) reports a separate case with Grok Imagine; that one is covered on the nonconsensual pattern page, not here.

## Where in the flow it broke

Based on the reports, and only as far as they go.

1. **Generation.** A free text-to-image tool was, per 404 Media, used by a group making sexual images of real women. Microsoft says its explicit-content filters were running; no source explains how output got through, if it came from Designer.
2. **Repeat abuse.** The group, per AP and 404 Media, shared ways around moderation. Microsoft's policy says repeated attempts "may result in loss of access"; no source says whether any account lost access.
3. **Posting.** One post stayed up for 17 hours, per The Verge via 404 Media, and reached tens of millions of views before removal.
4. **Platform response.** X suspended accounts, then blocked exact-name search for about two days. The block was partial (quoted and reworded searches worked) and lifted on Jan. 29.

## What a builder should take from it

Our proposals, not any company's. Each is a pass/fail check. Status: Not yet run. The full rules and tests are on the two linked pattern pages.

1. **Check the output, not only the prompt text.** Pass: a generated image flagged as sexual that shows an identifiable real person is blocked before it is returned, whatever words were typed. Fail: the only change after an incident is to the text filter.
2. **Act on shared bypass tactics.** Pass: when a known bypass is reported, it is added to a red-team set and rerun before the next release. Fail: the vendor says it cannot reproduce the output and the test set is unchanged.
3. **Count repeat attempts per account.** Pass: blocked real-person sexual requests are counted per account and trigger review at a threshold the team sets. Fail: no record of repeat attempts exists.
4. **Give the person shown a direct takedown path.** Pass: a report that says "this is me, I did not consent" hides the post on receipt and goes to a person. Fail: removal depends on mass reports by fans.
5. **Match copies, not names.** Pass: once a post is removed, copies of the same image are found by image match, not only by search terms. Fail: a reworded search still finds copies.

## What we could not verify

- How the images were made, which prompts were used, or whether Designer made the specific viral images. Microsoft said it could not reproduce them.
- What Microsoft changed in Designer beyond "text filtering prompts."
- The 404 Media articles past their free openings.
- The White House remarks and SAG-AFTRA statement, known only through Gizmodo.
- The 47 million view figure attributed to The New York Times, and the claim that users misspelled her name, both seen only in search summaries and not used.
- Whether any law or bill changed because of this case. The AP describes the EU Digital Services Act and the then-pending AI Act only in general terms; we make no claim about US law here (Needs review).

## Sources

| URL | Author / publisher | Date | Status |
|---|---|---|---|
| https://www.404media.co/ai-generated-taylor-swift-porn-twitter/ | Emanuel Maiberg, Samantha Cole, 404 Media | 2024-01-25 | Opened 2026-10-29; free opening only |
| https://www.404media.co/microsoft-closes-loophole-that-created-ai-porn-of-taylor-swift/ | Emanuel Maiberg, 404 Media | 2024-01-29 | Opened 2026-10-29; free opening only |
| https://www.nbcnews.com/tech/tech-news/taylor-swift-nude-deepfake-ai-photos-images-rcna135913 | Kat Tenbarge, NBC News | 2024-01-26 | Opened 2026-10-29 |
| https://www.nbcnews.com/tech/tech-news/microsoft-ceo-satya-nadella-calls-taylor-swift-deepfakes-alarming-terr-rcna136402 | Angela Yang, NBC News | 2024-01-30 | Opened 2026-10-29 |
| https://www.cnbc.com/2024/01/29/microsoft-ceo-responds-to-ai-generated-taylor-swift-fake-nude-images.html | CNBC (NBC News text) | 2024-01-29 | Opened 2026-10-29; same text as NBC, not independent |
| https://www.geekwire.com/2024/asked-about-taylor-swift-ai-deepfake-images-microsoft-ceo-satya-nadella-says-we-have-to-act/ | Todd Bishop, GeekWire | 2024-01-26 | Opened 2026-10-29 |
| https://www.walb.com/2024/01/29/x-pauses-taylor-swift-searches-deepfake-explicit-images-spread/ | Associated Press, via WALB | 2024-01-29 | Opened 2026-10-29 |
| https://www.cbsnews.com/news/taylor-swift-deepfakes-x-search-block-twitter/ | CBS MoneyWatch | 2024-01-29 | Opened 2026-10-29 |
| https://amp.scmp.com/news/world/united-states-canada/article/3250240/x-lifts-ban-taylor-swift-searches-after-spread-fake-porn-images | Reuters, via South China Morning Post | 2024-01-30 | Opened 2026-10-29 |
| https://gizmodo.com/taylor-swift-ai-porn-forces-x-moderate-its-content-1851205077 | Maxwell Zeff, Gizmodo | 2024-01-29 (updated 01-30) | Opened 2026-10-29 |
| https://siliconangle.com/2024/01/29/microsoft-x-respond-taylor-swift-ai-misue-increased-content-moderation/ | SiliconANGLE | 2024-01-29 | Opened 2026-10-29; opinion-heavy, used only for what 404 Media reported |
| https://www.commondreams.org/news/taylor-swift-nude-deepfakes | Common Dreams | 2025-08-05 | Opened 2026-10-29; a later, separate case |

Summary only, not used for facts: The Verge (known through 404 Media), The New York Times, HotNews.ro, Hipertextual, Digital Music News and other outlets seen in search results; X's Safety post (known through CBS).

## Corrections

If you have a primary statement from Microsoft or X, the full 404 Media text, or a better date, from a source we can open, tell us and we will fix this page.
