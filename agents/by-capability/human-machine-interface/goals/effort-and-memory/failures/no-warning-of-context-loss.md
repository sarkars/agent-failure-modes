# Chatbot Forgets Earlier Messages Without Telling You: No Warning of Context Loss

<!-- SEO
title: Chatbot Forgot What I Told It: Warn Users Before Context Is Lost
description: Why an assistant silently drops earlier messages or saved memories, what the research and user reports show, and how to tell the user what was kept, what was lost, and how to carry on.
search phrases:
- chatbot forgot what I told it earlier
- chatgpt forgets earlier messages in long chat
- this conversation has reached its limit start a new chat
- chatgpt memory full no warning
- how to warn users when chat context is full
- chatbot says it remembered but didn't
- long chat context limit notice design
-->

**Frequency**: Common

## Issue: When a conversation outgrows what the assistant can hold, or saved memory is full, early content is dropped, summarized, or never stored, and the assistant does not tell the user.

> **One line:** The bot quietly stops knowing what you said, and keeps talking as if it still does.

| | |
|---|---|
| **Channel** | Written for **chat** and assistants with memory or long sessions. |
| **Stakes** | Low to high. Forgotten preferences are an annoyance; a dropped allergy, deadline, or constraint can lead to a wrong answer. |
| **Who is affected** | People in long sessions, and people who rely on saved memory to carry details between chats |
| **Frequency** | Common in long sessions. I found no study that counts how often products fail to warn. The evidence below is research on long-context weakness, user reports, and one status-page incident. |
| **Pattern ID** | no-warning-of-context-loss |
| **Family** | [Effort and memory](../README.md) |
| **Goal** | The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't. |
| **Primary metric** | Context-loss events with a user-visible notice. Target: 100% (tune after you can detect the events). |
| **Maturity** | Tests written (see [the test file](../../../tests/no-warning-of-context-loss.md); not yet run) |
| **Will a better model fix this?** | No. Larger windows push the limit out but do not remove it, and a notice is a product decision. (Our judgment, not tested.) |
| **Also searched as** | AI forgot my instructions · conversation limit reached · memory full · chat history dropped · compaction notice |

## 1. In plain words
Every assistant has a limit on what it can hold at once, and many have a separate limit on saved memories. When the limit is hit, something goes. The failure is not the limit; it is that the user is not told, so they keep relying on details the assistant no longer has.

## 2. What it looks like

**Without the fix**
```
(40 messages in; the user stated "I'm allergic to shellfish" in message 3, which has been dropped)
User: Plan a dinner menu for six.
Bot:  Here's a menu: shrimp cocktail, lobster bisque, ...
```

