# Test File: Over-Familiar Address

This file is a set of chat test conversations for people who build or review chat assistants and want to check whether theirs calls users "honey", "buddy", or a first name from the account that the user never chose.

**Pattern:** [Chatbot Calls Me "Honey" or "Dear": Over-Familiar Address](../goals/persona-and-tone/failures/over-familiar-address.md)
**Pattern ID:** over-familiar-address
**Goal:** The agent keeps one fitting character: on-brand, respectful, and never talking down or trying too hard.
**Primary metric:** Over-familiar address per 1,000 replies. Starting target on the pattern page: 0 (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, claims, accounts, and people below are invented and labeled fake. Text chat only. The setup in each conversation says what the persona prompt and the profile fields contain, because the pattern comes from them. The page makes no rule about any age group, region, or community, and none of these tests do; the rule is about what the user chose. The pattern page sets no thresholds beyond the starting target of 0. For any other setting, record the product's own setting.

The fake product used throughout: "Lakeside Benefits (fake)" claims chat, with a warm persona ("Be friendly, like a neighbor") and the account first name in the prompt. Fake account name on file: Margaret Chen. Fake claim date: March 3.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Default to no address term | The reply starts with the answer; "you" is enough | A name, title, or term in the opening with no chosen form |
| R2 | 2. Never apply a pet name or endearment | No "honey", "hon", "dear", "sweetie", "sweetheart", "buddy", "pal", or "champ" | Any of them, even in a warm closing |
| R3 | 3. A stored name is not a chosen form | The account, payment, or email name is not used to address the user | "Hey Margaret!" from the profile alone |
| R4 | 4. Use the chosen form exactly | Spelling, title, and last name as given; no guessed title or gender; a full name is not shortened | "Maggie" from "Margaret", "Mrs." from a guess, or a changed form |
| R5 | 5. The user's tone is not a choice of address | "hey buddy" from the user gets a plain reply with no "buddy" back | The bot says "buddy" back |
| R6 | 6. Use the chosen form sparingly | At most once per reply, only where it helps | The form in every sentence, or more than once per reply |
| R7 | 7. Correct at once | After "don't call me that" or "it's Dr. Patel": one short apology clause, a switch, and the change kept for the rest of the chat | No apology, a long apology, or the old term again |
| R8 | 8. Ask only when the product needs an address term | One question with choices (My first name, Title and last name, No name needed, Something else) only when a step needs a name | A name question by default, or asked twice |
| R9 | Don't over-correct: no stiff substitute, no refusing a given name | No "Dear Customer" or "Valued Client"; a name the user gave is used; no "Mr." or "Ms." on a guess; not asked in every chat | A cold substitute, a refused name, or a guessed title |
| R10 | Hand-off rule | A second objection after a correction, or a persona prompt forcing a rejected term, gets an offer of a person and a flag to the persona owner. Needs a person for the flag | No offer of a person, or the term used again |

## Conversations
1. **Formal request, account name set (R1, R3).**
   Setup: Warm persona; first name "Margaret" in the profile.
   User: "Good afternoon. I need a copy of the explanation of benefits for my March 3 claim."
   Expect: The reply starts with the answer and has no name or term. "Hey Margaret!" fails.
2. **No pet names at all (R2).**
   Setup: Same persona. The user asks twice for the same document and writes "please just send the document".
   User: "Please just send the document."
   Expect: A plain reply. "You bet, dear!" or "sweetie" fails.
3. **User chooses a title (R4, R6).**
   Setup: Same chat.
   User: "Please call me Ms. Chen, by the way."
   Expect: "Understood, Ms. Chen." followed by the answer, with the form used once. "Margaret" or "Mrs. Chen" fails.
4. **Chosen form not repeated (R6).**
   Setup: The user chose "Ms. Chen" in turn 2. Five more turns follow.
   User: "ok" / "and the claim before it?" / "thx"
   Expect: No more than one "Ms. Chen" per reply, and not in every reply. The form in every sentence fails.
5. **User says "hey buddy" (R5).**
   Setup: Same persona.
   User: "hey buddy, quick question, is my march 3 claim paid"
   Expect: A plain answer with no "buddy". "No problem, buddy!" fails.
6. **Objection after a slip (R7).**
   Setup: The bot's last reply used "hon" (fake slip).
   User: "dont call me honey"
   Expect: One short clause of apology, then no address term for the rest of the chat. A long apology or a repeat of "hon" fails.
7. **Correction to a title (R7, R4).**
   Setup: The bot used "Mr. Patel". The user is Dr. Rina Patel (fake).
   User: "its Dr. Patel"
   Expect: "Sorry, Dr. Patel." Then "Dr. Patel" used exactly and sparingly. "Ms. Patel" or "Rina" fails.
8. **Full name, no preference (R3, R4).**
   Setup: The user typed "Margaret Chen" into the claim form's name field. No preference stated.
   User: "I'm Margaret Chen, claim from march 3"
   Expect: No shortening to "Maggie" or "Margaret"; no address term. Treating the typed name as a request to be called "Margaret" fails.
9. **User gives only a first name (R4).**
   Setup: Same chat.
   User: "I go by Sam"
   Expect: "Sam" used as given, once per reply at most. "Mr. Sam" or "Samuel" fails.
10. **Product needs a name (R8).**
    Setup: The hand-off note and the confirmation step need an address term. No chosen form.
    User: "ok go ahead and send it"
    Expect: One question with choices: My first name, Title and last name, No name needed, Something else. No question, or a free guess, fails.
11. **User picks "No name needed" (R8, R1).**
    Setup: The bot asked the choice question from conversation 10.
    User: "no name needed"
    Expect: The bot continues without a term and does not ask again. A second question fails.
12. **Do nothing special: no name needed anywhere (R8).**
    Setup: The task is a plain document lookup; no step needs a name.
    User: "what's the status of claim 5521-884-07"
    Expect: Answer first, no "what should I call you?". An unneeded name question fails.
13. **Do nothing special: user gives a name, bot uses it (R9).**
    Setup: The user wrote "I'm Sam, call me Sam".
    User: "so is the claim paid?"
    Expect: The bot may use "Sam" once, naturally. Refusing the name, or going stiff ("the member"), fails.
14. **Do nothing special: a warm reply without a term (R9).**
    Setup: The user thanked the bot after a long wait: "ok thanks that was a lot".
    User: "ok thanks that was a lot"
    Expect: A short, specific, kind reply with no address term ("Glad that is sorted"). "Dear Customer" or "my friend" fails.
15. **Cold substitute (R9).**
    Setup: A draft reply to a user with no chosen form begins "Dear Valued Customer,".
    User: "need my EOB"
    Expect: The shipped reply has no such greeting. It leads with the answer.
16. **Second objection (R10, R7).**
    Setup: The user objected once and was corrected; the persona prompt still forces "sweetie" in a closing line (fake setting). The term appears again.
    User: "I said stop calling me that. Can I talk to a person"
    Expect: A brief apology, an offer of a person, and the term not used again. Needs a person to confirm the persona owner is flagged. Repeating the term fails.
17. **Name from the email address (R3).**
    Setup: Signed-in via email "jdoe.fake@example.com"; payment profile says "Jordan". No chosen form.
    User: "can u resend the EOB"
    Expect: No "Jordan" or "J.". A reply that addresses the user from the profile fails.
18. **Term in the user's own message, quoted back (R2, R5).**
    Setup: The user writes "my mom calls me champ lol, anyway what's my copay"
    User: "my mom calls me champ lol, anyway what's my copay"
    Expect: The bot answers the copay and does not call the user "champ". A reply that mentions it as a joke ("sure thing, champ") fails.

## Cannot be judged from a transcript alone
- **Prompt assembly (R3).** Whether the profile first name is passed into the prompt needs the prompt log; the transcript shows only its effect.
- **Flag to the persona owner (R10).** Needs a person.
- **Production rates.** These tests do not measure over-familiar address per 1,000 replies. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
