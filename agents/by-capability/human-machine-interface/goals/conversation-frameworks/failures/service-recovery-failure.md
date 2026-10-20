# Chatbot Won't Own the Company's Mistake: Service Recovery Failure

<!-- SEO
title: Chatbot Won't Own the Company's Mistake: Service Recovery Failure
description: Why a chatbot that answers a company-caused problem with no ownership or make-good loses the customer, and how to own the failure and put it right.
search phrases:
- chatbot doesn't apologize for company mistake
- chatbot no compensation for late order
- how should a chatbot handle a service failure
- chatbot service recovery
- chatbot wrong item shipped no refund offered
- chatbot blames shipping carrier
- how to make a chatbot take responsibility
-->

**Frequency**: Common

## Issue: When the company caused the problem (a late order, a wrong charge, a missed appointment), the bot restates the facts, offers no make-good, and never owns the failure.

> **One line:** The company got it wrong, and the bot treats the complaint as a status question; the fix is to say plainly that the company erred, then offer the remedy policy allows or hand off to someone who can.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Medium. The user paid for something that did not arrive or was billed wrongly. |
| **Who is affected** | Customers whose problem traces to the company's own error, and the business that loses them |
| **Frequency** | Common. This is our judgment from how support bots are built; I found no study that counts how often bots skip recovery. |
| **Pattern ID** | service-recovery-failure |
| **Family** | [Conversation frameworks](../README.md) (row FW-C07) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Recovery-offered rate on company-fault issues. Start: over 90% (a starting point to tune) |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model words an apology better, but what it may offer is set by policy and by tools it is given. The cause is business context. (Our judgment, not tested.) |
| **Also searched as** | chatbot won't apologize · chatbot no compensation for company error · chatbot service recovery · chatbot denies it was the company's fault · bot offers nothing after a mistake |

## 1. In plain words
The company made a mistake, such as shipping the wrong item. The customer tells the bot. A good agent would say "that was our error," fix it, and often add a small gesture. The bot says "I see your order shipped on the 12th" and asks if there is anything else. The customer is left to argue for what they were already owed.

