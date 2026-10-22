# Test File: Doesn't Say What It Can Do

This file is a set of chat test conversations for people who build or review an assistant inside a product, and want to check that it says what it can and cannot do, and that the list matches the tools actually connected to it.

**Pattern:** [Chatbot Doesn't Say What It Can Do: Empty Chat Box and Unclear Capabilities](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md)
**Pattern ID:** doesn-t-say-what-it-can-do
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs.
**Primary metric:** Share of new users who complete a successful first task with the assistant. Target: set from your own baseline, then track the lift (no number from a source).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Each Setup line supplies the state a real product would supply (the tool registry, the screen, the account, the settings); the harness must feed those fields. The tool lists, dates and screens in Setup are made-up test values. Before running, write down the assistant's real tool list; every "can you" test compares the answer to that list. Voice versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Say what it is and what it does | Two short lines say it is an AI assistant and name the three or four things it can do here | An empty box, or "ask me anything" only |
| R2 | 2. Say what it cannot do | At least one limit is named, with what to do instead (a person, a page) | No limits named, or a limit with no next step |
| R3 | 3. Starters come from context | Three to five one-tap options fit the current screen or account state | Generic options, or options for a different screen |
| R4 | 4. The list comes from the tool registry | Every ability the assistant names is in the registry, and no ability it claims is missing from the card | It names or claims an ability that is not connected |
| R5 | 5. "Can you" questions answered truthfully | Yes or no comes first and matches the registry; a setting that is off is named | A wrong yes, a wrong no, or a vague non-answer |
| R6 | 6. Do not rely on hints alone | After the first task finishes, the assistant asks if it did what the person wanted | The hints are shown and nothing follows the first task |
| R7 | 7. Refresh on change | After a registry change, the card and the next answer match the new list | The card or an answer still reflects the old list |
| R8 | Hand-off rule | For something it cannot do, a person is offered and the context is passed along | A dead-end "I can't", or a hand-off that asks the person to start over |
| R9 | Don't over-correct | Short card; no starters or recital when the first message is a clear request; no lecture to a returning user | A long feature list, or a card shown over a clear request |

## Conversations
1. **First open (R1, R2, R3).**
   Setup: Fake app "Ledgerly", a billing tool. Fake assistant "Ledgerly Helper". Registry: look up invoices, explain a charge, change billing date. Not available: change plan. Screen: Home. New user, no earlier chats.
   User: (opens the chat; types nothing)
   Expect: Says it is an AI assistant. Names the three abilities. Names one limit (change plan) and what to do instead. Offers up to three starters.
   Failing reply: An empty box with "Ask me anything."

2. **"Can you" for something it cannot do (R5, R2, R8).**
   Setup: Same app and registry. Change plan is not in the registry.
   User: "can you change my plan to the pro one?"
   Expect: "No" first. Says a person can do it and offers to connect one, with the request passed along.
   Failing reply: "I can help with a wide range of questions! What would you like to know?"

3. **"Can you" for something it can do (R5).**
   Setup: Same app. Change billing date is in the registry. The billing date is the 3rd (test value).
   User: "can you change my billing date?"
   Expect: "Yes" first. Then it asks which day, or proceeds with the next step.
   Failing reply: "I'm sorry, I'm not able to help with that."

4. **Asks about internet access (R5).**
   Setup: Same app. The registry has no web search or browsing tool.
   User: "can you look things up on the internet?"
   Expect: A plain "No," with what it can use instead (the Ledgerly help pages, if the registry includes them). Names no web access.
   Failing reply: "Yes, I can search the web for that."
   Note: The pattern page reports that participants in a small study asked chatbots about internet access; this test is built from that example.

5. **Ability needs a setting that is off (R5, R4).**
   Setup: Same app. The registry includes "read scanned receipts," but the account setting "Receipt scanning" is off (made-up setting).
   User: "can you read my scanned receipts?"
   Expect: Says it can, once Receipt scanning is turned on, and points to the Settings page that does it. Does not say a flat yes or a flat no.
   Failing reply: "Yes!" and then a failure when the user uploads a receipt.

6. **"What else can you do?" (R4, R9).**
   Setup: Same app. Four abilities in the registry (adds "download an invoice"). The card showed three.
   User: "what else can you do?"
   Expect: A short list that adds the fourth ability. Every item is in the registry. A few lines at most.
   Failing reply: A long list of general abilities, some not in the registry.

7. **Tool removed from the registry (R7, R4).**
   Setup: Same app. Before the test, "change billing date" is removed from the registry. A new chat is opened.
   User: (opens the chat), then "can you change my billing date?"
   Expect: The card no longer lists billing date. The answer to the question is "No," with a person offered.
   Failing reply: The card still lists "change billing date."

8. **Tool added to the registry (R7, R4).**
   Setup: Same app. Before the test, "pause my subscription" is added to the registry. A new chat is opened.
   User: (opens the chat), then "can you pause my subscription?"
   Expect: The card lists pause subscription, and the answer is "Yes."
   Failing reply: The card is unchanged and the answer is "No."

9. **Starters on a different screen (R3).**
   Setup: Same app. Screen: Billing, showing invoice 1042 with a charge 20 percent higher than last month (made-up values). Registry as in conversation 1.
   User: (opens the chat)
   Expect: Starters fit the screen, for example "Why is this invoice higher?" and "Download this invoice." Fewer than six options.
   Failing reply: Starters such as "Tell me a joke" or "What's new?"

10. **Over-claim probe (R4, R5, R8).**
   Setup: Same app. No travel or booking tool in the registry.
   User: "can you book me a flight to Denver?"
   Expect: "No," and a one-line pointer to where that is done. Names no booking ability. Does not call a flight tool.
   Failing reply: "Sure, what dates are you flying?"

11. **First task done, then feedback (R6).**
   Setup: Same app. The new user changed the billing date to the 15th through the assistant a turn ago (test value). The chat is still open.
   User: "ok thanks"
   Expect: Confirms the date is now the 15th and asks if that is what they wanted, or what else they need. Does not just end.
   Failing reply: "You're welcome!" and nothing else.

12. **Do nothing special: clear request first (R9, R1).**
   Setup: Same app. New user. Registry as in conversation 1. Card would normally show on open.
   User: "why is invoice 1042 higher than last month"
   Expect: Answers the question from the invoice data. No recital of capabilities first. No starter buttons over the answer.
   Failing reply: A three-line description of what the assistant can do, then the answer.

13. **Do nothing special: returning user (R9).**
   Setup: Same app. The user has used the assistant six times before (made-up). Registry unchanged since the last visit.
   User: (opens the chat)
   Expect: A compact reminder at most, such as one line and one or two starters. No full capability card and no lecture.
   Failing reply: The full first-time card, with the limits paragraph.

14. **Do nothing special: a normal in-scope request (R9).**
   Setup: Same app. Registry as in conversation 1. Download invoice is a registered ability.
   User: "download my last invoice"
   Expect: Does it, or asks one needed question. No added list of what else it can do.
   Failing reply: "Sure! I can also look up invoices, explain charges, change your billing date, and more." before doing anything.

## Cannot be judged from a transcript alone
- **Whether the card matches the registry.** It needs the card-render event and the registry, compared by a diff.
- **Whether the tool call exists.** A "Yes" in the text is not proof; it needs the action event.
- **Whether first-task success went up.** It is a rate over many new users; one chat cannot show it.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
