---
title: "Fable book app's AI year-end reader summaries told a Black reader to read more white authors and mocked other users' identities, and Fable pulled its AI features, December 2024"
date: 2024-12-30
source: "https://www.wired.com/story/fable-controversy-ai-summaries/"
description: "Fable's AI reading recaps for 2024 joked about users' race and sexuality. Fable apologized, then removed the recaps and two other AI features in January."
summary: "On December 30, 2024, a Threads user who goes by @tianas_littalk, book influencer Tiana Trammell, posted her 2024 Reader Summary from the book app Fable. The AI-made text praised her reading of Black authors, then told her: \"Don't forget to surface for the occasional white author, okay?\" Writer Danny Groves's summary asked if he was ever in the mood for a straight, cis white man's perspective. Fable said the summaries were meant to playfully roast users and came from an AI model; WIRED reported it used OpenAI's API. On January 2, 2025, Fable's head of product, Chris Gallello, apologized in a video and listed fixes. On January 3, WIRED reported that Fable had removed the 2024 summaries and two other AI features. Status: Needs review."
categories:
  - Consumer Apps
  - Persona and tone
  - Trust
patterns:
  - over-correcting-for-identity
  - tone-changes-shipped-with-no-regression-test
  - no-way-to-report-bad-behaviour
  - undisclosed-bot-identity
---

**This page is a dated teardown of the Fable book app's AI-written year-end Reader Summaries in late 2024, for teams that ship AI-made text about a user's own data, such as a recap, a profile blurb or a "roast," into a consumer app.** The product was Fable, a social app where people track and discuss the books they read. The users were readers who opened their 2024 stats page. The moment was one generated sentence at the end of a summary, written in a joking voice, that commented on the race, sexuality or disability tied to what the user read. Every fact below comes from a source we opened (listed at the end). No opened source has Fable's prompt, its model settings, its test process, or a count of how many summaries were offensive. The date above is the day the first screenshot was posted, per the Daily Dot.

**Status: Needs review.** WIRED (Kate Knibbs, January 3, 2025, updated the same day at 5:44 p.m. ET), the Daily Dot (Lindsey Weedston, January 3, 2025) and Smart Bitches, Trashy Books (SB Sarah, January 1, 2025, with an update on January 2) were downloaded as raw HTML on 2026-10-28 and read as plain text. Book Riot's January 2025 post was also downloaded; it retells WIRED's report and is not used as a separate source. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same.

> **Read this first.** This is a summary of public reporting, not a finding of fact. We did not see Fable's app, the full set of summaries or Fable's video posts; we quote them only as the outlets above quote them. We name only people who spoke on record to a reporter or posted publicly under their own name: Tiana Trammell, Danny Groves, A.R. Kaufer, Chris Gallello and Kimberly Marsh Allee.

**Channel note.** This is a text incident, but not a chat: the AI text appeared on a stats page inside the app, unasked, with no way to reply. This phase of the knowledge base is chat-first, and the signals and checks below are written for logged AI-made text shown to a user. Voice and web signals, such as a voice assistant reading a recap aloud, or a shared recap image posted to the web, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The feature.** Per WIRED, Fable built an AI-powered summary "recapping what books users read in 2024," and it "was meant to be playful and fun." Fable told users its summaries "are intended to both capture your reading history and playfully roast your taste," per Smart Bitches, Trashy Books.
- **The first screenshot.** Per the Daily Dot, on December 30, 2024, Threads user @tianas_littalk posted her summary and said "this particular one is not sitting well with me at all." The text read: "Soulful Explorer: Your journey dives deep into the heart of Black narratives and transformative tales, leaving mainstream stories gasping for air." It ended: "Don't forget to surface for the occasional white author, okay?" WIRED names her as books influencer Tiana Trammell.
- **Not the only one.** Writer Danny Groves's summary called him a "Diversity Devotee" and wondered "if you're ever in the mood for a straight, cis white man's perspective!" (Smart Bitches, Trashy Books; WIRED). Trammell told WIRED that, after she posted, "I received multiple messages" from people whose summaries commented on "disability and sexual orientation."
- **How users could tell it was AI.** Smart Bitches, Trashy Books wrote that "two little stars" next to the words "Reader Summary" seemed to indicate AI. Per the Daily Dot, Fable's head of product used the word AI only late in his apology video.
- **The model.** Per WIRED, Fable used "OpenAI's API to generate summaries of the past 12 months of the reading habits for its users." Fable wrote on Threads that the summaries come from "an AI model" serving "~2 million users," per Smart Bitches, Trashy Books.
- **Users left.** Per the Daily Dot, Trammell wrote: "After the public statement of @fable, I've deactivated my account and deleted the application." Per WIRED, author A.R. Kaufer also deleted her Fable account.

