<!--
CONVERSATION GUIDE TEMPLATE

A guide tells a chatbot what to do at one moment where a known failure pattern happens.
It leads with the behavior to aim for. The check that spots a miss comes second.

RULES
1. One guide per Pattern ID. File name: conversation-guides/<pattern-id>.md, the same name as the pattern file.
   Never rename or move a guide once published.
2. Line 1 is the H1, phrased the way a developer searches ("How to stop a chatbot from guessing: ask a clarifying question").
3. Derive everything from the pattern's own fix, metrics and detection signals. Invent no data, thresholds or results.
4. Checks are "proposed, not yet calibrated" until checked against human-labeled conversations.
5. Chat first. Voice and web signals are listed as PLANNED, never as detected.
6. "Offer choices" is a move, not a default: say when it helps and when a menu would trap the user.
   Choices are 2-4 options plus "Something else", and free text always stays open.
7. The Guide spec block at the end is fixed-format so code can be built from it later. Keep its keys.
8. American examples. Cite only sources you opened.
-->

# [How to stop a chatbot from ...]: [guide name]

<!-- SEO
title: [<=60 chars, starts with the searched phrase]
description: [<=155 chars, says what the bot should do instead]
search phrases:
- [real query 1]
- [real query 2]
-->

> **Do this:** [the target behavior in one sentence]

| | |
|---|---|
| **Pattern ID** | [pattern-id] (link to the pattern page) |
| **Guides the moment when** | [the trigger: what is happening in the conversation] |
| **Runs** | Before sending / After the turn / Across the conversation |
| **Status** | Proposed, not yet calibrated |

## 1. What good looks like
[2-3 sentences. The behavior, not the failure.]

```
User: ...
Bot:  ...
```

## 2. The moves
Pick the first move that fits. Each move is one sentence of behavior plus a short example line.

| Move | Use it when | Example |
|---|---|---|
| Lead with the answer | [...] | [...] |
| Ask one clarifying question | [...] | [...] |
| Offer choices | [...] | "Do you mean A, B, or something else?" |
| Admit uncertainty and show how to check | [...] | [...] |
| Hand off to a person | [...] | [...] |

Keep only the moves that apply to this pattern.

## 3. When not to use it
[The over-correction this guide can cause, from the pattern's "Don't over-correct" line.]

## 4. The check (proposed, not yet calibrated)
How to spot that the bot did not follow this guide, taken from the pattern's detection signals.

| Signal | Counter-signal (what it could be instead) |
|---|---|
| [...] | [...] |

## 5. Guide spec
```
pattern_id: [pattern-id]
runs: [pre_send | post_turn | conversation]
reads: [event schema v0.1 fields]
trigger: [plain-language condition]
moves: [ordered list from section 2]
choices: [when offered: 2-4 options + something_else; free_text: always]
on_miss: [log | rewrite | ask | handoff]
metric: [the pattern's primary metric]
counter_metric: [what must not get worse]
status: proposed
```

## Related
- [Pattern page]
- [Conversation guides index](../conversation-guides/README.md)