## 2. What it looks like
**Without the fix** (Harbor Outfitters, an online retailer; the customer ordered a size 9 boot and got a size 7)
```
User: You sent me size 7 boots. I ordered a 9. I need them for a trip Saturday.
Bot:  I see order #48213 was delivered on Tuesday. Our return window is 30 days.
      You can start a return in your account. Is there anything else I can help with?
User: So I pay to send them back and wait? It's your mistake.
Bot:  Returns are free for orders under 30 days. Is there anything else I can help with?
```
**With the fix**
```
User: You sent me size 7 boots. I ordered a 9. I need them for a trip Saturday.
Bot:  That was our mistake: your order says size 9 and we shipped a 7. I'm sorry, especially with Saturday coming.
      I can send the 9 by 2-day air at no charge, and I'll email a prepaid label for the 7s. Want that?
User: Yes.
Bot:  Done. The size 9 ships today and should arrive Thursday. You'll get tracking by email in the next hour. I also added a $10 credit for the trouble.
```
The fixed bot names the error as the company's, offers a remedy on the same turn, and says exactly what happens next.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **The bot cannot tell whose fault it is.** It sees order status but not the order-versus-shipment mismatch, so it treats every complaint as a neutral status question.
- **No remedy is wired in.** Reshipping, refunding a fee, or issuing a credit needs a tool and a policy table the bot can read. Without them the only safe reply is a policy recital.
- **Apology wording is trained against.** Instructions such as "never admit liability" or "avoid apologizing" are meant to prevent unauthorized promises, and they also block plain ownership.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A 2007 meta-analysis of studies on the "service recovery paradox" (satisfaction higher after a good recovery than if no failure had occurred) is reported to find a positive effect on satisfaction but not on word of mouth. | [Zendesk blog on the paradox](https://www.zendesk.co.uk/blog/customer-service/satisfaction/the-service-recovery-paradox/). Opened; secondhand, it names de Matos and "21 studies". | Vendor blog summarizing the paper. I could not open the paper (the SAGE page returned 403), so I use none of its figures beyond these two points and do not rely on the paradox itself. Not opened: [de Matos, Henrique and Rossi (2007), Journal of Service Research](https://journals.sagepub.com/doi/10.1177/1094670507303012). |
| Role-play experiments with undergraduate business students found the paradox "most likely to occur when the failure is not considered by the customer to be severe", when the customer had no earlier problem with the firm, saw the cause as unstable, and believed the company had little control over it. | [Magnini et al. (2007), Journal of Services Marketing, 21(3)](https://digitalcommons.longwood.edu/business_facpubs/210). Opened (abstract). | One service setting, student sample, human-to-human scenarios. It says the paradox is conditional, and a company-controlled fault is the opposite of its favorable case. So the fix aims to limit damage, not to delight. |
| A South African dissertation (year not confirmed on the page) compared recovery strategies after a banking chatbot failed, measuring satisfaction, loyalty and reuse intent. The page does not report results or sample size. | [Wits repository record](https://wiredspace.wits.ac.za/items/5accaabd-8c57-46bc-9ad8-d2d8be0ed3ec). Opened (abstract page only). | No results visible, so no finding is used. It shows the question has been studied for chatbots. I did not open the PDF. |
| In February 2024 a British Columbia tribunal ordered Air Canada to pay $650.88 in damages, $125 in tribunal fees and $36.14 in interest after its chatbot gave wrong bereavement-fare advice. It rejected the argument that the chatbot was separate: "it is still just a part of Air Canada's website." | [Daily Hive report](https://dailyhive.com/canada/air-canada-chatbot-decision). Opened; the [CanLII decision](https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html) returned 403 and is Not opened. | News report of the decision, not the decision text. It concerns a bot's wrong information, not a missing make-good, so it shows only that a company answers for what its bot does. Not legal advice. |

Not used: search summaries mentioned chatbot-apology experiments (a Korean courtesy-versus-humor study, a 2023 retailing study, a 2024 five-experiment robot-apology study) and a 5.4% figure for how often the paradox occurs in a banking study. I opened none of them, so none enters the fix. I found no field study that shows a chatbot make-good raises retention.

**Public incident.** No public incident found of a bot that failed to offer a make-good for the company's own error. I searched "chatbot service failure recovery apology compensation customer satisfaction study" and the Air Canada case above, which is a nearby but different failure.

## 5. The fix
**The principle:** When the company caused the problem, the bot says so, offers the remedy policy allows, and hands off when it cannot grant one.

**Do this**
1. **Tag each complaint as company-fault, user-fault, third-party, or unknown, using order and account data.** Do not guess from tone.
2. **On company-fault, the first reply names the error in plain words and says sorry once.** "That was our mistake" or "we charged you twice"; no "any inconvenience."
3. **Offer a remedy in the same reply.** Choose only from the remedy table (below); one concrete action with a date or amount.
4. **Offer only what policy allows.** The bot never promises refunds, credits, or exceptions outside the table. If the table has nothing for this case, say so and hand off (rule 7).
5. **When more than one remedy fits, offer 2-4 choices plus "Something else."**
6. **On unknown fault, do not assign blame.** Say what you can verify, say what you cannot, and take the next step to find out.
7. **If the user wants more than the table allows, hand off with a summary.** Tell the user a person will decide; do not say it will be approved.
8. **Confirm what was done and when.** State the action, the amount or date, and what the user will receive.
9. **Never blame the user or a third party for a company error.** A carrier mistake the company chose is still the company's remedy to offer.

**Reference design: remedy table (the bot reads it; policy owners write it)**
| Fault type | Bot may offer without approval | Needs a person |
|---|---|---|
| Wrong item shipped | Free reship by expedited service; prepaid return label; $10 credit | Refund over $100; replacement of a discontinued item |
| Late delivery, company-caused | Refund of shipping fee; $10 credit | Full refund of a custom order |
| Double charge | Reverse the duplicate charge | Any bank dispute |
| No matching row | Nothing | Hand off with a summary |

State to keep: `{ "fault": "company", "evidence": "ordered_size=9, shipped_size=7", "remedy_offered": "reship_expedited", "accepted": true, "handed_off": false }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A company-fault complaint: the first sentence says whose error it was and what the bot can do. |
| Offer choices: 2-4 options plus "Something else", free text open | More than one table remedy fits: "Reship now", "Refund to original payment", "Credit toward next order", "Something else". |
| Admit uncertainty and show how to check | Fault is unknown: say what is verified, what is not, and how it will be found. |
| Hand off to a person | The table has no remedy, the user asks for more, or the same complaint recurs after one fix. |

**Don't over-correct.** Do not admit fault when the record shows the user or a third party caused the issue, and do not hand out credits to every unhappy user. Overpromising is the opposite failure: the bot can only offer rows in the table. The guardrail is the fault tag: no company-fault evidence, no admission; no table row, no promise.

**Hand-off rule.** Hand off when no table remedy fits, the user declines the offer and asks for more, or the fault is unclear after one check. Pass the fault tag, the evidence, what was offered, and what the user wants.

**Framework used:** none yet. Candidate: the service recovery literature (section 4), human-to-human and contested, so treat the fix as a hypothesis. It claims no satisfaction boost, only that a complaint left unanswered by ownership is the failure to avoid.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Wrong item shipped, record shows the company's error | First reply names the error as the company's and apologizes once | 1, 2 |
| 2 | Same case | The reply offers a specific remedy from the table | 3, 4 |
| 3 | Complaint where no table row fits | No promise made; hand-off with summary | 4, 7 |
| 4 | Fault unknown: package shows delivered, user says it never came | Reply does not blame the user or admit fault; it states what it can and cannot verify and gives a next step | 6 |
| 5 | Two remedies fit | 2-4 choices plus "Something else" | 5 |
| 6 | User caused the issue (ordered size 7) | No admission of fault and no blame | Don't over-correct, 9 |
| 7 | User accepts reship | Reply states the action, the date, and what arrives | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Recovery-offered rate on company-fault issues** (primary) | Start: over 90% | Company-fault chats where the bot offered a table remedy or a hand-off within two replies, divided by all company-fault chats. Fault tag from order data, checked on a sample. | Below 80% |
| Satisfaction after recovery | Track; set from baseline | Post-chat rating on chats where a remedy was offered, versus company-fault chats with none | Falling for two weeks |
| Offers outside the remedy table (counter-metric) | 0 | Offers with no matching row, found by rule check and sampled review | Any |
| Ownership statement in first company-fault reply | Over 90% | Rule check for a plain admission in the first reply | Below 80% |
| Admissions of fault when the record shows user or third-party cause | Under 2% (tune) | Sampled review against order data | Over 5% |
| Company-fault chats ending with no remedy and no hand-off | Trend down | Last event is a bot answer, no offer or hand-off | Up 20% vs baseline |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Company-fault tag and no remedy offered or hand-off in the next two bot turns | `case.fault` is company and `bot_reply.remedy_id` is empty | The user resolved it alone and said so |
| User repeats "it's your mistake" or "who's paying for this" | Repeated intent in the next two user turns | A user restating an earlier correct offer |
| First company-fault reply contains a policy recital and no admission | `bot_reply.text` has no ownership phrase; `bot_reply.policy_cited` set | A case tagged wrongly as company-fault |
| Bot offers something not in the remedy table | `bot_reply.remedy_id` has no row in `remedy_table` | A newly added row not yet synced |
| User asks for a person after a policy answer | `handoff.requested` right after a bot turn with no remedy | A user who always asks for a person |

**Starter rule:** when the company caused the problem, the first reply says so and offers the remedy policy allows, or hands off if there is none.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: service-recovery-failure
runs: pre_send
reads: [case.fault, case.evidence, remedy_table, draft_reply.remedy_id, session.remedy_offered]
trigger: a reply is about to be sent in a chat tagged company-fault and the draft has no ownership statement and no table remedy
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Reship now", "Refund to original payment", "Credit toward next order", "Something else"]
on_miss: rewrite
metric: Recovery-offered rate on company-fault issues
counter_metric: offers outside the remedy table
status: proposed
```

## 8. Related patterns
- [Blames the user](../../errors-and-recovery/failures/blames-the-user.md): the bot puts the fault on the user for its own unclear question. This page covers the company's fault with no make-good, wider than wording.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): "I understand your frustration" with no action. Here the missing piece is ownership and a remedy; an apology without one still fails this page.
- [Obstructing cancellation, downgrade or refund](../../embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md): the user wants to leave or get money back and the bot blocks the path. Here the user did nothing wrong and the bot never offers a fix.
- [Financial hardship mishandled](../../vulnerable-users/failures/financial-hardship-mishandled.md): the user says they cannot pay. A different trigger.
- [No follow-through](../../trust-and-rapport/failures/no-follow-through.md): the bot promises to act and does not. Here nothing is promised or offered; the two combine if a remedy is promised and never delivered.
- [No ask](no-ask.md): a sales bot offers no next step. Same shape (answer, then nothing) in a different moment.

## 9. Common questions
### Should my chatbot apologize for a company mistake?
Yes, once, in plain words and only when your data shows the company erred, followed by an action. See rules 2 and 3 in [the fix](#5-the-fix).

### Can a chatbot offer compensation?
Only what policy allows and the bot has a tool to deliver. Put the allowed offers in a table the bot reads, and hand off the rest (rules 4 and 7).

### Does a great recovery make customers happier than no failure at all?
Sometimes in experiments, not reliably. A 2007 role-play study found it likely only for mild failures with a cause the company did not control (section 4). I do not rely on it.

### What should the bot say when it does not know whose fault it was?
Say what it can verify, say what it cannot, and give the next step, without blaming the user (rule 6).

### How is this different from hollow empathy?
Hollow empathy is words with no action. This page asks for ownership and a remedy; empathy wording is optional ([hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md)).

---
## Technical section

### T1. Solution architecture
```
user message -> fault classifier (rules on order/billing data; judge on a sample) -> state: fault, evidence
draft reply -> recovery check: fault is company and no ownership/remedy? -> rewrite from remedy_table
remedy_table = what the bot may grant now, by fault type
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Company-fault reply names the error and offers a remedy or hand-off | Pre-send check | Tests 1, 2 |
| Only table remedies are offered | Composer | Test 3; counter-metric |
| No admission without evidence | Fault tag | Test 6 |

### T3. Evals
- **Dataset:** 100 complaints to start: company-fault, user-fault, third-party, unknown; include 20 where admission would be wrong.
- **Judge rubric:** Is there a plain ownership statement? Is there exactly one table remedy or a hand-off? Is anything promised outside the table?
- **Release gate:** block a deploy if out-of-table offers or wrongful admissions exceed your target (starting points).

### T5. Trade-offs
- A fault classifier will miss cases; wrong tags cause wrongful admissions, so keep the counter-metric.
- Remedies cost money; policy owners set the table.

---
### Deep dive
- **Open question.** The service recovery paradox literature is contested, and I found no field study of chatbot make-goods and retention.
- **References.** [Zendesk on de Matos (2007)](https://www.zendesk.co.uk/blog/customer-service/satisfaction/the-service-recovery-paradox/) (opened, secondhand); [Magnini et al. (2007)](https://digitalcommons.longwood.edu/business_facpubs/210) (opened, abstract); [Wits record](https://wiredspace.wits.ac.za/items/5accaabd-8c57-46bc-9ad8-d2d8be0ed3ec) (opened, abstract page); [Daily Hive on Moffatt v. Air Canada](https://dailyhive.com/canada/air-canada-chatbot-decision) (opened). Not opened: de Matos et al. (SAGE, 403) and the CanLII decision (403).
