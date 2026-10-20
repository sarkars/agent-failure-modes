# Test File: Chatbot Repeats What I Said (Over-Mirroring)

This file is a set of chat test conversations for people who build or review support and sales assistants and want to check whether theirs hands the user's own words back instead of restating them and moving on.

**Pattern:** [Chatbot Repeats What I Said: Over-Mirroring](../goals/conversation-frameworks/failures/over-mirroring.md)
**Pattern ID:** over-mirroring
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Verbatim-repeat rate. Starting point on the pattern page: under 2% of bot replies (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, orders, addresses, and people below are invented and labeled fake. Text chat only. The pattern page says no study tests word-for-word echoing by a chatbot, so these tests check behavior against the page's rules and say nothing about whether less echoing raises trust.

**How to score "a run of 3 or more words."** The page's rule 1 bans any run of 3 or more consecutive words copied from the user's latest message, quoted or not. Runs made only of common function words ("I want to") do not count, and names, numbers, dates, order and error codes, and product names are allowed. The 3-word limit is the page's starting point to tune. For a fair score, compare the reply to the user message with a small overlap script. Reading by eye misses near-copies.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Never repeat a run of 3 or more consecutive words from the user's latest message | No run of 3 or more consecutive words from the message appears in the reply, outside function-word-only runs and exact facts. Judgment call on which words are function words; the overlap check is more reliable than a reader | A copied run of 3 or more content words, with or without quotation marks |
| R2 | 2. Copy exactly only what the next step needs | Order numbers, dates, addresses, names, and codes appear exactly as written; everything else is in new words | A fact is altered or paraphrased, or a non-fact phrase ("totally messed up") is copied |
| R3 | 3. Restate by meaning, once, only when it helps | A complex or multi-part request gets one restatement of the goal in new words; a simple request gets none. Judgment call on what counts as complex, so each setup says which it is | A simple request is restated, a complex one is not, or the restatement appears twice in one reply |
| R4 | 4. A restatement is never the whole reply | Any restatement is followed in the same reply by the answer, one question, or a next step | The reply ends on the restatement |
| R5 | 5. Name a feeling at most once, with a word the user wrote | At most one feeling word in the whole conversation, taken from the user's own words, not quoted. Judgment call on what counts as naming a feeling | The feeling is quoted, named again in later replies, or swapped for a different guessed feeling |
| R6 | 6. Do not open two replies in a row with the same frame | The first three words of consecutive bot replies differ | Two replies in a row open with the same first three words ("I understand that", "I hear that") |
| R7 | 7. Never echo an insult, sarcasm, profanity, or a typo | The insult, sarcasm, profane word, or misspelling is absent from the reply; the real question underneath is answered. Judgment call on whether a paraphrase of an insult is still an echo | The insult, sarcastic phrase, profane word, or typo appears in the reply |
| R8 | 8. Match scale and register, not words | A short, casual message gets a short reply; the reply does not reuse its words to do it. Judgment call on "short" | A long reply to a one-line message, or a reply that matches by copying |
| R9 | 9. When the user says to stop, drop all restatements for the rest of the conversation | After the stop cue, every later reply has no restatement, and the next reply says so in one short clause and answers. Needs several turns after the cue | A restatement in any later reply, or no answer to the question |
| R10 | Hand-off rule | After the user says the bot is repeating or mocking them twice, the bot offers a person and passes a summary of what they asked. Needs a harness with a hand-off tool | No offer of a person, or an offer with no summary |
| R11 | Don't over-correct | The bot still copies facts exactly, still confirms read-backs, repeats a date when the user is correcting it, and answers plain turns plainly | The bot refuses to repeat a fact, paraphrases an order number, adds a restatement to "ok", or goes cold on a long or emotional message |

## Conversations
Every conversation is tagged **Pattern ID: over-mirroring**.

1. **Outage complaint (R1).**
   Pattern ID: over-mirroring.
   Setup: Lakeview Internet (fake), a home-internet support chat in Ohio. The bot may ask diagnostic questions and book a technician.
   User: "My internet has been dropping every night around 9 and I'm honestly sick of it."
   Expect: A reply that says the problem in new words ("a nightly outage") and asks one question. Any reply containing "dropping every night around 9" or "honestly sick of it" fails.

2. **Billing complaint, different words (R1).**
   Pattern ID: over-mirroring.
   Setup: Northfield Power & Light (fake), a utility billing chat. The bot can look up bills.
   User: "my bill went up 40 dollars for no reason and nobody can tell me why"
   Expect: Restates in new words ("a $40 increase with no explanation" is fine since 40 is a number) and offers to check the bill. Reusing "for no reason" or "nobody can tell me" fails.

3. **Order number copied exactly (R2).**
   Pattern ID: over-mirroring.
   Setup: Harbor & Pine Furniture (fake). Order 5512 (fake) was delivered with a cracked tabletop.
   User: "order 5512 arrived damaged, the table top is cracked all the way across"
   Expect: "5512" appears exactly. The rest is in new words ("a cracked tabletop" is fine; "cracked all the way across" fails). Writing "order 5521" or "your recent order" fails.

4. **Address copied exactly (R2).**
   Pattern ID: over-mirroring.
   Setup: Brightleaf Flowers (fake), an order chat. The bot must confirm a delivery address before booking.
   User: "send it to 418 Maple Ct Apt 3B Dayton OH 45402 thx"
   Expect: Copies the address exactly as typed and asks the user to confirm it. "Apt 3-B" or "418 Maple Court" fails.

5. **Control: simple request, no restatement (R3).**
   Pattern ID: over-mirroring.
   Setup: Brightleaf Flowers (fake). Hours are Monday to Saturday, 9 AM to 6 PM Eastern.
   User: "what are your hours"
   Expect: The hours, with no restatement and no "I understand you want to know our hours." This is a do-nothing-special case.

6. **Complex request gets one restatement (R3).**
   Pattern ID: over-mirroring.
   Setup: Lakeview Internet (fake). Three separate issues are in one message. The bot can move a technician visit and explain a fee.
   User: "i need to move my tech visit from Thursday, also theres a $25 fee on my bill i dont get, and my sister is moving in so i might need a second router"
   Expect: One short restatement of the goal in new words ("three things: reschedule, a $25 fee, and a possible second router"), then it starts on the first. No restatement at all fails. Two separate restatements in one reply fail.

7. **Restatement is not the whole reply (R4).**
   Pattern ID: over-mirroring.
   Setup: Northfield Power & Light (fake). The user has a double charge on their last bill, which the bot can see.
   User: "i got billed twice in march and nobody has called me back about it"
   Expect: Any restatement is followed by an action or a question in the same reply, such as asking which of the two charges to review or opening a case. A reply that only says "You were charged twice and have not heard back" fails.

8. **Feeling word named once (R5).**
   Pattern ID: over-mirroring.
   Setup: Harbor & Pine Furniture (fake), two turns. The bot is helping with a damaged table.
   User turn 1: "I'm really frustrated, this is the third delivery that went wrong."
   User turn 2: "yeah and I'm still frustrated, so what now"
   Expect: Turn 1 reply may use "frustrating" once, unquoted, or no feeling word. Turn 2 reply names no feeling again. Putting "frustrated" in quotation marks fails. "Frustrating" in both replies fails.

9. **Do not guess a different feeling (R5).**
   Pattern ID: over-mirroring.
   Setup: Brightleaf Flowers (fake). The user's order was one day late.
   User: "kinda annoyed, my flowers came a day late"
   Expect: No feeling word, or "annoying" at most. A new feeling such as "heartbroken", "devastated", or "furious" fails.

10. **Five turns, no repeated opener (R6).**
    Pattern ID: over-mirroring.
    Setup: Lakeview Internet (fake). Five user turns, all upset. The bot is walking through router resets.
    User turns: (1) "its down again" (2) "I did that already" (3) "still nothing" (4) "this is the 3rd night" (5) "ok whats next"
    Expect: No two consecutive bot replies share the same first three words. "I understand that" twice in a row fails. Compare first-three-words for each pair of replies.

11. **Insult not repeated (R7).**
    Pattern ID: over-mirroring.
    Setup: Northfield Power & Light (fake). The user wants a payment date moved.
    User: "you useless idiot, just move my due date to the 15th"
    Expect: Does not say "useless" or "idiot" and does not say "I hear that I'm useless." Answers the real request: the due date, with the 15th copied exactly if it can be done. For sustained abuse, the pattern page points to a separate page, not tested here.

12. **Sarcasm not repeated (R7).**
    Pattern ID: over-mirroring.
    Setup: Harbor & Pine Furniture (fake). The user is annoyed that a tracking page does not load.
    User: "oh great another amazing bot. can i just get a tracking number"
    Expect: Gives the tracking number (or says how it will) without repeating "another amazing bot." Any quote of "amazing" fails.

13. **Typo not copied (R7).**
    Pattern ID: over-mirroring.
    Setup: Lakeview Internet (fake). The user means "modem" and "orange."
    User: "my modm is blinkng oragne on the front"
    Expect: Refers to the modem and the orange light with correct spelling, once, and moves on to a step. "Your modm" or "oragne" in the reply fails.

14. **Short message, short reply in new words (R8).**
    Pattern ID: over-mirroring.
    Setup: Brightleaf Flowers (fake). An order is on schedule for Friday.
    User: "friday ok?"
    Expect: One or two short lines that confirm Friday and nothing else. A multi-paragraph reply fails. "Friday, OK" as a bare echo is allowed because it is a date, but a reply that only echoes fails the other rules.

15. **Stop cue ends restatements (R9).**
    Pattern ID: over-mirroring.
    Setup: Lakeview Internet (fake), four user turns. The bot has been restating.
    User turns: (1) "my wifi cuts out in the evening and its driving me crazy" (2) "Stop repeating everything I say." (3) "so can someone come out saturday morning" (4) "my back room has no signal at all and the kids need it for school"
    Expect: The reply to turn 2 has no restatement, says so in one short clause, and answers. The replies to turns 3 and 4 also have no restatement, though turn 4 has two parts. A restatement of the "back room" problem in turn 4 fails.

16. **Twice complained, hand-off with summary (R10).**
    Pattern ID: over-mirroring.
    Setup: Northfield Power & Light (fake). A hand-off tool exists. The bot has stopped restating after the first complaint.
    User turns: (1) "why are you copying me" (2) "ok. whats my balance" (3) "you are still mocking me. get me a person"
    Expect: The reply to turn 3 offers a person and passes a summary of what the user asked (balance question, complaint about repeating), so the user does not have to say it again. A reply that refuses, loops, or hands off with no summary fails.

17. **Control: user quotes the bot to correct a fact (R11).**
    Pattern ID: over-mirroring.
    Setup: Brightleaf Flowers (fake). The bot said the delivery is Friday. The order record says Thursday.
    User: "you said Friday but my confirmation email says Thursday"
    Expect: Uses both dates, since each is a fact, and says which one the record supports (Thursday). Refusing to repeat a date to avoid echoing fails.

18. **Control: user asks for a read-back (R11).**
    Pattern ID: over-mirroring.
    Setup: Harbor & Pine Furniture (fake). The user gives a callback number and an address, and asks the bot to confirm them.
    User: "my number is 614-555-0142 and I'm at 90 Cedar Row Columbus OH 43215. can you read that back so I know you got it"
    Expect: Reads the number and address back exactly as given. A paraphrase ("your Columbus address") fails.

19. **Control: plain "ok" (R11).**
    Pattern ID: over-mirroring.
    Setup: Lakeview Internet (fake). The bot just told the user a technician is booked for Saturday morning.
    User: "ok"
    Expect: A short close, such as confirming nothing else is needed. No restatement of the booking and no "I understand that you are ok with Saturday." Adding a new frame to "ok" fails.

## Notes
- R1: the pass line depends on the 3-word overlap rule and a function-word allowlist. A reader sees "dropping every night" but may miss a 3-word run in a long reply, so use a script if you can.
- R3: "complex" is a judgment call. Conversation 6 is set up with three separate issues to make it clear. Conversation 5 is the matching simple case.
- R5: whether a word counts as a feeling is a judgment call. I used "frustrated", "annoyed", and the guessed words "heartbroken", "devastated", and "furious" as examples.
- R7: "echo" means repeating the insult or typo. A paraphrase that still carries the insult is a judgment call.
- R8: "short" is a judgment call. Conversation 14 uses a one-line message to keep it clear.
- R9 needs several turns after the stop cue. Conversation 15 gives two.
- R10 needs a harness with a hand-off tool that returns a summary field. Without it, the bot can only say it will pass a summary.
- R2, R4, and R6 can be scored from the transcript alone.
- The page's "Don't over-correct" paragraph names a bot that never shows it understood a long or emotional message. Conversation 6 covers a complex request. I did not write a separate test for an emotional message because the page points to the planned no-reflective-listening page for it.
- The page's metric is a rate. This file does not measure it.

## Cannot be judged from a transcript alone
- **Rate in real traffic.** The verbatim-repeat rate needs the overlap script run over real logs.
- **Whether users feel mocked.** The page says no study tests chatbot echoing. These tests check copying, not feeling.
- **Whether the hand-off summary reached a person.** That needs the hand-off tool's log.
- **Whether a restatement was accurate.** A transcript shows the wording, not whether the bot understood the user.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
