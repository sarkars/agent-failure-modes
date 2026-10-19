# Chatbot Stops Mid-Answer or Never Replies: Silent Failure and Timeout

<!-- SEO
title: Chatbot Stops Mid-Answer or Never Replies: Silent Failure
description: Why a request that times out or a streamed answer that cuts off, with no error shown, leaves users stuck. How to detect incomplete responses and end every failure with a visible state.
search phrases:
- chatbot stops mid sentence
- chatbot request timed out no response
- llm streaming response cut off
- chatbot stuck loading never answers
- how to detect incomplete llm stream finish_reason
- chatbot timeout fallback message
- ai agent request timeout handling ux
-->

**Frequency**: Common

## Issue: A request times out or a streamed answer is cut off and the user sees no error: a spinner that never ends, or partial text that looks finished.

> **One line:** The worst failure is the one that says nothing: the user cannot tell whether to wait, retry, or leave.

| | |
|---|---|
| **Channel** | Written for **chat** and agent interfaces. Voice has its own version ([slow tool silence](../../../../speech-and-audio/goals/conversation-flow/failures/slow-tool-silence.md)); voice signals below are marked planned. |
| **Stakes** | Medium. Users resend, which can duplicate actions, or act on a partial answer. |
| **Who is affected** | Anyone whose request hits a timeout, a dropped connection, or a failed tool call |
| **Frequency** | Common in products that stream replies or call slow tools. I found developer reports and vendor guidance, but no count. |
| **Pattern ID** | silent-failure-and-timeout |
| **Family** | [Response time](../README.md) |
| **Goal** | Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. |
| **Primary metric** | Silent-failure rate: requests that end with no reply, no error, and no marker that the answer is incomplete. Starting target: 0. |
| **Maturity** | Tests written (see [the test file](../../../tests/silent-failure-and-timeout.md); not yet run) |
| **Will a better model fix this?** | No. The failure is in the transport, timeouts, and interface, not in the model's wording. (Our judgment, not tested.) |
| **Also searched as** | chatbot stops mid sentence · request timed out no message · chat stuck loading forever · response cut off · bot never answered |

## 1. In plain words
Two things go wrong. A request times out and the screen stays on a spinner or on nothing. Or a streamed answer stops partway and the interface shows what arrived as if it were the whole answer. In both cases the system knows something failed, and the user does not. The fix is to make every request end in a visible state: done, incomplete, or failed, each with a next step.

[Silent long-running work](silent-long-running-work.md) covers waits that are still going. [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md) covers failures that show a poor message. This page covers failures that show **no** message, and cut-off answers that look complete.

## 2. What it looks like

**Without the fix**
```
User: Summarize the three refund cases from this thread.
Bot:  Case 1: a $48 duplicate charge, refunded on March 3. Case 2: a late delivery where the customer
      was offered a cre
      (the text stops here; no error, no retry button)
User: hello?
User: (reloads the page; the answer is gone)
```

**With the fix**
```
User: Summarize the three refund cases from this thread.
Bot:  Case 1: a $48 duplicate charge, refunded on March 3. Case 2: a late delivery where the customer
      was offered a cre
      [This answer was cut off. Your question is saved. Continue the answer / Start over]
```
The fixed version marks the answer as incomplete, keeps the question, and offers to continue.

