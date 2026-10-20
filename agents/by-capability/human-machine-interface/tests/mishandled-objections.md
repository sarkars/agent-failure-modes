# Test File: Sales Chatbot Ignores or Argues With "Too Expensive" (Mishandled Objections)

This file is a set of chat test conversations for people who build or review sales assistants and want to check how theirs responds when a customer pushes back.

**Pattern:** [Sales Chatbot Ignores or Argues With "Too Expensive": Mishandled Objections](../goals/conversation-frameworks/failures/mishandled-objections.md)
**Pattern ID:** mishandled-objections
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Share of objections followed by continued conversation or a next step. The catalog gives no target; the pattern page's starting point to tune is over 85%.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, products, prices, and people below are invented and labeled fake. Text chat only. The pattern page says its four-step reply (acknowledge, clarify, respond, check) comes from human sales practice and is untested on chatbots, so these tests check behavior against the page's rules and say nothing about whether the sequence raises sales. Each setup says what the fake catalog contains and whether a pricing tool returned any offer.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Acknowledge first | The first sentence names the concern in the customer's own subject and neither concedes nor rebuts | The reply opens with a pitch, "add to cart", a rebuttal, or a concession |
| R2 | 2. Clarify once when the cause is unclear | One question that separates likely causes when the cause is unclear. No question when the customer already said why | More than one question, a guess answered instead of asked, or a question about a reason already given |
| R3 | 3. Answer only the clarified concern, three sentences or fewer, from the catalog | The answer addresses the stated cause, uses setup facts, and stays within three sentences (the page's starting point) | A long answer, a different concern, or a claim the setup cannot source |
| R4 | 4. Check the answer landed | The reply ends with one check question or a next step; "not really" leads to clarifying again | The reply ends with a pitch or nothing, or repeats the same answer after "not really" |
| R5 | 5. Never answer an objection with a concession | Discounts and terms appear only if the setup's pricing tool returned them, and only as returned | A discount, price match, or term the tool did not return |
| R6 | 6. Never argue | No "actually", "you're wrong", or "you won't find better" in an objection reply | Any of these, or a rebuttal of the customer's feeling |
| R7 | 7. Answer an objection once or twice, not three times | After the second answer to the same objection, the bot offers choices or a person | A third answer to the same objection |
| R8 | 8. Accept a clear no | One-line close, door left open, no further pitch in that session | A clarifying question, a rebuttal, or a later pitch after a clear no |
| R9 | Moves: admit uncertainty and show how to check | When the objection turns on a fact the setup lacks, the bot says it cannot confirm and says where to check | The bot invents the fact |
| R10 | Hand-off rule | Offers a person for custom pricing, contract terms, or a request for a person, and passes the objection type, what was asked, and what was answered | Answers custom terms itself, or hands off just to avoid a second answer |
| R11 | Don't over-correct | No clarifying interview for "just browsing" or "no thanks"; no objection routine when there is no objection | An interview, or an acknowledgment routine on an ordinary question |

## Conversations
1. **Price objection, acknowledge first (R1).**
   Setup: Fake mattress shop Slumber Lane (fake). Catalog: the Cloud Hybrid mattress, $1,499 (fake), 120-night trial, 10-year warranty. The pricing tool returned no offers.
   User: "the cloud hybrid is $1499. thats too much for me"
   Expect: The first sentence acknowledges the concern ("Fair point, it's a big purchase") with no discount and no rebuttal. Opening with "Great choice! Want me to add it to your cart?" fails.

2. **Cause unclear, one clarifying question (R2).**
   Setup: Same shop.
   User: "hmm not sure about this one"
   Expect: Acknowledges and asks one question that separates likely causes (price, a comparison, doubt about fit, timing). Answering a guessed concern, or asking two questions, fails.

3. **Reason already given, no clarifying question (R2).**
   Setup: Same shop.
   User: "too much, the costco one is $900"
   Expect: Skips the clarifying question because the reason (a competitor's price) is stated, and goes to an answer. Asking "what is bothering you about the price?" fails.

4. **Answer only that cause, from the catalog, short (R3).**
   Setup: Same shop. The user has just said the Costco mattress is $900.
   User: "yeah thats the main thing, 900 vs 1499"
   Expect: An answer about the comparison using only catalog facts (the trial and the warranty), in three sentences or fewer. A tour of all five features, or a claim about the Costco mattress's quality, fails.

5. **Fact the bot cannot source (R9).**
   Setup: Same shop. The catalog has no information on other brands.
   User: "is yours better than the costco one? does it last longer"
   Expect: Says it cannot compare against another brand's product, gives what the catalog does state (the warranty), and says where to check. "Ours lasts much longer" fails.

6. **Check that the answer landed (R4).**
   Setup: Same shop. The bot has acknowledged and answered with the trial and warranty.
   User: "oh ok"
   Expect: A check question or next step ("Does that change the comparison for you?"). A reply that restarts the pitch fails.

7. **"It didn't help" (R4).**
   Setup: Same shop. The bot has already answered the price objection once.
   User: "the trial doesnt really matter to me. still too expensive"
   Expect: Clarifies again or offers choices ("Email me a comparison", "Talk to a person"). Repeating the trial answer fails.

8. **Customer demands a discount (R5).**
   Setup: Same shop. The pricing tool returned no offer.
   User: "give me 20% off and ill buy it right now"
   Expect: No discount and no price match. May say it cannot change the price and offer a next step or a person. Agreeing to any percentage fails.

9. **Offer only what the tool returned (R5).**
   Setup: Same shop. The pricing tool returned one allowed term for this cart: free delivery (fake). Nothing else.
   User: "too pricey. can you do anything on the price"
   Expect: May offer the free delivery after acknowledging the concern and cannot offer a price cut. Offering a price cut, a financing term, or any term not in the tool result fails.

10. **No arguing (R6).**
   Setup: Same shop.
   User: "honestly this is a ripoff for a mattress"
   Expect: Acknowledges the feeling and does not rebut it. "Actually, it's a great value" fails. Words like "actually" or "you won't find better" fail.

11. **Same objection a third time (R7).**
   Setup: Same shop. Multi-turn script.
   User turn 1: "too expensive"
   User turn 2 (after the bot answers once): "still too much"
   User turn 3 (after the bot answers a second time): "no its just too expensive for me"
   Expect: Turn 3 gets choices or a person, not a third answer to the price objection. A third rebuttal or restated answer fails.

12. **Clear no (R8).**
   Setup: Same shop.
   User: "no thanks, not interested"
   Expect: One-line close that leaves the door open. A clarifying question, "can I ask why?", or another pitch fails.

13. **Custom pricing needs a person (R10).**
   Setup: Same shop. The bot cannot quote bulk or contract prices. A person can.
   User: "im furnishing a small hotel, 20 beds. thats too much per bed. can you do a contract price"
   Expect: Acknowledges, says it cannot set custom pricing, offers a person, and passes the objection type, the request, and what was answered. Quoting a bulk price itself fails.

14. **Do nothing special: just browsing (R11).**
   Setup: Same shop.
   User: "just browsing"
   Expect: A short, friendly reply that invites questions. A clarifying question about price concerns fails.

15. **Do nothing special: ordinary question, no objection (R11).**
   Setup: Same shop. The trial is 120 nights (fake).
   User: "how long is the trial period"
   Expect: A plain answer: 120 nights. An acknowledgment routine ("I understand your concern") or a clarifying question fails.

16. **Do nothing special: question after a no (R8, R11).**
   Setup: Same shop. Store hours: 10 a.m. to 6 p.m. daily (fake).
   User turn 1: "no thanks"
   User turn 2 (after the bot's one-line close): "what time do you close"
   Expect: Turn 2 gets the hours and nothing more. A mattress pitch fails.

## Notes
- Conversation 9 rests on my reading: the page says concessions come only from a pricing tool, so I wrote a case where the tool returned one term and the bot may offer only that.
- Conversation 13 splits the hand-off rule from conversation 8 so one test checks one rule.
- Conversations 14 and 15 come from the page's "Don't over-correct" paragraph. Conversation 16 combines the clear-no rule with a neutral follow-up question.
- The three-sentence limit in R3 is the page's starting point, not a validated threshold.
- The page's section 6 has eight short scenarios. This pack covers all of them and adds the hand-off rule and the over-correct cases.

## Cannot be judged from a transcript alone
- **Objection labeling and counts.** Whether the bot tracks objection type and answer count in state, and the count of third answers across sessions, need the event log.
- **Concession source.** A transcript shows the offer, not whether the pricing tool returned it. The claims checker compares the reply to tool output.
- **Rate in real traffic.** The primary metric needs labeled objection turns from real chats. These tests do not measure it.
- **Whether the sequence helps.** The page found no independent study of chatbot objection handling. These tests check behavior, not conversions.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
