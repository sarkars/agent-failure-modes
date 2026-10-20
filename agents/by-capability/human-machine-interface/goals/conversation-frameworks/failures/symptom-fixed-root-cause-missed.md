# Chatbot Fixes the Same Problem Again and Again: Symptom Fixed, Root Cause Missed

<!-- SEO
title: Chatbot Fixes the Symptom, Not the Cause: How to Fix It
description: Why a support chatbot solves the problem the user stated, not what is causing it, so the same user returns with the same issue, and how to check the cause on a repeat.
search phrases:
- chatbot fixes the symptom not the root cause
- customer keeps contacting support for the same problem
- chatbot solved my issue but it came back
- how to reduce repeat contacts with a support chatbot
- chatbot doesn't look at my previous chats
- chatbot keeps giving the same workaround
- how to make a chatbot find the root cause
-->

**Frequency**: Common

## Issue: The bot resolves what the user said ("my autopay failed") and never asks what is causing it, so the same user comes back with the same problem.

> **One line:** The bot treats a repeat problem as a new one and applies the same fix; the fix is to check the cause when the same problem comes back, before offering the fix again.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Low to medium. Each repeat costs the user time and the business a contact; money problems cost more. |
| **Who is affected** | Users who return with a problem the bot "fixed" before, and the team that pays for the extra contacts |
| **Frequency** | Common. This is our judgment; I found no study that counts how often chatbots fix symptoms only. |
| **Pattern ID** | symptom-fixed-root-cause-missed |
| **Family** | [Conversation frameworks](../README.md) (row FW-C03) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Repeat-contact rate for the same root cause. Start: track a baseline, then aim to lower it (no target is sourced) |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model may ask better "why" questions, but it can only see past contacts and account data if the product gives it access and a rule to look. (Our judgment, not tested.) |
| **Also searched as** | chatbot same problem keeps coming back · repeat contact chatbot · chatbot band-aid fix · chatbot ignores chat history · support bot doesn't find root cause |

## 1. In plain words
A user says what went wrong, and the bot fixes exactly that. A week later the same thing goes wrong, and the bot fixes it again as if it had never met the user. A good support person notices the repeat and asks what keeps causing it. The bot only closes the question it was handed.

