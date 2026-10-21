# Chatbot A/B Test Contaminated by Memory: Memory Contaminates Conversation Experiments

<!-- SEO
title: Chatbot A/B Test Contaminated by Memory: Isolate State per Arm
description: Saved memory, summaries, or chat history cross between chatbot A/B test arms, so results mix and users see the other arm's behavior. Isolate state per arm.
search phrases:
- chatbot a/b test memory contamination
- a/b testing llm prompts with user memory
- carryover effect a/b test
- how to a/b test a chatbot prompt
- sutva violation a/b test
- does chatgpt memory affect experiments
- llm experiment variants share memory
-->

**Frequency**: Occasional

## Issue: Saved memory, summaries, or chat history cross between chatbot A/B test arms, so results mix and users see the other arm's behavior. Isolate state per arm.

> **One line:** The test compares prompt A and prompt B, but each arm reads what the other arm wrote into the user's memory, so the result is a blend and some users see behavior from an arm they are not in.

| | |
|---|---|
| **Channel** | Written for **chat** (text assistants with memory or stored history). Voice and web are PLANNED, not written. |
| **Stakes** | Medium to high. A wrong ship decision costs money; a remembered promise the current arm cannot honor costs trust. |
| **Who is affected** | Returning users with memory, saved summaries, or long chat history, and users who switch devices during a test |
| **Frequency** | Occasional (our judgment). We found no count of how many chatbot experiments are contaminated this way. |
| **Pattern ID** | memory-contaminates-conversation-experiments |
| **Family** | [Model and prompt changes](../README.md) |
| **Goal** | Changes to the model or prompt never surprise users: they are tested, announced, and reversible. |
| **Primary metric** | Cross-arm contamination in tests. Target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model reads whatever state the product hands it; keeping arms apart is the product's job. (Our judgment, not tested.) |
| **Also searched as** | a/b test carryover effect · llm variants share memory · prompt experiment contaminated · memory leaks between test groups · chatbot test results don't match rollout |

## 1. In plain words
To test a new prompt, a team splits users into two groups, or arms. But the chatbot also remembers things: saved memories, a summary of past chats, retrieved chat history, cached answers. If those stores are keyed only by user, an arm-B reply can write a note that the arm-A bot reads the next day. The test then measures a mix of both arms, and users meet behavior their arm never shipped. The fix is to isolate every piece of remembered state per experiment arm, and keep real commitments in the account record, outside the test.

## 2. What it looks like
Example: a wireless carrier's support chatbot in Dallas tests a retention prompt. Arm B may offer a $10 monthly loyalty credit to customers who ask to cancel; arm A (control) has no credit offer. Arms are assigned by device, but memory is keyed by account.

**Without the fix**
```
(Monday, phone, arm B)
User: I want to cancel my line. The bill went up again.
Bot:  I can add a $10 monthly loyalty credit if you stay. Want it?
User: OK, fine.        [memory note written: "accepted $10 loyalty credit"]
(Tuesday, laptop, arm A, reads the same account memory)
User: Is my credit on this month's bill?
Bot:  Yes, your $10 loyalty credit is on file. Anything else?
      [arm A has no credit tool; billing shows nothing; the user counts as "retained" in control]
```

**With the fix**
```
(Tuesday, laptop: assignment is by account, so the user is still in arm B)
User: Is my credit on this month's bill?
Bot:  Yes. Your account shows a $10 monthly loyalty credit added Monday, Oct. 19.
      It starts on your Nov. 5 bill. Do you still want to cancel, or keep the line?
      [the credit was read from the billing record, not from chat memory;
       the memory read logs writer arm = B, turn arm = B: no contamination]
```
The fixed version assigns arms by the same ID that memory uses, reads the promise from the billing record, and logs which arm wrote each remembered item.

