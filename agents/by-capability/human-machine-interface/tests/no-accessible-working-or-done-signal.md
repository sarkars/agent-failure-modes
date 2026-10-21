# Test File: No Accessible Working or Done Signal

This file is a set of chat test conversations for people who build or review web chat widgets, and want to check whether theirs tells a screen-reader user in text when the assistant is working, stuck, or done.

> **Read this first.** The pattern page found no controlled study of working or done signals for blind users of AI chat, so the rubric below is a design hypothesis, not a measured standard. The status cue comes from page markup, so each case gives a harness view of the status region, not only the bot's words. Spoken output needs a person with a screen reader. This file is design guidance only. It is not a conformance claim and not legal advice. Anything about WCAG needs review by your accessibility lead or counsel.

**Pattern:** [No Accessible Working or Done Signal](../goals/accessibility/failures/no-accessible-working-or-done-signal.md)
**Pattern ID:** no-accessible-working-or-done-signal
**Goal:** People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent.
**Primary metric:** Status announcements present in the accessibility tree. Target: 100% (a starting point to tune, from the pattern page).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds the persona prompt and what the harness shows. "Harness shows" means a log of status-region writes with timestamps, read from the accessibility tree.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. One status region in the page at load | Empty status region and log exist before the first send | Region created on the first send, or missing |
| R2 | 2. Write "working" within 1 second of send | A "working" status such as "Working on your request." within 1 second | Dots only, or the first status after the reply |
| R3 | 3. Hide the dots and spinner | Dots are `aria-hidden`; no `aria-live` on them | Dots exposed, or `aria-live` on the animation |
| R4 | 4. Announce a change in step, not every token | New status only on a step change, at most once per 15 seconds | A write per token, or "still working" every second |
| R5 | 5. Write "done" when the reply is complete | "Reply ready." stays until the next send | No done write, or it is cleared at once |
| R6 | 6. Say so when the wait is long or stuck | At 30 seconds with no progress: "This is taking longer than usual." plus one next step | Silence, or "Still working." with no next step |
| R7 | 7. Reply in a log region; do not move focus | Reply is appended to the log; focus stays in the message box | Focus jumps to the reply |
| R8 | 8. One meaning on screen and in text | Visible indicator and status text name the same state | They name different states |
| R9 | 9. Reserve assertive for a failed send | Alert only when the message was not sent; typed text kept | Alert for an ordinary wait, or a failed send with no alert |
| R10 | Hand-off rule: two stuck or failed waits | A person is offered with the conversation so far, by a route that works without sight | Another "try again", or a route that needs sight |
| R11 | Don't over-correct | No status for a sub-second reply; a user who asked to stay with the bot is not pushed to a person | Status spam, or a forced hand-off |

## Conversations
1. **Region exists at load (R1).**
   Setup: Fake bank "Pinecrest Bank" (fake) web chat. Harness shows the page markup before any message.
   User: (no message yet; the page has just loaded)
   Expect: An empty status region and an empty log region are already in the tree.
   Failing reply: Harness shows the status region first created after the first send.

2. **Working within 1 second (R2).**
   Setup: Same widget. The wire fee lookup takes 6 seconds. Fees in the fake fee schedule: $25 domestic, $45 international.
   User: "What is the fee for a wire transfer?"
   Expect: Status "Working on your request." at or before 1 second after send.
   Failing reply: Harness shows animated dots and zero status writes; the answer appears at 6 seconds.

3. **Dots hidden from assistive technology (R3).**
   Setup: Same widget. Harness shows the typing-dots element while the bot works.
   User: "Can I send a wire on Sunday?"
   Expect: The dots carry `aria-hidden="true"` and no `aria-live`. The status text says the same thing.
   Failing reply: Harness shows `aria-live="polite"` on the dots element.

4. **Step changes, not every token (R4).**
   Setup: Fake insurer "Harbor Mutual" (fake). A claim check takes 40 seconds with two real steps: "Checking your policy" and "Reviewing the claim."
   User: "Where is my claim for the water damage?"
   Expect: Status writes only at send and at each step change, no more than one per 15 seconds. Streamed words are not announced.
   Failing reply: Harness shows a status write for each streamed word, or "Still working." every second.

5. **Done stays, focus stays (R5, R7).**
   Setup: Same insurer widget. The reply finishes at 40 seconds. Fake claim is approved for $1,200.
   User: "Where is my claim for the water damage?"
   Expect: The reply is appended to the log. Status reads "Reply ready." and stays until the next send. Focus remains in the message box.
   Failing reply: Status cleared when the reply lands, or focus moved to the reply text.

6. **Stuck wait gets a next step (R6).**
   Setup: Fake utility "Brightline Power" (fake). The bill lookup shows no progress for 30 seconds.
   User: "Why did my bill go up $22?"
   Expect: Status "This is taking longer than usual." plus choices: "Keep waiting", "Try again", "Talk to a person", "Something else". Free text stays open.
   Failing reply: Status stays "Working on your request." at 45 seconds with no next step.

7. **Screen and text say the same thing (R8).**
   Setup: Fake retailer "Oakline Outfitters" (fake). Harness shows the visible indicator and the status text. The visible indicator reads "Checking order 4417" while the reply is still being built.
   User: "Where is order 4417?"
   Expect: Status text names the same state as the visible line, such as "Checking your order."
   Failing reply: Status text reads "Reply ready." while the visible indicator still says "Checking order 4417".

8. **Failed send (R9).**
   Setup: Fake pharmacy "Fernwood Rx" (fake). The network drops and the message is not sent.
   User: "What time do you close today?"
   Expect: An alert announces that the message was not sent. The typed text is still in the box.
   Failing reply: No announcement and the box is emptied. A second failing case: an alert fired for an ordinary 12-second wait.

9. **Two stuck waits (R10).**
   Setup: Fake carrier "Cascade Mobile" (fake). Two lookups in this conversation passed the stuck limit. The user has not asked to stay with the bot.
   User: "Is the $49 reactivation fee coming off? This is the second time it hangs."
   Expect: Offers a person, passes the conversation so far, and offers chat with a person or a phone callback, which work without sight.
   Failing reply: "Please try again." offered a third time.

10. **Do nothing special: fast reply, and a user who wants the bot (R11).**
    Setup: Fake pizzeria "Marlow's" (fake). The reply is ready in under 1 second. Earlier the user said, "I'd rather stay with you than call anyone."
    User: "read my order back"
    Expect: The reply arrives with no extra status chatter, and no push to a person.
    Failing reply: "Taking longer than usual. Would you like to talk to a person?" for a sub-second reply.

## Cannot be judged from a transcript alone
- **Spoken output.** A DOM write is not proof that a screen reader spoke it. A person must test it.
- **Screen reader and browser pairs (fix rule 10).** The pattern page asks for at least two pairs per release. A chat transcript cannot show that.
- **Status announcements present in the accessibility tree, at scale.** It needs scripted runs per release across every state.
- **Voice delivery.** This file is text only; voice is planned and not tested.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
