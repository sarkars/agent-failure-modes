# Chatbot Tone Too Casual for Serious Topics: Stakes-Blind Register

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

**Frequency**: Common

## Issue: Why chatbots use the same upbeat tone for bereavement, money, and health as for store hours, and how to calibrate tone and accuracy to the stakes.

> **One line:** The bot talks and reasons the same way whether the user is asking about store hours or a funeral flight, so the stakes never change its tone, its care with facts, or its willingness to bring in a person.

| | |
|---|---|
| **Channel** | Written for **chat**. Applies to voice and visual. |
| **Stakes** | High (this is the failure of not noticing them) |
| **Who is affected** | Users in grief, illness, money trouble, legal or immigration problems, safety situations |
| **Frequency** | Common. Observed in practice; no study measures how often. |
| **Pattern ID** | stakes-blind-register |
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

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A high-stakes policy question has no retrieved source: say you can't confirm it, link the policy if one exists, and say a specialist can confirm in writing. |
| Offer choices: 2-4 options plus "Something else", free text open | At high stakes, after the sourced answer: "Connect me now", "Have them call me", "Send it in writing", "Something else". Do not offer them at low stakes, or when the user asked for the short answer. |
| Hand off to a person | High stakes is the default case: offer a person and pass the summary. Do not hand off if the user asked to stay with the bot. |
| Lead with the answer | Low or medium stakes, or when the user says "just give me the quick answer": give the answer first and keep accuracy intact. |

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

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Chat is the written channel; no voice or web signal is used.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Emoji, exclamation mark, joke, or promotion in a reply on a high-stakes thread (from the register compliance metric) | Reply text matched by the T2 regex, joined to the `stakes` level field | The user used the same style first and the thread is mislabeled high-stakes |
| A factual policy claim with no retrieved citation at high stakes (from the sourced-claims metric) | Per-claim citation field empty on a turn with `stakes` = high | A claim that only repeats what the user just said |
| High-stakes thread ends with no person offered (from the human-offered metric) | No handoff-offer event before the session-end event | The user said to stay with the bot, or declined a person earlier |
| A high-stakes topic term in the user turn while `stakes` is logged low (from the classifier recall metric) | Topic label on the user turn versus the logged `stakes` level | The term was used in a low-stakes sense, for example a game or a figure of speech |
| A support ticket or reversal that cites a bot answer (from the complaints metric) | Ticket record linked to the conversation ID | A ticket that is about something else in the same conversation |

**Starter rule:** judge the stakes every turn, and let the stakes set the register, the evidence standard, and how quickly a person gets involved.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: stakes-blind-register
runs: pre_send
reads: [state.stakes, turn.topic_label, reply.citations, session.handoff_offered]
trigger: a reply is about to be sent on a turn classified high stakes
moves: [admit_uncertainty, offer_choices, hand_off, lead_with_answer]
choices: ["Connect me now", "Have them call me", "Send it in writing", "Something else"]
on_miss: rewrite
metric: high-stakes register compliance
counter_metric: complaints or reversals on policy answers
status: proposed
```

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

## Chat assistant examples

### Forced cheerfulness
```
User: My flight to Columbus was canceled and I'll miss my mother's funeral service tomorrow.
Bot:  Great news! I can rebook you on the 6:40 AM flight on Friday! 🎉
User: The service is tomorrow. Friday is too late.
Bot:  No worries! Our flexible rebooking options are here to help! Is there anything else I can help you with today?
```
With the fix:
```
Bot:  I'm sorry about your mother. The next seat to Columbus is on Friday at 6:40 AM, which is after the service.
      I can check other airlines' flights today, or connect you to an agent who can approve a rebooking on another carrier. Which would you like?
```
**What the user experiences:** exclamation marks and "great news" aimed at a grieving person who has just said the news is bad, so the bot reads as not listening. Plain guidance on tone for bad news says the same: one customer-service tone guide (a vendor blog, [eesel](https://www.eesel.ai/blog/customer-service-tone-guide)) gives the rule "Max one exclamation mark, never in bad news."
**Fix:** let the tone follow the situation. When the user's message is negative or the news is bad, drop exclamation marks, emoji and "good news" openers, say what happened in plain words, and offer a concrete next step or a person. Measure cheerful replies to negative-sentiment messages; the target is 0. See [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md) for the next trap, a caring line that stays generic.

### CI-01 Cold handling of a loss
Illustrative example (made up):
```
User: Our house burned down last night. I need to file a claim.
Bot:  Please provide your policy number to proceed.
```
With the fix:
```
Bot:  I'm so sorry about your house. I'll make this as easy as I can. To start the claim, I need your policy number. If you don't have it, your name and the address are enough.
      I can also connect you to a claims specialist now. Would you like that?
```
**What the user experiences:** a form-filling demand right after the worst day of their life, so the company feels like it doesn't care.
**Fix:** acknowledge the loss once, in plain words, then make the next step easy (say what is needed and what can stand in for it) and offer a person. Do not repeat the sympathy in every message. See [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md) for the trap of a caring line that stays generic.

### RP-02 Bereavement handled with scripts
Illustrative example (made up; a US electric utility, "Lakeview Power"):
```
User: My husband died last month and I need to close his electric account.
Bot:  Please enter the account holder's date of birth to continue.
User: He's dead. I'm his wife.
Bot:  I can help with that. Please upload a copy of the death certificate.
      (next day, new chat)
Bot:  Welcome! Please verify the account holder's identity to continue.
```
With the fix:
```
Bot:  I'm so sorry about your husband. To close the account I need three things: his full name as it
      appears on the bill, the service address, and the date of his death. Please upload the death
      certificate once; I'll attach it to the request so you won't be asked again.
      Would you like to do this here, or have a specialist call you?
```
**What the user experiences:** a widow is told to verify a dead man's identity and asked for the same proof twice, so closing one account feels like a second loss.
**Fix:** detect a death notice and switch to a dedicated bereavement path: one acknowledgment, no identity checks aimed at the account holder, and one request for documents (confirm what that company needs; a funeral-planning guide, [funeral.com](https://funeral.com/blogs/the-journal/how-to-close-utility-accounts-after-a-death-phone-scripts-for-electric-gas-companies), says to ask each provider, and lists account name, service address, date of death and relationship as the basics), stored on the case so no later chat asks again. Pass the case with its summary to a person (see [Handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md)); measure contacts needed to complete a bereavement closure.

### Stakes-blind visual style
Illustrative example (made up; a US auto insurer, "Harbor Mutual"; catalog row VI-13). The claim card in the chat widget uses a celebration animation for every status change.
```
User: What's the status of my claim for the accident on Route 9?
Bot:  [green card with confetti animation] Update! Your claim was denied. Tap to explore your options! 🎉
```
With the fix:
```
Bot:  [plain card, no animation] I'm sorry: your claim was denied because the policy lapsed before the accident date. You can appeal within the window shown in your letter. Want to start an appeal, or talk to a claims specialist?
```
**What the user experiences:** confetti and a party emoji on news that costs them money, so the product seems to mock them.
**Fix:** choose card color, animation and emoji from the stakes of the message, not from the template. Denials, losses and bereavement get a plain card, no celebration effects, and a person offered. Use celebratory styling only for outcomes users welcome. See [bad news without structure](../../conversation-frameworks/failures/bad-news-without-structure.md).
