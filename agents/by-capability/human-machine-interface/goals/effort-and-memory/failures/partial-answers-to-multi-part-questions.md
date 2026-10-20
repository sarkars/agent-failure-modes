# Chatbot Ignores Part of My Question: Partial Answers to Multi-Part Questions

<!-- SEO
title: Chatbot Ignores Part of My Question: Fix Partial Answers
description: Why an LLM answers two of five questions in a multi-part prompt and drops the rest, what benchmarks show, and a rule that answers or acknowledges every part.
search phrases:
- chatbot ignores part of my question
- llm answers only first question of multi-part prompt
- chatgpt skips some of my questions
- ai ignores some instructions in a long prompt
- how to make ai answer every question in a message
- llm multiple instructions in one prompt fails
- claude skipped part of my message
-->

**Frequency**: Common

## Issue: The user asks several things in one message and the assistant answers some of them, drops the rest, and writes the reply as if it were complete.

> **One line:** Five questions went in; two were answered; nothing said the other three were skipped.

| | |
|---|---|
| **Channel** | Written for **chat** and coding or writing assistants. Voice and web: PLANNED, not written. |
| **Stakes** | Low to high. Low for a skipped side question; high when the dropped part is a deadline, an allergy, a cancellation, or the one question the user most needs answered. |
| **Who is affected** | Anyone who sends a message with several questions, requests, or constraints in it |
| **Frequency** | Common in reports. I found no study that counts how often chat assistants drop a part of a user's multi-part message. The nearest measured evidence is benchmark work on many instructions in one prompt (section 4). |
| **Pattern ID** | partial-answers-to-multi-part-questions |
| **Family** | [Effort and memory](../README.md) |
| **Goal** | The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't. |
| **Primary metric** | Part-coverage rate on multi-part prompts: parts answered or acknowledged divided by parts asked. Start: over 95% (tune). |
| **Maturity** | Researched (tests not yet written) |
| **Will a better model fix this?** | Partly. Benchmarks show scores falling as instructions pile up, and a model can still skip a part silently, so a stronger model needs a part check and a rule for saying what was skipped. (Our judgment, not tested.) |
| **Also searched as** | AI ignores half my prompt · chatbot skipped my second question · LLM drops instructions · ChatGPT only answers the first question · AI forgot part of my message |

## 1. In plain words
The user sends one message with several asks: "What's the fee, can I cancel online, and how long does a refund take?" The assistant answers the first and last, and the middle one never comes up. The reply reads as finished, so the user may not notice until they act on it.

## 2. What it looks like

**Without the fix**
```
User: Three things about my Summit Fitness membership: (1) what's the cancellation fee,
      (2) can I cancel online or only in person, (3) will I get back the $30 I paid for
      the annual locker rental?
Bot:  The cancellation fee is $25 if you cancel within the first year, and it is waived
      after that. Let me know if you have other questions!
```

**With the fix**
```
Bot:  1. Fee: $25 if you cancel in the first year; none after that.
      2. Online or in person: I can't confirm this. Our policy page doesn't say.
         I can connect you with a person who can.
      3. Locker rental: I don't have a rule on refunds for that, so I can't promise the $30.
      That covers all three. Want me to connect you with a person for 2 and 3?
```
The fixed reply gives every numbered part its own answer, and the two it cannot answer are named as unanswered instead of left out.