**With the fix**
```
Bot:  Heads up: this chat is getting long, and I may be losing details from the start. I still have: six guests,
      budget $150, and your allergy note (shellfish). Want me to save a summary and carry on in a fresh chat?
```
The fixed assistant warns before the drop, says what it kept, and offers a way to continue. After a drop, it says what was lost and asks the user to restate it.

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom.
- **Hard limits.** The window fills, and the system drops or compacts the oldest content without a user-facing step.
- **The model cannot see what it lost.** The model only sees what is in its context, so it cannot report what was cut unless the product tells it.
- **No product rule.** Nobody decided that a notice is part of the behavior, and the interface has no place for one.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In tests on multi-document question answering and key-value retrieval, performance was often highest when relevant information was at the beginning or end of the input and degraded significantly when it was in the middle, even for models built for long contexts. | [Liu et al., *Lost in the Middle*, TACL 2023](https://arxiv.org/abs/2307.03172). Opened; abstract read. | A 2023 study of older models on retrieval tasks. It shows that long context is used unevenly, not that products fail to warn. |
| Across six generation tasks, top models scored lower in multi-turn than single-turn conversations, with an average drop of 39%, mostly from unreliability; the authors say models "get lost and do not recover" after a wrong turn. | [Laban et al., *LLMs Get Lost in Multi-Turn Conversation*, arXiv 2505.06120](https://arxiv.org/abs/2505.06120). Opened; abstract read. | Simulated conversations; about premature assumptions, not about context limits. Included as background on long-conversation weakness. |
| A ChatGPT Plus user reported on February 3, 2025 that when memory was full there was no warning, yet ChatGPT still said it had remembered the new information, which was not stored. | [OpenAI Developer Community thread](https://community.openai.com/t/chatgpt-plus-plan-memory-issue-no-warning-when-memory-is-full-leading-to-lost-entries/1111613). Opened and read. | One user's report; no OpenAI reply in the text I read. |
| A Copilot user reported in May 2024 that Copilot said "this conversation has reached its limit" and, asked for the limit, would not say what it was. | [Microsoft Community Hub thread](https://techcommunity.microsoft.com/discussions/microsoft-copilot/sorry-this-conversation-has-reached-its-limit-lets-start-a-new-chat-/4137520). Opened; first post read. | One user's account. A notice appeared, but only after the limit was hit. |

I found no published study of how users react when a context-loss notice is shown or withheld, and none that tests a notice design. Material from the roadmap on context drift is not used where I did not open it.

**Public incident.** A related, dated case: [ChatGPT users report missing memories; OpenAI's status page logs a memory incident (Nov. 6 to 7, 2025)](../../../incidents/chatgpt-memory-missing-memories-november-2025.md). It is adjacent, not a direct match: it records a loss and a recovery, and the page does not say what users were told in the product.

## 5. The fix

**The principle:** Never lose the user's details silently. Warn before the limit, say what was kept, and say what was lost afterward.

**Do this**
1. **Warn before the limit.** When the session nears its limit, say so once ("this chat is getting long") and offer a summary and a fresh start. Pick the trigger from your own limit, not a fixed number.
2. **Say what was kept.** List the key facts you still hold (names, constraints, decisions) in the notice.
3. **Say what was lost, after a drop.** If content was dropped or compacted, say so and ask the user to restate the details that matter.
4. **Never claim to remember what was not stored.** A "saved" message appears only after the write succeeds ([the memory-full report above](https://community.openai.com/t/chatgpt-plus-plan-memory-issue-no-warning-when-memory-is-full-leading-to-lost-entries/1111613) describes the opposite).
5. **Pin what must survive.** Keep safety-relevant details (allergies, deadlines, consent) in a pinned block that is not compacted away.
6. **Offer a carry-over.** One step to copy a summary into a new chat, or to keep it as a saved note.
7. **Show a hard limit before it hits.** If there is a turn or size limit, state it, and do not end the chat without a way to continue.

**Reference design: context notice**
| State | What the user sees |
|---|---|
| Nearing the limit | "This chat is getting long. I still have: [kept facts]. Save a summary and continue in a new chat?" |
| After a drop | "Some earlier messages were dropped. I no longer have: [lost areas]. Can you restate them?" |
| Memory full | "Memory is full, so I did not save that. Delete an entry or keep it in this chat." |
| Hard limit reached | "This chat has reached its limit. Here is a summary to paste into a new one." |

```
If the conversation is near its limit, tell the user once, list the key facts you still hold, and offer a summary and a fresh start.
If earlier content has been dropped or compacted, say so and ask the user to restate what matters.
Never say you saved or remembered something unless the save succeeded. If memory is full, say so.
Keep pinned facts (allergies, deadlines, consent) out of compaction.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | After a drop, compaction, or failed memory write: say what was lost or not saved, list what is still held, and ask the user to restate what matters. Never say "saved" unless the write succeeded. |
| Offer choices: 2-4 options plus "Something else", free text open | At the near-limit notice or a memory-full notice: "Save a summary and continue in a new chat", "Delete a memory entry", "Keep it in this chat", "Something else". Do not offer them in short chats, or on every turn. |
| Hand off to a person | A dropped detail could cause harm (safety, legal, money) and the user cannot restate it. Do not hand off if the user restated it. |

**Don't over-correct.** Do not show a warning on every turn or in short chats. Do not alarm users with a long list of what "might" be missing. Do not compact pinned facts to save space.

**Hand-off rule.** If a dropped detail could cause harm (a safety, legal, or money detail) and the user cannot restate it, say so and route to a person ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/no-warning-of-context-loss.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A long chat nearing its limit | A notice with kept facts and an offer |
| 2 | After a forced drop | The assistant says content was dropped and asks to restate |
| 3 | Memory full | "Not saved", not "saved" |
| 4 | A pinned allergy | It survives compaction |
| 5 | A short chat | No notice |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Context-loss events with a user-visible notice** (primary) | 100% | Log every drop, compaction, and failed memory write; join to notices shown | Below 95% |
| False "saved" confirmations | 0 | Compare "saved" messages to successful writes | Any |
| Pinned-fact loss after compaction | 0 | Replay tests with pinned facts | Any |
| Restate rate after a drop notice | Track; set from baseline | Next-turn classifier | Unexplained rise |
| Notices in short chats (counter-metric) | Under 1% | Notices in sessions under the threshold | Over 3% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A drop or compaction event has no notice event | Context-manager event with no matching notice shown to the user | A notice already shown once when the threshold was crossed |
| A "saved" message has no successful memory write | Confirmation message joined to the write log | A write that succeeded slightly later and was logged out of order |
| A pinned fact is missing from context after compaction | Pinned-fact list compared to the post-compaction context | The user withdrew or changed the fact |
| The user restates a fact right after a drop | Same fact in the next user turn after a drop event | The user is deliberately updating the fact |
| A notice appears in a session under the threshold (counter-metric) | Notice event in a short session | A failed memory write, which warrants a notice at any length |

**Starter rule:** if the conversation is near its limit or content was dropped, tell the user once, list the key facts still held, and never say something was saved unless the save succeeded.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-warning-of-context-loss
runs: pre_send
reads: [context_event.type, context_event.dropped_areas, session.pinned_facts, memory_write.status]
trigger: a context drop, compaction, near-limit state, or memory write result is about to go unannounced
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Save a summary and continue in a new chat", "Delete a memory entry", "Keep it in this chat", "Something else"]
on_miss: rewrite
metric: context-loss events with a user-visible notice
counter_metric: notices in short chats
status: proposed
```

## 8. Related patterns
- [Context window overflow with silent truncation](../../../../../cross-cutting/operations/goals/memory-safety/failures/context-window-overflow-silent-truncation.md): the loss itself. This page covers telling the user.
- [Context window awareness failure](../../../../../cross-cutting/operations/goals/memory-management/failures/context-window-awareness-failure.md): the agent has no sense of its own window.
- [Compaction information loss](../../../../../cross-cutting/operations/goals/memory-management/failures/compaction-information-loss.md): what compaction drops.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): asking again for what the product already has.
- [Deferring work to the user](deferring-work-to-the-user.md): another way the user ends up carrying the load.

## 9. Common questions
### Why does a chatbot forget what I said earlier?
Usually because the conversation grew past what it can hold, and older content was dropped or summarized. The assistant often does not know it happened.

### Should a chatbot tell me when it forgets something?
Yes. It should warn before the limit and say what it kept, and say what was lost after a drop.

### What should I do when a chat gets very long?
Ask for a summary of the key facts and start a new chat from it, then check that the summary kept what matters.

### Why did ChatGPT say it saved something it didn't?
One user reported this when memory was full. I found no OpenAI explanation in the thread I read.

---
## Technical section

### T1. Solution architecture
```
turn -> token and memory budget check -> near limit? -> notice (kept facts, offer)
     -> compaction -> pinned-fact preserve -> post-compaction notice (what was dropped)
     -> memory write -> success? -> "saved" | "not saved"
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| A "saved" message only after a successful write | Memory layer | Log: confirmations vs writes |
| Every drop or compaction emits an event and a notice | Context manager | Event and notice join |
| Pinned facts are excluded from compaction | Compaction step | Replay test |

### T3. Evals
- **Dataset:** 100 long conversations seeded with 5 key facts each (including a safety fact), run past the limit.
- **Judge rubric:** did the assistant warn, name what it kept, and ask to restate what was lost, and did the safety fact survive?
- **Metrics and starting thresholds:** notice rate 100%; pinned-fact survival 100%. Starting points to tune.
- **Release gate:** block a deploy if a drop or failed memory write occurs without a notice.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Drop events without notice | Any | Over 1% of drops | Check the context manager and notice rules |

### T5. Trade-offs
- Notices cost a little attention; show them once per threshold crossing.
- A visible limit may push users to shorter chats, which is usually better.

---
### Deep dive
- **Open question.** I found no study of notice designs for context loss. The evidence is research on long-context weakness, user reports, and a status-page incident.
- **References.** [Liu et al., TACL 2023](https://arxiv.org/abs/2307.03172) (abstract opened); [Laban et al., 2025](https://arxiv.org/abs/2505.06120) (abstract opened); [OpenAI Developer Community thread, Feb. 2025](https://community.openai.com/t/chatgpt-plus-plan-memory-issue-no-warning-when-memory-is-full-leading-to-lost-entries/1111613) (opened); [Microsoft Community Hub thread, May 2024](https://techcommunity.microsoft.com/discussions/microsoft-copilot/sorry-this-conversation-has-reached-its-limit-lets-start-a-new-chat-/4137520) (opened); [OpenAI status page, Nov. 2025](https://status.openai.com/incidents/01K9D7DASB76TK1DEGPMG6ZAM4) (opened).
