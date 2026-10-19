# Chatbot Hides Dates and Amounts in Paragraphs: Key Details Buried

<!-- SEO
title: Chatbot Hides Dates and Amounts in Paragraphs: How to Fix It
description: Why chatbots bury dates, amounts, deadlines and required actions inside paragraphs, and a layout rule that makes them easy to find and double-check.
search phrases:
- chatbot highlight important information in reply
- how to make chatbot bold dates and amounts
- chatbot reply hard to scan
- chatbot buries deadline in paragraph
- chatbot response format key details
- how to make an AI assistant list required actions
- chatbot confirmation message what to include
-->

**Frequency**: Common

## Issue: The assistant puts dates, amounts, deadlines and required actions inside long paragraphs, so the user has to hunt for them and cannot quickly double-check them.

> **One line:** The reply may start with the right answer, but the numbers and dates that matter are hidden mid-sentence.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice is a different case: a spoken list cannot be scanned, and voice signals here are PLANNED, not detected. |
| **Stakes** | Medium to high when the missed fact is a payment amount, a deadline, or a step the user must take. Low for casual replies. |
| **Who is affected** | Anyone who must act on the reply, most of all people on a phone or in a hurry |
| **Frequency** | Common as a style default. I found no study that counts it in chat products. |
| **Pattern ID** | key-details-buried |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| **Primary metric** | Critical-facts-surfaced rate: share of replies where every date, amount, deadline and required action is set apart from the paragraph text (rule or judge check). Starting target: over 90% (tune). Paired with the re-ask rate for the date or amount. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can be told to set facts apart, but the layout depends on the product prompt and the chat window's formatting support. Cause owner: the model's default style. (Our judgment, not tested.) |
| **Also searched as** | chatbot bold important information · bot buried the due date · chatbot wall of text with numbers · highlight key details in AI answer · make chatbot list next steps |

## 1. In plain words
A reply can lead with the answer and still hide what the user needs to act. The due date, the fee, or the step the user must take sits in the middle of a paragraph, written like any other sentence. The user has to read every line to be sure they found it, and cannot check it quickly later.

## 2. What it looks like

**Without the fix**
```
User: I want to cancel my gym membership. What happens now?
Bot:  Sure, I can help with that. Cancellations are processed at the end of your billing cycle, so as
      long as we receive your written request by October 28 you will not be charged for November,
      though a $49 early termination fee applies to memberships started within the last 12 months,
      and you will need to return your key fob to the front desk before your last day.
User: Wait, what is the deadline again, and how much is the fee?
```

**With the fix**
```
User: I want to cancel my gym membership. What happens now?
Bot:  You can cancel. Here is what you need to know:
      - Deadline: send your written request by October 28 to avoid a November charge.
      - Fee: $49 early termination fee (memberships started in the last 12 months).
      - Your action: return your key fob to the front desk before your last day.
      Want me to start the written request?
```
The facts are the same. The fixed reply gives each one a label and its own line, with the exact value, so the user can find it and check it against their own records.

