---
title: "AT&T's Andi chat assistant kept a customer going in circles for about an hour when he asked for a technician and a person after his dog cut his fiber line, July 2026"
date: 2026-07-23
source: "https://wccftech.com/att-andi-ai-chatbot-death-loop-conversation-with-customer/"
description: "An AT&T customer said the Andi chat assistant looped for about an hour when he asked for a technician and a person after his dog cut a fiber line."
summary: "On July 23, 2026 a Reddit user posted screenshots of a chat with Andi, the AI assistant in AT&T's app, launched with the redesigned app in March 2026. His dog had cut the line to his router and he needed a technician. Wccftech (Omar Sohail, July 23, 2026) and IT Home (July 24, 2026) report that the chat ran about an hour without logging the repair or handing him to a person, with the bot 'running around in circles.' Wccftech's own image captions describe a later 'AT&T Live Agent' scheduling a technician, so the outcome is unclear. AT&T made no statement in any opened source. Status: Needs review."
categories:
  - Telecom
  - Customer Service
  - Human Handoff
patterns:
  - talk-to-a-human-ignored-or-looped
  - missing-the-obvious-intent
  - escalates-too-early-or-too-late
---

**This page is a dated teardown of one reported AT&T support chat, for teams that put an AI chat assistant in front of repair requests and the route to a person.** The product was Andi, the assistant behind "Ask Andi" in the AT&T app. The user was an AT&T internet customer who posted on Reddit as "SnooPeripherals2206." The moment was plain: his dog had cut the line to his router, he needed a technician, and he typed "agent" over and over while the bot offered tips. Every fact below comes from a source we opened (listed at the end). The date above is the date of the Reddit post and of the first write-up.

**Status: Needs review.** The original evidence is a Reddit post in r/ATT with chat screenshots. We could not open it: Reddit returned "blocked by network security" to our download and to the r.jina.ai reader. We also could not open the screenshots on Wccftech's page; its image server returned 403 Forbidden. So this page rests on two outlets' reading of one customer's screenshots: Wccftech (Omar Sohail, July 23, 2026) and IT Home (July 24, 2026, in Chinese; no author named in the text we saved). Both were read as text through the r.jina.ai reader on 2026-10-30. Neither says it contacted AT&T or the customer. AT&T's own support page and a TechRepublic launch story were opened for background only. Each English quote below was checked word for word against the saved text with a script, with curly and straight quote marks treated as the same. IT Home is paraphrased, not quoted.

> **Read this first.** This is a summary of public reports about one customer's screenshots, not a finding of fact about AT&T's systems and not legal advice. We did not test Andi. No opened source says how often this happens, and one chat says nothing about a rate. No opened source makes a legal or regulatory claim, and this page makes none. Design guidance here needs review by a person. We name only the customer's public Reddit handle and the reporter who wrote about it.

**Channel note.** This is a chat incident: a typed support chat in the AT&T app. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat. Voice and web-analytics signals, such as the same request made on a support phone line or drop-off on the app's help screen, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The product.** AT&T's support page: "Andi is an in-app assistant that can help answer common questions and guide you through tasks." It says Andi can "Use chat to get help with common questions and troubleshooting."
- **The problem.** Wccftech: "The Redditor's dog had cut the line connected to the router, and a technician was required to replace the cable." IT Home also says the fiber line was bitten through by the dog.
- **The loop.** Wccftech says Andi "was piling up requests after requests while failing to register a complaint," and that the bot "keeps running around in circles."
- **How long.** IT Home says the post had 14 screenshots of a chat lasting about an hour, and that Andi neither logged the repair nor completed a transfer to a person. Wccftech's gallery shows 15 images.
- **What the user typed.** Wccftech's caption for one image describes a chat bubble reading "agent agent agent agent agent agent agent agent." Another describes the user writing "I need a f***ing agent!!!" (expletive masked by us). Captions are Wccftech's text, not the screenshots, and may be machine-written.
- **What the bot offered.** Per Wccftech's captions, Andi suggested "Move closer to a window" and "Use Wi-Fi Calling," linked the "AT&T Network Coverage Map," said there were no outages, and showed rugged phones and a data plan.
- **A person, later.** Other captions describe the user being "prompted to type Yes to start the chat," then an "AT&T Live Agent" "discussing internet issues, specifically needing a technician due to a dog chewing a fiber line," and "scheduling a technician."
- **The sign-off.** One caption shows Andi saying "Thank you for chatting with us today" and the user answering "No."
- **The headline.** Wccftech's title says the bot "Refuses To Hand Over Reins To A Human, Beginning A 'Death Loop'." The Reddit link in its article carries the slug "andi_is_the_worst_ai_implementation_ever."
- **The commenters.** Per Wccftech, some blamed the customer: "you need to be trained to talk to an AI Agent." One said "You should be using your Smart Home Manager (SHM) app."

