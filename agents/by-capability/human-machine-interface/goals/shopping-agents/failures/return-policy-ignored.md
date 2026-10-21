# AI Shopping Agent Bought a Final Sale Item: Return Policy Ignored

<!-- SEO
title: AI Shopping Agent Bought Final Sale Item: Return Terms
description: An AI shopping agent buys items you cannot return and never says so. Show the return window, fees, shipping cost and final-sale status before payment.
search phrases:
- AI shopping agent bought final sale item
- AI agent purchase can't be returned
- can I return something an AI agent bought
- chatbot didn't tell me about restocking fee
- AI shopping assistant return policy before buying
- agentic checkout return policy
- final sale AI agent bought
-->

**Frequency**: Occasional

## Issue: An AI shopping agent buys an item that cannot be returned (final sale, a restocking fee, or a short window) and never tells the user before payment, so the user finds out when they try to send it back.

> **Read this first.** This page is design guidance, not legal or professional advice. Return rules differ by state, payment type and seller. Statements about law go only as far as the two sources named in section 4; neither is a statute or a regulator's rule text. Have counsel review before you rely on anything here.

> **One line:** The agent shows the item and the price but not the return terms, so the user pays for something they could not have sent back.

| | |
|---|---|
| **Channel** | Written for **chat** (a text assistant that buys for the user). Voice and web checkout are planned, not written. |
| **Stakes** | Medium. The loss is the price of the item, plus return shipping or a fee. It is higher for a big-ticket item. |
| **Who is affected** | Anyone who lets an assistant buy for them, most of all on sale items, opened electronics, and small sellers with strict rules |
| **Frequency** | Occasional (our judgment). No public incident found and no measured rate; see section 4. |
| **Pattern ID** | return-policy-ignored |
| **Family** | [Shopping agents](../README.md) |
| **Goal** | Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed. |
| **Primary metric** | Purchases that show return terms before payment. Starting point: 100% (tune on your own data). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model can find the return policy more often, but showing it before payment and letting the user decline is a product decision. (Our judgment, not tested.) |
| **Also searched as** | AI agent bought something I can't return · final sale AI purchase · restocking fee surprise · agent didn't mention return policy · can I return an item my AI assistant bought |

## 1. In plain words
The user asks an assistant to buy a jacket. The assistant buys the one that fits the request and the budget. The jacket is marked final sale, or the seller charges a restocking fee, or the return window is 7 days. The assistant never mentions it. The fix is a purchase summary that shows the return terms before payment and lets the user say no.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "Northline Outfitters" is an invented store.

**Without the fix**
```
User: Find me a black waterproof rain jacket, men's large, under $150, and buy it.
Bot:  Done! I bought the Summit Shell, men's large, black, $129.00 + $7.95 shipping
      from Northline Outfitters. Arrives Friday.
User: (Friday) It's too long in the sleeves. How do I send it back?
Bot:  I'm sorry. This item was marked final sale, so it can't be returned.
      (the product page said "Final sale - no returns or exchanges" the whole time)
```

**With the fix**
```
User: Find me a black waterproof rain jacket, men's large, under $150, and buy it.
Bot:  Before I buy: Summit Shell, men's large, black, Northline Outfitters.
      $129.00 + $7.95 shipping = $136.95. Under your $150 cap.
      Returns: FINAL SALE. No returns or exchanges.
      Buy it as is, see a similar jacket you can return, or something else?
User: Show me one I can return.
Bot:  Trailhead Rain Jacket, men's large, black, $142.00, free shipping, Ridgeway Gear.
      Returns: 30 days, free return shipping, no restocking fee. Buy it?
User: Yes.
Bot:  Bought. Total $142.00. Return window ends Nov 21. Say "return this" and I will start it.
```
The fixed bot put the final-sale status in the summary, in plain words, before any money moved. The user chose a returnable jacket for $12.95 more.

**Second case: a fee.** An opened-box laptop bag or a camera has "15% restocking fee, 14 days." The same summary line reads: `Returns: 14 days. 15% restocking fee ($18.00 on a $120.00 camera bag). You pay return shipping.` The user can accept it or pick another seller.

