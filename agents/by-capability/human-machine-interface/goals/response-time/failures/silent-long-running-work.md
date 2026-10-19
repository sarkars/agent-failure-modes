# Assistant Goes Quiet for Ten Seconds or More: Silent Long-Running Work

<!-- SEO
title: Chatbot or Agent Goes Silent While Working: Show Progress During Long Waits
description: Why an AI assistant that works for 10 seconds or more with no status leaves users unsure it is working, what response-time research and an agent feedback study found, and rules for status, progress, and ETA that are honest.
search phrases:
- chatbot stuck thinking no response
- ai agent working but no progress shown
- how long should a chatbot wait before showing a status
- progress indicator for ai agent tasks
- chatbot takes too long to respond what to show
- agentic ai status updates ux
- is the chatbot frozen or still working
-->

**Frequency**: Very Common

## Issue: The assistant works on a request for about 10 seconds or more, with no status, progress, or estimate, so the user cannot tell whether it is working or stuck.

> **One line:** Ten seconds of nothing looks the same as a crash.

| | |
|---|---|
| **Channel** | Written for **chat** and agent interfaces; voice has its own version in [slow tool silence](../../../../speech-and-audio/goals/conversation-flow/failures/slow-tool-silence.md). |
| **Stakes** | Low to medium. Users resend, reload, or leave, which can duplicate actions or lose work. |
| **Who is affected** | Anyone waiting on a multi-step or tool-using reply |
| **Frequency** | Very common in agent products that run several steps. I found no count. |
| **Family** | [Response time](../README.md) |
| **Goal** | Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. |
| **Primary metric** | Share of waits over 10 seconds with a progress or ETA message. Starting target: over 95% (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/silent-long-running-work.md); not yet run) |
| **Will a better model fix this?** | No. A faster model shortens waits, but showing status is an interface decision. (Our judgment, not tested.) |
| **Also searched as** | spinner forever · is it frozen · bot thinking too long · no loading state · agent silent while working |

## 1. In plain words
Fast replies need no status. A reply that takes a few seconds needs a sign that work has started. A job that takes ten seconds or more needs more: what it is doing, how far along it is, or when it will finish, and a way to stop or leave. Without that, people resend, which can start the work twice.

## 2. What it looks like

**Without the fix**
```
User: Find me the cheapest flight to Denver next Friday and book it.
Bot:  (nothing for 25 seconds)
User: hello?
Bot:  (nothing)
User: (sends the request again; two searches run, then two bookings are attempted)
```

**With the fix**
```
User: Find me the cheapest flight to Denver next Friday and book it.
Bot:  On it. Searching three airlines now (about 20 seconds). I'll show you the options before I book anything.
Bot:  Found 14 flights. Comparing prices... almost done.
Bot:  Cheapest: United 6:05 am, $148. Want me to book it?
```
The fixed bot says it started, says what it is doing and about how long it will take, and does not act until the user confirms.

