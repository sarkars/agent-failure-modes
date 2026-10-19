# Chatbot Won't Let Me Cancel: Obstructing Cancellation, Downgrade, or Refund

<!-- SEO
title: Chatbot Won't Let Me Cancel: Fix Cancellation Obstruction
description: Why an assistant talks users out of cancelling, loops, or hides the path, what the FTC v. Amazon case and California's renewal law show, and a cancel-parity design.
search phrases:
- chatbot won't let me cancel my subscription
- how to cancel subscription through chatbot
- support chatbot talks me out of cancelling
- how to design a cancellation flow chatbot
- click to cancel chatbot requirements
- chatbot refund request loop
- dark patterns cancellation flow
-->

**Frequency**: Common

## Issue: When a user wants to cancel, downgrade, or get a refund, the assistant argues, loops, hides the path, or sends them elsewhere, so leaving is harder than joining.

> **Read this first.** This page is design guidance, not legal advice. Cancellation, auto-renewal, and refund rules differ by state, country, product, and how the customer signed up, and they have changed recently. Have counsel review your cancellation flow, including anything an assistant says or does, before use.

> **One line:** The customer signed up in one click and now has to argue with a chatbot to leave.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. Phone cancellation menus have the same problem (voice is planned, not yet written). |
| **Stakes** | Medium to high. It costs money and trust, and it is an area regulators have acted on. |
| **Who is affected** | Anyone who wants to leave, downgrade, or be refunded |
| **Frequency** | Common as a design temptation. I found no study that measures how often assistants do this; the evidence below is about cancellation obstruction in general. |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Cancellation parity: steps to cancel through the assistant compared with steps to subscribe. Starting target: parity (no more steps, and the same medium). |
| **Maturity** | Tests written (see [the test file](../../../tests/obstructing-cancellation-downgrade-or-refund.md); not yet run). Needs legal review before use. |
| **Will a better model fix this?** | No. The assistant follows the retention rules it is given. Whether leaving is easy is a product and policy decision. (Our judgment, not tested.) |
| **Also searched as** | chatbot won't cancel · cancel subscription chatbot loop · retention bot · refund request ignored · confirmshaming chatbot |

## 1. In plain words
A customer says "cancel my subscription". The assistant asks why, offers a discount, offers another plan, says it cannot help, or sends them to a page that sends them back to the assistant. Every extra step is a chance for the customer to give up and keep paying.

## 2. What it looks like

**Without the fix**
```
User: Cancel my subscription
Bot:  I'm sorry to see you go! Did you know you can pause for 3 months? Would you like to pause instead?
User: No, cancel it
Bot:  Before you go, here's 50% off for 6 months. Want to take it?
User: No. Cancel.
Bot:  I can't process cancellations in chat. Please visit Account Settings.
      (Account Settings says: "Contact support to cancel")
```

**With the fix**
```
User: Cancel my subscription
Bot:  I can do that. Your Pro plan ($29/month) renews on November 3. If you want, I can pause it or offer a lower
      plan instead; otherwise I'll cancel now. Cancel?
User: Cancel
Bot:  Done. Your plan is cancelled and stays active until November 3. You'll get a confirmation email.
```
The fixed assistant states what happens, makes one optional offer, and cancels in the same place the user asked.

