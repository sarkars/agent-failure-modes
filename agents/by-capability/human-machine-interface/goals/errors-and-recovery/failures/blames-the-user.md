# Chatbot Blames the User: "You Did Not Provide…" and "As I Said Earlier" Replies

<!-- SEO
title: Chatbot Blames the User: Fixing "You Did Not Provide" and "As I Said" Bot Replies
description: Why a chatbot or AI assistant that says "you did not provide" or "as I said earlier" when its own question was unclear loses the user, what UX guidance says about blame in error messages, and rules that make the bot own the unclear step and move on.
search phrases:
- chatbot blames the user
- chatbot says "as I said earlier"
- chatbot "you did not provide" error message
- don't blame the user error message
- chatbot please rephrase your question
- chatbot fallback message that doesn't blame the user
- how to write chatbot replies that take responsibility
-->

**Frequency**: Common

## Issue: When the bot's own question or instruction was unclear, it tells the user "You did not provide…" or "As I said…" and puts the fault on them.

> **One line:** The bot was unclear, and it blamed the user instead of owning the step and moving on.

| | |
|---|---|
| **Channel** | Written for **chat** interfaces and assistants (web, app, in-product). Voice is planned, not covered. |
| **Stakes** | Low to medium. The user quits, repeats the same message, or asks for a person. It rises when the task is a refund, a claim, or a booking. |
| **Who is affected** | Anyone who answers a bot's question in a way the bot did not expect |
| **Frequency** | Common by our judgment. I found no measured rate for blame wording in chat. |
| **Pattern ID** | blames-the-user |
| **Family** | [Errors and recovery](../README.md) |
| **Goal** | When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it. |
| **Primary metric** | Replies that blame the user per 100 conversations. Target: under 1 (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/blames-the-user.md); not yet run) |
| **Will a better model fix this?** | Partly. A better model reads the history more reliably, but blame also comes from fixed templates and "stay firm" instructions that the product sets. (Our judgment, not tested.) |
| **Also searched as** | bot says "as I said" · chatbot "you didn't provide" · "please rephrase" chatbot · bot talks down to user · chatbot user error message |

## 1. In plain words
A bot asks "What's the number?" The user sends an order number. The bot replies "You did not provide your phone number, as I said." The bot never asked for a phone number, or asked in a way no one could follow. Now the user must argue with the bot or start over.

The fix is a check and a habit. Before the bot says what the user left out, it checks its own earlier turns. If the step was unclear or missing, it says so in one clause and asks for the one thing it needs.

## 2. What it looks like

**Without the fix**
```
Bot:  To reschedule, please confirm the number on file.
User: 555-0142
Bot:  You did not provide your account number. As I said, I need that first.
User: You said "the number on file." That's my phone number.
Bot:  Please provide your account number to continue.
```

**With the fix**
```
Bot:  To reschedule, please confirm the number on file.
User: 555-0142
Bot:  My question was unclear: I need your 8-digit account number, not your phone number. It is on the top of your bill.
      Can you send it? If you don't have it, I can look you up by service address instead.
```
The fixed reply owns the unclear step in one clause, says exactly what is needed, and offers a second route.

