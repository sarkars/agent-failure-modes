# Chatbot Failure Audit: A Free Review of Your Chat Transcripts (Draft Offer)

This page describes a free, no-code review of a sample of chat transcripts, for developers and teams who run a text chatbot and want to know which written failure patterns show up in their own conversations.

> **Status: Draft, not offered yet.** Written 2026-10-22. The offer is not open. There is no contact route, no sign-up, and no one to send transcripts to. It waits for an owner decision listed as open in the [distribution plan](../roadmap/distribution-plan.md): whether to offer free failure audits to outside teams, and who handles the transcripts. No audit has been run. This page uses no outside data.

## What the audit would look at
- **Input:** a sample of the team's own text chat transcripts, with personal data removed before sharing (see "Data handling" below). Sample size, format and selection are not decided.
- **Method:** a reviewer reads each transcript against the written patterns in the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md). Each pattern page has a "Detection signals (proposed, not yet calibrated)" block. The reviewer marks where a signal fires, then checks the counter-signal on the same row before calling it a finding.
- **Honest limit:** the signals are proposed. They have not been checked against human-labeled conversations. The study that would check them, [S0](studies/s0-do-our-detectors-agree-with-people.md), is a draft. So every finding is a reviewer's reading of one transcript, not a measured rate.
- **Channel:** text chat only. Voice and web-page signals are planned, not written, so voice calls and page-behavior logs are out of scope.

## What the team would get
- A written report that lists each finding by **Pattern ID**, with a link to that pattern's page.
- For each finding: the transcript excerpt (as redacted by the team), the proposed signal that fired, and the counter-signal the reviewer ruled out.
- For each finding: the fix from the pattern page and the [conversation moves](../solutions-library/conversation-moves.md) its Guide spec names.
- Where it fits, a pointer to the matching instruction block in the [L1 base agent design](../roadmap/l1-base-agent-design.md), which copies each pattern's reference design into a prompt.
- No promise of any metric change. The report does not predict fewer drop-offs, more containment, or any other number. If a team wants to measure a change, the pattern pages name the metric to track; see also [metrics](metrics.md) and the [glossary](glossary.md).

The write-up is meant to be anonymous: no company name, product name or user detail. Whether a write-up is ever published, and with whose consent, is part of the open owner decision.

## What it is not
- **Not a guarantee.** A clean report does not mean the bot has no failures. A sample shows only what is in the sample.
- **Not legal or compliance review.** About 99 pattern pages carry a "Read this first" notice that they are design guidance, not legal advice. The audit inherits that limit.
- **Not a security test.** It is not a penetration test, a red-team exercise, or a prompt-injection test.
- **Not a model evaluation.** It reads conversations, not the model, code or prompt.

## Data handling: open design questions for the owner
No policy exists yet. These are the questions the owner would need to answer before any transcript is shared:
1. **Redaction.** Who removes names, emails, phone numbers, addresses, order numbers and payment details, and is it done before the transcripts leave the team? Can the team send only redacted text?
2. **Who reads them.** Which named people see the transcripts, and does anyone outside that list (including any AI tool) process them?
3. **Retention.** How long are transcripts kept, where, and how is deletion confirmed to the team?
4. **Consent.** Did the team's users agree to their chats being reviewed by an outside party? The team, not this project, would need to answer that.
5. **Publication.** Is any excerpt ever published, and does the team sign off on each one?

The [privacy, governance and access notes](../roadmap/privacy-governance-and-access.md) are background reading for these questions. They are not a policy for this offer.

## Worked example: a sample audit of a synthetic transcript

> **Synthetic.** This transcript was written for this page. No real user, bot or company is involved. "Acme Home" is the invented online retailer from the [L1 base agent design](../roadmap/l1-base-agent-design.md), treated here as a US store. The bot below does **not** follow the L1 instructions; the findings show which L1 blocks would address each problem. All prices and dates in it are invented.

