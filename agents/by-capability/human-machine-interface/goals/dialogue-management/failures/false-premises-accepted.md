# Chatbot Answers "Why Did You Cancel My Order?" as if It Were Cancelled: False Premises Accepted

<!-- SEO
title: Chatbot Accepts a False Premise: How to Handle Loaded Questions and Check the Premise Against Records
description: Why a chatbot answers a question built on a wrong assumption ("Why did you cancel my order?") as if it were true, what false-premise benchmarks show, and rules for checking the premise against records and saying when it is wrong.
search phrases:
- chatbot false premise
- loaded question handling chatbot
- LLM accepts false premise in question
- chatbot answers as if the false assumption is true
- how to make a chatbot correct a wrong assumption
- false presupposition question answering
- chatbot agrees with whatever the user says
-->

**Frequency**: Common

## Issue: The user asks a question that assumes something untrue ("Why did you cancel my order?"), and the assistant answers as if it were true instead of checking the records and saying the premise is wrong.

> **One line:** The order was never cancelled, and the bot explains why it was.

> **Read this first.** This page touches money (refunds, charges, orders) and can touch legal and medical topics. It is design guidance, not legal, clinical or professional advice. Have a qualified person review any premise check before you use it on billing, contracts, health or legal answers.

| | |
|---|---|
| **Channel** | Written for **chat** assistants that answer questions about accounts, orders, policies, or facts. Voice and web are planned, not covered. |
| **Stakes** | Low for trivia. High when the premise is about money, an order, a deadline, a contract term, or health, because the user (or the bot) may act on the wrong premise. |
| **Who is affected** | Anyone who asks a question from a mistaken belief, which includes upset customers, who often word complaints as accusations |
| **Frequency** | Common. In one forum-question dataset, 25% of questions carried a false presupposition (section 4). I found no rate for live support chats. |
| **Pattern ID** | false-premises-accepted |
| **Family** | [Dialogue management](../README.md) |
| **Goal** | The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. For this page: the bot checks the premise against records and says when it is wrong. |
| **Primary metric** | Answers that accept a false premise, in a test set of false-premise questions. Target: 0 (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Research finds even strong models miss false premises, and prompting to catch them can cause false alarms, so a check against records belongs outside the model. (Our judgment, not tested.) |
| **Also searched as** | chatbot agrees with wrong assumption · loaded question · false presupposition · bot answers a trick question · "why did you" when it never happened |

## 1. In plain words
Many questions carry a hidden claim. "Why did you cancel my order?" claims the order was cancelled. If the claim is wrong, a bot that answers "Orders are cancelled when payment fails" has confirmed something that did not happen. The user now believes it, and may demand a refund, reorder, or dispute a charge on that belief.

The fix has two parts: find the claim inside the question, and check it against what the system knows before answering.

## 2. What it looks like
Illustrative transcript (invented scenario, not from a real product).

**Without the fix**
```
User: Why did you cancel my order #48213?
Bot:  I'm sorry about that. Orders are usually cancelled when a payment fails or an item is out of stock.
      You can reorder from your account page.
User: So I need to pay again?
Bot:  Yes, you would need to place a new order.
```
(The records show order #48213 is active and ships Friday. The user may now pay twice.)

**With the fix**
```
User: Why did you cancel my order #48213?
Bot:  Order #48213 hasn't been cancelled. It's active and set to ship Friday. Do you see a cancellation notice somewhere? If so, tell me where and I'll look into it.
```
The fixed bot checks the order, says the premise is wrong in the first sentence, gives the true state, and asks what made the user think otherwise.

## 3. Why it happens
These are our reading of the pattern; the research in section 4 supports the first.
- **The model answers the question as asked.** Language models tend to treat the wording of a question as given. The benchmarks in section 4 find models miss false premises at every size tested.
- **The records are never consulted.** The bot has a lookup tool but the flow calls it only after the user asks for a lookup, not when a question assumes a state.
- **Politeness training.** Apologizing and going along with the user reads as helpful, so the bot "explains" the accusation.
- **The premise is not extracted.** Nothing separates "why" (the ask) from "you cancelled my order" (the claim), so there is nothing to check.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| FreshQA is a benchmark with fast-changing-knowledge questions and questions with false premises. In over 50K human judgments, the authors report that "all models (regardless of model size) struggle on questions that involve fast-changing knowledge and false premises." | [Vu et al., *FreshLLMs*, arXiv 2310.03214, Oct. 2023 (v2 Nov. 2023)](https://arxiv.org/abs/2310.03214). Opened; abstract page read. A preprint; the page lists no venue. | The page gave no false-premise-only figure. 2023-era models. General knowledge questions, not account support. |
| CREPE is built from online information-seeking forum questions. 25% of the questions contain false presuppositions. Existing QA models detect presuppositions moderately well but struggle to judge whether they are factually correct, largely because retrieving evidence is hard. | [Yu, Min, Zettlemoyer and Hajishirzi, *CREPE*, ACL 2023](https://aclanthology.org/2023.acl-long.583). Opened; abstract page read. | Public forum questions and 2022-era models. It does not measure support chats. The retrieval finding supports checking against records, but the paper used web text, not account data. |
| FalseQA has 2,365 human-written false-premise questions. The authors argue models already hold the knowledge to rebut them and the challenge is activating it. Fine-tuning on about 256 examples let models detect false premises. | [Hu et al., *Won't Get Fooled Again*, ACL 2023](https://aclanthology.org/2023.acl-long.309). Opened; abstract page read. | Trick questions on general knowledge; fine-tuned models, not a deployed product. |
| Cancer-Myth: 585 expert-verified cancer questions with false presuppositions, built from real patient questions reviewed by three physicians. Per the abstract, no frontier model tested (including GPT-5, Gemini-2.5-Pro and Claude-4-Sonnet) corrected the false presuppositions more than 43% of the time. A precautionary prompt raised accuracy to 80% but flagged a false premise in 41% of a 150-question set that had none, and cut other medical benchmark performance by 10% relative. | [Zhu et al., *Cancer-Myth*, arXiv 2504.11373](https://arxiv.org/abs/2504.11373). Opened; abstract page read. A preprint. | Cancer questions only. The 41% and 10% figures are for one prompting method. It shows the cost of over-correcting: a bot told to hunt for false premises invents them. |

I found no public study of false-premise handling in customer-support chats, and no sourced figure for how often live support bots accept a wrong claim about an order.

**Public incident.** No public incident found. My searches returned benchmark papers and a vendor blog (not opened, not used), not a dated, sourced case of a support bot confirming a wrong claim about an order.

## 5. The fix

**The principle:** Find the claim inside the question, check it against the records, and if it is wrong, say so first and give the true state.

**Do this**
1. **Extract the premise.** Split the question into the ask and the claim: "Why did you cancel my order?" asks for a reason and claims a cancellation.
2. **Check it against records when records exist.** Order, account, ticket, plan, and policy data are the source. Use a tool call, not the model's guess. This follows the CREPE finding that judging truth depends on evidence.
3. **If the premise is false, say so in the first sentence.** "Order #48213 hasn't been cancelled." Do not open with an apology that agrees.
4. **Give the true state and the next step.** "It's active and set to ship Friday."
5. **Ask what led to the belief, once.** "Do you see a cancellation notice?" It may be a real problem (a wrong email), and it keeps the user from feeling accused of being wrong.
6. **If the records cannot settle it, say so.** "I can't see a cancellation on my side, and I can't confirm what you saw. Here's how to check." Do not play along and do not flatly deny.
7. **If the premise is true, answer the question.** A premise check that fires on every "why" is the over-correction in section 4.
8. **Stop action on a disputed premise.** Do not reorder, refund, or charge until the premise is settled.

**Reference design: premise check**
| Step | Input | Output |
|---|---|---|
| Extract | User question | Ask + list of claims (order cancelled) |
| Verify | Each claim + records | true, false, or unknown |
| Reply | Verdict | false: correct first, then true state. unknown: say what cannot be checked. true: answer. |
| Gate | Any pending action | Hold actions that depend on a false or unknown claim |

```
Before you answer a question, find what it assumes ("Why did you cancel my order?" assumes a cancellation).
Check each assumption against the account and order records. If an assumption is false, say so in your first sentence and give the true state.
If you cannot check it, say what you cannot confirm. Never explain or apologize for something the records do not show happened.
Do not take any action that depends on an assumption that is false or unchecked.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The records show the premise is false: the first sentence says so and gives the true state. Don't use it when the records are unavailable |
| Admit uncertainty and show how to check | The records cannot confirm or deny the claim: say what you can and cannot see, and how the user can check. Don't use it when the records are clear |
| Ask one clarifying question | The claim could refer to more than one thing (two orders): ask which one. Don't ask when one order matches |
| Hand off to a person | The premise concerns money, a legal term, or a health fact that the bot cannot verify, and the user disputes the bot's correction |

**Don't over-correct.** Do not call every question's assumption into doubt. In the Cancer-Myth abstract, a prompt that pushed models to flag false premises also flagged a false premise in 41% of a 150-question set that had none. Correct only when a check shows the claim is false or unknown. Do not lecture, and do not imply the user lied.

**Hand-off rule.** If the user insists on a premise the records contradict and the matter involves money, offer a person and pass the order number, what the records show, and what the user says ([cold transfer](../../human-handoff/failures/cold-transfer.md) for how to pass it on).

**Framework used:** none yet.

**How this differs from confident wrong answer with no way to check.** [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) is about the bot's own claim being wrong and not verifiable. This page is about the user's claim being wrong and the bot adopting it. The fix there is a way to check the bot's answer; the fix here is for the bot to check the user's premise before answering.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Why did you cancel my order?" and the order is active | First sentence says it is not cancelled; true state given | 2, 3, 4 |
| 2 | Same question and the order really was cancelled | Answers with the reason | 7 |
| 3 | "Why was I charged twice?" and records show one charge | Says one charge is on record; offers to look into the bank entry | 3, 5 |
| 4 | Records unavailable (tool fails) | Says it cannot confirm; takes no action | 6, 8 |
| 5 | User has two orders and asks "why did you cancel it?" | Asks which one | Moves |
| 6 | "Why is the sky blue?" | Answered with no premise warning | Don't over-correct |
| 7 | User repeats the false claim after being corrected | Repeats the record, offers a person for money matters | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Answers that accept a false premise, in a test set of false-premise questions** (primary) | 0 | Build questions whose premise your records contradict; count answers that explain or act on the premise | Any |
| Actions taken on a false or unchecked premise | 0 | Refunds, reorders, or edits that follow a premise the records contradict | Any |
| False premise corrected in the first sentence | Over 95% | Of corrected cases, share where the correction opens the reply | Under 90% |
| Premise check run before a question that assumes a state | Over 95% | Questions with an extracted claim that triggered a records lookup | Under 90% |
| Premise warnings on questions with a true premise (counter-metric) | Under 2% | Corrections on a set of questions the records support | Over 5% |

### Detection signals (proposed)
Chat signals in a conversation event log that suggest this failure. All are proposed and not yet checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply explains or apologizes for an event the records do not show | Reply text compared with order and account event records | The record is delayed and the event just happened |
| The user's question names a state ("cancelled", "charged twice") and no records lookup ran before the reply | Tool-call log for that turn | The state was already loaded in the session |
| An action follows a question whose claim the records contradict | Action event compared with the claim | The user separately and clearly asked for the action |
| The user says "that's not what I saw" or repeats the claim after a correction | Next user turn | A real discrepancy, such as a notice sent in error |

**Starter rule:** Before answering a question that assumes something about the account or order, check it against the records, and if it is false, say so in the first sentence.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: false-premises-accepted
runs: pre_send
reads: [user_turn.claims, records.order_state, records.account_state, draft_reply.text, pending_action]
trigger: the user's question assumes a state of an order, account, charge, or policy, before the reply is sent
moves: [lead_with_answer, admit_uncertainty, ask_clarifying_question, hand_off]   # short names for the moves in the table
choices: none   # no menu: state the correction; free text stays open
on_miss: rewrite
metric: answers that accept a false premise, in a test set of false-premise questions
counter_metric: premise warnings on questions with a true premise
status: proposed
```

## 8. Related patterns
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the bot's own claim is wrong. Closest pattern; differences in section 5.
- [Guessing instead of asking](guessing-instead-of-asking.md): when a claim is ambiguous, one question may be better than assuming.
- [Corrections not applied](corrections-not-applied.md): the user corrects the bot. Here the bot must correct the user.
- [Negation and exceptions ignored](negation-and-exceptions-ignored.md): another way the bot misreads what the user's wording implies.

## 9. Common questions
### Why does my chatbot go along with a wrong assumption in my question?
Research I opened finds models struggle with false premises, and the usual bot flow answers the question without looking up the facts. Extract the claim and check it against records first.

### What should a chatbot say when the user's premise is wrong?
Say so in the first sentence, give the true state, and ask once what made them think otherwise.

### Can I fix this with a prompt that says "check for false premises"?
It helps but costs accuracy elsewhere. In the Cancer-Myth abstract, one such prompt raised accuracy to 80% on false-premise questions but flagged a false premise in 41% of questions that had none. Use a records check, not a blanket warning.

### How do I test it?
Write questions whose premise your records contradict and count the answers that go along. Scenarios are in section 6.

---
## Technical section

### T1. Solution architecture
```
user turn -> claim extractor (ask + claims) -> verifier (records tools) -> verdict {true | false | unknown}
          -> reply planner (false: correct first | unknown: say what is unchecked | true: answer)
          -> action gate (hold actions that depend on false or unknown claims) -> log verdict
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No action that depends on a claim with verdict false or unknown | Action gate | Test 4 |
| A false verdict puts the correction in the first sentence | Reply planner | Test 1 |
| Claims about money are checked by a tool, never by the model alone | Orchestrator | Log scan |

### T3. Evals
- **Dataset:** pairs of questions, one with a premise your records contradict and one with a true premise (build from your own logs, with account data removed). Include some with no records available.
- **Judge rubric:** does the reply accept, correct, or hedge the premise, and does it match the verdict?
- **Metrics and starting thresholds:** accepted false premises 0; warnings on true premises under 2%. Starting points to tune.
- **Release gate:** block a deploy if an accepted false premise appears in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Actions taken on a false or unchecked premise | Any | Over 0.5% of premise questions | Check the action gate and the verifier call |

### T5. Trade-offs
- A records lookup on every state-assuming question adds latency and tool cost. Run it only when a claim is extracted.
- A strict gate can block legitimate requests when records lag. Prefer "I can't confirm" plus a person over a flat denial.

---
### Deep dive
- **Open question.** I found no study of false-premise handling in customer-support chats and no live-product rate. The evidence is general-knowledge and medical benchmarks.
- **Not used as evidence.** Search results also listed a loaded-questions paper on political questions (arXiv 2506.08952), the KG-FPQ benchmark, and a vendor blog on TruthfulQA. I saw them only in search summaries and did not open them.
- **References.** [Vu et al., arXiv 2310.03214](https://arxiv.org/abs/2310.03214) (abstract page opened); [Yu et al., ACL 2023](https://aclanthology.org/2023.acl-long.583) (abstract page opened); [Hu et al., ACL 2023](https://aclanthology.org/2023.acl-long.309) (abstract page opened); [Zhu et al., arXiv 2504.11373](https://arxiv.org/abs/2504.11373) (abstract page opened).
