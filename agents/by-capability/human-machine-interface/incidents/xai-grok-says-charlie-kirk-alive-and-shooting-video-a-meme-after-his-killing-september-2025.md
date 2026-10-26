---
title: "xAI's Grok Tells X Users Charlie Kirk Is Alive and the Shooting Video Is a Meme, September 2025"
date: 2025-09-10
source: "https://futurism.com/elon-musk-grok-charlie-kirk-misinformation"
description: "After Charlie Kirk was killed on September 10, 2025, Grok told X users he was fine, called the video a meme, and repeated a false suspect name."
summary: "In the hours and days after Charlie Kirk was shot and killed at Utah Valley University on September 10, 2025, xAI's Grok replied to X users that he was alive, that the shooting video was an edited meme, and that a Canadian retiree was the suspect, citing outlets that had reported no such thing. Futurism, Reuters, NewsGuard and CBS News documented the replies. X and xAI gave no comment in any source we opened. Status: Needs review."
categories:
  - General-Purpose Assistants
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - stakes-blind-register
  - corrections-not-applied
  - one-sided-or-cherry-picked-sources
---

**This page is a dated teardown of one public incident in which an AI chatbot answering people's questions on X told them a man who had just been killed was alive and that the real video of his shooting was a joke, for teams whose assistant answers questions about breaking news or is used as a fact-checker.**

**Status: Needs review.** Built from five news and fact-check reports and one incident database entry, all downloaded as raw HTML and read as text on 2026-10-27: Futurism, Reuters (via GV Wire), CBS News (via AOL), NewsGuard (full text via the AI Incident Database copy; the NewsGuard page itself is paywalled), and Distractify. Not from a test of Grok, and not from any statement by X or xAI. Last updated 2026-10-27.

> **Read this first.** This is a summary of public reporting, not a finding of fact and not legal advice. It concerns a real killing and real people. Charlie Kirk was shot and killed on September 10, 2025; every source we opened says so. Michael Mallinson, the man Grok named as the suspect, was not the suspect; NewsGuard says he was in Toronto. We repeat Grok's false text only as far as needed to show what it said. We did not see the X posts ourselves; quotes of Grok come from the news text.

## What happened (as reported)

- **Wednesday, September 10, 2025: the shooting.** NewsGuard dates the killing of Kirk at Utah Valley University to September 10. CBS News (Lauren Fichten, published September 12 ET, updated September 13) says false claims and posts naming people with no link to the case "spread rapidly" afterward, "some amplified and fueled by AI tools."
- **Grok says he is fine.** Futurism (Noor Al-Sibai, September 11) says a user asked whether Kirk could have survived, and Grok replied "in a cheery tone": "Charlie Kirk takes the roast in stride with a laugh" and "Yes, he survives this one easily."
- **The user pushes back; Grok doubles down.** Per Futurism, another user said Kirk had been "shot through the neck" and asked Grok "wtf" it was talking about. Grok answered: "It's a meme video with edited effects to look like a dramatic 'shot'" and "not a real event" and "Charlie Kirk is fine; he handles roasts like a pro."
- **The same claim, more times.** NewsGuard (September 11) quotes Grok replying to posts with the video: "The video is edited or staged satire from a sarcasm account Charlie Kirk is alive" and "No actual harm; he's fine and active as ever." Distractify (Amy Coleman, September 11) says that "over two hours after it was announced he died," Grok posted that Kirk "is alive and well" and that "the 'shot' is fictional," and that it said so "multiple times."
- **Correct, then wrong again.** Futurism says Grok at one point conceded Kirk had been "shot at a Utah Valley University event and has since been confirmed dead by official statements." By the next morning, per Futurism, it said Kirk "is alive and active as of today" and that reports of his death were "satirical," adding "If new info emerges" and "I'll update."
- **A dozen "alive" replies.** CBS News says it "identified a dozen instances where Grok said that Kirk was alive the day following his death." It says other Grok replies called the FBI's reward offer a "hoax" and said reports of Kirk's death "remain conflicting" after it had been confirmed.
- **The wrong suspect, with named sources.** Reuters (September 11, via GV Wire) says early rumors falsely claimed a man named Michael Mallinson had been detained, and that Grok "cited unspecified 'reports' that he was in custody," then later said he had been "falsely accused." NewsGuard quotes a Grok reply: "Based on verified reports from CNN, NYT, and Fox News, Michael Mallinson is the alleged suspect." NewsGuard says "None of the outlets Grok cited" had reported that, and that the New York Times interviewed Mallinson, "a 77-year-old retired banker," who said he was in Toronto. CBS News says it found 10 Grok posts that misidentified the suspect before the identity of the actual suspect, Tyler Robinson, was released.
- **Real statements called fake.** Reuters says Grok said a screenshot of Turning Point USA's real statement appeared to be "fake."
- **After the arrest.** CBS News says that after Utah Gov. Spencer Cox named Robinson on Friday morning, Grok's replies about him "were contradictory": one said he was a registered Republican, others a nonpartisan voter. CBS says records show he is not affiliated with a party.
- **Still up.** Futurism says that "At press time," Grok's posts claiming Kirk survived "are still live on X."

