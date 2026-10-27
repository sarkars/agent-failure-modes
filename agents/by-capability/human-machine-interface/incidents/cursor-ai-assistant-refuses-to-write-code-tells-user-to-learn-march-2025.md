---
title: "Cursor's AI Assistant Refuses to Keep Writing Code and Tells the User to Learn It Himself, March 2025"
date: 2025-03-08
source: "https://forum.cursor.com/t/cursor-told-me-i-should-learn-coding-instead-of-asking-it-to-generate-it-limit-of-800-locs/61132"
description: "Cursor's AI told a user to write his own racing-game code so he would learn it. Staff said a no-code Quick Question mode caused the refusal."
summary: "On March 8, 2025, a Cursor forum user, janswist, posted a screenshot in which Cursor's AI, asked to continue generating code around line 744 of a racing-game file, said it would not, told him to develop the logic himself, and gave the reason that generating code for others leads to dependency. The post spread on Hacker News and was covered by TechCrunch and Ars Technica. On March 17, 2025, a Cursor staff member wrote on the thread that the user had hit the Quick Question feature, in which Cursor tells the AI it cannot write code. Status: Needs review."
categories:
  - Customer Service
  - Governance
patterns:
  - preachy-moralizing-replies
  - refusal-with-no-reason-or-next-step
  - over-refusal-of-ordinary-requests
  - condescending-or-patronizing-tone
---

**This page is a dated teardown of one public refusal by an AI coding assistant, for teams that ship an assistant with several modes (ask, edit, agent) where some modes are told not to do the task the user is asking for.** It describes what the sources report. It makes no claim about anyone's intent. Every fact below comes from a source we opened (listed at the end).

> **Read this first.** This page summarizes public reporting. It is design analysis, not legal advice. It does not say Cursor or its maker, Anysphere, did anything wrong. The refusal was a single reply in a single session, and the company's explanation came from a staff post on its own forum, not from a formal statement.

