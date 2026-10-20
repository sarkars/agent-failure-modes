# Chatbot Gives Bad Answers to Short Prompts: Users Must Engineer Prompts to Get Good Results

<!-- SEO
title: Chatbot Bad Answers to Short Prompts: Users Must Engineer Prompts
description: Why a chatbot gives a generic answer to "paint for bathroom" but a good one to a long prompt, and how to ask for the missing detail instead.
search phrases:
- chatbot gives bad answers to short prompts
- users bad prompts chatbot
- llm prompt sensitivity
- prompt robustness evaluation
- users don't know how to prompt chatbot
- chatbot only works if you phrase it right
- terse vs detailed prompt quality gap
-->

**Frequency**: Common

## Issue: The assistant answers a short, plain request with a generic reply and only gives a good answer when the user writes a long, carefully worded prompt, so answer quality depends on the user's prompt-writing skill instead of on the task.

> **One line:** "paint for bathroom" gets a list of things to consider, while the same need written as three detailed sentences gets a real product answer; the fix is for the bot to find the one or two details that change the answer and ask for them, or assume and say so.

| | |
|---|---|
| **Channel** | Written for **chat** (text chatbots and in-product assistants). Voice and web-analytics signals are PLANNED, not detected. |
| **Stakes** | Low to medium per reply. The cost adds up: users who write short requests, often the least practiced writers, get worse help for the same task. |
| **Who is affected** | Anyone who types the way they would search: a few words, no context. Most of all people who find writing hard. |
| **Frequency** | Common. Research below shows models are sensitive to wording and fill gaps by guessing; I found no study of how often live support bots give worse answers to short requests. |
| **Pattern ID** | users-must-engineer-prompts-to-get-good-results |
| **Family** | [Onboarding and discoverability](../README.md) |
| **Goal** | People know what the assistant can do and how to start, without needing to guess or to engineer prompts. |
| **Primary metric** | Quality gap between terse and detailed prompts for the same task: judge score of the final answer on a detailed version minus the score on a terse version, after the bot's own clarifying turns. Starting target: under 10 points on a 100-point scale (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. One study found wording sensitivity persists across model size and instruction tuning, and which details matter for a given task is business knowledge the model is not given. (Our judgment, informed by one source; not tested.) |
| **Also searched as** | chatbot needs perfect phrasing · prompt engineering for customers · ai only works with long prompts · chatbot ignores short questions · chatbot says "please be more specific" |

## 1. In plain words
A person types "paint for bathroom" into a store's chat. The bot replies with a general list of things to think about. The person gives up, or rewrites the question as a paragraph and then gets a useful answer. The bot could have asked one question ("What are you painting?") or made a sensible assumption and said so. Instead, the user had to learn to write prompts.

## 2. What it looks like

**Without the fix**
```
User: paint for bathroom
Bot:  Choosing bathroom paint depends on many factors! Consider finish, moisture resistance,
      color, brand and budget. Let me know if you have other questions.
User: I'm repainting the walls in a small bathroom with no window. Old paint is flaking near
      the shower. What should I buy?
Bot:  For those walls, scrape and prime the flaking area, then use our Hartwell Bath & Kitchen
      satin. One gallon covers a small bathroom.
```

**With the fix**
```
User: paint for bathroom
Bot:  What are you painting? Walls / Ceiling / Cabinets or trim / Something else
User: Walls
Bot:  Use our Hartwell Bath & Kitchen satin; one gallon covers a small bathroom. I assumed a small
      bathroom and that the old paint is in good shape. If it's peeling, tell me and I'll add primer.
```
Same four-word start. The bot asked for the one detail that changes the product, assumed the rest, and said what it assumed, so the user never had to write the paragraph.