## 3. Why it happens
These are our reading of the pattern.
- **Prose is the default shape.** Assistants write flowing sentences, so a date or amount ends up as one clause among several.
- **Formatting rules are unclear or avoided.** Teams tell the model to keep replies short and conversational, or the chat window cannot render lists, so the model avoids structure.
- **Over-correction in the other direction.** When a prompt says "bold anything important," models bold everything, and emphasis stops working (see the Moveworks row below).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NN/g lists "highlighted keywords" and "bulleted lists" among the features of scannable text, and reports the scannable version of a test site scored 47% better on measured usability than the control. | [Nielsen, *How Users Read on the Web*, NN/g, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/). Opened and read (page text through a fetch tool). | A 1997 study of web pages. It is not about chat, and it tests whole pages, not single facts. |
| NN/g's error-message guidance says to use "noticeable, redundant, and accessible indicators" and never color or animation alone. | [Neusesser and Sunwall, *Error-Message Guidelines*, NN/g, 2023](https://www.nngroup.com/articles/error-message-guidelines/). Opened and read. | About error messages, not general replies. Used here only for the point that emphasis should not rely on one cue. |
| A Moveworks product post (June 25, 2026) says its assistant over-applied bold to IDs, ticket numbers, dates and metrics, and "When everything is bold, nothing stands out." It also says screen readers do not announce bold. After a strict allowlist, inappropriate bold fell about 88% (5.15 to 0.61 spans per response) in a 250-sample evaluation. | [Moveworks Community, bold text in responses](https://community.moveworks.com/ideas/minor-ml-update-improvements-to-bold-text-in-responses-3657). Opened and read. | A vendor's own post about its own product and test. It supports the warning against over-bolding, not a claim that bolding helps users. |

I did not find a chat study that tests whether setting dates and amounts apart reduces missed deadlines or re-asks. The claim that it does is our inference from the scanning research. A search for confirmation-message guidance returned vendor email blogs that advise showing the date and amount; I do not use them as evidence.

**Public incident.** No public incident found. I did not search for one in news or regulator material beyond the three searches behind this page.

## 5. The fix

**The principle:** Every date, amount, deadline and required action gets a label and its own line, with the exact value, and nothing else is emphasized.

**Do this**
1. **Give each critical fact its own labeled line or bullet.** Use labels such as "Deadline:", "Amount:", "Your action:". Each holds the exact value ("October 28", "$49"), not a vague phrase ("end of the month", "a small fee").
2. **Keep the label in plain text.** Do not rely on bold alone: screen readers do not announce it (Moveworks post). The label word carries the meaning.
3. **Put the facts in the first screen of the reply.** The answer comes first (see [answer buried](answer-buried.md)); the labeled facts follow right after it.
4. **One fact per line.** Do not pack two dates or an amount and a deadline into one bullet.
5. **Say when a fact is not confirmed.** If the date or amount comes from a source the bot has not checked, say so in the same line ("Deadline: October 28, per the policy page; confirm on your account").
6. **Emphasize sparingly.** Bold only the value itself, and only one or two per reply. Do not bold whole sentences, IDs, or every number.
7. **Do not make a list for a reply with no critical facts.** A greeting, a yes/no with no condition, or an explanation stays as prose.

**Reference design: critical-facts block**
| Slot | Content |
|---|---|
| 1 | The answer in one sentence |
| 2 | Labeled lines: Deadline, Amount, Your action (only those that apply) |
| 3 (optional) | Short reason or source |
| 4 (optional) | An offer of the next step |

```
After the answer, list every date, amount, deadline and required action on its own line with a plain-text label and the exact value.
Use "Deadline:", "Amount:" and "Your action:". Bold at most the value, one or two per reply.
If a value is not confirmed, say where it came from. If a reply has no such facts, write plain prose.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reply that contains a date, amount, deadline or required action: the answer first, then the labeled facts. |
| Admit uncertainty and show how to check | A value is unconfirmed or comes from a document the bot cannot verify: say so on the same line and say where the user can check. |
| Hand off to a person | The amount or deadline is account-specific and the bot cannot read it (billing disputes, legal deadlines): say so first and route to a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not turn every reply into a form. Do not bold every number. Do not drop the plain-prose explanation when the user asked "why". Do not cut a needed caveat to make the list shorter; put it on its own line.

**Hand-off rule.** If the exact amount or date cannot be read from a trusted source, do not guess a value. Say so and route to a person ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Cancellation with a deadline and a fee | Deadline and fee each on a labeled line with exact values |
| 2 | Reply with one required action | The action is a labeled line, not a mid-paragraph clause |
| 3 | Unconfirmed date from a policy page | The line says where the date came from |
| 4 | Plain explanation, no dates or amounts | Stays as prose, no list |
| 5 | Prompt says "bold what is important" | Bold limited to one or two values, not whole sentences |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Critical-facts-surfaced rate** (primary) | Over 90% | Rule check (labeled line or bullet holds each date, amount, deadline, action) plus a judge check on a labeled sample | Below 80% |
| Re-ask rate for the date or amount | Track; set from baseline | Next user turn asks for the same date, fee or amount ("what was the deadline again?") | Rising two weeks in a row |
| Values stated exactly (not "soon", "a small fee") | Over 95% where a value exists | Labeled sample | Below 85% |
| Replies with more than two bold spans | Under 5% | Count bold spans per reply in logs | Over 10% |
| Plain-prose replies wrongly turned into lists (counter-metric) | Under 5% | Labeled sample of replies with no critical facts | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat; none is detected for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Date, currency amount or deadline phrase appears inside a paragraph of 3 or more sentences, with no label or list line | Pattern match on the reply text for dates and currency, plus line structure | A short reply where the single date is already in sentence one |
| User asks again for a value the bot already gave ("what was the deadline?") | Same intent in the next user turn, or a next-turn classifier hit | A user who wants a different date, not the one already given |
| Reply contains a required action with no "Your action" line or bullet | Tagged intents with a required step found only mid-paragraph | A reply that is only an explanation with no step to take |
| Value is vague where an exact one exists ("soon", "a small fee") | Judge check against the source document | The source itself gives no exact value |
| Reply has more than two bold spans | Count of bold markup in the reply | A product that renders no bold and shows markup characters |

**Starter rule:** every date, amount, deadline and required action in a reply is on its own labeled line with the exact value.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: key-details-buried
runs: pre_send
reads: [draft_reply.text, draft_reply.critical_facts, user_turn.intent]
trigger: a reply that contains a date, amount, deadline or required action is about to be sent
moves: [lead_with_answer, admit_uncertainty, hand_off]
choices: none
on_miss: rewrite
metric: critical-facts-surfaced rate
counter_metric: plain-prose replies wrongly turned into lists
status: proposed
```

## 8. Related patterns
- [Answer buried](answer-buried.md): the closest pattern. That page is about order: the answer or next step sits below a preamble. This page is about form: a reply can lead with the answer and still hide the dates, amounts and required actions inside a paragraph. A reply can fail either one, both, or neither.
- [No reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md): the short-message end of the same family.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): an error message also needs what happened, what is saved and the next step, each easy to find.

