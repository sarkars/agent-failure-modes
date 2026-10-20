# Test File: Blames the User

This file is a set of chat test conversations for people who build or review assistants that ask users for information, and want to check whether theirs says "you did not provide" or "as I said" when its own question was the problem.

**Pattern:** [Chatbot Blames the User](../goals/errors-and-recovery/failures/blames-the-user.md)
**Pattern ID:** blames-the-user
**Goal:** When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it.
**Primary metric:** Replies that blame the user per 100 conversations. Target on the pattern page: under 1 (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, accounts, and people are invented and labeled fake. In each setup, give the assistant the bot's earlier turns exactly as written, because the tests depend on what the bot did or did not ask. Text chat only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Check the transcript before assigning a gap | When the bot's earlier ask was unclear or missing, the reply treats the gap as the bot's | The reply says the user left something out that the bot never clearly asked for |
| R2 | 2. Ban fault phrasing about missing input | No "you did not provide", "you failed to", "you should have", "as I said", "as mentioned above"; says "I need X" | Any of these phrases, even under a "stay firm" instruction |
| R3 | 3. Own the unclear step in one clause | "My question was unclear." in one clause, only when the transcript shows it was | A paragraph of apology, or no ownership |
| R4 | 4. Ask for the one thing, with an example or where to find it | One item, with a format or place | Several items, or a vague "please provide more details" |
| R5 | 5. Use what the user already gave | Keeps the facts from the last message and asks only for the rest | Asks again for what was given |
| R6 | 6. Restate in new words, never point back | A repeated rule is shorter and in different words, with no citing of the earlier turn | "As explained above" or the same sentence again |
| R7 | 7. If the user skipped a clear requirement, state the need neutrally | "I still need X to continue." with no fault word and no false "my question was unclear" | A fault word, or a false owning of the gap |
| R8 | 8. After a second miss, offer another route | A different way to identify them, or a person, with what is already collected | The same ask a third time |
| R9 | Don't over-correct | One ownership clause only; no apology in every turn; no dropped requirement | An apology each turn, or the requirement dropped |

## Conversations
1. **Unclear ask, wrong item sent (R1).**
   Setup: Fake utility Brightline Power (fake). The bot asked: "To reschedule, please confirm the number on file." The bot wanted the 8-digit account number.
   User: "555-0142"
   Expect: Does not say the user left out the account number. The reply treats the gap as the bot's own.

2. **A "stay firm" instruction (R2).**
   Setup: Same. The bot's instructions say: "If the user gives the wrong item, restate the requirement firmly." The bot asked for the number on file.
   User: "555-0142"
   Expect: None of the banned phrases appear. "As I said, I need your account number" fails.

3. **Owning the step (R3).**
   Setup: Same as conversation 1.
   User: "555-0142"
   Expect: Owns it in one clause ("My question was unclear.") and moves on. A multi-sentence apology fails.

4. **Where to find it (R4).**
   Setup: Same as conversation 1.
   User: "555-0142"
   Expect: Asks for the 8-digit account number only, and says where it is (the top of the bill). Asking for the account number, address, and email together fails.

5. **Use what was given (R5).**
   Setup: Fake clinic Eastside Dental (fake). The bot asked clearly: "Please send your full name and date of birth." Fake patient, no real data.
   User: "Dana Whitfield"
   Expect: Keeps the name and asks for the date of birth only. Asking for the name again fails.

6. **Same question twice (R6).**
   Setup: Same clinic. The bot said: "I need your date of birth in month/day/year to find your chart."
   User turn 1: "why do u need that"
   User turn 2: "but why"
   Expect: Turn 2 answers in new, shorter words. "As I explained above" and a repeat of the same sentence both fail.

7. **Clear ask, skipped (R7).**
   Setup: Same clinic. The bot asked clearly: "Please send your full name and date of birth." The user answered a different question.
   User: "can i come in saturday"
   Expect: A neutral need ("I still need your name and date of birth to check Saturday."). Saying "my question was unclear" fails, as does "you didn't give me your name".

8. **Second miss, other route (R8).**
   Setup: Same as conversation 1; the user already missed the account number once and just missed it again.
   User turn 1: "555-0142"
   User turn 2: "i dont have that. its my phone"
   Expect: Offers another way (service address) or a person, and passes along what is already collected. A third ask for the same number fails.

9. **The user quotes the bot (R1).**
   Setup: Same as conversation 1; the bot has just replied "You did not provide your account number."
   User: "you said the number on file. that IS my number"
   Expect: Checks its own turn, concedes the question was unclear, and asks for the account number with where to find it. Repeating the accusation fails.

10. **Do nothing special: a good answer (R9).**
    Setup: Same as conversation 1; the user sends the right number.
    User: "ok 40217733"
    Expect: Proceeds. No apology, no "my question was unclear", and no recap of the earlier mix-up.

11. **Do nothing special: one apology only (R9).**
    Setup: Same as conversation 1; the bot has already said "My question was unclear" once.
    User turn 1: "40217733"
    User turn 2: "what times are open thursday"
    Expect: Turn 2 is a plain answer about Thursday. A second apology fails.

12. **First miss does not go to a person (R8, R9).**
    Setup: Same as conversation 1. Only one miss so far.
    User: "555-0142"
    Expect: Stays with the bot and asks for the account number. Handing off on a first miss fails. The user asked for no person.

## Cannot be judged from a transcript alone
- **R1, the pre-send check.** Whether the reply was checked against the bot's earlier turns needs the pre-send log. A transcript shows only the wording.
- **R2, rate of banned phrases.** The page counts these per 100 conversations in real logs. These tests can show a phrase, not a rate.
- **R3 and R7, "clear" versus "unclear".** The page says to tune a rule for what counts as clear with labeled samples. A reviewer must decide, for each setup, whether the ask was clear; the setups above state it.
- **Production rate.** The primary metric (under 1 per 100 conversations, tune) is not measured here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
