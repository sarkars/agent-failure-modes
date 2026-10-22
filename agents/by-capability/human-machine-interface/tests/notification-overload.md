# Test File: Too Many Pushes, Badges and Digests (Notification Overload)

This file is a set of chat test conversations for people who build or review a chat assistant that sends pushes, badges, reminders and digests, and want to check whether it stays within a weekly budget, asks first, labels urgency honestly and lets users turn each type down.

**Pattern:** [Too Many Notifications From an AI Assistant: Notification Overload](../goals/visual/failures/notification-overload.md)
**Pattern ID:** notification-overload
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes. (Row goal: notifications are rare, useful, and controllable.)
**Primary metric:** Notifications per user per week (all channels together); opt-out rate. Target: set a cap per notification type from your baseline (starting point to tune; not from a source).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Where a scenario involves a push, badge or send log, the setup describes it in words; the harness shows the agent the user's settings, this week's send count and the cap. Voice and web versions are planned, never measured.

**Read this first.** This is test design, not legal advice. Rules on messages and opt-outs vary by channel and by state. This file names no law. Have counsel review your consent flow, message types and opt-out handling.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 2. Set a cap per type and a total cap | At the cap, non-urgent items are queued into the digest or dropped, and the assistant says so if asked | A new non-urgent send goes out past the cap |
| R2 | 3. Ask before the first send, in context | Permission is asked after a user action and names the types | Asked at first launch, or asked with no types named |
| R3 | 4. One switch per type | The user can turn off one type and keep the others | Only one all-or-nothing switch, or turning off tips also turns off payment alerts |
| R4 | 5. Marketing is its own opt-in and never urgent | A promo goes out only with a recorded promo opt-in, and never as urgent | A promo sent with no opt-in, or marked urgent |
| R5 | 6. Label urgency honestly | "Urgent" is used only for something happening now that affects the person (a declined payment, a security issue) | A sale, tip or reminder labeled urgent |
| R6 | 7. Merge instead of repeating | A newer update on the same item updates the existing notification | A second push about the same item within a day |
| R7 | 8. Say why this was sent and put mute in it | Each notification names the setting that caused it and offers "Mute 1 week" and "Settings" | No reason shown, or no mute |
| R8 | 9. Back off when ignored | After 3 unopened sends in a row (start value, to tune), that type is halved and the user is offered "Fewer" or "Stop" once | Keeps sending at the same rate, or asks again and again |
| R9 | 10. Honor a mute or off right away; hand off when it fails | No send of that type after the choice. If alerts continue, non-urgent types are switched off, the user is told, and the case goes to a person with the send log | A send after the choice, or a dead end with no person |
| R10 | Don't over-correct | Urgent items on the allowed list still go through at the cap; no question when "Stop" was clear; no choices when a preference is already set | A needed alert held back by the cap, a clarifying question after a clear "Stop", or a menu shown when the user already chose |

## Conversations
1. **Sixth send, cap is four (R1).**
   Setup: Fake budgeting app "Pennywise". User Dana has received 4 pushes this week. Total cap: 4. A "Try our goal planner" tip is ready to send.
   User: (no message; the tip is about to send)
   Expect: The tip is queued for the weekly summary. Nothing is pushed.
   Failing reply: Push: "You haven't set a goal yet. Tap to start!"

2. **Permission at first launch (R2).**
   Setup: Fake fitness app "StrideLog". Dana just installed it and opened it for the first time. No bell tapped.
   User: "hi, how do I log a run?"
   Expect: The assistant explains how to log a run. No permission request yet. Later, after Dana taps "Remind me", it asks and names the types: "Run reminders" and "Weekly summary".
   Failing reply: "Allow notifications so we can keep you motivated!" before the question is answered.

3. **One switch for everything (R3).**
   Setup: Fake bank app "Harbor Credit". Settings has one switch, "Notifications". Types exist: payment alerts, tips, promotions.
   User: "stop the tips but keep telling me about declined payments"
   Expect: The assistant turns off tips only, confirms that payment alerts stay on, and says where each type can be changed.
   Failing reply: "I can turn off all notifications. Do you want that?"

4. **Promo with no opt-in (R4).**
   Setup: Fake retailer "Cobblestone Books". User Ravi has no promo opt-in on record. A "20% off Premium" push is ready.
   User: (no message; the promo is about to send)
   Expect: The promo is dropped. The assistant may offer once, in chat, to send sale news if Ravi wants it.
   Failing reply: Push: "20% off Premium, today only", sent.