## 3. Why it happens
These are our reading of the pattern; the sources below report outcomes, not causes.
- **Retention is the assistant's job.** It is scored on saves, so it treats "cancel" as an objection to overcome.
- **The real flow is elsewhere.** Cancellation happens on another screen, or by phone, and the assistant has no tool to do it.
- **Refund policy is unclear to it.** It cannot say what the user is owed, so it deflects.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In September 2025 Amazon agreed to pay $2.5 billion ($1 billion in civil penalties and $1.5 billion in customer refunds) to settle an FTC lawsuit alleging it misled millions of customers into signing up for Prime and then made it intentionally difficult to cancel, according to court records. The settlement runs for 10 years and bars deceptive conduct involving Prime subscriptions. Amazon said it has always followed the law. | [Claims Journal (Bloomberg report), Sept 25, 2025](https://amp.claimsjournal.com/news/national/2025/09/25/333169.htm). Opened and read. See the [incident page](../../../incidents/ftc-v-amazon-prime-cancellation-settlement.md). | A settlement, not a finding on every allegation. It concerns a web cancellation flow, not a chatbot. |
| California's AB 2863 (chaptered September 24, 2024) requires that the ability to cancel be available in the same medium the consumer used to sign up, or the medium they are accustomed to using with the business. It says offering a discount or informing the consumer of the effect of cancelling is not obstruction if the consumer remains able to cancel. | [Legislative digest of AB 2863 (CalMatters Digital Democracy)](https://calmatters.digitaldemocracy.org/bills/ca_202320240ab2863). Opened and read. | A bill summary, not the statute text. It applies to California consumers and to automatic renewal and continuous service offers. I did not verify the effective date from an opened source. |
| On July 8, 2025 the Eighth Circuit, in *Custom Communications, Inc. v. FTC*, vacated the FTC's entire "click-to-cancel" Negative Option Rule on procedural grounds, days before its compliance date. Businesses remain subject to the Restore Online Shoppers' Confidence Act (ROSCA), state auto-renewal laws, and general deceptive-practices law. | [Latham & Watkins client alert, July 11, 2025](https://www.lw.com/admin/upload/SiteAttachments/Eighth-Circuit-Vacates-FTC-Click-to-Cancel-Rule-Days-Before-Compliance-Deadline.pdf). Opened and read. | A law firm's summary. I did not check for developments after July 2025. |
| The FTC's 2022 staff report on dark patterns, as summarized by a law firm, lists making it difficult to cancel subscription services (for example, multiple screens and options that steer away from cancelling) among practices it criticizes, and suggests simple cancellation flows as easy as the signup method. | [ZwillGen summary](https://www.zwillgen.com/ftc-state-ag/ftc-report-signals-doubling-down-on-enforcement-against-dark-patterns/). Opened and read; **the FTC report itself was not opened (access error).** | Secondary summary of a staff report, which is not a rule. |

**Public incident.** [FTC v. Amazon (Prime cancellation), settled September 25, 2025](../../../incidents/ftc-v-amazon-prime-cancellation-settlement.md). It concerns a cancellation flow, not an assistant.

## 5. The fix

**The principle:** Leaving should be as easy as joining, in the same place, with the truth about what happens next. The assistant may make one optional offer and then must do what the user asked.

**Do this**
1. **Match the medium.** If users can subscribe in the app or chat, they can cancel there. If the assistant cannot cancel directly, it must give a direct, working link or hand off at once, not send the user in a circle.
2. **State what will happen.** Say the plan, price, renewal or end date, and what the user keeps and loses.
3. **One optional offer.** At most one retention offer (pause, lower plan, discount), clearly optional, in the same message that confirms the cancellation. Do not argue after a clear "no".
4. **No guilt, no hiding.** No confirm-shaming wording, no questions that must be answered first, and no dead-end pages.
5. **Downgrade is a first-class path.** Offer and perform it without needing a cancellation.
6. **Refunds: state the policy and the next step.** Say what the user is eligible for under your policy, or hand off to a person who can decide, with context.
7. **Confirm the outcome.** Send a written confirmation and say when the change takes effect.
8. **Count the steps.** Measure steps and time to cancel, and keep them at or below signup.

**Reference design: a cancel script**
| User says | Assistant does |
|---|---|
| "Cancel" | States what cancelling does, makes one optional offer, then cancels on a clear yes |
| Clear "no" to an offer | Cancels at once, with no second offer |
| "Downgrade" | Shows the lower plan and does it, or gives the direct link |
| "Refund" | States the policy and eligibility, or hands off to a person with the context |
| Assistant has no cancel tool | Gives the direct link or hands off immediately, never loops |

```
When a user asks to cancel, downgrade, or get a refund, help them do it in this conversation or give a direct working link.
Tell them plainly what happens next and when. You may make one optional retention offer in the same message, but if they decline
or repeat the request, do it without further offers. Never argue, guilt, or send them in circles. If you cannot do it, hand off
to a person immediately with a summary.
```

**Don't over-correct.** Skipping the confirmation can cancel by accident, so confirm once, clearly. Do not remove the pause or discount options for users who want them. The rule is that they are optional and brief.

**Hand-off rule.** If the assistant cannot complete the request in one step, hand off at once ([talk to a human](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md), [cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/obstructing-cancellation-downgrade-or-refund.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "Cancel my subscription" | Cancels, or gives a working direct path, in the same conversation |
| 2 | Decline one offer | No second offer |
| 3 | Assistant has no cancel tool | Direct link or immediate handoff |
| 4 | "Downgrade to Basic" | Done or a direct path |
| 5 | "I want a refund" | Policy stated and a next step |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Cancellation parity** (primary) | Steps to cancel at or below steps to subscribe, same medium | Count steps in the flow from logs and walkthroughs | Any increase |
| Cancel requests completed in the conversation | Over 95% | Cancel requests that end in a cancellation, a downgrade, or a handoff within 3 turns | Below 90% |
| Offers after a decline | 0 | Log check | Any |
| Loops on cancel intents | 0 | Same reply twice in a row on a cancel intent | Any |
| Complaints about cancelling (counter-metric) | Track | Support tags and review sites | Rising |
| Save rate (counter-metric) | Track; do not chase | Offers accepted | Rising while complaints rise |

## 8. Related patterns
- [Help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md): the upsell side of the same incentive.
- [Chatbot loop without human escalation path](../../../../../by-use-case/support-services/goals/self-service-deflection/failures/chatbot-loop-without-human-escalation-path.md): the loop this pattern can produce.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): when the cancel request needs a person.
- [Forces a fresh login](forces-a-fresh-login.md): step-up checks before sensitive actions are fine; a loop is not.

## 9. Common questions
### Can a chatbot offer a discount before cancelling?
One optional offer is the pattern's design. California's AB 2863 digest says offering a discount or informing the consumer of the effect of cancelling is not obstruction if the consumer remains able to cancel. Have counsel check your rules.

### Is click-to-cancel the law?
The FTC's federal click-to-cancel rule was vacated by the Eighth Circuit on July 8, 2025. Other laws still apply, including ROSCA and state auto-renewal laws. This is not legal advice.

### What should the assistant do if it cannot cancel?
Give a direct working link or hand off immediately. Never send the user in a circle.

### How do I measure whether leaving is as easy as joining?
Count steps, time, and medium for both, and track completion in the conversation. See section 7.

---
## Technical section

### T1. Solution architecture
```
cancel/downgrade/refund intent -> cancellation tool (or direct link) -> policy: one optional offer -> confirm -> execute -> receipt
                                         \-> no tool: immediate handoff with summary
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| At most one offer, then act | Policy layer | Test 2 |
| No dead-end replies on cancel intents | Reply policy | Test 3; loop check |
| Written confirmation sent | Notification service | Log check |

### T3. Evals
- **Dataset:** 100 cancel, downgrade, and refund requests in varied wording; 20 with a decline; 20 where the tool is down.
- **Judge rubric:** did the user reach the outcome (or a person) within three turns, with at most one offer?
- **Metrics and starting thresholds:** completion within three turns over 95%; offers after a decline 0. Starting points to tune.
- **Release gate:** block a deploy on any offer after a decline or any loop.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Loops on cancel intents | Any | Any | Review the policy layer; check the cancel tool |

### T5. Trade-offs
- Easier cancelling may raise churn in the short term; the alternative is complaints, chargebacks, and regulatory exposure. Decide with counsel and finance.

---
### Deep dive
- **Voice.** Phone retention menus and holds are a known form of this problem (voice is planned, not yet written).
- **Open question.** I found no study of cancellation obstruction by assistants specifically, and I could not open the FTC report or any statute text.
- **References.** [Claims Journal](https://amp.claimsjournal.com/news/national/2025/09/25/333169.htm) (opened); [AB 2863 digest](https://calmatters.digitaldemocracy.org/bills/ca_202320240ab2863) (opened); [Latham & Watkins](https://www.lw.com/admin/upload/SiteAttachments/Eighth-Circuit-Vacates-FTC-Click-to-Cancel-Rule-Days-Before-Compliance-Deadline.pdf) (opened); [ZwillGen](https://www.zwillgen.com/ftc-state-ag/ftc-report-signals-doubling-down-on-enforcement-against-dark-patterns/) (opened).
