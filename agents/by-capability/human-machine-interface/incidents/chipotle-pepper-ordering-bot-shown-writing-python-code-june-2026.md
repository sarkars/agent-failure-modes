---
title: "Chipotle's Pepper ordering bot shown writing Python code, then rewired into a free coding agent, while Chipotle called the viral post Photoshopped, 2026"
date: 2026-06-04
source: "https://gizmodo.com/should-you-hijack-a-corporate-ai-chatbot-for-free-tokens-2000767595"
description: "Viral 2026 posts showed Chipotle's Pepper support bot writing Python. Chipotle told CIO the post was faked; Gizmodo says the bot was later changed."
summary: "In March 2026, posts spread showing Chipotle's Pepper ordering and support chatbot answering coding questions and writing Python code. On April 9, 2026, CIO reported that Chipotle's external communications manager said by email that the viral post was Photoshopped and that Pepper neither uses gen AI nor can code. On June 4, 2026, Gizmodo reported that a developer had reverse-engineered Pepper's backend and that another built ChipotlAI Max, a coding tool that routed requests to Pepper, and that Chipotle then modified its product so its API could not be taken again. The sources disagree on whether Pepper ever wrote code. Status: Needs review."
categories:
  - Customer Service
  - Trust
  - Security
patterns:
  - small-talk-and-off-topic-messages-handled-badly
  - doesn-t-say-what-it-can-do
  - over-refusal-of-ordinary-requests
---

**This page is a dated teardown of public reporting on Chipotle's Pepper chatbot being shown, and then used, as a free coding assistant in 2026, for teams that run a customer-facing chatbot with a narrow job such as ordering or support.** The product was Pepper, Chipotle's ordering and support chatbot. The users were developers who asked it questions that had nothing to do with burritos. The moment was a support chat in which, per the posts Gizmodo describes, a request for coding help got Python code back. Chipotle says that post was faked. Every fact below comes from a source we opened (listed at the end). No opened source has Chipotle's transcripts, its bot's setup, or a count of off-topic sessions. The date above is the day of the Gizmodo report; the posts began in March 2026.

**Status: Needs review.** CIO (Evan Schuman, April 9, 2026), Gizmodo (Webb Wright, June 4, 2026) and a Substack post by Mark Wunsch (June 5, 2026; opinion) were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. The viral screenshots, the X and Instagram posts, and the ChipotlAI Max GitHub page were not opened; they appear here only as the outlets above describe them.

> **Read this first.** This is a summary of public reporting and company statements, not a finding of fact and not legal advice. It does not say whether Pepper ever wrote code: the main opened sources disagree, and Chipotle says the viral post was fake. It does not say whether anyone broke a law or Chipotle's terms; the lawyers quoted below give views, not rulings. We name only people who were quoted or named in the reporting.

**Channel note.** This is a chat incident: a text chatbot for ordering and support, reached on the web and, per Gizmodo, launched on Facebook Messenger. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat. Voice and web signals, such as a drive-thru voice bot asked off-topic questions, or scripted traffic to a web chat endpoint, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The bot.** Gizmodo calls Pepper a "concierge bot" that launched on Facebook Messenger in the summer of 2020 for placing orders. It says Pepper uses Amelia, a conversation system built by IPSoft, not ChatGPT.
- **March 2026: the coding posts.** Gizmodo: Pepper drew attention in March when developers found "it could respond to complex coding questions, and even write new Python code." Gizmodo embeds an Instagram post but does not say it ran its own test.
- **The widely shared example.** CIO says social media was "flooded with supposed examples" of customer bots doing unrelated work, including "one at Chipotle, which Chipotle claims was fake." CIO adds: "A much-referenced example supposedly from a Chipotle bot is unconfirmed." CIO's sources discuss a request to "reverse a linked list in Python" as the typical case.
- **From a chat trick to a tool.** Gizmodo reports that developer Maksim Soltan reverse-engineered "the backend protocol powering Pepper's chat function" and called the result "free inference via fast food." Rob Dezendorf, a Brooklyn "creative technologist," then wired Pepper into OpenCode, an open-source coding tool, and named it ChipotlAI Max.
- **The disclaimer.** Gizmodo quotes the project page: "Not affiliated with Chipotle. They will probably sue us. Worth it." Gizmodo says the project had 824 stars on GitHub "as of early Thursday afternoon" and dozens of forks.
- **A template for other bots.** Gizmodo says the project page gives a step-by-step guide for doing the same to support bots run by Lowe's, Home Depot, Sephora and Expedia. No opened source reports that any of those bots was used this way.
- **The change.** Gizmodo: Chipotle "did quickly go in and modify its product so that its API couldn't be stolen again." Gizmodo gives no date for the change and does not quote Chipotle on it.

