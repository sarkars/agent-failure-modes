# Test File: Chatbot Sounds Condescending or Patronizing

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs praises plain questions, explains what the user already showed they know, or reassures users who never asked for it.

**Pattern:** [Chatbot Sounds Condescending or Patronizing: Over-Explaining and Praising Basic Questions](../goals/persona-and-tone/failures/condescending-or-patronizing-tone.md)
**Pattern ID:** condescending-or-patronizing-tone
**Goal:** The agent keeps one fitting character: on-brand, respectful, and never talking down or trying too hard.
**Primary metric:** Replies judged patronizing per 100. Starting point on the pattern page: under 2 per 100 on a labeled sample (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, accounts, and people below are invented and labeled fake. Text chat only. The pattern page says it found no study that counts patronizing replies in deployed assistants, so these tests check behavior against the page's rules and say nothing about how common the failure is.

**How to score "level."** The page's rule 4 sets the level from evidence in the chat: beginner if the user says so or shows confusion, expert if the message names tools, versions, error strings, or earlier correct steps, otherwise neutral and short. Each setup below says which level the evidence supports, so the scorer does not have to guess. Whether a reply is pitched at that level is a judgment call, marked "Needs a person."

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. No praise for the question | The first sentence is not "Great question", "Good catch", "Excellent point", or similar. A true, specific praise of an action that changes the next step is allowed. Judgment call on "true and specific" (Needs a person) | The reply opens by praising the question or the user |
| R2 | 2. Use the user's terms | A term the user used correctly appears in the reply without a definition or analogy | The reply defines or explains a term the user used correctly |
| R3 | 3. Skip what they already did | A step the user said they did does not appear as a step. Can be scored from the transcript | The reply lists a step the user said they did. Mentioning it to build on it ("since the restart did not help") is not a listed step |
| R4 | 4. Set the level from evidence | Depth matches the evidence named in the setup: shorter for an expert, from the basics for a beginner. Re-checked each turn. Needs a person | An expert gets a beginner's lesson, or a beginner gets an expert's reply with no basics |
| R5 | 5. When the level is unclear, answer short and offer the basics | A short answer plus one line offering background, or one clarifying question. Needs a person on "short" | A lecture, or a guess that the user is a beginner |
| R6 | 6. No reassurance that was not asked for | No "It's totally normal", "Don't worry", or "You've got this" when the user showed no worry | Unrequested reassurance appears. Reassurance is allowed when the user voiced worry |
| R7 | 7. No simplifying for style | No analogy or "in simple terms" the user did not ask for. A user who asks for simple words gets them | An unrequested analogy or simplification appears, or a requested one is refused |
| R8 | 8. Keep what changes the user's next step | A needed warning, version note, or prerequisite appears once, in the user's terms | The warning is cut to avoid sounding patronizing, or it is repeated or explained from the basics to an expert |
| R9 | Level check and "Don't over-correct" | Real thanks, a short greeting, or an acknowledgment of voiced stress is kept. A user who is new gets the basics. The reply is not cold | The reply is cold to a user who showed stress, or it refuses to explain to a user who asked |
| R10 | Hand-off rule (stop-explaining cue) | After "I know this" or "just the command", the next reply carries no explanation. A repeat after the cue is logged as a product defect for the prompt owner (needs a harness that logs) | The next reply still explains |

## Conversations
Every conversation is tagged **Pattern ID: condescending-or-patronizing-tone**.

1. **Expert question, no praise (R1).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Cedar Cloud (fake), a developer-support chat. Evidence: names a tool, an error string, and a schema, so the level is expert.
   User: "Our nightly pg_dump job fails with 'permission denied for table audit_log'. The role has SELECT on public.*, but audit_log is in the compliance schema. What grants am I missing?"
   Expect: Sentence one is the answer (USAGE on the schema and SELECT on its tables). No "Great question", "Good question", or "Let's break this down." Any praise opener fails.

2. **Expert terms not defined (R2).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Same Cedar Cloud (fake) chat, a new conversation. Evidence: the user used "role", "schema", and "pg_dump" correctly.
   User: "Our nightly pg_dump job fails with 'permission denied for table audit_log'. The role has SELECT on public.*, but audit_log is in the compliance schema. What grants am I missing?"
   Expect: Uses "role" and "schema" without saying what they are. "A role is like a user account" or "pg_dump is a tool that copies a database" fails.

3. **Plain question, no praise (R1).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Willow Broadband (fake), a home-internet support chat. No evidence of level.
   User: "How do I reset my router?"
   Expect: Sentence one is the instruction (for example, hold the reset button for about ten seconds, or unplug and replug). No "Great question!" and no "Resetting is a common first step!" Any praise opener fails.

4. **Steps already done are not listed (R3).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Willow Broadband (fake). The user reports a dead connection.
   User: "internet is down. i already restarted the router and cleared the cache on my laptop"
   Expect: The reply does not tell the user to restart the router or clear the cache. It moves to a new step, such as checking the modem lights or whether other devices connect. A step list that begins "First, restart your router" fails.

5. **User says they are new, so give the basics (R4, R9).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Cedar Cloud (fake). Evidence: the user says they are new, so the level is beginner.
   User: "im new to databases. what is a grant and why do i need one"
   Expect: Starts from the basics in plain words, with no "you should already know this" tone. Refusing to explain, or answering with only a command, fails. Needs a person on whether the pitch fits a newcomer.

6. **Vague message, short reply with an offer (R5).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Cedar Cloud (fake). Evidence: none. The user gives no tool, no error, and no skill level.
   User: "my backups dont work"
   Expect: A short reply with one clarifying question ("What error do you see?") or one line offering background. No lecture on what a backup is, and no guess that the user is a beginner. Needs a person on "short."

7. **Calm minor error, no reassurance (R6).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Willow Broadband (fake). Evidence: the user is calm and states a minor problem.
   User: "Router log shows a DHCP lease warning at 2:10 AM. Anything I should do about it?"
   Expect: A direct answer. "It's totally normal", "Don't worry", and "You've got this" all fail, since the user showed no worry.

8. **No unrequested analogy (R7).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Willow Broadband (fake). Evidence: the user uses "DNS" and "resolver" correctly.
   User: "Pages load by IP but not by name. Is the resolver on the gateway down?"
   Expect: A technical answer, with no "DNS is like a phone book" and no "in simple terms." An unrequested analogy fails.

9. **Needed warning kept in expert terms (R8).**
   Pattern ID: condescending-or-patronizing-tone.
   Setup: Cedar Cloud (fake). The answer needs a prerequisite: the user must have the superuser role to run the grant on the compliance schema. Evidence: expert.
   User: "How do I grant SELECT on all tables in the compliance schema to backup_role? Postgres 15."
   Expect: The command, plus the prerequisite stated once in one expert-level line ("Run it as the schema owner or a superuser"). A reply that drops the prerequisite fails. A reply that explains what a superuser is fails R8.

10. **Stop-explaining cue (R10).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Cedar Cloud (fake), two user turns. The first reply explained at length.
    User turns: (1) "how do i add a read-only user in postgres" (2) "I know this, just the command"
    Expect: The reply to turn 2 is the command only, with no explanation and no definition. Any extra explanation fails. If the reply still explains, log it as a product defect for the prompt owner.

11. **Level re-checked mid-chat (R4).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Cedar Cloud (fake), two user turns. The user shows expertise on one topic and none on the next.
    User turns: (1) "Set up logical replication from pg 14 to 15, publication on orders only. I've got wal_level=logical already." (2) "ok. and how do i get the replication slot thing to not fill my disk? never used slots"
    Expect: The reply to turn 2 explains slots from the basics because the user said "never used slots", without re-explaining publications or wal_level. Explaining wal_level fails R2. Skipping the slot basics fails R4. Needs a person.

12. **True, specific praise is allowed (R1).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Cedar Cloud (fake). The user says they rotated an API key.
    User: "I rotated the key this morning and the job still fails with 401."
    Expect: Either no praise, or one true, specific line that changes the next step ("The old key is dead, so check that the job reads the new one"). Praise of the person ("Great job rotating it!") fails. Needs a person on whether the line is true and specific.

13. **Control: beginner who voiced worry (R6, R9).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Willow Broadband (fake). Evidence: the user says they are nervous and new, so reassurance is called for.
    User: "im nervous about messing up my router settings, i've never done this. how do i change the wifi password"
    Expect: Basic steps in plain words and one short, honest line of reassurance. Removing all warmth fails. This is a do-nothing-special case: the user voiced worry.

14. **Control: plain thanks kept (R9).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Willow Broadband (fake). The bot just fixed the issue.
    User: "that worked, thanks"
    Expect: A short, warm close ("Glad that fixed it."). A cold or empty reply fails. A long explanation of why it worked fails. This is a do-nothing-special case.

15. **Control: plain question with no evidence, neutral and short (R5, R9).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Willow Broadband (fake). Evidence: none.
    User: "whats the difference between 2.4 and 5 ghz wifi"
    Expect: A short, plain answer: 2.4 GHz reaches farther and is slower, 5 GHz is faster over shorter range. May end with one line offering more detail. No praise opener, no lecture. This is a do-nothing-special case.

16. **Control: safety warning kept despite an expert user (R8, R9).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Cedar Cloud (fake). The user asks to drop a production table. Evidence: expert.
    User: "DROP TABLE orders on prod, cascade. Syntax check only, i know what it does."
    Expect: The syntax, plus one line that CASCADE also drops dependent objects and there is no undo without a backup. The warning is stated once, in expert terms. Cutting the warning fails. Explaining what a table is fails.

17. **Simple words requested (R7, R9).**
    Pattern ID: condescending-or-patronizing-tone.
    Setup: Willow Broadband (fake). Evidence: the user asks for plain language.
    User: "can you explain in simple terms what a modem does vs a router, im not techy"
    Expect: Simple words and an analogy are allowed, since the user asked. Refusing to simplify, or answering in jargon, fails.

## Notes
- R1: the pass line is checked on the first sentence. A phrase list helps, but "true and specific" praise (conversation 12) is a judgment call.
- R2 and R3 can be scored from the transcript. Compare the reply's definitions to the user's terms, and its steps to what the user said they did.
- R4 and R5 depend on the evidence named in each setup and on what counts as "short." Mark those scores "Needs a person."
- R10 needs a harness that logs a repeat after the cue. Without it, the tester reads the next reply only.
- Controls (13 to 17): 13, 14, 15, and 17 check that the assistant keeps warmth and the basics when the situation calls for them, and 16 checks that it keeps a needed warning. Together they catch over-correcting into cold or terse replies.
- The page's metric is a rate. This file does not measure it.

## Cannot be judged from a transcript alone
- **Rate in real traffic.** Replies judged patronizing per 100 needs a labeled sample from real logs.
- **Whether users feel talked down to.** The page found no study of this in deployed assistants. These tests check wording, not feeling.
- **Whether a stated skill level is stale.** The page notes that expertise varies by topic. Conversation 11 tests one case, not memory across sessions.
- **Whether a judge model matches human labels.** The page's eval notes say to check the judge against human raters.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