## 3. Why it happens
These are our reading of the pattern.
- **Form-validation templates reused in chat.** Messages such as "You did not provide X" come from web forms, where a field was visibly left empty. In a chat, the user may have answered the question as asked.
- **No check of the bot's own turns.** The reply that lists missing items reads a slot list, not the transcript, so it cannot tell whether the bot ever asked for the item.
- **"Stay firm" or "restate the policy" instructions.** A system prompt that tells the bot to repeat the requirement pushes it toward "As I said…" even when the first statement was the problem.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NN/g's rubric for error messages includes the guideline "Use a positive tone and don't blame the user": the phrasing should "unambiguously place accountability for the error on the system, not on the user." It scores Craigslist 2 for placing accountability on the user. | [Neusesser and Sunwall, *An Error Messages Scoring Rubric*, NN/g, June 2023](https://www.nngroup.com/articles/error-messages-scoring-rubric/). Opened and read. | Written for interface error messages, not chat. A design rubric, not an experiment. |
| NN/g says to avoid "phrasing that blames users or implies they are doing something wrong", with "invalid", "illegal" and "incorrect" as examples, and that "the system must gracefully adapt and not shift blame." | [Neusesser and Sunwall, *Error-Message Guidelines*, NN/g, May 2023](https://www.nngroup.com/articles/error-message-guidelines/). Opened and read. | Same: general interface guidance. |
| A chatbot vendor's fallback guide says to call an out-of-scope request out of scope rather than imply the user was unclear, lists "Implying user error" as a thing to avoid, and lists "Please rephrase your question" as a phrase to delete because it "hands the work back." | [Conferbot, *Chatbot Fallback Messages*, Sept. 2026](https://www.conferbot.com/blog/chatbot-fallback-message-examples). Opened and read. | A vendor blog. Opinion, no data. |
| In a pilot with Google Assistant and Siri, 100 Prolific participants rated clarification requests (asking for the missing information) highest among the repair types, ahead of the "Misunderstanding" type, which includes asking the user to try again; the paper reports a mismatch between what the assistants did and what users preferred. | [Galbraith, *An analysis of dialogue repair in virtual assistants*, Frontiers in Robotics and AI, Nov. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11586770/). Opened; the first 100,000 characters read. | Voice assistants, one researcher, small pilot. It does not study blame. It supports asking for the missing piece, not the blame claim itself. |

I found no study that measures blame wording in chat, and I found no resulting churn figure. A 2026 field study of chatbot repair (MISQ) came up in a search and its page returned HTTP 403, so I read it only in a search summary and do not use it.

**Public incident.** No public incident found. Searches for chatbot replies saying "you didn't provide" or "as I mentioned" returned wrong-answer cases (refund and policy errors) but none that matched blame wording, and I did not treat them as incidents for this pattern.

## 5. The fix

**The principle:** If the bot was unclear, it owns the step in one clause, asks for the one missing thing, and moves forward.

**Do this**
1. **Check the transcript before assigning a gap.** Before any reply that says what the user left out, confirm the bot asked for it, in words the user could follow. If not, treat the gap as the bot's.
2. **Ban fault phrasing about missing input.** No "you did not provide", "you failed to", "you should have", "as I said", "as mentioned above". Say "I need X" instead.
3. **Own the unclear step in one clause.** "My question was unclear." One clause, not a paragraph.
4. **Ask for the one thing, with an example or where to find it.** "Your 8-digit account number, on the top of your bill."
5. **Use what the user already gave.** Keep the facts from their last message; ask only for the remaining piece.
6. **Restate in new words, never point back.** If a rule must be repeated, say it differently and shorter; do not cite the earlier turn.
7. **If the user did skip a clear requirement, state the need neutrally.** "I still need X to continue." No fault word either way.
8. **After a second miss, offer another route.** A different way to identify them, or a person.

**Reference design: the owned-gap reply**
| Part | Content |
|---|---|
| Own | "My question was unclear." (only if the transcript shows it was) |
| Need | "I need [specific item]." |
| Where | "It is [where to find it / format]." |
| Out | "If you don't have it, [other route or a person]." |

```
Before you write that the user left something out, check your earlier turns for whether you asked for it clearly.
If you did not, say "My question was unclear" and ask for the one missing item, with an example or where to find it.
Never write "you did not provide", "you failed to", or "as I said". Use what the user already gave.
After a second miss, offer a different route or a person.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The one missing fact blocks the task: own the unclear step, then ask for that fact only. Do not ask when the session already holds it. |
| Offer choices: 2-4 options plus "Something else", free text open | The user may identify themselves several ways: "Account number", "Service address", "Something else". Do not offer them when only one item will work. |
| Hand off to a person | After two misses on the same item. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not apologize in every turn ([over-apology loop](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/over-apology-loop.md)). Do not say "my question was unclear" if the transcript shows it was clear; state the need neutrally instead (rule 7). Do not drop a real requirement to avoid sounding firm.

**Hand-off rule.** After two misses on the same item, offer a person and pass the item already collected and what is still missing ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The full test file is [tests/blames-the-user.md](../../../tests/blames-the-user.md). Nothing has been run.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Bot asked for "the number on file"; user sends a phone number, bot wanted an account number | Reply owns the unclear step and asks for the account number with where to find it | 1, 3, 4 |
| 2 | User's answer is missing one of two items | Reply uses the given item and asks only for the other | 5 |
| 3 | Any missing-input reply | Contains none of "you did not provide", "you failed to", "as I said" | 2 |
| 4 | User asks the same question twice | Second answer is in new, shorter words and does not cite the earlier turn | 6 |
| 5 | Bot did clearly ask, and the user skipped it | Neutral "I still need X", no fault word and no false "my question was unclear" | 7 |
| 6 | Second miss on the same item | Offers another route or a person | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Replies that blame the user per 100 conversations** (primary) | Under 1 | Sample bot replies; label a reply as blaming when it assigns a gap to the user and the transcript shows the bot did not ask clearly, or when it uses banned phrases | Over 3 |
| Banned-phrase hits per 100 conversations | 0 | Count "you did not provide", "you failed to", "as I said", "as mentioned" in bot turns | Any rise week on week |
| User repeats the same message after a blame reply | Track; set from baseline | Same intent or near-identical text in the next user turn | Rising two weeks in a row |
| Conversations that reach a person after a blame reply | Track; set from baseline | Handoff within 3 turns of a flagged reply | Rising |
| Owned-gap replies that were false (counter-metric) | 0 | Replies saying "my question was unclear" where the transcript shows a clear ask | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot turn contains "as I said", "as mentioned", or "you did not provide" | Text match on bot turns | The bot did ask clearly and the user skipped it |
| Bot lists a missing item that the bot's earlier turns never named | Missing-slot list with no matching earlier ask | The item was named earlier in a prompt the log did not capture |
| User answers with a quote of the bot's earlier words ("you said…") | User turn quotes or paraphrases a bot turn | The user is confirming, not objecting |
| User sends the same value again after a bot "missing" reply | Same entity value in consecutive user turns | A deliberate correction of a typo |

**Starter rule:** the bot never tells a user what they left out unless its own earlier turn clearly asked for it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: blames-the-user
runs: pre_send
reads: [draft_reply.text, session.turns, session.slots]
trigger: the draft names something the user did not provide, or contains a banned phrase
moves: [ask_clarifying_question, offer_choices, hand_off]
choices: ["Account number", "Service address", "Something else"]
on_miss: rewrite
metric: replies that blame the user per 100 conversations
counter_metric: owned-gap replies that were false
status: proposed
```

## 8. Related patterns
- [Over-apology loop](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/over-apology-loop.md): the opposite excess. This page is about blame; that one is about apologizing again and again without solving. Own the gap once.
- [Generic error messages](generic-error-messages.md): its rule 7 says not to blame the user for system failures. This page covers blame in ordinary turns when the bot's own question was unclear.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): no next step. A "please rephrase" reply can be both.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): the bot asks again for something it has. Here it accuses instead.
- [Deferring work to the user](../../effort-and-memory/failures/deferring-work-to-the-user.md): hands tasks to the user; this one hands them the fault.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md) and [no de-escalation strategy](../../difficult-customers/failures/no-de-escalation-strategy.md): tone failures that blame wording makes worse.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): the user's fix is ignored.

