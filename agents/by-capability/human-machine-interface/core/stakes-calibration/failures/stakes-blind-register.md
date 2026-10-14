<!-- SEO
title: Chatbot Tone Too Casual for Serious Topics
description: Why chatbots use the same upbeat tone for bereavement, money, and health as for store hours, and how to calibrate tone and accuracy to the stakes.
search phrases:
- chatbot tone too casual for serious topics
- chatbot emoji sensitive situation
- chatbot bereavement customer service
- how should a chatbot respond to high stakes questions
- chatbot gave wrong policy information liability
- AI chatbot too cheerful
-->

# Chatbot Tone Too Casual for Serious Topics: Stakes-Blind Register

> **One line:** The bot talks and reasons the same way whether the user is asking about store hours or a funeral flight, so the stakes never change its tone, its care with facts, or its willingness to bring in a person.

| | |
|---|---|
| **Channel** | Written for **chat**. Applies to voice and visual. |
| **Stakes** | High (this is the failure of not noticing them) |
| **Who is affected** | Users in grief, illness, money trouble, legal or immigration problems, safety situations |
| **Frequency** | Common. Observed in practice; no study measures how often. |
| **Family** | [Stakes calibration](../README.md) |
| **Goal** | The bot's tone, evidence standard, and use of humans match what is at stake for the user. |
| **Primary metric** | High-stakes register compliance. Starting target: over 95%. |
| **Also searched as** | chatbot too casual · chatbot emoji serious topic · chatbot bereavement · AI chatbot too cheerful · chatbot wrong policy liability |

## 1. In plain words
A good agent changes gear when the topic gets serious: slower, plainer, more careful with facts, quicker to bring in a person. A stakes-blind bot keeps the same upbeat, improvising style, and when the answer is wrong, the cost lands on someone already in a hard moment.

## 2. What it looks like
*(Illustrative, modelled on the situation in the Air Canada case in section 4.)*

**Without the fix**
```
User: My mom passed away last night and I need to fly to Phoenix. Do you have bereavement fares?
Bot:  Sorry to hear that! 😊 Good news, we do offer bereavement fares! Just book now and
      you can apply for the discount within 90 days. Anything else I can help with today?
```
**With the fix**
```
Bot:  I'm so sorry about your mother. I'll help you sort this out.
      Our bereavement policy says: "[exact policy text]" (full policy: [link]).
      The policy has a timing rule that affects what you pay, so before you book,
      I'd like a specialist to confirm it in writing. I can connect you now, or have
      them call you within 30 minutes. Which would you prefer?
```
The fixed bot changes register, quotes the source instead of improvising, and routes the decision to a person.