## 3. Why it happens
These are our reading of the pattern.
- **The interface shows only the final reply.** Intermediate steps run, but nothing is displayed.
- **No estimate exists.** The system does not know how long a multi-step task will take, so nobody wrote a message.
- **Status is seen as clutter.** Teams fear noisy narration, so they show nothing.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Response-time limits: about 0.1 second feels instant; about 1 second keeps the user's flow of thought; about 10 seconds is the limit for keeping attention on the dialogue, after which users will want to do other tasks and should be given feedback on when the computer expects to be done; percent-done indicators are advised for operations over about 10 seconds, and feedback matters most when response times vary. | [Nielsen, *Response Times: The 3 Important Limits*, NN/g](https://www.nngroup.com/articles/response-times-3-important-limits/) (from the 1993 book *Usability Engineering*). Opened and read. | Old, general interface guidance, not tested on chat or agents. |
| In a controlled mixed-methods study (N=45) of an in-car agentic voice assistant, intermediate feedback (planned steps and intermediate results) significantly improved perceived speed, trust, and user experience and reduced task load compared with silent operation; interviews suggested high transparency at first, then less as the system proves reliable, adjusted for stakes. | [Kirmayr et al., *What Are You Doing?*, CHI 2026 (arXiv 2602.15569)](https://arxiv.org/abs/2602.15569). Opened; abstract read. | An in-car, voice, dual-task setting. The authors' findings may not transfer to desktop or coding agents. |
| An experiment on "visible thinking" in chatbots found that displayed reflections can anthropomorphise the agent and shape user expectations, which the authors flag in help-seeking settings. | [Cox et al., *Watching AI Think*, arXiv 2601.16720 (2026)](https://arxiv.org/abs/2601.16720). Opened; abstract read. | The abstract gives no timing results. I use it only as a caution that what you display is not neutral. |

I saw other claims in search summaries (for example, that slower replies can feel more thoughtful, and that skeleton screens shorten perceived waits). I did not open those sources, so I do not use them. I found no study of status messages in text-chat agents.

**Public incident.** No public incident found. I searched for dated reports of silent agent waits causing duplicated actions and found design guidance, not a sourced incident.

## 5. The fix

**The principle:** Under about a second, show nothing special. Over about a second, show that work has started. Over about ten, show what is happening and when it will end, and let the user leave or stop.

**Do this**
1. **Acknowledge fast.** If the first content will take over about a second, show that the request was received.
2. **Say what you are doing, truthfully.** "Searching three airlines" must reflect real work; do not narrate steps that are not happening.
3. **Show progress or an estimate past about ten seconds.** Use a step count or a time range only if you can stand behind it; otherwise say "this can take up to a minute".
4. **Let the user leave.** Offer to notify them when it is done, and keep the result in the conversation.
5. **Let the user stop.** A visible stop control, and a clear statement of what stopping does.
6. **Do not act twice.** Resending during a wait must not start a duplicate action; show "still working" and attach to the running job.
7. **Say when it fails or runs long.** If the wait passes the estimate, say so and offer a choice ([generic error messages](../../errors-and-recovery/failures/generic-error-messages.md)).
8. **Match detail to stakes and experience.** More narration for new, ambiguous, or high-stakes tasks; less once the user trusts the flow (the in-car study's interviewees preferred this).

**Reference design: wait states**
| Wait | What the user sees |
|---|---|
| Under about 1 s | The reply, no special feedback |
| About 1 to 10 s | "Working on it" with the current step |
| Over about 10 s | A step count or time range, a stop control, and an offer to notify |
| Past the estimate | "This is taking longer than expected" with a choice |

```
If a request will take more than a second to start answering, acknowledge it. If it will take more than ten seconds, say what you are doing and about how long, and offer to notify the user when done.
Only describe steps you are really doing. Do not start the same job twice if the user resends.
If it runs past your estimate, say so and let the user wait, stop, or come back later.
```

**Don't over-correct.** Do not narrate every micro-step on short tasks. Do not show a fake progress bar that moves with no real progress, and do not use a typing indicator that suggests a person is typing (deceptive typing indicators are a planned pattern in the [response-time roadmap](../../../roadmap/response-time.md)). Keep messages short.

**Hand-off rule.** If a job fails or the estimate is exceeded twice, offer a person and keep the request details ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/silent-long-running-work.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A 25-second task | A status within 2 seconds and a progress message by 10 |
| 2 | The user resends during a wait | No duplicate job |
| 3 | A task runs past its estimate | A "taking longer" message and a choice |
| 4 | A short task | No extra narration |
| 5 | The user stops the task | It stops and says what happened |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Waits over 10 s with a progress or ETA message** (primary) | Over 95% | Log: wait duration and status events | Below 90% |
| Time to first feedback | Under 1 s for an acknowledgment | p90 from request to first event | Over 2 s |
| Duplicate jobs from resends | 0 | Jobs started twice within a minute by the same request text | Any |
| False progress (counter-metric) | 0 | Progress events with no matching backend step | Any |
| Narration on short tasks (counter-metric) | Under 5% | Status messages on tasks under 3 s | Over 10% |

## 8. Related patterns
- [Slow tool silence](../../../../speech-and-audio/goals/conversation-flow/failures/slow-tool-silence.md): the voice version.
- [Streaming stalls](../../../../../cross-cutting/operations/goals/real-time-performance/failures/streaming-stalls.md): the technical stall behind a silent wait.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): what to say when the wait ends in failure.
- [Lazy completion](../../effort-and-memory/failures/lazy-completion.md): reporting what is left.
- [No reply to acknowledgments and closers](../../response-structure/failures/no-reply-to-acknowledgments-and-closers.md): another silent gap.

## 9. Common questions
### How long should a chatbot wait before showing a status?
The limits I read say about one second keeps flow and about ten seconds is the limit of attention. Acknowledge after about a second; show progress or an estimate past ten.

### Should an AI agent narrate every step?
Not always. In one in-car study, intermediate feedback improved perceived speed and trust, and interviewees preferred more detail at first and less as trust grew.

### Is a spinner enough?
For short waits, maybe. Past about ten seconds the guidance I read advises a percent-done indicator or an estimate; I did not find a chat-specific comparison.

### What if I resend while it is still working?
A good design recognizes the running job and does not start it twice.

---
## Technical section

### T1. Solution architecture
```
request -> job created (id) -> events: received | step N of M | tool call | done | failed
        -> UI renders status by elapsed time (1 s, 10 s) -> stop and notify controls
        -> duplicate guard (same request, same job id)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Status events come only from real steps | Job runner | Log: UI events vs backend steps |
| A duplicate request attaches to the running job | API layer | Test 2 |
| Past-estimate message after the estimate | UI | Test 3 |

### T3. Evals
- **Dataset:** 100 tasks of varying length (2 s to 90 s), including failures and resends.
- **Judge rubric:** were status, progress, and "taking longer" messages present at the right times, and were they truthful?
- **Metrics and starting thresholds:** waits over 10 s with progress over 95%; duplicates 0. Starting points to tune.
- **Release gate:** block a deploy if a new long-running tool lacks status events.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Duplicate jobs | Any | More than 1 per hour | Check the duplicate guard and resend handling |

### T5. Trade-offs
- More status can be noisy; scale it to elapsed time and stakes.
- An ETA that is often wrong hurts more than a range; use "up to" wording when unsure.

---
### Deep dive
- **Open question.** I found no study of status messages in text-chat agents. The in-car study is voice and the visible-thinking study is about empathy and competence perceptions.
- **References.** [Nielsen, NN/g](https://www.nngroup.com/articles/response-times-3-important-limits/) (opened); [Kirmayr et al., CHI 2026](https://arxiv.org/abs/2602.15569) (abstract opened); [Cox et al., 2026](https://arxiv.org/abs/2601.16720) (abstract opened).
