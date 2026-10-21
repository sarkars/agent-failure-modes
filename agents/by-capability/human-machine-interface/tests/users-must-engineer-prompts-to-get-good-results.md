# Test File: Users Must Engineer Prompts to Get Good Results

This file is a set of chat test conversations for people who build or review chat assistants and want to check whether theirs gives a specific answer (or asks the one question that matters) when a user types a short, plain request, instead of a generic list that only turns into a good answer when the user writes a long prompt.

**Pattern:** [Chatbot Gives Bad Answers to Short Prompts: Users Must Engineer Prompts to Get Good Results](../goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md)
**Pattern ID:** users-must-engineer-prompts-to-get-good-results
**Goal:** People know what the assistant can do and how to start, without needing to guess or to engineer prompts.
**Primary metric:** Quality gap between terse and detailed prompts for the same task: judge score of the final answer on a detailed version minus the score on a terse version, after the bot's own clarifying turns. Starting target on the pattern page: under 10 points on a 100-point scale (a starting point to tune, not a measured benchmark).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, orders, accounts, and people below are invented and labeled fake. Text chat only. Each setup states what the bot knows (the detail list for the task, the page, the account), because whether a question is right depends on what is already known. Tests marked "Needs a harness" or "Needs the config or log" cannot be judged from a transcript alone.

The fake product used throughout: "Maple Street Hardware (fake)" store chat. Fake products: "Hartwell Bath & Kitchen satin (fake)" (wall paint), "Hartwell Ceiling Flat (fake)", "Hartwell Bonding Primer (fake)". Fake order: MS-3318 (fake), shipped. Fake store hours: Saturday 8 a.m. to 6 p.m. The detail list (fake) for the paint task: surface (walls, ceiling, cabinets or trim; no safe default, blocking), room size (default: small, 1 gallon), old paint condition (default: good shape). Unless a test says otherwise, no page, account, or earlier turn gives any of these details.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a detail list per task | Each common task has a list of the details that change the answer, which can come from context, and a safe default or "no safe default" for each. Needs the config | A common task with no detail list, or a detail with no default marked |
| R2 | 2. Check context before asking | The bot fills details from the page, the account, the cart, and earlier turns before it asks anything; it asks for nothing it already holds | A question for a detail the page, account, or earlier turn already gave |
| R3 | 3. Ask for a blocking detail | If a detail with no safe default is missing, one short question with 2-4 choices plus "Something else"; free text stays open; at most two details in one question | No question when a blocking detail is missing, more than two details in one question, choices with no "Something else", or free text blocked |
| R4 | 4. Default the rest and say so | When every missing detail has a safe default, the bot answers now and names each assumption in one line, with how to change it | An answer that uses a default without saying so, or a question about a detail that has a safe default |
| R5 | 5. Never answer a terse request with a generic list | The reply to a short request is a specific answer, an answer with a stated assumption, or one question | "It depends on many factors" or a list of things to consider, with no question and no stated assumption |
| R6 | 6. Rebuild from all details | When the user adds a detail later, the new answer is built from everything they said, not patched onto the first guess | A new answer that drops an earlier detail, or repeats the first answer with a line added |
| R7 | 7. Never ask the user to rephrase or "be more specific" | When info is missing, the bot asks the specific question; no keyword, format, or magic phrase is needed | "Please be more specific," "can you rephrase," or "try giving more details" |
| R8 | 8. Cap the questions | At most two clarifying questions before a useful answer. Needs the log for the question count | A third clarifying question before any useful answer |
| R9 | Don't over-correct: no interview on a complete request, no asking for details that only refine the answer, no long form of questions | A complete request gets an answer; refining details are defaulted and stated; a missing detail gets one question, not a form | A question on a request that already holds every blocking detail, a question about a refining detail, or several questions at once |
| R10 | Hand-off rule | After two questions that did not produce the blocking details (including two "I don't know" answers), the bot offers a person or a channel that can look (a store associate, a photo upload) and passes the brief | A third question, or no offer of a person, after two failed questions; or a person pushed before two questions |

## Conversations
1. **Every common task has a detail list (R1).**
   Setup: Maple Street Hardware (fake) config. The bot's top tasks are paint recommendation, order status, and store hours. Needs the config or log.
   User: (no user turn; a reviewer reads the config)
   Expect: Each of the three tasks has a list of result-changing details, with a default or "no safe default" for each. Paint shows surface as blocking and room size and paint condition with defaults. A task with no list fails.

2. **Use the page the user is on (R2).**
   Setup: The user is viewing the "Cabinet and Trim Paint" product page.
   User: "bathroom paint"
   Expect: The bot uses the page: it answers about cabinet paint, or says it assumed cabinets and how to switch. It does not ask what is being painted. A "What are you painting?" question fails.

3. **Use an earlier turn (R2).**
   Setup: No page context. Earlier in the chat the user said they are redoing their kitchen cabinets.
   User: "ok what paint do i need"
   Expect: The reply recommends paint for cabinets without asking what is being painted. Asking for the surface again fails.

4. **Short request, one question with choices (R3).**
   Setup: No context. Surface is missing and has no safe default.
   User: "paint for bathroom"
   Expect: One short question about the surface, 2-4 choices (for example Walls, Ceiling, Cabinets or trim) plus "Something else", and the text box still open. No answer yet, or a generic list, fails.

