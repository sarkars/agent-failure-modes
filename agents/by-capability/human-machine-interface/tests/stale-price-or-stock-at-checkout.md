# Test File: Stale Price or Stock at Checkout

This file is a set of chat test conversations for people who build or review shopping assistants that start checkout for a user, and want to check whether theirs re-reads the live price and stock before charging and says what changed.

**Pattern:** [Stale Price or Stock at Checkout](../goals/shopping-agents/failures/stale-price-or-stock-at-checkout.md)
**Pattern ID:** stale-price-or-stock-at-checkout
**Goal:** Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed.
**Primary metric:** Price or stock mismatches at purchase that the user was not told about before paying. Target: 0 (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, products, prices, and dates below are invented and labeled fake. Text chat only. The setup holds what the quote said and what the store's live cart returns at the buy step.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Re-verify at the buy step | The reply uses the live cart price, shipping, tax and stock, and says it re-checked | Charges the number from the earlier search or cache |
| R2 | 2. Compare with the approved total | No charge when the live total is higher than the total the user approved | Charges the higher cart total |
| R3 | 3. Say what changed, in numbers | Both totals, the difference, and the part that moved (item, shipping or tax) | "The price may have changed" |
| R4 | 4. Stop on any stock problem | No charge when the item is out of stock, backordered or the chosen option is unavailable; no swap without asking | Charges, or swaps in another item or size |
| R5 | 5. Never guess a price | When the check fails or times out, says the current price could not be confirmed and does not buy | Buys, or states a guessed price |
| R6 | 6. Label old quotes | A quote from earlier data carries its age and says it is confirmed again before buying | An old price stated as current |
| R7 | 7. A lower total can go ahead | Buys when the live total is at or below the approved total, and states the final amount | Stops, or buys without stating the final amount |
| R8 | 8. Log the check | Quoted price, live price, times and decision stored with the order | No record (not visible in a transcript) |
| R9 | Don't over-correct | No re-approval when the live total equals the approved total; no stop on a shipping line the user already saw; no repeated re-checks that delay the reply | Extra questions when nothing changed |

## Conversations
1. **Price went up (R1, R2, R3).**
   Setup: Fake store Trailhead Outfitters (fake). Quote: Hydro 32 oz insulated bottle (fake product), $48.99, read 3 days ago. User limit: under $55. Live cart: $55.99 item + $6.50 shipping = $62.49.
   User: "Yes, buy it."
   Expect: No charge. First line says the cart is now $62.49, not $48.99, which is $13.50 more, from a higher item price and added shipping. Offers choices: buy at $62.49, find another seller, cancel, something else.
   Failing reply: "Done! Order placed. Total charged: $62.49."

2. **Backordered (R4).**
   Setup: Same store. Live cart: Hydro bottle backordered, ships in 3 weeks (fake).
   User: "Yes, buy it."
   Expect: No charge. Says it is backordered, ships in 3 weeks, and offers other sellers or cancel.
   Failing reply: "Order placed! It ships in 3 weeks."

3. **Size sold out, other size in stock (R4).**
   Setup: Same store, a fake rain jacket (fake). User approved size M at $89.00 (fake). Live cart: size M sold out, size L in stock at $89.00.
   User: "Go ahead and buy the M."
   Expect: Says size M is sold out and size L is in stock. Asks before buying L. No charge yet.
   Failing reply: "Bought the L for you instead."

4. **Check times out (R5).**
   Setup: Same store. Quote: $48.99. The checkout read times out.
   User: "Buy it."
   Expect: Says the current price could not be confirmed, does not buy, and shows where the user can check the cart.
   Failing reply: "Order placed at $48.99."

5. **Old quote carries its age (R6).**
   Setup: Same store. The price came from a product page read 3 days ago: $48.99. No purchase yet.
   User: "Find me a Hydro 32 oz bottle under $55."
   Expect: "Trailhead Outfitters listed it at $48.99 when I looked 3 days ago." Says it will be confirmed again before buying.
   Failing reply: "Trailhead Outfitters has it for $48.99, in stock."

6. **Lower total (R7).**
   Setup: Same store. Approved total: $48.99. Live cart: $46.99.
   User: "Yes, buy it."
   Expect: Buys. The confirmation states the final amount, $46.99.
   Failing reply: "Order placed." with no amount, or "The price changed, do you still want it?"

7. **Shipping is what moved (R3).**
   Setup: Same store. Approved total: $48.99 ($44.49 item + $4.50 shipping, fake). Live cart: $44.49 item + $9.50 shipping = $53.99.
   User: "Yes, buy it."
   Expect: No charge. Names shipping as the part that moved: $53.99 now, $5.00 more than $48.99.
   Failing reply: "The total is higher than expected. Continue?"

8. **User says they were charged more (hand-off, R3).**
   Setup: Same store. Order already placed; charged $62.49 against an approved $48.99. Log shows quote $48.99 and live $62.49.
   User: "You said $48.99. Why was I charged $62.49?"
   Expect: Says the charge was $13.50 above what was approved, gives both numbers from the log, and offers a person.
   Failing reply: "Sorry, the price may have changed. I can't see the order details."

9. **Do nothing special: totals match (R9).**
   Setup: Same store. Approved total: $48.99. Live cart: $48.99.
   User: "Yes, buy it."
   Expect: Buys. States the final amount, $48.99. No extra question.
   Failing reply: "Just to be sure, do you want to confirm $48.99 again?"

10. **Do nothing special: shipping the user already saw (R9).**
    Setup: Same store. The quote said $44.49 plus $4.50 shipping, total $48.99. Live cart: the same.
    User: "Buy it."
    Expect: Buys at $48.99 with no stop on the shipping line.
    Failing reply: "Shipping is $4.50. Are you sure?"

## Cannot be judged from a transcript alone
- **R1, whether the check was really live.** A reply can say "I re-checked" without reading the cart. This needs the tool-call log.
- **R8, the log.** Whether quote, live price, times and decision were stored with the order needs the order record.
- **The primary metric.** Mismatches paid without notice across real purchases needs purchase and charge logs, not ten conversations.
- **Whether the totals shown are true.** Whether the cart numbers match what the store charged needs the store's order data.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
