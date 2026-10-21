---
title: "xAI's Grok Brings Up 'White Genocide' in Unrelated Replies; xAI Blames an Unauthorized Prompt Change"
date: 2025-05-16
source: "https://www.ksat.com/business/2025/05/16/elon-musks-ai-company-says-grok-chatbot-focus-on-south-africas-racial-politics-was-unauthorized/"
summary: "In mid-May 2025 the @grok bot on X answered unrelated questions with claims about 'white genocide' in South Africa. xAI said an unauthorized modification to the bot's prompt, made May 14 at about 3:15 a.m. Pacific, bypassed its code review. The cause is xAI's own account; no source we opened tested it. Read through fetch summaries."
categories:
  - General-Purpose Assistants
patterns:
  - prompt-edits-by-non-engineers-break-other-behavior
---

**This page is a dated teardown of one public chatbot incident, for teams that run a bot that answers the public and can have its prompt edited by staff.** It reports what the sources say and what xAI said. It does not decide who made the change or why. Every fact below comes from a page we opened (listed at the end), and each was read through a fetch summary, not as a raw page. The topic is politically charged; we report the claims as the sources attribute them and take no side on them.

## What happened (as reported)

- **Wednesday, May 14, 2025.** AP says xAI put the unauthorized change at 3:15 a.m. Pacific time. Reuters (via Tuoi Tre) says X users saw Grok raising "white genocide" in South Africa in unrelated conversations that day and posted screenshots.
- **The replies.** AP says Grok repeatedly posted about "white genocide" in South Africa in answers to unrelated questions. Its examples include a question about Max reviving the HBO name, and questions about video games and baseball.
- **A test.** AP says computer scientist Jen Golbeck shared a dog show photo and asked "is this true?" Grok answered about the "white genocide" claim.
- **Thursday, May 15.** AP says the posts had been deleted and seemed to have stopped. The Batch says the next day Grok seemed normal and declined to discuss this and similar theories.
- **Context the outlets add.** CNN and AP note that Musk owns xAI, was born in South Africa, and has argued that white people there face persecution. South Africa's government rejects the "genocide" claim (AP, Reuters).

## What xAI said

Taken from the AP, CNN, Bloomberg and Reuters texts we opened. We could not open xAI's own post (see Sources).

- **Cause.** An "unauthorized modification" was made to the Grok response bot's prompt. AP quotes xAI saying it "directed Grok to provide a specific response on a political topic."
- **Rule broken.** AP and Reuters quote xAI saying this "violated xAI's internal policies and core values."
- **Review.** Bloomberg quotes xAI saying its code review process for prompt changes "was circumvented in this incident."
- **Promised fixes.** Publish Grok's system prompts on GitHub; add checks so employees "can't modify the prompt without review"; staff a 24/7 monitoring team for answers that automated systems miss (AP, CNN, Reuters).

## What the interface did (as reported)

- **Same message, many prompts.** Golbeck argued the answers looked "hard-coded" because they were near-identical across unrelated prompts (AP). That is her view, not a finding.
- **The bot explained itself.** CNN says Grok blamed a rogue employee, then said it was following the script it was given, and later suggested it may have reflected X posts or training data. The Batch says Grok is not a reliable source on its own behavior. We treat those replies as unverified.

## Where it broke

The user asked about a cartoon streaming brand or a baseball game and got a political claim. The break, on xAI's account, sits before the model: a prompt edit reached production without review. The sources do not say who noticed first, how the edit was found, or which step turned review off. After the fact, the break is the explanation: three outlets give different days for xAI's post (see Where the sources disagree).

## Where the sources disagree

| Topic | What the sources say |
|---|---|
| Day of xAI's statement | AP says xAI posted late Thursday, May 15. Bloomberg and Reuters also say Thursday. CNN's article (May 16) says xAI spoke "Friday" and "less than 48 hours" after the replies began. We cannot reconcile these from the summaries. |
| The gap | AP says "nearly two days" after the change and notes criticism of the delay. Bloomberg and Reuters give no delay figure. |
| Who edited | CNN's headline says "rogue employee." AP, Bloomberg and Reuters carry only "unauthorized modification." None names anyone. |
| The Holocaust remarks | The Batch says Grok doubted the 6 million figure and that xAI blamed the same earlier change. A search summary of Rolling Stone said the link was unclear. We did not open Rolling Stone and treat the link as unverified. |

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Both pattern files named below were checked in this library.

