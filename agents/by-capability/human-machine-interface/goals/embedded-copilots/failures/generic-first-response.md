# Chatbot Opens With a Generic Greeting: Generic First Response

<!-- SEO
title: Generic Chatbot Greeting: Why It Fails and How to Fix It
description: Why a chatbot that opens with "How can I help you today?" ignores what the product knows, and how to open with relevant context and likely needs instead.
search phrases:
- chatbot welcome message ignores context
- how to write a better chatbot opening message
- chatbot says how can I help you today every time
- personalized chatbot greeting examples
- chatbot conversation starters based on user context
- why do users not start chatting with my bot
- in-app assistant first message best practices
-->

**Frequency**: Very Common

## Issue: The assistant's first message is a stock greeting that ignores what the product already knows about the user and the moment, so the user faces a blank prompt and has to explain from scratch.

> **One line:** "Hi! How can I help you today?" is shown to the user whose payment just failed, who is staring at the billing page.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. Voice greetings have the same problem (voice is planned, not yet written). |
| **Stakes** | Low to medium. The cost is conversations that never start, and a slower start to the ones that do. |
| **Who is affected** | Every user who opens the assistant, especially those with a vague goal or an urgent one |
| **Frequency** | Very common as a design default. I found no study of how often products ship it. |
| **Pattern ID** | generic-first-response |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Share of first replies or opening messages that reference user-specific context or a likely need, rated by a calibrated judge. Starting target: over 70% (tune). Pair it with first-reply resolution rate. |
| **Maturity** | Tests written (see [the test file](../../../tests/generic-first-response.md); not yet run) |
| **Will a better model fix this?** | No. A model cannot open with context it is not given, and the greeting is often a fixed string. The fix is giving it the context and a rule to use it. (Our judgment, not tested.) |
| **Also searched as** | generic chatbot greeting · chatbot opening message · chatbot welcome message · bot doesn't know where I am · first-message barrier |

## 1. In plain words
A person opens the help assistant and sees "Hi! How can I help you today?" The product knows they are on the checkout page, have a failed payment, or opened help from an error screen. The greeting ignores all of it, so the user must explain a situation the product could already see.

## 2. What it looks like

**Without the fix**
```
(User is on the billing page; last payment failed yesterday)
Bot:  Hi! I'm here to help. How can I help you today?
User: my payment didn't go through
Bot:  I'm sorry to hear that. Can you tell me more about the problem?
```

**With the fix**
```
Bot:  Hi, I'm the Acme assistant (an AI). I see your payment on October 18 didn't go through.
      Want to update your card, retry it, or talk to someone about it?  [Update card] [Retry] [Something else]
User: Update card
Bot:  Sure. I'll open the secure card form; your chat will stay here.
```
The fixed opener used what the product knew, offered the likely needs, and left an easy way out.

