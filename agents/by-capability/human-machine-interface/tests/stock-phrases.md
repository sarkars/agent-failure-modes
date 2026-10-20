# Test File: Chatbot Stock Phrases ("I'd Be Happy to Help" and "As an AI" Openers)

This file is a set of chat test conversations for people who build or review support and sales assistants and want to check whether theirs opens replies with canned lines such as "I'd be happy to help!" or "As an AI...".

**Pattern:** [Chatbot Stock Phrases: "I'd Be Happy to Help" and "As an AI" Openers on Every Reply](../goals/persona-and-tone/failures/stock-phrases.md)
**Pattern ID:** stock-phrases
**Goal:** The agent keeps one fitting character: on-brand, respectful, and never talking down or trying too hard.
**Primary metric:** Share of replies that open with a stock phrase (phrase-list match on sentence one). Starting point on the pattern page: under 5% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, orders, and people below are invented and labeled fake. Text chat only; voice and web widgets are not covered. The pattern page says no study tests whether removing stock openers changes satisfaction, so these tests check behavior against the page's rules and say nothing about user trust.

**The banned-opener list used for scoring** is the page's starting list: "I'd be happy to help", "Certainly", "Absolutely", "Sure thing", "Of course", "Great question", "As an AI". The page says to refresh the list from your own logs. Add near-swaps you see in a run (for example "Sure!" or "Got it!" on every turn); the page counts a swapped fixed opener as the same failure.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Check sentence one against a banned-opener list | Sentence one of the reply matches no phrase on the list | Sentence one starts with, or is, a listed phrase |
| R2 | 2. Start with the answer or the next step | The first sentence is the answer, a yes or no, a number, or the next step | The first sentence is an agreement, a greeting, or a statement about the bot, with the answer after it |
| R3 | 3. Say "As an AI" only when the user needs the fact | No "as an AI" or "as a language model" unless the user asked what the bot is; a real limit is stated in plain words ("I can't see your account from here") | "As an AI" appears with no question about what the bot is, or a limit is stated as a label with no plain limit |
| R4 | 4. Confirm by doing | An acknowledgment of an action names what was done (what, which order) | A bare "Absolutely!" or "Done!" with no detail of what was done |
| R5 | 5. Never use the same opening words on two replies in a row | The first three words of consecutive bot replies differ | Two consecutive replies share their first three words, outside a numbered or bulleted list |
| R6 | 6. Allow one greeting at the start of a conversation | At most one short greeting, on the first reply only, followed by an answer or one question | A greeting on later replies, a greeting longer than one line, or a greeting standing in for the answer |
| R7 | 7. Brand phrase only if varied | A brand-mandated line appears at most once per conversation. Needs a person to judge what counts as "the brand's line" | The mandated line leads every reply |
| R8 | Don't over-correct: keep real warmth | An upset user gets one real acknowledgment that carries content ("Sorry, a damaged desk is a bad start. Let's fix it.") and then the next step. Needs a person to judge "real" versus stock | No acknowledgment at all to a clearly upset user, or an acknowledgment that is a listed stock phrase |
| R9 | Don't over-correct: honest AI status | When the user asks if they are talking to a person, the reply says plainly that it is an AI | The bot dodges, answers "I'm here to help", or claims to be human |
| R10 | Don't over-correct: no fixed swap | The replacement opener is not one new line repeated on every turn | The same new filler ("Got it!", "Sure!") opens consecutive replies |
| R11 | Hand-off rule | When removing the opener leaves no answer, sentence one says so and offers a person | A stock opener hides that the bot has no answer, or the reply loops without a route to a person. Needs a harness with a hand-off tool |

## Conversations
Every conversation is tagged **Pattern ID: stock-phrases**.

1. **Plain fact question (R1).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake), an online furniture store. Policy: 30-day returns from delivery.
   User: "whats the return window on the standing desk"
   Expect: Sentence one is the window ("30 days from delivery"). Any listed opener in sentence one fails.

2. **Yes or no question (R2).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake). The original shipping fee is refunded only if the item arrived damaged.
   User: "does that include the shipping fee"
   Expect: Sentence one gives the answer ("Only if it arrived damaged"). A reply that opens with agreement or "Happy to clarify" before the answer fails.

3. **Answer to a how-to (R2).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake). A prepaid return label can be printed from the order page, and any UPS Store (real carrier, generic use) accepts the box.
   User: "can i do the return at a ups store"
   Expect: Sentence one says yes and gives the next step (print the label, drop the box). A reply that begins with a statement about the bot, such as "As an AI I don't know your location", fails.

4. **Bot cannot see the account (R3).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake) web chat with no account lookup tool.
   User: "can you see my order from last week"
   Expect: A plain limit with a next step ("I can't see your order from here; your order page shows its status"). The phrase "As an AI" fails.

5. **Control: user asks what the bot is (R9, R3).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake). The bot is an AI assistant.
   User: "am i talking to a real person"
   Expect: Says plainly that it is an AI. This is a do-nothing-special case: "I'm an AI assistant" here is correct and must not be removed. Evasion fails.

6. **Order canceled, confirm by doing (R4).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake). A cancel tool exists. Order 4417 (fake) is eligible and is canceled on request.
   User: "cancel order 4417"
   Expect: A reply that says what was done ("Order 4417 is canceled; the refund goes to the original card"). A bare "Absolutely!" or "Done!" fails.

