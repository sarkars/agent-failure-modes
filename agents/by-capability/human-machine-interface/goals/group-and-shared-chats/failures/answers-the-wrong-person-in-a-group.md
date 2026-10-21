# AI Bot in a Group Chat Answers the Wrong Person: Answers the Wrong Person in a Group

<!-- SEO
title: AI Bot in a Group Chat Answers the Wrong Person: Why and Fix
description: In a shared thread the bot replies to, or as, the wrong member. Why group chats confuse assistants, and a fix: track who asked what.
search phrases:
- ai assistant group chat replies to wrong person
- chatbot in group chat answers the wrong user
- slack bot mixes up users in a thread
- ai bot in shared channel responds to everyone
- group chat ai doesn't know who is talking
- ai replies to the wrong message in a group
- teams bot answered someone else's question
-->

**Frequency**: Common

## Issue: In a shared thread the bot replies to, or as, the wrong member: it answers a question to the wrong person, mixes up who said what, or speaks for someone who did not ask.

> **One line:** In a group chat the bot treats every message as coming from one person, so it answers the wrong member or attaches one person's request to another.

| | |
|---|---|
| **Channel** | Written for **chat**: group chats and shared channels (Slack or Teams channel, group text, family or team assistant, shared support thread). Voice and meeting settings are PLANNED, not covered. |
| **Stakes** | Low for a misdirected answer. Medium to high when the reply carries one person's details, money, or a decision to someone else. |
| **Who is affected** | Everyone in a shared thread with a bot, most of all the member who asked and was skipped, and the member who got an answer to someone else's question. |
| **Frequency** | Common (our judgment). I found no count of how often bots misdirect replies in group chats, only individual reports (section 4). |
| **Pattern ID** | answers-the-wrong-person-in-a-group |
| **Family** | [Group and shared chats](../README.md) |
| **Goal** | In shared conversations the agent knows who is speaking to it, keeps private information private, and does not take over. |
| **Primary metric** | Replies addressed to the wrong person per 100 group threads. Starting target: under 1 (a starting point to tune, not from a source). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model can only use the speaker names and message order it is given. Who is asking is a state and routing problem in the product, not a language one. (Our judgment, not tested.) |
| **Also searched as** | bot answered the wrong person · ai mixes up users in group chat · bot replies to everyone in channel · ai doesn't know who asked · wrong person got the answer · shared thread bot confusion |

## 1. In plain words
In a one-to-one chat, every message is from the same person. In a group, it is not. If the bot is not told who wrote each message, or who it is supposed to answer, it guesses. It then replies to the last speaker, to the loudest one, or to nobody in particular, and the person who asked gets nothing. Fix it by recording who asked what, and answering that person by name.

## 2. What it looks like
A family assistant in a group text. Dana asks about the school pickup. Marcus, her husband, sends a message right after.

**Without the fix**
```
Dana:   @Helper what time does Ben's school let out Friday?
Marcus: Also can you add milk to the list
Helper: Added milk to the list. Anything else, Dana?
Dana:   And what about Friday pickup?
Helper: Sure, Marcus! Pickup is at 3:10.
Marcus: I didn't ask that
```

**With the fix**
```
Dana:   @Helper what time does Ben's school let out Friday?
Marcus: Also can you add milk to the list
Helper: Dana: Friday pickup is 3:10 (per the school calendar you shared).
Helper: Marcus: milk is on the shared list.
```
The fixed bot kept two open requests, each tied to the person who made it, and addressed each answer by name.

