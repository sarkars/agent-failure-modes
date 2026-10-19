# Chatbot Tells You to Do It Yourself: Deferring Work to the User

<!-- SEO
title: Chatbot Tells You to Do It Yourself: Fix Deferring Work to the User
description: Why an assistant says "you can check your account" or "you may want to look that up" when it has a tool that could do it, what the evidence says, and rules for doing the work or saying why not.
search phrases:
- chatbot tells me to check the website myself
- chatbot won't look up my order
- ai assistant tells me to do it myself
- chatbot gives instructions instead of doing the task
- chatgpt refuses to do the task and tells me how
- ai laziness incomplete answers
- chatbot you can check your account
-->

**Frequency**: Common

## Issue: The assistant has a tool or the data to do something, and instead writes "you can check…", "you may want to look up…", or a how-to, so the user ends up doing the work.

> **One line:** The user asked the bot to do it, and the bot explained how they could.

| | |
|---|---|
| **Channel** | Written for **chat** and assistants with tools (order lookup, search, code, calendar). |
| **Stakes** | Low to medium. It wastes time and sends people to other channels; on urgent matters it can cost money. |
| **Who is affected** | Everyone, most of all people who came to the bot because they could not find the answer themselves |
| **Frequency** | Common in practice. I found no study that counts it for assistants with tools. The nearest evidence is a vendor-acknowledged "laziness" episode in 2023 to 2024. |
| **Pattern ID** | deferring-work-to-the-user |
| **Family** | [Effort and memory](../README.md) |
| **Goal** | The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't. |
| **Primary metric** | Deferral rate: replies handing a task to the user that the agent has a tool for. Target: near 0 (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/deferring-work-to-the-user.md); not yet run) |
| **Will a better model fix this?** | Partly. A vendor said in January 2024 that an update was intended to reduce "laziness", but a stronger model still needs the tool, permission, and a rule for when to ask. (Our judgment, not tested.) |
| **Also searched as** | bot tells me to Google it · chatbot punts to the website · lazy AI · AI doesn't do the task · AI explains instead of doing |

## 1. In plain words
A user asks for something the assistant can do: look up an order, rewrite a file, find a time on a calendar. The reply is "You can find this in your account under Orders" or "Here is how you could refactor it". The work goes back to the user, and the bot has not said why.

## 2. What it looks like

**Without the fix**
```
User: Where's my order #48213?
Bot:  You can check the status of your order by signing in to your account and opening Order History.
User: I'm asking you to check it.
Bot:  I'd be happy to help! You can track your order using the tracking link in your confirmation email.
```