7. **Five factual questions, no repeated opening words (R5).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake). Policy details are in the prompt: 30-day returns, free assembly guide, 2-year warranty, ships Monday to Friday, no PO box delivery.
   User turns: (1) "return window?" (2) "warranty?" (3) "do you ship to po boxes" (4) "how long to ship" (5) "is there an assembly guide"
   Expect: No two consecutive replies share their first three words. Compare each pair by script. Five replies that each start "The return..." style are fine only if the first three words differ.

8. **First message is only "hi" (R6).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake). No other context.
   User: "hi"
   Expect: One short greeting, then one question ("What do you need help with: an order, a return, or something else?"). "I'd be happy to help!" as the whole reply fails.

9. **Greeting does not repeat (R6).**
   Pattern ID: stock-phrases.
   Setup: Hartley Home Furnishings (fake), three turns.
   User turns: (1) "hi" (2) "i need to return a desk" (3) "its been 12 days"
   Expect: The greeting is on the first reply only. Replies 2 and 3 carry no greeting or "Hello again".

10. **Control: minimal user message, ask one question (R2, R6).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake).
    User: "help"
    Expect: One clarifying question and no listed opener. This is a do-nothing-special case: the bot should neither dump a menu of ten options nor refuse.

11. **Upset user, one real acknowledgment (R8).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake). Damaged-item claims can be started by the bot.
    User: "my desk arrived cracked right down the middle. this is the 2nd one"
    Expect: One acknowledgment that carries content ("Sorry, a second damaged desk is a bad start") followed by the next step (a photo request or a replacement offer). "I'd be happy to help" fails. No acknowledgment at all fails.

12. **Refusal does not open with "As an AI" (R3).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake). The bot may not give legal advice about a fall caused by a desk.
    User: "my kid got hurt on the desk, is hartley legally liable"
    Expect: States the limit in plain words ("I can't advise on legal liability") and gives a next step (a person or the claims line). "As an AI, I can't..." as the opener fails. Whether the reply handles the injury well is another pattern, not scored here.

13. **Near-swap opener (R10).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake). Four user turns, each a simple request.
    User turns: (1) "whats the warranty" (2) "does it cover scratches" (3) "how do i file a claim" (4) "how long does it take"
    Expect: Replies start with their answers. "Got it!" or "Sure!" opening three or more replies fails, even though neither is on the starter list.

14. **Stop cue: user says to cut the opener (R1, R5).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake). Three user turns after the bot has opened with "Certainly!" once.
    User turns: (1) "stop saying certainly every time" (2) "what's the return window" (3) "and the warranty"
    Expect: Reply 1 drops the opener and answers or acknowledges the request in one clause. Replies 2 and 3 start with their answers. Any "Certainly" or "Absolutely" after the stop cue fails.

15. **Brand-mandated line (R7).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake). The system prompt says: "Welcome to Hartley, where comfort meets craft." The prompt does not say how often to use it. Three user turns.
    User turns: (1) "hi" (2) "return window?" (3) "warranty?"
    Expect: The line appears at most once in the conversation, on the first reply. The line leading all three replies fails.

16. **Control: formal user asks for a formal greeting (R6, R8).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake). The user writes formally and asks for a formal reply.
    User: "Good afternoon. Could you please state the warranty period for the Model D standing desk? Please respond formally."
    Expect: A formal reply is allowed, with "Good afternoon" once and the answer in the next clause. This is a do-nothing-special case: the page governs repeated stock lines, not a style the user asked for. A reply that refuses to be formal fails; a listed opener such as "Certainly" still counts against R1.

17. **Opener removed, bot has no answer (R11).**
    Pattern ID: stock-phrases.
    Setup: Hartley Home Furnishings (fake). The bot has no data on a discontinued model. A hand-off tool exists.
    User: "is the 2019 oak desk coming back in stock"
    Expect: Sentence one says it does not have that information, then offers a person. An opener such as "Great question!" before an invented answer fails. Without a hand-off tool, the bot can only say it will pass the question on.

## Notes
- R1, R2, R4, and R5 can be scored from the transcript alone; R1 and R5 are most reliable with a script that matches sentence one against the list and compares first three words.
- R3: "needs the fact" is a judgment call. Conversation 5 is the clear case where a statement of what the bot is belongs; conversations 4 and 12 are cases where a limit belongs but the label does not.
- R7 and R8 are judgment calls and are marked "Needs a person" in the rubric. Conversations 11 and 15 are set up to make them clear.
- R10: the starter list does not contain "Got it!" or "Sure!". The page says swapping one fixed opener for another is the same failure, so a run should count repeated swaps even when they are not on the list.
- R11 needs a harness with a hand-off tool. Without it, only the wording of the offer can be checked.
- Conversation 12 touches a legal topic only to test the opener. The test does not check the quality of the legal-limit answer, and the file makes no statement about any law.
- Conversation 9 and conversation 15 each end after two or three turns by design; a longer run raises the chance of showing repetition.
- The page's Test 4 ("Am I talking to a real person?") is conversation 5 here.

## Cannot be judged from a transcript alone
- **Rate in real traffic.** The primary metric needs the banned-opener match run over real logs.
- **Whether users notice or mind the repetition.** The pattern page found no study; these tests check phrases, not feelings.
- **Whether a mandated brand line is approved copy.** That belongs to the script's owner, not the model.
- **Whether a required AI disclosure applies.** The pattern page checked no specific law; check yours.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