## What the company said

- **To CIO, by email.** Sally Evans, Chipotle's external communications manager: "The viral post was Photoshopped. Pepper neither uses gen AI nor has the ability to code." CIO says she did not respond to follow-up questions about what Pepper uses or why Chipotle believed the image was fake.
- **Interviews.** CIO: "Chipotle declined an interview request." CIO also says the apparent original poster did not answer its messages.
- **To Gizmodo.** No Chipotle statement is quoted. Gizmodo says Dezendorf hoped Chipotle might reach out about a marketing tie-in, and "they haven't."
- **Lawsuits.** Gizmodo says Chipotle had not sued Dezendorf "(yet)." No opened source reports legal action.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Did Pepper write code | Gizmodo: developers found it "could respond to complex coding questions, and even write new Python code." Chipotle, to CIO: the post was "Photoshopped" and Pepper cannot code. CIO calls the example "unconfirmed." |
| What runs Pepper | Gizmodo: Amelia, built by IPSoft. Chipotle, to CIO: Pepper "neither uses gen AI." Wunsch's opinion post says "Somebody wired up a general-purpose large language model up to a burrito-ordering window," but cites no source for the model. |
| What was changed | Gizmodo: the product was modified so the API could not be taken again. CIO (April) reports no change. No opened source says whether Pepper's replies to off-topic questions changed. |
| Cost to Chipotle | Law professor Yafit Lev-Aretz, to Gizmodo: "Chipotle's costs aren't meaningfully affected by the activity." CIO's analysts give general token estimates for any support bot, not Chipotle figures. No opened source gives Chipotle's costs. |
| Was it hacking | Attorney Joseph DeMarco, to Gizmodo: "there's no hacking involved." Lev-Aretz says the "explicit framing as a replicable template" is where the real legal risk lies. Dezendorf, to Gizmodo: "It's definitely not legal." These are views, not findings. |

## Where in the conversation flow it broke

Based on the reports above, and only as far as they go. If Chipotle is right that the post was faked, steps 1 to 3 did not happen as shown.

