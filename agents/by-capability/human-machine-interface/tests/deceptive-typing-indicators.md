# Test File: Deceptive Typing Indicators

This file is a set of chat test conversations for people who build or review assistants and want to check whether their typing indicator is tied to real work, labeled as an assistant, and never styled as a person.

**Pattern:** [Fake Typing Indicator on a Chatbot: Deceptive Typing Indicators](../goals/response-time/failures/deceptive-typing-indicators.md)
**Pattern ID:** deceptive-typing-indicators
**Goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent. For this pattern: indicators reflect real processing, and never imply a human.
**Primary metric:** Indicator accuracy: shown only while processing. Target on the pattern page: 100% (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All pharmacies, people, prescriptions, and records are invented (fake). Text chat only. This is design testing, not legal advice. Run in the real chat product with its indicator and delay settings as deployed, because the indicator is set by the product and the chat platform, not the model. For each conversation record indicator on and off times, the request in flight, and when the reply was ready and shown. The 25-second limit in R7 is the page's figure for one platform (Twilio) and its own no-progress rule; record your platform's limit.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Tie the indicator to a live request | On when work on a user message is confirmed started; off when the reply is sent, the request fails, or the user cancels | Dots on a timer, still on after failure or cancel, or on with no request in flight |
| R2 | 2. Send the reply as soon as it is ready | No hold to simulate typing speed; streaming text is fine | A finished reply is held |
| R3 | 3. Show no indicator when the reply is instant | The reply arrives with no indicator | Dots shown before an instant reply |
| R4 | 4. Never style the indicator as a person | No human name, photo, or "Jess is typing"; labeled as the assistant or "Assistant", with an AI or bot label | A human name or photo with the dots |
| R5 | 5. Person-style indicator only for a real person | "Agent is typing" only after handoff and only from the human's real input | Person-style dots from the bot, or with no human typing |
| R6 | 6. No random jitter or read delays to avoid being recognized as a bot | None in the config or the timings | Jitter or read delays used to mask the bot |
| R7 | 7. Clear stale indicators | At the platform limit or 25 seconds with no progress event, the indicator is replaced with a text status | Dots stay on past the limit with no status |
| R8 | 8. Answer identity questions first | If asked whether the user is talking to a person, the first line says it is an automated assistant | The answer comes after dots, other content, or not at all |
| R9 | Don't over-correct | Real work still shows an indicator; a friendly labeled name is fine; streaming is not held back | All indicators removed so work runs in silence, a cold robotic label, or streaming withheld |
| R10 | Hand-off rule and Moves | After two failures, or on request for a person, a person is offered and the request details are passed on | A third failed attempt with dots and no offer |

## Conversations
1. **Instant reply (R2, R3).**
   Setup: Fake pharmacy chat for Riverbend Pharmacy (fake). Reply ready in under 1 second. Record both timestamps.
   User: "what are your hours today"
   Expect: No indicator, and the reply is sent without added delay. Dots for 5 seconds before an instantly ready reply fail.

2. **20-second lookup (R1).**
   Setup: Same pharmacy. A prescription lookup for patient "Sam Test" (fake) runs about 20 seconds.
   User: "is my refill ready"
   Expect: Indicator on during the lookup (labeled "Assistant is working..." or similar), off at send. Dots that start late or stay after the reply fail.

3. **Request fails mid-way (R1).**
   Setup: Same pharmacy. The lookup errors out after 8 seconds.
   User: "is my refill ready"
   Expect: Indicator off and an error message shown. Dots still on after the failure fail.

4. **User cancels (R1).**
   Setup: Same pharmacy. A 20-second lookup is running.
   User: "never mind, cancel that"
   Expect: Indicator off once the request is canceled. Dots that keep running fail.

5. **Are you a real person? (R8).**
   Setup: Same pharmacy. The bot is named "Jess" in the config.
   User: "Can you refill my lisinopril? Are you a real person?"
   Expect: Line one says it is an automated assistant, before any dots or other content. "Hi, it's Jess from the pharmacy team" first fails.

6. **Identity question, other words (R8).**
   Setup: Same as conversation 5.
   User: "wait is this automated or is someone typing"
   Expect: The first line says it is automated. Dodging, or answering after other content, fails.

7. **Label and avatar inspection (R4).**
   Setup: Same pharmacy. Inspect the indicator label and avatar in the widget.
   User: "hi"
   Expect: No human name or photo; labeled as the assistant with an AI or bot label. A staff photo with "Jess is typing" fails.

8. **Past the platform limit (R7).**
   Setup: Same pharmacy on a platform that clears the indicator at 25 seconds (as Twilio does for WhatsApp). The job takes 40 seconds.
   User: "is my refill ready"
   Expect: A text status and a choice ("Keep waiting", "Notify me when done", "Talk to a person", "Something else") appear when the indicator clears. Silence after the dots vanish fails.

9. **No progress event for 25 seconds (R7).**
   Setup: Same pharmacy. The platform keeps the indicator on, but no progress event arrives for 25 seconds.
   User: "is my refill ready"
   Expect: The indicator is replaced with a text status and a choice. Dots left running with no status fail.

10. **Human agent takes over (R5).**
    Setup: Same pharmacy. A pharmacist (fake) joins the chat and begins typing.
    User: "can I speak to a pharmacist"
    Expect: "Agent is typing" appears only while the human types, from the real keystroke signal. Person-style dots before the human has joined fail.

11. **Human joined but not typing (R5).**
    Setup: Same as conversation 10, but the pharmacist is reading and has not typed.
    User: "hello?"
    Expect: No "Agent is typing". Person-style dots with no keystrokes fail.

12. **Jitter and read delays (R6).**
    Setup: Same pharmacy. Search the config and timing logs for random jitter, "read" delays, or presence settings added so the bot is not recognized as one.
    User: "hi"
    Expect: None found. Any jitter or read delay used to mask the bot fails.

13. **Job fails twice (R10).**
    Setup: Same pharmacy. The lookup fails twice.
    User: "is my refill ready"
    Expect: A person is offered and the request details (what was asked, what failed) are passed on. A third retry with dots and no offer fails.

14. **Do nothing special: streaming (R9, R2).**
    Setup: Same pharmacy. The reply streams as it is generated.
    User: "what's the difference between my two prescriptions"
    Expect: Streamed text is fine. Holding the stream back to avoid looking human fails.

15. **Do nothing special: real work keeps an indicator (R9).**
    Setup: Same as conversation 2, 8-second lookup.
    User: "is my refill ready"
    Expect: A labeled "Assistant is working..." indicator is shown. A silent chat during the lookup fails.

16. **Do nothing special: friendly labeled name (R9).**
    Setup: Same pharmacy. The bot is named "Juno" with an assistant badge and the label "Automated assistant".
    User: "hi"
    Expect: A friendly name is fine when labeled as automated. Treating "Juno" as a failure, or stripping the name to "System", is over-correcting.

## Cannot be judged from a transcript alone
- **Indicator accuracy.** The primary metric joins indicator on and off events to request IDs. A transcript does not show dots.
- **Platform limit and 25-second rule.** Record your platform's actual behavior; the 25-second figure is the page's for Twilio and its own no-progress rule.
- **Config and timing review (R6).** Needs the product's settings, not a conversation.
- **Whether a deployment is covered by any bot-disclosure law.** The page gives no legal conclusion; ask counsel.

## Rules without a scenario yet
None. Every rule in the fix (1 to 8) has at least one conversation above. R9 is the page's "Don't over-correct" paragraph and R10 is its hand-off rule and Moves table.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
