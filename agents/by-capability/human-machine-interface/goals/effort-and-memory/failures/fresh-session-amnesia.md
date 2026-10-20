# Chatbot Forgets Previous Conversation in a New Chat: Fresh-Session Amnesia

<!-- SEO
title: Chatbot Forgets Previous Conversation: Fresh-Session Amnesia
description: Why a new chat starts with nothing from your last one, what vendor docs and user reports show, and how to offer a continuity summary the user approves.
search phrases:
- chatbot forgets previous conversation
- chatgpt doesn't remember between sessions
- new chat doesn't remember my last chat
- claude resume session lost context
- how to carry context into a new chat
- ai assistant start over every time
- chatbot memory across sessions design
-->

**Frequency**: Very Common

## Issue: A new chat or session starts with nothing from the last one and offers no handover, so the user has to explain the whole situation again.

> **One line:** You come back to finish yesterday's job and the assistant greets you like a stranger.

| | |
|---|---|
| **Channel** | Written for **chat** and assistants with separate sessions. Voice and web are PLANNED, not written. |
| **Stakes** | Low to high. Re-explaining a recipe preference is a nuisance; re-explaining a billing dispute, a half-built project, or a medical history costs time and invites mistakes. |
| **Who is affected** | Anyone who returns to unfinished work in a new chat, a new day, or after a session ends |
| **Frequency** | Very common. Every chat product with separate sessions has the gap; I found no count of how often users hit it. |
| **Pattern ID** | fresh-session-amnesia |
| **Family** | [Effort, completeness, and memory](../README.md) |
| **Goal** | The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't. |
| **Primary metric** | Resume success (a returning user continues without re-explaining) and user re-explanation rate. Starting targets to tune on your own data. |
| **Maturity** | Researched (no tests written; see Section 6) |
| **Will a better model fix this?** | No. A model cannot recall a session its product never gave it. (Our judgment, not tested.) |
| **Also searched as** | chatgpt forgot everything · new chat starts over · resume session blank · claude doesn't remember last chat · re-explain context every time |

## 1. In plain words
Each new chat is a blank page. If the product does not carry anything forward, the user must retype the goal, the decisions already made, and what is left to do. The fix is not to remember everything silently: it is to offer a short continuity summary that the user can read, edit, approve, and delete.

## 2. What it looks like

**Without the fix**
```
(Monday) User: We're picking a plan for the 12-person office. Budget $400/month, no annual contracts.
         ...(25 turns narrow it to Plan B vs Plan C)
(Tuesday, new chat)
User: Let's pick up the plan decision.
Bot:  Happy to help! Which plans are you comparing, and what's your budget?
User: I told you all of this yesterday.
```

**With the fix**
```
User: Let's pick up the plan decision.
Bot:  Last time you were choosing a plan for 12 people, budget $400/month, no annual contracts,
      down to Plan B vs Plan C. Want me to continue from there?
      [Yes, continue] [Edit this summary] [Start fresh] [Something else]
User: Yes, continue.
Bot:  Plan B is $340/month monthly-billed; Plan C is $390 with more storage. Which matters more?
```
The fixed bot shows what it will carry forward and lets the user approve, change, or refuse it before it uses it.

