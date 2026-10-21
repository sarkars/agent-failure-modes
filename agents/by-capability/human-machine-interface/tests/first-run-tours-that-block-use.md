# Test File: First-Run Tours That Block Use

This file is a set of chat test conversations for people who build or review an in-product text assistant, and want to check whether a tour, tutorial or setup quiz stands in front of the user's first question.

**Pattern:** [First-Run Tours That Block Use](../goals/onboarding-and-discoverability/failures/first-run-tours-that-block-use.md)
**Pattern ID:** first-run-tours-that-block-use
**Goal:** People know what the assistant can do and how to start, without needing to guess or to engineer prompts.
**Primary metric:** Drop-off during the first-run flow: share of first sessions that end before the user's first message is answered. Starting target: no higher than a no-tour control group (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds what the harness shows the agent: first-run state, input state and stored tour history.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. The input box works on first open | Input is active; no tour, video, carousel or quiz disables or covers it | Input is disabled or hidden behind first-run content |
| R2 | 2. A message typed during first-run content is sent and answered | The content closes and the message gets an answer | The text is dropped, or the tour continues first |
| R3 | 3. One line of scope plus 2-4 starters, free text open | One scope line, 2-4 starters, "Something else", nothing more | A carousel, a long intro, or more than four starters |
| R4 | 4. Answer first, teach second | Answer first; at most one tip, after it, tied to the request | A tip before the answer, two tips, or an unrelated tip |
| R5 | 5. Any tour is opened by the user | A tour starts only from "Show me around" or a help request | A tour starts by itself on any visit |
| R6 | 6. An opened tour is short and closable | Few steps; Close on every step; closing returns to the chat with input intact | No Close on a step, or the typed text is lost on close |
| R7 | 7. A dismissed tour stays dismissed | Not shown again next visit; available on request | The tour returns after a dismissal |
| R8 | 8. Ask nothing before the first answer unless needed | No profile quiz; if the answer depends on one fact, one question tied to the request | A setup wizard or unrelated questions first |
| R9 | Hand-off rule: a request for a person | Goes straight to the hand-off path, no tour step first | Tour steps shown before the hand-off |
| R10 | Don't over-correct | A clear first question gets a plain answer; no tip when none fits; a tour is still offered when asked | A tip on every reply, a blank box with no hint, or a refusal to give a tour |

## Conversations
1. **First open, input active (R1).**
   Setup: Fake invoicing app "Ledgerly" (fake). A user opens the assistant for the first time. No history.
   User: (opens the chat)
   Expect: The input box is active from the first moment. No card, video or overlay blocks it.
   Failing reply: "Welcome to Ask Ledgerly! Card 1 of 6: Meet your AI assistant. [Next]" with the input disabled.

2. **Overlay covers the input (R1).**
   Setup: Same app. A guidance overlay is layered on the chat panel on first open.
   User: "can i just type here?"
   Expect: The overlay does not stop the message. The input takes it and the assistant answers.
   Failing reply: The message cannot be typed until the user clicks through to "Done".

3. **Typed text during first-run content (R2).**
   Setup: Same app. A welcome card is showing. The user types and sends.
   User: "how do I send a late payment reminder"
   Expect: The card closes. The question is sent and answered.
   Failing reply: "Card 3 of 6: Smart categories." The typed text is never sent.

4. **Tapped starter closes the intro (R2).**
   Setup: Same app, first open, starters showing.
   User: (taps "Find unpaid invoices")
   Expect: The intro closes and the assistant answers the request.
   Failing reply: "Great choice! First, let me show you around." Then the tour starts.

5. **Scope line and starters only (R3).**
   Setup: Same app, first open, no message yet.
   User: (opens the chat)
   Expect: One line of scope, 2-4 starters such as "Find unpaid invoices" and "Send a reminder", plus "Something else". Nothing else before the first question.
   Failing reply: A six-card feature carousel, or eight starter buttons and a video.

6. **Answer before the tip (R4).**
   Setup: Same app. The assistant has a tip about bulk reminders ("remind all overdue").
   User: "how do I send a late payment reminder"
   Expect: The answer comes first. At most one tip follows, about reminders.
   Failing reply: "Tip: you can also bulk-edit categories! Now, about your reminder." Tip first and off topic.

7. **Second visit, no tour asked for (R5).**
   Setup: Same app. A returning user, second visit. They never asked for a tour. The app just shipped an update.
   User: "show me invoices from last month"
   Expect: A normal answer. No tour starts, including for the update.
   Failing reply: "What's new in Ledgerly! Let's take a quick tour." The tour starts by itself.

8. **Tour closed on step 2 (R6).**
   Setup: Same app. The user tapped "Show me around" and is on step 2. They began typing a question in the box.
   User: (taps Close)
   Expect: Close was visible on step 2. The chat returns with the typed text still in the input.
   Failing reply: No Close on step 2, or the input comes back empty.

9. **Dismissed tour stays dismissed (R7).**
   Setup: Same app. The user closed the tour last session. Dismissal is stored.
   User: "what can you do for me today?"
   Expect: A plain scope answer in chat. The tour is not started; it is mentioned as available on request.
   Failing reply: "Welcome back! Let's start the tour again, step 1 of 6."

10. **Setup question before the answer (R8).**
    Setup: Same app. The user has two businesses linked, "Pine Street Bakery" (fake) and "Northgate Plumbing" (fake).
    User: "list my unpaid invoices"
    Expect: One clarifying question: which business. No wizard, no profile quiz.
    Failing reply: "First, tell us your industry, team size and goals." Three questions before any answer.

11. **Person requested on first open (R9).**
    Setup: Same app, first open. A welcome card is showing.
    User: "talk to a person"
    Expect: The hand-off starts at once. No tour step is shown first.
    Failing reply: "Before I connect you, here is step 2 of 6."

12. **Do nothing special: clear first question (R10).**
    Setup: Same app, first open. The question is clear and no feature tip fits it.
    User: "what's my total for invoice 1042"
    Expect: A plain answer with the amount from the data. No tip, no tour offer, no extra choices.
    Failing reply: "Tip: try voice mode! Also take our tour? Or choose: Reports, Settings, Help."

13. **Do nothing special: tour is asked for (R10).**
    Setup: Same app. The user asks for help getting started.
    User: "can you show me around"
    Expect: A short tour is offered and started, a few steps, with Close on each.
    Failing reply: "You don't need a tour. Just ask me anything."

## Cannot be judged from a transcript alone
- **Drop-off during the first-run flow.** It needs first-session logs and a no-tour control group. Thirteen conversations do not measure it.
- **Input state in the real client.** A transcript shows the text, not whether the box was disabled or covered. It needs a client run.
- **Auto-started tours.** It needs tour-start events with the trigger recorded.
- **Third-party guidance tools.** Event sharing between the tool and the chat client cannot be set up in a text scenario.
- **Voice and visual first-run flows.** Not covered; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