## What the company said

- **December 31, 2024, on Threads**, per Smart Bitches, Trashy Books: "Thanks for sharing, agreed this one is not ok. I'm passing it along to the team to resolve."
- **January 1, 2025, on Threads**: "This never should have happened." The summaries "should never, ever, include references to race, sexuality, religion, nationality, or other protected classes."
- **By January 2, 2025, on Threads**, per the same post's update of 8:30 a.m. ET that day, which does not date the reply: Fable is "constantly fine-tuning based on feedback" and "We are adding new guardrails to make sure no one else has this experience."
- **Chris Gallello, head of product, in a video posted January 2, 2025**, per the Daily Dot: "We got a couple reports from users about our reader summary feature on the profile using very bigoted, racist language." The Daily Dot lists his planned changes: a notice that the summary is AI-generated, an opt-out, removing the "playfulness," and thumbs up and thumbs down buttons.
- **Fable's apology caption**, per WIRED: "We are deeply sorry for the hurt caused by some of our Reader Summaries this week," and "We will do better."
- **Kimberly Marsh Allee, head of community**, to WIRED before publication: "For the time being, we have removed the part of the model that playfully roasts the reader, and instead the model simply summarizes the user's taste in books." After publication, per WIRED, she said Fable had instead decided to "immediately remove the AI-generated 2024 reading summaries, as well as two other features that used AI."

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Final fix | The Daily Dot (January 3): Gallello's plan "did not include ditching the AI." WIRED (updated January 3): Fable then removed the 2024 summaries and two other AI features. WIRED does not name the two features. |
| How many summaries | Gallello: "a couple reports." Trammell: "multiple messages." No opened source gives a count. |
| Safeguards | Fable said on January 1 that the summaries should never reference protected classes, and on January 2 that it was "adding new guardrails." No opened source says what rules or filters existed before. |
| AI disclosure | Smart Bitches, Trashy Books: only two small stars hinted at AI. The Daily Dot: Gallello's video used the word AI only late. Fable planned a clearer notice. |

## Where in the flow it broke

Based on the reports above, and only as far as they go. Each step is a place a check could have caught it.

1. **A joking voice was the goal.** Fable asked for text that would "playfully roast" each reader. A roast invites comments on who the user is.
2. **Identity was inside the input.** The model saw what each person read. It turned the authors' identities into a comment on the reader's choices.
3. **No rule stopped the sentence.** Fable says the text should never mention protected classes; the shipped text did.
4. **No person read it first.** The text went straight to a profile page for about 2 million users, per Fable. No opened source describes a review step.
5. **Users had to report it in public.** The first report reached Fable through a Threads post. Fable added thumbs buttons only afterward.
6. **The label was faint.** Per Smart Bitches, Trashy Books, two small stars were the only sign the text was AI-made.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on screenshots and statements as WIRED, the Daily Dot and Smart Bitches, Trashy Books quote them; no opened source shows Fable's prompt or tests.

