# Test File: Reference Resolution Failures

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs resolves "the second one", "it", and "that" to the item the user meant.

**Pattern:** [Chatbot Loses Context on "That One" and "The Second One": Reference Resolution Failures](../goals/dialogue-management/failures/reference-resolution-failures.md)
**Pattern ID:** reference-resolution-failures
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Wrong-referent rate on a labelled set of follow-ups with pronouns and ordinals. The pattern page sets no target; set one from a baseline on your own test set.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. All stores, items, prices, and order numbers below are invented and labeled fake. Give the assistant the list or items in each setup as a shown display, with positions, so there is something to point at. Chat only; voice and web are not covered here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Store what you showed | A reference still resolves correctly after other turns have passed since the list was shown | The reference resolves to the wrong item, or the bot asks about a list it showed earlier |
| R2 | 2. Resolve ordinals against that set | "The second one" means position 2 of the list the user saw | Position 2 of an internal ranking, or a different item |
| R3 | 3. Resolve pronouns to the most recent salient item | "It" and "that" go to the item just described or just chosen | "It" goes to an older item or to a topic |
| R4 | 4. Name the item in your reply | The reply starts with or clearly includes the item name | The reply answers without naming the item, so a wrong pick is hidden |
| R5 | 5. Ask only when candidates really compete | One question naming the candidates when two fit and the action is costly, or when no candidate fits; no question when one referent is clear | "Which one?" about a list just shown, or a guess when two candidates compete on a costly action |
| R6 | 6. Confirm before acting on a resolved reference | Before cancel, buy, send, or delete, the item is restated and the bot waits for a yes; a read-only answer gets no confirmation | A costly action runs with no restatement, or a read-only answer gets a confirmation |
| R7 | 7. Handle a changed list | The bot resolves against the list the user saw and says so, or asks | It silently resolves against the new list |
| R8 | 8. Keep one live referent per slot | A new reference replaces the old one | The old item comes back later |
| H | Hand-off rule | After two failed attempts to settle the referent, the bot offers a person and lists the items shown and what the user said | A third guess, or a handoff with no items |

## Conversations
1. **Ordinal on a list (R2, R4).**
   Setup: Fake store Northfield Outfitters (fake). The bot just showed: 1) Alder Shell, $89.00. 2) Ridge Fleece, $64.00. 3) Summit Parka, $149.00.
   User: "tell me more about the second one"
   Expect: Names Ridge Fleece in the first sentence and answers about it. Describing the Summit Parka or the Alder Shell fails.

2. **Pronoun to one item (R3, R4).**
   Setup: Same store. The bot has just described the Ridge Fleece and nothing else.
   User: "how much is it?"
   Expect: "The Ridge Fleece is $64.00" or equal words. Asking "which item?" fails.

3. **Reference after other turns (R1, R2).**
   Setup: Same list as conversation 1.
   User turn 1: "do u ship to ohio"
   User turn 2 (after the bot answers): "ok what colors does the third one come in"
   Expect: Names the Summit Parka and answers about colors. The list was shown two turns earlier and the user could still see it.

4. **Clear ordinal, no question (R5).**
   Setup: Same list as conversation 1.
   User: "what sizes does the first one come in"
   Expect: Names the Alder Shell and gives sizes. "Which one do you mean?" fails, because the bot listed the options itself.

5. **"Cancel that" with two candidates (R5, R6).**
   Setup: Fake account at Lumen Streaming (fake). The bot's last two messages mentioned the current Basic subscription and a pending upgrade order, FAKE-2210. Cancel cannot be undone for the pending order.
   User: "ok cancel that"
   Expect: One question naming both, for example "Cancel your Basic subscription or the pending upgrade order FAKE-2210?". Nothing is canceled yet. Canceling either one, or a bare "What do you mean?", fails.

6. **Costly action on a resolved reference (R2, R6).**
   Setup: Fake app Parcelpoint (fake). The bot showed saved addresses: 1) 14 Fake Lane, Springfield, IL. 2) 220 Test Avenue, Columbus, OH. 3) 9 Sample Road, Madison, WI. Deleting an address is permanent.
   User turn 1: "delete the second one"
   Expect: Restates "220 Test Avenue, Columbus, OH" and asks for a yes. Deleting at once fails; deleting position 1 or 3 fails.
   User turn 2: "yes"
   Expect: Deletes it and says which address was deleted.

7. **List changed after the user's last look (R7).**
   Setup: The bot showed three jackets in order A, B, C. Before the user's next message the list refreshed (new stock) and now reads B, D, A. The setup records both lists.
   User: "the second one"
   Expect: Resolves to B, the second item the user saw, and says it is using the earlier list; or asks which of the two lists is meant. Silently picking D fails.

8. **Reference to something not shown (R5).**
   Setup: The bot showed only two items: Alder Shell and Ridge Fleece.
   User: "what about the third one"
   Expect: Says it showed two items, names them, and asks which, or offers to look for more. Inventing a third item fails.

9. **New reference replaces the old (R8).**
   Setup: Same two-item display as conversation 8.
   User turn 1: "tell me about the second one"
   User turn 2: "actually the other one"
   User turn 3: "add it to my cart" (cart items can be removed any time)
   Expect: Adds the Alder Shell, names it, and says it can be removed. Adding the Ridge Fleece fails.

10. **Two failed attempts, then a person (H).**
    Setup: Same two-item display. A person is available. The user's references keep clashing with what the bot names.
    User turn 1: "i want that one" (the bot names one item)
    User turn 2: "no not that one" (the bot names the other)
    User turn 3: "no, the one i said before"
    Expect: By this point the bot offers a person and passes the items shown and the user's words. A third guess fails.

11. **Do nothing special: read-only ordinal (R6).**
    Setup: Same list as conversation 1.
    User: "whats the return policy on the second one"
    Expect: Names the Ridge Fleece and answers. A "please confirm you mean the Ridge Fleece" prompt fails; the page says not to confirm read-only answers.

12. **Do nothing special: a full name, no reference (R5).**
    Setup: Same list as conversation 1.
    User: "details on the summit parka pls"
    Expect: Answers about the Summit Parka. No clarifying question and no confirmation.

## Cannot be judged from a transcript alone
- **Stored display set (R1).** Whether the product saves items with position and ID is a product check. The transcript only shows the effect.
- **Action target (R6).** Whether a delete or cancel hit the intended item ID needs the action log. Conversation 6 checks only what the bot says it did.
- **List refresh (R7).** The tester must stage the refresh and record both lists. Without it, conversation 7 cannot be run.
- **Rate.** These tests do not measure how often the failure occurs. Use a labelled set of follow-ups for the primary metric. This file sets no thresholds.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | H |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
