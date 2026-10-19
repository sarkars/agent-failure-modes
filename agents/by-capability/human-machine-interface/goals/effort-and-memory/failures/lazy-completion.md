# Chatbot Does Part of the Job and Stops: Lazy Completion

<!-- SEO
title: Chatbot Only Does Part of the Task: Fix Lazy Completion and Placeholders
description: Why an assistant writes "rest of code here" or "repeat for the others" instead of finishing, what the evidence says, and rules for delivering the full job or listing exactly what is left.
search phrases:
- chatgpt lazy only does part of the task
- chatbot leaves placeholder code instead of full code
- ai says repeat for the other items
- chatgpt won't write the whole thing
- how to stop ai from truncating output
- ai gives sample instead of full list
- gpt-4 laziness fix
-->

**Frequency**: Common

## Issue: The assistant does a sample or part of the job and leaves the rest ("// rest of code here", "repeat for the others"), without saying exactly what is left or why.

> **One line:** Ten items were asked for; three arrived, plus a note to do the rest.

| | |
|---|---|
| **Channel** | Written for **chat** and coding or writing assistants. |
| **Stakes** | Low to medium. It wastes time; it is worse when the user does not notice the gap and ships the partial result. |
| **Who is affected** | Anyone who asks for a long list, a full file, a multi-part document, or a batch of similar items |
| **Frequency** | Common in reports. I found no study that measures how often it happens. The sources below are an acknowledged vendor episode, a contested test, and research on output length limits. |
| **Family** | [Effort and memory](../README.md) |
| **Goal** | The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't. |
| **Primary metric** | Completeness rate: required items delivered divided by items requested. Target: 100%, or an explicit gap list. |
| **Maturity** | Tests written (see [the test file](../../../tests/lazy-completion.md); not yet run) |
| **Will a better model fix this?** | Partly. OpenAI said in January 2024 that an update was intended to reduce "laziness", and research ties short outputs to training data, but a stronger model still needs a completeness check and a gap rule. (Our judgment, not tested.) |
| **Also searched as** | ChatGPT lazy · AI stops halfway · "rest of the code" placeholder · AI won't finish · truncated answer |

## 1. In plain words
The user asks for all 12 translations, the whole file, or every row. The assistant does the first few, then writes "and so on" or "// remaining cases similar". The work is incomplete, and often the reply reads as if it were finished.

## 2. What it looks like

**Without the fix**
```
User: Convert all 12 of these product names to snake_case and give me the full list.
Bot:  Here are the first few:
      1. Blue Widget -> blue_widget
      2. Red Gadget  -> red_gadget
      3. Green Gizmo -> green_gizmo
      ... and so on for the rest.
```