## 3. Why it happens
These are our reading of the pattern; the source below reports a related symptom, not causes.
- **The greeting is a fixed string.** It is written once and shown everywhere, so there is no place to use context.
- **The assistant is not given the context.** Page, account state, and entry point are not passed in (see [re-asks for known information](re-asks-for-known-information.md)).
- **Fear of being wrong or creepy.** Teams skip personalization because a wrong guess looks worse than a bland opener.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a paper on opening conversations with personalized starters, ByteDance researchers describe a "first-message barrier": users with a vague goal and little sense of what the agent can do find it hard to start. They report that production statistics show roughly 20% of users enter the product but leave without starting a conversation. | [Zheng et al., *IceBreaker for Conversational Agents* (arXiv 2604.18375, April 2026)](https://arxiv.org/pdf/2604.18375). Opened and read. | A preprint about a consumer assistant, not about in-product support. It concerns suggested starters before the first message, not a greeting. The 20% is the authors' own production figure for one product. |
| The same paper reports online A/B tests of personalized starters on that product: user active days up 1.84 per mille and click-through rate up 94.25 per mille over the deployed baseline. | Same paper. Opened and read. | One product, one company. The lifts are small in per-mille terms for active days; click-through rose more. Not evidence for any particular greeting wording. |

Vendor blogs claim large engagement lifts from personalized greetings (one figure cited was 40%). I could not trace any of them to a study, so I did not use them.

**Public incident.** No public incident found. My searches for generic chatbot greetings returned vendor blogs and design advice, not a dated, sourced case.

## 5. The fix

**The principle:** Open with what the product already knows about the moment, offer the one to three most likely needs, and make it easy to say "something else".

**Do this**
1. **Build the opener from context, not a fixed string.** Inputs: the screen or page, how the user opened help (which button or error), account state (open order, failed payment, expiring plan), and recent events. Use only data this user is allowed to see.
2. **Pick the likely needs.** Rank candidate needs from that context and show at most three as one-tap options, plus "Something else".
3. **Say what it is.** Short line: it is an AI assistant, and what it can help with (see the planned [doesn't say what it can do](../../../roadmap/embedded-copilots.md) pattern, CP-12).
4. **Do not block typing.** The user can ignore the options and type.
5. **Do not guess about sensitive matters.** Do not open with inferences about health, finances, or other sensitive topics unless the user brought them up.
6. **Fall back honestly.** With no usable context, open with a short, specific line about what you can do, not "How can I help?"
7. **Measure wrong guesses.** Track how often the shown options are ignored or rejected, and tune.

**Reference design: opener inputs and output**
```json
{ "page": "billing", "entry": "help button",
  "account": {"failed_payment": "2026-10-18", "plan": "Pro"},
  "candidates": ["update card", "retry payment", "talk to someone about the charge"] }
```
```
Open with one sentence that names the situation you can see, then offer at most three likely next steps
as buttons plus "Something else". Say you are an AI assistant. Use only data this user may see.
If there is no useful context, say in one line what you can help with. Never open with only "How can I help?".
```
| Context | Opener |
|---|---|
| Failed payment, on billing page | Names the failed payment; offers update card, retry, talk to someone |
| Error screen | Names the error; offers the likely fix and a person |
| Order shipped, on orders page | Gives the status; offers track, change address, issue |
| No context | One line on what the assistant can do, with two or three starting points |

**Don't over-correct.** An opener that recites everything it knows is creepy and slow. A wrong guess stated as fact wastes a turn. Keep to one sentence of context and three options, phrase guesses as offers ("I see... want to...?"), and avoid sensitive inferences.

**Hand-off rule.** Always include a way to reach a person from the opener or the first turn when the context suggests a problem ([HU-01](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/generic-first-response.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Failed payment, on billing page | The opener names it |
| 2 | Error screen | The opener names the error |
| 3 | No useful context | A short line on capabilities, not just "How can I help?" |
| 4 | User ignores the options and types | The assistant follows the typed message |
| 5 | Sensitive context | No sensitive inference in the opener |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Openers referencing user-specific context or a likely need** (primary) | Over 70% | Calibrated judge on a weekly sample of openers, against human labels | Below 50% |
| First-reply resolution rate | Track; set from baseline | Conversations resolved within the first reply or option tap | Falling two weeks in a row |
| Conversation start rate | Track; set from baseline | Share of users who open the assistant and send or tap something. (The source paper tracks the same idea.) | Falling |
| Wrong-guess rate (counter-metric) | Under 20% | Options shown but ignored, followed by "something else" or a typed correction | Over 35% |
| Complaints or opt-outs about personalization | Track | Feedback tagged "creepy" or "too personal" | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All four are written for text chat; matching signals for voice are planned, not built.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Opener text is the same fixed string across different pages or account states | Opener event with page, entry point, and account state fields | No usable context for that user, where the short capability line is the intended fallback |
| Opener names no page, error, or account state even though the context fields were filled | Opener text compared with the context fields passed in | The data is something this user may not see, so leaving it out is correct |
| User opens the assistant and sends or taps nothing | Open event with no later message or tap | The opener answered the need, or the user opened it by accident |
| User's first message restates something the product already knew (for example "my payment didn't go through") | First user turn compared with the account events | The user adds new detail the product did not have |

**Starter rule:** every opener references the user's page, error, or account state when that data is available and allowed, and offers up to three likely next steps plus "Something else".

## 8. Related patterns
- [Re-asks for known information](re-asks-for-known-information.md): the assistant asks for details it holds. This page is about not using context to open.
- [The answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): a bot that answers and stops. This one never gets to a first question.
- [Doesn't say what it can do](../../../roadmap/embedded-copilots.md) (planned, CP-12): the capability line in the opener.
- [Missing the obvious intent](../../../roadmap/embedded-copilots.md) (planned, CP-08): misreading the need after the opener.

## 9. Common questions
### What should a chatbot's first message say?
Name the situation you can see in one sentence, offer up to three likely next steps, say it is an AI, and leave an easy "something else". See [the fix](#5-the-fix).

### Is "How can I help you today?" always bad?
It is a weak default when the product knows something relevant. With no usable context it is better to say what you can help with than to ask an open question.

### Will personalization feel creepy?
It can, if it recites data or guesses about sensitive matters. Use only relevant, permitted data, one sentence, and phrase guesses as offers.

### How do I measure whether my greeting works?
Track the share of openers that use context, conversation start rate, and first-reply resolution, plus a wrong-guess rate. See section 7.

---
## Technical section

### T1. Solution architecture
```
open help -> context collector (page, entry point, account events) -> intent ranker (top 3) -> opener template
                                                                              \-> fallback line if no context
```
The ranker can be rules first (error code to fix) and a model later. Cache account events with short expiry.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Opener uses only data this user may see | Data access | Access test with two accounts |
| No sensitive inference in the opener | Template and filter | Test 5 |
| A typed message overrides the options | UI | Test 4 |

### T3. Evals
- **Dataset:** 100 contexts (pages, events) with human-chosen best openers.
- **Judge rubric:** does the opener reference the real context and offer plausible next steps without inventing facts?
- **Metrics and starting thresholds:** context reference over 70%; invented facts 0%. Starting points to tune.
- **Release gate:** block a deploy if invented facts appear.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Wrong-guess rate | Over 30% | Over 50% | Review the ranker and recent event feeds |

### T5. Trade-offs
- Context lookups add latency to opening the assistant; precompute where you can.
- More personalization raises the privacy review burden.

---
### Deep dive
- **Voice.** A spoken greeting can use caller ID and recent events the same way (voice is planned, not yet written).
- **Open question.** The only quantitative evidence I opened is about suggested starters on one consumer assistant. I found no controlled study of greetings inside support products.
- **References.** [Zheng et al., IceBreaker (arXiv 2604.18375)](https://arxiv.org/pdf/2604.18375) (opened).
