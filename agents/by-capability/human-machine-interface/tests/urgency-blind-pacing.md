# Test File: Urgency-Blind Pacing

This file is a set of chat test conversations for people who build or review support chat assistants and want to check whether theirs moves straight to an action or a person when a message cannot wait, such as a stolen card, an account takeover, an outage, or a payment due today.

**Pattern:** [Chatbot Treats a Fraud Alert Like a Casual Question: Urgency-Blind Pacing](../goals/response-time/failures/urgency-blind-pacing.md)
**Pattern ID:** urgency-blind-pacing
**Goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent.
**Primary metric:** Time to action or human for urgent intents. Starting target on the pattern page: under 2 min (a starting point to tune, not a measured benchmark).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, orders, accounts, and people below are invented and labeled fake. Text chat only. Some items need the product's urgent-intent list, the handoff record, or a timer, and are marked "Needs a person". The wait times in the setups are made-up test values, not figures from the pattern page. The bot should never state a legal or liability figure to a user, in any test.

The fake products used throughout: "Harbor Credit Union (fake)" chat, for a member named Dana Whitfield (fake), debit card ending 4417 (fake). The bot has a card-freeze tool and a fraud team queue. Where a test says so, the setup changes (no tool, no staff, slow tool). "Ledgerline (fake)" is an invoicing app for small businesses with a status page and an on-call incident desk, used for the outage test.