## 3. Why it happens
These are our reading of the pattern; the benchmark and the report in section 4 describe the symptom, not a proven cause.
- **Nothing counts the parts.** The model writes one fluent reply. No step lists the asks and checks each one against the draft, so a part missed in drafting stays missed.
- **More parts, more chances to miss one.** Benchmark scores fall as the number of instructions in a prompt rises (section 4). Parts buried mid-paragraph or phrased as a side clause are easy to skim past.
- **A partial answer looks complete.** The reply is fluent and well formed, so neither the model nor a reviewer sees a gap. Nothing in the format signals "I stopped at part 2".

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A benchmark of up to ten instructions per text prompt (ManyIFEval) found that across ten LLMs, "performance consistently degrades as the number of instructions increases." The abstract also says a logistic regression on instruction count predicts performance with about 10% error. | [Harada et al., *When Instructions Multiply*, arXiv 2509.21051, submitted 25 Sep 2025, EMNLP 2025](https://arxiv.org/abs/2509.21051). Opened; the abstract page only, not the full paper. | The instructions are formatting-style constraints on one generated text, not separate questions from a customer. The abstract gives no accuracy figures, so I quote none. |
| A user filed an issue against Claude Code (v2.1.222, an Opus model, dated Aug. 9, 2026) saying that in a long session the model repeatedly answered part of a multi-part message, silently dropped the rest, and did not say any item was deferred, declined, or pending. In one example, after correction, the model said "I skipped that part of your message entirely last turn." | [Claude Code issue 85255](https://claudeissues.com/issue/85255-model-silently-omits-parts-of-multi-part-requests-while-presenting-the-response) (mirror page). Opened and read. | One user's report on a coding agent. At the time of reading the page showed no maintainer response and an open status, so it is not a confirmed defect. |
| A study of multi-task inference (MTI Bench: 5,000 instances, 25 tasks, 2 to 3 sub-tasks each) found that putting several tasks in one call cut total inference time by 1.46x on average, and that Llama-2-Chat-70B and GPT-4 scored up to 7.3% and 12.4% better than when the tasks were run one at a time. | [Son et al., *Multi-Task Inference*, ACL 2024](https://aclanthology.org/2024.acl-long.304/). Opened; abstract only. | A counterpoint: bundling tasks does not always hurt. Dropped parts are not inevitable, and that study's sub-tasks are short benchmark items, not open-ended user messages. |

I found no controlled study of how often deployed chat assistants skip a part of a user's multi-part question, and no public incident dated and sourced for this exact failure.

**Public incident.** None found. The Claude Code issue above is a single open user report, not a confirmed incident.

## 5. The fix

**The principle:** Every part the user asked is answered, or named as not answered with a reason.

**Do this**
1. **List the parts before answering.** Split the message into its separate asks (questions, requests, constraints), in the user's order. Count them.
2. **Answer each part where the user will look for it.** Use the user's numbering or order, one labeled answer per part. A message with two or more parts gets a short numbered or labeled reply.
3. **Acknowledge, don't drop.** If a part cannot be answered (missing data, policy, out of scope), say "I can't answer 2 because...", with the reason and a next step.
4. **Do not merge parts so one disappears.** Two asks get two answers, even if both are short.
5. **End with a coverage line when there are three or more parts:** "That covers all three" or "Answered 1 and 3; 2 is open (see above)."
6. **Check before sending.** Compare the list of parts with the draft. Any part without an answer or an acknowledgment gets one before the reply goes out.
7. **Answer the urgent or high-stakes part first,** then the rest, when the user did not ask for an order.

**Reference design: part check**
| Step | Check |
|---|---|
| Before | Parts asked = N (split the message; count questions and requests) |
| During | One labeled answer or "can't answer" per part |
| After | Each part maps to an answer or an acknowledgment? If not, add it |
| Send | Coverage line when N is 3 or more |

```
When the user's message contains more than one question or request, list them first and answer every one.
Use the user's order or numbering. If you cannot answer a part, say so, say why, and give a next step.
Do not skip a part. For three or more parts, end with a line saying which parts are answered and which are open.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Each part that can be answered gets its answer, labeled, in the user's order. Put the high-stakes part first when order was not given. |
| Admit uncertainty and show how to check | A part cannot be answered or verified: say so, say why, and point to where the user can check. Do not guess to fill the slot. |
| Ask one clarifying question | One part is ambiguous and the answer changes with the meaning. Answer the clear parts anyway, and ask only about the unclear one. |
| Hand off to a person | The open part is high stakes and the assistant cannot answer it. Do not hand off the whole message when only one part is stuck. |

**Don't over-correct.** Do not turn a two-part message into a long report, and do not number a single-question reply. Do not restate each question at length before answering. When the user wants only one of several things ("just the fee"), answer that one. Do not answer parts nobody asked, to look thorough.

**Hand-off rule.** If a dropped or unanswerable part is high stakes and the assistant has no answer, offer a person and pass along the open parts ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A message with five numbered questions | Five answers or acknowledgments, in order |
| 2 | Three asks in one run-on sentence, no numbers | Three separate answers |
| 3 | One of three parts is outside what the bot knows | Two answers plus a named "can't answer" for the third |
| 4 | A buried side question at the end of a long paragraph | The side question is answered or acknowledged |
| 5 | The user asks only for one of several things | Only that one is answered; no padding |
| 6 | The user's later message says "you skipped my second question" | The skipped part is answered; no argument over whether it was asked |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Part-coverage rate on multi-part prompts** (primary) | Over 95% (start) | Split sampled multi-part user messages into parts; label each part answered, acknowledged, or dropped in the reply; divide the first two by all parts | Below 90% |
| Replies with a silently dropped part | Under 2% of multi-part replies | Sampled review: a part with neither answer nor acknowledgment | Over 5% |
| "You didn't answer" follow-ups | Track; set from baseline | Next-turn classifier for "you skipped...", "what about my...", a repeated earlier question | Rising two weeks in a row |
| Parts acknowledged as unanswered, with a reason | Track; set from baseline | Count of "can't answer" parts that name a reason | Falling while drops rise |
| Padded or over-structured replies (counter-metric) | Under 5% of replies | Single-question replies that were numbered or restated; replies that answer parts nobody asked | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User message has 3 or more questions or requests, and the reply has fewer answers than parts | Part count of the user turn versus answer count of the reply | The user said they only wanted one of them |
| User repeats an earlier question or says "you didn't answer" in the next turn | Next-turn classifier; same intent as a question in the previous turn | A follow-up that digs deeper into an answer the bot did give |
| Reply ends with an invitation like "Let me know if you have other questions" while a part of the user turn has no answer | Last sentence of the reply versus the part list | A closing line after every part was covered |
| Reply length is far below what the number of parts would need | Reply token count versus part count | A user who asked for a one-line answer |

**Starter rule:** when a message has more than one question or request, answer every part or say which part you can't answer and why.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: partial-answers-to-multi-part-questions
runs: pre_send
reads: [user_turn.parts, draft_reply.parts_covered]
trigger: a reply is about to be sent to a message with more than one question or request
moves: [lead_with_answer, admit_uncertainty, ask_clarifying_question, hand_off]
choices: none
on_miss: rewrite
metric: part-coverage rate on multi-part prompts
counter_metric: padded or over-structured replies
status: proposed
```

## 8. Related patterns
- [Lazy completion](lazy-completion.md): the user asked for N of one kind of item (all 12 translations) and got some. Here the asks are different questions, and each one is dropped whole, not left half-done.
- [Deferring work to the user](deferring-work-to-the-user.md): the bot answers a part by telling the user to go check it. Here the part gets no answer and no pointer at all.
- [Agent routes only the primary intent in a multi-issue ticket](../../../../../by-use-case/support-services/goals/ticket-routing/failures/agent-routes-only-primary-intent-in-multi-issue-ticket-dropping-secondary-urgent-issue.md): the same drop, but in the routing step of a support ticket, where the secondary issue never reaches a queue. This page is about the reply the user reads.
- [Answer buried](../../response-structure/failures/answer-buried.md): the answer is there but hard to find. Here it is missing.
- [Skipped steps with no receipt (roadmap row EM-06)](../../../roadmap/effort-completeness-and-memory.md): silent drops in a task with steps. Here the dropped items are the user's questions.

## 9. Common questions
### Why does my chatbot ignore part of my question?
Often the model writes one fluent reply and misses a part. Benchmarks show that scores fall as more instructions go into one prompt (section 4). I found no source that proves a cause for any single product.

### How do I get an AI to answer every question in my message?
Number the questions, one per line, and ask it to label each answer and to say which parts it could not answer. Our judgment, not tested.

### Should I split my questions into separate messages?
Not always. One benchmark found that bundling tasks in one call did not hurt and sometimes helped (section 4). Split when one part depends on another, or when a part was dropped twice.

### How can a team check whether its bot drops parts?
Take a sample of multi-part user messages, split each into parts, and label every part answered, acknowledged, or dropped. The share not dropped is the part-coverage rate in section 7.

---
## Technical section

### T1. Solution architecture
```
user turn -> part splitter (questions, requests, constraints; numbered if present)
          -> draft reply -> coverage check (each part -> answer | acknowledgment)
          -> gap? rewrite once with the missing part -> coverage line -> send + log (N parts, covered)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Every part has an answer or an acknowledgment before send | Pre-send check | Test 1 and the sampled review in section 7 |
| No invented answer to fill a slot | Pre-send check | Test 3 |
| Single-question replies stay short | Pre-send check | Test 5 |

### T3. Evals
- **Dataset:** a few hundred multi-part prompts with 2 to 8 parts each, with parts as numbered lists, run-on sentences, and a buried side question; mark which parts are unanswerable. Size is a starting point to tune.
- **Judge rubric:** for each part, is it answered, acknowledged with a reason, or dropped? Is any answer invented?
- **Metrics and starting thresholds:** part coverage over 95%; silently dropped parts under 2% of replies. Starting points to tune.
- **Release gate:** block a deploy if coverage on the eval set falls below the last release's.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Part-coverage rate | Below 95% | Below 90% | Sample dropped parts; check where in the prompt they sit |

### T5. Trade-offs
- A part splitter can miscount (a rhetorical question, a list inside one ask). Count it as a part only when a reply is needed.
- A coverage check adds a step before send and may add latency.
- Forcing structure on every reply makes simple answers stiff; apply it from two parts up.

---
### Deep dive
- **Open question.** I found no chat-specific study of dropped parts in user messages. The evidence is benchmark work on instruction counts and one user report.
- **Not claimed.** The "curse of instructions" label and IFScale, SIFo, Meeseeks and AGENTIF results appeared in search summaries only; I did not open them and use none of their numbers.
- **References.** [Harada et al., 2025](https://arxiv.org/abs/2509.21051) (opened, abstract); [Son et al., ACL 2024](https://aclanthology.org/2024.acl-long.304/) (opened, abstract); [Claude Code issue 85255](https://claudeissues.com/issue/85255-model-silently-omits-parts-of-multi-part-requests-while-presenting-the-response) (opened).
