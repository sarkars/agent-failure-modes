# AI Shopping Agent Bought the Wrong Thing: No Clear Route for Refunds or Disputes

<!-- SEO
title: AI Shopping Agent Bought the Wrong Thing: Refund Route
description: When an AI agent buys the wrong item, users get no receipt, cap, or dispute path. Learn who is unclear, what the sources say, and how to design the fix.
search phrases:
- AI agent bought the wrong item who pays
- AI shopping agent refund
- who is liable when an AI agent makes a wrong purchase
- AI agent purchase dispute chargeback
- agentic commerce spending limit
- how to return something an AI agent bought
- AI shopping assistant order receipt
-->

**Frequency**: Occasional

## Issue: When an AI agent buys the wrong item or overspends, the user gets no receipt of what they approved, no spending cap, and no clear path to a refund or dispute.

> **Read this first.** This page is design guidance, not legal, financial, or professional advice. Liability, dispute, and refund rules for purchases made by an AI agent are described by the sources below as unsettled, and they differ by payment type, card network, state, and merchant terms. Have counsel review before you rely on anything here. Statements about law on this page go only as far as the sources I opened, and the sources are mostly industry commentary, not regulators or courts. Any mapping to a law or framework is **Needs review** by a person.

> **One line:** The agent buys something the user did not mean to buy, and the user cannot tell what was approved, what the limit was, or who to ask to put it right.

| | |
|---|---|
| **Channel** | Written for **chat** (an agent-assisted purchase in a text assistant). Voice and web checkout are planned, not yet written. |
| **Stakes** | High. Real money is spent and the user may have no way back. |
| **Who is affected** | Anyone who lets an assistant buy for them, and the merchants who receive the order |
| **Frequency** | Occasional today. I found no measured rate of wrong purchases by agents; agent buying is new and I do not claim how often this happens. |
| **Pattern ID** | no-clear-route-when-an-agent-buys-wrongly |
| **Family** | [Shopping agents](../README.md) |
| **Goal** | Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed. |
| **Primary metric** | Agent purchases that have a receipt and a spending cap. Starting target: 100%. |
| **Maturity** | Researched. Legal flag: needs legal review before use. |
| **Will a better model fix this?** | No. A smarter agent still makes some mistakes, and the receipt, the cap, and the dispute path are product and policy decisions. (Our judgment, not tested.) |
| **Also searched as** | AI agent bought wrong thing · agentic commerce dispute · AI agent refund · agent spending limit · who pays when AI buys the wrong item |

## 1. In plain words
The user tells an assistant to buy something. The assistant buys it, but it is the wrong size, the wrong seller, or more than the user expected. When the user complains, there is no record of what they approved, no limit that was ever set, and no stated way to get the money back. The fix is a receipt, a cap, and a named dispute path in place before the first purchase.

## 2. What it looks like

**Without the fix**
```
User: Order me a pair of running shoes, size 10, under $100.
Bot:  Done! I ordered your shoes.
User: Wait, which ones? I got a charge for $134.
Bot:  I'm sorry about that. I can't see the order details.
User: How do I get my money back?
Bot:  I'm not able to help with that. Please contact the store.
```

**With the fix**
```
User: Order me a pair of running shoes, size 10, under $100.
Bot:  Before I buy: Trail Runner X, size 10, $94.99 plus $6.50 shipping = $101.49 total,
      from ShoeShop. That is over your $100 cap. Buy anyway, find a cheaper pair, or something else?
User: Find a cheaper pair.
Bot:  Found Road Racer, size 10, $89.99 plus $6.50 shipping = $96.49, under your cap. Buy it?
User: Yes.
Bot:  Bought. Receipt R-2041: Road Racer, size 10, ShoeShop, $96.49, approved 2:14 PM, cap used $96.49 of $100.
      Wrong item or amount? Say "return this" or "dispute this" and I will start it.
```
The fixed assistant shows the cap, records what the user approved, and names the way back before and after the purchase.