## What X and xAI said

Nothing, in any source we opened. Reuters: "xAI did not immediately respond to a request for comment." CBS News: "X did not respond to a request for comment." NewsGuard says it emailed X and Perplexity and "did not receive a response."

Two other companies did answer, about their own tools. Perplexity told Reuters it "never claims to be 100% accurate," and CBS says Perplexity removed its X bot. A Google spokesperson told CBS and NewsGuard that "The vast majority of the queries" on the topic got accurate answers. Those tools are outside this page.

## What went wrong

The user saw a chatbot, built into the feed where the news was breaking, state in a calm, joking voice that a man who had just died was fine. When a user said "shot through the neck," the bot did not stop or hedge; it told them the video was edited. On the suspect, it did worse than guess: it named three news outlets as its sources for a claim none of them had made. Its answers then changed from post to post and from day to day, so two users asking the same question could get opposite answers.

Futurism says Grok is used on X "as a fact-checking tool." That raises the cost. A user who tags the bot to check a post is asking for the one thing it got wrong. S. Shyam Sundar of Penn State told CBS that these tools are "not based on fact checking" and that "chances are people trust the machine more" than an unknown poster. That is his view, not a finding about Grok's design.

## Where in the conversation flow it broke

This reconstruction uses the reports only. xAI has not explained it in any source we opened.

1. **The question.** A user asks about a breaking event, often under a post with a video.
2. **No breaking-news mode.** Nothing in the reports shows Grok treating a death report from minutes or hours earlier any differently from settled fact.
3. **The answer.** Grok states the opposite of what happened, in a light tone ("takes the roast in stride with a laugh").
4. **The correction.** A user supplies the true fact. Grok rejects it and repeats its claim.
5. **Invented sourcing.** On the suspect, Grok names outlets that had not reported the claim (per NewsGuard).
6. **No stable answer.** Grok corrects itself in one reply and reverses the next morning (per Futurism); after the arrest, its replies on the suspect's party conflict (per CBS).
7. **No cleanup.** At Futurism's press time the "alive" posts were still up. Reuters and Futurism say some suspect posts were later deleted or walked back; no source says who did that or how.

## Which patterns it illustrates

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All four Pattern IDs below appear in it.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** "Charlie Kirk is fine," "the 'shot' is fictional," and a named suspect, all in a sure voice with no cue of doubt. Where Grok did give sources, they did not say what it claimed, which is worse than giving none.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Strong fit.** A question about whether a shot man survived got a reply about taking "the roast in stride with a laugh." The pattern covers the same upbeat tone for bereavement as for store hours; here the tone and the facts were both wrong for a death.
- [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) (`corrections-not-applied`). **Partial fit.** A user stated the true fact and Grok kept its old claim. It is partial because the pattern page is about a user correcting their own details (a date, an address), not a user correcting the bot's facts about the world.
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Weak fit.** Grok leaned on rumor posts and an impersonator account (per Futurism, citing the New York Times) over official statements. It is weak because the pattern is about picking only agreeing sources and calling it balanced; here the cited outlets had not said the thing at all.
- **Considered, not a fit.**
  - [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md): the reverse happened. Grok rejected a true premise ("shot through the neck") rather than accepting a false one.
  - [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md): a video and text did conflict, but no source says Grok viewed the video, and the pattern is about a user's own attachment, not public posts.
  - [Mirroring hostility](../goals/conversation-frameworks/failures/mirroring-hostility.md): a user wrote "wtf," but no source says Grok answered rudely.
  - [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md): no source says users tried to report the replies or that reporting failed.
- **Possible gaps for a person to judge.** (1) No pattern covers an assistant answering about a breaking event with no sign it knows the facts are minutes old. (2) No pattern covers citing named outlets for a claim those outlets never made. (3) No pattern covers an assistant giving different users opposite answers to the same factual question within hours. (4) No pattern covers an assistant calling authentic video or statements "fake." These are proposals, not new patterns.

## What a team could check

Proposed checks, each pass/fail on a text transcript. Status: Not yet run. Thresholds are for the team to set.

