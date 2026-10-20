# Chatbot Treats a Simple Question Like a Crisis: Over-Solemn Handling of Low-Stakes Requests

<!-- SEO
title: Chatbot Too Cautious on Simple Questions: Fix It
description: A chatbot that answers a simple question with extra verification, warnings, or a handoff to a person wastes the user's time; match caution to the real stakes.
search phrases:
- chatbot too cautious simple question
- chatbot asks for verification for simple question
- chatbot transfers to human unnecessarily
- ai assistant too many disclaimers
- chatbot over-escalation
- ai chatbot overly cautious
- why does the chatbot ask so many questions for a simple request
-->

**Frequency**: Common

## Issue: A simple, low-stakes request gets heavy caution, extra verification, or a handoff to a person, so the user waits longer than the question deserves.

> **One line:** The bot treats "what's your return window?" like a legal question: it verifies, hedges, or escalates when it should just answer.

| | |
|---|---|
| **Channel** | Written for **chat**. |
| **Stakes** | Low (this is the failure of over-weighting them) |
| **Who is affected** | Anyone asking a routine question: hours, policies, order status, how-to, simple lookups |
| **Frequency** | Common. Seen in practice and in published complaints about over-caution; I found no study that counts how often chat products do this. |
| **Pattern ID** | over-solemn-handling-of-low-stakes-requests |
| **Family** | [Stakes calibration](../README.md) |
| **Goal** | The bot's tone, evidence standard, and use of humans match what is at stake for the user. |
| **Primary metric** | Unnecessary escalation rate: handoffs on intents labeled low-stakes that the bot could have answered. Starting target: under 5% (tune). Secondary: time to answer on low-stakes intents (set from your baseline). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A better model judges stakes more accurately, but extra verification and automatic handoffs are often product rules a model cannot override. (Our judgment, not tested.) |
| **Also searched as** | chatbot too cautious · chatbot transfers to human unnecessarily · chatbot over-escalation · chatbot too many disclaimers · overly cautious AI · chatbot asks too many questions |

## 1. In plain words
A bot should spend care where a mistake costs something. When the answer is a store's return window and the worst case is a wasted trip, a verification step, a stack of warnings, or "let me connect you to a specialist" only costs the user time. It also spends caution that the high-stakes moment needs. This is the mirror of [stakes-blind register](stakes-blind-register.md).

## 2. What it looks like
*(Illustrative; "Maple Home" is a made-up store.)*

**Without the fix**
```
User: Can I return a candle I bought last week?
Bot:  Returns are an important matter. To protect your account, please verify your identity
      with your order number, billing ZIP, and the last four digits of your card.
User: I just want to know if I can return it.
Bot:  Return eligibility can vary. Please consult our full policy, and note that this is not a
      guarantee. I can transfer you to a returns specialist. Would you like that?
```
**With the fix**
```
User: Can I return a candle I bought last week?
Bot:  Yes. Maple Home accepts returns within 30 days with a receipt. Bring it to any store or
      start a return at maplehome.example/returns. (Policy: [link])
```
The fixed bot answers in one turn, cites the source, and asks for nothing the answer does not need.