## 3. Why it happens
These are our reading of the pattern.
- **Sessions are isolated by design.** Many products keep each chat separate, or load saved notes only, so a new chat has no transcript to read.
- **Memory stores notes, not the thread.** Saved facts such as "prefers short answers" do not hold "we narrowed it to B or C and still need the contract term."
- **No handover step.** Nothing in the product turns the end of a session into a summary, and nothing offers it at the start of the next.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Claude's help center says Claude saves memory as topics while you chat, project memory stays inside its project, and incognito chats are not saved to memory or chat history. Memory is on by default for Free, Pro, and Max; Team and Enterprise members must turn it on. | [Claude Help Center, *Understanding Claude's memory*](https://support.claude.com/en/articles/11817273-understanding-claude-s-memory). Opened and read. | Vendor documentation of how memory works. It does not measure how often users still have to re-explain. |
| The same page describes user controls: view, edit, and delete each topic under Settings > Memory; pause memory; reset it, which permanently deletes all memories; and turn off past-chat search. | Same page. Opened and read. | These are the controls a continuity summary should match. |
| A user on OpenAI's developer forum wrote on February 3, 2025 that ChatGPT kept context inside one chat but new chats started with no memory of earlier ones, that it began that day without warning, and asked whether it was a bug or a permanent change. | [OpenAI Developer Community thread](https://community.openai.com/t/chatgpt-suddenly-forgot-everything-anyone-else-experiencing-this/1111406). Opened and read. | One user's report. The page I opened shows no OpenAI staff reply. |
| A Claude Code issue filed April 4, 2026 reported that `claude --continue` and `claude --resume` started a fresh session, so files read, decisions made, and in-progress work were lost. It was closed as a duplicate of a reported regression and later locked. | [anthropics/claude-code issue 43696](https://github.com/anthropics/claude-code/issues/43696). Opened and read. | A bug report on one tool, one OS, and an unnamed version. It shows the user-visible effect of a failed resume, not how common it is. |

I found no controlled study of how often users re-explain context in a new chat, or of whether continuity summaries help. I tried the OpenAI help center memory FAQ and the OpenAI memory announcement, but both returned HTTP 403, so I do not cite them. Details of ChatGPT's memory layers came only from search summaries and third-party blogs; I leave them out.

**Public incident.** [ChatGPT users reported missing memories in November 2025](../../../incidents/chatgpt-memory-missing-memories-november-2025.md). That is stored memory disappearing, which is a different failure from a session that never had a handover (see Section 8).

## 5. The fix

**The principle:** When a user returns to unfinished work, offer a short summary of where things stood, let them approve, edit, or refuse it, and never load it without their say-so.

**Do this**
1. **Offer, don't assume.** At the start of a new session, if there is an unfinished task, show a 2-5 line summary and ask whether to continue from it.
2. **Make it specific.** Goal, decisions made, constraints given, and what is left. Not "we talked about plans."
3. **Let the user edit or refuse.** Always offer "Edit this summary" and "Start fresh". Starting fresh must work in one click.
4. **Get approval before the summary becomes memory.** A summary shown for this session is not the same as one saved for later. Ask before saving it.
5. **Make it deletable.** The user can view the summary, edit it, and delete it, in the same place as other memory controls. Deleting it means the next session starts blank.
6. **Say where it came from.** "From your chat on Monday." Never present a summary as if the bot simply remembered.
7. **Offer the summary at the end of a long session too**, so the user can save it before leaving.
8. **If nothing is available, say so.** "I can't see your earlier chat. Paste a few lines or tell me the goal." Do not pretend to remember.

**Reference design: continuity summary**
| Part | Content |
|---|---|
| Source | "From your chat on [day]." |
| Goal | One sentence of what the user was trying to do |
| Decided | Choices already made and constraints the user gave |
| Open | What is left |
| Controls | Continue, Edit, Start fresh, Delete this summary |

```
At the start of a new session, if an approved or offered continuity summary exists, show it with its source and ask whether to continue from it.
Never load a summary the user has not seen. Offer edit, start fresh, and delete. Do not ask again for anything the approved summary already contains.
If no summary exists, say you cannot see earlier chats and ask for the goal in one line.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A new session opens on unfinished work: "Yes, continue", "Edit this summary", "Start fresh", "Something else". Do not offer them when the user's first message is clearly a new topic. |
| Admit uncertainty and show how to check | No earlier chat is visible, or the summary may be stale: say what you can and cannot see, and ask the user to confirm the key facts. |
| Ask one clarifying question | No summary exists and the first request depends on context: ask for the goal in one line, not a form. |

**Don't over-correct.** Do not load every past chat into every new one, and do not announce "I remember everything." Old context can be wrong, private, or irrelevant to a new topic. Do not nag: offer the summary once per session. Do not save summaries the user never approved.

**Hand-off rule.** If the user is mid-dispute or mid-transaction and no context can be recovered, pass the summary they approved to a person ([handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md) covers getting that summary right).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests: **Not yet run**, and no full test file has been written.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Return the next day to an unfinished task | A specific summary is offered with its source, before the bot asks anything |
| 2 | The user picks "Start fresh" | The summary is not used and not re-offered in that session |
| 3 | The user edits the summary | The edited version, not the original, is used |
| 4 | The user deletes the summary | The next session starts blank and says nothing about it |
| 5 | The user opens with a new, unrelated topic | No summary is pushed |
| 6 | No earlier chat is available | The bot says so and asks for the goal in one line |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Resume success** (primary): returning users who continue the task without re-explaining | Track; set from baseline | Sampled review of returning sessions, or the share where the user accepts the summary and the task advances | Falling |
| **User re-explanation rate** (primary pair): returning sessions where the user restates goals already given | Track; set from baseline | Detect restated goal or constraints in the first 3 user turns | Rising two weeks in a row |
| Summary offered on unfinished work | 100% (tune) | Sessions that open on an unfinished task with an offer event | Below 95% |
| Summary edits or "Start fresh" clicks | Track | Count of each choice | Start-fresh over half of offers |
| Summaries used without user approval (counter-metric) | 0 | Loads with no approval event | Any |
| Summaries not deletable on request (counter-metric) | 0 | Delete test in each release | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| First user turn refers to earlier work ("last time", "yesterday", "as before") and the bot asks for the basics | Turn text plus the bot's next-turn question | The user wants a deliberate fresh start |
| User says "I already told you" in the first 5 turns of a session | Turn text in a new-session event | A repeat within one session (see re-asks) |
| Same goal or constraints appear in the opening turns of two sessions by one user | Per-user session history | Habit questions that are really new each time |
| User abandons within 3 turns of a new session that began on unfinished work | Session end event | The task was already finished |

**Starter rule:** at the start of a new session on unfinished work, offer a short continuity summary the user can approve, edit, or refuse.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: fresh-session-amnesia
runs: conversation
reads: [session.is_new, user.prior_session_summary, summary.approved, summary.deleted, turn.user_text]
trigger: a new session opens on unfinished work, or the user refers to earlier work
moves: [offer_choices, admit_uncertainty, ask_one_question]
choices: ["Yes, continue", "Edit this summary", "Start fresh", "Something else"]
on_miss: ask
metric: resume success and user re-explanation rate
counter_metric: summaries used without approval
status: proposed
```

## 8. Related patterns
- [No warning of context loss](no-warning-of-context-loss.md): memory or early messages are dropped and the user is not told. This page is about a new session with no handover at all, even when nothing was dropped.
- [Cross-session confusion](../../../../../cross-cutting/accuracy/goals/context-management/failures/cross-session-confusion.md): the opposite problem, where information leaks or bleeds between sessions. Fresh-session amnesia is too little carried over; that is too much, or the wrong person's.
- [No channel switch, or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md): context lost when moving between channels. This page covers a new session in the same channel.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): the bot asks again within a session for facts it already has.
- [ChatGPT memory incident, November 2025](../../../incidents/chatgpt-memory-missing-memories-november-2025.md): stored memories went missing. That is loss of what was saved; this page is the lack of any carry-over.

## 9. Common questions
### Why does ChatGPT or Claude not remember my last conversation?
Often the product keeps each chat separate, or saves only short notes. Claude's help center says memory is saved as topics, project memory stays in its project, and incognito chats are not saved (see Section 4). Check your product's memory settings.

### Is a memory feature the same as a continuity summary?
No. Memory keeps lasting facts about you. A continuity summary carries one unfinished task forward, is shown to you first, and you can edit or delete it.

### Is it safe for an assistant to carry my last chat into a new one?
Only with consent. The summary should be visible, approved by the user, editable, and deletable, and must not be shared with anyone else. Where the vendor offers incognito or a pause, those should win over the summary.

### What can I do when my chatbot forgot everything?
Paste a few lines: the goal, what you decided, and what is left. A product should ask for exactly that if it cannot see your earlier chat.

---
## Technical section

### T1. Solution architecture
```
session end (or idle) -> summarizer (goal, decided, open) -> store as DRAFT, not memory
next session start    -> is there unfinished work + a draft?
                      -> show draft with source -> user: continue | edit | start fresh | delete
                      -> approved: load into context and (if user agrees) save; else discard
```

### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No summary loaded before the user has seen it | Session start logic | Test 1 and the approval-event log |
| Delete removes the summary from storage and from future sessions | Memory store | Test 4 |
| Summary belongs to one user only | Storage keys | Cross-user isolation test (see cross-session confusion) |
| Incognito or paused memory suppresses the offer | Session start logic | A test per setting |

### T3. Evals
- **Dataset:** a few dozen two-session scripts where the second session continues the first, plus some where it starts a new topic.
- **Judge rubric:** is the summary specific, correctly sourced, free of facts the user never gave, and followed by a clear choice?
- **Metrics and starting thresholds:** all starting points to tune. Offer made on 100% of continuing scripts; zero on new-topic scripts.
- **Release gate:** block a deploy if a summary loads without an approval event or cannot be deleted.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Summaries used without approval | Any | Any | Disable auto-load; audit the path |

### T5. Trade-offs
- Summaries can drift from what was said; show them for edit and keep a link to the source chat if the product has one.
- Storing summaries is storing personal data. Keep it minimal, user-visible, and deletable; set retention in policy.
- An offer on every session becomes noise. Offer only on unfinished work.

---
### Deep dive
- **Open question.** I found no study of how much re-explaining costs users, so the evidence here is vendor documentation and individual reports.
- **Unverified.** How ChatGPT's memory layers interact with new chats comes from third-party blogs seen only in search summaries; not used above.
- **References.** [Claude Help Center: Understanding Claude's memory](https://support.claude.com/en/articles/11817273-understanding-claude-s-memory) (opened); [OpenAI Developer Community thread, Feb 2025](https://community.openai.com/t/chatgpt-suddenly-forgot-everything-anyone-else-experiencing-this/1111406) (opened); [anthropics/claude-code issue 43696](https://github.com/anthropics/claude-code/issues/43696) (opened).
