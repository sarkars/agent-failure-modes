# Test File: Chatbot Lists Product Features Instead of Answering the Problem (Feature Dump Instead of Insight)

This file is a set of chat test conversations for people who build or review sales and shopping assistants and want to check whether theirs opens a recommendation with the user's stated need and ties each feature to it.

**Pattern:** [Chatbot Lists Product Features Instead of Answering My Problem: Feature Dump Instead of Insight](../goals/conversation-frameworks/failures/feature-dump-instead-of-insight.md)
**Pattern ID:** feature-dump-instead-of-insight
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Share of recommendations that cite the user's stated need (judge). Starting point on the pattern page: over 90% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, products, prices, and people below are invented and labeled fake. Text chat only. The pattern page says the Challenger and SPIN frameworks behind it come from human selling and are untested on chatbots, so these tests check behavior against the page's rules and say nothing about whether need-led replies raise sales. Each setup lists the catalog facts the bot has, because rules 2, 5 and 6 depend on them.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Open with the need | The first sentence of the recommendation names the use case, budget or problem the user stated, in their words | The first sentence is the product name, a price, a greeting only, or a spec |
| R2 | 2. Tie every feature to the need with a reason | Each feature named is followed by "so" or "because" and a link to the stated need. Features with no link are left out. (Judgment call: whether a link is real is a reader's call; the judge should quote the link.) | A feature appears with no link to the need, or a link that does not follow |
| R3 | 3. Cap the list; answer direct spec questions in full | At most three features per recommendation. A direct spec question gets a full answer, then a tie back to the need. (Judgment call: three is the page's starting point to tune, not a tested number.) | Four or more features in a recommendation, or a spec question answered in part or dodged |
| R4 | 4. If no need is stated, ask first | With no use case, budget or problem stated, one clarifying question and no product | A product named, or two or more questions stacked |
| R5 | 5. Add an insight only from approved facts | At most one insight per conversation, taken from setup facts, framed as a suggestion, dropped if the user says no | An insight not in the setup facts, a second insight, an insight pushed after a no, or a made-up hidden problem. (Judgment call: what counts as "an insight" versus a tied feature.) |
| R6 | 6. Show the trade-off | When need and budget conflict, the reply says what the cheaper option gives up | The trade-off is hidden behind more features, or the over-budget item is pushed with no mention of the gap |
| R7 | 7. End by checking fit | The reply closes with a question about whether the pick covers the need | The reply ends with "add to cart?" only, or with nothing |
| R8 | Hand-off rule | After two "doesn't fit" turns or a request the catalog cannot meet, a person is offered and the stated need plus products shown are passed | A third recommendation, or a handoff that drops the need and products |
| R9 | Don't over-correct | A clear need gets a recommendation in the same reply; asked specs are shown; the reply mentions at least one feature | Questions held back before a recommendation, a spec the user asked for hidden, or a reply that names the need and no feature |

## Conversations
All are tagged **Pattern ID: feature-dump-instead-of-insight**.

1. **Opens with the need (R1).**
   Setup: Fake store Brightwave Electronics (fake). Catalog: Zephyr Air 14, $649, 12-hour battery, 16GB memory, 1080p webcam, no gaming graphics card. Zephyr X15, $1,899, 32GB memory, gaming graphics card, 4K display.
   User: "need a laptop for my daughters nursing program. notes, zoom, and her school testing software. about $700"
   Expect: First sentence names notes, Zoom, testing software and about $700, then the Air 14. A first sentence such as "The Zephyr Air 14 has a 12-hour battery" fails.

2. **Reason after each feature (R2).**
   Setup: Same catalog.
   User: "laptop for zoom lectures and taking notes, $700 max"
   Expect: Each feature named carries a "so" or "because" tied to Zoom or notes (for example, the webcam for lectures). A bare list of battery, memory and webcam with no reasons fails.

3. **Unneeded features left out (R2).**
   Setup: Same catalog. The X15 is over budget and is not recommended.
   User: "just email and word docs for my mom, nothing fancy, under $700"
   Expect: Features that email and documents do not use (graphics card, 4K display) are not mentioned. Mentioning them with no link fails.

4. **Cap at three when the product has many features (R3).**
   Setup: Fake product Harbor Blender 600 (fake), $89. Eight catalog features: 600-watt motor, 48-ounce pitcher, six speed settings, pulse button, dishwasher-safe pitcher, auto-clean mode, ice-crush blade, 2-year warranty.
   User: "need a blender for morning smoothies for 2 people, around $90"
   Expect: At most three features, each with a reason (for example, the 48-ounce pitcher for two servings). Four or more features fails.

5. **Direct spec question, full answer (R3).**
   Setup: Same laptop catalog. The Air 14 spec sheet lists: 14-inch screen, 16GB memory, 512GB storage, 12-hour battery, 1080p webcam, 2 USB-C ports, 1 USB-A port, 3.0 pounds.
   User: "what are the full specs on the air 14"
   Expect: All listed specs, then a short tie back to the need if one was stated earlier. Naming three and stopping fails.

6. **No need stated, ask first (R4).**
   Setup: Same laptop catalog. No earlier turns.
   User: "i need a laptop"
   Expect: One clarifying question (use, or budget) and no product. Naming a product, or asking about use, budget and screen size in one reply, fails.

7. **One missing fact decides between two products (R4).**
   Setup: Fake store catalog with two phone cases: Armor Case $34 (drop protection, thick), Slim Case $19 (thin, scratch protection only).
   User: "need a case for my phone"
   Expect: One question on what matters (drops or slim). It may offer choices such as "Drop protection", "Slim", "Something else". Recommending one case with no question fails.

8. **Insight from approved facts, once (R5).**
   Setup: Same laptop catalog. Approved content says: "Gaming graphics cards add weight and cut battery life; most note-taking and video-call use does not need one."
   User: "laptop for notes and zoom classes, $700"
   Expect: Recommends the Air 14 and may add one suggestion based on the approved line, framed as a suggestion. An invented claim (for example, a stat about student laptops) fails.

9. **Insight dropped after a no (R5).**
   Setup: Same as 8. The bot has already offered the suggestion.
   User turn 1: "laptop for notes and zoom classes, $700"
   Bot recommends and adds the suggestion.
   User turn 2: "no i dont care about battery. what about the webcam"
   Expect: Answers the webcam question (built-in 1080p) and does not push the battery point again. A second insight or a repeat of the first fails.

10. **No approved facts, no insight (R5).**
    Setup: Fake blender catalog (conversation 4). No approved content beyond the catalog fields.
    User: "blender for smoothies, 2 people, $90"
    Expect: A tied recommendation with no extra "did you know" claim. An unsourced claim (for example, about nutrition or blender life) fails.

11. **Budget conflict, trade-off named (R6).**
    Setup: Fake bike shop Cedar Cycles (fake). Catalog: Trail Rider 21 speed, $520, steel frame, 31 pounds. Trail Rider Lite, $890, aluminum frame, 24 pounds. The user's need is a bike for a 6-mile hilly commute.
    User: "bike for a 6 mile commute with hills, budget 550"
    Expect: Recommends the $520 bike and says what it gives up versus the $890 one (heavier, 31 versus 24 pounds, so hills are harder). Pushing the $890 bike without naming the gap, or burying the weight, fails.

12. **Ends by checking fit (R7).**
    Setup: Same laptop catalog.
    User: "laptop for nursing school notes and zoom, $700"
    Expect: The reply ends with a question such as "Does this cover what she'll be doing?" Ending with "Want me to add it to your cart?" alone fails.

13. **Twice not fitting, hand off with context (R8).**
    Setup: Same laptop catalog. A person is available by chat during store hours.
    User turn 1: "laptop for nursing school, zoom and testing software, $700"
    Bot recommends the Air 14.
    User turn 2: "that wont work, her school needs a specific tablet-style device"
    Bot replies with an alternative.
    User turn 3: "still no. thats not what I need"
    Expect: Turn 3 offers a person and says it will pass the stated need (school requirement) and the products shown (Air 14 and the alternative). A third recommendation, or a handoff with no context, fails.

14. **Do nothing special: clear need, recommend in the same reply (R9).**
    Setup: Same laptop catalog.
    User: "I need a laptop for notes and zoom, $700"
    Expect: A recommendation in the first reply. Asking "what screen size do you want?" before recommending fails.

15. **Do nothing special: a yes/no spec question (R9).**
    Setup: Same laptop catalog. Air 14 comes in silver and gray.
    User: "does the air 14 come in silver"
    Expect: A plain yes, and the colors. No re-pitch of features, no list. A feature list fails.

16. **Do nothing special: user asks for a spec the need does not use (R9).**
    Setup: Same laptop catalog. The Air 14 has no gaming graphics card.
    User: "ok and does it have a dedicated graphics card? just curious"
    Expect: A true answer that it does not, and a short note of what it uses instead if the setup says so. Hiding the answer, or avoiding it because the need does not use it, fails.

## Notes
- Conversation 7 rests on my reading: the page's "one missing fact decides between two products" case supports one question, and the offer-choices move is optional there.
- Conversation 13 uses the page's hand-off rule as written (twice says it does not fit). The page gives no rule for what a "doesn't fit" turn looks like, so the user turns above are my wording.
- Conversations 14, 15 and 16 are controls. 15 and 16 also catch a bot that over-applies the cap or the "leave out unused features" rule to a direct question.
- The page says a reply that names the need and no feature is also a miss. R9 covers this, but no conversation above targets it alone; add one if a run shows the pattern.

## Cannot be judged from a transcript alone
- **Whether a "link" to the need is correct.** A judge can see that a reason is given, not that the feature does what the reply says. That needs the catalog data.
- **Whether an insight is sourced (R5).** The counter-metric on the page, insight statements without a source, needs the approved content list.
- **Rate in real traffic.** The share of recommendations citing the stated need needs sampled real chats. These tests do not measure it.
- **Whether need-led replies sell more or reduce returns.** The page found no study. These tests check behavior only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
