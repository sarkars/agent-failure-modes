# Chatbot Buries the Answer: Long Preamble Before the Point

<!-- SEO
title: Chatbot Buries the Answer: How to Lead With the Answer
description: Why chatbots open with a long preamble before the answer, what research says about scanning and over-long replies, and rules for answer-first chat replies.
search phrases:
- chatbot gives long answer before the point
- how to make a chatbot answer first
- chatbot response too long
- chatbot starts with great question
- answer first chatbot response design
- inverted pyramid chatbot
- chatbot restates my question before answering
-->

**Frequency**: Very Common

## Issue: The assistant opens with a restatement, a caveat, or background, and the thing the user asked for sits several lines down, or at the end.

> **One line:** The user has to read the whole reply to find out whether it answered them.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice is a different case: a spoken preamble cannot be skimmed past (see [verbosity despite brevity instructions](../../../../speech-and-audio/goals/conversation-flow/failures/verbosity-despite-brevity-instructions.md)). |
| **Stakes** | Usually low. It rises when the buried part is a deadline, a fee, a safety step, or a "no". |
| **Who is affected** | Everyone, most of all people reading on a phone or in a hurry |
| **Frequency** | Very common as a style default. I found no study that counts it; the sources below show that models over-generate and that people scan. |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. |
| **Primary metric** | Answer-first rate: the first sentence holds the answer or the next step. Starting target: over 90% (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/answer-buried.md); not yet run) |
| **Will a better model fix this?** | Partly. Models can be told to lead with the answer, but the default style is shaped by training, and replies in a product also need a rule for when the answer is "it depends". (Our judgment, not tested.) |
| **Also searched as** | bot restates my question · chatbot fluff before the answer · TL;DR first · BLUF for chatbots · long winded bot |

## 1. In plain words
A reply can be correct and still fail if the answer is not where the reader looks first. The common shape is: a compliment ("Great question!"), a restatement of the question, some background, a caveat, and then the answer.

## 2. What it looks like

**Without the fix**
```
User: Can I return opened headphones?
Bot:  Great question! Returns are an important part of the shopping experience, and we want you to be
      completely satisfied. Our return policy depends on several factors, including the product category,
      the purchase date, and the condition of the item. For electronics, ... [4 more lines] ...
      So in short: yes, opened headphones can be returned within 30 days if they are in working condition.
```

**With the fix**
```
User: Can I return opened headphones?
Bot:  Yes, within 30 days of delivery, if they still work. Want me to start the return? I'll need your order number.
```
The fixed reply puts the answer and the next step in the first two sentences. Detail follows only if asked, or in a short second paragraph.