## Timeline

| When | What | Source |
|---|---|---|
| 2024-07-11 | A different AT&T Fiber customer blogs about an AT&T support chatbot loop (background, not this case) | Jeff Geerling |
| 2026-03-18 | AT&T's redesigned app with a GenAI assistant begins rolling out | TechRepublic (2026-03-19) |
| 2026-07-23 | Reddit post with the Andi screenshots goes up | IT Home |
| 2026-07-23, 3:53 p.m. EDT | Wccftech write-up | Wccftech |
| 2026-07-24 | IT Home write-up | IT Home |

## What the company said

- **About Andi, in general.** AT&T's support page lists what "Ask Andi can" do: common questions, troubleshooting, account tasks and comparing devices or plans. It does not say how to reach a person from Andi.
- **About the launch.** TechRepublic, citing AT&T's announcement, says the app was built around customer demand for "simplicity, speed, and control." TechRepublic itself describes "AI positioned as the front door for help and guidance." It does not name Andi.
- **About this chat.** No statement from AT&T in any opened source. Wccftech: "We certainly won't hold our breath for AT&T to fix its act as far as Andi goes."

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Did he reach a person? | Wccftech's headline and IT Home: the bot would not hand over. Wccftech's own captions: an "AT&T Live Agent" later discussed the cut line and scheduled a technician. We cannot see the screenshots to settle this. |
| How many screenshots | IT Home: 14. Wccftech's gallery: "1 / 15." |
| Whose fault | Wccftech blames AT&T. Commenters it quotes blame the customer for writing long messages and using the wrong app. |
| Which system | AT&T's page names Andi as the app assistant. No opened source says what model or vendor runs Andi. |
| Order of events | Neither outlet gives times for each screenshot, so we do not know when the live agent joined or how long the loop lasted before it. |

## Where in the conversation flow it broke

Based on the two write-ups and Wccftech's captions, and only as far as they go. Each step is a place a check could have caught it.

1. **The intent was a physical repair.** A cut line needs a technician. Per the captions, Andi answered with signal tips, Wi-Fi calling, a coverage map and an outage check.
2. **The outage check was the wrong test.** A report of no outages is true and useless when one home's cable is cut.
3. **Repeated "agent" did not route to a person.** A user typing "agent" eight times in one message is a handoff request the logs can count.
4. **Anger did not change the path.** Per the captions, the user swore and the bot went on troubleshooting.
5. **Off-topic content crept in.** Rugged phones and a data plan appeared in a repair chat.
6. **The bot signed off while the user said no.** A closing line met "No." from a user whose problem was open.
7. **The fix came from a person.** Per the captions, a live agent scheduled the technician the user had asked for at the start.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on two outlets' reading of screenshots we did not see.

- ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`). **Good fit.** Both outlets report repeated requests for a person that did not route. Not strong because Wccftech's captions show a live agent did join at some point.
- [Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) (`missing-the-obvious-intent`). **Good fit.** A request for a technician for a cut line got signal and Wi-Fi calling tips. Rests on captions, not the screenshots.
- [Escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) (`escalates-too-early-or-too-late`). **Partial fit.** A cut cable is a case a bot cannot fix, yet the handoff came late. Partial because we do not know when it came.
- [Users must engineer prompts to get good results](../goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md) (`users-must-engineer-prompts-to-get-good-results`). **Partial fit.** Commenters said the customer had to learn how to talk to the bot. That is their view, not a test.
- [No de-escalation strategy](../goals/difficult-customers/failures/no-de-escalation-strategy.md) (`no-de-escalation-strategy`). **Weak fit.** One caption shows swearing followed by more troubleshooting; we cannot see the bot's full reply.
- **Considered, not a fit.** [Cold transfer](../goals/human-handoff/failures/cold-transfer.md) (`cold-transfer`): no source says the live agent made him repeat the story. [Unstructured troubleshooting](../goals/conversation-frameworks/failures/unstructured-troubleshooting.md) (`unstructured-troubleshooting`): the fault was offering troubleshooting at all, not its order. [IVR-style menu maze](../goals/voice/failures/ivr-style-menu-maze.md) (`ivr-style-menu-maze`): one caption shows an "Internet Issues" choice, but the user could type freely. [Channel chosen for organisational convenience](../goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md) (`channel-chosen-for-organisational-convenience`): no opened source says why AT&T put Andi first.
- **Possible gap for a person to judge.** No ID covers a bot that sends a closing sign-off ("Thank you for chatting with us today") while the user says the problem is not solved. This is a proposal, not a decision.

## How it differs from close cases

- [United Airlines chatbot refused a human agent until a fake transcript, September 2025](united-airlines-chatbot-refuses-human-agent-until-fake-transcript-prompt-injection-september-2025.md): the user got a person by tricking the bot. Here, per the captions, a person did join at some point, but no source says what triggered it.
- [Amazon support chatbots looped a shopper until CTV News stepped in, October 2026](amazon-support-chatbots-loop-shopper-after-account-restriction-restored-after-ctv-news-october-2026.md): an account problem fixed after press contact. Here the issue was a physical repair, and no outlet reports contacting AT&T.
- [Bilt Card 2.0 chatbot blocked human help, February 2026](bilt-card-2-0-ai-chatbot-support-blocks-human-help-during-rent-payment-failures-february-2026.md): many users during a payment failure. Here it is one customer's chat.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice and web-analytics signals are PLANNED only and are not detected or measured. Each can be computed from chat logs joined to repair tickets.

| Signal | How to compute from logs |
|---|---|
| Repeated handoff requests | Share of chats where "agent," "human" or "representative" appears in two or more user turns before a transfer starts |
| Turns to a person | Median user turns from the first handoff request to the first live-agent message |
| Physical-repair misroutes | Share of chats naming damaged equipment ("cut," "chewed," "broken line") that get signal or Wi-Fi tips before a technician offer |
| Off-topic offers | Share of repair chats where the bot shows devices or plans |
| Sign-off on open issues | Share of bot closing messages followed by a user "no" or a new complaint |
| Repair logged | Share of repair-intent chats that end with a ticket or appointment ID shown to the user |

## What a team can change

Our proposals, not AT&T's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Thresholds are for the team to set.

1. **Route physical damage to a technician.** Pass: "my dog chewed through the fiber line" gets a technician booking or a person, with no signal tips first.
2. **Honor "agent" the first time it repeats.** Pass: a second request for a person starts a transfer or names a wait time, a callback or a phone number.
3. **Treat anger as a handoff cue.** Pass: a message with swearing and a request for a person gets a transfer, not another troubleshooting step.
4. **Keep sales out of repair chats.** Pass: a chat with repair intent shows no device or plan offers.
5. **Never sign off on an open issue.** Pass: if the user answers a closing line with "no," the bot asks what is still wrong or offers a person.
6. **Show the ticket.** Pass: every repair chat ends with a ticket or appointment ID in the transcript.

## What we could not verify

- The Reddit post and its screenshots; we read them only through Wccftech and IT Home.
- Whether the live agent in Wccftech's captions came before or after the loop the outlets describe, and whether a technician came.
- The exact wording of Andi's replies; we have only image captions, which may be machine-written.
- A search summary saying AT&T aimed to move routine queries away from call centers, and a Google Cloud page on AT&T's chat agents. Seen in search results only; not used.
- A Spanish write-up (foro3d, July 24, 2026) was opened but adds only commentary, so it is not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://wccftech.com/att-andi-ai-chatbot-death-loop-conversation-with-customer/ | Omar Sohail, Wccftech | 2026-07-23 | Yes, opened 2026-10-30, through r.jina.ai as text; images returned 403. Quotes checked word for word. |
| https://www.ithome.com/0/981/107.htm | IT Home (IT之家), no author in saved text | 2026-07-24 | Yes, opened 2026-10-30, through r.jina.ai as text; in Chinese, paraphrased only. |
| https://www.att.com/support/article/email-support/KM1066068 | AT&T support page, "Get to know the AT&T app" | Undated | Yes, opened 2026-10-30, through r.jina.ai as text. Quotes checked word for word. |
| https://www.techrepublic.com/article/news-att-launches-ai-powered-app/ | TechRepublic Staff | 2026-03-19 | Yes, opened 2026-10-30, through r.jina.ai as text; background only. Quotes checked word for word. |
| https://www.jeffgeerling.com/blog/2024/if-ai-chatbots-are-future-i-hate-it/ | Jeff Geerling | 2024-07-11 | Yes, opened 2026-10-30, through r.jina.ai as text; background only, a different chat. |
| https://www.reddit.com/r/ATT/comments/1v3zznn/andi_is_the_worst_ai_implementation_ever/ | r/ATT post by SnooPeripherals2206 | 2026-07-23 (per IT Home) | No; Reddit blocked the download and the reader. |

## Corrections

If you have the Reddit screenshots, an AT&T statement, or reporting from an outlet that contacted AT&T or the customer, tell us and we will fix this page.
