# Test File: Blank Box With No Hint What to Ask

This file is a set of chat test conversations for people who build or review chat assistants and want to check whether theirs opens with a scope line and a few starting points, or with an empty box.

**Pattern:** [Chatbot Empty State: Blank Box With No Hint What to Ask](../goals/onboarding-and-discoverability/failures/blank-box-no-hint-what-to-ask.md)
**Pattern ID:** blank-box-no-hint-what-to-ask
**Goal:** People know what the assistant can do and how to start, without needing to guess or to engineer prompts.
**Primary metric:** Share of first sessions with a first message or tap, paired with abandonment before the first message. Starting target on the pattern page: set from your own baseline, then track the lift (no source sets a number).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, pages, streets, and people below are invented and labeled fake. Text chat only. The setup in each conversation says what the opening screen is configured to show, because several rules are about the screen and not the reply. Items marked "Needs a person" must be checked in the interface, not from a transcript.

The fake product used throughout: "Northfield Utilities (fake)" with a chat widget. Tasks the bot finishes: check an outage at an address, explain a charge on a bill. Task it cannot finish: set up a plan change (a person does that).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Open with a scope line | One sentence that says it is an AI assistant and names 2-4 things it can do on this site or screen | No scope line, a line that does not say it is an AI, or more than 4 tasks named |
| R2 | 2. Show 2-4 starters plus "Something else" | 2-4 starters, each for a task the bot completes, plus "Something else" | A blank box, 1 starter, more than 4, a starter for a task the bot cannot finish, or no "Something else" |
| R3 | 3. Keep free text open | The input is never disabled; "Something else" focuses it. Needs a person for the interface | The input is disabled or the tap does not focus it |
| R4 | 4. Make the placeholder a real example | The placeholder is a concrete example such as "e.g. Is there an outage on Elm St?" | "Ask me anything", "How can I help you?", "Type a message", or an empty placeholder |
| R5 | 5. Match the page | On a page with a known topic, the first starter is that topic | The same starter order on every page, or a topic unrelated to the page first |
| R6 | 6. Answer "what can you do?" and "hi" with the scope line and starters | The reply repeats the scope line and the starters | Another open question ("How can I help you today?") or a long unprompted feature list |
| R7 | 7. Fit the opening in one view | Scope line and starters show without scrolling at the widget's default size. Needs a person for the interface | The user must scroll to see the starters or the input |
| R8 | Don't over-correct: no wall of starters, no pop-up on load, no menu lock, no task listed that the bot cannot finish | A clear first request is answered first; at most 4 starters; free text stays open; the scope line names only finishable tasks | Starters pushed in front of a clear request, 10 starters, the widget forced open on page load, or an unfinishable task in the scope line |
| R9 | Hand-off rule | A first message asking for a person connects them with the page and typed text passed along, and does not answer with the starters; a person-only top intent is named as such in the scope line | Starters in reply to a request for a person, or the page and typed text lost |

## Conversations
1. **Support page opening (R1, R2).**
   Setup: Widget opens on the Support page (fake). Needs a person (read the rendered opening).
   User: (opens the widget, types nothing)
   Expect: One scope line that says it is an AI and names 2-4 tasks, then 2-4 starters plus "Something else". "Ask me anything" alone fails.

2. **Scope line says it is an AI (R1).**
   Setup: Same widget, Help page (fake).
   User: (opens the widget)
   Expect: The scope line says the assistant is an AI and names tasks like "check outages" and "explain a charge". A scope line that only says "Welcome!" fails.

3. **"Something else" opens free text (R3).**
   Setup: Same opening. Needs a person (interface check).
   User: (taps "Something else")
   Expect: The input is focused and accepts typing. A disabled input or a reply that restarts the menu fails.

4. **Placeholder text (R4).**
   Setup: Same opening. Needs a person (inspect the input).
   User: (reads the placeholder)
   Expect: A concrete example such as "e.g. Is there an outage on Elm St?" (fake street). "Ask me anything", "How can I help you?" or "Type a message" fails.

5. **Billing page order (R5).**
   Setup: Widget opens on the /billing page (fake). Top intents: check an outage, explain a bill.
   User: (opens the widget)
   Expect: "Explain my bill" is the first starter. The same order as the Support page fails.

6. **Page with no known topic (R5, R2).**
   Setup: Widget opens on the home page (fake), no known topic.
   User: (opens the widget)
   Expect: Starters come from the top intents in general, 2-4 plus "Something else". A starter for a task the bot cannot finish fails.

7. **"what can you do?" as the first message (R6).**
   Setup: Empty chat, home page.
   User: "what can you do?"
   Expect: Repeats the scope line and the starters. "I can help with many things! What would you like to know?" fails.

8. **"hi" as the first message (R6).**
   Setup: Empty chat, home page.
   User: "hi"
   Expect: Greets once, then gives the scope line and starters. "How can I help you today?" alone fails.

9. **Small phone screen (R7).**
   Setup: Widget at default size on a 375px-wide phone screen. Needs a person (interface check).
   User: (opens the widget)
   Expect: The scope line, the starters, and the input are visible without scrolling. Starters hidden below the fold fail.

10. **Do nothing special: clear first request (R8).**
    Setup: Empty chat, home page, starters configured.
    User: "is there an outage on Elm St"
    Expect: The bot checks and answers the outage question (or asks for the one missing detail). The starter menu again before answering fails.

11. **Do nothing special: thanks after an answer (R8).**
    Setup: The bot has just answered an outage question.
    User: "ok thanks"
    Expect: A short close. Re-showing the starter menu or the scope line fails.

12. **Clear request that does not match the page (R5, R8).**
    Setup: Widget opens on /billing, first starter is "Explain my bill".
    User: "is the power out near 12 Elm St"
    Expect: The bot handles the outage request; the page-matched starter does not take over. Steering the user back to billing fails.

13. **Too many starters (R2, R8).**
    Setup: Ten intents rank in the top intents for the last 30 days (fake data).
    User: (opens the widget)
    Expect: At most 4 starters plus "Something else". Ten starters fail.

14. **Scope line names an unfinishable task (R1, R8).**
    Setup: Plan changes are done only by a person. The draft scope line reads: "I can check outages, explain bills, and change your plan."
    User: (opens the widget)
    Expect: The shipped scope line does not claim plan changes; it names the finishable tasks. Listing "change your plan" as something the bot does fails.

15. **Widget forced open on load (R8).**
    Setup: Page load. Needs a person (watch the page).
    User: (loads the home page and does nothing)
    Expect: The widget stays closed until the user opens it. A widget that pops open to show the opening fails.

16. **First message asks for a person (R9).**
    Setup: Empty chat on /billing, a person is available.
    User: "I want a real person"
    Expect: Connects a person and passes the page and any typed text along. Replying with the starter menu fails.

17. **Person-only top intent named in the scope line (R9, R1).**
    Setup: "Change my plan" is a top intent but only a person can do it.
    User: (opens the widget)
    Expect: The scope line says plan changes go to a person. Silence about it, with a starter that dead-ends, fails.

## Cannot be judged from a transcript alone
- **Free text and layout (R3, R7).** Need the interface.
- **Pop-up on load (R8).** Needs a person watching the page.
- **Whether starters match real top intents.** The setups state the intents. Checking them against 30 days of logs needs the logs.
- **Production rates.** These tests do not measure first-message rate or abandonment. Use the metrics on the pattern page. This file sets no thresholds beyond the starting target stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
