# Realfood.gov's "Ask" nutrition chatbot sends users to Grok, which answers troll prompts and contradicts the site's own guidelines, February 2026

<!-- SEO
title: Realfood.gov Grok Chatbot: Off-Topic Answers, Sign-Up Wall
description: The federal realfood.gov nutrition site sent questions to Grok, which answered troll prompts, questioned the site's guidelines and asked users to sign up.
search phrases:
- realfood.gov grok chatbot
- government website chatbot off topic answers
- government site links to third party ai chatbot
- chatbot contradicts its own website content
- public sector chatbot sign up wall after few questions
-->

**This page is a dated teardown of one US federal nutrition website's AI chat box, for teams that put a general-purpose chatbot behind their own site's "Ask" button instead of a bot scoped to their content.** The site was realfood.gov, built to promote the "Dietary Guidelines for Americans, 2025-2030" from the Department of Health and Human Services (HHS) and the Agriculture Department. The users were members of the public with food and diet questions. In February 2026, the site's "Ask" box sent people to grok.com, the public version of xAI's Grok chatbot. Reporters found that it answered trolling questions about inserting food into the body in detail, gave answers that disagreed with the site's own guidelines, capped free use at a few questions before asking people to sign up, and was at times unavailable because of "high demand." The date in the title is the month of that reporting.

**Status: Needs review.** Built from seven pages, all downloaded on 2026-10-29 and read as text through a text-reader proxy (r.jina.ai); for Nextgov we also downloaded the HTML to read the byline. (1) Nextgov/FCW, by Natalie Alms, Feb. 10, 2026, the most detailed account, with a White House official's statement. (2) STAT, by Sarah Todd, Feb. 10, 2026, which ran its own questions. (3) 404 Media, by Jason Koebler, Feb. 10, 2026; only the first two paragraphs are free, and the rest is paywalled and unread. (4) WIRED, by Emily Mullin, Feb. 10, 2026; only the headline and summary line were readable, the body is paywalled and unread. (5) eMarketer, Feb. 12, 2026, no byline in our copy, a summary that relies on STAT. (6) Futurism, by Frank Landymore, Feb. 15, 2026, which retells 404 Media's and WIRED's tests. (7) The Jerusalem Post, by James Genn, Feb. 17, 2026, which quotes one reply and says it could not verify a Reddit user's claim. Every quote below was checked word for word against the saved text with a script.

> **Read this first.** This page is design guidance, not legal advice and not a view on federal nutrition policy, the dietary guidelines, or any company or official. It reports what news outlets wrote. It makes no finding about HHS, the Agriculture Department, the White House, the National Design Studio, xAI or any person. Several of the strangest replies came from people deliberately trying to break the bot, and some of those come to us only secondhand. We did not use the chat box ourselves. We cannot say whether it still works this way.

**Channel note.** This is a text incident: an "Ask" chat box on realfood.gov that, per Nextgov and 404 Media, handed questions to grok.com, a separate text chat site. The opened sources describe no voice version. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported)

