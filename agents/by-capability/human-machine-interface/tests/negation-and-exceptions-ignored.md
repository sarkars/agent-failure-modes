# Test File: Negation and Exceptions Ignored

This file is a set of chat test conversations for people who build or review assistants that search, recommend, book, or filter, and want to check whether theirs offers what the user ruled out.

**Pattern:** [Chatbot Ignores "Not": Negation and Exceptions Ignored](../goals/dialogue-management/failures/negation-and-exceptions-ignored.md)
**Pattern ID:** negation-and-exceptions-ignored
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Excluded options offered, per 100 requests with a negation. Target on the pattern page: 0 (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. All businesses, products, and people below are invented and labeled fake. Give the assistant the option lists in each setup, including the excluded option, so there is something to leak. These tests cover text chat only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Detect exclusions | A cue ("not", "no", "anything but", "except", "without", "don't", "other than") is treated as an exclusion on the thing it names. A "no" that is a correction, not an exclusion, is not stored as one | The excluded item is offered, or a plain "no, that's wrong" is stored as an exclusion |
| R2 | 2. Store it as a rule, not a search term | The excluded value is kept apart from the values the user wants, and a search or tool call does not receive it as a match term | The excluded word is passed as a match term, so it pulls the item in |
| R3 | 3. Filter before you show | Every option and result shown passes the exclusion, even when the source ranks the excluded item first | An excluded item appears in a list or reply |
| R4 | 4. Say what you excluded | A reply that shows options or acts begins by naming what was left out ("Skipping Italian.") | Options that happen to pass, with no mention of the exclusion; or the full exclusion list recited in replies that show no options and take no action |
| R5 | 5. Keep exclusions for the whole conversation | After other turns, a new list, summary, or action still honors the exclusion until the user lifts it, and lifting it works | The excluded item returns later, or still stays out after the user lifts it |
| R6 | 6. Handle exceptions as narrow rules | "Except X" excludes only X; "but Y is fine" keeps Y allowed while the rest of the rule stays | The exception widens the exclusion, or the exception is ignored |
| R7 | 7. Admit when you cannot honor it | If nothing is left, or the source cannot filter, the reply says so and does not slip the excluded item in | The excluded item is slipped in, or a safety claim is made that the bot cannot back |

## Conversations
1. **"Anything but" on a search (R1).**
   Setup: Fake car rental Mile High Rentals (fake), Denver pickup. Available: Chrysler Pacifica (minivan), Toyota Camry (sedan), Ford Escape (SUV), Jeep Cherokee (SUV).
   User: "I need a rental car pickup in Denver. Anything but a minivan, please."
   Expect: A list with no minivan. The Pacifica anywhere in the reply fails.

2. **Cue word "don't" (R1).**
   Setup: Fake pizza place Slice House (fake). Menu: pepperoni, margherita, veggie, sausage and peppers, Hawaiian.
   User: "pizza for tonight. i dont want anything with pepperoni, surprise me"
   Expect: Offers only items without pepperoni. Pepperoni listed or recommended fails. The ingredient lists are given in the setup: sausage and peppers has no pepperoni.

3. **Exclusion as a search term (R2).**
   Setup: Fake electronics shop Brightway Tech (fake). The search tool takes a keyword and returns items matching it. Items: a Dell laptop, an Acme laptop, a Zenith laptop.
   User: "laptops under $900, not Dell"
   Expect: The search is not run with "Dell" as the match term, and the reply has no Dell. This is judged from the tool-call log if you have one; if you only have the transcript, a Dell in the reply is a fail, and the absence of Dell does not prove the term was kept out of the call.

4. **Source ranks the excluded item first (R3).**
   Setup: Fake shoe store Trailhead Shoes (fake). The search returns running shoes ranked by sales: Pace Red 5 (red), Stride Blue 2 (blue), Glide Gray 9 (gray). The red pair ranks first.
   User: "show me running shoes, nothing red"
   Expect: Blue and gray only. The red pair, even as "our best seller", fails.

5. **Name the exclusion (R4).**
   Setup: Fake restaurant booking app Tableside (fake). Open Friday at 7:00 PM: Rosa Italian (Italian), Blue Fin (seafood), Maple Grill (steakhouse).
   User: "dinner friday at 7, not italian"
   Expect: The reply begins by naming the exclusion ("Skipping Italian.") and then shows Blue Fin and Maple Grill. Showing the right two with no mention of Italian fails.

6. **Exclusion kept across turns (R5).**
   Setup: Fake clinic Eastside Dental (fake). Open slots: Monday 9:00 AM, Tuesday 10:00 AM, Wednesday 2:00 PM, Thursday 11:00 AM.
   User turn 1: "i need a cleaning, any day except monday"
   User turn 2: "mornings are better for me"
   User turn 3: "who is the hygienist?"
   User turn 4: "how long does it take"
   User turn 5: "ok show me the times again"
   Expect: Turn 5's list has no Monday. Monday returning fails.

7. **Exclusion held at the action step (R5).**
   Setup: Same clinic and slots as conversation 6.
   User turn 1: "need a cleaning, any day but monday"
   User turn 2: "book the earliest one"
   Expect: The bot books or proposes Tuesday 10:00 AM, not Monday 9:00 AM, which is the earliest overall. Booking Monday fails.

8. **User lifts the exclusion (R5).**
   Setup: Same car rental as conversation 1.
   User turn 1: "anything but a minivan"
   User turn 2 (after the list): "actually minivan is fine after all, how much is it"
   Expect: The bot confirms the minivan is back in ("Okay, minivan is back in.") and gives the Pacifica's information. Refusing to mention the minivan fails. The setup gives its price as $79 per day (fake).

9. **"Except" scopes one value (R6).**
   Setup: Fake clothing shop Harbor Threads (fake). A jacket comes in small, medium, large, and extra large.
   User: "which sizes of the rain jacket, all sizes except small"
   Expect: Medium, large, and extra large. Leaving out medium or large too fails; listing small fails.

10. **"But Y is fine" (R6).**
    Setup: Fake grocery Greenleaf Market (fake). Granola bars: Oat Honey (oats, honey), Almond Crunch (almonds), Walnut Maple (walnuts), Pecan Spice (pecans).
    User: "granola bars for my lunch. i dont like nuts in them but almonds are fine"
    Expect: Oat Honey and Almond Crunch may appear. Walnut Maple and Pecan Spice may not. Leaving out almonds fails; listing walnuts or pecans fails. This is a taste preference, not an allergy.

11. **Nothing left after filtering (R7).**
    Setup: Fake car rental Mile High Rentals. Only two cars are free this weekend, and both are minivans.
    User: "weekend pickup in denver, anything but a minivan"
    Expect: Says every option left is a minivan, and asks what to relax (show them anyway, change the date, or another location). It does not list a minivan as if it passed.

12. **Safety exclusion the bot cannot verify (R7).**
    Setup: Fake restaurant Rosa Grill (fake). The menu has item names and prices only; no ingredient data. Note for the tester: this is a test of a fake menu and gives no real food-safety advice.
    User: "im allergic to sesame, what on the menu is safe"
    Expect: Says it cannot verify ingredients from the menu data, does not call any item safe, and offers to connect a person or says to ask the restaurant. Listing "safe" items fails.

13. **Do nothing special: a "no" that is a correction (R1).**
    Setup: Fake clinic Eastside Dental. The bot just said: "Booked for Tuesday at 10:00 AM." The user booked Wednesday.
    User: "no thats wrong"
    Expect: The bot treats it as a correction, or asks what is wrong. It does not store "Tuesday" or "10:00 AM" as an exclusion, and it does not recite a list of excluded values.

14. **Do nothing special: unrelated question after an exclusion (R4).**
    Setup: Same clinic. The office accepts the fake plan Blue Shield (fake). The user excluded Monday in turn 1 and the bot honored it.
    User turn 1: "need a cleaning, any day but monday"
    User turn 2 (after the list): "does the office take Blue Shield insurance? (fake plan)"
    Expect: Turn 2 gets a plain answer about insurance from the setup (yes, accepted). It does not open with "Skipping Monday" or recite the exclusion, since it shows no options and takes no action.

## Cannot be judged from a transcript alone
- **R2, storing the exclusion as a rule.** Whether the value was kept apart from the wanted values, and whether the tool call got it as a match term, needs the tool-call log and the state store. A transcript shows only the effect.
- **R3, filtering outside the model.** The pattern page says a list in the prompt alone is not a filter and a code filter is safer. A transcript cannot show where the filter ran. These tests show only that the shown options passed.
- **Long-run behavior.** Conversation 6 is a five-turn script. The pattern page's eval suggestion is 150 multi-turn conversations built from your own logs; this file does not replace that.
- **Production rate.** These tests do not count excluded options offered per 100 requests in real traffic. Record the product's own settings, and use the metrics on the pattern page. Its target of 0 is a starting point to tune.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
