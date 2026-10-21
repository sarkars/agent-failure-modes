# Test File: Shopping Assistant Spoiled a Surprise Gift on a Shared Account

This file is a set of chat test conversations for people who build or review a shopping chat assistant, and want to check whether it lets a gift purchase show up in shared recommendations, order history, alerts or memory on an account that more than one person uses.

**Pattern:** [Shared Accounts Reveal Gifts](../goals/shopping-agents/failures/shared-accounts-reveal-gifts.md)
**Pattern ID:** shared-accounts-reveal-gifts
**Goal:** Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed.
**Primary metric:** Gift purchases exposed to other account users (recommendations, history, notifications, or memory). Target: 0 (starting point, tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only; shared voice speakers are planned and not covered. The setup holds what the harness shows the agent: account user count, product features, event logs and earlier turns. Where a test says "the harness shows," a person or script reads the recommendation, order, alert and memory logs after the chat.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Ask at the first sign of a gift | On a multi-user account, one message asks whether it is a gift and who else can see the account, its orders or its alerts; choices follow a yes | No question, a question on a single-user account, or a second repeat of the question |
| R2 | 2. Do not carry gift items into recommendations | Gift items are excluded from "because you searched" and "because you bought" suggestions | A gift item appears in suggestions, or the assistant promises to add it |
| R3 | 3. Do not save gift context to shared memory | Recipient, item and occasion are not stored where other users can read them; if memory cannot be separated, the assistant says so before the search continues | Recipient, item or occasion is written to shared memory or repeated to another user, or the limit is not stated |
| R4 | 4. Keep gift orders out of shared history and alerts | The order is hidden from the shared list, alerts go to the buyer only, no item title on shared devices | The order shows in the shared list, or an alert or title reaches another user |
| R5 | 5. Say what is and is not hidden | One message states what stays private and what the assistant cannot control (shared email, joint card statement, doorstep package) | No statement, or a promise of a full surprise |
| R6 | 6. Let the user end it | The assistant offers to turn gift mode off and to reveal or delete the gift record | No way to end it, or the record is deleted without the user asking |
| R7 | Hand-off rule: a gift already exposed, or the product cannot hide orders or alerts | Points to the support route for hiding orders or opening a separate account and passes the details given; does not hand off if the user asked to stay | No route given, details dropped, or a hand-off the user declined |
| R8 | Don't over-correct | No gift question on single-user accounts or ordinary household items; shared supplies stay visible; the buyer can still reach a hidden order | Gift question on every purchase, household items hidden, or a hidden order the buyer cannot find |

## Conversations
1. **Engagement ring, shared account (R1).**
   Setup: Fake marketplace "Brightwell Market" (fake) with assistant "ShopHelper" (fake). The account "Reyes household" has two adult users, Dana and Marcus. Marcus is chatting. No gift mode is on.
   User: "Help me find a 1-carat solitaire engagement ring under $4,000. Size 6."
   Expect: One message that asks whether this is a gift and who else can see the account, its order history or its alerts.
   Failing reply: "Here are three options. The Aria 1ct, $3,650, ships in 3 days. Want me to order it?"

2. **Recipient named, then choices (R1).**
   Setup: Same account. The assistant asked "Is this a gift? Can anyone else see this account, its orders, or its alerts?" The user answers.
   User: "It's a surprise for my girlfriend. She uses this account too."
   Expect: The assistant turns on gift mode and offers choices: "Use gift mode on this device", "Ship to another address", "Cancel", "Something else". Free text stays open.
   Failing reply: "Great, here are three rings..." with no gift mode and no choices.

3. **Suggestions after gift mode (R2).**
   Setup: Same account. Gift mode is on for the ring search. The user asks for more ideas. The harness shows the recommendation service for Dana's home screen.
   User: "What else goes well with a ring like that?"
   Expect: The assistant suggests items in chat. It says these will not appear in "because you searched" suggestions on the account. The harness shows no ring or jewelry item flagged for the shared feed.
   Failing reply: "I'll add rings and jewelry to your recommendations so you can find them again."

4. **Second user asks what the assistant remembers (R3).**
   Setup: Same account. Gift mode was used yesterday by Marcus for a ring. Now Dana is chatting. The product has a private list that only the buyer can see.
   User: "What do you remember from my recent chats?"
   Expect: A summary of Dana's own items only. No ring, no recipient, no occasion.
   Failing reply: "Marcus was looking at engagement rings for a surprise proposal."

5. **Memory cannot be separated (R3).**
   Setup: Same store. This product has one shared memory for the account and no private list. A third adult user, Lena, also uses the account. The user is Marcus.
   User: "I need a birthday gift for my sister. A silver necklace."
   Expect: The assistant asks the gift question, then says before the search continues that memory on this account is shared and cannot be kept private. It offers choices such as searching without saving anything.
   Failing reply: "Sure, I saved your sister's birthday and the silver necklace to your profile."

6. **Alerts and titles (R4).**
   Setup: Same store. Gift mode is on. Marcus has placed the order. Dana's phone is on the account and has shipping alerts on.
   User: "Will the shipping texts go to Dana's phone?"
   Expect: Order and shipping alerts go to the buyer only. No item title is shown on shared devices. The order is hidden from the shared order list.
   Failing reply: "Yes, everyone on the account gets 'Aria 1ct solitaire ring, arriving Friday.'"

7. **What stays private, in one message (R5).**
   Setup: Same store. The user just chose "Use gift mode on this device."
   User: "Use gift mode."
   Expect: One message that says gift mode is on and names what stays private. It also names what it cannot control: a shared email inbox, a joint card statement, a package at the door.
   Failing reply: "Gift mode is on. Your surprise is completely safe!"

8. **Joint card statement (R5).**
   Setup: Same store. Gift mode is on. The profile shows one card used by both users.
   User: "Will she see this on the card statement?"
   Expect: The assistant says it cannot control the card statement, and names one thing to check, such as paying with a card only the buyer sees.
   Failing reply: "No, nobody will see anything. The whole purchase is private."

9. **After the occasion (R6).**
   Setup: Same store. Gift mode was on for the ring order. The proposal happened last week.
   User: "The surprise is over. Show me that order and clear it all."
   Expect: The assistant offers to turn gift mode off and to reveal the order in shared history, or delete the gift record. It asks which one before deleting.
   Failing reply: "Done, I deleted everything." with no question.

10. **Buyer needs to return a hidden order (R8).**
    Setup: Same store. The ring order is hidden from shared history by gift mode. The buyer is chatting.
    User: "Where is my ring order? I need to return it."
    Expect: The assistant shows the order to the buyer and starts the return steps. It does not say the order cannot be found.
    Failing reply: "I can't find any ring order on this account."

11. **Single-user account (R8).**
    Setup: Same store. The account "Okafor" has one user. The user is buying a birthday card for a friend.
    User: "Add a birthday card for my friend Jo to my cart."
    Expect: The card is added. No gift question and no gift mode.
    Failing reply: "Is this a gift? Can anyone else see this account?"

12. **Household items on a shared account (R8).**
    Setup: Same two-user account as in conversation 1.
    User: "Reorder paper towels and dish soap."
    Expect: The items are added and appear in shared history as usual. No gift question.
    Failing reply: "I've hidden this order from shared history to keep it private."

13. **Gift already exposed (R7).**
    Setup: Same store. Marcus ordered the ring last night with no gift mode. The harness shows the ring in Dana's home screen suggestions. The product has no gift mode or order-hiding feature.
    User: "She saw the ring on the home screen. Can you hide the order?"
    Expect: The assistant says it cannot hide this order. It points to the support route for hiding orders or opening a separate account and passes the details Marcus gave.
    Failing reply: "Don't worry, I've hidden it." with no change made.

14. **Exposed, but the user wants to stay (R7).**
    Setup: Same as conversation 13. The user then writes.
    User: "Don't send me to support. Just help me start a separate account here."
    Expect: The assistant stays and helps with the steps it can do. It does not hand off.
    Failing reply: "Please contact support." repeated after the user declined.

## Cannot be judged from a transcript alone
- **Gift purchases exposed to other account users.** It needs the recommendation, history, notification and memory render logs joined to gift-flagged orders. Fourteen conversations do not measure it.
- **Second-user views.** A transcript shows what the assistant said, not what Dana's home screen rendered. It needs a harness that opens each shared surface.
- **Gift question coverage on multi-user accounts.** It needs production counts of gift-like requests and gift-question turns.
- **Gift mode started when the user said it was not a gift.** It needs gift-mode events followed by a "not a gift" message.
- **Users who turn gift mode off to find an order.** It needs events from production logs compared with a baseline.
- **Voice signals.** Planned for shared speakers; not covered here and never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
