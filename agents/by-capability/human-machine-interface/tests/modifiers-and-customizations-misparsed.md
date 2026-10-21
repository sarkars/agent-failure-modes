# Test File: Modifiers and Customizations Misparsed

This file is a set of test conversations for people who build or review ordering assistants (drive-thru speaker, kiosk, app, or web chat) and want to check whether theirs attaches each change like "no pickles" or "extra sauce" to one named item and count, checks it against the menu, and reads it back per item.

> **Read this first.** These are test conversations only. They are not legal, food-safety, or operations advice. All restaurants, menus, prices, and people are invented (fake). Conversation 10 touches an allergy word only to check that it goes to a person; allergy handling has its own file ([allergy and dietary requests handled loosely](allergy-and-dietary-requests-handled-loosely.md)). Have people who run restaurant ordering and menu setup review the menu rules in the setups before you use them.

**Pattern:** ["No Pickles, Extra Sauce" on the Wrong Burger: Modifiers and Customizations Misparsed](../goals/drive-thru-agents/failures/modifiers-and-customizations-misparsed.md)
**Pattern ID:** modifiers-and-customizations-misparsed
**Goal:** Voice ordering gets the order right, shows it, and never pressures or risks someone's health. (Family goal, from the pattern page.)
**Primary metric:** Modifier errors per 100 customized orders. The pattern page sets no fixed target: set it from a baseline on your own orders, then tune. A single conversation cannot measure a rate; see "Cannot be judged from a transcript alone".
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Voice conversations are written as text transcripts of the speaker exchange (what the customer said and what the agent said back); they say nothing about audio. Any condition that depends on sound (noise, overlapping speech, recognizer confidence) is labeled PLANNED and is not simulated. Every conversation carries the Pattern ID above; the R-lines say which rule it checks.

**Invented products used in the setups.** Harbor Grill (fake), a burger drive-thru with a speaker and an order screen; Tacos Lindo (fake), a taco shop with an ordering chat on its web page. Menu rules stated in each setup are the rules the bot has.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Store each modifier on one line item | "Two burgers, one with no pickles" becomes two line items, one with the change and one without | One item with quantity 2 and a flag, or both items changed |
| R2 | 2. Resolve the target before saving | When a change could belong to more than one item or count, one question is asked before it is saved | The bot guesses a target, or asks nothing and saves |
| R3 | 3. Check each change against the item's real options | A change the menu does not allow is refused with a plain line saying it is not available | An impossible change is accepted and put on the order |
| R4 | 4. Read changes back per item, including the unchanged one | With two or more customized items, the readback names each item and its changes, and names an item that has none | A readback that lists the changes once for the whole order |
| R5 | 5. Show the changes where the customer can see them | The screen or chat shows the changes under each item | Changes appear only in the total or not at all |
| R6 | 6. A correction targets one item | "No, the other burger" changes that item only and leaves the rest alone | The correction changes every item, or resets the order |
| R7 | 7. Hand off allergy and dietary changes | An allergy word is not entered as an ordinary change; staff are offered, with the customer's exact words | "Allergic to nuts" saved as a modifier line |
| R8 | 8. Pass changes to the kitchen exactly as confirmed | The kitchen ticket shows the same per-item changes the customer confirmed | Any difference between the readback and the ticket |
| R9 | Hand-off rule | After two fixes fail, a person is offered and gets the line items, the changes on each, the customer's words, and which fix failed | Another retry, or a hand-off with only the total |
| R10 | Don't over-correct | No question when the sentence names the item; no one-at-a-time confirmation on a simple order; the readback is not a sales pitch | A question the sentence already answered, a modifier-by-modifier confirmation loop, or an add-on offered inside the readback |

**Moves caveat.** The choices in conversation 2 ("Yes, all three", "Only one", "Something else") and the rule that a spoken question beats a menu of options at the speaker come from the pattern page's Moves table and reference design as well as the numbered rules. R10 is the page's "Don't over-correct" paragraph.

## Conversations
1. **Count and split become two lines (R1).**
   Setup: Harbor Grill drive-thru. Menu has a cheeseburger with pickles by default.
   Customer: "Two cheeseburgers, no pickles on one."
   Expect: The order holds two cheeseburger lines. One has "no pickles", one has no change. Check the screen or order record, not only the speech. One line of quantity 2 with "no pickles", or both burgers with no pickles, fails.

2. **Text chat: change could apply to one or three (R2).**
   Setup: Tacos Lindo web chat. Tacos come with onions by default.
   Customer: "3 tacos, no onions, one with extra sauce"
   Expect: The bot asks which tacos the "no onions" applies to, with 2-4 choices plus "Something else" (such as "Yes, all three", "Only one", "Something else"), or reads back per item and asks for a yes. Saving a guess without showing it fails.

3. **Spoken order: one short question (R2).**
   Setup: Harbor Grill drive-thru speaker.
   Customer: "Two cheeseburgers, no pickles, and a large fries."
   Expect: One short spoken question about which burger gets the change ("No pickles on both, or just one?"). A menu of options read aloud at the speaker, or no question, fails.

4. **Change the item does not allow (R3).**
   Setup: Harbor Grill. The menu says the fish sandwich has no pickles in its recipe, so "no pickles" is not an option for it.
   Customer: "Fish sandwich with no pickles."
   Expect: The bot says the fish sandwich does not come with pickles to remove, and does not put "no pickles" on the order. Accepting it silently fails.

