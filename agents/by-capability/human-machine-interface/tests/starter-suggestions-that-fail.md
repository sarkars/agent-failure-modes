# Test File: Starter Suggestions That Fail

This file is a set of chat test conversations for people who build or review chat assistants with starter chips or suggested questions and want to check whether every chip they show actually works.

**Pattern:** [Chatbot Suggested Questions That Give Bad Answers: Starter Suggestions That Fail](../goals/onboarding-and-discoverability/failures/starter-suggestions-that-fail.md)
**Pattern ID:** starter-suggestions-that-fail
**Goal:** People know what the assistant can do and how to start, without needing to guess or to engineer prompts.
**Primary metric:** Suggestion success rate: replies rated resolved. Starting target on the pattern page: 100% for shown chips.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, orders, articles, and people below are invented and labeled fake. Text chat only. Each setup states the chip registry, the test status, and the user state, because the point is which chips are shown and how the tapped chip is answered. Items marked "Needs a person" need the registry, the logs, or the interface.

The fake product used throughout: "Northfield Shop (fake)". Chips: "Track my order" (needs a logged-in user), "Return policy", "Gift card balance".

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Give every chip a test case | Each chip has its exact payload, the user state it is shown in, and the facts or action a resolved reply must contain. Needs a person with the registry | A chip with no stored payload, state, or resolved-if list |
| R2 | 2. Gate display on a pass | A chip is shown only if its test was rated resolved after the latest change to the model, prompt, knowledge base, or tools; a rewording needs a new pass; the tapped chip's reply meets its resolved-if list | A chip shown without a pass since the last change, a reworded chip shown on the old pass, or a tapped chip answered with a weak or made-up reply |
| R3 | 3. Re-run on every change and on a schedule | All chip tests run on each deploy and content publish, and nightly as a starting point. Needs a person or harness with the run log | A change with no re-run, or no scheduled run |
| R4 | 4. Pull failing chips automatically | A failed test hides the chip until it passes again, with no manual step | A failing chip still shown until a person notices |
| R5 | 5. Show a chip only where it can succeed | A chip that needs an account, order, or tool is shown only in the state its test covered | An order chip shown to a logged-out user |
| R6 | 6. Check generated suggestions before display | A model-written follow-up is shown only if retrieval returns a supporting source or a tool can do it | An unsupported follow-up shown, or a supported one dropped |
| R7 | 7. Show 2-4 chips plus "Something else", text box open | 2-4 passing chips plus "Something else", free text active; padding with untested chips is never used | More than 4, a chip row with no "Something else", a disabled text box, untested chips added to reach 2, or the user's typed question answered with only chips |
| R8 | 8. Watch chips live | Each chip's live success is tracked from ratings and sampled review; a chip whose live conversations fail is pulled and re-tested. Needs a person with the logs | No live tracking, or a failing chip left up |
| R9 | Don't over-correct: no empty box, no only-safe chips, no stopping the watch | Pulling every chip leaves a scope line and the text box, not a blank box; chips come from real common requests; checks continue after a pass | A blank box after all chips are pulled, only trivial chips such as "What are your hours?", or no checks after the first pass |
| R10 | Hand-off rule | After a fallback reply twice, or the user rephrasing the chip's question twice, the bot offers a person and passes the chip ID and transcript | Keeps retrying the chip's flow, or offers a person without the chip ID and transcript |

## Conversations
1. **Chip registry entries complete (R1).**
   Setup: Registry has 3 chips (fake). "Track my order" has payload "Track my order", state logged in, resolved-if "carrier and expected delivery date from the order record". "Return policy" has a payload and state but no resolved-if list.
   Expect: Needs a person with the registry. "Return policy" fails R1 until a resolved-if list is added.

2. **Shown chip answers as promised (R2).**
   Setup: "Track my order" passed after the last change. User is logged in with fake order #10001 shipped, carrier "FakeShip", due Friday.
   User: (taps "Track my order")
   Expect: Reply states FakeShip and Friday, and offers a tracking link (fake). A generic "I can help with orders" fails.

3. **Chip reworded (R2).**
   Setup: "Gift card balance" is changed to "Check a gift card". The new text has no test result.
   User: (opens the widget)
   Expect: The new chip is hidden until its own test passes. The reworded chip shown on the old pass fails.

4. **Chip passed before a prompt change (R2).**
   Setup: "Return policy" last passed at 10:00. The prompt changed at 14:00. No re-run yet.
   User: (opens the widget)
   Expect: "Return policy" is hidden until it passes again. A shown chip with a pass older than the change fails.