Setup: the user is signed in to the Acme Home site and has one recent order. The log shows no session or account lookup before the bot's first question.

```
1  User: where is my order
2  Bot:  Great question! Order tracking is something many customers ask about. Can you tell me your email address and your order number?
3  User: im logged in, its on your site
4  Bot:  Sorry, I didn't understand that. Please try again.
5  User: the blue lamp i ordered last week
6  Bot:  Sorry, I didn't understand that. Please try again.
7  User: can i just return it then
8  Bot:  Thanks for asking about returns! Our return policy is designed to be flexible. Most items can be returned. You have 14 days from delivery to start a return, and a $7.95 return shipping fee applies.
9  User: agent
10 Bot:  Sorry, I didn't understand that. Please try again.
11 User: forget it
   [session ends]
```

### Sample findings

| Pattern ID | Where in the transcript | Proposed signal that fired | Suggested fix move |
|---|---|---|---|
| [`re-asks-for-known-information`](../goals/embedded-copilots/failures/re-asks-for-known-information.md) | Line 2 | "Assistant asks an identity or account question before any session or account lookup" (no lookup in the log; the user is signed in, so the counter-signal does not apply) | **Lead with the answer:** look up the session and account first, then state what was found and ask for a yes ("Your most recent order is 48213. Is that the one?") |
| [`re-asks-for-known-information`](../goals/embedded-copilots/failures/re-asks-for-known-information.md) | Line 3 | "User answers with a note that the product already has it" | Same fix. L1 group A, "re asks for known information" block |
| [`answer-buried`](../goals/response-structure/failures/answer-buried.md) | Line 2 | "Reply opens with praise or a restatement of the question" ("Great question!"); not the first-turn greeting the counter-signal allows | **Lead with the answer:** the first sentence holds the answer or the next step. L1 group B, "answer buried" block |
| [`answer-buried`](../goals/response-structure/failures/answer-buried.md) | Line 8 | "Deadline, fee, or safety step appears only after the first two sentences" (the 14-day deadline and the fee are in sentence 4) | **Lead with the answer:** put deadlines and fees in the first two sentences |
| [`dead-end-i-don-t-understand-replies`](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | Lines 4 and 6 | "Identical fallback reply twice in a row" | **Offer choices** on the first miss (closest options plus "something else"), then **Ask one clarifying question** on the second, with a person offered. L1 group A, "dead end" block |
| [`dead-end-i-don-t-understand-replies`](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | Lines 9 and 10 | "User asks for a person and no handoff follows" | **Hand off to a person** at once when the user asks, with a summary |
| [`dead-end-i-don-t-understand-replies`](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | Lines 10 and 11 | "Conversation ends within 2 turns of a fallback" | Same ladder; the counter-signal (user got the answer elsewhere) cannot be ruled out from the log alone |
| [`confident-wrong-answer-with-no-way-to-check`](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) | Line 8 | "A policy, price, deadline, or eligibility answer with no source passage or link" | **Lead with the answer** only from a retrieved passage, shown with its link; if the source is weak or missing, **Admit uncertainty and show how to check**. L1 group B, "confident wrong answer" block |

### How to read these findings
- A signal firing is not proof of a failure. Line 8 shows no source, but the audit cannot say whether the 14-day rule is wrong; only the team's policy can settle that.
- The eight findings come from four patterns. The count describes this one synthetic transcript, nothing more.
- Each fix quoted above is the fix on that pattern's page. The test file linked from each page lists scenarios to check the fix; none has been run.

## Sources
No outside sources; built from library pages. Pages read for this draft:
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md) (Pattern IDs and the "Read this first" count)
- The four pattern pages linked in the findings table (signals, counter-signals, fixes and Moves)
- [Conversation moves](../solutions-library/conversation-moves.md)
- [L1 base agent design](../roadmap/l1-base-agent-design.md)
- [Distribution plan](../roadmap/distribution-plan.md) (asset 8, loop 4, open owner decision 5)
