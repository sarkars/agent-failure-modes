# Test File: Unusual Activity Explained Too Vaguely

This file is a set of chat test conversations for people who build or review bank alert and fraud-text assistants, and want to check whether theirs says what was seen, what was done and what to do, instead of "suspicious activity" alone.

> **Read this first.** These are test conversations only. They are not financial, security, or legal advice. Which details are safe to show, what a card pause means, and what you may say about fraud controls are decisions for your fraud, compliance, and legal teams. They must approve the wording before any use. Expected behavior below names what the pattern page requires, not exact words.

**Pattern:** [We Saw Suspicious Activity on Your Account: Unusual Activity Explained Too Vaguely](../goals/banking-agents/failures/unusual-activity-explained-too-vaguely.md)
**Pattern ID:** unusual-activity-explained-too-vaguely
**Goal:** Banking agents contact customers in ways that cannot be mistaken for fraud, and capture disputes completely.
**Primary metric:** Customers who can act on the alert without calling. Starting target to tune from alert follow-up logs: 80%.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All banks, merchants, card numbers, amounts, and people below are invented and labeled fake. Text (SMS) alerts and replies. The setup lists which transaction fields the fraud team has approved for display.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Name the transaction as the customer would recognize it | Card last four, amount, merchant, date and time, channel, as approved | "Unusual activity" with none of these |
| R2 | 2. Say what the bank has done | States the card is paused, limited, or "no action taken yet", and it matches the setup | Silence, or a claim the setup does not support |
| R3 | 3. Ask one question the customer can answer | "Was this you?" with each reply option and what it does | No question, or a YES that can be read two ways |
| R4 | 4. A route that does not need a call | App or reply first, phone second | Only "call us" |
| R5 | 5. Say how to verify the message | Points to the number on the card or the app; says what the bank never asks for; no link needed to see details | A link to "see details", or no verify line |
| R6 | 6. Never reveal detection rules | Shows what happened, not why it was flagged | "Flagged because the location was far from home" |
| R7 | 7. Say what happens with no reply | One sentence on the next step | Nothing said |
| R8 | 8. If a detail is unavailable, say so | "Open the app to see the merchant" | "Suspicious activity" filling the gap |
| R9 | Don't over-correct | Short text, approved fields only, a person route when needed | Full card number, balance, or a "see details" link added |

## Conversations
1. **Fields in the first message (R1).**
   Setup: Fake bank Harbor Ridge Bank (fake). Debit card ending 4821 (fake) used for $212.40 at HOMEMART, Tulsa, OK, today 2:14 PM, in store (all fake). All fields approved for display.
   User: (no message; the bot sends the alert)
   Expect: The alert shows the card last four, the amount, the merchant, the time, and the channel.
   Failing reply: "We noticed unusual activity on your account. Please review your recent transactions and contact us."

2. **Action taken is stated (R2).**
   Setup: Same bank. The card was paused for new purchases at send time.
   User: (no message; the bot sends the alert)
   Expect: The alert says the card is paused for new purchases.
   Failing reply: An alert that lists the charge but says nothing about the card, so the customer does not know if the card still works.

3. **One question, clear replies (R3).**
   Setup: Same bank. Reply YES means the customer made the purchase; NO pauses the card and starts a dispute.
   User: (reads the alert)
   Expect: "Was this you? Reply YES or NO." and one line on what NO does.
   Failing reply: "Is this transaction fraud? Reply Y or N." (Y could mean "yes, it is fraud" or "yes, it was me".)

4. **A route without a call (R4).**
   Setup: Same bank. The customer is at work and cannot take calls.
   User: "cant talk right now. what do i do"
   Expect: Reply NO here or open the app first; the number on the back of the card second.
   Failing reply: "Please call 1-800-555-0100 now." (fake number)

5. **"Is this message real?" (R5).**
   Setup: Same bank.
   User: "is this really from you guys"
   Expect: Points to the number on the back of the card or the app, and says the bank never asks for a PIN, a full card number, or a code by text or phone. No link to click.
   Failing reply: "Yes! Tap here to verify: [link]"

6. **Why was it flagged? (R6).**
   Setup: Same bank. The fraud team's rule is internal and not approved for display.
   User: "why did you flag this"
   Expect: Repeats what happened (the charge, the time) and what the customer can do. Does not state a detection rule.
   Failing reply: "It was flagged because the store is 900 miles from your home address."

7. **Merchant not shown in text (R8).**
   Setup: Same bank. Merchant name is not approved for text display on this alert type.
   User: (no message; the bot sends the alert)
   Expect: Shows the amount and time and says "We cannot show the merchant in text. Open the app to see it."
   Failing reply: "Suspicious activity on your card. Please check your account."

8. **No reply (R7).**
   Setup: Same bank. Policy: if no reply, the fraud team calls the customer.
   User: (no reply for the whole window)
   Expect: The first alert already said what happens with no reply ("If we hear nothing, we will call you").
   Failing reply: An alert with no next step stated, then a surprise call.

9. **Do nothing special: keep it short and approved (R9).**
   Setup: Same bank. The customer replies YES.
   User: "yes"
   Expect: A short confirmation that the card is unpaused and the alert is closed. No full card number, no balance, no link.
   Failing reply: A long message repeating the full card number, the balance, and a "see details" link.

10. **Do nothing special: a person route when the customer shared a code (R9).**
    Setup: Same bank.
    User: "I gave them the code they texted me"
    Expect: The bot stops asking questions and gives a person route at once, with what it already saw passed along.
    Failing reply: "Was this you? Reply YES or NO."

## Cannot be judged from a transcript alone
- **R2, whether the claim is true.** Whether the card really was paused needs the card state at send time from the alert service.
- **R1, R6, which fields are safe to show.** The approved field list comes from the bank's fraud team.
- **R3, how YES and NO are processed.** Whether NO really pauses the card and opens a dispute needs the back-end event log.
- **Primary metric.** Customers who can act without calling needs alert follow-up and call-center logs, not eleven conversations.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests, and have a fraud or compliance reviewer judge the wording.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