**With the fix**
```
Bot:  Here are all 12:
      1. Blue Widget -> blue_widget
      ... (all twelve listed)
      12. Pink Sprocket -> pink_sprocket
      (12 of 12 done.)
```
When the full job cannot fit, the fixed bot says so plainly: "I've done items 1 to 8. Items 9 to 12 are left because of the length of this reply. Say 'continue' and I'll do them."

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom and one sourced cause.
- **Output length habits.** A research paper found that models struggled to produce outputs beyond about 2,000 words and traced it to the scarcity of long-output examples in fine-tuning data (see section 4).
- **No completeness check.** Nothing compares the number of items delivered with the number requested.
- **Cost pressure.** Semafor's commentary noted that a chatbot that does less costs less to run. That is opinion, not evidence of cause; I did not find a source showing it is why any model did it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| OpenAI's ChatGPT account posted on December 8, 2023: "we've heard all your feedback about GPT4 getting lazier! we haven't updated the model since Nov 11th, and this certainly isn't intentional. model behavior can be unpredictable, and we're looking into fixing it." | Quoted in [Semafor, Dec. 12, 2023](https://www.semafor.com/article/12/12/2023/is-chatgpt-getting-lazier-over-the-holidays) and [Gigazine, Dec. 13, 2023](https://gigazine.net/gsc_news/en/20231213-chatgpt-winter-break-hypothesis). Both opened and read; I did not open the post itself. | A vendor acknowledgment through two secondary sources. It gives no root cause. |
| On January 25, 2024 OpenAI released an updated GPT-4 Turbo preview that "completes tasks like code generation more thoroughly than the previous preview model and is intended to reduce cases of 'laziness' where the model doesn't complete a task". CIO Dive says users had reported refusals and half-completed responses. | [CIO Dive, Jan. 25, 2024](https://www.ciodive.com/news/openai-laziness-gpt4-turbo-model-updates/705664/). Opened and read. | Trade press on one vendor's model; no counts. |
| A developer's API test found shorter completions when the system prompt said December than when it said May (the "winter break hypothesis"). A researcher who tried to reproduce it with N=240 could not find a significant difference. | [Gigazine](https://gigazine.net/gsc_news/en/20231213-chatgpt-winter-break-hypothesis), and [Semafor](https://www.semafor.com/article/12/12/2023/is-chatgpt-getting-lazier-over-the-holidays), which says the hypothesis is not proven. Opened and read. | Social-media tests, contested. I do not rely on it for any cause. |
| Long-context models that take inputs up to 100,000 tokens "struggle to generate outputs exceeding even a modest length of 2,000 words"; the authors' experiments tie the limit to the longest samples seen in supervised fine-tuning, and a pipeline that splits the task into subtasks produced outputs over 20,000 words. | [Bai et al., *LongWriter*, arXiv 2408.07055](https://arxiv.org/abs/2408.07055). Opened; abstract read. | 2024 models; about length, not about "laziness" as users describe it. It supports chunking as a fix. |

I did not find a study that measures how often assistants leave placeholders or stop partway. A practitioner prompt file that bans placeholder comments came up in my search, but I could not open it, so I do not use it.

**Public incident.** [OpenAI acknowledges reports of GPT-4 Turbo refusing tasks and giving half-completed answers (Dec. 2023 to Jan. 2024)](../../../incidents/openai-gpt-4-turbo-laziness-reports.md).

## 5. The fix

**The principle:** Do the full job, or say exactly what is left and why.

**Do this**
1. **Count what was asked.** If the request names a number of items, or a list, or a file, note the count before writing.
2. **Deliver all of it, or say how much.** End with a completeness line: "12 of 12 done", or "8 of 12 done; 9 to 12 remain".
3. **Never use placeholders in a deliverable.** No "// rest of code here", "and so on", or "repeat for the others", unless the user asked for a sample.
4. **If it will not fit, chunk and say so.** Deliver the first part, state what is left, and offer to continue. Do not stop silently.
5. **If you will not or cannot do part of it, say why.** A policy reason, a missing input, or a limit, stated plainly.
6. **Verify before sending.** Compare the delivered count to the requested count, and check for placeholder strings.
7. **Don't dress up a partial result as complete.** A partial result is labeled partial in the first line.

**Reference design: completeness check**
| Step | Check |
|---|---|
| Before | Requested items = N (from the request or the attached list) |
| During | Write items in order; no placeholders |
| After | Delivered = N? If not, add a gap line naming the missing items and the reason |
| Send | Completeness line at the end |

```
If the user asks for a set number of items, a full file, or every row, deliver all of them. Do not use placeholders such as "rest of code" or "and so on" unless the user asked for a sample.
If you cannot fit everything, deliver the first part, say exactly which items remain and why, and offer to continue.
End with a completeness line: "N of N done" or "X of N done; remaining: ...".
```

**Don't over-correct.** Do not pad answers to look thorough, and do not refuse a long job because it is long. When the user asked for a sample or an outline, give a sample or an outline. Do not repeat the whole work in each continuation.

**Hand-off rule.** If a job is too large for the assistant at all, say so and propose a split or a person ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/lazy-completion.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "All 12 items" | 12 items, or an exact gap line |
| 2 | "The full file" | No placeholder comments |
| 3 | A job too long for one reply | The first part, a gap list, an offer to continue |
| 4 | "Just give me a sample" | A sample, not the whole job |
| 5 | Part of the request is not allowed | The allowed part is done and the rest is explained |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Completeness rate** (primary) | 100%, or an explicit gap list | Items delivered divided by items requested, on requests with a countable target | Below 95% |
| Placeholder strings in deliverables | 0 | Match "rest of", "and so on", "// ...", "similar to above" in outputs | Any |
| Partial results without a gap line | 0 | Delivered below requested with no gap statement | Any |
| "Please continue" after a partial reply | Track; set from baseline | Next-turn classifier | Rising two weeks in a row |
| Padded answers (counter-metric) | Under 5% | Samples where length exceeds the minimal complete answer | Over 10% |

## 8. Related patterns
- [Deferring work to the user](deferring-work-to-the-user.md): the assistant hands a task back without starting it. Lazy completion starts the job and leaves part of it undone.
- [Answer buried](../../response-structure/failures/answer-buried.md): length without the answer first.
- [No warning of context loss](no-warning-of-context-loss.md): another case where the user is not told what is missing.
- [Conversation depth mismatch](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-depth-mismatch.md): the wrong amount of detail for the question.

## 9. Common questions
### Why does ChatGPT stop partway and tell me to do the rest?
Reports of this led OpenAI to say in December 2023 that it was looking into it. The sources I opened give no cause; one paper links short outputs to training data.

### How do I get the whole file instead of placeholders?
Ask for the complete file and say that placeholders are not acceptable, and ask it to end with a count of what it delivered. Products can enforce this with a completeness check.

### Is it okay for an assistant to say "I'll do the rest next"?
Yes, if it says exactly what is left and offers to continue. The failure is stopping silently.

### Does telling the model it is a certain month change this?
One developer's test said so; a researcher could not reproduce it. Do not rely on it.

---
## Technical section

### T1. Solution architecture
```
request -> count targets (items, files, rows) -> generate in chunks if needed
        -> completeness check (delivered vs requested, placeholder scan)
        -> send | regenerate | send with gap line and offer to continue
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Placeholder strings are blocked in deliverables | Output filter | Log scan |
| Delivered count equals requested count, or a gap line is present | Completeness checker | Test 1, 3 |
| Samples only when requested | Intent check | Test 4 |

### T3. Evals
- **Dataset:** 100 countable requests (lists, files, batches) of varying size, plus 30 where a sample is the right answer.
- **Judge rubric:** did the assistant deliver all items or give an exact gap line, with no placeholders?
- **Metrics and starting thresholds:** completeness 100% or a gap line; placeholders 0. Starting points to tune.
- **Release gate:** block a deploy if completeness falls on the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Completeness rate | Below 97% | Below 92% | Check the last prompt or model change |

### T5. Trade-offs
- Chunked delivery costs extra turns; it is better than a silent gap.
- A completeness check adds latency and tokens.

---
### Deep dive
- **Open question.** I found no measurement of how often placeholders or partial completions occur, and the "winter break" effect is not established.
- **References.** [Semafor, 2023](https://www.semafor.com/article/12/12/2023/is-chatgpt-getting-lazier-over-the-holidays) (opened); [Gigazine, 2023](https://gigazine.net/gsc_news/en/20231213-chatgpt-winter-break-hypothesis) (opened); [CIO Dive, 2024](https://www.ciodive.com/news/openai-laziness-gpt4-turbo-model-updates/705664/) (opened); [Bai et al., LongWriter](https://arxiv.org/abs/2408.07055) (abstract opened).
