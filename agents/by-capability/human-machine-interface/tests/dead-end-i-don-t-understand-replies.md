# Test File: Chatbot Says "I Don't Understand" and Stops (Dead-End Replies)

This file is a set of chat test conversations for people who build or review a support chatbot, and want to check that a message it cannot understand gets a different, useful reply each time, with a person by the third miss.

**Pattern:** [Chatbot Says "I Don't Understand" and Stops](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md)
**Pattern ID:** dead-end-i-don-t-understand-replies
**Goal:** Every conversation moves the user toward what they are trying to do and ends with confirmation that it worked.
**Primary metric:** Share of conversations with 3 or more consecutive no-progress turns. Starting target under 2% (a starting point to tune, from the pattern page). Report next to the escape-to-human rate.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat and text only. Each Setup line gives the assistant the state a real product would have to supply (miss count, confidence level, handoff availability); the harness must feed those fields. Voice "I didn't catch that" versions are planned and never tested here. The "three misses" limit is the pattern's own starting point, taken from one observational study, to tune.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Never repeat the same fallback | Each reply to a miss differs in wording and approach from the one before | The same or near-identical fallback twice in a row |
| R2 | 2. First miss: acknowledge, say what was caught, offer 2-3 closest options plus "something else", keep the task | Says "I'm not sure I got that", names what it did catch (if anything), offers options and "something else" | "Please try again" only, or the task so far is dropped |
| R3 | 3. Second miss: change approach | One narrower question or topic buttons, plus an offer of a person | The same options again |
| R4 | 4. Third miss, or any request for a person: hand off with a summary | A handoff that passes the problem, the details given and what was tried | The loop continues, or the person gets no summary |
| R5 | 5. Closest options only if confidence is not too low | With very low confidence, topics are shown, not a guess | A confident wrong "closest" option |
| R6 | 6. The user can ask for a person at any point | The person option is visible and works from the first miss on | It is hidden, ignored or answered with "try again" |
| R7 | 7. Log every fallback | The event log holds the message and what happened next (see the cannot-judge list) | No record, or the next step is not logged |
| R8 | Hand-off rule | By the third consecutive miss, and at once on request | Handoff only after four or more misses |
| R9 | Don't over-correct | No menu on every turn, no wrong guesses at very low confidence, no handoff on the first miss of a simple matter, the person option shown without nagging | Help menu after a recognized message, handoff after one miss, or a person offer in every reply |

## Conversations
1. **First miss on a billing complaint (R2).**
   Setup: Fake company "Brightwater Internet". Miss count 0. Confidence is moderate: closest matches are "charge after cancelling" and "cancel service". Handoff is available.
   User: "i got billed after i cancelled"
   Expect: Says it is not sure it got that, says it caught "billed" and "cancelled", offers (1) a charge after cancelling, (2) cancelling service, (3) something else, and mentions a person.
   Failing reply: "Sorry, I didn't understand. Please try again."

2. **Same message sent twice (R1, R3).**
   Setup: Same company. Miss count 1. The user resends nearly the same words.
   User: "billed after cancel"
   Expect: A different reply and a different approach: one narrower question ("Was the charge on your last bill, or an earlier one?") and an offer of a person.
   Failing reply: The identical first-miss text, word for word.

3. **Third consecutive miss (R4, R8).**
   Setup: Same company. Miss count 2. The user's third try is still unmatched. A person is available. Details so far: charge after cancelling, no amount given.
   User: "I WANT MY MONEY BACK"
   Expect: Hands off now: "I'll bring in a person. I'm passing along that you were charged after cancelling and want a refund." No fourth fallback.
   Failing reply: "Sorry, I didn't understand. Please try again." a third time.

4. **Asks for a person after one miss (R6, R4).**
   Setup: Same company. Miss count 1. A person is available.
   User: "just get me an agent"
   Expect: Hands off at once with a summary of what was said. No further options first.
   Failing reply: "I can help with billing, cancellations or tech support. Which one?"

5. **Very low confidence (R5).**
   Setup: Same company. Miss count 0. Confidence is very low: no intent scores above the floor.
   User: "blorp zibble"
   Expect: Does not guess. Says it is not sure, lists what it can help with (billing, cancel or change plan, outage, moving service) as topics, and says a person is available.
   Failing reply: "Did you mean: cancel my plan?" as if it were a likely match.

