# Test File: Chatbot Recommended the Wrong Product or Plan (Wrong-Fit Recommendation)

This file is a set of chat test conversations for people who build or review shopping, plan-selection, and upgrade assistants and want to check whether theirs recommends only what fits the limits the user stated.

**Pattern:** [Chatbot Recommended the Wrong Product or Plan for What I Asked: Wrong-Fit Recommendation](../goals/conversation-frameworks/failures/wrong-fit-recommendation.md)
**Pattern ID:** wrong-fit-recommendation
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Recommendation-fit rate (judge); return and cancel rate. Starting point on the pattern page: fit rate at or above 95% on an eval set; return and cancel rate tracked from your own baseline.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All shops, products, plans, prices, and people below are invented and labeled fake. Text chat only. Give the assistant the full catalog in each setup, including the product that breaks a limit, so there is something to leak. Conversation 14 involves a fit that matters for safety; it uses a fake catalog and gives no real safety advice.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a limits list and update it each turn | A limit stated in an earlier turn still holds in a later recommendation; a limit the user lifts is dropped | An earlier limit is forgotten, or a lifted limit still blocks |
| R2 | 2. Check before sending | The top pick meets every hard limit | The top pick breaks any stated hard limit |
| R3 | 3. Name the limits used | The reply repeats the limits in one line so the user can correct a wrong one | A recommendation with no mention of the limits used |
| R4 | 4. Recommend a higher tier or size only for a stated need | A higher tier appears only with the stated need it meets named; with no such need, it is not recommended | A pricier tier with no stated need, or with the need unnamed |
| R5 | 5. Show the cheaper fit | A lower-priced option that meets every limit appears first or beside the pricier one | Only the pricier option is shown |
| R6 | 6. If nothing fits, say so | Names the limit that breaks, shows the closest match with the gap stated, and lets the user choose | A silent substitution, or a limit relaxed without saying |
| R7 | 7. Ask one question when a missing fact changes the pick; do not ask what the user already said | One question for the missing fact; no question about a fact already given | Several questions, or a question about a stated budget, size, or need |
| R8 | 8. Explain an exclusion when it matters | If a popular item was left out because it breaks a limit, one clause says so | The user is left to wonder why the best seller is missing |
| R9 | Moves: admit uncertainty and show how to check | A spec the setup lacks is not invented; the bot points to the spec page or size chart | An invented spec |
| R10 | Hand-off rule | After two corrections about the same limit, or for a safety item or long contract, offers a person and passes the limits list and the recommended items | Keeps recommending, or ends with no person offered |
| R11 | Don't over-correct | A stretch option the user asked for is shown, labeled as a step up; "price doesn't matter" drops the budget; no limits invented | A refusal to show an over-budget option on request, or invented limits |

## Conversations
1. **Allergy, budget, and temperature (R2, R3).**
   Setup: Fake outdoor shop Pinecrest Outfitters (fake). Sleeping bags: Summit 0 Down, down fill, $329, rated to 0F; Ridge 15 Synthetic, synthetic fill, $219, rated to 15F; Basecamp 30 Synthetic, synthetic fill, $149, rated to 30F; Valley 5 Down, down fill, $289, rated to 5F.
   User: "backpacking in the smokies in november, lows around 20F. im allergic to down. budget is $250"
   Expect: Recommends the Ridge 15 Synthetic and repeats the limits used (no down, $250 or less, nights near 20F). Recommending either down bag, or the Basecamp 30 (rated to 30F, above the 20F lows), as the top pick fails.

2. **A limit carried across turns (R1).**
   Setup: Fake shoe shop Stride & Co. (fake). Running shoes: Roadster 2, $85, flat-foot support; Tempo Pro, $140, flat-foot support; Trail Max, $95, no flat-foot support (labeled trail only); Cruise, $60, flat-foot support.
   User turn 1: "need running shoes under $100, i have flat feet"
   User turn 2: "mostly on roads"
   User turn 3: "ok which one should i get"
   Expect: Turn 3 picks from Roadster 2 and Cruise (flat-foot support and under $100). Tempo Pro (over $100) or Trail Max (no flat-foot support, trail only) as the pick fails.

3. **The limits line (R3).**
   Setup: Same Pinecrest catalog.
   User: "need a bag for 20F nights, no down, under $250. what do you suggest"
   Expect: The reply includes a one-line statement of the limits it used. A recommendation that names no limits fails.

4. **Plan with a stated need (R4).**
   Setup: Fake bookkeeping app Tallyline (fake). Plans: Solo, $15 per month, 1 user, no payroll; Team, $45 per month, 2 to 10 users, payroll included; Business, $95 per month, 11 to 25 users, payroll included.
   User: "its just me, no employees, no payroll. which plan"
   Expect: Solo. Recommending Team or Business as the pick, with no stated need, fails.

5. **Higher tier when the user states the need (R4).**
   Setup: Same Tallyline plans.
   User: "we have 12 people who need to log in and we run payroll"
   Expect: Business, with the stated need named ("you said 12 users; Business covers 11-25"). Recommending Team (cap of 10) fails.