The urgent list for the tests (the product's written list, per rule 1): card fraud, lost or stolen card, account takeover, outage, payment due today. Anything else is not urgent.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a written urgent list | The product has a written list of urgent intents with an action or queue for each; an intent not on the list gets the normal flow. Needs a person to read the list | No written list, an intent with no action or queue, or a non-listed intent treated as urgent |
| R2 | 2. Classify on the first user turn | Turn 1 is read for wording and context ("charges I didn't make", "due today", "down since 9") and an urgent intent is recognized on that turn, not after follow-up questions | Urgent wording in turn 1 gets a normal flow, or recognition only after the user repeats it |
| R3 | 3. Lead with the action or the route | The first reply to an urgent intent offers the fast action or a person, with no greeting menu, no feature list, and no unrelated question | A greeting, menu, feature list, or unrelated question comes first |
| R4 | 4. Ask only what the action needs | At most one question, and only if the action cannot start without it. Required identity checks stay | Two or more questions, a question the action does not need, or a required identity check skipped |
| R5 | 5. State the wait for a person, or say there is none | The reply gives the wait or callback time. If no one is staffed, it says so and gives the fastest alternative | A person is offered with no wait stated, or "no one is available" with no alternative |
| R6 | 6. Say what the action did and did not do | After the action the reply says what changed and what did not ("The card is frozen. Earlier charges are not undone.") | Silence about limits, or wording that implies the action fixed more than it did |
| R7 | 7. Hand off with the urgency flag and the context | The handoff record holds the intent, `urgency=high`, what was done, and what the user said. Needs the handoff record | A handoff with no flag, no action taken, or no summary, so the user must repeat |
| R8 | 8. Drop the slow extras | On an urgent intent there is no upsell, survey, or long disclaimer before the action | An upsell, survey, or long disclaimer before the action |
| R9 | 9. If the action takes longer than expected, say so | A status message appears while the action runs. Needs a person or a timer | A silent wait while the tool runs |
| R10 | Don't over-correct: not every angry or capitalized message is urgent; no action without the user's choice or required checks | A capitalized or angry message with no listed intent is answered normally with no urgent flag; a look-alike question gets a normal answer; no card is frozen before the user chooses and any required check passes | An urgent flag on a non-urgent message, or a freeze run without the user's choice or required checks |
| R11 | Hand-off rule | A person is offered at once when the bot has no safe action, when an action fails, or when the user asks for a person | A menu or question first in those cases, or a repeated loop with no person |

## Conversations
1. **The urgent list exists and is complete (R1).**
   Setup: Open the product's urgent-intent configuration. Needs a person.
   User: (none)
   Expect: Each listed intent (card fraud, lost or stolen card, account takeover, outage, payment due today) has a first-reply action or a queue named. A listed intent with neither fails.

2. **Not on the list: a plain request (R1).**
   Setup: Harbor Credit Union (fake) chat. Do nothing special applies: this is a normal request.
   User: "can i order new checks"
   Expect: The normal flow, with no urgent wording, no urgent flag, and no fraud-team offer. An urgent fast path fails.

3. **Plain fraud report in turn 1 (R2).**
   Setup: Dana Whitfield (fake) is signed in. Card ending 4417 (fake).
   User: "Someone is using my debit card. I just got 3 texts for charges I didnt make."
   Expect: The bot recognizes card fraud on this first turn, with no "what would you like to do today" step first. A normal flow, or recognition only after a second user message, fails.

4. **Vague wording, same intent (R2).**
   Setup: Same as 3.
   User: "weird charges on my card, i didnt make them"
   Expect: Treated as card fraud on turn 1, same fast path as test 3. A reply asking "what can I help with" fails.

5. **Payment due today (R2).**
   Setup: Dana (fake) has a loan payment due today and the bot can show the fastest payment route.
   User: "my car payment is due today and the app keeps erroring"
   Expect: Recognized on turn 1 as payment due today. The first reply shows the fastest payment route, or a person from billing if the route fails. A reply that asks for account type first fails.

6. **Outage from a business user (R2).**
   Setup: Ledgerline (fake) chat. The status page link and an incident desk exist.
   User: "invoices wont send, everything is down for us since 9 this morning"
   Expect: Recognized on turn 1 as an outage. The first reply gives the status page link and a report path or the incident desk. A greeting menu, or "have you tried clearing your cache", fails.

7. **First reply has no menu or greeting (R3).**
   Setup: Harbor Credit Union (fake). The bot has a freeze tool.
   User: "lost my wallet cant find my card"
   Expect: The first reply offers to freeze the card ending 4417 or to connect a person. It has no "Hi, I'm Penny" greeting, no list of services, and no question about account type. Any of those first fails.

8. **One question, only if the action needs it (R4).**
   Setup: Harbor Credit Union (fake). The bot can lock the account and reset access. Dana is not signed in, and the lock needs one identity step.
   User: "someone changed my password and i cant get in"
   Expect: At most one question, the identity step the lock needs. A list of questions (type of account, when it happened, which device) fails. A lock with the identity step skipped also fails.

9. **State the wait for a person (R5).**
   Setup: The fraud team queue shows a test wait of 3 minutes.
   User: "someone is using my card right now"
   Expect: The first reply offers the freeze and the fraud team, with the wait stated ("about 3 minutes"). A person offered with no wait fails.

10. **Nobody staffed (R5).**
    Setup: The fraud team is closed. The bot has no freeze tool in this test.
    User: "my card was stolen last night, theres charges"
    Expect: The bot says no one is available now and gives the fastest alternative that exists in the setup (for example the card-issuer phone line for lost cards, with the hours it answers). "A person will be with you shortly", or no alternative, fails.

11. **After the freeze, say what it did and did not do (R6).**
    Setup: The bot offered the freeze. The user picks it. The freeze succeeds.
    User: "Freeze the card now"
    Expect: The reply says the card ending 4417 is frozen and that earlier charges are not undone. "All fixed" or "You're protected", or any reply that does not mention earlier charges, fails.

12. **Handoff carries the flag and context (R7).**
    Setup: The user asks for the fraud team after the freeze in test 11. Needs a person to read the handoff record.
    User: "ok connect me to the fraud team"
    Expect: The handoff record holds the intent (card fraud), `urgency=high`, card last 4 (4417), the freeze done, and the user's words. The person's first message does not ask the user to start over. A record missing any of these fails.

13. **No slow extras before the action (R8).**
    Setup: The bot normally adds a rewards offer and a satisfaction survey at the end of chats. The user reports a stolen card.
    User: "my card got stolen at the gas station"
    Expect: No rewards offer, survey, or long disclaimer before the freeze or person is offered. Any extra before the action fails.

14. **Slow freeze tool (R9).**
    Setup: The freeze tool takes about 20 seconds in this test. Needs a person or a timer.
    User: "Freeze the card now"
    Expect: A status message such as "Working on the freeze, one moment" appears while the tool runs. A blank wait of 20 seconds with no message fails.

15. **Do nothing special: capital letters, not urgent (R10).**
    Setup: Harbor Credit Union (fake). Do nothing special applies.
    User: "WHAT ARE YOUR HOURS ON SATURDAY"
    Expect: A normal answer about Saturday hours. No urgent flag, no freeze offer, no fraud-team offer. An urgent flag fails.

16. **Do nothing special: look-alike question (R10).**
    Setup: Same. Do nothing special applies.
    User: "how does card fraud protection work?"
    Expect: A normal explanation of how fraud protection works. No urgent flag, no freeze offer. Treating it as a live fraud report fails.

17. **No freeze before the user chooses and the check passes (R10).**
    Setup: Policy requires one identity step before a freeze. The user has not yet chosen.
    User: "somebody is using my card"
    Expect: The bot offers the freeze and the fraud team and waits for the user's choice. After "freeze it", it asks the one required identity step before freezing. A freeze on the first message, or a freeze with the identity step skipped, fails.

18. **No safe action: go to a person at once (R11).**
    Setup: The bot has no lock tool for account takeover in this test. The security team is staffed with a test wait of 4 minutes.
    User: "my account got hacked, they emptied it"
    Expect: The first reply connects the user to the security team with the wait stated and the flag passed on. A menu, a help article, or a question first fails.

19. **Action fails: go to a person (R11).**
    Setup: The user chose the freeze. The freeze tool returns an error.
    User: "Freeze the card now"
    Expect: The bot says the freeze did not go through and offers the fraud team at once, with the wait. Another try with no person offered, or "something went wrong, try again later", fails.

20. **User asks for a person during an urgent case (R11).**
    Setup: The user has just reported fraud. The fraud team is staffed.
    User: "no i want to talk to someone"
    Expect: The person is connected or queued at once with context passed on. A menu or another question first fails.

## Cannot be judged from a transcript alone
- **The urgent list (R1).** Needs a person reading the product's configuration. A transcript shows only whether one message was treated as urgent.
- **Handoff contents (R7).** Need the handoff record: intent, urgency flag, action taken, user summary.
- **Status message timing (R9).** Needs a person or a timer. The pattern page sets no fixed delay before a status message; record the product's own.
- **Time to action or human.** These tests do not measure the primary metric. Use the metrics on the pattern page.
- **Wait times in the setups.** They are invented test values and are not benchmarks.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
