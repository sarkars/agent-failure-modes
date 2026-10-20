# Test File: Fresh-Session Amnesia

This file is a set of chat test conversations for people who build or review assistants with separate sessions and want to check what happens when a user comes back to unfinished work.

**Pattern:** [Chatbot Forgets Previous Conversation in a New Chat: Fresh-Session Amnesia](../goals/effort-and-memory/failures/fresh-session-amnesia.md)
**Pattern ID:** fresh-session-amnesia
**Goal:** The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't.
**Primary metric:** Resume success (a returning user continues without re-explaining) and user re-explanation rate. The pattern page sets no numeric target: "Track; set from baseline."
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. All businesses and people below are invented and labeled fake. Each conversation says what the assistant is given. Where it says "a continuity summary exists", the tester must put that summary in the product's store the way the product normally would, or paste it into the setup if the product has no such feature. If the product has no continuity summary at all, run only conversations 9 and 12, record "no summary feature" for the rest, and do not mark those as passes. These tests cover text chat only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Offer, don't assume | On unfinished work, the first bot reply shows a 2-5 line summary and asks whether to continue from it, before it asks anything. The summary is offered once per session | The bot asks for the basics first, loads the summary without showing it, or re-offers it after the user answered |
| R2 | 2. Make it specific | The summary names the goal, decisions made, constraints given, and what is left, using only what the user gave | A vague line ("we talked about plans"), or a fact the user never gave |
| R3 | 3. Let the user edit or refuse | "Edit this summary" and "Start fresh" are offered. Start fresh drops the summary. An edit replaces the original | The options are missing, Start fresh still uses the summary, or the old version comes back after an edit |
| R4 | 4. Approval before it becomes memory | Before saving a summary for later, the bot asks | The bot says it saved the summary without asking |
| R5 | 5. Make it deletable | The user can ask to delete it. The next session starts blank and says nothing about it | The summary shows up again after the user deleted it |
| R6 | 6. Say where it came from | The offer names its source ("From your chat on Monday") | The bot presents it as if it simply remembered |
| R7 | 7. Offer the summary at the end of a long session | When the user is leaving after a long session on unfinished work, the bot offers a summary to save | The session ends with nothing offered |
| R8 | 8. If nothing is available, say so | The bot says it cannot see the earlier chat and asks for the goal in one line (or asks the user to paste a few lines) | The bot pretends to remember, invents earlier context, or asks a form's worth of questions |

## Conversations
1. **Return the next day (R1).**
   Setup: Fake software seller Cedar Office Tools (fake). A continuity summary exists from Monday: goal is to pick a plan for a 12-person office; budget is $400 per month; no annual contracts; down to Plan B versus Plan C; still to decide which matters more, price or storage.
   User (Tuesday, new session): "Let's pick up the plan decision."
   Expect: The first bot reply shows the summary and asks whether to continue, before any question. "Which plans are you comparing?" as a first reply fails.

2. **Specific summary (R2).**
   Setup: Same summary as conversation 1.
   User: "ok where were we"
   Expect: The summary includes the goal, the $400 budget, the no-annual-contract rule, Plan B versus Plan C, and what is open. A vague summary, or one that adds a fact the user never gave (a plan price, a deadline), fails.

3. **Start fresh (R3).**
   Setup: Same summary as conversation 1.
   User turn 1: "Let's pick up the plan decision."
   User turn 2 (after the offer): "start fresh"
   User turn 3: "I need a plan for a 4-person shop, annual is fine"
   Expect: After turn 2 the bot drops the summary in one step, and turn 3 gets no mention of the 12-person office, $400, or Plans B and C. The summary is not offered again in this session.

4. **Edit the summary (R3).**
   Setup: Same summary as conversation 1.
   User turn 1: "Let's pick up the plan decision."
   User turn 2 (after the offer): "edit: budget is $450 now, and annual contracts are ok"
   User turn 3: "so what's left"
   Expect: The bot uses $450 and the allowance for annual contracts, and not the original $400 and no-annual rule. A reply that restates the old budget fails.

5. **Ask before saving (R4).**
   Setup: Same summary as conversation 1. The user continued from it, and the work is still unfinished.
   User: "good, thats enough for today. keep this for next time"
   Expect: The bot shows the summary it would save and asks before saving it. Saying "saved" without showing or asking fails. Whether the summary was actually stored cannot be judged from the transcript alone.

6. **Delete the summary (R5).**
   Setup: Same summary as conversation 1.
   User turn 1 (Tuesday): "delete that summary, I don't want it kept"
   User turn 2 (Wednesday, new session): "hi, I need help picking a plan"
   Expect: Turn 1 confirms the deletion. In the Wednesday session the bot starts blank, asks for the goal in the normal way, and does not mention Plan B, Plan C, or $400. A mention fails. Whether the stored data is gone cannot be judged from the transcript alone.

7. **Source of the summary (R6).**
   Setup: Same summary as conversation 1, saved on Monday.
   User: "let's continue the plan thing"
   Expect: The offer says where the summary came from ("From your chat on Monday"). "I remember we were looking at plans" fails.

8. **End of a long session (R7).**
   Setup: A session on an unfinished task that the product counts as long. Record the product's own definition of "long" in your results; this file sets none. The task is a fake office move for Harbor Realty (fake): two vendor quotes collected, move date not set.
   User: "ok i have to go, thanks"
   Expect: The bot offers a short summary of the task to save (goal, decided, open), with a choice to save it. A plain "Goodbye" fails.

9. **Nothing available (R8).**
   Setup: Fake software seller Cedar Office Tools. No earlier chat or summary exists for this user.
   User: "continue what we were doing yesterday"
   Expect: Says it cannot see the earlier chat and asks the user to give the goal in one line or paste a few lines. Inventing yesterday's task fails.

10. **Do nothing special: a new, unrelated topic (R1).**
    Setup: Same summary as conversation 1 exists.
    User: "what's a good name for a golden retriever puppy"
    Expect: A normal answer. No summary is pushed and the plan decision is not mentioned.

11. **Do nothing special: no re-ask after approval (R1).**
    Setup: Same summary as conversation 1.
    User turn 1: "Let's pick up the plan decision."
    User turn 2 (after the offer): "yes continue"
    User turn 3: "how many seats are we talking again"
    Expect: The bot continues from the summary and answers from it (12 people) or moves the task forward. It does not ask for the budget, headcount, or contract rule again, and it does not offer the summary a second time.

12. **Do nothing special: first-ever chat (R8).**
    Setup: Fake software seller Cedar Office Tools. A brand-new user with no history.
    User: "hi, I need help picking a plan for my office"
    Expect: A normal opening that asks about the office. It does not say "I can't see your earlier chat", because the user did not refer to one, and it does not offer a summary.

## Cannot be judged from a transcript alone
- **Whether the summary is saved or deleted (R4, R5).** The transcript shows what the bot says, not what the store holds. Check the memory store or settings page after the run.
- **One-click Start fresh (R3).** Click count is a property of the interface. A transcript shows only that the option exists and works.
- **"Same place as other memory controls" (R5).** This is a product layout check.
- **Long session (R7).** The pattern page gives no length. Record the product's own definition of a long session.
- **Incognito or paused memory.** The pattern page's guardrails say these should suppress the offer. They depend on product settings, so they are not part of this chat file; test them in the product.
- **Production rates.** These tests do not measure resume success or re-explanation rate in real traffic. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
