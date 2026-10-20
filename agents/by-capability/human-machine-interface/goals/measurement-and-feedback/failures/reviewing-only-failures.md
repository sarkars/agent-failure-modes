# Chatbot Quality Review Only Reads Complaints: Reviewing Only Failures

<!-- SEO
title: Chatbot Quality Review Only Reads Complaints: Fix It
description: A chatbot QA process that reads only complaints and bad ratings misses the users who quietly give up. Sample conversations at random, including successes.
search phrases:
- how to review chatbot conversations for quality
- how many chatbot conversations should I review
- chatbot QA random sample of conversations
- chatbot only looking at thumbs down feedback
- silent failures in ai chatbots
- how to find chatbot problems users don't report
- ai agent error analysis production traces
-->

**Frequency**: Common

## Issue: The team reviews only the chats that drew a complaint, a thumbs-down, or a handoff, so users who quietly give up never get read.

> **One line:** The team reads the complaints and calls that quality review, so every failure that nobody reported stays invisible; the fix is to also read a random sample of all conversations, successes included.

| | |
|---|---|
| **Channel** | Written for **chat** (web, app, in-product). Voice and web-page signals are PLANNED, not written, detected, or measured. |
| **Stakes** | Any. A quiet failure on a billing, health, or legal question can hurt a user and never reach the team. |
| **Who is affected** | Users who fail and say nothing, and the team that thinks the bot works |
| **Frequency** | Common (our judgment). I found no count of how many teams review only complaints; the evidence below is practitioner guidance and one consumer-research summary. |
| **Pattern ID** | reviewing-only-failures |
| **Family** | [Measurement and feedback](../README.md) |
| **Goal** | Teams can tell whether conversations really work, and users can tell the team when they don't. |
| **Primary metric** | Share of reviewed conversations that are random samples. Starting target: at least 50% of each review cycle (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model changes how often the bot fails, not which chats the team opens. Choosing what to read is process work. (Our judgment, not tested.) |
| **Also searched as** | chatbot only reviewing complaints · QA only on thumbs down · silent chatbot failures · unreported bad answers · how many chats to review · sample chatbot transcripts |

## 1. In plain words
Most users who get a bad answer do not complain. They close the window. If the team reads only chats with a complaint, a low rating, or a handoff, it sees the loud failures and none of the quiet ones. The fix is to read a random sample of all closed conversations every cycle, including ones that look fine.

## 2. What it looks like
Example: an electric utility's billing chatbot. The team reads complaints each Friday.

**Without the fix**
```
User: Can I get my late fee waived? My check was delayed in the mail.
Bot:  Late fees are $15 after the due date. You can pay online at any time.
User: I know. I'm asking about a waiver for this one.
Bot:  Payments made by the due date avoid late fees. Is there anything else I can help with?
User: (closes the window; no rating, no complaint)
Friday review: 4 chats with complaints read, all about the outage line. This chat is never opened.
Dashboard: contained.
```

**With the fix**
```
User: Can I get my late fee waived? My check was delayed in the mail.
Bot:  Late fees are $15 after the due date. You can pay online at any time.
User: I know. I'm asking about a waiver for this one.
Bot:  Payments made by the due date avoid late fees. Is there anything else I can help with?
User: No, that's it.
Bot:  Before you go: did you get what you needed? [Yes] [Partly] [No, I still need help] [Something else]
User: No, I still need help
Bot:  I couldn't answer the waiver question. Want a billing specialist? They will see this chat.
Friday review: 100 randomly drawn chats read, 31 not contained. This one was drawn (source: random), failed, no complaint.
```
The fixed team opens chats it was never told about, and the bot checks in only on chats the sampler picked.

## 3. Why it happens
These are our reading of the pattern.
- **The review queue is fed by complaints.** Tickets, thumbs-downs, and handoffs are the easy lists to pull, so they become the whole review.
- **Dashboards count a quiet exit as a pass.** A chat with no handoff and no complaint is counted as contained. See [metrics: containment](../../../reference/metrics.md).
- **Reading chats costs time.** Teams pick the chats most likely to be bad and skip the rest. Kaizo, a vendor, says teams read three percent of conversations because reading was expensive (see section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "Up to two-thirds of customers do not report their dissatisfaction", from interviews with "scores of actual consumers" (Stephens and Gwinner, East Carolina University). | [ASU W. P. Carey news, Sept. 27, 2006](https://news.wpcarey.asu.edu/20060927-penny-your-thoughts-when-customers-dont-complain). Opened and read. | A news summary of a consumer-behavior paper, not the paper. Not chat; the study date and sample size are not given on the page. |
| Husain and Shankar: "The simplest approach is reviewing a random sample of traces." They recommend at least 100 traces, 2 to 4 week review cycles, and keeping random traces in every batch so you find failure modes your other signals miss. | [Husain and Shankar, *AI Evals: Everything You Need to Know*, published Sept. 18, 2026](https://hamel.dev/blog/posts/evals-faq/). Opened; the first 100,000 of about 153,000 characters read. | Expert practitioner guidance (they also teach evals), not an experiment. The last third of the page was not read. |
| Kaizo says teams read three percent of conversations, and argues against a random start for AI agents: "AI failures are systematic," so a small random sample "either misses it or surfaces one instance you dismiss as an outlier." It recommends scoring every conversation. | [Kaizo blog, "Your AI Agent Is Closing Tickets. Who Is Checking It?", July 27, 2026](https://kaizo.com/blog/qa-for-ai-handled-conversations/). Opened and read. | Vendor selling automated scoring; single source; no author named. It disagrees with the fix on where to start, and the rules below keep targeted slices alongside the random sample. |
| Langfuse documents error analysis as five steps: gather a representative sample, open-code the first thing that went wrong in each trace, cluster, label and measure, then decide and act. | [Langfuse docs, Error analysis](https://langfuse.com/blog/2025-08-29-error-analysis-to-evaluate-llm-applications). Opened and read. | Vendor docs, undated. It gives no sample size and does not say "random". |

I found no controlled study that compares complaint-only review with random sampling for chatbots, and no independent count of the quiet-failure rate. The numbers above show that many unhappy people stay silent (in general consumer research) and that experts sample at random; they do not measure how many chatbot failures a complaint queue misses.

**Public incident.** No public incident found where a chatbot's failures went unseen because only complaints were reviewed. Searches run: "chatbot quality review random sample conversations not just complaints silent failure"; "most dissatisfied customers do not complain silent unhappy customers study"; "LLM application evaluation review production traces random sample error analysis Hamel Husain". A figure of 96% of unhappy customers not complaining reached me only through a search summary of a vendor blog, and the 1999 "26 to 1" figure only through summaries, so I do not use either.

## 5. The fix
**The principle:** Every review cycle reads a random sample of all conversations, successes included, and labels where each reviewed chat came from.

**Do this**
1. **Draw a random sample each cycle with no outcome filter.** Sample from all closed conversations before removing anything. Test: the sample query has no rating, handoff, or complaint condition, and the random seed is logged.
2. **Include successes.** Chats that were contained, thumbs-up, or unrated are in the pool at their natural share. Test: the sample contains at least one chat from each outcome bucket.
3. **Tag the source of every reviewed chat.** Use `random`, `complaint`, `flagged`, or `high_risk`. Test: no reviewed chat has an empty source.
4. **Keep the complaint queue, and keep it separate.** Complaints get their own triage ([report path](no-way-to-report-bad-behaviour.md)). Random chats do not replace it.
5. **Review at least 100 random chats per cycle.** This is Husain and Shankar's suggested minimum; treat it as a starting point and read all chats if you have fewer. Test: count of random reviews per cycle.
6. **Judge against what the user needed, not what the bot said.** Pass or fail, plus one note on the first thing that went wrong. Test: every random review has a verdict and, on a fail, a note.
7. **Report the quiet-failure rate.** Of failed random chats, the share with no complaint, no thumbs-down, and no handoff. Test: the number appears on the review report.
8. **Add targeted slices on top.** Add extra reads for risky topics, long chats, or repeated retries. Never let slices shrink the random share below its target (Kaizo's point is why slices exist; the random share is what gives an unbiased rate).

**Reference design: sampling plan**
| Queue | How chats enter | Share of the review |
|---|---|---|
| `random` | Hash of conversation id picks a fixed share of all closed chats | At least 50% (primary metric) |
| `high_risk` | Rules on topic: money, health, legal | Extra, not counted in the random share |
| `flagged` | Retries, very long chats, monitor flags | Extra |
| `complaint` | Thumbs-down, report, escalation | Handled by the report path |

```
Pick sampled chats at conversation start by hashing the conversation id, so the check can run at close.
For a sampled chat that ends without a confirmed outcome, ask once: "Did you get what you needed?"
Offer: Yes, Partly, No I still need help, Something else. Keep free text open. Never ask in every chat.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | When a randomly sampled chat closes with no confirmed outcome: "Yes", "Partly", "No, I still need help", "Something else". Do not offer them in chats outside the sample, after the user already said it worked, or when the user is still mid-task. |
| Hand off to a person | The user answers "No, I still need help" and the topic is money, health, or legal, or the same question failed twice. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not read only random chats and drop complaints or high-risk slices: the sample is a rate, not a safety net. Do not ask every user for a verdict; that adds friction and skews who answers. Do not treat a clean random sample as proof of no problem: a rare fault can hide in it.

**Hand-off rule.** If a sampled user says they still need help and the topic is high-stakes, offer a person in the same turn and pass the chat ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**. Each test maps to a rule in section 5.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Inspect this week's sample query | No outcome filter; the seed is logged | 1 |
| 2 | Count outcome buckets in the sample | Contained, thumbs-up, and unrated chats are all present | 2 |
| 3 | Open 20 reviewed chats | Each has a source tag | 3 |
| 4 | Thumbs-down a reply | It goes to the complaint queue, not only the sample | 4 |
| 5 | Count random reviews for the cycle | At least 100, or all chats if fewer | 5 |
| 6 | Open 10 failed random reviews | Each has a verdict and a first-thing-wrong note | 6 |
| 7 | Read the review report | It shows the quiet-failure rate | 7 |
| 8 | Add a high-risk slice | The random share stays at or above target | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Share of reviewed conversations that are random samples** (primary) | At least 50% per cycle | Reviewed chats with source `random` divided by all reviewed chats | Below 30% |
| Random reviews per cycle | At least 100 | Count of `random` review records | Below 50 |
| Quiet-failure rate | Track from baseline | Failed random chats with no complaint, thumbs-down, or handoff, divided by random chats | Rising two cycles in a row |
| Reviewed chats with a source tag | 100% | Review records with source set | Any missing |
| Sample bias check | Within a few points of traffic mix | Compare outcome mix of the sample to all closed chats | Any outcome bucket missing |
| Complaint queue median time to triage (counter-metric) | Under 2 business days | `triaged_at` minus `created_at` | Over 5 business days |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log. All are written for text chat; voice and web-page equivalents are PLANNED, not written. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Review records exist and none has source `random` | Review record `source` field | A new team that has not started sampling yet |
| User leaves right after a bot reply that repeats their question back | Session end event within 1 turn of the bot turn; user's last two messages share the same intent | The user got the answer and left |
| Chat closed as contained with no user confirmation and no later contact | `contained` true, `confirmed_resolution` empty, no repeat contact in the window | A one-fact question that needs no confirmation |
| Review queue has only chats with `thumbs_down`, `report`, or `handoff` events | Event types of all reviewed chats | A week that was spent on an incident |
| Sample outcome mix differs from traffic mix | Outcome counts, sample vs all chats | A holiday week with unusual traffic |

**Starter rule:** every review cycle reads a random sample of all closed chats, with no outcome filter and a source tag on each review.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: reviewing-only-failures
runs: conversation
reads: [conversation.sample_flag, conversation.outcome, session.confirmed_resolution, review.source, review.verdict]
trigger: a randomly sampled conversation closes with no confirmed outcome
moves: [offer_choices, hand_off]
choices: ["Yes", "Partly", "No, I still need help", "Something else"]
on_miss: log
metric: share of reviewed conversations that are random samples
counter_metric: complaint queue median time to triage
status: proposed
```

## 8. Related patterns
- [No way to report bad behaviour](no-way-to-report-bad-behaviour.md): closest match. It is about whether a user can flag a bad reply and whether a person reads it. This pattern is about the team also reading chats nobody flagged.
- [Satisfaction metric gaming](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/satisfaction-metric-gaming.md): the bot is tuned to raise ratings. Here the ratings are fine; the team just never reads the unrated chats.
- [Answer and go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): the bot ends without confirming. The silent-exit metric there is a signal this pattern's sample can verify. (No page named "containment counted as success" exists in the library; this and [metrics](../../../reference/metrics.md) cover it.)
- [User feedback bias](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/user-feedback-bias.md): button data under-represents most users. Sampling is one fix for that.

## 9. Common questions
### How many chatbot conversations should I review?
Husain and Shankar suggest at least 100 traces per review cycle, with cycles of 2 to 4 weeks. Treat that as a starting point, and read all chats if you have fewer ([source](https://hamel.dev/blog/posts/evals-faq/)).

### Should I review random chats or only the risky ones?
Both. A random sample gives an unbiased failure rate. Targeted slices find rare faults a small sample misses. Kaizo, a vendor, argues against starting random; this page keeps both and counts only random chats toward the primary metric.

### Is a chat with no complaint a successful chat?
Not necessarily. Consumer research summarized by ASU says up to two-thirds of dissatisfied customers do not report it. That finding is not about chatbots, so read some quiet chats to find out for your own bot.

### What is a silent failure in a chatbot?
A chat the dashboard counts as a success (no handoff, no complaint) where the user did not get what they needed. See [metrics](../../../reference/metrics.md) for how containment hides it.

---
### Deep dive
- **Open question.** I found no study that compares complaint-only review with random sampling for chatbots, so the quiet-failure rate for your bot is something to measure, not assume.
- **Unverified, kept out of the page.** The "96% of unhappy customers do not complain" and "26 to 1" figures reached me only through search summaries of vendor blogs.
- **Modality notes.** Voice call review and web-page agent review are PLANNED, not written.
- **References.** [ASU W. P. Carey, 2006](https://news.wpcarey.asu.edu/20060927-penny-your-thoughts-when-customers-dont-complain) (opened); [Husain and Shankar, 2026](https://hamel.dev/blog/posts/evals-faq/) (opened, partly); [Kaizo, 2026](https://kaizo.com/blog/qa-for-ai-handled-conversations/) (opened); [Langfuse error analysis](https://langfuse.com/blog/2025-08-29-error-analysis-to-evaluate-llm-applications) (opened).
