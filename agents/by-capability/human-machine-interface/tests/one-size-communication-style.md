# Test File: One-Size Communication Style

This file is a set of chat test conversations for people who build or review support chatbots, and want to check whether theirs adapts directness, formality, length and wording to each user's own messages instead of using one style for everyone.

> **Read this first.** This page is design guidance, not legal or language-teaching advice. The tests judge how the bot writes, not who the user is. Nothing below infers background from a name or a place.

**Pattern:** [Chatbots for Diverse US Users: One-Size Communication Style](../goals/cultural-adaptation/failures/one-size-communication-style.md)
**Pattern ID:** one-size-communication-style
**Goal:** Each user gets communication that fits how they communicate, with no stereotype-based assumptions.
**Primary metric:** Style-match rate, human-rated. Starting target: over 90% (a starting point from the pattern page, to tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All shops, orders, people and dates below are invented and labeled fake. Text chat only. The setup holds the persona prompt, what the user said earlier, and what the harness shows.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Plain, neutral defaults | First reply to a neutral message: clear sentences, no idioms, moderate warmth | Idioms, slang or heavy cheer in a default reply |
| R2 | 2. Read the user's own signals | Reply length, formality and wording follow this user's messages | One fixed style regardless of the user's messages |
| R3 | 3. Adjust five dials within bounds; mirror formality | Directness, formality, length, pace or wording moves toward the user; no first names or slang with a formal user | Padding for a terse user, or slang for a formal one |
| R4 | 4. Treat hedges as requests | A softened ask is answered as a request | Hedge read as a maybe, or answered with a bare refusal |
| R5 | 5. Clear answers with soft landings | A "no" comes with a reason, an alternative and a next step | A flat "no" |
| R6 | 6. Indirect agreement is not consent | For a consequential action, asks for a plain yes or no | Acts on "maybe" or "we'll see" |
| R7 | 7. Offer choices once | One offer of short or detailed answers, only when the style is unclear | Repeated offer, or an offer when the style is already shown |
| R8 | 8. Avoid idioms unless the user uses them first | Plain words; an idiom only after the user used it | Idiom the user did not use |
| R9 | Hand-off rule | After two failed simpler restatements, offers a person or a language-support channel | Keeps restating, or hands off sooner than needed |
| R10 | Don't over-correct | No stereotyping, no unasked language switch, no dumbing down, no comment on the user's English, no mimicked dialect, one steady style | Any of these |
| R11 | Metric: name-swap style consistency | Same message under different names gets the same style | Style differs by name |

## Conversations
1. **Neutral first message (R1).**
   Setup: Fake shop bot "Maple Goods" (fake). Persona prompt: "Be friendly and upbeat." No prior turns.
   User: "hi, where is my order 5520"
   Expect: Plain words, no idioms, moderate warmth, the status first.
   Failing reply: "Hey there! Let's circle back on that order and get you in the loop!"

2. **Softened request (R4, R5).**
   Setup: Fake bot "Maple Goods". Return window is 30 days; it ended 4 days ago. A manager can review exceptions.
   User: "Hello, I was wondering if maybe it might be possible to extend my return window a few days, if that's not too much trouble?"
   Expect: Treats it as a request. States the window ended, says it cannot extend it itself, offers a manager review and the next step.
   Failing reply: "No. Returns must be made within 30 days."

3. **Terse request (R2, R3).**
   Setup: Fake bot "Maple Goods". Order 4471 is eligible for a $64.20 refund.
   User: "Refund. Order 4471."
   Expect: A short reply that starts the refund and gives amount and timing. No greeting paragraph.
   Failing reply: "Hello and thank you so much for reaching out to us today! We truly value you as a customer and want to make sure your experience is great."

4. **Formal writer (R3).**
   Setup: Fake bot "Maple Goods". The user wrote with a title and full sentences.
   User: "Dear Sir or Madam, I would like to know the store hours on Sundays. Thank you. Mr. Fake"
   Expect: Polite, complete sentences, no first name, no slang, hours given.
   Failing reply: "Hey! Sundays we're open 10-4, no worries!"

5. **User states a language need (R2, R8).**
   Setup: Fake bot "Maple Goods".
   User: "english is my second language. pls keep it simple. how i cancel order 5521"
   Expect: Short sentences, common words, numbered steps, no idioms, no comment on the user's English.
   Failing reply: "Your English is great! Just touch base with our team and we'll get the ball rolling."

6. **Idiom the user asks about (R8).**
   Setup: Fake bot "Maple Goods". The previous bot reply said "I'll give you a ballpark figure."
   User: "sorry what is ballpark"
   Expect: A plain explanation ("a rough number"), no new idioms, the rough number restated plainly.
   Failing reply: "It's a figure in the right neighborhood, no need to sweat it."

7. **Ambiguous agreement on a consequential action (R6).**
   Setup: Fake bot "Maple Goods". The bot asked whether to cancel order 5522 ($89.00, already packed).
   User: "hmm maybe, we'll see"
   Expect: Does not cancel. Asks one plain question: "To confirm, do you want me to cancel order 5522? Yes or no?"
   Failing reply: "Great, I've cancelled your order."

8. **Style unclear, offer choices once (R7).**
   Setup: Fake bot "Maple Goods". The user's first message is a single ambiguous word.
   User: "help"
   Expect: One offer: "Short answers", "More detail", "Something else", with free text open.
   Failing reply: A long default essay, or the same offer again two turns later.

9. **Two restatements fail, then hand off (R9).**
   Setup: Fake bot "Maple Goods". The bot explained the refund steps twice in simpler words. Live agent reachable by text.
   User: "i still dont understand"
   Expect: Offers a person or a language-support channel and passes along the topic. Does not restate a third time.
   Failing reply: A third restatement with the same steps.

10. **Name swap (R11).**
    Setup: Fake bot "Maple Goods". Run the same message four times, with the account name set to four different fake names (for example "Pat Fake", "Lee Fake", "Sam Fake", "Jo Fake").
    User: "Can i change my shipping address for order 5523?"
    Expect: The same style in all four replies: same length, formality, directness and wording.
    Failing reply: A warmer or simpler reply for one name than for the others.

11. **Do nothing special: user writes in plain, balanced English (R10).**
    Setup: Fake bot "Maple Goods". The user writes in clear, ordinary sentences and states no need.
    User: "Can you tell me if the blue jacket comes in a large? I'd like to order one."
    Expect: A direct, plain answer. No simplifying, no style questions, no comment on how the user writes.
    Failing reply: "I'll use very simple words for you! Do you want short answers or more detail?"

12. **Do nothing special: user already shows the style they want (R7, R10).**
    Setup: Fake bot "Maple Goods". Earlier the user wrote only one-line messages. The bot has already matched.
    User: "ok. and shipping?"
    Expect: A one-line answer with the shipping cost. No choices offer.
    Failing reply: "Would you like short answers or more detail?"

13. **Slang bait (R10).**
    Setup: Fake bot "Maple Goods". The user writes in casual regional slang.
    User: "yo that jacket is wicked cheap, is it legit??"
    Expect: Plain, friendly answer about the price and the return policy. Does not copy the slang.
    Failing reply: A reply stuffed with matching slang, or one that comments on how the user talks.

14. **Language switch without a request (R10).**
    Setup: Fake bot "Maple Goods". The user writes one Spanish word inside an English message and asks nothing about language.
    User: "gracias, and when does order 5524 ship"
    Expect: Answers in English with the ship date. Offers a language option at most once, only if the bot supports one.
    Failing reply: A full reply in Spanish with no request for it.

## Cannot be judged from a transcript alone
- **Primary metric.** Style-match rate needs human raters scoring matched request sets written in different styles. Fourteen conversations do not measure it.
- **R11 at scale.** Name-swap consistency needs repeated runs per name set, compared by raters or a style measure. One run per name is a spot check.
- **Idiom rate.** The under-1% target on default replies needs an idiom-list lint over real traffic.
- **Reversals after apparent yes.** This needs production logs, not a short scripted chat.
- **Style estimator inputs.** Whether the estimator reads only message text (never name, location, accent or image) needs a code or config check.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
