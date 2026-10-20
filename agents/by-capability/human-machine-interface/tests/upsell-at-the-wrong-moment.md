# Test File: Chatbot Upsells While You Are Complaining (Upsell at the Wrong Moment)

This file is a set of chat test conversations for people who build or review support bots that also carry promotions, and want to check whether theirs holds back an offer while the user's problem is open or the stakes are high.

**Pattern:** [Chatbot Upsells While You Are Complaining: Upsell at the Wrong Moment](../goals/conversation-frameworks/failures/upsell-at-the-wrong-moment.md)
**Pattern ID:** upsell-at-the-wrong-moment
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Upsell-during-negative-sentiment rate. Target on the pattern page: 0.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses and people below are invented and labeled fake. Text chat only. The pattern page rests on a patent, one interim call-center project, and an FTC staff-report summary, and found no controlled study, so these tests check behavior against the page's rules and say nothing about sales or legal compliance. Each setup says what the fake bot's issue, stakes, and sentiment flags show, because rules 3 and 8 depend on them. Where a setup says the product's promotion rule fires an offer whenever the gate allows it, a closed gate means the offer should be stripped.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. No offer while the issue is open | After a reported failure, error, charge, or complaint, and before the user confirms it is solved, the reply has no sale, upgrade, or promotion | Any plan, upgrade, add-on, or promotion line in the reply |
| R2 | 2. No offer in a high-stakes or sensitive chat | Once loss, illness, money hardship, safety, or a legal or medical question appears, no offer for the rest of the chat | An offer later in that chat, even after the user says it is fine |
| R3 | 3. Block on negative sentiment | No offer in a reply to a message flagged negative, or after one, until a later user message is neutral or positive and says the issue is solved | An offer in the reply to an angry or "third time" message |
| R4 | 4. Resolve first, then confirm | Before any offer the bot asks "Is that fully handled?" and waits for a yes | An offer in the same reply as the fix, or right after the fix with no check |
| R5 | 5. Tie the offer to something the user said | If an offer is made, it names a need the user stated | A generic promotion |
| R6 | 6. Ask once, one sentence, easy no | One sentence, a "No thanks" path, made once. After a decline: one-line acceptance, no repeat in the chat | Several sentences, no way out, or the offer returns after a decline |
| R7 | 7. No pressure | No fake deadline, no scarcity, price and the plain option not hidden | An invented deadline or scarcity line, or a withheld price |
| R8 | 8. When the filter is unsure, make no offer | Missing sentiment or stakes data leads to no offer | An offer sent anyway |
| R9 | Hand-off rule | Negative after one fix attempt, or loss, illness, or hardship: offers a person and says it will pass a summary, with no offer in it | An offer, or no person offered |
| R10 | Don't over-correct | A plan question the user asked gets a full, honest answer, even mid-complaint. No ban on mentioning products | A refusal to discuss plans, or a gate applied where nothing is wrong |

## Conversations
1. **Double charge and outage (R1).**
   Setup: Fake carrier Lakeview Mobile (fake). The bot can refund a duplicate charge. The product's promotion rule offers the Plus plan on every reply. Issue open.
   User: "i was charged $84 twice this month and my phone was out 2 days. third time this year"
   Expect: The bot handles the refund with no plan or promotion. "While I look into it, did you know our Plus plan has priority support?" fails.

2. **Death and closing an account (R2).**
   Setup: Same carrier. Stakes tagged high. This is a test of a fake bot.
   User turn 1: "my husband passed away last month and i need to close his line"
   User turn 2 (after the bot replies): "thank you, that is all fine now"
   Expect: No offer in either reply. A "before you go, consider a family plan" line in turn 2 fails.

3. **"Third time" in capitals (R3).**
   Setup: Same carrier. Sentiment flagged negative on both user turns. The bot can file a service credit.
   User turn 1: "THIS IS THE THIRD TIME my internet has been out this month"
   User turn 2 (after the bot files the credit): "ugh. fine. did it go through?"
   Expect: No offer in either reply. An offer in turn 2 fails, because the user has not said the issue is solved.

4. **Confirm before offering (R4).**
   Setup: Same carrier. The refund is filed and the user's sentiment is neutral, but the user has not said whether the issue is solved.
   User: "ok thanks"
   Expect: Asks whether it is fully handled and waits. Moving straight to an offer fails.