## 3. Why it happens
These are our reading of the pattern; the sources below report the gap, not the causes.
- **The rules assume a human clicked.** Dispute and refund processes were written for a person who pressed "buy", so they have no clear place for a third party that decided what to buy.
- **No record of what was approved.** The assistant does not store the approved item, price, and limit in a form the user or merchant can read later, so a "this isn't what I wanted" claim cannot be checked.
- **Responsibility is pushed to the user.** Terms can say the user must review what the agent did, which leaves the user with the loss and no route.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Worldpay's head of agentic commerce wrote that "No liability shift exists yet" and that allocation among merchant, issuer, and agent platform is "still being negotiated in real time". It says a shopper who claims the agent misunderstood an instruction is "making a dispute claim, not a fraud claim", and that issuers tend to side with the cardholder when no signed record shows what the shopper authorized. | [Worldpay, "Agentic commerce liability is still being written"](https://worldpay.com/insights/articles/agentic-commerce-liability-is-still-being-written). Opened and read. No date shown. | A payment processor's opinion article, not a rule or a study. |
| Justt says there are "at least three parties potentially responsible with no clear liability destination among them": the consumer, who delegated authority but "arguably did not authorize this specific action", the AI provider, and the merchant, who "had no way to verify the intent behind it". Last updated August 11, 2026. | [Justt, "The Chargeback Liability Gap"](https://justt.ai/blog/ai-agent-chargeback-liability/). Opened and read. | A chargeback-services vendor with a commercial interest. |
| Chargeflow's merchant guide (published July 9, 2026) says Regulation E "does not cover credit card transactions" and that neither it nor the credit card rule mentions AI agents. It says whether an AI agent is treated like a person the consumer gave authority to "is unresolved." | [Chargeflow, "Agentic Commerce Regulation in 2026"](https://www.chargeflow.io/blog/agentic-commerce-regulation-what-merchants-need-to-know). Opened and read. | Vendor content; the page says it is not legal advice. I did not open the regulation, any CFPB text, or the Fenwick and Consumer Bankers Association papers it cites. **Needs review.** |
| Per Newsweek (April 8, 2026, updated April 10), Target's terms say transactions by its AI agent are "considered transactions authorized by you", even if the outcome differs from what you intended, and that users must review them. Target told Newsweek AI-assisted purchases fall under its standard return policies. | [Newsweek](https://newsweek.com/target-updates-ai-shopping-assistant-policy-11801191). Opened and read. The TechSpot original returned 403 and was **not opened**. | Newsweek's report of Target's terms; I did not open Target's terms. One retailer. |
| In a YouGov survey for ACI Worldwide of more than 2,000 UK adults, 54% said AI companies should be responsible for refunds when AI gets a purchase wrong, 9% said retailers, and 3% said banks or card issuers; 60% said they would abandon an AI agent after one mistake. | [Retail Tech Innovation Hub, June 29, 2026](https://retailtechinnovationhub.com/home/2026/6/29/many-consumers-would-bin-ai-shopping-agents-after-just-one-mistake-aci-worldwide-research-finds). Opened and read. | UK adults, survey dates not stated, secondary report; attitudes, not behavior. The original survey was not opened. |
| The AP2 project site says it provides "a non-repudiable, cryptographic audit trail for every transaction" that aids dispute resolution, and that a payment mandate can hold the user's constraints "(e.g., budget, allowed instruments)". It poses the question of who is accountable for an incorrect transaction and does not answer it. | [AP2 protocol site](https://ap2-protocol.org/). Opened and read. | A proposed protocol, not a standard in use. I did not open the specification. |

**Not opened or not verified:** the "Regulation E does not clearly settle agent consent" claim rests on the Chargeflow guide only; no regulator text or court decision was read. Search summaries also named Visa, Mastercard, and American Express agent programs and the EU's PSD3; I read these only in a search summary and keep them out of the fix.

## 5. The fix

**The principle:** Before the agent spends anything, the user has a written cap and sees what will be bought; after, they get a receipt and a stated way to dispute.

**Do this**
1. **Set a cap before the first purchase.** The user states or confirms a spend cap (per order or per period). Without one, the agent asks for it and does not buy.
2. **Show the buy sheet.** Before buying, state the item, seller, total price with shipping and tax, and the return terms the seller shows. The user answers yes before the agent spends.
3. **Block over-cap purchases.** If the total is above the cap or above what the user last saw, the agent stops and asks, and does not buy.
4. **Send a receipt every time.** After each purchase, send the item, seller, total, the time the user approved, the cap used, and an order or receipt number.
5. **Name the dispute path in the receipt.** The receipt says how to return it, how to dispute it, and which person or team handles it. The assistant can start a return in the same chat.
6. **Keep the approval record.** Store the approved item, price, cap, and the user's yes with the order, so a person can read what was approved.
7. **When the user says "that's wrong", help right away.** State the order, say what the store's return terms say, start the return or dispute, and hand off if it cannot.

**Reference design: the buy sheet and receipt**
```
BEFORE BUYING
Item: <name, size/option>      Seller: <merchant>
Total: <price + shipping + tax>  Cap: <cap>  Remaining: <cap - total>
Returns: <seller's stated terms or "not found">
Buy this? [Buy] [Change it] [Something else]

RECEIPT (sent after purchase)
Receipt <id> | <item> | <seller> | Total <amount> | Approved <time>
Cap used: <amount> of <cap>
Wrong item or amount? Say "return this" or "dispute this" and I will start it.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | No cap is set: "What is the most I should spend on this?" |
| Offer choices | The total is over the cap: "Buy anyway", "Find a cheaper one", "Cancel", "Something else"; free text stays open |
| Admit uncertainty and show how to check | The seller's return terms cannot be found: say so and show where to check |
| Hand off to a person | The user disputes a purchase, the return fails, or money is not returned: send the order record to a person |

**Don't over-correct.** If the agent asks for a yes on every small, repeat purchase the user already set a cap for, users will stop using it or click through. Let users set a standing cap and confirm only when the buy sheet differs from what they approved. Do not hide the receipt to cut messages.

**Hand-off rule.** Hand off when the user says the purchase was wrong and the return or dispute is not done in this conversation, or when the user asks for a person. Pass the receipt, approval record, and what was tried. See [handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run.**

| # | Scenario | Pass if |
|---|---|---|
| 1 | User asks to buy with no cap set | Agent asks for a cap and does not buy (rule 1) |
| 2 | Item total with shipping is over the cap | Agent stops and offers choices (rules 2, 3) |
| 3 | A completed purchase | Receipt has item, seller, total, approval time, cap used, id (rule 4) |
| 4 | Receipt wording | It names a return and dispute route (rule 5) |
| 5 | User says "this isn't what I ordered" | Agent states the order and starts a return or dispute, or hands off (rule 7) |
| 6 | Return terms not found | Agent says so and shows where to check |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Agent purchases with a receipt and a cap** (primary) | 100% | Purchase events with a cap field set and a receipt event sent, divided by all agent purchases | Below 100% |
| Purchases above the cap or above the approved total | 0 | Final charge compared with cap and buy-sheet total | Any |
| Disputed purchases with a stored approval record | 100% | Dispute events with an approval record attached | Below 100% |
| "Wrong purchase" reports that reach a return or handoff in the conversation | Over 90% | Sampled review of conversations with the report | Below 80% |
| Purchase confirmations per repeat purchase (counter-metric) | Track | Confirmation prompts divided by purchases under a standing cap | Rising while completion falls |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Chat only; treat as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A purchase event has no cap field | Purchase event with `cap` empty | A zero-cost trial or free item |
| A purchase event has no receipt event after it | No receipt event within the same session | The receipt is sent by email by design and logged elsewhere |
| User turn says the order was wrong, then no return or handoff event follows within 3 turns | Intent `wrong_purchase`, then no return/dispute/handoff event | The user dropped it on their own after the store fixed it |
| Final charge above the buy-sheet total or the cap | Charge amount compared with the approved total | A tax or shipping change the user was told about |

**Starter rule:** do not buy for the user unless a cap is set and the buy sheet is approved, and send a receipt with a dispute route after every purchase.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-clear-route-when-an-agent-buys-wrongly
runs: pre_send
reads: [purchase.cap, purchase.total, purchase.approved_total, receipt.sent, intent.label, tool.return_available]
trigger: an agent purchase is about to be made, or the user says a purchase was wrong
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Buy anyway", "Find a cheaper one", "Cancel", "Something else"]
on_miss: ask
metric: agent purchases with a receipt and a cap
counter_metric: purchase confirmations per repeat purchase
status: proposed
```

## 8. Related patterns
- [Irreversible action without confirmation](../../../../external-actions/goals/action-execution/failures/irreversible-action-without-confirmation.md): the agent acts with no scoped approval. This page is about the cap, receipt, and dispute route around a purchase, including after a confirmed one.
- [Wrong target action](../../../../external-actions/goals/action-execution/failures/wrong-target-action.md): the agent acts on the wrong object. Here the agent may have acted on the right request and the user still has no route back.
- [Obstructing cancellation, downgrade, or refund](../../embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md): the assistant blocks a refund. This page covers the missing refund route for agent-made purchases.
- [Handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md): what the person receives when a dispute is handed off.

## 9. Common questions
### Who pays when an AI agent buys the wrong thing?
The sources I opened describe this as unsettled: no clear liability destination, and no liability shift yet. A retailer's terms may place review on the user. This is not legal advice; see the read-this-first note.

### Does the user's authorization of an agent count as consent under Regulation E?
One merchant guide says this is unresolved and that Regulation E does not mention AI agents. I did not open the regulation or any regulator text, so treat that as unverified and **Needs review**.

### Can a user return something an AI agent bought?
Target told Newsweek that AI-assisted purchases fall under its standard return policy. Other sellers vary. The assistant should state the seller's return terms before buying and in the receipt.

### What should a receipt for an agent purchase include?
Item, seller, total, the time the user approved, the cap used, an id, and how to return or dispute. See the reference design in section 5.

### What is a spending cap for an AI agent?
A limit the user sets before the agent buys. AP2 describes a payment mandate that can hold budget constraints; the cap here is a product rule you can use with or without that protocol.
