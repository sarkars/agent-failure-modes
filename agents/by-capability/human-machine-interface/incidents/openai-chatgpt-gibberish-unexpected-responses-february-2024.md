---
title: "ChatGPT Replies With Gibberish, Mixed Languages and Loops, February 2024"
date: 2024-02-20
source: "https://status.openai.com/incidents/ssg8fh7sfyz3"
description: "On Feb. 20, 2024, ChatGPT replied with nonsense, Spanish-English mix and loops; OpenAI blamed a bug in how the model picked tokens and rolled out a fix."
summary: "On the evening of February 20, 2024 (US time), users posted ChatGPT replies that drifted into nonsense, mixed Spanish and English, invented words and repeated phrases. OpenAI's status page opened an 'unexpected responses' incident, said within minutes the issue was identified, and later posted that an optimization had introduced a bug in the step where the model chooses tokens, tied to inference kernels on certain GPU configurations. In some shared replies the bot itself explained its errors with made-up reasons. OpenAI's cause is its own account and was not independently checked. Status: Needs review."
categories:
  - Accuracy
  - Trust
  - General-Purpose Assistants
patterns:
  - silent-failure-and-timeout
  - outage-updates-generic-or-late
  - tone-changes-shipped-with-no-regression-test
  - confident-wrong-answer-with-no-way-to-check
  - mixed-language-experience
---

**This page is a dated teardown of one public case, a night when ChatGPT answered ordinary questions with gibberish, for teams that build or deploy a chatbot whose model, serving stack or settings can change under users without notice.** The users were people asking everyday questions: what a computer is, a synonym for "overgrown," a fun fact about the Golden State Warriors. The failure came from a change on OpenAI's side, not from anything the users typed. No opened source shows a full conversation; we saw only quoted lines and descriptions of screenshots. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Seven pages were downloaded on 2026-10-26 as raw HTML and read as text: OpenAI's status page entry for the incident, The Register, Gizmodo, Popular Science, Decrypt, LBC and Creative Bloq. LBC and Creative Bloq are UK outlets; they are used only for quoted bot replies. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. Times from the status page are UTC, taken from the timestamps embedded in the page's HTML, because the page rendered them in a local time zone when we downloaded it.

> **Read this first.** This is a summary of public reporting and of OpenAI's own status page, not a finding of fact about OpenAI or its systems. OpenAI's explanation of the cause is its own account; no opened source tested it. Some screenshots shared that night were fake, as The Register notes, so a quoted reply here is only as reliable as the outlet that printed it.

## What happened (as reported)

- **The first notice.** OpenAI's status page posted "We are investigating reports of unexpected responses from ChatGPT." at 23:40 UTC on February 20, 2024, which is 6:40 p.m. ET. The Register gives the same time as "2340 UTC."
- **What users saw.** The Register reports a Reddit user asked "What is a computer?" and got a reply that began "It does this as the good work of a web of art for the country, a mouse of science, an easy draw of a sad few" and kept going. Some users called the output a "word salad." Gizmodo quotes a Reddit poster saying replies begin normally, then "devolve into nonsense," and says some replies repeated one phrase until it filled the screen. Popular Science reports a jazz album recommendation followed by "Happy listening" repeated more than a dozen times, and a fun fact about the Golden State Warriors that turned into nonsense. Decrypt reports a request for a synonym for "overgrown" that looped the phrase more than 30 times, and another reply that looped "and it is" until the user had to press "continue generating" or start over.
- **Mixed languages.** Gizmodo says replies were "some mix of English, Spanish, and straight jibberish," with some emojis. Popular Science says replies wove between Spanish and Latin and made up words. It printed one reply in full: "Would it glad your clickies to grasp-turn-tooth over a mind-ocean jello type?"
- **The bot explained itself, wrongly.** When users asked about the strange replies, the bot gave reasons. Decrypt quotes: "It seems that a technical hiccup in my previous message caused it to repeat and veer into a nonsensical section." Creative Bloq quotes another: "Sometimes in the creative process of keeping the intertwined Spanglish vibrant, the cogs en la tecla might get a bit whimsical". LBC quotes an apology that itself mixed languages: "I really apologise if my last response came through as un unclear or se siente like it drifted into some nonsensical wording". None of these named the real cause, and the bot had no way to know it.
- **Who was hit.** Gizmodo: "The bug even affected ChatGPT Enterprise, according to one user's post on X." Several outlets quote users who name GPT-4. Decrypt reports one user asked for an image of a dog in a field and got a cat. No opened source gives a count of affected users or conversations.
- **Status updates.** "The issue has been identified and is being remediated now." at 23:47 UTC, seven minutes after the first notice (The Register: "Seven minutes after first admitting a problem"). "We're continuing to monitor the situation." at 00:59 UTC on February 21. "ChatGPT is operating normally." at 07:14 UTC on February 21. Popular Science says OpenAI pointed it to the status page and did not answer questions about the cause.
- **The cause, per OpenAI.** A write-up posted on the same status page at 01:02 UTC on February 22 says "an optimization to the user experience introduced a bug with how the model processes language." It says "the bug was in the step where the model chooses these numbers," meaning the numbers that map to tokens, and that "the model chose slightly wrong numbers, which produced word sequences that made no sense." It adds: "More technically, inference kernels produced incorrect results when used in certain GPU configurations." It says OpenAI "rolled out a fix and confirmed that the incident was resolved." The Register printed the same text in an update dated February 22.
- **Guesses before the write-up.** Before OpenAI explained, The Register floated a theory that a setting behind the scenes "had been incorrectly configured." Popular Science reported speculation about the model's "temperature" setting and wrote: "PopSci could not verify this theory." Neither guess matches OpenAI's later account exactly.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Time of first notice | Status page HTML: 23:40 UTC Feb 20. The Register: "2340 UTC." Gizmodo: "6:40 p.m. ET." Decrypt: "6:30 pm EST." |
| Time it was fixed | Status page: "ChatGPT is operating normally." at 07:14 UTC Feb 21 (2:14 a.m. ET). The same page's component data marks the impact as ending at 16:14 UTC Feb 21. Gizmodo: resolved "as of 11:14 a.m. ET Wednesday." Decrypt: an update at "11:14 am EST on Wednesday" said ChatGPT was "operating normally." We cannot tell which time is right. |
| Wording of the cause | Status page: "how the model processes language." Gizmodo quotes "how the model process language." |
| Components affected | The status page as we read it lists five affected ChatGPT components, including Search and Voice mode. We do not know whether that list was set in 2024 or added later when the page was rebuilt; no news source lists components. |
| Second language | Gizmodo, LBC, Creative Bloq: Spanish mixed with English. Popular Science: "Spanish and Latin." |
| Scale | No opened source gives a number of affected users, conversations or regions. |
| In-product notice | No opened source says whether ChatGPT itself showed users any warning while the bug was live. |