## 3. Why it happens
These are our reading of the pattern.
- **The history has no speakers.** Many bots flatten a thread to "user" and "assistant" roles. Slack's Bolt for Python AI example, as summarized in a search result, labels each message by whether it has a bot ID; that separates the bot from humans but not one human from another. (Search summary only; I did not open that page.)
- **Nothing says who the bot is answering.** Without a rule such as "answer the person who mentioned you", the bot answers the most recent message, whoever wrote it. When two requests arrive close together, it handles one and drops the other.
- **A shared thread is treated as one conversation.** One public discussion proposed treating the bot as a shared team tool that does not distinguish between users, with each thread a single continuous conversation (search summary only). That is fine for a team FAQ and wrong when members ask different things.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A user posted a feature request on June 17, 2024: in a group chat with several AI companions, a different companion often replies than the one addressed, so they reroll or delete messages. A team member replied on June 27, 2024 that tagging with "@" was started but paused. The page shows 10 votes and no release. | [Nastia feature request, "Ability to target specific companion during group chat"](https://nastia.featurebase.app/p/ability-to-target-specific-companion-during-group-chat). Opened and read. | One user's report on a companion app, and the bot there is the wrong speaker, not the wrong addressee. The request lists unrelated problems too. |
| A Discourse admin reported on October 11, 2024 that after adding an AI persona to a multi-person direct message, it replied to every message, including ones not mentioned to it. A reply said AI is supported in category channels via mentions and in 1:1 chats, but not in user-based private group chats. | [Discourse Meta thread](https://meta.discourse.org/t/how-to-remove-ai-persona-from-a-multiple-person-dm/330438). Opened and read. | One report, and a case of the bot answering when not addressed. A related request was marked completed on Oct 15, 2024; I did not check what it changed. |
| A paper on multi-party chat says models trained only on two-person dialogue appear to lack a key group skill: "being able to decide when to talk". | [Wei et al., *Multi-Party Chat: Conversational Agents in Group Settings with Humans and Models*, arXiv 2304.13835](https://arxiv.org/abs/2304.13835). Abstract opened; the full paper not read. | Research on older dialogue models, not current assistants. The abstract does not address who the bot should answer. |

Another search found a speaker-attribution benchmark (M3-SLU, arXiv 2510.19358) whose summary says models capture what was said but often fail to say who said it. I did not open it, and it is built on audio, so I do not use it.

**Public incident.** No public incident found of a bot misdirecting a reply in a group thread that caused harm. Searches run: "AI assistant group chat replies to wrong person", "multi-party conversation dialogue speaker attribution LLM benchmark", "ChatGPT group chats speaker identification", "Slack bot threads multiple users context who asked". They returned forum threads, benchmarks, and developer docs, none a dated incident I could read.

## 5. The fix
**The principle:** Record who said each message and who each reply is for, and never answer from a guess about the speaker.

**Do this**
1. **Tag every message with its sender.** Store the platform user ID and display name on each message, and pass them to the model as "Dana: (text)", not "user: (text)". Check: a transcript shows a name on every human turn.
2. **Keep an open-request list.** When a member asks the bot something, log it as {asker, request, status}. Check: two requests within a minute produce two entries with different askers.
3. **Address each reply to its asker.** Start with the asker's name, or reply in their message thread, or use the platform's reply-to. Check: each reply names the member whose request it closes.
4. **Answer only when addressed.** Reply when mentioned, replied to, or named; otherwise stay quiet. Check: unaddressed messages get no reply.
5. **When the asker is unclear, ask.** If a message could be from or for more than one member ("and Friday?"), ask who it is for before answering. Check: ambiguous follow-ups trigger one question, not a guess.
6. **Never answer as a member.** Do not speak for someone ("Marcus says so") unless that member said it in the thread. Check: no first-person claims for another member.
7. **Close the request.** Mark the request answered and keep it out of later answers to a different member. Check: Dana's answer is not repeated to Marcus.

**Reference design**
```
Group state, kept per thread
  members: {user_id: display_name}
  open_requests: [{asker_id, text, message_id, status: open | answered}]
On each incoming message
  - Add to history as "<display_name>: <text>".
  - addressed? = mention | reply to a bot message | bot name | an open request is continued by this asker
  - not addressed -> no reply (log it).
  - addressed, one clear asker -> answer; begin with the asker's name or reply in their thread.
  - addressed, asker unclear or two members could be meant -> ask who it is for.
On each reply: set the matching open_request to answered; log asker_id and addressee_id.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | One addressed member, one clear request: answer by name, in their thread or reply. |
| Ask one clarifying question | A follow-up could belong to two members: "Dana, is that Friday pickup for Ben, or did Marcus mean something else?" |
| Offer choices: 2-4 options plus "Something else", free text open | Two open requests and it is unclear which the new message continues: "Is this about 1. school pickup 2. the shopping list 3. Something else". Do not offer them when the asker is clear. |
| Hand off to a person | The group says the bot keeps mixing people up, or it is a support thread and the bot cannot tell the customer from a bystander. Do not hand off if they ask to keep going with the bot. |

**Don't over-correct.** A bot that asks "who is that for?" on every message, or that adds a name to every line, becomes noise in a busy channel. Ask only when the asker is unclear. A bot that stays silent unless @-mentioned may also miss a plain follow-up from the person it just answered; treat a reply to the bot's message as addressing it.

**Hand-off rule.** If two clarifying questions in a row fail to settle who the bot is serving, or the thread is a customer support case with several people, route to a human and pass the open-request list (who asked what).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Replay scripted group threads.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Two members ask different things within one minute | Two replies, each naming its asker (2, 3) |
| 2 | Member B writes between member A's question and the bot's answer | The answer goes to A, not B (3) |
| 3 | A message not addressed to the bot | No reply (4) |
| 4 | "And Friday?" after two members have spoken | One question about who it is for (5) |
| 5 | Member A asks; later member B asks the same words | Each answered separately; no cross-talk (2, 7) |
| 6 | Bot is asked to relay "what did Marcus say?" and he said nothing | It says he has not said anything (6) |
| 7 | Transcript sent to the model | Every human turn carries a name (1) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Replies addressed to the wrong person per 100 group threads** (primary) | Under 1 | Sample threads; a reviewer compares each reply's addressee with the asker of the open request | Over 3 |
| Replies with no addressee named or threaded | Under 5% | Log `addressee_id` on each reply; count nulls | Over 15% |
| Unaddressed messages the bot answered | Under 2% | Messages with no mention, reply-to, or bot name that got a reply | Over 5% |
| Open requests never answered | Under 3% | Open requests older than 10 minutes | Over 8% |
| Clarifying questions per 100 bot replies (counter) | Track; set from baseline | Count clarifying questions | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Proposed until checked against human-labeled group threads. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply's `addressee_id` differs from the `asker_id` of the closest open request | Reply event vs. open-request log | The asker handed the question to another member on purpose |
| A member repeats their question after the bot replied to someone else | Same member, same intent, within 3 turns of a bot reply | A deliberate rephrase |
| A member writes "I didn't ask that" or "that was for me" after a bot reply | Phrase match in the next human turn | A joke between members |
| Two open requests from different askers, one answered with the other's name | Open-request log, reply text | A shared question the bot answered for both |
| History sent to the model has no names | Model input check | A single-user thread |

**Starter rule:** the bot answers each addressed member by name, from a list of who asked what, and asks when the asker is unclear.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: answers-the-wrong-person-in-a-group
runs: pre_send
reads: [thread.members, thread.open_requests, message.sender_id, message.mentions, reply.addressee_id]
trigger: a reply is about to be sent in a thread with more than one human member
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["School pickup", "The shopping list", "Something else"]
on_miss: rewrite
metric: replies addressed to the wrong person per 100 group threads
counter_metric: clarifying questions per 100 bot replies
status: proposed
```

## 8. Related patterns
- [Reference resolution failures](../../dialogue-management/failures/reference-resolution-failures.md): the closest page. It covers a bot misreading "it" or "that one" in a single-user chat. This page is about which person a message and a reply belong to, which a single-user chat never raises.
- [Third-party data shared by users](../../privacy-and-governance/failures/third-party-data-shared-by-users.md): what the bot does with other people's details. This page covers misdirected replies, whether or not private data is involved (matched by name; I did not re-read that page).
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the habit behind rule 5, applied to the speaker (matched by name; not re-read).
- Related roadmap rows in this family without pages yet: private information leaks into the group, the bot takes over the conversation.

## 9. Common questions
### Why does my AI bot answer the wrong person in a group chat?
Usually it does not know who sent each message, or who it is meant to answer, so it replies to the latest message. Tag every message with its sender and keep a list of who asked what (rules 1 and 2).

### Why does the bot reply to every message in the channel?
It has no rule for when it is addressed. One Discourse report describes that in a multi-person DM (section 4). Reply only when mentioned, replied to, or named (rule 4).

### Should the bot reply in a thread or in the channel?
Reply where the asker will see it as theirs: in their thread or as a reply to their message, with their name. A reply in the open channel with no name can read as for anyone (rule 3).

### Does a bigger model fix this?
Not by itself. A larger model still sees only the names and order it is given. I tested no model on this (our judgment).

### What should the bot do when two people ask at once?
Answer both, each by name, and keep the two requests separate (rules 2, 3 and 7). If a short follow-up could belong to either, ask which (rule 5).
