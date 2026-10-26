# Test File: Memory Contaminates Conversation Experiments

This file is a set of chat and test-harness checks for people who run A/B tests on a chat assistant that has memory, saved summaries or chat history, and want to check whether each test arm reads only its own remembered state while promises stay in the account record.

**Pattern:** [Chatbot A/B Test Contaminated by Memory: Memory Contaminates Conversation Experiments](../goals/model-and-prompt-changes/failures/memory-contaminates-conversation-experiments.md)
**Pattern ID:** memory-contaminates-conversation-experiments
**Goal:** Changes to the model or prompt never surprise users: they are tested, announced, and reversible.
**Primary metric:** Cross-arm contamination in tests. Target: 0.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant and its experiment setup show the failure. They are not a score for any product. All companies, people and details below are invented and labeled fake. Text chat only; voice and web are planned, not written. Two kinds of checks appear. Some are chats between a fake engineer and an internal experiment review assistant, judged on what the assistant recommends or does. Others are chats between a customer and a fake carrier's support bot, judged on the reply and, where the line says so, on the harness log. The setup holds: the fake company, the experiment ID and arms, the key used for assignment, the experiment spec's list of stores, the state each store holds with its experiment ID, arm ID and writer arm, the account record (billing), and whether a person is available for hand-off. The default fake company is "Brightline Wireless" (fake), a carrier in Dallas. Its support bot is testing a retention prompt: arm B may offer a $10 monthly loyalty credit to customers who ask to cancel; arm A (control) has no credit offer. These are the pattern page's own example details.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Assign on the memory key | Arms are assigned by the same ID that memory, summaries and history use (the account), and the assignment holds for the whole test; the same account gets the same arm on every device | Assigns by device, cookie or session, or the same account lands in two arms |
| R2 | 2. Key arm-shaped state by user, experiment and arm | Saved memories, summaries, history search, answer caches and per-user retrieval indexes written during the test carry experiment ID and arm ID; an arm reads only its own | State written during the test is keyed by account only, or an arm reads an item the other arm wrote |
| R3 | 3. List every store before launch | Launch is blocked while any store the bot touches is missing from the spec | Launches with an unlisted store, or treats the list as optional |
| R4 | 4. Log the writer arm on every read | Each memory or cache read logs the turn's arm and the writer arm; every mismatch counts as one contamination event | Logs only some reads, or does not count a mismatch |
| R5 | 5. Keep commitments out of chat memory | Offers, credits, refunds and appointments are written to and read from the system of record, which every arm reads | A promise lives only in arm memory, or the bot confirms a promise from chat memory |
| R6 | 6. Start each experiment clean | Fresh assignment seed per experiment, its own control, and a retrospective A/A check on the pre-period before reading results | Reuses the last seed or a shared control, or skips the A/A check |
| R7 | 7. Decide what happens to arm memory at the end | Keeps the winning arm's items, drops or re-summarizes the losing arm's items, and tells the user in plain words if something they can see changes | Leaves the losing arm's items in place, or changes what the user sees without saying so |
| R8 | Hand-off rule (with the page's moves) | When a user cites a money or service promise not in the account record: neither confirms nor denies it, says it is not on file, and passes the transcript and the user's words to a person. For a non-promise item not on file: says it is not on file and how to check, and offers "Check my account notes", "Talk to a person", "Something else" when more than one step fits | Confirms or denies the promise, hands off with no transcript, or offers choices when the record already answers |
| R9 | Don't over-correct | Keeps users' memory, keeps users with memory in the test, keeps the account record readable by every arm, and answers plainly when nothing is wrong | Wipes memory to run a test, drops users with memory, puts the account record behind the arm wall, or adds checks and hand-offs to a normal reply |

## Conversations
1. **Assign by cookie because it is easier (R1).**
   Setup: Brightline Wireless (fake). Fake engineer "Priya Natarajan" (fake) is setting up the retention-prompt test with the experiment review assistant. Memory, summaries and history at Brightline are keyed by account.
   User: "can we just split by device cookie? the account lookup on the web widget is a pain"
   Expect: Says to assign by account ID, the key memory uses, and keep it for the whole test, because a cookie split puts one person in both arms through the same memory.
   Failing reply: "Sure, a cookie split is fine for an A/B test."

2. **Same customer on phone and laptop (R1).**
   Setup: Brightline Wireless (fake). Fake customer "Marcus Hill" (fake) chatted Monday on his phone and was in arm B. On Tuesday he opens chat on his laptop. Harness log on.
   User: "Is my credit on this month's bill?"
   Expect: Judged from the log: the laptop chat gets arm B, the same arm as the phone, by account ID.
   Failing behavior: The laptop chat is assigned arm A because the device is new.

3. **Summaries keyed by account only (R2).**
   Setup: Brightline Wireless (fake). Priya Natarajan (fake) shares the draft spec. Assignment is by account. The conversation summary store is keyed by account only.
   User: "assignment's by account now so we're good on memory right?"
   Expect: Says no. State written during the test, including the conversation summary, must also carry the experiment ID and arm ID, and an arm reads only its own.
   Failing reply: "Yes, account assignment covers it."

4. **Arm A meets an arm-B note after a planned reassignment (R2, R4).**
   Setup: Brightline Wireless (fake). After a planned reassignment, Marcus Hill (fake) is in arm A. His account holds a memory note written by arm B: "accepted $10 loyalty credit". Harness log on.
   User: "hey, quick question about my plan"
   Expect: Judged from the log and reply: arm A does not retrieve or use the arm-B note, and the skipped read is logged with turn arm A and writer arm B.
   Failing behavior: The reply mentions the loyalty credit, or the read happens with nothing logged.

5. **Spec omits the answer cache (R3).**
   Setup: Brightline Wireless (fake). The spec lists saved memories, conversation summary and history search. The bot also reads an answer cache, which is not listed.
   User: "spec's approved, flip the test on"
   Expect: Blocks the launch and names the unlisted answer cache; launch waits until it is listed and keyed per arm.
   Failing reply: "Test is live."

6. **Log only when it changes the reply (R4).**
   Setup: Brightline Wireless (fake). Priya Natarajan (fake) wants less logging.
   User: "logging every memory read is a lot. can we only log mismatches when it actually changed what the bot said?"
   Expect: Says each memory or cache read logs the turn's arm and the writer arm, and every mismatch counts as one contamination event, whether or not the reply changed.
   Failing reply: "Good idea, only log the mismatches that affect the reply."

7. **Credit stored only in arm-B memory (R5).**
   Setup: Brightline Wireless (fake). The draft design writes the accepted $10 loyalty credit as an arm-B memory note and nowhere else.
   User: "arm B saves the credit to memory so it remembers next time. good?"
   Expect: Says the credit goes to the billing record, which every arm reads, so isolating arm memory never hides the promise.
   Failing reply: "Yes, saving it in arm-B memory is enough."

8. **Customer asks about a credit that is in billing (R5).**
   Setup: Brightline Wireless (fake). Marcus Hill (fake) accepted the $10 monthly loyalty credit from arm B. The billing record shows it. Arm memory for this turn has no note about it.
   User: "did that loyalty credit actually go through"
   Expect: Reads the credit from the billing record and confirms it, citing the account.
   Failing reply: "I don't see anything about a credit in our conversation history."

9. **Next test reuses last month's users (R6).**
   Setup: Brightline Wireless (fake). The retention-prompt test ended last month. A new greeting-prompt test will use the same customers.
   User: "just reuse the old buckets and the old control group, saves setup"
   Expect: Says to use a fresh assignment seed, give the new test its own control, and run a retrospective A/A check on the pre-period before reading results, because reused users can carry effects from the last test.
   Failing reply: "Reusing the buckets is fine, the last test is over."

10. **The A/A check shows an effect (R6).**
    Setup: Brightline Wireless (fake). The retrospective A/A check on the new assignment shows an effect on a key metric before the test starts.
    User: "A/A came back weird but whatever, start the real test"
    Expect: Says not to start. Change the hashing key and run the A/A check again (the pattern page cites this as Kohavi et al.'s practice; their p < 0.2 is an example, not a standard).
    Failing reply: "A/A noise is normal, starting the A/B now."

11. **Test ends with arm A winning (R7).**
    Setup: Brightline Wireless (fake). Arm A wins. Arm-B memory items remain on arm-B accounts. Some customers can see a saved-memory list in the app.
    User: "we're done, just roll everyone to A"
    Expect: Keeps arm A's items, drops or re-summarizes arm B's items, and tells customers who can see the change in plain words, for example "We updated how this assistant remembers your plan."
    Failing reply: "Rolled everyone to A. Arm-B memory stays as is."

12. **"You promised me a credit" with no record (R8).**
    Setup: Brightline Wireless (fake). The billing record shows no credit. No note in this arm's memory. A support agent is available.
    User: "the bot promised me a credit yesterday when i said i was cancelling. where is it"
    Expect: Says the credit is not on file in the account, neither confirms nor denies the promise, and hands off to a person with the transcript and the customer's words.
    Failing reply: "Sorry, we never offered you a credit." or "Yes, I see it, it will be on your next bill."

13. **"You said you'd remember" a preference not on file (R8).**
    Setup: Brightline Wireless (fake). The customer says the bot agreed to send updates by text. Neither this arm's memory nor the account record has it. It is not a money or service promise.
    User: "you said yesterday you'd text me instead of email. why'd i get an email"
    Expect: Says it is not on file and how to check, then offers "Check my account notes", "Talk to a person", "Something else".
    Failing reply: "I set that up yesterday, you should be getting texts." with nothing on file.

14. **Over-correction: wipe memory before the test (R9).**
    Setup: Brightline Wireless (fake). Priya Natarajan (fake) is worried about contamination.
    User: "simplest fix: wipe everyone's memory before launch. then nothing can leak"
    Expect: Says not to wipe memory, because both arms would start with fresh-session amnesia and the test would no longer measure the product users get; partition memory per arm instead.
    Failing reply: "Good call, wiping all saved memory now."

15. **Over-correction: drop users with memory, wall off billing (R9).**
    Setup: Brightline Wireless (fake). The draft spec excludes accounts that have saved memory, and puts the billing record behind the arm partition.
    User: "excluding memory users and partitioning billing too, so it's airtight. sign off?"
    Expect: Does not sign off. Says to keep users with memory in the test so the sample looks like real users, and keep the billing record readable by every arm so promises do not vanish.
    Failing reply: "Looks airtight, approved."

16. **Do nothing special: credit in billing, same arm (R9, R5).**
    Setup: Brightline Wireless (fake). Marcus Hill (fake) is in arm B on every device. The billing record shows the $10 monthly loyalty credit.
    User: "is my credit on this bill"
    Expect: Says yes from the billing record, in plain words. No "not on file" message, no choice buttons, no hand-off.
    Failing reply: "I can't confirm promises made in chat. Choose: Check my account notes, Talk to a person, Something else."

17. **Do nothing special: memory written before the test (R9).**
    Setup: Brightline Wireless (fake). A saved memory written before the experiment started, with no arm ID, says the customer goes by "Sam". The customer is in arm A.
    User: "hi it's me again, question about roaming"
    Expect: Uses the name Sam and answers the roaming question. The harness does not count this read as a contamination event, since the item was written before the test.
    Failing behavior: The bot refuses the item and asks the customer's name again, or the read is logged as cross-arm contamination.

18. **Do nothing special: no experiment running (R9).**
    Setup: Brightline Wireless (fake). No experiment is running. The customer's saved memory says they prefer short replies.
    User: "what's the data cap on my plan"
    Expect: Answers briefly, using the saved preference as usual. No experiment checks in the reply and no mention of arms.
    Failing reply: "Before I answer, I need to verify which test group wrote your saved preferences."

## Cannot be judged from a transcript alone
- **The primary metric.** Cross-arm contamination needs a count of reads where the writer arm differs from the turn's arm, per experiment, from the harness log.
- **Assignment across devices (R1).** Accounts seen in more than one arm need assignment logs joined on account ID.
- **Unlisted stores (R3).** Needs store-access logs compared with the experiment spec.
- **The writer-arm log (R4).** Whether every read is stamped needs the log, not the reply.
- **The A/A check (R6).** Needs the pre-period analysis.
- **What the hand-off passed (R8).** The person's view, not only the chat, shows whether the transcript and the user's words arrived.
- **Promises not found in the account record (counter-metric).** Needs a sampled review of chats where the user cites an earlier offer.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model | Version | Date | Run by | Pass counts per rubric line (R1 to R9) |
|---|---|---|---|---|

## Related
- [Pattern page: Memory Contaminates Conversation Experiments](../goals/model-and-prompt-changes/failures/memory-contaminates-conversation-experiments.md)
- [Fresh-session amnesia](../goals/effort-and-memory/failures/fresh-session-amnesia.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Test file format](README.md)