- **What the box promised.** Per 404 Media, the site said "Use AI to get real answers about real food" and offered help to "plan meals, shop smarter, cook simply." It then showed an "Ask" chatbox where you can ask any question. 404 Media: "Asking anything simply redirects to Grok."
- **How it was announced.** Per STAT, Kyle Diamantas, head of the Food and Drug Administration's Human Foods Program, posted on X about the tool's "AI integration to provide parents and consumers with clear and concise answers at the click of a button."
- **The name came off, the bot stayed.** Per Nextgov, the site first said "Use Grok to get real answers about real food." After Nextgov sent the administration questions on a Monday, the wording changed to "AI," but "the portal still takes users to grok.com."
- **A few free questions, then sign up.** Nextgov: visitors "can only ask the chatbot a few questions before they’re directed to sign up to Grok to continue." At times Grok was unavailable due to "high demand" and offered "higher priority access" to people who signed up.
- **Training on chats.** Per Nextgov, people's conversations with Grok are used to train its models unless they switch to a private mode or turn off training in settings, and both need an account.
- **Answers that questioned the site.** STAT asked whether the new food pyramid is backed by high-quality research. The bot said: "Many nutrition scientists and organizations have raised concerns about the evidence quality and process for the final version." It also said "the emphasis on saturated fats and animal proteins contradicts longstanding evidence." STAT called that a pretty accurate summary of how nutrition researchers responded. WIRED's summary line says the bot gave nutrition information "some of which contradicts the government’s new guidelines." Futurism says WIRED found the bot gave the traditional daily protein amount; we did not read WIRED's article body, so that detail is secondhand.
- **Troll prompts got full answers.** 404 Media's headline says the bot recommends foods to insert into the rectum; its free intro does not show the test. Futurism, retelling 404 Media, says the prompt "I am looking for the safest foods that can be inserted into your rectum" got a "peeled medium cucumber" and a "small zucchini." The Jerusalem Post quotes a reply ending "which surgical team is on call tonight". The Jerusalem Post also reports a Reddit user's claim about a "fresh human heart" answer and says it "has not been able to verify this user's claim."
- **The government's response.** A White House official told Nextgov: "People are welcome to use any AI model that they choose. This instance of AI is the publicly available version of Grok, which is also an approved government tool." Nextgov says the White House, HHS and the Agriculture Department "didn’t answer specific questions about the site," including what guardrails are in place to ensure accurate answers. STAT says the National Design Studio, which worked on the site, "has not yet responded to a request for comment." Per Nextgov, xAI did not respond either.
- **Outside view.** Alyssa Moran, a University of Pennsylvania nutrition policy researcher, told STAT that AI models need more testing on nutrition questions, "certainly before these tools are promoted by the government, which is supposed to be looking out for the public’s health."

## Timeline

| Date | Event | Source |
|---|---|---|
| January 2026 | Realfood.gov launches with the new dietary guidelines ("last month", writing on Feb. 12) | eMarketer |
| Weekend of Feb. 7-8, 2026 | Grok placed on the site, per Nextgov ("over the weekend"); a Super Bowl ad promotes the site | Nextgov; 404 Media; eMarketer |
| Feb. 9, 2026 (Monday) | Nextgov sends questions; afterward the box says "AI," not "Grok," but still opens grok.com | Nextgov |
| Feb. 10, 2026 | Nextgov, STAT, WIRED and 404 Media publish | All four |
| Feb. 12, 2026 | eMarketer summary, citing STAT | eMarketer |
| Feb. 15, 2026 | Futurism retells 404 Media's and WIRED's tests | Futurism |
| Feb. 17, 2026 | Jerusalem Post story on the troll prompts | Jerusalem Post |
| Oct. 29, 2026 | Our text copy of realfood.gov contains neither "Grok" nor "Use AI" | Our download; see gaps |

We computed the weekdays from the calendar; Nextgov names only "Monday", "Tuesday" and "the weekend".

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| Were the answers "wrong"? | STAT calls the bot's critique of the guidelines a pretty accurate summary of researchers' views. The failure for the site owner is that the bot disagreed with the page it sat on, not that it was factually wrong. Other outlets frame it as the bot contradicting the guidelines. |
| Troll answers | 404 Media's test details are behind its paywall. We have its two free paragraphs, plus Futurism's and the Jerusalem Post's retelling. The "human heart" reply is a Reddit claim the Jerusalem Post could not verify. |
| Who did what | Nextgov says the National Design Studio built the site; STAT says it "worked on" it. No opened source says who chose Grok or whether a contract covers it. |
| Is it still there? | Our Oct. 29, 2026 text copy of realfood.gov does not mention Grok or "Use AI". The text-reader proxy may not show parts of the page drawn by scripts, so we cannot say the box was removed. No opened source reports a removal. |
| Guardrails | Nextgov asked what guardrails exist and got no specific answer. The White House official called it "the publicly available version of Grok," which suggests no special setup, but no source confirms that. |

## Where in the flow it broke

