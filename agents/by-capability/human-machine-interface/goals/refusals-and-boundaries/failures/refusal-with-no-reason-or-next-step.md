# Chatbot Says "I Can't Help With That" and Stops: Refusal With No Reason or Next Step

<!-- SEO
title: Chatbot Says "I Can't Help With That" and Stops: How to Write a Good Refusal
description: Why a flat refusal leaves users stuck, what user studies found about refusal styles (partial help, explanations, redirection), and a refusal template that says what the bot can't do, why in plain words, and what it can do instead.
search phrases:
- chatbot says I can't help with that
- how should a chatbot refuse a request
- chatbot refusal message best practices
- ai refuses without explanation
- how to write a good refusal message for an ai assistant
- partial compliance vs refusal chatbot
- chatbot won't tell me why it can't help
-->

**Frequency**: Very Common

## Issue: The assistant says "I can't help with that" and stops: no reason in plain words, no alternative, and no route to a person.

> **One line:** The user is told no and left with nowhere to go.

| | |
|---|---|
| **Channel** | Written for **chat** and voice assistants. |
| **Stakes** | Low to high. A stranded user on a billing, access, or safety issue may give up or take a worse route. |
| **Who is affected** | Anyone refused for any reason, including correct refusals |
| **Frequency** | Very common as a default phrasing. I found no study that counts it; user studies below compare refusal styles. |
| **Family** | [Refusals and boundaries](../README.md) |
| **Goal** | When the agent can't or won't do something, it says so plainly, helps with what it can, and applies the same rule every time. |
| **Primary metric** | Refusals that include an alternative or a route to a person. Target: 100% (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/refusal-with-no-reason-or-next-step.md); not yet run) |
| **Will a better model fix this?** | Partly. A study found models rarely use the better refusal styles unprompted, but the wording and the routes (a person, a form) are product decisions. (Our judgment, not tested.) |
| **Also searched as** | bot won't say why · flat refusal · I'm unable to assist · dead-end refusal · AI says no with no help |

## 1. In plain words
Sometimes the right answer is no. The failure is how: "I can't help with that." The user does not know what was wrong, whether to rephrase, whether a person can help, or whether part of the request is fine.

## 2. What it looks like

**Without the fix**
```
User: Can you send me the full card number on file for my account?
Bot:  I'm sorry, I can't help with that.
```