## 3. Why it happens
These are our reading of the pattern, with the one sourced cause marked.
- **Length is rewarded in training.** The roadmap notes work finding that reward models track output length; I did not open it, so treat it as a lead. YapBench (below) reports that preference-based training and LLM judges can induce a length bias.
- **A polite opener is the default.** Assistants are tuned to sound warm, so they restate and praise before answering.
- **Prompts ask for thoroughness.** "Be thorough and helpful" with no rule on order produces background first.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Nielsen Norman Group describes the inverted pyramid (most important information first) as suited to the web because users read carefully only rarely, and says readers can stop at any point and still get the main point. | [Schade, *Inverted Pyramid: Writing for Comprehension*, NN/g, 2018](https://www.nngroup.com/articles/inverted-pyramid/). Opened and read. | Guidance for web pages, not chat. Applying it to chat is our inference. |
| In NN/g's research, 79% of test users always scanned a new page and 16% read word by word. In a test of five versions of the same site, the concise version scored 58% better on measured usability and the scannable version 47% better, and a version combining three changes (concise, scannable, objective) 124% better. | [Nielsen, *How Users Read on the Web*, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/). Opened and read. | A 1997 study of web pages with a small usability test. It is old and not about chat. |
| A January 2026 benchmark of over 300 brevity-ideal prompts across 76 assistant models found an order-of-magnitude spread in median excess length, with failure modes such as filling the space on ambiguous inputs and explanation or formatting overhead on one-line requests. | [Borisov et al., *Do Chatbot LLMs Talk Too Much? The YapBench Benchmark*, arXiv 2601.00624](https://arxiv.org/abs/2601.00624). Opened; abstract read. | A preprint. It measures excess length, not whether the answer was buried or whether users were hurt. |

I did not find a chat study that tests answer-first ordering directly. Several sources from my searches were vendor blogs with general UX advice, which I do not use as evidence.

**Public incident.** No public incident found. I searched for reports of verbose or long-winded chatbots in news, lawsuits, and regulator material and found surveys, commentary, and one tech-site anecdote about an escalation loop (a different failure).

## 5. The fix

**The principle:** The first sentence answers the question or states the next step. Everything else is optional and can be skipped.

**Do this**
1. **Lead with the answer.** The first sentence is the answer ("Yes, within 30 days"), the decision, or the next step. No praise, no restating the question.
2. **Give the one condition that changes the answer, right after it** ("if they still work").
3. **When the answer is "it depends", say what it depends on in sentence one** and ask for that one fact.
4. **Put the next step second.** Offer the action and name what you need.
5. **Add detail below, short.** Use one short paragraph or three bullets. If more is needed, offer it ("Want the full policy?").
6. **Keep must-know items out of the tail.** A deadline, a fee, or a safety step goes in the first two sentences, not the last line.
7. **Match length to the question.** A yes/no question gets a one-line answer first.

**Reference design: answer-first shape**
| Slot | Content |
|---|---|
| 1 | The answer or decision, in one sentence |
| 2 | The one condition or the next step |
| 3 (optional) | Short support: reason, source, or steps |
| 4 (optional) | An offer of more |

```
Start every reply with the answer or the next step in one sentence. Do not open with praise, a restatement of the question, or background.
Put any condition that changes the answer in the next sentence. If the answer depends on something, say what in the first sentence and ask for it.
Put deadlines, fees, and safety steps in the first two sentences.
After that, add at most one short paragraph or three bullets, then offer more detail.
```

**Don't over-correct.** Do not cut needed safety, legal, or medical caveats to save space; move them up, not out. Do not be curt on a hard emotional message (see [family patterns on emotion](../../emotional-intelligence/README.md)). Do not answer "yes" when the true answer is "it depends".

**Hand-off rule.** If the answer cannot be given safely (account-specific, legal, or high-stakes), say so in the first sentence and route to a person ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/answer-buried.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A yes/no policy question | The first sentence says yes or no |
| 2 | "It depends" question | Sentence one names the dependency and asks for it |
| 3 | Deadline in the answer | The deadline is in the first two sentences |
| 4 | "Great question" bait | No praise or restatement opener |
| 5 | A hard question needing a caveat | The caveat is kept, and near the top |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Answer-first rate** (primary) | Over 90% | A labeled sample: does the first sentence hold the answer or next step? | Below 80% |
| Praise or restatement openers | Under 2% | Pattern match on openers ("Great question", "You're asking about") | Over 5% |
| Must-know items in the first two sentences | Over 95% where applicable | Labeled sample | Below 85% |
| Follow-up "so is that a yes?" rate | Track; set from baseline | Next-turn classifier | Rising two weeks in a row |
| Caveat retention (counter-metric) | No drop | Replies on high-stakes topics that keep required caveats | Any drop after a change |

## 8. Related patterns
- [Verbosity despite brevity instructions](../../../../speech-and-audio/goals/conversation-flow/failures/verbosity-despite-brevity-instructions.md): the voice and instruction-following side.
- [Monologue without engagement](../../../../speech-and-audio/goals/conversation-flow/failures/monologue-without-engagement.md): long turns that never check in.
- [Conversation depth mismatch](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-depth-mismatch.md): the wrong amount of detail for the question. This page is about order, not amount.
- [Generic first response](../../embedded-copilots/failures/generic-first-response.md): a related opener problem.
- [No reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md): the short-message end of the same family.

## 9. Common questions
### Should a chatbot answer first and explain after?
Yes for most questions. The NN/g guidance I opened says readers can stop at any point and still get the main point. It is web guidance, so test it in chat.

### Isn't a short opener polite?
A short greeting on the first turn is fine. After that, "Great question!" before every answer adds length with no information.

### What if the honest answer is "it depends"?
Say that in the first sentence and name the one thing it depends on, then ask for it.

### Won't answer-first replies drop important caveats?
They should not. Move the caveat up, next to the answer, not out. See [the fix](#5-the-fix).

---
## Technical section

### T1. Solution architecture
```
question -> generate draft -> answer-first check (first sentence = answer | next step | dependency)
                           -> must-know items check (deadline, fee, safety in first two sentences)
                           -> send, or regenerate with the rule
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No praise or restatement opener | Output filter or prompt | Pattern match in logs |
| Must-know items in first two sentences | Judge check on tagged intents | Labeled sample |
| Caveats on high-stakes topics preserved | Policy layer | Test 5 |

### T3. Evals
- **Dataset:** 200 real questions from logs, with a label for the answer and the must-know items.
- **Judge rubric:** is the answer in the first sentence, is the condition next, and are required caveats present?
- **Metrics and starting thresholds:** answer-first over 90%; caveat retention 100% on high-stakes items. Starting points to tune.
- **Release gate:** block a prompt change if answer-first or caveat retention falls on the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Answer-first rate | Below 85% | Below 75% | Review recent prompt or model changes |

### T5. Trade-offs
- An answer-first rule can make replies feel abrupt on emotional topics; allow a one-line acknowledgment first there.
- A judge model that prefers longer replies may mark answer-first replies down; calibrate it on human labels.

---
### Deep dive
- **Open question.** I found no chat-specific study of answer ordering. The NN/g sources study web pages, and YapBench measures length, not order.
- **References.** [Schade, NN/g, 2018](https://www.nngroup.com/articles/inverted-pyramid/) (opened); [Nielsen, NN/g, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/) (opened); [Borisov et al., 2026](https://arxiv.org/abs/2601.00624) (abstract opened).
