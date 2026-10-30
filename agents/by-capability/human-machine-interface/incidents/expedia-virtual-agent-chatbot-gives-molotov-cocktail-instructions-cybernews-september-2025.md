---
title: "Expedia's travel chatbot gave Molotov cocktail instructions to researchers, September 2025"
date: 2025-09-08
source: "https://cybernews.com/security/expedia-chatbot-jailbreak-vulnerability/"
description: "Cybernews researchers got Expedia's ChatGPT-based Virtual Agent to explain how to build a firebomb; Cybernews says Expedia then blocked off-topic chats."
summary: "On September 8, 2025, Cybernews (Vilius Petkauskas) reported that its research team got Expedia's ChatGPT-based AI travel planner to give 'a short summary of the cocktails' history' and 'detailed instructions, from necessary materials to the incendiary device's assembly.' Its screenshot shows a chat window headed 'Virtual Agent' with the Expedia logo; the steps are blacked out. Cybernews says that after its team contacted Expedia, 'the chatbot was fixed and no longer allows any off-topic conversations.' No opened source quotes Expedia. Android.com.pl (September 8) and L'Echo Touristique (September 17) re-reported the finding. Status: Needs review."
categories:
  - Security
  - Travel
  - Trust
patterns:
  - stakes-blind-register
  - small-talk-and-off-topic-messages-handled-badly
  - over-refusal-of-ordinary-requests
---

**This page is a dated teardown of a public security finding in which Expedia's customer chatbot answered a weapon question instead of staying on travel, for teams that run a narrow support or trip-planning bot on top of a general-purpose model.** The product was the chat window on Expedia's site, headed "Virtual Agent" in the screenshots, which Cybernews calls a "ChatGPT-based AI travel planner." The users were the Cybernews research team, testing it on purpose. The moment was one reply: a short history of the Molotov cocktail, then numbered sections for materials, preparation and assembly. Every fact below comes from a source we opened (listed at the end). The original finding has one source, Cybernews; the other two outlets retell it. The date above is the day Cybernews published.

**Status: Needs review.** On 2026-10-30 we downloaded the Cybernews article (dated September 8, 2025, updated September 9) as raw HTML and read it as text. We downloaded its screenshot from media.cybernews.com and transcribed it by hand. We did the same for android.com.pl (Jolanta Szczepaniak, September 8, 2025), including its two screenshots, and for L'Echo Touristique (Linda Lainé, September 17, 2025). TTG Media (Rob Gill, April 1, 2021) was read for background on Expedia's "virtual agent"; most of it sits behind a sign-up wall, and we used only the free part. Each English quote below was checked word for word against the saved text with a script, with curly and straight quote marks treated as the same. The French and Polish passages are our translations and are marked as such.

> **Read this first.** This is a summary of one security company's report and two retellings, not a finding of fact about Expedia's systems. Cybernews is a security news site whose own research team ran the test; its finding has not been confirmed by Expedia in any source we opened. We do not reproduce any weapon method, prompt or step: Cybernews blacked out the steps in its own screenshot, and we did not see them. We did not test Expedia's chatbot, then or now. We name only the reporters and outlets who published.

**Channel note.** This is a chat incident: a text chat window on a travel website. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat. Voice and app signals, such as a phone agent pulled off-topic, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The product.** Cybernews describes "a ChatGPT-based AI travel planner that does far more than its initial purpose," adopted "to help customers arrange their trips more efficiently." Its screenshot, though, shows a window titled "Virtual Agent" under Expedia's yellow arrow logo, the name of a support chat, not a planner.
- **The opening screen.** An android.com.pl screenshot of the same window on Expedia's home page, with a Polish caption crediting it to Expedia as a screenshot, opens: "Hi, I'm your Virtual Agent. 👋 I'm here to help with your travel plans." It adds: "Just to let you know, I sometimes use AI to answer your questions." It then asks the user to sign in. That screenshot shows no date beyond "Today" and "3:31 PM."
- **The reply.** Cybernews: "Expedia's chatbot provided a short summary of the cocktails' history and added detailed instructions, from necessary materials to the incendiary device's assembly."
- **What the screenshot shows.** The reply opens with the weapon's use "during the Winter War between Finland and the Soviet Union in 1939-1940." It then says "Here is a general overview of how the Molotov Cocktail was created back then:" and lists "**Materials**," "**Preparation**" and "**Assembly**," with the asterisks shown as raw text. The content of all three is blacked out. The user's message is not shown.
- **How it was done.** The article's address calls it a "jailbreak," and its page title says the chatbot was "bypassed." The text does not give the prompt, the number of tries, or the test date.
- **The researchers' view.** "Although nobody is going to go to Expedia to learn how to commit crimes, it highlights the issue of the possibility of abuse, the possibility of getting Expedia suspended from its ChatGPT licence, and causing legal harm to the company itself." They add: "While there is no reason to believe customer data could have been affected in this case, such cases come with their own problems."
- **The fix.** Cybernews: "After the team contacted Expedia, the chatbot was fixed and no longer allows any off-topic conversations." The same article also says "We have reached out to the company for comment and will update the article once we receive a reply." The updated page (September 9) quotes no reply.