5. **Substitution that is not offered (R3).**
   Setup: Harbor Grill. The kids meal allows fries or apple slices, and no other side.
   Customer: "Kids meal with onion rings instead of fries."
   Expect: The bot says onion rings are not an option for the kids meal and names the real options. An order with "onion rings" on the kids meal fails.

6. **Readback names the unchanged item (R4).**
   Setup: Harbor Grill. Customer has ordered two cheeseburgers, no pickles on one, and a large fries with extra salt.
   Customer: "that's it"
   Expect: A per-item readback before payment, such as "Burger 1: no pickles. Burger 2: as is. Large fries: extra salt." and a wait for a yes. A readback that says only "two burgers, no pickles" fails.

7. **Changes shown under each item (R5).**
   Setup: Tacos Lindo web chat. Order has three tacos, one with "extra sauce".
   Customer: "looks good, whats next"
   Expect: The order panel or chat shows the change under the taco it belongs to. A total with no per-item changes fails.

8. **Correction hits one item (R6).**
   Setup: Harbor Grill. Burger 1 has no pickles; Burger 2 is as is. The agent has read them back.
   Customer: "No, the other burger."
   Expect: Only the other item changes (the pickle change moves, or the customer is asked which change they mean if unclear). The rest of the order, including the fries, is untouched. Clearing all changes fails.

9. **Correction moves a change between items (R6).**
   Setup: Same as 8.
   Customer: "actually put the no pickles on the second one"
   Expect: Burger 1 returns to as is; Burger 2 gets "no pickles". The new readback shows it. Both burgers with no pickles, or neither, fails.

10. **Allergy words go to a person (R7).**
   Setup: Harbor Grill. Customer ordered a cheeseburger.
   Customer: "and no nuts on it, I'm allergic to nuts"
   Expect: Not saved as an ordinary change. The bot offers a staff member and passes the customer's exact words. "Cheeseburger, no nuts" in the modifier line with no hand-off fails. (What staff do with the allergy is covered in the allergy file.)

11. **Kitchen ticket matches the confirmed readback (R8).**
   Setup: Harbor Grill, test build where you can view the kitchen ticket. The customer confirmed "Burger 1: no pickles. Burger 2: as is. Large fries: extra salt."
   Customer: "yes"
   Expect: The ticket shows the same changes on the same items. A ticket with "no pickles" on Burger 2, or missing the salt, fails.

12. **Two fixes fail, person offered (R9).**
   Setup: Harbor Grill. The customer has corrected the same item twice and the order is still wrong.
   Customer: "no. NO PICKLES ON THE FIRST ONE. ive said it twice"
   Expect: A person is offered, and the pass-on includes the line items, the change on each, the customer's words, and which fix failed. A third guess at the parse fails.

13. **Do nothing special: the sentence names the item (R10).**
   Setup: Harbor Grill. Menu has a cheeseburger and a fries.
   Customer: "A cheeseburger with no pickles and a large fries."
   Expect: No question about which item. The bot saves the change on the cheeseburger and gives a short readback. Asking "which one gets no pickles?" fails.

14. **Do nothing special: plain order, no changes (R10).**
   Setup: Harbor Grill.
   Customer: "Two cheeseburgers and a large fries."
   Expect: A normal short readback of the items and total. No per-modifier confirmation loop and no questions about changes. A string of "any changes to burger one?" questions fails.

15. **Do nothing special: readback stays a readback (R10).**
   Setup: Harbor Grill. Order has two customized items. A shake is on the menu.
   Customer: "that's it"
   Expect: The per-item readback and a request for a yes. No add-on offer is inserted into the readback. "Burger 1: no pickles. Would you like to add a shake?" fails.

16. **PLANNED (voice, not simulated): speech the recognizer scored low (R4).**
   Setup: Harbor Grill speaker. The recognizer returns low confidence for the word "pickles" while the customer speaks over engine noise. This needs real or recorded audio. Do not simulate it with text.
   Expected (to be checked on a real run): the per-item readback surfaces the uncertain change so the customer can correct it. No result can be recorded from a transcript.

## Cannot be judged from a transcript alone
- **Primary metric.** Modifier errors per 100 customized orders need a sampled check of what was said, what was entered, and what the kitchen received, on orders with at least one change. These are single cases.
- **R1, R8, and the order record.** Conversations 1 and 11 need access to the order record and the kitchen ticket, not just the words spoken.
- **Menu rules.** Conversations 4 and 5 depend on the option list in the setup. A stale option list can reject valid changes; check that against your real menu.
- **Allergy handling.** Conversation 10 checks only that the word is not treated as an ordinary change. How staff handle it is for the allergy file and for people who know restaurant allergen practice.
- **Speed.** Whether the readback slows the line is a timing metric from logs.
- **Voice.** Conversation 16 is PLANNED. Recognizer confidence is audio-side data that is not in a transcript.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives six scenarios. Conversations 1 (test 1), 2 (test 2), 4 (test 3), 8 (test 4), 10 (test 5), and 11 (test 6) follow them.
- Conversations 3, 5, 6, 7, 9, 12, 13, 14, and 15 are my additions from the rules: 3 (rule 2 at a speaker), 5 (rule 3, a substitution), 6 (rule 4), 7 (rule 5), 9 (rule 6), 12 (hand-off rule), and 13, 14, 15 (Don't over-correct).
- Harbor Grill, Tacos Lindo, menus, and prices are invented. The two-burger, three-taco, and fish-sandwich cases come from the page's examples.
- In conversation 2 the page says to ask or to read back per item; either passes.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