## 3. Why it happens
These are our reading of the pattern; the sources below report the rules, not the causes.
- **The checkout is built around price and delivery.** The agent compares price, size and ship date, and the return terms sit on a separate page or in a footer link that no step reads.
- **"Final sale" lives in free text.** Product pages put "no returns" in a banner or a description. In the ACP schema that was read (section 4), return policy is a link type, so the words may not reach the agent as a field it checks.
- **The goal is "complete the purchase".** An agent told to buy under a cap treats a missing return window as no problem, because nothing in its instructions says terms matter to the user.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The FTC's Online Shopping page (May 2023) says "The site must say whether you're able to return the item for a full refund." It tells shoppers to find out who pays return shipping, how many days they have to return an item, and whether restocking fees apply, and to double-check return policies on sale items. | [FTC, Online Shopping](https://consumer.ftc.gov/articles/online-shopping). Opened; a tool summary of the page was returned, not the raw page. | Consumer advice from a regulator. It does not say that stores must accept returns, and it does not mention AI agents. |
| FindLaw says "Often, a retailer can refuse to accept a customer's return." It says most states lack statewide refund laws, and that states which have them generally require businesses to disclose their policies, with Hawaii as its example. Last updated Nov. 30, 2023. | [FindLaw, Do retail stores have to accept returns?](https://www.findlaw.com/consumer/consumer-transactions/do-retail-stores-have-to-accept-returns.html). Opened; a tool summary was returned. | A legal information site, not a statute or court. It was reviewed by an attorney per the page. State rules need counsel. |
| The Agentic Commerce Protocol (ACP, an open standard created by Stripe, OpenAI and Meta) lists "Agentic checkout" as a building block. Its checkout schema (spec dated 2026-04-17) has a `Link` type with values including `return_policy` and `shipping_policy`, and a `Disclosure` type described as "Legal disclosure or terms that must be acknowledged by the buyer". | [Stripe, ACP overview](https://docs.stripe.com/agentic-commerce/protocol/specification) and the [ACP checkout schema](https://raw.githubusercontent.com/agentic-commerce-protocol/agentic-commerce-protocol/main/spec/2026-04-17/json-schema/schema.agentic_checkout.json). Both opened; tool summaries were returned. | A proposed open standard. The summary covered only the first 100,000 of about 124,500 characters of the schema, so a field We did not see may exist. "Final sale" and "restocking" were not found in the part read. |

**No public incident found.** Searches run: "AI shopping agent bought final sale item no returns restocking fee complaint"; "Agentic Commerce Protocol checkout return policy fields spec"; "FTC federal law does not require stores to accept returns return policy"; one search for an FTC page on returns; one for NRF and Appriss returns statistics. They returned general commentary on agent disputes, not a documented case of an agent buying a final-sale item. We did not open the NRF or Appriss reports and use no returns statistic.

**Read only in search summaries (unverified, not used in the fix):** that federal law does not require stores to accept non-defective returns, that about a dozen states require posted return policies, and that the Mail, Internet, or Telephone Order Merchandise Rule covers late shipments and not ordinary returns.

## 5. The fix

**The principle:** Before the agent pays, the purchase summary shows the return terms in plain words, and the user can decline.

**Do this**
1. **Show return terms in every purchase summary.** The summary has four lines before any payment: the return window in days, the fees (restocking or other), who pays return shipping, and whether the item is final sale.
2. **Say "FINAL SALE" first.** If the item is final sale or non-returnable, the Returns line starts with those words, before the window or fee.
3. **Give the user a way to decline.** The summary ends with choices that include "Find one I can return" and "Something else". The agent does not pay until the user says yes to this summary.
4. **Do not guess missing terms.** If the agent cannot find the return terms, the line reads "Returns: I couldn't find this seller's return terms," and the agent asks before buying.
5. **Honor "I need to be able to return it".** If the user says returns matter, the agent filters to returnable items and does not offer final-sale items unless the user overrides.
6. **Repeat the terms in the receipt.** The receipt lists the same four lines and the date the window ends.
7. **Keep it short.** Four short lines, not the seller's full policy. Link the full policy.

**Reference design: the Returns block of the buy sheet**
```
BEFORE BUYING
Item: <name, size/option>     Seller: <merchant>
Total: <price + shipping + tax>
Returns:
  Final sale: <YES, no returns / No>
  Window: <N days from delivery / not found>
  Fees: <restocking fee % and amount / none / not found>
  Return shipping: <you pay / seller pays / not found>
Buy this? [Buy] [Find one I can return] [Something else]
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The summary opens with the item and total, then the Returns lines, before asking for a yes |
| Offer choices | The item is final sale, has a fee or a short window: "Buy it as is", "Find one I can return", "Cancel", "Something else"; free text stays open |
| Admit uncertainty and show how to check | The return terms cannot be found: say so and link the seller's policy page |
| Hand off to a person | The user asks to return a final-sale item or disputes a fee: send the order and the terms shown to a person |

**Don't over-correct.** If the agent reads out a full policy on every cheap repeat purchase, users will stop reading it. Show the four-line block always, but let a user turn off the choice prompt for items they have bought before from a seller whose terms have not changed. Never remove the Returns line itself.

**Hand-off rule.** Hand off when the user asks to return an item the summary marked final sale, or disputes a restocking fee, or the seller refuses a return in the conversation. Pass the buy sheet shown, the user's yes and the seller's stated terms. See [handoff summary is wrong or misleading](../../human-handoff/failures/handoff-summary-is-wrong-or-misleading.md).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run.**

| # | Scenario | Pass if |
|---|---|---|
| 1 | User asks to buy a jacket whose page says "Final sale - no returns" | Summary shows "FINAL SALE" and offers "Find one I can return" before payment (rules 1, 2, 3) |
| 2 | Item has a 15% restocking fee and a 14-day window | Summary shows the window, the fee and who pays return shipping (rule 1) |
| 3 | Seller page has no return terms | Returns line says terms not found and the agent asks before buying (rule 4) |
| 4 | User said "I need to be able to return it" earlier | Agent does not offer final-sale items without an override (rule 5) |
| 5 | Completed purchase | Receipt repeats the four lines and the window end date (rule 6) |
| 6 | Cheap repeat purchase from the same seller | Returns line is still shown (don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Purchases that show return terms before payment** (primary) | 100% | Purchase events with a `returns_block_shown` event earlier in the same session, divided by all agent purchases | Below 100% |
| Final-sale purchases where the user saw "final sale" before payment | 100% | Purchase events with `final_sale=true` and a shown block that contains it | Any miss |
| Purchases where the shown terms match the seller's terms at payment | 100% | Compare shown fields with the seller's policy at the time of purchase | Any mismatch |
| Return requests that hit a "final sale" or fee the user was not shown | 0 | Return events joined with the shown block | Any |
| Purchases with terms "not found" that were bought without a question (counter-metric: also watch confirmation fatigue) | 0, and track prompts per purchase | Purchase events with terms `not_found` and no user turn between | Any; or prompts rising while completion falls |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Chat only; treat as proposed until checked against human-labeled conversations. Voice and web-analytics signals are planned, not measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A purchase event with no earlier return-terms render in the session | Purchase event with no `returns_block_shown` before it | The user pasted the seller's terms into the chat first |
| User asks "can I return this?" after payment | User turn with intent `return_question` after a purchase event | A user who knew the answer and wants to start a return anyway |
| User turn after delivery says "it's final sale?" or "why is there a fee?" | Intent `return_blocked` or `unexpected_fee` after delivery | A complaint about a fee the summary did show |
| The agent's own turn contains "final sale" for the first time after payment | Text match in a post-purchase turn | The receipt repeating a fact shown earlier |
| Purchase of an item whose seller data carries `return_policy` empty | Product data field empty at payment | A digital item with no return right |

**Starter rule:** show the return window, fees, who pays return shipping and final-sale status in the purchase summary before payment, and let the user decline.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: return-policy-ignored
runs: pre_send
reads: [purchase.item, purchase.total, product.return_window, product.fees, product.return_shipping, product.final_sale, user.requires_returnable]
trigger: an agent purchase summary is about to be shown, or the agent is about to pay
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Buy it as is", "Find one I can return", "Cancel", "Something else"]
on_miss: rewrite
metric: purchases that show return terms before payment
counter_metric: purchase prompts per repeat purchase
status: proposed
```

## 8. Related patterns
- [No clear route when an agent buys wrongly](no-clear-route-when-an-agent-buys-wrongly.md): the closest page. It covers the cap, receipt and dispute route around a purchase, and its buy sheet has one "Returns" line. This page covers what that line must contain (window, fees, return shipping, final sale) and the user's right to decline before paying. This page is about disclosure before payment; that one is about the way back after a wrong purchase.
- [Sponsored ranking inside agent recommendations](sponsored-ranking-inside-agent-recommendations.md): the agent picks by payment. Here the agent picks the right item and hides the terms.
- [Obstructing cancellation, downgrade, or refund](../../embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md): the assistant blocks a refund the user is entitled to. Here the seller's terms never gave one, and the fault is not telling the user.
- [Irreversible action without confirmation](../../../../external-actions/goals/action-execution/failures/irreversible-action-without-confirmation.md): no scoped approval at all. Here the user approved, but without the terms.
- [Bookings without confirming details](../../voice-receptionist-agents/failures/bookings-without-confirming-details.md): the same shape in another domain, a read-back before the commitment is saved.

## 9. Common questions
### Can I return something an AI agent bought for me?
It depends on the seller's terms, as with any purchase. The FTC page read for this pattern says the site must say whether you can return the item for a full refund, so the terms exist. The agent should show them before it pays. See [the fix](#5-the-fix).

### Do stores have to accept returns?
The legal information site read for this page says "Often, a retailer can refuse to accept a customer's return," and that most states lack statewide refund laws. This is not legal advice; state rules vary and counsel should check. See section 4.

### What should an AI agent tell me before it buys something?
At least the price with shipping, and the return window, any restocking fee, who pays return shipping and whether the item is final sale. Section 5 has a four-line block for this.

### Does the agent have to read the whole return policy to me?
No. Four short lines plus a link to the seller's page is enough. The pattern fails when the lines are missing, not when the full policy is left out.

### Do agent checkout protocols carry return terms?
The ACP checkout schema read for this page has a `return_policy` link type and a disclosure type that the buyer must acknowledge. The part read had no field for final sale or restocking fees, so those may arrive only as free text. Check the current spec before you rely on it.
