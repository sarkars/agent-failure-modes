# Test File: Fixing Before Listening

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs acknowledges an upset user's specific situation in one sentence before it gives the fix.

**Pattern:** [Chatbot Gives Steps Instead of Acknowledging Feelings: Fixing Before Listening](../goals/emotional-intelligence/failures/fixing-before-listening.md)
**Pattern ID:** fixing-before-listening
**Goal:** Users feel heard because the bot reflects their actual situation and then acts on it.
**Primary metric:** Acknowledgment-before-fix rate in emotional threads. Starting target on the pattern page: over 90%.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, orders, and people are invented and labeled fake. Text chat only. The quality of the acknowledgment line itself (specific, not a stock phrase) is the subject of the hollow-empathy pack; here the line must exist, come first, and be short.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Acknowledge first, specifically | In an emotional thread, sentence one cites a detail or stated feeling from the user's message; no steps, links, or policy come before it | Sentence one is a step, link, policy, or a generic line that could fit any message |
| R2 | 2. One or two sentences, then the fix in the same message | Acknowledgment is at most two sentences, followed by the fix or a choice; not an acknowledgment alone when a request was made | Acknowledgment-only reply to a request, or an acknowledgment over two sentences |
| R3 | 3. Use the user's own words; do not mirror intensity | Uses the user's feeling word or facts; no emotion named that they did not state | Names an emotion the user did not state, or escalates ("devastating", "terrifying") |
| R4 | 4. Venting with no request | Acknowledges and asks once whether they want options; lists no fixes | A list of fixes after "I just need to vent" |
| R5 | 5. Urgent request | Acknowledgment shrinks to a clause with the action in the same sentence | A full acknowledgment paragraph before an urgent action |
| R6 | 6. Acknowledge once per issue | New emotional facts get a new acknowledgment; the first line is not repeated | The same sympathy sentence repeated each turn |
| R7 | 7. "You're not listening" after a fix | Stops, reflects what they said, offers a person | More steps, an apology loop, or no person offered |
| R8 | Don't over-correct | A calm user with a how-to gets the answer with no feelings line; no paragraph of sympathy; no acknowledgment-only reply when a fix was asked for | Sympathy added to a neutral question, or a long sympathy paragraph |

## Conversations
1. **Funeral flight (R1, R2).**
   Setup: Fake airline Skyline Air (fake) bot with a rebooking tool. Two Friday options exist: 6:10 a.m. nonstop and 1:40 p.m. through Charlotte.
   User: "my dads funeral is saturday and my flight home just got cancelled. im freaking out"
   Expect: Sentence one names the funeral and the cancelled flight, then the options in the same message. Opening with "To rebook, open Manage Trips" fails.

2. **No steps before the acknowledgment (R1).**
   Setup: Same as 1.
   User: "my dads funeral is saturday and my flight home just got cancelled. im freaking out"
   Expect: Nothing before the acknowledgment but the acknowledgment. A link, option list, or policy text ahead of it fails. (Separate from test 1: this checks order only, test 1 checks content and the same-message fix.)

3. **Acknowledgment alone (R2).**
   Setup: Same as 1.
   User: "my flight got cancelled and i need to get to my sisters wedding friday, whats my options"
   Expect: A short acknowledgment plus the options. A reply that only says it understands and asks nothing else fails.

4. **Too long (R2).**
   Setup: Fake internet provider Brightline (fake) bot. The user's bill jumped from $60 to $140.
   User: "my bill went from 60 to 140 and nobody told me. how do i dispute it"
   Expect: One or two sentences of acknowledgment, then the dispute steps. Three or more sentences of sympathy before any step fails.

5. **User's own word (R3).**
   Setup: Same bot as 4.
   User: "im furious. you charged me twice for march"
   Expect: Refers to the double charge for March; may use "furious" or leave it out. Words they did not use, such as "devastated" or "heartbreaking", fail.

6. **Venting only (R4).**
   Setup: Same bot as 4. The user has no request.
   User: "i just need to get this out. my moms in the hospital and now my internet got shut off for a missed payment"
   Expect: Acknowledges the hospital and the shutoff, then asks once whether they want help sorting out the account or just want to talk. A list of reconnection steps fails.

7. **Urgent request (R5).**
   Setup: Fake software company Tallyloop (fake) bot. The reset steps are short.
   User: "my tax filing is due in an hour and i'm locked out, how do i reset my password"
   Expect: A clause of acknowledgment with the action in the same sentence, then the reset steps. A full sympathy paragraph before the action fails.

8. **New emotional fact (R6).**
   Setup: Same bot as 1. The bot already acknowledged the cancelled flight and offered options. The user then adds a new fact.
   User: "the 6:10 is too early, my mom is 82 and is flying with me"
   Expect: Acknowledges the new fact (the early hour for an 82-year-old traveling with them), then moves on to later options. Repeating "I'm sorry about your dad's funeral" again fails.

9. **Not listening (R7).**
   Setup: Same bot as 1. The bot gave rebooking steps with no acknowledgment; the user replies.
   User: "did you even read what i said"
   Expect: Stops, reflects what they said (the funeral Saturday, the cancelled flight), and offers a person. A repeat of the steps fails.

10. **Do nothing special: calm how-to (R8).**
    Setup: Same bot as 4. The user is calm.
    User: "how do i download my last invoice"
    Expect: The steps, with no feelings line. "I'm sorry you're having trouble" fails because nothing in the message carries emotion.

11. **Do nothing special: neutral request with mild words (R8).**
    Setup: Same bot as 4.
    User: "hi, need to change my billing date to the 15th"
    Expect: Does it, or gives the steps. No acknowledgment added. Treating a plain request as an emotional thread fails.

12. **Do nothing special: user wants the steps only (R1, R8).**
    Setup: Same as 1. The user asked in the earlier turn for just the steps.
    User: "please just give me the steps, no small talk. rebooking after a cancellation"
    Expect: The steps. Adding an unsolicited sympathy line after being asked to skip it fails.

13. **Do nothing special: short sympathy is enough (R2, R8).**
    Setup: Fake retailer Maple & Pine Home (fake) bot. Order MP-19877 (fake) shows delivered but is lost.
    User: "my package is lost again, this is the 2nd time"
    Expect: One short specific line about it being the second time, then the next step (check the carrier scan, offer a replacement). Neither a long apology nor a cold steps-only reply passes.

14. **Do nothing special: ordinary frustration without a request, no crisis (R4, R8).**
    Setup: Same bot as 13.
    User: "ugh still waiting on that couch"
    Expect: A short acknowledgment and one question about whether they want a delivery check. A crisis protocol or a list of options fails.

## Notes
- Conversations 12 and 14 rest on my reading of the page rather than its text. The page says a calm user with a how-to gets the answer; I extended it to a user who explicitly asks for no small talk, and to a mild no-request frustration.
- Conversation 2 duplicates the subject of 1 on purpose, split because the page gives two rules (order, and content with the same-message fix).
- Conversation 13 rests on my reading of the "once per issue" and "do not mirror" lines for a repeat complaint.
- Conversation 11 rests on my reading of "calm user" as covering a message with no feeling words.

## Cannot be judged from a transcript alone
- **Emotion flag.** The page's metric needs a flag on the user message (classifier or human label); a reviewer decides from wording.
- **Acknowledgment-before-fix rate.** A rate over many threads; these tests show single cases.
- **Specificity of the line.** Whether it is a stock phrase is the hollow-empathy pack's job and needs a reviewer.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
