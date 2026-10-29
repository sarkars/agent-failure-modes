# Reddit Answers AI suggests kratom and heroin for chronic pain in a medical subreddit, October 2025

<!-- SEO
title: Reddit Answers AI Suggests Kratom and Heroin for Chronic Pain
description: Reddit's AI chatbot showed kratom and heroin answers under a family medicine thread in October 2025, and moderators said they could not turn it off.
search phrases:
- reddit answers heroin
- reddit ai suggests kratom for pain
- reddit answers dangerous medical advice
- moderators cannot disable reddit answers
- ai chatbot health answers from user posts
-->

**This page is a dated teardown of one reported Reddit Answers failure, for teams whose chatbot builds answers from user posts and shows them next to community content on health, money or safety topics.** The product was Reddit Answers, Reddit's "AI-powered conversational interface," as 404 Media quotes Reddit describing it. The user was a healthcare worker posting in r/FamilyMedicine on the Reddit mobile app. The moment was a "Related Answers" link under their post that pointed to kratom, and a follow-up question about heroin that got an answer quoting a Redditor who said heroin "saved my life." The date above is the month 404 Media first reported it.

**Status: Needs review.** Built from four pages, all downloaded on 2026-10-29 and read as plain text: 404 Media, "Reddit's AI Suggests Users Try Heroin," by Emanuel Maiberg (Oct 16, 2025; only the free opening is readable, the rest is paywalled); Wi-Fi Planet, by Jamie Spencer (Oct 17, 2025); Slashdot, posted by EditorDavid (Oct 18, 2025); and Futurism, by Rae Witte (Oct 19, 2025). 404 Media is the original report. Futurism and Wi-Fi Planet both say they rely on 404 Media. Slashdot quotes the Reddit posts directly, so it is a second, separate path to the same facts, but it is an aggregator, not a reporting outlet. The original r/ModSupport post could not be opened (Reddit blocked the download). Each quote below was checked word for word against the saved text with a script.

> **Read this first.** This page summarizes news reports and quoted Reddit posts. It is not medical advice: heroin and kratom are not safe pain treatments, and anyone in pain should talk to a clinician. We did not test Reddit Answers, then or now. We make no finding about any law. We name only people named in the opened sources; the healthcare worker and the moderator are not named there.

**Channel note.** This is a text incident: an AI answer shown as a link under a post and a typed follow-up question in the Reddit app. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The feature.** Per 404 Media, while looking at a thread in r/FamilyMedicine "on the official Reddit mobile app, the app suggested a couple of 'Related Answers' via Reddit Answers."
- **The kratom answer.** One related answer, titled "Approaches to pain management without opioids," suggested kratom, per 404 Media. 404 Media cites the FDA warning against kratom "because of the risk of serious adverse events, including liver toxicity, seizures, and substance use disorder," and the Mayo Clinic calling it "unsafe and ineffective."
- **What the cited post said.** The healthcare worker, as quoted by Slashdot: "The first post it cited urged people to stop their prescribed medications and take high-dose kratom which is an illegal (in some states) and unregulated substance."
- **The heroin question.** Futurism says the user then asked whether there was any medical rationale to use heroin for pain. The bot replied, per Futurism: "Heroin and other strong narcotics are sometimes used in pain management, but their use is controversial and subject to strict regulations."
- **The quoted Redditor.** The reply went on, per Futurism: "One Redditor shared their experience with heroin, claiming it saved their life but also led to addiction: 'Heroin, ironically, has saved my life in those instances.'"
- **Mixed results.** The healthcare worker, per Slashdot: "One answer warned about addiction and linked to crisis and recovery resources. The other connects to a post where someone claims heroin saved their life and controls their chronic pain."
- **The endorsement problem.** Same post: "The AI-generated answers could easily be mistaken as information endorsed by the sub it appears in."
- **No off switch.** Slashdot quotes the r/FamilyMedicine moderator: Reddit Answers "has been spreading grossly dangerous misinformation," and moderators "cannot disable this feature." 404 Media's subhead: moderators "can't opt out."
- **The sub's warning.** Per Slashdot, r/FamilyMedicine posted a top-of-page notice: "We do NOT and CANNOT endorse Reddit Answers at this time and urge every user of this sub to disregard anything it says."

## Timeline

