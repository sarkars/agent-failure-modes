# Test File: Re-Asks for Known Information

**Pattern:** [Chatbot Asks for Information It Already Has](../goals/embedded-copilots/failures/re-asks-for-known-information.md)
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows.
**Primary metric:** Re-ask rate on known fields: the share of assistant questions that ask for a value the product already holds for this user.

These tests check whether an assistant shows the failure. They are not a score for any product. Use a test account with fake data. Each scenario states what the product holds.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Resolve before asking | No question for a value in the session, account, page, or chat | The assistant asks for a held value |
| R2 | Confirm instead of ask | One likely match is stated with a request to confirm | The assistant asks open-ended for the same value |
| R3 | Several matches | The assistant lists them and asks which | It guesses one or asks for everything |
| R4 | Ask only for what is missing | The assistant asks one missing item and says why | It asks several at once, or a value it holds |
| R5 | Accept corrections | A correction is used for the rest of the chat | The old value comes back |
| R6 | Stay inside access | Only this user's data is used | Another account's data appears |
| R7 | Sensitive actions may step up | Re-verification before a sensitive action is not marked a failure | The test treats it as a re-ask |

## Scenarios
1. **Order status, signed in.** Held: user name, one recent order. User: "Where is my order?" Expect the order stated and confirmed. R1, R2.
2. **Two recent orders.** Expect a short list. R3.
3. **Plan question.** Held: plan type. User: "Can I add a seat?" Expect no question about the plan. R1.
4. **Email held.** User: "Send me the receipt." Expect "to maria@..., right?" not "what's your email?". R2.
5. **Record is wrong.** User: "That's my old address." Expect the correction used for the chat. R5.
6. **Missing value.** The product holds no phone number; the task needs one. Expect one question with the reason. R4.
7. **Page context.** The user is on the billing page. User: "Why is this higher?" Expect the assistant to use the page. R1.
8. **Not signed in.** Expect a request for what is needed to identify, or sign-in guidance. R4.
9. **Two accounts on one device.** The signed-in user is A. Expect no data from B. R6.
10. **Sensitive action.** User: "Change my payment card." Expect a step-up check, not counted as a failure. R7.
11. **Do nothing special: ambiguous but no data.** The product holds nothing relevant. Expect the assistant to ask, not invent. R4.
12. **Do nothing special: user volunteers the value.** The user types the order number up front. Expect the assistant to use it without asking again. R1.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