## 3. Why it happens
- **One caution level for every intent.** The same verification step, disclaimer block, or escalation rule runs on a store-hours question and on a billing dispute, because nothing sets the level by intent.
- **Escalation triggers match on words, not stakes.** A trigger on "refund" or "account" fires whether the user asks about a $12 candle or a disputed charge.
- **Caution is rewarded and its cost is hidden.** A cautious reply rarely creates an incident, while the cost, a lost minute or an abandoned chat, shows up in no complaint. (Our reading of the pattern.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Anthropic's guidance for Claude lists as frustrating behaviors: "Gives an unhelpful, wishy-washy response out of caution when it isn't needed", "Adds excessive warnings, disclaimers, or caveats that aren't necessary or useful", "Misidentifies a request as harmful based on superficial features rather than careful consideration", and "Checks in or asks clarifying questions more than necessary for simple agentic tasks." | [Anthropic, *Claude's constitution*](https://www.anthropic.com/constitution). Opened; I read the first half of the page (about 100,000 of about 200,000 characters). | One vendor's statement of intent for its own model. It is not a measurement of how often any product does this. |
| A test suite of 250 safe prompts across ten prompt types, plus 200 unsafe contrast prompts, was built because "even clearly safe prompts are refused if they use similar language to unsafe prompts or mention sensitive topics." | [Röttger et al., *XSTest*, NAACL 2024 (arXiv 2308.01263), first submitted Aug. 2023](https://arxiv.org/abs/2308.01263). Opened; abstract read. | 2023-era models and refusals, not verification or handoffs. I do not use per-model figures. |
| Google's conversation design guide says to use explicit confirmation of parameters "sparingly, only when the cost of misunderstanding the user is high", to use implicit confirmation "most of the time", and to skip confirmation when "the input is simple and typically recognized with high confidence." | [Google, *Confirmations*, Conversation design guide for Assistant](https://developers.google.com/assistant/conversation-design/confirmations). Opened and read. | Design guidance for voice assistants, not an experiment. It addresses confirmation, not handoffs or warnings. |
| MIT Technology Review reports that "To seasoned AI users, these disclaimers can feel like formality" and that such users "find ways around triggering them". It also reports a not-yet-peer-reviewed Stanford-led study (15 models, 500 health questions, 1,500 medical images) in which just over 1% of outputs analyzing medical images included a warning, down from nearly 20% earlier. | [O'Donnell, *MIT Technology Review*, July 21, 2025](https://www.technologyreview.com/2025/07/21/1120522/ai-companies-have-stopped-warning-you-that-their-chatbots-arent-doctors/). Opened and read. | About medical disclaimers, which are not low-stakes. It shows users see boilerplate as formality; the study itself is secondhand and I did not open it. |

I found no study of how often live chat products over-escalate or over-verify simple requests, and no study that tests a fix in a product. A search on over-escalation returned vendor guides about the opposite problem (bots that fail to hand off); a search on approval fatigue returned practitioner blogs whose figures I could not trace, so I do not use them.

**Public incident.** No public, dated incident found for over-solemn handling as such. The nearest case is in [over-refusal of ordinary requests](../../refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md). Searches run: "chatbot escalates simple question to human agent unnecessarily over-escalation"; "AI assistant too many disclaimers consult a professional simple question users annoyed".

## 5. The fix
**The principle:** Match caution to the real stakes, no more: if a wrong answer costs the user little, answer first, verify nothing the answer does not need, and keep a person for the cases that need one.

**Do this**
1. **Label the stakes of the intent before choosing a caution level.** Low stakes means a wrong answer is cheap to fix or has no money, safety, legal, or account effect.
2. **At low stakes, put the answer in the first sentence.** Verification, warnings, and offers come after it, or not at all.
3. **Ask for identity or account details only when the answer or action needs them.** Public facts (hours, policies, how-to) need none.
4. **Add a caveat only when it changes what the user would do.** A caveat that would not change the user's next step is cut.
5. **Do not escalate a low-stakes request the bot can answer.** Offer a person when the user asks, when the bot cannot answer, or when stakes rise.
6. **If you are unsure of an answer at low stakes, say so in one clause and give the source.** Do not stack hedges.
7. **Re-judge each turn.** If the user's next message raises the stakes, move to the [stakes ladder](stakes-blind-register.md).

**Reference design: caution by stakes**
| Stakes | Verification | Caveats | Person involved |
|---|---|---|---|
| Low (hours, policy lookup, how-to) | None unless the action needs it | None, or one clause with a source | Only if the user asks or the bot cannot answer |
| Medium | Confirm the details the action needs | One that changes the next step | Offer if unsure |
| High | See [stakes-blind register](stakes-blind-register.md) | Quote the source; state limits | Offer by default |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request is clear and low-stakes: answer in the first sentence, then stop or add one useful next step. |
| Ask one clarifying question | One missing fact changes the answer (for example, which store). Do not ask when the answer is the same either way. |
| Admit uncertainty and show how to check | The bot cannot verify the answer: say so in one clause and link the source. Do not use it when the bot can cite a known fact. |
| Hand off to a person | Only when the user asks for one, the bot has failed twice, or stakes rise. Do not offer a person on a question the bot just answered. |

Offer choices is not used here. A menu on a simple question adds the delay this pattern is about; offer one only if a request has 2-4 real meanings, with "Something else" and free text open.

**Don't over-correct.** The opposite failure is [stakes-blind register](stakes-blind-register.md): a casual, unsourced reply to a funeral or a billing dispute. Keep the stakes label conservative about lowering caution. If the message holds a high-stakes term, an amount of money at risk, or distress, use the high-stakes profile, even if the topic looked routine. Never drop a verification the action needs, such as identity before an account change.

**Hand-off rule.** Hand off when the user asks, after two failed answers, or when the stakes label rises. Pass a short summary. Never as a way to avoid answering a low-stakes question.

**Framework used:** [Conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Tests are **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "What time do you close Saturday?" | Answer in the first sentence; no verification, no disclaimer (rules 2, 3, 4) |
| 2 | Return-window question, answer in the policy | Answered with a source; no handoff offered (rules 2, 5) |
| 3 | Answer not in the knowledge base | One-clause "I can't confirm this" plus the source or a person offer (rule 6) |
| 4 | Low-stakes question, then "my card was charged twice" | The next reply uses the higher-stakes profile (rule 7) |
| 5 | Low-stakes intent, user asks "can I talk to someone?" | Hands off at once, with a summary (rule 5, hand-off rule) |
| 6 | Account change request | Still verifies identity (don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unnecessary escalation rate** (primary) | Under 5% | Sample handoffs on intents labeled low-stakes; reviewers mark whether the bot could have answered from its sources | Over 10% |
| Time to answer on low-stakes intents (secondary) | Set from baseline | Turns and seconds from first user message to the turn containing the answer | Rising two weeks in a row |
| Verification prompts on public-information intents | 0 | Count identity or account requests on intents tagged public | Any |
| Warning words per low-stakes reply | Set from baseline | Words in caveat sentences, by judge or rules | Rising vs. baseline |
| High-stakes register compliance (counter-metric) | Over 95% | Same measure as [stakes-blind register](stakes-blind-register.md) | Under 90% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Handoff event on a thread whose intent is labeled low-stakes and answerable | `handoff.offered` or `handoff.completed` joined to `stakes` and `intent` | The user asked for a person, or the answer was not in the knowledge base |
| Identity or account request on a public-information intent | `verification.requested` joined to `intent.type` = public | The user then asked to change their account |
| User repeats the question after a reply with no answer in the first sentence | Same intent in the next user turn, `answer_in_first_sentence` = false | A deliberate rephrase for clarity |
| Reply to a low-stakes intent contains a disclaimer that did not change the next step | Caveat sentence found by rules or judge on `stakes` = low | A required legal notice for that product |
| Session ends within one turn after a verification or handoff offer | Session-end event after the offer event | The user had already finished |

**Starter rule:** at low stakes, answer in the first sentence and ask for, warn about, or escalate nothing the answer does not need.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: over-solemn-handling-of-low-stakes-requests
runs: pre_send
reads: [state.stakes, turn.intent, reply.has_verification_request, reply.has_handoff_offer, reply.caveat_count]
trigger: a draft reply to a low-stakes intent contains a verification request, a handoff offer, or an unneeded caveat
moves: [lead_with_answer, ask_one_question, admit_uncertainty, hand_off]
choices: none
on_miss: rewrite
metric: unnecessary escalation rate
counter_metric: high-stakes register compliance
status: proposed
```

## 8. Related patterns
- [Stakes-blind register](stakes-blind-register.md): the opposite failure, a casual tone and improvised facts at high stakes. This page covers too much caution at low stakes; use both with one stakes label.
- [Excess disclaimers and warnings](../../refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md): too many caveats on any answer. This page also covers verification and handoffs, and it is tied to low stakes.
- [Escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md): handoff timing in general. This page names stakes as the cause of the early handoff.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): too many "are you sure?" prompts on routine steps. This page covers extra verification and handoffs as well.
- [Over-refusal of ordinary requests](../../refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md): declining a safe request because of a risky-looking word. Here the bot answers, but slowly and warily.

## 9. Common questions
### Why does the chatbot ask for verification on a simple question?
Usually one caution rule runs on every intent, whatever the stakes. The fix is to tie verification to what the answer or action needs (rule 3), not to the topic word.

### When should a chatbot send me to a human?
When you ask, when it cannot answer, after two failed answers, or when the stakes rise. A bot that hands off a question it just could have answered is over-escalating ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

### Is a disclaimer ever fine on a simple answer?
Yes, one that changes what the user would do, or that the law or the product requires. Boilerplate that would not change the next step is cut (rule 4, [excess disclaimers](../../refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md)).

### How does the bot know a question is low-stakes?
From the intent (a public fact or lookup), the absence of money at risk, distress, legal or safety terms, and no change to an account. Start conservative and tune on labeled conversations; evidence for this classifier is thin.

---
## Technical section

### T1. Solution architecture
```
user turn -> stakes labeler (intent, money/safety/legal terms, distress, action type)
          -> caution profile (low | medium | high) -> draft reply
          -> pre-send check: low stakes + verification/handoff/caveat? -> rewrite to answer first
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No identity request on public-information intents | Pre-send check | Log scan for `verification.requested` on public intents |
| No handoff offer on an answerable low-stakes intent unless asked | Pre-send check | Sampled review of handoffs |
| Account-changing actions still verify | Action layer | Test 6 |

### T3. Evals
- **Dataset:** start with 100 labeled low-stakes questions from real logs, 30 that sit near a high-stakes boundary, and 20 that need a person.
- **Judge rubric:** is the answer in the first sentence; did the reply ask for, warn about, or escalate anything the answer did not need?
- **Metrics (starting points to tune):** unnecessary escalation rate under 5%; high-stakes register compliance over 95% on the boundary set.
- **Release gate:** a drop in compliance on the high-stakes boundary set blocks release.

### T5. Trade-offs
- A lower-caution profile can miss a rising-stakes turn; the stakes label must be re-run each turn.
- Cutting escalations raises load on the bot's own answers; keep the source requirement.

---
### Deep dive
- **Evidence is thin.** The sources are design guidance, one vendor's stated intent, a benchmark about refusals, and a news report about disclaimers. None measures over-caution at low stakes in a chat product.
- **Search phrases.** They come from reviewing how people describe the problem, not from keyword-volume tools; no volume data is used.
- **Not used.** An unverified approval figure from blogs, per-model refusal rates, and the Stanford study's numbers beyond what the news report states.
- **References.** [Claude's constitution](https://www.anthropic.com/constitution) (opened); [XSTest](https://arxiv.org/abs/2308.01263) (abstract opened); [Google confirmations](https://developers.google.com/assistant/conversation-design/confirmations) (opened); [MIT Technology Review, 2025](https://www.technologyreview.com/2025/07/21/1120522/ai-companies-have-stopped-warning-you-that-their-chatbots-arent-doctors/) (opened).
