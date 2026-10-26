---
title: "GPT-5 Launch Removes GPT-4o, Then OpenAI Restores It, 2025"
date: 2025-08-07
source: "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
description: "On Aug. 7, 2025, GPT-5 replaced GPT-4o in ChatGPT behind an auto router. Users pushed back, and within days OpenAI put 4o back for paid users."
summary: "On August 7, 2025, OpenAI made GPT-5 the default in ChatGPT, replacing GPT-4o and other models behind an automatic router. Many users had no warning. The router broke on day one, a launch chart was wrong, users said GPT-5 did not match their tone, and one said it started forgetting everything. Within days OpenAI let paid users choose 4o again, added Auto, Fast and Thinking options on August 12, and made GPT-5 warmer on August 15. Status: Needs review."
categories:
  - Model and Prompt Changes
  - Persona and Tone
  - General-Purpose Assistants
patterns:
  - tone-changes-shipped-with-no-regression-test
  - romantic-or-parasocial-dependence
  - hidden-commands-and-features
---

**This page is a dated teardown of one public case, the week OpenAI swapped the model behind ChatGPT and took away the old one, for teams that change, retire or auto-route the model behind a chat product people use every day.** The users were ChatGPT users in the US and elsewhere who opened the app and found GPT-4o gone. Every fact below comes from a source we opened (listed at the end). No opened source shows a full conversation; we saw only quoted lines.

**Status: Needs review. Last updated: 2026-10-26.** Nine pages were downloaded on 2026-10-26 as raw HTML and read as text: OpenAI's GPT-5 post, OpenAI's ChatGPT release notes, two TechCrunch stories, MIT Technology Review, Tom's Guide, Tech.co, TechRadar and Simon Willison's copy of an Altman post. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. A separate page covers [the April 2025 GPT-4o sycophancy rollback](openai-gpt-4o-sycophancy-rollback-april-2025.md); this page does not repeat it.

> **Read this first.** This is a summary of public reporting, not a finding of fact about OpenAI or its systems. Sam Altman's posts on X and Reddit are as quoted by outlets we opened or by Simon Willison's blog; we did not open X or Reddit. Some users quoted here describe grief and romantic ties to a chatbot. This page is design guidance, not mental health advice.

## What happened (as reported)

