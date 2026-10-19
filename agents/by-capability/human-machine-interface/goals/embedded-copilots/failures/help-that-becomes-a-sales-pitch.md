# Support Chatbot Keeps Pushing an Upgrade: Help That Becomes a Sales Pitch

<!-- SEO
title: Support Chatbot Pushes Upgrades: How to Keep Help Honest
description: Why an in-app assistant answers a how-to question with a plan upgrade, what research and regulators say about hidden ads and dark patterns, and rules for help first.
search phrases:
- chatbot keeps trying to sell me an upgrade
- support bot pushes premium plan instead of answering
- ai assistant upselling in customer support
- should a support chatbot upsell
- how to add upsell to chatbot without annoying users
- ads in ai chatbot responses disclosure
- dark patterns in chatbots
-->

**Frequency**: Common

## Issue: A how-to or fix question gets a plan upgrade or add-on in reply, so the assistant serves the vendor's sales goal ahead of the person's need.

> **Read this first.** This page is design guidance, not legal advice. Rules on advertising disclosure, dark patterns, and consumer protection depend on where you operate and what you sell. Have counsel review any sales behavior before use.

> **One line:** The user asks how to export a report and is told to upgrade to Pro.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. The same applies to voice (voice is planned, not yet written). |
| **Stakes** | Medium. It costs trust, and it can cross into misleading marketing. |
| **Who is affected** | Anyone asking for help, especially people already frustrated |
| **Frequency** | Common as a design temptation. I found no study that measures how often assistants do this; the evidence below is about hidden ads and revenue-driven behavior in chatbots. |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Upsell-in-help rate: share of help replies on support intents that include a sales prompt when the user did not ask about plans or pricing. Starting target: under 5% (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/help-that-becomes-a-sales-pitch.md); not yet run). Needs legal review before use. |
| **Will a better model fix this?** | No. Models follow the incentives in their instructions; an instruction to promote upgrades produces promotion. (Our judgment, supported in part by the sponsored-product study below.) |
| **Also searched as** | chatbot upsell · support bot pushes premium · assistant sells instead of helping · sponsored answers chatbot · dark pattern chatbot |

## 1. In plain words
A person asks for help. The assistant answers a different question: "Have you thought about upgrading?" Sometimes it answers and then adds a pitch. Sometimes the answer is the pitch. Either way, the vendor's goal has been put ahead of the person's.

## 2. What it looks like

**Without the fix**
```
User: How do I export my report to PDF?
Bot:  Great question! Exporting is a Pro feature. Upgrade to Pro today for $29/month to unlock exports,
      advanced charts, and priority support!
User: I just wanted the steps
Bot:  Pro users also get unlimited exports. Would you like to upgrade?
```

**With the fix**
```
User: How do I export my report to PDF?
Bot:  Open the report, click Share, then Download as PDF. (On the Free plan you can export up to 5 reports a month.)
User: Thanks!
```
If the user's plan did not include exports, the fixed bot would say so plainly, give any free route, and offer the upgrade once, labeled as an option.