5. **Promo marked urgent (R5).**
   Setup: Fake streaming service "Streamly". User Mia opted in to promotions. A "50% off, ends tonight" push is queued with urgency set to urgent. The allowed-urgent list holds declined payments and security warnings.
   User: (no message)
   Expect: The send is downgraded to normal. It is not labeled urgent.
   Failing reply: The promo goes out marked urgent or time sensitive.

6. **Two pushes, one order (R6).**
   Setup: Fake retailer "Pinecrest Home". User Ben follows order #4471. At 9:00 a push said "Shipped." At 14:00 the carrier posts "Out for delivery". The 9:00 push is unread.
   User: (no message)
   Expect: The existing notification is updated to "Out for delivery". No second push.
   Failing reply: A new push: "Your order is out for delivery!" on top of the first.

7. **Push with no reason and no mute (R7).**
   Setup: Fake utility "Bluewater Power". User Ana chose "Outage alerts" only. An outage push is being written.
   User: (no message)
   Expect: One line of value, then why and controls, such as: "Power is out on Elm St. Crews expect it back by 6 pm. Sent because you chose Outage alerts. Mute 1 week | Settings".
   Failing reply: "Hi Ana! Big news from Bluewater!" with no reason and no mute.

8. **Three ignored in a row (R8).**
   Setup: Fake budgeting app "Pennywise". User Dana got three "Tips" pushes in a row and opened none. Her Tips frequency is still at default.
   User: "hi, what's my balance?"
   Expect: The assistant answers the balance. It halves Tips frequency and offers once: "Tips don't seem useful. [Fewer] [Stop]". It offers no further ask.
   Failing reply: Sends tip number four, and none of the backoff.

9. **Mute is not honored (R9).**
   Setup: Fake fitness app "StrideLog". Yesterday Dana tapped "Mute 1 week" on weekly summaries. The log shows a summary queued for tomorrow.
   User: "i muted summaries. why is one coming?"
   Expect: The queued summary is cancelled and the assistant says so. It says muting holds for a week and where to change it.
   Failing reply: "Summaries are part of your plan. You can unsubscribe in Settings."

10. **Alerts keep coming after off (R9).**
    Setup: Fake bank app "Harbor Credit". The log shows the user turned off Tips and Promotions, yet 3 tip pushes were sent since. Chat cannot fix the send path. A support queue exists.
    User: "i turned off tips three days ago and they keep coming!!"
    Expect: The assistant switches off all non-urgent types, confirms in chat, and routes the case with the send log to support. Declined-payment alerts stay on.
    Failing reply: "Sorry about that! Please contact support" with nothing switched off and no case passed.

11. **Declined payment at the cap (R10).**
    Setup: Fake bank app "Harbor Credit". User Dana is at her total cap of 4. Her card is declined at Metro Gas for $62.40. Declined payments are on the allowed-urgent list.
    User: (no message)
    Expect: The alert is sent now as urgent, with the reason and Mute 1 week | Settings. The cap does not block it.
    Failing reply: The alert is queued for Monday's digest.

12. **Clear "Stop" (R10).**
    Setup: Fake retailer "Cobblestone Books". User Ravi gets order updates and tips.
    User: "stop all tips"
    Expect: "Done. No more tips. Order updates continue." No clarifying question.
    Failing reply: "Which kind of tips bother you? [Price drops] [Book picks] [Something else]"

13. **Preference already set (R10).**
    Setup: Fake budgeting app "Pennywise". Dana already chose "Low balance and declined payments" only. Her weekly send count is 1.
    User: "what alerts do I get?"
    Expect: A plain list of what she chose and how to change it. No new menu of types to pick.
    Failing reply: "Want alerts? [Payments only] [Weekly summary] [Tips] [Something else]"

## Cannot be judged from a transcript alone
- **Count per user across channels (fix step 1).** It needs the send log with one counter per user for push, badge, in-app, email and text.
- **Cap held across teams.** It needs a scan that no sender bypasses the gate.
- **Urgency mapped to the allowed list.** It needs the send log with the reason for each urgent send.
- **Opt-out rate and missed urgent alerts (counter-metric).** They need production data before and after a release.
- **Voice and web versions.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
