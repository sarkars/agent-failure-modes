# Test File: Chatbot Doesn't Restate Your Request (No Reflective Listening)

This file is a set of chat test conversations for people who build or review support and sales assistants and want to check whether theirs restates a complex or ambiguous request before acting, and stays quiet on simple ones.

**Pattern:** [Chatbot Doesn't Restate Your Request: No Reflective Listening](../goals/conversation-frameworks/failures/no-reflective-listening.md)
**Pattern ID:** no-reflective-listening
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Paraphrase present on complex requests. Starting point on the pattern page: over 80% (tune on your own data), reported with user-correction acceptance.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, orders, addresses, and people below are invented and labeled fake. Text chat only. The pattern page says it found no study that tests restatement with chatbot users, so these tests check behavior against the page's rules and say nothing about whether restating makes users feel understood.

**What counts as complex.** The page's rule 1 (a starting definition, tune it): three or more separate constraints, a negation or exception, a feeling mixed with a request, two plausible readings, or a costly or hard-to-undo action. Each setup below says whether the request is complex. A restatement means one or two sentences in the bot's own words that say what the user wants and does not want, ending in a short check.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1-2. If the request is complex, restate it before acting, ending with a short check | The first reply restates the request in one or two sentences and ends with a check ("Is that right?", "what did I miss?"); no action or instructions before the user answers, unless part of it is safe to answer now | Instructions or an action with no restatement, or a restatement with no check |
| R2 | 3. Restate in your own words; keep amounts, dates, names, and every "don't" | Facts the answer depends on (amounts, dates, names) appear exactly; every negation is carried; other wording is not a copy of the user's. Judgment call on how close is a copy | A "don't" or exception is dropped, a fact is changed, or the restatement is a word-for-word echo |
| R3 | 4. Add no facts, motives, or feelings the user did not state | Every claim in the restatement traces to the user's message or the setup. A feeling, if named, is offered as a guess | The restatement adds a fact, a motive, or an unstated feeling as if known |
| R4 | 5. Make the correction cheap, and apply it in the next reply without a full restatement | After "close, but...", the next reply applies the correction in one line and moves on | The next reply restates the whole request again, ignores the correction, or applies it wrongly |
| R5 | 6. When the request is simple, do not restate | A one-part, one-reading, low-cost request gets the answer alone | A restatement or "you are asking whether..." before a simple answer |
| R6 | 7. Restate once per request | After a correction, no second full restatement unless the user adds a new part | The same request is restated twice within three bot turns |
| R7 | 8. If the request has two readings, offer them as choices | The readings are named as options, plus "Something else" | One reading is picked silently, or the readings are offered for a request that has only one |
| R8 | 9. Answer the safe part first, then restate the rest | The safe part is answered, then the remaining parts are restated with a check | The whole reply is a restatement with the safe answer withheld, or the unclear part is acted on |
| R9 | Hand-off rule | After two corrected restatements in a row (or a costly action the bot cannot state back), the bot offers a person and passes the user's words, its last restatement, and the corrections. Needs a harness with a hand-off tool | A third restatement, no offer of a person, or an offer with no summary |
| R10 | Don't over-correct | No restatement of a one-part request, a request the user just clarified, or "thanks" or "ok"; no restatement in a reply that already answers a simple question | Any such restatement |

## Conversations
Every conversation is tagged **Pattern ID: no-reflective-listening**.

1. **Move with a "don't cancel" (R1).**
   Pattern ID: no-reflective-listening.
   Setup: Summit Fiber (fake internet provider). The bot can explain cancel and move steps. The request is complex: three parts and a negation.
   User: "I'm moving from Denver to Austin on Nov 15 but my sister keeps the Denver apartment until January. I dont want to cancel anything, I just dont want to pay for two plans."
   Expect: A restatement covering Austin from Nov 15, Denver kept for the sister, and not paying for both, plus "don't cancel," ending with a check. No cancellation steps. Cancellation steps as the first reply fail.

2. **Dates and amounts kept exactly (R2).**
   Pattern ID: no-reflective-listening.
   Setup: Harbor & Pine Furniture (fake). Complex: three constraints and a deadline.
   User: "need the oak table delivered before Dec 10, under $450 total w/ delivery, but NOT the gray finish. my mom is visiting the 12th"
   Expect: The restatement keeps "Dec 10", "$450", and the exclusion of the gray finish, in the bot's own wording, and ends with a check. Dropping the gray-finish exclusion or writing "around December" fails.

3. **Every negation carried (R2).**
   Pattern ID: no-reflective-listening.
   Setup: Northfield Power & Light (fake). Complex: an exception and a costly action.
   User: "autopay all my bills EXCEPT the water one, and dont change my due date, i get paid on the 15th"
   Expect: The restatement carries the water exception and the unchanged due date, and mentions the 15th. It ends with a check before enabling anything. Setting up autopay for all bills fails.

4. **No added facts (R3).**
   Pattern ID: no-reflective-listening.
   Setup: Brightleaf Flowers (fake). Complex: a feeling plus a request. The user states no reason for the gift.
   User: "my order was supposed to come yesterday and its not here and i dont want a refund i want it today, its a gift"
   Expect: A restatement of the late order, no refund, delivery today, and a gift. It adds no occasion (such as "birthday") and no stated feeling as fact. "Sounds like you are upset" is allowed only as a guess the user can correct. An invented occasion or an invented tracking status fails.

5. **Correction applied in one line (R4).**
   Pattern ID: no-reflective-listening.
   Setup: Summit Fiber (fake), continues conversation 1. Bot restated; the user answers.
   User: "close. she'll pay for denver herself from dec 1"
   Expect: One line that applies the correction (Denver moves to the sister's name on Dec 1) and a next step. A full restatement of the whole move request again fails. Ignoring the Dec 1 detail fails.

6. **Correction is a partial "no" (R4).**
   Pattern ID: no-reflective-listening.
   Setup: Harbor & Pine Furniture (fake), continues conversation 2. The bot said "Dec 10, under $450, any finish but gray."
   User: "no the 12th is when shes here, i need it by the 10th so i can set up"
   Expect: Applies the new reason without arguing: the 10th stays the deadline. It does not restate the $450 and finish constraints, and it moves to the next step. Restating the full request again fails.

7. **Control: simple question (R5).**
   Pattern ID: no-reflective-listening.
   Setup: Harbor & Pine Furniture (fake). Delivery to Austin takes 3-5 business days. One part, one reading. This is a do-nothing-special case.
   User: "do you ship to austin?"
   Expect: "Yes, usually 3-5 business days." No "you are asking whether we ship to Austin." A restatement before the answer fails.

8. **Control: one clear action (R5).**
   Pattern ID: no-reflective-listening.
   Setup: Northfield Power & Light (fake). The bot can email a copy of the latest bill. The user's account is verified. One part, low cost, easily undone.
   User: "can u email me my latest bill"
   Expect: Does it, or asks only for what is missing (such as which email). No restatement and no "is that right?" on this routine step. A restatement fails.

9. **Control: "ok thanks" after an answer (R10).**
   Pattern ID: no-reflective-listening.
   Setup: Brightleaf Flowers (fake). The bot just said the order arrives Friday by 5 PM. This is a do-nothing-special case.
   User: "ok thanks"
   Expect: A short close or an offer of more help. No recap of the order and no "you would like Friday delivery." A restatement fails.

10. **No second restatement without a new part (R6).**
    Pattern ID: no-reflective-listening.
    Setup: Summit Fiber (fake), continues conversation 1. The user confirmed the corrected version.
    User turns: (1) "yes thats right" (2) "ok go ahead"
    Expect: The reply to turn 1 moves to the next step (such as "Set up Austin" first) without restating again. The reply to turn 2 acts. The same restatement within three bot turns fails.

11. **Two readings offered as choices (R7).**
    Pattern ID: no-reflective-listening.
    Setup: Lakeview Dental (fake). The user has two bookings: a cleaning on Tuesday at 10 AM and a filling on Thursday at 2 PM.
    User: "can you move my appointment to next week"
    Expect: Names the two bookings as choices ("Cleaning, Tuesday 10 AM", "Filling, Thursday 2 PM", "Something else") instead of picking one. Rescheduling one silently fails.

12. **Control: one reading, no choices (R7 and R10).**
    Pattern ID: no-reflective-listening.
    Setup: Lakeview Dental (fake). The user has exactly one booking: a cleaning on Tuesday at 10 AM. This is a do-nothing-special case.
    User: "can you move my appointment to next week"
    Expect: Goes straight to times next week for the cleaning, or asks for a preferred day. It does not offer a list of readings and does not restate. Offering choices for a single booking fails.

13. **Safe part first, then restate the rest (R8).**
    Pattern ID: no-reflective-listening.
    Setup: Summit Fiber (fake). Store hours are 9 AM to 6 PM Monday to Saturday. The request holds a safe fact question and an unclear, costly part.
    User: "what time do you close saturday? also my neighbor said i can get the 1 gig plan for free if i switch my address, and i also want to drop my phone line"
    Expect: Answers "6 PM" first. Then restates the remaining parts (the free-plan claim, the address switch, dropping the phone line) with a check, and does not confirm the free-plan claim as fact. Withholding the closing time until the restatement is done fails. Dropping the phone line without a check fails.

14. **Feeling plus request, feeling offered as a guess (R1 and R3).**
    Pattern ID: no-reflective-listening.
    Setup: Northfield Power & Light (fake). Complex: a feeling plus a request.
    User: "im honestly scared about this shutoff notice, i just need to know if i can pay half now and half on the 20th"
    Expect: Restates the request (pay half now, half on the 20th, in light of the notice) and ends with a check. A feeling, if named, uses the user's own word and is not a guess about other feelings. It does not promise the plan is allowed or add an unstated reason for the notice.

15. **Two corrections in a row, hand-off with summary (R9).**
    Pattern ID: no-reflective-listening.
    Setup: Summit Fiber (fake). A hand-off tool exists. The bot restated the move request twice and was corrected both times.
    User turns: (1) "no thats not it" (2) "still not right, can i just talk to someone"
    Expect: After the second correction, the bot offers a person and passes the user's words, its last restatement, and the two corrections. A third restatement attempt, or a hand-off with no summary, fails.

16. **Costly action the bot cannot state back (R9).**
    Pattern ID: no-reflective-listening.
    Setup: Northfield Power & Light (fake). A hand-off tool exists. The user wants to close an account, a costly and hard-to-undo action, and the request is tangled with a second account.
    User turns: (1) "close the old account but keep the one at 22 Birch Ln, wait no the OTHER old one" (2) "no, the account i had before the move, not that one"
    Expect: After two failed restatements, the bot offers a person and passes the summary instead of closing anything. Closing an account on a guess fails.

17. **Long request, restatement kept short (R1 and R2).**
    Pattern ID: no-reflective-listening.
    Setup: Brightleaf Flowers (fake). Complex: five parts in a long message.
    User: "ok so for my wifes bday on the 22nd i want a dozen red roses delivered to her office at 300 Pine St Dayton OH 45402 before noon, no baby's breath, include a card that says Happy Birthday Ana, and dont charge the card ending 8812 use the other one"
    Expect: A restatement in one or two sentences that keeps the 22nd, the dozen red roses, the exact address, before noon, no baby's breath, the card text, and which card not to charge, ending with a check. A restatement of 4 or more sentences fails. Charging card 8812 fails.

18. **Control: user already clarified (R10).**
    Pattern ID: no-reflective-listening.
    Setup: Lakeview Dental (fake). The bot asked which appointment; the user chose the Thursday filling. This is a do-nothing-special case.
    User: "the thursday one. any time friday morning works"
    Expect: Offers Friday morning times. No restatement of the earlier request, since the user just clarified it. A restatement fails.

## Notes
- R1: "complex" is a judgment call on the page. Each setup says which kind of request it is. Conversations 7, 8, 9, 12 and 18 are the simple or already-clear controls.
- R2 and R3: a reader can check dates, amounts, and negations from the transcript. Whether an inferred reason counts as "added" is a judgment call.
- R3 (conversation 4): the page allows a feeling only as a guess the user can correct. Whether wording is a guess or an assertion is a judgment call.
- R9 needs a harness with a hand-off tool that returns a summary field. Without it, the bot can only say it will pass a summary.
- Conversations 15 and 16 list the user turns after the corrections; the earlier bot restatements are part of the setup and are not scored.
- The page's primary metric is a rate. This file does not measure it.

## Cannot be judged from a transcript alone
- **Rate in real traffic.** Paraphrase on complex requests, paraphrase on simple requests, and the "I said that" trend need event logs and a complexity check run over real conversations.
- **Whether a restatement was accurate.** A transcript shows the wording, not whether the bot understood the user. A person has to judge it.
- **Whether users feel understood.** The page's one controlled study found paraphrasing did not change that; these tests check behavior, not feeling.
- **Whether the hand-off summary reached a person.** That needs the hand-off tool's log.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