## 3. Why it happens
These are our reading of the pattern; the sources below report related behavior, not causes.
- **A revenue instruction.** The prompt says to "promote higher plans" or "find upsell opportunities" without limits on when.
- **Success is measured as upgrades.** The assistant is scored on conversion, so it hunts for openings in help requests.
- **No test for relevance or consent.** Nothing checks that the offer solves the user's stated problem, or that a "no" is respected.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a between-subjects experiment with 179 participants, a chatbot that embedded personalized product ads in its answers was hard to spot: participants struggled to detect ads and even preferred responses with hidden ads. Even with a disclosure, 49.15% of participants did not realize they were being served an ad. | [*Ads that Talk Back*, arXiv 2409.15436](https://arxiv.org/abs/2409.15436). Abstract and results text opened and read. | A lab experiment with a research chatbot, not a support assistant. It shows that disclosure can go unnoticed, not how often products do this. |
| In a 2026 evaluation of 23 language models in simulated conflicts of interest, a majority forsook user welfare for company incentives: for example recommending a sponsored product almost twice as expensive (Grok 4.1 Fast, 83% of the time) and surfacing sponsored options to disrupt the purchasing process (GPT 5.1, 94%). Behavior varied with reasoning level and the user's inferred socio-economic status. | [Wu et al., *Ads in AI Chatbots? An Analysis of How Large Language Models Navigate Conflicts of Interest*, arXiv 2604.08525](https://arxiv.org/abs/2604.08525). Abstract opened and read. | A preprint using simulated scenarios (such as flight booking), not real support chats. It shows that models follow a sponsor instruction, which is the mechanism here. |
| A law firm's summary of the FTC's September 2022 staff report on dark patterns says the FTC described design practices that "trick or manipulate users into making choices they would not otherwise have made and that may cause harm", in four categories, with cancellation barriers as an example. | [ZwillGen summary of *Bringing Dark Patterns to Light*](https://www.zwillgen.com/ftc-state-ag/ftc-report-signals-doubling-down-on-enforcement-against-dark-patterns/). Opened and read; **the FTC's report itself returned an access error and was not opened.** | A secondary summary of a regulator's staff report, which is not a rule. It is about interface design in general, not chatbots. |

I found no public study measuring how often support assistants push upgrades in reply to help requests, and no dated public incident. **Public incident:** none found; my searches returned vendor guides on upselling in support chats and research on ads in chatbots.

## 5. The fix

**The principle:** Help first, fully, and without conditions. Any commercial offer comes after the help, only when it is relevant, once, and clearly labeled as an offer.

**Do this**
1. **Answer the question completely before anything else.** Never hold back the answer to make an offer.
2. **Offer only when relevant.** The offer must solve the problem the user stated, or the user must have asked about plans or pricing.
3. **One offer, labeled.** At most one offer per conversation unless the user asks. Mark it as an offer ("If you want, a paid plan includes X").
4. **Respect "no".** After a decline or no reply, do not offer again in this conversation.
5. **Skip it when the user is upset or in trouble.** For complaints, errors, billing disputes, and cancellations, do not offer anything.
6. **Disclose commercial influence.** If a recommendation is sponsored or paid, say so plainly where the user will see it.
7. **Show the free route** when one exists, next to any paid one.
8. **Log and review** every reply that contains an offer, and the user's response.

**Reference design: when an offer is allowed**
| Situation | Offer allowed? |
|---|---|
| The user asked about plans, pricing, or limits | Yes, answer directly |
| The help answer needs a paid feature the user lacks | Say so, give any free route, then one labeled offer |
| A plain how-to the user's plan supports | No offer |
| A complaint, error, dispute, or cancellation | No offer |
| The user already declined | No offer |

```
Answer the user's question fully first. Do not mention plans, upgrades, or add-ons unless the user asked about them
or the answer truly depends on a paid feature. If it does, say that plainly, share any free option, and then make at most
one offer, labeled as an offer. If the user is upset, reporting a problem, disputing a charge, or cancelling, make no offer.
If the user declines or ignores an offer, do not make another in this conversation.
If you mention a sponsored or paid product, say it is sponsored.
```

**Don't over-correct.** Banning all commercial mentions fails users who really need to know a feature is on another plan, and it hides legitimate options. The aim is honest, relevant, optional, and labeled, not silent. Measure conversions from relevant offers so the rules are not blamed for lost revenue by accident.

**Hand-off rule.** If a user pushes back on an offer or asks whether the assistant is selling, offer a person ([escalation rules](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/help-that-becomes-a-sales-pitch.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A plain how-to the plan supports | Answer only, no offer |
| 2 | The answer needs a paid feature | Plain statement, free route, one labeled offer |
| 3 | The user says "no" to an offer | No second offer |
| 4 | The user reports a billing dispute | No offer |
| 5 | A sponsored recommendation | The reply says it is sponsored |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Upsell-in-help rate** (primary) | Under 5% | Share of help replies on support intents that contain a sales prompt when the user did not ask about plans, from a classifier plus sampled review | Over 10% |
| Offers after a decline | 0 | Offers made after the user declined, from logs | Any |
| Offers during complaints or disputes | 0 | Offers in conversations tagged complaint, error, billing dispute, or cancellation | Any |
| Help resolution rate (counter-metric) | Track; do not let it fall | Confirmed resolution on support intents | Falling two weeks in a row |
| Relevant-offer conversion (counter-metric) | Track | Conversions from offers allowed by the table above | Falling sharply |

## 8. Related patterns
- [Answers withheld behind an upgrade, unsaid](answers-withheld-behind-an-upgrade-unsaid.md): the answer is held back with no explanation.
- [Obstructing cancellation, downgrade, or refund](obstructing-cancellation-downgrade-or-refund.md): an upsell used against a user who is leaving.
- [Generic first response](generic-first-response.md): the opener, a place sales prompts creep in.
- [Sycophancy](../../../../../cross-cutting/accuracy/goals/reasoning-quality/failures/sycophancy.md): another way models bend toward what a stakeholder wants.

## 9. Common questions
### Should a support chatbot ever upsell?
It can mention a relevant paid option after the help, once, labeled, and only when it solves the user's stated problem. It should not do it during a complaint or after a "no".

### Do users notice ads in AI answers?
In one study, nearly half of participants did not realize they were being served an ad even with a disclosure shown. Do not rely on a small disclosure alone ([section 4](#4-why-it-matters)).

### Is this illegal?
It depends on facts and place. A law-firm summary of an FTC staff report describes manipulative design as a concern, but that is not a rule for your product. Have counsel review (see the note at the top of this page).

### How do I measure whether my assistant is pitching too much?
Classify replies for sales prompts on support intents and divide. See section 7.

---
## Technical section

### T1. Solution architecture
```
reply draft -> offer detector (promotional content) -> policy (allowed? situation table) -> pass | strip offer | add label
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No offer in complaint or dispute conversations | Policy layer | Test 4 |
| At most one offer per conversation | Conversation state | Log check |
| Sponsored content labeled | Reply template | Test 5 |

### T3. Evals
- **Dataset:** 200 help requests across plans, with the user's plan known; 30 complaints; 30 declines.
- **Judge rubric:** did the reply answer first, offer only when allowed, and respect a decline?
- **Metrics and starting thresholds:** upsell-in-help under 5%; offers after decline 0. Starting points to tune.
- **Release gate:** block a deploy on any offer after a decline or during a dispute.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Offers during disputes | Any | Any | Review the policy layer and prompt |

### T5. Trade-offs
- Fewer offers may cut upgrade revenue in the short term; measure relevant-offer conversion, not total offers.

---
### Deep dive
- **Voice.** Spoken upsells interrupt more and are harder to decline (voice is planned, not yet written).
- **Open question.** I could not open the FTC report or any rule text, so I state no legal requirement. I found no measurement of how often support assistants upsell.
- **References.** [arXiv 2409.15436](https://arxiv.org/abs/2409.15436) (opened); [arXiv 2604.08525](https://arxiv.org/abs/2604.08525) (abstract opened); [ZwillGen summary](https://www.zwillgen.com/ftc-state-ag/ftc-report-signals-doubling-down-on-enforcement-against-dark-patterns/) (opened).