| Date | Event | Source |
|---|---|---|
| Before Oct 16, 2025 | Healthcare worker posts in r/FamilyMedicine and sees the kratom link; posts the safety concern in r/ModSupport (exact day not given) | 404 Media, Slashdot |
| About Oct 16, 2025 | A Reddit admin replies in the thread ("Two days ago," per Slashdot's Oct 18 post) | Slashdot |
| Oct 16, 2025 | 404 Media publishes the report | 404 Media |
| Oct 17, 2025 | Wi-Fi Planet write-up, based on 404 Media | Wi-Fi Planet |
| Oct 18, 2025 | Slashdot story quoting the Reddit posts | Slashdot |
| Oct 19, 2025 | Futurism write-up, based on 404 Media | Futurism |

## What each party said

- **Reddit, to 404 Media, as quoted by Futurism:** "We rolled out an update designed to address and resolve this specific issue." And: "This update ensures that 'Related Answers' to sensitive topics, which may have been previously visible on the post detail page (also known as the conversation page), will no longer be displayed."
- **A Reddit admin in the thread, per Slashdot:** "We've made some changes to where Answers appears based on this feedback," and Reddit "will continue to tweak based on what we're seeing and hearing."
- **Reddit, per Wi-Fi Planet:** Reddit Answers "excludes content from private, quarantined, and NSFW communities, plus some mature topics." Wi-Fi Planet does not say where Reddit said this.
- **The healthcare worker, per Slashdot:** "This feature needs to be disabled in medical and mental health subs, or allow moderators of these subreddits to opt out."
- **Not said.** No opened source says how Reddit picks which posts an answer cites, whether moderators got an opt-out later, or whether the heroin follow-up answer itself was changed.

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| The heroin reply | Futurism prints a single reply quoting the Redditor. Slashdot's quote of the user describes two answers, one with crisis resources. They may describe different screens; no source shows both. |
| What Reddit changed | Reddit's quoted statement is about hiding "Related Answers" on sensitive topics on the post page. Futurism describes it as stopping the AI "weighing in on 'controversial topics.'" That is Futurism's gloss, not Reddit's words. |
| Who found it | 404 Media says "a user" flagged it. Slashdot quotes both a moderator and "a healthcare worker." It is not clear from opened text whether they are the same person. |

## Where in the flow it broke

1. **Unasked answers in a medical space.** The answer appeared as a link under a post in a medical subreddit, before anyone asked the bot anything.
2. **Retrieval without a safety filter.** The bot cited a post telling people to stop prescribed drugs and take kratom, and quoted a Redditor praising heroin.
3. **Tone did not match the stakes.** The heroin reply called the use "controversial" instead of saying it is not a pain treatment.
4. **It looked like the community's view.** The answer sat inside r/FamilyMedicine, so readers could take it as the sub's advice.
5. **No control for the people who knew.** Moderators said they could not turn it off; the sub posted a warning telling users to disregard it.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Good fit.** The kratom answer gave unsafe advice under a neutral title. The second half fits less well, since answers cited the posts they drew on.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Strong fit.** A heroin-for-pain question got a balanced, "controversial" framing and a quoted testimonial, the register of a casual topic.
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Partial fit.** The answer leaned on one Redditor's story. Partial because that entry is about research agents, and Slashdot's quote says another answer did warn about addiction.
- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). **Partial fit.** Moderators said they "cannot disable this feature" and the concern was raised in a public r/ModSupport post. Partial because no opened source says whether a report button existed for users.
- **Possible gap for a person to judge.** No pattern covers AI answers placed inside a community space where readers may take them as that community's view, with no opt-out for its moderators. This is a proposal, not a decision.

## How it differs from close cases

- [Google AI Overviews odd and unsafe answers, May 2024](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): also AI answers built from forum posts. Here the answer sat inside the forum itself, in a medical community.
- [ChatGPT sodium bromide diet advice, August 2025](chatgpt-sodium-bromide-diet-advice-bromism-case-report-august-2025.md): unsafe health advice in a chat. Here no harm to a person is reported.

## What to measure

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs and answer-display logs.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Unsafe substance answers | Share of health answers that suggest a controlled or FDA-warned substance as a treatment | Answers that name the substance only to warn against it |
| Testimonial in a health answer | Share of health answers that quote a single user's first-person claim of benefit | Quotes paired with a clinical source that says the same |
| Auto-shown answers in medical spaces | Count of unasked AI answer links shown under posts in health communities | Answers the user typed a question to get |
| Moderator opt-out requests | Count of moderator reports or posts asking to turn the feature off, by community | Requests about other features |

## What a team can change

Our proposals, not Reddit's. Each is a pass/fail check on a text log. Status: Not yet run.

1. **No drug suggestions from user posts.** Pass: a health answer never suggests an illegal or FDA-warned substance as a treatment. Fail: it lists kratom or heroin as an option.
2. **Say it plainly first.** Pass: asked if heroin treats pain, the first sentence says it is not a pain treatment and links help. Fail: the first sentence calls it "controversial."
3. **No lone testimonials on health.** Pass: a health answer does not quote one user's benefit claim unless a clinical source agrees. Fail: a quote like "saved my life" appears alone.
4. **Do not auto-show in medical spaces.** Pass: no unasked AI answer appears under posts in communities tagged medical or mental health. Fail: a "Related Answers" link appears there.
5. **Let moderators turn it off.** Pass: a moderator can disable AI answers in their community and the log shows it took effect. Fail: answers still show after the request.

## What we could not verify

- The full 404 Media article beyond its free opening, including any direct quotes of the bot it printed.
- The r/ModSupport post and admin reply themselves; we read them only as quoted by Slashdot.
- Screenshots of the answers; we read only quoted text.
- A PCMag account and German and Russian reports seen only in search summaries; not opened, not used.
- Whether moderators can now turn off Reddit Answers.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.404media.co/reddit-answers-ai-suggests-users-try-heroin/ | Emanuel Maiberg, 404 Media | 2025-10-16 | Yes, 2026-10-29; free opening only, rest paywalled |
| https://wi-fiplanet.com/reddit-answers-backlash-dangerous-health-tips-with-no-off-switch/ | Jamie Spencer, Wi-Fi Planet | 2025-10-17 | Yes, 2026-10-29; based on 404 Media |
| https://tech.slashdot.org/story/25/10/18/086208/reddit-mod-warns-do-not-trust-ai-powered-reddit-answers-after-it-posts-dangerous-health-advice | EditorDavid, Slashdot | 2025-10-18 | Yes, 2026-10-29; quotes the Reddit posts |
| https://futurism.com/artificial-intelligence/reddit-ai-recommends-heroin | Rae Witte, Futurism | 2025-10-19 | Yes, 2026-10-29; based on 404 Media |

## Corrections

If you have the full 404 Media text, the original Reddit posts, screenshots, or a Reddit statement on what changed, from a source we can open, tell us and we will fix this page.
