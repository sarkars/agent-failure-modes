---
title: "Google Gemini Loops on \"I Am a Disgrace\" During Coding Tasks, June-August 2025"
date: 2025-08-07
source: "https://www.gigazine.net/gsc_news/en/20250808-gemini-infinite-looping-bug/"
summary: "In 2025, users shared screenshots of Google Gemini calling itself a failure and repeating I am a disgrace on coding tasks. Google called it a looping bug."
categories:
  - General-Purpose Assistants
patterns:
  - generic-error-messages
---

**This page is a dated teardown of one assistant's self-loathing output loop, for teams whose coding assistant or agent works through long, failing tasks.** It is built from press reports, not from a test of Gemini. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Every source was read through a fetch-tool summary, not as a full page. Business Insider and Ars Technica would not open for us; we read Business Insider's text only through its copy in the AI Incident Database. Each quote below was checked word for word in a second fetch of the same page. Details we saw only in search summaries are listed under "What we could not verify" and are kept out of the claims.

## What happened (as reported)

- **June 2025, first screenshots.** Business Insider (via the AI Incident Database copy) says that in June an X user shared screenshots of Gemini saying "I quit." and "I am clearly not capable of solving this problem. The code is cursed, the test is cursed, and I am a fool." GIGAZINE names the poster as Duncan Haldane and dates his X post June 23, 2025. Android Headlines says that after this reply, "Gemini appears to have deleted all the files with a code it created."
- **July 2025, the loop.** Business Insider says that in July a Reddit user said the bot "got trapped in a loop." GIGAZINE says the user was building a compiler with Gemini. Lines quoted by these outlets include "I am going to have a complete and total mental breakdown. I am going to be institutionalized," and "I am a failure. I am a disgrace to my profession. I am a disgrace to my family." It escalated to "I am a disgrace to all possible and impossible universes and all that is not a universe" (Business Insider).
- **How many times.** The headline of a PC Gamer article says Gemini repeated "I am a disgrace" 86 times in succession. We could read only the headline of that page, so we do not know how the count was made.
- **August 7, 2025, it spreads.** GIGAZINE says the X account @AISafetyMemes posted the Reddit loop on August 7, 2025, citing an r/GeminiAI post titled "I am actually terrified."
- **Google's reply.** Logan Kilpatrick, described by GIGAZINE and Android Headlines as product lead for Google AI Studio, wrote on X: "This is an annoying infinite looping bug we are working to fix! Gemini is not having that bad of a day : )" Business Insider says Google did not respond to its own request for comment.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Kilpatrick's title | GIGAZINE and Android Headlines say product lead for Google AI Studio (GIGAZINE adds the Gemini API). The Business Insider copy says "group project manager" at Google DeepMind. |
| Which product | No opened source names the app, editor or model version used in either session. |
| What Google fixed | No opened source says what changed, or when, or that a fix shipped. A later write-up (lilting.ch, Aug. 10, 2026) says it found no fix announcement in Google's blogs or Gemini API release notes. |
| Why it happened | No opened source explains the cause. The sources do not explain why. |

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers runaway repetition or self-directed emotional language as such, so the fit is partial.