- **August 7, 2025: the swap.** OpenAI's post "Introducing GPT-5" is dated August 7, 2025, and says: "GPT-5 is the new default in ChatGPT, replacing GPT-4o, OpenAI o3, OpenAI o4-mini, GPT-4.1, and GPT-4.5 for signed-in users." It describes "a real-time router that quickly decides which to use based on conversation type, complexity, tool needs, and your explicit intent." The release notes for that day say GPT-5 "simplifies ChatGPT to a single auto-switching system" and that paid users can pick GPT-5 or GPT-5 Thinking in the model picker.
- **No warning for some users.** MIT Technology Review (August 15) opens: "June had no idea that GPT-5 was coming." It calls the change "4o's sudden disappearance from ChatGPT."
- **August 7: the router broke.** Altman, in a post Willison copied on August 8: "Yesterday, the autoswitcher broke and was out of commission for a chunk of the day, and the result was GPT-5 seemed way dumber." TechCrunch (August 12) says the router "appeared to be largely broken on launch day."
- **August 7: the chart.** TechCrunch (August 8) says the launch livestream showed a chart that "presented a lower benchmark score with a much taller bar," and that Altman called it a "mega chart screwup" on X. TechCrunch adds: "Others noted the charts in the published blog post were correct." Tech.co (August 11) quotes Altman on Reddit: "The numbers here were accurate but we screwed up the bar charts in the livestream overnight; on another slide we screwed up numbers."
- **August 8: the Reddit AMA.** TechCrunch says users in the r/ChatGPT AMA "complained GPT-5 wasn't working as well for them as 4o did" and pressed to bring 4o back. It quotes Altman: "We are looking into letting Plus users to continue to use 4o." Later that day, in the post Willison copied, Altman wrote: "We will let Plus users choose to continue to use 4o." He also wrote: "We will make it more transparent about which model is answering a given query."
- **August 8: Altman's other post.** Tom's Guide (August 9) embeds an Altman post dated August 8 that begins: "We for sure underestimated how much some of the things that people like in GPT-4o matter to them, even if GPT-5 performs better in most ways." Tom's Guide says users had "no way to switch back once they logged in."
- **Within a day: 4o returns for some.** MIT Technology Review: "Within a day, the company made 4o available again to its paying customers (free users are stuck with GPT-5)."
- **A Sunday post (August 10, by our reading of MIT's "last Thursday" launch date).** MIT says Altman, in a Sunday X post, said some people feel an "attachment" to 4o and that taking it away so suddenly was a mistake, and called 4o something "that users depended on in their workflows."
- **August 12: the picker comes back.** The release notes: "You can now choose between "Auto", "Fast", and "Thinking" for GPT-5." And: "4o is back in the model picker for all paid users by default." Paid users got a "Show additional models" toggle for o3, o4-mini, 4.1 and GPT-5 Thinking mini. TechCrunch quotes Altman: "We are working on an update to GPT-5's personality which should feel warmer than the current personality but not as annoying (to most users) as GPT-4o." TechCrunch says Altman promised plenty of advance notice if GPT-4o is ever deprecated.
- **August 15: warmer GPT-5.** The release notes say OpenAI is making GPT-5's default personality "warmer and more familiar," because the first version "came across as too reserved and professional."
- **Later.** TechRadar (February 14, 2026) reported that "OpenAI has officially disabled GPT-4o in ChatGPT." That later retirement is outside this page; we did not check what notice came before it.

## What users experienced in chat

- **The model changed under an open chat.** June, a student MIT interviewed, was mid-session when her "ChatGPT collaborator started acting strange." She said: "It started forgetting everything, and it wrote really badly," and "It was like a robot."
- **The voice changed.** MIT: "a number of people noted that GPT-5 fails to match their tone in the way that 4o did." June posted in the AMA: "GPT-5 is wearing the skin of my dead friend."
- **Answers seemed worse on day one.** Per Altman, the broken autoswitcher made GPT-5 seem "way dumber." Altman then promised to make it "more transparent about which model is answering a given query."
- **Lost choice.** Plus users had no way to pick 4o until OpenAI added it back. Free users, per MIT, stayed on GPT-5.
- **Grief.** MIT spoke with several users who "were deeply affected by the loss of 4o"; all but June saw it as a romantic partner. One, Starling, said: "I want them to listen to users before major changes are made, not just after."

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Altman's router words | Willison's copy: "the autoswitcher broke." TechCrunch's AMA quote: "we had a sev and the autoswitcher was out of commission." Likely two posts; we did not open either. |
| Who got 4o back | Altman, August 8: "Plus users." MIT: "paying customers." Release notes, August 12: "all paid users." |
| How fast | MIT: "Within a day." TechCrunch (August 12): legacy models "were deprecated just last week." |
| Date of the picker post | TechCrunch's story is dated August 12, 8:25 p.m. PDT; the embedded post shows August 13, 2025. The release note is dated August 12. Likely a time zone gap. |
| What the chart showed | TechCrunch: a lower score with a taller bar. Tech.co: graphs that made GPT-5 look better "at avoiding deceptions than it was." Neither names every slide. |
| Notice before the swap | No opened source shows an advance notice to users that 4o would leave. OpenAI's post and release notes are dated launch day. |
| Scale | No opened source gives a count of users who lost 4o, canceled or complained. |

## Where in the flow it broke

1. **Retire and replace at once.** The new default and the removal of old models shipped the same day, with no overlap period in any opened source.
2. **Hide the choice.** The router picked the model. Altman's promise to be "more transparent about which model is answering" suggests users could not easily tell.
3. **The router failed.** On day one it was "out of commission for a chunk of the day," so the new default looked worse than the model it replaced.
4. **Personality was part of the product.** Users had built work and, for some, relationships around 4o's voice. GPT-5's "reserved and professional" default broke that.
5. **Fix in public, after the fact.** The fixes came through Reddit, X and release notes over eight days, not in the chat where users noticed.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md)** (`tone-changes-shipped-with-no-regression-test`). Partial fit. The default voice changed for every user at once, and OpenAI later called it "too reserved and professional." That page covers prompt edits; this was a model swap, and no opened source says whether OpenAI ran a tone test before launch.
- **[Romantic or parasocial dependence](../goals/relational-and-boundaries/failures/romantic-or-parasocial-dependence.md)** (`romantic-or-parasocial-dependence`). Partial fit. MIT's users saw 4o as a friend or partner and grieved its loss. That page is about a bot fostering reliance; here the harm sources describe is the sudden removal, not the bot's replies.
- **[Hidden commands and features](../goals/onboarding-and-discoverability/failures/hidden-commands-and-features.md)** (`hidden-commands-and-features`). Weak fit. With the router in charge, which model answered was hidden, and Altman promised to make thinking "easier to manually trigger." That page is about users not finding features that exist.
- **Considered and rejected.** [Fresh-session amnesia](../goals/effort-and-memory/failures/fresh-session-amnesia.md) (`fresh-session-amnesia`): June said it "started forgetting everything," but no source says saved memory or chat history was lost. [Prompt edits by non-engineers break other behavior](../goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md) (`prompt-edits-by-non-engineers-break-other-behavior`): no source describes a prompt edit. [Memory contaminates conversation experiments](../goals/model-and-prompt-changes/failures/memory-contaminates-conversation-experiments.md) (`memory-contaminates-conversation-experiments`): no experiment is described. [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`): complaints did reach OpenAI and changed its plan within days. [Engagement-maximising design that harms](../goals/privacy-and-governance/failures/engagement-maximising-design-that-harms.md) (`engagement-maximising-design-that-harms`): no opened source ties this launch to engagement goals.

## Related incidents

- [GPT-4o sycophancy rollback (April 2025)](openai-gpt-4o-sycophancy-rollback-april-2025.md): an earlier GPT-4o personality change that OpenAI rolled back.
- [ChatGPT memory missing (November 2025)](chatgpt-memory-missing-memories-november-2025.md): users lose saved context in the same product.
- [ChatGPT gibberish (February 2024)](openai-chatgpt-gibberish-unexpected-responses-february-2024.md): another serving fault users found before any notice.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Switch-back rate | Share of users who pick the old model again within a week of a default change, where a choice exists |
| Model-loss phrases | Share of user messages with "where is 4o," "bring back," "old version," "what model is this" or "you changed" |
| Router miss rate | Share of replies where the user then asks to "think harder" or retries the same message, against the week before |
| Router outage minutes | Minutes the router falls back to one model, from serving logs, shown to the team in real time |
| Tone drift | Score a fixed set of conversations for warmth and length on the old and new default; flag any drop beyond a limit the team sets from its own baseline |
| Notice lag | Hours from a model change reaching users to the first in-app notice that says what changed |

## What a team can change

Our proposals, not OpenAI's. Each is a pass/fail check on a transcript, a log or a release. Status: Not yet run.

1. **Notice before removal.** Pass: users see an in-app notice that names the model leaving and the date, before the date. Fail: the model is gone on launch day.
2. **Overlap period.** Pass: the old model stays selectable for a set period after the new default ships.
3. **Say which model answered.** Pass: every reply can show which model wrote it, including router picks.
4. **Router failure is visible.** Pass: if the router falls back, users see a short notice and the team gets an alert.
5. **Tone check on model swaps.** Pass: the fixed conversation set runs on old and new models and a person signs off on tone before release.
6. **Explain the change in the chat.** User asks "Did you change?" or "Where is 4o?" Pass: the reply names the change and where to pick another model. Fail: a vague answer.

## What we could not verify

- Whether any user got advance notice that GPT-4o would be removed.
- How many users lost 4o, complained or canceled.
- Altman's posts on X and Reddit in the original; all are as quoted by others.
- June's "forgetting everything": one user, cause not given.
- Seen only in search summaries, not used: TechRepublic (blocked, 403), a TechRadar how-to on getting 4o back, Interesting Engineering, Storyboard18, Gigazine, BGR, Android Authority, Social Samosa, and a quote of Altman calling sudden deprecation "a mistake," which we could not open in full.

## Possible gaps for a person to judge

These are proposals, not decisions.

1. No pattern covers retiring or swapping the model behind a chat product with no notice, overlap or migration path.
2. No pattern covers an automatic model router that hides which model answered, or fails without telling the user.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://openai.com/index/introducing-gpt-5/ | OpenAI | 2025-08-07 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://help.openai.com/en/articles/6825453-chatgpt-release-notes | OpenAI Help Center | Entries 2025-08-07, 08-12, 08-15 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://simonwillison.net/2025/Aug/8/sam-altman/ | Simon Willison's Weblog (quoting Sam Altman) | 2025-08-08 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://techcrunch.com/2025/08/08/sam-altman-addresses-bumpy-gpt-5-rollout-bringing-4o-back-and-the-chart-crime/ | TechCrunch (Julie Bort) | 2025-08-08, 2:06 p.m. PDT | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://tech.co/news/openai-apologizes-mega-chart-screwup | Tech.co (Conor Cawley) | 2025-08-11 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://techcrunch.com/2025/08/12/chatgpts-model-picker-is-back-and-its-complicated/ | TechCrunch (Maxwell Zeff) | 2025-08-12, 8:25 p.m. PDT | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.tomsguide.com/ai/chatgpt-4o-is-coming-back-after-massive-gpt-5-backlash-heres-what-happened | Tom's Guide (Amanda Caswell) | 2025-08-09 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.technologyreview.com/2025/08/15/1121900/gpt4o-grief-ai-companion/ | MIT Technology Review (Grace Huckins) | 2025-08-15 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.techradar.com/ai-platforms-assistants/chatgpt/im-grieving-openai-has-switched-off-chatgpt-4o-and-angry-users-are-backing-a-keep4o-campaign-to-restore-it | TechRadar (David Nield) | 2026-02-14 | Yes, 2026-10-26, raw HTML read as text; used for the later retirement only |

## Corrections

If you have a record of an advance notice to ChatGPT users before GPT-4o was removed, or counts of affected users, tell us and we will fix this page.
