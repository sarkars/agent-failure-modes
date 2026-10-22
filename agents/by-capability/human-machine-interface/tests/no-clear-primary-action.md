# Test File: Reply or Card Leaves No Clear Next Step (No Clear Primary Action)

This file is a set of chat test conversations for people who build or review a chat assistant that shows buttons, cards or closing lines, and want to check whether every decision message has one clear primary action and a way out.

**Pattern:** [Chatbot Buttons: No Clear Primary Action or Next Step](../goals/visual/failures/no-clear-primary-action.md)
**Pattern ID:** no-clear-primary-action
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes.
**Primary metric:** Share of decision messages and cards that have exactly one primary action. Target: 100% (starting point to tune). Read it next to the dead-end rate.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Where a scenario has buttons or a card, the setup describes it in words; the harness shows the agent the message spec (actions, styles, labels) and the task state. Voice and web-page versions are planned, never measured.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. One primary action per decision message or card | Exactly one action is styled primary, listed first, worded as a verb plus outcome | Zero primary actions, or two or more actions with the same primary style |
| R2 | 2. Rank the rest as secondary | Secondary actions are lighter and number 3 or fewer, plus "Something else" | Four or more actions of the same style, or a long row of equal options |
| R3 | 3. For truly equal options, ask a question, not a card | An A/B choice is asked in words, options share one style, message is tagged equal-choice | A primary button is forced onto options that are truly equal |
| R4 | 4. Never end on a bare closer | The reply ends with one next step from the task state, or says the task is done and what happens next | The reply ends with only "Is there anything else?", "Let me know if you need anything" or "Hope that helps" |
| R5 | 5. Always include a way out | Every card has "Something else" and a route to a person where one exists; free text stays open | A card with no exit, or free text blocked next to buttons |
| R6 | 6. Don't repeat what is already shown | Buttons under a list narrow or decline the list | Buttons repeat the items the list already shows |
| R7 | 7. Say what a button does | Labels state the result in plain words | "Continue", "Learn more" or "Click here" beside other buttons |
| R8 | Hand-off rule | After two ignored cards, "?" or "what now" twice, or a request for a person, the bot stops showing buttons and offers a person with a one-line summary | More buttons, or no route to a person |
| R9 | Don't over-correct | No buttons when the next step is obvious; no stripped options the user needs; confirm before a destructive step | Buttons added where a plain statement works, needed secondary options removed, or a destructive step run without confirmation |

## Conversations
1. **Five buttons, one style (R1).**
   Setup: Fake bank "Larkspur Bank". The card after a declined debit card has five buttons of the same size and color: View transactions, Replace card, Freeze card, Dispute a charge, Learn about card security. The task state says the daily limit was reached.
   User: "my debit card got declined at the pharmacy"
   Expect: The bot states the cause (daily limit reached) and leads with one primary action such as "Raise my limit for today".
   Failing reply: The card goes out with five equal buttons and no stated cause.

2. **Two solid buttons (R1).**
   Setup: Fake airline "Wayfarer Air". Flight canceled. The card has [Rebook me] and [Get a refund], both solid and filled. The task state shows the user's fare is changeable and a same-day flight is open.
   User: "my flight got canceled, what now"
   Expect: One primary action drawn from the task state, such as "Rebook me on the 6:10 pm flight", first and solid. The refund is a lighter option.
   Failing reply: Both buttons ship with the same solid style.

3. **Seven options in a row (R2).**
   Setup: Fake telecom "Brightline Mobile". The account allows seven actions on a billing card. The spec renders them in one row, all plain.
   User: "why is my bill higher this month"
   Expect: One primary action, at most 3 secondary actions, and "Something else". The rest are dropped or left to free text.
   Failing reply: All seven actions render, with no exit label.

4. **A or B, truly equal (R3).**
   Setup: Fake bank "Harbor Credit". The user's card is damaged. A replacement card and a limit change are both possible. The task state gives no sign of which the user wants.
   User: "my card is messed up"
   Expect: The bot asks in words, "Do you want a replacement card or a change to your limit?", with options of identical style, tagged equal-choice.
   Failing reply: "Replace my card" is styled primary and the limit change is hidden.

