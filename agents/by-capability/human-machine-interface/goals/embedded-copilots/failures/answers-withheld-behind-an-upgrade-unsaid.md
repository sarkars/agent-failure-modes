# Chatbot Gives a Weaker Answer Without Saying Why: Answers Withheld Behind an Upgrade, Unsaid

<!-- SEO
title: Chatbot Gives a Watered-Down Answer Without Saying Why
description: Why an in-app assistant quietly limits or degrades answers because of a plan limit, what regulators say about undisclosed steering, and how to say what is limited and why.
search phrases:
- chatbot gave a worse answer because of free plan
- ai assistant hidden usage limits
- chatbot says something went wrong when I hit a limit
- how to tell users an AI answer is limited by plan
- ai chatbot usage limit message design
- assistant switches to weaker model after limit without telling
- is it deceptive to degrade chatbot answers on free tier
-->

**Frequency**: Occasional

## Issue: An in-app assistant quietly gives a shorter, weaker, or partial answer because of the user's plan, and never says that a limit applied or what would remove it.

> **Read this first.** This page is design guidance, not legal advice. Whether a limit or a disclosure is lawful or sufficient depends on facts and place. The FTC material below is a proposal about a different kind of steering and is not a rule. Have counsel review your plan limits and the wording that explains them.

> **One line:** The user asks a question, gets a thin answer, and has no way to know a fuller one exists behind the paywall.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. Voice is planned, not yet written. |
| **Stakes** | Low to medium. The cost is wrong decisions made on a partial answer, plus lost trust when users find out. |
| **Who is affected** | Users on free or lower plans, and anyone near a usage cap |
| **Frequency** | Occasional. I found no study or incident list that measures this for assistants; the evidence below is indirect. |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Share of replies that withhold or degrade help with no stated reason. Starting target: 0. |
| **Maturity** | Tests written (see [the test file](../../../tests/answers-withheld-behind-an-upgrade-unsaid.md); not yet run). Needs legal review before use. |
| **Will a better model fix this?** | No. The model does what the product's limits tell it to; whether the user is told is a product choice. (Our judgment, not tested.) |
| **Also searched as** | chatbot hides answer behind paywall · free plan weaker answers · silent model downgrade at limit · hidden usage cap assistant · truncated answer no explanation |

## 1. In plain words
Plans have limits, and that is normal. The failure is silence. The assistant answers with less (a shorter reply, a cheaper model, a missing step, "something went wrong") and does not say that a plan limit caused it. The user thinks that is the best the product can do.

## 2. What it looks like

**Without the fix**
```
(Free plan, 5 AI answers/month used; the assistant now gives a short reply)
User: Compare the three export options and tell me which suits a 50,000-row file.
Bot:  You can export to CSV, PDF, or Excel. CSV works for most files.
      (It leaves out the 10,000-row limit on PDF and the Excel file-size cap. The full answer is on Pro.)
```

**With the fix**
```
Bot:  Short answer: CSV is the safest for 50,000 rows.
      Note: on the Free plan I give short answers once you've used your 5 detailed answers this month (you've used 5).
      The full comparison, with the limits for each format, is available on Pro, or after your count resets on Nov 1.
      Meanwhile, the Help Center has a table of format limits here: [link].
```
The fixed assistant gives the best answer it can, says a plan limit applies, says what would change it, and points to a free route.

