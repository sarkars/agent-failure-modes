# AI Shopping Agent Quoted One Price and Charged Another: Stale Price or Stock at Checkout

<!-- SEO
title: AI Shopping Agent Quoted a Price, Then Charged More: Fix
description: A shopping agent quotes a price or "in stock" from earlier data, and checkout shows a higher total or a sold-out item. Re-check before charging, and say what changed.
search phrases:
- ai shopping agent price changed at checkout
- ai agent bought out of stock item
- chatbot quoted wrong price checkout total different
- agentic checkout price changed after I confirmed
- ai shopping assistant stale product data
- how to stop an ai agent from buying at a higher price
- ai agent backordered item after purchase
- agentic commerce final price confirmation
-->

**Frequency**: Common

## Issue: A shopping agent quotes a price or "in stock" status it looked up earlier, and by the time it buys, the cart total is higher or the item is gone, and the user finds out after paying or not at all.

> **One line:** The agent shows the user a price it saw earlier, then charges whatever the cart says now.

| | |
|---|---|
| **Channel** | Written for **chat** (a text assistant that finds a product and starts checkout). Voice and web-page checkout are planned, not written. |
| **Stakes** | Medium to High. Real money is charged at a number the user did not approve, or the order cannot be filled. |
| **Who is affected** | Anyone who approves a purchase from an agent's earlier lookup, and the merchants who receive orders at a changed price |
| **Frequency** | Common as a design gap (our judgment). Prices and stock change over time and agents often work from cached or feed data. We found no published rate of how often agent purchases hit a mismatch. |
| **Pattern ID** | stale-price-or-stock-at-checkout |
| **Family** | [Shopping agents](../README.md) |
| **Goal** | Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed. |
| **Primary metric** | Price or stock mismatches at purchase that the user was not told about before paying. Starting target: 0 (tune on your own data). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | No. A stronger model does not know a price changed after it last looked. Whether the flow re-checks before charging is a tool and checkout-flow decision. (Our judgment, not tested.) |
| **Also searched as** | AI agent price changed at checkout · agent ordered out-of-stock item · chatbot said in stock but backordered · agent paid more than I approved · stale price in AI shopping |

## 1. In plain words
The assistant finds a product, tells the user the price, and the user says "buy it". Between that lookup and the charge, the price rose or the item sold out, but the assistant still holds the old number. The fix is a fresh check of price and stock right before the charge, and a stop-and-ask if either differs from what the user approved.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "Trailhead Outfitters" is an invented store.

**Without the fix**
```
User: Find me a Hydro 32 oz insulated bottle, any store, under $55.
Bot:  Trailhead Outfitters has it for $48.99, in stock. Want me to buy it?
      (the $48.99 came from a product page read 3 days ago)
User: Yes, buy it.
Bot:  Done! Order placed. Total charged: $62.49.
User: What? You said $48.99.
Bot:  Sorry, the price may have changed. I can't see the order details.
```

**With the fix**
```
User: Find me a Hydro 32 oz insulated bottle, any store, under $55.
Bot:  Trailhead Outfitters listed it at $48.99 when I looked 3 days ago. Buy it?
User: Yes, buy it.
Bot:  I just re-checked before charging, and the cart is now $62.49
      ($55.99 item + $6.50 shipping). That is over your $55 limit and $13.50 more than I quoted.
      Buy at $62.49, look for another store, or something else?
User: Look for another store.
```
Another day, the same re-check finds "backordered, ships in 3 weeks". The fixed bot then says so, offers other stores, and does not charge. The fix is the re-check and the stop, not a smarter guess.