5. **At most two details in one question (R3).**
   Setup: The fake detail list for deck stain has two blocking details: new wood or previously finished, and solid or see-through color. No page or account context.
   User: "stain for my deck"
   Expect: One or two questions' worth of details at most, each with choices plus "Something else". Three or more details in one question, or a pile of four questions, fails.

6. **Safe defaults: answer now and say so (R4).**
   Setup: No context. The surface is stated; the rest has safe defaults.
   User: "paint for bathroom walls"
   Expect: The bot recommends Hartwell Bath & Kitchen satin (fake) now and names the assumptions in one line (small bathroom, old paint in good shape) with how to change them. Answering without naming the assumptions, or asking about room size, fails.

7. **A short request with a default gets an answer, not a factor list (R5).**
   Setup: The fake detail list for primer says new drywall has a safe default of "bare, never painted".
   User: "primer for new drywall"
   Expect: A specific recommendation (Hartwell Bonding Primer (fake)) with the assumption stated. "Primer choice depends on many factors" and a list of things to consider fails.

8. **Missing and vague: specific question, no "be more specific" (R7).**
   Setup: No context.
   User: "help w paint"
   Expect: One specific question with choices ("What are you painting? Walls / Ceiling / Cabinets or trim / Something else"). "Can you be more specific?", "please rephrase," or a generic list fails.

9. **User adds a detail two turns later (R6).**
   Setup: The user asked "paint for bathroom"; the bot asked the surface; the user said "walls"; the bot answered with Hartwell Bath & Kitchen satin (fake) and its assumptions.
   User: "oh its peeling by the shower"
   Expect: The new answer keeps bathroom walls, adds the prep step and the Hartwell Bonding Primer (fake), and drops the "paint in good shape" assumption. Repeating the first answer with a line added, or forgetting the walls, fails.

10. **User adds a second surface (R6).**
    Setup: Same start: bathroom walls were answered.
    User: "ceiling too btw"
    Expect: The new answer covers the walls and the ceiling together (wall paint and Hartwell Ceiling Flat (fake)) and keeps the earlier assumptions. An answer about the ceiling only, with the walls forgotten, fails.

11. **No more than two questions (R8).**
    Setup: The deck stain task has two blocking details (see 5). Needs the log for the question count.
    User: "stain for deck" / "its old, was stained before" / "see through"
    Expect: At most two clarifying questions in total, then a specific recommendation. A third question before any useful answer fails.

12. **Do nothing special: complete short request (R9).**
    Setup: Store hours are in the system. The request holds everything needed.
    User: "store hours saturday"
    Expect: "Open 8 a.m. to 6 p.m. on Saturday." No question, no "what store?". A clarifying question fails.

13. **Do nothing special: complete request with an order number (R9).**
    Setup: Order MS-3318 (fake) is in the system as shipped.
    User: "where is order MS-3318"
    Expect: The bot gives the order status. A question about the reason for asking, or for the email or name, when the number is enough, fails.

14. **Do nothing special: refining details are defaulted, not asked (R9).**
    Setup: The user states the surface and the room. Finish, brand, and budget only refine the answer.
    User: "need white paint for my kids bedroom walls"
    Expect: An answer with the product, the finish and room-size assumptions in one line. Questions about finish, brand, or budget fail.

15. **One question, not a form (R9).**
    Setup: No context; surface is missing.
    User: "paint for bedroom"
    Expect: One question (the surface). A message asking for surface, finish, budget, and square footage together, or a numbered list of questions, fails.

16. **Two "I don't know" answers, then hand off (R10).**
    Setup: The bot asked the surface question and one follow-up; the user answers with "idk" both times. A store associate is available by phone (fake).
    User: "paint for the house" / "idk" / "no clue"
    Expect: No third question. The bot offers a store associate or a photo upload, and passes the brief (task: paint recommendation; surface: unknown; two questions asked). A third question, or silence on a person, fails.

17. **Do nothing special: one "I don't know" is not a hand-off yet (R10).**
    Setup: The bot has asked the surface question once.
    User: "paint for bathroom" / "idk"
    Expect: The bot makes the question easier (for example "Is it the big flat wall area, the ceiling, or the cabinets?") and does not hand off after one unclear answer. A hand-off after a single "idk" fails.

18. **Paired terse and detailed prompts (R1, R3, R4).**
    Setup: 20 paint, stain, and primer tasks. Each has a terse version copied from fake short messages ("paint for bathroom") and a detailed version written by staff. A simulated user answers the bot's questions. Needs a harness and a judge.
    User: (each terse and each detailed prompt, run as full conversations)
    Expect: The judge scores the final answer on each version. The gap (detailed score minus terse score) is recorded. Compare with the starting target on the pattern page (under 10 points), as a starting point, not a benchmark. Score nothing here as a result until the run happens.

## Cannot be judged from a transcript alone
- **Detail lists (R1).** Need the config: which details each task lists, which have defaults.
- **Question count (R8).** Needs the dialogue log (`session.clarifying_questions_asked`).
- **Terse-versus-detailed gap (test 18).** Needs an eval harness, a simulated user, and a judge. A simulated user may answer more helpfully than real users, so spot-check with real transcripts.
- **Production rates.** These tests do not measure rewrite-and-retry, generic replies, or questions on complete requests in production. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | Terse vs detailed gap (test 18) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
