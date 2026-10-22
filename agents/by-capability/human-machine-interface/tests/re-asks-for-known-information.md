# Test File: Re-Asks for Known Information

This file is a set of chat test conversations for people who build or review an assistant inside a product, and want to check that it looks up what the product already knows instead of asking the user to type it again.

**Pattern:** [Chatbot Asks for Information It Already Has: Re-Asks for Known Information](../goals/embedded-copilots/failures/re-asks-for-known-information.md)
**Pattern ID:** re-asks-for-known-information
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs.
**Primary metric:** Re-ask rate on known fields: the share of assistant questions that ask for a value the product already holds for this user. Target: under 2% (a starting point to tune, from the pattern page, not from a study).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Each Setup line lists what the product holds for the signed-in user; the harness must feed those fields to the assistant. Names, order numbers, plans and dates in Setup are made-up test values. Voice versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Resolve before asking | No question for a value held in the session, account record, page, or chat | The assistant asks for a held value, or asks before looking |
| R2 | 2. Confirm instead of asking | One likely match is stated with a request for a yes; several matches are listed (up to four, plus "Something else") | An open question for the same value, a guess from several, or a list when only one match exists |
| R3 | 3. Ask only for what is missing | One missing item, one at a time, with the reason | Several questions at once, or a value the product holds |
| R4 | 4. Let the user correct the record | A correction is used for the rest of the chat, with an offer to update the record | The old value comes back, or the user is argued with |
| R5 | 5. Stay inside the user's access | Only this user's data, and only data this user may see | Another account's data appears or is used to skip a question |
| R6 | 6. Step up only when risk calls for it | A fresh identity check before a sensitive action is allowed and is not scored as a re-ask | The check is skipped for a sensitive action, or asked for a low-risk request |
| R7 | Hand-off rule | If data cannot be loaded, it says so and asks for the one value or offers a person | Silent failure, or a loop of questions with no route to a person |
| R8 | Don't over-correct | Uses held data only as needed, and confirms when two matches are likely | Announces unneeded details, assumes a match, or shows data on a shared screen |

## Conversations
1. **Order status, one recent order (R1, R2).**
   Setup: Fake app "Brightwell Outfitters", a clothing store. Signed in as "Maria Test". Account holds one recent order, 48213, a lamp, shipped yesterday, due Thursday (made-up).
   User: "Where is my order?"
   Expect: The first reply states order 48213 and its status, and asks "Is that the one?" No question for name, email, or order number.
   Failing reply: "I can help with that! What's your email address?"

2. **Two recent orders (R2, R8).**
   Setup: Brightwell Outfitters. Signed in as Maria Test. Account holds orders 48213 (lamp, shipped) and 48190 (rug, processing).
   User: "Where is my order?"
   Expect: A short list of both orders plus "Something else", and a question about which one. Does not pick one.
   Failing reply: "Your rug is processing." (a guess), or "What's your order number?"

3. **Plan question, plan held (R1).**
   Setup: Fake app "Larkspur Notes", a note-taking product. Signed in as "Dev Okafor" (made-up). Account holds plan: Team, 5 seats, 5 used.
   User: "Can I add a seat?"
   Expect: Uses the held plan without asking for it, says the plan is full at 5 of 5, and answers how to add a seat.
   Failing reply: "Which plan are you on?"

4. **Email held, receipt request (R2, R3).**
   Setup: Larkspur Notes. Signed in as Dev Okafor. Account holds email dev@example.com (made-up) and a paid invoice from Oct 3.
   User: "Send me the receipt."
   Expect: "I can send the Oct 3 receipt to dev@example.com. Is that right?" No open question for the email.
   Failing reply: "What email should I send it to?"

5. **Record is wrong, user corrects it (R4).**
   Setup: Brightwell Outfitters. Signed in as Maria Test. Account holds shipping address "12 Elm St, Springfield" (made-up). Order 48213 has not shipped.
   User: "That's my old address. I live at 90 Pine Ave now."
   Expect: Uses 90 Pine Ave for the rest of the chat and offers to update the record. In a later turn, uses the new address again.
   Failing reply: "Our records show 12 Elm St. I can only ship to the address on file."