**With the fix**
```
User: Where's my order #48213?
Bot:  It shipped Tuesday and is due Friday: UPS tracking 1Z... (link). It's in the Memphis hub now.
```
When the bot truly cannot look it up (no access, or the user is not verified), it says so and what it needs: "I can't see order details until you verify your email. I've sent a code to j***@example.com."

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom.
- **The tool isn't wired or isn't permitted.** The assistant has no order lookup, or it is gated behind a login step the flow never starts.
- **A deflection default.** The bot is tuned to reduce contacts, so a pointer to a help page is a safe reply.
- **A model habit, with no published cause.** In 2023 and 2024, OpenAI acknowledged reports of incomplete answers; the source I opened gives no root cause, and I did not find one for chat assistants in general.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| CIO Dive reported that users said GPT-4 Turbo refused tasks or produced half-completed responses, that OpenAI acknowledged the complaints in December 2023, and that on January 25, 2024 OpenAI released an updated preview model intended to reduce cases of "laziness where the model doesn't complete a task". | [CIO Dive, Jan. 25, 2024](https://www.ciodive.com/news/openai-laziness-gpt4-turbo-model-updates/705664/). Opened and read. | A trade-press report about one vendor's model. It describes refusals and incomplete answers, not handing steps to the user. The source gives no root cause and no counts. |
| One developer reported on December 7, 2023 that GPT-4 Turbo declined a code refactoring request, citing a platform limit, and returned examples of what a refactor might look like instead. The thread also quotes an OpenAI staff post asking for examples of "over-refusal". | [OpenAI Developer Community thread](https://community.openai.com/t/gpt-4-turbo-refusing-to-follow-instructions/548716). Opened and read. | A single user report, not confirmed by OpenAI in the thread. |

I found no study that measures how often assistants with tools hand tasks back to users, and none that tests a fix. My searches for agents offloading work to users returned papers on the reverse (users delegating to agents, agents over-delegating to sub-agents), which I do not use. I read search summaries that cite Gartner customer-effort figures, but I could not open the original or the vendor page that quoted them, so I do not use those numbers.

**Public incident.** A related, dated case: [OpenAI acknowledges reports of GPT-4 Turbo refusing tasks](../../../incidents/openai-gpt-4-turbo-laziness-reports.md). It is adjacent, not a direct match (see the incident page).

## 5. The fix

**The principle:** Do what you can do, ask only for what only the user can supply, and when you will not or cannot do something, say so and say why.

**Do this**
1. **Use the tool.** If the request maps to a tool the assistant has, call it before replying. Do not describe how the user could do it.
2. **Answer from the result.** Put the result in the first sentence (see [answer buried](../../response-structure/failures/answer-buried.md)).
3. **Ask only for what only the user can supply** (a code sent to their email, a choice, a missing number). Name the one thing you need.
4. **If you cannot do it, say so plainly and say why** ("I can't see order details until you verify your email"), then offer the next step.
5. **If a how-to is the right help, offer it as an addition, not instead.** "Here is the result. To track it yourself later, use...".
6. **Never refuse on a limit you have not checked.** Do not cite a platform or length limit unless the limit applies.
7. **Hand off when no route works,** with a summary ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Reference design: do, ask, or say why**
| Situation | Reply |
|---|---|
| Tool exists and user is permitted | Do it and report the result |
| Tool exists, user needs verification | Start verification; name the one thing needed |
| No tool, but the answer is known | Give the answer |
| No tool and no answer | Say so, give the best next route, offer a person |

```
If a tool can do what the user asked, call it and report the result in the first sentence. Do not tell the user how to do it themselves instead.
Ask the user only for information only they can supply, and name it.
If you cannot do something, say so and say why. Do not cite limits you have not checked.
Offer a how-to only in addition to the result.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request maps to a tool the assistant has and the user is permitted: call it and put the result in the first sentence. Do not use it when the tool would be irreversible and the user has not confirmed. |
| Ask one clarifying question | Only the user can supply one thing (a code sent to their email, a missing number): name that one thing. Do not ask for anything the assistant can look up. |
| Admit uncertainty and show how to check | The assistant cannot do it (no tool, or verification needed): say so, say why in one clause, and give the next step. |
| Hand off to a person | No tool route works and a person has the tool. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not take actions the user did not ask for, and do not run costly or irreversible tools without confirmation. When a user clearly wants to learn how, teach them; do not do it silently. Do not call tools on unverified users just to avoid deferring.

**Hand-off rule.** If a task needs a tool the assistant lacks and a person has it, hand off with a summary of what the user asked and what was tried ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/deferring-work-to-the-user.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Order status with a lookup tool | The bot looks it up and reports it |
| 2 | Same, user not verified | The bot says why it cannot and starts verification |
| 3 | Tool unavailable | The bot says so and offers a person |
| 4 | "How do I do it?" | A how-to is given, not an action |
| 5 | A cited limit | The limit actually applies |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Deferral rate** (primary) | Near 0 | A labeled sample of replies, joined to the tools the assistant had for that request | Over 3% |
| "Do it yourself" replies with no stated reason | 0 | Pattern match plus sample | Any |
| Same-request repeat ("I asked you to") within 2 turns | Track; set from baseline | Next-turn classifier | Rising two weeks in a row |
| Unrequested tool calls (counter-metric) | 0 | Log of tool calls without a matching request | Any |
| Irreversible actions without confirmation (counter-metric) | 0 | Log check | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply points the user to a page, account, or how-to, and the turn has no tool call, although the request maps to a tool the assistant has | Intent-to-tool map joined to the turn's tool-call log and reply text | The user asked "how do I" and wanted a how-to |
| "Do it yourself" reply with no stated reason | Pattern match on the reply text, plus no reason clause | The reply says what is blocking it (for example, verification needed) |
| User repeats the request ("I asked you to") within 2 turns | Same intent in the next user turn | A rephrase that adds new detail |
| Reply cites a platform or length limit with no limit check logged | Reply text plus the limit-check event | The limit actually applies |

**Starter rule:** if a tool can do what the user asked, call it and report the result in the first sentence, and do not tell the user how to do it themselves instead.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: deferring-work-to-the-user
runs: pre_send
reads: [request.intent, tool_map, permission.status, turn.tool_calls, reply.text]
trigger: a reply is about to be sent that hands a task to the user while a permitted tool maps to the request
moves: [lead_with_answer, ask_clarifying_question, admit_uncertainty, hand_off]
choices: none
on_miss: rewrite
metric: deferral rate, replies handing a task to the user that the agent has a tool for
counter_metric: unrequested tool calls
status: proposed
```

## 8. Related patterns
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): the reverse favor, asking for what the product already has.
- [Missing the obvious intent](../../embedded-copilots/failures/missing-the-obvious-intent.md): misreading a plain request.
- [Forces a fresh login](../../embedded-copilots/failures/forces-a-fresh-login.md): when verification, not deferral, is the block.
- [Answer buried](../../response-structure/failures/answer-buried.md): put the result first.
- [Conversation depth mismatch](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-depth-mismatch.md): the wrong amount of detail.

## 9. Common questions
### Why does a chatbot tell me to check my account instead of checking it?
Often it has no lookup tool, or the lookup needs verification the flow never starts. The fix is to wire the tool and start verification, or say what is blocking it.

### Is it ever right for a bot to give instructions instead of doing the task?
Yes, when the user asks how, or when an action is irreversible and the user has not confirmed. Say so.

### What should a bot say when it cannot do something?
Say it cannot, say why in one clause, and give the next step.

### Is this the same as AI "laziness"?
It overlaps. OpenAI used that word in 2024 for incomplete answers; I did not find a source that defines it more exactly. See [the incident page](../../../incidents/openai-gpt-4-turbo-laziness-reports.md).

---
## Technical section

### T1. Solution architecture
```
request -> intent -> tool map (which tool can do this?) -> permission check
        -> call tool | start verification | explain the block -> reply with result
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| A request with a mapped, permitted tool must produce a tool call | Orchestrator | Log: request intent vs. tool calls |
| A refusal states a reason | Reply policy | Labeled sample |
| Irreversible tools require confirmation | Tool layer | Test 6 |

### T3. Evals
- **Dataset:** 150 requests each mapped to a tool the assistant has, plus 50 where it has none.
- **Judge rubric:** did the assistant act, ask only for what it needs, or say why it could not?
- **Metrics and starting thresholds:** deferral rate under 3%; refusals with a stated reason 100%. Starting points to tune.
- **Release gate:** block a deploy if deferrals rise on the mapped-request set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Deferral rate | Over 3% | Over 8% | Check tool wiring and recent prompt changes |

### T5. Trade-offs
- More tool calls cost money and risk wrong actions; confirm irreversible ones.

---
### Deep dive
- **Open question.** I found no study of deferral in assistants with tools. The incident evidence is one vendor's acknowledged episode and one user report.
- **References.** [CIO Dive, 2024](https://www.ciodive.com/news/openai-laziness-gpt4-turbo-model-updates/705664/) (opened); [OpenAI Developer Community thread, 2023](https://community.openai.com/t/gpt-4-turbo-refusing-to-follow-instructions/548716) (opened).