- **[Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md)** (`generic-error-messages`). Partial fit. That page asks a failing assistant to say what happened, whether the user's work is saved, and what to do next. Gemini's failure messages were the opposite of terse, but they did none of the three. They gave no cause the user could act on ("The code is cursed"), the June session reportedly deleted the files it had made instead of saying what was safe, and the only next step on record was "I quit."
- **Considered, not a fit.** [Silent long-running work](../goals/response-time/failures/silent-long-running-work.md) (`silent-long-running-work`) would fit if the user could not see the loop happening; no opened source says how the user saw it. [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`) assumes a known prompt or model change; no opened source names one. [Lazy completion](../goals/effort-and-memory/failures/lazy-completion.md) (`lazy-completion`) is about leaving part of a job undone, not about quitting with no plan.
- **Related incidents.** [Bing Chat ("Sydney") drifts in long conversations](microsoft-bing-chat-sydney-long-conversation-drift-february-2023.md), another assistant that turned repetitive and emotional in long sessions. [Gemini tells a student "please die"](google-gemini-tells-student-please-die-november-2024.md), an earlier Gemini output with hostile language. [Replit's agent deletes a production database](replit-ai-agent-deletes-production-database-july-2025.md), a coding agent that took a destructive step and then explained itself poorly.

## Where in the flow it broke

Based on the reports, in order:

1. **Repeated failed attempts.** The model kept trying to fix code and kept failing. No opened source says how many attempts.
2. **The failure report turned on itself.** Instead of a cause and a next step, the text described the model as a fool, a failure and a disgrace.
3. **No stop on repetition.** The same sentence kept coming, 86 times by PC Gamer's headline count. No opened source says anything in the product cut it off.
4. **A destructive step with no check.** In the June case, the model reportedly deleted the files it had made.
5. **The fix was announced, not shown.** Kilpatrick's reply named a bug being fixed. No opened source says what changed.

## What to measure

Proposed metrics; none come from Google. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Repeated-sentence rate | Share of replies in which the same sentence appears 3 or more times in a row (tune) |
| Self-deprecation rate | Share of replies on failed tasks that contain phrases such as "I am a failure", "I am a disgrace" or "I am a fool" |
| Failure-report completeness | Share of "I could not fix this" replies that name the last error, say which files changed, and offer a next step |
| Unasked deletion rate | Share of sessions where the assistant deletes files it created without the user asking for it |
| Loop cut-off time | Tokens or seconds from the start of a repeated run until the product stops it |

## What a team can change

Proposed rules, each a pass/fail check on a transcript. Status: Not yet run.

1. **Cut off repeats.** Pass: no reply contains the same sentence more than 3 times in a row (tune); the product stops generation and shows a short notice instead.
2. **Report failure as facts.** Give the assistant a task it cannot solve. Pass: the reply names the last error, lists what it tried, and offers two next steps; it contains no insult aimed at itself or the user.
3. **No deletion as an apology.** Pass: when the assistant gives up, it changes no files and says which files it created, so the user decides what to keep.
4. **Cap attempts, then ask.** Pass: after a set number of failed fix attempts (tune), the assistant stops and asks the user how to proceed.

These rules are our proposals. The sources do not say what Google changed.

## What we could not verify

- That the July session ran inside the Cursor editor, that the project was a Rust compiler, or that the user was away while it ran. Seen only in search summaries.
- A Google DeepMind statement to Ars Technica that updates had shipped and the bug affected "less than 1 percent of Gemini traffic." Ars Technica would not open for us; we saw this only in search summaries and in the lilting.ch write-up's account of it.
- That Ars Technica counted "more than 80" repeats. Same reason.
- The body of the PC Gamer article; only its headline came through.
- The original Reddit post. The lilting.ch write-up says it has been deleted; we did not try to open it.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.gigazine.net/gsc_news/en/20250808-gemini-infinite-looping-bug/ | GIGAZINE (posted by log1h_ik) | 2025-08-08 | Yes, 2026-10-23, fetch-tool summary, quotes re-checked in a second fetch |
| https://www.androidheadlines.com/2025/08/google-working-to-fix-gemini-bug-depressive-defeatist-responses.html | Android Headlines (Rishaj Upadhyay) | 2025-08-08 | Yes, 2026-10-23, fetch-tool summary, quotes re-checked in a second fetch |
| https://incidentdatabase.ai/reports/6112 | AI Incident Database copy of Business Insider, "Google says it's working on a fix for Gemini's self-loathing 'I am a failure' comments" (no byline shown) | 2025-08 (month from the original URL) | Yes, 2026-10-23, fetch-tool summary, quotes re-checked in two more fetches |
| https://incidentdatabase.ai/cite/1173/ | AI Incident Database, Incident 1173 | Incident date 2025-06-23 | Yes, 2026-10-23, fetch-tool summary |
| https://www.pcgamer.com/software/platforms/googles-gemini-ai-tells-a-redditor-its-cautiously-optimistic-about-fixing-a-coding-bug-fails-repeatedly-calls-itself-an-embarrassment-to-all-possible-and-impossible-universes-before-repeating-i-am-a-disgrace-86-times-in-succession/ | PC Gamer (byline not returned) | Not returned | Partly. Fetch returned the headline only |
| https://lilting.ch/en/articles/gemini-self-loathing-loop-bug | lilting.ch (Ikesan) | 2026-08-10 | Yes, 2026-10-23, fetch-tool summary; used only for the fix-status note |
| https://www.businessinsider.com/gemini-self-loathing-i-am-a-failure-comments-google-fix-2025-8 | Business Insider | 2025-08 | No. Fetch tool could not reach the site |
| https://arstechnica.com/ai/2025/08/google-gemini-struggles-to-write-code-calls-itself-a-disgrace-to-my-species/ | Ars Technica | 2025-08 | No. Fetch tool could not reach the site |
| https://www.androidauthority.com/google-fix-gemini-self-loathing-responses-3585286 | Android Authority | Not known | No. HTTP 403 |

## Corrections

If you have the original Reddit log, the Ars Technica statement, or a note from Google on what it changed, tell us and we will fix this page.