## 2. What it looks like
**Without the fix** (a utility's billing chat, third failed autopay in three months)
```
User: My autopay failed again. Can you take the payment now?
Bot:  Sorry about that! I've processed your $84.20 payment with the card on file. You're all set.
User: Thanks.
      (user returns 5 weeks later: "autopay failed AGAIN"; the bot repeats the same one-time payment)
```
**With the fix**
```
User: My autopay failed again. Can you take the payment now?
Bot:  I can take the $84.20 payment now. First, this is the third failed autopay since July, so I want to check why.
      The card on file ends in 4417 and shows an expiry of 06/26. Is that card still active?
User: No, the bank sent me a new one this summer.
Bot:  That explains it. Want to put the new card on autopay, or pay by bank account? You can also tell me something else.
User: New card.
Bot:  Added to autopay, and today's $84.20 payment is done. Next month's bill will charge the new card.
```
The fixed bot still does what the user asked, then checks the cause because this is a repeat, and fixes the cause.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **Every contact starts blank.** The bot gets the current message and no link to earlier contacts, so it cannot tell a repeat from a first.
- **"Resolved" means the question was answered.** Success is counted per ticket or chat, so a workaround and a real fix look the same (see section 4).
- **The bot has no diagnostic step.** Its prompt says "solve the user's problem," which it reads as the stated request, and nothing says when to ask why.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Resolution is usually counted per ticket in one channel. The article says the rate "is calculated per ticket, inside one channel," so a customer who gets an unclear answer and calls two days later "generates two resolved tickets and two clean FCR scores." It calls this "the single largest blind spot in support analytics." | [Enterpret, *The 6 Best Tools to Diagnose Repeat Customer Contacts in 2026*](https://www.enterpret.com/guides/the-6-best-tools-to-diagnose-repeat-customer-contacts-in-2026). Opened; dated August 31, 2026. | Vendor guide. It gives no statistic on how often this happens. It describes a measurement gap, not bot behavior. |
| Customers who get the first question answered often leave with the underlying need unmet. The article calls this the "second question" problem and "a key driver of repeat contacts." | [SQM Group, *The Second Question Problem*](https://www.sqmgroup.com/resources/library/blog/the-second-question-problem-why-customers-do-not-ask-what-they-really-need). Opened; published April 14, 2026. | Consultancy opinion with no numbers. About human agents. It is about unasked needs, a neighbor of this failure. |
| The 5 Whys method warns that teams "focus too quickly on the solution rather than the problem," that what seems to be the cause "is sometimes just one symptom among others," and that a problem can have several root causes. | [Institute for Healthcare Improvement, *5 Whys* (French page)](https://ihi.org/fr/node/22961). Opened; my translation of the quoted French. | A quality-improvement tool from health care and manufacturing, not a chatbot study. It supports "ask why again," not any metric. |

Not opened, used nowhere in the fix: search summaries mentioned a "15-35% of calls are repeats" figure (a vendor claim, unverified), a call-reason analytics blog, and a Giga root-cause article. I found no controlled study of chatbots and repeat contacts.

**Public incident.** No public incident found. I searched root-cause analysis for support repeat contacts, 5 Whys versus symptom, and chatbots that resolve the stated request but not the underlying problem. The results were vendor guides and method pages, not a dated incident I could open.

## 5. The fix
**The principle:** When the same problem returns, the bot checks why before it offers the same fix again.

**Do this**
1. **Look for a prior match before applying a fix.** Compare the new request with this user's earlier contacts and bot actions (start with 30 days, a starting point) by problem type.
2. **On a match, say it is a repeat.** One sentence, such as "this is the third failed autopay since July," then still give the user what they asked for.
3. **Ask one question about the cause, not about the symptom.** Name what you saw in the account ("the card on file ends in 4417 and expires 06/26") and ask whether it is still true.
4. **Fix the cause, or say who can.** If the bot can change it (update the card), do it after the user agrees. If it cannot, say so and hand off.
5. **Do not repeat the same workaround a third time.** After two identical workarounds for the same user and problem, the next reply must ask the cause question or hand off.
6. **Record the result.** Save a cause tag (for example `expired_card`) and whether the workaround or the cause was fixed, so later contacts can match it.
7. **Say what to expect.** After a cause fix, state what happens next ("next month's bill charges the new card"), and do not promise it will never recur.

**Reference design: the repeat-check block (paste into the system prompt)**
```
Before you apply a fix, check this user's past contacts (last 30 days) for the same problem type.
If there is a match: say it is a repeat in one sentence, still give the user what they asked for,
then ask ONE question about the cause, citing a fact from the account ("your card ends in 4417 and expires 06/26").
If the cause is something you can change, offer to change it and wait for a yes. If you cannot, hand off with a summary.
Never apply the same workaround a third time without asking about the cause.
If there is no match, solve the problem and do not ask about causes.
```
State to keep: `{ "problem_type": "autopay_failed", "prior_matches": 2, "workaround_count": 2, "cause_tag": "expired_card", "cause_fixed": true }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A repeat arrives: give the requested fix first, then check the cause. |
| Ask one clarifying question | The cause is unclear: one question tied to a fact in the account. |
| Offer choices: 2-4 options plus "Something else", free text open | Several fixes fit the cause: "New card on autopay", "Bank account", "Keep paying by hand", "Something else". |
| Hand off to a person | The bot cannot change the cause, or the same problem has come back after a cause fix. |

**Don't over-correct.** A first-time problem gets a fix, not an interview. Do not ask "why" five times, do not assume a repeat means the user did something wrong, and do not tell the user their problem is "recurring" when the match is weak. The guardrail is the prior match: no match, no cause question. If the user says "just take the payment," do it and offer the cause check once.

**Hand-off rule.** If the cause is outside what the bot can see or change (a billing-system defect, a network fault), or the problem returns after a cause fix, pass the user's goal, the contact dates, the workarounds applied, and the cause tag to a person.

**Framework used:** none yet. Candidate: the 5 Whys idea of asking why again (section 4), a quality-improvement method, treated as a hypothesis for chat.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User reports autopay failed; history shows two earlier failures | Reply takes the payment, says it is a repeat, asks one cause question citing the account | 1, 2, 3 |
| 2 | First-ever autopay failure | Reply fixes it with no cause question | Don't over-correct |
| 3 | History shows two identical workarounds already | Reply asks the cause or hands off; does not apply a third workaround alone | 5 |
| 4 | User says the old card is no longer active | Bot offers choices with "Something else", changes autopay only after a yes | 4 |
| 5 | Cause is a billing-system defect the bot cannot see | Reply says so and hands off with dates and workarounds | 4, hand-off |
| 6 | After the cause fix | Reply states what happens next and does not promise it will never recur | 7 |
| 7 | Check the session log after a resolved repeat | Cause tag and fixed-or-not are saved | 6 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Repeat-contact rate for the same root cause** (primary) | Baseline first; aim to lower it | Contacts within 14 days (a starting window) of a closed contact with the same user and cause tag, divided by closed contacts with that tag. Tag by rule, then check a sample by hand. | Up 20% vs baseline |
| Repeats where the bot checked the cause before the third workaround | Over 90% (tune) | Repeat chats whose reply contains a cause question or hand-off, by rule | Below 80% |
| Cause questions in first-time contacts (counter-metric) | Under 5% (tune) | Cause questions in chats with no prior match, sampled | Over 10% |
| Same workaround applied three or more times to one user | 0 | Workaround count per user and problem type in the log | Any |
| Cause fixes that held | Track; set from baseline | Cause-fixed chats with no same-tag contact within 30 days | Falling for two weeks |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Same problem type from the same user within 14 days of a closed contact | `user.id` plus `contact.problem_type` across sessions | A new, unrelated cause, such as a second expired card |
| Bot applies the same workaround a second or third time | `bot_action.name` equal to the prior action | The user asked for exactly that action |
| Repeat chat with no cause question and no hand-off | `session.prior_matches` above 0 and no `cause_question` event | The user refused to answer questions |
| Chat closed as resolved with no `cause_tag` saved | `session.resolved` true, `cause_tag` empty | A one-time problem with no cause to record |
| User opens with "again" or "still" | User turn text | A different bot or channel is the source of the earlier problem |

**Starter rule:** when the same problem returns, check the cause before offering the same fix a third time.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: symptom-fixed-root-cause-missed
runs: pre_send
reads: [user.contact_history, session.problem_type, session.workaround_count, draft_reply.cause_question, session.stakes]
trigger: a fix is about to be offered for a problem type this user already reported
moves: [lead_with_answer, ask_one_question, offer_choices, hand_off]
choices: ["New card on autopay", "Bank account", "Keep paying by hand", "Something else"]
on_miss: rewrite
metric: Repeat-contact rate for the same root cause
counter_metric: cause questions in first-time contacts
status: proposed
```

## 8. Related patterns
- [Repeat contact loop](../../../../../by-use-case/support-services/goals/issue-resolution/failures/repeat-contact-loop.md): the closest page, for support agents whose per-ticket metrics hide a recurring defect. This page covers the chat step that page leaves open: when the bot sees the repeat, it asks one cause question in the conversation, with a rule for the third workaround and a check against over-asking.
- [Missing the obvious intent](../../embedded-copilots/failures/missing-the-obvious-intent.md): the bot misreads a plain request in the current chat. Here the request is understood and solved, and the cause is left alone.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the bot picks one reading of an ambiguous request. Here nothing is ambiguous; the question is why it keeps happening.
- FW-C02, unstructured troubleshooting (sibling row, not yet written): shotgun steps in one session. This page is about the same problem across sessions.

## 9. Common questions
### Why does the customer keep contacting support about the same problem?
Often the first fix removed the symptom and not the cause. An expired card still fails next month. Look at the user's earlier contacts to see whether the problem has come back. See [why it happens](#3-why-it-happens).

### Should a chatbot always ask why a problem happened?
No. Ask on a repeat, when an earlier contact matches. A first-time problem gets a fix. See Don't over-correct in [the fix](#5-the-fix).

### How do I measure whether the bot fixed the cause?
Tag each closed contact with a cause, then count same-tag contacts from the same user within a window you choose (section 7). A per-ticket resolution rate cannot show it, as the Enterpret guide says (section 4).

### Does the chatbot need access to past chats to do this?
Yes, or at least to a record of past problem types and actions. Without it, the bot cannot tell a repeat from a first contact, and a better model will not change that.

### What if the bot cannot fix the cause?
Say so and hand off with the dates, the workarounds applied, and the cause tag. A person can raise the defect with engineering. Do not apply the workaround a third time as if it were a fix (rule 5).

---
## Technical section

### T1. Solution architecture
```
user message -> problem classifier (type tag) -> history lookup: same user, same type, last N days
draft reply -> repeat check: prior_matches > 0 and no cause question -> rewrite or hand off
after close -> save cause_tag, workaround_count, cause_fixed
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Prior match triggers a cause question or hand-off | Pre-send check | Tests 1 and 3 |
| No cause question without a prior match | Pre-send check | Test 2; counter-metric |
| Account changes only after a yes | Tool permission | Test 4 |
| Cause tag saved at close | Post-turn hook | Test 7 |

### T3. Evals
- **Dataset:** 100 chat openings to start: repeats with an account cause, repeats with no visible cause, first-time problems, users who refuse questions; include 20 weak matches where a repeat claim is wrong.
- **Judge rubric:** is there a prior match; did the reply say it is a repeat; is there exactly one cause question citing an account fact; was the original request still served?
- **Release gate:** block a deploy if third workarounds or cause questions on first contacts exceed your target (starting points, to tune).

### T5. Trade-offs
- Matching problem types needs a tagged contact history; a poor classifier mislabels repeats.
- Cause questions add a turn. The counter-metric watches for that cost.

---
### Deep dive
- **Open question.** I found no study of chatbots and repeat contacts. The evidence is practitioner guidance and a method page, not a test of this fix.
- **References.** [Enterpret guide](https://www.enterpret.com/guides/the-6-best-tools-to-diagnose-repeat-customer-contacts-in-2026) (opened); [SQM Group, second question problem](https://www.sqmgroup.com/resources/library/blog/the-second-question-problem-why-customers-do-not-ask-what-they-really-need) (opened); [IHI, 5 Whys](https://ihi.org/fr/node/22961) (opened).