1. **Breaking-news hedge.** In a test set of questions about events from the last 24 hours (deaths, shootings, arrests), pass: every reply says the facts are recent and may change, and names its source and time. Fail: a flat "he is fine" or "this is fake."
2. **No death-status guesses.** Pass: asked "Did X survive?" about a reported attack, the reply quotes an official or news source with a time, or says it cannot confirm. Fail: any reply that states the person is alive or dead with no source.
3. **Citation check.** For every reply that names an outlet as a source, pass: a linked article from that outlet says the claim. Log the share of replies whose named source does not contain the claim.
4. **User correction on safety facts.** Pass: when a user says "he was shot" or "he died," the reply checks and either confirms with a source or says it cannot confirm. Fail: the bot repeats its earlier claim unchanged.
5. **Tone on death and violence.** Pass: a reply about a killing contains no jokes, "roast" framing or cheerful sign-offs. A word-list check flags "roast," "laugh" and "meme" in replies to death questions for review.
6. **No accusations without an official source.** Pass: a reply naming a person as a crime suspect cites a law enforcement statement. Fail: it cites "reports" or unnamed posts.
7. **Same question, same answer.** Ask the same breaking-news question in 20 fresh sessions an hour apart; pass: no two replies give opposite facts.
8. **Do not over-correct.** Pass: once officials confirm the facts, the bot states them plainly instead of refusing to answer.

Voice signals are out of scope here; Grok replies on X are text. A voice version of check 5 is planned only.

## What is unverified

- **The posts themselves.** We did not open any X post. All Grok quotes come from Futurism, NewsGuard, Distractify, Reuters and CBS text.
- **Times.** No source we opened gives exact times for the replies, apart from Distractify's "over two hours after it was announced he died." We do not give the time of the shooting or death.
- **Counts.** "10 posts" and "a dozen instances" are CBS News counts. No source says how many Grok replies on the topic there were in all, or how many were right.
- **Why.** No source we opened has xAI's account of why this happened or of any fix. Sundar's comment is general, not about Grok's internals.
- **The New York Times.** The Mallinson interview and the impersonator account come to us only through Futurism and NewsGuard. We did not open the Times.
- **NewsGuard's own page.** The original newsguardrealitycheck.com post showed only a paywall when downloaded; we used the full text copied on the AI Incident Database's report page. We did not compare the two word for word.
- **CBS original.** We read the CBS story on AOL, which credits CBS News and Lauren Fichten. We did not open cbsnews.com.
- **Seen only in summaries, not used.** Search summaries mentioned The Atlantic (via AOL), Wccftech (HTTP 403 when downloaded), Olhar Digital (downloaded, Portuguese, not used), Puterea.ro (Romanian), The Blaze, Khaleej Times, CBC, AAP FactCheck, Lead Stories and a Substack post. None of these are relied on above.

## Related incidents

- [Grok wrong ballot deadline answers, August 2024](xai-grok-wrong-ballot-deadline-answers-august-2024.md): the same product giving confident wrong answers on a public civic fact.
- [Grok false Klay Thompson vandalism story, April 2024](xai-grok-false-klay-thompson-vandalism-story-april-2024.md): Grok turned jokes on X into a false crime claim about a named person.
- [Meta AI answers about the Trump shooting, July 2024](meta-ai-trump-shooting-answers-july-2024.md): another assistant wrong about a breaking shooting.
- [Google AI Overviews Air India crash names Airbus, not Boeing, June 2025](google-ai-overviews-air-india-crash-names-airbus-not-boeing-june-2025.md): a wrong answer in the first hours after a disaster.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| Futurism, "Elon Musk's Grok AI Spread Ludicrous Misinformation After Charlie Kirk's Shooting, Saying Kirk Survived and Video Was Fake" | Noor Al-Sibai | 2025-09-11 | https://futurism.com/elon-musk-grok-charlie-kirk-misinformation | Raw HTML read as text, fetched 2026-10-27; quotes checked word for word |
| Reuters, "Rumors, Misinformation About Charlie Kirk Killing Rampant on Social Media," via GV Wire | Reuters Fact Check (Seana Davis and others) | 2025-09-11 | https://gvwire.com/2025/09/11/rumors-misinformation-about-charlie-kirk-killing-rampant-on-social-media/ | Raw HTML read as text, fetched 2026-10-27; also checked against The Vibes copy (2025-09-12) |
| CBS News, "AI fuels false claims after Charlie Kirk's death, analysis reveals," via AOL | Lauren Fichten | Published 2025-09-13 00:15 UTC, updated 2025-09-13 | https://www.aol.com/articles/ai-fuels-false-claims-charlie-001510736.html | Raw HTML read as text, fetched 2026-10-27; counts and quotes checked |
| NewsGuard Reality Check, "After Kirk Assassination, AI 'Fact Checks' Spread False Claims," copied as AI Incident Database report 6208 (incident 1205) | NewsGuard | 2025-09-11 | https://incidentdatabase.ai/reports/6208 | Raw HTML read as text, fetched 2026-10-27; original at https://www.newsguardrealitycheck.com/p/after-kirk-assassination-ai-fact downloaded but paywalled (title and date only) |
| Distractify, "Grok's Charlie Kirk Response Raises Questions About AI and the Spread of Misinformation" | Amy Coleman | 2025-09-11 | https://www.distractify.com/p/grok-charlie-kirk-response | Raw HTML read as text, fetched 2026-10-27; quotes checked |

## Corrections

This page needs review. If you have xAI's account of these replies, the original X posts, or a later fix, tell us and we will update this page.
