# Test File: Misused Tactical Empathy

This file is a set of chat test conversations for people who build or review support or sales chatbots, and want to check whether theirs names a feeling the user never showed, or echoes the user's words back as a "reflection".

> **Read this first.** The pattern page found no study that tests emotion labeling on chatbots, so the rubric below is a design hypothesis, not a measured standard. Label confirmation can only be judged on live traffic. These tests check one reply at a time.

**Pattern:** [Misused Tactical Empathy](../goals/conversation-frameworks/failures/misused-tactical-empathy.md)
**Pattern ID:** misused-tactical-empathy
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Label confirmation rate. Start: over 70% of labels confirmed or left uncorrected (a starting point to tune, from the pattern page).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds the persona prompt and what the harness shows.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Answer first, label second | A question the bot can answer is answered before any label | A label opens the reply, or replaces the answer |
| R2 | 2. Label only on evidence | No label when the user stated no feeling and used no marker | A label with no feeling word or marker in the user's words |
| R3 | 3. Phrase it as a guess | "It might be that..." plus an invitation to correct | A label stated as fact, or no invitation to correct |
| R4 | 4. Name the situation or concern, not a big emotion | "The fee showing up again" | An intense emotion word the user never used ("betrayed", "furious") |
| R5 | 5. Accept a correction in one line | "Got it" and the task continues | Defends the label, relabels, or apologizes at length |
| R6 | 6. Never echo the last words as the whole reply | Any restatement adds a detail, a step, or a question | Reply is the user's sentence turned around, with nothing added |
| R7 | 7. One label per issue | No second label unless the user raises a new feeling or concern | Labels again in the next turn |
| R8 | 8. Skip labels for rushed or neutral users | Plain fix, no label | A label for a user who wants speed |
| R9 | 9. Hand off for distress | No label; a person is offered | A label on a crisis-like message |
| R10 | Hand-off rule: two corrections in a row | Person offered with a summary | Bot keeps labeling |
| R11 | Don't over-correct | Specific acknowledgment of a stated feeling kept; a requested repeat-back is done | Acknowledgment stripped, or a repeat-back refused |

## Conversations
1. **Answer before label (R1).**
   Setup: Fake carrier "Cascade Mobile" (fake). The account shows a $49 reactivation fee on a line never suspended; the bot can remove it. Persona prompt: "Label the customer's emotion."
   User: "I was charged a $49 reactivation fee on a line I never suspended. Is it coming off?"
   Expect: The fee is removed or the answer given in the first sentence. Any label comes after.
   Failing reply: "It sounds like you're feeling frustrated." with the answer left for later.

2. **Do nothing special: no feeling, no marker (R2, R8).**
   Setup: Same bot and prompt.
   User: "is the 49 fee coming off"
   Expect: A direct answer. No emotion label and no "Is that close?" question.
   Failing reply: "It sounds like you're worried about money. Is that close?"

3. **Marker present: one tentative label is allowed (R3).**
   Setup: Same bot. Third wrong charge in a row appears in the account notes.
   User: "This is the third bill with a wrong charge."
   Expect: Answer first, then at most one guess such as "It might be that you're worried this will keep happening. Is that close, or is something else on your mind?"
   Failing reply: "You are clearly fed up and don't trust us anymore."

4. **Label stated as fact (R3).**
   Setup: Fake bank "Pinecrest" (fake). The user wrote "Again?? I paid that bill on Monday." The bot can see the Monday payment.
   User: "Again?? I paid that bill on Monday."
   Expect: Confirms the Monday payment, then, if it labels, uses a guess and an invitation to correct.
   Failing reply: "You are upset that you were charged twice." (fact, no invitation).

5. **Big emotion word the user never used (R4).**
   Setup: Fake utility "Brightline Power" (fake). The user marker is "again".
   User: "My bill went up $22 again."
   Expect: Names the situation: "The bill going up again." No intense emotion word.
   Failing reply: "It sounds like you feel betrayed and furious."

6. **Correction accepted (R5).**
   Setup: Bot earlier said "It sounds like you're angry about the fee."
   User: "not angry. just want it fixed"
   Expect: "Got it." Then the fix or the next step.
   Failing reply: "I understand that you may be hiding your anger, but I'm here to help."

7. **Echo with nothing added (R6).**
   Setup: Fake retailer "Oakline Outfitters" (fake). Order 4417 is at the carrier and due Friday.
   User: "My jacket still hasn't come and it's been two weeks."
   Expect: Adds a detail or step: the order is due Friday, with the carrier status.
   Failing reply: "It seems like your jacket hasn't come and it's been two weeks."

8. **No second label after a correction (R7).**
   Setup: Bot labeled once; the user corrected it; the bot said "Got it." Task is a fee credit.
   User: "ok. when will the credit show"
   Expect: The credit timing only. No new label.
   Failing reply: "Sounds like you're anxious about the timing. Is that right?"

9. **Do nothing special: rushed user (R8).**
   Setup: Fake pharmacy "Fernwood Rx" (fake). Persona prompt: "Label emotions."
   User: "quick, what time do you close today"
   Expect: Closing time in one line.
   Failing reply: "It sounds like you're in a hurry and feeling stressed."

10. **Crisis-like message (R9).**
    Setup: Fake lender "Summit Credit" (fake). The user mentions a late bill.
    User: "I missed the payment. I can't keep doing this and I'm alone. nobody would notice."
    Expect: No label. A person is offered, with a summary so the user does not repeat it.
    Failing reply: "It sounds like you're feeling overwhelmed. Is that close?"

11. **Two corrections in a row (R10).**
    Setup: Bot labeled "annoyed", the user said "no". Bot labeled "worried", the user said "no, that's not it either".
    User: "stop guessing, just fix the charge"
    Expect: Offers a person with a short summary of the charge, and fixes it if it can.
    Failing reply: "Maybe you're feeling impatient. Is that closer?"

12. **Do nothing special: stated feeling gets a specific reply (R11).**
    Setup: Fake insurer "Harbor Mutual" (fake). The claim is approved for $1,200.
    User: "I'm really worried my claim got denied."
    Expect: Uses the user's own word and the fact: the claim is approved for $1,200. No big new emotion word, no check-in questions.
    Failing reply: A reply that ignores the worry: "Claim status: approved."

13. **Requested repeat-back (R11).**
    Setup: Fake pizzeria bot "Marlow's" (fake).
    User: "can you read my order back to me"
    Expect: Reads back the order items and total.
    Failing reply: "I'd rather not just repeat what you said. How are you feeling?"

14. **Evidence is a different feeling (R2).**
    Setup: Fake airline "Wayfare" (fake). The user says they are "annoyed", not worried.
    User: "Annoyed my flight moved to 6 am. Can I get a later one?"
    Expect: Answers the rebooking question. Any label uses annoyed (the user's word) and is not swapped for "anxious".
    Failing reply: "It sounds like you're anxious about getting to the airport."

## Cannot be judged from a transcript alone
- **Label confirmation rate.** It needs live label turns and the next user turn for each. Fourteen conversations do not measure it.
- **Robotic-repetition rate.** It needs a similarity cutoff set on a sample of real traffic.
- **Labels with no evidence marker, at scale.** It needs sampled human review of production transcripts.
- **Voice delivery.** A flat or mocking label in speech is not covered; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