5. **Article unpublished, nightly run (R3, R4).**
   Setup: The help article behind "Return policy" (fake) is unpublished at 5:00 p.m. The nightly run is at 3:00 a.m. Needs a person or harness (run log).
   Expect: At the next run the chip fails and is hidden with no manual step. Still shown the next morning fails.

6. **Re-run on deploy (R3).**
   Setup: A deploy changes the model version. Needs a person (run log).
   Expect: A run of all chip tests starts on that deploy. A change with no run fails.

7. **Failing chip pulled without a person (R4).**
   Setup: "Gift card balance" fails its test because the tool is disconnected (fake).
   User: (opens the widget)
   Expect: The chip is not shown; "Track my order" and "Return policy" are. A failing chip still shown fails.

8. **Logged-out user (R5).**
   Setup: User is logged out. "Track my order" requires login.
   User: (opens the widget)
   Expect: No order chip. "Return policy" and "Something else" are shown. "Track my order" shown to a logged-out user fails.

9. **Model-written follow-up with no source (R6).**
   Setup: After an answer about returns, the model proposes "Want me to waive your restocking fee?" Retrieval returns no source and no tool exists.
   User: (reads the suggestions)
   Expect: That suggestion is not displayed. Displaying it fails.

10. **Do nothing special: supported follow-up (R6).**
    Setup: The model proposes "See the return window" and retrieval returns the fake return policy article.
    User: (reads the suggestions)
    Expect: The follow-up is shown. Dropping a supported suggestion fails.

11. **Chip set shape (R7).**
    Setup: Three chips pass. Needs a person (interface check).
    User: (opens the widget)
    Expect: 3 chips plus "Something else", text box active. Five chips, no "Something else", or a disabled box fails.

12. **Only one chip passes (R7, R9).**
    Setup: Only "Return policy" passes.
    User: (opens the widget)
    Expect: "Return policy" plus "Something else", or a one-line scope statement. Padding with untested chips to reach 2 fails.

13. **All chips fail (R9).**
    Setup: Every chip fails its test.
    User: (opens the widget)
    Expect: A one-line scope statement and an active text box, not an empty box with "Ask me anything". A blank box with no hint fails.

14. **Live ratings fail after a content change (R8).**
    Setup: Sampled live conversations from "Return policy" are rated failed after a content change (fake data). Needs a person (ratings and logs).
    Expect: The chip is pulled and queued for re-test. A chip left up fails.

15. **Reply leads with the answer (R2).**
    Setup: "Return policy" passes; the fake policy is 30 days with receipt.
    User: (taps "Return policy")
    Expect: First line states 30 days with receipt. A greeting or a question first fails.

16. **Chip request the bot cannot finish live (R2).**
    Setup: "Track my order" passed earlier, but the carrier tool is down now (fake).
    User: (taps "Track my order")
    Expect: Says it cannot get tracking right now and gives a real route (the carrier page or a person). A made-up date fails.

17. **Fallback twice after a chip (R10).**
    Setup: The user tapped "Gift card balance". Two fallback replies have been sent. A person is available.
    User: "no i just want the balance"
    Expect: Offers a person and passes the chip ID and the transcript. A third retry fails.

18. **Rephrasing the chip twice (R10).**
    Setup: The user tapped "Track my order", then rephrased it twice ("where is my stuff", "order status??") and still has no answer.
    User: "ugh where IS it"
    Expect: Offers a person with the chip ID and transcript. Repeating the tracking flow fails.

19. **Do nothing special: user ignores the chips (R7).**
    Setup: Three chips shown.
    User: "can i return something i bought in august"
    Expect: Answers the return question from the policy. Answering with only the chips again fails.

20. **Do nothing special: passing chip left alone (R9).**
    Setup: "Return policy" passed this morning. No change has happened since. It is 9:00 a.m.
    User: (opens the widget)
    Expect: The chip is shown. Hiding a passing chip for no reason fails. Needs a person for the "never checking again" half (run log).

## Cannot be judged from a transcript alone
- **Registry, run log, and rating data (R1, R3, R8).** Need the registry, the logs, and the ratings.
- **Interface (R7).** Needs the interface.
- **Whether a reply is really resolved.** The setups state the facts a resolved reply must contain, so these tests check the report, not the product's data.
- **Production rates.** These tests do not measure suggestion success rate. Use the metrics on the pattern page. This file sets no thresholds beyond the starting target stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
