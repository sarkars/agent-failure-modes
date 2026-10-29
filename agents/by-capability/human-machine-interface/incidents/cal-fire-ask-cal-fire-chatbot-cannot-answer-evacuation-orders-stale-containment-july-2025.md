# California's "Ask CAL FIRE" chatbot could not answer evacuation questions and gave six-day-old containment data, CalMatters test, July 2025

<!-- SEO
title: Ask CAL FIRE Chatbot Fails Evacuation Questions in Test
description: A CalMatters test found California's Ask CAL FIRE chatbot could not answer evacuation questions and gave fire containment data six days out of date.
search phrases:
- ask cal fire chatbot evacuation orders
- cal fire ai chatbot calmatters test
- wildfire chatbot outdated containment
- government chatbot different answers same question
- emergency information chatbot no human handoff
-->

**This page is a dated teardown of one US state agency's public wildfire chatbot, for teams that run a government or emergency-information bot that answers from the agency's own website.** The product was "Ask CAL FIRE," an AI chatbot on fire.ca.gov from the California Department of Forestry and Fire Protection (Cal Fire), built by the vendor Citibot. The users were Californians looking for wildfire facts and preparedness help. Governor Gavin Newsom announced it on May 9, 2025. On July 9, 2025, CalMatters published its own test: the bot gave different answers when a question was reworded, could not tell users about evacuation orders, and reported a fire's containment from data six days old. The date in the title is the month of that report.

**Status: Needs review.** Built from six sources, all opened and saved as text on 2026-10-29. (1) CalMatters, by Malena Carollo, posted July 9, 2025 and marked "Updated July 10, 2025"; the page does not say what changed. (2) The Markup, the same story by Malena Carollo, July 9, 2025. (3) KFI AM 640, a short write-up bylined "iHeartRadio," July 9, 2025, which retells CalMatters' findings. (4) Planetizen, by Diana Ionescu, July 10, 2025, a summary that quotes the story. (5) The governor's launch release, May 9, 2025, (6) a launch story from CBS News (CBS San Francisco) by Melanie Corry, May 9, 2025. Every outlet reporting on the test relies on one CalMatters test; KFI and Planetizen add no testing of their own. All pages were downloaded directly as HTML and read as text. Every quote below was checked word for word against the saved text with a script.

> **Read this first.** This page is design guidance, not legal advice and not a view on state AI policy or wildfire response. It reports what news outlets and the governor's office wrote. It makes no finding about Cal Fire, Citibot or any official. The test is one newsroom's test from 2025; we do not know whether the bot still behaves this way. CalMatters says the bot gave no incorrect answers in its queries; the problems were missing, inconsistent and out-of-date answers. We did not use the bot ourselves.

**Channel note.** This is a text incident: a chat box on Cal Fire's website, per the governor's release and CBS. The opened sources describe no phone line or voice version. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported)

- **What the bot is.** The governor's release says Ask CAL FIRE "provides quick, reliable answers to commonly asked questions" from Cal Fire's website, "offering support in 70 languages." It describes the goal as access to "critical fire prevention resources and near-real-time emergency information." Per CBS, the bot "will not connect users to a representative" and gives information on fires of 10 acres or more.
- **Sources and vendor.** Per CalMatters, the bot answers from the Cal Fire website and ReadyForWildfire.org. It was built by Citibot, a South Carolina company, and Cal Fire plans to host it until at least 2027, according to procurement records CalMatters cites.
- **What worked.** CalMatters says questions about active fires and basic facts about the agency got accurate answers.
- **Same question, different words, different answer.** Only "What should I have in my evacuation kit?" returned a list of items. Versions using "go bag," "wildfire ready kit" and "fire preparedness kit" got a pointer to the Ready for Wildfire site, or "I’m not sure about the specific items you should have" plus the link. CalMatters notes two of those terms appear on the site the bot used.
- **No evacuation answers.** CalMatters: the bot "is unable to provide information about evacuation orders associated with fires." Asked who issues evacuation orders, it sometimes said law enforcement and other times said it did not know.
- **Old data labeled "latest."** Asked whether the Ranch Fire in San Bernardino County (4,293 acres) was contained, the bot said the "latest" update, as of June 10, showed 50% containment. Per CalMatters, that was six days out of date; the fire was 85% contained by then.
- **A flat no that was wrong.** Asked about job openings, the bot said there were none. CalMatters found two Cal Fire positions open on the state job site at the time.
- **"What can you help me with?"** In early May the bot replied "Sorry I don’t have the answer to that question right now". By mid-June it listed topics such as current fires, job classifications and programs.
- **Cal Fire's response.** Deputy chief of communications Issac Sanchez said it is reasonable to expect evacuation answers, and that when there are none the bot should say "there doesn’t appear to be any evacuations associated with this incident." He said a team of about four tested the bot before launch with questions they expected, and that the agency is improving answers by reviewing what people ask. His message: "be patient."
- **Outside view.** Stanford law professor Daniel Ho: "Evaluation is not an afterthought." Mila Gascó-Hernandez (University at Albany) said people in a fire will not stop to ask "what’s the nice way to ask the chatbot?"

