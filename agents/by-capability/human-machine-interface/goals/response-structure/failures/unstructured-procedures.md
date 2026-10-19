# Chatbot Gives Step-by-Step Instructions as a Paragraph: Unstructured Procedures

<!-- SEO
title: Chatbot Step-by-Step Instructions Come as a Paragraph: Fix
description: Why chatbots give how-to steps as prose with merged or out-of-order actions, what style guides say about numbered steps, and a rule for one action per step.
search phrases:
- chatbot step by step instructions format
- chatbot gives instructions in a paragraph
- how to make a chatbot give numbered steps
- chatbot skips a step in instructions
- chatbot how-to answer hard to follow
- one action per step chatbot
- chatbot instructions out of order
-->

**Frequency**: Common

## Issue: The user asks how to do something, and the assistant answers in running prose where two or three actions share a sentence, steps are out of order, or a step is easy to miss.

> **One line:** The reply has the right content, but the user cannot tell where one step ends, which comes next, or which one they skipped.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice needs its own treatment: a listener cannot see a numbered list (planned, not written). |
| **Stakes** | Low for a settings change. Higher when a skipped or reordered step loses data, locks an account, or touches money or a device. |
| **Who is affected** | Anyone following a task while switching between the chat and another app, which is most how-to users |
| **Frequency** | Common as a style default. I found no study that counts how often chatbots answer procedures in prose. |
| **Pattern ID** | unstructured-procedures |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| **Primary metric** | Procedure replies using numbered steps. Target: 100% (tune). Paired with the user step-error rate. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Models can follow a "number the steps" instruction, but ordering and one-action-per-step depend on the prompt and a check, and a product also needs a rule for what counts as a procedure. (Our judgment, not tested.) |
| **Also searched as** | chatbot instructions hard to follow · bot skipped a step · wall of text how-to · bot lists steps out of order · chatbot numbered list |

## 1. In plain words
A how-to answer is something the user does while reading. They look at the chat, do a thing, look back, and need to find their place. Prose makes that hard. When two actions share one sentence, the user may do the first and forget the second. When the order is loose, they may do step 3 before step 2.

## 2. What it looks like

**Without the fix**
```
User: How do I download my W-2 from my payroll app?
Bot:  You can get your W-2 by signing in to the app and opening the Documents tab, then choosing Tax
      Forms, where you should select the year and tap Download, though before that you may need to
      turn on paperless delivery in Settings, otherwise the form won't appear.
```

**With the fix**
```
User: How do I download my W-2 from my payroll app?
Bot:  Do this first if you haven't already: turn on paperless delivery in Settings. Without it the form won't appear.
      1. Sign in to the app.
      2. Open the Documents tab.
      3. Tap Tax Forms.
      4. Select the tax year.
      5. Tap Download.
      Tell me which step you're on if something looks different.
```
The fixed reply puts the prerequisite before the steps, gives each action its own numbered line, and keeps the order the user follows. The "without" reply hides the prerequisite at the end, after the steps it affects.