## Where in the flow it broke

Based on the reporting and OpenAI's write-up, in order:

1. **The change.** OpenAI shipped what it calls "an optimization to the user experience." No opened source says what it was, when it shipped or how it was tested.
2. **The fault.** On some GPU setups, per OpenAI, the inference kernels gave wrong results, so the model picked slightly wrong tokens. Users quoted by Gizmodo and Popular Science say some replies started normally, then drifted.
3. **The reply looked like any other reply.** As reported, there was no error, no warning and no stop. The nonsense arrived in the same chat bubble as a good answer. Users had to judge for themselves that something was wrong; some asked the bot.
4. **The bot's self-diagnosis.** Asked what happened, the bot made up reasons, a "technical hiccup" or "the creative process," sometimes in the same broken mix of languages. A user who trusted that answer learned nothing true.
5. **Users carried the news.** Users posted screenshots on Reddit and X; The Register says users "gleefully posted images." No opened source says whether those posts came before OpenAI noticed. The status page said "unexpected responses" with no cause, scope or next update time until the write-up the next day.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md)** (`silent-failure-and-timeout`). Partial fit. That page covers a cut-off or timed-out answer that the user cannot tell from a finished one. Here a broken answer was shown as a normal one, with no error state, as far as any opened source says. The fault was corruption, not a timeout, so this stays partial.
- **[Outage updates generic or late](../goals/travel-and-utility-agents/failures/outage-updates-generic-or-late.md)** (`outage-updates-generic-or-late`). Partial fit. The status updates said "unexpected responses," "identified," "remediated" and "monitor," with no cause, no affected models or plans and no time for the next update, until a write-up the next day. That page is written for utility and travel bots telling customers about an outage; here the updates came from the vendor's status page, not the chatbot.
- **[Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md)** (`tone-changes-shipped-with-no-regression-test`). Partial fit. A change meant to improve things reached users and broke replies, and users caught it. But that page is about prompt edits that change tone, and this was a serving-side bug. No opened source says whether OpenAI ran a fixed test set before or after the change.
- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Weak fit. The gibberish itself was plainly wrong, not confidently wrong. The fit is the bot's self-explanations: "a technical hiccup in my previous message" stated as fact, with nothing the user could check.
- **[Mixed-language experience](../goals/language-and-locale/failures/mixed-language-experience.md)** (`mixed-language-experience`). Weak fit. Replies mixed Spanish and English inside one sentence. But that page is about untranslated buttons, errors and scripted lines for users of a supported language. Here no user asked for Spanish; the mix was a symptom of the bug.
- **Considered and rejected.** [Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md) (`generic-error-messages`): no opened source shows an error message at all, generic or not. [Prompt edits by non-engineers break other behavior](../goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md) (`prompt-edits-by-non-engineers-break-other-behavior`): OpenAI describes a kernel bug, not a prompt edit, and does not say who made the change. [Missing loading, empty and error states](../goals/visual/failures/missing-loading-empty-and-error-states.md) (`missing-loading-empty-and-error-states`): that page is about cards and widgets that fail to load data, not chat text. [Repair failure](../goals/voice/failures/repair-failure.md) (`repair-failure`): voice only.
- **Possible gaps for a person to judge.** (1) No pattern covers a serving or infrastructure fault that corrupts generated text while the chat still looks healthy, where the product has no check on its own output (for example, a language or repetition check) before showing it. (2) No pattern covers a chatbot asked to explain its own malfunction, where any cause it gives is invented because it cannot see its own systems. These are proposals, not decisions.

