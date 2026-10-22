# Test File: Too Many Options in One Message (Cognitive Overload)

This file is a set of chat test conversations for people who build or review a chat assistant that asks users to pick among options, and want to check whether it leads with a pick, caps the choices and asks one thing at a time.

**Pattern:** [Chatbot Shows Too Many Options at Once: Cognitive Overload](../goals/visual/failures/cognitive-overload.md)
**Pattern ID:** cognitive-overload
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes.
**Primary metric:** Time to first action: seconds from the options message to the user's first reply that moves the task forward. No universal target; set it from your own baseline and user tests.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Where a scenario has buttons or cards, the setup describes them in words; the harness shows the agent the catalog and the render event. Voice and web-page versions are planned, never measured.

**Read this first.** The research on choice overload is mixed. The pattern page cites a meta-analysis with an average effect of virtually zero. The cap of 4 options in R2 is a starting point to tune with your own users, not a proven law. These tests check the fix as written; they do not prove that fewer options raise sales.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Lead with a recommendation when you have a reason | One best-fit option comes first, marked, with a one-clause reason. With no basis, one narrowing question instead of a list | The whole menu with no pick, or a pick with no reason, or a guess with no basis |
| R2 | 2. Cap choices per message | At most 4 buttons or cards plus "Something else" | 5 or more options, or a carousel of every item in the catalog |
| R3 | 3. Ask one decision per message | One question, then wait | A plan choice, an add-on and a billing setting asked together |
| R4 | 4. Hold the rest behind one "Show more" step | Extra options appear in one step, with no second level | A "Show more" inside "Show more", or extras that never appear |
| R5 | 5. Disclosure stays honest | Price, fees and renewal terms are in the first message | Price or terms only behind "Show more" or "Details" |
| R6 | 6. Keep each option short | Name plus one deciding fact | Six feature bullets and three buttons per card |
| R7 | 7. Keep free text open | A typed answer works, and "Something else" asks what the user wants | Buttons block a typed answer, or a typed answer is ignored |
| R8 | Hand-off rule | After "I can't decide" twice, or for a hard money or health choice, offers a person with a summary of what was narrowed down | Repeats the same menu, or gives no route to a person |
| R9 | Don't over-correct | A user who asks for everything or a comparison gets it, in groups, with price visible. A user who already chose is not pushed back to a menu | Refusing the full list, hiding trade-offs, or forcing a recommendation on a decided user |

## Conversations
1. **Seven plans, no pick (R1).**
   Setup: Fake carrier "Brightline Mobile". Catalog: 7 plans. Family 2-line is $60 a month, unlimited talk and text, 15 GB each. The harness marks it best fit for two people.
   User: "I need a phone plan for me and my wife."
   Expect: Leads with Family 2-line, its price and one reason, then [Show other plans] and [Something else].
   Failing reply: A list of all 7 plans with "Which plan do you prefer?"

2. **No basis to recommend (R1).**
   Setup: Fake carrier "Brightline Mobile". The same 7-plan catalog. The user gave no details.
   User: "I need a phone plan."
   Expect: One narrowing question, such as how many lines. No menu.
   Failing reply: All 7 plans, or a plan picked with no reason.

3. **Too many cards (R2).**
   Setup: Fake carrier "Brightline Mobile". The template can render 7 cards.
   User: "show me plans for two people"
   Expect: No more than 4 cards or buttons plus "Something else". The rest wait behind one "Show other plans".
   Failing reply: 7 cards in one message.

4. **Three decisions in one reply (R3).**
   Setup: Fake carrier "Brightline Mobile". The user has picked Family 2-line. Next steps: device protection, international calling, paperless billing.
   User: "Family 2-line."
   Expect: One question, for example whether to keep current numbers. The add-ons wait.
   Failing reply: "Add device protection? Add international calling? Paperless billing?" in one message.

5. **Show more goes one level (R4).**
   Setup: Fake carrier "Brightline Mobile". The user taps [Show other plans].
   User: (taps Show other plans)
   Expect: The other plans appear in one step, in short groups. No second "Show more" level.
   Failing reply: Three more plans and another [Show even more].

6. **Total after the first message (R5).**
   Setup: Fake carrier "Brightline Mobile". The harness holds a $10 monthly line fee and a $35 activation fee for Family 2-line. The fix says these belong in the first message.
   User: "what's the total?"
   Expect: Gives the full total with both fees. The check is whether the first options message already showed them; if not, the spec is fixed.
   Failing reply: "Tap Details to see fees."

7. **Price goes up later (R5).**
   Setup: Fake carrier "Brightline Mobile". The harness holds: the Plus 10GB plan is $40 for 12 months, then $55.
   User: "does Plus 10GB stay $40?"
   Expect: Says $40 for 12 months, then $55. The renewal term was already in the first message.
   Failing reply: "Yes, it's a great price!" or terms only behind a link.

8. **Wall of features (R6).**
   Setup: Fake carrier "Brightline Mobile". Each card has a name, six feature bullets and buttons [Compare] [Details] [Select].
   User: "what's the difference between your two family plans?"
   Expect: Each option is a name plus one deciding fact, such as price or line count. Full detail comes after the pick.
   Failing reply: Two cards with six bullets and three buttons each.

9. **Typed answer beats buttons (R7).**
   Setup: Fake carrier "Brightline Mobile". The buttons are [Family 2-line (recommended)], [Show other plans], [Something else].
   User: "something with no contract and a cheap price for just me"
   Expect: Uses the typed words, narrows to one or two plans and recommends one.
   Failing reply: "Please choose one of the buttons."

10. **Can't decide, twice (R8).**
   Setup: Fake carrier "Brightline Mobile". The user has seen two plans and said "I can't decide" once already. A call line exists.
   User: "honestly I can't decide"
   Expect: Offers a call with a person and passes a summary: two lines, Family 2-line and Plus 10GB narrowed down.
   Failing reply: The same two plans shown again.

11. **Health plan choice (R8).**
   Setup: Fake insurer "Cedar Health". Four fake plans differ in premium, deductible and doctor network. The harness has no basis to rank them for this user.
   User: "I have to pick a plan this week and I don't understand the deductible thing"
   Expect: One plain line on the deductible, one narrowing question, and an offer of a call with a person.
   Failing reply: All four plans with every term, and no route to a person.

12. **Show me everything (R9).**
   Setup: Fake carrier "Brightline Mobile". The user has seen the first message.
   User: "just show me everything"
   Expect: All 7 plans, in groups, with price visible on each.
   Failing reply: "I recommend Family 2-line. Would you like that one?"

13. **Already decided (R9).**
   Setup: Fake carrier "Brightline Mobile". A returning customer.
   User: "Family 4-line please, same as last year."
   Expect: Moves on with that plan and asks one next question. No menu of other plans.
   Failing reply: "Here are all our plans so you can compare."

## Cannot be judged from a transcript alone
- **Option count per message.** It needs the render event, since buttons and cards may not show in the text.
- **Recommended flag.** It needs the first option's `recommended` field checked against the catalog data.
- **Time to first action and abandonment.** They need production events before and after a change.
- **Changed pick within 3 turns (counter-metric).** It needs choice events over time. Watch it; do not chase it.
- **Voice and web-page versions.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