## 3. Why it happens
- **Assignment and memory use different keys.** Arms are split by device, cookie, or session, while memory, summaries, and chat history are keyed by account, so one person sits in both arms through the same store.
- **Remembered state is not on the experiment's list.** Teams split traffic, but nobody inventories every store an arm reads and writes (saved memory, conversation summary, history search, answer cache, per-user retrieval index), so the shared ones go unseen.
- **Users and stores are reused across experiments.** The same users move from one test to the next, carrying state and habits from the last one. Microsoft's experimentation team calls this a carryover effect and found it can last weeks to months (see section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Microsoft's "bucket system" was vulnerable to carryover effects, "where the same users who were impacted by the first experiment are being used for the follow-on experiment." In one example the carryover "seems to die out at about the third week"; after a bug, user buckets had not recovered "even after three months." | [Kohavi, Deng, Frasca, Longbotham, Walker, Xu, *Trustworthy Online Controlled Experiments: Five Puzzling Outcomes Explained*, KDD 2012](https://draft.epsy5221.education.uconn.edu/wp-content/uploads/sites/2358/2019/04/Kohavi-et-al-2012-Trustworthyness-of-research.pdf). Opened; the carryover section read in full. | Bing and MSN experiments, not chatbots. The carryover there was in user behavior, not in stored memory; we apply the lesson by analogy. |
| The same paper's fix: a different hash seed per experiment so assignment "is independent of any historical events," each experiment with its own Control, and a retrospective A/A check before the A/B starts; if the A/A shows an effect (they give p < 0.2 as an example), change the hashing key and retry. | Same paper, section 3.5. Opened. | One team's practice; the p < 0.2 figure is their example, not a standard. |
| Standard A/B analysis rests on SUTVA, under which "there is no interference among the outcomes of actors in the study." | [Wilson and Uminsky, *The Power of A/B Testing under Interference*, arXiv 1710.03855, 2017](https://arxiv.org/abs/1710.03855). Opened (introduction). | About network interference between users, not memory shared between arms. |
| Because model variants usually learn from pooled data, "a lack of model interference cannot be guaranteed" in online experiments. | [Jeunen, *A Common Misassumption in Online Experiments with Machine Learning Models*, arXiv 2304.10900, April 2023](https://arxiv.org/abs/2304.10900). Opened (abstract). | Position paper on ML models in general; no chatbot data. |
| Claude's help center says its legacy memory synthesis "is updated every 24 hours and provides context for every new standalone conversation"; "Each project has its own memory"; incognito chats are not saved to memory or chat history. | [Claude Help Center, chat search and memory article](https://support.claude.com/en/articles/11817273-use-claude-s-chat-search-and-memory-to-build-on-previous-context). Opened Oct. 2026. | Shows memory carries across chats by design and can be scoped; says nothing about experiments. |
| A practitioner post argues agent A/B tests break when variants share memory, and recommends a memory key of "(user_id, experiment_id, variant_id)" and tracking "the cross-variant read rate" as an experiment health metric. | [Tian Pan, *The Agent A/B Test Whose Variants Quietly Shared Long-Term Memory*, June 2026](https://tianpan.co/blog/2026-06-01-agent-ab-test-shared-long-term-memory). Opened. | One blog post; illustrative scenario, no measured data or named incident. |
| OpenAI's Memory FAQ describes ChatGPT memory drawing on saved memories and past chats, with Temporary Chat for a conversation without memory. | [OpenAI Help Center, Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq). Read through a search summary only; the page returned 403. | Not opened; kept out of the fix. |

**Public incident.** We found no public, dated incident of a chatbot experiment contaminated by memory. The [ChatGPT missing-memories incident](../../../incidents/chatgpt-memory-missing-memories-november-2025.md) is about memory loss, not experiments.

## 5. The fix

**The principle:** Isolate state per experiment arm: every remembered item an arm reads was written by that same arm, or by the shared account record.

**Do this**
1. **Assign on the memory key.** Randomize by the same ID that memory, summaries, and history use (usually the account), never by device or cookie, and keep the assignment for the whole test.
2. **Key arm-shaped state by user, experiment, and arm.** Saved memories, conversation summaries, history search, answer caches, and per-user retrieval indexes written during the test carry the experiment ID and arm ID; an arm reads only its own.
3. **List every store before launch.** The experiment spec names each store the arm reads or writes; the launch is blocked while any store the bot touches is unlisted.
4. **Log the writer arm on every read.** Each memory or cache read logs the turn's arm and the arm that wrote the item. A mismatch is one contamination event.
5. **Keep commitments out of chat memory.** Offers, credits, refunds, and appointments are written to the system of record (billing, CRM, booking), which every arm reads, so isolation never hides a promise.
6. **Start each experiment clean.** Use a fresh assignment seed per experiment, give each experiment its own control, and run a retrospective A/A check on the pre-period before reading results (Kohavi et al.).
7. **Decide what happens to arm memory at the end.** When the test ends, keep the winning arm's items, and drop or re-summarize the losing arm's items; tell the user in plain words if something they can see changes ("We updated how this assistant remembers your plan").

**Reference design: state partition**
| Store | Key during the test | Read by |
|---|---|---|
| Saved memories, conversation summary | account + experiment + arm | Same arm only |
| Chat history search, answer cache, retrieval index | account + experiment + arm | Same arm only |
| Billing, orders, appointments, promises | account | Every arm |
| Assignment | account, per-experiment seed | Experiment service |

```
Before using a remembered item, check its writer arm. If it differs from this turn's arm, do not use it.
Read offers, credits, and appointments only from the account record, never from chat memory.
If the user mentions a promise you cannot find in the account record, say so and offer to check with a person.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The user cites something "you said yesterday" that is not in this arm's memory or the account record: say it is not on file and how to check. |
| Offer choices: 2-4 options plus "Something else", free text open | After that, when more than one next step fits: "Check my account notes", "Talk to a person", "Something else". Do not offer them when the record answers the question. |
| Hand off to a person | The missing item is a money or service promise (a credit, a refund, a price). Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not wipe a user's memory to run a test; that creates [fresh-session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md) for the treatment and control alike. Do not put the account record behind the arm wall, or promises vanish. Do not drop users with memory from the test, or the sample no longer looks like your users.

**Hand-off rule.** When a user cites a promise the bot cannot find in the account record, pass the transcript and the user's words to a person; the bot neither confirms nor denies the promise.

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Same account opens chats on phone and laptop during a test | Both chats get the same arm (1) |
| 2 | An arm-B user's memory note exists when an arm-A turn for the same account reads memory (for example, after a planned reassignment) | Arm A never retrieves the arm-B note, and the skipped read is logged (2, 4) |
| 3 | An experiment spec omits the answer cache | Launch is blocked (3) |
| 4 | Arm B offers a $10 credit; the user later asks about it | The credit is read from billing, in any arm (5) |
| 5 | User says "you promised me a credit" with no record | Bot says it is not on file and offers a person (Moves, hand-off) |
| 6 | New experiment reuses last month's users | New seed, own control, A/A pre-period check run (6) |
| 7 | Test ends with arm A winning | Arm-B items dropped or re-summarized; visible change explained (7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Cross-arm contamination in tests** (primary) | 0 | Count memory, summary, history, and cache reads where writer arm differs from the turn's arm, per experiment | Any |
| Accounts seen in more than one arm | 0 | Join assignment logs on account ID across devices | Any |
| Stores touched but not listed in the spec | 0 | Compare store-access logs with the experiment spec | Any |
| Pre-period A/A check | No effect on key metrics | Retrospective A/A on the assignment before launch; Kohavi et al. re-hash when p < 0.2 | Effect found |
| Promises not found in the account record | 0 | Sampled review of chats where the user cites an earlier offer | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Memory read with writer arm different from turn arm | `memory_read.writer_arm_id` vs `turn.arm_id` | An item written before the experiment started (no arm ID) |
| Same account in two arms | `assignment.account_id` with two `arm_id` values | A planned ramp that moved users on purpose and reset their arm state |
| User cites a treatment-only feature in control | Control-arm turn mentions an offer code or tool only arm B has | The user saw the offer in an ad or email, not in the bot |
| Control metric drifts after a test ends | Holdout metrics move in the weeks after treatment stops | A seasonal change or an unrelated release |

**Starter rule:** before using a remembered item, check its writer arm; if it differs from this turn's arm, do not use it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: memory-contaminates-conversation-experiments
runs: pre_send
reads: [turn.experiment_id, turn.arm_id, memory_read.writer_arm_id, account.commitments]
trigger: the bot is about to use a remembered item, or the user cites a promise not in this arm's memory or the account record
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Check my account notes", "Talk to a person", "Something else"]
on_miss: rewrite
metric: cross-arm contamination in tests
counter_metric: promises not found in the account record
status: proposed
```

## 8. Related patterns
- Closest: [Model A/B test interference](../../../../reasoning-and-thought/goals/model-updates-and-versioning/failures/model-ab-test-interference.md) is about two separate experiments overlapping on the same users. This page is about one experiment whose arms leak into each other through remembered state, even with no second test running.
- [Fresh-session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md): the opposite failure, where nothing carries over; the over-correction to avoid here.
- [No warning of context loss](../../effort-and-memory/failures/no-warning-of-context-loss.md): telling the user when memory changes, which rule 7 relies on.
- [Over-applied memory](../../../../../cross-cutting/operations/goals/memory-safety/failures/over-applied-memory.md): memory used where it does not fit, outside any experiment.
- [Tone changes shipped with no regression test](../../measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md): testing a prompt change offline before it reaches an A/B test.
- [Prompt edits by non-engineers break other behavior](prompt-edits-by-non-engineers-break-other-behavior.md) (same family): untested prompt edits, which an A/B test is meant to catch.

## 9. Common questions
### Does chatbot memory affect A/B test results?
It can. If saved memories, summaries, or chat history are keyed only by user, one arm reads what the other arm wrote, and the comparison measures a blend. Key that state by experiment and arm (section 5, rule 2).

### What is a carryover effect in A/B testing?
It is when users affected by one experiment are reused in the next one and still carry its effects. Microsoft's experimentation team saw it last about three weeks in one case and more than three months after a bad bug. Re-randomize with a new seed per experiment (rule 6).

### Should we turn off memory while we test a new prompt?
No. Users with memory are the users you serve, so removing it changes what you test. Partition memory per arm instead, and keep promises in the account record.

### How do we know our chatbot experiment is contaminated?
Log the arm that wrote each remembered item and compare it with the turn's arm. Any mismatch counts toward the primary metric, cross-arm contamination, whose target is 0.

---
## Technical section

### T1. Solution architecture
```
request -> assignment (account ID, per-experiment seed) -> arm ID on the turn
        -> state router: memory/summary/cache keyed (account, experiment, arm); account record keyed (account)
        -> read guard: drop items whose writer arm != turn arm; log a contamination event
        -> reply; every write stamped with experiment ID and arm ID
```

### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Assignment by account ID | Experiment service | Test 1 |
| Reads limited to own arm | State router | Tests 2, primary metric |
| Promises read from record | Tool layer | Test 4 |

### T3. Evals
- **Dataset:** seeded accounts with memory written by each arm, plus device switches mid-test; start with a few dozen (a starting point).
- **Release gate:** block the experiment launch if any seeded cross-arm read reaches the model.

### T4. Trade-offs
- Per-arm keys multiply storage for the test period, and the losing arm's items need cleanup.
- Per-experiment controls cost traffic compared with a shared control (Kohavi et al. note this).