## 3. Why it happens
These are our reading of the pattern, supported by the sources in section 4.
- **A clean end of stream is mistaken for a complete answer.** Streams can end with the normal end marker even though the text stopped early.
- **Timeouts are handled below the conversation.** A gateway or flow aborts a slow request, and the chat layer never receives an event to show.
- **No state for "incomplete".** The interface knows "loading" and "done", so a partial answer is rendered as done.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Atlassian's Forge documentation says streaming LLM responses "increase the risk of delivering incomplete output to the user, particularly in cases of interruptions such as timeouts or network failures". It says the LLM's text can cut off early and the client can also fail to receive the finishing stream messages, and gives one way to detect an incomplete response: check whether a completion choice with a `finish_reason` is missing when the stream ends. | [Atlassian, Handling LLM API streaming errors](https://developer.atlassian.com/platform/forge/runtime-reference/forge-llms-api-errors/) (page last updated Jul 23, 2026). Opened and read. | Vendor documentation for one platform; the `finish_reason` check applies to APIs that send it. |
| The same page recommends recovering by prompting the model with the prior context and the interrupted output, instead of resubmitting the original prompt, and reports that Claude Sonnet 4.5 usually either resumes from the interrupted text or explains that the output already met the instruction. | Same page. Opened and read. | One vendor's observation on one model; not a controlled test. |
| A developer reported on the OpenAI community forum (January 22, 2024) that Chat Completion in stream mode returned a fragment ("hmm, 1+1 is equ") and then the stream received the final DONE message, even for one-word answers and with history turned off. | [OpenAI Developer Community thread](https://community.openai.com/t/chat-completion-in-stream-mode-cuts-off-the-answer-mid-sentence/597554). Opened and read. | A single user report; I did not verify the cause or whether it was fixed. It shows that a normal end marker and a truncated answer can occur together. |
| Canva's app design guidelines say an error message should tell users what went wrong and what to do next ("trying again, or reloading the page"), warn that vague messages like "Something went wrong" are frustrating, and say to avoid technical codes like "504 gateway timeout" for general users. | [Canva Developers, Errors & messaging](https://www.canva.dev/docs/apps/design-guidelines/errors/). Opened and read. | General interface guidance, not tested on chat. |

I read other reports in search summaries only: a vendor-forum thread on a flow that aborted after a timeout with no response (the page I tried to open returned a 404), a Cursor forum bug report about agent turns that cut off mid-sentence, and a Zapier community post about a chatbot stuck on "awaiting response". I did not open them, so I do not rely on them. I found no study measuring how often silent failures occur in production chat.

**Public incident.** No public incident found. The sources above are developer reports and vendor guidance, not a dated incident with a named company and documented user harm.

## 5. The fix

**The principle:** Every request ends in one of three visible states: complete, incomplete, or failed. Never a spinner with no end, and never partial text shown as finished.

**Do this**
1. **Put a deadline on every wait.** When a request passes its deadline, end the spinner and show a failure state. The deadline can be a range tied to the task, in line with [silent long-running work](silent-long-running-work.md).
2. **Treat the stream as complete only on a positive signal.** Where the API sends a finish reason, mark the answer incomplete if it is missing when the stream closes (the check Atlassian describes). Where it does not, use your own end-of-answer marker.
3. **Show an incomplete state.** Label a cut-off answer ("This answer was cut off") and keep the partial text visible.
4. **Name what happened, what is saved, and what to do.** Use the three parts from [generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): cause in plain words, whether the question and any partial work are saved, one next step. Show a short reference code for support, not as the message.
5. **Offer to continue, not only to retry.** For a cut-off answer, offer "Continue" using the prior context and partial output, as Atlassian suggests, and "Start over" as the second choice.
6. **Do not act twice.** A retry or resend after a timeout must not repeat an action that already ran (reuse the job id, as in silent long-running work).
7. **Log every failure with its cause.** A timeout, a dropped stream, and a failed tool call are different causes and different fixes.

**Reference design: request end states**
| End state | What the user sees | What is logged |
|---|---|---|
| Complete | The answer, no marker | `end_reason=complete` |
| Incomplete | The partial text, "This answer was cut off", Continue / Start over | `end_reason=incomplete` with the last received event |
| Timed out | "This is taking longer than we can wait. Your question is saved. Try again, or I can notify you." | `end_reason=timeout` with the deadline and elapsed time |
| Failed | The cause in plain words, what is saved, one next step | `end_reason=failed` with a cause code |

```
Every request ends with exactly one end state: complete, incomplete, timed out, or failed.
If an answer stopped before its natural end, say it was cut off and offer to continue.
If a request fails or times out, say what happened, whether the user's message is saved, and one next step.
Never present partial text as a finished answer.
```

**Don't over-correct.** Do not show an error for every slow reply that finishes, do not retry automatically without limit (it can duplicate actions and hide a real outage), and do not mark an intentionally short answer as incomplete. A false "cut off" label costs trust as much as a missing one.

**Hand-off rule.** If a request fails twice in a row, offer a person and pass the saved question with it ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/silent-failure-and-timeout.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | The backend never answers | A failure state appears at the deadline, not a spinner |
| 2 | The stream stops mid-sentence and then closes | The answer is marked incomplete with a Continue choice |
| 3 | A tool call fails | The cause, what is saved, and a next step are shown |
| 4 | The user resends after a timeout | No duplicate action |
| 5 | A normal answer finishes | No error or incomplete marker |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Silent-failure rate** (primary) | 0 | Requests with no `end_reason`, or whose UI never left the loading state past the deadline | Any |
| Streams closed without a finish signal | Track; set from baseline | Streams that closed with no finish reason and no complete marker | Rising two weeks in a row |
| Incomplete answers shown as complete (counter-check) | 0 | Sampled review of answers ending mid-sentence with no incomplete marker | Any |
| Failures with cause, saved state, and next step | 100% | Log: end reason and the template used | Below 95% |
| False incomplete labels (counter-metric) | Under 1% | Answers labeled cut off that were complete | Over 3% |
| Duplicate actions after a timeout retry | 0 | Actions started twice within a minute from one request | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A request has a start event and no end event within the deadline | Request start with no matching answer or error event | A very long job that reported progress and finished late |
| Stream closed with no finish reason | Stream close event missing `finish_reason` (where the API sends one) | An API or provider that never sends one |
| Assistant text ends without terminal punctuation or a closing structure, then the stream closes | Last chars of the final assistant message | A deliberately short or list-style answer |
| User sends "hello?", "??", or repeats the message soon after sending | Next user turn within a short window with the same or empty content | A user adding a new detail |
| User reloads or leaves right after a request with no reply | Session end or page load event after a request start | The user got the answer elsewhere |
Voice signals (silence on the line, the caller hanging up during a tool wait) are **planned**, not yet written.

**Starter rule:** every request ends in a labeled state (complete, incomplete, timed out, or failed), and a cut-off answer is never shown as finished.

## 8. Related patterns
- [Silent long-running work](silent-long-running-work.md): the wait is still going; this page is about waits that end without a message.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): the failure is shown, but poorly.
- [Streaming stalls](../../../../../cross-cutting/operations/goals/real-time-performance/failures/streaming-stalls.md): the technical stall behind a pause.
- [Lazy completion](../../effort-and-memory/failures/lazy-completion.md): an answer that ends early on purpose rather than by failure.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on when a person takes over.

## 9. Common questions
### Why does my chatbot stop mid-sentence?
Several causes are reported: a dropped connection, a timeout, a length limit, or a stream that closes before the model finishes. Atlassian's documentation lists timeouts and network failures as the interruptions that cause incomplete streamed output. Your own logs will show which one it is.

### How do I know a streamed answer is complete?
If your API sends a finish reason, check that one arrived before the stream closed; Atlassian describes this check. A stream can also close normally with a truncated answer (one forum user reported exactly this), so a normal close is not proof.

### What should the chatbot say when a request times out?
Say what happened in plain words, that the question is saved, and one next step. Canva's guidelines suggest trying again or reloading, and advise against codes like "504 gateway timeout" in the message itself.

### Should the bot retry automatically?
Once, quietly, is often reasonable if no action has run yet. Beyond that, show the failure and let the user choose, because repeated retries can duplicate actions.

---
## Technical section

### T1. Solution architecture
```
request -> job (id, deadline) -> stream events: start | delta | tool | finish(reason) | close
        -> end-state resolver: complete (finish signal) | incomplete (closed without it)
                              | timed out (deadline passed) | failed (error or tool failure)
        -> UI renders the end state; log end_reason, last_event, cause code
        -> continue path: prior context + partial output -> resume prompt
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Every job resolves to exactly one end state | End-state resolver | Log scan: jobs with no end state |
| A closed stream without a finish signal is never rendered as complete | Client | Test 2 |
| A retry reuses the job id | API layer | Test 4 |
| The loading state ends at the deadline | Client | Test 1 |

### T3. Evals
- **Dataset:** 100 injected failures: backend silence, mid-stream cut-offs, dropped connections, tool failures, plus 20 normal replies as controls.
- **Judge rubric:** did the user see the right end state, the saved-state message, and a next step; were controls left untouched?
- **Metrics and starting thresholds:** silent failures 0; false incomplete labels under 1%. Starting points to tune.
- **Release gate:** block a deploy if a new streaming path has no end-state handling.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Silent-failure rate | Any | More than 5 in an hour | Check deadlines and the stream-close handler |
| Streams closed without a finish signal | Rising | Doubling day over day | Check the provider, gateway timeouts, and recent deploys |

### T5. Trade-offs
- A short deadline hides real slow successes; a long one prolongs silence. Set it per task type and show progress ([silent long-running work](silent-long-running-work.md)).
- Resuming from partial output depends on the model following the instruction; Atlassian reports two typical responses, so show the result and let the user accept or start over.
- Marking incomplete answers needs a reliable signal; where the provider sends none, you have to define your own.

---
### Deep dive
- **Open question.** I found no measured rate of silent failures in production chat and no study of how users react to an "incomplete" label. The evidence is vendor guidance and developer reports.
- **References.** [Atlassian, Handling LLM API streaming errors](https://developer.atlassian.com/platform/forge/runtime-reference/forge-llms-api-errors/) (opened); [OpenAI Developer Community thread, January 2024](https://community.openai.com/t/chat-completion-in-stream-mode-cuts-off-the-answer-mid-sentence/597554) (opened); [Canva Developers, Errors & messaging](https://www.canva.dev/docs/apps/design-guidelines/errors/) (opened).