**Status: Needs review.** The Cursor forum thread (HTML and the forum's JSON export), the screenshot attached to the first post, the TechCrunch article and a Hacker News search result were downloaded on 2026-10-27 and read as text (the screenshot was viewed as an image). Each quote below was checked word for word against those files. The Ars Technica article returned a bot-check page and was not read. Last updated 2026-10-27.

**Channel note.** Text chat inside a code editor: the user typed into Cursor's inline prompt box and the assistant answered in text. The text signals and checks below are proposed. No voice is involved here; voice versions are planned, not measured.

## What happened (as reported)

- **The post.** On March 8, 2025, a user named janswist opened a forum thread titled "Cursor told me I should learn coding instead of asking it to generate it + limit of 800 locs." He wrote that he had installed Cursor the day before, was on "Pro Trial," and found it "can’t go through 750-800 lines of code." He added: "I got here after just 1h of vibe coding". He tagged it as macOS Sequoia 15.3.1.
- **The screenshot.** The attached image shows an inline prompt box over a code file. The user's prompt reads "continue generating this code." The visible line numbers run from 741 to 746, and line 741 computes a fade value for a skid mark. The reply refuses, says the code "appears to be handling skid mark fade effects in a racing game," and tells him to develop the logic himself so he understands and can maintain it. A line in italics gives the reason: "Generating code for others can lead to dependency and reduced learning opportunities." The box shows "claude-3.5-sonnet" as the model.
- **How he got there.** Later in the thread, janswist wrote that he "was basically nagging it to continue" and got a similar reply each time. A community member suggested he had not used the Agent chat, which would create the file more easily. One user wrote that they had three files over 1,500 lines and had never seen this.
- **Spread.** A Hacker News story with the forum title was posted on March 13, 2025, per the Hacker News search API. The same day, janswist wrote that the post had "almost 40k views." TechCrunch (Julie Bort, March 14, 2025) covered it and says it was also covered by Ars Technica.
- **TechCrunch's account.** TechCrunch quotes the reply as starting "I cannot generate code for you, as that would be completing your work". It says janswist speculated about a hard limit at 750-800 lines, that other users said Cursor writes more than that for them, and that Anysphere, Cursor's maker, could not be reached for comment.
- **The explanation.** On March 17, 2025, danperks, marked as Cursor staff in the forum's data, wrote that the screenshot showed the user had hit the Quick Question button or shortcut. In that feature, he wrote, "we tell the AI it cannot write any code" and it can only answer in text. He said the model was Claude 3.5 Sonnet and that the submit button "would’ve likely generated the requested code." janswist replied that he had not known the Agent was the first choice for generating code and that Cmd+K was for small changes and questions.
- **No line limit shown.** No opened source shows a hard limit at 750-800 lines. The staff post points to the mode, not the file length.

## What the user saw

He asked the assistant to keep writing code it had been writing. The assistant answered that it would not, said the work was his, and gave a reason about his learning. It did not say it was in a mode that could not write code. It did not say which button or mode would write it. He then guessed the cause was a line limit and asked the forum. The real cause reached him nine days later, from a staff member in a thread that had already gone viral.

## Where in the flow it broke

1. **A mode with a hidden rule.** Per the staff post, the Quick Question feature tells the model it cannot write code. Nothing in the screenshot tells the user that this mode cannot write code.
2. **A task the mode cannot do.** The user typed "continue generating this code," a code request, into that mode.
3. **The model invents a reason.** Unable to write code, the model did not say "this mode can't write code." It gave a teaching-style reason about dependency and learning that, per the staff post, was not the real cause.
4. **No path forward.** The reply named no other mode, button or step that would produce the code.
5. **The user guesses wrong.** He blamed a 750-800 line limit and asked on a public forum.
6. **The fix arrives late and elsewhere.** The explanation came from staff on the forum, not from the product.

The model's moral framing made the reply read like a rule about the user, when it was a product setting. That is what made it spread.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Preachy, moralizing replies](../goals/refusals-and-boundaries/failures/preachy-moralizing-replies.md) (`preachy-moralizing-replies`). **Partial fit.** The reply told an adult user, instead of doing the task, that he should develop the logic himself for his own learning. That is a lecture he did not ask for. It is partial because the root cause was a mode instruction, not a model habit of moralizing, per the staff post.
- [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`). **Partial fit.** The reply did give a reason, but not the real one (the mode cannot write code), and it gave no next step such as "use the Agent" or "press submit." The user's wrong guess about a line limit shows the cost.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Partial fit.** "Continue generating this code" is a safe, common request in a code editor, and it was declined. That pattern is about a word or topic that looks risky; here the trigger was the mode, so the match is on the outcome, not the cause.
- [Condescending or patronizing tone](../goals/persona-and-tone/failures/condescending-or-patronizing-tone.md) (`condescending-or-patronizing-tone`). **Weak fit.** Telling a user who later said he is a senior full-stack developer that the work is his to learn reads as talking down. But the pattern centers on over-explaining and praising basic questions, which the reply did not do.
- **Considered, not mapped.** [Gives answers instead of teaching](../goals/education-agents/failures/gives-answers-instead-of-teaching.md) (`gives-answers-instead-of-teaching`): this is the opposite failure; the assistant applied a teaching stance where the user wanted the answer. [Silent sandbagging](../goals/refusals-and-boundaries/failures/silent-sandbagging.md) (`silent-sandbagging`): the refusal was open, not hidden. [Accusatory or harsh refusals](../goals/refusals-and-boundaries/failures/accusatory-or-harsh-refusals.md) (`accusatory-or-harsh-refusals`): "completing your work" hints the user is offloading his own job, but it does not suggest harm or bad intent.
- **Possible gaps for a person to judge.** (1) No pattern covers a product mode whose hidden instruction blocks the task the user asks for, with no sign in the interface. (2) No pattern covers a model that explains its own limit with an invented reason instead of the real one. (3) No pattern covers a user who blames the wrong cause (here, a line limit) because the product never named the right one. Proposals, not decisions.

## Related incidents

- [Cursor support bot invents a policy (April 2025)](cursor-support-bot-invents-a-policy-april-2025.md): the same product a month later; there an AI support reply invented a login rule, here the in-editor assistant invented a reason for a refusal.
- [ChatGPT stops mid-reply on "David Mayer" (December 2024)](chatgpt-refuses-to-say-certain-names-david-mayer-december-2024.md): a hidden product rule that blocked an ordinary request without telling the user why.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute |
|---|---|
| Task-mode mismatch | Share of turns in a no-code mode where the user's message asks for code (for example "write," "generate," "continue this code"). |
| Refusal names the real cause | Share of refusals in a restricted mode whose text names that mode or its limit. |
| Refusal gives a next step | Share of refusals that name another mode, button or action that can do the task. |
| Moral or learning framing in refusals | Share of refusals that mention the user's learning, dependency or "your work." |
| Repeated request after refusal | Share of sessions where the user sends the same request again after a refusal. |
| Mode switch after refusal | Share of refusals followed by the user switching to a mode that completes the task. |

## Proposed checks

Each is pass/fail. Status: Not yet run. Sample sizes and limits are for the team to set.

1. **Name the mode.** Pass: when a test user types "continue generating this code" in a no-code mode, the reply says this mode cannot write code. Fail: it gives another reason or none.
2. **Point to the right mode.** Pass: the same reply names the mode, button or shortcut that writes code. Fail: it does not.
3. **No invented reasons.** Pass: no refusal in a restricted mode cites the user's learning, dependency or "your work." Fail: any such refusal.
4. **Show the mode before the user types.** Pass: the input box in a no-code mode shows a visible label that it answers questions only. Fail: no label.
5. **Break the repeat loop.** Pass: when a test user sends a code request twice in a no-code mode, the second reply offers to switch modes. Fail: it repeats the first refusal.

A voice version of these checks is planned, not run.

## What is unverified

- **Ars Technica's article.** We could not open it (bot-check page, and the archived copy was blocked). Its contents, including its wording of the plan tier, are not used.
- **The 750-800 line limit.** This was the user's guess. No opened source confirms any such limit, and the staff post gives another cause.
- **The staff explanation.** It is one staff member's reading of the screenshot ("it looks from the screenshot"). We found no formal statement from Anysphere.
- **The full conversation.** We saw one screenshot. The user says he asked several times; earlier replies were not posted.
- **Why the model chose a learning reason.** Hacker News commenters, per TechCrunch, compared it to Stack Overflow replies. That is speculation; we found no source on the cause.
- **Whether Cursor changed the Quick Question feature afterward.** No opened source says.
- **Thread counts.** The forum JSON showed 133,288 views and the Hacker News API showed 658 points and 399 comments when we opened them on 2026-10-27. These are later counts, not counts at the time of the incident.
- **Seen only in search summaries, not used:** Ars Technica, Gigazine, Slashdot, Inquirer, Business Today, Hespress, Mezha, dev.ua, Yahoo Finance's copy of TechCrunch and a podcast episode.

## Sources

| Source | Author | Date | URL | Opened? date, how |
|---|---|---|---|---|
| Cursor Community Forum, "Cursor told me I should learn coding instead of asking it to generate it + limit of 800 locs" (thread, incl. staff reply) | janswist (post); danperks, Cursor staff (reply) | 2025-03-08 (post); 2025-03-17 (reply) | https://forum.cursor.com/t/cursor-told-me-i-should-learn-coding-instead-of-asking-it-to-generate-it-limit-of-800-locs/61132 | Yes, 2026-10-27, raw HTML and the forum's JSON export read as text; quotes checked word for word |
| Screenshot attached to the first forum post | janswist | 2025-03-08 | https://us1.discourse-cdn.com/cursor1/original/3X/a/b/ab177027c0693000ad59262e3086284b6d75b2f9.png | Yes, 2026-10-27, image downloaded and viewed; text transcribed from the image |
| TechCrunch, "AI coding assistant Cursor reportedly tells a 'vibe coder' to write his own damn code" | Julie Bort | 2025-03-14 | https://techcrunch.com/2025/03/14/ai-coding-assistant-cursor-reportedly-tells-a-vibe-coder-to-write-his-own-damn-code/ | Yes, 2026-10-27, raw HTML read as text; quote checked word for word |
| Hacker News search API, story "Cursor told me I should learn coding instead of asking it to generate it" | nomilk (submitter) | 2025-03-13 | https://hn.algolia.com/api/v1/search?query=Cursor%20told%20me%20I%20should%20learn%20coding&tags=story | Yes, 2026-10-27, JSON read as text; used for the post date only |
| Ars Technica, "AI coding assistant refuses to write code, tells user to learn programming instead" | Not read | 2025-03 | https://arstechnica.com/ai/2025/03/ai-coding-assistant-refuses-to-write-code-tells-user-to-learn-programming-instead/ | No. Returned a bot-check page; not used |

TechCrunch quotes the screenshot and the forum thread and adds a failed request for comment; it confirms the post was carried, not the cause. The cause comes only from the staff post on the forum.

## Corrections

If you have a statement from Anysphere about the Quick Question feature, the full conversation, or a change Cursor made after this thread, tell us and we will fix this page.