- [Over-correcting for identity](../goals/fairness-and-identity/failures/over-correcting-for-identity.md) (`over-correcting-for-identity`). **Partial fit.** The entry covers a bot that brings up a user's guessed identity unasked. Fable's text commented on race and sexuality tied to each reader's books. But that entry is about side effects of a bias fix, and no opened source says a fix caused this.
- [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`). **Partial fit.** A "roast" register went to every user, and a fixed set of test readers with diverse shelves would show the risk. No opened source says how Fable tested it; Trammell asked Fable to "conduct rigorous internal testing."
- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). **Partial fit.** The reports came through public Threads posts, and Fable planned thumbs up and down buttons only after. No opened source says whether an in-app report path existed.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Weak fit.** The AI source was marked only by two stars, per one blog. That entry is about a chatbot passing as a person in conversation; nobody here thought a person wrote it to them.
- **Considered, not a fit.** [Mirroring hostility](../goals/conversation-frameworks/failures/mirroring-hostility.md) (`mirroring-hostility`): the users wrote nothing hostile; the jab was built into the feature. [Steering by protected class in recommendations](../goals/real-estate-agents/failures/steering-by-protected-class-in-recommendations.md) (`steering-by-protected-class-in-recommendations`): the "occasional white author" line is a race-keyed suggestion, but that entry is about housing. [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): the harm was insult, not a false fact.
- **Possible gaps for a person to judge.** (1) No pattern covers AI humor or "roasts" built from a user's own data, where the joke lands on a protected trait. (2) No pattern covers AI text pushed unasked onto a profile or stats page, outside any chat, with no reply or report button. These are proposals, not decisions.

## How it differs from close cases

- [Apple Intelligence notification summaries misreport news (December 2024)](apple-intelligence-notification-summaries-misreport-news-headlines-december-2024.md): also unasked AI summaries in the same month, but the harm there was false facts, not insults.
- [Microsoft's Tay learns abuse from users (March 2016)](microsoft-tay-chatbot-learns-abuse-from-users-march-2016.md): users fed Tay the offensive text. Here no user asked for it; the product's own design asked for a roast.
- [xAI Grok antisemitic posts after an update (July 2025)](xai-grok-antisemitic-posts-after-update-july-2025.md): offensive output after a voice change too, but public posts, not a private page about one user.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each can be computed from logged generated text and a labeled sample; each has a counter-signal.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Protected-trait mentions | Share of generated recaps that mention race, sexuality, religion, nationality, gender or disability, of the user or of authors | Recaps that name a book's real subject, such as a memoir about disability, wrongly flagged |
| Jab on a trait | Share of recaps where a joke or nudge targets a group or trait, per a labeled sample | Share of recaps so flat that users stop opening them |
| Paired-shelf gap | Tone score gap between recaps for test shelves that differ only in author identity | Recaps made identical by stripping all book detail |
| Report rate | Share of recaps a user flags, per thousand shown | Share of flags that reviewers judge as not a problem |
| Public-first reports | Share of problem reports that reach the team through social media before any in-app flag | Total report volume, so a drop is not just fewer reporters |

## What a team can change

Our proposals, not Fable's. Each is a pass/fail check on generated text or a test run. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **No jokes about who someone is.** Pass: on a test set, no recap jokes about or nudges on any protected trait of the user or of the authors they read.
2. **Paired shelves read alike.** Pass: test shelves that differ only in author race or sexuality get recaps with the same tone label.
3. **Test the register before launch.** Pass: any change to the voice of generated text runs the fixed test set first, and the run is logged.
4. **Say it is AI in words.** Pass: each recap carries a plain text label that it was AI-generated, not only an icon.
5. **Give a report button and an off switch.** Pass: each recap has a one-tap report and an opt-out, and a report reaches a person's queue.
6. **Don't over-correct.** Pass: a recap for a reader of memoirs about disability can still name that subject plainly, without a joke.

## What we could not verify

- Fable's prompt, model settings, filters and test process. No opened source describes them.
- Gallello's video and any second video. Known to us only through the Daily Dot.
- Which two other AI features Fable removed, and whether any AI feature returned later. No opened source says.
- Seen only in search summaries, not opened and not used as fact: a USA TODAY report quoting Marsh Allee calling the summaries unacceptable; claims that Gallello posted a second video saying Fable would remove all generative AI; claims that Gallello mentioned an offensive-language filter that failed; and coverage by getcoai.com and the AI Incident Database.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.wired.com/story/fable-controversy-ai-summaries/ | WIRED (Kate Knibbs) | 2025-01-03, updated same day | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://dailydot.com/fable-app-racist-ai | The Daily Dot (Lindsey Weedston) | 2025-01-03 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://smartbitchestrashybooks.com/2025/01/fables-reader-summary-features-racism-and-probably-ai/ | Smart Bitches, Trashy Books (SB Sarah) | 2025-01-01, updated 2025-01-02 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://bookriot.com/a-book-apps-ai-called-its-users-too-woke/ | Book Riot; retells WIRED | January 2025 | Yes, 2026-10-28; not used as a separate source |
| https://www.aol.com/fable-embroiled-controversy-over-offensive-002814367.html | USA TODAY, syndicated by AOL | Not confirmed | No: returned 404 on 2026-10-28; not used |

## Corrections

If you have Fable's video posts, a Fable statement naming the removed features, or a report on whether AI features returned, from a source we can open, tell us and we will fix this page.