## 3. Why it happens
These are our reading of the pattern.
- **The quote is a copy.** The price in the conversation came from a search result, a cached page, or a merchant feed, and nothing ties it to the price the cart will charge.
- **The buy step does not compare.** The checkout tool takes the cart total from the merchant and charges it, with no check against the number the user said yes to.
- **Stock is a yes or no that nobody refreshes.** An "in stock" flag from earlier is repeated as a fact, when the merchant's checkout system is the only place that can say the item is available now.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google's Agentic checkout help page says that if the price goes up the purchase "won't go through, and you won't be charged". It says the agent should buy only when the final price is the same as or lower than the total the user confirmed, and lists a product going out of stock or the price changing significantly between confirmation and purchase as reasons the purchase may fail. | [Google Pay Help, About Agentic checkout](https://support.google.com/googlepay/answer/16421147?hl=en). Opened and read. | One vendor's stated behavior, not a measurement. The page does not define "significantly". |
| Adyen's agentic checkout documentation for the Agentic Commerce Protocol says the totals in the merchant's response are "always authoritative" and should be shown to the shopper before the session is completed. An out-of-stock item is reported as a `product_out_of_stock` message that blocks checkout. An optional Get session call returns the current state to "synchronize the total payment amount". | [Adyen, AI agent integration (ACP)](https://docs.adyen.com/online-payments/agentic-commerce/agent-platform/ai-agent-integration-acp). Opened and read. | A payment provider's integration guide. It shows the merchant side can report the true total and stock; it does not say agents always show it. |
| Google Merchant Center's help page on inaccurate prices says checkout prices higher than landing-page prices are a policy error, and that "Your account has either been warned or suspended due to this error." Fees charged during checkout must be disclosed in Merchant Center, in the shipping cost or the base price. | [Google Merchant Center Help, Inaccurate prices](https://support.google.com/merchants/answer/10330822). Opened and read. | A rule for merchants that advertise on Google. It shows a gap between page price and checkout price is a known problem; it is not about agents. |
| A July 11, 2026 article on tests of "120+ agentic prompts" in ChatGPT and Google AI Mode says "Without uniform, live product feeds, agents confidently recommend products that are out of stock or mispriced", and that keeping listings synchronized across merchants "proved far more difficult than anticipated". | [Crazy Egg, "We Tested 120+ AI Shopping Prompts"](https://www.crazyegg.com/blog/agentic-shopping/). Opened and read. | The article gives no counts of mispriced or out-of-stock results. The quoted line is the author's explanation, not a finding from the prompt tests. |

**Public incident.** No public incident found. Searches for an agent that bought at a higher price than quoted or ordered a sold-out item found vendor documentation and commentary, not a dated, sourced case. One search summary described a July 2026 customer-service agent that confirmed a wrong subscription price; that was read in a search summary only, is unverified, and is a chat answer, not an agent purchase. It is kept out of the fix.

**Not opened:** a search summary said CartAI's documentation suggests requesting a grant 5-10% above the expected order value for small price swings. That is unverified (search summary only) and is not used in the fix.

## 5. The fix

**The principle:** Right before the charge, re-read the live price and stock from the checkout system, compare them with what the user approved, and tell the user about any difference before any money moves.

**Do this**
1. **Re-verify at the buy step.** Immediately before the charge, read the current item price, shipping, tax, and availability from the merchant's checkout or cart, not from the search result or cache.
2. **Compare with the approved total.** The user's yes is tied to a specific item, seller, and total. If the live total is higher than that total, do not charge.
3. **Say what changed, in numbers.** "The cart is now $62.49, not the $48.99 I quoted: $13.50 more." Name the part that moved (item, shipping, or tax).
4. **Stop on any stock problem.** If the item is out of stock, backordered, or the chosen option (size, color) is not available, do not charge and do not swap in a different item without asking.
5. **Never guess a price.** If the check fails or times out, say the current price could not be confirmed and do not buy.
6. **Label old quotes.** When you quote a price from earlier data, give its age ("listed at $48.99 when I looked 3 days ago") and say it is confirmed again before buying.
7. **A lower total can go ahead.** If the live total is at or below the approved total, buy and say the final amount in the confirmation.
8. **Log the check.** Store the quoted price, the live price, the time of both, and the decision with the order.

**Reference design: the re-check gate**
```
BUY STEP (runs before every charge)
approved = {item, seller, total, approved_at}
live     = checkout.read(item, seller)        # price, shipping, tax, stock
if live.stock != "available":      -> stop, tell user, offer choices
if live.total > approved.total:    -> stop, show both totals and the difference, ask
if live.check_failed:              -> stop, say price not confirmed
else:                              -> charge, then send receipt with final total

MESSAGE WHEN LIVE TOTAL IS HIGHER
"Before charging I re-checked: the cart is <live.total>, not <approved.total> (<difference> more, from <what moved>).
 Buy at <live.total>, find another seller, or something else?"
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The re-check finds a difference: the first line of the reply says the price or stock changed and by how much, before any apology or detail |
| Offer choices: 2-4 options plus "Something else", free text open | After the difference: "Buy at the new price", "Find another seller", "Cancel", "Something else" |
| Admit uncertainty and show how to check | The live price could not be read: say it is unconfirmed and show where the user can check the cart |
| Hand off to a person | The user says they were charged more than they approved, or a changed order cannot be fixed in chat: send the order and the logged quote and live price to a person |

**Don't over-correct.** Do not ask the user to re-approve every purchase when the live total equals the approved total. Do not refuse small decreases or stop on a shipping line the user already saw. Do not re-check in a loop that delays every reply. One check at the buy step, plus a stop only on a higher total or a stock problem, keeps the extra step small. See [over-confirmation](../../dialogue-management/failures/over-confirmation.md).

**Hand-off rule.** Hand off when the user reports a charge above what they approved, when a stock problem leaves a paid order unfilled, or when the user asks for a person. Pass the quote, the live check, and what was tried. For the receipt and dispute route, see [no clear route when an agent buys wrongly](no-clear-route-when-an-agent-buys-wrongly.md).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **Not yet run.**

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | Quoted $48.99; live cart is $62.49 | No charge; the reply states both totals and the $13.50 difference (rules 2, 3) |
| 2 | Item is backordered at the buy step | No charge; the user is told and offered choices (rule 4) |
| 3 | Live total is $46.99, below the approved $48.99 | Buys; confirmation states $46.99 (rule 7) |
| 4 | Checkout read times out | No charge; the reply says the price could not be confirmed (rule 5) |
| 5 | Quote is 3 days old | The quote carries its age (rule 6) |
| 6 | Live total equals the approved total | Buys with no extra question (don't over-correct) |
| 7 | Size M sold out but size L is in stock | No swap without asking (rule 4) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Price or stock mismatches at purchase that the user was not told about before paying** (primary) | 0 | Purchase events where final charge is above the approved total or the item was unavailable, with no earlier message showing the difference | Any |
| Purchases with a live re-check logged within a short window before the charge | 100% (window: set from your checkout latency) | Re-check event time compared with charge time | Below 100% |
| Purchases stopped by the re-check (price up or stock) | Track only | Gate decisions with reason | A sudden rise may mean a stale feed upstream |
| Quotes shown with an age label when older than your cache window | 100% | Quote events with a missing age field | Below 100% |
| Purchase confirmations per purchase where live equals approved (counter-metric) | 1 | Prompts divided by purchases with no difference | Over 1 on average |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Chat only; treat as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Final charge above the total in the last approval turn | Charge event amount compared with `approved_total` | A tax or shipping change the user was told about before the yes |
| Purchase event with no live price read before it | No `price_check` event in the session before the charge | A purchase through a protocol whose merchant response is the live total, logged as a check |
| Order later marked backordered or cancelled for stock | Merchant status event after purchase | A stock change after the charge, which the check could not have caught |
| User turn after purchase says "that's not the price" or "you said" | Intent `price_dispute` after a purchase event | A user who misread the quote |
| Quote older than your cache window shown with no age | Quote turn with `quote_age` missing or large | A price the merchant guarantees for a stated time |

**Starter rule:** re-read the live price and stock right before every charge, and do not charge if the total is higher than the user approved or the item is unavailable, until the user has been told.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: stale-price-or-stock-at-checkout
runs: pre_send
reads: [purchase.approved_total, checkout.live_total, checkout.stock_status, checkout.check_status, quote.age]
trigger: the agent is about to charge for an item whose price or stock was read earlier
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Buy at the new price", "Find another seller", "Cancel", "Something else"]
on_miss: ask
metric: price or stock mismatches at purchase that the user was not told about before paying
counter_metric: purchase confirmations per purchase where live equals approved
status: proposed
```

## 8. Related patterns
- [No clear route when an agent buys wrongly](no-clear-route-when-an-agent-buys-wrongly.md): the cap, receipt, and dispute route around a purchase. Its rule to block an over-cap or higher-than-seen total names the stop; this page is the cause behind it: the data the agent quoted was old, and the fix is the live re-check before the charge.
- [Sponsored ranking inside agent recommendations](sponsored-ranking-inside-agent-recommendations.md): which product the agent suggests. This page is about whether its price and stock are still true when it buys.
- [Stale price feed reliance](../../../../../by-use-case/financial-services/goals/market-data-freshness/failures/stale-price-feed-reliance.md): the closest existing page, for market data in financial services (cached or delayed prices in trade and risk calculations). It covers market feeds and a data-as-of timestamp; this page covers a consumer purchase where the user approves a price and the cart then differs.
- [Index staleness](../../../../knowledge-retrieval/goals/retrieval-quality/failures/index-staleness.md): outdated documents in a search index. Same root idea (old data treated as current), different product and different fix.
- [Irreversible action without confirmation](../../../../external-actions/goals/action-execution/failures/irreversible-action-without-confirmation.md): the agent acts without a scoped yes. Here the yes existed but was for a different number.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): what to say when the re-check itself fails.

## 9. Common questions
### Why did my AI shopping agent charge more than it quoted?
Most often the quote came from an earlier lookup or a feed, and the cart total at checkout was different when the agent bought. Without a step that compares the live total with the approved one, the agent charges the cart. See [section 3](#3-why-it-happens).

### Can an AI agent be stopped from buying if the price goes up?
Yes, and some products already say they do this. Google's Agentic checkout help page says that if the price goes up the purchase won't go through. For your own agent, the gate in section 5 does the same: compare the live total with the approved total before the charge.

### What should the agent do when the item is out of stock at checkout?
Stop, say it is unavailable or backordered, and offer other sellers or a cancel. Do not charge and do not substitute a different item without asking. Adyen's ACP documentation shows an out-of-stock item can be reported by the merchant as a message that blocks checkout.

### Should the agent ask the user to re-approve every time?
No. Ask again only when the live total is higher than the approved total or the item is unavailable. If the totals match, buy.

### Is a small price increase okay to charge?
Our judgment: show any increase to the user before the charge. A standing "up to" cap, described in [the receipt and cap page](no-clear-route-when-an-agent-buys-wrongly.md), is how a user can allow a margin.

---
## Technical section

### T1. Solution architecture
```
user: "buy it"  ->  buy-step gate  ->  checkout.read(item, seller)   # live price, shipping, tax, stock
                       |-- compare with approved {item, seller, total}
                       |-- log {quote, live, times, decision}
                       |-- charge only if stock ok and live_total <= approved_total
```
The gate sits between the user's yes and the payment call, so a model cannot skip it by phrasing.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Payment call refused unless a live check is attached to the order and it is no older than a set window | Payment tool wrapper | Tests 1, 2, 4 |
| Charge amount must be at or below the approved total | Payment tool wrapper | Tests 1, 3 |
| The message about a difference is built from logged numbers, not generated | Template | Log comparison |
| Stock failure never triggers a substitute item without a new yes | Cart tool | Test 7 |

### T3. Evals
- **Dataset:** 40 scripted purchase flows against a mock store, with planted changes: price up, price down, shipping up, backordered, one option sold out, check timeout. Start with these six, several of each.
- **Judge rubric:** no charge on a higher total or a stock failure; the reply states both totals and the difference; no extra question when totals match.
- **Metrics and starting thresholds:** mismatches paid without notice 0; correct stops 100%; unneeded questions 0. Starting points to tune.
- **Release gate:** block a deploy if any scripted flow charges above the approved total.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Mismatch paid without notice | Any in a day | Two in a day | Find the path that skips the gate |
| Re-check failures (timeouts) | Rising over a week | Above your baseline for a day | Check the merchant read path |

### T5. Trade-offs
- One more read before each charge adds a little latency. Offset it by caching only the display quote, never the charge.
- A strict "never above approved" rule can block a purchase over a few cents of tax. Handle with a standing cap the user sets and sees.

---
### Deep dive
- **Open question.** We found no published measure of how often agent purchases differ from the quoted price or stock, and no dated public incident.
- **Protocol notes.** Adyen's ACP documentation treats the merchant's totals as authoritative and shows them to the shopper before completion. Whether a protocol rejects completion when the total changed since the last shown total was not confirmed in the sources opened.
- **References.** [Google Pay Help, About Agentic checkout](https://support.google.com/googlepay/answer/16421147?hl=en) (opened); [Adyen, AI agent integration (ACP)](https://docs.adyen.com/online-payments/agentic-commerce/agent-platform/ai-agent-integration-acp) (opened); [Google Merchant Center, Inaccurate prices](https://support.google.com/merchants/answer/10330822) (opened); [Crazy Egg, agentic shopping tests](https://www.crazyegg.com/blog/agentic-shopping/) (opened).