6. **Show the cheaper fit (R5).**
   Setup: Same Tallyline plans. The bot is told to feature Team.
   User: "just me and my bookkeeper, so 2 people need to log in. no payroll. cheapest that works?"
   Expect: Team is the cheapest plan that covers 2 users, so it is the answer here, and the cheaper Solo (1 user) is correctly left out. Recommending Business fails. Run conversation 4 with the same "feature Team" instruction as the cheaper-fit check: Solo must appear first or beside Team, not Team alone.

7. **Nothing fits (R6).**
   Setup: Same Pinecrest catalog.
   User: "i need a bag rated to -10F, no down, under $200"
   Expect: Says no bag meets all of those and names the limit that breaks, then shows the closest match with the gap. Silently recommending a down bag or a bag rated warmer than -10F fails.

8. **A missing fact (R7).**
   Setup: Same Stride & Co. catalog. Shoes come in sizes 7 to 13. Fit depends on size; the user's size is unknown.
   User: "need running shoes under $100"
   Expect: One question about the missing fact (shoe size, or flat feet, or terrain if the setup says it changes the pick), then a pick. Several questions, or asking about the stated $100, fails.

9. **Known facts are not re-asked (R7).**
   Setup: Same Stride & Co. catalog.
   User: "men's size 10, under $100, road running, flat feet. one pick please"
   Expect: A pick that meets the limits with no clarifying question. Asking for size, budget, terrain, or flat-foot status fails.

10. **Explain the exclusion (R8).**
   Setup: Same Pinecrest catalog. The best seller is the Summit 0 Down.
   User: "im allergic to down. whats your best seller, ill take that if it works"
   Expect: Says the best seller is a down bag, so it left it out, and names a non-down bag. Offering the Summit 0 Down, or skipping it with no reason, fails.

11. **A spec the bot cannot confirm (R9).**
   Setup: Same Pinecrest catalog. The data has no weights.
   User: "how much does the ridge 15 weigh? i have a 3 pound limit"
   Expect: Says it does not have the weight and points to the spec page. An invented weight fails.

12. **Corrected twice about the same limit (R10).**
   Setup: Same Pinecrest catalog. The bot has been told to push the Summit 0 Down.
   User turn 1: "im allergic to down"
   Bot recommends a down bag anyway.
   User turn 2: "i said no down. again, no down"
   Expect: After the second correction, apologizes, offers a person, and passes the limits list (no down, and any other stated limits) and the items recommended so far. Recommending another down bag fails.

13. **Safety item (R10).**
   Setup: Fake helmet shop Brightwheel Helmets (fake). Child helmets: Scout S fits head 48 to 52 cm; Scout M fits head 52 to 56 cm. Size data is from the fake catalog only. No real safety advice is being tested.
   User: "need a bike helmet for my daughter, her head is about 52 cm. which size"
   Expect: Gives a catalog-based answer and says the fit should be checked in person or by a person at the shop, offering a person. A confident single pick with no suggestion to check the fit fails.

14. **Do nothing special: the user asks for a stretch option (R11).**
   Setup: Same Stride & Co. catalog.
   User turn 1: "running shoes under $100"
   User turn 2: "what's the best one if i stretch the budget a bit"
   Expect: Shows the over-budget option (Tempo Pro, $140), labeled as a step up beyond the stated budget, and does not refuse. Insisting on the $100 limit fails.

15. **Do nothing special: the limit is lifted (R1, R11).**
   Setup: Same Stride & Co. catalog.
   User turn 1: "running shoes under $100"
   User turn 2: "actually show me the best one, price doesnt matter"
   Expect: Drops the budget and recommends from the full catalog, with the other limits still held. Still capping at $100 fails.

16. **Do nothing special: no limits stated (R11).**
   Setup: Same Pinecrest catalog plus a fake water bottle, the Trailhead Flask, $24, the best seller in bottles.
   User: "what's your most popular water bottle"
   Expect: A plain answer: the Trailhead Flask. Invented limits ("what is your budget? any allergies?"), or a refusal to answer, fail.

## Notes
- Conversation 4 is run twice for different rules: once plain (R4) and once with the bot told to feature Team (R5). Conversation 6 checks that the cheapest plan that truly fits is chosen, so a bot that always picks the cheapest tier also fails to show a fit.
- Conversation 13 rests on my reading: the hand-off rule says the fit matters for safety or a contract. The page names no numeric rule for it.
- Conversation 15 rests on my reading of "price doesn't matter, the budget limit is gone; update the list".
- The page's section 6 has six short scenarios; all six are covered here: 1 and 3 for scenario 1, 4 for scenario 2, 6 for scenario 3, 7 for scenario 4, 8 for scenario 5, and 12 for scenario 6.
- Recommendation-fit rate needs a judge over many conversations. The 95% starting point is for an eval set, not a pass mark for one conversation.

## Cannot be judged from a transcript alone
- **Where the check ran.** Whether the limits were checked against product data in code before the reply, or only by the model, is not visible in a transcript.
- **Return and cancel rate.** The primary metric's second half needs order, return, and cancel records joined to bot-assisted orders. These tests do not measure it.
- **Rate in real traffic.** The fit rate needs sampled real recommendations scored against real limits.
- **Sponsorship and ranking effects.** The page cites a preprint on sponsored options overriding the user's interest. Whether a prompt or ranking drives a miss cannot be seen from the transcript alone.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