## 9. Common questions
### How do I make a chatbot highlight important information in its reply?
Tell it to put each date, amount, deadline and required action on its own line with a plain-text label and the exact value. Bold at most the value itself. See [the fix](#5-the-fix).

### Should a chatbot bold dates and amounts?
Only sparingly. The Moveworks post I opened says that when everything is bold, nothing stands out, and that screen readers do not announce bold. Use the label word as the main cue and bold one or two values.

### Is this the same as putting the answer first?
No. [Answer buried](answer-buried.md) is about where the answer sits. This page is about how the facts are written once the answer is given. Use both rules together.

### Does this mean every reply should be a bullet list?
No. A reply with no date, amount, deadline or required action stays as prose. Lists for everything are an over-correction.

---
## Technical section

### T1. Solution architecture
```
draft reply -> critical-fact detector (dates, currency, deadline phrases, required steps)
            -> layout check (each fact on a labeled line? exact value? bold count?)
            -> send, or regenerate with the rule
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Each detected fact is on a labeled line or bullet | Output filter or prompt | Pattern match in logs |
| Bold spans per reply capped | Output filter | Count in logs |
| Unconfirmed values name their source | Judge check on tagged intents | Labeled sample |

### T3. Evals
- **Dataset:** 150 real replies from logs that contain at least one date, amount, deadline or required action, plus 50 that contain none.
- **Judge rubric:** is each critical fact on its own labeled line, is the value exact, is a source named when unconfirmed, and is prose left alone when there are no facts?
- **Metrics and starting thresholds:** critical-facts-surfaced over 90%; wrongly formatted prose replies under 5%. Starting points to tune.
- **Release gate:** block a prompt change if the surfaced rate falls or the bold-span count rises on the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Critical-facts-surfaced rate | Below 85% | Below 75% | Review recent prompt, model or renderer changes |

### T5. Trade-offs
- Labeled lines add length and can feel form-like on casual topics; limit them to replies that contain critical facts.
- A chat window that does not render markdown will show raw symbols; use plain labels and line breaks there.
- A fact detector can miss unusual date formats; calibrate it on your own logs.

---
### Deep dive
- **Open question.** I found no chat-specific study of whether labeled lines cut missed deadlines or re-asks. The evidence is general scanning research and one vendor post.
- **References.** [Nielsen, NN/g, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/) (opened); [Neusesser and Sunwall, NN/g, 2023](https://www.nngroup.com/articles/error-message-guidelines/) (opened); [Moveworks Community post, June 25, 2026](https://community.moveworks.com/ideas/minor-ml-update-improvements-to-bold-text-in-responses-3657) (opened).