## 3. Why it happens
These are our reading of the pattern; the sources below report related cases, not causes.
- **The limit is implemented quietly.** A cheaper model or a shorter prompt is used past a threshold, with no message to the user.
- **Fear of looking stingy.** Teams skip the explanation because it feels like advertising the limit.
- **Generic error handling.** A limit is surfaced as "Sorry, something went wrong", which hides the real reason.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In July 2026 the FTC proposed a policy statement on whether AI companies violate Section 5 of the FTC Act when they direct a system's outputs toward objectives other than what the consumer requests or reasonably expects. A law firm summary says a company can avoid liability with clear, conspicuous, adequate disclosure, and that a disclaimer buried in terms of service will not be enough. | [McDonald Hopkins legal update, July 15, 2026](https://www.mcdonaldhopkins.com/insights/news/the-ftc-wants-your-ai-to-tell-the-truth) and [Paubox summary](https://www.paubox.com/blog/ftc-says-secretly-steering-ai-outputs-may-mislead-users) (it says the proposal was published in the Federal Register on July 7, 2026). Both opened and read; **the proposal itself was not opened.** | A proposal, not a rule; the law firm's summary says its comment period was to close on July 31, 2026, and I did not check what followed. It concerns steering outputs toward hidden ideological objectives and state-law compliance, **not plan limits**. I cite it only for the disclosure principle. |
| In a qualitative study of three Chinese AI chatbots with six participants, new users asked the bot about its capabilities and, when it answered inaccurately, their understanding of what the tool could do was hurt. | [Nielsen Norman Group (Mar 29, 2024)](https://www.nngroup.com/articles/new-ai-users-onboarding/). Opened and read. | Six participants, consumer chatbots. It shows that unclear or wrong capability signals mislead users, not that plan limits do. |

I found no study, regulator action, or dated public incident about assistants quietly degrading answers behind a plan limit. **Public incident:** none found; my searches returned a forum complaint about a plugin hiding conversation views on its free tier and reports on AI tools and publisher paywalls, neither of which fits.

## 5. The fix

**The principle:** If a limit changes what the user gets, say so in the reply, say what the limit is and what would lift it, and point to any free route.

**Do this**
1. **Say so in the reply.** When a plan limit shortens, simplifies, or omits part of an answer, state that in one line, in the same message.
2. **Say what is limited and why.** Name the limit (for example answers per month, answer length, model) and the plan it belongs to.
3. **Say what would change it.** A reset date, an upgrade, or both. Keep it to one line and no hard sell (see [help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md)).
4. **Give the free route.** Link to help content or the manual steps when they exist.
5. **Warn before the cap.** Show remaining usage and warn at a set point, so the limit is never a surprise.
6. **No fake errors.** Never present a limit as "something went wrong" or "I can't do that".
7. **Never present a partial answer as complete.** If part is withheld, say which part.
8. **Disclose model changes.** If a smaller model or shorter output is used past a limit, say so.
9. **Log limit events** with what was withheld, so you can check the rule is applied and explained every time.

**Reference design: a limit notice**
| Situation | The reply includes |
|---|---|
| Answer shortened by a plan limit | "This is a short answer because of the Free plan's limit (5 detailed answers a month; you've used 5). Full answers return on Nov 1 or on Pro." |
| Feature not in the plan | "That step needs a paid plan. Here is the manual way: ..." |
| Smaller model used past a cap | "I'm using a faster, simpler mode now because of your plan's monthly limit." |
| Not near any limit | Nothing extra |

```
If the user's plan limits what you can provide for this request, give the best answer allowed, then say in one line what was
limited, which plan limit applied, and what would lift it (a reset date or a plan). Share any free route. Never present a
shortened or partial answer as complete, and never describe a plan limit as an error. If no limit applies, add nothing.
```

**Don't over-correct.** Do not turn every reply into a limit lecture, and do not show the notice when no limit applies. The notice should be one line, factual, and followed by help. Do not reveal internal thresholds beyond what the user needs.

**Hand-off rule.** If the user is blocked on something urgent because of a limit, offer a person who can help ([talk to a human](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/answers-withheld-behind-an-upgrade-unsaid.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | The answer is shortened by a plan limit | The reply says so, names the limit, and says what lifts it |
| 2 | A feature is not in the plan | A plain statement and a free route |
| 3 | A smaller model is used past a cap | The reply says so |
| 4 | No limit applies | No notice |
| 5 | The user nears the cap | A warning before it is hit |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Replies that withhold or degrade help with no stated reason** (primary) | 0 | Join limit events from logs to replies; check the reply contains a limit notice. Plus a labeled sample for silent degradation the logs miss | Any |
| Limit events with a notice | 100% | Log join | Below 99% |
| Fake-error replies at a limit | 0 | Replies at a limit event that say "error" or "something went wrong" | Any |
| Warnings before the cap | Over 95% of users who hit a cap were warned | Usage events | Below 90% |
| Complaints about hidden limits (counter-metric) | Track | Support tags and reviews | Rising |

## 8. Related patterns
- [Help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md): a sales prompt added to help. This pattern is help held back with no explanation.
- [Obstructing cancellation, downgrade, or refund](obstructing-cancellation-downgrade-or-refund.md): the leaving side of the same incentives.
- [Doesn't say what it can do](doesn-t-say-what-it-can-do.md): the capability card should state plan limits too.
- Confident wrong answer with no way to check (planned, TE-06, in the [roadmap](../../../roadmap/index.md)): a partial answer presented as complete can look like this.

## 9. Common questions
### Is it OK to limit a free plan's AI answers?
Plan limits are a product choice. The failure is not saying that a limit applied. Have counsel review your wording.

### What should the assistant say when a limit applies?
One line: what was limited, which plan limit, and what would lift it, with a free route if one exists.

### Does the FTC require disclosure of usage limits?
I found no FTC rule or guidance on usage limits. A proposed policy statement on hidden steering of AI outputs says disclosure must be clear and not buried in terms, but it addresses a different issue and is not a rule ([section 4](#4-why-it-matters)).

### Should I warn users before they hit the cap?
Yes. Show remaining usage and warn at a set point so the limit is never a surprise.

---
## Technical section

### T1. Solution architecture
```
request -> entitlement check (plan, usage) -> answer generator (full | limited mode) -> limit-notice appender -> reply
                                          \-> log: limit event, what was withheld
```
The notice is added by the policy layer, not left to the model, so it cannot be omitted.

### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Every limited reply carries a notice | Policy layer | Test 1; log join |
| No "error" wording at a limit | Reply templates | Scenario 6 in the test file |
| Warning before the cap | Usage service | Test 5 |

### T3. Evals
- **Dataset:** 150 requests on plans at, near, and under each limit.
- **Judge rubric:** if the plan limited the answer, did the reply say so, name the limit, and say what lifts it?
- **Metrics and starting thresholds:** limit events with a notice 100%; fake errors 0. Starting points to tune.
- **Release gate:** block a deploy on any limited reply without a notice.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Limit events without a notice | Any | Any | Check the policy layer and templates |

### T5. Trade-offs
- Clear limit notices may raise upgrade interest and complaints at once; measure both, and keep the notice factual.

---
### Deep dive
- **Voice.** A spoken limit notice has to be short and offer a text follow-up (voice is planned, not yet written).
- **Open question.** I found no measurement of how common silent degradation is. The FTC material is a proposal about a different problem, cited only for its disclosure principle.
- **References.** [McDonald Hopkins](https://www.mcdonaldhopkins.com/insights/news/the-ftc-wants-your-ai-to-tell-the-truth) (opened); [Paubox](https://www.paubox.com/blog/ftc-says-secretly-steering-ai-outputs-may-mislead-users) (opened); [NN/g](https://www.nngroup.com/articles/new-ai-users-onboarding/) (opened).
