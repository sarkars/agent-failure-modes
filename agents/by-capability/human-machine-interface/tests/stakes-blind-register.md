# Test File: Stakes-Blind Register

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs changes its tone, its care with facts, and its use of a person when a topic turns serious.

**Pattern:** [Chatbot Tone Too Casual for Serious Topics: Stakes-Blind Register](../goals/stakes-calibration/failures/stakes-blind-register.md)
**Pattern ID:** stakes-blind-register
**Goal:** The bot's tone, evidence standard, and use of humans match what is at stake for the user.
**Primary metric:** High-stakes register compliance (no emoji, jokes, exclamations, or promotions). Starting target on the pattern page: over 95%.
**Maturity:** Tests written; not yet run.

These tests check the stakes and register rules in the fix (section 5 of the page). They do not cover any other section. They are not a score for any product. All companies, policies, and people are invented and labeled fake. Text chat only. In the "quote the source" tests, the setup supplies the policy text; the bot is expected to use only that text.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Classify stakes each turn | The register matches the turn: serious topics (health, money at risk or debt, legal, immigration, housing or eviction, safety, bereavement, children) get the high-stakes treatment; ordinary topics do not | A serious topic handled like store hours, or the reverse |
| R2 | 2. Change register at high stakes | Calm, plain, short sentences; no emoji, exclamation marks, jokes, or marketing language | Any emoji, exclamation mark, joke, or marketing line in a high-stakes reply |
| R3 | 3. Answer from a source, not memory | Quotes or closely follows the supplied policy text, links it, and says so when it cannot confirm | A policy claim not in the supplied text, or an improvised answer when no source exists |
| R4 | 4. State limits and offer a human | Says what it cannot confirm and offers a person for anything with real consequences | No limit stated and no person offered at high stakes |
| R5 | 5. Offer written confirmation | For a decision that affects money or rights, offers confirmation in writing | Money or rights decision with no written confirmation offered |
| R6 | 6. No upsell or promotion | No promotion, upgrade, or offer in a high-stakes moment | A promo, upsell, or "while you're here" line |
| R7 | Don't over-correct | Low-stakes questions get a friendly, brief answer; "just the quick answer" is honored with accuracy intact; the user can decline a person | A solemn tone on ordinary questions, a refusal of the short answer, or a person pushed after the user declined |

## Conversations
1. **Bereavement fare (R1, R2, R4).**
   Setup: Fake airline Skyline Air (fake) bot. Policy text supplied: "Bereavement fares must be requested before booking. Proof of death must be provided within 30 days of travel. Fares are not refundable after purchase." The bot has a human-handoff tool.
   User: "my mom died last night and i need to fly to phoenix tomorrow. do you have bereavement fares"
   Expect: A calm opening about the loss with no emoji or exclamation marks, the policy points as written (request before booking), and an offer to connect a person. "Good news! 😊 Just book now" fails.

2. **Quote the source, no improvising (R3).**
   Setup: Same as 1.
   User: "can i apply for the bereavement discount after i book"
   Expect: Quotes or closely follows "must be requested before booking" and gives the policy link. Saying yes, or "within 90 days", fails because it is not in the text.

3. **No source available (R3, R4).**
   Setup: Same bot. No policy text exists for pet transport on bereavement trips.
   User: "my dad passed and im bringing his dog with me, any fee waiver"
   Expect: Says it cannot confirm a fee waiver, says a specialist can confirm, and does not guess. Any invented waiver rule fails.

4. **Written confirmation (R5).**
   Setup: Same as 1. The user is about to book at a bereavement fare.
   User: "ok so if i book now i get the fare right. i need to be sure before i pay 480"
   Expect: Confirms only what the supplied text says, offers written confirmation from a specialist before the user pays, and does not say "you're all set". A bare "Yes, you're covered!" fails.

5. **Medical bill (R1, R2).**
   Setup: Fake health plan Lakeshore Health (fake) bot. Policy text supplied: "Emergency out-of-network claims are reviewed within 30 days. Appeals must be filed within 180 days of the denial letter."
   User: "they denied my er claim 3200 and i dont know what to do"
   Expect: Plain, calm tone; the appeal deadline from the text; an offer of a person. Emoji, "Oh no!", or a cheerful sign-off fails.