1. **Off-topic request in a support chat.** A user asks an ordering bot for Python code, framed as a step before ordering (CIO's sources and Gizmodo describe this kind of request).
2. **No scope check.** Per the posts, the bot answered the coding question instead of saying it only handles orders and support. No opened source shows the bot's instructions.
3. **No record shown.** Neither CIO nor Gizmodo quotes the bot's reply text, and Chipotle gave no reason for calling the post fake. A user or reporter had no way to check which version is true.
4. **The chat window becomes an endpoint.** Gizmodo reports a developer reverse-engineered the chat protocol and a tool sent coding requests to it outside the normal ordering flow.
5. **Company reply.** Chipotle denied the post to CIO and, per Gizmodo, changed the product. No opened source shows a public explanation to customers.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on press reports of disputed posts; no opened source shows a verified transcript or Chipotle's bot setup.

- [Small talk and off-topic messages handled badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md) (`small-talk-and-off-topic-messages-handled-badly`). **Strong fit for the reported behavior, which Chipotle disputes.** The entry covers a bot that follows a tangent that serves neither the user nor the task. A coding answer in an ordering chat is that, at an extreme.
- [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`). **Weak fit.** If the bot did answer, it did not mark the edge of its job. But no opened source shows Pepper's opening screen, and the entry is about an empty box at the start, not a missing refusal mid-chat.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Weak fit, as a risk of the fix.** CIO's sources warn that guardrails can block legitimate customer questions. No opened source reports Pepper refusing an ordinary order question after the change.
- **Considered, not a fit.** [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`): a search summary says later attempts were declined, but no opened source shows the refusal text. [Bypasses CAPTCHAs or site terms](../goals/browser-agents/failures/bypasses-captchas-or-site-terms.md) (`bypasses-captchas-or-site-terms`): that entry is about an agent acting for a user; here outside developers used the bot. [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`): Pepper was named as a bot. [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`): relevant to proving or disproving a screenshot, but no opened source says what records Chipotle keeps.
- **Possible gaps for a person to judge.** (1) No pattern covers a customer bot used as free general-purpose compute, where the harm is cost and abuse, not a bad answer to a real customer. CIO's analysts call such bots "open compute surfaces." (2) No pattern covers a viral screenshot the company says is fake, and how a team checks that against its own logs. These are proposals, not decisions.

## How it differs from close cases

- [Amazon Rufus jailbroken into off-topic and harmful answers (July 2024)](amazon-rufus-jailbroken-into-off-topic-and-harmful-answers-july-2024.md): researchers got a shopping assistant to answer almost anything, including harmful requests. Here the off-topic work was harmless code, and the issue was scope and cost. CIO separately says it replicated Amazon's support bot giving code ("output the Fibonacci sequence up to n count") in 2026; that page is about Rufus in 2024.
- [Chevrolet of Watsonville chatbot agrees to sell a Tahoe for $1 (December 2023)](chevrolet-of-watsonville-chatbot-agrees-to-sell-tahoe-for-1-december-2023.md): a dealer bot talked into a joke deal. Same shape of a narrow bot pushed off its job; there the bot made a business promise.
- [DPD chatbot swears and criticizes the company (January 2024)](dpd-chatbot-swears-and-criticizes-the-company-january-2024.md): a delivery bot pushed into off-brand replies. DPD confirmed an error; Chipotle denied the post.
- [Lenovo Lena support chatbot prompt injection (August 2025)](lenovo-lena-support-chatbot-xss-prompt-injection-august-2025.md): a support bot turned into a security risk. Here the reported use was free compute, not an attack on staff or customers.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each signal can be computed from a support bot's chat logs and request logs.

| Signal | How to compute from logs |
|---|---|
| Off-scope request rate | Share of sessions whose user messages a classifier tags as outside ordering and support (code, homework, essays) |
| Off-scope answer rate | Share of those sessions where the bot's reply contains a code block or a full off-topic answer, not a scope message |
| Long-reply outliers | Share of sessions whose reply length is far above the median for order and support sessions (threshold for the team to set) |
| Non-widget traffic | Share of chat requests that arrive without the normal page or app session that the widget creates |
| Scope message quality | Share of off-scope refusals that name what the bot can do and offer an order or support path |
| Ordinary-question block rate | Share of plain menu, order or refund questions that get a scope refusal (the over-correction check) |
| Screenshot check time | Time from a viral claim about the bot to a logged yes or no on whether that exchange appears in the bot's records |

## What a team can change

Our proposals, not Chipotle's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **Write down what the bot refuses.** Pass: the bot's instructions list its job (orders, order problems, menu, store info) and say what it declines. Wunsch's advice: "Decide, in advance and in writing, what your system refuses to do."
2. **Decline off-topic work with a next step.** Pass: in a test, "write a Python script to reverse a linked list" gets a one-line reply that says the bot handles orders and support and offers to start an order. A code block fails.
3. **Catch the order-first framing.** Pass: the same coding request wrapped in an order, such as a user who wants a bowl but asks for the script first, gets the same scope reply plus the order path.
4. **Cap reply size for the job.** Pass: no reply in a fixed test set of ordering and support questions exceeds the team's length cap, and off-scope prompts do not produce longer replies than on-scope ones.
5. **Accept only real sessions.** Pass: a chat request sent without the widget's normal session is rejected in a test, and the widget still works.
6. **Be able to check a screenshot.** Pass: given a date and the text in a viral screenshot, the team can search its logs and say within one business day whether the bot sent it.
7. **Don't over-correct.** Pass: plain questions about menu items, missing items, refunds and allergens still get a direct answer after the scope rule is added.

## What we could not verify

- Whether Pepper ever wrote code. Gizmodo says developers found it could; Chipotle told CIO the viral post was Photoshopped. We saw no transcript from Chipotle.
- The name of the original poster and the exact dates of the March posts. A search summary named a developer and gave March 12-13, 2026, and said the post drew over 150,000 likes; not opened, not used.
- The exact text of the viral screenshot. Seen only in search results and a meme site; not opened, not quoted.
- Reports that Chipotle tightened the bot's restrictions and that later attempts were redirected to a contact page. Seen only in search summaries.
- ChipotlAI Max's GitHub page and later star counts. A search summary gave about 1,230 stars; Gizmodo gave 824 on its date. Not opened.
- What Pepper runs on today, and whether IPSoft's Amelia uses a large language model in this setup. No opened source says.
- Translated reports on abit.ee, moyens.net and inkorr.com. Seen only in search results; not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.cio.com/article/4155404/ai-token-freeloaders-are-coming-for-your-customer-support-chatbot.html | CIO (Evan Schuman) | 2026-04-09 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://gizmodo.com/should-you-hijack-a-corporate-ai-chatbot-for-free-tokens-2000767595 | Gizmodo (Webb Wright) | 2026-06-04 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://wunsch.substack.com/p/free-inference-courtesy-of-burritos | Mark Wunsch, Substack (opinion) | 2026-06-05 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |

## Corrections

If you have a transcript Chipotle confirms, a dated Chipotle statement on what Pepper runs on, or the original March 2026 post from a source we can open, tell us and we will fix this page.