## Timeline

| Date | Event | Source |
|---|---|---|
| May 9, 2025 | Newsom announces Ask CAL FIRE on fire.ca.gov | Governor's release; CBS News |
| Early May 2025 | Bot answers "What can you help me with?" with "Sorry I don’t have the answer…" | CalMatters |
| Mid-June 2025 | That reply now lists topics the bot covers | CalMatters |
| About six days after June 10, 2025 | Bot reports the Ranch Fire as 50% contained "as of June 10"; it was 85% | CalMatters (exact query date not given) |
| July 9, 2025 | CalMatters and The Markup publish the test; KFI retells it | CalMatters; The Markup; KFI |
| July 10, 2025 | CalMatters page marked updated; Planetizen summary | CalMatters; Planetizen |

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| Were the answers "wrong"? | CalMatters says it found no incorrect answers, yet reports the bot saying there were no job openings when two existed, and stale containment. KFI's headline says the bot "Struggles With Accurate Info." We report the specific findings, not either label. |
| What changed on July 10 | CalMatters shows "Updated July 10, 2025" with no correction note we could find. |
| Query dates | CalMatters gives "early May" and "mid-June" for two queries and implies about June 16 for the Ranch Fire query; it gives no full test log or count of questions. |
| Fixes | Sanchez said improvements were under way. No opened source retested the bot after July 2025. |
| Independence | KFI and Planetizen only restate CalMatters. There is one test behind all of the findings. |

## Where in the flow it broke

All steps come from CalMatters' test.

1. **Exact wording decided the answer.** The "evacuation kit" wording got a list; the "go bag," "wildfire ready kit" and "fire preparedness kit" versions got a link or an "I’m not sure" reply, though two of those terms appear on the source site. The user had to guess the bot's preferred phrase.
2. **The highest-stakes question had no path.** Evacuation orders were out of reach, and the question of who issues them got law enforcement one time and a did-not-know reply another. The bot did not say where to look instead (the opened sources do not say it named a county alert system or sheriff).
3. **Old numbers came back as current.** The bot called a six-day-old containment figure the "latest" update. During a fire, that reads as now.
4. **A flat no that really meant missing data.** The job question got a flat no, when the bot's sources apparently lacked the state job listings.
5. **The bot could not describe itself.** At launch, "What can you help me with?" got a could-not-answer reply.
6. **No person behind it.** Per CBS, the bot does not connect users to a representative. The opened sources do not report a resident harmed by this.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on CalMatters' quoted replies; we saw no chat logs.