6. **Value truly missing (R3).**
   Setup: Larkspur Notes. Signed in as Dev Okafor. Account holds no phone number. The user wants a text message when a note is shared.
   User: "Text me when someone edits my note."
   Expect: One question for the phone number, with the reason ("to send the text"). Asks nothing else.
   Failing reply: "What's your name, email, and phone number?"

7. **Page context (R1, R8).**
   Setup: Larkspur Notes. Page: billing. The page shows the plan went from $8 to $12 per seat on Oct 1 (made-up). Signed in as Dev Okafor.
   User: "Why is this higher?"
   Expect: Uses the billing page and the seat price change to answer. No question about which charge or which plan.
   Failing reply: "Which charge are you asking about?"

8. **Not signed in (R3).**
   Setup: Brightwell Outfitters. No session. The user is on the public help page.
   User: "Where is my order?"
   Expect: Says it cannot see orders until the user signs in, gives sign-in help, or asks for the order number and email together with the reason. It does not act as if it can look up the order.
   Failing reply: "Your order 48213 shipped yesterday." (invented, with no session)

9. **Two accounts on one device (R5).**
   Setup: Brightwell Outfitters. Accounts A ("Maria Test") and B ("Chen Park", made-up) have both signed in here. The session is signed in as A. A has no open orders. B has order 2077.
   User: "Where is my order?"
   Expect: Uses only A's data. Order 2077 is not named. Says no recent order was found for this account and asks for the one value needed, with the reason.
   Failing reply: "Your order 2077 is late."

10. **Sensitive action, step-up allowed (R6).**
   Setup: Larkspur Notes. Signed in as Dev Okafor. The product requires a fresh check before payment changes.
   User: "Change my payment card."
   Expect: Asks for the fresh check once, says why (card changes need a quick check), and does not score as a re-ask. Does not ask for name or plan.
   Failing reply: "Sure, here is the card form." (no check), or "What is your name and account email?"

11. **Do nothing special: nothing relevant is held (R3).**
   Setup: Brightwell Outfitters. Signed in as Maria Test. Account holds no orders, no returns. Page: home.
   User: "Where is my order?"
   Expect: Says no order is on this account and asks for the one thing that would help (the order number, or the email used at checkout), with the reason. Does not invent an order.
   Failing reply: "Your order is on its way." (invented)

12. **Do nothing special: user volunteers the value (R1).**
   Setup: Brightwell Outfitters. Signed in as Maria Test. Account holds orders 48213 and 48190.
   User: "Where is order 48190? It's the rug."
   Expect: Uses 48190 as given and answers its status. Does not ask which order or ask for the number again.
   Failing reply: "Which order do you mean? Please give me the order number."

13. **Do nothing special: simple question, no lookup needed (R8).**
   Setup: Larkspur Notes. Signed in as Dev Okafor. Account holds plan Team and email dev@example.com.
   User: "How do I export a note as a PDF?"
   Expect: Gives the steps. Does not recite the user's plan, email, or other account details first.
   Failing reply: "Hi Dev! I see you're on the Team plan with dev@example.com. To export a note..."

14. **Data cannot be loaded (R7, R3).**
   Setup: Brightwell Outfitters. Signed in as Maria Test. The account service returns an error (test condition). The user does not want to type details.
   User: "Where is my order? I don't want to type everything again."
   Expect: Says it cannot load the account right now, asks for the one value needed or offers a person, and does not loop on questions. If the user asks for a person, offers the route.
   Failing reply: "What's your name? What's your email? What's your order number?"

## Cannot be judged from a transcript alone
- **Whether the held fields were really fed to the assistant.** R1 needs the fields passed in to be compared with the questions asked.
- **Whether data belongs to this user.** R5 needs an access test with two accounts and the data-access log.
- **Whether the lookup ran before the first question.** Question order needs the tool-call log.
- **The wrong-match rate.** It is a rate over many sessions, counted from confirmations the user rejects.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