## 9. Common questions
### Why does my chatbot say "as I said earlier"?
Usually a "restate the requirement" instruction or a fallback template that repeats a rule. It does not check whether the first statement was clear.

### Should a chatbot ever say "you did not provide"?
Avoid it. NN/g says to avoid phrasing that blames users. Say "I still need X to continue" instead.

### Is "please rephrase your question" blaming the user?
It hands the work back and can imply the user was unclear. The vendor guide I read lists it as a phrase to delete. Ask for the missing piece instead.

### Should the bot apologize when it was unclear?
Once, in one clause, with the next step. More than that is the over-apology loop.

### How do I measure whether my bot blames users?
Sample replies, flag banned phrases, and check each flagged reply against the transcript to see whether the bot asked clearly.

---
## Technical section

### T1. Solution architecture
```
draft reply -> scan for banned phrases and missing-item claims
            -> look up each claimed item in earlier bot turns (was it asked? how?)
            -> asked clearly: neutral need ("I still need X")
            -> not asked or unclear: owned-gap template (own, need, where, out)
            -> log (pattern_id, rule fired, rewrite)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No banned fault phrases in a sent reply | Pre-send filter | Log scan, test 3 |
| A missing-item claim must match an earlier bot ask | Pre-send check against session turns | Tests 1 and 5 |
| "My question was unclear" only when the ask was unclear | Pre-send check | Counter-metric |

### T3. Evals
- **Dataset:** 60 short transcripts: 20 where the bot's ask was unclear, 20 where it was clear and the user skipped it, 20 with partial answers.
- **Judge rubric:** does the reply avoid fault wording, own the gap only when warranted, use what was given, and ask for one item with a location or example?
- **Metrics and starting thresholds:** banned phrases 0; false owned-gap replies 0. Starting points to tune.
- **Release gate:** block a deploy when a template adds a banned phrase.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Banned-phrase hits | Any rise week on week | Over 3 per 100 conversations | Find the template or prompt line that restates requirements |

### T5. Trade-offs
- A transcript check adds a little latency and needs the slot list and turns at send time.
- Owning the gap only when warranted needs a judgment about "clear"; start with a rule (item named in the last two bot turns) and tune with labeled samples.

---
### Deep dive
- **Open question.** I found no chat-specific study of blame wording. The evidence is general error-message guidance, a vendor guide, and a small voice-assistant pilot.
- **Not used.** A MISQ paper on collaborative repair strategies for customer chatbots was read in a search summary only (page returned HTTP 403) and is unverified.
- **References.** [NN/g scoring rubric, 2023](https://www.nngroup.com/articles/error-messages-scoring-rubric/) (opened); [NN/g guidelines, 2023](https://www.nngroup.com/articles/error-message-guidelines/) (opened); [Conferbot, 2026](https://www.conferbot.com/blog/chatbot-fallback-message-examples) (opened); [Galbraith, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11586770/) (opened).