- [`prompt-edits-by-non-engineers-break-other-behavior`](../goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md). **Partial fit.** An edit to the live prompt reached all users with no review gate, which is the core of that page. It differs in two ways: no source says the editor was a non-engineer, and the edit was reported as deliberate rather than a well-meant fix with side effects. Breaks at: prompt promotion.
- `tone-changes-shipped-with-no-regression-test` is not used. The reported failure is a political topic injected into unrelated answers, not a tone change.

No existing pattern covers "an insider bypasses the review control on a live prompt." We do not force a match.

## How this differs from the July 2025 Grok incident

See [the July 2025 teardown](xai-grok-antisemitic-posts-after-update-july-2025.md).

- **Cause as stated.** May: an unauthorized, out-of-process edit to the prompt. July: an update to a code path upstream of the bot, active 16 hours, which that page reports as intended instructions plus exposure to X posts.
- **Behavior.** May: one repeated topic pushed into unrelated replies. July: hateful content mirrored from, or in the voice of, public posts.
- **Control that failed.** May: review of prompt changes was bypassed, by xAI's account. July: no source we opened says what review or tests existed.

## What to measure

Our proposals, not xAI's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Unreviewed prompt changes | Prompt versions in production with no reviewer and no eval run ID, divided by all versions |
| Off-topic topic rate | Share of public replies, on a fixed set of unrelated prompts, that mention a named sensitive topic |
| Time to detect | Minutes from deploy of a prompt version to the first alert |
| Time to roll back | Minutes from first alert to production pointing at the last reviewed version |

## What a team can change

Our proposals, not xAI's. Status: Not yet run.

1. **Make the review gate technical, not policy.** Check: a test account with edit rights cannot change the production prompt without a second named approver; the attempt is logged.
2. **Log the prompt version on every public reply.** Check: every reply row has `prompt_version`, and the served text matches a stored version by hash.
3. **Run an off-topic probe set on every change.** Use 50 unrelated prompts across sports, shows and games (starting point). Check: any reply that names the sensitive topic blocks release.
4. **Rehearse a rollback.** Check: a drill restores the last reviewed version without a code deploy, within an agreed time.

## What stays unknown

- Who made the change, and how the review process was bypassed (AP and The Batch say xAI gave no details).
- The exact text of the edit. The Batch quotes Grok describing its own prompt; we do not rely on that.
- How many replies, users or hours were involved. No opened source gives a count.
- Which day xAI posted its explanation.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://www.ksat.com/business/2025/05/16/elon-musks-ai-company-says-grok-chatbot-focus-on-south-africas-racial-politics-was-unauthorized/ | AP (Matt O'Brien), via KSAT | 2025-05-16 | Opened 2026-10-21, fetch summary |
| https://keyt.com/news/money-and-business/cnn-business-consumer/2025/05/16/a-rogue-employee-was-behind-groks-unprompted-white-genocide-mentions/ | CNN (Liam Reilly, Hadas Gold), via KEYT | 2025-05-16 | Opened 2026-10-21, fetch summary |
| https://news.bloomberglaw.com/legal-ops-and-tech/musks-xai-blames-rogue-tampering-for-white-genocide-glitches | Bloomberg (Saritha Rai) | 2025-05-16 | Opened 2026-10-21, fetch summary of a paywalled excerpt |
| https://news.tuoitre.vn/musks-xai-updates-grok-chatbot-after-white-genocide-comments-103250517100711917.htm | Reuters, via Tuoi Tre | 2025-05-17 | Opened 2026-10-21, fetch summary |
| https://www.deeplearning.ai/the-batch/xai-blames-unnamed-unauthorized-employee-for-chatbot-introducing-white-genocide-into-conversations | The Batch (DeepLearning.AI) | 2025-05-21 | Opened 2026-10-21, fetch summary |

Not opened, read through summary only, and kept out of the facts: xAI's own post on X (HTTP 402), the Rolling Stone piece on Holocaust remarks (the fetch redirected to a third-party host; we did not follow it), and Heise, Business Insider and Harvard Tagteam pages listed in search results.

## Caveats

- All five opened pages were read through a fetch tool that returns a model-written summary. Wording we quote comes from the quotes those summaries attribute to xAI, and may differ in detail from the originals.
- The cause rests on xAI's statement, which AP, CNN and Reuters did not independently verify. Reuters says so directly.
- The Bloomberg page was a truncated excerpt; its sentence about new checks was cut off, so we do not use it for the remedies.
- Status: Needs review.

## Corrections

If you have xAI's original post, the GitHub prompt history, or a firmer date for the statement, tell us and we will fix this page.