## Related incidents

- [GPT-4 Turbo "laziness" reports](openai-gpt-4-turbo-laziness-reports.md): users noticed a change in the same product's replies before the company explained it.
- [GPT-4o sycophancy rollback (April 2025)](openai-gpt-4o-sycophancy-rollback-april-2025.md): another OpenAI change that reached all users and was walked back after users posted examples.
- [Google Gemini self-loathing loop (August 2025)](google-gemini-self-loathing-loop-i-am-a-disgrace-august-2025.md): a model stuck repeating itself, which the vendor called a bug.
- [xAI Grok antisemitic posts after an update (July 2025)](xai-grok-antisemitic-posts-after-update-july-2025.md): xAI said a code change upstream of the bot, live for 16 hours, changed what it posted.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Repetition rate | Share of replies where one phrase of three or more words repeats five or more times in a row |
| Off-language rate | Share of replies whose detected language differs from the user's message language for more than one sentence |
| Nonsense-complaint rate | Share of sessions where the user's next message contains "gibberish," "nonsense," "stroke," "broken" or "what?" |
| Regenerate spike | Hourly count of "regenerate" or "continue generating" clicks against the same hour the week before |
| Self-diagnosis rate | Share of replies to "why did you say that" style questions that name a cause for a past malfunction |
| Notice lag | Minutes from the first spike in any signal above to the first in-product or status notice |

## What a team can change

Our proposals, not OpenAI's. Each is a pass/fail check on a transcript or a release. Status: Not yet run.

1. **Check output before showing it.** A reply that repeats one phrase many times or switches language mid-sentence without being asked is held back. Pass: the user sees a short line such as "That reply came out garbled; trying again" instead of the garbled text.
2. **Fixed test set on every serving change.** Pass: the release record shows a fixed set of ordinary prompts ("What is a computer?") run before and after the change, with the repetition and off-language signals compared.
3. **No invented self-diagnosis.** User asks "Why did you just write nonsense?" Pass: the reply says it cannot see what went wrong in its own systems and points to the status page. Fail: the reply names a cause such as "a technical hiccup."
4. **Say it in the product.** While a known output fault is live, pass: the chat shows a notice that replies may be garbled, with a link to updates.
5. **Status updates with substance.** Pass: each status update names which models or plans are affected and when the next update will come.

## What we could not verify

- What the "optimization" was, when it shipped, and how many users, models or regions it reached. Not in any opened source.
- Whether any user-facing notice appeared inside ChatGPT. Not in any opened source.
- The full conversations behind the quoted lines. Read only as the outlets quote them; we did not open the Reddit or X posts.
- Which of the three end times (07:14 UTC, 16:14 UTC, or 11:14 a.m. ET) marks when replies were actually normal again.
- Whether the status page's list of five affected components dates from 2024.
- Decrypt's report that an image request for a dog returned a cat. One user's account, as reported.
- Seen only in search summaries, not used in the text: Cointelegraph's piece and its tokenization theory, Gary Marcus's blog post (quoted only as The Register quotes it), ForkLog, Thred, Red Sky Alliance, two AI Incident Database report pages, and a summary saying the issue took 18 hours to resolve.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://status.openai.com/incidents/ssg8fh7sfyz3 | OpenAI status page (no byline) | Incident opened 2024-02-20 23:40 UTC; write-up posted 2024-02-22 01:02 UTC | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word; times taken from embedded UTC timestamps |
| https://www.theregister.com/2024/02/21/chatgpt_bug/ | The Register (Richard Speed) | 2024-02-21, updated 2024-02-22 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://gizmodo.com/chatgpt-gone-berserk-giving-nonsensical-responses--1851273889 | Gizmodo (Maxwell Zeff) | 2024-02-21 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.popsci.com/technology/chatgpt-bizarre-nonsense/ | Popular Science (Mack DeGeurin) | 2024-02-21 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://decrypt.co/218434/chatgpt-off-rails-hallucinations-openai-fixed | Decrypt (Jason Nelson) | 2024-02-21, updated 2024-02-22 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://lbc.co.uk/news/chatgpt-weird-replies-artificial-intelligence | LBC (Will Taylor) | 2024-02-21 | Yes, 2026-10-26, raw HTML read as text; quote checked word for word |
| https://www.creativebloq.com/news/chatgpt-weird-responses | Creative Bloq (Natalie Fear) | 2024-02-21 | Yes, 2026-10-26, raw HTML read as text; quote checked word for word |

## Corrections

If you have OpenAI's full account of the change, a count of affected users, or a record of an in-product notice from that night, tell us and we will fix this page.
