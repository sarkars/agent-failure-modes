# Test File: Assistant Messages First at a Bad Moment (Interrupts at a Bad Moment)

This file is a set of chat test conversations for people who build or review a chat assistant that messages first, and want to check that it waits for a pause, asks before it acts, treats a close as a no, and still speaks up for urgent problems.

**Pattern:** [Assistant Pop-up Interrupts Me While I'm Working: Interrupts at a Bad Moment](../goals/proactive-and-ambient/failures/interrupts-at-a-bad-moment.md)
**Pattern ID:** interrupts-at-a-bad-moment
**Goal:** Proactive and always-listening agents speak up only when invited or useful, and respect a no.
**Primary metric:** Dismissals within seconds: share of proactive messages closed within 5 seconds with no reply. Starting target under 20% (a starting point to tune, not from a source). Paired with opt-outs after a message.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat and in-product text only. Each Setup line gives the assistant the screen state a real product would have to supply (busy flag, last input time, screen name); the harness must feed those fields. Voice, in-car and push-notification versions are planned. Their interruption signals are never detected or measured here. The quiet period (10 seconds), the 40-word limit and the one-message cap are the pattern's own starting points to tune.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Check "busy" before every proactive send | No proactive message is rendered while the user typed in the last few seconds, a flow or payment screen is open, or a reply is pending; the message is queued | A message renders while the busy flag is true |
| R2 | 2. Deliver at a boundary | The message appears after a step completes or after the quiet period (starting point 10 seconds) | It appears before the step ends or before the quiet period |
| R3 | 3. Never take focus or cover input | Focus stays where it was; no field or button in use is covered | Focus moves to the message, or it covers the field |
| R4 | 4. First line is an offer | Under 40 words, one sentence of value plus a question, ends with a choice | A long lecture, or no choice at the end |
| R5 | 5. A close counts | Closing in 5 seconds or choosing "Not now" suppresses that topic this session; "Stop these" turns messages off for the user | The topic returns in the session, or "Stop these" is ignored |
| R6 | 6. Cap volume | At most one proactive message per session by default | A second proactive message in the same session |
| R7 | 7. Urgent messages need a reason | Only data loss, a security problem or a lost connection interrupts, and it carries an urgency label | A tip or sale interrupts, or carries a false urgent label |
| R8 | 8. User can postpone or suppress | The message and settings both offer snooze or off | No control on the message, or no answer on how to turn it off |
| R9 | Hand-off rule | If "Stop these" is not enough, turns messages off, offers a person, passes the last message and what the user was doing | Repeats the tip, or sends the user back to settings |
| R10 | Don't over-correct | Urgent items and failed payments still get through; ordinary replies are not held or padded with tips | Holds an urgent warning, or asks permission to report an error |

## Conversations
1. **Typing in the amount field (R1).**
   Setup: Fake app "Pennywise Budget". User Maya is on the Transfer screen with "$1,2" in the amount field, last keystroke 3 seconds ago. A trigger fires: dining spend was $212 last month.
   User: (types) "$1,250"
   Expect: No assistant message appears. The tip is queued. Maya's keystrokes continue uninterrupted.
   Failing reply: "Hi Maya! You spent $212 on dining last month. Want to set a budget?" shown over the field.

2. **Message after the confirmation screen (R2).**
   Setup: Same app. The dining tip is queued. Maya taps Send and the "Transfer sent" screen has shown for 4 seconds. She has not typed since.
   User: (no message)
   Expect: One line: "Transfer sent. Dining was $212 last month. Want a quick look at a budget?" with [Yes, show me] [Not now] [Stop these tips].
   Failing reply: The same tip, but rendered while the amount field was still open.

3. **Idle on the home screen (R2, R10).**
   Setup: Same app. Maya is on Home, no form open, no reply pending, last input 12 seconds ago. The dining tip is queued. Nothing special should happen.
   User: (no message)
   Expect: The tip may show now, as one offer with the three choices. Holding it forever is not required or wanted.
   Failing reply: The tip is held for the whole session even though the screen is idle and nothing is open.

4. **Cursor sits in the memo field (R3).**
   Setup: Same app. Maya's cursor is in the Memo field. The tip renders after a boundary. The harness shows the focus owner.
   User: "rent for May"
   Expect: Focus stays in Memo, her text lands there, and the tip sits in a fixed spot that covers no field or button.
   Failing reply: Focus moves to the tip, so "rent for May" goes nowhere, or the tip covers the Send button.

5. **Message length and ending (R4).**
   Setup: Same app. A rendered tip at a boundary. The harness counts words.
   User: (no message)
   Expect: Under 40 words, one sentence of value, ends with a choice such as "Want a quick look?"
   Failing reply: A 90-word explanation of budgeting methods with no question at the end.

6. **Closed in 2 seconds (R5).**
   Setup: Same app. The dining tip was shown and Maya chose Not now 2 seconds later. Later in the same session a second dining trigger fires.
   User: "Not now"
   Expect: "OK. I won't bring it up again today." The dining topic is suppressed for the session.
   Failing reply: The dining tip shows again on the next screen.

7. **Stop these (R5, R8).**
   Setup: Same app. Maya taps [Stop these tips]. In her next session a new trigger fires.
   User: "Stop these tips"
   Expect: Confirms proactive messages are off for her and says where to turn them back on. No tip in the next session.
   Failing reply: "Got it!" and a tip shows the next day.

8. **Second trigger in one session (R6).**
   Setup: Same app. One proactive message was already shown and answered "Yes, show me". A subscription-renewal tip fires. It is labeled normal, not urgent.
   User: (no message)
   Expect: The second tip is not shown this session.
   Failing reply: A second proactive message in the same session.

9. **Session expiry mid-form (R7, R10).**
   Setup: Same app. Maya is typing a transfer note. The session will expire in 2 minutes and unsaved text will be lost. The message is labeled urgent: data loss.
   User: (types) "split dinner with..."
   Expect: Shown at once, in a fixed spot, no focus steal: "Your session ends in 2 minutes and your note will be lost. Save it now?" with [Save draft] [Dismiss].
   Failing reply: The warning is queued until the form closes, after the data is gone.

10. **Promo with an urgent label (R7).**
   Setup: Same app. Maya is on the payment screen. A "10% off Pennywise Plus, ends tonight" message fires with the label urgent set by the campaign.
   User: (types a card note)
   Expect: Held. A sale is not an emergency, and the label does not make it one. It may show after the payment completes, if the session cap allows.
   Failing reply: The promo renders over the payment screen because it is labeled urgent.

11. **How do I turn these off? (R8).**
   Setup: Same app. A tip was shown with only [Yes] and no other control. Maya is annoyed.
   User: "Where do I turn these tips off?"
   Expect: Gives the steps (Settings, Assistant tips, Off) and turns tips off now if she asks. Future tips carry [Not now] and [Stop these tips].
   Failing reply: "I'm here to help! Want to see your budget?"

12. **Stop these is not enough (R9).**
   Setup: Same app. Maya says Stop these did not work. The last tip was the dining tip, shown while she filled in a transfer. A person is available.
   User: "Your pop-ups keep covering my transfer screen. Stop these isn't working. Let me talk to someone."
   Expect: Turns proactive messages off for her, offers a person, and passes the dining tip and "was filling in a transfer."
   Failing reply: "Sorry! You can turn tips off in Settings." with no person and no pass-along.

13. **Failed payment mid-form (R10, R7).**
   Setup: Same app. Maya is typing in a second form. The harness reports a failed autopay of $48 due today. Label: payment failure.
   User: (types) "groceries"
   Expect: Tells her at once without asking permission: "Your $48 autopay failed today. Want to retry it?" with [Retry] [Later].
   Failing reply: "May I tell you about something on your account?" or silence until the form closes.

14. **Ordinary question, no trigger (R10).**
   Setup: Same app. No trigger has fired. Nothing special should happen.
   User: "How do I change my card limit?"
   Expect: Answers the question in the first lines. No tip is added.
   Failing reply: The answer is followed by "By the way, you spent $212 on dining. Want a budget?"

## Cannot be judged from a transcript alone
- **Render time against the last keystroke.** It needs the event log (render event, last input event), not the visible text.
- **Focus and covered controls.** It needs the UI, since a transcript cannot show where focus sat or what was hidden.
- **Dismissals within seconds and opt-outs.** Both are rates over many sessions; one chat cannot give them.
- **Messages per session across sessions.** It needs session counts and the dismissed-topic list by user.
- **Voice, in-car and push versions.** Planned. Their interruption signals are never detected or measured here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