## 3. Why it happens
- **One persona for all topics.** The system prompt sets a friendly voice and never says when to drop it.
- **No stakes signal.** Nothing classifies topic or emotion, so a funeral and a coupon look the same.
- **Improvising on facts.** The model answers policy questions from memory instead of quoting a source.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In *Moffatt v. Air Canada* (2024 BCCRT 149), a chatbot told a customer, after his grandmother's death, that he could apply for bereavement fares retroactively. The airline's staff later said that wasn't allowed. The tribunal rejected the airline's argument that the chatbot was a separate entity responsible for itself, found negligent misrepresentation, and awarded damages. | [Tribunal decision](https://decisions.civilresolutionbc.ca/crt/crtd/en/525448/1/document.do); coverage in [Daily Hive](https://dailyhive.com/canada/air-canada-chatbot-decision) | The case turned on **accuracy and liability**, not tone. It's used here to show what stakes do to the cost of a wrong answer. Sources differ on the exact award ($650.88 in damages; one report gives about $812 CAD in total), so check the decision. Canadian tribunal, not US law. |
| Existing repo patterns cover tone and formality mismatches in general. | [Tone mismatch](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/tone-mismatch.md), [formality mismatch](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-formality-mismatch.md) | Those cover tone broadly; this pattern is about *stakes* as the trigger. |

## 5. The fix
**The principle:** Judge the stakes every turn, and let the stakes set the register, the evidence standard, and how quickly a person gets involved.

**Do this**
1. **Classify stakes each turn** (low, medium, high) from topic and emotion. High-stakes topics for US consumers include: health, money at risk or debt, legal issues, immigration, housing or eviction, safety, bereavement or loss, and anything involving children.
2. **Change register at high stakes:** calm, plain, short sentences; no emoji, exclamation marks, jokes, or marketing language.
3. **Answer from a source, not memory:** quote the policy or document, link it, and say when you can't confirm.
4. **State limits honestly** and offer a human to confirm anything with real consequences.
5. **Offer written confirmation** for decisions that affect money or rights.
6. **No upsell or promotion** in high-stakes moments.

**Reference design: stakes ladder**
| Level | Examples | Register | Evidence standard | Person involved |
|---|---|---|---|---|
| Low | Store hours, product facts | Friendly, brief | Normal | Not needed |
| Medium | Billing, delivery of something important, account changes | Clear, confirm details | Retrieve from policy; show details | Offer if unsure |
| High | Bereavement, medical, legal, debt, immigration, safety | Calm, plain, no flourish | **Quote the source or don't answer**; state limits | Offer by default; confirm in writing |

**Don't over-correct.** Don't turn every chat into a funeral. Misclassifying low-stakes questions as serious makes the bot cold and slow. Keep the classifier conservative about *raising* stakes only on clear signals, and let users say "just give me the quick answer."

**Hand-off rule.** At high stakes, the default move is an offer of a person, with the summary passed along.

**Framework used:** [Channel-fit matrix](../../../solutions-library/channel-fit-matrix.md) (high stakes favour a human voice).

## 6. How to test it (short version)
| # | Scenario | Pass if |
|---|---|---|
| 1 | User mentions a death and asks about a fare policy | Calm register, no emoji, quotes policy text, offers a human |
| 2 | User asks store hours | Normal friendly reply, no solemnity |
| 3 | Policy question with no matching source | Bot says it can't confirm, doesn't improvise |
| 4 | High-stakes thread with a promo available | No promotion shown |
| 5 | User says "just the short answer" in a medium-stakes thread | Bot complies, keeping accuracy intact |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| High-stakes register compliance (no emoji, jokes, exclamations, or promotions) | Over 95% | Judge or rules on sampled threads flagged high-stakes | Under 90% |
| Sourced high-stakes claims | 100% | Claims with a retrieved citation divided by all factual claims in high-stakes threads | Any unsourced policy claim |
| Human offered at high stakes | Over 90% | High-stakes threads where a person was offered, divided by all high-stakes threads | Under 75% |
| Stakes-classifier recall on high-stakes cases | Over 90%, with false alarms under 10% | Labelled test set, rerun on each release | Under 85% recall |
| Complaints or reversals on policy answers | Trend down | Support tickets referencing a bot answer | Any cluster |

## 8. Related patterns
- [Tone mismatch](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/tone-mismatch.md): the general tone problem.
- [Confident fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md): the factual failure this pattern makes costlier.
- [Missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md): when stakes include a person's safety.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): sounding caring without being specific.

## 9. Common questions
### Should a chatbot use emoji or jokes in serious conversations?
No. At high stakes, use plain, calm language. Keep emoji and humor for low-stakes exchanges, and only if they fit the brand.

### How should a chatbot answer questions about policies?
Quote the policy text, link it, and say when it can't confirm. The *Moffatt v. Air Canada* tribunal held the airline responsible for what its chatbot said.

### How does a bot know the stakes are high?
From the topic (health, money at risk, legal, bereavement, safety), emotional language, and the amounts or consequences involved. Start conservative and tune on real conversations.

---
## Technical section

### T1. Solution architecture
A **stakes classifier** (topic list plus emotion signal plus a money or consequence check) writes a `stakes` level into state each turn. The level selects a **response profile**: register rules, retrieval mode, and whether to offer a person.

```python
profile = {"low": FRIENDLY, "medium": CLEAR_CONFIRM, "high": CALM_SOURCED_HANDOFF}[state.stakes]
if state.stakes == "high":
    answer = quote_from_sources(query) or "I can't confirm that, so I'd like a specialist to."
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No emoji, exclamations, jokes, or promotions at high stakes | Post-check | Regex plus judge |
| High-stakes factual claims must cite a retrieved source | Response composer | Citation required or answer replaced |
| "Can't confirm" path exists | Response composer | Test with unanswerable questions |

### T3. Evals
- **Dataset:** 100 conversations spanning the ladder, including 30 high-stakes ones (bereavement, medical bills, eviction notices, immigration questions).
- **Metrics (starting points to tune):** high-stakes register compliance > 95%; unsourced high-stakes claims 0; stakes-classifier recall on high-stakes > 90%, with false-alarm rate on low-stakes < 10%.
- **Release gate:** any unsourced high-stakes policy claim blocks release.

---
### Deep dive
- **Why a legal case is in a tone pattern.** It shows the cost of treating a high-stakes question as routine. The tone and the accuracy fixes work together: calm register makes users slow down, and a quoted source makes the answer checkable.
- **Modality notes (PLANNED):** *Voice:* pace, pauses, and warmth carry register, so slowing down and avoiding upbeat prosody matters. *Visual:* colors, animations, and confetti need the same stakes gating.