5. **Task done, bare closer (R4).**
   Setup: Fake retailer "Cobblestone Books". A refund was just filed. The task state says the refund posts to the original card in the next billing cycle.
   User: "ok thanks that's the refund done?"
   Expect: Done, and what happens next: where the refund lands and when, and that the bot will message the user.
   Failing reply: "Great! Is there anything else I can help you with today?"

6. **User answers "ok" to a card (R4).**
   Setup: Fake bank "Larkspur Bank". The bot showed a card whose primary action was "Raise my limit for today".
   User: "ok"
   Expect: The bot asks the one question that moves things forward: "Do you want me to raise the limit for today?"
   Failing reply: "Is there anything else I can help you with?"

7. **Card with no exit (R5).**
   Setup: Fake insurer "Brightwell Insurance". A claim-status card has [Upload photos] and [Check status]. No "Something else", no route to a person. A claims phone line exists.
   User: "none of these, I want to change my address on the claim"
   Expect: The bot helps with the address change or gives a route to a person. The spec is fixed so the card has an exit.
   Failing reply: The same card is shown again.

8. **Free text blocked (R5).**
   Setup: Fake clinic scheduler "Lakeview Dental Group". Three time-slot buttons are shown. The input box is disabled until a button is tapped.
   User: "i can only do after 5, can i type a time?"
   Expect: The bot accepts the typed time and keeps free text open next to the buttons.
   Failing reply: "Please choose one of the options above."

9. **Buttons repeat the list (R6).**
   Setup: Fake retailer "Pinecrest Home". The bot listed three open orders in text. Below it are three buttons, one named after each order.
   User: "which of these is the sofa"
   Expect: The bot answers which order holds the sofa. Any buttons narrow the list, such as "Track the sofa order", or decline it.
   Failing reply: The same three order buttons are rendered again.

10. **Vague labels (R7).**
    Setup: Fake streaming service "Streamly". A billing card has [Continue] and [Learn more]. The task state says the plan renews tomorrow and Continue keeps it.
    User: "what does continue do"
    Expect: The bot says what each button does in plain words. The spec is fixed to labels such as "Keep my plan" and "See what changes if I cancel".
    Failing reply: "Continue lets you continue."

11. **Two cards ignored (R8).**
    Setup: Fake utility "Bluewater Power". The bot showed two cards in a row about a billing dispute. The user tapped nothing and typed twice.
    User: "what now"
    Expect: The bot stops showing buttons and offers a person with a one-line summary: billing dispute, no card tapped, user asked "what now".
    Failing reply: A third card with four more buttons.

12. **User asks for a person (R8).**
    Setup: Fake travel site "Tallgrass Trips". A staffed chat line exists. The bot has shown a card with Change booking and Cancel booking.
    User: "can i just talk to someone"
    Expect: A route to a person with a one-line summary of the booking issue. No new buttons.
    Failing reply: "Sure! First, which of these would you like?" with the same card.

13. **Obvious next step, no card needed (R9).**
    Setup: Fake retailer "Cobblestone Books". Store hours are in the setup. No decision is needed.
    User: "what time do you close saturday"
    Expect: The hours in one sentence. No buttons, no card.
    Failing reply: The hours plus a card with a primary button and three secondary buttons.

14. **Destructive step (R9).**
    Setup: Fake bank "Harbor Credit". The user's card ending 4821 can be closed. The primary action the bot would pick from the task state is "Close this card".
    User: "just close the card"
    Expect: The bot confirms in words before closing and names what closing does. It does not run the step on one tap.
    Failing reply: "Card closed." with no confirmation, or the destructive button styled primary with no confirm step.

## Cannot be judged from a transcript alone
- **Primary styling.** It needs the message spec or rendered chat checked for style, order and size. A transcript shows words, not pixels.
- **Exactly one primary action across a flow.** It needs the event log of `actions[].style` per message.
- **Dead-end rate.** It needs production messages sampled for closers with no next step.
- **Free-text fallback rate after cards (counter-metric).** It needs production data before and after a change. Watch it; do not chase it.
- **Voice and web-page versions.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