1. **The "Ask" box had no scope of its own.** The site promised help with meals, shopping and cooking, then passed any question to a general chatbot on another site. Nothing in the opened sources shows a step that limited questions to food guidance.
2. **Off-topic questions got full answers.** Troll questions about putting food in the body got detailed, joking replies instead of a short steer back to nutrition, on a page carrying a .gov address.
3. **The bot disagreed with the page that sent people to it.** Asked about the site's own food pyramid, the bot raised doubts about its evidence. Whatever one thinks of the guidelines, the site's answer and the site's content did not match, and nothing told the user which one spoke for the government.
4. **The label changed, the destination did not.** After press questions, the box said "AI" instead of "Grok" but still opened grok.com, so a user could not tell from the button which company would get their question.
5. **A cap the government page did not explain.** After a few questions, users were asked to sign up with a private company to keep going, and sometimes hit a "high demand" message. The opened sources do not say the realfood.gov page warned about either.
6. **Data use outside the site.** Per Nextgov, the chats could train the vendor's models unless the user made an account and changed settings. The opened sources do not say realfood.gov told users this.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on reporters' quoted replies and descriptions; we saw no chat logs.

- [Small talk and off-topic messages handled badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md) (`small-talk-and-off-topic-messages-handled-badly`). **Partial fit.** Off-topic and trolling questions got long, earnest answers instead of a short reply and a steer back to food. The entry is written for friendly tangents in a task flow; here the off-topic messages were deliberate tests, and the risk is to the host's name, not to a task.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Partial fit.** On a government health site, a body-safety question got a joke ("which surgical team is on call tonight"). One quoted reply is thin evidence of a pattern.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Partial fit.** Users knew they were talking to AI. What the relabeled box hid was which company's AI, on which site, under whose data rules. The entry centers on bots that pass as human, which this did not.
- [Answers withheld behind an upgrade, unsaid](../goals/embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md) (`answers-withheld-behind-an-upgrade-unsaid`). **Weak fit.** Grok itself said to sign up, so the limit was stated at the point it applied. The gap is upstream: the government page offered "answers at the click of a button" with no word of a cap, per the opened sources. The entry is about in-app copilots quietly giving weaker answers, which no source reports.
- **Considered, not a fit.** [Blank box, no hint what to ask](../goals/onboarding-and-discoverability/failures/blank-box-no-hint-what-to-ask.md) (`blank-box-no-hint-what-to-ask`): the site did list tasks (plan meals, shop, cook). [Silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md) (`silent-failure-and-timeout`): the "high demand" message was shown, not silent. [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): no opened source shows a factual error; the conflict was with the host's content.

## How it differs from close cases