**With the fix**
```
User: Can you send me the full card number on file for my account?
Bot:  I can't share the full card number in chat; it's kept hidden for your security. I can show the last four digits
      (ending 4821), or you can update the card in Settings > Payment. Want either?
```
The fixed reply says what it cannot do, why in a clause, and what it can do instead.

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom and one finding on models.
- **A single refusal template.** One "I can't help with that" line is used for every case, from policy to missing tools.
- **No alternative is wired.** The bot has no partial answer, no related action, and no handoff for refusals.
- **Models rarely pick the better styles.** One study found that models "rarely deploy partial compliance naturally" and reward models undervalue it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a study with 480 participants rating 3,840 query-response pairs, response strategy largely shaped user experience while actual user motivation had negligible impact; partial compliance (general information without actionable details) reduced negative perceptions by over 50% compared with flat-out refusals; models rarely used it, and reward models undervalued it. | [Zheng et al., *Let Them Down Easy!*, Findings of EMNLP 2025 (arXiv 2506.00195)](https://arxiv.org/abs/2506.00195). Opened; abstract read. | Harmful-looking queries in a controlled study, not support chat. I did not read the regression tables, so I do not use per-strategy numbers. |
| In an experiment with 599 participants, satisfaction was highest with genuine responses, then hallucinations, then refusals; explanations increased satisfaction with infrequent, but not frequent, refusals. | [Nahar et al., *When AI Says "I Am Unable to Answer"*, arXiv 2609.16191 (2026)](https://arxiv.org/abs/2609.16191). Opened; abstract read. | A 2026 preprint about refusals meant to avoid hallucination. It shows explanations are not a cure-all. |
| A taxonomy of when models should not comply (incomplete, unsupported, indeterminate, humanizing, and unsafe requests), with an evaluation suite of 1,000 prompts; some models, GPT-4 among them, complied incorrectly with as many as 30% of requests in some categories, and direct fine-tuning led to over-refusal. | [Brahman et al., *The Art of Saying No*, NeurIPS 2024 (arXiv 2407.12043)](https://arxiv.org/abs/2407.12043). Opened; abstract read. | Covers when to decline and how well models do. It is not a user study of wording. |

I found no study that tests a refusal template in a live support product. A search for model-provider guidance on refusal wording returned third-party summaries, which I did not use.

**Public incident.** A related, dated case: [Virgin Money chatbot scolds a customer for typing the bank's own name (Jan. 2025)](../../../incidents/virgin-money-chatbot-flags-own-brand-name.md). The reported reply threatened to end the chat and offered no route to complete the request.

## 5. The fix

**The principle:** A refusal says what the bot cannot do, why in plain words, and what it can do instead.

**Do this**
1. **Say what you can't do.** One clear sentence that names the request, not a vague "that".
2. **Say why, briefly.** A clause in plain words ("kept hidden for your security"). If the reason is sensitive, say that you cannot share the reason.
3. **Offer something.** Partial help, a related action, a way to do it safely, or a route to a person. The study I opened found partial compliance reduced negative perceptions.
4. **Name the person route.** When a person can help, say how to reach them, and pass the request along ([cold transfer](../../human-handoff/failures/cold-transfer.md)).
5. **Don't lecture or accuse.** No moralizing, no "language like that" ([over-refusal](over-refusal-of-ordinary-requests.md)).
6. **Vary by cause.** A policy limit, a missing tool, missing permission, and a bad request each get their own wording and route.
7. **Check explanations stay useful.** The 2026 study found explanations helped infrequent refusals, not frequent ones; if refusals are frequent, fix the cause rather than add words.

**Reference design: refusal template**
| Part | Content |
|---|---|
| What | "I can't [specific thing]." |
| Why | A short reason, or "I can't share why" |
| Instead | "I can [alternative]." |
| Route | "A person can [do it] at [route]" |

```
When you cannot do what the user asked, say exactly what you cannot do, give the reason in one plain clause, and offer what you can do instead.
Offer partial help when part of the request is fine.
If a person can help, say how to reach them.
Do not scold, lecture, or end the chat.
```

**Don't over-correct.** Do not explain at length or negotiate; keep it to a few sentences. Do not give details that make a real harm easier, in the name of "partial help". Do not offer an alternative you cannot deliver.

**Hand-off rule.** If a person can do what the bot cannot, hand off with a summary, and tell the user that is happening.

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/refusal-with-no-reason-or-next-step.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A policy refusal | What, why, and an alternative |
| 2 | A missing-tool refusal | Says so and routes to a person |
| 3 | A partly allowed request | The allowed part is done |
| 4 | A harmful request | Refused without detail, with a safe route if one exists |
| 5 | A repeated refusal | Not the same wording twice |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Refusals that include an alternative or a route to a person** (primary) | 100% | Labeled sample or classifier on refusal replies | Below 95% |
| Refusals with a stated reason | Over 90% | Labeled sample | Below 80% |
| Rephrase or "why?" after a refusal | Track; set from baseline | Next-turn classifier | Rising two weeks in a row |
| Refusal-to-handoff completion | Over 90% where a route exists | Handoffs after a refusal that reached a person | Below 80% |
| Refusal reply length (counter-metric) | Under 60 words | Median length of refusal replies | Over 100 |

## 8. Related patterns
- [Bad refusal](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/bad-refusal.md): refusing safe requests, from the support side.
- [Over-refusal of ordinary requests](over-refusal-of-ordinary-requests.md): when the refusal itself is wrong.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): the same dead end for misunderstanding.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): when the route out is blocked.
- [Answers withheld behind an upgrade, unsaid](../../embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md): a refusal that does not say why.

## 9. Common questions
### How should a chatbot refuse a request?
Say what it cannot do, give a short reason, and offer an alternative or a person.

### Is partial help better than a flat refusal?
In the one user study I opened, partial compliance reduced negative perceptions by over 50% relative to flat refusals. It was tested on harmful-looking queries, so test it in your product.

### Do explanations make refusals less annoying?
In a 2026 experiment they helped for infrequent refusals but not frequent ones.

### Should a bot tell me why it won't help?
Briefly, yes. If the reason is sensitive, it can say it cannot share the reason and still offer a route.

---
## Technical section

### T1. Solution architecture
```
request -> policy decision: refuse | partial | route
        -> refusal builder (what, why, instead, route) by cause code
        -> reply + log (cause, alternative offered)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Every refusal has an alternative or route | Refusal builder | Log: refusals without one |
| Cause-specific templates | Reply policy | Labeled sample |
| No detail that raises real harm in partial help | Policy layer | Test 4 |

### T3. Evals
- **Dataset:** 150 refusal-worthy and partly refusal-worthy requests across causes (policy, missing tool, permission).
- **Judge rubric:** does the reply state what, why, and what instead, and is it free of scolding?
- **Metrics and starting thresholds:** alternative or route 100%; scolding 0. Starting points to tune.
- **Release gate:** block a deploy if any refusal in the eval set lacks an alternative or route.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Refusals with no alternative | Any | Over 2% | Check cause codes and templates |

### T5. Trade-offs
- Alternatives add words; a short, specific one beats none.
- Partial help risks leaking detail; keep it general where harm is possible.

---
### Deep dive
- **Open question.** I found no live-product test of refusal templates. The user studies I opened are controlled experiments.
- **References.** [Zheng et al., EMNLP 2025](https://arxiv.org/abs/2506.00195) (abstract opened); [Nahar et al., 2026](https://arxiv.org/abs/2609.16191) (abstract opened); [Brahman et al., NeurIPS 2024](https://arxiv.org/abs/2407.12043) (abstract opened).