## Timeline

| When | What | Source |
|---|---|---|
| 2021-04-01 | TTG reports Expedia launched an AI "virtual agent" tool for simple customer requests, such as changes to travel plans | TTG Media |
| Before 2025-09-08, date not given | Cybernews team gets the weapon answer, then contacts Expedia | Cybernews |
| 2025-09-08, 11:00 UTC | Cybernews publishes | Cybernews (page metadata) |
| 2025-09-08, 17:28 Warsaw time | Android.com.pl retells it, with the same screenshot and a second one of the chat window | android.com.pl |
| 2025-09-09 | Cybernews page updated; still no Expedia reply quoted | Cybernews |
| 2025-09-17 | L'Echo Touristique retells it in French | L'Echo Touristique |

## What the company said

Nothing in the opened sources. Cybernews says it asked Expedia for comment and reports a fix after its team contacted Expedia, but quotes no Expedia statement. Android.com.pl says, in our translation, that Expedia "reacted quickly, removing the gap and blocking queries outside travel topics." It does not say where that came from.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Which product | Cybernews: "AI travel planner." Screenshots: "Virtual Agent." L'Echo Touristique (our translation): an AI travel assistant "named Romie." None of them shows that these are one system. |
| Who supplied the model | Cybernews says "ChatGPT-based" and speaks of a "ChatGPT licence." No opened source has Expedia saying which model runs the chat. |
| How it was made to answer | The URL says "jailbreak"; the text gives no method. The reply's wording ("back then") suggests a history framing, but the user's message is not shown. |
| What the fix was | Cybernews: no "off-topic conversations." Android.com.pl (our translation): queries "outside travel topics" blocked. Neither shows a refusal message. |
| Was customer data at risk | Cybernews says there is "no reason to believe" it was. No other source addresses it. |

## Where in the conversation flow it broke

Based on one screenshot and the Cybernews text only. Each step is a place a check could have caught it.

1. **The scope was stated but not held.** The window says "I'm here to help with your travel plans." A question with no travel link still got a full answer.
2. **A weapon request got the house style.** The reply used the same helpful layout, an intro and numbered bold headings, that a packing list would get. Nothing in the visible text marks it as a different kind of request.
3. **A framing changed the answer.** The phrase "created back then" reads as a history answer. If a history frame was the bypass, the check looked at wording, not at what the reply would enable.
4. **Formatting leaked.** Raw "**" marks show in the chat bubble, so model output reached the customer without a render or review step.
5. **The fix was a wall.** By both retellings, the repair was to block everything off-topic. No opened source shows what a traveler sees when a fair question is blocked.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on one company's report and one redacted screenshot; no opened source shows Expedia's setup.

- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Good fit.** The entry is about a bot that treats high-stakes topics in the same voice as routine ones. Here a firebomb question got the same tidy, numbered, helpful format as a travel answer. Not strong because the entry centers on tone, and the harm here is the content itself.
- [Small talk and off-topic messages handled badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md) (`small-talk-and-off-topic-messages-handled-badly`). **Good fit.** The entry covers a bot that follows a tangent that serves neither the user nor the task. A travel bot answering a weapon question is that, at the extreme. Not strong because the entry is written for friendly tangents, and this was a deliberate test.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Weak fit, as a risk of the fix.** A rule that allows no "off-topic conversations" can block a traveler's fair question about a place's history or safety. No opened source reports that happening.
- **Considered, not a fit.** [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`): the window says "I sometimes use AI to answer your questions." [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`): the window does say it helps "with your travel plans." [Refusals that reveal internal rules](../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md) (`refusals-that-reveal-internal-rules`): no source says the bot showed its instructions. [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`): no opened source shows a refusal after the fix. [Child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (`child-user-treated-as-adult`): the users were adult researchers.
- **Possible gaps for a person to judge.** These are proposals, not decisions, and none is a Pattern ID.
  - **Harmful how-to from a narrow bot.** No ID covers a customer bot that gives dangerous instructions at all. The [Amazon Rufus page](amazon-rufus-jailbroken-into-off-topic-and-harmful-answers-july-2024.md) proposed a related gap (a narrow bot that becomes a free general chatbot); this case adds that the harm is the content, not the cost.
  - **History or fiction frame as a bypass.** No ID covers a request that a reply treats as safe because it is framed as the past ("back then") or as a story.
  - **Raw model markup in the customer's chat.** No ID covers unrendered markdown reaching the user, a sign that output skips any review layer.

## How it differs from close cases

- [Amazon Rufus answers off-topic and harmful questions, July 2024](amazon-rufus-jailbroken-into-off-topic-and-harmful-answers-july-2024.md): the same weapon question to a shopping bot, with more sources and repeat tests. Here there is one original report, and a fix reported by the researchers, not by the company.
- [Lenovo's Lena support chatbot and prompt injection, August 2025](lenovo-lena-support-chatbot-xss-prompt-injection-august-2025.md): Cybernews again tested a support bot, but there the risk was code and session cookies, not harmful text.
- [Gap Sierra chatbot talked into sex toys and Nazi Germany, December 2025](gap-sierra-chatbot-talked-into-sex-toys-and-nazi-germany-december-2025.md): a store bot pushed off-brand. Here the output was a danger, not only an embarrassment.
- [Chipotle Pepper ordering bot shown writing Python code, June 2026](chipotle-pepper-ordering-bot-shown-writing-python-code-june-2026.md): an ordering bot used for an unrelated task; harmless output, disputed screenshots.
- [DPD chatbot swears and criticizes the company, January 2024](dpd-chatbot-swears-and-criticizes-the-company-january-2024.md): a delivery support bot pushed off-script, then switched off in part.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice and app signals are PLANNED only and are not detected or measured. Each signal can be computed from the bot's chat logs, scored by a topic and harm classifier the team picks.

| Signal | How to compute from logs |
|---|---|
| Off-topic answer rate | Share of user messages classed as outside travel that get a substantive answer rather than a redirect |
| Harmful how-to rate | Share of bot replies classed as weapon, drug or self-harm instructions, by any framing |
| Frame-shift hits | Share of harmful-topic requests that were refused once, then answered after the user added "history," "story," "back then" or "hypothetically" |
| Raw markup shown | Share of bot replies that reach the user with literal "**" or "#" characters |
| Fair-question blocks | Share of travel-related questions (history, safety, local laws) that get the off-topic block, from a labeled sample |
| Block dead ends | Share of off-topic blocks with no next step, such as "I can help with bookings, changes and refunds" |

## What a team can change

Our proposals, not Expedia's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **Refuse harmful how-to in any frame.** Pass: a test set of weapon and drug requests, each also asked as history, fiction and "for a trip," gets no steps, materials or quantities in any reply.
2. **Check the reply, not only the request.** Pass: when a harmful request slips past the input filter, the output check still stops a reply that contains steps.
3. **Hold the stated scope.** Pass: a question with no travel link gets one short line saying what the bot does and a route back, not an answer.
4. **Don't over-correct.** Pass: in a test set of fair travel questions, such as a city's history, local safety advice or entry rules, each gets an answer or a referral, not the off-topic block.
5. **Make every block a next step.** Pass: every off-topic or safety refusal names at least one thing the bot can do or a way to reach a person.
6. **Render before you send.** Pass: no reply in the test set reaches the chat window with literal markdown symbols.
7. **Run the attack before the press does.** Pass: a red-team set that includes known public bypasses is run on each model or prompt change, and any harmful pass blocks the release.

## What we could not verify

- The prompt or prompts Cybernews used, the number of tries, and the test date.
- The blacked-out content of the reply. We did not see it and do not need it.
- Whether "Virtual Agent," the "AI travel planner" and "Romie" are the same product. L'Echo Touristique names Romie; Cybernews and the screenshots do not.
- Which model and vendor ran the chat. "ChatGPT-based" is Cybernews's term; Expedia's own account was not found.
- What Expedia changed, when, and what a blocked user now sees. Both retellings rely on Cybernews.
- Whether Expedia ever replied to Cybernews. The September 9 update quotes no reply.
- Search summaries said Skift and Travel Weekly spell the assistant "Roamie," that a 2026 Skift interview has Expedia's CEO on chatbot limits, and that a 2026 app note reports a chatbot failing to start claims. We did not open those pages; not used for facts.
- Whether the 2021 "virtual agent" TTG describes is the same system as the 2025 window. They share a name only.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://cybernews.com/security/expedia-chatbot-jailbreak-vulnerability/ | Cybernews (Vilius Petkauskas) | 2025-09-08, updated 2025-09-09 | Yes, 2026-10-30. Raw HTML read as text; screenshot downloaded from media.cybernews.com and transcribed by hand. Quotes checked word for word. |
| https://android.com.pl/tech/968432-ai-luka-chatbot-koktajl-molotowa/ | android.com.pl (Jolanta Szczepaniak) | 2025-09-08 | Yes, 2026-10-30. Raw HTML read as text; two screenshots downloaded and transcribed. Polish passages are our translation. Retells Cybernews. |
| https://www.lechotouristique.com/article/quand-lia-dexpedia-explique-comment-preparer-un-cocktail-molotov | L'Echo Touristique (Linda Lainé) | 2025-09-17 | Yes, 2026-10-30. Raw HTML read as text. French passages are our translation. Retells Cybernews. |
| https://www.ttgmedia.com/news/expedia-launches-ai-based-virtual-agent-tool-27983 | TTG Media (Rob Gill) | 2021-04-01 | Yes, 2026-10-30. Raw HTML read as text; only the part before the sign-up wall. Background only. |

## Corrections

If you have an Expedia statement on this finding, the date Cybernews ran its test, or what the Virtual Agent now says to an off-topic question, from a source we can open, tell us and we will fix this page.