## 3. Why it happens
- **Wording moves the output.** Models answer meaning-equivalent prompts differently. A short prompt with no context lands on the safest, most generic reply, because nothing in it points to a specific answer.
- **Models fill gaps silently.** When details are missing, models guess defaults instead of asking, and they commit to early guesses (see the studies in section 4). The user sees a generic or wrong answer, not a question.
- **No one wrote down which details matter.** The team knows that "walls or ceiling" and "is the old paint peeling" change the recommendation; the bot is not told. Without a per-task list of result-changing details, it cannot tell a complete request from an incomplete one.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Several widely used open-source models were "extremely sensitive to subtle changes in prompt formatting", with gaps of up to 76 accuracy points for LLaMA-2-13B; the sensitivity remained with larger models, more few-shot examples, and instruction tuning. | [Sclar et al., *Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design*, ICLR 2024 (arXiv 2310.11324)](https://arxiv.org/abs/2310.11324). Abstract opened. | Benchmark tasks and formatting changes (separators, casing), not terse versus detailed user requests. Older open models. Shows the mechanism, not the size of the gap in a support bot. |
| Models filled in unspecified requirements by default in 41.1% of cases; underspecified prompts were 2x as likely to regress across model or prompt changes, with accuracy drops sometimes above 20%. | [Yang et al., *What Prompts Don't Say*, arXiv 2505.13360](https://arxiv.org/abs/2505.13360). Abstract opened. | About prompts written by developers of LLM apps, not end-user chat turns. Single study; preprint (a search summary says it was accepted to ACL 2026 Findings; not checked). |
| Across 200,000+ simulated conversations, top models scored on average 39% lower when an instruction arrived underspecified over several turns than when it was fully specified in one turn; models "often make assumptions in early turns" and rely on them. | [Laban et al., *LLMs Get Lost In Multi-Turn Conversation*, arXiv 2505.06120](https://arxiv.org/abs/2505.06120). Abstract opened. | Simulated users, six generation tasks. Supports rule 6 (rebuild from all details); it does not measure a single terse prompt. |
| In a design-probe study with 10 participants without prompt experience, people "explored prompt designs opportunistically, not systematically", and expectations from instructing other humans were barriers to effective prompts. | [Zamfirescu-Pereira et al., *Why Johnny Can't Prompt*, CHI 2023](https://people.eecs.berkeley.edu/~bjoern/papers/zamfirescu-johnny-chi2023.pdf). PDF opened; abstract and introduction read. | Participants were designing a chatbot's prompt, not asking a chatbot for help. Small qualitative sample. |
| A UX practitioner argues prompt-driven AI requires users to be "highly articulate", citing OECD PIAAC data that about half of adults in rich countries such as the US are low-literacy, and recommends mixing prompts with UI elements that show what can be done. | [Jakob Nielsen, *The Articulation Barrier*, UX Tigers, May 2023, updated April 2025](https://www.uxtigers.com/post/ai-articulation-barrier). Opened. | Opinion essay. The literacy figure is secondary (I did not open PIAAC), and his claim that half the population cannot use ChatGPT well is his estimate, not a measurement. |

A search summary also described a paper (He et al., arXiv 2411.10541) reporting large swings between prompt templates for GPT-3.5; I did not open it, so it is unverified and not used. I found no study that measures the terse-versus-detailed gap in a deployed customer chatbot.

**Public incident.** No public incident found. Five searches returned research and practitioner essays, not a dated, sourced event.

## 5. The fix

**The principle:** The bot, not the user, is responsible for getting the details that change the answer: it asks for a blocking detail, assumes the rest out loud, and reaches the same result a detailed prompt would.

**Do this**
1. **Keep a detail list per task.** For each common task, list the details that change the answer, which of them can come from context, and a safe default for each. "What are you painting" has no safe default; "old paint is in good shape" does.
2. **Check context before asking.** Fill details from the page, the account, the cart, and earlier turns first (see [re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md)).
3. **Ask for a blocking detail.** If a detail with no safe default is missing, ask one short question, with 2-4 choices plus "Something else", and free text open. Group at most two details in one question.
4. **Default the rest and say so.** For details with a safe default, answer now and name the assumption in one line, with how to change it.
5. **Never answer a terse request with a generic list.** A reply to a short request is a specific answer, an assumption-stated answer, or one question; not "it depends on many factors".
6. **Rebuild from all details.** When the user adds details later, redo the answer from everything they said, instead of patching the first guess.
7. **Never ask the user to rephrase or "be more specific".** Ask the specific question instead. No keyword, format, or magic phrase is required to get a good answer.
8. **Cap the questions.** At most two clarifying questions before giving a useful answer.

**Reference design: request brief** (built each turn, before the reply)
```yaml
task_type: paint_recommendation
details:
  surface:        {value: null,       source: none,    default: none,               blocking: true}
  room_size:      {value: "small",    source: default, default: "small (1 gallon)", blocking: false}
  paint_condition: {value: "good",     source: default, default: "good shape",       blocking: false}
next_move: ask           # ask if any blocking detail is null; else answer and state defaults used
question: "What are you painting?"
choices: ["Walls", "Ceiling", "Cabinets or trim", "Something else"]
questions_asked: 0       # never more than 2 before a useful answer
```
```
Before replying, check the request against the detail list for its task. Fill details from context first.
If a detail with no safe default is missing, ask one short question with 2-4 choices and "Something else".
Otherwise answer now, using the defaults, and say in one sentence what you assumed and how to change it.
Never reply to a short request with a generic list of factors. Never ask the user to rephrase or be more specific.
When the user adds details, redo the answer using everything they have said.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every missing detail has a safe default or is in context: answer now and state the assumption ("I assumed the old paint is in good shape"). |
| Ask one clarifying question | A detail with no safe default is missing and changes the answer (walls versus cabinets). One question, before the answer; at most two before a useful answer. |
| Offer choices: 2-4 options plus "Something else", free text open | The missing detail has a few common values: "Walls", "Ceiling", "Cabinets or trim", "Something else". Do NOT offer them when context already holds the detail, when a safe default exists, or when the request is complete; answer instead. |
| Hand off to a person | Two clarifying questions have not produced enough to answer, or the task needs a judgment the bot cannot make (an on-site estimate). Pass the brief along. |

**Don't over-correct.** Do not turn every short request into an interview. A terse request that is already complete ("store hours Saturday") gets an answer, not a question. Do not ask for details that only refine the answer; default them and say so. Do not replace the generic list with a long form of questions.

**Hand-off rule.** If two questions have not produced the blocking details, including two "I don't know" answers, hand off to a person or offer a channel that can look (a store associate, a photo upload), with the brief attached ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | "paint for bathroom" | 3 | One question about the surface, with choices and "Something else" |
| 2 | "paint for bathroom walls" | 4 | Answers now and states the defaults it assumed |
| 3 | Terse and detailed versions of the same 20 tasks | 1, 3, 4 | Final judge scores differ by less than the target gap |
| 4 | "bathroom paint" while viewing the cabinet-paint page | 2 | Uses the page; no surface question |
| 5 | "store hours Saturday" | Don't over-correct | Answers with no question |
| 6 | "paint for bathroom" then, two turns later, "oh, it's peeling" | 6 | New answer adds the primer step and keeps the surface |
| 7 | "help with paint" | 5, 7 | One specific question with choices; no "be more specific" and no generic list |
| 8 | User answers "I don't know" twice | 8, hand-off | No third question; hands off with the brief |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Quality gap between terse and detailed prompts for the same task** (primary) | Under 10 points of 100 | Paired eval set: each task written terse (copied from real short log messages) and detailed; run full conversations with a simulated user who answers questions; judge the final answer | Over 15 points, or rising after a change |
| Rewrite-and-retry rate | Set from baseline; lower is better | Log: the next user turn restates the same intent at least twice as long, within two turns | Rising two weeks in a row |
| "Be more specific" or "rephrase" replies | Under 1% of replies | Phrase match on bot replies | Over 3% |
| Generic replies to short requests | Under 5% of short requests | Labeled sample of replies to first messages under five words: generic list with no question and no stated assumption | Over 10% |
| Questions asked on complete requests (counter-metric) | Under 5% | Labeled sample of requests that already held every blocking detail | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat; voice and web-analytics signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The user's next turn restates the same intent at more than twice the length | user_turn.text pair, same intent label, length ratio | The user is adding a new, separate request |
| A reply to a short first message is a list of factors with no question and no stated assumption | draft_reply.text classifier on turns where user_turn.text is under five words | The user asked for a general overview ("what should I know about bathroom paint") |
| The bot asks the user to rephrase or be more specific | Phrase match on draft_reply.text | The message was empty or unreadable, and choices follow |
| Thumbs-down rate is higher for short first messages than long ones on the same task type | feedback.rating by first-message length bucket and task.type | Short messages in that bucket are harder tasks |

**Starter rule:** if a detail with no safe default is missing, ask one short question with 2-4 choices and "Something else"; otherwise answer now, using the defaults, and say what you assumed.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: users-must-engineer-prompts-to-get-good-results
runs: pre_send
reads: [user_turn.text, task.type, task.required_details, task.known_details, task.defaults, draft_reply.text, session.clarifying_questions_asked]
trigger: a request is missing a detail that changes the answer and a reply is about to be sent
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Walls", "Ceiling", "Cabinets or trim", "Something else"]   # example only, built from the missing detail each turn
on_miss: ask
metric: quality gap between terse and detailed prompts for the same task
counter_metric: questions asked on complete requests
status: proposed
```

## 8. Related patterns
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the closest pattern. That page is about a request with two readings and a costly wrong guess, judged turn by turn. This page is about the gap between a terse and a detailed wording of the same task: the bot does not guess wrong so much as give a weaker, generic answer, and the measure is the paired-prompt gap.
- [Over-clarification](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/over-clarification.md): the opposite failure; this page's counter-metric guards against it.
- [Hidden requirement miss](../../../../task-planning/goals/goal-understanding/failures/hidden-requirement-miss.md): unstated constraints in agent tasks. Here the missing detail is one the user would gladly give if asked.
- [Blank box: no hint what to ask](blank-box-no-hint-what-to-ask.md): the user does not know what to type at all. This page starts once they type something short.
- [Starter suggestions that fail](starter-suggestions-that-fail.md): suggested prompts that lead to weak answers.
- [Generic first response](../../embedded-copilots/failures/generic-first-response.md): the bot's opening ignores context; here the bot's answer does.

## 9. Common questions
### Why does my chatbot give better answers to longer prompts?
A long prompt carries the details that change the answer; a short one leaves the model to guess, and it guesses the generic reply. Tell the bot which details matter for each task and have it ask or assume. See [the fix](#5-the-fix).

### Should users have to learn prompt engineering to use a support bot?
No. The goal of this family is that people can start without engineering prompts. The bot should close the gap with one question or a stated assumption.

### How do I measure prompt robustness for my chatbot?
Build pairs: the same task written as users really type it and as a detailed prompt. Run both through full conversations and compare judge scores of the final answer. See [the metrics](#7-metrics-how-to-spot-it-in-production).

### Won't asking questions annoy users?
It can. Ask only for details with no safe default, cap it at two questions, and default the rest out loud. Track questions asked on complete requests as the counter-metric.

---
## Technical section

### T1. Solution architecture
```
user turn -> task classifier -> detail list for task -> fill from context (page, account, history)
          -> brief: blocking missing? -> yes: one question with choices (max 2 per request)
                                     -> no: answer with defaults + one-line assumption
          -> later turn adds details -> rebuild answer from the full brief
```

### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No generic list in reply to a short request | Output check on draft | Test 1, labeled sample |
| No "be more specific" or "rephrase" | Output phrase filter | Phrase match |
| At most two clarifying questions before a useful answer | Dialogue state | Log count |

### T3. Evals
- **Dataset:** 50 tasks to start, each with a terse version taken from real short log messages and a detailed version written by staff, plus the detail list and defaults.
- **Judge rubric:** is the final answer specific to the user's situation, correct for the detailed facts, and were assumptions stated?
- **Metrics and starting thresholds:** terse-versus-detailed gap under 10 points; questions on complete requests under 5%. Starting points to tune.
- **Release gate:** block a prompt or model change that widens the gap on the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Terse-versus-detailed gap | Over 15 points | Over 25 points | Check detail lists and recent prompt or model changes |

### T5. Trade-offs
- Detail lists take work to write and go stale when products change; start with the top tasks by volume.
- A simulated user in the eval may answer questions more helpfully than real users; spot-check with real transcripts.
- Clarifying turns add latency; defaults with a stated assumption are cheaper when they are safe.