## 3. Why it happens
These are our reading of the pattern.
- **Prose is the default register.** Assistants are tuned to sound conversational, so a procedure comes out as sentences joined by "then", "and", and "after that".
- **Conditions land where they occurred to the writer.** A prerequisite that comes to mind late is attached to the end of a sentence instead of moved to the top.
- **No rule for "this is a procedure".** The prompt says nothing about format, and nothing in the product checks whether the reply to a "how do I" question is a list.
- **Chat bubbles discourage long lists.** Teams trim formatting for short messages and lose it for procedures too.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google's developer style guide defines a procedure as "a sequence of numbered steps for accomplishing a task", says to use one step for each action, and says to write steps in the order the reader follows them. A single-step procedure is written as a bulleted item, not a numbered list. | [Google developer documentation style guide, *Procedures*](https://developers.google.com/style/procedures). Opened and read. | A style guide for documentation, not an experiment and not about chat. |
| Document360's knowledge-base guide says each numbered step should describe exactly one action, because readers can lose track of whether they finished the second part of a combined step. It allows an exception where two actions are so closely linked that splitting them feels artificial. | [Document360, *Procedures and steps*](https://docs.document360.com/docs/procedures-and-steps). Opened and read. | A vendor's writing guidance, not tested with users. |
| In an NN/g study of 8 site-specific AI chatbots with 9 participants, people scanned replies, found dense unformatted text overwhelming, and found bullets, headings, and bold text helped. The article recommends lists for processes with many steps. | [NN/g, *Less Chat, More Answer*](https://nngroup.com/articles/less-chat-more-answer). Opened and read. | Small qualitative study. It does not measure step errors. |

I found no controlled study that compares prose with numbered steps in chatbot replies, or that measures step errors in either form. My search turned up vendor guides and a questionnaire for chatbot usability, none of which tests this. The step-error metric below is therefore one you collect yourself.

**Public incident.** None found. I did not read a dated, public report of harm from a chatbot's unnumbered instructions.

## 5. The fix

**The principle:** When the user asks how to do something, the reply is a numbered list, in the order they will do it, with one action per step.

**Do this**
1. **Detect a procedure.** A request to do, set up, fix, install, change, or cancel something with more than one action is a procedure. A single-action answer is one sentence, not a list.
2. **Number the steps.** Use 1, 2, 3 on separate lines. Put nested actions under a step as a, b, c only when a step has real sub-steps.
3. **One action per step.** If a step has two verbs, split it. Keep the exception for actions that cannot be separated, such as holding a key while clicking.
4. **Start each step with the verb.** "Tap Download", not "You should then tap Download".
5. **Put conditions before the action they govern.** "If you use the web version, ..." comes first.
6. **Put prerequisites before step 1.** What the user needs, or must turn on, goes above the list, not at the end.
7. **Name what the user will see** when it helps them check the step worked: "A banner says Download started."
8. **Keep the list short.** For a long task, give the first 5-7 steps and offer the rest. Say how many steps there are in all.
9. **End with one way to continue.** "Tell me which step you're on." Do not add a second question.

**Reference design: procedure reply parts**
| Part | Content |
|---|---|
| Lead | One short sentence only if it adds a condition or prerequisite; otherwise start at step 1 |
| Prerequisites | What to have or turn on first (only if any) |
| Steps | Numbered, one action each, verb first, in order |
| Check | What the user sees when it worked (only if useful) |
| Next | "Tell me which step you're on" or an offer to go step by step |

```
When the user asks how to do a multi-action task, reply with a numbered list in the order they will do it.
Put each action on its own line, start with a verb, and put prerequisites and conditions before the step they affect.
For a one-action answer, use one sentence. For a long task, give the first 5-7 steps and offer the rest.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request is clear: start at step 1, or at the one prerequisite that changes the steps. No preamble. |
| Ask one clarifying question | The steps differ by platform, version, or plan and the session does not say which. Ask that one thing before listing. Do not ask when the steps are the same either way. |
| Offer choices: 2-4 options plus "Something else", free text open | The platform is unknown and there are a few likely ones: "Windows", "Mac", "Phone", "Something else". Do not offer them when the product already knows the platform. |

**Don't over-correct.** Do not number a reply that is an explanation, a comparison, or a single action. Do not split one action into five steps to look thorough. Do not drop the numbering to save space when the task has more than two actions.

**Framework used:** none yet. The rules come from the documentation style guides above.

## 6. How to test it (short version)
Results: **not yet run**. A full test file is not written.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "How do I reset my password?" (4 actions) | Numbered list, one action per line |
| 2 | A task with a prerequisite stated last in the source text | Prerequisite appears above step 1 |
| 3 | "Where is the Settings menu?" (one action) | One sentence, no list |
| 4 | A task whose steps differ by Windows and Mac, platform unknown | One question or a choice set before the steps |
| 5 | A task of 14 steps | First 5-7 steps shown and the rest offered, with the total stated |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Procedure replies using numbered steps** (primary) | 100% | Label each reply to a how-to request as procedure or not; count procedure replies with a numbered list | Below 95% |
| User step-error rate | Track; set from baseline | In sampled procedure conversations, a human labels whether the user's next message reports a wrong or skipped step | Rising two weeks in a row |
| Steps with more than one action | Under 5% of steps | Sampled review, or a check for two imperative verbs joined by "and" or "then" in one step | Over 10% |
| Prerequisite placed after step 1 | 0 | Sampled review of procedure replies with a prerequisite | Any |
| Repeat "what's the next step?" turns | Track; set from baseline | User turns right after a procedure reply that ask what comes next | Rising |
| Lists on non-procedure replies (counter-metric) | Under 5% | Numbered lists in replies labelled as explanations or single actions | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply to a how-to request has 3 or more action verbs and no list markers | Draft reply text plus intent label "how-to" | A short reply where the actions are trivial and linked |
| One sentence holds two imperative verbs joined by "then" or "and" | Parsed reply text | Two actions that cannot be separated, such as holding a key while clicking |
| User asks "what's next" or "which step" right after a procedure reply | Next user turn | The user wants an overview, not the next action |
| User reports doing a step out of order or skipping one | Next user turn, labelled | A real difference in their screen, not the reply |

**Starter rule:** a reply to a request to do something with more than one action is a numbered list, one action per line, in order.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: unstructured-procedures
runs: pre_send
reads: [turn.intent, draft.format, session.platform]
trigger: the intent is a multi-action how-to and the draft is not a numbered list
moves: [lead_with_answer, ask_clarifying_question, offer_choices]
choices: ["Windows", "Mac", "Phone", "Something else"]
on_miss: rewrite
metric: procedure replies using numbered steps
counter_metric: numbered lists on non-procedure replies
status: proposed
```

## 8. Related patterns
- [Answer buried](answer-buried.md): the same family. That page is about where the answer sits in a reply; this one is about the shape of a reply that is a procedure. A procedure can lead with the answer and still be one long paragraph.
- [Deferring work to the user](../../effort-and-memory/failures/deferring-work-to-the-user.md): hands the user a task. This page is about how a task the bot should explain is laid out.
- [No way back in a flow](../../dialogue-management/failures/no-way-back-in-a-flow.md): what to do when the user is partway through steps and needs to go back.

## 9. Common questions
### How should a chatbot format step-by-step instructions?
As a numbered list in the order the user does them, one action per step, each step starting with a verb. Put prerequisites above the list.

### Should every chatbot answer be a numbered list?
No. Use a list for a task with more than one action. A single action is one sentence, and an explanation stays in short paragraphs. Google's style guide also says a one-step procedure is not numbered.

### What if the steps depend on the user's device or plan?
Ask one question or offer a few choices before the steps, with "Something else" always open, unless the session already knows.

### How many steps should one reply have?
I found no tested limit. A practical starting point is 5-7 steps, then offer the rest. That is a number to tune, not a sourced figure.

---
## Technical section

### T1. Solution architecture
```
user turn -> intent label (how-to | explanation | single action | other)
          -> draft reply -> format check (numbered list? one verb per step? prerequisite above step 1?)
          -> pass | rewrite -> send, and log (intent, format, check result)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| A how-to reply has a numbered list | Pre-send format check | Test 1; log scan |
| Prerequisites sit above step 1 | Pre-send check on the draft | Test 2 |
| One-action answers are not turned into lists | Pre-send check | Test 3 |

### T3. Evals
- **Dataset:** 100 how-to requests with a known step order, mixed with 50 explanation and single-action requests.
- **Judge rubric:** is it a numbered list, in the right order, with one action per step, and the prerequisite first?
- **Metrics and starting thresholds:** numbered-step rate 100% on the how-to set; list rate on the other set under 5%. Starting points to tune.
- **Release gate:** block a prompt or model change that lowers the numbered-step rate on the how-to set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Procedure replies using numbered steps | Below 95% | Below 85% | Check the latest prompt or model change |

### T5. Trade-offs
- Numbered lists take more vertical space in a small chat window. NN/g found that dense text overwhelmed participants, so the cost is usually worth it for procedures.
- A format check can mislabel an explanation as a procedure. Keep the counter-metric on the dashboard.

---
### Deep dive
- **Open question.** I found no chat study that measures step errors with prose versus numbered steps. The evidence is documentation style guidance and one small chatbot usability study.
- **References.** [Google developer documentation style guide, Procedures](https://developers.google.com/style/procedures) (opened); [Document360, Procedures and steps](https://docs.document360.com/docs/procedures-and-steps) (opened); [NN/g, Less Chat, More Answer](https://nngroup.com/articles/less-chat-more-answer) (opened).
