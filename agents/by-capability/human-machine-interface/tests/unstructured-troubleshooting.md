# Test File: Chatbot Troubleshooting Gives Five Fixes at Once (Unstructured Troubleshooting)

This file is a set of chat test conversations for people who build or review support bots and want to check whether theirs asks for one change at a time and reads the result before choosing the next step.

**Pattern:** [Chatbot Troubleshooting Gives Five Fixes at Once: Unstructured Troubleshooting](../goals/conversation-frameworks/failures/unstructured-troubleshooting.md)
**Pattern ID:** unstructured-troubleshooting
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Repeated-step rate: steps the bot asks for that the user already tried in the same chat. Starting point on the pattern page: under 5% (tune on your own data). Reported with steps to resolution.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses and people below are invented and labeled fake. Text chat only. The pattern page says the troubleshooting methods behind it come from human practice (IT support training, site reliability engineering) and are untested on chatbots, so these tests check behavior against the page's rules and say nothing about whether one change at a time shortens chats. A change alters a device or setting; looking at a light or reading a number is a check and may go with the change. Each setup lists the steps the fake bot may use.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. One change per reply | At most one narrowing question or one change in the reply, not both | Two or more changes in one reply |
| R2 | 2. Say what result to report | The step ends with the specific thing to look at and tell the bot | "Do that and let me know" with nothing named |
| R3 | 3. No second change until the first is reported | No new change and no later steps listed "for reference" while the last result is pending | A second change, or a preview of later steps, before the result |
| R4 | 4. Keep a step log | Steps the user says they did are not asked for again, unless the log shows a step was done wrong, and then the reply says what was wrong | A logged step requested again with no reason |
| R5 | 5. Choose the next step from the result | The next step follows from what was reported: persists, pick the next likely cause; changed, say how and follow it | The next step ignores the result |
| R6 | 6. Verify before closing | On "it works", asks the user to confirm the original symptom is gone and check one related function | Closes on "glad it's fixed" |
| R7 | 7. Undo what did not help | After a changed setting fails, says how to restore the old setting before moving on | Moves to the next step with the setting still changed |
| R8 | 8. Warn before a step that loses data | Names what is lost and offers a backup first | Asks for the step without a warning |
| R9 | 9. Hand off when steps run out | After three changes with no progress, or on request for a person, offers a person and passes the step log | A fourth change, or a hand-off with no log |
| R10 | Don't over-correct | Obvious cause: one step that fixes it. Steps the user already tried are logged, not redone. A request for everything gets a short ordered list run one step at a time | A quiz where the cause is plain, steps redone, or the whole list handed over to run at once |

## Conversations
1. **Opening report (R1).**
   Setup: Fake provider Maple Ridge Internet (fake). The bot can suggest: restart the router, change the Wi-Fi channel, reset network settings, update the router firmware, move the router away from the microwave.
   User: "My Wi-Fi keeps dropping around 8 pm."
   Expect: One narrowing question (every device or just one) or one change. A numbered list of two or more changes fails.

2. **Name what to report (R2).**
   Setup: Same provider. The user has said every device drops. The bot picks the router restart.
   User: "every device"
   Expect: One restart step, with what to look at (the light) and what to report (whether it turns solid and whether the drop comes back tonight). "Restart it and let me know" fails.

3. **Wait for the result (R3).**
   Setup: Same provider. The user restarted the router. The result still pending is whether the drop returns at 8 pm.
   User: "restarted it. light came back solid"
   Expect: Acknowledges the light, asks the user to report on tonight's drop, and gives no new change or preview of later steps. A channel change in the same reply fails.

4. **User did several steps from a list (R4).**
   Setup: Same provider. An earlier bot reply listed five fixes.
   User: "did 1, 2 and 4. still drops"
   Expect: Logs all three and asks for none of them again. One new change from the remaining steps is fine. Asking for the restart, channel change, or firmware update fails.

5. **A step was done wrong (R4).**
   Setup: Same provider. The log shows a router restart the user said lasted about two seconds. The page's restart step is to unplug for 30 seconds.
   User: "still drops after the restart"
   Expect: If the bot asks for the restart again, it says why: the first unplug was too short. Asking again with no reason fails.

6. **Follow the blinking light (R5).**
   Setup: Same provider. The step log holds one restart. The bot asked what the light does.
   User: "the light keeps blinking and never goes solid"
   Expect: One new change different from the restart, tied to the blinking light. Asking for the restart again or an unrelated step fails.

7. **The problem changed (R5).**
   Setup: Same provider. The restart is logged.
   User: "after the restart it only drops on my laptop now, phone is fine"
   Expect: Says the picture changed and gives one step aimed at the laptop. Continuing with router steps as if nothing changed fails.

8. **"It works now" (R6).**
   Setup: Same provider. The restart is logged.
   User: "ok it works now!"
   Expect: Asks the user to confirm the original problem is gone, for example no drop by 8 pm, and to check one related function, then closes. "Glad it's fixed!" with nothing else fails.

9. **Restore a setting that did not help (R7).**
   Setup: Same provider. The bot had the user change the Wi-Fi channel from Auto to a fixed channel. The log holds that change.
   User: "changed it, still drops"
   Expect: Says how to put the channel back to Auto before the next step. A new step with the channel still changed fails.

10. **Factory reset warning (R8).**
    Setup: Same provider. The next step is a factory reset of the router, which erases its saved settings. The router can export a settings file.
    User: "ok what's next"
    Expect: Names what the reset erases and offers the settings backup first. Asking for the reset with no warning fails.

11. **Three changes, no progress (R9).**
    Setup: Same provider. The log holds three changes (restart, channel change, firmware update), none of which helped.
    User: "still dropping"
    Expect: Offers a person and says it will pass the step log so the user does not repeat steps. A fourth change fails.

12. **User asks for a person (R9).**
    Setup: Same provider. The log holds one change.
    User: "can i just talk to someone"
    Expect: Hands off with the problem, the step tried, and its result. Arguing for one more step first fails.

13. **Control: user already tried the basics (R10).**
    Setup: Same provider.
    User: "wifi drops every night. already restarted the router and did a factory reset yesterday, still drops"
    Expect: Logs both, asks for neither again, and asks one narrowing question or gives one new change. Asking for a restart again fails.

14. **Control: the cause is plain (R10).**
    Setup: Same provider. The user's first message states the cause.
    User: "internet went out right after i vacuumed. the router power cord is on the floor, pulled out of the wall"
    Expect: One step: plug it back in, and say what to look at. A series of narrowing questions fails.

15. **Control: user asks for everything to try (R10).**
    Setup: Same provider. The five suggestions from conversation 1 are the full list.
    User: "just give me everything to try"
    Expect: May give a short ordered list of those steps, but asks for only the first and waits for the result. Telling the user to do all five and report back fails.

## Notes
- Conversation 5 rests on my reading of rule 4's exception ("unless the log shows it was done wrong"). The page does not say the bot must redo the step, only that it may with a reason.
- Conversation 15 treats the five suggestions as a "short" list because the setup lists five. The page does not define short.
- Conversation 1 counts a narrowing question as one allowed item per the reference design, and does not allow it alongside a change.

## Cannot be judged from a transcript alone
- **The step log (R4).** A transcript shows whether a step was asked for again, not whether the log recorded it.
- **Repeated-step rate in real traffic.** It needs production chats with step names. These tests do not measure it.
- **Whether one change at a time helps.** The page found no chatbot study and no numbers. These tests check behavior, not chat length.
- **Parsing messages like "did 1, 2 and 4".** The page notes this will miss some cases. A run on varied wording is needed.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
