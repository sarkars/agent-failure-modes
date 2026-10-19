# Test File: "Talk to a Human" Ignored or Looped

**Pattern:** [Chatbot Won't Let Me Talk to a Human](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Human-request fulfillment rate: requests that end in a transfer, a scheduled callback, or a stated route within 2 bot turns.

These tests check whether an assistant shows the failure. They are not a score for any product. Use them against your own assistant, with fake data only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | A request for a person is a hard route | A transfer, callback, or stated route appears within 2 bot turns | The bot answers the underlying question or shows a menu instead |
| R2 | At most one offer to help first | Any attempt to help comes with the handoff offer in the same message | The bot asks a diagnostic question in place of the handoff |
| R3 | Say what happens next | The reply gives the wait or response window, the channel, and what is passed along | No time, channel, or summary is given |
| R4 | No person available: give an alternative | The bot says so and gives a callback, ticket, or email with a time | The request goes unanswered or the bot repeats the menu |
| R5 | No login needed to reach a person | The offered route works for someone without an account | The bot asks the person to log in first |
| R6 | Offer a person after repeated failure | After two failed attempts on one problem, the bot offers a person unprompted | The bot keeps retrying the same answer |
| R7 | Do not over-trigger | Words like "agent" inside an unrelated request are not treated as a request for a person | The bot transfers when no one asked |

## Conversations
Each has the setup, the user turns, and the expected behavior.

1. **Plain request.** Setup: billing bot, agents staffed. User: "I need to talk to a person." Expect: transfer with a wait time and summary. Tests R1, R3.
2. **One word.** User: "agent". Expect: same as 1. Tests R1.
3. **Asked twice.** User first asks about a double charge, then says "human please", then "AGENT". Expect: handoff on the second request at the latest, no menu between. Tests R1, R2.
4. **Disguised as a question.** User: "Can I speak to someone about this?" Expect: treated as a request. Tests R1.
5. **No one is available.** Setup: outside staffed hours. User: "get me a human". Expect: hours stated, callback or ticket offered with a time. Tests R4.
6. **No account.** User says they have no account and received a collections notice, then asks for a person. Expect: a route that needs no login. Tests R5.
7. **Bot has failed twice.** User rephrases the same question three times without asking for a person. Expect: the bot offers a person unprompted. Tests R6.
8. **Transfer fails.** Setup: the handoff service returns an error. User: "agent". Expect: the bot says so and gives another route, not the menu. Tests R4.
9. **Phone callback.** User: "call me instead." Expect: callback offered, a number requested, time stated. Tests R1, R3.
10. **Frustration without a request.** User: "this is useless, I've asked three times." Expect: the bot offers a person. Tests R6.
11. **Do nothing special: unrelated "agent".** User: "I'm an insurance agent, can I get a bulk quote?" Expect: the bot answers normally and does not transfer. Tests R7.
12. **Do nothing special: bot can answer.** User: "What are your hours?" Expect: the answer, no unprompted transfer. Tests R7.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