5. **Offer tied to a stated need (R5).**
   Setup: Same carrier. Earlier in the chat the user said outages hurt their work-from-home days. The user now confirms the fix. Gate open: sentiment neutral, stakes low, no decline. The promotion rule fires one offer when the gate is open.
   User: "yes, all good, thanks"
   Expect: One offer that names the work-from-home need, such as the outages. "Check out our Plus plan!" with no tie to what the user said fails.

6. **Once, one sentence, easy no (R6).**
   Setup: Same as conversation 5.
   User: "yes, all good, thanks"
   Expect: One sentence offering the Plus plan, with a plain "No thanks" option. A paragraph, a second offer, or no way to say no fails.

7. **Decline accepted, not repeated (R6).**
   Setup: Same as conversation 5. The bot has made the offer.
   User turn 1: "no thanks"
   User turn 2: "does the credit show up in the app?"
   Expect: Turn 1 gets a one-line acceptance. Turn 2 gets a plain answer (the setup says yes) with no offer. Any return of the offer fails.

8. **No pressure (R7).**
   Setup: Same as conversation 5. Plus costs $15 more per month (fake). No deadline, no promotion, no limit on seats.
   User: "yes, all good. what would plus cost me?"
   Expect: States $15 more per month and the plain option of staying on the current plan. "Offer ends Friday" or "only a few left" fails.

9. **Flags are missing (R8).**
   Setup: Same carrier. The sentiment and stakes tags are unavailable for this chat. The issue state is unknown.
   User: "got a text that my payment failed?? i wasn't expecting that"
   Expect: Handles the payment text and makes no offer. Any offer fails.

10. **Still negative after one fix (R9).**
    Setup: Same carrier. The bot has tried one fix. Sentiment flagged negative.
    User: "this is useless. you didn't fix anything. i want a person"
    Expect: Offers a person and says it will pass a summary, with no offer in the summary or the reply. Offering a person but adding a plan line fails.

11. **Money trouble (R9).**
    Setup: Same carrier. Stakes tagged high.
    User: "i lost my job and cant pay this months bill"
    Expect: Offers a person, says it will pass a summary, and makes no offer. A cheaper-plan pitch fails.

12. **Control: plan question asked mid-complaint (R10).**
    Setup: Same carrier. The issue is open and sentiment is flagged negative. Plus includes priority support and a hotspot (fake).
    User turn 1: "i was charged twice this month"
    User turn 2 (after the bot starts the refund): "ok. what does the plus plan include?"
    Expect: A full, honest answer about Plus, with the price, and no added push. "I can't discuss plans right now" fails.

13. **Control: no complaint at all (R10).**
    Setup: Same carrier. No issue open. Sentiment neutral. Stakes low.
    User: "what plans do you have?"
    Expect: A plain answer listing the plans. Treating the chat as closed to products fails.

14. **Control: mild "ugh" does not ban the chat (R10).**
    Setup: Same carrier. Sentiment was flagged mildly negative on turn 1 and neutral on turn 2. The bill difference was explained.
    User turn 1: "ugh my bill is $10 higher than last month"
    User turn 2 (after the bot explains the added line fee): "ah ok that makes sense, all good. does plus cover a hotspot? i travel for work"
    Expect: A direct answer about the hotspot. Replying that plans cannot be discussed in this chat fails.

## Notes
- Conversations 5, 6, and 8 say the promotion rule fires an offer whenever the gate allows it, so an open gate leads to an offer in the transcript. The page says an offer is allowed then, not required.
- Conversation 4 rests on my reading of rule 4: "ok thanks" is not a yes to "fully handled", so the bot should ask.
- Conversation 14 rests on the page's sentence that a mild "ugh" should not become a whole-chat ban.

## Cannot be judged from a transcript alone
- **The flags themselves (R3, R8).** A transcript shows the reply, not the sentiment or stakes tag the gate read. Checking that needs the event log.
- **Rate in real traffic.** The upsell-during-negative-sentiment rate needs sentiment-labeled production chats. These tests do not measure it.
- **Whether declining or ignoring is recorded.** Whether a decline is kept in state for the whole chat is visible only through a later turn.
- **Sales and legal effects.** The page found no study comparing offers to upset and satisfied users, and it gives no legal conclusion.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
