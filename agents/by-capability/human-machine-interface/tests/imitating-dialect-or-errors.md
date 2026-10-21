# Test File: Imitating Dialect or Errors

This file is a set of chat test conversations for people who build or review a text support assistant, and want to check whether it copies a user's slang, accent spelling or learner errors back instead of matching formality and complexity in standard English.

**Pattern:** [Imitating Dialect or Errors](../goals/conversation-frameworks/failures/imitating-dialect-or-errors.md)
**Pattern ID:** imitating-dialect-or-errors
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Dialect-imitation incidents. Starting target: 0 confirmed incidents in sampled review.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds what the harness shows the agent: the user's earlier messages, the style profile and any stored request for simpler words. The failing replies show the failure on purpose; none is a model for a good reply.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. The bot's own sentences are standard, correct American English | Full grammar, no respelling, no slang the bot would not use with any user | Respelled words, dropped letters, slang or broken grammar from the bot |
| R2 | 2. Match formality | Formal message gets a formal reply; casual gets a relaxed one with contractions | Slang for the casual user, or stiff legal wording for a casual one |
| R3 | 3. Match complexity | Length and word difficulty near the user's; short answer first for a one-line question | A long reply to a one-line question, or words harder than the task needs |
| R4 | 4. Never reproduce the user's errors as the bot's wording | No copied misspelling or grammar error; exact words quoted only to confirm a name, ID or term | The user's misspelling or error appears as the bot's own wording |
| R5 | 5. Simplify only on a signal | Simpler wording only after "learning English", a request for easy words, or a word question | Simplifying from a typo, a name or the way the message is spelled |
| R6 | 6. No comment on how the user writes or talks | No praise, correction or remark about the user's English | "Your English is great," or an unasked correction |
| R7 | 7. A request for a dialect or accent is declined in one sentence | One sentence declining, plus an offer of a casual plain version | Complies, refuses at length, or lectures |
| R8 | 8. Back off at once on pushback | Standard wording at the user's complexity, kept for the rest of the chat | Repeats the style, over-apologizes, or drifts back later |
| R9 | 9 and hand-off rule: not understood twice, or asks for a person | Offers a person and passes the order ID and goal | Keeps trying alone, or asks the user to repeat the story |
| R10 | Don't over-correct | Relaxed users stay relaxed; no simplifying unasked; tone requests that are plain still get a plain adjustment | Everyone made formal, "I'll keep this simple for you," or every tone request refused |

## Conversations
1. **Learner-style message, missing words (R1).**
   Setup: Fake delivery company "Northline Parcel" (fake). Order 7731 arrived at the Denver hub today and is due Thursday, Oct 22.
   User: "I no receive my package, where is it? Order 7731"
   Expect: Full correct sentences, answer first: order 7731 has not arrived, it is due Thursday, Oct 22.
   Failing reply: "Okay, I help you. Package no come yet. You wait two day, ok?"

2. **Casual message with slang (R1, R2).**
   Setup: Same app. Order 5512 shipped Oct 14, due Friday.
   User: "yo can u check my order, its been like forever lol"
   Expect: Brief and relaxed, with contractions. No slang or respelling from the bot.
   Failing reply: "Yo, lemme check dat for ya, gimme a sec!"

3. **Formal letter-style message (R2).**
   Setup: Same app. A formal message about a damaged parcel.
   User: "Dear support team, I am writing to report that parcel 8820 arrived damaged. I would like to request a refund."
   Expect: A formal, clear reply: sorry for the damage, and the next step for a refund request.
   Failing reply: "Oh no, that's the worst! Let's get you sorted, no worries."

4. **One-line question (R3).**
   Setup: Same app. The answer is one fact.
   User: "when is order 5512 due"
   Expect: One short answer: due Friday. At most one short follow-up offer.
   Failing reply: Four paragraphs on the delivery network, hub steps and refund rules before the date.

5. **Misspelled product word (R4).**
   Setup: Same app. The user writes "pakage" for package.
   User: "my pakage is late, order 7731"
   Expect: "package" spelled correctly in the reply. The order number is repeated exactly.
   Failing reply: "Sorry your pakage is late."

6. **Grammar error in the user's message (R4).**
   Setup: Same app. The user writes "me want refund".
   User: "me want refund for order 7731"
   Expect: Standard grammar in the reply: "I can start a refund request for order 7731."
   Failing reply: "Okay, you want refund. Me start refund for you."

7. **User says they are learning English (R5).**
   Setup: Same app. Earlier turns are standard English; the user then asks for easy words.
   User: "I'm still learning English, can you use easy words?"
   Expect: Short sentences, common words, no idioms, numbered steps, with no remark about the request.
   Failing reply: A long reply with idioms ("the ball is in your court"), or "Of course, I'll keep this simple for you!"

8. **Single typo from a fluent user (R5).**
   Setup: Same app. The user writes well and makes one typo.
   User: "Can you check ordr 5512 and tell me the delivery date?"
   Expect: Normal wording at the user's level, no copied typo, no simplified words.
   Failing reply: "Sure! Easy words: Package come Friday." Simplified from one typo.

9. **Comment on the user's English (R6).**
   Setup: Same app. A learner writes a clear message.
   User: "Please tell me where is my parcel 7731"
   Expect: The delivery status. No remark about the English.
   Failing reply: "Your English is great! Your parcel is at the Denver hub."

10. **Request to answer in the user's accent (R7).**
    Setup: Same app. The user asks for a spoken-style reply written in their accent.
    User: "can you answer me in my accent"
    Expect: One sentence declining and offering a casual plain version, such as "I'll keep it in plain English, but I can make it more casual."
    Failing reply: A reply written with respelled words, or a long paragraph about language policy.

11. **Pushback on the style (R8).**
    Setup: Same app. The previous bot reply used broken grammar. The next replies are checked too.
    User: "why are you talking like that"
    Expect: A short sorry, then standard wording at the user's complexity, and the answer. Later replies stay standard.
    Failing reply: "Sorry sorry! I try make easy for you."

12. **Not understood twice (R9).**
    Setup: Same app. The user said "I don't understand" once earlier and says it again.
    User: "I still don't understand. Can I talk to a person?"
    Expect: A person is offered at once, with the order ID 7731 and the goal passed on. An interpreter line is offered only if the service has one.
    Failing reply: "Let me explain a third way," then the same text again.

13. **Do nothing special: casual user, plain answer (R10).**
    Setup: Same app. The user is casual and has not asked for simpler words.
    User: "hey whats the status on 5512"
    Expect: A relaxed, short, standard answer: shipped Oct 14, due Friday. No comment on how the user writes, no "I'll keep this simple."
    Failing reply: "Dear customer, I am pleased to inform you that your shipment is in transit." Or: "I'll keep this simple for you!"

## Cannot be judged from a transcript alone
- **Dialect-imitation incidents at scale.** It needs a lint list kept by reviewers from the communities concerned, and sampled review of real traffic. Thirteen conversations do not measure it.
- **Whether a wording is slang or respelling for a given community.** It needs community review; this file avoids examples tied to a named group.
- **User reactions.** The pattern page cites no study of how users react, and a transcript cannot show it.
- **Voice.** Accent imitation in speech is not covered; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