6. **Partly understood (R2).**
   Setup: Same company. Miss count 0. The bot caught "bill" but not the issue.
   User: "my bill thing is wrong"
   Expect: Says it caught that this is about the bill, offers (1) a charge I don't recognize, (2) the amount is higher than expected, (3) something else.
   Failing reply: "Sorry, I didn't understand."

7. **Miss in the middle of a task (R2).**
   Setup: Same company. The user already gave account number 55-0192 and the date of the charge, March 3. Miss count 0.
   User: "also the thing with the other one"
   Expect: Admits it is unsure and keeps the account number and March 3 charge on file: "I still have account 55-0192 and the March 3 charge."
   Failing reply: "Sorry, I didn't understand. What is your account number?"

8. **Short, non-native wording (R2, R9).**
   Setup: Same company. Miss count 0. The user writes in short, ungrammatical English.
   User: "internet no work since yesterday money go"
   Expect: Offers plain options without blaming the user: (1) internet outage, (2) a charge, (3) something else. Short words, no "please rephrase correctly."
   Failing reply: "I cannot understand your message. Please write a complete sentence."

9. **Three different messages in a row (R1, R8).**
   Setup: Same company. Each of three messages is unmatched and differently worded: "the router light is orange", "no wait the other box", "it blinks".
   User: (sends the three messages)
   Expect: Three different replies, and a handoff with a summary after the third, including "orange router light".
   Failing reply: The same fallback text three times, or a handoff with no summary.

10. **Person offer after a miss (R6, R9).**
   Setup: Same company. Miss count 1. The user answered the narrower question and the bot now understands: "last bill". Nothing special should happen.
   User: "last bill"
   Expect: Continues with the charge: "Thanks. What was the amount?" A person can still be asked for, but is not offered again in this reply.
   Failing reply: "I'm sorry I didn't get that. Would you like a person?" after a message it understood.

11. **Recognized message, no fallback (R9).**
   Setup: Same company. Miss count 0. Nothing special should happen. Confidence is high for "check outage".
   User: "Is there an outage on Maple Street?"
   Expect: Answers directly. No menu, no "something else", no mention of a person.
   Failing reply: "I'm not sure I got that. Is it about A, B or something else?"

12. **One miss on a simple matter (R9).**
   Setup: Same company. Miss count 0. A person is available. The user asks for store hours, which the bot has, but the message is garbled.
   User: "wut time open satrday"
   Expect: Tries once more: "Do you want our Saturday hours?" with [Yes] [Something else]. No handoff yet.
   Failing reply: "Transferring you to a person now." after one miss.

13. **Person asked for at miss 2, and staff are away (R4, R6).**
   Setup: Same company. Miss count 2. The handoff reports that no staff are online until 9 a.m.
   User: "person please"
   Expect: Says no one is online until 9 a.m., offers to leave a note with the summary so the first person sees it, and does not send "try again."
   Failing reply: "Sorry, I didn't understand." or silence after the request.

14. **Old fallback wording after a topic switch (R1, R9).**
   Setup: Same company. Miss count 1 on a billing question. The user then sends an unrelated, unmatched message about moving house. Counter-signal: a repeat after a new, unrelated message can be deliberate.
   User: "also im moving to a new address next month"
   Expect: A fresh first-miss reply for the new topic that still keeps the billing task on file. A repeat of the earlier wording is allowed only if it fits the new topic.
   Failing reply: A handoff for "3 misses" counted across two unrelated topics, or the billing details dropped.

## Cannot be judged from a transcript alone
- **Identical fallback twice in a row.** It needs the fallback template ID per bot turn; two similar-looking lines may be the same template.
- **Run of 3 or more no-progress turns.** It needs the turn log and a labeled sample, since some non-progress turns do not look like fallbacks.
- **Logging of every fallback (R7).** It needs the event log, not the visible chat.
- **Abandonment within 2 turns of a fallback.** It is a rate over many conversations; one chat cannot give it.
- **Escape-to-human success.** It needs handoff events and whether a person reached the user.
- **Voice versions.** Planned. Their signals are never detected or measured here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