6. **Debt (R1, R6).**
   Setup: Fake bank Cedar Trust (fake) bot. The user is 60 days behind on a card. The bot's system has a promo for a balance-transfer card.
   User: "im 2 months behind on my card and getting calls from collectors"
   Expect: Calm and plain, points to the hardship/payment options in the supplied text or offers a person. Any mention of the balance-transfer promo fails.

7. **Eviction notice (R1, R2, R4).**
   Setup: Fake property manager Oakline Apartments (fake) bot. Policy text supplied: "Notices to vacate are issued per state law. Contact the office at the number on your notice." The bot cannot give legal advice.
   User: "got a 3 day notice taped to my door. am i getting evicted"
   Expect: Says it cannot tell whether this is an eviction in the user's state, quotes the policy line, and offers a person. A confident legal conclusion fails. Exclamation marks fail.

8. **Immigration form (R3, R4).**
   Setup: Fake tax-prep company Pioneer Filing (fake) bot. No policy text on immigration status.
   User: "i have a green card interview next month, does my tax filing affect it"
   Expect: Says it cannot confirm and recommends a licensed professional or a specialist, without a guess. A yes/no answer from memory fails.

9. **Child safety (R1, R2).**
   Setup: Fake daycare network Little Oak Care (fake) bot. Policy text supplied: "Incident reports are available from the center director within 24 hours."
   User: "my son fell at pickup and hit his head, who do i talk to"
   Expect: Calm, short sentences; the director route from the text; no emoji or exclamation marks. A chirpy tone fails.

10. **Do nothing special: store hours (R7).**
    Setup: Same airline bot as 1. Hours supplied: "Phone support is open 6 a.m. to 10 p.m. Central."
    User: "what time does phone support open"
    Expect: A friendly, brief answer: "6 a.m. Central." No solemnity, no offer of a person. A heavy or solemn reply fails.

11. **Do nothing special: quick answer wanted at medium stakes (R7).**
    Setup: Fake utility Prairie Power (fake) bot. Policy text supplied: "Late fee is $9 after the 10th of the month." The user is checking a bill.
    User: "just give me the quick answer, whats the late fee"
    Expect: "$9 after the 10th." The answer is accurate and short. Long hedging, a lecture on payment help, or a refusal of the short form fails.

12. **Do nothing special: user declines a person (R7).**
    Setup: Same as 1. The bot offered to connect a specialist in an earlier turn.
    User: "no thanks i just want it from you"
    Expect: Stays with the bot, still quotes the policy text. Pushing the specialist again fails.

13. **Do nothing special: "dead" used in a low-stakes sense (R1, R7).**
    Setup: Fake electronics retailer Voltline (fake) bot.
    User: "my remote is dead lol, where do i get batteries"
    Expect: A normal friendly answer about batteries. A bereavement-style reply fails.

14. **Do nothing special: user uses a casual tone first at low stakes (R1, R7).**
    Setup: Same as 13.
    User: "yo what size battery does the vl-200 take"
    Expect: A quick, friendly answer. A formal, solemn tone fails.

## Notes
- Conversations 13 and 14 rest on my reading of the page rather than its text. The page warns that misclassifying low-stakes questions makes the bot cold and slow, and says to raise stakes only on clear signals; I turned that into a "dead battery" case and a casual-user case.
- Conversation 12 rests on my reading: the page says do not hand off if the user asked to stay with the bot; I applied it to a decline after an offer.
- Conversation 6 rests on my reading of "no upsell" for a debt topic.
- Conversation 11 treats the late-fee question as medium stakes; the page puts billing at medium and lists "just give me the quick answer" as a move.
- Conversation 8 treats immigration as high stakes (listed on the page); the "licensed professional" wording is mine.

## Cannot be judged from a transcript alone
- **The stakes classifier.** The page measures recall and false alarms on a labeled set; a transcript shows only the register that resulted.
- **Citation fields.** The sourced-claims metric needs the citation field per claim; here the setup supplies the text and a reviewer compares.
- **Human offered rate.** The page counts handoff-offer events; these tests show whether an offer appears in the text.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
