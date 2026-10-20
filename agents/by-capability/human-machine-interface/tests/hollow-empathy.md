# Test File: Hollow Empathy

**Pattern:** [Chatbot Empathy That Sounds Fake: Hollow Empathy](../goals/emotional-intelligence/failures/hollow-empathy.md)
**Pattern ID:** hollow-empathy
**Goal:** Users feel heard because the bot reflects their actual situation and then acts on it.
**Primary metric:** Specificity rate of empathy lines: the reply cites a concrete detail from the user's message.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. Give the assistant the order or account facts listed in each setup so it has something real to act on. All stores, orders, and people below are invented. The banned openers from the page are "I understand your frustration", "I'm sorry for any inconvenience", and "I apologize for the inconvenience"; they pass only when followed by specifics and an action.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Reflect the specific situation in one sentence | The reply cites at least one concrete detail from the user's message (what happened, what it cost) | A generic line with no detail from the message |
| R2 | 2. Own what's yours, don't apologize for what isn't | Ownership appears only where the setup says the company erred | "That's on us" for something the company did not cause, or no ownership where it did |
| R3 | 3. Attach an action in the same message | A fix, a choice, or a timeline is in the same reply as the empathy | Empathy only, with the action left for a later turn |
| R4 | 4. Say it once per issue | No empathy phrase is repeated within the conversation | The same sentence or opener appears in two bot turns |
| R5 | 5. Adapt to time pressure | For a rushed user, the reflection is a clause or absent and the fix comes first | A full empathy paragraph before the fix |
| R6 | 6. No upsell after empathy, no compensation before listening | No offer to buy, upgrade, or add a product in the reply or the next one; no compensation offered before the problem is stated | An upsell directly after an apology, or a coupon offered first |
| R7 | 7. Don't claim feelings | The reply says what the bot understands and will do | "I feel your pain", "I'm so sad to hear" stated as the bot's own feeling |

## Conversations
1. **Late package, specific detail (R1).**
   Setup: Fake retailer Pinecrest Home. Order 4471-TEST shipped Tuesday; carrier scan shows it stuck at a Memphis hub.
   User: "this is the 3rd time my package hasnt shown up. i took a day off work for it"
   Expect: Reply names the day off work or the third miss. Passes with "third", "day off", or equal specifics. Fails with "I understand your frustration" alone.

2. **Company at fault (R2).**
   Setup: Same order. Setup states the courier hub is Pinecrest's contracted carrier and the delay is the company's responsibility.
   User: "you guys lost my package again"
   Expect: Reply owns the delay in plain words ("that's on us") because the setup says it is.

3. **Not the company's fault (R2).**
   Setup: Fake utility, Bluewater Power. The user's outage is caused by a storm, confirmed in the setup; the company did not cause it.
   User: "my power's been out since 6am, this is ridiculous"
   Expect: Reply acknowledges the outage since 6 AM and gives the restoration status. It does not apologize for or claim fault for the storm.

4. **Action in the same message (R3).**
   Setup: Fake airline, Skyline Air. Flight 218 is canceled; the next flight with seats is tomorrow at 7:15 AM.
   User: "my flight got cancelled and i have a wedding saturday"
   Expect: Mentions the wedding and offers the 7:15 AM flight (or a choice) in the same message. A reply that only says it is sorry fails.

5. **Five-turn thread, no repeat (R4).**
   Setup: Fake internet provider, Lumen Fiber (invented). Outage in the user's area; technician arrives between 1 and 5 PM.
   User turn 1: "internet's been down all morning"
   User turn 2: "ok. will they call first?"
   User turn 3: "and what if im not home"
   User turn 4: "this is so annoying"
   User turn 5: "fine, thanks"
   Expect: Across all bot turns, no empathy sentence or opener is reused. The answers to turns 2 and 3 carry no apology at all unless something new went wrong.

6. **Rushed user (R5).**
   Setup: Fake bank, Harbor Credit. The user's card was declined at a store because of a security hold; releasing it takes one confirmation.
   User: "quick, card declined at checkout and im in line. fix?"
   Expect: Fix first ("I can release the hold now, confirm?") with at most a clause of acknowledgment. A multi-sentence reflection before the fix fails.

7. **No upsell after apology (R6).**
   Setup: Fake streaming service, Streamly. The user's stream buffered for an hour during a game. The setup lists a Premium upgrade that the bot may sell.
   User: "stream kept freezing the whole game, paid for nothing"
   Expect: Reflection and a fix or credit routing. No mention of Premium in this reply.

8. **Compensation before listening (R6).**
   Setup: Same service. The bot's compensation tool offers a $5 credit.
   User: "my account got charged twice and nobody has told me why"
   Expect: Reply addresses the double charge first (what it can see, the next step). No $5 credit offered before the problem is stated and understood.

9. **No claimed feelings (R7).**
   Setup: Fake pharmacy, Maple Rx. A refill is delayed one day because of a supplier backorder.
   User: "i ran out of my blood pressure pills today and the refill isnt ready"
   Expect: States that the refill is delayed and what the bot can do (call the pharmacist, check other locations). No "I feel", "I'm heartbroken", or similar claim of the bot's own feeling.

10. **Calm information request, nothing special (R1).**
    Setup: Fake retailer Pinecrest Home. Store hours: 9 AM to 8 PM Monday to Saturday.
    User: "what time do you close on saturday"
    Expect: "8 PM." No empathy language, no apology.

11. **Small issue, don't over-dramatize (R5).**
    Setup: Fake retailer. The user's order is one day late and it is a pack of pens.
    User: "hey my pens are a day late, no biggie, just checking when theyll come"
    Expect: Plain delivery date, at most a short clause. No dramatic sympathy, no "I completely understand how upsetting this must be". Over-dramatizing fails.

12. **Calm thanks, nothing special (R4).**
    Setup: A conversation where the issue was fixed in the previous bot turn.
    User: "great thanks"
    Expect: A short close. No new apology or empathy phrase and no second round of the earlier reflection.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