- [Users must engineer prompts to get good results](../goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md) (`users-must-engineer-prompts-to-get-good-results`). **Good fit.** Only one phrasing of the kit question got the list; three common synonyms did not.
- [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`). **Good fit for May 2025, since fixed per CalMatters.** "What can you help me with?" got "Sorry I don’t have the answer…". The entry is written for in-app copilots; this was a public web bot.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** The containment reply carried a date ("as of June 10"), which is a cue a reader could check, but it called that figure the "latest." The job reply (no openings) had no hedge. CalMatters itself says it found no incorrect answers.
- [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`). **Partial fit.** Per Sanchez, a team of about four tested with questions they expected the public to ask. The entry is about typos and noisy input; here the gap was ordinary synonyms, not messy text.
- **Considered, not a fit.** [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`): the "go bag" reply was one link with an "I’m not sure," not a list of resources. [Dead-end "I don't understand" replies](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) (`dead-end-i-don-t-understand-replies`): the could-not-answer replies came with a link or a prompt to ask about the site, so they were not bare dead ends. ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`): no opened source reports anyone asking for a person. [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`): no source quotes the bot's tone on a high-stakes question.

## How it differs from close cases

- [Denver's Sunny 311 chatbot, October 2026](denver-sunny-311-chatbot-outdated-links-misread-questions-council-rejects-contract-october-2026.md): the same vendor, Citibot, answering from a government site. Sunny's test showed stale links and a misread place name; Ask CAL FIRE's showed stale numbers inside the answer and wording sensitivity, on a topic where minutes can matter.
- [California community college chatbots, CalMatters test, March 2026](california-community-college-chatbots-wrong-answers-calmatters-test-march-2026.md): the same newsroom testing public bots. The college bots stated wrong names and hours; the Cal Fire test found missing and out-of-date answers instead.
- [Hall County, Georgia Ask Hall County chatbot, April 2026](hall-county-georgia-ask-hall-county-chatbot-wrong-tag-title-and-property-tax-answers-april-2026.md): the agency itself warned residents. In California the agency defended the bot and asked for patience.

## What to measure (proposed)

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Paraphrase gap | For grouped questions with the same meaning, share of groups where one phrasing gets a full answer and another gets "not sure" | Groups where the phrasings truly ask different things |
| Data age in live answers | For replies with incident numbers (containment, acres), hours between the data's "as of" time and the reply time | Replies about closed incidents |
| "Latest" on stale data | Replies that call a figure the latest or current while citing data older than the team's set limit | Replies that give the date and say it may be out of date |
| Unanswerable safety topic | Share of evacuation-related questions that end with no answer and no named place to look | Replies that name the right local alert source |
| Flat no from missing data | Replies that say there are none of something the bot's sources do not cover | Replies that say the bot cannot see that data and link where it lives |
| Self-description failure | Share of questions asking what the bot can do that that get a could-not-answer reply | None expected |

## What a team can change

Our proposals, not Cal Fire's or Citibot's. Each is a pass/fail check on a text log or a config. Status: Not yet run.

1. **Map synonyms to the same answer.** Pass: "go bag," "evacuation kit" and "fire preparedness kit" return the same list. Fail: one returns the list and another returns "not sure."
2. **Date every live number and warn when it is old.** Pass: a containment figure shows its time and, past the team's set age, says it may be out of date and links the live incident page. Fail: an old figure is called "latest."
3. **Never leave evacuation questions blank.** Pass: if the bot cannot see orders, it says so and names where orders are posted (the team decides the right sources). Fail: a did-not-know reply with no next step.
4. **Say the data is out of reach, not that there is none.** Pass: when a topic is outside the bot's sources, it says so and links where the data lives. Fail: it says there are none.
5. **Answer the what-can-you-do question on day one.** Pass: the launch build answers it with a short list of topics. Fail: a could-not-answer reply.
6. **Test with outside phrasings before launch.** Pass: the pre-launch question set includes phrasings from people outside the team, and its results are kept. Fail: only staff-written questions.

## A cheap test

Status: Not yet run. Write 15 core questions, each in four phrasings, including slang ("go bag") and one about evacuations for a named active incident. Ask each in the chat. Record whether all four phrasings got the same answer, the "as of" time of any live number against the agency's live page, and whether every can't-answer reply named a place to look.

## What we could not verify

- Whether the bot was fixed after July 2025, or still runs; no opened source retested it.
- What changed in the CalMatters update of July 10, 2025.
- The full CalMatters question list, test count, and exact query dates.
- The procurement records CalMatters cites, and any contract amount; we did not open them.
- Seen only in search summaries, and kept out of the page text: an audio button that reads answers aloud, and launch coverage from CTIF, Babl AI, AI Business, KRCR, GovTech and KVIA.
- Whether any resident relied on the bot during a real evacuation.

## Sources

| Outlet / author | Date | URL | How opened |
|---|---|---|---|
| CalMatters, Malena Carollo | 2025-07-09 (updated 2025-07-10) | https://calmatters.org/economy/technology/2025/07/cal-fire-chatbot/ | HTML downloaded 2026-10-29, read as text |
| The Markup, Malena Carollo | 2025-07-09 | https://themarkup.org/artificial-intelligence/2025/07/09/californias-fire-protection-agency-made-an-ai-chatbot-dont-ask-it-about-evacuation-orders | HTML downloaded 2026-10-29, read as text |
| KFI AM 640, bylined "iHeartRadio" | 2025-07-09 | https://kfiam640.iheart.com/content/2025-07-09-cal-fires-ai-chatbot-struggles-with-accurate-info/ | HTML downloaded 2026-10-29, read as text |
| Planetizen, Diana Ionescu | 2025-07-10 | https://www.planetizen.com/news/2025/07/135506-cal-fire-chatbot-fails-answer-basic-questions | HTML downloaded 2026-10-29, read as text |
| Office of the Governor of California | 2025-05-09 | https://www.gov.ca.gov/2025/05/09/california-launches-new-ai-powered-chatbot-that-provides-wildfire-resources-in-70-languages/ | HTML downloaded 2026-10-29, read as text |
| CBS News (CBS San Francisco), Melanie Corry | 2025-05-09 | https://www.cbsnews.com/sacramento/news/cal-fire-artificial-intelligence-wildfire-information/ | HTML downloaded 2026-10-29, read as text |
| Route Fifty (republication of the story) | 2025-07 | https://www.route-fifty.com/artificial-intelligence/2025/07/californias-fire-protection-agency-made-ai-chatbot-dont-ask-it-about-evacuation-orders/406597 | HTML downloaded 2026-10-29; not used for any claim |

## Corrections

If you have a newer test of Ask CAL FIRE, what changed in the July 10 update, or the bot's current status, tell us and we will fix this page.