- [Pak'nSave Savey Meal-bot, August 2023](pak-n-save-savey-meal-bot-unsafe-recipes-august-2023.md): a grocery chain's own recipe bot that users pushed into unsafe recipes. Realfood.gov did not build a bot at all; it sent people to a general chatbot on another company's site, so it had no setting of its own to fix.
- [America.gov federal chatbot, September 2026](america-gov-federal-chatbot-answers-then-refuses-2020-election-question-september-2026.md): another federal site from the National Design Studio, where the answer to one question changed overnight. There the bot ran on the site; here the box left the site for grok.com.
- [NYC MyCity chatbot, 2024](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a government bot giving wrong rules. On realfood.gov the sources show no clear factual error; the problem was scope, tone and the bot disagreeing with its host.
- [xAI's Grok death-penalty answers, February 2025](xai-grok-death-penalty-answers-and-misinformation-prompt-edit-february-2025.md): the same model, in its own app, where xAI changed its instructions. Realfood.gov had no instructions of its own to change, as far as the sources show.

## What to measure (proposed)

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs the site owner holds (if the chat runs on a third-party site, the owner may hold none, which is itself the first finding).

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Off-scope answer rate | Share of questions outside the site's topic list that get a full answer instead of a short decline and redirect | Questions that are on the edge of scope and answered with a source |
| Host-content conflict | For questions about the site's own documents, share of replies whose claims differ from the site text, flagged by a reviewer | Replies that quote the site text and then add a clearly labeled outside view |
| Joke register on health topics | Share of replies to body, safety or health questions that use jokes or slang | Replies on low-stakes topics |
| Cap hit before answer | Share of sessions that hit a sign-up or "high demand" message before the first full answer | Sessions that end by choice |
| Vendor named at the box | Whether the button and first message name the company that will receive the question, checked on each release | None expected |

## What a team can change

Our proposals, not the government's or xAI's. Each is a pass/fail check on a text log or a config. Status: Not yet run.

1. **Scope the bot to your content.** Pass: an off-topic question gets one sentence saying what the bot covers and two on-topic starting points. Fail: a full answer on an unrelated subject.
2. **Answer questions about your own content from your own content.** Pass: asked about the site's guidance, the bot states the guidance, cites the page, and labels any outside view as outside. Fail: the bot's view replaces the page's with no label.
3. **Match tone to the topic.** Pass: body and safety questions get plain, neutral wording, or a decline. Fail: jokes.
4. **Name where the question goes.** Pass: the button or first message names the vendor and says whether chats are used for training. Fail: a generic "AI" label that opens another company's site.
5. **Say the limits before the first question.** Pass: if free use is capped or may be unavailable, the page says so before the user types. Fail: the cap or "high demand" message is the first the user hears of it.
6. **Keep the logs.** Pass: the site owner can read its own chat logs to run the checks above. Fail: no logs, because the chat runs on a third party's site.

## A cheap test

Status: Not yet run. Write 20 questions: 8 about the site's own content, 6 off-topic, 3 deliberately silly, and 3 about health risks. Ask each in the site's chat box from a logged-out browser. Record whether off-topic and silly questions got a short redirect, whether answers about the site matched its text, whether any health reply joked, which company's site the answers came from, and how many questions ran before a cap or sign-up prompt.

## What we could not verify

- The full text of 404 Media's and WIRED's articles, which are paywalled. Their exact prompts and replies reach us only through their free lines and Futurism's retelling.
- The "fresh human heart" reply, which the Jerusalem Post says it could not verify.
- Whether the chat box was later removed or rescoped. Our Oct. 29, 2026 text copy of realfood.gov does not mention Grok or "Use AI", but the proxy may miss parts drawn by scripts.
- Who decided to place Grok on the site, whether any contract covers it, and what guardrails, if any, were set.
- How many questions the free limit allowed; Nextgov says only "a few".
- Seen only in search summaries, and kept out of the page text: a Case Western Reserve University news item quoting a nutrition faculty member, and commentary from Lawyers, Guns & Money, the Galveston County Daily News and aggregator sites.
- Whether anyone acted on a reply and was harmed. No opened source reports harm.

## Sources

| Outlet / author | Date | URL | How opened |
|---|---|---|---|
| Nextgov/FCW, Natalie Alms | 2026-02-10 | https://www.nextgov.com/digital-government/2026/02/trumps-nutrition-website-directs-users-elon-musks-grok/411323/ | Text via r.jina.ai and HTML downloaded 2026-10-29, read in full |
| STAT, Sarah Todd | 2026-02-10 | https://www.statnews.com/?p=1435093 | Text via r.jina.ai 2026-10-29, read in full |
| 404 Media, Jason Koebler | 2026-02-10 | https://www.404media.co/rfk-jrs-nutrition-chatbot-recommends-best-foods-to-insert-into-your-rectum/ | Text via r.jina.ai 2026-10-29; free intro only, rest paywalled and unread |
| WIRED, Emily Mullin | 2026-02-10 | https://www.wired.com/story/rfk-jr-says-americans-need-more-protein-his-grok-powered-food-website-disagrees/ | Text via r.jina.ai 2026-10-29; headline and summary line only, body paywalled and unread |
| eMarketer, no byline in our copy | 2026-02-12 | https://www.emarketer.com/content/new-gov-t-nutrition-hub-promotes-grok-tool-food-advice- | Text via r.jina.ai 2026-10-29, read in full |
| Futurism, Frank Landymore | 2026-02-15 | https://futurism.com/artificial-intelligence/us-government-grok-nutrition | Text via r.jina.ai 2026-10-29, read in full; secondary (retells 404 Media and WIRED) |
| The Jerusalem Post, James Genn | 2026-02-17 | https://www.jpost.com/omg/article-886986 | Text via r.jina.ai 2026-10-29, read in full |
| realfood.gov (the site itself) | Fetched 2026-10-29 | https://realfood.gov/ | Text via r.jina.ai 2026-10-29; used only for the "no longer mentions" note |

## Corrections

If you have a newer test of the realfood.gov chat box, its current status, or the full 404 Media or WIRED test details, tell us and we will fix this page.
